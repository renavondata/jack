#!/usr/bin/env python3
"""Prepare an entry on a log's current head, then assemble its SSH signature into a line the kernel admits; the bodies of
jack forecast and jack resolve, and jack score's tables (RUNBOOK.md). Generates no key. Not kernel.
"""
import argparse
import datetime
import decimal
import fractions
import hashlib
import json
import math
import os
import re
import shlex
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from harness.keys import dearmour  # noqa: E402
from kernel import check, log  # noqa: E402

LOG = os.path.join(ROOT, "log.jsonl")


class Usage(Exception):
    """Exit 2: nothing written."""


def read_log(path):
    with open(path, "rb") as f:
        return check.read_lines(f.read())


def unsigned(a):
    """The canonical message (§2) on the head of a.log, or Usage."""
    lines = read_log(a.log)
    if not lines:
        raise Usage(f"{a.log} is empty: genesis is tools/genesis.py's job")
    if not log.instant(a.ts):
        raise Usage("--ts must be an instant like 2026-10-14T09:00:00Z (SPEC §4)")
    try:
        body = json.loads(a.body_json)
    except ValueError as x:
        raise Usage(f"--body-json is not JSON: {x}") from None
    if not isinstance(body, dict):
        raise Usage("--body-json must be a JSON object")
    entry = dict(seq=len(lines), parent=log.line_hash(lines[-1]), ts=a.ts, type=a.type, proposer=a.proposer, body=body)
    try:
        message = log.canonical(entry)
        log.check_shape(dict(log.parse_line(message), sig="AAAA"))
        log.check_body(a.type, body)
    except log.Refuse as x:
        raise Usage(f"the entry is refused before signing: {x.reason} {x.detail}") from None
    return message


def prepare(a):
    message = unsigned(a)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(message)
    sign = shlex.join(["ssh-keygen", "-Y", "sign", "-f", re.sub(r"\.pub$", "", a.pubkey), "-n", "core-entry", a.out])
    log_args = [] if a.log == LOG else ["--log", a.log]
    assemble = shlex.join(["python3", "tools/entry.py", "assemble", a.out, a.out + ".sig", *log_args])
    print(f"Unsigned entry written to {a.out} ({len(message)} bytes, canonical).\n"
          f"Sign it with exactly:\n\n    {sign}\n\n"
          f"then assemble:\n\n    {assemble} >> {shlex.quote(a.log)}\n")
    return 0


def assemble(a):
    """Print the signed line only if the kernel admits the log with it appended."""
    with open(a.unsigned, encoding="utf-8") as f:
        entry = json.loads(f.read())
    with open(a.sig) as f:
        entry["sig"] = dearmour(f.read())
    line = log.canonical(entry)
    verdict = check.check(read_log(a.log) + [line])
    if not verdict["ok"]:
        print(json.dumps(verdict, sort_keys=True), file=sys.stderr)
        return 1
    sys.stdout.write(line + "\n")
    return 0


def now():
    """The verb's clock, UTC, in SPEC §4's form; the kernel never reads one."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def forecast_body(a, now):
    """jack forecast's body, or Usage: N in 1-999, TS an instant not earlier than the verb's clock, a claim; args an object."""
    try:
        args = {} if a.args is None else {"args": json.loads(a.args)}
    except ValueError as x:
        raise Usage(f"--args is not JSON: {x}") from None
    for bad, why in ((not 1 <= a.p <= 999, f"--p {a.p} is outside 1-999 (per mille)"), (not a.claim, "the claim is empty"),
                     (not log.instant(a.by) or a.by < now, f"--by {a.by!r} is not an instant at or after the clock, {now}"),
                     (not isinstance(args.get("args", {}), dict), "--args is not a JSON object")):
        if bad:
            raise Usage(why)
    return dict({"claim": a.claim, "p": a.p, "resolves_by": a.by}, **({} if a.type is None else {"type": a.type}), **args)


def resolution_body(a, state, party, root=ROOT):
    """jack resolve's body, or Usage with the kernel's own reason, before signing; sha256:<hex64> names a file of that hash."""
    if a.seq not in state.forecasts or a.seq in state.resolved or a.outcome not in (0, 1):
        raise Usage(f"schema: seq {a.seq} is not an unresolved forecast, or outcome {a.outcome} is not 0 or 1")
    if state.forecasts[a.seq] == party:
        raise Usage(f"self_judged: {party} made forecast {a.seq}; no party resolves its own forecast")
    path = os.path.join(root, "transcripts", "evidence", h := a.evidence.removeprefix("sha256:"))
    if a.evidence.startswith("sha256:") and not (log.HEX64.fullmatch(h) and os.path.isfile(path)
                                                and hashlib.sha256(open(path, "rb").read()).hexdigest() == h):
        raise Usage(f"{a.evidence} names no file transcripts/evidence/<hex64> whose SHA-256 is <hex64>")
    return {"forecast": a.seq, "outcome": a.outcome, "evidence": a.evidence}


def valid_run(parts, head, seeds):
    """jack push: the record (SHA-256 of the parts in name order) if the twelve are BRANCH head's clean run, else None."""
    reps = [json.loads(parts[n]) for n in sorted(parts)]
    edges = [r["seeds"] for r in reps]
    ok = len(reps) == 12 and [e[0] for e in edges] == [0] + [e[1] for e in edges[:-1]] and edges[-1][1] == seeds and all(
        r["commit"] == head and r["logs"] == r["seeds"][1] - r["seeds"][0] and r["disagreements"] == [] == r["uncompared"] for r in reps)
    return hashlib.sha256(b"".join(parts[n] for n in sorted(parts))).hexdigest() if ok else None


def fmt(x):
    """Four decimals, half to even, of the exact value (a Fraction, or a float's binary value)."""
    q = fractions.Fraction(x)
    return str((decimal.Decimal(q.numerator) / decimal.Decimal(q.denominator)).quantize(decimal.Decimal("0.0001"), decimal.ROUND_HALF_EVEN))


def resolution_rates(es):
    """C1's prequential Laplace base: every resolution, pooled by type, in seq order."""
    forecasts, seen = {}, {}
    for e in sorted(es, key=lambda e: e["seq"]):
        if e["type"] == "forecast":
            forecasts[e["seq"]] = e
        if e["type"] == "resolution":
            f = forecasts[e["body"]["forecast"]]
            typ = f["body"].get("type", "free")
            s, n = seen.get(typ, (0, 0))
            yield e, f, fractions.Fraction(s + 1, n + 2), (s, n)
            seen[typ] = (s + e["body"]["outcome"], n + 1)


def score(lines, as_of=None):
    """jack score (BRIEF-C1.md): per (proposer, type), then per proposer and per type with all its forecasts counted: resolved,
    mean p, outcome rate, mean log-loss in nats and the base-rate loss (Laplace, pooled by type, in resolution-seq order)."""
    if not check.check(lines)["ok"] or as_of is not None and not log.instant(as_of):
        raise Usage(f"the log is refused by the kernel, or --as-of {as_of!r} is not an instant")
    es = [json.loads(line) for line in lines]
    kind = {i: e["body"]["type"] if isinstance(e["body"].get("type"), str) else "free" for i, e in enumerate(es) if e["type"] == "forecast"}
    rows = []  # one per resolution: (proposer, type, p, outcome, loss, base-rate loss)
    for e, forecast, base, _ in resolution_rates(es):
        f, o = e["body"]["forecast"], e["body"]["outcome"]
        p = forecast["body"]["p"]
        rows.append((es[f]["proposer"], kind[f], p, o, -math.log((p if o else 1000 - p) / 1000), -math.log(base if o else 1 - base)))
    out, mean = [], lambda rs, j, d=1: fmt(fractions.Fraction(sum(r[j] for r in rs)) / (d * len(rs)))
    for head, key, counted in ((("proposer", "type"), slice(0, 2), False), (("proposer",), slice(0, 1), True), (("type",), slice(1, 2), True)):
        names = [*head, *(["forecasts"] if counted else []), "resolved", "mean p", "rate", "loss", "base-rate loss"]
        out += ["", "| " + " | ".join(names) + " |", "|" + "---|" * len(head) + "---:|" * (len(names) - len(head))]
        for g in sorted({r[key] for r in rows}):
            rs = [r for r in rows if r[key] == g]
            cells = [*g, *([str(sum((es[i]["proposer"], t)[key] == g for i, t in kind.items()))] if counted else []),
                     str(len(rs)), mean(rs, 2, 1000), mean(rs, 3), mean(rs, 4), mean(rs, 5)]
            out.append("| " + " | ".join(cells) + " |")
    late = sorted((es[i]["body"]["resolves_by"], i) for i in kind if as_of and i not in {r["body"]["forecast"] for r in es
                                                                                       if r["type"] == "resolution"} and es[i]["body"]["resolves_by"] < as_of)
    out += [f"\noverdue at {as_of}:", "| seq | proposer | type | p | resolves_by |", "|---:|---|---|---:|---|"] if as_of else []
    out += [f"| {i} | {es[i]['proposer']} | {kind[i]} | {es[i]['body']['p']} | {by} |" for by, i in late]
    return "\n".join(out[1:])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--type", required=True)
    p.add_argument("--proposer", required=True)
    p.add_argument("--ts", required=True)
    p.add_argument("--body-json", required=True, help="JSON object for the entry body")
    p.add_argument("--pubkey", required=True, help="the signer's public key file")
    p.add_argument("--out", required=True)
    p.add_argument("--log", default=LOG)
    p.set_defaults(fn=prepare)
    s = sub.add_parser("assemble")
    s.add_argument("unsigned")
    s.add_argument("sig")
    s.add_argument("--log", default=LOG)
    s.set_defaults(fn=assemble)
    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except (Usage, OSError, ValueError, log.Refuse) as x:
        print(str(x), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
