#!/usr/bin/env python3
"""Trusted-base digest of the working tree: sha256 over path\\0content\\0 for kernel/, kernel2/, judge/,
.github/workflows/ and SPEC.md, sorted by path — the same function judge.py computes from git."""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from judge.judge import TRUSTED, is_under  # noqa: E402


def working_tree_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
            if is_under(rel, TRUSTED) and not name.endswith(".pyc"):
                out.append(rel)
    return sorted(out)


def digest():
    h = hashlib.sha256()
    for rel in working_tree_files():
        with open(os.path.join(ROOT, rel), "rb") as f:
            h.update(rel.encode() + b"\0" + f.read() + b"\0")
    return h.hexdigest()


if __name__ == "__main__":
    print(digest())
