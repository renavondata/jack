#!/usr/bin/env python3
"""Trusted-base digest of the working tree: sha256 over path\\0content\\0 for kernel/, kernel2/, judge/,
.github/workflows/ and SPEC.md, sorted by path — the same function judge.py computes from git."""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from judge.judge import TRUSTED, is_under  # noqa: E402


def working_tree_files():
    """Tracked trusted-base files only, as the judge sees them (build output such as kernel2/.cache is not law)."""
    tracked = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"], capture_output=True, check=True).stdout
    return sorted(p for p in tracked.decode().split("\0") if p and is_under(p, TRUSTED))


def digest():
    h = hashlib.sha256()
    for rel in working_tree_files():
        with open(os.path.join(ROOT, rel), "rb") as f:
            h.update(rel.encode() + b"\0" + f.read() + b"\0")
    return h.hexdigest()


if __name__ == "__main__":
    print(digest())
