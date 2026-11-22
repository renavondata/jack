#!/usr/bin/env python3
"""Replay of the lane, 13 November 00:00Z to 22 November 14:00Z (adviser, entry 125).

Question: how often would the sovereign's push paste have begun to act, and how
often would a court merge have landed on main before his push did?

A start is the first moment of a quiet stretch at which the paste's tests hold
for 40 seconds. v1 tests: no pull request open on jack but #125, #316, #562 and
no session issue open on the runner repository. v2 adds: no repropose or
counsel-sign run in flight. A start counts as refused when a pull request
merges on jack within LAND minutes after it (26 minutes of check, then the
passphrase).

Reads GitHub with `gh api`; writes nothing. An analysis aid, not jack code.
Run: python3 lane-replay.py
"""
import datetime as d
import json
import subprocess

START = d.datetime(2026, 11, 13, 0, 0, 0)
END = d.datetime(2026, 11, 22, 14, 0, 0)
LAND = 31
SKIP = {125, 316, 562}


def t(s):
    return d.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def gh(path):
    return json.loads(subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True).stdout)


def pages(path, n, key=None):
    out = []
    for p in range(1, n + 1):
        r = gh(f"{path}{'&' if '?' in path else '?'}per_page=100&page={p}")
        out += r[key] if key else r
    return out


prs = [p for p in pages("repos/renavondata/jack/pulls?state=all&sort=created&direction=desc", 6)
       if p["number"] not in SKIP]
iss = [i for i in pages("repos/renavondata/opencode-runner/issues?state=all&sort=created&direction=desc", 7)
       if "pull_request" not in i]
runs = []
for w in ("repropose.yml", "counsel-sign.yml"):
    runs += pages(f"repos/renavondata/opencode-runner/actions/workflows/{w}/runs", 5, "workflow_runs")

merges = sorted(t(p["merged_at"]) for p in prs if p["merged_at"])


def intervals(with_runs):
    iv = [(t(p["created_at"]), t(p["closed_at"]) if p["closed_at"] else END) for p in prs]
    for i in iss:
        a, b = t(i["created_at"]), (t(i["closed_at"]) if i["closed_at"] else END)
        if (b - a).total_seconds() <= 4 * 3600:  # longer ones are leftover issues, not sessions
            iv.append((a, b))
    if with_runs:
        iv += [(t(r["created_at"]), t(r["updated_at"]) if r["conclusion"] else END) for r in runs]
    return sorted(iv)


def quiet(iv):
    cur, q = START, []
    for a, b in iv:
        if b <= cur:
            continue
        if a >= END:
            break
        if a > cur:
            q.append((cur, min(a, END)))
        cur = max(cur, b)
        if cur >= END:
            break
    if cur < END:
        q.append((cur, END))
    return q


def starts(iv, rule):
    out = []
    for a, b in quiet(iv):
        s = a
        while s < b and not rule(s.minute):
            s = s.replace(second=0) + d.timedelta(minutes=1)
        if s < b and (b - s).total_seconds() >= 40:
            out.append(s)
    return out


days = (END - START).total_seconds() / 86400
for name, with_runs in (("v1", False), ("v2", True)):
    iv = intervals(with_runs)
    for label, rule in (("minute>=40", lambda m: m >= 40), ("any minute", lambda m: True)):
        s = starts(iv, rule)
        bad = sum(any(x < m <= x + d.timedelta(minutes=LAND) for m in merges) for x in s)
        print(f"{name} {label}: starts {len(s)} ({len(s) / days:.1f} a day), refused {bad} ({100 * bad // max(1, len(s))}%)")

# Added for entry 127: where the refusals fall, and how they turn on the landing time.
print()
iv = intervals(True)
for label, rule in (("any minute", lambda m: True), (":40 or later", lambda m: m >= 40), (":10 or later", lambda m: m >= 10)):
    s = starts(iv, rule)
    cells = []
    for land in (28, 31, 35):
        bad = sum(any(x < m <= x + d.timedelta(minutes=land) for m in merges) for x in s)
        cells.append(f"{land} min: {bad} ({100 * bad / len(s):.1f}%)")
    print(f"v2 {label}: starts {len(s)}; refused if the push lands within " + ", ".join(cells))
s = starts(iv, lambda m: True)
early = [x for x in s if x.minute < 10]
bad = sum(any(x < m <= x + d.timedelta(minutes=LAND) for m in merges) for x in early)
print(f"v2 any minute, starts in minutes :00 to :09: {len(early)}, refused {bad}")
