# The counsel courier — definition (counsel's text; v2 of 7 November 2026 after `REVIEW-meta-jack-astra.md` F30–F37)

This is the definition of the job that makes counsel's entries on steel. It lives here, in the court, so that a
change to how counsel's acts are made is a proposal read like any other, not a file on a machine (the same
reason `transcripts/sessions/` holds the session prompts). The runner's copy is
`.github/workflows/counsel-sign.yml` and `.github/scripts/counsel-sign.py` in `renavondata/opencode-runner`;
until that repository fetches the script from `main` here, the sovereign installs it by hand, which is a repair
by §7's letter and is listed as one. The job of 6 November (`counsel.yml`, `counsel-act.py`) keeps making
counsel's GitHub acts (pull requests, issues, closes) and skips sign requests.

## What it holds

- `~/.ssh/jack-counsel-3` (private; generated on steel by the sovereign; never in a prompt, a chat or a repository).
- `COUNSEL_GH_TOKEN` (else `~/.config/jack/gh-counsel`): `assize-reviewer`'s token, under the grant of seq 2131 —
  on `renavondata/jack`, opening counsel's proposals and closing its own stale ones with a comment; on
  `renavondata/opencode-runner`, filing and closing issues. It posts no comment on any other issue (the grant does
  not cover it); it reports in the job's log and, on a refusal, files one issue.

## When it runs

On every push to `counsel-requests` in `renavondata/opencode-runner` that adds `requests/sign-<id>.json`
(`{"id": "sign-<id>", "act": "sign", "branch": "counsel/<name>"}`), on the `build` lane, with a 45-minute
limit (a proposal's check runs the tests, the pins and the count). A push adding no sign request exits green
before it looks for the key.

## What it does, in order, for the branch each trigger names — and refuses otherwise

1. The branch is `counsel/<name>` with `<name>` one token, and `origin/counsel/<name>` exists.
2. **The worktree is RUNBOOK's:** `~/git/worktrees/jack/counsel/<name>`. If it exists, its branch must be
   `counsel/<name>` (else refused: the path belongs to another branch) and it is reset to `origin/counsel/<name>`;
   if not, it is created there. Nothing is ever deleted.
3. If the branch does not contain `origin/main`, `origin/main` is merged into it with the trailer
   `Proposer: counsel counsel-3` — the merge the `proposal` verb itself names as its prerequisite.
4. **The branch touches only counsel's paths.** `git diff --name-only origin/main...HEAD` is compared with the
   `counsel` row of `judge/scope.json` *at `origin/main`*; any path outside it (so any change to `tools/`,
   `kernel/`, `judge/`, `pins/`, `tests/`) refuses the request before anything is signed. After step 3 the
   branch's `tools/` is therefore `main`'s, and the verbs that run are the ones `main` holds.
5. **The whole request is read before anything runs.** `transcripts/requests/<name>.jsonl` at the head: every
   line parses; every `verb` is `forecast` or `proposal`; `proposal` occurs exactly once and last. Otherwise
   refused, nothing signed.
6. **Signed once, and the act finished.** The content commit is the last commit on the branch changing a path
   other than `log.jsonl`. If the branch's `log.jsonl` already holds a `proposal` entry by `counsel` with that
   commit, the request is done except for the verb's own unfinished ending: if no open pull request has the
   branch as head, one is opened (`gh pr create`, as the verb prints when its push or PR step failed). Nothing
   is signed again.
7. Otherwise, with `JACK_KEY=~/.ssh/jack-counsel-3` and `GH_TOKEN` counsel's, each `forecast` line runs as
   `tools/jack forecast "<claim>" --p <p> --by <by> [--type <type> --args '<args>']` and the `proposal` line as
   `tools/jack proposal --title "<title>"`, one at a time, each after the last has printed. The verbs push the
   branch and open the pull request. A refusal stops the request at that line: the entries before it stand as
   lawful (RUNBOOK: branch verbs undo nothing), the refusal is printed verbatim and filed as one issue, and
   nothing is retried or forced.

## What it never does

Sign anything not in the request file; run a verb other than the two; run a branch's own code (step 4); touch
`main`; delete a worktree or a branch; comment on an issue it did not file; read `log.jsonl` whole into a model.

## Custody, disclosed

Whoever can push a `counsel/*` branch to jack *and* a trigger to `counsel-requests` is counsel: today, the
sovereign's git credentials, which the drafting session uses for pushes (pushes are not acts, COUNSEL-OPEN row 44).
Two further routes reach the key and are not closed by this definition: every runner on steel runs as the login
user `g`, whose home holds every party key and a `gfrmin` login with admin scopes (`opencode-runner` issue #188),
and `run.yml` exports whatever `key:` an issue body names as `JACK_KEY` to the session it starts. So any session
on steel, and anyone who can file a `run` issue, can sign as any party. The fix is #188's — a runner user that
holds only the job's credentials — and it is the sovereign's, once; until then this courier is as strong as the
host, and the enforcement map's `irreversible` row says so.

## Pin, when the courier is code in this repository

`courier_signs_only_the_request`: the entries on the branch after the content commit are exactly the request
file's lines, in order, signed by `counsel`; a branch changing `tools/` is refused unsigned. Mutants: a forecast
entered from the prompt; `tools/` of the branch run instead of `main`'s.

## The script

```python
#!/usr/bin/env python3
"""Sign counsel's requested entries with counsel's key on steel (counsel-sign.yml). See counsel-courier.md."""
import json, os, subprocess, sys
HERE, BEFORE, AFTER = os.environ["GITHUB_REPOSITORY"], os.environ["BEFORE"], os.environ["AFTER"]
HOME = os.path.expanduser("~")
JACK, WT = f"{HOME}/git/jack", f"{HOME}/git/worktrees/jack"
KEY = f"{HOME}/.ssh/jack-counsel-3"
read = os.environ["READ_TOKEN"]

def sh(*args, cwd=None, env=None, ok=True):
    r = subprocess.run(list(args), cwd=cwd, env=env, capture_output=True, text=True)
    if ok and r.returncode:
        raise SystemExit(f"refused: {' '.join(args[:4])}\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return r

def gh_read(*args):
    return sh("gh", "api", *args, env={**os.environ, "GH_TOKEN": read}).stdout

def refuse(tok, rid, why):  # the grant covers filing issues on the runner; the refusal is the one issue filed
    body = f"counsel-sign refused {rid}: {why}\n\n<!-- counsel-sign-refusal: {rid} -->\n"
    sh("gh", "api", "-X", "POST", f"repos/{HERE}/issues", "-f", f"title=counsel-sign: {rid} refused",
       "-f", f"body={body}", env={**os.environ, "GH_TOKEN": tok}, ok=False)
    raise SystemExit(f"{rid}: refused: {why}")

if set(BEFORE) == {"0"}:
    files = [f["filename"] for f in json.loads(gh_read(f"repos/{HERE}/commits/{AFTER}"))["files"] if f["status"] == "added"]
else:
    files = [f["filename"] for f in json.loads(gh_read(f"repos/{HERE}/compare/{BEFORE}...{AFTER}"))["files"] if f["status"] == "added"]
files = sorted(f for f in files if f.startswith("requests/sign-") and f.endswith(".json"))
print(f"{len(files)} sign request(s): {files}")
if not files:
    sys.exit(0)
tok = os.environ.get("COUNSEL_GH_TOKEN") or ""
p = f"{HOME}/.config/jack/gh-counsel"
if not tok and os.path.exists(p):
    tok = open(p).read().strip()
if not tok:
    sys.exit("counsel's token is absent (COUNSEL_GH_TOKEN or ~/.config/jack/gh-counsel); nothing done")
if not os.path.exists(KEY):
    sys.exit(f"{KEY} is absent on this runner; nothing done")
ENV = {**os.environ, "GH_TOKEN": tok, "JACK_KEY": KEY}
print("identity:", json.loads(sh("gh", "api", "user", env=ENV).stdout)["login"])
sh("git", "fetch", "-q", "origin", cwd=JACK)
sh("git", "worktree", "prune", cwd=JACK)
scope = json.loads(sh("git", "show", "origin/main:judge/scope.json", cwd=JACK).stdout)["parties"]["counsel"]

for f in files:
    q = json.loads(sh("gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{HERE}/contents/{f}?ref={AFTER}",
                      env={**os.environ, "GH_TOKEN": read}).stdout)
    rid, branch = q["id"], q.get("branch", "")
    name = branch[len("counsel/"):]
    if q.get("act") != "sign" or not branch.startswith("counsel/") or not name or "/" in name or ".." in name:
        refuse(tok, rid, f"not a sign request on a counsel/<name> branch: {q}")
    if sh("git", "rev-parse", "--verify", "-q", f"origin/{branch}", cwd=JACK, ok=False).returncode:
        refuse(tok, rid, f"origin/{branch} does not exist")
    wt = f"{WT}/{branch}"                                   # RUNBOOK: a branch's worktree at ~/git/worktrees/jack/<branch>
    if os.path.isdir(wt):
        cur = sh("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=wt, ok=False).stdout.strip()
        if cur != branch:
            refuse(tok, rid, f"{wt} holds branch {cur!r}, not {branch}; nothing deleted")
        sh("git", "fetch", "-q", "origin", cwd=wt); sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt)
    else:
        sh("git", "worktree", "add", "-q", wt, "-B", branch, f"origin/{branch}", cwd=JACK)
    sh("git", "branch", "-q", f"--set-upstream-to=origin/{branch}", branch, cwd=wt)
    if sh("git", "merge-base", "--is-ancestor", "origin/main", "HEAD", cwd=wt, ok=False).returncode:
        sh("git", "-c", "user.name=counsel", "-c", "user.email=counsel@steel", "merge", "origin/main",
           "-m", f"Merge main into {branch}", "-m", "Proposer: counsel counsel-3", cwd=wt)
        print(f"{rid}: merged origin/main into {branch} (the verb's own prerequisite)")
    changed = sh("git", "diff", "--name-only", "origin/main...HEAD", cwd=wt).stdout.split()
    outside = [c for c in changed if not any(c == s or (s.endswith("/") and c.startswith(s)) for s in scope)]
    if outside:
        refuse(tok, rid, f"{branch} changes paths outside counsel's scope, so its code is not main's: {outside}")
    req = f"{wt}/transcripts/requests/{name}.jsonl"
    if not os.path.exists(req):
        refuse(tok, rid, f"{branch} has no transcripts/requests/{name}.jsonl")
    try:
        lines = [json.loads(l) for l in open(req) if l.strip()]
    except ValueError as x:
        refuse(tok, rid, f"request does not parse: {x}")
    verbs = [l.get("verb") for l in lines]
    if not lines or verbs[-1] != "proposal" or verbs.count("proposal") != 1 or any(v not in ("forecast", "proposal") for v in verbs):
        refuse(tok, rid, f"the request must be forecast lines then exactly one proposal line, last: {verbs}")
    content = sh("git", "log", "--format=%H", "origin/main..HEAD", "--", ".", ":!log.jsonl", cwd=wt).stdout.split()
    content = content[0] if content else sh("git", "rev-parse", "HEAD", cwd=wt).stdout.strip()
    signed = any(e["type"] == "proposal" and e["proposer"] == "counsel" and e["body"].get("commit") == content
                 for e in (json.loads(l) for l in open(f"{wt}/log.jsonl") if l.strip()))
    if signed:
        n = sh("gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number", "--jq", ".[0].number", cwd=wt, env=ENV).stdout.strip()
        if not n:  # the verb's own unfinished ending: push stood, PR did not open
            sh("git", "push", "-q", "-u", "origin", branch, cwd=wt)
            title = sh("git", "log", "-1", "--format=%s", cwd=wt).stdout.strip()
            print(sh("gh", "pr", "create", "--base", "main", "--head", branch, "--title", title[:200],
                     "--body", "Proposer: counsel counsel-3", cwd=wt, env=ENV).stdout)
        print(f"{rid}: {branch}: content commit {content[:12]} already proposed; pull request {n or 'opened now'}; nothing signed")
        continue
    for i, l in enumerate(lines):
        if l["verb"] == "forecast":
            cmd = ["tools/jack", "forecast", l["claim"], "--p", str(l["p"]), "--by", l["by"]]
            if "type" in l: cmd += ["--type", l["type"]]
            if "args" in l: cmd += ["--args", json.dumps(l["args"], separators=(",", ":"))]
        else:
            cmd = ["tools/jack", "proposal", "--title", l["title"]]
        r = subprocess.run(cmd, cwd=wt, env=ENV, capture_output=True, text=True)
        print(f"{rid}: line {i + 1} {l['verb']}: exit {r.returncode}\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
        if r.returncode:
            refuse(tok, rid, f"line {i + 1} ({l['verb']}) refused; the lines before it stand; nothing retried:\n{(r.stdout + r.stderr)[-1200:]}")
    print(f"{rid}: {branch}: {len(lines)} line(s) signed")
```
