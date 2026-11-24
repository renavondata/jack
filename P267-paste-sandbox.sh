#!/bin/bash
# Adviser's test of counsel's paste pins-worker-grant.sh on a copy (ADVISER.md entry 267; R19).
# Usage: P267-paste-sandbox.sh <a clone of jack that has origin/main and origin/agent/pastes fetched>
# It builds, under a fresh directory, a bare copy of main, a clone of it at home/git/jack-guy, and stand-ins for gh,
# sleep and tools/jack. Nothing here reaches GitHub, signs anything or uses a key. The stand-in for gh answers from
# files; it does not run the paste's jq expressions, which are those of the paste he ran on 23 November.
set -u
REPO=$1; SB=$(mktemp -d); export SB; mkdir -p $SB/bin $SB/state $SB/home/git
git init -q --bare $SB/origin.git; git -C "$REPO" push -q $SB/origin.git refs/remotes/origin/main:refs/heads/main 2>/dev/null
git -C $SB/origin.git symbolic-ref HEAD refs/heads/main
git -C "$REPO" show origin/agent/pastes:pins-worker-grant.sh > $SB/paste.sh; echo "paste $(sha256sum < $SB/paste.sh | cut -c1-16)"
git clone -q $SB/origin.git $SB/home/git/jack-guy; cd $SB/home/git/jack-guy; git config user.name sandbox; git config user.email sandbox@example.invalid
cat > tools/jack <<'PY'
#!/usr/bin/env python3
import json, os, subprocess, sys
st = os.environ['SB'] + '/state/'
open(st + 'calls', 'a').write('jack ' + json.dumps(sys.argv[1:]) + '\n')
if os.path.exists(st + 'grant_refuse'): sys.exit('refused: stand-in refusal')
assert sys.argv[1:3] == ['decision', 'grant'], sys.argv
n = sum(1 for _ in open('log.jsonl'))
open('log.jsonl', 'a').write(json.dumps({'seq': n, 'type': 'decision', 'proposer': 'guy', 'body': {'kind': 'grant', 'subject': sys.argv[3]}}) + '\n')
subprocess.run(['git', 'commit', '-q', '-am', 'stand-in grant'], check=True)
subprocess.run(['git', 'push', '-q', 'origin', 'main'], check=True)
PY
git commit -q -am 'sandbox: a stand-in for tools/jack'; git push -q origin main; BASE=$(git rev-parse HEAD)
cat > $SB/bin/gh <<'SH'
#!/bin/bash
st=$SB/state; a="$*"
pop() { f=$st/$1; if [ -s "$f" ]; then head -n1 "$f"; sed -i 1d "$f"; else echo 0; fi; }
case "$a" in
  "api user --jq .login") cat $st/login;;
  "api repos/renavondata/jack/pulls?state=open&per_page=100 --jq"*) pop prs_seq;;
  "api repos/renavondata/opencode-runner/issues?state=open&labels=run&per_page=100 --jq"*) echo 0;;
  "api repos/renavondata/opencode-runner/actions/runs?status="*) echo 0;;
  "api repos/renavondata/opencode-runner/compare/main..."*) cat $st/ahead;;
  "api repos/renavondata/opencode-runner/git/ref/heads/"*) cat $st/branchsha;;
  "api repos/renavondata/opencode-runner/pulls?state=open&head=renavondata:"*) cat $st/prnum 2>/dev/null;;
  "api repos/renavondata/opencode-runner/pulls -f title="*) echo CREATE >> $st/calls; echo 1299 > $st/prnum; echo 1299;;
  "api -X PUT repos/renavondata/opencode-runner/pulls/"*"/merge -f merge_method=merge -f sha="*) echo "MERGE ${a##*sha=}" >> $st/calls; [ -e $st/merge_fail ] && exit 1; echo 0 > $st/ahead;;
  *) echo "UNEXPECTED $a" >> $st/calls; exit 1;;
esac
SH
cat > $SB/bin/sleep <<'SH'
#!/bin/bash
echo s >> $SB/state/sleeps
if [ "$(wc -l < $SB/state/sleeps)" = 1 ] && [ -e $SB/state/move ]; then   # main moves once, during the first wait
  rm -rf $SB/other; git clone -q $SB/origin.git $SB/other; cd $SB/other; git config user.name x; git config user.email x@example.invalid
  echo x >> "$(cat $SB/state/move)"; git add -A; git commit -qm 'main moves while the paste waits'; git push -q origin HEAD:main
fi
SH
chmod +x $SB/bin/gh $SB/bin/sleep
reset() { rm -rf $SB/state; mkdir -p $SB/state; echo gfrmin > $SB/state/login; echo 1 > $SB/state/ahead
  echo 8915c4323910dbd81a0757aea0e11e95b7c05749 > $SB/state/branchsha; git -C $SB/origin.git update-ref refs/heads/main $BASE
  cd $SB/home/git/jack-guy && git fetch -q origin && git checkout -q main && git reset -q --hard origin/main && git clean -qfd; cd /; }
run() { echo "== $1"; HOME=$SB/home PATH=$SB/bin:$PATH bash $SB/paste.sh 2>&1 | grep -v 'waiting for a quiet lane' | grep -v '^$' | cut -c1-120
  echo "   exit ${PIPESTATUS[0]}; acts: $(cut -d' ' -f1 $SB/state/calls 2>/dev/null | tr '\n' ' '); waits: $(cat $SB/state/sleeps 2>/dev/null | wc -l); grants on main: $(git -C $SB/origin.git show main:log.jsonl | grep -c 'A2.10 for FIX-20261124-pins-worker')"; }
reset; printf '1\n1\n0\n2\n0\n0\n0\n' > $SB/state/prs_seq; run "a. the whole path, with a lane that is busy, quiet once, busy, then quiet three times"
: > $SB/state/calls; : > $SB/state/sleeps; run "b. the same line pasted again"
reset; echo someone > $SB/state/login; run "c. gh is another login"
reset; echo x > $SB/home/git/jack-guy/stray.txt; run "d. his tree is not clean"
reset; echo 0000000000000000000000000000000000000000 > $SB/state/branchsha; run "e. the runner's branch is not at the commit named"
reset; touch $SB/state/merge_fail; run "f. the runner's merge fails"
reset; echo 1257 > $SB/state/prnum; run "g. the runner's pull request is already open"
reset; touch $SB/state/grant_refuse; run "h. the verb refuses the grant"
reset; yes 1 | head -2000 > $SB/state/prs_seq; run "i. the lane is never quiet"
reset; printf '1\n0\n0\n0\n' > $SB/state/prs_seq; echo transcripts/FIX-20261124-pins-worker.md > $SB/state/move; run "j. the text changes on main while the paste waits"
reset; printf '1\n0\n0\n0\n' > $SB/state/prs_seq; echo README.md > $SB/state/move; run "k. main moves by another file while the paste waits"
reset; git clone -q $SB/origin.git $SB/o2; (cd $SB/o2; git config user.name x; git config user.email x@example.invalid; echo x >> transcripts/sessions/fix.md; git commit -qam t; git push -q origin HEAD:main); BASE2=$BASE; (cd $SB/home/git/jack-guy; git pull -q); run "l. a template on main is not the one named"
rm -rf $SB
