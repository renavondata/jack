#!/usr/bin/env python3
"""C2a: exact resolution-order Bayes mixture and A4.4's bounded-difference bet.

Pure entry folds; the CLI alone reads files/the clock. Window diagnostics never
reset the first opening's roster, likelihoods, prior differences or wealth.
"""
import argparse
import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.entry import now, read_log, resolution_rates
from kernel import check, log

B = math.log(999)


def clip(p):
    return min(Fraction(999, 1000), max(Fraction(1, 1000), p))


def event(f):
    """Physical key and cutoff, or None. Claim prose never supplies an identity."""
    body = f["body"]
    a, typ = body.get("args", {}), body.get("type")
    if typ == "world.renavon" and a.get("stream") == "freshness":
        w = a.get("window_utc")
        if isinstance(a.get("dataset"), str) and isinstance(w, (list, tuple)) and len(w) == 2 and all(log.instant(t) for t in w) and w[0] < w[1]:
            return (typ, "freshness", a["dataset"], tuple(w)), w[0]
    if typ == "world.hkjc" and isinstance(a.get("meeting"), str) and type(a.get("race")) is int and log.instant(a.get("off_utc")):
        kind = a.get("kind", "favourite_wins")
        if isinstance(kind, str):
            return (typ, a["meeting"], a["race"], kind), a["off_utc"]
    return None


def opening_push(es):
    return next(e for e in es if e["type"] == "push" and e["seq"] > 337)


def roster_at(es, opening):
    keys = {}
    for e in es:
        if e["ts"] <= opening:
            for d in e["body"].get("keys", []) if e["type"] == "genesis" else [e["body"]] if e["type"] == "key" else []:
                keys[d["key_id"]] = d
    return list(dict.fromkeys(d["principal"] for d in keys.values() if "forecast" in d["powers"])) + ["base"]


def normalize(values):
    total = sum(values.values(), Fraction(0))
    return {k: v / total for k, v in values.items()}


def likelihood(p, y):
    return p if y else 1 - p


def difference(q, b, y):
    return math.log(likelihood(q, y) / likelihood(b, y)) / B


def stake(prior):
    return min(max(0.0, sum(prior) / (2 + sum(x * x for x in prior))), 1 - 1 / (len(prior) + 2))


def factor(lam, x):
    return 1 + lam * x


def value(es, opening=None, as_of=None, attack_green=None, no_attack_gate=False, window_opening=None):
    """One continuing ledger; window_opening selects diagnostics only, never resets it."""
    es = sorted((e for e in es if as_of is None or e["ts"] <= as_of), key=lambda e: e["seq"])
    opening = opening or opening_push(es)["ts"]
    window_opening = window_opening or opening
    roster = roster_at(es, opening)
    weights = {k: Fraction(1, len(roster)) for k in roster}
    window_weights, own = weights.copy(), dict.fromkeys(roster, Fraction(1))
    groups, excluded, unkeyed = {}, [], []
    for f in (e for e in es if e["type"] == "forecast"):
        identity = event(f)
        if identity is None:
            unkeyed.append(f["seq"])
            continue
        key, cutoff = identity
        g = groups.setdefault(key, {"cutoff": cutoff, "forecasts": {}, "resolution": None})
        g.setdefault("candidates", []).append(f)
    rates = list(resolution_rates(es))
    for r, f, _, _ in rates:
        identity = event(f)
        if identity and groups[identity[0]]["resolution"] is None:
            groups[identity[0]]["resolution"] = r
    for g in groups.values():
        for f in g["candidates"]:
            who, r = f["proposer"], g["resolution"]
            reason = None
            if f["ts"] >= g["cutoff"] or r is not None and (f["ts"] > r["ts"] or f["seq"] >= r["seq"]):
                reason = "rigged: ts >= cutoff" if f["ts"] >= g["cutoff"] else "rigged: after resolution"
            elif event(f)[1] != g["cutoff"]:
                reason = "conflicting cutoff"
            elif who not in roster:
                reason = "not in opening roster"
            elif who in g["forecasts"]:
                reason = "revision"
            if reason:
                excluded.append((f["seq"], reason))
            else:
                g["forecasts"][who] = (f["seq"], clip(Fraction(f["body"]["p"], 1000)))
    rows, prior, omitted, wealth, mixture_lr = [], [], [], 1.0, Fraction(1)
    for r, f, raw_base, counts in rates:
        identity = event(f)
        if identity is None:
            continue
        key, _ = identity
        g, cutoff = groups[key], groups[key]["cutoff"]
        if r != g["resolution"]:
            continue
        if cutoff <= opening or not no_attack_gate and (attack_green is None or cutoff <= attack_green):
            omitted.append((r["seq"], key, "before opening/attack green"))
            continue
        b, y = clip(raw_base), r["body"]["outcome"]
        ps = {k: g["forecasts"].get(k, (None, b))[1] for k in roster}
        q = sum((weights[k] * ps[k] for k in roster), Fraction(0))
        x, lam = difference(q, b, y), stake(prior)
        step = factor(lam, x)
        wealth *= step
        rows.append(dict(key=key, cutoff=cutoff, resolution_seq=r["seq"], Y=y, base=b, base_counts=counts,
                         forecasts=g["forecasts"].copy(), weights_before=weights.copy(), q=q, D_over_B=x,
                         **{"lambda": lam}, factor=step, E_after=wealth))
        prior.append(x)
        ls = {k: likelihood(ps[k], y) for k in roster}
        weights = normalize({k: weights[k] * ls[k] for k in roster})
        own = {k: own[k] * ls[k] / likelihood(b, y) for k in roster}
        mixture_lr *= likelihood(q, y) / likelihood(b, y)
        if cutoff > window_opening:
            window_weights = normalize({k: window_weights[k] * ls[k] for k in roster})
    return dict(opening=opening, as_of=as_of, events=len(rows), rows=rows, E_value=wealth,
                window_events=sum(r["cutoff"] > window_opening for r in rows), window_weights=window_weights,
                terminal_weights=weights, own_likelihood_ratio_vs_base=own, mixture_likelihood_ratio_vs_base=mixture_lr,
                excluded_forecasts=sorted(excluded), unkeyed=unkeyed, excluded_events=omitted)


def table(result):
    """Six-decimal display only; exact probabilities remain in the calculation."""
    def rounded(x):
        if isinstance(x, dict):
            return {k: rounded(v) for k, v in x.items()}
        if isinstance(x, (tuple, list)):
            return [rounded(v) for v in x]
        return round(float(x), 6) if isinstance(x, (Fraction, float)) else x
    out = rounded(result)
    for row, exact in zip(out["rows"], result["rows"]):
        row["base"] = str(exact["base"])
        row["forecasts"] = {k: [seq, str(p)] for k, (seq, p) in exact["forecasts"].items()}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "log.jsonl"))
    ap.add_argument("--opening")
    ap.add_argument("--as-of", default=now())
    ap.add_argument("--attack-green", help="instant from a verified main tests run holding tests/test_value.py")
    ap.add_argument("--no-attack-gate", action="store_true", help="illustrative fixture only")
    ap.add_argument("--table", action="store_true")
    a = ap.parse_args(argv)
    if not all(log.instant(t) for t in (a.as_of, a.opening or a.as_of, a.attack_green or a.as_of)):
        ap.error("timestamps must be UTC instants")
    lines = read_log(a.log)
    if not check.check(lines)["ok"]:
        ap.error("log refused by kernel")
    result = value(list(map(json.loads, lines)), a.opening, a.as_of, a.attack_green, a.no_attack_gate)
    print(json.dumps(table(result), indent=1) if a.table else
          f"value: E {result['E_value']:.6f} over {result['events']} events; window events {result['window_events']}")


if __name__ == "__main__":
    main()
