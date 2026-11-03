model: openai/gpt-5.4-mini
key: ~/.ssh/jack-{KEY}
branch: {BRANCH}-r

# {PARTY}: re-propose PR #{N} ({BRANCH}) on a fresh prefix — the same content, the same entries (renavondata/jack)

You are the **{PARTY}** (`JACK_KEY=~/.ssh/jack-{KEY}`, party `{PARTY}`), in the worktree `~/git/worktrees/jack/{BRANCH}-r` on branch `{BRANCH}-r`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read`/`Glob` a path outside it. Do not read `log.jsonl` whole. Read RUNBOOK `## jack forecast`, `## jack resolve` and `## jack proposal` only.

PR #{N} (branch `{BRANCH}`, your own key's work) went stale: `main` gained entries before it merged and the herald's verb refused it as CONFLICTING. Nothing in it was wrong. Re-create it here, identically, on the current prefix.

1. **Content.** `git fetch -q origin {BRANCH}`. List the stale branch's commits that are not entry commits: `git log --reverse --format=%H origin/main..origin/{BRANCH} -- . ':!log.jsonl'`. Cherry-pick each in that order (`git cherry-pick <sha>`); if a cherry-pick stops on `log.jsonl`, `git checkout --ours log.jsonl && git add log.jsonl && git cherry-pick --continue` — the entries are re-made below, never copied. After the picks, `git diff --stat origin/main` must show every file PR #{N} changed except `log.jsonl`.
2. **Entries.** Print the stale branch's entries that are not on `main`:
   ```
   python3 - <<'EOF'
   import json,subprocess
   main=[json.loads(l) for l in open('log.jsonl')]
   stale=[json.loads(l) for l in subprocess.check_output(['git','show','origin/{BRANCH}:log.jsonl'],text=True).splitlines()]
   common=0
   while common<min(len(main),len(stale)) and main[common]==stale[common]: common+=1
   for e in stale[common:]:
       if e['type']!='proposal': print(json.dumps({'type':e['type'],'body':e['body']}))
   EOF
   ```
   **Skip any `forecast` of type `world.renavon` whose `args.window_utc[0]` is at or before now — and "now" is the UTC instant `date -u +%Y-%m-%dT%H:%M:%SZ` prints, never a local clock: print it, print each window's `window_utc[0]`, and compare the two strings before deciding (on 3 November a session skipped twenty-four forecasts for windows five to eight hours ahead on the belief that they had begun; it had read Hong Kong time)**: a forecast signed at or after its window's start is `rigged` and worth nothing (REVIEW-C2a-am3 F1); list those you skip, and if every entry would be skipped, propose nothing and report that. **This rule is for lines whose `type` is `forecast` and nothing else. A line whose `type` is `resolution` is always re-entered, whatever window its forecast named: the resolution is what discharges the writ, and skipping it lets the writ expire.** On 3 November at 14:03Z a re-proposal skipped six resolutions (of forecasts 882–887) as if they were forecasts of a begun window, and their writs were left four hours from expiry with nothing filed. Re-enter each of the rest, in order, **one verb at a time — wait for each to print its result before starting the next; two verbs run together take the same sequence number and the branch is unusable** — with the verb: a `forecast` → `tools/jack forecast "<claim>" --p <p> --by <resolves_by> --type <type> --args '<args as JSON>'` (claim, p, resolves_by, type and args verbatim); a `resolution` → `tools/jack resolve <forecast> --outcome <outcome> --evidence "<evidence verbatim>"`. The proposal entry is not copied: the verb makes it in step 3. If a resolution is refused because the forecast is already resolved on `main`, skip it and say so.
3. **Propose.** `tools/jack proposal --title "{TITLE} (re-proposed: PR #{N} went stale)"` — it runs the test suite and can take ten minutes, so call it with the bash tool's `timeout` set to `900000`. If the push is refused, run the two commands the verb prints and report their output. Report the PR number and the entries re-made (type, seq or forecast, outcome or p). (If `main` moves again before the herald merges this one, the herald files the next re-proposal; that is not yours to wait for.)
