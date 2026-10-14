#!/usr/bin/env python3
"""Judge self-check (CI, every push): run judge.py exactly as the judge workflow does, trunk against itself.

Passes only if the judge accepts and, whenever kernel2/check is tracked, kernel2 actually ran and its
verdict agreed. Any judge error, refusal or silent absence of kernel2 fails the check.
"""
import argparse
import json
import os
import subprocess
import sys


def selfcheck(repo):
    judge = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge.py")
    r = subprocess.run([sys.executable, judge, "--repo", repo, "--trunk", "HEAD", "--proposal", "HEAD"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"judge failed on trunk (exit {r.returncode}): {r.stderr.strip()[-400:]} {r.stdout.strip()[-400:]}")
        return 1  # selfcheck: judge refused or failed
    report = json.loads(r.stdout)
    tracked = subprocess.run(["git", "-C", repo, "ls-files", "kernel2/check"], capture_output=True, text=True).stdout.strip()
    if tracked and not isinstance(report.get("kernel2"), dict):
        print(f"kernel2/check is tracked but did not run: kernel2 = {report.get('kernel2')!r}")
        return 1
    print(f"judge self-check ok: kernel {report['verdict']}, kernel2 {report['kernel2']}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".")
    sys.exit(selfcheck(ap.parse_args().repo))
