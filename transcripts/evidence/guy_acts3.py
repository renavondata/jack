"""guy_acts.py (project doc claude/guy_acts.py, 13 Oct) generalised: repo and local path as arguments,
and an END bound so a closed week can be re-run identically later. Classification unchanged, with one
attribution rule added on 1 Nov 2026 (guy_acts3): the sovereign's GitHub login is also the login counsel's session
and the steel sessions act under (COUNSEL-OPEN 17), so a platform act is attributed to the party that DECLARED it —
a comment by that login on the same issue within two minutes whose body carries a line `Proposer: <party> <key_id>`
with a party other than guy. Such an act is written with class `party-act` and the declaration in its note; nothing is
dropped. Comments carrying such a trailer are the party's, not free-text of the sovereign's.
Usage: python3 guy_acts2.py <owner/repo> <local git path> <start ISO Z> <end ISO Z> <out.csv>
"""
import csv, json, subprocess, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

R = sys.argv[1]
LOCAL = sys.argv[2]
G = "gfrmin"
HKT = timezone(timedelta(hours=8))
START = sys.argv[3]
END = sys.argv[4]
OUT = sys.argv[5]


def api(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def pages(path, key=None, stop=None):
    n = 1
    while True:
        sep = "&" if "?" in path else "?"
        d = api(f"{path}{sep}per_page=100&page={n}")
        items = d[key] if key else d
        if not items:
            return
        for it in items:
            yield it
        if stop and stop(items[-1]):
            return
        n += 1


def t(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


start = t(START)
end = t(END)
acts = []  # (time, class, kind, ref, note)


def add(ts, cls, kind, ref, note=""):
    if start <= t(ts) < end:
        acts.append((t(ts), cls, kind, ref, note))


issues = {}
for it in pages(f"repos/{R}/issues?state=all&since={START}&sort=updated&direction=desc"):
    issues[it["number"]] = it

for n, it in issues.items():
    if it["user"]["login"] != G or "pull_request" in it:
        continue
    labels = {l["name"] for l in it["labels"]}
    if "wish" in labels:
        add(it["created_at"], "decision", "wish filed", f"#{n}", it["title"][:70])
    elif "instruction" in labels:
        add(it["created_at"], "decision", "instruction filed", f"#{n}", it["title"][:70])
    else:
        add(it["created_at"], "decision", "instruction filed", f"#{n}", it["title"][:70])

events = [e for e in pages(f"repos/{R}/issues/events", stop=lambda e: t(e["created_at"]) < start)
          if e.get("actor") and e["actor"]["login"] == G and t(e["created_at"]) >= start]
events.sort(key=lambda e: e["created_at"])
signed_once = set()
skip = set()
by_issue = defaultdict(list)
for e in events:
    by_issue[e["issue"]["number"]].append(e)
for n, evs in by_issue.items():
    it = issues.get(n) or evs[0]["issue"]
    author = (it.get("user") or {}).get("login")
    is_pr = "pull_request" in it
    labels_now = {l["name"] for l in it.get("labels", [])}
    for i, e in enumerate(evs):
        if id(e) in skip:
            continue
        ev, lab, ts = e["event"], (e.get("label") or {}).get("name", ""), e["created_at"]
        if ev in ("assigned", "unassigned"):
            if (e.get("assigner") or {}).get("login") == G:
                add(ts, "repair", f"issue event ({ev})", f"#{n}")
            continue
        if ev in ("review_dismissed", "auto_squash_enabled", "auto_merge_enabled", "auto_rebase_enabled",
                  "automatic_base_change_succeeded", "automatic_base_change_failed"):
            continue
        if ev == "unlabeled" and lab == "instruction":
            later = next((f for f in evs[i + 1:] if f["event"] == "labeled"
                          and (f.get("label") or {}).get("name") == "instruction"), None)
            if later is not None:
                skip.add(id(later))
                quick = t(later["created_at"]) - t(ts) <= timedelta(minutes=10)
                add(ts, "repair", "re-fire (instruction)" if quick else "unsign/re-sign cycle", f"#{n}")
            else:
                add(ts, "decision", "unsigned (withdrawn)", f"#{n}")
            continue
        if ev == "unlabeled":
            back = next((f for f in evs[i + 1:] if f["event"] == "labeled"
                         and (f.get("label") or {}).get("name") == lab
                         and t(f["created_at"]) - t(ts) <= timedelta(minutes=10)), None)
            if back is not None:
                skip.add(id(back))
                add(ts, "repair", f"re-fire ({lab})", f"#{n}")
            elif lab == "instruction":
                add(ts, "decision", "unsigned", f"#{n}")
            else:
                add(ts, "repair", f"label removed ({lab})", f"#{n}")
        elif ev == "labeled":
            if lab == "instruction" and author != G and n not in signed_once:
                signed_once.add(n)
                add(ts, "decision", "draft signed", f"#{n}")
            elif lab in ("instruction", "wish") and author == G and \
                    t(ts) - t(it["created_at"]) <= timedelta(minutes=2):
                pass
            else:
                add(ts, "repair", f"label added ({lab})", f"#{n}")
        elif ev == "closed":
            if is_pr:
                if not (it.get("pull_request") or {}).get("merged_at"):
                    add(ts, "repair", "PR closed unmerged", f"#{n}")
            elif "draft" in labels_now and author != G:
                add(ts, "decision", "draft declined", f"#{n}")
            elif author == G:
                add(ts, "repair", "own issue closed", f"#{n}")
            else:
                add(ts, "repair", "stop/failure issue closed", f"#{n}", (it.get("title") or "")[:60])
        elif ev in ("merged", "referenced", "cross-referenced", "mentioned", "subscribed",
                    "head_ref_deleted", "head_ref_restored", "review_requested",
                    "auto_merge_enabled", "added_to_merge_queue"):
            continue
        else:
            add(ts, "repair", f"issue event ({ev})", f"#{n}")

for n, it in issues.items():
    if "pull_request" not in it:
        continue
    approved = False
    for rv in sorted(api(f"repos/{R}/pulls/{n}/reviews?per_page=100"), key=lambda r: r.get("submitted_at") or ""):
        if rv["user"] and rv["user"]["login"] == G and rv.get("submitted_at"):
            if rv["state"] in ("APPROVED", "DISMISSED"):
                add(rv["submitted_at"], "repair" if approved else "decision",
                    "re-Accept (same PR)" if approved else "Accept", f"PR #{n}")
                approved = True
            else:
                add(rv["submitted_at"], "repair", f"review {rv['state'].lower()}", f"PR #{n}")

for run in pages(f"repos/{R}/actions/runs?created={START}..{END}", key="workflow_runs"):
    trig = (run.get("triggering_actor") or {}).get("login")
    if trig != G:
        continue
    if run["event"] == "workflow_dispatch":
        add(run["created_at"], "repair", f"dispatch {run['name']}", str(run["id"]))
    elif run.get("run_attempt", 1) > 1:
        add(run.get("run_started_at") or run["created_at"], "repair", f"re-run {run['name']}", str(run["id"]))

try:
    for rs in api(f"repos/{R}/rulesets"):
        d = api(f"repos/{R}/rulesets/{rs['id']}")
        add(d["created_at"], "decision", "ruleset created", d["name"])
except subprocess.CalledProcessError:
    pass

for c in pages(f"repos/{R}/issues/comments?since={START}"):
    if c["user"]["login"] != G:
        continue
    body = c["body"].strip()
    machine = body.startswith(("override by gfrmin", "re-fired by gfrmin", "Closed by gfrmin"))
    if not machine:
        add(c["created_at"], "comment", "free-text comment", c["issue_url"].rsplit("/", 1)[1], body[:70].replace("\n", " "))

# attribution by declaration (guy_acts3): a Proposer: trailer in a comment on the same issue within two minutes
import re
decl = []  # (time, issue number, party, key_id)
for c in pages(f"repos/{R}/issues/comments?since={START}"):
    if c["user"]["login"] != G:
        continue
    m = re.search(r"^Proposer: ([a-z0-9_-]+) ([a-z0-9_-]+)\s*$", c["body"], re.M)
    if m and m.group(1) != G.lower() and m.group(1) != "guy":
        decl.append((t(c["created_at"]), c["issue_url"].rsplit("/", 1)[1], m.group(1), m.group(2)))
attributed = []
for a in acts:
    ts, cls, kind, ref, note = a
    issue = ref.lstrip("#").replace("PR #", "").strip()
    who = next(((p, k) for (dt, n, p, k) in decl if n == issue and abs((dt - ts).total_seconds()) <= 120), None)
    if who and cls in ("repair", "decision"):
        attributed.append((ts, "party-act", kind, ref, f"declared Proposer: {who[0]} {who[1]}; {note}".strip("; ")))
    elif who and cls == "comment":
        attributed.append((ts, "party-comment", kind, ref, f"Proposer: {who[0]} {who[1]}"))
    else:
        attributed.append(a)
acts = attributed
acts.sort()
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["repo", "time_hkt", "class", "kind", "ref", "note"])
    for a in acts:
        w.writerow([R, a[0].astimezone(HKT).strftime("%Y-%m-%d %H:%M"), *a[1:]])

days = defaultdict(Counter)
for a in acts:
    days[a[0].astimezone(HKT).strftime("%a %d %b")][a[1]] += 1
merges = Counter()
branch = subprocess.run(["git", "-C", LOCAL, "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
                        capture_output=True, text=True).stdout.strip() or "origin/master"
log = subprocess.run(["git", "-C", LOCAL, "log", branch, "--first-parent", "--merges",
                      f"--since={START}", f"--until={END}", "--format=%cI"], capture_output=True, text=True, check=True).stdout.split()
for c in log:
    merges[t(c).astimezone(HKT).strftime("%a %d %b")] += 1
print(f"== {R}  {START} .. {END}")
print(f"{'day (HKT)':<12} decision repair  merges  repairs/merge  repair share")
tot = Counter()
alldays = sorted(set(days) | set(merges), key=lambda s: datetime.strptime(s + " 2026", "%a %d %b %Y"))
for d in alldays:
    c = days[d]; tot.update(c)
    share = c["repair"] / max(1, c["repair"] + c["decision"])
    m = merges[d]; tot["merges"] += m
    rpm = f"{c['repair'] / m:.1f}" if m else "-"
    print(f"{d:<12} {c['decision']:>8} {c['repair']:>6} {m:>7} {rpm:>14}  {share:>11.0%}")
share = tot["repair"] / max(1, tot["repair"] + tot["decision"])
print(f"{'total':<12} {tot['decision']:>8} {tot['repair']:>6} {tot['merges']:>7} {tot['repair'] / max(1, tot['merges']):>14.1f}  {share:>11.0%}")
print(f"free-text comments by gfrmin (not counted as acts): {tot['comment']}")
for cls in ("decision", "repair"):
    k = Counter(a[2] for a in acts if a[1] == cls)
    print(cls + ": " + "; ".join(f"{v} {n}" for n, v in k.most_common()))
