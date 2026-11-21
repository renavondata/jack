#!/usr/bin/env python3
'''Compute the unmarked promotion replay, with eight latest-first workers.

Invocation from the repository root, after fixing .replay/T and making detached
checkouts .replay/frozen and .replay/w0 through .replay/w7:
    python3 .replay/driver.py
The caller starts this once under nohup setsid. No child creates a process group.
Only atomically renamed rows count as completed. This file never resumes a run.
'''

import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import queue
import subprocess
import time
import traceback


BASE = Path(__file__).resolve().parents[1]
REPLAY = BASE / '.replay'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=BASE, env=ENV)


def compute(index, commit, worker):
    root = REPLAY / ('w' + str(worker))
    subprocess.run(
        ['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf',
         '-C', str(root), 'checkout', '-q', '--detach', commit],
        cwd=BASE, env=ENV, check=True,
    )
    evidence = REPLAY / 'ev' / str(index)
    evidence.mkdir()
    log = root / 'log.jsonl'
    holds_log = log.is_file()
    if holds_log:
        entries = log.read_bytes().splitlines()
        as_of = json.loads(entries[-1])['ts']
        updated_at = json.loads(entries[0])['ts']
    else:
        utc_env = dict(ENV, TZ='UTC')
        as_of = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd',
             '--date=format-local:%Y-%m-%dT%H:%M:%SZ', commit],
            cwd=BASE, env=utc_env,
        ).decode('utf-8').strip()
        updated_at = as_of
        log = evidence / 'empty.jsonl'
        log.write_bytes(b'')
    run = {
        'path': '.github/workflows/tests.yml',
        'event': 'push',
        'head_branch': 'main',
        'head_sha': commit,
        'conclusion': 'success',
        'updated_at': updated_at,
    }
    run_path = evidence / 'run.json'
    runs_path = evidence / 'runs.json'
    acts_path = evidence / 'acts.csv'
    run_path.write_text(json.dumps(run), encoding='utf-8')
    runs_path.write_bytes(b'[]\n')
    acts_path.write_bytes(b'repo,time_hkt,class,kind,ref,note\n')
    argv = ['--subject', 'C2a', '--as-of', as_of,
            '--log', '<log>', '--root', '<root>', '--run', '<run>',
            '--runs', '<runs>', '--acts', '<acts>']
    replacements = {
        '<log>': str(log), '<root>': str(root), '<run>': str(run_path),
        '<runs>': str(runs_path), '<acts>': str(acts_path),
    }
    result = subprocess.run(
        ['python3', '-I', '.replay/frozen/tools/status.py',
         *[replacements.get(arg, arg) for arg in argv]],
        cwd=BASE, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    lines = result.stdout.decode('utf-8').split('\n')
    if lines[-1] == '':
        lines.pop()
    return {'commit': commit, 'log': holds_log, 'argv': argv, 'run': run,
            'exit': result.returncode, 'stdout': lines}


def main():
    (REPLAY / 'driver.pid').write_text(str(os.getpid()) + '\n')
    started = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (REPLAY / 'started.json').write_text(json.dumps({'utc': stamp}))
    commits = git('rev-list', '--first-parent', '--reverse',
                  (REPLAY / 'T').read_text().strip()).decode().splitlines()
    if any((REPLAY / 'rows').iterdir()):
        raise RuntimeError('rows directory must start empty')
    work = queue.Queue()
    for index in reversed(range(len(commits))):
        work.put((index, commits[index]))
    print('started', stamp, 'rows', len(commits), 'workers', 8, flush=True)

    def worker(number):
        while True:
            try:
                index, commit = work.get_nowait()
            except queue.Empty:
                return
            row_started = time.monotonic()
            row = compute(index, commit, number)
            target = REPLAY / 'rows' / (str(index) + '.json')
            temporary = target.with_suffix('.json.tmp')
            temporary.write_text(json.dumps(row, ensure_ascii=False) + '\n',
                                 encoding='utf-8')
            os.replace(temporary, target)
            print('row', index, commit, 'worker', number,
                  'seconds', round(time.monotonic() - row_started, 3),
                  'elapsed', round(time.monotonic() - started, 3), flush=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(worker, number) for number in range(8)]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    elapsed = time.monotonic() - started
    (REPLAY / 'finished.json').write_text(
        json.dumps({'rows': len(commits), 'wall_seconds': elapsed}) + '\n')
    print('complete', len(commits), 'wall_seconds', elapsed, flush=True)


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        traceback.print_exc()
        os._exit(1)
