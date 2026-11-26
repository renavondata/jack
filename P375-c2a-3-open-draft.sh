#!/bin/bash
# DRAFT, not for use: counsel's file for the sovereign's opening paste of C2a-3 (BRIEF-C2a-3 §Order of acts step 2),
# to the design of ADVISER.md entries 327 to 329. The values marked TBD are fixed from the opening note's part 1.
# It runs on steel, as gfrmin, in tmux, in ~/git/jack-guy, after 2026-11-30T00:00:00Z. It may be left: it ends by
# itself with a `push` on main's log or a line that says where it stopped. It may be pasted again after a stop.
#   1. checks the push branch, entering nothing;
#   2. waits, replaying main's new commits as it waits, until the clock, the lane and the diary's timer allow;
#   3. enters his `fix` (skipped on a second paste, if it is the first `fix` that names C2a-prime);
#   4. replays what is left, merges main into the branch with his trailer, tests, and pushes with --opens C2a-3.
set -u
R=renavondata/jack; RR=renavondata/opencode-runner
H=82ddc41bc6a12171729ddab1176bc0bdb7da10f4   # the head of opening-c2a-3 that the opening note records
S=44273c2a53be1fd881ab2880132ac0e7543efe3c66285bbe63e8b1a324901fe0   # judge/status.py on the branch
SP=c4a5b44b8465f4be9cd4a5bbeb294cfd5c56a7397319e7f1c167853d7fd628a7  # SPEC.md as counsel's patch leaves it
T=96658263399ec7eeb815fc07210ce09b8e5ca3a4                           # the table's T
L=deabad5082b88e1332a9ed56d5ca8fcae06cadb5   # the last chain commit the reviewer's record holds
END=1795996800             # 2026-11-30T00:00:00Z
D=TBD                      # minutes the diary's next tick must lie ahead, from the rehearsal
TRIES=3                    # pushes refused because main moved, before it stops
FIX="C2a-prime: criterion 3 read unmet from 2026-11-17T13:32:51Z to its end — its test walked every ancestor of main, and a branch cut before the opening was merged after it (jack #1071); for C2a-3 the test reads main's own commits"
NB=opening-c2a-3; PB=opening-c2a-3-push
WT=~/git/worktrees/jack-guy/$PB
X=~/.cache/jack-c2a-3-open        # scratch: the replay's checkouts and files
die() { echo "Stopped: $*"; echo "Send counsel everything printed above before pasting anything again."; exit 1; }

# Guards, as his read's paste.
command -v pgrep > /dev/null || die "pgrep is not here, so this cannot tell whether another paste is running"
if pgrep -f '/\.cache/jack-paste(-read)?\.sh' > /dev/null; then die "another paste of counsel's is still running here"; fi
cd ~/git/jack-guy || die "there is no ~/git/jack-guy"
git switch -q main || die "cannot switch to main"
[ "$(gh api user --jq .login)" = gfrmin ] || die "gh is not signed in as gfrmin"
git pull -q --ff-only || die "main does not fast-forward"
[ -z "$(git status --porcelain)" ] || die "the tree is not clean"
git fetch -q origin main "$NB" || die "cannot fetch main and $NB"

# 1. The branch, before anything is entered.
[ "$(git rev-parse "origin/$NB")" = "$H" ] || die "$NB is not at the head the opening note names"
P=$(git rev-list --reverse origin/main.."$H" | head -1)
git log -1 --format=%s "$P" | grep -q '^push: C2a-3 opening' || die "the branch's first commit over main is not the opening patch"
[ -z "$(git rev-list --merges origin/main.."$H")" ] || die "the branch holds a merge before the opening's"
[ "$(git show "$H:SPEC.md" | sha256sum | cut -c1-64)" = "$SP" ] || die "the branch's SPEC.md is not the one his grant names"
[ "$(git show "$H:judge/scope.json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["cap"])')" = 9100 ] || die "the branch's cap is not 9100"
[ "$(git show "$H:judge/status.py" | sha256sum | cut -c1-64)" = "$S" ] || die "the branch's evaluator is not the one the code read accepted"
git show "$H:pins/replay.py" | grep -qF "$S" || die "pins/replay.py does not hold the evaluator's hash"
git show "$H:transcripts/REVIEW-C2a-3-code.md" | head -1 | grep -qE '^VERDICT: ACCEPT( WITH OBLIGATIONS)?$' || die "the code read does not accept"
git show "$H:transcripts/REVIEW-C2a-3-code.md" | grep -qx "Evaluator: judge/status.py sha256 $S" || die "the code read names another evaluator"
echo "1. the branch: $NB at $H, as the opening note records it"

# The fixes that name C2a-prime on main's log, by the sovereign. Ours, first and alone: skip the `fix`. Any other: stop.
fixes() { git show origin/main:log.jsonl | F="$FIX" python3 -c '
import json, os, sys
f = os.environ["F"]
xs = [e for e in map(json.loads, sys.stdin) if e["type"] == "decision" and e["proposer"] == "guy"
      and e["body"].get("kind") == "fix" and e["body"].get("subject", "").startswith("C2a-prime")]
print("none" if not xs else "ours" if len(xs) == 1 and xs[0]["body"]["subject"] == f else "other")'; }

# The replay of main's first-parent chain after L, as the replay's template defines a chain commit: the evaluator on
# main twice and the table driver's `mark`, against the branch's evaluator once. Run at low priority.
replay_setup() {
  rm -rf "$X"; mkdir -p "$X" || die "cannot make $X"
  git worktree add -q --detach "$X/old" origin/main && git worktree add -q --detach "$X/new" "$H" \
    && git worktree add -q --detach "$X/w" origin/main || die "cannot make the replay's checkouts"
  git show origin/main:transcripts/evidence/promotion-replay-c2a-3-driver.py > "$X/driver.py" || die "cannot read the table's driver"
  touch "$X/done"
}
replay_next() {  # replays the oldest chain commit after L not yet replayed; prints its line; returns 1 when caught up
  git fetch -q origin main || return 2
  nice -n 19 python3 - "$X" "$T" "$L" <<'PY'
import ast, json, os, subprocess, sys
X, T, L = sys.argv[1:4]
src = open(os.path.join(X, 'driver.py')).read()
ns = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.FunctionDef) and node.name in ('lines_from', 'mark'):
        exec(compile(ast.Module([node], []), 'driver.py', 'exec'), ns)
chain = subprocess.check_output(['git', 'rev-list', '--first-parent', '--reverse', T + '..origin/main']).decode().split()
done = set(open(os.path.join(X, 'done')).read().split())
todo = [c for c in chain[chain.index(L) + 1:] if c not in done]
if not todo:
    sys.exit(1)
c = todo[0]
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
w = os.path.join(X, 'w')
subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', '-C', w, 'checkout', '-q', '--detach', c], check=True, env=ENV)
ledger = open(os.path.join(w, 'log.jsonl'), 'rb').read().splitlines()
as_of, updated = json.loads(ledger[-1])['ts'], json.loads(ledger[0])['ts']
assert len(ledger) > 7181, c
ev = os.path.join(X, 'ev'); os.makedirs(ev, exist_ok=True)
run = {'path': '.github/workflows/tests.yml', 'event': 'push', 'head_branch': 'main', 'head_sha': c,
       'conclusion': 'success', 'updated_at': updated}
open(os.path.join(ev, 'run.json'), 'w').write(json.dumps(run))
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
e3, new = run_with('new', as_of)
if (e3, new) != (e1, expected):
    print('FAILED', c, json.dumps({'exit': [e1, e3], 'expected': expected, 'printed': new}))
    sys.exit(3)
open(os.path.join(X, 'done'), 'a').write(c + '\n')
print('passed', c)
PY
}

# The lane, as his read's paste reads it, and one more test: no resolution follows the last merge on main's log.
quiet_round() {
  local s c t=0
  [ "$(gh api "repos/$R/pulls?state=open&per_page=100" --jq 'map(select(.number!=125 and .number!=316 and .number!=562))|length')" = 0 ] || return 1
  [ "$(gh api "repos/$RR/issues?state=open&labels=run&per_page=100" --jq 'map(select(.pull_request==null and ((.created_at|fromdate) > (now-86400))))|length')" = 0 ] || return 1
  for s in queued in_progress requested waiting pending; do
    c=$(gh api "repos/$RR/actions/runs?status=$s&per_page=100" --jq '[.workflow_runs[]|select(.name=="repropose" or .name=="counsel-sign" or .name=="counsel" or .name=="opencode")]|length') || return 1
    t=$((t+c))
  done
  [ "$t" = 0 ] || return 1
  git fetch -q origin main || return 1
  git show origin/main:log.jsonl | python3 -c '
import json, sys
es = [json.loads(l) for l in sys.stdin]
last = max((i for i, e in enumerate(es) if e["type"] == "merge"), default=-1)
sys.exit(1 if any(e["type"] == "resolution" for e in es[last + 1:]) else 0)'
}
# The diary's timer: both calendars present, and its next tick at least D minutes away.
timer_round() {
  local cal next
  cal=$(systemctl --user show jack-diary.timer -p TimersCalendar --value) || return 1
  [ "$(printf '%s\n' "$cal" | grep -c 'OnCalendar=')" -ge 2 ] || return 1
  next=$(systemctl --user show jack-diary.timer -p NextElapseUSecRealtime --value) || return 1
  [ "$(date -d "$next" +%s)" -ge $(( $(date +%s) + D * 60 )) ]
}

# 2. The wait, replaying as it waits. It has no bound of its own: the brief's step 2 has it wait, and not stop, while
# what it waits for can still come, and from 30 November the date, the lane and a gap in the timer always can.
wait_clear() {  # $1: the step's number, for its lines; $2: what has been entered, for a stop
  local q=0 caught=0 rc
  while :; do
    if [ "$caught" = 0 ]; then
      replay_next; rc=$?
      [ "$rc" = 3 ] && die "a commit of main does not replay as the brief says; $2"
      [ "$rc" = 1 ] && caught=1
      [ "$rc" = 2 ] && echo "$1. could not fetch main for the replay; trying again"
    fi
    if [ "$caught" = 1 ] && [ "$(date +%s)" -gt "$END" ] && quiet_round && timer_round; then q=$((q+1)); else q=0; fi
    if [ "$q" -ge 3 ]; then
      replay_next; rc=$?             # main may have moved during the rounds: catch up before going on
      [ "$rc" = 3 ] && die "a commit of main does not replay as the brief says; $2"
      [ "$rc" = 1 ] && return 0
      q=0; caught=0
    fi
    echo "$1. waiting ($(date -u +%H:%MZ); replay caught up: $caught; quiet rounds $q of 3). You may leave this."
    sleep 30
  done
}
replay_setup
wait_clear 2 "nothing was entered"

# 3. The fix.
case "$(fixes)" in
  ours) echo "3. skipped: his fix is already on main";;
  other) die "another fix names C2a-prime on main's log; the brief sends that to counsel and to him";;
  none) tools/jack decision fix "$FIX" || die "the fix was refused"
        git pull -q --ff-only || die "main does not fast-forward after the fix"
        [ "$(fixes)" = ours ] || die "the fix is not on main as entered"
        echo "3. entered: the fix";;
esac

# 4. Replay what is left, merge, test, push; again if main moves, up to TRIES times.
tries=0
while :; do
  if [ "$tries" -gt 0 ]; then
    wait_clear 4 "the fix stands and nothing was pushed"      # a retry waits for the lane and the timer, as the first push did
  else
    while :; do replay_next; rc=$?; [ "$rc" = 1 ] && break; [ "$rc" = 3 ] && die "a commit of main does not replay after the fix; the fix stands and nothing was pushed"; [ "$rc" = 2 ] && sleep 30; done
  fi
  git fetch -q origin main || die "cannot fetch main"
  rm -rf "$WT"; git worktree prune; git branch -q -D "$PB" 2>/dev/null
  git worktree add -q -B "$PB" "$WT" "$H" || die "cannot make the push's worktree"
  if ! git -C "$WT" merge -q --no-ff origin/main -m "Merge main into $NB for C2a-3's opening" -m "Proposer: guy guy-master"; then
    [ "$(git -C "$WT" diff --name-only --diff-filter=U)" = pins/pins.py ] || die "the merge conflicts beyond pins/pins.py; the fix stands and nothing was pushed"
    python3 - "$WT" <<'PY' || die "the conflict in pins/pins.py is not the EXPECTED line alone; the fix stands and nothing was pushed"
import ast, re, sys
p = sys.argv[1] + '/pins/pins.py'; t = open(p).read()
m = re.fullmatch(r'(?s)(.*?)<<<<<<< [^\n]*\nEXPECTED = \d+\n=======\nEXPECTED = \d+\n>>>>>>> [^\n]*\n(.*)', t)
assert m and '<<<<<<<' not in m.group(2)
body = m.group(1) + 'EXPECTED = 0\n' + m.group(2)
n = sum(1 for x in ast.walk(ast.parse(body)) if isinstance(x, ast.Call) and getattr(x.func, 'id', '') == 'Pin')
open(p, 'w').write(body.replace('EXPECTED = 0\n', 'EXPECTED = %d\n' % n, 1))
print('EXPECTED set to', n)
PY
    git -C "$WT" add pins/pins.py && git -C "$WT" commit -q --cleanup=strip -m "Merge main into $NB for C2a-3's opening" -m "Proposer: guy guy-master" || die "cannot commit the merge"
    git -C "$WT" log -1 --format=%B | grep -qx 'Proposer: guy guy-master' || die "the merge commit lacks his trailer"
  fi
  # The opening note's tests at the merged head.
  [ "$(cd "$WT" && python3 -c 'import json,subprocess; from judge.judge import counted_lines; s=json.load(open("judge/scope.json")); print(counted_lines(".", subprocess.check_output(["git","rev-parse","HEAD"]).decode().strip(), s["counted"]) <= 9100)')" = True ] \
    || die "the merged head holds more than 9100 counted lines; the fix stands and nothing was pushed"
  [ "$(sha256sum < "$WT/judge/status.py" | cut -c1-64)" = "$S" ] || die "the merged evaluator is not the one the code read accepted"
  # Each commit's Proposer party against its paths (the opening note's second record): counsel's patch first, with
  # SPEC.md and judge/scope.json alone; the builder's under judge/status.py and tests/; the reviewer's among the
  # reviewer's paths in judge/scope.json; and the merge, his.
  (cd "$WT" && python3 - "$P" <<'PARTIES') || die "a commit of the branch is outside its party's paths; the fix stands and nothing was pushed"
import json, subprocess, sys
P = sys.argv[1]
g = lambda *a: subprocess.check_output(['git', *a]).decode()
reviewer = json.loads(open('judge/scope.json').read())['parties']['reviewer']
for c in g('rev-list', '--reverse', 'origin/main..HEAD').split():
    party = (g('log', '-1', '--format=%(trailers:key=Proposer,valueonly)', c).split() or ['none'])[0]
    merge = len(g('rev-list', '--parents', '-n', '1', c).split()) > 2
    paths = set(g('diff-tree', '--no-commit-id', '--name-only', '-r', '--no-renames', c).split()) if not merge else set()
    if c == P:
        ok = party == 'counsel' and paths == {'SPEC.md', 'judge/scope.json'}
    elif merge:
        ok = party == 'guy'
    elif party == 'builder':
        ok = all(p == 'judge/status.py' or p.startswith('tests/') for p in paths)
    elif party == 'reviewer':
        ok = all(any(p == r or p.startswith(r) for r in reviewer) for p in paths)
    else:
        ok = False
    print(c[:8], party, 'merge' if merge else ' '.join(sorted(paths)), 'ok' if ok else 'OUTSIDE')
    if not ok:
        sys.exit(1)
PARTIES
  if tools/jack push "$PB" --opens C2a-3 --review "$WT/transcripts/REVIEW-C2a-3-code.md"; then break; fi
  tries=$((tries+1)); [ "$tries" -ge "$TRIES" ] && die "the push was refused $TRIES times; the fix stands and nothing was pushed"
  git pull -q --ff-only || die "main does not fast-forward after a refused push"
  echo "4. the push was refused; main has moved; again ($tries of $TRIES)"
done
git pull -q --ff-only
echo
echo "Done: C2a-3 is open. Its push is on main's log."
