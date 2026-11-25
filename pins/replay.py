"""SPEC's frozen replay samples and accepted evaluator bytes, using runner history."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]
PARENT = "2d99d2427296df1174a55f41459058d5f6b65a8f"
STATUS_SHA = "44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0"
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
    raw = git("show", "HEAD:spec/vectors/promotion-replay-c2a-3.json")
    assert hashlib.sha256(raw).hexdigest() == "943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77"
    third = json.loads(raw)
    rows = [(table["rows"][i], i, marked(table["rows"][i]["stdout"]) if i >= 593 else table["rows"][i]["stdout"])
            for i in (300, 400, 593)]
    rows += [(third["rows"][i], i, third["rows"][i]["marked" if i == 735 else "stdout"]) for i in (734, 735)]
    for source, indexes in ((table, (300, 400, 593)), (third, (734, 735))):
        chain = git("rev-list", "--first-parent", "--reverse", source["T"]).decode().splitlines()
        assert all(source["rows"][i]["commit"] == chain[i] for i in indexes)
    with tempfile.TemporaryDirectory(prefix="promotion-replay-") as tmp:
        tmp = Path(tmp)
        tree = tmp / "tree"
        git("clone", "-q", "--shared", "--no-checkout", str(SOURCE), str(tree))
        for row, index, lines in rows:
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
            expected = ("\n".join(lines) + ("\n" if lines else "")).encode()
            assert result.returncode == row["exit"], (index, result.returncode, result.stderr)
            assert result.stdout == expected, f"row {index}: output drift\n{result.stdout.decode()}"
    # Output mutants must die above; a no-output edit can only die at this check.
    assert hashlib.sha256((Path(root) / "judge/status.py").read_bytes()).hexdigest() == STATUS_SHA, "status: accepted bytes differ"
    frozen = git("show", f"{PARENT}:tools/value.py")
    assert hashlib.sha256(frozen).hexdigest() == "11440c89429513b49922658d419b0bc6c8e625b15701b335576eedf537cf9992", "move parent: value bytes"
    old, new = b"from tools.entry import now, read_log, resolution_rates", b"from judge.entries import now, read_log, resolution_rates"
    assert frozen.count(old) == 1
    assert (Path(root) / "judge/value.py").read_bytes() == frozen.replace(old, new), "value: moved bytes differ"
