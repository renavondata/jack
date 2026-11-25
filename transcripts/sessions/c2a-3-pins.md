model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: write the eight pins of C2a's third window and re-aim the pin `replay_drift` (BRIEF-C2a-3, §Pins and §The code)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included. Your scratch directory is `.pins/` at the top of the worktree. Never `git add` that directory: add the paths you commit by name. Do not set `TMPDIR`, `TEMP` or `TMP`, in your shell or for any command you run. Never edit `log.jsonl`.

**The push branch.** The window's code is on `opening-c2a-3`, a branch the sovereign has published. He applies it to `main` with `jack push` when the window opens. So you run no `tools/jack` verb at all, and open no pull request. Your own branch, `{BRANCH}`, is only where this session works: step 3 sets it to the published branch, you commit on it, and you publish each commit with `git push -q origin HEAD:opening-c2a-3`. You push nothing else, and never with force. If that push fails, stop and report git's message, and do not pull, merge or rebase.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here. Run `python3 -m py_compile` on each Python file you change.

**The clock.** Step 1 writes the session's start, in seconds, to `.pins/start`. Every minute named below is counted from it. The job stops at 180 minutes, and a single command at 15 unless this text gives it longer.

**Where you start.** The first commit of `opening-c2a-3` over `main` is the sovereign's cherry-pick of counsel's patch. The builder's session (runner #1322) put three commits on it, and its last is *B*, `7d7f89471a52c248ad9c3214645f7e936235ab4f`. Commits after *B*, if there are any, are an earlier session's work to this same text: you continue it from what those commits and their messages show, and your report says so.
1. If `.pins/` already exists, stop and report: a session of this template begins from nothing, on a branch of its own. Otherwise run `mkdir .pins && date -u +%s > .pins/start`.
2. Run `git fetch -q origin main opening-c2a-3`; if it fails, run it once more. Then `git status --porcelain --untracked-files=normal` must print `?? .pins/` and nothing else, and `git merge-base --is-ancestor HEAD origin/main` must succeed: the runner cut this branch from `main` a moment ago. If the fetch fails twice, or either test fails, stop and report.
3. Run `git reset -q --hard origin/opening-c2a-3`.
4. `git merge-base --is-ancestor 7d7f89471a52c248ad9c3214645f7e936235ab4f HEAD` must succeed.
5. `sha256sum judge/status.py` must give `44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0`, `sha256sum judge/value.py` must give `1ea89facaff6aa27e7bd959dfdf24202a2f8afe39ecb078a0b4bf8e42c481845`, and `sha256sum spec/vectors/promotion-replay-c2a-3.json` must give `943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77`.
6. `sha256sum transcripts/BRIEF-C2a-3-draft.md` must give `a5c331b40d1e81f959e147461884b3a55e11d829933bfd2296d660a526433945`. The sovereign read that text before the build: his grant is seq 7615 on `main`'s log.
7. **Every commit after *B*** is held to two tests: an earlier session's now, and each of your own before you push it. With no commit after *B* both commands print nothing. If an earlier session's commit fails either, stop and report.
   - `git log -m --no-renames --name-only --format= 7d7f89471a52c248ad9c3214645f7e936235ab4f..HEAD | grep . | sort -u` names every path that any of those commits touched. It must name nothing outside `pins/`.
   - `git log --format='%h %(trailers:key=Proposer,valueonly)' 7d7f89471a52c248ad9c3214645f7e936235ab4f..HEAD | grep .` prints a line for each of those commits: its hash, then the fields of its trailer. Each line must be a hash, then `reviewer`, then at least one field more, with no `<` anywhere in it. Any other line fails this test. A trailer that is missing or not filled is one `jack push` refuses a branch for.

If any check fails, stop and report. Change no file outside `pins/`: the evaluator and its tests are the builder's, and your pins test them (SPEC §10.8).

**The text you write to** is `transcripts/BRIEF-C2a-3-draft.md` on this branch:
- §Pins, whole: the eight pins it lists, each with every requirement, mutant and twin it gives;
- in §The code, the paragraph that begins **The pin `replay_drift` is re-aimed**, and the paragraphs **Tests and size** and **Existing pins and their mutants**;
- and the paragraphs of §The code, §The window, §The subject and §The late-report rule that a pin tests.

Read them whole before writing code. Write what they say and nothing they do not. Where the brief writes `<N3>`, the number is 9100.

**What to write.** Commit each part as you finish it and publish it at once. For each commit, in this order:
- `git diff --cached --no-renames --name-only` must name nothing outside `pins/`.
- Write the commit's message, without a trailer, into `.pins/text`. Then run `I=${ISSUE:-{BRANCH}}; { cat .pins/text; printf '\n\nProposer: reviewer {MODEL} runner-issue-%s\n' $I; } > .pins/msg && git commit -q -F .pins/msg`.
- Run step 7's two commands. If your new commit fails either, do not push it: stop and report.
- Run `git push -q origin HEAD:opening-c2a-3`.

1. **The eight pins,** named as §Pins names them, registered in `pins/pins.py` in the form `Pin("<name>"`, which `judge/status.py` looks for (its tuple `THIRD_WINDOW_PINS`). Put their test functions and fixtures in a file of your own under `pins/`, as `pins/c2a_prime.py` holds C2a-prime's. Raise `EXPECTED` in `pins/pins.py` by eight.
   - Each mutant is the edit §Pins describes. Its `find` string must occur exactly once in `judge/status.py` as it stands.
   - A mutant must be killed by the behaviour its pin names, not by an error elsewhere.
   - Where §Pins gives a twin, the twin passes on the evaluator as it stands.
   - A pin may run the builder's tests in `tests/test_status_third.py`, as `pins/c2a_prime.py` runs C2a-prime's. Where a requirement or twin of §Pins is not tested there, write the fixture in your own file.
   - If a twin cannot pass on the evaluator as it stands, do not change the evaluator. Write the pin, report the twin with the sentence of §Pins it tests, and go on.
2. **The pin `replay_drift`, re-aimed,** in `pins/replay.py` and its registration in `pins/pins.py`, as the brief's paragraph orders:
   - it keeps its three rows of the first table, `spec/vectors/promotion-replay.json`, and that table's SHA-256 check, as it has them;
   - it adds rows 400 and 735 of the second table, `spec/vectors/promotion-replay-c2a-3.json`, and checks that table's SHA-256, `943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77`, as it checks the first's. A row of the second table is run as the first table's rows are run, and its output is compared with its `stdout`, or, at row 735, which is marked, with its `marked`;
   - it holds `judge/status.py` to the SHA-256 `44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0`, the evaluator as the builder left it. The code read states the SHA-256 of the evaluator it accepts, and the opening checks that the two agree;
   - it holds `judge/value.py` to the moved bytes, as it does now;
   - its three mutants stay, and each must be killed: `unmarked_output_changed`, `marked_walk_regressed` and `other_source_bytes`.

**What you do not do.** Change no file outside `pins/`. So not `judge/`, `tests/`, `tools/`, `kernel/`, `spec/vectors/`, `.github/`, `SPEC.md`, `CHARTER.md`, `RUNBOOK.md` or `LAW.md`. Run no whole replay of the table and write no review: those are another session's.

**Checks,** when the pins are published. Run each and copy its result into your report. Checks (a) and (b) copy this worktree for each of their tasks, so while either runs `.pins/` must hold nothing but small files. Run them one at a time, each as one command, with the bash tool's `timeout` set to `1800000` on that call, which is thirty minutes. If a command is ended at its limit, say so in your report and do not run it again. When a check finds a fault in your pins, mend it, commit and publish as above, and run that check again.
- (a) `python3 -m unittest discover -s tests -t .`. Every test must pass.
- (b) `python3 pins/run.py`. Every pin must be KILLED, none SURVIVED, STALE, TWIN FAILED or PENDING. Name any that is not, with its line of detail.
- (c) The counted lines, at *B* and at your head: count them as `counted_lines` in `judge/judge.py` does, over the `counted` list of `judge/scope.json`. Give both numbers. At your head they must be at most 9100. Write each pin as short as it can be and still test what §Pins says.
- (d) The two tests of step 7, at your head.

**Time.** Start neither check (a) nor check (b) after minute 115. By minute 150, commit and publish whatever is uncommitted, even if unfinished, and say what is left in that commit's message. After that, start nothing but your report.

**Report.** Give:
- your head, and *B*;
- `git diff --stat 7d7f89471a52c248ad9c3214645f7e936235ab4f HEAD`, and the output of step 7's two commands;
- the results of checks (a) to (d);
- each of the eight pins with the mutants and twins you wrote, and any requirement, mutant or twin of §Pins you did not write, quoted, with the reason;
- the rows `replay_drift` now runs, and the time its twin took;
- any finding against the evaluator: a twin that does not pass, with the sentence of the brief it tests.

End with one line: `PUSHED <head>`, `PUSHED <head>: unfinished, <what is left>` or `STOPPED: <reason>`.
