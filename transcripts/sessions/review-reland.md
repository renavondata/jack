model: openai/gpt-5.4-mini
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: re-land the formal review of BRIEF-{WINDOW} by {MODEL} under a file name of its own — the same bytes, no new read (renavondata/jack)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read or write anything outside this worktree. Do not read `log.jsonl` whole. Now is {NOW}.

**You read no brief and you judge nothing.** A session of `{MODEL}` has already read `transcripts/BRIEF-{WINDOW}-draft.md` at its present bytes and committed its review. Two reviews were once given the same file name, and a re-proposal wrote one over the other; a review that was overwritten, or that overwrote another, is not on `main` in the form `tools/jack push --opens {WINDOW}` accepts (RUNBOOK, `jack push`: the commit that adds the file must have added the bytes `main` holds). Your whole task is to run the script below once and then, if it wrote a file, three commands. Edit no file by hand. If anything fails in a way this text does not cover, stop and report it; never choose between two versions of a file.

**The script.** Run it exactly as written:
```
python3 - <<'EOF'
import os, re, subprocess, sys
W, MODEL, STAMP = "{WINDOW}", "{MODEL}", "{STAMP}"
MAIN = os.environ.get("RELAND_MAIN", "origin/main")  # tests only: a main as it stood
def git(*a):
    r = subprocess.run(["git", *a], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def one(*a):
    o = git(*a)
    return o.decode().strip() if o is not None else None
subprocess.run(["git", "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*"], check=True)
brief = "transcripts/BRIEF-" + W + "-draft.md"
cur = one("rev-parse", MAIN + ":" + brief)
pat = re.compile("transcripts/REVIEW-" + re.escape(W) + r"-[A-Za-z0-9._-]+\.md")
found = []  # (commit time, blob, commit, path, bytes): every commit on any branch that wrote an accepting review by MODEL of the brief at main's bytes
for c in (one("log", "--all", "--format=%H", "--", "transcripts/REVIEW-" + W + "-*.md") or "").split():
    for p in (one("diff-tree", "--no-commit-id", "--name-only", "-r", "--root", c) or "").split("\n"):
        if not pat.fullmatch(p):
            continue
        data = git("show", c + ":" + p)
        if data is None:
            continue
        head = data.decode("utf-8", "replace").split("\n")[:3]
        if len(head) < 3 or head[0] not in ("VERDICT: ACCEPT", "VERDICT: ACCEPT WITH OBLIGATIONS"):
            continue
        tree = re.fullmatch("Reviewed tree: ([0-9a-f]{40})", head[1])
        if not tree or not head[2].startswith("Reader: reviewer; model " + MODEL + ";"):
            continue
        if subprocess.run(["git", "merge-base", "--is-ancestor", tree.group(1), MAIN]).returncode:
            continue
        if one("rev-parse", tree.group(1) + ":" + brief) != cur:
            continue
        found.append((int(one("log", "-1", "--format=%ct", c)), one("rev-parse", c + ":" + p), c, p, data))
if not found:
    sys.exit("NOTHING TO RE-LAND: no accepting review by " + MODEL + " of " + brief + " at main's bytes on any branch")
found.sort()
when, blob, commit, path, data = found[0]  # the earliest: the review as its reader's own session committed it
others = sorted({f[1] for f in found} - {blob})
if others:
    sys.exit("NOTHING TO RE-LAND: later commits hold different bytes for this review (" + ", ".join(o[:12] for o in others) + "); counsel is told")
for q in (one("ls-tree", "-r", "--name-only", MAIN, "--", "transcripts/") or "").split("\n"):
    if pat.fullmatch(q) and one("rev-parse", MAIN + ":" + q) == blob:
        adds = (one("log", "--diff-filter=A", "--format=%H", MAIN, "--", q) or "").split()
        last = one("log", "-1", "--no-merges", "--format=%H", MAIN, "--", q)
        if last in adds:
            sys.exit("NOTHING TO RE-LAND: " + q + " on main holds these bytes as the commit that added it left them")
new = "transcripts/REVIEW-" + W + "-" + STAMP + "-" + MODEL.split("/")[0] + ".md"
if one("rev-parse", "-q", "--verify", MAIN + ":" + new) or os.path.exists(new):
    sys.exit("NOTHING TO RE-LAND: " + new + " exists already; counsel is told")
open(new, "wb").write(data)
if one("hash-object", new) != blob:
    os.remove(new)
    sys.exit("NOTHING TO RE-LAND: the bytes written do not hash to " + blob)
print("WROTE " + new + " from " + commit[:12] + ":" + path + " (blob " + blob[:12] + ", " + str(len(found)) + " commits hold it)")
EOF
```
It ends with one line.
- **`NOTHING TO RE-LAND: …`** — write nothing and propose nothing. That line is your report.
- **`WROTE <new path> from <commit>:<old path> …`** — run these one at a time, with the paths and the commit as printed:
  1. `git add <new path>`
  2. `git commit -m "REVIEW-{WINDOW}: the review by {MODEL}, re-landed byte for byte from <commit>:<old path>" -m "Proposer: reviewer openai/gpt-5.4-mini <this issue's number>"`
  3. `tools/jack proposal --title "REVIEW-{WINDOW}: the review by {MODEL}, re-landed byte for byte"` with the bash tool's `timeout` set to `900000`. If the push is refused, run the two commands the verb prints.

**Your report** is your final message: the script's last line, and the PR number or that nothing was proposed. The runner posts it on this issue; run no `gh issue comment`.
