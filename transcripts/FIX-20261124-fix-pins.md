# FIX-20261124-fix-pins: the pins that three fixes of 23 and 24 November owe

Counsel's text, 24 November 2026, for the sovereign's read (CHARTER A2.10). The reviewer makes it under `transcripts/sessions/fix-reviewer.md`, on branch `FIX-20261124-fix-pins`, and proposes it. **It is made after C2a-3 has ended and not before.** It adds three pins to `pins/pins.py`. It changes no code that the pins test.

**Why.**
- **The charter asks a witness for every rule.** CHARTER.md, line 42: "Every rule is admitted with a witness that violates it and one that satisfies it". LAW.md says how that is kept today: "every change to `tools/`, `harness/`, `sim/` or `pins/` carries a pin in `pins/pins.py` whose named mutant it kills and whose passing twin it admits" (lines 61 to 64).
- **Three fixes do not carry one.** The two fixes of 23 November changed `pins/run.py` and `tools/jack` and added no pin, and counsel's texts for them did not say so. The fix of `transcripts/FIX-20261124-merge-closed.md` is the builder's, and `pins/` is not the builder's path. The fix of `transcripts/FIX-20261124-pins-worker.md` carries its own pin and owes none.
- **The cap leaves no room for these pins now.** `main` has 8,340 counted lines against a cap of 8,400, and the pins fix with its pin takes at most 55 of the 60 lines left. Only an opening push raises the cap, and C2a-3's is the next. And while C2a-3 is open its brief refuses any code but its own: "no code but §The code" (`transcripts/BRIEF-C2a-3-draft.md`, refusal list).
- **So the pins are owed, and this text is where the debt is written.** His grant of this text is his word that the two fixes of 23 November stand on `main` without their pins until C2a-3 has ended, and no longer than it takes to make them after that. C2a-3 runs for seven days at most. The merge fix is itself built after C2a-3 has ended, and its pin follows it at once.

**Which fix owes what.**
- **`transcripts/FIX-20261123-pins-parallel.md` owes one pin.** It added one rule: "A `PINS_WORKERS` that is not a whole number of at least 1 is refused before any pin runs". Its other points say how the runs are scheduled and put back in order. They add no refusal, and what holds them is that text's acceptance (i), which `transcripts/FIX-20261124-pins-worker.md` repeats.
- **`transcripts/FIX-20261123-check.md` owes one pin with two mutants.** In its own words, "It does not change what the commands are or what the check refuses." But it re-made the code by which the check finds a failing command and refuses, and no pin holds that refusal. And it added a rule: the check gives its commands a temporary directory of their own and removes it.
- **`transcripts/FIX-20261124-merge-closed.md` owes one pin,** for its refusal of a pull request that is no longer open.

**Before anything else.** If any of these fails, stop, report which, and change nothing.
- C2a-3 has opened: `main`'s log holds a `push` entry whose `ts` is after 2026-11-30T00:00:00Z. The first such entry is its opening.
- C2a-3 has ended: after that entry the log holds a `decision` of kind `promote` with subject `C2a`, or a `decision` of kind `veto` with subject `C2a` or `C2a-3`; or the instant now is after the `resolves_by` of the forecast whose `args.id` is `V8`.
- No later window has opened: the log holds no second `push` entry after C2a-3's opening.
- The merge fix is on `main`: `tests/test_jack.py` holds `test_merge_refused_when_the_pull_request_is_closed_during_a_wait`.

**The change.** Three pins are registered in `pins/pins.py`, each in the form `Pin("<name>", <test>, [Mutant(...)])`.
1. **`pins_workers_refused`.**
   - Requires: with `PINS_WORKERS` set to `0`, `main` of `pins/run.py` prints to standard error the line that names the value, runs no pin and returns 1.
   - Mutant `workers_unchecked`, in `pins/run.py`: the refusal of a number below 1 is removed from `main`.
   - Twin: the runner on `main` refuses `0`.
2. **`merge_refuses_closed`.**
   - Requires: `tools/jack merge` refuses a pull request that it finds no longer open during a wait, in the words `transcripts/FIX-20261124-merge-closed.md` gives.
   - The pin's test runs `test_merge_refused_when_the_pull_request_is_closed_during_a_wait` of `tests/test_jack.py` in the copy, as other pins run a named unit test.
   - Mutant `closed_state_unread`, in `tools/jack`: the refusal of a state other than `OPEN` is removed from `passed`.
   - Twin: that test passes on `main`.
3. **`check_refuses_failure`.**
   - Requires: the check of `tools/jack` refuses when one of its three commands fails, and names the first that failed in `CHECK`'s order; and it gives its commands a temporary directory of their own, which it removes.
   - The pin's test runs `test_check_names_the_first_failure_in_its_order` of `tests/test_jack.py` in the copy.
   - Mutant `check_failure_unread`, in `tools/jack`: `the_check` no longer reads a command's exit status.
   - Mutant `check_tmpdir_shared`, in `tools/jack`: `the_check` no longer sets `TMPDIR` for its commands.
   - Twin: that test passes on `main`.
4. **The mutants' strings are the code's as `main` holds it when the session runs.** Each `find` must occur exactly once in the file it edits (`tests/test_pins.py`, line 49).
5. **`EXPECTED` in `pins/pins.py` is raised by three,** since `tests/test_pins.py` compares it with the number of pins registered (line 40).
6. **Nothing else.** No other pin changes, and no file but `pins/pins.py`.

**Paths.**
- **May change:** `pins/pins.py`.
- **May not change:** any other file.

**Size.** `pins/` is counted. This change adds at most 60 counted lines. The cap in force when the session runs is the one C2a-3's opening push sets, which stays until the next opening and is his to state (`transcripts/BRIEF-C2a-3-draft.md`, §The cap), and the count brought to him for it has a line for these 60. If the pins do not fit under the cap as `main` holds it, push the branch, do not propose, and report the count.

**Acceptance.**
- **(i) The three pins.** At the head, `python3 pins/run.py --only pins_workers_refused merge_refuses_closed check_refuses_failure` prints four rows, each `KILLED`, and ends `KILLED 4, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`. Report the table and how long the run took. If it took more than two minutes, push the branch, do not propose, and report the time: these pins run in every `tests` job.
- **(ii) The whole pins.** `python3 pins/run.py` at the head ends with `origin/main`'s last line, with its `KILLED` raised by four.
- **(iii) The unit tests.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(iv) Each mutant bites where it says.** For each of the four mutants, report the first line of the failure its row shows.

**What this text does not do.**
- It makes no pin for the order in which the pool's results are put back. That is a property of every healthy run, and each change of the runner is accepted against the whole table.
- It does not change LAW.md's sentence. With these pins the sentence is true again of the four fixes.
- It does not change the templates `fix.md` and `fix-reviewer.md`, which ask no pin of a fix. Counsel owes a revision of them, so that the next fix text names its pin or says why it has none.

**Interests.** Counsel wrote the two fix texts of 23 November without a pin and without saying so, and counsel's own pre-read of 24 November is what found it. Pins cost counted lines in a cap that counsel asks him to raise.
