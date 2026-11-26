#!/bin/bash
# Counsel's rehearsal for C2a-3's opening paste: it times, on steel, the steps that lie between his `fix` and the
# push, so that the opening note can state D (BRIEF-C2a-3 §Order of acts step 2: "The opening note states the time
# from fix to push as the rehearsal measures it"). It enters nothing, signs nothing, pushes nothing and changes no
# branch: it works in a fresh clone of its own under ~/.cache, so that ~/git/jack-guy is not touched, and removes it.
# It first waits until no session runs on the runner, so that the figure is steel's unloaded one. It takes about
# fifty minutes after that and may be left.
#   A. one replay of main's newest first-parent commit, as the opening paste replays (old evaluator twice, new once);
#   B. main merged into opening-c2a-3 in a scratch worktree, EXPECTED set as the opening paste sets it;
#   C. the push verb's own check on that tree (tools/jack the_check: tests, pins and kernel count, in parallel);
#   D. judge/selfcheck.py, which both verbs run after their commit;
#   E. the diary timer's calendars and next elapse, as the opening paste reads them.
set -u
H=82ddc41bc6a12171729ddab1176bc0bdb7da10f4
X=~/.cache/jack-c2a-3-rehearse
die() { echo "Stopped: $*"; echo "Send counsel everything printed above."; rm -rf "$X"; exit 1; }
# As CI runs the tests (.github/workflows/tests.yml): no key, no global or system git config, a neutral identity.
N=(env -u JACK_KEY GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_AUTHOR_NAME=rehearsal GIT_AUTHOR_EMAIL=rehearsal@invalid GIT_COMMITTER_NAME=rehearsal GIT_COMMITTER_EMAIL=rehearsal@invalid)
t() { date +%s; }
[ -d ~/git/jack-guy/.git ] || die "there is no ~/git/jack-guy"
until [ "$(gh api 'repos/renavondata/opencode-runner/actions/runs?status=in_progress&per_page=50' --jq '[.workflow_runs[]|select(.name!="herald")]|length')" = 0 ]; do
  echo "waiting for the runner to be idle ($(date -u +%H:%MZ)). You may leave this."; sleep 60; done
rm -rf "$X"; mkdir -p "$X/tmp" || die "cannot make $X"
git clone -q --reference ~/git/jack-guy "$(git -C ~/git/jack-guy remote get-url origin)" "$X/c" || die "cannot clone"
cd "$X/c" && git fetch -q origin opening-c2a-3 || die "cannot fetch"
[ "$(git rev-parse origin/opening-c2a-3)" = "$H" ] || echo "note: opening-c2a-3 is not at ${H:0:8}; timing what it holds"
git worktree add -q --detach "$X/old" origin/main && git worktree add -q --detach "$X/new" origin/opening-c2a-3 \
  && git worktree add -q --detach "$X/w" origin/main && git worktree add -q --detach "$X/m" origin/opening-c2a-3 || die "cannot make checkouts"
git show origin/main:transcripts/evidence/promotion-replay-c2a-3-driver.py > "$X/driver.py" || die "cannot read the driver"

s=$(t); C=$(git rev-parse origin/main)
python3 - "$X" "$C" <<'PY' || die "A failed"
import ast, json, os, subprocess, sys
X, c = sys.argv[1:3]
ns = {}
for node in ast.parse(open(os.path.join(X, 'driver.py')).read()).body:
    if isinstance(node, ast.FunctionDef) and node.name in ('lines_from', 'mark'):
        exec(compile(ast.Module([node], []), 'driver.py', 'exec'), ns)
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
w = os.path.join(X, 'w')
ledger = open(os.path.join(w, 'log.jsonl'), 'rb').read().splitlines()
as_of, updated = json.loads(ledger[-1])['ts'], json.loads(ledger[0])['ts']
ev = os.path.join(X, 'ev'); os.makedirs(ev, exist_ok=True)
open(os.path.join(ev, 'run.json'), 'w').write(json.dumps({'path': '.github/workflows/tests.yml', 'event': 'push',
     'head_branch': 'main', 'head_sha': c, 'conclusion': 'success', 'updated_at': updated}))
open(os.path.join(ev, 'runs.json'), 'w').write('[]\n')
open(os.path.join(ev, 'acts.csv'), 'w').write('repo,time_hkt,class,kind,ref,note\n')
def run_with(evaluator, at):
    argv = ['python3', '-I', os.path.join(X, evaluator, 'judge', 'status.py'), '--subject', 'C2a', '--as-of', at,
            '--log', os.path.join(w, 'log.jsonl'), '--root', w, '--run', os.path.join(ev, 'run.json'),
            '--runs', os.path.join(ev, 'runs.json'), '--acts', os.path.join(ev, 'acts.csv')]
    r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=ENV)
    return r.returncode, ns['lines_from'](r.stdout)
e1, R = run_with('old', as_of)
_, V = run_with('old', '2026-11-22T11:44:05Z')
expected = ns['mark'](c, R, V)
print('A. replay of', c[:8], 'passed' if run_with('new', as_of) == (e1, expected) else 'DID NOT PASS')
PY
echo "A. $(( $(t) - s )) s"

s=$(t)
cd "$X/m" || die "no scratch worktree"
if ! "${N[@]}" git -c commit.gpgsign=false -c core.hooksPath=/dev/null merge -q --no-ff origin/main -m rehearsal > /dev/null 2>&1; then
  [ "$(git diff --name-only --diff-filter=U)" = pins/pins.py ] || die "B: the merge conflicts beyond pins/pins.py"
  python3 - <<'PY' || die "B: the conflict is not the EXPECTED line alone"
import ast, re
p = 'pins/pins.py'; t = open(p).read()
m = re.fullmatch(r'(?s)(.*?)<<<<<<< [^\n]*\nEXPECTED = \d+\n=======\nEXPECTED = \d+\n>>>>>>> [^\n]*\n(.*)', t)
assert m and '<<<<<<<' not in m.group(2)
body = m.group(1) + 'EXPECTED = 0\n' + m.group(2)
n = sum(1 for x in ast.walk(ast.parse(body)) if isinstance(x, ast.Call) and getattr(x.func, 'id', '') == 'Pin')
open(p, 'w').write(body.replace('EXPECTED = 0\n', 'EXPECTED = %d\n' % n, 1)); print('B. EXPECTED set to', n)
PY
  git add pins/pins.py && "${N[@]}" git -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -q --no-edit || die "B: cannot commit the scratch merge"
fi
echo "B. $(( $(t) - s )) s"

s=$(t)
"${N[@]}" TMPDIR="$X/tmp" python3 tools/count_kernel.py > "$X/count.txt" 2>&1 || die "C: the kernel count fails: $(tail -3 "$X/count.txt")"
"${N[@]}" TMPDIR="$X/tmp" python3 -m unittest discover -s tests -t . > "$X/tests.txt" 2>&1 & a=$!
"${N[@]}" TMPDIR="$X/tmp" python3 pins/run.py > "$X/pins.txt" 2>&1 & b=$!
wait $a; ra=$?; ta=$(( $(t) - s )); wait $b; rb=$?
echo "C. tests exit $ra in $ta s; pins exit $rb; both in $(( $(t) - s )) s; $(tail -1 "$X/pins.txt")"

s=$(t)
"${N[@]}" python3 judge/selfcheck.py --repo "$X/m" | tail -1
echo "D. $(( $(t) - s )) s"

echo "E. $(systemctl --user show jack-diary.timer -p TimersCalendar --value | tr '\n' ' ')"
echo "E. next elapse $(systemctl --user show jack-diary.timer -p NextElapseUSecRealtime --value)"
cd ~ && rm -rf "$X"
echo "Done: nothing was entered. Send counsel the lines from A to E."
