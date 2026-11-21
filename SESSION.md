model: openai/gpt-6.1-sol
key: ~/.ssh/jack-builder
branch: move-promotion-judge

# builder: build the move of the promotion evaluator under `judge/`, with SPEC §10 item 15 `promote_unmet` (ruling of 20 November 2026; grant seq 6851)

You are the **builder** (`JACK_KEY=~/.ssh/jack-builder`, party `builder`), in the worktree `~/git/worktrees/jack/move-promotion-judge` on branch `move-promotion-judge`. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it.

This branch is a **push branch**: the sovereign applies it to `main` with `jack push`, because it changes the trusted base. So you run no `tools/jack` verb at all, and open no pull request. You commit on this branch and push it with `git push origin move-promotion-judge`, nothing else.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here. Run `python3 -m py_compile` on each Python file you change.

**Where you start.** The sovereign has published `move-promotion-judge` with one commit, `2d99d242`. That commit is his cherry-pick of counsel's text, whose subject begins `SPEC §10 item 15 promote_unmet`.
1. Run `git fetch -q origin main move-promotion-judge`.
2. `git status --porcelain` must print nothing.
3. `git log --oneline origin/main..origin/move-promotion-judge` must show exactly that one commit.
4. Then:
   - if `git rev-parse HEAD` equals `git rev-parse origin/move-promotion-judge`, go on;
   - otherwise, if `git merge-base --is-ancestor HEAD origin/main` succeeds, the runner cut a fresh branch from `main`: run `git reset -q --hard origin/move-promotion-judge`;
   - otherwise the worktree holds other work: stop and report, and reset nothing.
5. `sha256sum SPEC.md` must give `72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2`.

If any check fails, stop and report. Never change `SPEC.md`: the sovereign's grant at log seq 6851 names it by that hash, and a push whose `SPEC.md` differs installs nothing.

**The text you build to** is `SPEC.md` on this branch:
- §10 item 15 (from `15. **promote_unmet**`);
- the line `Items 11–15 apply to every judged log, the self-check included.`;
- the paragraph headed **The promotion evaluator**.

Read them whole before writing code. The sovereign read that text before this build (CHARTER A2.10; his grant, seq 6851). Build what it says and nothing it does not. The answers it carries out are in `transcripts/RULING-20261120-promotion-judge.md` (answers 2, 4, 8 and 16; points 4 and 5). Where the text and the code today disagree, the text governs. Where the text is silent, keep today's behaviour.

**What to build.** Commit each part as you finish it, so that nothing is lost if the session ends. Hand commits end with the paragraph `Proposer: builder openai/gpt-6.1-sol runner-issue-<the value of $ISSUE>` (RUNBOOK, Common to every verb; use the branch name if `$ISSUE` is empty).

1. **The move.**
   - `git mv tools/status.py judge/status.py` and `git mv tools/value.py judge/value.py`.
   - Move the three functions `judge/value.py` takes from `tools/entry.py` (`now`, `read_log`, `resolution_rates`) into one new file under `judge/`, with their bodies unchanged. `tools/entry.py` then imports them from there, so that its other users work as before.
   - In the two moved files, change **only**:
     - (a) the import lines, so that they import nothing outside the standard library and the trusted base (`kernel/`, `judge/`);
     - (b) criterion 3's walk in `c2a_tree_evidence`: the call `git_bytes(root, 'rev-list', f'{start}..{rev}')` gains `'--first-parent'`, as the same function's other walk already has.
   - Leave everything else in them byte for byte. That includes the two lines reading `tools/status.py` from a tree by that path (today lines 436 and 437): the ruling's point 4 leaves them to C2a-3's change. `git diff -M origin/main -- tools/status.py tools/value.py judge/status.py judge/value.py` must show the two renames and nothing but (a) and (b). Name the old paths too, or git cannot pair the renames and shows each file as wholly new.
2. **Their callers.** Make every caller under `tools/`, `tests/`, `harness/` or `sim/` use the moved files and the moved functions, among them `tools/jack` (also its `from tools import status, clerk`), `tools/clerk.py`, and the tests that import them or run `tools/status.py`, grouped imports such as `from tools import clerk, status` included. Find them with `git grep -n -E 'tools/(status|value)[.]py|tools[.](status|value)|from tools import .*(status|value)'` and read each hit.
   - **One kind of hit is not a caller.** A test that writes the evaluator's source into a synthetic history at the path `tools/status.py` does so for the two lines that read that path from a tree (step 1). It keeps that path. Only reads of the live checkout's own source follow the move.
   - **Do not touch `pins/` or `spec/vectors/`.** They are the reviewer's (A2.9), and a reviewer updates them on this branch after you. List in your report every pin that fails only because a path moved.
3. **Item 15 in the judge.** Add item 15 to `judge/judge.py` and to the self-check, exactly as the text states:
   - the installing push;
   - the entry commits;
   - conditions (a) to (d);
   - the evaluator in force, extracted from git as the kernel is;
   - the subject accepted by its own parser;
   - no time limit;
   - refusal when the evaluator cannot decide;
   - the attested files listed in the judge's report.

   Its refusal reason is `promote_unmet`. On every commit before the sovereign's push, the self-check refuses by design, because there is no installing push yet. So test item 15 through synthetic repositories that hold a grant and a push, as the existing judge tests build theirs.
4. **The promote verb** (`jack decision promote`, in `tools/jack`), as the text states:
   - it commits the three evidence files (the tests run, the runs and the acts table it assessed with) under `transcripts/evidence/`, with the entry, in one commit on the commit it assessed;
   - the entry's `body.evidence` is `{run, runs, acts}`, each `{path, sha256}`.

   Keep the rest of what it does today. Counsel's revision of RUNBOOK lands on `main` before the sovereign's push (RUNBOOK, Text before code). It restates item 15 for this verb, and the moved paths, and adds nothing to them. So the text you build the verb to is item 15. Say in your report every place where RUNBOOK on `main` today still describes the old behaviour or paths.
5. **The workflows.** `.github/workflows/tests.yml` checks out the whole history (`fetch-depth: 0`), as `judge.yml` already does.
6. **Your tests,** under `tests/`, for what you built: item 15's conditions (a) to (d), the installing push, the move. Pins are not yours.

**What you do not do.** Change no `SPEC.md`, `CHARTER.md`, `RUNBOOK.md`, `judge/scope.json`, `pins/` or `spec/vectors/`. Run no `tools/jack` verb, and do not propose. Build nothing for C2a-3, C2c-1 or any later window.

**Checks before you push.** Run each and copy its result into your report:
- (a) `python3 -m unittest discover -s tests -t .`. Every failure must be in a test of `pins/` itself, such as `tests/test_pins.py`'s check that each mutant's target exists, and must fail only because a pin names a path or text that this move took elsewhere. That includes the mutants of the three functions taken from `tools/entry.py`. List each such failure. Fix any other failure. Do not weaken a test of `pins/` to make it pass: the reviewer updates the pins on this branch after you;
- (b) `python3 pins/run.py`: list every failing pin, and say for each whether it fails only because a path or text moved;
- (c) `python3 tools/count_kernel.py`; and the lines under `judge/scope.json`'s `counted` prefixes, counted as judge item 10 counts them, at `origin/main` and at your head, both numbers. The sovereign's push states their difference (ruling, answer 6);
- (d) the diff in step 1 shows only (a) and (b);
- (e) **three replay rows**, from the table on `main` (`git show origin/main:spec/vectors/promotion-replay.json`), as the paragraph defines a run. Run the moved evaluator from this worktree on rows 592, 593 and 705 (0-based, first-parent order of its *T*). Row 592 must equal its stored row exactly. At rows 593 and 705, only the two marked lines may differ, and as the marks state. This is a spot check, not the acceptance test, which a reviewer runs.

**Time.** The job stops at 180 minutes, and a single command at 15. By minute 160, commit what you have and push the branch, even if unfinished, and say so.

**Report.** Give:
- the branch head;
- `git diff --stat origin/main`;
- the step 1 diff;
- the results of checks (a) to (e);
- the pins that fail and why;
- every place where RUNBOOK on `main` today describes the old behaviour or paths;
- anything in the text you could not build as it stands, quoted, with the reason.

End with one line: `PUSHED <head>` or `STOPPED: <reason>`.
