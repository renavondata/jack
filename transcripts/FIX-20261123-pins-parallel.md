# FIX-20261123-pins-parallel: run the pins on several cores, with the same table

Counsel's text, 23 November 2026, for the sovereign's read (CHARTER A2.10). The reviewer makes it under `transcripts/sessions/fix-reviewer.md`, on branch `FIX-20261123-pins-parallel`, and proposes it. It changes how `pins/run.py` schedules its runs. It changes no pin, twin or mutant, and no row of the table the pins print.

**Why.**
- **The pins are the longest step of the `tests` job:** 690 to 802 s since the push of seq 7281, against 187 s before it (ADVISER.md entry 140). New forecast streams are paused until the job takes 15 minutes or less (ADVISER.md entry 146).
- **The time is the pins' own work, which they need.** A profile of a full run (ADVISER.md entry 150) puts 39% of it in `replay_drift`, which runs `judge/status.py` over rows of the real history, 15% in `c2a_prime`'s cases, and a tenth each in the judge and in the fixtures. Building the fixtures once took the pins only from 926 s to 885 s on counsel's machine.
- **The runs are independent, but run one after another on one core.** `pins/run.py` gives every twin and every mutant its own disposable copy of the tree, and every test its own fixtures. Nothing one run does is read by another. The hosted runner has four cores, and steel more.
- **A prototype, counsel's own and not proposed,** ran the twins and then the mutants of passing twins in a pool of forked workers. On two cores the full pins took 538 s, against 926 s one after another. Its 162 rows have the same pin, mutant and status as a run that keeps each pin's runs together. Scheduling whole pins instead took 685 s, because `replay_drift`'s four runs, about 90 s each, then ran in one worker.

**The change.**
1. **`python3 pins/run.py` runs its runs in parallel.** It uses a pool of worker processes, started by `fork`. The number of workers is the environment's `PINS_WORKERS` if that is set. Otherwise it is the number of CPUs the process may use (`os.sched_getaffinity(0)`), and at most 4. With one worker it runs exactly as today.
2. **One run is the unit of work.** First every pin's twin runs, then every mutant of each pin whose twin passed. Each is its own task, with its own disposable copy, exactly as today. A pin whose twin fails still gets one `TWIN FAILED` row and no mutant runs, and a pin with a missing path still gets its `PENDING` rows without running.
3. **The results are put back in today's order.** That is the order of `pins.PINS`, and within a pin the order of its mutants, whatever order the runs finish in. The table, its counts line and the exit code are those of a sequential run.
4. **`run_pins(pin_list, root)` called as a function stays sequential.** `tests/test_pins.py` calls it with pins of its own, and its default stays one worker. Only `main` chooses the pool.
5. **Nothing else.** No pin, twin, mutant, fixture or test changes, and no file but `pins/run.py`.

**Paths.**
- **May change:** `pins/run.py`.
- **May not change:** any other file.

**Acceptance.**
- **(i) The same rows.** At the head, run `PINS_WORKERS=1 python3 pins/run.py` and then `python3 pins/run.py`, keeping both tables.
  - Their first three columns (pin, mutant, status), row by row, must be identical. Compare them with `awk` and `cmp`, and report the result. The detail column is not compared, because it holds temporary paths that differ from run to run, sequential runs included.
  - Both must end with the last line of `origin/main`'s `python3 pins/run.py`, today `KILLED 158, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`.
- **(ii) The unit tests are unchanged.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(iii) Faster.** Report `nproc` and the number of workers the parallel run used. With at least two workers, the parallel run at the head takes at most two thirds of the time of the `PINS_WORKERS=1` run, measured one after the other. If it does not, push the branch, do not propose, and report both times.
- **(iv) Report the time of the `tests` job on the proposal's head**, from its run on GitHub, with the time of each step.
