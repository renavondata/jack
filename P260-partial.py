# Adviser probe for ADVISER.md entry 260: a ProcessPoolExecutor worker that dies while it sends its result back.
# Run: python3 -I P260-partial.py <delay in seconds of the manager's wait> <characters in the result>
import concurrent.futures as cf, concurrent.futures.process as cfp, multiprocessing as mp, os, signal, sys, threading, time
delay, size = float(sys.argv[1]), int(sys.argv[2])
def task(n):
    threading.Thread(target=lambda: (time.sleep(0.1), os._exit(9)), daemon=True).start()
    return (False, "x" * n)
def idle(_):
    time.sleep(60)
real_wait = mp.connection.wait
def slow_wait(*a, **k):
    time.sleep(delay)
    return real_wait(*a, **k)
if delay: cfp.mp.connection.wait = slow_wait
ex = cf.ProcessPoolExecutor(2, mp_context=mp.get_context("fork"))
f1 = ex.submit(task, size); f2 = ex.submit(idle, 0)
time.sleep(3)
procs = list(ex._processes.values())
print("Python %s delay %.1f size %d; at 3 s: manager alive %s, broken %s, futures done %s, worker exitcodes %s" % (
    sys.version.split()[0], delay, size, ex._executor_manager_thread.is_alive(), bool(ex._broken),
    [f1.done(), f2.done()], [p.exitcode for p in procs]))
sys.stdout.flush()
for p in procs:
    if p.exitcode is None: os.kill(p.pid, signal.SIGKILL)
os._exit(0)
