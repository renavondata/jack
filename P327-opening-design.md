# The opening paste of C2a-3: counsel's design, before any code (draft of 25 November)

BRIEF-C2a-3 §Order of acts step 2 orders one paste of the sovereign's after 2026-11-30T00:00:00Z. This is the
design I would build it to, put to the adviser before a line is written. The paste is a file on `agent/pastes`, run
by a hash-checked line, like his read's.

## What it is given (fixed in the file, from the opening note)
- `H`, the head of `opening-c2a-3` that the note's part 1 records: after the pins, the code read and the last
  replay session.
- `S`, the evaluator's SHA-256 (`44273c2a…` unless the code read changes it), which `REVIEW-C2a-3-code.md`'s
  `Evaluator:` line and `pins/replay.py` must both hold.
- `L`, the last chain commit the replay record holds.
- The `fix` text, word for word from the brief.

## Its steps
1. **Guards,** as his read's paste: no other paste of counsel's running; `~/git/jack-guy`; `gh` is `gfrmin`; `main`
   fast-forwards; the tree is clean.
2. **The branch, before anything is entered:** `opening-c2a-3` is at `H`; its first commit over `main` is his
   cherry-pick with `SPEC.md` at `c4a5b44b…`; `judge/scope.json`'s cap is 9100, the number his grant states;
   `REVIEW-C2a-3-code.md` begins `VERDICT: ACCEPT` (or `… WITH OBLIGATIONS`) and its `Evaluator:` line, the hash
   `pins/replay.py` holds, and `sha256sum judge/status.py` are all `S`; no merge commit over `main`.
3. **If his `fix` is already on `main`'s log** (the exact subject, by `guy`, kind `fix`), skip to step 6: the paste
   may be run again after a stop.
4. **The wait.** It enters nothing until four things hold together, checked each round, three rounds running,
   thirty seconds apart, for at most eight hours:
   - the clock is past 2026-11-30T00:00:00Z;
   - the lane is quiet, as his read's paste tests it, and no `resolution` follows the last `merge` on `main`'s log;
   - the diary timer's next elapse (`systemctl --user show jack-diary.timer -p NextElapseUSecRealtime`) is at least
     `D` minutes away, `D` the rehearsal's measured time from `fix` to push plus a margin;
   - the timer shows both its calendars (`-p TimersCalendar`), so the streams are running.
   While it waits, it replays every chain commit after `L` up to `main`'s head, as the replay's template defines a
   chain commit, in a scratch worktree, and stops if one does not pass.
5. **The `fix`:** `tools/jack decision fix "<text>"`; then pull, and check the entry is on `main`.
6. **The last replay:** the one commit that holds the `fix`, and any after it, as in step 4.
7. **The merge:** a worktree of `opening-c2a-3` at `~/git/worktrees/jack-guy/opening-c2a-3-push`, merged with
   `origin/main` by a commit whose message ends `Proposer: guy guy-master`. One conflict is foreseen and no other:
   `EXPECTED` in `pins/pins.py`, 108 on `main` after the pins fix and 115 on the branch. The paste resolves it to the
   count of pins registered in the merged tree, 116, and only if that line is the whole of the conflict; any other
   conflict aborts the merge and stops, with the `fix` entered and no push made (§Stop and report if).
8. **The opening note's tests at the merged head:** counted lines at most 9100; each commit's `Proposer:` party
   against its paths, the two kinds of commit apart; the three hashes of step 2 again; the unit tests and the pins
   are the push's own `tests` run and are not re-run here.
9. **The push:** `tools/jack push opening-c2a-3-push --opens C2a-3 --review <the worktree>/transcripts/REVIEW-C2a-3-code.md`.
   If the verb refuses because `main` moved, pull, merge again (step 7), replay the new commits, test again and push
   again, up to a bound the note states; at the bound it stops and says what it has entered.

## Questions I have not settled
- The time `D`. The rehearsal measures it; the brief says the one such paste so far took 6 min 21 s from `fix` to
  push, before the verb's check grew. The verb's check now runs the unit tests and the pins, about 10 minutes on
  steel.
- Whether the replay in step 4 should run the reviewer's own driver from the branch, or a script of the paste's.
  The first keeps one definition of a chain commit; the second keeps the paste from running code a session wrote.
- Whether step 7's resolution of `EXPECTED` belongs in his paste at all, or whether a pins session should instead
  set `EXPECTED` on the branch to the count it will have after the merge. The second makes the branch's own tests
  fail until the merge.
