"""Full acceptance replay of the moved evaluator (SPEC, The promotion evaluator): every table row, then the tail after T."""
import json, subprocess, sys, os, time
REPO = '/home/claude/jack-complete'
MOVED = '/home/claude/wt-build'          # checkout of the move's head
FROZEN_T = '/home/claude/accept/frozen-T'      # checkout of T
FROZEN_P = '/home/claude/accept/frozen-parent' # checkout of the move's parent
TREE = os.environ.get('TREE', '/home/claude/accept/tree')
OUT = os.environ.get('OUT', '/home/claude/accept/result.jsonl')
LO, HI = int(os.environ.get('LO', '0')), int(os.environ.get('HI', '100000'))
DO_TAIL = os.environ.get('TAIL', '1') == '1'
def git(*a, cwd=REPO):
    return subprocess.run(['git', '-C', cwd, *a], capture_output=True, check=True).stdout
table = json.loads(git('show', 'origin/main:spec/vectors/promotion-replay.json'))
T = table['T']
MARK_FROM = 593
def marked(expected):
    exp = list(expected)
    crit = next((l for l in exp if l.startswith('criterion 3:') and l.endswith('and unchanged: False SHORT')), None)
    if crit is None:
        return exp, 'no-criterion-3-mark'
    failure = crit[:-len(' SHORT')]
    exp = [l.replace('and unchanged: False SHORT', 'and unchanged: True met') if l == crit else l for l in exp]
    for i, l in enumerate(exp):
        if l.startswith('promote C2a: refused: '):
            rest = l[len('promote C2a: refused: '):]
            if failure + '; ' in rest: rest = rest.replace(failure + '; ', '', 1)
            elif '; ' + failure in rest: rest = rest.replace('; ' + failure, '', 1)
            elif rest == failure: rest = ''
            else: return exp, 'promote-line-lacks-criterion-3'
            exp[i] = 'promote C2a: ' + ('refused: ' + rest if rest else 'lawful')
    return exp, None
def files_for(run_obj, tmp):
    paths = {}
    for name, data in (('run', json.dumps(run_obj)), ('runs', '[]'), ('acts', 'repo,time_hkt,class,kind,ref,note\n')):
        p = os.path.join(tmp, name); open(p, 'w').write(data); paths[name] = p
    return paths
def run_eval(evaluator_root, argv, commit, run_obj, logless):
    subprocess.run(['git', '-C', TREE, 'checkout', '-q', '--detach', '-f', commit], check=True)
    tmp = os.environ.get('WTMP', '/home/claude/accept/tmp'); os.makedirs(tmp, exist_ok=True)
    f = files_for(run_obj, tmp)
    logp = os.path.join(TREE, 'log.jsonl')
    if logless:
        logp = os.path.join(tmp, 'empty.jsonl'); open(logp, 'w').close()
    rep = {'<root>': TREE, '<log>': logp, '<run>': f['run'], '<runs>': f['runs'], '<acts>': f['acts']}
    args = [rep.get(x, x) for x in argv]
    script = os.path.join(evaluator_root, 'judge/status.py' if os.path.exists(os.path.join(evaluator_root, 'judge/status.py')) else 'tools/status.py')
    r = subprocess.run([sys.executable, script, *args], capture_output=True, cwd=evaluator_root)
    return r.stdout.decode().splitlines(), r.returncode, r.stderr.decode()[-500:]
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        r = json.loads(l)
        if r['kind'] == 'row': done.add(r['i'])
out = open(OUT, 'a')
bad = 0; t0 = time.time()
for i, row in enumerate(table['rows']):
    if i in done or not (LO <= i < HI): continue
    actual, code, err = run_eval(MOVED, row['argv'], row['commit'], row['run'], not row['log'])
    exp, note = (marked(row['stdout']) if i >= MARK_FROM else (list(row['stdout']), None))
    ok = actual == exp and code == row['exit']
    bad += not ok
    out.write(json.dumps({'kind': 'row', 'i': i, 'commit': row['commit'], 'ok': ok, 'note': note, 'exit': code,
                          'diff': [] if ok else [(j, a, b) for j, (a, b) in enumerate(zip(exp, actual)) if a != b][:5] + [('len', len(exp), len(actual))],
                          'stderr': '' if ok else err}) + '\n'); out.flush()
    if i % 50 == 0: print(f'row {i} {time.time()-t0:.0f}s bad={bad}', flush=True)
# tail: first-parent commits after T up to the move's parent
if not DO_TAIL:
    print('DONE-ROWS', flush=True); raise SystemExit
parent = git('rev-parse', '2d99d2427296df1174a55f41459058d5f6b65a8f').decode().strip()   # 2d99d242, the move's parent
tail = git('rev-list', '--first-parent', '--reverse', f'{T}..{parent}').decode().split()
TLO, THI = int(os.environ.get('TLO', '0')), int(os.environ.get('THI', '1000'))
tdone = set()
if os.path.exists(OUT):
    for l in open(OUT):
        r = json.loads(l)
        if r['kind'] == 'tail': tdone.add(r['commit'])
print('tail', len(tail), flush=True)
for k, c in enumerate(tail):
    if c in tdone or not (TLO <= k < THI): continue
    log0 = git('show', f'{c}:log.jsonl').decode().splitlines()
    ts_last, ts_first = json.loads(log0[-1])['ts'], json.loads(log0[0])['ts']
    run_obj = {'path': '.github/workflows/tests.yml', 'event': 'push', 'head_branch': 'main', 'head_sha': c, 'conclusion': 'success', 'updated_at': ts_first}
    argv = ['--subject', 'C2a', '--as-of', ts_last, '--log', '<log>', '--root', '<root>', '--run', '<run>', '--runs', '<runs>', '--acts', '<acts>']
    frozen, fcode, ferr = run_eval(FROZEN_P, argv, c, run_obj, False)
    moved, mcode, merr = run_eval(MOVED, argv, c, run_obj, False)
    exp, note = marked(frozen)
    ok = moved == exp and mcode == fcode
    bad += not ok
    out.write(json.dumps({'kind': 'tail', 'commit': c, 'ok': ok, 'note': note, 'exit': [fcode, mcode],
                          'diff': [] if ok else [(j, a, b) for j, (a, b) in enumerate(zip(exp, moved)) if a != b][:5], 'stderr': '' if ok else (ferr + merr)}) + '\n'); out.flush()
print(f'DONE rows={len(table["rows"])} tail={len(tail)} bad={bad} {time.time()-t0:.0f}s', flush=True)
