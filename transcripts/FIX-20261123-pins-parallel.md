# FIX-20261123-pins-parallel: run the pins on several cores, with the same table

Counsel's text, 23 November 2026, for the sovereign's read (CHARTER A2.10). The reviewer makes it under `transcripts/sessions/fix-reviewer.md`, on branch `FIX-20261123-pins-parallel`, and proposes it. It changes how `pins/run.py` schedules its runs. It changes no pin, twin or mutant, and no row of the table the pins print.

**Why.**
- **The pins are the longest step of the `tests` job:** 690 to 802 s since the push of seq 7281, against 187 s before it (ADVISER.md entry 140). New forecast streams are paused until the job takes 15 minutes or less (ADVISER.md entry 144).
- **The time is the pins' own work, which they need.** A profile of a full run (ADVISER.md entry 150) puts 39% of it in `replay_drift`, which runs `judge/status.py` over rows of the real history, 15% in `c2a_prime`'s cases, and a tenth each in the judge and in the fixtures. Building the fixtures once took the pins only from 926 s to 885 s on counsel's machine.
- **The runs are independent but for one file, and run one after another on one core.** `pins/run.py` gives every twin and every mutant its own disposable copy of the tree, and every test its own fixtures. What runs share is the world that `pins/pins.py` caches for the process (lines 33 to 35), and with it one key directory. In that directory, every fixture's kernel copy reads `verified-signatures.json` when it is imported, and `tests/promotion_fixture.pad` rewrites that file whole. Within one process that is safe, because runs follow one another. Across workers it would not be, so point 5 gives each worker its own world (the adviser's H1, ADVISER.md entry 154). The hosted runner has four cores, and steel more.
- **A prototype, counsel's own and not proposed,** ran the twins and then the mutants of passing twins in a pool of forked workers. On two cores the full pins took 538 s, against 926 s one after another. Its 158 rows have the same pin, mutant and status as a run that keeps each pin's runs together. Scheduling whole pins instead took 685 s, because `replay_drift`'s four runs, about 90 s each, then ran in one worker.

**The change.**
1. **`python3 pins/run.py` runs its runs in parallel.** It uses a pool of worker processes, started by `fork`. The number of workers is the environment's `PINS_WORKERS` if that is set. Otherwise it is the number of CPUs the process may use (`os.sched_getaffinity(0)`), and at most 4. With one worker it runs exactly as today. Hand each task to the pool as indexes into `pins.PINS` and a pin's mutants, and look the pin up in the worker: several pins' tests are closures or lambdas, which cannot be pickled.
2. **One run is the unit of work.** First every pin's twin runs, then every mutant of each pin whose twin passed. Each is its own task, with its own disposable copy, exactly as today. A pin whose twin fails still gets one `TWIN FAILED` row and no mutant runs, and a pin with a missing path still gets its `PENDING` rows without running.
3. **The results are put back in today's order.** That is the order of `pins.PINS`, and within a pin the order of its mutants, whatever order the runs finish in. The table, its counts line and the exit code are those of a sequential run.
4. **`run_pins(pin_list, root)` called as a function stays sequential.** `tests/test_pins.py` calls it with pins of its own. It gains a third argument, the number of workers, whose default is one. Only `main` passes more.
5. **Each worker has its own world.** The pool's initializer clears `pins.world`'s cache, so that each worker makes its own world, with its own key directory and its own `verified-signatures.json`. This holds whether or not the parent called `world()` before the fork. No two workers share that directory, and no worker reads a file that another rewrites.
6. **Nothing else.** No pin, twin, mutant, fixture or test changes, and no file but `pins/run.py`.

**Paths.**
- **May change:** `pins/run.py`.
- **May not change:** any other file.

**Size.** `main` has 8,245 counted lines against a cap of 8,400, and `pins/` is counted. This change adds at most 65 counted lines.

**Acceptance.**
- **(i) The same rows.** At the head, run `PINS_WORKERS=1 python3 pins/run.py` and then `python3 pins/run.py`, keeping both tables.
  - Strip each row's detail with `sed 's/  (.*$//'`, which removes everything from the two spaces before the detail's bracket. What is left of the two tables must be identical: compare them with `cmp`, and report the result. The detail is not compared, because it holds temporary paths that differ from run to run, sequential runs included.
  - Both must end with the last line of `origin/main`'s `python3 pins/run.py`, today `KILLED 158, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`.
- **(ii) The other statuses, through the pool.** Every row of (i) is `KILLED`, so it does not show the pool handling the rest. In a `python3` process at the head, make five pins of your own, as `tests/test_pins.py`'s `Runner` makes its own:
  - one whose mutant is killed;
  - one whose mutant survives;
  - one that is stale, because its mutant's `find` does not occur exactly once;
  - one that is pending, because its mutant's path does not exist;
  - one whose twin fails.

  Call `run_pins` on them twice, with one worker and with two. The two results must be equal, in order, in pin, mutant and status, and `exit_code` of each must be the same. Report both lists. Commit none of this.
- **(iii) The unit tests are unchanged.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(iv) Faster.** Report `nproc`, the number of workers the parallel run of (i) used, and both of (i)'s times. With at least two workers, the parallel run must take less time than the `PINS_WORKERS=1` run. If it does not, push the branch, do not propose, and report both times. Counsel measured about three fifths on two cores. That is a measurement on one machine, and it is not the bar.
- **(v) No shared key directory.** Show that the parallel workers' worlds differ, even when the parent made one first. In a `python3` process at the head, call `pins.world()`, then run the pool, as `main` does, with two workers on two pins that build padded fixtures, for example `charter_edit_unrecorded` and `amend_stale`. Have each worker print its process id and `os.path.dirname(pins.world().guy.path)`. You may do this by a print in the initializer behind an environment variable, or by a temporary line you remove before the commit. Report the lines: every worker's directory must differ from the parent's and from every other worker's.
