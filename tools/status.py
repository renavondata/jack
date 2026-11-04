#!/usr/bin/env python3
"""jack status: the current window's pre-stated criteria, the procedure:object ratio and the overdue forecasts, computed
from log.jsonl and the tree, so that no criterion is counted by hand (PLAN-20261030 §4; BRIEF-C1 criterion 4, A3.4, J7).
No entry, no signing, no fetch. The clock enters only as --as-of (default now); the kernel never reads it."""
import argparse
import ast
import csv
import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check  # noqa: E402
from judge.judge import counted_lines, signer_blob  # noqa: E402
from tools import value as val  # noqa: E402

FMT = "%Y-%m-%dT%H:%M:%SZ"
P0 = Fraction(6, 11)  # BRIEF-C1b v7; never estimated from the live window
WORKFLOW = ".github/workflows/tests.yml"
MAP = "tools/enforcement.json"
C2A_PRIME_CAP = 8400
WINDOW_FIX_FUNCTIONS = ("decision_window", "fix_window", "carrying_commit", "attributed_failure", "window_fix_seqs")


def sovereign_keys(es):
    return {d["pubkey"].split()[1] for d in es[0]["body"]["keys"]}


def c1b_window(es):
    """The opening's seq breaks timestamp ties; only the named L0 supplies the maximum."""
    opening = next(e for e in es if e["type"] == "decision" and
                   promotes(e, "C1a"))
    l0 = next(e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and
              e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "L0")
    return opening["seq"], opening["ts"], l0["body"]["resolves_by"]


def promotes(e, subject):
    return e["type"] == "decision" and e["body"].get("kind") == "promote" and e["body"].get("subject") == subject


def c2a_window(es, late=False):
    opening = val.opening_push(es)
    v0 = next(e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and
              e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "V0")
    end = instant(v0["body"]["resolves_by"])
    if not late:
        end = min(end, instant(opening["ts"]) + dt.timedelta(days=14))
    return opening["seq"], opening["ts"], end.strftime(FMT)


def second_opening(es):
    end = c2a_window(es, late=True)[2]
    if not any(promotes(e, "C2a") and e["ts"] <= end for e in es):
        return next((e for e in es if e["type"] == "push" and e["ts"] > end), None)


def decision_window(e, es):
    name = e["body"].get("subject")
    if name == "C2a" or name == "C2a-prime" and e["body"].get("kind") == "veto":
        opening = second_opening(es)
        return "C2a-prime" if opening and e["ts"] > opening["ts"] else "C2a" if name == "C2a" else None
    return None if name == "C2a-prime" else name


def prime_window(es):
    opening = second_opening(es)
    if opening is None:
        raise ValueError("C2a-prime opening missing")
    v5 = next((e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and
               e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "V5"), None)
    if v5 is None:
        raise ValueError("C2a-prime has no promotion forecast before its opening")
    return opening["seq"], opening["ts"], v5["body"]["resolves_by"]


def fix_window(es, name, late=False):
    if name == "C2a":
        return c2a_window(es, late=late)
    if name == "C2a-prime":
        return prime_window(es)
    if name == "C1b":
        return c1b_window(es)
    if name == "C1a":
        opening = next(e for e in es if e["type"] == "amend" and e["body"].get("id") == "A3")
        return opening["seq"], opening["ts"], (instant(opening["ts"]) + dt.timedelta(days=14)).strftime(FMT)
    if name == "C2b":
        promotion = next(e for e in es if promotes(e, "C2a"))
        opening = next(e for e in es if e["type"] == "push" and e["seq"] > promotion["seq"])
        x7 = next(e for e in es if e["type"] == "forecast" and e["seq"] < opening["seq"] and
                  e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "X7")
        end = instant(x7["body"]["resolves_by"])
        if not late:
            end = min(end, instant(opening["ts"]) + dt.timedelta(days=14))
        return opening["seq"], opening["ts"], end.strftime(FMT)
    raise ValueError("no pre-stated window bounds for " + name)


def carrying_commit(root, rev, entry, first_parent=False):
    """Entry identity in all parents, not the latest tree with the same log prefix."""
    if git_bytes(root, "rev-parse", "--is-shallow-repository").strip() == b"true":
        raise ValueError("complete carrying-commit history missing")
    def holds(sha):
        if not git_bytes(root, "ls-tree", sha, "log.jsonl"):
            return False
        return entry in map(json.loads, tree_bytes(root, sha, "log.jsonl").splitlines())
    for row in git_bytes(root, "rev-list", "--parents", *(["--first-parent"] if first_parent else []), rev).decode().splitlines():
        sha, *parents = row.split()
        if holds(sha) and not any(holds(p) for p in (parents[:1] if first_parent else parents)):
            return sha
    raise ValueError("carrying commit missing")


def attributed_failure(root, rev, subject, start, end):
    paths = git_bytes(root, "ls-tree", "-r", "--name-only", rev, "transcripts/evidence/").decode().splitlines()
    named = [p for p in paths if p.endswith(".csv") and not p.endswith("-raw.csv") and os.path.basename(p)[:-4] in subject]
    if not named:
        raise ValueError("named attributed acts file missing at carrying commit")
    for path in named:
        tree_bytes(root, rev, path[:-4] + "-raw.csv")
        tokens = tree_bytes(root, rev, path[:-4] + "-classifier.sha256").split()
        if not tokens or hashlib.sha256(tree_bytes(root, rev, "transcripts/evidence/guy_acts3.py")).hexdigest().encode() != tokens[0]:
            continue
        try:
            reader = csv.DictReader(io.StringIO(tree_bytes(root, rev, path).decode()), strict=True)
            rows = list(reader) if reader.fieldnames == "repo,time_hkt,class,kind,ref,note".split(",") else []
            if any(None in r or None in r.values() for r in rows):
                continue
            minutes = [dt.datetime.strptime(r["time_hkt"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone(dt.timedelta(hours=8)))
                       for r in rows if r["repo"] == "renavondata/jack" and r["class"] == "repair"]
            if any(instant(start) <= t and t + dt.timedelta(seconds=60) <= instant(end) for t in minutes):
                return True
        except (UnicodeError, csv.Error, ValueError):
            pass  # An unparsable attributed table holds no row.
    return False


def window_fix_seqs(es, root, rev):
    qualified, seen = set(), set()
    for e in es:
        if e["type"] != "decision" or e["body"].get("kind") != "fix":
            continue
        name, colon, _ = e["body"]["subject"].partition(":")
        if not colon:
            continue
        first = name not in seen
        seen.add(name)
        if not first or signer_blob(e) not in sovereign_keys(es):
            continue
        try:
            _, start, end = fix_window(es, name)
            late = fix_window(es, name, late=True)[2]
            closing = [d for d in es if d["type"] == "decision" and d["ts"] <= late and decision_window(d, es) == name]
            following = next((p for p in es if p["type"] == "push" and p["ts"] > late), None)
            if e["ts"] <= late or following and e["seq"] >= following["seq"] or any(d["body"]["kind"] == "promote" for d in closing):
                continue
            carrier = carrying_commit(root, rev, e)
            if any(d["body"]["kind"] == "veto" and d["ts"] <= end for d in closing) or attributed_failure(root, carrier, e["body"]["subject"], start, end):
                qualified.add(e["seq"])
        except (OSError, ValueError, StopIteration, TypeError, subprocess.CalledProcessError) as exc:
            print(f"window fix {e['seq']}: unverified — {exc or 'window bounds missing'}", file=sys.stderr)
    return qualified


def score_items(items):
    """The live and historical item projection: exact A4.3 rows and terminal wealth."""
    result, successes, capital = [], 0, Fraction(1)
    for n, item in enumerate(items):
        q = Fraction(successes + 1, n + 2)
        stake = max(Fraction(0), (q - P0) / (P0 * (1 - P0)))
        capital *= 1 + stake * (item["Y"] - P0)
        result.append(dict(item, stake=stake, E=capital))
        successes += item["Y"]
    return {"items": result, "E": capital}


def item_process(es, after_seq=-1, promotion_at=None, window_fixes=()):
    """BRIEF-C1b §Liveness (i)-(iv), in entry order. No clock-created or regrouped items.

    `after_seq` is the first window's opening, not the latest restart: A4 wealth continues.
    `promotion_at` optionally projects expiries at a proposed promotion, without entering it.
    Callers supply a prefix ending at the observation instant. Resolved writs leave the open
    set immediately; a sovereign boundary clears pending resolutions without reopening them.
    """
    sovereign = sovereign_keys(es)
    opened, pending, items, late_reports = {}, [], [], []

    def finalise(e, kind, members, success):
        repairs = tuple(sorted({r for _, rs in members for r in rs}))
        items.append({"seq": e["seq"], "ts": e["ts"], "kind": kind,
                      "forecasts": tuple(f for f, _ in members), "repairs": repairs,
                      "Y": int(success and not repairs)})

    def expire(e):
        for f in sorted(opened):
            forecast, repairs = opened[f]
            if forecast["body"]["resolves_by"] < e["ts"]:
                finalise(e, "expiry", [(f, repairs)], False)
                del opened[f]
    for e in es:
        seq, body, typ = e["seq"], e["body"], e["type"]
        expire(e)
        royal = signer_blob(e) in sovereign
        repair = royal and typ not in ("genesis", "key", "amend", "push", "proposal") and not (
            typ == "decision" and body["kind"] != "fix")
        if repair and seq not in window_fixes:
            if items:
                late_reports.append(seq)
            for _, repairs in opened.values():
                repairs.append(seq)
        if typ == "forecast" and seq > after_seq:
            opened[seq] = (e, [])
        if typ == "resolution" and body["forecast"] in opened:
            f = body["forecast"]
            _, repairs = opened.pop(f)
            if royal:
                finalise(e, "sovereign resolution", [(f, repairs)], False)
            else:
                pending.append((f, repairs))
        if typ == "merge" and pending:
            finalise(e, "batch", sorted(pending), not royal)
        if typ == "merge" or royal:
            pending = []
    if promotion_at is not None:
        expire({"seq": es[-1]["seq"] + 1, "ts": promotion_at})
    return dict(score_items(items), late_reports=late_reports)


def instant(s):
    return dt.datetime.strptime(s, FMT).replace(tzinfo=dt.timezone.utc)


def evidence_ok(root, ev, rev=None):
    """True iff `ev` is sha256:<hex64> naming transcripts/evidence/<hex64> whose SHA-256 is that value."""
    if not (isinstance(ev, str) and ev.startswith("sha256:") and len(ev) == 71):
        return False
    path = "transcripts/evidence/" + ev[7:]
    try:
        return hashlib.sha256(tree_bytes(root, rev, path)).hexdigest() == ev[7:]
    except (OSError, subprocess.CalledProcessError):
        return False


def status(es, window, days, as_of, root=ROOT, subject="C1a", rev=None, decision=None):
    """The figures BRIEF-C1 evaluates on the exit prefix, on the prefix as of `as_of` (an instant string)."""
    now = instant(as_of)
    es = [e for e in es if instant(e["ts"]) <= now]
    if subject in ("C1b", "C2a"):
        prime = subject == "C2a" and second_opening(es) is not None and (decision is None or decision_window(decision, es) == "C2a-prime")
        opening, start, end = (prime_window if prime else c2a_window if subject == "C2a" else c1b_window)(es)
        start, end = instant(start), instant(end)
        window = "C2a-prime" if prime else subject
    else:
        opened = next(e for e in es if e["type"] == "amend" and e["body"].get("id") == window)
        opening, start = opened["seq"], instant(opened["ts"])
        end = start + dt.timedelta(days=days)
    closing = next((e for e in es if promotes(e, subject) and decision_window(e, es) == (window if subject == "C2a" else subject)), None)
    if closing:
        end = min(end, instant(closing["ts"]))
    prefix = [e for e in es if instant(e["ts"]) <= end and (not closing or e["seq"] <= closing["seq"])]
    inw = [e for e in prefix if e["seq"] > opening or (subject == "C1a" and e["seq"] == opening)]
    world = {e["seq"] for e in es if e["type"] == "forecast" and str(e["body"].get("type", "")).startswith("world.")}
    resolved = {e["body"]["forecast"]: e for e in prefix if e["type"] == "resolution"}
    fc = [e for e in inw if e["type"] == "forecast"]
    rs = [e for e in inw if e["type"] == "resolution"]
    wrs = [e for e in rs if e["body"]["forecast"] in world]
    objects = sum(1 for e in inw if (e["type"] == "forecast" and e["seq"] in world) or (e["type"] == "resolution" and e["body"]["forecast"] in world))
    late = [e for e in fc if e["seq"] not in resolved and instant(e["body"]["resolves_by"]) < now]
    overdue = sorted((e["body"]["resolves_by"], e["seq"], e["proposer"], (e["body"].get("args") or {}).get("evidence", ""))
                     for e in es if e["type"] == "forecast" and e["seq"] not in resolved and instant(e["body"]["resolves_by"]) < now)
    return {
        "window": window, "start": start.strftime(FMT), "end": end.strftime(FMT), "as_of": as_of,
        "prefix_last_seq": prefix[-1]["seq"] if prefix else None, "entries_in_window": len(inw),
        "forecasts": len(fc), "proposers": sorted({e["proposer"] for e in fc}),
        "resolutions": len(rs), "world_resolutions": len(wrs),
        "world_resolutions_with_evidence": sum(1 for e in wrs if evidence_ok(root, e["body"]["evidence"], rev)),
        "procedure": len(inw) - objects, "object": objects,
        "veto": (any(e["type"] == "decision" and e["body"].get("kind") == "veto" and e["body"].get("subject") == subject for e in prefix)
                 if subject != "C2a" else any(e["type"] == "decision" and e["body"].get("kind") == "veto" and decision_window(e, es) == window for e in prefix)),
        "j7_unresolved_past_due": len(late), "j7_denominator": len(fc),
        "overdue": overdue,
        "opening": opening, "prefix": prefix,
    }


def git_bytes(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, check=True).stdout


def tree_bytes(root, rev, path):
    if rev is not None:
        return git_bytes(root, "show", f"{rev}:{path}")
    with open(os.path.join(root, path), "rb") as f:
        return f.read()


def tree_facts(root, rev):
    scope = json.loads(tree_bytes(root, rev, "judge/scope.json"))
    block = tree_bytes(root, rev, "SPEC.md").decode().split("at C1 it is:", 1)[1].split("```", 2)[1]
    return {"counted": counted_lines(root, rev, scope["counted"]),
            "kernel": counted_lines(root, rev, ["kernel/"]), "scope": scope == json.loads(block)}


def run_verified(run, sha):
    return isinstance(run, dict) and all(run.get(k) == v for k, v in (
        ("path", WORKFLOW), ("event", "push"), ("head_branch", "main"), ("head_sha", sha), ("conclusion", "success")))


def completed_by(run, when):
    try:
        return instant(run["updated_at"]) <= instant(when)
    except (KeyError, TypeError, ValueError):
        return False


def attack_start(root, runs, as_of, path="tests/test_clerk.py"):
    """A tests run counts only if its committed tree actually includes the clerk attack test."""
    times = []
    for run in runs:
        if run.get("head_sha") and run_verified(run, run["head_sha"]) and completed_by(run, as_of):
            try:
                if tree_bytes(root, run["head_sha"], path):
                    times.append(run["updated_at"])
            except subprocess.CalledProcessError:
                pass  # a missing object/file is no witness; this tool never fetches
    return min(times, default=None)


def off_log_repairs(acts, start, end):
    if acts is None:
        return None
    hkt = dt.timezone(dt.timedelta(hours=8))  # counsel's weekly CSV contract
    return sum(row["repo"] == "renavondata/jack" and row["class"] == "repair" and
               instant(start) <= dt.datetime.strptime(row["time_hkt"], "%Y-%m-%d %H:%M").replace(tzinfo=hkt) <= instant(end)
               for row in acts)


# Awaiting the reviewer's registration; add these to VALUE_PINS when registered.
C2A_PRIME_PINS = ("second_window_from_the_end second_window_end_is_v5 second_window_cap offlog_from_second_opening "
                  "promote_refused_before_end window_fix_is_decision process_unchanged_from_window_code").split()
VALUE_PINS = ("worked_table forecast_before_cutoff rigged revision weights_from_resolved_prefix abstention_is_base "
              "one_event_one_key grouping_by_principal uniform_prior no_learning_rate exact_probabilities per_type_base "
              "bounded_difference lambda_predictable factor_algebra window_from_the_push wealth_continues promote_refused_value").split()


def c2a_tree_evidence(root, rev, prefix, opening, prime=False):
    """Check the opening's scope through every intervening tree; keep C1b's process code."""
    try:
        start = (carrying_commit(root, rev, next(e for e in prefix if e["seq"] == opening), first_parent=True)
                 if prime else prefix_tree(root, rev, [e for e in prefix if e["seq"] <= opening]))
        if start is None:
            return False, False, False
        def scope_at(sha):
            return (tree_bytes(root, sha, "judge/scope.json"),
                    tree_bytes(root, sha, "SPEC.md").split(b"at C1 it is:", 1)[1].split(b"```", 2)[1])
        original = scope_at(start)
        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", f"{start}..{rev}").decode().split())
        unchanged = unchanged and json.loads(original[0])["cap"] == (C2A_PRIME_CAP if prime else 7800) and not any(
            e["type"] == "push" and e["seq"] > opening for e in prefix)
        process_start = start
        if prime:
            process_start = None
            for e in (e for e in prefix if e["type"] == "merge" and e["seq"] > opening):
                ancestors = git_bytes(root, "rev-list", e["body"]["commit"]).decode().splitlines()
                if any(p["type"] == "proposal" and p["body"]["title"].startswith("C2a-prime window code") and
                       p["body"]["commit"] in ancestors for p in prefix):
                    process_start = carrying_commit(root, rev, e, first_parent=True)
                    break
        def process_at(sha, window_code=False):
            module = ast.parse(tree_bytes(root, sha, "tools/status.py"))
            nodes = module.body
            names = {"score_items", "sovereign_keys"} | (set() if prime else {"item_process"})
            constants = {"P0"}
            if window_code:
                functions = {n.name: n for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
                declaration = next(n for n in nodes if isinstance(n, ast.Assign) and
                                   any(isinstance(t, ast.Name) and t.id == "WINDOW_FIX_FUNCTIONS" for t in n.targets))
                roots = set(ast.literal_eval(declaration.value))
                names, pending, constants = {"item_process"}, roots, {"WINDOW_FIX_FUNCTIONS"}
                while pending:
                    names |= pending
                    pending = {n.id for name in pending for n in ast.walk(functions[name])
                               if isinstance(n, ast.Name) and n.id in functions} - names
                names |= {name for name, function in functions.items() if any(isinstance(n, ast.Call) and
                          (isinstance(n.func, ast.Name) and n.func.id in roots | {"item_process"} or
                           isinstance(n.func, ast.Attribute) and n.func.attr in roots | {"item_process"}) for n in ast.walk(function))}
            return [ast.dump(n) for n in nodes if getattr(n, "name", None) in names or
                    isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants for t in n.targets)]
        same = None if process_start is None else (process_at(start) == process_at(rev) and
               (not prime or process_at(process_start, True) == process_at(rev, True)) and
               tree_bytes(root, start, "tools/clerk.py") == tree_bytes(root, rev, "tools/clerk.py"))
        pins = tree_bytes(root, rev, "pins/pins.py").decode()
        registered = all(f'Pin("{name}"' in pins or f"Pin('{name}'" in pins for name in VALUE_PINS if prime or name not in C2A_PRIME_PINS)
        return unchanged, same, registered
    except (OSError, ValueError, IndexError, KeyError, StopIteration, SyntaxError, subprocess.CalledProcessError):
        return False, False, False


def assess_value(s, facts, verified, root, rev, runs, acts):
    end = min(s["as_of"], s["end"])
    prime = s["window"] == "C2a-prime"
    cap = C2A_PRIME_CAP if prime else 7800
    unchanged, same, registered = c2a_tree_evidence(root, rev, s["prefix"], s["opening"], prime)
    gate = attack_start(root, runs, end, "tests/test_value.py")
    v = val.value(s["prefix"], as_of=end, attack_green=gate)
    live_gate = attack_start(root, runs, end)
    fixes = window_fix_seqs(s["prefix"], root, rev)
    process = item_process(s["prefix"], c1b_window(s["prefix"])[0], end, fixes)
    live = score_items(i for i in process["items"] if live_gate is not None and live_gate < i["ts"])
    off = off_log_repairs(acts, s["start"], end)
    same_text = ": pending the window code's merge" if same is None else " " + str(same)
    s.update(value=v, continued_liveness=live, late_reports=process["late_reports"])
    if prime:
        s["fix_typings"] = [f"window fix {e['seq']}: repair before window code; {'decision' if e['seq'] in fixes else 'repair'} after window code"
                            for e in s["prefix"] if e["type"] == "decision" and e["body"].get("kind") == "fix" and signer_blob(e) in sovereign_keys(s["prefix"])]
    return [(verified and registered, "criterion 1: C2a pins and twins in verified tests run"),
            (verified, "criterion 2: checker agreement in verified tests run"),
            (facts["counted"] <= cap and facts["kernel"] <= 500 and facts["scope"] and unchanged,
             f"criterion 3: counted {facts['counted']}/{cap}; kernel {facts['kernel']}/500; scope equals SPEC and unchanged: {facts['scope'] and unchanged}"),
            (gate is not None and all(gate < r["cutoff"] for r in v["rows"]),
             f"criterion 4: attack green on main before first scored cutoff: {gate or 'unverified'}"),
            (v["E_value"] >= 20, f"criterion 5: value E {v['E_value']:.6f} >= 20"),
            (same and live_gate is not None and live["E"] >= 20 and not process["late_reports"],
             f"criterion 6: continued liveness E {live['E']} >= 20; unchanged{same_text}; attack {live_gate or 'unverified'}; late repairs {len(process['late_reports'])}"),
            (off == 0, f"criterion 7: off-log repairs: {off if off is not None else 'unknown (no acts file)'}")]


def assess(es, subject, as_of, root, rev, run=None, runs=(), acts=None, mapping=None, decision=None):
    """One assessment for live status and a promotion's own prefix, tree and instant."""
    if decision is not None:
        es = [e for e in es if e["seq"] <= decision["seq"]]
        as_of, subject = decision["ts"], decision["body"]["subject"]
        rev = prefix_tree(root, rev, es[:-1])
        if rev is None:
            raise ValueError("historical tree unverified")
        run = next((r for r in runs if run_verified(r, rev) and completed_by(r, as_of)), None)
        mapping = None
    s = status(es, "A3", 14, as_of, root, subject, rev, decision)
    facts = tree_facts(root, rev)
    verified = run_verified(run, rev) and completed_by(run, as_of)
    checks = [(verified, "criterion 1: pins and twins in verified tests run"),
              (verified, "criterion 2: checker agreement in verified tests run"),
              (facts["counted"] <= 6900 and facts["kernel"] <= 500 and facts["scope"],
               f"criterion 3: counted {facts['counted']}/6900; kernel {facts['kernel']}/500; scope equals SPEC: {facts['scope']}")]
    if subject == "C2a":
        checks = assess_value(s, facts, verified, root, rev, runs, acts)
    elif subject == "C1b":
        process = item_process(s["prefix"], s["opening"])
        proposed = item_process(s["prefix"], s["opening"], min(as_of, s["end"]))
        gate = attack_start(root, runs, as_of)
        checks.append((gate is not None and all(gate < i["ts"] for i in proposed["items"]),
                       f"criterion 4: attack green on main before first item: {gate or 'unverified'}"))
        live, exit_ = [score_items(i for i in p["items"] if gate is not None and gate < i["ts"])
                       for p in (process, proposed)]
        s.update(live, late_reports=process["late_reports"], promotion_E=exit_["E"])
        checks.append((s["E"] >= 20 and s["promotion_E"] >= 20,
                       f"criterion 5: live E {s['E']} >= 20; items {len(s['items'])}; at promote E {s['promotion_E']}"))
        if mapping is None:
            try:
                mapping = json.loads(tree_bytes(root, rev, MAP))
            except (OSError, subprocess.CalledProcessError):
                mapping = {}
        s["map"] = mapping
        checks.append((all(mapping.get(k, {}).get("enforcer", "").startswith("code:") for k in ("W1", "W3", "W4", "A5")),
                       "criterion 7: C1b enforcement map rows code"))
        n = len(process["late_reports"])
        checks.append((n == 0, f"late-reported repairs: {n}"))
        off = off_log_repairs(acts, s["start"], min(s["end"], as_of))
        checks.append((off == 0, f"off-log repairs: {off if off is not None else 'unknown (no acts file)'}"))
    else:
        checks.extend([(s["forecasts"] >= 20 and len(s["proposers"]) >= 3 and s["resolutions"] >= 10 and
                        s["world_resolutions_with_evidence"] >= 5,
                        f"criterion 4: forecasts {s['forecasts']}/20; proposers {len(s['proposers'])}/3; "
                        f"resolutions {s['resolutions']}/10; world-typed with evidence {s['world_resolutions_with_evidence']}/5"),
                       (verified, "criterion 5: score vectors in verified tests run")])
    checks.append((not s["veto"], f"criterion {7 if subject == 'C2a' else 6}: veto on {subject}: {'YES' if s['veto'] else 'none'}"))
    exit_procedure = s["procedure"] + int(not any(promotes(e, subject) for e in s["prefix"]))
    checks.append((exit_procedure <= 5 * s["object"], f"A3.4 ratio: procedure {s['procedure']} : object {s['object']}; "
                   f"at promote {exit_procedure} : {s['object']} (maximum 5:1)"))
    s.update(subject=subject, checks=checks)
    return s


def prefix_tree(root, head, prefix):
    """Find the last ancestor with exactly the pre-decision log, never today's replacement tree."""
    for sha in git_bytes(root, "rev-list", "--first-parent", head).decode().splitlines():
        try:
            entries = [json.loads(line) for line in tree_bytes(root, sha, "log.jsonl").splitlines()]
        except subprocess.CalledProcessError:
            continue
        if entries == prefix:
            return sha
    return None


def unmet(s):
    return [text for ok, text in s["checks"] if not ok]


def promotion_line(s):
    failures = unmet(s)
    return f"promote {s['subject']}: " + ("refused: " + "; ".join(failures) if failures else "lawful")


def render(s):
    lines = [f"window {s['subject']}: {s['start']} .. {s['end']} (as of {s['as_of']}; prefix to seq {s['prefix_last_seq']})"]
    if s.get("window") == "C2a-prime":
        lines.append(f"window: C2a-prime (second window of C2a, opened seq {s['opening']})")
        lines += s.get("fix_typings", [])
    lines += [text + (" met" if ok else " STOP" if text.startswith("A3.4") else " SHORT") for ok, text in s["checks"]]
    lines += [f"map {k}: {v['principle']} | {v['enforcer']}" for k, v in sorted(s.get("map", {}).items())]
    lines += [f"J7: {s['j7_unresolved_past_due']} of {s['j7_denominator']} window forecasts unresolved past resolves_by"]
    lines += [f"overdue forecast {seq} ({who}) due {by}; evidence {ev or '-'}" for by, seq, who, ev in s["overdue"]]
    if "value" in s:
        v, live = s["value"], s["continued_liveness"]
        weights = v["window_weights"]
        below = ", ".join(k for k in weights if weights[k] < weights["base"]) or "none"
        lines += [f"value: E {v['E_value']:.6f} over {v['events']} events; window events {v['window_events']}",
                  "elections: " + " / ".join(f"{k} {float(w):.6f}" for k, w in weights.items()) + f"; below base: {below}",
                  f"liveness continued: E {live['E']} over {len(live['items'])} items (including projected expiries)"]
    lines = s.get("history", []) + lines
    return "\n".join(lines + s.get("repairs", []) + [promotion_line(s)])


def parser(description):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--log", default=os.path.join(ROOT, "log.jsonl"), help="kernel-checked log (default repository log.jsonl)")
    ap.add_argument("--root", default=ROOT, help="local git repository for tree/history evidence (default this repository)")
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).strftime(FMT), help="UTC YYYY-MM-DDTHH:MM:SSZ; default now")
    ap.add_argument("--subject", choices=("C1a", "C1b", "C2a"), help="status defaults to the latest opened window")
    ap.add_argument("--run", metavar="FILE", help="one Actions workflow-run JSON object for HEAD: tests.yml path, push event, main branch, "
                    "exact SHA, success conclusion, updated_at by as-of; absent leaves criteria 1/2 unverified")
    ap.add_argument("--runs", metavar="FILE", help="JSON array of Actions workflow_runs: historical promotion, attack and W3 witnesses; default empty")
    ap.add_argument("--acts", metavar="FILE", help="weekly CSV saved under transcripts/evidence/: repo,time_hkt,class,kind,ref,note; "
                    "time_hkt is YYYY-MM-DD HH:MM UTC+8; absent means off-log repairs unknown")
    ap.add_argument("--map", metavar="FILE", help=f"enforcement-map JSON object (default {MAP} at assessed commit); rows have principle/enforcer")
    ap.epilog = ("C1b opens at decision promote C1a and ends at L0's resolves_by or promote C1b. Tree facts use committed HEAD; "
                 "historical promotions use their pre-decision tree and contemporaneous runs. Promotion also projects newly due expiries "
                 "and the procedure entry at as-of. W3 accepts only tests.yml, matching commit, success, updated_at <= merge entry ts.")
    return ap


def inputs(a):
    with open(a.log, "rb") as f:
        lines = check.read_lines(f.read())
    if not check.check(lines)["ok"]:
        raise SystemExit("the log is refused by the kernel")
    es = [json.loads(line) for line in lines if json.loads(line)["ts"] <= a.as_of]
    def load(path, default):
        if not path:
            return default
        with open(path) as f:
            return json.load(f)
    run, runs, mapping = load(a.run, None), load(a.runs, []), load(a.map, None)
    if not isinstance(runs, list) or not all(isinstance(r, dict) for r in runs):
        raise ValueError("--runs must be a JSON array of workflow-run objects")
    if isinstance(run, dict):
        runs = runs + [run]
    acts = None
    if a.acts:
        with open(a.acts, newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != "repo,time_hkt,class,kind,ref,note".split(","):
                raise ValueError("--acts header must be repo,time_hkt,class,kind,ref,note")
            acts = list(reader)
    head = git_bytes(a.root, "rev-parse", "HEAD").decode().strip()
    subject = a.subject or ("C1b" if any(promotes(e, "C1a") for e in es) else "C1a")
    return dict(es=es, rev=head, subject=subject, as_of=a.as_of, root=a.root, run=run, runs=runs, acts=acts, mapping=mapping)


def report(**context):
    decisions = [e for e in context["es"] if e["ts"] <= context["as_of"] and
                 any(promotes(e, w) for w in ("C1a", "C1b", "C2a"))]
    current = "C2a-prime" if context["subject"] == "C2a" and second_opening(context["es"]) else context["subject"]
    closing = next((e for e in decisions if promotes(e, context["subject"]) and decision_window(e, context["es"]) == current), None)
    s = assess(**context, decision=closing)
    s["repairs"] = []
    for e in decisions:
        try:
            historical = s if e == closing else assess(**context, decision=e)
            failures = unmet(historical)
            if s["subject"] == "C2a" and promotes(e, "C1b"):
                s.setdefault("history", []).append("C1b history:\n" + render(historical))
        except (StopIteration, OSError, ValueError, subprocess.CalledProcessError):
            failures = ["historical criteria unverified"]
        if failures:
            s["repairs"].append(f"sovereign REPAIR: promote {e['body']['subject']} seq {e['seq']}: " + "; ".join(failures))
    return s


def main(argv=None):
    ap = parser(__doc__)
    ap.add_argument("--json", action="store_true", help="structured status, exact fractions encoded as strings")
    a = ap.parse_args(argv)
    try:
        context = inputs(a)
        if a.subject is None and any(e["type"] == "push" and e["seq"] > 337 for e in context["es"]):
            context["subject"] = "C2a"
        s = report(**context)
        print(json.dumps(s, indent=1, default=str) if a.json else render(s))
    except (StopIteration, OSError, ValueError, subprocess.CalledProcessError) as exc:
        if str(exc) == "C2a-prime has no promotion forecast before its opening":
            print(f"promote C2a: refused: {exc}")
            return
        raise SystemExit(f"status unverified: {exc or 'window opening or L0 missing'}")


if __name__ == "__main__":
    main()
