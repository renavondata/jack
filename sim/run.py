#!/usr/bin/env python3
"""Run the simulator over the committed seed list within a time budget; write a transcript.

Properties checked per case: oracle (the kernel's verdict equals the generator's
intent), prefix (every proper prefix of an accepted log is accepted),
sticky_refusal (appending any entry to a refused log leaves the verdict
identical), deterministic (a second check agrees with the first).
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
from harness import build  # noqa: E402
from harness.build import proposal  # noqa: E402
from kernel import check, log  # noqa: E402
from sim import gen  # noqa: E402

PROPERTIES = ("oracle", "prefix", "sticky_refusal", "deterministic")
POOL = None


def strip(v):
    return {k: x for k, x in v.items() if k != "detail"}


def evaluate(case, pool, checker=check.check):
    """[(property, detail)] for every property that fails on this case."""
    failures = []
    v = checker(case.lines)
    if strip(v) != case.expected:
        failures.append(("oracle", f"expected {case.expected}, got {strip(v)}"))
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
        if (w.get("seq"), w.get("rule"), w.get("reason")) != (v.get("seq"), v.get("rule"), v.get("reason")):
            failures.append(("sticky_refusal", f"after appending: {strip(w)}"))
    return failures


def _init():
    global POOL
    POOL = gen.KeyPool(tempfile.mkdtemp(prefix="sim-"))


def _one(seed):
    try:
        case = gen.generate(seed, POOL)
        return seed, case.kind, evaluate(case, POOL)
    except Exception as x:  # a generator defect is a finding, recorded against its seed, never a dead run
        return seed, "error", [("generator", f"{type(x).__name__}: {x}")]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default=os.path.join(os.path.dirname(__file__), "seeds.txt"))
    ap.add_argument("--budget", type=float, default=600, help="seconds")
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--limit", type=int, default=None, help="at most this many seeds")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "runs"))
    a = ap.parse_args(argv)
    with open(a.seeds) as f:
        seeds = [l.strip() for l in f if l.strip()][:a.limit]
    started, t0 = datetime.datetime.now(datetime.timezone.utc), time.monotonic()
    done, by_kind, failures = [], {}, []
    with multiprocessing.Pool(a.jobs, initializer=_init) as pool:
        for seed, kind, bad in pool.imap(_one, seeds, chunksize=1):
            done.append(seed)
            by_kind[kind] = by_kind.get(kind, 0) + 1
            failures += [(seed, kind, prop, detail) for prop, detail in bad]
            if time.monotonic() - t0 > a.budget:
                break
        pool.terminate()
    elapsed = time.monotonic() - t0
    ssh = subprocess.run(["ssh", "-V"], capture_output=True, text=True).stderr.strip()
    transcript = {"started": started.isoformat(), "elapsed_s": round(elapsed, 1), "budget_s": a.budget, "jobs": a.jobs,
                  "seeds_file": os.path.relpath(a.seeds), "seeds_run": len(done),
                  "seeds": [done[0], done[-1]] if done else [], "by_kind": dict(sorted(by_kind.items())),
                  "properties": list(PROPERTIES), "failures": failures,
                  "python": sys.version.split()[0], "openssh": ssh}
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{started.strftime('%Y%m%dT%H%M%SZ')}-{len(done)}.json")
    with open(path, "w") as f:
        json.dump(transcript, f, indent=1)
    print(f"{len(done)} seeds in {elapsed:.1f}s, {len(failures)} property failures → {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
