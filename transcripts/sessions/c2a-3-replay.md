model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: the whole replay of C2a's third window: the changed evaluator against the second table, and against `main`'s first-parent chain after it (BRIEF-C2a-3, §The code)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included. Your scratch directory is `.replay/` at the top of the worktree. Never `git add` that directory: add the paths you commit by name. Do not set `TMPDIR`, `TEMP` or `TMP`, in your shell or for any command you run. Never edit `log.jsonl`.

**The push branch.** The window's code, its tests, its pins and the code read are on `opening-c2a-3`, a branch the sovereign has published. You run no `tools/jack` verb at all, and open no pull request. You change no file of the code, its tests, its pins or its review. You add or extend two files under `transcripts/evidence/`, in one commit, and publish it with `git push -q origin HEAD:opening-c2a-3`. You push nothing else, and never with force. If that push fails, stop and report git's message, and do not pull, merge or rebase.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here, and write your driver's strings in single quotes. Run `python3 -m py_compile` on each Python file you write before you run it.

**The clock.** Step 1 writes the session's start, in seconds, to `.replay/start`. Every minute named below is counted from it. The job stops at 180 minutes, and a single command at 15 unless this text gives it longer.

**What you check.** The brief's paragraph **No other line is marked**, in §The code, is the rule; read it whole, and the paragraphs **The table** and **The marks** before it. The changed evaluator must print, with the same exit status:
- at every row of `spec/vectors/promotion-replay-c2a-3.json`, the row's `marked` lines if it has them, and its `stdout` lines if not;
- at every commit of `main`'s first-parent chain after the table's *T*, what the evaluator on `main` prints there, under the same mark.

The record of what this check has found is `transcripts/evidence/promotion-replay-c2a-3-check.jsonl` on `opening-c2a-3`. An earlier session of this template may have begun it. Each line is one row that passed, and a row that does not pass is never written. You continue the record: you check what it does not yet hold, as much as the time allows.

**Where you start.**
1. If `.replay/` already exists, stop and report. Otherwise run `mkdir .replay && date -u +%s > .replay/start`.
2. Run `git fetch -q origin main opening-c2a-3`; if it fails, run it once more. Then `git status --porcelain --untracked-files=normal` must print `?? .replay/` and nothing else, and `git merge-base --is-ancestor HEAD origin/main` must succeed. If the fetch fails twice, or either test fails, stop and report.
3. Run `git reset -q --hard origin/opening-c2a-3`, then `git rev-parse HEAD > .replay/tree` and `git rev-parse origin/main > .replay/M`. Your shell keeps no variable from one command to the next, so begin every command that uses them with `R=$(cat .replay/tree); M=$(cat .replay/M);`.
4. `git merge-base --is-ancestor 7d7f89471a52c248ad9c3214645f7e936235ab4f HEAD` must succeed, and `git rev-list --merges origin/main..HEAD` must print nothing.
5. `sha256sum judge/status.py` must give `44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0`, and `sha256sum judge/value.py` must give `1ea89facaff6aa27e7bd959dfdf24202a2f8afe39ecb078a0b4bf8e42c481845`.
6. `transcripts/REVIEW-C2a-3-code.md` must exist on the branch, its first line must be `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`, and it must hold the line `Evaluator: judge/status.py sha256 44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0`. The code read comes before the replay.
7. `sha256sum spec/vectors/promotion-replay-c2a-3.json` must give `943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77`. *T* is that file's member `T`, `96658263399ec7eeb815fc07210ce09b8e5ca3a4`. `git show origin/main:judge/status.py | sha256sum` must give `0ac73f8ed1ba96e62081c146aed2a7543f41464eb91bc2af9f3820cafe5acce6`, the evaluator at *T*: it is `main`'s evaluator until the opening push.
8. `M=$(cat .replay/M); git rev-list --first-parent 96658263399ec7eeb815fc07210ce09b8e5ca3a4..$M` names the chain's commits after *T*. `git merge-base --is-ancestor 96658263399ec7eeb815fc07210ce09b8e5ca3a4 $M` must succeed.

If any check fails, stop and report.

**What is left to check.** If `transcripts/evidence/promotion-replay-c2a-3-check.jsonl` exists, every line is a JSON object with the members `kind`, `index`, `commit`, `exit` and `lines`, in that order. `kind` is `table` or `chain`. A `table` line's `index` is the row's index in the table, counting from 0; a `chain` line's is the commit's place in `git rev-list --first-parent --reverse 96658263399ec7eeb815fc07210ce09b8e5ca3a4..<M>`, counting from 0. `lines` is the SHA-256 of the lines that passed, joined by newlines with a newline after each. What is left is every table row and every chain commit after *T* up to *M* whose commit the record does not hold with that kind. If the record holds a line whose commit is not where its `kind` and `index` put it, stop and report.

**The runs.** For both kinds:
- **Checkouts** are made with `git -c core.autocrlf=false -c core.eol=lf`, so that no file is converted on checkout, each a detached worktree of this repository: `.replay/new` at your tree, `.replay/old` at *T*, and one checkout `.replay/w<k>` for each worker *k*. Before you make them, `df -BG --output=avail . | tail -1` must show at least 12G; if less, stop and report.
- **The changed evaluator** runs as `python3 -I .replay/new/judge/status.py`, and **the evaluator on `main`** as `python3 -I .replay/old/judge/status.py`, each with a row's arguments, from the worker's checkout moved to the row's commit with `git -c core.autocrlf=false -c core.eol=lf -C .replay/w<k> checkout -q --detach <c>`. That checkout is the row's `--root`, and its `log.jsonl` the row's `--log`.
- **Evidence files** go under `.replay/ev/`: `--run` is a file holding `json.dumps` of the row's run object; `--runs` a file holding `[]` and a newline; `--acts` a file holding `repo,time_hkt,class,kind,ref,note` and a newline.
- **Outputs.** The exit status is the process's return code; stderr is discarded; the lines are stdout decoded as UTF-8 and split on the newline character, with the last element dropped if it is the empty string. The environment of each run is the session's own with every variable whose name begins with `GIT_` removed.

**A table row.** Its `argv` and `run` are the stored row's: the row's run is made from them as `SPEC.md` §10's paragraph **The promotion evaluator** defines a run, with the five placeholders in angle brackets replaced by the paths above. Run the changed evaluator once. The row passes when the exit status equals the row's `exit` and the lines equal the row's `marked` if it has that member, and its `stdout` if not.

**A chain commit.** It is made as the table's rows were made, by `transcripts/evidence/promotion-replay-c2a-3-driver.py` on `main`, which made the table: read its function `compute` whole, and the paragraph **The marked rows** of `transcripts/sessions/c2a-3-table.md`. From the commit, compute the row's as-of, its `run`, and its arguments as that driver does. Then:
- run the evaluator on `main` twice, as the driver's two runs: with the row's as-of, and with `--as-of` `2026-11-22T11:44:05Z`. Every chain commit has more than 7,181 lines in its `log.jsonl`, so every one is marked: if one has not, stop and report. Apply the driver's function `mark` to the two runs' lines. If it raises, stop and report the commit and the error;
- run the changed evaluator once, with the row's as-of;
- the commit passes when the changed evaluator's exit status equals that of the first run of the evaluator on `main`, and its lines equal the lines `mark` returned.

**The driver.** Write your own, `.replay/driver.py`. You may copy from the table's driver on `main`, and keep its form: ten workers; a queue; each finished row written to `.replay/rows/<name>.json.tmp` and renamed to `.replay/rows/<name>.json` with `os.replace`; a watchdog that ends its workers and their runs at minute 110 and writes how many rows are done to `.replay/driver.log`; a first line that writes its process id to `.replay/driver.pid`.
- **Order of work.** Give the chain commits to the workers first, the newest first, then the table rows, the highest index first.
- **A row that does not pass stops the driver at once.** It writes the row, the expected lines and the changed evaluator's lines to `.replay/fail.json`, and ends its workers.
- Start it detached, once: `nohup setsid python3 .replay/driver.py > .replay/driver.log 2>&1 &`. Start no worker or evaluator with a new session or group.
- Poll about every ten minutes with one command that prints the rows done, whether the driver is alive, and the minute. If a poll finds the driver gone, read `.replay/driver.log`.
- **To stop the driver,** kill its whole group: `kill -TERM -- -$(cat .replay/driver.pid)`, then, after ten seconds, `kill -KILL -- -$(cat .replay/driver.pid) 2> .replay/kill.err; true`. Do this whenever the session stops with the driver running.

**Time.** What is measured on this machine: the table's session (runner #1297) ran its 773 rows with ten workers in 4,786 s, two runs at each of its 38 marked rows. A late row took about 430 s with ten running at once. So the table's rows take about an hour, and each chain commit three late runs. `main`'s chain grows by about twenty commits a day. A session may not finish the chain, and the next session of this template continues it.

**If a row did not pass.** Commit nothing. Stop the driver if it runs, and report the row: its kind, index and commit, the expected lines and exit, and the changed evaluator's lines and exit, from `.replay/fail.json`. End with `FAILED: <kind> <index> <commit>`.

**Otherwise, the record.**
1. Append to `transcripts/evidence/promotion-replay-c2a-3-check.jsonl`, creating it if it does not exist, one line for each row in `.replay/rows/` that passed, as `json.dumps` of the object with the five members above, in that order, followed by a newline. Write the table's lines by index, then the chain's by index. Change no line already there.
2. Copy your driver to `transcripts/evidence/promotion-replay-c2a-3-check-driver.py`, replacing any earlier copy.
3. **Check before you commit,** and print each result: every line of the record parses, and no `kind` and commit appear twice; the record's `table` lines name every index from 0 to 772, or say how many it does not yet; its `chain` lines name the commits of `git rev-list --first-parent --reverse 96658263399ec7eeb815fc07210ce09b8e5ca3a4..<M>` in order from the first, with none missing between two that are there.
4. `git status --porcelain --untracked-files=normal` must name nothing but `.replay/` and the two files. Write the commit's message, without a trailer, into `.replay/text`, saying how many rows of each kind are now in the record and up to which commit of the chain. Then run `git add transcripts/evidence/promotion-replay-c2a-3-check.jsonl transcripts/evidence/promotion-replay-c2a-3-check-driver.py && I=${ISSUE:-{BRANCH}}; { cat .replay/text; printf '\n\nProposer: reviewer {MODEL} runner-issue-%s\n' $I; } > .replay/msg && git commit -q -F .replay/msg`.
5. `git log -1 --format='%(trailers:key=Proposer,valueonly)'` must print `reviewer`, then at least one field more, with no `<`, and `git log -1 --name-only --format=` must name the two files and nothing else. If not, do not push: stop and report.
6. Run `git push -q origin HEAD:opening-c2a-3`.
7. Remove the checkouts: `git worktree remove --force` for each, then `git worktree prune`.

**Report.** Give:
- the tree you read, *M*, and how many rows of each kind the record held when you began;
- how many rows of each kind you checked, the driver's wall time, and the time its last rows took;
- the results of the checks before the commit, and the head after your push;
- what is left: table rows not yet in the record, and chain commits after the last one it holds, up to *M*.

End with one line: `PUSHED <head>: complete to <M>`, when the record holds every table row and every chain commit up to *M*; `PUSHED <head>: unfinished, <what is left>`; `FAILED: <kind> <index> <commit>`; or `STOPPED: <reason>`.
