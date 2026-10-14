"""Run a tree's checker or judge as a black box (CLI contract, SPEC.md). Not kernel."""
import json
import os
import subprocess
import sys
import tempfile


def _json_or_crash(r):
    try:
        if r.returncode in (0, 1):
            return json.loads(r.stdout)
    except ValueError:
        pass
    return {"ok": False, "reason": "crash", "detail": r.stderr.decode(errors="replace")[-800:], "rc": r.returncode}


def check_with(root, lines, cmd=None):
    """Verdict of the checker rooted at `root` (default: python -m kernel.check) over `lines`."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "log.jsonl")
        with open(path, "w") as f:
            f.write("".join(l + "\n" for l in lines))
        argv = list(cmd or [sys.executable, "-E", "-s", "-m", "kernel.check"]) + [path]
        return _json_or_crash(subprocess.run(argv, cwd=root, capture_output=True))


def judge_with(root, repo, trunk, proposal):
    argv = [sys.executable, os.path.join(root, "judge", "judge.py"), "--repo", repo, "--trunk", trunk, "--proposal", proposal]
    return _json_or_crash(subprocess.run(argv, capture_output=True))
