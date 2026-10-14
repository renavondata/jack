#!/usr/bin/env python3
"""Run the simulator over the committed seed list within a time budget; write a transcript.

Properties checked per case: oracle (the kernel's verdict equals the generator's
intent), prefix (every proper prefix of an accepted log is accepted),
sticky_refusal (appending any entry to a refused log leaves the verdict
identical), deterministic (a second check agrees with the first); with --second CMD, agree (the second
checker's verdict on the log equals the kernel's, as harness/diff.py compares them; §9 criterion 2).
"""
import argparse
import datetime
import json
import multiprocessing
import os
import random
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import build, diff  # noqa: E402
from harness.build import proposal  # noqa: E402
from kernel import check, log  # noqa: E402
from sim import gen  # noqa: E402

PROPERTIES = ("oracle", "prefix", "sticky_refusal", "deterministic")
POOL = None
SECOND = None


def strip(v):
    return {k: x for k, x in v.items() if k != "detail"}


def second_verdict(cmd, lines):
    """The second checker's verdict on these lines, run on a file exactly as harness/diff.py runs it."""
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("".join(l + "\n" for l in lines))
        return diff.run(cmd, path)
    finally:
        os.unlink(path)


def evaluate(case, pool, checker=check.check, second=None):
    """[(property, detail)] for every property that fails on this case."""
    failures = []
    v = checker(case.lines)
    if strip(v) != case.expected:
        failures.append(("oracle", f"expected {case.expected}, got {strip(v)}"))
    if second:
        b = second_verdict(second, case.lines)
        if b != strip(v):
            failures.append(("agree", f"kernel {strip(v)}, second {b}"))
    if strip(checker(case.lines)) != strip(v):
        failures.append(("deterministic", "second check differs"))
    if v.get("ok"):
        n = len(case.lines)
        cuts = range(n) if n <= 10 else random.Random(case.seed or 0).sample(range(n), 3)
        for k in cuts:
            if not checker(case.lines[:k]).get("ok"):
                failures.append(("prefix", f"prefix of length {k} refused"))
                break
    else:
        extra = build.make_entry(len(case.lines), log.line_hash(case.lines[-1]), "proposal", "ann", proposal("x"), pool.ann)
        w = checker(case.lines + [extra])
        if (w.get("seq"), w.get("reason")) != (v.get("seq"), v.get("reason")):
            failures.append(("sticky_refusal", f"after appending: {strip(w)}"))
    return failures


def _init(second=None):
    global POOL, SECOND
    SECOND = second
    POOL = gen.KeyPool(tempfile.mkdtemp(prefix="sim-"))


def _one(seed):
    try:
        case = gen.generate(seed, POOL)
        return seed, case.kind, evaluate(case, POOL, second=SECOND)
    except Exception as x:  # a generator defect is a finding, recorded against its seed, never a dead run
        return seed, "error", [("generator", f"{type(x).__name__}: {x}")]


def progress(n, total, elapsed, budget, failures):
    """One status line: seeds done, rate, and when the run ends (seeds exhausted or budget, whichever first)."""
    rate = n / elapsed if elapsed else 0.0
    left = min((total - n) / rate if rate else budget, budget - elapsed)
    return (f"{n}/{total} seeds ({100 * n / total:.1f}%), {rate:.0f}/s, {failures} failures, "
            f"{elapsed / 60:.1f}m elapsed, ~{max(left, 0) / 60:.1f}m left  ")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default=os.path.join(os.path.dirname(__file__), "seeds.txt"))
    ap.add_argument("--budget", type=float, default=600, help="seconds")
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--limit", type=int, default=None, help="at most this many seeds")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "runs"))
    ap.add_argument("--second", default=None, help="second checker command, e.g. kernel2/check")
    ap.add_argument("--quiet", action="store_true", help="no progress line on stderr")
    a = ap.parse_args(argv)
    second = a.second.split() if a.second else None
    if second:  # build once, before the workers race to build it
        diff.run(second, os.devnull)
    with open(a.seeds) as f:
        seeds = [l.strip() for l in f if l.strip()][:a.limit]
    started, t0 = datetime.datetime.now(datetime.timezone.utc), time.monotonic()
    done, by_kind, failures = [], {}, []
    shown, tty = 0.0, sys.stderr.isatty()
    with multiprocessing.Pool(a.jobs, initializer=_init, initargs=(second,)) as pool:
        for seed, kind, bad in pool.imap(_one, seeds, chunksize=1):
            done.append(seed)
            by_kind[kind] = by_kind.get(kind, 0) + 1
            failures += [(seed, kind, prop, detail) for prop, detail in bad]
            now = time.monotonic()
            if not a.quiet and (now - shown >= (1 if tty else 30) or len(done) == len(seeds)):
                shown = now
                print(progress(len(done), len(seeds), now - t0, a.budget, len(failures)),
                      end="\r" if tty else "\n", file=sys.stderr, flush=True)
            if now - t0 > a.budget:
                break
        pool.terminate()
    if tty and not a.quiet:
        print(file=sys.stderr)
    elapsed = time.monotonic() - t0
    ssh = subprocess.run(["ssh", "-V"], capture_output=True, text=True).stderr.strip()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git = lambda *x: subprocess.run(["git", "-C", root, *x], capture_output=True, text=True).stdout.strip()  # noqa: E731
    transcript = {"started": started.isoformat(), "elapsed_s": round(elapsed, 1), "budget_s": a.budget, "jobs": a.jobs,
                  "seeds_file": os.path.relpath(a.seeds), "seeds_run": len(done),
                  "seeds": [done[0], done[-1]] if done else [], "by_kind": dict(sorted(by_kind.items())),
                  "properties": list(PROPERTIES) + (["agree"] if second else []), "second": a.second,
                  "commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain", "--untracked-files=no")),
                  "failures": failures,
                  "python": sys.version.split()[0], "openssh": ssh}
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{started.strftime('%Y%m%dT%H%M%SZ')}-{len(done)}.json")
    with open(path, "w") as f:
        json.dump(transcript, f, indent=1)
    print(f"{len(done)} seeds in {elapsed:.1f}s, {len(failures)} property failures → {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
