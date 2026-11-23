model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: make the fix that `transcripts/{BRANCH}.md` specifies, and propose it (renavondata/jack)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included: put scratch files and logs under `.review-logs/` in the worktree, which you do not commit.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here. Run `python3 -m py_compile` on each Python file you change.

**The text you build to** is `transcripts/{BRANCH}.md` on `main`, a counsel text the sovereign has read (CHARTER A2.10: "Code is written to a text Guy has read"). Its sections **The change**, **Paths** and **Acceptance** are what you build and check. The rest of it gives the reasons. Build what it says and nothing it does not. Where it is silent, keep today's behaviour. Where it and the code disagree, the text governs, unless the text says the code governs.

**Before anything else.** If any of these checks fails, stop, report which, and change nothing.
1. Run `git fetch -q origin main`. `git status --porcelain` must print nothing, and `git merge-base --is-ancestor origin/main HEAD` must succeed, with `git log --oneline origin/main..HEAD` printing nothing.
2. Run `git show origin/main:transcripts/{BRANCH}.md | sha256sum`, and keep the 64 hex digits as T.
3. **His read.** Find a `decision` entry on `main`'s log whose `proposer` is `guy`, whose kind is `grant`, and whose subject contains `read transcripts/{BRANCH}.md at sha256 ` followed by T. Compose the search yourself, for example with `python3` reading `git show origin/main:log.jsonl` line by line, and print the entry's `seq` and `ts`. If there is none, stop: no code is written to a text he has not read.
4. **Its paths.** Every path the text's **Paths** section lists under **May change** must lie under one of the reviewer's paths in `judge/scope.json` (`parties.reviewer`). If any does not, stop: that part is another party's. What the section lists under **May not change** is not tested here.

**What you do.**
- Make the change in **The change**, within **Paths**, and nothing else.
- Commit each part as you finish it, so that nothing is lost if the session ends. Hand commits end with the paragraph `Proposer: reviewer {MODEL} runner-issue-<the value of $ISSUE>`, as RUNBOOK's *Common to every verb* asks (use `{BRANCH}` if `$ISSUE` is empty).
- Run every check in **Acceptance**, and these four, which every fix runs. A line of **Acceptance** that only asks you to report something after the proposal is made is done after it, and does not hold the proposal back. Keep each one's output under `.review-logs/`, and give each one's elapsed time:
  - (a) `python3 -m unittest discover -s tests -t .`. It must pass, and report the same number of tests as on `origin/main` unless the text adds or removes tests by name;
  - (b) `python3 pins/run.py`. Its last line must be the same as on `origin/main` unless the text says otherwise;
  - (c) `python3 tools/count_kernel.py`;
  - (d) the counted lines under `judge/scope.json`'s `counted` prefixes, counted as judge item 10 counts them, at `origin/main` and at your head. The head must be at or under `cap`.

  Run long commands with `nohup` in the background, logging under `.review-logs/`, and wait for them in steps of at most ten minutes. A single command stops at 15 minutes.
- `git diff --name-only origin/main HEAD` must list only paths the text lists under **May change**. If the text has a **Size** section, the counted lines of (d) at your head, less those at `origin/main`, must be within it.
- If every check holds, propose: `tools/jack proposal --title '{BRANCH}: <the text's heading after its colon>'`. It runs the test suite and can take thirty minutes, so call it with the bash tool's `timeout` set to `2400000`. If the push is refused because `main` moved, run `git fetch -q origin main && git merge --no-edit -m 'Merge main into {BRANCH}' -m 'Proposer: reviewer {MODEL} runner-issue-<the value of $ISSUE>' origin/main`, re-run (a) and (b), and propose again, once.
- If a check fails and you cannot meet it within the text, do not propose. Push the branch with `git push origin {BRANCH}` and report.

**What you do not do.**
- Change no path outside **Paths**.
- Change no assertion of any test or pin the text does not name.
- Run no `tools/jack` verb but `proposal`.

**Time.** The job stops at 180 minutes. By minute 160, commit what you have and push the branch, even if unfinished, and say so.

**Report.** Give:
- T and his grant's `seq`;
- the branch head and `git diff --stat origin/main`;
- each check's result and elapsed time, at `origin/main` and at your head where the text asks for both;
- the proposal's number, or why there is none;
- anything in the text you could not build as it stands, quoted, with the reason.

End with one line: `PROPOSED <number>`, `PUSHED <head>` or `STOPPED: <reason>`.
