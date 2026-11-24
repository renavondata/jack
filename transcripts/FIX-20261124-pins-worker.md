# FIX-20261124-pins-worker: a pins run ends when one of its workers dies

Counsel's text, 24 November 2026, for the sovereign's read (CHARTER A2.10). The reviewer makes it under `transcripts/sessions/fix-reviewer.md`, on branch `FIX-20261124-pins-worker`, and proposes it. It changes what `pins/run.py` does when a worker process of its pool ends without returning, and when a pin's test raises `SystemExit`. It changes no pin, twin or mutant, and no row of the table a healthy run prints.

**Why.**
- **Since 23 November the pins run in a pool of worker processes** (`transcripts/FIX-20261123-pins-parallel.md`; proposal #1365, seqs 7344 and 7345). `parallel_pins` hands the pool its tasks by `pool.map`, at lines 84 and 86 of `pins/run.py`, and waits for every result with no bound.
- **If a worker ends without returning, the run waits for ever.** `multiprocessing.Pool` starts another worker in its place, and the result of the task the dead one held never comes. It does not matter how the worker ended.
  - Killed from outside: the adviser tried it (ADVISER.md entry 201). A pool of two in which one task calls `os._exit(9)` was still waiting after 20 s, when `timeout` ended it.
  - By an exit of its own: counsel's pre-read gave the runner on `main` a pin whose test calls `sys.exit(0)` when it meets its mutant, with two workers. It was still waiting after 20 s.
- **No bound of the court's own ends that wait.**
  - `.github/workflows/tests.yml` sets no `timeout-minutes`, so the `pins` job would run to GitHub's own limit for a job.
  - `tools/jack`'s check waits for its three commands with no timeout (lines 97 to 108). It runs in every session's `jack proposal`.
  - The merge verb's wait for a proposal's checks has no deadline (`tools/jack`, line 154). The herald's job ends it after 60 minutes.
- **A test that exits is a second fault, in the parent.** `run_test` catches `Exception` (line 50), and `SystemExit` is not one. With one worker, a pin's test that calls `sys.exit(0)` ends the whole run with status 0 and no table, and the check reads that as a pass.
- **No pin does either today.** `sys.exit`, `SystemExit` and `os._exit` occur in `pins/` and `harness/` only in the two `__main__` guards. This text is here so that neither fault can hold the lane, or pass for a run, when it comes.
- **Python's other pool ends a run with a dead worker at once.** `concurrent.futures.ProcessPoolExecutor` marks the pool broken when a worker ends abruptly, and every task without a result then raises `BrokenProcessPool`. Two trials of counsel's, neither proposed:
  - a pool of three with twelve tasks, of which the sixth calls `os._exit(9)`, returned in 0.3 s with three results and nine tasks not returned;
  - the pre-read's prototype of this change printed, on a full run, a table identical to `main`'s after the cut of acceptance (i). In 1,500 trials with a task dying at random, the dead task was always among the first not returned, as many as there are workers.

**When it may be made.** Before C2a-3 opens or after it has ended, and never while it is open. `transcripts/BRIEF-C2a-3-draft.md` on `main` refuses, inside its window, any code but its own: "no code but §The code". Before anything else, read `main`'s log.
- C2a-3 opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z. If the log holds none, go on.
- If it holds one, C2a-3 has ended when the log holds, after that entry, a `decision` of kind `promote` with subject `C2a`, or a `decision` of kind `veto` with subject `C2a` or `C2a-3`; or when the instant now is after the `resolves_by` of the forecast whose `args.id` is `V8`. If C2a-3 has not ended, stop, report that the window is open, and change nothing.

**The change.**
1. **`parallel_pins` uses `concurrent.futures.ProcessPoolExecutor`** in place of `multiprocessing.Pool`. The workers are started by `fork`, as now, and the pool's initializer is `init_worker` with the arguments it has now.
2. **Each run is handed to the pool as its own task,** in the order `pool.map` gives them now: first every twin, then every mutant of each pin whose twin passed. The results are put back in today's order. A healthy run prints the table, the counts line and the exit code that it prints today.
3. **`run_test` catches `SystemExit` as it catches `Exception`.** Under a mutant it is a kill, and on the twin it is a failed twin, with the detail it gives any other exception. This holds in a worker and in the parent alike. `KeyboardInterrupt` is left as it is.
4. **When the pool breaks, the run ends.** `parallel_pins` raises an exception of a class of its own, `WorkerLost`, defined in `pins/run.py`. It does so whether the break shows when a task is handed to the pool or when a result is asked of it. Its message says:
   - that a worker ended without returning;
   - how many tasks of the phase in hand, twins or mutants, have no result, those not yet handed over included;
   - the earliest of them in the order of hand-over, up to twice the number of workers, each as its pin's name and its mutant's name, or `twin`.

   The pool cannot say which of its running tasks died with the worker. It takes its tasks in the order they were handed over, so the tasks it was running are among the earliest without a result. Naming twice the number of workers allows for results that were on their way back when the pool broke.
5. **`main` catches `WorkerLost`, prints its message to standard error and returns 1.** It prints no table for such a run. A run that lost a worker is not a run of the pins, and nothing reads its rows. What reads the run is its exit status: the check of `tools/jack` refuses on it, and the `pins` job of `.github/workflows/tests.yml` fails on it, which the `tests` job of that workflow reads (lines 58 to 68).
6. **Nothing else.** With one worker the pins run in the parent process and no pool is made, as today. `run_pins` keeps its three arguments. No pin, twin, mutant, fixture or test changes, and no file but `pins/run.py`.

**What this text does not do.**
- It sets no limit on how long one pin may run. A worker that hangs, and does not die, still holds the run. That is a different fault, with a different remedy.
- It does not retry the lost task. A run that lost a worker is run again whole, by whoever started it.
- It does not give `tests.yml` a `timeout-minutes`. The workflow is trusted base and changes only by his push.
- It ends the run on any worker's death, an idle worker's included. Today's pool replaces an idle worker and goes on.
- It does not clean up after a broken run. The pool ends the surviving workers, and their disposable copies of the tree can be left in the temporary directory. The check of `tools/jack` removes its own temporary directory, and the hosted runner's machine is discarded after the job.
- **Its pin is owed, and comes later.** LAW.md says that every change to `pins/` carries a pin in `pins/pins.py` (lines 61 to 64), and the cap leaves no room for one now (**Size**). The pin is `pins_worker_lost`, the reviewer's, with the mutants `broken_pool_unreported` and `exit_uncaught`. `transcripts/FIX-20261124-fix-pins.md` specifies it, and it is made after C2a-3 has ended, under the cap that its opening push sets. Until then what holds the change is the acceptance below, run in the reviewer's session and reported by it. His grant of this text is his word on that interval.

**Paths.**
- **May change:** `pins/run.py`.
- **May not change:** any other file.

**Size.** `main` has 8,340 counted lines against a cap of 8,400, and `pins/` is counted. This change adds at most 30 counted lines. Every line of a Python file counts, blank lines and comments included. `transcripts/FIX-20261124-merge-closed.md` adds at most 18, so the two together take at most 48 of the 60 lines left.

**Acceptance.** The pins you make for these items are your own, made as `toy_pin` in `tests/test_pins.py` (line 13) makes one. Commit none of them.
- **(i) The same rows.** At the head, run `PINS_WORKERS=1 python3 pins/run.py` and then `PINS_WORKERS=2 python3 pins/run.py`, keeping both tables. Report `nproc`.
  - Cut each row's detail at its first colon with `sed -E 's/  \(([^:]*).*$/  (\1/'`, as `transcripts/FIX-20261123-pins-parallel.md` does and for its reason. What is left of the two tables must be identical: compare them with `cmp`, and report the result.
  - Both must end with the last line of `origin/main`'s `python3 pins/run.py`.
- **(ii) A lost worker ends the run.** Make nine pins: eight whose test passes and whose one mutant is killed, and a ninth, the dying pin. Call `run_pins` on the nine with two workers, under `timeout 60`, three times:
  - (a) the dying pin's test calls `os._exit(9)` whenever it runs, and the pin is last in the list;
  - (b) the same pin, first in the list;
  - (c) the dying pin's test passes on the tree as it is and calls `os._exit(9)` when its mutant has been applied, and the pin is fifth in the list.

  Each call must raise `WorkerLost` within the 60 seconds. For each message:
  - it names the dying pin's task: with `twin` in (a) and (b), and with its mutant's name in (c);
  - it names at most four tasks;
  - the number it gives is at least the number of tasks it names, and at most nine.

  Report the three messages and how long each call took.
- **(iii) A pool that breaks during hand-over.** Make 300 pins of the passing kind and put the dying pin of (ii)(a) first. Call `run_pins` with two workers under `timeout 60`. It must raise `WorkerLost`, and no other exception. Report the message.
- **(iv) A test that exits.** Make three pins: one whose test calls `sys.exit(0)` when its mutant has been applied and passes otherwise; one whose test calls `sys.exit(0)` whenever it runs; one of the passing kind. Call `run_pins` on them with one worker and with two, each under `timeout 60`. Both calls must return. Their results must be equal, in order: `KILLED` for the first pin's mutant, `TWIN FAILED` for the second pin, `KILLED` for the third pin's mutant. `exit_code` of each must be 1. Report both lists.
- **(v) `main` reports a lost worker.** With a temporary line that you remove before the commit, or by a small script that imports `pins/run.py` and replaces its pin list, run `main` over the nine pins of (ii)(a) with `PINS_WORKERS=2`. It must print the message to standard error, print no table and return 1. Report what it printed.
- **(vi) The other statuses still come through the pool.** Repeat acceptance (ii) of `transcripts/FIX-20261123-pins-parallel.md` at the head: five pins, one for each status, with one worker and with two. The two results must be equal, in order, in pin, mutant and status. Report both lists.
- **(vii) Each worker still has its own world.** Repeat acceptance (v) of `transcripts/FIX-20261123-pins-parallel.md` at the head, and report the lines.
- **(viii) The unit tests are unchanged.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(ix) The times.** Report the time of (i)'s run with two workers at the head, and of `PINS_WORKERS=2 python3 pins/run.py` on `origin/main`, on the same machine. This item sets no bar: one pair of timings on a shared machine decides nothing.

**Interests.** Counsel wrote the text that put the pins in a pool, and its read by the adviser missed the first fault, as the adviser's entry 201 says. Counsel's own pre-read found the second. Counsel's proposals wait on the same `tests` job as every other party's.
