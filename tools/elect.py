#!/usr/bin/env python3
"""C2b election: represented gains, exact importance sums, signed grid draws.

The folds below do no I/O. Verification/signing and the read-only CLI follow them.
The hash draw relies on custody, hash uniformity and non-anticipating rewards;
observed frequencies are a diagnostic with no detection guarantee.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import math
import os
import struct
import subprocess
import sys
import tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from tools import value
from tools.entry import now, read_log, resolution_rates, score
from kernel import check, log, sig

K, GJ, D = 3, 84, 3
GRID = 2**256
GAMMA = min(1, math.sqrt(K * math.log(K) / ((math.e - 1) * GJ)))
ETA = GAMMA / K
ROSTER = (("reviewer", "openai/gpt-5.4-mini"), ("builder", "openai/gpt-5.4-mini"),
          ("reviewer", "openai/gpt-6-astra-fast"))
DATASETS = ("hk_property_poi", "hkex_disclosures", "hkex_disclosure_interests",
            "crhk_companies", "sfc_licences", "hk_property_transactions")
FMT = "%Y-%m-%dT%H:%M:%SZ"
NAMESPACE = "jack-election"
PINS = ("gain_in_unit_interval round_loss_is_mean bad_round_kept exp3_importance exp3_constants "
        "instance_feedback_complete draw_replays_from_prefix sigma_verifies draw_on_the_grid roster_fixed "
        "invite_before_session invite_cutoff_W0 invite_p_is_success_rate invite_resolution_strict "
        "resolver_not_forecaster self_invite rigged_election mixture_untouched_and_continued procedure_types_out").split()


def gain(ns):
    ns = tuple(ns)
    if len(ns) != 6 or any(type(n) is not int or not 1 <= n <= 999 for n in ns):
        raise ValueError("gain needs six per-mille integers in 1..999")
    return Fraction(math.fsum(math.log(n) for n in ns) / 6 / math.log(999))


def cuts(G):
    if len(G) != K or any(g < 0 for g in G):
        raise ValueError("three nonnegative gains required")
    w = [math.exp(ETA * float(g)) for g in G]
    p = [(1 - GAMMA) * x / sum(w) + GAMMA / K for x in w]
    return (0, *(math.floor(sum(p[:k]) * GRID) for k in range(1, K)), GRID)


def arm(U, cs):
    if not 0 <= U < GRID or len(cs) != K + 1 or cs[0] != 0 or cs[-1] != GRID:
        raise ValueError("invalid grid")
    return next(k for k in range(K) if cs[k] <= U < cs[k + 1])


def propensity(k, cs):
    return Fraction(cs[k + 1] - cs[k], GRID)


def instant(s):
    if not log.instant(s):
        raise ValueError("timestamp must be UTC YYYY-MM-DDTHH:MM:SSZ")
    return dt.datetime.strptime(s, FMT).replace(tzinfo=dt.timezone.utc)


def later(s, hours):
    return (instant(s) + dt.timedelta(hours=hours)).strftime(FMT)


def window(es):
    es = sorted(es, key=lambda e: e["seq"])
    promoted = next(e for e in es if e["type"] == "decision" and
                    e["body"].get("kind") == "promote" and e["body"].get("subject") == "C2a")
    opening = next(e for e in es if e["type"] == "push" and e["seq"] > promoted["seq"])
    x0 = next(e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and
              e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "X0")
    revisions = [e for e in es if x0["seq"] < e["seq"] < opening["seq"] and e["type"] == "forecast" and
                 e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "X0" and
                 e["body"]["args"].get("revises") is not None]
    x0 = revisions[-1] if revisions else x0
    return opening["seq"], opening["ts"], min(x0["body"]["resolves_by"], later(opening["ts"], GJ * (D + 1)))


def first_slot(opening):
    return (instant(opening).replace(minute=0, second=0) + dt.timedelta(hours=1)).strftime(FMT)


def slot(W0, opening):
    t = (instant(W0) - instant(first_slot(opening))).total_seconds() / 3600
    if t != int(t) or not 0 <= t < GJ * (D + 1):
        raise ValueError("window is not an hourly slot after the opening")
    return int(t)


def invites(es):
    return [e for e in sorted(es, key=lambda e: e["seq"]) if e["type"] == "forecast" and
            e["body"].get("type") == "election.invite"]


def key_at(es, key_id):
    keys = {}
    for e in sorted(es, key=lambda e: e["seq"]):
        for d in e["body"].get("keys", []) if e["type"] == "genesis" else [e["body"]] if e["type"] == "key" else []:
            keys[d["key_id"]] = d
    return keys.get(key_id)


def round_string(stream, W0):
    return f"election.invite {stream} {W0}"


def raw_sigma(sigma):
    raw = base64.b64decode(sigma, validate=True)
    if len(raw) != 64 or base64.b64encode(raw).decode() != sigma:
        raise ValueError("sigma must encode 64 raw signature bytes")
    return raw


def resolver(invite):
    who = invite["body"]["args"]["principal"]
    if who not in ("reviewer", "builder"):
        raise ValueError("roster_fixed")
    return "builder" if who == "reviewer" else "reviewer"


def round_result(es, invite, as_of):
    """First physical resolution/base from value's loaders; deadline freezes imputation.

    A missing page has no evidenced resolution. Revision forecasts do not repair it.
    Timely complete feedback settles immediately; partial feedback waits for deadline.
    """
    a, by = invite["body"]["args"], invite["body"]["resolves_by"]
    prefix = sorted((e for e in es if e["ts"] <= min(as_of, by)), key=lambda e: e["seq"])
    forecasts, resolved = {}, {}
    for f in prefix:
        if f["type"] != "forecast" or not value.event(f):
            continue
        fa = f["body"].get("args", {})
        if (fa.get("invite") == invite["seq"] and f["seq"] > invite["seq"] and
                invite["ts"] < f["ts"] < a["window_utc"][0] and
                f["proposer"] == a["principal"] and fa.get("model") == a["model"] and
                fa.get("stream") == a["stream"] and fa.get("window_utc") == a["window_utc"] and
                f["body"]["resolves_by"] == by and fa.get("dataset") in DATASETS):
            forecasts.setdefault(fa["dataset"], f)
    for r, f, base, _ in resolution_rates(prefix):
        identity = value.event(f)
        if identity:
            resolved.setdefault(identity[0], (r, value.clip(base)))
    ns, bases, times = [], [], []
    for dataset in DATASETS:
        f = forecasts.get(dataset)
        pair = resolved.get(value.event(f)[0]) if f else None
        if pair and (pair[0]["proposer"] != a["principal"] and
                     pair[0]["proposer"] == resolver(invite) and pair[0]["body"].get("evidence") and
                     pair[0]["ts"] >= a["window_utc"][1]):
            r, b = pair
            y = r["body"]["outcome"]
            ns.append(int(value.likelihood(value.clip(Fraction(f["body"]["p"], 1000)), y) * 1000))
            bases.append(value.likelihood(b, y))
            times.append(r["ts"])
        else:
            ns.append(1)
    complete = len(bases) == 6
    # A product comparison is the strict mean-log-loss comparison, with exact ties.
    success = int(complete and math.prod(Fraction(n, 1000) for n in ns) > math.prod(bases))
    return dict(gain=gain(ns), success=success, settled=complete or as_of >= by,
                settled_at=max(times) if complete else by, ns=ns, complete=complete)


def state(es, rounds, instance, as_of):
    G = [Fraction(0) for _ in range(K)]
    for f in rounds:
        a, r = f["body"]["args"], round_result(es, f, as_of)
        if a["instance"] == instance and r["settled"]:
            k = ROSTER.index((a["principal"], a["model"]))
            G[k] += r["gain"] / Fraction(a["propensity"])
    return G


def success_rate(es, rounds, k, as_of):
    rs = [round_result(es, f, as_of) for f in rounds if
          (f["body"]["args"]["principal"], f["body"]["args"]["model"]) == ROSTER[k]]
    settled = [r for r in rs if r["settled"]]
    rate = Fraction(1000 * (sum(r["success"] for r in settled) + 1), len(settled) + 2)
    return min(999, max(1, math.floor(rate + Fraction(1, 2))))


def ready(es, rounds, stream, W0, as_of):
    _, opening, end = window(es)
    t = slot(W0, opening)
    if stream != "freshness" or later(W0, 1) > end:
        raise ValueError("outside election window/stream")
    if any(f["body"]["args"].get("stream") == stream and f["body"]["args"].get("window_utc", [None])[0] == W0 for f in invites(es)):
        raise ValueError("revision: (stream, W0) already invited")
    if as_of >= W0:
        raise ValueError(f"skipped: {W0}")
    if as_of < opening:
        raise ValueError("before election opening")
    previous = [f for f in rounds if f["body"]["args"]["instance"] == t % (D + 1)]
    if any(f["body"]["args"]["round"] >= t for f in previous):
        raise ValueError("rigged_election: non-increasing instance round")
    if any(not round_result(es, f, as_of)["settled"] for f in previous):
        raise ValueError(f"wait: instance {t % (D + 1)} round {t - D - 1} unresolved")
    return t


def invite_body(es, rounds, stream, W0, as_of, sigma):
    t = ready(es, rounds, stream, W0, as_of)
    G = state(es, rounds, t % (D + 1), as_of)
    cs = cuts(G)
    U = int.from_bytes(hashlib.sha256(raw_sigma(sigma)).digest(), "big")
    k = arm(U, cs)
    principal, model = ROSTER[k]
    args = dict(stream=stream, window_utc=[W0, later(W0, 1)], principal=principal, model=model,
                roster=[list(pair) for pair in ROSTER], round=t, instance=t % (D + 1),
                gains=[str(g) for g in G], cuts=[str(c) for c in cs],
                propensity=f"{cs[k + 1] - cs[k]}/{GRID}", gamma=repr(GAMMA), eta=repr(ETA), sigma=sigma)
    claim = (f"stream {stream}, window {W0}: the invited entrant <{principal}, {model}> achieves a mean clipped "
             "log-loss on the window's six events below the base rate's")
    return dict(claim=claim, p=success_rate(es, rounds, k, as_of), type="election.invite",
                resolves_by=later(W0, 5), args=args)


def replay_fields(es, rounds, f, verifies):
    """Called with a seq prefix, never a timestamp-sorted or future prefix."""
    declaration = key_at(es, "herald-2")
    public, _ = sig.parse_sshsig(f["sig"])
    if not declaration or public != base64.b64decode(declaration["pubkey"].split()[1]):
        return "self_invite: unkeyed"
    a = f["body"].get("args", {})
    if f["ts"] >= a["window_utc"][0]:
        return "rigged_election: rigged: ts >= W0"
    if not verifies(declaration["pubkey"], round_string(a["stream"], a["window_utc"][0]), a["sigma"]):
        return "rigged_election: sigma"
    expected = invite_body(es, rounds, a["stream"], a["window_utc"][0], f["ts"], a["sigma"])
    for field in sorted(set(a) | set(expected["args"])):
        if field not in a or field not in expected["args"] or log.canonical(a[field]) != log.canonical(expected["args"][field]):
            return f"rigged_election: args.{field} differs"
    for field in ("claim", "p", "type", "resolves_by"):
        if log.canonical(f["body"].get(field)) != log.canonical(expected[field]):
            return f"rigged_election: {field} differs"
    return None


def audit(es, verifies):
    prefix, rounds, errors = [], [], {}
    for f in sorted(es, key=lambda e: e["seq"]):
        if f["type"] == "forecast" and f["body"].get("type") == "election.invite":
            try:
                error = replay_fields(prefix, rounds, f, verifies)
            except (ValueError, KeyError, TypeError, IndexError, StopIteration, log.Refuse) as exc:
                error = f"rigged_election: {exc}"
            if error:
                errors[f["seq"]] = error
            else:
                rounds.append(f)
        prefix.append(f)
    return rounds, errors


def summary(es, rounds, as_of):
    _, opening, end = window(es)
    records = [(f, round_result(es, f, as_of)) for f in rounds]
    rows = []
    for k, pair in enumerate(ROSTER):
        selected = [(f, r) for f, r in records if (f["body"]["args"]["principal"], f["body"]["args"]["model"]) == pair]
        settled = [r for _, r in selected if r["settled"]]
        mean = sum((r["gain"] for r in settled), Fraction(0)) / len(settled) if settled else None
        masses = [propensity(k, tuple(map(int, f["body"]["args"]["cuts"]))) for f in rounds]
        rows.append(dict(principal=pair[0], model=pair[1], invited=len(selected),
                         G=sum((state(es, rounds, j, as_of)[k] for j in range(D + 1)), Fraction(0)),
                         mean_gain=mean, successes=sum(r["success"] for r in settled),
                         frequency=Fraction(len(selected), len(rounds)) if rounds else None,
                         mean_recorded_propensity=sum(masses) / len(masses) if masses else None))
    instances = []
    for j in range(D + 1):
        past = [(f, r) for f, r in records if f["body"]["args"]["instance"] == j]
        instances.append(dict(instance=j, last_round=past[-1][0]["body"]["args"]["round"] if past else None,
                              resolved=past[-1][1]["settled"] if past else True))
    hours = [later(first_slot(opening), t) for t in range(GJ * (D + 1))]
    occupied = {f["body"]["args"]["window_utc"][0] for f in rounds}
    skipped = [h for h in hours if h <= as_of and later(h, 1) <= end and h not in occupied]
    return dict(arms=rows, instances=instances, skipped=skipped,
                diagnostic="arm frequencies vs mean recorded propensities: diagnostic, no detection guarantee")


def summary_line(result):
    return "election: " + json.dumps(result, default=str, separators=(",", ":"))


# I/O boundary: SSHSIG has a fixed namespace/hash envelope; args stores raw sigma.
def sshstr(b):
    return struct.pack(">I", len(b)) + b


def envelope(pubkey, raw):
    return (b"SSHSIG" + struct.pack(">I", 1) + sshstr(base64.b64decode(pubkey.split()[1])) +
            sshstr(NAMESPACE.encode()) + sshstr(b"") + sshstr(b"sha512") +
            sshstr(sshstr(b"ssh-ed25519") + sshstr(raw)))


def sign_sigma(key, message):
    result = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", os.path.expanduser(key), "-n", NAMESPACE, "-"],
                            input=message.encode("ascii"), capture_output=True, check=True)
    blob = base64.b64decode(b"".join(result.stdout.splitlines()[1:-1]), validate=True)
    # OpenSSH's final SSH string is the raw Ed25519 signature, with length 64.
    if blob[-68:-64] != struct.pack(">I", 64):
        raise ValueError("not an Ed25519 SSH signature")
    return base64.b64encode(blob[-64:]).decode()


def verify_sigma(pubkey, message, sigma):
    raw = raw_sigma(sigma)
    with tempfile.TemporaryDirectory(prefix="jack-election-") as tmp:
        allowed, signature = os.path.join(tmp, "allowed"), os.path.join(tmp, "signature")
        with open(allowed, "w") as f:
            f.write(f'herald-2 namespaces="{NAMESPACE}" {pubkey}\n')
        with open(signature, "w") as f:
            f.write("-----BEGIN SSH SIGNATURE-----\n" + base64.b64encode(envelope(pubkey, raw)).decode() +
                    "\n-----END SSH SIGNATURE-----\n")
        r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", allowed, "-I", "herald-2", "-n", NAMESPACE,
                            "-s", signature], input=message.encode("ascii"), capture_output=True)
        return r.returncode == 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--invite", nargs=2, metavar=("STREAM", "W0"))
    group.add_argument("--replay", type=int)
    group.add_argument("--resolve-plan", type=int)
    group.add_argument("--table", action="store_true")
    ap.add_argument("--log", default=os.path.join(ROOT, "log.jsonl"))
    ap.add_argument("--as-of", help="explicit observation clock (default now)")
    ap.add_argument("--sigma", help="base64 of the 64 raw Ed25519 signature bytes")
    a = ap.parse_args(argv)
    try:
        live_clock = a.as_of is None
        a.as_of = a.as_of or now()
        instant(a.as_of)
        lines = read_log(a.log)
        if not check.check(lines)["ok"]:
            raise ValueError("log refused by kernel")
        es = list(map(json.loads, lines))
        target = a.replay if a.replay is not None else a.resolve_plan
        if target is not None:
            es = [e for e in es if e["seq"] <= target]
        else:
            es = [e for e in es if e["ts"] <= a.as_of]
        rounds, errors = audit(es, verify_sigma)
        if target is not None:
            if target in errors:
                print(errors[target])
                return 1
            f = next((f for f in rounds if f["seq"] == target), None)
            if f is None:
                raise ValueError("not an election invite")
            print(resolver(f) if a.resolve_plan is not None else f"election invite {target}: replay verified")
            return 0
        if a.invite:
            stream, W0 = a.invite
            ready(es, rounds, stream, W0, a.as_of)
            declaration = key_at(es, "herald-2")
            if not declaration or "forecast" not in declaration["powers"]:
                raise ValueError("herald-2 lacks forecast power")
            # No persisted green flag: test exactly the working tree before signing.
            tested = subprocess.run([sys.executable, "-m", "unittest", "-q",
                                     "tests.test_elect.Election.test_self_invite",
                                     "tests.test_elect.Election.test_rigged_election"], cwd=ROOT)
            if tested.returncode:
                raise ValueError("attack tests not green on this tree")
            message = round_string(stream, W0)
            print(message, flush=True)
            sigma = a.sigma or sign_sigma("~/.ssh/jack-herald", message)
            if not verify_sigma(declaration["pubkey"], message, sigma):
                raise ValueError("rigged_election: sigma")
            if live_clock:
                a.as_of = now()  # tests/signing may have crossed W0 or a feedback deadline
            print(json.dumps(invite_body(es, rounds, stream, W0, a.as_of, sigma), separators=(",", ":")))
        else:
            result = summary(es, rounds, a.as_of)
            # score itself supplies the type's exact C1 formatting and base convention.
            result["invite_scores"] = [line for line in score([log.canonical(e) for e in es]).splitlines()
                                       if "election.invite" in line]
            result["refused"] = errors
            print(summary_line(result))
        return 0
    except (ValueError, KeyError, TypeError, IndexError, StopIteration, OSError, subprocess.CalledProcessError) as exc:
        text = str(exc) or "election window not open"
        print(text)
        return 3 if text.startswith("wait:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
