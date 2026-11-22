#!/usr/bin/env python3
"""queue_check.py: the head of QUEUE.md's queue, computed from the public record. It binds nothing.

Run in any clone of renavondata/jack:   python3 -I queue_check.py
Exit: 0 fine; 2 a frozen text changed; 3 a budget is spent; 4 the page has lapsed.
"""
import argparse, datetime as dt, hashlib, re, json, subprocess, sys

PRED = "transcripts/RESEARCH-meta-jack-20261107.md"   # the rows B0 to B7 live here, on main
STATED_END = "2026-11-30T00:00:00Z"                    # C2a-prime's stated end: no fix and no opening before it
BUILT, TEST_AFTER, LAPSE = "2026-11-22T09:00:00Z", "2026-12-07T00:00:00Z", "2027-01-31T00:00:00Z"
NOTES, MAIN = "origin/adviser/notes", "origin/main"
BRANCHES = ["--remotes=origin/counsel/*", "--remotes=origin/agent/*"]


def git(*a):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"git {' '.join(a)}: {r.stderr.strip()}")
    return r.stdout


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def first(es, test, after=-1):
    return next((e for e in es if e["seq"] > after and test(e)), None)


def decision(kind, *subjects):
    return lambda e: e["type"] == "decision" and e["body"].get("kind") == kind and e["body"].get("subject") in subjects


def is_push(e):
    return e["type"] == "push"


def a6(es, prev):
    return first(es, lambda e: e["type"] == "amend" and e["body"].get("id") == "A6")


def fresh_veto(es, prev):   # A6, clause 1: a veto naming C2a-prime at or above A6's activate_at
    return first(es, decision("veto", "C2a-prime", "C2a"), prev["body"]["activate_at"] - 1)


def move(es, prev):         # the push after that veto, with the evaluator under judge/ on main
    moved = subprocess.run(["git", "cat-file", "-e", f"{MAIN}:judge/status.py"], capture_output=True).returncode == 0
    return first(es, is_push, prev["seq"]) if moved else None


def c2a3_open(es, prev):    # his fix naming C2a-prime after its stated end, then the first push after it
    fix = first(es, lambda e: e["type"] == "decision" and e["body"].get("kind") == "fix" and
                str(e["body"].get("subject", "")).startswith("C2a-prime:") and e["ts"] > STATED_END, prev["seq"])
    return fix and first(es, lambda e: is_push(e) and e["ts"] > STATED_END, fix["seq"])


def promoted(name):
    return lambda es, prev: first(es, decision("promote", name), prev["seq"])


def opened(es, prev):
    return first(es, is_push, prev["seq"])


# id, title, has a day budget, check(entries, the entry that passed the step before) -> the entry that passes this one
STEPS = [("Q1", "A6 is in force", True, a6),
         ("Q2", "C2a-prime is ended by a veto under A6", True, fresh_veto),
         ("Q3", "the promotion evaluator is moved under judge/ by his push", True, move),
         ("Q4", "C2a-3 is open: his fix of C2a-prime, then the opening push, both after 2026-11-30T00:00:00Z", True, c2a3_open),
         ("Q5", "C2a is promoted", False, promoted("C2a"))]
for w in ("C2b", "C2c-1", "C2c-2", "C2c-3"):
    STEPS += [(f"Q{len(STEPS) + 1}", f"{w} is open", True, opened),
              (f"Q{len(STEPS) + 2}", f"{w} is promoted" + (": bootstrapped, B0 to B7 hold" if w == "C2c-3" else ""), False, promoted(w))]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--page", help="read the page from this file (for testing)")
    ap.add_argument("--predicate", help="read the predicate's file from this file (for testing)")
    ap.add_argument("--now", help="pretend it is this instant (for testing)")
    a = ap.parse_args()
    if not a.no_fetch:
        git("fetch", "-q", "origin", "+refs/heads/main:refs/remotes/origin/main", "+refs/heads/adviser/notes:refs/remotes/origin/adviser/notes",
            "+refs/heads/counsel/*:refs/remotes/origin/counsel/*", "+refs/heads/agent/*:refs/remotes/origin/agent/*")
    now = a.now or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    es = [json.loads(line) for line in git("show", f"{MAIN}:log.jsonl").splitlines() if line.strip()]

    # the page: what is frozen, his words, the budget
    page = open(a.page).read() if a.page else git("show", f"{NOTES}:QUEUE.md")
    frozen, _, words = page.partition("\n## Words")
    # under Words, one line each:  ADOPTED|REVIEW|OVERRIDE <instant>[ sha256 <the page's new hash>] — "his words"
    lines = re.findall(r"^(ADOPTED|REVIEW|OVERRIDE) (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)(?: sha256 ([0-9a-f]{64}))?", words, re.M)
    hashes = [h for _, _, h in lines if h]
    adopted = next((t for k, t, _ in lines if k == "ADOPTED"), None)
    overrides = sum(k == "OVERRIDE" for k, _, _ in lines)
    budget = dict(zip(("drafts", "reads", "days"), map(int, re.search(r"Budget: drafts (\d+), cold reads (\d+), days (\d+)", frozen).groups())))
    pred_text = open(a.predicate).read() if a.predicate else git("show", f"{MAIN}:{PRED}")
    pred = sha("\n".join(row for row in pred_text.splitlines() if re.match(r"- \*\*B\d ", row)))
    checks = {"predicate": pred == re.search(r"predicate sha256 `([0-9a-f]{64})`", frozen).group(1),
              "checker": sha(open(__file__).read()) == re.search(r"checker sha256 `([0-9a-f]{64})`", frozen).group(1),
              "page": not adopted or bool(hashes) and hashes[-1] == sha(frozen)}

    # the head: the first step whose check fails
    passed, prev = [], None
    for sid, title, timed, check in STEPS:
        entry = check(es, prev)
        if entry is None:
            break
        passed.append(entry)
        prev = entry
    head = len(passed)
    print(f"QUEUE CHECK {now}  main@{git('rev-parse', '--short', MAIN).strip()}  log to seq {es[-1]['seq']}  page "
          + (f"adopted {adopted}" if adopted else "NOT ADOPTED: it binds nothing yet"))
    for i, (sid, title, timed, _) in enumerate(STEPS):
        mark = "done" if i < head else "HEAD" if i == head else "    "
        print(f"  {mark}  {sid:<4}{title}" + (f"  (seq {passed[i]['seq']}, {passed[i]['ts']})" if i < head else ""))
    code, spent = 0, []
    if head < len(STEPS):
        since = max([adopted or BUILT] + ([passed[-1]["ts"]] if passed else []) + ([STATED_END] if STEPS[head][0] == "Q4" else []))
        days = max(0, (dt.datetime.fromisoformat(now[:19]) - dt.datetime.fromisoformat(since[:19])).days)
        drafts = len(set(git("log", f"--since={since}", "--no-merges", "--format=%H", *BRANCHES, "--", "transcripts/*.md",
                             ":(exclude)transcripts/REVIEW-*").split()))
        gh = subprocess.run(["gh", "api", "--paginate", f"repos/renavondata/opencode-runner/issues?state=all&per_page=100&since={since}",
                             "--jq", f'.[] | select(.pull_request | not) | select(.created_at >= "{since}") | .title'], capture_output=True, text=True)
        reads = sum(t.startswith("reader:") for t in gh.stdout.splitlines()) if gh.returncode == 0 else None
        timed = STEPS[head][2]
        print(f"head {STEPS[head][0]} since {since}: drafts {drafts}/{budget['drafts']}, cold reads "
              f"{'not counted (no gh access to the runner)' if reads is None else str(reads) + '/' + str(budget['reads'])}, "
              + (f"days {days}/{budget['days']}" if timed else f"days {days} (no day budget: the window's stated end governs)"))
        spent = [n for n, v in (("drafts", drafts), ("reads", reads), ("days", days if timed else None)) if v is not None and v > budget[n]]
    sessions = {s for s in git("log", "--since=24.hours", "--format=%(trailers:key=Claude-Session,valueonly)", *BRANCHES, NOTES).split() if s}
    print("frozen: " + ", ".join(f"{k} {'unchanged' if ok else 'CHANGED'}" for k, ok in checks.items())
          + f"   his overrides: {overrides}   sessions that wrote in the last 24 h: {len(sessions)}")
    if not all(checks.values()):
        print("STOP: a frozen text has changed with no review or OVERRIDE recorded under Words.")
        code = 2
    elif spent:
        print(f"STOP: the head's budget is spent ({', '.join(spent)}). Put one choice to him: ship with the known defects listed, or cut the step down.")
        code = 3
    if head == len(STEPS) or now >= LAPSE or (now >= TEST_AFTER and head < 4):
        print("LAPSED: " + ("the last step has passed." if head == len(STEPS) else "its end date or its test of 6 December has passed. What follows is his to decide."))
        code = 0 if head == len(STEPS) else 4
    sys.exit(code)


if __name__ == "__main__":
    main()
