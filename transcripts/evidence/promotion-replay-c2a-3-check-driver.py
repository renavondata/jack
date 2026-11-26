import os
from pathlib import Path
Path('.replay/driver.pid').write_text(str(os.getpid()) + '\n')

import concurrent.futures
import hashlib
import json
import queue
import signal
import subprocess
import threading
import time
import traceback


BASE = Path('.replay')
VETO = '2026-11-22T11:44:05Z'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
START = float((BASE / 'start').read_text())
BEGUN = time.monotonic()
PLAN = json.loads((BASE / 'plan.json').read_text())
TABLE = json.loads(Path('spec/vectors/promotion-replay-c2a-3.json').read_text())['rows']
LOCK = threading.RLock()
STOP = threading.Event()
FINISHED = threading.Event()
DONE = []


class Cancelled(Exception):
    pass


def log(message):
    with LOCK:
        print(message, flush=True)


def cancelled():
    if STOP.is_set():
        raise Cancelled()


def end_group():
    os.killpg(os.getpgrp(), signal.SIGTERM)
    time.sleep(10)
    os.killpg(os.getpgrp(), signal.SIGKILL)


def stop_group(reason, detail=None):
    with LOCK:
        if STOP.is_set():
            return
        STOP.set()
        outcome = dict(reason=reason, done=len(DONE), wall_seconds=time.monotonic() - BEGUN,
                       minute=(time.time() - START) / 60, detail=detail)
        (BASE / 'outcome.json').write_text(json.dumps(outcome) + '\n')
        log(f'STOP {json.dumps(outcome)}')
        # Non-daemon: escalation must survive the worker pool finishing.
        threading.Thread(target=end_group, daemon=False).start()


def on_term(signum, frame):
    STOP.set()


def watchdog():
    if not FINISHED.wait(max(0, START + 110 * 60 - time.time())):
        stop_group('watchdog')


def lines_from(data):
    lines = data.decode('utf-8').split('\n')
    if lines[-1] == '':
        lines.pop()
    return lines


def mark(commit, R, V):
    rw = [i for i, line in enumerate(R) if line.startswith('window C2a:')]
    vw = [i for i, line in enumerate(V) if line.startswith('window C2a:')]
    if len(rw) != 1 or len(vw) != 1 or R[:rw[0]] != V[:vw[0]]:
        raise ValueError(json.dumps({'commit': commit, 'failed': 1, 'R': R, 'V': V}))
    if [s for s in R if s.startswith('sovereign REPAIR')] != [s for s in V if s.startswith('sovereign REPAIR')]:
        raise ValueError(json.dumps({'commit': commit, 'failed': 2, 'R': R, 'V': V}))
    forecast_indices = []
    j_indices = []
    for output, window in [(R, rw[0]), (V, vw[0])]:
        js = [i for i in range(window + 1, len(output)) if output[i].startswith('J7:')]
        fs = [i for i in range(window + 1, len(output)) if output[i].startswith('overdue forecast')]
        if len(js) != 1 or fs != list(range(js[0] + 1, js[0] + 1 + len(fs))):
            raise ValueError(json.dumps({'commit': commit, 'failed': 3, 'R': R, 'V': V}))
        forecast_indices.append(fs)
        j_indices.append(js[0])
    rf, vf = forecast_indices
    j = j_indices[1]
    return V[:j + 1] + [R[i] for i in rf] + V[j + 1 + len(vf):]


def evaluate(name, argv):
    cancelled()
    result = subprocess.run(['python3', '-I', str(BASE / name / 'judge' / 'status.py'), *argv],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=ENV)
    # A terminated run is never compared, marked, or recorded.
    cancelled()
    return result.returncode, lines_from(result.stdout)


def compute(k, task):
    begun = time.monotonic()
    kind, index, commit = task['kind'], task['index'], task['commit']
    root = BASE / f'w{k}'
    cancelled()
    subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', '-C', str(root),
                    'checkout', '-q', '--detach', commit], check=True, env=ENV)
    cancelled()
    evidence = BASE / 'ev' / f'{kind}-{index}'
    evidence.mkdir()
    logpath = root / 'log.jsonl'
    if not logpath.is_file():
        logpath = evidence / 'empty.jsonl'
        logpath.write_bytes(b'')
    if kind == 'table':
        stored = TABLE[index]
        run = stored['run']
        stored_argv = stored['argv']
        expected_exit = stored['exit']
        expected_lines = stored.get('marked', stored['stdout'])
    else:
        ledger = logpath.read_bytes().splitlines()
        if len(ledger) <= 7181:
            raise ValueError(f'Chain commit is not marked: {commit}, lines={len(ledger)}')
        as_of = json.loads(ledger[-1])['ts']
        run = {'path': '.github/workflows/tests.yml', 'event': 'push', 'head_branch': 'main',
               'head_sha': commit, 'conclusion': 'success', 'updated_at': json.loads(ledger[0])['ts']}
        stored_argv = ['--subject', 'C2a', '--as-of', as_of, '--log', '<log>', '--root', '<root>',
                       '--run', '<run>', '--runs', '<runs>', '--acts', '<acts>']
    runpath, runspath, actspath = [evidence / name for name in ('run.json', 'runs.json', 'acts.csv')]
    runpath.write_text(json.dumps(run), encoding='utf-8')
    runspath.write_text('[]\n', encoding='utf-8')
    actspath.write_text('repo,time_hkt,class,kind,ref,note\n', encoding='utf-8')
    replacements = {'<log>': logpath, '<root>': root, '<run>': runpath, '<runs>': runspath, '<acts>': actspath}
    argv = [str(replacements.get(arg, arg)) for arg in stored_argv]
    if kind == 'chain':
        expected_exit, R = evaluate('old', argv)
        veto_argv = list(argv)
        veto_argv[veto_argv.index('--as-of') + 1] = VETO
        second_exit, V = evaluate('old', veto_argv)
        cancelled()
        expected_lines = mark(commit, R, V)
        if second_exit != expected_exit:
            log(f'EXIT DIFFERENCE commit={commit} first={expected_exit} second={second_exit}')
    actual_exit, actual_lines = evaluate('new', argv)
    with LOCK:
        cancelled()
        if (actual_exit, actual_lines) != (expected_exit, expected_lines):
            failure = dict(task, expected_exit=expected_exit, expected_lines=expected_lines,
                           actual_exit=actual_exit, actual_lines=actual_lines)
            (BASE / 'fail.json').write_text(json.dumps(failure, ensure_ascii=False) + '\n', encoding='utf-8')
            stop_group('failure', task)
            return
        record = dict(task, exit=actual_exit,
                      lines=hashlib.sha256(''.join(s + '\n' for s in actual_lines).encode('utf-8')).hexdigest())
        target = BASE / 'rows' / f'{kind}-{index}.json'
        temporary = target.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(record) + '\n', encoding='utf-8')
        os.replace(temporary, target)
        DONE.append(task)
        seconds = time.monotonic() - begun
        total = len(PLAN['tasks'])
        minute = (time.time() - START) / 60
        log(f'ROW kind={kind} index={index} commit={commit} worker={k} seconds={seconds:.3f} done={len(DONE)}/{total} minute={minute:.3f}')


def worker(k, jobs):
    while not STOP.is_set():
        try:
            task = jobs.get_nowait()
        except queue.Empty:
            return
        try:
            compute(k, task)
        except Cancelled:
            return
        except BaseException:
            if not STOP.is_set():
                stop_group('error', dict(task, traceback=traceback.format_exc()))
            return


def main():
    signal.signal(signal.SIGTERM, on_term)
    total = len(PLAN['tasks'])
    log(f'START pid={os.getpid()} tasks={total} workers=10 minute={(time.time() - START) / 60:.3f}')
    threading.Thread(target=watchdog, daemon=True).start()
    jobs = queue.Queue()
    for task in PLAN['tasks']:
        jobs.put(task)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(worker, k, jobs) for k in range(10)]
        for future in futures:
            future.result()
    if STOP.is_set():
        return
    assert len(DONE) == total
    FINISHED.set()
    outcome = dict(reason='complete', done=len(DONE), wall_seconds=time.monotonic() - BEGUN,
                   minute=(time.time() - START) / 60)
    (BASE / 'outcome.json').write_text(json.dumps(outcome) + '\n')
    log(f'COMPLETE {json.dumps(outcome)}')


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        stop_group('error', traceback.format_exc())
