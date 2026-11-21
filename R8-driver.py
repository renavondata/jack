#!/usr/bin/env python3
"""Adviser's own driver for R8: recompute the promotion replay table from the 6fc0a5f9 paragraph.

usage: drv.py setup T NWORKERS | drv.py work K NWORKERS | drv.py compare
Rows go to rows/<index>.json (written to .tmp, then renamed). Resumable: a row file present is skipped.
"""
import json, os, subprocess, sys, time

REPO = '/home/claude/repos/jack'
BASE = '/home/claude/work/r8'
ROWS = os.path.join(BASE, 'rows')
FROZEN = os.path.join(BASE, 'frozen')
EMPTY = os.path.join(BASE, 'empty.jsonl')
RUNS = os.path.join(BASE, 'runs.json')
ACTS = os.path.join(BASE, 'acts.csv')
GITC = ['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf']


def git(*a, cwd=REPO, env=None):
    return subprocess.run(GITC + list(a), cwd=cwd, env=env, capture_output=True, check=True).stdout


def clean_env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['TZ'] = 'UTC'
    return e


def setup(T, n):
    os.makedirs(ROWS, exist_ok=True)
    open(EMPTY, 'w').close()
    with open(RUNS, 'w') as f:
        f.write('[]\n')
    with open(ACTS, 'w') as f:
        f.write('repo,time_hkt,class,kind,ref,note\n')
    if not os.path.isdir(FROZEN):
        git('worktree', 'add', '-q', '--detach', FROZEN, T)
    for k in range(n):
        w = os.path.join(BASE, f'w{k}')
        if not os.path.isdir(w):
            git('worktree', 'add', '-q', '--detach', w, T)
    commits = git('rev-list', '--first-parent', '--reverse', T).decode().split()
    with open(os.path.join(BASE, 'commits.txt'), 'w') as f:
        f.write('\n'.join(commits) + '\n')
    print(len(commits), 'rows')


def row(i, c, w, env):
    git('checkout', '-q', '--detach', c, cwd=w, env=env)
    logp = os.path.join(w, 'log.jsonl')
    has = subprocess.run(['git', 'cat-file', '-e', f'{c}:log.jsonl'], cwd=REPO, env=env).returncode == 0
    if has:
        lines = [l for l in open(logp, encoding='utf-8').read().split('\n') if l]
        as_of = json.loads(lines[-1])['ts']
        upd = json.loads(lines[0])['ts']
        log = logp
    else:
        as_of = upd = git('log', '-1', '--format=%cd', '--date=format-local:%Y-%m-%dT%H:%M:%SZ', c, env=env).decode().strip()
        log = EMPTY
    run = {'path': '.github/workflows/tests.yml', 'event': 'push', 'head_branch': 'main',
           'head_sha': c, 'conclusion': 'success', 'updated_at': upd}
    runf = os.path.join(BASE, f'run-{os.path.basename(w)}.json')
    with open(runf, 'w') as f:
        f.write(json.dumps(run))
    argv = ['--subject', 'C2a', '--as-of', as_of, '--log', '<log>', '--root', '<root>',
            '--run', '<run>', '--runs', '<runs>', '--acts', '<acts>']
    real = [{'<log>': log, '<root>': w, '<run>': runf, '<runs>': RUNS, '<acts>': ACTS}.get(a, a) for a in argv]
    t0 = time.time()
    p = subprocess.run([sys.executable, '-I', os.path.join(FROZEN, 'tools', 'status.py')] + real,
                       cwd=BASE, env=env, capture_output=True)
    out = p.stdout.decode('utf-8').split('\n')
    if out and out[-1] == '':
        out.pop()
    return {'commit': c, 'log': has, 'argv': argv, 'run': run, 'exit': p.returncode, 'stdout': out,
            'secs': round(time.time() - t0, 1)}


def work(k, n):
    env = clean_env()
    commits = open(os.path.join(BASE, 'commits.txt')).read().split()
    order = list(range(len(commits)))[::-1]          # newest (slowest) first
    mine = order[k::n]
    w = os.path.join(BASE, f'w{k}')
    for i in mine:
        dst = os.path.join(ROWS, f'{i}.json')
        if os.path.exists(dst):
            continue
        r = row(i, commits[i], w, env)
        tmp = dst + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(r, f)
        os.replace(tmp, dst)
        print(i, commits[i][:8], r['exit'], len(r['stdout']), r['secs'], flush=True)


def compare():
    t = json.load(open(os.path.join(BASE, 'table.json')))
    commits = open(os.path.join(BASE, 'commits.txt')).read().split()
    print('T', t['T'], 'rows table', len(t['rows']), 'mine', len(commits),
          'commits equal', [r['commit'] for r in t['rows']] == commits)
    missing, diffs = [], []
    for i, tr in enumerate(t['rows']):
        p = os.path.join(ROWS, f'{i}.json')
        if not os.path.exists(p):
            missing.append(i)
            continue
        m = json.load(open(p))
        bad = [k for k in ('commit', 'log', 'argv', 'run', 'exit', 'stdout') if tr.get(k) != m.get(k)]
        if list(tr.get('run', {})) != list(m['run']):
            bad.append('run-order')
        if bad:
            diffs.append((i, tr['commit'][:8], bad))
    print('missing', len(missing), missing[:10])
    print('differing', len(diffs))
    for d in diffs[:50]:
        print(' ', d)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'setup':
        setup(sys.argv[2], int(sys.argv[3]))
    elif cmd == 'work':
        work(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'compare':
        compare()
