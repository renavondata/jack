"""Differential harness: two checkers over the same logs must agree, verdict by verdict (§6, §9 criterion 2)."""
import argparse
import glob
import json
import os
import subprocess
import sys


def strip(v):
    return {k: x for k, x in v.items() if k != "detail"}


def run(cmd, path):
    r = subprocess.run(list(cmd) + [path], capture_output=True)
    if r.returncode not in (0, 1):
        return {"ok": False, "reason": "crash", "rc": r.returncode}
    try:
        return strip(json.loads(r.stdout))
    except ValueError:
        return {"ok": False, "reason": "crash", "stdout": r.stdout.decode(errors="replace")[:200]}


def compare(cmd_a, cmd_b, paths):
    """[(path, verdict_a, verdict_b)] for every log on which the two checkers disagree."""
    out = []
    for p in paths:
        a, b = run(cmd_a, p), run(cmd_b, p)
        if a != b:
            out.append((p, a, b))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--a", default=f"{sys.executable} -E -s -m kernel.check", help="first checker command")
    ap.add_argument("--b", default="kernel2/check", help="second checker command")
    ap.add_argument("logs", nargs="+", help="log files or globs")
    a = ap.parse_args(argv)
    paths = sorted(p for g in a.logs for p in glob.glob(g))
    bad = compare(a.a.split(), a.b.split(), paths)
    for p, va, vb in bad:
        print(f"DISAGREE {p}\n  a: {json.dumps(va, sort_keys=True)}\n  b: {json.dumps(vb, sort_keys=True)}")
    print(f"{len(paths)} logs, {len(bad)} disagreements")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
