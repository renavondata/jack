#!/usr/bin/env python3
"""Window-file assessment, binding, provenance and R1 numeral checks (BRIEF-C2c-1)."""
import ast
import csv
import datetime as dt
import hashlib
import io
import itertools
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from judge.judge import changed_by, commits_of, counted_lines, modes, principal_at, signer_blob  # noqa: E402
from kernel import check, log  # noqa: E402
from tools import clerk, enforcement, status as st, value as val  # noqa: E402
from fractions import Fraction  # noqa: E402

FMT = "%Y-%m-%dT%H:%M:%SZ"
STAMP_FMT = "%Y%m%dT%H%M"
HKT_FMT = "%Y-%m-%d %H:%M"
WINDOWS_DIR = "transcripts/windows"
CLOSED = ("C1a", "C1b", "C2a", "C2a-prime", "C2b")
KINDS = ("verified_run", "tree_bounds", "pins_killed", "eprocess", "no_claim_past_due_unescalated",
         "ratchet", "count_zero", "undertakings_kept", "no_veto", "ratio")
NUMERIC_ARGS = ("counted", "kernel", "threshold", "null", "grace", "lead", "min_rows", "max")
HEX_CHARS = set("0123456789abcdefABCDEF")
SHA_LEN = len(hashlib.sha256(b"").hexdigest())
TWO = 1 + 1


def window_path(subject):
    return f"{WINDOWS_DIR}/{subject}.json"


def opening_review_requirement(root, layer):
    """Read the opening's review requirement; callers never parse window files."""
    brief = f"transcripts/BRIEF-{layer}-draft.md"
    raw = tree_bytes_opt(root, "origin/main", window_path(layer))
    if raw is None:
        return brief, None, None, 1
    wfile = json.loads(raw)
    needed = wfile.get("numbers", {}).get("readers")
    if type(needed) is not int or needed < 1:
        raise ValueError(f"{window_path(layer)}: invalid numbers.readers")
    return brief, window_path(layer), raw, needed


def git_lines(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []


def tree_bytes_opt(root, rev, path):
    try:
        return st.tree_bytes(root, rev, path)
    except (OSError, subprocess.CalledProcessError):
        return None


def tree_files(root, rev, prefix):
    if rev is not None:
        return [p for m, p in modes(root, rev) if p.startswith(prefix)]
    top = os.path.join(root, prefix)
    if not os.path.exists(top):
        return []
    if os.path.isfile(top):
        return [prefix]
    out = []
    for d, _, names in os.walk(top):
        for n in sorted(names):
            full = os.path.join(d, n)
            if os.path.isfile(full) and not os.path.islink(full):
                out.append(os.path.relpath(full, root))
    return sorted(out)


def has_file(root, rev, subject):
    return bool(subject) and subject not in CLOSED and tree_bytes_opt(root, rev, window_path(subject)) is not None


def default_subject(root, rev, es):
    for path in tree_files(root, rev, WINDOWS_DIR + "/"):
        if not path.endswith(".json"):
            continue
        name = os.path.basename(path)[:-len(".json")]
        if name in CLOSED:
            continue
        raw = tree_bytes_opt(root, rev, path)
        if raw is None:
            continue
        try:
            if find_opening(es, json.loads(raw)) is not None:
                return name
        except (ValueError, KeyError):
            continue
    return None


def is_num_val(v):
    if type(v) is int:
        return True
    return isinstance(v, list) and len(v) == TWO and all(type(x) is int for x in v)


def resolve_num(numbers, key):
    if not isinstance(key, str) or key not in numbers or not is_num_val(numbers[key]):
        raise ValueError(f"missing or invalid numeric key {key!r}")
    v = numbers[key]
    return Fraction(v[0], v[1]) if isinstance(v, list) else v


def check_window_file_numbers(wfile):
    numbers = wfile.get("numbers")
    if not isinstance(numbers, dict):
        raise ValueError("window file missing numbers table")
    for pname, proc in wfile.get("processes", {}).items():
        for field in ("null", "threshold"):
            if field in proc:
                resolve_num(numbers, proc[field])
    for c in wfile.get("criteria", []):
        if c.get("kind") not in KINDS:
            raise ValueError(f"unknown criterion kind {c.get('kind')!r}")
        args = c.get("args", {})
        for k in NUMERIC_ARGS:
            if k in args:
                resolve_num(numbers, args[k])
    return True


def value_tables():
    """Supply R1's value constants without letting value.py open a window file."""
    raw = tree_bytes_opt(ROOT, None, window_path("C2c-1"))
    if raw is None:
        raise ValueError("C2c-1 window file missing")
    wfile = json.loads(raw)
    return wfile["numbers"], wfile["spec_constants"], wfile["history"]


def parses_as_number_or_instant(s):
    t = s.strip()
    if not t:
        return False
    if log.instant(t):
        return True
    try:
        int(t)
        return True
    except ValueError:
        pass
    try:
        float(t)
        return True
    except ValueError:
        pass
    try:
        if "/" in t:
            Fraction(t)
            return True
    except (ValueError, ZeroDivisionError):
        pass
    return False


def scan_source_numerals(source, wfile=None):
    allowed_keys = set()
    if isinstance(wfile, dict):
        for table in ("numbers", "spec_constants", "history"):
            if isinstance(wfile.get(table), dict):
                allowed_keys |= set(wfile[table].keys())
    tree = ast.parse(source)
    neg_ones = set()
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            op = node.operand
            if isinstance(op, ast.Constant) and type(op.value) is int and op.value == 1:
                neg_ones.add(id(op))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Fraction":
            if any(isinstance(a, ast.Constant) and type(a.value) is int and a.value not in (0, 1) for a in node.args):
                violations.append(f"Fraction literal at line {node.lineno}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            v = node.value
            if type(v) is float or type(v) is complex:
                violations.append(f"float literal {v!r} at line {node.lineno}")
            elif type(v) is int and v not in (0, 1) and id(node) not in neg_ones:
                violations.append(f"int literal {v!r} at line {node.lineno}")
            elif type(v) is str and v not in allowed_keys and parses_as_number_or_instant(v):
                violations.append(f"numeric/instant string literal {v!r} at line {node.lineno}")
    return violations


def scan_tools_window_paths(tools_dir=None):
    tools_dir = tools_dir or os.path.join(ROOT, "tools")
    offenders = []
    for d, dirs, names in os.walk(tools_dir):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for n in sorted(names):
            if n.endswith(".pyc"):
                continue
            p = os.path.join(d, n)
            if not os.path.isfile(p) or os.path.islink(p):
                continue
            rel = os.path.relpath(p, ROOT)
            try:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except OSError:
                continue
            if WINDOWS_DIR in text and rel != "tools/window.py":
                offenders.append(rel)
    return offenders


def find_opening(es, wfile):
    opens = wfile.get("opens", {})
    if opens.get("rule") == "first_push_after_decision":
        dec = opens.get("decision", {})
        d = next((e for e in es if e["type"] == "decision" and e["body"].get("kind") == dec.get("kind") and
                  e["body"].get("subject") == dec.get("subject")), None)
        if d is None:
            return None
        return next((e for e in es if e["type"] == "push" and e["seq"] > d["seq"]), None)
    return None


def find_promotion_forecast(es, opening_seq, wfile):
    promo = wfile.get("promotion", {})
    who, typ, fid = promo.get("proposer"), promo.get("type"), promo.get("forecast_id")
    return next((e for e in es if e["seq"] < opening_seq and e["type"] == "forecast" and
                 e["proposer"] == who and e["body"].get("type") == typ and
                 (e["body"].get("args") or {}).get("id") == fid), None)


def extract_sha(text):
    if not isinstance(text, str):
        return None
    for tok in text.replace(";", " ").replace(",", " ").split():
        cand = tok.removeprefix("sha256:")
        if len(cand) == SHA_LEN and all(c in HEX_CHARS for c in cand):
            return cand.lower()
    return None


def check_binding(prefix, subject, actual_sha, promo_fc):
    budgets = [e for e in prefix if e["type"] == "decision" and e["body"].get("kind") == "budget" and
               str(e["body"].get("subject", "")).startswith(f"{subject}:")]
    if not budgets:
        return "window file not bound"
    b_sha = extract_sha(budgets[-1]["body"].get("subject", ""))
    f_raw = (promo_fc["body"].get("args") or {}).get("window_sha256") if promo_fc else None
    f_sha = extract_sha(f_raw) if isinstance(f_raw, str) else None
    if not b_sha or not f_sha:
        return "window file not bound"
    if actual_sha != b_sha or actual_sha != f_sha:
        return "window file changed"
    return None


def commit_parents(root, sha):
    lines = git_lines(root, "rev-list", "--parents", "-n", str(1), sha)
    return lines[0].split()[1:] if lines else []


def diff_paths(root, a, b):
    return set(git_lines(root, "diff", "--name-only", "--no-renames", a, b)) - {""}


def attribute_commit(root, sha, main_before, main_ancestors=None):
    parents = commit_parents(root, sha)
    if len(parents) <= 1:
        return "ok", changed_by(root, sha)
    if main_ancestors is None:
        main_ancestors = set(git_lines(root, "rev-list", main_before))
    if len(parents) == TWO:
        mp = [p for p in parents if p in main_ancestors]
        if len(mp) == 1:
            return "ok", diff_paths(root, mp[0], sha)
    return "unattributable", set().union(*(diff_paths(root, p, sha) for p in parents))


def proposal_merge_info(root, m_sha):
    parents = commit_parents(root, m_sha)
    if len(parents) != TWO:
        return None
    p1, p2 = parents[0], parents[1]
    old_raw = tree_bytes_opt(root, p1, "log.jsonl") or b""
    new_raw = tree_bytes_opt(root, p2, "log.jsonl") or b""
    if not new_raw.startswith(old_raw):
        return None
    old_lines, new_lines = check.read_lines(old_raw), check.read_lines(new_raw)
    if not new_lines or not check.check(new_lines)["ok"]:
        return None
    chain = commits_of(root, p1, p2)
    entries = [json.loads(l) for l in new_lines]
    first = len(old_lines)
    named = [(i, e) for i, e in enumerate(entries) if i >= first and e["type"] == "proposal" and
             e["body"].get("commit") in chain]
    if not named:
        return None
    seq, last_prop = named[-1]
    prop_commit = last_prop["body"]["commit"]
    above = list(itertools.takewhile(lambda c: c != prop_commit, chain))
    if any(changed_by(root, c) - {"log.jsonl"} for c in above):
        return None
    proposer = principal_at(entries, seq, signer_blob(last_prop))
    prop_chain = commits_of(root, p1, prop_commit)
    has_merge = any(e["type"] == "merge" for e in entries[first:])
    return {"p1": p1, "p2": p2, "proposer": proposer, "prop_commit": prop_commit,
            "prop_chain": prop_chain, "chain": chain, "has_merge": has_merge}


def provenance_changers(root, rev):
    head = rev or (git_lines(root, "rev-parse", "HEAD") or [None])[0]
    if not head:
        return {}
    changers = {}
    for m_sha in git_lines(root, "rev-list", "--first-parent", head):
        info = proposal_merge_info(root, m_sha)
        if info is not None:
            p1 = info["p1"]
            anc = set(git_lines(root, "rev-list", p1))
            paths = set()
            for c in info["prop_chain"]:
                _, cp = attribute_commit(root, c, p1, anc)
                paths |= cp
            who = info["proposer"]
        else:
            ps = commit_parents(root, m_sha)
            paths = diff_paths(root, ps[0], m_sha) if ps else changed_by(root, m_sha)
            who = None
        for p in paths:
            if p not in changers:
                changers[p] = who
    return changers


def parse_stamp(stamp):
    for fmt in (STAMP_FMT, STAMP_FMT + "Z", FMT):
        try:
            return dt.datetime.strptime(stamp, fmt).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue
    return None


def find_opening_rev(root, rev, opening_seq):
    head = rev or (git_lines(root, "rev-parse", "HEAD") or [None])[0]
    if not head:
        return None
    fps = git_lines(root, "rev-list", "--first-parent", head)
    for sha in reversed(fps):
        raw = tree_bytes_opt(root, sha, "log.jsonl")
        if not raw:
            continue
        try:
            seqs = {json.loads(l)["seq"] for l in raw.splitlines() if l.strip()}
        except (ValueError, KeyError):
            continue
        if opening_seq in seqs:
            return sha
    return fps[-1] if fps else head


def newest_acts_pair(root, rev, subject, changers=None):
    changers = provenance_changers(root, rev) if changers is None else changers
    prefix = f"transcripts/evidence/acts-{subject}-"
    files = tree_files(root, rev, prefix)
    by_repo = {"jack": {}, "opencode-runner": {}}
    for p in files:
        if not p.endswith(".csv") or p.endswith("-raw.csv") or changers.get(p) != "builder":
            continue
        rest = p[len(prefix):-len(".csv")]
        for repo in ("opencode-runner", "jack"):
            tag = repo + "-"
            if rest.startswith(tag):
                stamp = rest[len(tag):]
                sdt = parse_stamp(stamp)
                if sdt is not None:
                    by_repo[repo][stamp] = (sdt, p)
                break
    common = set(by_repo["jack"]) & set(by_repo["opencode-runner"])
    if not common:
        return None
    best = max(common, key=lambda s: (by_repo["jack"][s][0], s))
    sdt = by_repo["jack"][best][0]
    rows = []
    for repo in ("jack", "opencode-runner"):
        raw = tree_bytes_opt(root, rev, by_repo[repo][best][1])
        if raw is None:
            return None
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace")))
        if reader.fieldnames != "repo,time_hkt,class,kind,ref,note".split(","):
            return None
        rows.extend(reader)
    return {"stamp": best, "stamp_dt": sdt, "rows": rows}


def check_promote_gate(root, head, subject, decision_ts):
    if not has_file(root, head, subject):
        raise ValueError("promotion criteria unknown for " + subject)
    raw = tree_bytes_opt(root, head, window_path(subject))
    wfile = json.loads(raw)
    fresh_min = resolve_num(wfile["numbers"], "acts_fresh_minutes")
    pair = newest_acts_pair(root, head, subject)
    if pair is None:
        raise ValueError(f"promote {subject}: refused: no counting acts pair in tree")
    d_dt = st.instant(decision_ts)
    if not (d_dt - dt.timedelta(minutes=fresh_min) <= pair["stamp_dt"] <= d_dt):
        raise ValueError(f"promote {subject}: refused: newest acts pair {pair['stamp']} is not within {fresh_min} minutes before {decision_ts}")
    return True


def pin_killed_in_run(run, pin_name):
    if not isinstance(run, dict):
        return False
    if "pins" in run:
        ps = run["pins"]
        if isinstance(ps, dict):
            return ps.get(pin_name) == "KILLED"
        if isinstance(ps, list):
            return pin_name in ps
    if "transcript" in run and isinstance(run["transcript"], str):
        lines = [l.split() for l in run["transcript"].splitlines() if l.strip().startswith(pin_name)]
        return bool(lines) and all("KILLED" in toks for toks in lines)
    return False


def fold_undertakings(raw_bytes):
    rows = {}
    for line in (raw_bytes or b"").decode("utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        uid = obj["id"]
        rows.setdefault(uid, {}).update(obj)
    return [r for r in rows.values() if not r.get("done") and not r.get("closed")]


def retired_by_proposal(root, opening_rev, rev, path):
    """A due file may leave the tree only through a proposal merged in this window."""
    if not opening_rev or not rev:
        return False
    for merge_sha in git_lines(root, "rev-list", "--first-parent", f"{opening_rev}..{rev}"):
        info = proposal_merge_info(root, merge_sha)
        if info is None:
            continue
        if any(path in changed_by(root, commit) for commit in info["prop_chain"]):
            return True
    return False


def valid_world_entry(entry):
    if not isinstance(entry, dict):
        return False
    ri, rr, sb = entry.get("resolver_inputs"), entry.get("reads_record"), entry.get("scheduled_by")
    if not (isinstance(ri, list) and ri and all(isinstance(x, str) and x for x in ri)):
        return False
    if type(rr) is not bool:
        return False
    return isinstance(sb, str) and (sb == "none" or sb.startswith("transcripts/sessions/"))


def score_items_p0(items, p0):
    result, successes, capital = [], 0, Fraction(1)
    for n, item in enumerate(items):
        q = Fraction(successes + 1, n + TWO)
        stake = max(Fraction(0), (q - p0) / (p0 * (1 - p0)))
        capital *= 1 + stake * (item["Y"] - p0)
        result.append(dict(item, stake=stake, E=capital))
        successes += item["Y"]
    return {"items": result, "E": capital}


def evaluate_criterion(c, ctx):
    kind, args, evs = c["kind"], c.get("args", {}), c.get("evidence", [])
    root, rev, open_rev = ctx["root"], ctx["rev"], ctx["opening_rev"]
    wfile, numbers = ctx["wfile"], ctx["wfile"]["numbers"]
    prefix, inw = ctx["prefix"], ctx["inw"]
    as_of, start, end = ctx["as_of"], ctx["start"], ctx["end"]
    end_eff = min(as_of, end)
    run, runs = ctx["run"], ctx["runs"]

    if kind == "verified_run":
        if run is None:
            return "unknown (no run)"
        return "met" if st.run_verified(run, rev) and st.completed_by(run, as_of) else "unmet"

    if kind == "pins_killed":
        pins_raw = tree_bytes_opt(root, rev, "pins/pins.py")
        if pins_raw is None:
            return "unmet"
        pins_txt = pins_raw.decode("utf-8", errors="replace")
        if not all(f'Pin("{p}"' in pins_txt or f"Pin('{p}'" in pins_txt for p in args.get("pins", [])):
            return "unmet"
        if run is None:
            return "unknown (no run)"
        ok = st.run_verified(run, rev) and st.completed_by(run, as_of) and all(pin_killed_in_run(run, p) for p in args.get("pins", []))
        return "met" if ok else "unmet"

    if kind == "tree_bounds":
        c_cap = resolve_num(numbers, args["counted"])
        k_cap = resolve_num(numbers, args["kernel"])
        try:
            facts = st.tree_facts(root, rev)
            if facts["counted"] > c_cap or facts["kernel"] > k_cap:
                return "unmet"
            if args.get("scope_equals_spec") and not facts["scope"]:
                return "unmet"
            if open_rev:
                orig_scope = tree_bytes_opt(root, open_rev, "judge/scope.json")
                if orig_scope != tree_bytes_opt(root, rev, "judge/scope.json"):
                    return "unmet"
            map_raw = tree_bytes_opt(root, rev, "tools/enforcement.json")
            if map_raw is None:
                return "unmet"
            enforcement.check_map(json.loads(map_raw), numbers)
        except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError):
            return "unmet"
        frozen = wfile.get(args["frozen"], {})
        max_pushes = frozen.get("pushes_inside_the_window", 0)
        if sum(1 for e in inw if e["type"] == "push") > max_pushes:
            return "unmet"
        if open_rev and rev:
            f_paths = frozen.get("paths", [])
            f_except = frozen.get("except", {})
            win_merges = [e for e in inw if e["type"] == "merge"]
            for m_sha in git_lines(root, "rev-list", "--first-parent", f"{open_rev}..{rev}"):
                info = proposal_merge_info(root, m_sha)
                covered = info is not None and (info["has_merge"] or any(
                    e["body"].get("commit") in info["chain"] + [info["p2"], info["prop_commit"], m_sha] for e in win_merges))
                if not covered:
                    ps = commit_parents(root, m_sha)
                    m_diff = diff_paths(root, ps[0], m_sha) if ps else changed_by(root, m_sha)
                    if m_diff - {"log.jsonl"}:
                        return "unmet"
                    continue
                p1, proposer = info["p1"], info["proposer"]
                anc_p1 = set(git_lines(root, "rev-list", p1))
                allowed = f_except.get(proposer, [])
                for c_sha in info["prop_chain"]:
                    status_code, c_paths = attribute_commit(root, c_sha, p1, anc_p1)
                    if status_code != "ok":
                        return "unmet"
                    for p in c_paths - {"log.jsonl"}:
                        if any(p.startswith(fp) for fp in f_paths) and (tree_bytes_opt(root, c_sha, p) is None or
                                                                        not any(p.startswith(ap) for ap in allowed)):
                            return "unmet"
                status_code, merge_paths = attribute_commit(root, m_sha, p1, anc_p1)
                if status_code != "ok":
                    return "unmet"
                for p in merge_paths - {"log.jsonl"}:
                    if any(p.startswith(fp) for fp in f_paths) and (tree_bytes_opt(root, m_sha, p) is None or
                                                                      not any(p.startswith(ap) for ap in allowed)):
                        return "unmet"
        return "met"

    if kind == "eprocess":
        pname = args["process"]
        thresh = resolve_num(numbers, args.get("threshold") or wfile["processes"][pname]["threshold"])
        if pname == "value":
            if run is None:
                return "unknown (no run)"
            try:
                first_open = val.opening_push(prefix)["ts"]
            except StopIteration:
                first_open = next((e["ts"] for e in prefix if e["type"] == "push"), start)
            gate = st.attack_start(root, runs, end_eff, "tests/test_value.py")
            tables = (numbers, wfile["spec_constants"], wfile["history"])
            v_gate = val.value(prefix, opening=first_open, as_of=end_eff, attack_green=gate,
                               window_opening=start, table_values=tables)
            ok = (st.run_verified(run, rev) and st.completed_by(run, as_of) and
                  gate is not None and all(gate < r["cutoff"] for r in v_gate["rows"]) and v_gate["E_value"] >= thresh)
            return "met" if ok else "unmet"
        if pname == "liveness":
            p0 = resolve_num(numbers, args.get("null") or wfile["processes"][pname]["null"])
            try:
                c1b_open = st.c1b_window(prefix)[0]
            except StopIteration:
                c1b_open = next((e["seq"] for e in prefix if e["type"] == "decision" and e["body"].get("kind") == "promote"), -1)
            if open_rev and rev:
                for p in ("tools/status.py", "tools/clerk.py", "tools/window.py"):
                    b_open, b_now = tree_bytes_opt(root, open_rev, p), tree_bytes_opt(root, rev, p)
                    if b_open is not None and b_open != b_now:
                        return "unmet"
            proc = st.item_process(prefix, c1b_open, end_eff)
            if proc["late_reports"]:
                return "unmet"
            if run is None:
                return "unknown (no run)"
            live_gate = st.attack_start(root, runs, end_eff, "tests/test_clerk.py")
            if live_gate is None:
                return "unmet"
            gated = score_items_p0((i for i in proc["items"] if live_gate < i["ts"]), p0)
            ok = st.run_verified(run, rev) and st.completed_by(run, as_of) and gated["E"] >= thresh
            return "met" if ok else "unmet"
        return "unmet"

    if kind == "no_claim_past_due_unescalated":
        grace_td = dt.timedelta(hours=resolve_num(numbers, args["grace"]))
        lead_td = dt.timedelta(hours=resolve_num(numbers, args["lead"]))
        esc = ctx["escalations"]
        if esc is None:
            return "unknown (no escalations)"
        through_dt = st.instant(esc["through"])
        now_dt, open_dt = st.instant(as_of), st.instant(start)
        if through_dt < now_dt - grace_td:
            return "unknown (stale escalations)"
        res_ts = {e["body"]["forecast"]: st.instant(e["ts"]) for e in prefix if e["type"] == "resolution"}
        rows = esc.get("rows", [])
        for e in prefix:
            if e["type"] != "forecast":
                continue
            rb_dt = st.instant(e["body"]["resolves_by"])
            due_grace = rb_dt + grace_td
            if not (open_dt < due_grace <= min(through_dt, now_dt)):
                continue
            r_dt = res_ts.get(e["seq"])
            if r_dt is not None and r_dt <= due_grace:
                continue
            matched = any(r.get("forecast") == e["seq"] and r.get("kind") in ("handed", "escalated") and
                          rb_dt - lead_td <= st.instant(r["filed_at"]) <= due_grace for r in rows if r.get("filed_at"))
            if not matched:
                return "unmet"
        return "met"

    if kind == "ratchet":
        map_path = args["map"]
        open_raw = tree_bytes_opt(root, open_rev, map_path) if open_rev else None
        now_raw = tree_bytes_opt(root, rev, map_path)
        if now_raw is None:
            return "unmet"
        try:
            now_map = enforcement.check_map(json.loads(now_raw), numbers)
            open_map = json.loads(open_raw) if open_raw is not None else {}
        except ValueError:
            return "unmet"
        req_rows = args.get("rows", [])
        min_rows = resolve_num(numbers, args["min_rows"])
        wit_cfg = wfile.get(args["witnesses"], {}).get("witnesses", {})
        pins_raw = tree_bytes_opt(root, rev, "pins/pins.py")
        pins_txt = pins_raw.decode("utf-8", errors="replace") if pins_raw else ""
        moved = 0
        for rname in req_rows:
            o_enf = open_map.get(rname, {}).get("enforcer", "")
            n_enf = now_map.get(rname, {}).get("enforcer", "")
            wit = now_map.get(rname, {}).get("witness", "")
            want_wit = wit_cfg.get(rname, "")
            if not o_enf.startswith("hand:") or not n_enf.startswith("code:"):
                return "unmet"
            if not wit or wit != want_wit:
                return "unmet"
            if not (f'Pin("{wit}"' in pins_txt or f"Pin('{wit}'" in pins_txt):
                return "unmet"
            if run is not None and not (st.run_verified(run, rev) and st.completed_by(run, as_of) and pin_killed_in_run(run, wit)):
                return "unmet"
            moved += 1
        if moved < min_rows:
            return "unmet"
        shells_prefix = args["shells"]
        shell_files = tree_files(root, rev, shells_prefix)
        if not shell_files:
            return "unmet"
        runner_ev = ctx["runner"]
        if runner_ev is not None:
            by_wf = {os.path.basename(item.get("workflow", "")): item.get("sha256")
                     for item in runner_ev["items"] if isinstance(item, dict)}
            for sp in shell_files:
                s_bytes = tree_bytes_opt(root, rev, sp)
                s_sha = hashlib.sha256(s_bytes).hexdigest() if s_bytes is not None else None
                if by_wf.get(os.path.basename(sp)) != s_sha:
                    return "unmet"
        grace_td = dt.timedelta(hours=resolve_num(numbers, "grace_hours"))
        for ev_name in evs:
            if ev_name == "runner":
                if runner_ev is None:
                    return "unknown (no runner)"
                if runner_ev["stamp_dt"] < st.instant(as_of) - grace_td:
                    return "unknown (stale runner)"
            if ev_name == "run":
                if run is None:
                    return "unknown (no run)"
        return "met"

    if kind == "count_zero":
        sovereign = st.sovereign_keys(prefix)
        on_log = sum(1 for e in inw if signer_blob(e) in sovereign and (
            e["type"] in ("forecast", "resolution", "merge", "spec_conflict") or
            (e["type"] == "decision" and e["body"].get("kind") == "fix")))
        if on_log > 0:
            return "unmet"
        pair = ctx["acts"]
        if pair is None:
            return "unknown (no acts)"
        clock_h, clock_s = wfile["spec_constants"]["clock"][0], wfile["spec_constants"]["clock"][1]
        hkt = dt.timezone(dt.timedelta(hours=clock_h))
        open_dt, end_dt = st.instant(start), st.instant(end_eff)
        repairs = 0
        for row in pair["rows"]:
            if row.get("repo") in ("renavondata/jack", "renavondata/opencode-runner") and row.get("class") == "repair":
                r_start = dt.datetime.strptime(row["time_hkt"], HKT_FMT).replace(tzinfo=hkt)
                r_end = r_start + dt.timedelta(seconds=clock_s)
                if r_end > open_dt and r_start <= end_dt:
                    repairs += 1
        if repairs > 0:
            return "unmet"
        if pair.get("stale"):
            return "unknown (stale acts)"
        return "met"

    if kind == "undertakings_kept":
        due_file = args["due_file"]
        if tree_bytes_opt(root, rev, due_file) is not None:
            return "unmet"
        if not retired_by_proposal(root, open_rev, rev, due_file):
            return "unmet"
        who, utype = args["proposer"], args["type"]
        open_due_raw = tree_bytes_opt(root, open_rev, due_file) if open_rev else None
        open_rows = fold_undertakings(open_due_raw) if open_due_raw is not None else []
        undertakings = [e for e in prefix if e["type"] == "forecast" and e["proposer"] == who and e["body"].get("type") == utype]
        for row in open_rows:
            if row["due"] > start:
                if row["id"] in ctx["expired_undertakings"]:
                    return "unmet"
                matched = any((f["body"].get("args") or {}).get("id") == row["id"] and
                              (f["body"].get("args") or {}).get("window") == ctx["subject"] and
                              f["body"]["resolves_by"] <= row["due"] for f in undertakings)
                if not matched:
                    return "unmet"
        res_by_fc = {e["body"]["forecast"]: e for e in prefix if e["type"] == "resolution"}
        for f in undertakings:
            r = res_by_fc.get(f["seq"])
            rb = f["body"]["resolves_by"]
            if r is not None:
                if r["body"].get("outcome") != 1 or r["ts"] > rb:
                    return "unmet"
            elif rb < as_of:
                return "unmet"
        return "met"

    if kind == "no_veto":
        vetoed = any(e["type"] == "decision" and e["body"].get("kind") == "veto" and
                     e["body"].get("subject") == ctx["subject"] for e in inw)
        return "unmet" if vetoed else "met"

    if kind == "ratio":
        max_r = resolve_num(numbers, args["max"])
        return "met" if ctx["exit_procedure"] <= max_r * ctx["object"] else "unmet"

    return "unmet"


def load_escalations(root, rev, changers):
    path = "transcripts/evidence/escalations.json"
    if changers.get(path) != "builder":
        return None
    raw = tree_bytes_opt(root, rev, path)
    if raw is None:
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) and log.instant(data.get("through", "")) and isinstance(data.get("rows"), list) else None
    except ValueError:
        return None


def load_runner_evidence(root, rev, changers):
    prefix = "transcripts/evidence/runner-"
    best_stamp, best_dt, best_items = None, None, None
    for p in tree_files(root, rev, prefix):
        if not p.endswith(".json") or changers.get(p) != "builder":
            continue
        stamp = p[len(prefix):-len(".json")]
        sdt = parse_stamp(stamp)
        if sdt is None:
            continue
        raw = tree_bytes_opt(root, rev, p)
        if raw is None:
            continue
        try:
            items = json.loads(raw)
        except ValueError:
            continue
        if isinstance(items, list) and (best_dt is None or (sdt, stamp) > (best_dt, best_stamp)):
            best_stamp, best_dt, best_items = stamp, sdt, items
    return {"stamp": best_stamp, "stamp_dt": best_dt, "items": best_items} if best_dt is not None else None


def ratio_lines(wfile, root, rev, prefix, inw, subject, proc, obj, exit_proc):
    max_r = resolve_num(wfile["numbers"], "ratio_max")
    line1 = f"A3.4 ratio: procedure {proc} : object {obj}; at promote {exit_proc} : {obj} (maximum {max_r}:1)"
    wt_cfg = wfile.get("world_types", {})
    wt_path, wt_sha = wt_cfg.get("file", "transcripts/world-types.json"), wt_cfg.get("sha256", "")
    wt_raw = tree_bytes_opt(root, rev, wt_path)
    undeclared = []
    wt_obj = {}
    if wt_raw is None or hashlib.sha256(wt_raw).hexdigest() != wt_sha:
        undeclared.append(f"undeclared: {wt_path}")
    if wt_raw is not None:
        try:
            parsed = json.loads(wt_raw)
            if isinstance(parsed, dict):
                wt_obj = parsed
        except ValueError:
            pass
    log_wtypes = sorted({str(e["body"].get("type", "")) for e in prefix if e["type"] == "forecast" and
                         str(e["body"].get("type", "")).startswith("world.")})
    for t in log_wtypes:
        if t not in wt_obj or not valid_world_entry(wt_obj[t]):
            undeclared.append(f"undeclared: {t}")
    unsched_seqs = {e["seq"] for e in prefix if e["type"] == "forecast" and
                    str(e["body"].get("type", "")).startswith("world.") and
                    e["body"].get("type") in wt_obj and valid_world_entry(wt_obj[e["body"].get("type")]) and
                    wt_obj[e["body"].get("type")]["scheduled_by"] == "none"}
    obj2 = sum(1 for e in inw if (e["type"] == "forecast" and e["seq"] in unsched_seqs) or
               (e["type"] == "resolution" and e["body"]["forecast"] in unsched_seqs))
    proc2 = len(inw) - obj2
    exit_proc2 = proc2 + int(not any(st.promotes(e, subject) for e in prefix))
    line2 = f"A3.4 ratio excluding scheduled: procedure {proc2} : object {obj2}; at promote {exit_proc2} : {obj2}"
    if undeclared:
        line2 += "; " + "; ".join(undeclared)
    return [line1, line2]


def red_lines(wfile, prefix, start, escalations):
    if escalations is None:
        return []
    numbers = wfile["numbers"]
    grace_td = dt.timedelta(hours=resolve_num(numbers, "grace_hours"))
    red_td = dt.timedelta(minutes=resolve_num(numbers, "red_minutes"))
    through_dt = st.instant(escalations["through"])
    open_dt = st.instant(start)
    resolved = {e["body"]["forecast"] for e in prefix if e["type"] == "resolution"}
    filed = {r.get("forecast") for r in escalations.get("rows", []) if r.get("kind") in ("handed", "escalated")}
    out = []
    for e in prefix:
        if e["type"] == "forecast" and e["seq"] not in resolved:
            rb_dt = st.instant(e["body"]["resolves_by"])
            if rb_dt + grace_td > open_dt and rb_dt - red_td <= through_dt and e["seq"] not in filed:
                out.append(f"RED: forecast {e['seq']} due {e['body']['resolves_by']}, no session filed")
    return out


def assess(es, subject, as_of, root, rev, run=None, runs=(), acts=None, mapping=None, decision=None):
    if decision is not None:
        es = [e for e in es if e["seq"] <= decision["seq"]]
        as_of, subject = decision["ts"], decision["body"]["subject"]
        rev = st.prefix_tree(root, rev, es[:-1]) or rev
        run = next((r for r in runs if st.run_verified(r, rev) and st.completed_by(r, as_of)), run)
    es = [e for e in es if e["ts"] <= as_of]
    raw = tree_bytes_opt(root, rev, window_path(subject))
    if raw is None:
        raise ValueError(f"missing window file for {subject}")
    actual_sha = hashlib.sha256(raw).hexdigest()
    wfile = json.loads(raw)
    opening_entry = find_opening(es, wfile)
    if opening_entry is None:
        return {"from_window_file": True, "subject": subject, "as_of": as_of, "es": es, "prefix": es,
                "start": as_of, "end": as_of, "checks": [(False, f"{subject} has not opened")],
                "refusal": f"{subject} has not opened", "overdue": []}
    opening_seq, start = opening_entry["seq"], opening_entry["ts"]
    promo_fc = find_promotion_forecast(es, opening_seq, wfile)
    if promo_fc is None:
        msg = f"{subject} has no promotion forecast before its opening"
        return {"from_window_file": True, "subject": subject, "as_of": as_of, "es": es, "prefix": es,
                "start": start, "end": as_of, "checks": [(False, msg)], "refusal": msg, "overdue": []}
    stated_end = promo_fc["body"]["resolves_by"]
    closing = next((e for e in es if st.promotes(e, subject) and e["seq"] > opening_seq and e["ts"] <= stated_end), None)
    end = min(stated_end, closing["ts"]) if closing else stated_end
    prefix = [e for e in es if e["ts"] <= end and (not closing or e["seq"] <= closing["seq"])]
    bind_err = check_binding(prefix, subject, actual_sha, promo_fc)
    if bind_err is not None:
        return {"from_window_file": True, "subject": subject, "as_of": as_of, "es": es, "prefix": prefix,
                "start": start, "end": end, "checks": [(False, bind_err)], "refusal": bind_err, "overdue": []}
    try:
        check_window_file_numbers(wfile)
    except ValueError as exc:
        msg = str(exc)
        return {"from_window_file": True, "subject": subject, "as_of": as_of, "es": es, "prefix": prefix,
                "start": start, "end": end, "checks": [(False, msg)], "refusal": msg, "overdue": []}

    inw = [e for e in prefix if e["seq"] > opening_seq]
    open_rev = find_opening_rev(root, rev, opening_seq)
    changers = provenance_changers(root, rev)
    numbers = wfile["numbers"]
    pair = newest_acts_pair(root, rev, subject, changers)
    if pair is not None:
        if prefix and st.promotes(prefix[-1], subject):
            d_dt = st.instant(prefix[-1]["ts"])
            fresh_td = dt.timedelta(minutes=resolve_num(numbers, "acts_fresh_minutes"))
            pair["stale"] = not (d_dt - fresh_td <= pair["stamp_dt"] <= d_dt)
        else:
            grace_td = dt.timedelta(hours=resolve_num(numbers, "grace_hours"))
            pair["stale"] = pair["stamp_dt"] < st.instant(as_of) - grace_td
    elif acts is not None:
        pair = {"stamp": as_of, "stamp_dt": st.instant(as_of), "rows": acts, "stale": False}

    escalations = load_escalations(root, rev, changers)
    runner_ev = load_runner_evidence(root, rev, changers)

    due_path = wfile.get("undertakings", {}).get("file", "transcripts/COUNSEL-DUE.jsonl")
    open_due_raw = tree_bytes_opt(root, open_rev, due_path) if open_rev else None
    open_due_rows = fold_undertakings(open_due_raw) if open_due_raw is not None else []
    expired_ids = [r["id"] for r in open_due_rows if r["due"] <= start]

    world_seqs = {e["seq"] for e in prefix if e["type"] == "forecast" and str(e["body"].get("type", "")).startswith("world.")}
    obj = sum(1 for e in inw if (e["type"] == "forecast" and e["seq"] in world_seqs) or
              (e["type"] == "resolution" and e["body"]["forecast"] in world_seqs))
    proc = len(inw) - obj
    exit_proc = proc + int(not any(st.promotes(e, subject) for e in prefix))

    ctx = {"root": root, "rev": rev, "opening_rev": open_rev, "wfile": wfile, "subject": subject,
           "as_of": as_of, "start": start, "end": end, "prefix": prefix, "inw": inw,
           "run": run, "runs": runs, "acts": pair, "escalations": escalations, "runner": runner_ev,
           "expired_undertakings": expired_ids, "procedure": proc, "object": obj, "exit_procedure": exit_proc}

    criterion_lines = []
    checks = []
    for c in wfile.get("criteria", []):
        val_str = evaluate_criterion(c, ctx)
        line = f"criterion {c['id']}: {c['text']} {val_str}"
        criterion_lines.append(line)
        checks.append((val_str == "met", line))

    if mapping is None:
        map_raw = tree_bytes_opt(root, rev, "tools/enforcement.json")
        mapping = json.loads(map_raw) if map_raw else {}

    resolved = {e["body"]["forecast"] for e in prefix if e["type"] == "resolution"}
    overdue = sorted((e["body"]["resolves_by"], e["seq"], e["proposer"], (e["body"].get("args") or {}).get("evidence", ""))
                     for e in es if e["type"] == "forecast" and e["seq"] not in resolved and e["body"]["resolves_by"] < as_of)

    return {
        "from_window_file": True, "window": subject, "subject": subject,
        "start": start, "end": end, "as_of": as_of,
        "prefix_last_seq": prefix[-1]["seq"] if prefix else None,
        "es": es, "prefix": prefix, "opening": opening_seq,
        "criterion_lines": criterion_lines, "checks": checks,
        "expired_lines": [f"expired undertaking {uid}" for uid in expired_ids],
        "red_lines": red_lines(wfile, prefix, start, escalations),
        "ratio_lines": ratio_lines(wfile, root, rev, prefix, inw, subject, proc, obj, exit_proc),
        "map": mapping, "numbers": numbers, "overdue": overdue,
    }


def render(s):
    if "refusal" in s:
        return f"promote {s['subject']}: refused: {s['refusal']}"
    lines = [f"window {s['subject']}: {s['start']} .. {s['end']} (as of {s['as_of']}; prefix to seq {s['prefix_last_seq']})"]
    lines += s["criterion_lines"]
    lines += s.get("expired_lines", [])
    lines += s.get("red_lines", [])
    lines += s.get("ratio_lines", [])
    w1 = clerk.forecast_writs(s.get("es", s.get("prefix", [])), [], s["as_of"])
    if w1:
        lines.append(clerk.render(w1))
    lines += s.get("repairs", [])
    lines.append(st.promotion_line(s))
    return "\n".join(lines)
