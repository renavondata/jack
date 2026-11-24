# Adviser copy for ADVISER.md entry 257: the prototype that the reader session of runner #1277 wrote (its report, lines 732 to 829),
# with these three comment lines and the two lines that put the working directory on the path. Not the adviser's code and not the court's.
# Run in a clean worktree of main: TMPDIR=<a directory outside the tree> python3 <path>/P257-argon3.py
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

# (ii)(a)
dying_always = make_pin("dying", lambda root: os._exit(9))
try:
    run.run_pins(eight + [dying_always], run.ROOT, 2)
except WorkerLost as e:
    print("(ii)(a):", e)

# (ii)(b)
try:
    run.run_pins([dying_always] + eight, run.ROOT, 2)
except WorkerLost as e:
    print("(ii)(b):", e)

# (ii)(c)
def die_on_mutant(root):
    with open(os.path.join(root, "kernel/log.py")) as f:
        if "# mutated" in f.read():
            os._exit(9)
dying_mut = make_pin("dying", die_on_mutant)
try:
    run.run_pins(eight[:4] + [dying_mut] + eight[4:], run.ROOT, 2)
except WorkerLost as e:
    print("(ii)(c):", e)

# (ii)(d)
flag = os.path.join(os.environ["TMPDIR"], "flag_d")
if os.path.exists(flag): os.remove(flag)
def slow_first(root):
    while not os.path.exists(flag):
        time.sleep(0.01)
    time.sleep(5)
def die_write(root):
    open(flag, "w").close()
    os._exit(9)
try:
    t0 = time.monotonic()
    run.run_pins([make_pin("p0", slow_first)] + eight[1:] + [make_pin("dying", die_write)], run.ROOT, 2)
except WorkerLost as e:
    print(f"(ii)(d) ({time.monotonic()-t0:.2f}s):", e)
if os.path.exists(flag): os.remove(flag)
