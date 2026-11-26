# The opening push of C2a-3 (counsel's note for the sovereign's paste)

BRIEF-C2a-3 §The window and §Order of acts step 2. Part 1 records what the push carries, because `jack push` checks
none of it; part 2 is the paste; part 3 is what follows it. **Values marked TBD are fixed by the rehearsal, and the
commands are final only when counsel says so in the sitting message.**

## 1. What the push carries, at the branch head

Branch `opening-c2a-3`, head `82ddc41bc6a12171729ddab1176bc0bdb7da10f4` (*H*), as the reviewer's last replay session left it on 26 November.

- **The four records of §The window, taken at the merged head by the paste itself (part 2):**
  - **Counted lines,** `judge.counted_lines` over `judge/scope.json`'s `counted`: 8,643 at *H*; 8,696 at a scratch merge of `main`
    (`bda6ccf7`) into it on 26 November, with EXPECTED set as the paste sets it. At most 9,100. His grant keeps 55 lines of it for the pins fix before the opening and 82 for the merge fix
    and its three pins after the window.
  - **Each commit's party against its paths,** the two kinds of commit apart:

    | commit | author / committer | `Proposer:` | paths | |
    |---|---|---|---|---|
    | `5c6db4ee` | counsel / Guy Freeman | counsel | `SPEC.md`, `judge/scope.json` | the scope's change: counsel's patch `f6d6db7d`, applied by his own hand after his grant (seq 7615) |
    | `ae3fdb48`, `8a614383`, `7d7f8947` | Guy Freeman / Guy Freeman | builder (#1322) | `judge/status.py`, `tests/test_status_third.py` | the evaluator's change and its tests; `judge/` reaches `main` only by this push |
    | `86f62e9c`, `2dd66bef`, `68a3221e` | Guy Freeman / Guy Freeman | reviewer (#1333) | `pins/c2a_third.py`, `pins/pins.py`, `pins/replay.py` | the eight pins and `replay_drift` re-aimed |
    | `719d407d` | Guy Freeman / Guy Freeman | reviewer (#1335) | `transcripts/REVIEW-C2a-3-code.md` | the code read |
    | `3906d842`, `82ddc41b` | Guy Freeman / Guy Freeman | reviewer (#1373, #1378) | `transcripts/evidence/promotion-replay-c2a-3-check.jsonl`, `…-check-driver.py` | the replay's record |
    | the merge | Guy Freeman / Guy Freeman | guy | none of its own | `main` brought in after the `fix`, by the paste |

    Sessions on the runner commit under the runner's git identity, which is his name; the party of such a commit is in
    its trailer. Only the first commit and the merge are of his own hand.
  - **The replay:** the reviewer's record `transcripts/evidence/promotion-replay-c2a-3-check.jsonl` on the branch holds
    every row of `spec/vectors/promotion-replay-c2a-3.json` and every commit of `main`'s first-parent chain after *T*
    (`96658263`) up to `deabad5082b88e1332a9ed56d5ca8fcae06cadb5` (*L*), 51 commits, each as the brief's §The code states:
    824 lines, 773 of the table and 51 of the chain, every one passed (runner #1340 published nothing; #1373 and #1378
    did). The paste replays the commits after *L* while
    it waits, and the one that holds the `fix` after it.
  - **The code read:** `transcripts/REVIEW-C2a-3-code.md`, first line `VERDICT: ACCEPT`, `Reviewed tree: 68a3221e`,
    reader `google/gemini-4-argon` (runner #1335, another family than the builder's `openai/gpt-6.1-sol`). Two NOTEs, no
    FIX. Its `Evaluator:` line, the hash `pins/replay.py` holds, and `judge/status.py`'s own are all
    `44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0`.
- **The gate's two reviews of the brief** are on `main`: `transcripts/REVIEW-C2a-3-20261123T2340-openai.md` and
  `transcripts/REVIEW-C2a-3-20261124T0030-google.md`. The brief is not amended again before the push.
- **The pins and the tests,** as the code read ran them at `68a3221e`: 318 tests OK (one skipped); pins KILLED 173,
  none survived, stale, twin failed or pending.
- **One merge conflict is foreseen, and no other:** `EXPECTED` in `pins/pins.py`, 108 on `main` after the pins fix and
  115 on the branch. The paste sets it to the count of pins registered in the merged tree, 116, and stops at any other
  conflict.
- **The trusted base changes in five places:** `judge/scope.json`'s `cap`, 8,400 → 9,100; SPEC §10's block, to match;
  one clause of SPEC §10's cap history; the two sentences of SPEC §10's paragraph on the promotion evaluator; and the
  evaluator, `judge/status.py`.

To print these again:

```
git fetch origin main opening-c2a-3
git log --reverse --format='%h | %an | %cn | %(trailers:key=Proposer,valueonly,separator=%x20) | %s' origin/main..origin/opening-c2a-3
git show origin/opening-c2a-3:transcripts/REVIEW-C2a-3-code.md | head -3
git show origin/opening-c2a-3:judge/status.py | sha256sum
```

The window opens at this push's `ts` and ends at V8's `resolves_by`, `2026-12-07T00:00:00Z`, the date the brief gives a V8 entered before 2026-11-30T00:00:00Z, as this one is (§The window).

## 2. The paste

TBD: one line that fetches `c2a-3-open.sh` from `agent/pastes`, checks its hash and runs it, made as his read's was.
It may be started before 2026-11-30T00:00:00Z: it waits for that instant itself. What it does, in order
(ADVISER.md entries 327 to 337, and the revision for counsel's pre-read of 26 November):
1. checks the branch at the head above, with the three hashes and the review's verdict, entering nothing; and checks
   the log: counsel's V8 on it once, no `push` after 2026-11-30T00:00:00Z, none inside C2a-prime's window;
2. waits, with no bound of its own, until 2026-11-30T00:00:00Z has passed, the lane is quiet three rounds running,
   no `resolution` follows the last `merge` on `main`'s log, the diary's timer shows both its calendars and its next
   tick is at least *D* = 45 minutes away; and replays `main`'s new commits as it waits, stopping if one does not
   pass or the replay cannot run;
3. brings his `main` up to `origin/main`, checks the log again, and enters his `fix`, word for word from §Order of
   acts step 2, unless it is already the first `fix` that names C2a-prime; any other such `fix` stops it; then runs
   `window_fixes` over the whole log with the branch's evaluator, and stops if it does not return the `fix`'s `seq`
   or reports it unverified (§Stop and report if);
4. replays the commit that holds the `fix`; merges `main` into the branch with his trailer; takes the four records
   and the three hashes again at the merged head; and pushes with `--opens C2a-3`. If the push is refused and `main`
   has moved, it waits again as in 2 and tries again, three attempts in all; if it is refused and `main` has not
   moved, it stops (§Stop and report if).

**D, as the rehearsal measured it on steel on 26 November** (`c2a-3-rehearse.sh`, `agent/pastes` `a5923224`): one
chain commit's replay 858 s; the push verb's check (`tools/jack`, `the_check`) 1,110 s; `judge/selfcheck.py` 74 s,
which both verbs run; the scratch merge 2 s. With `window_fixes` (164 s on counsel's machine) and the verbs' own
reading of the log, the time from `fix` to push is about 39 minutes; the paste asks for 45. The timer's calendars on
steel are `*-*-* 00/3:20:00 UTC` and `*-*-* *:10:00 UTC`. On the lane of 25–26 November that left about 11 quiet
minutes a day with no tick due for 45 minutes, so the paste may wait a day or more for its slot (ADVISER.md
entry 371).

Where it stops, its last line says what it has entered.

## 3. After the push

Counsel reads the status tool on the new `main` with its evidence, as `jack decision promote` gives it:
`python3 judge/status.py --subject C2a --run <run> --runs <runs>` (`tools/jack`, lines 281 to 304). `<run>` is the
`tests` run on `main` at its head commit, which alone witnesses criteria 1 and 2; `<runs>` is the list of `tests` runs
on `main` paged from GitHub at that moment, which the attack gate and liveness read; from the promotion on, `--acts`
names the committed table.

- **The window line** reads from the push's `ts` to `2026-12-07T00:00:00Z`, V8's `resolves_by`. Criteria 1 and 2 are
  met once the `tests` run at the push's commit is green; criterion 3 reads `main`'s own commits from the push on.
- **The promotion cannot be immediate.** A3.4 reads `STOP` until the streams' entries fall inside the new window, as it
  did at C2a-prime's opening (twenty hours of batches then gave 80 : 240).
- **Criterion 6 does not turn on the writs that fall due.** On 25 November the evaluator on `main`, given the 919
  successful `tests` runs on `main` (`judge/status.py --subject C2a --runs <runs> --as-of <instant>`), read the attack
  gate at `2026-10-31T13:32:21Z`, and continued liveness (printed as a fraction) at about 9.1e9 over 641 items as of
  `12:30Z`, and about 3.5e6 over 665 items as of `2026-11-30T00:00:01Z`, its projected expiries included. Criterion 6
  needs 20. The rehearsal prints the evaluator's own figure again at the opening, with the log as it then stands.
- **The acts evidence.** Counsel commits the raw and attributed tables of the window by a proposal (§The acts
  evidence), re-runs the attributed command once it has merged, and sends the promotion paste, made in
  `~/git/jack-guy` like this one, which names the table:

  ```
  tools/jack decision promote C2a --acts transcripts/evidence/acts-c2a3-<end>.csv
  ```

  The verb refuses unless the status line reads `lawful` and the file is the one committed at `HEAD`. Between the
  opening and that paste the sovereign does nothing on GitHub under his own login but the pastes: one `repair` row on
  the table makes the promotion impossible, and the window then fails at V8's `resolves_by`.
- **What the table does not see,** as at C2a-prime: a re-run inside the window of a workflow run created before the
  opening. Before the promotion paste counsel also runs the classifier from an earlier instant and reads the rows that
  fall inside the window; a `repair` row there goes to the sovereign before any promotion.
- **If the window cannot promote,** nothing is entered for it: no second V8, and the next window is pre-stated afresh
  (§Stop and report if).
