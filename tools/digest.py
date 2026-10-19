#!/usr/bin/env python3
"""Trusted-base digest of the working tree: sha256 over path\\0content\\0 for kernel/, kernel2/, judge/,
.github/workflows/ and SPEC.md, sorted by path — the same function judge.py computes from git. A tree whose trusted
base holds a symbolic link or a submodule is not digested (SPEC §10.1): it is named, and the tool exits 2."""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from judge.judge import REGULAR, TRUSTED, is_under  # noqa: E402


class NotRegular(Exception):
    """The trusted base holds objects that are not regular files; the message names them."""


def working_tree_files():
    """Tracked trusted-base files only, as the judge sees them (build output such as kernel2/.cache is not law);
    NotRegular if any is a symbolic link or a submodule (git modes 120000, 160000)."""
    tracked = subprocess.run(["git", "-C", ROOT, "ls-files", "-s", "-z"], capture_output=True, check=True).stdout
    entries = [(meta.split()[0], p) for meta, p in (e.split("\t", 1) for e in tracked.decode().split("\0") if e)
               if is_under(p, TRUSTED)]
    foreign = sorted(p for mode, p in entries if mode not in REGULAR)
    if foreign:
        raise NotRegular(", ".join(foreign))
    return sorted(p for _, p in entries)


def digest():
    h = hashlib.sha256()
    for rel in working_tree_files():
        with open(os.path.join(ROOT, rel), "rb") as f:
            h.update(rel.encode() + b"\0" + f.read() + b"\0")
    return h.hexdigest()


def main():
    try:
        print(digest())
    except NotRegular as x:
        print(f"not regular files in the trusted base, not digested: {x}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
