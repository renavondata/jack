#!/usr/bin/env python3
"""jack status: the current window's pre-stated criteria, the procedure:object ratio and the overdue forecasts, computed
from log.jsonl and the tree, so that no criterion is counted by hand (PLAN-20261030 §4; BRIEF-C1 criterion 4, A3.4, J7).
No entry, no signing, no fetch. The clock enters only as --as-of (default now); the kernel never reads it."""
import argparse
import ast
import csv
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check  # noqa: E402
from judge.judge import counted_lines, signer_blob  # noqa: E402
from tools import value as val  # noqa: E402
from tools import elect  # noqa: E402

FMT = "%Y-%m-%dT%H:%M:%SZ"
P0 = Fraction(6, 11)  # BRIEF-C1b v7; never estimated from the live window
WORKFLOW = ".github/workflows/tests.yml"
MAP = "tools/enforcement.json"


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


def c2a_window(es):
    opening = val.opening_push(es)
    v0 = next(e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and
              e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "V0")
    end = min(instant(v0["body"]["resolves_by"]), instant(opening["ts"]) + dt.timedelta(days=14))
    return opening["seq"], opening["ts"], end.strftime(FMT)


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


def item_process(es, after_seq=-1, promotion_at=None):
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
        if repair:
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


def status(es, window, days, as_of, root=ROOT, subject="C1a", rev=None):
    """The figures BRIEF-C1 evaluates on the exit prefix, on the prefix as of `as_of` (an instant string)."""
    now = instant(as_of)
    es = [e for e in es if instant(e["ts"]) <= now]
    if subject in ("C1b", "C2a", "C2b"):
        opening, start, end = {"C1b": c1b_window, "C2a": c2a_window, "C2b": elect.window}[subject](es)
        start, end = instant(start), instant(end)
        window = subject
    else:
        opened = next(e for e in es if e["type"] == "amend" and e["body"].get("id") == window)
        opening, start = opened["seq"], instant(opened["ts"])
        end = start + dt.timedelta(days=days)
    closing = next((e for e in es if promotes(e, subject)), None)
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
        "veto": any(e["type"] == "decision" and e["body"].get("kind") == "veto" and e["body"].get("subject") == subject for e in prefix),
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


VALUE_PINS = ("worked_table forecast_before_cutoff rigged revision weights_from_resolved_prefix abstention_is_base "
              "one_event_one_key grouping_by_principal uniform_prior no_learning_rate exact_probabilities per_type_base "
              "bounded_difference lambda_predictable factor_algebra window_from_the_push wealth_continues promote_refused_value").split()


def c2a_tree_evidence(root, rev, prefix, opening):
    """Check the opening's scope through every intervening tree; keep C1b's process code."""
    try:
        start = prefix_tree(root, rev, [e for e in prefix if e["seq"] <= opening])
        if start is None:
            return False, False, False
        def scope_at(sha):
            return (tree_bytes(root, sha, "judge/scope.json"),
                    tree_bytes(root, sha, "SPEC.md").split(b"at C1 it is:", 1)[1].split(b"```", 2)[1])
        original = scope_at(start)
        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", f"{start}..{rev}").decode().split())
        unchanged = unchanged and json.loads(original[0])["cap"] == 7800 and not any(
            e["type"] == "push" and e["seq"] > opening for e in prefix)
        def process_at(sha):
            nodes = ast.parse(tree_bytes(root, sha, "tools/status.py")).body
            return [ast.dump(n) for n in nodes if getattr(n, "name", None) in ("item_process", "score_items", "sovereign_keys") or
                    isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "P0" for t in n.targets)]
        same = process_at(start) == process_at(rev) and tree_bytes(root, start, "tools/clerk.py") == tree_bytes(root, rev, "tools/clerk.py")
        pins = tree_bytes(root, rev, "pins/pins.py").decode()
        registered = all(f'Pin("{name}"' in pins or f"Pin('{name}'" in pins for name in VALUE_PINS)
        return unchanged, same, registered
    except (OSError, ValueError, IndexError, subprocess.CalledProcessError):
        return False, False, False


def assess_value(s, facts, verified, root, rev, runs, acts):
    end = min(s["as_of"], s["end"])
    unchanged, same, registered = c2a_tree_evidence(root, rev, s["prefix"], s["opening"])
    gate = attack_start(root, runs, end, "tests/test_value.py")
    v = val.value(s["prefix"], as_of=end, attack_green=gate)
    live_gate = attack_start(root, runs, end)
    process = item_process(s["prefix"], c1b_window(s["prefix"])[0], end)
    live = score_items(i for i in process["items"] if live_gate is not None and live_gate < i["ts"])
    off = off_log_repairs(acts, s["start"], end)
    s.update(value=v, continued_liveness=live, late_reports=process["late_reports"])
    return [(verified and registered, "criterion 1: C2a pins and twins in verified tests run"),
            (verified, "criterion 2: checker agreement in verified tests run"),
            (facts["counted"] <= 7800 and facts["kernel"] <= 500 and facts["scope"] and unchanged,
             f"criterion 3: counted {facts['counted']}/7800; kernel {facts['kernel']}/500; scope equals SPEC and unchanged: {facts['scope'] and unchanged}"),
            (gate is not None and all(gate < r["cutoff"] for r in v["rows"]),
             f"criterion 4: attack green on main before first scored cutoff: {gate or 'unverified'}"),
            (v["E_value"] >= 20, f"criterion 5: value E {v['E_value']:.6f} >= 20"),
            (same and live_gate is not None and live["E"] >= 20 and not process["late_reports"],
             f"criterion 6: continued liveness E {live['E']} >= 20; unchanged {same}; attack {live_gate or 'unverified'}; late repairs {len(process['late_reports'])}"),
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
    if subject == "C2b":
        try:
            elect.window([e for e in es if e["ts"] <= as_of])
        except StopIteration:
            promoted = next((e for e in es if promotes(e, "C2a") and e["ts"] <= as_of), None)
            opened = promoted and any(e["type"] == "push" and e["seq"] > promoted["seq"] and e["ts"] <= as_of for e in es)
            reason = "C2b window unverified: X0 missing" if opened else "C2b has not opened: no opening push after promote C2a"
            names = ("pins and twins", "checker agreement", "counted lines and trusted bytes", "attack tests",
                     "value continued", "liveness continued", "elections witnessed", "counsel bound", "veto, off-log repairs and A3.4")
            return dict(subject=subject, start=as_of, end=as_of, as_of=as_of, prefix_last_seq=None,
                        j7_unresolved_past_due=0, j7_denominator=0, overdue=[],
                        checks=[(False, f"criterion {i}: {name}: {reason}") for i, name in enumerate(names, 1)])
    s = status(es, "A3", 14, as_of, root, subject, rev)
    facts = tree_facts(root, rev)
    verified = run_verified(run, rev) and completed_by(run, as_of)
    checks = [(verified, "criterion 1: pins and twins in verified tests run"),
              (verified, "criterion 2: checker agreement in verified tests run"),
              (facts["counted"] <= 6900 and facts["kernel"] <= 500 and facts["scope"],
               f"criterion 3: counted {facts['counted']}/6900; kernel {facts['kernel']}/500; scope equals SPEC: {facts['scope']}")]
    if subject == "C2b":
        checks = assess_election(s, facts, verified and completed_by(run, min(as_of, s["end"])), root, rev, runs)
        checks += assess_c2b_exit(s, verified and completed_by(run, min(as_of, s["end"])), root, rev, runs, acts)
        s.update(subject=subject, checks=sorted(checks, key=lambda c: int(c[1].split(":", 1)[0].split()[-1])))
        return s
    elif subject == "C2a":
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


def election_tree_evidence(root, rev, prefix, opening):
    """Opening cap, immutable trusted bytes through every intervening commit."""
    start = prefix_tree(root, rev, [e for e in prefix if e["seq"] <= opening])
    if start is None:
        return False, False
    revisions = [rev] + git_bytes(root, "rev-list", f"{start}..{rev}").decode().split()
    def protected(sha):
        return (tree_bytes(root, sha, "judge/scope.json"), tree_bytes(root, sha, WORKFLOW),
                tree_bytes(root, sha, "SPEC.md").split(b"## 10.", 1)[1],
                git_bytes(root, "ls-tree", "-r", sha, "kernel/"))
    initial = protected(start)
    c2a = prefix_tree(root, rev, [e for e in prefix if e["seq"] <= val.opening_push(prefix)["seq"]])
    unchanged = (all(protected(c) == initial for c in revisions) and c2a is not None and
                 git_bytes(root, "ls-tree", "-r", c2a, "kernel/") == initial[-1] and
                 not any(e["type"] == "push" and e["seq"] > opening for e in prefix))
    names = elect.PINS + ("push_without_read_refused read_of_this_text read_not_counsels w5_overdue_escalates "
                         "w5_escalation_history w5_done_is_an_entry w5_rows_append_only w5_inventory "
                         "workflow_steps_preserved window_from_the_push wealth_continues promote_refused").split()
    registered = tree_bytes(root, rev, "pins/pins.py").decode()
    return unchanged, all(f'Pin("{name}"' in registered or f"Pin('{name}'" in registered for name in names)


def assess_election(s, facts, verified, root, rev, runs):
    end = min(s["as_of"], s["end"])
    scope = json.loads(tree_bytes(root, rev, "judge/scope.json"))
    try:
        unchanged, registered = election_tree_evidence(root, rev, s["prefix"], s["opening"])
    except (OSError, ValueError, IndexError, subprocess.CalledProcessError):
        unchanged, registered = False, False
    rounds, errors = elect.audit(s["prefix"], elect.verify_sigma)
    rounds = [f for f in rounds if f["seq"] > s["opening"]]
    gate = attack_start(root, runs, end, "tests/test_elect.py")
    resolutions = {e["body"]["forecast"]: e for e in s["prefix"] if e["type"] == "resolution"}
    witnessed = []
    for f in rounds:
        result, r = elect.round_result(s["prefix"], f, end), resolutions.get(f["seq"])
        if (r and result["settled"] and result["settled_at"] <= r["ts"] <= f["body"]["resolves_by"] and
                r["body"]["outcome"] == result["success"] and r["proposer"] in ("builder", "reviewer")):
            witnessed.append(f["seq"])
    summary = elect.summary(s["prefix"], rounds, end)
    from tools.entry import score
    summary["invite_scores"] = [line for line in score([elect.log.canonical(e) for e in s["prefix"]]).splitlines()
                                if "election.invite" in line]
    summary["refused"] = errors
    s["election"] = summary
    return [(verified and registered, "criterion 1: C2b pins and twins in verified tests run"),
            (verified, "criterion 2: checker agreement in verified tests run"),
            (facts["counted"] <= scope["cap"] and facts["kernel"] <= 500 and facts["scope"] and unchanged,
             f"criterion 3: counted {facts['counted']}/{scope['cap']}; kernel {facts['kernel']}/500; opening trusted bytes unchanged: {unchanged}"),
            (gate is not None and all(gate < f["ts"] for f in elect.invites(s["prefix"])),
             f"criterion 4: election attacks green before first invite: {gate or 'unverified'}"),
            (len(witnessed) >= 24 and not errors, f"criterion 7: elections witnessed {len(witnessed)}/24; refused invites {len(errors)}")]


COUNSEL_PINS = ("push_without_read_refused read_of_this_text read_not_counsels w5_overdue_escalates "
                "w5_done_is_an_entry w5_rows_append_only w5_inventory w5_escalation_history").split()


def liveness_unchanged(root, rev, prefix):
    start = prefix_tree(root, rev, [e for e in prefix if e["seq"] <= val.opening_push(prefix)["seq"]])
    if start is None:
        return False
    def process(sha):
        return [ast.dump(n) for n in ast.parse(tree_bytes(root, sha, "tools/status.py")).body
                if getattr(n, "name", None) in ("item_process", "score_items", "sovereign_keys") or
                isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "P0" for t in n.targets)]
    return process(start) == process(rev)


def counsel_bound(s, verified, root, rev):
    """Read committed tick witnesses, never regenerate a missing historical escalation."""
    from tools import due
    end = min(s["as_of"], s["end"])
    try:
        pins = tree_bytes(root, rev, "pins/pins.py").decode()
        registered = all(f'Pin("{name}"' in pins or f"Pin('{name}'" in pins for name in COUNSEL_PINS)
        start = prefix_tree(root, rev, [e for e in s["prefix"] if e["seq"] <= s["opening"]])
        if start is None:
            raise ValueError("opening inventory unverified")
        text = tree_bytes(root, start, due.FILE)
        due.fold(due.rows(text))
        for sha in git_bytes(root, "rev-list", "--reverse", "--first-parent", f"{start}..{rev}").decode().split():
            current = tree_bytes(root, sha, due.FILE)
            due.unchanged(text, current)
            due.fold(due.rows(current))
            text = current
        current = tree_bytes(root, rev, due.FILE)
        due.unchanged(text, current)
        rows = due.fold(due.rows(current))
        lines, malformed = due.project(rows, s["prefix"], end)
        overdue = [r["id"] for r, line in zip(rows, lines) if r["due"] < end and
                   not line.startswith(f"W5 {r['id']} due {r['due']} {r['what']}: done seq ")]
        ticks = []
        paths = git_bytes(root, "ls-tree", "-r", "--name-only", rev, "transcripts/evidence/w5/").decode().splitlines()
        for path in paths:
            text = tree_bytes(root, rev, path).decode()
            stamps = re.findall(r"\bas[- ]of[: ]+([0-9T:+Z.-]+)", text)
            if len(stamps) != 1:
                raise ValueError(f"tick has no unique as-of: {path}")
            when = due.instant(stamps[0]).strftime(FMT)
            if when <= end:
                ticks.append((when, path, text.splitlines()))
        ticks.sort()
        missing = []
        for row in rows:
            if row["due"] >= end:
                continue
            first = next((tick for tick in ticks if tick[0] > row["due"]), None)
            marker = f"W5 {row['id']} due {row['due']} {row['what']}: "
            if first is None or not any(line.startswith(marker) and
                                       re.search(r"\bESCALATED\b", line[len(marker):]) for line in first[2]):
                missing.append(row["id"])
        ok = verified and registered and not malformed and not overdue and not missing
        return ok, (f"criterion 8: counsel bound: gate/W5 pins in verified tests {verified and registered}; "
                    f"overdue undone {overdue}; first-tick escalation missing {missing}; malformed {malformed}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.CalledProcessError) as exc:
        return False, f"criterion 8: counsel bound unverified: {exc}"


def assess_c2b_exit(s, verified, root, rev, runs, acts):
    end, prefix = min(s["as_of"], s["end"]), s["prefix"]
    try:
        gate = attack_start(root, runs, end, "tests/test_value.py")
        v = val.value(prefix, as_of=end, attack_green=gate, window_opening=s["start"])
        value_check = (v["E_value"] >= 20, f"criterion 5: value continued E {v['E_value']:.6f} >= 20")
        s["value"] = v
    except (StopIteration, OSError, ValueError, subprocess.CalledProcessError) as exc:
        value_check = (False, f"criterion 5: value continued unverified: {exc}")
    try:
        gate = attack_start(root, runs, end)
        process = item_process(prefix, c1b_window(prefix)[0], end)
        live = score_items(i for i in process["items"] if gate is not None and gate < i["ts"])
        same = liveness_unchanged(root, rev, prefix)
        s.update(continued_liveness=live, late_reports=process["late_reports"])
        live_check = (same and gate is not None and live["E"] >= 20 and not process["late_reports"],
                      f"criterion 6: liveness continued E {live['E']} >= 20; unchanged {same}; "
                      f"attack {gate or 'unverified'}; late repairs {len(process['late_reports'])}")
    except (StopIteration, OSError, ValueError, subprocess.CalledProcessError) as exc:
        live_check = (False, f"criterion 6: liveness continued unverified: {exc}")
    off = off_log_repairs(acts, s["start"], end)
    procedure = s["procedure"] + int(not any(promotes(e, "C2b") for e in prefix))
    return [value_check, live_check, counsel_bound(s, verified, root, rev),
            (not s["veto"] and off == 0 and procedure <= 5 * s["object"],
             f"criterion 9: veto on C2b: {'YES' if s['veto'] else 'none'}; "
             f"off-log repairs: {off if off is not None else 'unknown (no acts file)'}; "
             f"A3.4 at promote {procedure} : {s['object']} (maximum 5:1)")]


def unmet(s):
    return [text for ok, text in s["checks"] if not ok]


def promotion_line(s):
    failures = unmet(s)
    return f"promote {s['subject']}: " + ("refused: " + "; ".join(failures) if failures else "lawful")


def render(s):
    lines = [f"window {s['subject']}: {s['start']} .. {s['end']} (as of {s['as_of']}; prefix to seq {s['prefix_last_seq']})"]
    lines += [text + (" met" if ok else " STOP" if text.startswith("A3.4") else " SHORT") for ok, text in s["checks"]]
    lines += [f"map {k}: {v['principle']} | {v['enforcer']}" for k, v in sorted(s.get("map", {}).items())]
    lines += [f"J7: {s['j7_unresolved_past_due']} of {s['j7_denominator']} window forecasts unresolved past resolves_by"]
    lines += [f"overdue forecast {seq} ({who}) due {by}; evidence {ev or '-'}" for by, seq, who, ev in s["overdue"]]
    if "value" in s and "continued_liveness" in s:
        v, live = s["value"], s["continued_liveness"]
        weights = v["window_weights"]
        below = ", ".join(k for k in weights if weights[k] < weights["base"]) or "none"
        lines += [f"value: E {v['E_value']:.6f} over {v['events']} events; window events {v['window_events']}",
                  "elections: " + " / ".join(f"{k} {float(w):.6f}" for k, w in weights.items()) + f"; below base: {below}",
                  f"liveness continued: E {live['E']} over {len(live['items'])} items (including projected expiries)"]
    if "election" in s:
        lines.append(elect.summary_line(s["election"]))
    lines = s.get("history", []) + lines
    return "\n".join(lines + s.get("repairs", []) + [promotion_line(s)])


def parser(description):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--log", default=os.path.join(ROOT, "log.jsonl"), help="kernel-checked log (default repository log.jsonl)")
    ap.add_argument("--root", default=ROOT, help="local git repository for tree/history evidence (default this repository)")
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).strftime(FMT), help="UTC YYYY-MM-DDTHH:MM:SSZ; default now")
    ap.add_argument("--subject", choices=("C1a", "C1b", "C2a", "C2b"), help="status defaults to the latest opened window")
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
                 any(promotes(e, w) for w in ("C1a", "C1b", "C2a", "C2b"))]
    closing = next((e for e in decisions if promotes(e, context["subject"])), None)
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
    from tools import clerk, due
    ap = parser(__doc__)
    ap.add_argument("--json", action="store_true", help="structured status, exact fractions encoded as strings")
    ap.add_argument("--inventory", metavar="COMMIT", help="W5 opening inventory commit")
    a = ap.parse_args(argv)
    try:
        context = inputs(a)
        if a.subject is None and any(e["type"] == "push" and e["seq"] > 337 for e in context["es"]):
            context["subject"] = "C2a"
            if any(promotes(e, "C2a") for e in context["es"]):
                context["subject"] = "C2b"
        s = report(**context)
        print(json.dumps(s, indent=1, default=str) if a.json else render(s).rsplit("\n", 1)[0])
        if not a.json:
            try:
                precedents = tree_bytes(a.root, context["rev"], "transcripts/COUNSEL-OPEN.md").decode()
            except (FileNotFoundError, subprocess.CalledProcessError):
                precedents = ""
            es, runs = context["es"], context["runs"]
            forecasts = clerk.forecast_writs(es, runs, a.as_of) if s["subject"] == "C1b" else []
            print(clerk.render(forecasts + clerk.merge_writs(es, runs, a.as_of, s["end"], precedents) +
                               clerk.window_writs(es, s, a.as_of)))
            result = due.main(["--root", a.root, "--rev", context["rev"], "--as-of", a.as_of] +
                              (["--inventory", a.inventory] if a.inventory else []))
            if result == 0:
                print(promotion_line(s))
            return result
    except (StopIteration, OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"status unverified: {exc or 'window opening or L0 missing'}")


if __name__ == "__main__":
    raise SystemExit(main())
