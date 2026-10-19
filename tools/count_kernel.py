"""Count the kernel's physical lines (CHARTER §9 criterion 3); never hide an excess."""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def is_python(path):
    """A .py file, or one whose first line is a #! line naming python: what judge/judge.py counts (SPEC §10.10)."""
    with open(path, "rb") as f:
        first = f.readline().rstrip(b"\n")
    return path.endswith(".py") or (first.startswith(b"#!") and b"python" in first)


def lines(path):
    with open(path, "rb") as f:
        return sum(1 for _ in f)


def regular_files(top):
    """Every regular file under `top`, nested ones too, sorted; a symbolic link is neither followed nor listed."""
    walk = os.walk(top)  # followlinks=False: a link to a directory is not entered
    return sorted(p for d, _, names in walk for p in (os.path.join(d, n) for n in names)
                  if os.path.isfile(p) and not os.path.islink(p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1000)
    args = ap.parse_args()
    counts = []
    for path in (p for p in regular_files(os.path.join(ROOT, "kernel")) if is_python(p)):
        counts.append((os.path.relpath(path, ROOT), lines(path)))
    for rel, n in counts:
        print(f"{rel:24} {n:6}")
    total = sum(n for _, n in counts)
    print(f"{'total':24} {total:6}")
    if total > args.limit:
        print(f"EXCESS: kernel is {total} lines, limit {args.limit}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
