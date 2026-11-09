#!/usr/bin/env python3
"""Collect and classify off-log platform acts for a window (transcripts/sessions/evidence.md step 1;
C2c-1.json evidence.acts; BRIEF-C2a-prime §The acts evidence; precedent transcripts/evidence/guy_acts3.py)."""
from collections import defaultdict
import csv, datetime as dt, hashlib, json, os, re, subprocess, sys  # noqa: E401
sys.path.insert(0, ROOT := os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from kernel import check  # noqa: E402

G, HKT, FMT = "gfrmin", dt.timezone(dt.timedelta(hours=8)), "%Y-%m-%dT%H:%M:%SZ"
MAX_PAGES = 100
PREDECESSOR = {"C2c-1": "C2b", "C2c-2": "C2c-1", "C2c-3": "C2c-2", "C2b": "C2a", "C2a": "C1b"}
REPOS = {"jack": "renavondata/jack", "renavondata/jack": "renavondata/jack",
         "opencode-runner": "renavondata/opencode-runner", "renavondata/opencode-runner": "renavondata/opencode-runner"}


def root_dir(): return os.environ.get("JACK_ROOT") or ROOT  # noqa: E704
def t(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))  # noqa: E704
def now_iso(): return os.environ.get("JACK_NOW") or dt.datetime.now(dt.timezone.utc).strftime(FMT)  # noqa: E704


def current_stamp(root=None, arg=None):
    if arg: return arg
    if os.environ.get("STAMP"): return os.environ["STAMP"]
    r = subprocess.run(["git", "-C", root or root_dir(), "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    b = r.stdout.strip() if r.returncode == 0 else ""
    m = re.match(r"^evidence-(\d{8}T\d{4}Z?)(?:-|$)", b)
    if m: return m.group(1)
    return t(now_iso()).strftime("%Y%m%dT%H%M")


def stamp_to_iso(stamp):
    for fmt in ("%Y%m%dT%H%M", "%Y%m%dT%H%MZ", FMT):
        try: return dt.datetime.strptime(stamp, fmt).replace(tzinfo=dt.timezone.utc).strftime(FMT)
        except ValueError: pass
    raise SystemExit(f"refused: invalid stamp {stamp!r}")


def load_entries(root=None):
    with open(os.path.join(root or root_dir(), "log.jsonl"), "rb") as f:
        lines = check.read_lines(f.read())
    if not lines or not check.check(lines)["ok"]:
        raise SystemExit("refused: log.jsonl is refused by the kernel")
    return [json.loads(line) for line in lines]


def opening_instant(window_name, es=None, root=None):
    root = root or root_dir()
    es = load_entries(root) if es is None else es
    try:
        from tools import window as win
        if win.has_file(root, None, window_name):
            op = win.find_opening(es, json.loads(win.tree_bytes_opt(root, None, win.window_path(window_name))))
            if op is not None: return op["ts"]
    except ImportError:
        pass
    if window_name in PREDECESSOR:
        prev = PREDECESSOR[window_name]
        d = next((e for e in es if e["type"] == "decision" and e["body"].get("kind") == "promote" and e["body"].get("subject") == prev), None)
        op = next((e for e in es if e["type"] == "push" and e["seq"] > d["seq"]), None) if d else None
        if op is not None: return op["ts"]
    if window_name == "C1b":
        d = next((e for e in es if e["type"] == "decision" and e["body"].get("kind") == "promote" and e["body"].get("subject") == "C1a"), None)
        if d is not None: return d["ts"]
    if window_name == "C1a":
        d = next((e for e in es if e["type"] == "amend" and e["body"].get("id") == "C1"), es[0] if es else None)
        if d is not None: return d["ts"]
    if window_name == "C2a-prime":
        v0 = next((e for e in es if e["type"] == "forecast" and e["proposer"] == "counsel" and (e["body"].get("args") or {}).get("id") == "V0"), None)
        op = next((e for e in es if e["type"] == "push" and e["ts"] > v0["body"]["resolves_by"]), None) if v0 else None
        if op is not None: return op["ts"]
    marker = next((e for e in es if (e["type"] == "decision" and e["body"].get("kind") == "budget" and str(e["body"].get("subject", "")).startswith(f"{window_name}:")) or
                   (e["type"] == "forecast" and e["body"].get("type") == "window.promotion" and (e["body"].get("args") or {}).get("window") == window_name)), None)
    op = next((e for e in es if e["type"] == "push" and e["seq"] > marker["seq"]), None) if marker else None
    if op is not None: return op["ts"]
    raise SystemExit(f"refused: window {window_name!r} has not opened on log.jsonl")


def api(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"refused: gh api {path}: {r.stderr.strip() or r.stdout.strip()}")
    return json.loads(r.stdout)


def pages(path, key=None, stop=None):
    n = 1
    while n <= MAX_PAGES:
        sep = "&" if "?" in path else "?"
        d = api(f"{path}{sep}per_page=100&page={n}")
        items = d[key] if key else d
        if not items: return
        for it in items: yield it
        if len(items) < 100 or (stop and stop(items[-1])): return
        n += 1
    raise SystemExit(f"refused: gh api {path}: exceeded {MAX_PAGES} pages")


def collect_acts(repo, start_iso, end_iso):
    start, end, acts = t(start_iso), t(end_iso), []
    def add(ts, cls, kind, ref, note=""):
        instant = t(ts)
        # Tables print whole UTC+8 minutes, so retain any minute that overlaps the window.
        minute = instant.replace(second=0, microsecond=0)
        if minute < end and minute + dt.timedelta(minutes=1) > start:
            acts.append((instant, cls, kind, ref, note))
    issues = {it["number"]: it for it in pages(f"repos/{repo}/issues?state=all&since={start_iso}&sort=updated&direction=desc")}
    for n, it in issues.items():
        if (it.get("user") or {}).get("login") != G or "pull_request" in it: continue
        labels = {l["name"] for l in it.get("labels", [])}
        add(it["created_at"], "decision", "wish filed" if "wish" in labels else "instruction filed", f"#{n}", (it.get("title") or "")[:70])
    events = [e for e in pages(f"repos/{repo}/issues/events",
                               stop=lambda e: t(e["created_at"]) < start - dt.timedelta(minutes=1))
              if e.get("actor") and e["actor"]["login"] == G and e.get("issue")]
    events.sort(key=lambda e: e["created_at"])
    signed_once, skip, by_issue = set(), set(), defaultdict(list)
    for e in events: by_issue[e["issue"]["number"]].append(e)
    for n, evs in by_issue.items():
        it = issues.get(n) or evs[0]["issue"]
        author, is_pr, labels_now = (it.get("user") or {}).get("login"), "pull_request" in it, {l["name"] for l in it.get("labels", [])}
        for i, e in enumerate(evs):
            if id(e) in skip: continue
            ev, lab, ts = e["event"], (e.get("label") or {}).get("name", ""), e["created_at"]
            if ev in ("assigned", "unassigned"):
                if (e.get("assigner") or {}).get("login") == G: add(ts, "repair", f"issue event ({ev})", f"#{n}")
                continue
            if ev in ("review_dismissed", "auto_squash_enabled", "auto_merge_enabled", "auto_rebase_enabled",
                      "automatic_base_change_succeeded", "automatic_base_change_failed"): continue
            if ev == "unlabeled" and lab == "instruction":
                later = next((f for f in evs[i + 1:] if f["event"] == "labeled" and (f.get("label") or {}).get("name") == "instruction"), None)
                if later is not None:
                    skip.add(id(later))
                    quick = t(later["created_at"]) - t(ts) <= dt.timedelta(minutes=10)
                    add(ts, "repair", "re-fire (instruction)" if quick else "unsign/re-sign cycle", f"#{n}")
                else: add(ts, "decision", "unsigned (withdrawn)", f"#{n}")
                continue
            if ev == "unlabeled":
                back = next((f for f in evs[i + 1:] if f["event"] == "labeled" and (f.get("label") or {}).get("name") == lab
                             and t(f["created_at"]) - t(ts) <= dt.timedelta(minutes=10)), None)
                if back is not None: skip.add(id(back)); add(ts, "repair", f"re-fire ({lab})", f"#{n}")  # noqa: E702
                elif lab == "instruction": add(ts, "decision", "unsigned", f"#{n}")
                else: add(ts, "repair", f"label removed ({lab})", f"#{n}")
            elif ev == "labeled":
                if lab == "instruction" and author != G and n not in signed_once: signed_once.add(n); add(ts, "decision", "draft signed", f"#{n}")  # noqa: E702
                elif lab in ("instruction", "wish") and author == G and t(ts) - t(it["created_at"]) <= dt.timedelta(minutes=2): pass
                else: add(ts, "repair", f"label added ({lab})", f"#{n}")
            elif ev == "closed":
                if is_pr:
                    if not (it.get("pull_request") or {}).get("merged_at"): add(ts, "repair", "PR closed unmerged", f"#{n}")
                elif "draft" in labels_now and author != G: add(ts, "decision", "draft declined", f"#{n}")
                elif author == G: add(ts, "repair", "own issue closed", f"#{n}")
                else: add(ts, "repair", "stop/failure issue closed", f"#{n}", (it.get("title") or "")[:60])
            elif ev in ("merged", "referenced", "cross-referenced", "mentioned", "subscribed",
                        "head_ref_deleted", "head_ref_restored", "review_requested", "auto_merge_enabled", "added_to_merge_queue"): continue
            else: add(ts, "repair", f"issue event ({ev})", f"#{n}")
    for n, it in issues.items():
        if "pull_request" not in it: continue
        approved = False
        for rv in sorted(api(f"repos/{repo}/pulls/{n}/reviews?per_page=100"), key=lambda r: r.get("submitted_at") or ""):
            if rv.get("user") and rv["user"]["login"] == G and rv.get("submitted_at"):
                if rv["state"] in ("APPROVED", "DISMISSED"):
                    add(rv["submitted_at"], "repair" if approved else "decision", "re-Accept (same PR)" if approved else "Accept", f"PR #{n}")
                    approved = True
                else: add(rv["submitted_at"], "repair", f"review {rv['state'].lower()}", f"PR #{n}")
    for run in pages(f"repos/{repo}/actions/runs?created={start_iso}..{end_iso}", key="workflow_runs"):
        if (run.get("triggering_actor") or {}).get("login") != G: continue
        if run["event"] == "workflow_dispatch": add(run["created_at"], "repair", f"dispatch {run['name']}", str(run["id"]))
        elif run.get("run_attempt", 1) > 1: add(run.get("run_started_at") or run["created_at"], "repair", f"re-run {run['name']}", str(run["id"]))
    for rs in api(f"repos/{repo}/rulesets"):
        d = api(f"repos/{repo}/rulesets/{rs['id']}")
        if d.get("created_at"): add(d["created_at"], "decision", "ruleset created", d["name"])
    comments = list(pages(f"repos/{repo}/issues/comments?since={start_iso}"))
    for c in comments:
        if (c.get("user") or {}).get("login") != G: continue
        body = (c.get("body") or "").strip()
        if not body.startswith(("override by gfrmin", "re-fired by gfrmin", "Closed by gfrmin")):
            add(c["created_at"], "comment", "free-text comment", c["issue_url"].rsplit("/", 1)[1], body[:70].replace("\n", " "))
    raw_acts = sorted(acts)
    decl = []
    for c in comments:
        if (c.get("user") or {}).get("login") != G: continue
        m = re.search(r"^Proposer: ([a-z0-9_-]+) ([a-z0-9_-]+)\s*$", c.get("body") or "", re.M)
        if m and m.group(1) not in (G.lower(), "guy"):
            decl.append((t(c["created_at"]), c["issue_url"].rsplit("/", 1)[1], m.group(1), m.group(2)))
    attributed = []
    for a in acts:
        ts, cls, kind, ref, note = a
        issue = ref.lstrip("#").replace("PR #", "").strip()
        who = next(((p, k) for (dt_, n, p, k) in decl if n == issue and abs((dt_ - ts).total_seconds()) <= 120), None)
        if who and cls in ("repair", "decision"):
            attributed.append((ts, "party-act", kind, ref, f"declared Proposer: {who[0]} {who[1]}; {note}".strip("; ")))
        elif who and cls == "comment":
            attributed.append((ts, "party-comment", kind, ref, f"Proposer: {who[0]} {who[1]}"))
        else: attributed.append(a)
    attributed.sort()
    return raw_acts, attributed


def write_csv(path, repo, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["repo", "time_hkt", "class", "kind", "ref", "note"])
        for a in rows:
            w.writerow([repo, a[0].astimezone(HKT).strftime("%Y-%m-%d %H:%M"), *a[1:]])


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if len(args) != 3 or args[1] not in REPOS:
        raise SystemExit("usage:acts.py <window> <renavondata/jack|renavondata/opencode-runner> <stamp>")
    window_name, repo, stamp = args[0], REPOS[args[1]], args[2]
    short = repo.split("/")[-1]
    root = root_dir()
    start_iso, end_iso = opening_instant(window_name, root=root), stamp_to_iso(stamp)
    if t(end_iso) < t(start_iso):
        raise SystemExit(f"refused: stamp {end_iso} precedes window {window_name} opening {start_iso}")
    raw_acts, attributed = collect_acts(repo, start_iso, end_iso)
    ev_dir = os.path.join(root, "transcripts", "evidence")
    os.makedirs(ev_dir, exist_ok=True)
    base = os.path.join(ev_dir, f"acts-{window_name}-{short}-{stamp}")
    write_csv(f"{base}.csv", repo, attributed)
    write_csv(f"{base}-raw.csv", repo, raw_acts)
    with open(os.path.abspath(__file__), "rb") as src:
        sha = hashlib.sha256(src.read()).hexdigest()
    with open(f"{base}-classifier.sha256", "w", encoding="utf-8") as f:
        f.write(sha + "\n")
    print(f"transcripts/evidence/acts-{window_name}-{short}-{stamp}.csv ({len(attributed)} rows, stamp {stamp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
