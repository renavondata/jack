"""Count the kernel's physical lines (CHARTER §9 criterion 3); never hide an excess."""
import argparse
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1000)
    args = ap.parse_args()
    counts = []
    for path in sorted(glob.glob(os.path.join(ROOT, "kernel", "*.py"))):
        with open(path, "rb") as f:
            counts.append((os.path.relpath(path, ROOT), sum(1 for _ in f)))
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
