# Counsel's third pre-read of `transcripts/sessions/c2a-3-build.md` at `a59c4f8b`

A fresh agent of counsel's own, launched 2026-11-24T14:38Z under the sovereign's rule of 18 November; its hand-back arrived at about 15:05Z. It is model output and no party's word. Copied whole, with the harness's indent removed.

---

VERDICT: FAIL

Text read: /home/claude/wt-bld/transcripts/sessions/c2a-3-build.md at a59c4f8b, and the three README lines.

FINDINGS

1. FIX, line 27 (step 8, second test). "The first field after the hash must be `builder`" passes trailers that `tools/jack` refuses (`filled`, line 24; `push`, lines 242-243: one line, two or more fields, no `<`). Scratch output:
   - `Proposer: builder` alone prints `1a52c52 builder`;
   - line 38's own words copied unfilled print `1d1d637 builder m runner-issue-<the value of $ISSUE>`;
   - two `Proposer:` lines print a second line with no hash.
   All three pass as written. His push would refuse the branch, after his `fix` is entered.
   Change: "After the hash must come `builder` and at least one more field, on that one line, with no `<`. Anything else is a commit without a filled trailer."

2. FIX, lines 25, 38, 49. Line 38 publishes each commit at once; lines 25 and 49 test your own commits "before your last push". When the checks pass no push follows them, so "last push" names nothing. Only paths are tested before publication. A commit of the session's own without its trailer is already on `opening-c2a-3`, cannot be amended (line 9, no force), and stops every later session at step 8.
   Change: line 25 "your own before your last push" to "your own before each push"; line 49's heading to "Checks."

3. FIX, line 17. A failed fetch is not among "either". Scratch: branch deleted on origin, runner's tracking ref left (its `git fetch origin` does not prune). The fetch exits 128 (`couldn't find remote ref opening-c2a-3`), both tests pass, steps 3 and 4 pass on the stale ref, and the first `git push -q origin HEAD:opening-c2a-3` re-creates the withdrawn branch (rc 0).
   Change: "If either fails" to "If the fetch or either test fails". Ref locks do occur here (run.yml line 63 retries five times), so one retry would spare a stop.

4. NOTE, line 52, check (c). `origin/main` is not the head's base (P's parent is), and it moves under the session whenever another job fetches in the shared clone; it moved from c755901c to af472859 in the real clone during this read. Scratch: main gained one test file, the head one, and the two counts were equal. FIX-20261124-pins-worker (granted, up to 55 counted lines) is pending.
   Change: "`origin/main`" to "*P*".

5. NOTE, line 64. A later session begins from nothing and reads only the worktree, so what is left reaches it only through commits.
   Change: "and say so" to "and say what is left in that commit's message".

6. NOTE, line 33. False as written: §The code from Change 1 names §The window, §The subject and §The late-report rule, not §Pre-stated criteria.
   Change: move "§Pre-stated criteria for C2a-3" out of "the sections those paragraphs name".

7. NOTE, line 42. Narrower than the brief's line 190, which also binds the strings `tests/test_status.py` lines 195-201 and `pins/c2a_prime.py` lines 26-31 replace (the second must occur exactly once). §The code is read whole, so no contradiction.

CASES

- A1: right. Status `?? .build/`, ancestor test passes, reset lands on P, step 4 finds P, step 8 prints nothing (second command exits 1), two commits pushed rc 0.
- A2: right. Continues; step 8 lists `judge/status.py`, `tests/test_b.py` and two `builder m runner-issue-1` lines.
- A3: all four caught. Counsel trailer: `e560844 counsel other-model builder`. No trailer: `8ee6a8e` alone. Rename: `pins/x.py` listed. Merge of main: `SPEC.md`, `judge/scope.json`, `log.jsonl`, `pins/y.py` listed and main's `herald`/`counsel` lines shown, even with a builder trailer on the merge. Not caught: finding 1.
- A4: right. Old branch at P+2: ancestor test rc 1, stop. Directory with `.build/`: step 1 stops. An old branch still on main goes on, harmlessly.
- A5: second push `! [rejected] HEAD -> opening-c2a-3 (non-fast-forward)`, rc 1. The rule fits. The commit stays on the session's local branch only; git's hint offers `git pull`, which would merge main.
- A6: steps 4 and 8, the `git diff --stat` and (d) gave identical output before and after main moved and was re-fetched. Only (c) shifts (finding 4).
- A7: nothing else. `.gitignore` holds `__pycache__/`, `*.pyc`, `kernel2/.cache/`; run.yml keeps prompt and transcript in `$RUNNER_TEMP`; full unit and pin runs left only `.build/`. With `status.showUntrackedFiles=all` the line would read `?? .build/start` (runner's config unseen).

B. No rule is impossible. Conflict: finding 2. Left to guess: findings 3 and 5, and whether a check is run again after a fix. A check killed at 15 minutes is reported and not rerun, nothing else follows, and the head stays untested whole. The limit is opencode's default (run.yml line 62); `c2a-3-table.md` line 103 raises it for one call.

VERIFIED TRUE

- Cherry-pick of f6d6db7 onto c755901c gives `SPEC.md` c4a5b44b… and one `9100`; the brief and table hashes match on main.
- `judge/status.py` line 433 is the first-parent walk; lines 436-437 read `tools/status.py`; `judge/evaluate.py` calls `main`, `inputs`, `assess`, `promotion_line`.
- `counted_lines` is at `judge/judge.py` line 117; 8,340 at main and at P.
- Mutants are in `pins/pins.py`, with `pins/replay.py`'s strings.
- With one harmless byte changed: `replay_drift twin TWIN FAILED (AssertionError: status: moved bytes differ)`.
- Table: 773 rows; 4 and 734 unmarked; 735 (first marked) and 772 marked. Check (e) as written reproduced `stdout` at all four rows with main's evaluator (298 s at row 772 here; steel 114 s), `marked` differing from `window C2a:` on.
- Both SPEC phrases are present.
- Unit tests at P: 312 OK in 737 s here.
- No double quote in a command; only `{MODEL}` and `{BRANCH}`; no outside path in a command.
- Nothing of the reviewer's or counsel's is ordered; no contradiction with the brief's §The window, §Precondition 6, Order of acts step 1, or RUNBOOK's "Text before code".

NOT VERIFIED

- The grant's words (not entered; `9,100` and the apostrophe must match).
- The builder's right to push to `opening-c2a-3`.
- What a 15-minute kill leaves running; timings on steel under load.

Housekeeping: scratch removed, real checkout untouched. The scratch unit run left about 55 temp directories in `/tmp` (`diff-keys-*`, `sim-*`, `pins-*`, `repo-*`); my attempt to delete them was denied, so they remain.
