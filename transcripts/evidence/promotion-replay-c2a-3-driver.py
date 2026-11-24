import concurrent.futures
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading
import time
import traceback


BASE = Path('.replay')
VETO = '2026-11-22T11:44:05Z'
FIRST_MARKED = 'bbfd0edf71df6dfe2183bfbbf24a372dd871146e'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
COMMITS = json.loads((BASE / 'commits.json').read_text())
START = float((BASE / 'start').read_text())
LOCK = threading.Lock()
DONE = []
EXIT_DIFFERENCES = []
FINISHED = threading.Event()


def log(message):
    with LOCK:
        print(message, flush=True)


def stop_group(reason):
    log(reason)
    # All workers and evaluator subprocesses inherit this session's group.
    # Escalate after ten seconds, including subprocesses that ignore TERM.
    group = os.getpgrp()
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    os.killpg(group, signal.SIGTERM)
    time.sleep(10)
    os.killpg(group, signal.SIGKILL)


def watchdog():
    delay = max(0, START + 115 * 60 - time.time())
    if not FINISHED.wait(delay):
        with LOCK:
            count = len(DONE)
        stop_group(f'STOP minute 115: {count}/{len(COMMITS)} rows complete')


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


def compute(k, index):
    begun = time.monotonic()
    commit = COMMITS[index]
    root = BASE / f'w{k}'
    subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
                    '-C', str(root), 'checkout', '-q', '--detach', commit],
                   check=True, env=ENV)
    evidence = BASE / 'ev' / str(index)
    evidence.mkdir()
    logpath = root / 'log.jsonl'
    has_log = logpath.is_file()
    if has_log:
        ledger = logpath.read_bytes().splitlines()
        as_of = json.loads(ledger[-1])['ts']
        updated = json.loads(ledger[0])['ts']
        marked = len(ledger) > 7181
    else:
        date_env = dict(ENV, TZ='UTC')
        as_of = subprocess.check_output([
            'git', 'log', '-1', '--format=%cd',
            '--date=format-local:%Y-%m-%dT%H:%M:%SZ', commit], env=date_env).decode().strip()
        updated = as_of
        logpath = evidence / 'empty.jsonl'
        logpath.write_bytes(b'')
        marked = False
    expected_marked = index >= COMMITS.index(FIRST_MARKED)
    if marked != expected_marked:
        raise ValueError(f'Marked set failed at {commit}: marked={marked}')
    run = {
        'path': '.github/workflows/tests.yml',
        'event': 'push',
        'head_branch': 'main',
        'head_sha': commit,
        'conclusion': 'success',
        'updated_at': updated,
    }
    runpath = evidence / 'run.json'
    runpath.write_text(json.dumps(run), encoding='utf-8')
    runspath = evidence / 'runs.json'
    runspath.write_text('[]\n', encoding='utf-8')
    actspath = evidence / 'acts.csv'
    actspath.write_text('repo,time_hkt,class,kind,ref,note\n', encoding='utf-8')
    argv = ['--subject', 'C2a', '--as-of', as_of, '--log', str(logpath),
            '--root', str(root), '--run', str(runpath), '--runs', str(runspath),
            '--acts', str(actspath)]
    cmd = ['python3', '-I', str(BASE / 'frozen' / 'judge' / 'status.py')]
    result = subprocess.run(cmd + argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=ENV)
    output = lines_from(result.stdout)
    stored_argv = ['--subject', 'C2a', '--as-of', as_of, '--log', '<log>',
                   '--root', '<root>', '--run', '<run>', '--runs', '<runs>', '--acts', '<acts>']
    row = {'commit': commit, 'log': has_log, 'argv': stored_argv,
           'run': run, 'exit': result.returncode, 'stdout': output}
    if marked:
        veto_argv = list(argv)
        veto_argv[3] = VETO
        second = subprocess.run(cmd + veto_argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=ENV)
        V = lines_from(second.stdout)
        row['marked'] = mark(commit, output, V)
        if second.returncode != result.returncode:
            with LOCK:
                EXIT_DIFFERENCES.append({'commit': commit, 'exit': result.returncode, 'second_exit': second.returncode})
            log(f'EXIT DIFFERENCE {commit}: {result.returncode} vs {second.returncode}')
    target = BASE / 'rows' / f'{index}.json'
    temporary = BASE / 'rows' / f'{index}.json.tmp'
    temporary.write_text(json.dumps(row, ensure_ascii=False) + '\n', encoding='utf-8')
    os.replace(temporary, target)
    seconds = time.monotonic() - begun
    with LOCK:
        DONE.append(index)
        count = len(DONE)
        print(f'ROW index={index} commit={commit} worker={k} seconds={seconds:.3f} marked={marked} done={count}/{len(COMMITS)} minute={(time.time() - START) / 60:.3f}', flush=True)
    return seconds


def worker(k, jobs):
    while True:
        try:
            index = jobs.get_nowait()
        except queue.Empty:
            return
        try:
            compute(k, index)
        except BaseException:
            stop_group(f'STOP worker={k} index={index}\n{traceback.format_exc()}')


def main():
    (BASE / 'driver.pid').write_text(str(os.getpid()) + '\n')
    begun = time.monotonic()
    log(f'START pid={os.getpid()} rows={len(COMMITS)} workers=10 T={COMMITS[-1]} minute={(time.time() - START) / 60:.3f}')
    threading.Thread(target=watchdog, daemon=True).start()
    jobs = queue.Queue()
    for index in reversed(range(len(COMMITS))):
        jobs.put(index)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(worker, k, jobs) for k in range(10)]
        for future in futures:
            future.result()
    assert len(DONE) == len(COMMITS)
    (BASE / 'exit-differences.json').write_text(json.dumps(EXIT_DIFFERENCES) + '\n')
    FINISHED.set()
    log(f'COMPLETE rows={len(DONE)} wall_seconds={time.monotonic() - begun:.3f} minute={(time.time() - START) / 60:.3f} exit_differences={json.dumps(EXIT_DIFFERENCES)}')


if __name__ == '__main__':
    main()
