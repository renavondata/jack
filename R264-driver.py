#!/usr/bin/env python3
"""Adviser's own driver for the second promotion replay table (BRIEF-C2a-3, The code; SPEC 10, The promotion evaluator).

usage: drv.py setup HEAD | drv.py extend HEAD | drv.py work K N DEADLINE_EPOCH | drv.py status
A row is one first-parent commit. Its own run is R. Where its log holds an entry after seq 7180 it is marked and has a
second run, V, with --as-of 2026-11-22T11:44:05Z. Rows are kept by commit hash in rows/<commit>.json (written to .tmp,
then renamed), so the work can stop and go on. Nothing here builds the table's `marked` member: that is done at the
comparison, from R and V, so that the raw runs do not depend on the session template's wording.
"""
import json, os, subprocess, sys, time

REPO = '/home/claude/repos/jack'
BASE = '/home/claude/work/r264'
ROWS = os.path.join(BASE, 'rows')
FROZEN = os.path.join(BASE, 'frozen')
EMPTY = os.path.join(BASE, 'empty.jsonl')
RUNS = os.path.join(BASE, 'runs.json')
ACTS = os.path.join(BASE, 'acts.csv')
GITC = ['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf']
VETO_TS, VETO_LINES = '2026-11-22T11:44:05Z', 7181


def git(*a, cwd=REPO, env=None):
    return subprocess.run(GITC + list(a), cwd=cwd, env=env, capture_output=True, check=True).stdout


def clean_env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['TZ'] = 'UTC'
    return e


def chain(head):
    return git('rev-list', '--first-parent', '--reverse', head).decode().split()


def setup(head, n=2):
    os.makedirs(ROWS, exist_ok=True)
    open(EMPTY, 'w').close()
    open(RUNS, 'w').write('[]\n')
    open(ACTS, 'w').write('repo,time_hkt,class,kind,ref,note\n')
    for name in ['frozen'] + [f'w{k}' for k in range(n)]:
        p = os.path.join(BASE, name)
        if not os.path.isdir(p):
            git('worktree', 'add', '-q', '--detach', p, head)
    extend(head)


def extend(head):
    commits = chain(head)
    open(os.path.join(BASE, 'commits.txt'), 'w').write('\n'.join(commits) + '\n')
    open(os.path.join(BASE, 'head.txt'), 'w').write(head + '\n')
    print(len(commits), 'rows to', head[:8])


def evaluate(real, env):
    t0 = time.time()
    p = subprocess.run([sys.executable, '-I', os.path.join(FROZEN, 'judge', 'status.py')] + real,
                       cwd=BASE, env=env, capture_output=True)
    out = p.stdout.decode('utf-8').split('\n')
    if out and out[-1] == '':
        out.pop()
    return p.returncode, out, round(time.time() - t0, 1)


def row(c, w, env):
    git('checkout', '-q', '--detach', c, cwd=w, env=env)
    logp = os.path.join(w, 'log.jsonl')
    has = subprocess.run(['git', 'cat-file', '-e', f'{c}:log.jsonl'], cwd=REPO, env=env).returncode == 0
    nlines = 0
    if has:
        lines = [l for l in open(logp, encoding='utf-8').read().split('\n') if l]
        nlines = len(lines)
        as_of, upd, log = json.loads(lines[-1])['ts'], json.loads(lines[0])['ts'], logp
    else:
        as_of = upd = git('log', '-1', '--format=%cd', '--date=format-local:%Y-%m-%dT%H:%M:%SZ', c, env=env).decode().strip()
        log = EMPTY
    run = {'path': '.github/workflows/tests.yml', 'event': 'push', 'head_branch': 'main',
           'head_sha': c, 'conclusion': 'success', 'updated_at': upd}
    runf = os.path.join(BASE, f'run-{os.path.basename(w)}.json')
    open(runf, 'w').write(json.dumps(run))
    argv = ['--subject', 'C2a', '--as-of', as_of, '--log', '<log>', '--root', '<root>',
            '--run', '<run>', '--runs', '<runs>', '--acts', '<acts>']
    sub = {'<log>': log, '<root>': w, '<run>': runf, '<runs>': RUNS, '<acts>': ACTS}
    code, out, secs = evaluate([sub.get(a, a) for a in argv], env)
    r = {'commit': c, 'log': has, 'argv': argv, 'run': run, 'exit': code, 'stdout': out, 'secs': secs,
         'log_lines': nlines, 'is_marked': nlines > VETO_LINES}
    if r['is_marked']:
        argv_v = list(argv)
        argv_v[3] = VETO_TS
        r['v_exit'], r['v_stdout'], r['v_secs'] = evaluate([sub.get(a, a) for a in argv_v], env)
    return r


def work(k, n, deadline):
    env = clean_env()
    commits = open(os.path.join(BASE, 'commits.txt')).read().split()
    order = list(range(len(commits)))[::-1]          # newest (slowest) first
    w = os.path.join(BASE, f'w{k}')
    last = 0.0
    for i in order[k::n]:
        dst = os.path.join(ROWS, f'{commits[i]}.json')
        if os.path.exists(dst):
            continue
        if time.time() + 1.15 * last + 5 > deadline:    # do not start a row that would be cut off
            print('deadline; stopping before row', i, flush=True)
            return
        r = row(commits[i], w, env)
        last = r['secs'] + r.get('v_secs', 0)
        tmp = dst + '.tmp'
        json.dump(r, open(tmp, 'w'))
        os.replace(tmp, dst)
        print(i, commits[i][:8], r['exit'], len(r['stdout']), r['secs'], r.get('v_secs', ''), flush=True)
    print('worker', k, 'has no row left', flush=True)


def status():
    commits = open(os.path.join(BASE, 'commits.txt')).read().split()
    done = [i for i, c in enumerate(commits) if os.path.exists(os.path.join(ROWS, f'{c}.json'))]
    secs = 0.0
    for i in done:
        r = json.load(open(os.path.join(ROWS, f'{commits[i]}.json')))
        secs += r['secs'] + r.get('v_secs', 0)
    left = [i for i in range(len(commits)) if i not in set(done)]
    print(f'{len(done)} of {len(commits)} rows done, {secs/3600:.2f} core-hours spent; rows left: {len(left)}'
          + (f', from index {left[0]} to {left[-1]}' if left else ''))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'setup':
        setup(sys.argv[2])
    elif cmd == 'extend':
        extend(sys.argv[2])
    elif cmd == 'work':
        work(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
    elif cmd == 'status':
        status()
