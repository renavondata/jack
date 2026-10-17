"""Differential harness (SPEC §9a): two checkers must agree, minus `detail`, on every log and each proper prefix of it."""
import argparse, glob, hashlib, json, os, pathlib, subprocess, sys, tempfile  # noqa: E401
sys.path.insert(0, ROOT := os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # for sim.gen, run as a script
from sim import gen  # noqa: E402
REASONS = ("malformed_json not_canonical schema bad_seq parent_mismatch genesis_misplaced no_proposer bad_key "
           "unknown_key proposer_mismatch no_power bad_signature").split()

def run(cmd, path, timeout=120):
    """The checker's verdict minus detail if it gave one (SPEC §9a.3), else what came instead (no "ok")."""
    try:
        r = subprocess.run([*cmd, path], capture_output=True, timeout=timeout)  # a duplicate member or NaN gives None:
        v = json.loads(r.stdout.decode("utf-8"), parse_constant=lambda c: None,  # a BOM or bad UTF-8 is a ValueError
                       object_pairs_hook=lambda kv: dict(kv) if len(dict(kv)) == len(kv) else None)
    except ValueError:
        v = None
    except (OSError, subprocess.SubprocessError) as x:  # a checker that cannot be run, or no output within the timeout
        return {"error": f"{type(x).__name__}: {x}"}
    good = type(v) is dict and type(v.get("ok")) is bool and r.returncode == (not v["ok"]) and (  # exit 0 iff ok
        set(v) == {"ok", "entries"} and type(v["entries"]) is int and v["entries"] >= 0 if v["ok"] else
        set(v) == {"ok", "seq", "reason", "detail"} and type(v["seq"]) is int and v["seq"] >= 0
        and v["reason"] in REASONS and type(v["detail"]) is str)
    return {k: x for k, x in v.items() if k != "detail"} if good else {"rc": r.returncode, "out": r.stdout.decode(errors="replace")[:400]}

def compare(cmd_a, cmd_b, logs, timeout=120, stats=None):
    """[(log, length, a, b)] for each disagreement (§9a.4) on a log, a path or a (seed, make) pair, or a proper prefix."""
    stats, bad = {"logs": 0, "prefixes": 0, "uncompared": []} if stats is None else stats, []
    for name, make in ((x, pathlib.Path(x).read_bytes) if isinstance(x, str) else x for x in logs):
        try:
            data = make()
        except Exception as x:  # an unreadable file or a generator defect: requested, but not compared
            stats["uncompared"].append(f"{name}: {type(x).__name__}: {x}")
            continue
        lines = data.removesuffix(b"\n").split(b"\n") if data else []  # SPEC §1: a final 0x0A is optional
        with tempfile.TemporaryDirectory() as tmp:
            for k in range(len(lines) + 1):  # each proper prefix, then the whole log, its bytes as they are
                (path := pathlib.Path(tmp, str(k))).write_bytes(b"".join(l + b"\n" for l in lines[:k]) if k < len(lines) else data)
                stats["prefixes" if k < len(lines) else "logs"] += 1
                bad += [] if (a := run(cmd_a, path, timeout)) == (b := run(cmd_b, path, timeout)) and "ok" in a else [(name, k, a, b)]
    return bad

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--a", default=f"{sys.executable} -E -s -m kernel.check", help="first checker command")
    ap.add_argument("--b", default="kernel2/check", help="second checker command")
    ap.add_argument("--seeds", type=int, default=0, help="also the logs of the first N seeds in sim/seeds.txt")
    ap.add_argument("--timeout", type=float, default=120, help="seconds per checker call")
    ap.add_argument("logs", nargs="*", help="log files or globs")
    a, stats = ap.parse_args(argv), {"logs": 0, "prefixes": 0, "uncompared": []}
    seeds = (raw := pathlib.Path(ROOT, "sim", "seeds.txt").read_bytes()).decode().splitlines()[:a.seeds]
    logs = [p for g in a.logs for p in sorted(glob.glob(g)) or [g]]
    requested, pool = len(logs) + a.seeds, gen.KeyPool(tempfile.mkdtemp(prefix="diff-keys-")) if seeds else None
    logs += [(s, lambda s=s: "".join(l + "\n" for l in gen.generate(s, pool).lines).encode()) for s in seeds]
    bad = compare(a.a.split(), a.b.split(), logs, a.timeout, stats)
    git = run(["git", "-C", ROOT, "rev-parse"], "HEAD")  # the commit of the working tree, or null if git cannot answer
    print(json.dumps(dict(stats, requested=requested, commit=git["out"].strip() if git.get("rc") == 0 else None, seeds_sha256=
                          hashlib.sha256(raw).hexdigest(), disagreements=[dict(zip("log length a b".split(), d)) for d in bad]), indent=1))
    return 1 if bad or stats["logs"] < requested else 0

if __name__ == "__main__":
    sys.exit(main())
