model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: compute the second promotion replay table, `spec/vectors/promotion-replay-c2a-3.json` (BRIEF-C2a-3, §The code)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included. Your scratch directory is `.replay/` at the top of the worktree. Never `git add` that directory: add the paths you commit by name. Do not set `TMPDIR`, `TEMP` or `TMP`, in your shell or for any command you run. In this session you add two new files, one under `spec/vectors/` and one under `transcripts/evidence/`, and you change nothing else. Never edit `log.jsonl` by hand. You run one verb, `tools/jack proposal`, as step 5 says.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here, and write your driver's strings in single quotes. Run `python3 -m py_compile` on each Python file you write before you run it.

**One session, start to finish.** This session computes the whole table and proposes it, or it stops and reports. Nothing carries over to another session, and nothing is restarted within this one: the driver is started once. If it stops, counsel reads the report and may file a fresh session on a new branch, which begins again from nothing.

**The clock.** The first command of step 1 writes the session's start, in seconds, to `.replay/start`. Every minute named below is counted from it. The job stops at 180 minutes, and it began a little before your first command.

**What you compute.** Two texts on `main` define the table. Read both before you write anything.
- `transcripts/BRIEF-C2a-3-draft.md`, §The code, the paragraphs that begin **The table** and **The marks**.
- `SPEC.md` §10, the paragraph headed **The promotion evaluator**, from "A run at a commit *c* is" to "whatever it holds." That is what the brief means by a row's run.

Build exactly the rows and the marks they define, and nothing else. Write your own driver. The adviser computes the same table separately, with a driver of its own, and that is the check on yours.

**Fixed for this session**, where the two texts leave a choice open:
- *T* is `origin/main` at step 1: run `git fetch -q origin main` and then `git rev-parse origin/main > .replay/T`, written once. Your shell may keep no variable from one command to the next, so begin every command that uses `$T` with `T=$(cat .replay/T);`. Then check all three:
  - `T=$(cat .replay/T); git show $T:judge/status.py | sha256sum` gives `0ac73f8ed1ba96e62081c146aed2a7543f41464eb91bc2af9f3820cafe5acce6`;
  - `T=$(cat .replay/T); git show $T:judge/value.py | sha256sum` gives `1ea89facaff6aa27e7bd959dfdf24202a2f8afe39ecb078a0b4bf8e42c481845`;
  - `T=$(cat .replay/T); git rev-list --first-parent $T | grep -c ^bbfd0edf71df6dfe2183bfbbf24a372dd871146e` prints 1.

  If any check fails, stop and report. The evaluator changes only by the sovereign's push, and none is due before this table.
- **The rows** are `git rev-list --first-parent --reverse $T`: every commit, in that order.
- **Checkouts** are made with `git -c core.autocrlf=false -c core.eol=lf`, so that no file is converted on checkout. Each is a detached worktree of this repository, made with `git -c core.autocrlf=false -c core.eol=lf worktree add -q --detach <path> $T`. A checkout of *T* holds about 800 MB, and there are eleven. Before you make them, `df -BG --output=avail . | tail -1` must show at least 12G. If it shows less, stop and report.
- **The evaluator** runs from the checkout at `.replay/frozen`, which stays at *T*, as `python3 -I .replay/frozen/judge/status.py` with the row's arguments. Its imports therefore come from that checkout.
- **Worker *k*** has its own checkout `.replay/w<k>`. It moves it to each of its rows' commit with `git -c core.autocrlf=false -c core.eol=lf -C .replay/w<k> checkout -q --detach <c>`. That checkout is the row's `--root`, and its `log.jsonl` the row's `--log`; where the commit holds none, `--log` is an empty file. Each row's evidence files go under `.replay/ev/`.
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
- **The row's `marked` member** is V, changed in one place. Take out the lines of V that begin `overdue forecast` and stand after V's `window C2a:` line. Where they stood, directly after the `J7:` line that follows V's `window C2a:` line, put the lines of R that begin `overdue forecast` and stand after R's `window C2a:` line, in R's order. The lines before the `window C2a:` line hold a `J7:` line of their own; leave them as they are.
- **The row's `exit`** is the exit status of the row's own run. If the second run's exit status differs from it at any row, name those rows in your report. That is no stop.
- **Two checks on the set.** The first marked row must be `bbfd0edf71df6dfe2183bfbbf24a372dd871146e`, and every row after it must be marked. If not, stop and report.

**The table's form.** Write `spec/vectors/promotion-replay-c2a-3.json` as the UTF-8 bytes of `json.dumps(table, indent=1, ensure_ascii=False)` followed by one newline, with keys in this order:
- `spec`: the SHA-256 of `SPEC.md` at *T*, the 64 hex digits that `T=$(cat .replay/T); git show $T:SPEC.md | sha256sum` prints;
- `T`: *T*, 40 hex digits;
- `frozen`: an object with the two members `judge/status.py` and `judge/value.py`, in that order, each the SHA-256 checked above;
- `python`: the line `python3 --version` prints, without its newline; `git`: the line `git --version` prints, without its newline;
- `rows`: the rows, in first-parent order, oldest first. Each row is an object with these members, in this order:
  - `commit`, 40 hex digits; `log`, true or false, whether the commit holds `log.jsonl`;
  - `argv`, the list `--subject`, `C2a`, `--as-of`, the row's as-of, `--log`, `<log>`, `--root`, `<root>`, `--run`, `<run>`, `--runs`, `<runs>`, `--acts`, `<acts>`. The five paths are written as those literal placeholders in angle brackets. Everything else is the value used;
  - `run`, the run object, members in SPEC's order;
  - `exit`, an integer; `stdout`, the list of the row's own lines;
  - and, on a marked row only, `marked`, the list of lines defined above.

`spec/vectors/promotion-replay.json` on `main` is the first table. Yours has its form, with `frozen` naming the evaluator's two files where they now are, and with `marked` added.

The adviser recomputes the table on its own machine and compares it row by row: `commit`, `argv`, `run`, `exit`, `stdout` and `marked`. It does not compare the file's bytes. `python` and `git` record this machine's versions, so that a row which differs only by interpreter can be told from an error.

**Time.** `main`'s first-parent chain had 766 commits on 24 November, of which the last 31 were marked. It grows by about twenty a day, and each new commit is a marked row with two runs. What is measured:
- The first table's session (runner #1153) ran its 706 rows on this machine with eight workers. Its driver took 4,129.8 s.
- A session on this machine (runner #1287) timed the evaluator at `main`'s head on 24 November: one run took 114 s; ten at once took 225 s each; twelve at once took 262 s each. So ten workers do the work of about five runs one after another, and twelve do little more.
- On counsel's machine, which is slower, the 101st row took 0.4 s, the 351st 23 s, the 706th 204 s and the 766th 258 s. Summed along the chain with the second runs, that is about sixteen hours of runs there, and about seven here by the ratio of 114 to 258.

So for 766 rows expect the driver to take about 85 minutes with ten workers, and about 15 more for each day since 24 November. That is counsel's estimate from those figures and no measurement of the whole.
- Run **ten** workers.
- Give the latest rows to the workers first, so that the long rows do not all fall at the end.
- A single command here stops at fifteen minutes. So start the driver detached, once: `nohup setsid python3 .replay/driver.py > .replay/driver.log 2>&1 &`. The driver writes its process id to `.replay/driver.pid` first. Being started with `setsid`, it leads its own process group. Start no worker or evaluator with a new session or group, so that all of them stay in it.
- **The driver ends itself.** It reads `.replay/start`. If rows remain at minute 115, it ends its workers and their evaluator runs, writes how many rows are done to `.replay/driver.log`, and exits. So no worker outlives a job that has stopped.
- **Rows written whole.** The driver writes each finished row to `.replay/rows/<index>.json.tmp`, then renames it to `.replay/rows/<index>.json` with `os.replace`. Only renamed files are rows. A marked row is finished when both its runs are done and its three checks hold.
- Poll about every ten minutes with one command that prints the rows done, whether the driver's process is alive, and the minute. Poll a running row only through `.replay/rows/` and `.replay/driver.log`.
- If a poll finds the driver gone with rows left, stop: kill its group (below), commit nothing, and report the end of `.replay/driver.log`, the rows done and the time the last finished rows took. Do not start it again. Never commit, or propose, a partial table.
- **To stop the driver**, kill its whole group: `kill -TERM -- -$(cat .replay/driver.pid)`, then, after ten seconds, `kill -KILL -- -$(cat .replay/driver.pid) 2> .replay/kill.err; true`. Do this whenever the session stops with the driver running.

**Steps.**
1. If `.replay/` already exists, stop and report: this session begins from nothing. Otherwise run `mkdir .replay && date -u +%s > .replay/start`, fix *T* and make the checks above. Create `.replay/frozen`, the worker checkouts and the driver.
2. Run the driver to the last row.
3. Assemble the table from `.replay/rows/`.
4. **Check before you commit,** and print each result:
   - (a) the table's `commit` values, in order, equal `git rev-list --first-parent --reverse $T` exactly: no row missing, repeated or out of order;
   - (b) three rows you pick at random after the 165th, and one marked row you pick at random, recomputed outside the driver, equal their stored rows exactly. A marked row is recomputed with both its runs, and its `marked` compared too; any of the three may be marked. Run the four rows' recomputations at the same time, each in a worker's checkout;
   - (c) the first four rows have `log` false, `exit` 1 and no line of `stdout`, and the fifth has `log` true;
   - (d) print how many rows are marked. No row before `bbfd0edf` has `marked`, and every row from it to *T* has. At the last row, print the line of `stdout` and the line of `marked` that begin `window C2a:`. The line of `marked` must end `(as of 2026-11-22T11:44:05Z; prefix to seq 7180)`;
   - (e) at every marked row, `stdout` and `marked` are equal in every line before the one that begins `window C2a:`;
   - (f) `python3 -m json.tool spec/vectors/promotion-replay-c2a-3.json > .replay/tool.out && echo valid`, then `sha256sum spec/vectors/promotion-replay-c2a-3.json`.

   If any check fails, stop and report which. Commit nothing, and do not draw (b)'s rows again.
5. **Record, push and propose.**
   - Note, for your report, the driver's wall time and the time the last row took, from `.replay/driver.log`.
   - Copy your driver to `transcripts/evidence/promotion-replay-c2a-3-driver.py`, as the record of how the table was made.
   - `git add` exactly `spec/vectors/promotion-replay-c2a-3.json` and that file.
   - Commit with a message whose last paragraph is RUNBOOK's trailer for a commit made by hand: `I=${ISSUE:-{BRANCH}}; printf 'vectors: second promotion replay table to %s\n\nProposer: reviewer {MODEL} runner-issue-%s\n' $(cut -c1-8 .replay/T) $I > .replay/msg && git commit -q -F .replay/msg`.
   - **Push the branch at once:** `git push -q origin {BRANCH}`. From here the table is kept whatever happens next.
   - **Bring the branch up to `main`.** `main` moves every hour, so it has moved while you worked. Run `git fetch -q origin main`. If `git merge-base --is-ancestor origin/main HEAD` fails, run `I=${ISSUE:-{BRANCH}}; printf 'Merge main into {BRANCH}\n\nProposer: reviewer {MODEL} runner-issue-%s\n' $I > .replay/mergemsg && git merge -q origin/main -F .replay/mergemsg`. If the merge conflicts, run `git merge --abort` and report, ending `PUSHED`. The table and its *T* stay as they are: *T* is `main` as it was when the session began.
   - Read the minute from `.replay/start` and keep the start for the two tests below. Then remove the checkouts and `.replay/`: `git worktree remove --force` for each, then `rm -rf .replay`, then `git worktree prune`. `git status --porcelain` must print nothing: the verb refuses a tree that is not clean, and its check copies the whole tree.
   - **Do not start the verb after minute 130.** It can take forty minutes. If it is later than that, report, ending `PUSHED`.
   - Otherwise run `python3 tools/jack proposal --title 'second promotion replay table (BRIEF-C2a-3, The code): every first-parent commit of main to <first 8 of T>'`, with the bash tool's `timeout` set to `2400000` on that call.
   - If it refuses because the branch does not contain `origin/main`, and minute 130 has not passed, fetch and merge again and run the proposal again, once. Give that merge the same two-paragraph message with two `-m` arguments in single quotes, with the issue's number written out in the second.
   - If the verb refuses at its own push, run the two commands it prints.
   - If the verb refuses for any other reason, its check's failure included, do not run it again. The branch is already pushed. Report the refusal's words, ending `PUSHED`.

**Report.** Give:
- *T*, the row count, the count of marked rows and the table's SHA-256;
- the output of the checks in step 4;
- any marked row whose second run's exit status differed from the row's;
- the driver's wall time, the time the last row took, and the pull request number;
- or, if you stopped, why, the rows done and the time the last finished rows took.

End with one line: `PROPOSED #<n>`; or `PUSHED <the branch's head>: <reason>`, when the table is committed and pushed and not proposed; or `STOPPED: <reason>`, when nothing is committed.
