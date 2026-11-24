# Adviser probe for ADVISER.md entry 257: acceptance (iii) of FIX-20261124-pins-worker.md at bc158dac, run against the prototype
# of runner #1277 (the part of P257-argon3.py above its cases). Run as P257-argon3.py is run.
import os, sys
sys.path.insert(0, os.getcwd())
import concurrent.futures, multiprocessing, os, signal, sys, time, unittest.mock
from concurrent.futures.process import BrokenProcessPool
from pins import pins, run

class WorkerLost(Exception):
    pass

def parallel_pins_new(pin_list, root, workers):
    active = [i for i, p in enumerate(pin_list)
              if all(os.path.exists(os.path.join(root, m.path)) for m in p.mutants)]
    def phase(pool, tasks):
        futures, out = {}, {}
        def call(fn, *a):
            try:
                return True, fn(*a)
            except BrokenProcessPool:
                return False, None
        for t in tasks:
            ok, f = call(pool.submit, run.run_task, t)
            if not ok:
                break
            futures[t] = f
        for t, f in futures.items():
            ok, res = call(f.result)
            if ok:
                out[t] = res
        if len(out) != len(tasks):
            lost = [pin_list[i].name + "/" + ("twin" if j is None else pin_list[i].mutants[j].name)
                    for i, j in tasks if (i, j) not in out]
            raise WorkerLost(f"a worker ended without returning; {len(lost)} tasks have no result: " + ", ".join(lost[:2 * workers]))
        return out
    with concurrent.futures.ProcessPoolExecutor(workers, mp_context=multiprocessing.get_context("fork"),
                                                initializer=run.init_worker, initargs=(pin_list, root)) as pool:
        twins = {i: r for (i, _), r in phase(pool, [(i, None) for i in active]).items()}
        tasks = [(i, j) for i in active if twins[i][0] for j in range(len(pin_list[i].mutants))]
        mutants = phase(pool, tasks)
    results = []
    for i, pin in enumerate(pin_list):
        if i not in twins:
            results += [run.Result(pin.name, m.name, "PENDING", f"{m.path} does not exist yet") for m in pin.mutants]
        elif not twins[i][0]:
            results.append(run.Result(pin.name, "twin", "TWIN FAILED", twins[i][1]))
        else:
            results.extend(mutants[i, j] for j in range(len(pin.mutants)))
    return results

run.parallel_pins = parallel_pins_new
run.WorkerLost = WorkerLost

def make_pin(name, fn):
    return pins.Pin(name, fn, [pins.Mutant("m", "kernel/log.py", "def canonical(obj):", "def canonical(obj):  # mutated")])

def pass_kill(root):
    with open(os.path.join(root, "kernel/log.py")) as f:
        assert "# mutated" not in f.read()

eight = [make_pin(f"p{k}", pass_kill) for k in range(8)]


# acceptance (iii), as the text at bc158dac has it: a real break at the third hand-over
real = concurrent.futures.ProcessPoolExecutor.submit
kept = []
def submit(self, *a, **k):
    if len(kept) == 2:
        concurrent.futures.wait(kept)
        os.kill(next(iter(self._processes)), signal.SIGKILL)
        t = time.monotonic()
        while not self._broken and time.monotonic() - t < 10: time.sleep(0.005)
    f = real(self, *a, **k); kept.append(f); return f
nine = [make_pin(f"q{k}", pass_kill) for k in range(9)]
t0 = time.monotonic()
with unittest.mock.patch.object(concurrent.futures.ProcessPoolExecutor, "submit", submit):
    try:
        run.run_pins(nine, run.ROOT, 2); print("(iii): no exception")
    except WorkerLost as e:
        print(f"(iii) ({time.monotonic()-t0:.2f}s):", e)
    except BaseException as e:
        print("(iii): other exception", type(e).__name__, e)
