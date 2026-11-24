# Adviser probe for ADVISER.md entry 254: what concurrent.futures.ProcessPoolExecutor does when a worker dies.
# Run: timeout 30 python3 -I P254-pool.py A   (and B, and C; C is expected to be ended by the timeout, exit 124)
import concurrent.futures as cf, multiprocessing as mp, os, signal, sys, time
from concurrent.futures.process import BrokenProcessPool
ctx = mp.get_context("fork")
def pid(_): return os.getpid()
def quick(i): return i
def slow_ignore(_):
    signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(300)
def die(_):
    time.sleep(0.3); os._exit(9)

def A():  # idle death, tasks still to come
    ex = cf.ProcessPoolExecutor(2, mp_context=ctx)
    fs = [ex.submit(quick, i) for i in range(2)]; [f.result() for f in fs]
    os.kill(next(iter(ex._processes)), signal.SIGKILL)
    t = time.monotonic()
    while not ex._broken and time.monotonic() - t < 10: time.sleep(0.01)
    try:
        f = ex.submit(quick, 2); f.result(); print("A: no break seen")
    except BrokenProcessPool as e: print("A: BrokenProcessPool at submit, _broken after %.2fs" % (time.monotonic() - t))
    ex.shutdown(); print("A: shutdown returned")
def B():  # idle death after the last result
    ex = cf.ProcessPoolExecutor(2, mp_context=ctx)
    fs = [ex.submit(quick, i) for i in range(4)]; cf.wait(fs)
    os.kill(next(iter(ex._processes)), signal.SIGKILL); time.sleep(0.5)
    print("B: results still read:", [f.result() for f in fs], "broken:", bool(ex._broken))
    ex.shutdown(); print("B: shutdown returned")
def C():  # one dies, one ignores SIGTERM
    ex = cf.ProcessPoolExecutor(2, mp_context=ctx)
    f1 = ex.submit(slow_ignore, 0); f2 = ex.submit(die, 1); t = time.monotonic()
    for f in (f1, f2):
        try: f.result(timeout=20)
        except BrokenProcessPool: print("C: future broken after %.1fs" % (time.monotonic() - t))
    sys.stdout.flush(); ex.shutdown(); print("C: shutdown returned")
{"A": A, "B": B, "C": C}[sys.argv[1]]()
