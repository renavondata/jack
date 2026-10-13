#!/usr/bin/env python3
"""Pin runner (CHARTER §9): each mutant is a text edit applied to a disposable copy of the tree.

A mutant is KILLED when the pin's test fails on the mutated copy and passes on
an unedited copy (the twin). A find string that does not occur exactly once is
STALE; a test that fails on the twin is TWIN FAILED; a target that does not
exist yet (the second checker) is PENDING. A pin that cannot fail is a defect,
so SURVIVED, STALE and TWIN FAILED fail the run; PENDING does not pass.
"""
import argparse
import os
import shutil
import sys
import tempfile
import traceback
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pins import pins  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Result = namedtuple("Result", "pin mutant status detail")
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "transcripts", "runs", "*.pyc")


def disposable_copy(root, into):
    dest = os.path.join(into, "tree")
    shutil.copytree(root, dest, ignore=IGNORE)
    return dest


def apply_mutant(copy, m):
    path = os.path.join(copy, m.path)
    if not os.path.exists(path):
        return "PENDING"
    with open(path) as f:
        text = f.read()
    if text.count(m.find) != 1:
        return "STALE"
    with open(path, "w") as f:
        f.write(text.replace(m.find, m.replace))
    return "ok"


def run_test(pin, root):
    try:
        pin.test(root)
        return True, ""
    except Exception:  # any failure under a mutant is detection; on the twin it is a defect
        return False, traceback.format_exc(limit=2).strip().splitlines()[-1]


def run_pins(pin_list, root):
    results = []
    for pin in pin_list:
        if any(not os.path.exists(os.path.join(root, m.path)) for m in pin.mutants):
            results += [Result(pin.name, m.name, "PENDING", f"{m.path} does not exist yet") for m in pin.mutants]
            continue
        with tempfile.TemporaryDirectory() as tmp:
            passed, detail = run_test(pin, disposable_copy(root, tmp))
        if not passed:
            results.append(Result(pin.name, "twin", "TWIN FAILED", detail))
            continue
        for m in pin.mutants:
            with tempfile.TemporaryDirectory() as tmp:
                copy = disposable_copy(root, tmp)
                status = apply_mutant(copy, m)
                if status != "ok":
                    results.append(Result(pin.name, m.name, status, m.find[:60]))
                    continue
                passed, detail = run_test(pin, copy)
            results.append(Result(pin.name, m.name, "SURVIVED" if passed else "KILLED", detail))
    return results


def exit_code(results):
    return 1 if any(r.status in ("SURVIVED", "STALE", "TWIN FAILED") for r in results) else 0


def table(results):
    width = max(len(r.pin) for r in results) + 2
    lines = [f"{'pin':{width}} {'mutant':28} status" + "\n" + "-" * (width + 40)]
    lines += [f"{r.pin:{width}} {r.mutant:28} {r.status}" + (f"  ({r.detail[:110]})" if r.detail else "")
              for r in results]
    counts = {s: sum(1 for r in results if r.status == s) for s in ("KILLED", "SURVIVED", "STALE", "TWIN FAILED", "PENDING")}
    lines.append("\n" + ", ".join(f"{k} {v}" for k, v in counts.items()))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--transcript", help="also write the table to this path")
    ap.add_argument("--only", nargs="*", help="run only these pins")
    a = ap.parse_args(argv)
    selected = [p for p in pins.PINS if not a.only or p.name in a.only]
    results = run_pins(selected, ROOT)
    text = table(results)
    print(text)
    if a.transcript:
        os.makedirs(os.path.dirname(a.transcript) or ".", exist_ok=True)
        with open(a.transcript, "w") as f:
            f.write(text + "\n")
    return exit_code(results)


if __name__ == "__main__":
    sys.exit(main())
