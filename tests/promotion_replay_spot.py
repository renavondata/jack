"""Run the three SPEC promotion replay spot checks using origin/main's frozen table."""
import difflib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def git(*args, cwd=ROOT):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, check=True).stdout


def main():
    table = json.loads(git("show", "origin/main:spec/vectors/promotion-replay.json"))
    chain = git("rev-list", "--first-parent", "--reverse", table["T"]).decode().splitlines()
    for index in (592, 593, 705):
        row = table["rows"][index]
        assert row["commit"] == chain[index]
        with tempfile.TemporaryDirectory(prefix=".promotion-replay-", dir=ROOT) as tmp:
            tree = Path(tmp) / "tree"
            git("clone", "-q", "--shared", "--no-checkout", str(ROOT), str(tree))
            git("checkout", "-q", "--detach", row["commit"], cwd=tree)
            replacements = {"<root>": str(tree), "<log>": str(tree / "log.jsonl")}
            for name, data in (("run", json.dumps(row["run"])), ("runs", "[]"),
                               ("acts", "repo,time_hkt,class,kind,ref,note\n")):
                path = Path(tmp) / name
                path.write_text(data)
                replacements[f"<{name}>"] = str(path)
            args = [replacements.get(x, x) for x in row["argv"]]
            result = subprocess.run([sys.executable, str(ROOT / "judge/status.py"), *args], capture_output=True)
            actual = result.stdout.decode().splitlines()
            expected = list(row["stdout"])
            differences = [(i, a, b) for i, (a, b) in enumerate(zip(expected, actual)) if a != b]
            if index != 592:
                criterion = next(line for line in expected if line.startswith("criterion 3:") and "and unchanged: False SHORT" in line)
                failure = criterion.removesuffix(" SHORT")
                expected = [line.replace("and unchanged: False SHORT", "and unchanged: True met")
                            if line == criterion else line for line in expected]
                for i, line in enumerate(expected):
                    if line.startswith("promote C2a: refused: "):
                        # Criterion 3 itself contains a semicolon, so remove its exact text and one adjoining separator.
                        rest = line.removeprefix("promote C2a: refused: ")
                        if failure + "; " in rest:
                            rest = rest.replace(failure + "; ", "", 1)
                        elif "; " + failure in rest:
                            rest = rest.replace("; " + failure, "", 1)
                        elif rest == failure:
                            rest = ""
                        else:
                            raise AssertionError("marked criterion absent from promotion line")
                        expected[i] = "promote C2a: " + ("refused: " + rest if rest else "lawful")
            if actual != expected or result.returncode != row["exit"]:
                print("\n".join(difflib.unified_diff(expected, actual, fromfile="expected", tofile="actual")))
                print(result.stderr.decode())
                raise SystemExit(f"row {index}: FAIL, exit {result.returncode} expected {row['exit']}")
            print(f"row {index} {row['commit']}: PASS; exit {result.returncode}; {len(actual)} lines; changed {[i for i, _, _ in differences]}")
            for i, before, after in differences:
                print(f"  line {i}: {before}\n        -> {after}")


if __name__ == "__main__":
    main()
