model: {MODEL}
key: ~/.ssh/jack-builder
branch: {BRANCH}

# builder: build the code of C2a's third window, six changes to the promotion evaluator `judge/status.py` and their tests (BRIEF-C2a-3, §The code)

You are the **builder** (`JACK_KEY=~/.ssh/jack-builder`, party `builder`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included. Your scratch directory is `.build/` at the top of the worktree. Never `git add` that directory: add the paths you commit by name. Do not set `TMPDIR`, `TEMP` or `TMP`, in your shell or for any command you run. Never edit `log.jsonl`.

**The push branch.** The window's code is built on `opening-c2a-3`, a branch the sovereign has published. He applies it to `main` with `jack push` when the window opens, because it changes the trusted base. So you run no `tools/jack` verb at all, and open no pull request. Your own branch, `{BRANCH}`, is only where this session works: step 3 sets it to the published branch, you commit on it, and you publish each commit with `git push -q origin HEAD:opening-c2a-3`. You push nothing else, and never with force. If that push is refused, another hand has moved the published branch: stop and report.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here. Run `python3 -m py_compile` on each Python file you change.

**The clock.** Step 1 writes the session's start, in seconds, to `.build/start`. Every minute named below is counted from it. The job stops at 180 minutes, and a single command at 15.

**Where you start.** The first commit of `opening-c2a-3` over `main` is the sovereign's cherry-pick of counsel's patch, whose subject begins `push: C2a-3 opening`. Call that commit *P*. Commits after *P*, if there are any, are an earlier session's work to this same text: you continue it, and your report says so.
1. If `.build/` already exists, stop and report: a session of this template begins from nothing, on a branch of its own. Otherwise run `mkdir .build && date -u +%s > .build/start`.
2. Run `git fetch -q origin main opening-c2a-3`. Then `git status --porcelain` must print `?? .build/` and nothing else, and `git merge-base --is-ancestor HEAD origin/main` must succeed: the runner cut this branch from `main` a moment ago. If either fails, stop and report.
3. Run `git reset -q --hard origin/opening-c2a-3`.
4. `git log --reverse --format=%s origin/main..HEAD | head -1` must begin `push: C2a-3 opening`. *P* is `git rev-list --reverse origin/main..HEAD | head -1`.
5. `sha256sum SPEC.md` must give `c4a5b44b8465f4be9cd4a5bbeb294cfd5c56a7397319e7f1c167853d7fd628a7`, and `grep -c 9100 judge/scope.json` must print 1.
6. **His read.** Find a `decision` entry on `main`'s log whose `proposer` is `guy`, whose kind is `grant`, and whose subject begins with the line below and also holds the words `the cap at C2a-3's opening is 9,100`. Compose the search yourself, for example with `python3` reading `git show origin/main:log.jsonl` line by line, and print the entry's `seq` and `ts`. If there is none, stop: no code is written to a text he has not read. The subject begins:

   `promote_unmet: SPEC.md c4a5b44b8465f4be9cd4a5bbeb294cfd5c56a7397319e7f1c167853d7fd628a7; table spec/vectors/promotion-replay-c2a-3.json 943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77. A2.10 for BRIEF-C2a-3: before entering this I read transcripts/BRIEF-C2a-3-draft.md at sha256 a5c331b40d1e81f959e147461884b3a55e11d829933bfd2296d660a526433945 and approved it unchanged.`
7. `sha256sum transcripts/BRIEF-C2a-3-draft.md` must give `a5c331b40d1e81f959e147461884b3a55e11d829933bfd2296d660a526433945`, and `sha256sum spec/vectors/promotion-replay-c2a-3.json` must give `943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77`.
8. **Every commit after *P*** is held to two tests: an earlier session's now, and your own before your last push. With no commit after *P* both commands print nothing. If an earlier session's commit fails either, stop and report.
   - `git log -m --no-renames --name-only --format= $(git rev-list --reverse origin/main..HEAD | head -1)..HEAD | grep . | sort -u` names every path that any of those commits touched. It must name nothing but `judge/status.py` and files under `tests/`.
   - `git log --format='%h %(trailers:key=Proposer,valueonly)' $(git rev-list --reverse origin/main..HEAD | head -1)..HEAD | grep .` prints a line for each of those commits: its hash, then the fields of its trailer. The first field after the hash must be `builder`. A hash alone is a commit without its trailer.

If any check fails, stop and report. Never change `SPEC.md` or `judge/scope.json`: his grant names `SPEC.md` by that hash, and the cap is his.

**The text you build to** is `transcripts/BRIEF-C2a-3-draft.md` on this branch:
- §The code, from the paragraph that begins **Change 1, the window.** to the section's end;
- the sections those paragraphs name: §The window, §The subject, §The late-report rule and §Pre-stated criteria for C2a-3;
- from §Pins, the names of the pins it adds, and no more.

Read them whole before writing code. The sovereign read that text before this build (CHARTER A2.10; his grant, step 6). Build what it says and nothing it does not. Where the brief writes `<N3>`, the number is 9100. Where the text and the code today disagree, the text governs. Where the text is silent, keep today's behaviour.

**What to build.** Commit each part as you finish it, and publish each commit at once with `git push -q origin HEAD:opening-c2a-3`, so that nothing is lost if the session ends. Before each commit, `git diff --cached --no-renames --name-only` must name nothing but `judge/status.py` and files under `tests/`. Hand commits end with the paragraph `Proposer: builder {MODEL} runner-issue-<the value of $ISSUE>` (RUNBOOK, Common to every verb; use the branch name if `$ISSUE` is empty).

1. **The six changes,** in `judge/status.py` and in no other file.
   - Leave every line that no change needs byte for byte. Among them: the line of `c2a_tree_evidence` that walks first parents for criterion 3 (line 433 on `main`), which a mutant of the pin `replay_drift` finds; and the two lines that read `tools/status.py` from a tree, which C2a's first window and C2a-prime go on using.
   - Many pins' mutants are a string of `judge/status.py` and its replacement (`pins/pins.py` and `pins/replay.py`). Leave each such string byte for byte where a change allows it. List in your report each one a change had to alter, with the old string and the new.
   - The new pins' names stand in a tuple of their own, which criterion 1 reads when it reads C2a-3 and at no other time. Leave `VALUE_PINS` as it is.
   - `judge/evaluate.py` calls the evaluator's `main`, `inputs`, `assess` and `promotion_line`. Keep those four as it calls them.
2. **Your tests,** under `tests/`: at least one for each of the six changes; for change 3, the test the brief describes, on the real `log.jsonl`.

**What you do not do.** Change no file but `judge/status.py` and files under `tests/`. So not `judge/value.py`, `judge/evaluate.py`, `judge/judge.py`, `kernel/`, `tools/`, `pins/`, `spec/vectors/`, `.github/`, `CHARTER.md`, `RUNBOOK.md` or `LAW.md`. The pins are the reviewer's (A2.9): you write none and register none. Build nothing for C2b or C2c-1.

**Checks before your last push.** Run each and copy its result into your report. Checks (a) and (b) copy this worktree for each of their tasks, so while either runs `.build/` must hold nothing but small files, and no `.build/w`. Run them one at a time, each as one command. If a command is ended at its 15 minutes, say so in your report and do not run it again.
- (a) `python3 -m unittest discover -s tests -t .`. A failure is allowed only in a test of `pins/` itself, and only because a pin holds the evaluator to bytes or to a string that a change had to alter. List each such failure. Fix any other. Do not weaken a test to make it pass.
- (b) `python3 pins/run.py`. A pin may fail only because the evaluator's bytes changed, or because a string that one of its mutants names had to change. List each such pin with its line of detail. If a pin fails for any other reason, the fault is in your code: fix it. The pin `replay_drift` holds `judge/status.py` to its bytes on `main`, so it fails by design until the reviewer re-aims it, and its detail must be the one that ends `moved bytes differ`. If its detail is anything else, your change has altered what an old row prints: fix that.
- (c) The counted lines, at `origin/main` and at your head: count them as `counted_lines` in `judge/judge.py` does, over the `counted` list of `judge/scope.json`. Give both numbers. Counted lines are scarce: your tests and the reviewer's pins must fit together under the cap, so write each test as short as it can be and still test its change.
- (d) The two tests of step 8, at your head.
- (e) **Four rows of the replay table,** `spec/vectors/promotion-replay-c2a-3.json`, run as `SPEC.md` §10's paragraph **The promotion evaluator** defines a run, from "A run at a commit *c* is" to "whatever it holds." The rows are those at index 4, 734, 735 and 772, counting from 0.
  - Run the evaluator of this worktree, `python3 -I judge/status.py`, with the row's `argv`, one row to a command.
  - `<root>` is a checkout of the row's `commit`, made with `git -c core.autocrlf=false -c core.eol=lf worktree add -q --detach .build/w <commit>`, where `<commit>` stands for the row's own, and moved to the next row's commit with `git -c core.autocrlf=false -c core.eol=lf -C .build/w checkout -q --detach <commit>`. `<log>` is that checkout's `log.jsonl`.
  - `<run>` is a file holding `json.dumps` of the row's `run`; `<runs>` a file holding `[]` and a newline; `<acts>` a file holding `repo,time_hkt,class,kind,ref,note` and a newline.
  - The run's environment is your own with every variable whose name begins with `GIT_` removed. Its lines are stdout decoded as UTF-8 and split on the newline character, with the last element dropped if it is the empty string.
  - At rows 4 and 734 the exit status and the lines must equal the row's `exit` and `stdout`. At rows 735 and 772 the exit status must equal the row's `exit`, and the lines must equal the row's `marked`. If a row differs, the fault is in your code: fix it.
  - Remove the checkout when you are done: `git worktree remove --force .build/w`, then `git worktree prune`.

  This is a spot check. The acceptance is the reviewer's replay of every row.

**Time.** By minute 150, commit what you have and publish it, even if unfinished, and say so. After that, start nothing but your report.

**Report.** Give:
- your head, and *P*;
- `git diff --stat $(git rev-list --reverse origin/main..HEAD | head -1) HEAD`, and the output of step 8's two commands;
- the results of checks (a) to (e);
- the pins that do not pass, and why;
- each mutant's string a change had to alter, old and new;
- anything in the text you could not build as it stands, quoted, with the reason.

End with one line: `PUSHED <head>`, `PUSHED <head>: unfinished, <what is left>` or `STOPPED: <reason>`.
