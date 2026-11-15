#!/usr/bin/env python3
"""BRIEF-C2b's election mechanism, built for replay; C2b holds no live round.

No mode writes an entry. Signature custody assumptions are those of §The draw;
the frequency table is a diagnostic with no detection guarantee.
"""
import argparse
import base64
import datetime as dt
from fractions import Fraction
import hashlib
import json
import math
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check, log, sig
from sim import election as el
from tools import entry, status as st, value as val

DATASETS = ("hk_property_poi", "hkex_disclosures", "hkex_disclosure_interests",
            "crhk_companies", "sfc_licences", "hk_property_transactions")
HOUR = dt.timedelta(hours=1)


def window(es):
    promotion = next((e for e in es if st.promotes(e, "C2a")), None)
    opening = next((e for e in es if promotion and e["type"] == "push" and e["seq"] > promotion["seq"]), None)
    forecast = next((e for e in es if opening and e["seq"] < opening["seq"] and e["type"] == "forecast" and
                     e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "X7"), None)
    if forecast is None or opening["ts"] >= forecast["body"]["resolves_by"]:
        raise ValueError("C2b has no opening with a promotion forecast before it")
    return opening, forecast["body"]["resolves_by"]


def slot(opening, end, stream, w0):
    """Amendment 12: first whole hour strictly later than the push is round 0."""
    start = st.instant(w0)
    first = st.instant(opening["ts"]).replace(minute=0, second=0) + HOUR
    t = (start - first) / HOUR
    if stream != "freshness" or start.minute or start.second or t < 0 or not t.is_integer() or w0 > end:
        raise ValueError("round outside the freshness window")
    return int(t), int(t) % (el.D + 1), (start + HOUR).strftime(st.FMT), (start + 5 * HOUR).strftime(st.FMT)


def clerk(es):
    declarations = {}
    for e in sorted(es, key=lambda e: e["seq"]):
        for d in e["body"].get("keys", []) if e["type"] == "genesis" else [e["body"]] if e["type"] == "key" else []:
            declarations[d["key_id"]] = d
    d = declarations.get("herald-2")
    if d is None or d["principal"] != "herald" or "forecast" not in d["powers"]:
        raise ValueError("unkeyed: herald-2 has no forecast power")
    return log.pubkey_blob(d["pubkey"])


def round_message(stream, w0):
    return f"election.invite {stream} {w0}".encode("ascii")


def verify_sigma(pub, stream, w0, encoded):
    raw = base64.b64decode(encoded, validate=True)
    message = (b"SSHSIG" + sig._pack(b"jack-election") + sig._pack(b"") + sig._pack(b"sha512") +
               sig._pack(hashlib.sha512(round_message(stream, w0)).digest()))
    if len(raw) != 64 or not sig.ed25519_verify(pub[-32:], raw, message):
        raise ValueError("rigged_election: sigma does not verify")
    return raw


def sign_sigma(key, pub, stream, w0):
    """One ssh-keygen call; extract its raw Ed25519 signature, not the SSHSIG hash."""
    signed = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", key, "-n", "jack-election", "-"],
                            input=round_message(stream, w0), capture_output=True, check=True)
    envelope = base64.b64decode(b"".join(l for l in signed.stdout.splitlines() if not l.startswith(b"-----")), validate=True)
    if envelope[:10] != b"SSHSIG\x00\x00\x00\x01":
        raise ValueError("rigged_election: SSHSIG header")
    fields, off = [], 10
    for _ in range(5):
        value, off = sig.sshstr(envelope, off)
        fields.append(value)
    typ, pos = sig.sshstr(fields[4], 0)
    raw, pos = sig.sshstr(fields[4], pos)
    if (fields[:4] != [pub, b"jack-election", b"", b"sha512"] or off != len(envelope) or
            typ != b"ssh-ed25519" or pos != len(fields[4])):
        raise ValueError("rigged_election: SSHSIG fields")
    encoded = base64.b64encode(raw).decode("ascii")
    verify_sigma(pub, stream, w0, encoded)
    return encoded


def feedback(invite, es, as_of, evidence):
    """First qualifying forecast per dataset; six slots, including every missing one.

    The signed deadline bounds the resolution prefix forever. Success is a strict
    product comparison of exact likelihoods, avoiding a floating-point log tie.
    """
    a, by = invite["body"]["args"], invite["body"]["resolves_by"]
    prefix = sorted((e for e in es if e["ts"] <= min(as_of, by)), key=lambda e: e["seq"])
    forecasts = {}
    for f in prefix:
        b = f["body"]
        fa = b.get("args", {})
        dataset = fa.get("dataset")
        if (f["type"] == "forecast" and b.get("type") == "world.renavon" and dataset in DATASETS and
                fa.get("stream") == a["stream"] and fa.get("window_utc") == a["window_utc"] and
                type(fa.get("invite")) is int and fa["invite"] == invite["seq"] and
                f["seq"] > invite["seq"] and invite["ts"] < f["ts"] < a["window_utc"][0] and
                (f["proposer"], fa.get("model")) == (a["principal"], a["model"]) and b["resolves_by"] == by):
            forecasts.setdefault(dataset, f)
    rates = {}
    for r, f, base, _ in entry.resolution_rates(prefix):
        identity = val.event(f)
        if identity:
            rates.setdefault(identity[0], (r, base))
    ns, bases, times = [], [], []
    for dataset in DATASETS:
        f = forecasts.get(dataset)
        resolved = rates.get(("world.renavon", "freshness", dataset, tuple(a["window_utc"]))) if f else None
        if resolved:
            r, base = resolved
            if (r["proposer"] != a["principal"] and r["seq"] > f["seq"] and
                    a["window_utc"][1] <= r["ts"] and evidence(r["body"]["evidence"])):
                y, p = r["body"]["outcome"], f["body"]["p"]
                ns.append(p if y else 1000 - p)
                bases.append(val.likelihood(val.clip(base), y))
                times.append(r["ts"])
                continue
        ns.append(1)
    complete = len(times) == len(DATASETS)
    settled = complete or as_of >= by
    return dict(settled=settled, gain=el.gain(ns) if settled else None,
                success=int(complete and math.prod(Fraction(n, 1000) for n in ns) > math.prod(bases)),
                at=max(times) if complete else by, ns=ns)


def state(history, es, as_of, evidence):
    gains = [(Fraction(0),) * el.K for _ in range(el.D + 1)]
    successes, rows, last = [[] for _ in el.ROSTER], [], {}
    for invite in history:
        a = invite["body"]["args"]
        arm = el.ROSTER.index((a["principal"], a["model"]))
        j = a["instance"]
        result = feedback(invite, es, as_of, evidence)
        if result["settled"]:
            gains[j] = el.update(gains[j], arm, result["gain"], Fraction(a["propensity"]))
            successes[arm].append(result["success"])
        row = dict(result, seq=invite["seq"], round=a["round"], instance=j, arm=arm,
                   propensity=Fraction(a["propensity"]))
        rows.append(row)
        last[j] = row
    return dict(gains=gains, successes=successes, rows=rows, last=last)


def invite_body(es, history, as_of, stream, w0, sigma, evidence):
    opening, end = window(es)
    t, j, w1, by = slot(opening, end, stream, w0)
    if as_of >= w0:
        raise ValueError("skipped: W0")
    if as_of < opening["ts"]:
        raise ValueError("round before opening")
    for _, f, _, _ in entry.resolution_rates(es):
        identity = val.event(f)
        if identity and identity[0][:2] == ("world.renavon", stream) and identity[0][3] == (w0, w1):
            raise ValueError("rigged_election: an event's outcome is already known")
    prior = state(history, es, as_of, evidence)
    if j in prior["last"] and not prior["last"][j]["settled"]:
        raise ValueError(f"wait: instance {j} round {prior['last'][j]['round']} unresolved")
    raw = verify_sigma(clerk(es), stream, w0, sigma)
    gains = prior["gains"][j]
    draw = el.draw(gains, raw)
    arm = draw["arm"]
    principal, model = el.ROSTER[arm]
    a = dict(stream=stream, window_utc=[w0, w1], round=t, instance=j, sigma=sigma,
             roster=[list(pair) for pair in el.ROSTER], principal=principal, model=model,
             gains=[f"{g.numerator}/{g.denominator}" for g in gains], cuts=[str(c) for c in draw["cuts"]],
             propensity=f"{draw['cuts'][arm + 1] - draw['cuts'][arm]}/{el.GRID}",
             gamma=repr(el.GAMMA), eta=repr(el.ETA))
    return dict(type="election.invite", args=a, p=el.success_rate(prior["successes"][arm]), resolves_by=by,
                claim=f"stream {stream}, window {w0}: the invited entrant <{principal}, {model}> "
                      "achieves a mean clipped log-loss on the window's six events below the base rate's")


def audit(es, as_of, evidence):
    prefix = sorted((e for e in es if e["ts"] <= as_of), key=lambda e: e["seq"])
    history, refused, seen = [], [], set()
    for i, f in enumerate(prefix):
        if f["type"] != "forecast" or f["body"].get("type") != "election.invite":
            continue
        before = prefix[:i]
        try:
            pub = clerk(before)
            blob, signature = sig.parse_sshsig(f["sig"])
            message = log.canonical({k: v for k, v in f.items() if k != "sig"}).encode()
            if blob != pub or f["proposer"] != "herald" or not sig.verify(message, blob, signature):
                raise ValueError("unkeyed: invite not signed by herald-2")
        except (ValueError, KeyError) as exc:
            refused.append((f["seq"], "unkeyed: " + str(exc)))
            continue
        try:
            a = f["body"]["args"]
            identity = (a["stream"], a["window_utc"][0])
            if identity in seen:
                raise ValueError("revision")
            seen.add(identity)
            expected = invite_body(before, history, f["ts"], *identity, a["sigma"], evidence)
            if log.canonical(expected) != log.canonical(f["body"]):
                raise ValueError("recomputed body differs")
            history.append(f)
        except (ValueError, KeyError, TypeError, IndexError, OverflowError) as exc:
            refused.append((f["seq"], "revision" if str(exc) == "revision" else "rigged_election: " + str(exc)))
    return dict(history=history, refused=refused, **state(history, prefix, as_of, evidence))


def replay(es, seq, evidence):
    invite = next((e for e in es if e["seq"] == seq), None)
    if invite is None or invite["type"] != "forecast" or invite["body"].get("type") != "election.invite":
        raise ValueError("not an election invite")
    result = audit([e for e in es if e["seq"] <= seq], invite["ts"], evidence)
    error = next((reason for n, reason in result["refused"] if n == seq), None)
    if error:
        raise ValueError(error)
    return next(f for f in result["history"] if f["seq"] == seq)


def resolve_plan(es, seq, as_of, evidence):
    invite = replay(es, seq, evidence)
    a = invite["body"]["args"]
    result = feedback(invite, es, as_of, evidence)
    return dict(invite=seq, resolver="builder" if a["principal"] == "reviewer" else "reviewer",
                datasets=list(DATASETS), resolves_by=invite["body"]["resolves_by"],
                outcome=result["success"] if result["settled"] else None)


def table(es, as_of, evidence):
    result = audit(es, as_of, evidence)
    rows = result["rows"]
    arms = []
    for k, (principal, model) in enumerate(el.ROSTER):
        own = [r for r in rows if r["arm"] == k]
        settled = [r for r in own if r["settled"]]
        arms.append(dict(principal=principal, model=model, invited=len(own), settled=len(settled),
                         G=str(sum((g[k] for g in result["gains"]), Fraction(0))),
                         mean_gain=str(sum((r["gain"] for r in settled), Fraction(0)) / len(settled)) if settled else None,
                          successes=sum(r["success"] for r in settled),
                          frequency=str(Fraction(len(own), len(rows))) if rows else None,
                          mean_propensity=str(sum((Fraction(int(f["body"]["args"]["cuts"][k + 1]) -
                              int(f["body"]["args"]["cuts"][k]), el.GRID) for f in result["history"]), Fraction(0)) /
                              len(rows)) if rows else None))
    skipped = []
    if result["history"]:
        first = min(f["body"]["args"]["round"] for f in result["history"])
        opening, end = window(es)
        f = st.instant(opening["ts"]).replace(minute=0, second=0) + HOUR
        occurred = {r["round"] for r in rows}
        for t in range(first, int((st.instant(min(as_of, end)) - f) / HOUR) + 1):
            if t not in occurred:
                skipped.append(dict(round=t, window_utc=(f + t * HOUR).strftime(st.FMT)))
    # C1's score includes all invites, including the audit's refusals, under their type.
    scored = entry.score([log.canonical(e) for e in sorted(es, key=lambda e: e["seq"])]) if any(
        e["type"] == "forecast" and e["body"].get("type") == "election.invite" for e in es) else ""
    invite_scores = "\n".join(line for line in scored.splitlines() if "election.invite" in line)
    return dict(arms=arms, instances=[dict(instance=j, last_round=result["last"].get(j, {}).get("round"),
                 settled=result["last"].get(j, {}).get("settled")) for j in range(el.D + 1)],
                skipped=skipped, refused=result["refused"], scores=invite_scores,
                diagnostic="arm frequencies versus recorded propensities: no detection guarantee")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group(required=True)
    modes.add_argument("--invite", nargs=2, metavar=("STREAM", "W0"))
    modes.add_argument("--replay", type=int)
    modes.add_argument("--resolve-plan", type=int)
    modes.add_argument("--table", action="store_true")
    ap.add_argument("--log", default=os.path.join(ROOT, "log.jsonl"))
    ap.add_argument("--root", default=ROOT, help="evidence tree")
    ap.add_argument("--as-of", default=entry.now())
    ap.add_argument("--sigma", help="base64 raw Ed25519 signature of the round string")
    ap.add_argument("--key", help="clerk's private key, only when --invite has no --sigma")
    a = ap.parse_args(argv)
    try:
        st.instant(a.as_of)
        lines = entry.read_log(a.log)
        if not check.check(lines)["ok"]:
            raise ValueError("log refused by kernel")
        es = [e for e in map(json.loads, lines) if e["ts"] <= a.as_of]
        evidence = lambda ev: st.evidence_ok(a.root, ev)
        if a.replay is not None:
            replay(es, a.replay, evidence)
            print(f"election invite {a.replay}: replay verified")
        elif a.resolve_plan is not None:
            print(json.dumps(resolve_plan(es, a.resolve_plan, a.as_of, evidence), sort_keys=True))
        elif a.table:
            print(json.dumps(table(es, a.as_of, evidence), sort_keys=True, indent=1))
        else:
            stream, w0 = a.invite
            opening, end = window(es)
            _, j, _, _ = slot(opening, end, stream, w0)
            if a.as_of >= w0:
                raise ValueError("skipped: W0")
            pub = clerk(es)
            result = audit(es, a.as_of, evidence)
            unkeyed = {n for n, why in result["refused"] if why.startswith("unkeyed")}
            if any(e["type"] == "forecast" and e["body"].get("type") == "election.invite" and
                   e["seq"] not in unkeyed and e["body"].get("args", {}).get("stream") == stream and
                   e["body"].get("args", {}).get("window_utc", [None])[0] == w0 for e in es):
                raise ValueError("revision")
            if j in result["last"] and not result["last"][j]["settled"]:
                raise ValueError(f"wait: instance {j} round {result['last'][j]['round']} unresolved")
            if not a.sigma and not a.key:
                raise ValueError("--invite needs --sigma or --key")
            sigma = a.sigma or sign_sigma(a.key, pub, stream, w0)
            print(json.dumps(invite_body(es, result["history"], a.as_of, stream, w0, sigma, evidence), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 3 if str(exc).startswith("wait:") else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
