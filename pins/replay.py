"""SPEC's frozen replay samples and exact permitted move, using the runner's history."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]
PARENT = "2d99d2427296df1174a55f41459058d5f6b65a8f"
HASHES = {"status": "b255520996cef0ec20691c46cbc236ce5826dc166d16697762fa85f30fe86acb",
          "value": "11440c89429513b49922658d419b0bc6c8e625b15701b335576eedf537cf9992"}
WALK = b'git_bytes(root, "rev-list", f"{start}..{rev}")'
FIRST_PARENT = b'git_bytes(root, "rev-list", "--first-parent", f"{start}..{rev}")'


def git(*args, cwd=SOURCE):
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True).stdout


def marked(lines):
    """Only the two lines marked by the grant, preserving every other byte."""
    criterion, = [s for s in lines if s.startswith("criterion 3:") and "and unchanged: False SHORT" in s]
    failure = criterion.removesuffix(" SHORT")
    expected = [s.replace("False SHORT", "True met") if s == criterion else s for s in lines]
    for i, line in enumerate(expected):
        if line.startswith("promote C2a: refused: "):
            rest = line.removeprefix("promote C2a: refused: ")
            if failure + "; " in rest:
                rest = rest.replace(failure + "; ", "", 1)
            elif "; " + failure in rest:
                rest = rest.replace("; " + failure, "", 1)
            else:
                assert rest == failure, line
                rest = ""
            expected[i] = "promote C2a: " + ("refused: " + rest if rest else "lawful")
    return expected


def replay_drift(root):
    raw = git("show", "HEAD:spec/vectors/promotion-replay.json")
    assert hashlib.sha256(raw).hexdigest() == "6d647d09b0e02f0b3e1ac785bdf8e13fa223491501d6a24a1886783b9458c4dd"
    table = json.loads(raw)
    chain = git("rev-list", "--first-parent", "--reverse", table["T"]).decode().splitlines()
    with tempfile.TemporaryDirectory(prefix="promotion-replay-") as tmp:
        tmp = Path(tmp)
        tree = tmp / "tree"
        git("clone", "-q", "--shared", "--no-checkout", str(SOURCE), str(tree))
        for index in (300, 400, 593):
            row = table["rows"][index]
            assert row["commit"] == chain[index]
            git("update-ref", "--no-deref", "HEAD", row["commit"], cwd=tree)
            (tmp / "log").write_bytes(git("show", row["commit"] + ":log.jsonl"))
            files = {"log": None, "run": json.dumps(row["run"]), "runs": "[]",
                     "acts": "repo,time_hkt,class,kind,ref,note\n"}
            replacements = {"<root>": str(tree)}
            for name, data in files.items():
                if data is not None:
                    (tmp / name).write_text(data)
                replacements[f"<{name}>"] = str(tmp / name)
            result = subprocess.run([sys.executable, "-E", "-s", str(Path(root) / "judge/status.py"),
                                     *(replacements.get(a, a) for a in row["argv"])],
                                    cwd=root, capture_output=True)
            lines = marked(row["stdout"]) if index >= 593 else row["stdout"]
            expected = ("\n".join(lines) + ("\n" if lines else "")).encode()
            assert result.returncode == row["exit"], (index, result.returncode, result.stderr)
            assert result.stdout == expected, f"row {index}: output drift\n{result.stdout.decode()}"
    # Output mutants must die above; a no-output edit can only die at this check.
    for name, sha in HASHES.items():
        frozen = git("show", f"{PARENT}:tools/{name}.py")
        assert hashlib.sha256(frozen).hexdigest() == sha, f"move parent: {name} bytes"
        if name == "status":
            old, new = b"from tools import value as val", b"from judge import value as val"
            assert frozen.count(WALK) == 1
            moved = frozen.replace(WALK, FIRST_PARENT)
        else:
            old, new = b"from tools.entry import now, read_log, resolution_rates", b"from judge.entries import now, read_log, resolution_rates"
            moved = frozen
        assert frozen.count(old) == 1
        assert (Path(root) / f"judge/{name}.py").read_bytes() == moved.replace(old, new), f"{name}: moved bytes differ"
