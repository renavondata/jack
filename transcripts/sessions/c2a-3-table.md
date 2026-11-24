model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: compute the second promotion replay table, `spec/vectors/promotion-replay-c2a-3.json` (BRIEF-C2a-3, §The code)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included. Your scratch directory is `.replay/` at the top of the worktree. Never `git add` that directory: add the paths you commit by name. Do not set `TMPDIR`, `TEMP` or `TMP`, in your shell or for any command you run. Your paths are `spec/vectors/`, `transcripts/` and `log.jsonl`. Edit no existing file, and never edit `log.jsonl` by hand. You run one verb, `tools/jack proposal`, at the end. You run it a second time only after the merge that step 5 names.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here, and write your driver's strings in single quotes. Run `python3 -m py_compile` on each Python file you write before you run it.

**One session, start to finish.** This session computes the whole table and proposes it, or it stops and reports. Nothing carries over to another session, and nothing is restarted within this one: the driver is started once. If it stops, counsel reads the report and may file a fresh session on a new branch, which begins again from nothing.

**What you compute.** Two texts on `main` define the table. Read both before you write anything.
- `transcripts/BRIEF-C2a-3-draft.md`, §The code, the paragraphs that begin **The table** and **The marks**.
- `SPEC.md` §10, the paragraph headed **The promotion evaluator**, from "A run at a commit *c* is" to "whatever it holds." That is what the brief means by a row's run.

Build exactly the rows and the marks they define, and nothing else. Write your own driver. The adviser computes the same table separately, with a driver of its own, and that is the check on yours.

**Fixed for this session**, where the two texts leave a choice open:
- *T* is `origin/main` at step 1: run `git fetch -q origin main` and then `git rev-parse origin/main > .replay/T`, written once. Then check all three:
  - `git show $T:judge/status.py | sha256sum` gives `0ac73f8ed1ba96e62081c146aed2a7543f41464eb91bc2af9f3820cafe5acce6`;
  - `git show $T:judge/value.py | sha256sum` gives `1ea89facaff6aa27e7bd959dfdf24202a2f8afe39ecb078a0b4bf8e42c481845`;
  - `git rev-list --first-parent $T | grep -c ^bbfd0edf71df6dfe2183bfbbf24a372dd871146e` prints 1.

  If any check fails, stop and report. The evaluator changes only by the sovereign's push, and none is due before this table.
- **The rows** are `git rev-list --first-parent --reverse $T`: every commit, in that order.
- **Checkouts** are made with `git -c core.autocrlf=false -c core.eol=lf`, so that no file is converted on checkout.
- **The evaluator** runs from a detached checkout of *T* at `.replay/frozen`, as `python3 -I .replay/frozen/judge/status.py` with the row's arguments. Its imports therefore come from that checkout.
- **Worker *k*** has its own detached checkout `.replay/w<k>`. It moves it to each of its rows' commit with `git -c core.autocrlf=false -c core.eol=lf -C .replay/w<k> checkout -q --detach <c>`. That checkout is the row's `--root`, and its `log.jsonl` the row's `--log`; where the commit holds none, `--log` is an empty file. Each row's evidence files go under `.replay/ev/`.
  - `--run` is a file holding `json.dumps(run)` of the object SPEC's paragraph names, with members in its order.
  - `--runs` is a file holding `[]` and a newline.
  - `--acts` is a file holding `repo,time_hkt,class,kind,ref,note` and a newline.
- **A commit's committer time** is `TZ=UTC git log -1 --format=%cd --date=format-local:%Y-%m-%dT%H:%M:%SZ <c>`.
- **A run's outputs.** Its exit status is the process's return code. Stderr is discarded. Its stdout lines are stdout as bytes, decoded as UTF-8 and split on the newline character, with the last element dropped if it is the empty string. So empty stdout gives no lines.
- **The environment** of each evaluator run is the session's own, with every variable whose name begins with `GIT_` removed.

**The marked rows.** The brief's paragraph **The marks** is the rule; this is how the session applies it.
- **Which rows.** A row is marked when its `log.jsonl` holds an entry after seq 7180, that is, when the file has more than 7,181 lines. Seq 7180 is the sovereign's veto. Check at *T* that line 7180 of `log.jsonl`, counting from 0, has `type` `decision`, `proposer` `guy`, `body.kind` `veto` and `ts` `2026-11-22T11:44:05Z`. If it has not, stop and report.
- **The second run.** For each marked row, run the evaluator a second time with the row's arguments, except that `--as-of` is `2026-11-22T11:44:05Z`. Call the lines of the row's own run R and the lines of the second run V.
- **Three things must hold at every marked row.** If one fails at any row, stop the driver, commit nothing, and report the row's commit, which of the three failed, and R and V in full. The brief sends that question to the sovereign before anything is built.
  1. R and V each hold exactly one line that begins `window C2a:`, and the lines before it are the same in R and in V.
  2. The lines that begin `sovereign REPAIR` are the same in R and in V, in the same order.
  3. After its `window C2a:` line, each of R and V holds exactly one line that begins `J7:`. Every line after the `window C2a:` line that begins `overdue forecast` stands in one unbroken run directly after that `J7:` line. Either may hold no such line.
- **The row's `marked` member** is V, with the lines of V that begin `overdue forecast` after its `window C2a:` line taken out, and the lines of R that begin `overdue forecast` after R's `window C2a:` line put in their place, in R's order, directly after V's `J7:` line.
- **The row's `exit`** is the exit status of the row's own run. If the second run's exit status differs from it at any row, name those rows in your report. That is no stop.
- **Two checks on the set.** The first marked row must be `bbfd0edf71df6dfe2183bfbbf24a372dd871146e`, and every row after it must be marked. If not, stop and report.

**The table's form.** Write `spec/vectors/promotion-replay-c2a-3.json` as `json.dumps(table, indent=1, ensure_ascii=False)` followed by one newline, with keys in this order:
- `spec`: the SHA-256 of `SPEC.md` at *T*, from `git show $T:SPEC.md | sha256sum`;
- `T`: *T*, 40 hex digits;
- `frozen`: an object with the two members `judge/status.py` and `judge/value.py`, in that order, each the SHA-256 checked above;
- `python`: what `python3 --version` prints; `git`: what `git --version` prints;
- `rows`: the rows, in first-parent order, oldest first. Each row is an object with these members, in this order:
  - `commit`, 40 hex digits; `log`, true or false, whether the commit holds `log.jsonl`;
  - `argv`, the list `--subject`, `C2a`, `--as-of`, the row's as-of, `--log`, `<log>`, `--root`, `<root>`, `--run`, `<run>`, `--runs`, `<runs>`, `--acts`, `<acts>`. The five paths are written as those literal placeholders in angle brackets. Everything else is the value used;
  - `run`, the run object, members in SPEC's order;
  - `exit`, an integer; `stdout`, the list of the row's own lines;
  - and, on a marked row only, `marked`, the list of lines defined above.

`spec/vectors/promotion-replay.json` on `main` is the first table. Yours has its form, with `frozen` naming the evaluator's two files where they now are, and with `marked` added.

**Time.** `main`'s first-parent chain had 766 commits on 24 November, of which the last 31 were marked. What is measured:
- Runner #1147 measured the first table on this machine (twelve cores), with the evaluator as it then was: the 100th row took 0.3 s, the 350th 26 s, and the last, about the 700th, 95 s. The whole of it was about seven core-hours.
- On counsel's machine, which is slower, the row at `main`'s head took 258 s on 24 November with today's evaluator.

So expect ten to fifteen core-hours, the second runs of the marked rows included. That is counsel's estimate and no measurement.
- Run **ten** workers.
- Give the latest rows to the workers first, so that the long rows do not all fall at the end.
- A single command here stops at fifteen minutes, and the job at 180. So start the driver detached, once: `nohup setsid python3 .replay/driver.py > .replay/driver.log 2>&1 &`. The driver writes its process id to `.replay/driver.pid` first. Being started with `setsid`, it leads its own process group. Start no worker or evaluator with a new session or group, so that all of them stay in it.
- **Rows written whole.** The driver writes each finished row to `.replay/rows/<index>.json.tmp`, then renames it to `.replay/rows/<index>.json` with `os.replace`. Only renamed files are rows. A marked row is finished when both its runs are done and its three checks hold.
- Poll about every ten minutes with one command that prints the rows done, whether the driver's process is alive, and the time. Poll a running row only through `.replay/rows/` and `.replay/driver.log`.
- If a poll finds the driver dead with rows left, stop: kill its group (below), commit nothing, and report the end of `.replay/driver.log`. Do not start it again.
- **To stop the driver**, kill its whole group: `kill -TERM -- -$(cat .replay/driver.pid)`, then, after ten seconds, `kill -KILL -- -$(cat .replay/driver.pid) 2>/dev/null; true`. Do this whenever the session stops with the driver running, so that no worker outlives the session.

If at minute 120 of this session rows remain, stop the driver as above, commit nothing, and report how many rows are done and the time the last finished rows took. The checks of step 4 and the verb need the hour that is left. Never commit, or propose, a partial table.

**Steps.**
1. If `.replay/` already exists, stop and report: this session begins from nothing. Otherwise make `.replay/`, fix *T* and make the checks above. Create `.replay/frozen`, the worker checkouts and the driver.
2. Run the driver to the last row.
3. Assemble the table from `.replay/rows/`.
4. **Check before proposing,** and print each result:
   - (a) the table's `commit` values, in order, equal `git rev-list --first-parent --reverse $T` exactly: no row missing, repeated or out of order;
   - (b) three rows you pick at random after the 165th, recomputed one at a time outside the driver, equal their stored rows exactly; and one marked row you pick at random, with both its runs recomputed, equals its stored row exactly, `marked` included;
   - (c) the first four rows have `log` false, `exit` 1 and no line of `stdout`, and the fifth has `log` true;
   - (d) print how many rows are marked. No row before `bbfd0edf` has `marked`, and every row from it to *T* has. At the last row, print the line of `stdout` and the line of `marked` that begin `window C2a:`. The line of `marked` must end `(as of 2026-11-22T11:44:05Z; prefix to seq 7180)`;
   - (e) at every marked row, `stdout` and `marked` are equal in every line before the one that begins `window C2a:`;
   - (f) `python3 -m json.tool spec/vectors/promotion-replay-c2a-3.json > /dev/null && echo valid`, then `sha256sum spec/vectors/promotion-replay-c2a-3.json`.

   If any check fails, stop and report which. Do not propose, and do not draw (b)'s rows again.
5. **Record and propose.**
   - Copy your driver to `transcripts/evidence/promotion-replay-c2a-3-driver.py`, as the record of how the table was made.
   - `git add` exactly `spec/vectors/promotion-replay-c2a-3.json` and that file.
   - Commit with a message whose last paragraph is RUNBOOK's trailer for a commit made by hand: `printf 'vectors: second promotion replay table to %s\n\nProposer: reviewer {MODEL} runner-issue-%s\n' $(cut -c1-8 .replay/T) $ISSUE > .replay/msg && git commit -q -F .replay/msg`. If `$ISSUE` is empty, put the branch name in its place.
   - Remove the checkouts and `.replay/`: `git worktree remove --force` for each, then `rm -rf .replay`, then `git worktree prune`. `git status --porcelain` must print nothing: the verb refuses a tree that is not clean, and its check copies the whole tree.
   - **Bring the branch up to `main` first.** `main` moves every hour, so it has moved while you worked. Run `git fetch -q origin main`. If `git merge-base --is-ancestor origin/main HEAD` fails, run `git merge origin/main -m 'Merge main into {BRANCH}' -m 'Proposer: reviewer {MODEL} runner-issue-<the value of $ISSUE>'`. If the merge conflicts, run `git merge --abort`, push the branch, and report. The table and its *T* stay as they are: *T* is `main` as it was when the session began.
   - Then run `python3 tools/jack proposal --title 'second promotion replay table (BRIEF-C2a-3, The code): every first-parent commit of main to <first 8 of T>'`, with the bash tool's `timeout` set to `2400000` on that call. The verb runs the test suite itself and can take thirty minutes.
   - If it refuses because the branch does not contain `origin/main`, make the merge above again and run the proposal again, once.
   - If the verb refuses at its own push, run the two commands it prints.

**Report.** Give:
- *T*, the row count, the count of marked rows and the table's SHA-256;
- the output of the checks in step 4;
- any marked row whose second run's exit status differed from the row's;
- the driver's wall time, the time the last row took, and the pull request number;
- or, if you stopped, why, and the rows done.

End with one line: `PROPOSED #<n>`, or `STOPPED: <reason>` (with the rows done, if it stopped at minute 120).
