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
- **This account is counsel's reading, and his read may correct it.** The charter says "every rule". Counsel reads a rule here as a refusal, or a requirement whose breach one edit of the code can show. By that reading three things stay without a standing witness: the order in which the pool's results are put back, that each worker has its own world, and that the check runs its commands side by side. Each was shown once, by its fix text's acceptance, and none is pinned.

**Before anything else.** Read `main`'s log. If any of these fails, stop, report which, and change nothing.
- C2a-3 has opened: the log holds a `push` entry whose `ts` is after 2026-11-30T00:00:00Z. The first such entry is its opening.
- C2a-3 has ended, by one of three. A `decision` of kind `promote` with subject `C2a` whose `ts` is after the opening's `ts`. Or a `decision` of kind `veto` with subject `C2a` or `C2a-3` whose `ts` is after the opening's `ts`. Or the instant now is after the `resolves_by` of the `forecast` entry whose proposer is `counsel`, whose `args.id` is `V8` and whose `seq` is below the opening's; if the log holds no such forecast, this third does not apply. An entry that carries the opening's own `ts` ends nothing (`transcripts/BRIEF-C2a-3-draft.md`, §The subject).
- No later window has opened: the log holds no `push` entry whose `seq` is above the opening's.
- The merge fix has merged: on `main`, `tests/test_jack.py` holds `test_merge_refused_when_the_pull_request_is_closed_during_a_wait` and `tools/jack` holds the refusal's words `not OPEN, during the wait`.

Make the same check again immediately before you propose. If it fails then, do not propose: push the branch and report.

These checks do not reach the time between a proposal and its merge. There the guards are two, and both are counsel's: counsel files this session only when the check holds, and counsel writes the next window's opening paste to enter nothing while a proposal other than the three standing ones is open or a session is in flight, as C2a-3's does (`transcripts/BRIEF-C2a-3-draft.md`, §Order of acts step 2).

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
   - The pin's test runs `test_check_names_the_first_failure_in_its_order` of `tests/test_jack.py` in the copy, with `TMPDIR` set to a directory of the pin's own. That test's commands read `TMPDIR` (line 418). So under `check_tmpdir_shared` they find a directory, the caller's, and what fails is the test's assertion that the check removed its own.
   - Mutant `check_failure_unread`, in `tools/jack`: `the_check` no longer reads a command's exit status.
   - Mutant `check_tmpdir_shared`, in `tools/jack`: `the_check` no longer sets `TMPDIR` for its commands.
   - Twin: that test passes on `main`.
4. **The mutants' strings are the code's as `main` holds it when the session runs.** Each `find` must occur exactly once in the file it edits (`tests/test_pins.py`, line 49).
5. **`EXPECTED` in `pins/pins.py` is raised by three,** since `tests/test_pins.py` compares it with the number of pins registered (line 40).
6. **Nothing else.** No other pin changes, and no file but `pins/pins.py`.

**Paths.**
- **May change:** `pins/pins.py`.
- **May not change:** any other file.

**Size.** `pins/` is counted. This change adds at most 60 counted lines. The cap in force when the session runs is the one C2a-3's opening push sets, which stays until the next opening and is his to state (`transcripts/BRIEF-C2a-3-draft.md`, §The cap). If the pins do not fit under the cap as `main` holds it, push the branch, do not propose, and report the count.

**Acceptance.**
- **(i) The three pins.** At the head, `python3 pins/run.py --only pins_workers_refused merge_refuses_closed check_refuses_failure` prints four rows, each `KILLED`, and ends `KILLED 4, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`. Report the table and how long the run took. If it took more than two minutes, push the branch, do not propose, and report the time: these pins run in every `tests` job.
- **(ii) The whole pins.** `python3 pins/run.py` at the head ends with `origin/main`'s last line, with its `KILLED` raised by four.
- **(iii) The unit tests.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(iv) Each mutant bites where it says.** For each of the four mutants, report the first line of the failure its row shows. For `check_tmpdir_shared` the failure must be an assertion of the unit test, and not a `KeyError` for a `TMPDIR` that is not set.

**What this text does not do.**
- It makes no pin for the three things *Which fix owes what* names as left without one.
- It does not change LAW.md's sentence, and it does not make it true of the past: LAW.md speaks of a pin carried with the change, and these come after it. LAW.md says of itself that it "binds nothing" (line 16). The charter's line is the law.
- It does not change the templates `fix.md` and `fix-reviewer.md`, which ask no pin of a fix. Counsel owes a revision of them, so that the next fix text names its pin or says why it has none.

**Interests.** Counsel wrote the two fix texts of 23 November without a pin and without saying so, and counsel's own pre-read of 24 November is what found it. Pins cost counted lines in a cap that counsel asks him to raise.
