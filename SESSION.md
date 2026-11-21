model: openai/gpt-6.1-sol
key: ~/.ssh/jack-reviewer
branch: review-promotion-replay

# reviewer: compute the promotion replay table, `spec/vectors/promotion-replay.json` (ruling of 20 November 2026, answer 9)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/review-promotion-replay` on branch `review-promotion-replay`. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Your paths are `spec/vectors/`, `transcripts/` and `log.jsonl`. Edit no existing file. You run one verb, `tools/jack proposal`, at the end. You run it a second time only after the merge that step 5 names.

**Quoting.** Code copied from a prompt on this runner has had its double quotes turned into a literal `\"`, in commands and in files alike (runners #1144 to #1146), and the code failed; code a session composes itself has not. So put no double quote in any shell command, and write your driver's strings in single quotes. Run `python3 -m py_compile` on each file you write before you run it. Every command below is written that way.

**Where this session stands.**
- If `.replay/STATE` exists, an earlier session on this branch began the work. Go on from the step it names; do not start again.
- If `.replay/` exists without `STATE`, an earlier session stopped inside step 1. Remove it: `git worktree remove --force` each checkout under it, then `rm -rf .replay` and `git worktree prune`. Then begin at step 1.
- Otherwise begin at step 1.

**What you compute.** The table is defined by one paragraph of a draft change to `SPEC.md`. It is the sovereign's to read; nothing in it is in force. Run `git fetch -q origin agent/spec-10-promotion` and read the paragraph headed "The promotion evaluator" in `git show 6fc0a5f9:SPEC.md`, from "The frozen table of those outputs" to "and exits with the same status." Build exactly the rows it defines, and nothing else from the draft: no marks, no moved evaluator, no tail. The ruling on `main` is `transcripts/RULING-20261120-promotion-judge.md` (answers 3, 7 and 9). Write your own driver for the runs from that paragraph; that the adviser computes the same table separately, from its own driver, is the check on yours.

**Fixed for this session**, where the paragraph leaves a choice open:
- *T* is `origin/main` at step 1: `git rev-parse origin/main > .replay/T`, written once and never again; a resumed session reads it. Then check all three:
  - `b88d318e` is on its first-parent chain (`git rev-list --first-parent $T | grep -c ^b88d318e` prints 1);
  - `git show $T:tools/status.py | sha256sum` gives `b255520996cef0ec20691c46cbc236ce5826dc166d16697762fa85f30fe86acb`;
  - `git show $T:tools/value.py | sha256sum` gives `11440c89429513b49922658d419b0bc6c8e625b15701b335576eedf537cf9992`.

  If any check fails, stop and report.
- **The rows** are `git rev-list --first-parent --reverse $T`: every commit, in that order.
- **The frozen evaluator** runs from a detached checkout of *T* at `.replay/frozen`, as `python3 -I .replay/frozen/tools/status.py …`. Its imports therefore come from that checkout.
- **Worker *k*** has its own detached checkout `.replay/w<k>`. It moves it to each of its rows' commit with `git -C .replay/w<k> checkout -q --detach <c>`. That checkout is the row's `--root`, and its `log.jsonl` the row's `--log`; where the commit holds none, `--log` is an empty file. Each row's evidence files go under `.replay/ev/`.
  - `--run` is a file holding `json.dumps(run)` of the object the paragraph names, with members in its order.
  - `--runs` is a file holding `[]` and a newline.
  - `--acts` is a file holding `repo,time_hkt,class,kind,ref,note` and a newline.
- **A commit's committer time** is `TZ=UTC git log -1 --format=%cd --date=format-local:%Y-%m-%dT%H:%M:%SZ <c>`.
- **A row's outputs.** Its exit status is the process's return code. Stderr is discarded. Its stdout lines are stdout as bytes, decoded as UTF-8 and split on `"\n"`, with the last element dropped if it is the empty string. So empty stdout gives no lines, `[]`.
- **The environment** of each evaluator run is the session's own, with every variable whose name begins with `GIT_` removed.

**The table's form.** Write `spec/vectors/promotion-replay.json` as `json.dumps(table, indent=1, ensure_ascii=False) + "\n"`, with keys in this order:
```
{"spec": "72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2",
 "T": "<T, 40 hex>",
 "frozen": {"tools/status.py": "b255520996cef0ec20691c46cbc236ce5826dc166d16697762fa85f30fe86acb",
            "tools/value.py": "11440c89429513b49922658d419b0bc6c8e625b15701b335576eedf537cf9992"},
 "python": "<python3 --version, as printed>",
 "git": "<git --version, as printed>",
 "rows": [{"commit": "<40 hex>", "log": true or false,
           "argv": ["--subject", "C2a", "--as-of", "<as-of>", "--log", "<log>", "--root", "<root>",
                    "--run", "<run>", "--runs", "<runs>", "--acts", "<acts>"],
           "run": {<the run object, members in the paragraph's order>},
           "exit": <int>, "stdout": ["<line>", ...]}, ...]}
```
- In `argv`, the five paths are written as the literal placeholders `<log>`, `<root>`, `<run>`, `<runs>` and `<acts>`. Everything else is the value used.
- Rows are in first-parent order, oldest first. `"log"` says whether the commit holds `log.jsonl`.
- The adviser recomputes the table on its own machine and compares it row by row: `argv`, `run`, `exit` and `stdout`. The versions are recorded so that a row which differs only by interpreter can be told from an error (its request R10).

**Time.** There are about 700 rows. Runner #1147 measured them on this machine (twelve cores):
- the 100th row took 0.3 s, the 350th 26 s, and the last 95 s;
- rows before the 165th, the commit that adds seq 367, end in under a second;
- twelve rows run at once (600 to 611) took 82 to 88 s each.

The whole table is therefore about seven core-hours.
- Run **eight** workers, not twelve: the diary's sessions share this machine.
- Give the latest rows to the workers first, so that the long rows do not all fall at the end.
- A single command here stops at fifteen minutes, and the job at 180. So start the driver detached: `nohup setsid python3 .replay/driver.py > .replay/driver.log 2>&1 &`.
- **One driver at a time.** The driver holds an exclusive, non-blocking `fcntl.flock` on `.replay/driver.lock` for as long as it runs, and exits at once if another holds it. Write a small `.replay/lockcheck.py` that tries the same lock and prints `held` or `free`. Run it before you start a driver and whenever you resume. If it prints `held`, a driver is running: poll it, and start none.
- **Rows written whole.** The driver writes each finished row to `.replay/rows/<index>.json.tmp`, then renames it to `.replay/rows/<index>.json` with `os.replace`. On start it deletes every `.tmp` file, and every row file that does not parse as JSON, and computes those rows again. It skips the other rows already there, so a restart resumes.
- Poll about every ten minutes with one command that prints the rows done and the time. Poll a running row only through `.replay/rows/` and `.replay/driver.log`.
- Keep `.replay/STATE` current: one line naming the next step.

If at minute 150 of this session rows remain, stop polling and leave `.replay/` in place. Write `step 2: resume the driver (check the lock first)` to `.replay/STATE`, and report how many rows are done. A later session on this branch resumes. Never commit, or propose, a partial table.

**Steps.**
1. Make `.replay/` and write `step 1` to `.replay/STATE` before anything else in it. Fix *T* (unless `.replay/T` exists) and make the checks above. Create `.replay/frozen`, the worker checkouts and the driver, each unless it exists. Then write `step 2` to `STATE`.
2. Run the driver to the last row.
3. Assemble the table from `.replay/rows/`.
4. **Check before proposing,** and print each result:
   - (a) the table's `commit` values, in order, equal `git rev-list --first-parent --reverse $T` exactly: no row missing, repeated or out of order;
   - (b) three rows you pick at random after the 165th, recomputed one at a time outside the driver, equal their stored rows exactly;
   - (c) the first four rows have `"log": false`, `"exit": 1` and `"stdout": []`;
   - (d) at `b88d318e` and at *T*, the **last** stdout line beginning `criterion 3: counted` ends in `False SHORT`, and the line beginning `promote C2a:` begins `promote C2a: refused: criterion 3: counted`; print both lines at both rows;
   - (e) `python3 -m json.tool spec/vectors/promotion-replay.json > /dev/null && echo valid`, then `sha256sum spec/vectors/promotion-replay.json`.

   If any check fails, write `step 4 failed: <which>` to `STATE` and stop. Do not propose.
5. **Record and propose.**
   - Copy your driver to `transcripts/evidence/promotion-replay-driver.py`, as the record of how the table was made.
   - `git add` exactly `spec/vectors/promotion-replay.json` and that file.
   - Commit with a message whose last paragraph is RUNBOOK's trailer for a commit made by hand: `printf 'vectors: promotion replay table to %s\n\nProposer: reviewer openai/gpt-6.1-sol runner-issue-%s\n' $(cut -c1-8 .replay/T) $ISSUE > .replay/msg && git commit -q -F .replay/msg`. If `$ISSUE` is empty, put the branch name in its place.
   - Remove the checkouts and `.replay/`: `git worktree remove --force` for each, then `rm -rf .replay`, then `git worktree prune`. `git status --short` must print nothing.
   - Then run `python3 tools/jack proposal --title 'promotion replay table (ruling of 20 November 2026, answer 9): every first-parent commit of main to <first 8 of T>'`.
   - If it refuses because the branch does not contain `origin/main`, it prints the merge to run, with two `-m` arguments in double quotes. Run that merge with the same two arguments in single quotes, then run the proposal again, once.

**Report.** Give:
- *T*, the row count and the table's SHA-256;
- the output of the checks in step 4;
- the driver's wall time, and the pull request number;
- or, if you stopped at minute 150, the rows done.

End with one line: `PROPOSED #<n>`, `RESUME: <rows done>/<rows>`, or `STOPPED: <reason>`.
