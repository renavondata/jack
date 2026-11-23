# FIX-20261124-pins-worker: a pins run ends when one of its workers dies

Counsel's text, 24 November 2026, for the sovereign's read (CHARTER A2.10). The reviewer makes it under `transcripts/sessions/fix-reviewer.md`, on branch `FIX-20261124-pins-worker`, and proposes it. It changes what `pins/run.py` does when a worker process of its pool ends without returning. It changes no pin, twin or mutant, and no row of the table a healthy run prints.

**Why.**
- **Since 23 November the pins run in a pool of worker processes** (`transcripts/FIX-20261123-pins-parallel.md`; proposal #1365, seqs 7344 and 7345). `parallel_pins` hands the pool its tasks by `pool.map`, at lines 84 and 86 of `pins/run.py`, and waits for every result with no bound.
- **If a worker is killed from outside, the run waits for ever.** `multiprocessing.Pool` starts another worker in its place, and the result of the task the dead one held never comes. The adviser tried it (ADVISER.md entry 201): a pool of two in which one task calls `os._exit(9)` was still waiting after 20 s, when `timeout` ended it.
- **Nothing bounds that wait where the court runs the pins unattended.** `.github/workflows/tests.yml` sets no `timeout-minutes`, and `tools/jack`'s wait for a proposal's checks has no deadline (line 154). So one worker killed on the hosted runner, by the kernel for want of memory for example, would hold that proposal's `tests` until GitHub's own limit, and the herald's merge with it.
- **It has not happened.** The fault is one day old and needs a killed worker. This text is here so that it cannot hold the lane when it does.
- **Python's other pool ends such a run at once.** `concurrent.futures.ProcessPoolExecutor` marks the pool broken when a worker ends abruptly, and every task without a result then raises `BrokenProcessPool`. Counsel's prototype, which is not proposed, gave a pool of three twelve tasks of which the sixth calls `os._exit(9)`: it returned in 0.3 s with three results and nine tasks named as not returned.

**The change.**
1. **`parallel_pins` uses `concurrent.futures.ProcessPoolExecutor`** in place of `multiprocessing.Pool`. The workers are started by `fork`, as now, and the pool's initializer is `init_worker` with the arguments it has now.
2. **Each run is handed to the pool as its own task,** in the order `pool.map` gives them now: first every twin, then every mutant of each pin whose twin passed. The results are put back in today's order. A healthy run prints the table, the counts line and the exit code that it prints today.
3. **When the pool breaks, the run ends.** `parallel_pins` catches `BrokenProcessPool` and raises an error of its own whose message says:
   - that a worker ended without returning;
   - how many tasks had not returned;
   - the earliest of them in the order they were handed over, up to twice the number of workers, each as its pin's name and its mutant's name, or `twin`.

   The pool cannot say which of its running tasks died with the worker. It takes its tasks in the order they were handed over, so the tasks it was running are among the earliest not returned. Naming twice the number of workers allows for results that were on their way back when the pool broke.
4. **`main` prints that message to standard error and returns 1.** It prints no table for such a run. A run that lost a worker is not a run of the pins, and nothing reads its rows.
5. **Nothing else.** With one worker the pins run exactly as today, in the parent process, and no pool is made. `run_pins` keeps its three arguments. No pin, twin, mutant, fixture or test changes, and no file but `pins/run.py`.

**Paths.**
- **May change:** `pins/run.py`.
- **May not change:** any other file.

**Size.** `main` has 8,340 counted lines against a cap of 8,400, and `pins/` is counted. This change adds at most 20 counted lines. Every line of a Python file counts, blank lines and comments included.

**Acceptance.**
- **(i) The same rows.** At the head, run `PINS_WORKERS=1 python3 pins/run.py` and then `python3 pins/run.py`, keeping both tables.
  - Cut each row's detail at its first colon with `sed -E 's/  \(([^:]*).*$/  (\1/'`, as `transcripts/FIX-20261123-pins-parallel.md` does and for its reason. What is left of the two tables must be identical: compare them with `cmp`, and report the result.
  - Both must end with the last line of `origin/main`'s `python3 pins/run.py`.
- **(ii) A lost worker ends the run.** In a `python3` process at the head, make four pins of your own, as `tests/test_pins.py`'s `Runner` makes its own. Three have a test that passes and one mutant that is killed. The test of the fourth calls `os._exit(9)`. Call `run_pins` on the four with two workers, under `timeout 60`. Do it twice, with the fourth pin last in the list and then first.
  - Each call must raise the error of point 3 within the 60 seconds.
  - Its message must name the fourth pin's twin among the tasks not returned.
  - Report both messages and how long each call took. Commit none of this.
- **(iii) `main` reports it.** With a temporary line that you remove before the commit, or by a small script that imports `pins/run.py` and replaces its pin list, run `main` over the four pins of (ii) with `PINS_WORKERS=2`. It must print the message to standard error, print no table and return 1. Report what it printed.
- **(iv) The other statuses still come through the pool.** Repeat acceptance (ii) of `transcripts/FIX-20261123-pins-parallel.md` at the head: five pins of your own, one for each status, with one worker and with two. The two results must be equal, in order, in pin, mutant and status. Report both lists.
- **(v) The unit tests are unchanged.** `python3 -m unittest discover -s tests -t .` passes at the head with the same `Ran N tests` as on `origin/main`.
- **(vi) No slower.** Report the times of (i)'s parallel run at the head and of `python3 pins/run.py` on `origin/main`, on the same machine with the same number of workers. If the head's run takes more than a quarter longer, push the branch, do not propose, and report both times.

**What this text does not do.**
- It sets no limit on how long one pin may run. A worker that hangs, and does not die, still holds the run. That is a different fault, with a different remedy.
- It does not retry the lost task. A run that lost a worker is run again whole, by whoever started it.
- It does not give `tests.yml` a `timeout-minutes`. The workflow is trusted base and changes only by his push.

**Interests.** Counsel wrote the text that put the pins in a pool, and its read by the adviser missed this fault, as the adviser's entry 201 says. Counsel's proposals wait on the same `tests` job as every other party's.
