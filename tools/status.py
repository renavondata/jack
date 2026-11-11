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


def c2a_v0(es):
    opening = val.opening_push(es)
    v0 = next(e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and
              e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "V0")
    return opening, v0


def c2a_window(es):
    opening, v0 = c2a_v0(es)
    end = min(instant(v0["body"]["resolves_by"]), instant(opening["ts"]) + dt.timedelta(days=14))
    return opening["seq"], opening["ts"], end.strftime(FMT)


def c2a_prime_window(es):
    opening, v0 = c2a_v0(es)
    v0_end = v0["body"]["resolves_by"]
    if any(promotes(e, "C2a") and instant(e["ts"]) <= instant(v0_end) for e in es):
        return None
    op2 = next((e for e in es if e["type"] == "push" and e["seq"] > opening["seq"] and
                instant(e["ts"]) > instant(v0_end)), None)
    if op2 is None:
        return None
    v5 = next((e for e in es if e["seq"] < op2["seq"] and e["type"] == "forecast" and
               e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "V5"), None)
    return op2["seq"], op2["ts"], v5["body"]["resolves_by"] if v5 else None


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


def item_process(es, after_seq=-1, promotion_at=None, window_fixes=frozenset()):
    """BRIEF-C1b §Liveness (i)-(iv), in entry order. No clock-created or regrouped items.

    `after_seq` is the first window's opening, not the latest restart: A4 wealth continues.
    `promotion_at` optionally projects expiries at a proposed promotion, without entering it.
    Callers supply a prefix ending at the observation instant. Resolved writs leave the open
    set immediately; a sovereign boundary clears pending resolutions without reopening them.
    """
    sovereign = sovereign_keys(es)
    opened, pending, items, late_reports, active_fixes = {}, [], [], [], set()

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
            if items and seq not in window_fixes:
                late_reports.append(seq)
            for _, repairs in opened.values():
                repairs.append(seq)
            if seq in window_fixes:
                active_fixes.add(seq)
        if typ == "push" and active_fixes:
            for _, repairs in opened.values():
                repairs[:] = [r for r in repairs if r not in active_fixes]
            active_fixes.clear()
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
    v5_ok = True
    if subject in ("C1b", "C2a"):
        w2 = c2a_prime_window(es) if subject == "C2a" else None
        if w2 is not None and (decision is None or instant(decision["ts"]) > instant(w2[1])):
            opening, start, end = w2[0], w2[1], w2[2] or w2[1]
            v5_ok = w2[2] is not None
            window = "C2a-prime"
        else:
            opening, start, end = (c2a_window if subject == "C2a" else c1b_window)(es)
            window = subject
        start, end = instant(start), instant(end)
    else:
        opened = next(e for e in es if e["type"] == "amend" and e["body"].get("id") == window)
        opening, start = opened["seq"], instant(opened["ts"])
        end = start + dt.timedelta(days=days)
    closing = next((e for e in es if promotes(e, subject) and (window != "C2a-prime" or instant(e["ts"]) > start)), None)
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
    veto = (any(e["type"] == "decision" and e["body"].get("kind") == "veto" and
                e["body"].get("subject") in ("C2a", "C2a-prime") and instant(e["ts"]) > start for e in prefix)
            if window == "C2a-prime" else
            any(e["type"] == "decision" and e["body"].get("kind") == "veto" and e["body"].get("subject") == subject for e in prefix))
    return {
        "window": window, "start": start.strftime(FMT), "end": end.strftime(FMT), "as_of": as_of,
        "prefix_last_seq": prefix[-1]["seq"] if prefix else None, "entries_in_window": len(inw),
        "forecasts": len(fc), "proposers": sorted({e["proposer"] for e in fc}),
        "resolutions": len(rs), "world_resolutions": len(wrs),
        "world_resolutions_with_evidence": sum(1 for e in wrs if evidence_ok(root, e["body"]["evidence"], rev)),
        "procedure": len(inw) - objects, "object": objects,
        "veto": veto,
        "j7_unresolved_past_due": len(late), "j7_denominator": len(fc),
        "overdue": overdue,
        "opening": opening, "prefix": prefix, "v5": v5_ok,
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


def off_log_repairs(acts, start, end, overlap=False):
    if acts is None:
        return None
    hkt = dt.timezone(dt.timedelta(hours=8))  # counsel's weekly CSV contract
    s, e = instant(start), instant(end)
    return sum(row["repo"] == "renavondata/jack" and row["class"] == "repair" and
               (s <= e and t <= e and t + dt.timedelta(seconds=60) > s if overlap else s <= t <= e)
               for row in acts
               for t in [dt.datetime.strptime(row["time_hkt"], "%Y-%m-%d %H:%M").replace(tzinfo=hkt)])


WINDOW_NAMES = ("C1a", "C1b", "C2a", "C2a-prime", "C2b")
CHANGE2_FUNCTIONS = ("window_fixes", "window_bounds", "names_window", "subject_names", "carrying_commit", "attributed_repairs")


def window_bounds(es, name):
    try:
        if name == "C1a":
            opened = next(e for e in es if e["type"] == "amend" and e["body"].get("id") == "A3")
            end = (instant(opened["ts"]) + dt.timedelta(days=14)).strftime(FMT)
            return opened["ts"], end, end
        if name == "C1b":
            _, start, end = c1b_window(es)
            return start, end, end
        if name == "C2a":
            _, start, early = c2a_window(es)
            return start, early, c2a_v0(es)[1]["body"]["resolves_by"]
        if name == "C2a-prime":
            w2 = c2a_prime_window(es)
            return (w2[1], w2[2], w2[2]) if w2 and w2[2] else None
    except StopIteration:
        return None
    return None


def names_window(es, e, kind, name):
    if e["type"] != "decision" or e["body"].get("kind") != kind:
        return False
    subj = e["body"].get("subject")
    if name not in ("C2a", "C2a-prime"):
        return subj == name
    try:
        w2 = c2a_prime_window(es)
    except StopIteration:
        w2 = None
    is_prime = w2 is not None and instant(e["ts"]) > instant(w2[1])
    return (is_prime and (subj == "C2a" if kind == "promote" else subj in ("C2a", "C2a-prime"))
            if name == "C2a-prime" else not is_prime and subj == "C2a")


def subject_names(subject, fname):
    word = lambda c: c.isalpha() or c.isdigit() or c in "-_"
    for token in (fname, fname[:-4]):
        pos = 0
        while (idx := subject.find(token, pos)) >= 0:
            end = idx + len(token)
            if (idx == 0 or not word(subject[idx - 1])) and (end == len(subject) or not word(subject[end])):
                return True
            pos = idx + 1
    return False


def carrying_commit(root, rev, fix):
    if not root:
        raise OSError("missing repository")
    head = rev or git_bytes(root, "rev-parse", "HEAD").decode().strip()
    parents = {p[0]: p[1:] for ln in git_bytes(root, "rev-list", "--parents", head).decode().splitlines() if ln for p in [ln.split()]}
    memo, seq = {}, fix["seq"]
    def holds(sha):
        if sha not in memo:
            lines = tree_bytes(root, sha, "log.jsonl").splitlines() if git_bytes(root, "ls-tree", sha, "--", "log.jsonl") else []
            memo[sha] = (seq < len(lines) and json.loads(lines[seq]) == fix) or any(b'"fix"' in l and json.loads(l) == fix for l in lines)
        return memo[sha]
    if not holds(head):
        return None
    queue, seen = [head], {head}
    for sha in queue:
        ps = parents.get(sha, [])
        if not ps and any(ln.startswith("parent ") for ln in git_bytes(root, "cat-file", "-p", sha).decode().splitlines()):
            raise OSError("shallow history")
        if not any(holds(p) for p in ps):
            return sha
        for p in (p for p in ps if holds(p) and p not in seen):
            seen.add(p); queue.append(p)
    return None


def attributed_repairs(root, rev, fix, subject, start, early):
    carry = carrying_commit(root, rev, fix)
    if carry is None:
        raise ValueError("carrying commit missing")
    ev_paths = set(git_bytes(root, "ls-tree", "-r", "--name-only", carry, "transcripts/evidence/").decode().splitlines())
    clf_path, hkt = "transcripts/evidence/guy_acts3.py", dt.timezone(dt.timedelta(hours=8))
    s_dt, e_dt = instant(start), instant(early)
    for path in sorted(ev_paths):
        fname = os.path.basename(path)
        if not (fname.endswith(".csv") and not fname.endswith("-raw.csv") and subject_names(subject, fname)):
            continue
        raw, sha_path = path[:-4] + "-raw.csv", path[:-4] + "-classifier.sha256"
        if raw not in ev_paths or sha_path not in ev_paths or clf_path not in ev_paths:
            continue
        toks = tree_bytes(root, carry, sha_path).decode().split()
        if not toks or toks[0] != hashlib.sha256(tree_bytes(root, carry, clf_path)).hexdigest():
            continue
        try:
            rd = csv.DictReader(tree_bytes(root, carry, path).decode().splitlines())
            rows = list(rd) if rd.fieldnames == "repo,time_hkt,class,kind,ref,note".split(",") else []
        except csv.Error:
            rows = []
        for row in rows:
            if row.get("repo") == "renavondata/jack" and row.get("class") == "repair":
                try:
                    t = dt.datetime.strptime(row.get("time_hkt", ""), "%Y-%m-%d %H:%M").replace(tzinfo=hkt)
                except ValueError:
                    continue
                if s_dt <= t and t + dt.timedelta(seconds=60) <= e_dt:
                    return True
    return False


def window_fixes(es, root=ROOT, rev=None, out=None):
    if not es:
        return set()
    sovereign, fixes, unverified = sovereign_keys(es), set(), []
    for e in es:
        if not (signer_blob(e) in sovereign and e["type"] == "decision" and e["body"].get("kind") == "fix"):
            continue
        subj = str(e["body"].get("subject", ""))
        name = next((w for w in WINDOW_NAMES if subj.startswith(w + ":")), None)
        if name is None or any(x["seq"] < e["seq"] and signer_blob(x) in sovereign and x["type"] == "decision" and
                               x["body"].get("kind") == "fix" and str(x["body"].get("subject", "")).startswith(name + ":") for x in es):
            continue
        bounds = window_bounds(es, name)
        if bounds is None or instant(e["ts"]) <= instant(bounds[2]):
            continue
        w_start, w_early, w_late = bounds
        next_push = next((p for p in es if p["type"] == "push" and instant(p["ts"]) > instant(w_late)), None)
        if next_push is not None and e["seq"] >= next_push["seq"]:
            continue
        if any(names_window(es, x, "promote", name) and instant(x["ts"]) <= instant(w_late) for x in es):
            continue
        veto_ok = any(names_window(es, x, "veto", name) and instant(x["ts"]) <= instant(w_early) for x in es)
        try:
            acts_ok = False if veto_ok else attributed_repairs(root, rev, e, subj, w_start, w_early)
        except (OSError, ValueError, UnicodeDecodeError, subprocess.CalledProcessError) as exc:
            unverified.append(f"window fix {e['seq']}: unverified — {exc}")
            continue
        if veto_ok or acts_ok:
            fixes.add(e["seq"])
    for line in unverified:
        print(line) if out is None else out.append(line)
    return fixes


VALUE_PINS = ("worked_table forecast_before_cutoff rigged revision weights_from_resolved_prefix abstention_is_base "
              "one_event_one_key grouping_by_principal uniform_prior no_learning_rate exact_probabilities per_type_base "
              "bounded_difference lambda_predictable factor_algebra window_from_the_push wealth_continues promote_refused_value "
              "second_window_from_the_end second_window_end_is_v5 second_window_cap offlog_from_second_opening "
              "promote_refused_before_end window_fix_is_decision window_fix_not_retroactive process_unchanged_from_opening").split()


def c2a_tree_evidence(root, rev, prefix, opening):
    """Check the opening's scope through every intervening tree; keep C1b's process code."""
    try:
        target, start = [e for e in prefix if e["seq"] <= opening], None
        for sha in git_bytes(root, "rev-list", "--first-parent", rev).decode().splitlines():
            try:
                entries = [json.loads(line) for line in tree_bytes(root, sha, "log.jsonl").splitlines()]
            except subprocess.CalledProcessError:
                entries = None
            if entries == target:
                start = sha
            elif start is not None:
                break
        if start is None:
            return False, False, False
        is_prime = opening != val.opening_push(prefix)["seq"]
        cap = 8400 if is_prime else 7800
        scope_at = lambda sha: (tree_bytes(root, sha, "judge/scope.json"),
                                tree_bytes(root, sha, "SPEC.md").split(b"at C1 it is:", 1)[1].split(b"```", 2)[1])
        original = scope_at(start)
        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", f"{start}..{rev}").decode().split())
        unchanged = unchanged and json.loads(original[0])["cap"] == cap and not any(
            e["type"] == "push" and e["seq"] > opening for e in prefix)
        start_nodes = ast.parse(tree_bytes(root, start, "tools/status.py")).body
        rev_nodes = ast.parse(tree_bytes(root, rev, "tools/status.py")).body
        assign_targets = lambda n: ({t.id for t in n.targets if isinstance(t, ast.Name)} if isinstance(n, ast.Assign) else
                                    {n.target.id} if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) else set())
        read_c2_tuple = lambda nodes: next((tuple(ast.literal_eval(n.value)) for n in nodes if "CHANGE2_FUNCTIONS" in assign_targets(n)), ())
        covered_funcs, covered_assigns = {"item_process", "score_items", "sovereign_keys"}, {"P0"}
        if is_prime:
            defs = {n.name: n for n in start_nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
            c2 = set(read_c2_tuple(start_nodes))
            refs, queue = set(c2), list(c2)
            while queue:
                fn = defs.get(queue.pop())
                for sub in ast.walk(fn) if fn is not None else ():
                    if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load) and sub.id in defs and sub.id not in refs:
                        refs.add(sub.id); queue.append(sub.id)
            targets = {"item_process"} | c2
            callers_in = lambda nodes: {n.name for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                                        any(isinstance(s, ast.Call) and isinstance(s.func, ast.Name) and s.func.id in targets for s in ast.walk(n))}
            covered_funcs |= refs | callers_in(start_nodes) | callers_in(rev_nodes)
            start_assigns = {name for n in start_nodes for name in assign_targets(n)}
            covered_assigns |= {sub.id for name in covered_funcs if name in defs for sub in ast.walk(defs[name])
                                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load) and sub.id in start_assigns}
        process_at = lambda nodes: [ast.dump(n) for n in nodes if getattr(n, "name", None) in covered_funcs or bool(assign_targets(n) & covered_assigns)]
        same = process_at(start_nodes) == process_at(rev_nodes) and tree_bytes(root, start, "tools/clerk.py") == tree_bytes(root, rev, "tools/clerk.py")
        pins = tree_bytes(root, rev, "pins/pins.py").decode()
        registered = all(f'Pin("{name}"' in pins or f"Pin('{name}'" in pins for name in VALUE_PINS)
        return unchanged, same, registered
    except (OSError, ValueError, IndexError, SyntaxError, subprocess.CalledProcessError):
        return False, False, False


def assess_value(s, facts, verified, root, rev, runs, acts):
    is_prime = s["window"] == "C2a-prime"
    cap = 8400 if is_prime else 7800
    end = min(s["as_of"], s["end"])
    unchanged, same, registered = c2a_tree_evidence(root, rev, s["prefix"], s["opening"])
    gate = attack_start(root, runs, end, "tests/test_value.py")
    v = val.value(s["prefix"], as_of=end, attack_green=gate, window_opening=s["start"])
    live_gate = attack_start(root, runs, end)
    unverified = []
    fixes = window_fixes(s["prefix"], root, rev, unverified)
    process = item_process(s["prefix"], c1b_window(s["prefix"])[0], end, fixes)
    live = score_items(i for i in process["items"] if live_gate is not None and live_gate < i["ts"])
    off = off_log_repairs(acts, s["start"], end, overlap=is_prime)
    s.update(value=v, continued_liveness=live, late_reports=process["late_reports"], unverified_fixes=unverified)
    return [(verified and registered, "criterion 1: C2a pins and twins in verified tests run"),
            (verified, "criterion 2: checker agreement in verified tests run"),
            (facts["counted"] <= cap and facts["kernel"] <= 500 and facts["scope"] and unchanged,
             f"criterion 3: counted {facts['counted']}/{cap}; kernel {facts['kernel']}/500; scope equals SPEC and unchanged: {facts['scope'] and unchanged}"),
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
    s = status(es, "A3", 14, as_of, root, subject, rev, decision=decision)
    if subject == "C2a" and not s["v5"]:
        unverified = []
        window_fixes([e for e in es if instant(e["ts"]) <= instant(as_of)], root, rev, unverified)
        s.update(subject=subject, unverified_fixes=unverified,
                 checks=[(False, "C2a-prime has no promotion forecast before its opening")])
        return s
    facts = tree_facts(root, rev)
    verified = run_verified(run, rev) and completed_by(run, as_of)
    checks = [(verified, "criterion 1: pins and twins in verified tests run"),
              (verified, "criterion 2: checker agreement in verified tests run"),
              (facts["counted"] <= 6900 and facts["kernel"] <= 500 and facts["scope"],
               f"criterion 3: counted {facts['counted']}/6900; kernel {facts['kernel']}/500; scope equals SPEC: {facts['scope']}")]
    if subject == "C2a":
        checks = assess_value(s, facts, verified, root, rev, runs, acts)
    elif subject == "C1b":
        unverified = []
        fixes = window_fixes(s["prefix"], root, rev, unverified)
        process = item_process(s["prefix"], s["opening"], window_fixes=fixes)
        proposed = item_process(s["prefix"], s["opening"], min(as_of, s["end"]), fixes)
        gate = attack_start(root, runs, as_of)
        checks.append((gate is not None and all(gate < i["ts"] for i in proposed["items"]),
                       f"criterion 4: attack green on main before first item: {gate or 'unverified'}"))
        live, exit_ = [score_items(i for i in p["items"] if gate is not None and gate < i["ts"])
                       for p in (process, proposed)]
        s.update(live, late_reports=process["late_reports"], promotion_E=exit_["E"], unverified_fixes=unverified)
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
    exit_procedure = s["procedure"] + int(not any(promotes(e, subject) and (s["window"] != "C2a-prime" or instant(e["ts"]) > instant(s["start"])) for e in s["prefix"]))
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
    win = [f"window: C2a-prime (second window of C2a, opened seq {s['opening']})"] if s.get("window") == "C2a-prime" else []
    return "\n".join(lines + s.get("unverified_fixes", []) + s.get("repairs", []) + win + [promotion_line(s)])


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
    w2 = c2a_prime_window([e for e in context["es"] if instant(e["ts"]) <= instant(context["as_of"])]) if context["subject"] == "C2a" else None
    closing = next((e for e in decisions if promotes(e, context["subject"]) and
                    (w2 is None or instant(e["ts"]) > instant(w2[1]))), None)
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
        raise SystemExit(f"status unverified: {exc or 'window opening or L0 missing'}")


if __name__ == "__main__":
    main()
