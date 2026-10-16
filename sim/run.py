#!/usr/bin/env python3
"""Run the simulator over the committed seed list within a time budget; write a transcript.

Properties checked per case: oracle (the kernel's verdict equals the generator's
intent), prefix (every proper prefix of an accepted log is accepted),
sticky_refusal (appending any entry to a refused log leaves the verdict
identical), deterministic (a second check agrees with the first). Prefixes: of an accepted log, every
proper prefix (up to ten lines; beyond that, lengths 0, 1, n-1 and three more) is accepted; of a log
refused at seq s, every prefix of length 0..s is accepted (sampled the same way) and every longer
prefix (up to three) carries the same refusal. With --second CMD, agree: the second checker gives the
kernel's verdict on every input above, the whole log twice; that is how §9 criterion 2's entry-by-entry
agreement is tested. A verdict that is not exactly SPEC §9's contract (shape, types, reason code,
encoding, exit status), a crash or a timeout equals nothing.
"""
import argparse
import datetime
import json
import multiprocessing
import os
import hashlib
import random
import re
import shlex
import shutil
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
SECOND = None
TIMEOUT = 120.0  # seconds per second-checker call
REASONS = frozenset("malformed_json not_canonical schema bad_seq parent_mismatch genesis_misplaced no_proposer "
                    "bad_key unknown_key proposer_mismatch no_power bad_signature".split())  # SPEC §9, closed set
SEED = re.compile(r"[0-9a-f]{16}\Z")  # the committed seed format


def strip(v):
    return {k: x for k, x in v.items() if k != "detail"}


def _no_duplicates(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"duplicate member {k!r}")
        d[k] = v
    return d


def _no_constants(name):
    raise ValueError(f"{name} is not JSON")


def _utf8(s):
    try:
        s.encode("utf-8")
        return True
    except UnicodeEncodeError:  # a lone surrogate
        return False


def parse_verdict(stdout, rc):
    """SPEC §9's CLI contract, strictly: the verdict without detail, or {"malformed": why} which equals no verdict."""
    shown = stdout.decode(errors='replace')[:200]
    try:
        if stdout.startswith(b"\xef\xbb\xbf"):
            raise ValueError("byte-order mark")
        v = json.loads(stdout.decode("utf-8"), object_pairs_hook=_no_duplicates, parse_constant=_no_constants)
    except (ValueError, UnicodeDecodeError) as x:
        return {"malformed": f"not JSON: {x}", "stdout": shown}
    if not isinstance(v, dict) or not isinstance(v.get("ok"), bool):
        return {"malformed": "no boolean ok", "stdout": shown}
    if v["ok"]:
        good = set(v) == {"ok", "entries"} and type(v["entries"]) is int and v["entries"] >= 0 and rc == 0
    else:
        good = (set(v) == {"ok", "seq", "reason", "detail"} and type(v["seq"]) is int and v["seq"] >= 0
                and v["reason"] in REASONS and isinstance(v["detail"], str) and _utf8(v["detail"]) and rc == 1)
    return strip(v) if good else {"malformed": f"verdict {strip(v)} with exit {rc}", "stdout": shown}


def second_verdict(cmd, lines, timeout=None):
    """The second checker's verdict on these lines, written to a file as the CLI contract requires."""
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("".join(l + "\n" for l in lines))
        try:
            t = TIMEOUT if timeout is None else timeout
            r = subprocess.run(list(cmd) + [path], capture_output=True, timeout=t)
        except subprocess.TimeoutExpired:
            return {"malformed": f"timeout after {t}s"}
        except OSError as x:
            return {"malformed": f"cannot run: {x}"}
        if r.returncode not in (0, 1):
            return {"malformed": f"exit {r.returncode}", "stderr": r.stderr.decode(errors='replace')[:200]}
        return parse_verdict(r.stdout, r.returncode)
    finally:
        os.unlink(path)


def evaluate(case, pool, checker=check.check, second=None):
    """[(property, detail)] for every property that fails on this case."""
    failures = []

    def agree(lines, what, kernel_verdict):
        """The second checker on these lines must give the kernel's verdict; records the first disagreement."""
        if second and not any(f[0] == "agree" for f in failures):
            b = second_verdict(second, lines)
            if b != strip(kernel_verdict):
                failures.append(("agree", f"on {what}: kernel {strip(kernel_verdict)}, second {b}"))

    v = checker(case.lines)
    if strip(v) != case.expected:
        failures.append(("oracle", f"expected {case.expected}, got {strip(v)}"))
    agree(case.lines, "the log", v)
    agree(case.lines, "the log again", v)  # the second checker's own determinism
    if strip(checker(case.lines)) != strip(v):
        failures.append(("deterministic", "second check differs"))
    n = len(case.lines)
    rng = random.Random(case.seed or 0)
    accepted_to = n if v.get("ok") else v["seq"]  # every prefix of this length or less is a valid log
    lengths = range(accepted_to + 1) if accepted_to < 10 else sorted({0, 1, accepted_to, *rng.sample(range(accepted_to + 1), 3)})
    for k in lengths:
        if k == n:
            continue  # the whole log, already compared
        p = checker(case.lines[:k])
        agree(case.lines[:k], f"the prefix of length {k}", p)
        if not p.get("ok"):
            failures.append(("prefix", f"prefix of length {k} refused: {strip(p)}"))
            break
    if not v.get("ok"):
        longer = range(accepted_to + 1, n)
        for k in (longer if len(longer) <= 3 else sorted(rng.sample(longer, 3))):
            p = checker(case.lines[:k])
            agree(case.lines[:k], f"the prefix of length {k}", p)
            if strip(p) != strip(v):
                failures.append(("sticky_refusal", f"prefix of length {k} gives {strip(p)}"))
                break
        extra = build.make_entry(n, log.line_hash(case.lines[-1]), "proposal", "ann", proposal("x"), pool.ann)
        w = checker(case.lines + [extra])
        agree(case.lines + [extra], "the log with one entry appended", w)
        if strip(w) != strip(v):
            failures.append(("sticky_refusal", f"after appending: {strip(w)}"))
    return failures


def _init(second=None, timeout=None):
    global POOL, SECOND, TIMEOUT
    SECOND, TIMEOUT = second, TIMEOUT if timeout is None else timeout
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


def positive(kind):
    def convert(s):
        x = kind(s)
        if x <= 0:
            raise argparse.ArgumentTypeError(f"must be positive: {s}")
        return x
    return convert


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default=os.path.join(os.path.dirname(__file__), "seeds.txt"))
    ap.add_argument("--budget", type=float, default=600, help="seconds")
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--limit", type=positive(int), default=None, help="at most this many seeds")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "runs"))
    ap.add_argument("--second", default=None, help="second checker command, e.g. kernel2/check")
    ap.add_argument("--complete", action="store_true",
                    help="fail unless every selected seed (after --limit) completed, so a run the budget cuts short "
                         "fails; refuse to start on an empty, duplicated, malformed or too-short seed list")
    ap.add_argument("--second-timeout", type=positive(float), default=TIMEOUT, help="seconds per second-checker call")
    ap.add_argument("--quiet", action="store_true", help="no progress line on stderr")
    a = ap.parse_args(argv)
    second = shlex.split(a.second) if a.second else None
    if second:  # build once, before the workers race to build it, and check the CLI contract on the empty log
        warm = second_verdict(second, [], timeout=a.second_timeout)
        if warm != {"ok": True, "entries": 0}:
            print(f"second checker fails the contract on the empty log: {warm}")
            return 2
    with open(a.seeds, "rb") as f:
        raw = f.read()
    seeds_sha256 = hashlib.sha256(raw).hexdigest()
    all_seeds = [l.strip() for l in raw.decode().splitlines() if l.strip()]
    seeds = all_seeds[:a.limit]
    if a.complete:
        why = ("no seeds" if not seeds else "duplicate seeds" if len(set(all_seeds)) != len(all_seeds)
               else "a seed is not 16 lowercase hex digits" if not all(SEED.match(s) for s in all_seeds)
               else f"{len(all_seeds)} seeds, fewer than --limit {a.limit}" if a.limit and len(all_seeds) < a.limit else None)
        if why:
            print(f"refusing to start: {why}")
            return 2
    started, t0 = datetime.datetime.now(datetime.timezone.utc), time.monotonic()
    done, by_kind, failures = [], {}, []
    shown, tty = 0.0, sys.stderr.isatty()
    with multiprocessing.Pool(a.jobs, initializer=_init, initargs=(second, a.second_timeout)) as pool:
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
    def git(*x):
        r = subprocess.run(["git", "-C", root, *x], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    commit, status = git("rev-parse", "HEAD"), git("status", "--porcelain", "--untracked-files=no")
    exe = shutil.which(second[0]) if second else None
    second_sha256 = None
    if exe and os.path.isfile(exe):
        with open(exe, "rb") as f:
            second_sha256 = hashlib.sha256(f.read()).hexdigest()
    transcript = {"started": started.isoformat(), "elapsed_s": round(elapsed, 1), "budget_s": a.budget, "jobs": a.jobs,
                  "seeds_file": os.path.relpath(a.seeds), "seeds_sha256": seeds_sha256, "seeds_selected": len(seeds),
                  "seeds_run": len(done), "complete": len(done) == len(seeds),
                  "seeds": [done[0], done[-1]] if done else [], "by_kind": dict(sorted(by_kind.items())),
                  "properties": list(PROPERTIES) + (["agree"] if second else []), "second": a.second,
                  "second_timeout_s": a.second_timeout if second else None, "second_path": exe, "second_sha256": second_sha256,
                  "limit": a.limit, "complete_required": a.complete,
                  "commit": commit, "dirty": None if status is None else bool(status),
                  "failures": failures,
                  "python": sys.version.split()[0], "openssh": ssh}
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{started.strftime('%Y%m%dT%H%M%SZ')}-{len(done)}.json")
    with open(path, "w") as f:
        json.dump(transcript, f, indent=1)
    print(f"{len(done)} seeds in {elapsed:.1f}s, {len(failures)} property failures → {path}")
    if a.complete and len(done) < len(seeds):
        print(f"incomplete: {len(done)} of {len(seeds)} seeds within the {a.budget:.0f}s budget")
        return 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
