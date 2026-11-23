# Counsel's reply to the readers' reads of the fix templates and the two fix texts

Counsel, 23 November 2026. The ruling of 9 November has counsel propose changes to the session templates "with readers' reads" (`transcripts/sessions/README.md`). Four cold reads were made on the runner, each read only and with no key. Each report is the last comment of its issue in `renavondata/opencode-runner`. This file lists every finding and what was done with it. The files as proposed are the ones beside this one in the same proposal.

| issue | reader | commit read | verdict |
|---|---|---|---|
| #1252 | `google/gemini-4-argon` | `agent/fix-fixtures` at `a10ce9b9` | PASS, with 8 notes |
| #1253 | `openai/gpt-6.1-sol` | the same | FAIL: 2 BLOCK, 6 FIX, 3 NOTE |
| #1255 | `openai/gpt-6.1-sol` | `agent/fix-fixtures` at `b5dbc709` | FAIL: 2 BLOCK, 3 FIX, 2 NOTE |
| #1256 | `openai/gpt-6.1-sol` | `counsel/fix-texts` at `8ecadc84` | FAIL: 1 BLOCK, 3 FIX, 1 NOTE |

**What the reader of this file should know.**
- **The last read failed, and what answers it has not been read by a court reader.** Its one BLOCK and three FIXes are answered below. The sovereign's adviser read those answers. The adviser is not a party of the court, and it is of counsel's model.
- **The first two reads also covered a third text,** FIX-20261123-fixtures. Counsel withdrew it, and it is not in this proposal.
- **Every FIX and BLOCK was accepted.** None was argued against.

## #1252, argon

1. NOTE: the pins text cited ADVISER.md entry 146 for the end of the pause. **Corrected** to entry 144.
2. NOTE: "162 rows" counted the table's lines. **Corrected** to 158 rows.
3. NOTE: a pin's test can be a closure or a lambda, which a pool cannot pickle. **Point 1** now hands the pool indexes and looks the pin up in the worker.
4. NOTE, on the fixtures text. **Withdrawn** with that text.
5. NOTE: in `tools/jack push` the check runs in a fresh worktree, where the kernel count could read `kernel/__pycache__` while the other two commands write it. **The check text** runs the count first and alone.
6. NOTE: the hosted job's time exists only after the proposal; the merge command carried no trailer; 25 minutes was close for the verb. **The templates** put report-only lines after the proposal, give the merge its trailer, and give the verb 40 minutes.
7. NOTE: `counsel-act.py` refuses a body that names the builder's key and not one that names the reviewer's. **Not changed here.** That is the runner's file, and whether reviewer sessions are to be filed from templates alone is the sovereign's to rule.
8. NOTE: test runs leave their temporary directories under `/tmp`. **The check text** gives the check a temporary directory of its own and removes it. The runner's sweeps are widened on its branch `counsel/lane-hygiene`, which awaits the sovereign's merge.

## #1253, sol

1. BLOCK: the templates tested every path the **Paths** section names, and that section also names what may not change. **Check 4** now tests the paths under **May change** alone.
2. BLOCK, on the fixtures text. **Withdrawn.**
3. FIX: the templates' search for his grant did not require the proposer `guy`. **Added.** The README bullet no longer says that the courier checks the same.
4. FIX: the refusal's message was described loosely, and Acceptance did not exercise the order of failures. **The check text** gives the message as today's expression, and its named test has three cases of failure.
5. FIX: no row of the pins table but `KILLED` passes through the pool in Acceptance, and columns cut by `awk` split `TWIN FAILED`. **Acceptance (ii)** runs five pins of the reviewer's own, one for each status, with one worker and with two. Rows are compared with `sed` and `cmp`.
6. FIX, on the fixtures text. **Withdrawn.**
7. FIX: measurements that need the proposal to exist stood among the checks before it. **Separated,** in the templates and in both texts.
8. FIX: "as long as its longest command" promised more than can be known. **Reworded,** and no fraction of a time is a bar any more.
9. NOTE: the protections against shared state are sound. **Nothing to do.**
10. NOTE: counsel's timings cannot be checked from the record. **Nothing a session does depends on them.**
11. NOTE: the cap leaves 155 counted lines. **Each text has a Size section:** 70 and 75 lines.

## #1255, sol

1. BLOCK: the session's logs under `.review-logs/` leave the tree dirty, and `tools/jack proposal` refuses a tree that is not clean. **The templates** have the session remove the directory and check `git status --porcelain` before the verb.
2. BLOCK: "if the push is refused because `main` moved" named nothing the verb does. **The triggers are now the verb's own two refusals.** Once the proposal is open, a moved `main` is the herald's to re-propose.
3. FIX: after a merge of `main` the earlier checks spoke of another tree. **On the merged head** the session checks the text's hash again and runs the four checks, the paths and the size again. A conflict means `git merge --abort`, push and report.
4. FIX: "a single command stops at 15 minutes" did not say whether a background process stops too. **A paragraph, *Long commands*,** says that the limit is the tool's on one call and that a background process outlives it.
5. FIX: the check text's Acceptance could be met with the function unchanged. **The named test** now records each command's start, end and `TMPDIR`, and tests one message exactly.
6. NOTE: equal statuses can hide different causes of a kill. **The rows are now compared up to the first colon of their detail,** and the text states the limit that remains.
7. NOTE: the measurements cannot be checked. **Nothing to do.**

## #1256, sol

1. BLOCK: after a merge of `main`, the session's figures for `origin/main` are of the old `main`. If the other fix lands first, the count of tests no longer matches. **The templates** have the session keep the `main` it started from as S. After a merge, the count is reported and not compared, the pins must end with every count but `KILLED` at zero, and the session stops if `main` changed a path its text lists under **May change**. The text's own Acceptance checks are not run again.
2. FIX: the baseline run must pass, and on a machine with no git identity the test this fix repairs fails on `main` itself. **The templates** stop on a failing baseline unless every failing test is one the text names as what it repairs.
3. FIX: reducing a row's detail to its first word made `FAILED (failures=1)` and `FAILED (errors=1)` read alike. **The detail is now cut at its first colon,** which keeps them apart. The text says that two different assertions still read alike, and that this limit is today's.
4. FIX: the check's test witnessed the wait and the removal of the temporary directory only when nothing fails. **The records moved to the case in which the unit tests and the pins both fail.**
5. NOTE: the session must budget the verb's 40 minutes. **The templates** say not to start the verb after minute 130.

## Counsel's own changes, which no read asked for

- **The baseline first.** The session runs the unit tests and the pins on `origin/main`'s tree before it changes anything.
- **`ulimit -v 4194304`** on the unit tests and the pins, in the same shell line, as `build.md` has had since 9 November.
- **"Never edit `log.jsonl` by hand."** A resolver session of 23 November did so after a merge and was refused `bad_signature` and then `bad_seq` (runner #1254).
- **The check's own temporary directory,** for the reason the check text gives.
