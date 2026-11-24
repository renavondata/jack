# FIX-20261124-fix-pins: the pins that the fixes of 23 and 24 November owe

Counsel's text, 24 November 2026, for the sovereign's read (CHARTER A2.10). The reviewer makes it under `transcripts/sessions/fix-reviewer.md`, on branch `FIX-20261124-fix-pins`, and proposes it. **It is made after C2a-3's opening push and not before.** It adds four pins to `pins/pins.py`. It changes no code that the pins test.

**Why.**
- **The charter asks a witness for every rule.** CHARTER.md, line 42: "Every rule is admitted with a witness that violates it and one that satisfies it". LAW.md says how that is kept today: "every change to `tools/`, `harness/`, `sim/` or `pins/` carries a pin in `pins/pins.py` whose named mutant it kills and whose passing twin it admits" (lines 61 to 64).
- **Four fixes do not carry one.** The two fixes of 23 November changed `pins/run.py` and `tools/jack` and added no pin, and counsel's texts for them did not say so. The two of 24 November add none either, and their texts say so.
- **The cap leaves no room for the pins now.** `main` has 8,340 counted lines against a cap of 8,400, and the two fixes of 24 November take at most 48 of the 60 lines left. Only an opening push raises the cap, and C2a-3's is the next.
- **So the pins are owed, and this text is where the debt is written.** His grant of this text is his word that those fixes stand on `main` without their pins until C2a-3's opening, and no longer than it takes to make them after it.

**Which fix owes what.**
- **`transcripts/FIX-20261123-pins-parallel.md` owes one pin.** It added one rule: "A `PINS_WORKERS` that is not a whole number of at least 1 is refused before any pin runs". Its other points say how the runs are scheduled and put back in order. They add no refusal, and what holds them is that text's acceptance (i), which `transcripts/FIX-20261124-pins-worker.md` repeats.
- **`transcripts/FIX-20261123-check.md` owes one pin.** In its own words, "It does not change what the commands are or what the check refuses." But it re-made the code by which the check finds a failing command and refuses, and no pin holds that refusal.
- **`transcripts/FIX-20261124-pins-worker.md` owes one pin with two mutants,** for its two rules: a run that loses a worker ends by `WorkerLost`, and a test that exits is a kill or a failed twin.
- **`transcripts/FIX-20261124-merge-closed.md` owes one pin,** for its refusal of a pull request that is no longer open.

**Before anything else.** If either of these fails, stop, report which, and change nothing.
- `main`'s log holds a `push` entry whose `ts` is after 2026-11-30T00:00:00Z. That is C2a-3's opening.
- Both fixes of 24 November are on `main`: `pins/run.py` defines `WorkerLost`, and `tests/test_jack.py` holds `test_merge_refused_when_the_pull_request_is_closed_during_a_wait`.

**The change.** Four pins are registered in `pins/pins.py`, each in the form `Pin("<name>", <test>, [Mutant(...)])`.
1. **`pins_workers_refused`.**
   - Requires: with `PINS_WORKERS` set to `0`, `main` of `pins/run.py` prints to standard error the line that names the value, runs no pin and returns 1.
   - Mutant `workers_unchecked`, in `pins/run.py`: the refusal of a number below 1 is removed from `main`.
   - Twin: the runner on `main` refuses `0`.
2. **`pins_worker_lost`.**
   - Requires, with two workers: a run in which one task's process ends by `os._exit(9)` raises `WorkerLost`, and its message names that task.
   - Requires, with one worker: a pin whose test raises `SystemExit(0)` when its mutant is applied gets `KILLED`, and a pin whose test raises it whenever it runs gets `TWIN FAILED`.
   - Mutant `broken_pool_unreported`, in `pins/run.py`: `parallel_pins` no longer turns the pool's break into `WorkerLost`.
   - Mutant `exit_uncaught`, in `pins/run.py`: `SystemExit` is removed from what `run_test` catches.
   - Twin: the runner on `main` does both.
   - The pin's test runs the copy's runner in a process of its own, with a time limit of 60 seconds, on pins it makes there. A pin's test is itself run inside a worker of the pool, so it cannot use that pool.
3. **`merge_refuses_closed`.**
   - Requires: `tools/jack merge` refuses a pull request that it finds no longer open during a wait, in the words `transcripts/FIX-20261124-merge-closed.md` gives.
   - The pin's test runs `test_merge_refused_when_the_pull_request_is_closed_during_a_wait` of `tests/test_jack.py` in the copy, as other pins run a named unit test.
   - Mutant `closed_state_unread`, in `tools/jack`: the refusal of a state other than `OPEN` is removed from `passed`.
   - Twin: that test passes on `main`.
4. **`check_refuses_failure`.**
   - Requires: the check of `tools/jack` refuses when one of its three commands fails, and names the first that failed in `CHECK`'s order.
   - The pin's test runs `test_check_names_the_first_failure_in_its_order` of `tests/test_jack.py` in the copy.
   - Mutant `check_failure_unread`, in `tools/jack`: `the_check` no longer reads a command's exit status.
   - Twin: that test passes on `main`.
5. **The mutants' strings are the code's as `main` holds it when the session runs.** Each `find` must occur exactly once in the file it edits (`tests/test_pins.py`, line 49).
6. **`EXPECTED` in `pins/pins.py` is raised by four,** since `tests/test_pins.py` compares it with the number of pins registered (line 40).
7. **Nothing else.** No other pin changes, and no file but `pins/pins.py`.

**Paths.**
- **May change:** `pins/pins.py`.
- **May not change:** any other file.

**Size.** `pins/` is counted. This change adds at most 80 counted lines. The cap in force when the session runs is the one C2a-3's opening push sets, which is his to state (`transcripts/BRIEF-C2a-3-draft.md`, §The cap), and the count brought to him for it has a line for these 80. If the pins do not fit under the cap as `main` holds it, push the branch, do not propose, and report the count.

**Acceptance.**
- **(i) The four pins.** At the head, `python3 pins/run.py --only pins_workers_refused pins_worker_lost merge_refuses_closed check_refuses_failure` prints five rows, each `KILLED`, and ends `KILLED 5, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`. Report the table and how long the run took. If it took more than two minutes, push the branch, do not propose, and report the time: these pins run in every `tests` job.
- **(ii) The whole pins.** `python3 pins/run.py` at the head ends with `origin/main`'s last line, with its `KILLED` raised by five.
- **(iii) The unit tests.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(iv) Each mutant bites where it says.** For each of the five mutants, report the first line of the failure its row shows. `broken_pool_unreported` must fail because the pool's own exception came out, and not because the 60 seconds passed.

**What this text does not do.**
- It makes no pin for the order in which the pool's results are put back. That is a property of every healthy run, and each change of the runner is accepted against the whole table.
- It does not change LAW.md's sentence. With these pins the sentence is true again of the four fixes.
- It does not change the templates `fix.md` and `fix-reviewer.md`, which ask no pin of a fix. Counsel owes a revision of them, so that the next fix text names its pin or says why it has none.

**Interests.** Counsel wrote four fix texts that carried no pin, two of them without saying so, and counsel's own pre-read of 24 November is what found it. Pins cost counted lines in a cap that counsel asks him to raise.
