#!/bin/bash
# Adviser's test of counsel's paste c2a-3-read.sh on a copy (ADVISER.md entry 281; R19).
# Usage: P281-read-sandbox.sh <a clone of jack with origin/main, origin/agent/pastes, origin/counsel/c2a-3-patch and
#        origin/review-c2a-3-table-1 fetched>
# The copy's main is origin/main, with the reviewer's table commit put on it if main does not hold the table yet, and
# a stand-in for tools/jack. Nothing here reaches GitHub, signs anything or uses a key. The stand-in for gh answers
# from files and does not run the paste's jq expressions.
set -u
REPO=$1; SB=$(mktemp -d); export SB; mkdir -p $SB/bin $SB/state $SB/home/git
git init -q --bare $SB/origin.git
git -C "$REPO" push -q $SB/origin.git refs/remotes/origin/main:refs/heads/main refs/remotes/origin/counsel/c2a-3-patch:refs/heads/counsel/c2a-3-patch refs/remotes/origin/review-c2a-3-table-1:refs/heads/tbl 2>/dev/null
git -C $SB/origin.git symbolic-ref HEAD refs/heads/main
git -C "$REPO" show origin/agent/pastes:c2a-3-read.sh > $SB/paste.sh; echo "paste $(sha256sum < $SB/paste.sh | cut -c1-16)"
git clone -q $SB/origin.git $SB/home/git/jack-guy; cd $SB/home/git/jack-guy; git config user.name sandbox; git config user.email sandbox@example.invalid
if ! git cat-file -e origin/main:spec/vectors/promotion-replay-c2a-3.json 2>/dev/null; then
  T=$(git log --format=%H --grep='^vectors: second promotion replay table' origin/tbl | tail -1); git cherry-pick -q $T >/dev/null 2>&1 || { echo "cannot put the table on the copy"; exit 1; }
  echo "the table is put on the copy's main from $(echo $T | cut -c1-8)"
fi
cat > tools/jack <<'PY'
#!/usr/bin/env python3
import json, os, subprocess, sys
st = os.environ['SB'] + '/state/'
open(st + 'calls', 'a').write('jack ' + sys.argv[1] + ' ' + sys.argv[2] + '\n')
if os.path.exists(st + 'grant_refuse'): sys.exit('refused: stand-in refusal')
assert sys.argv[1:3] == ['decision', 'grant'], sys.argv
n = sum(1 for _ in open('log.jsonl'))
open('log.jsonl', 'a').write(json.dumps({'seq': n, 'type': 'decision', 'proposer': 'guy', 'body': {'kind': 'grant', 'subject': sys.argv[3]}}) + '\n')
subprocess.run(['git', 'commit', '-q', '-am', 'stand-in grant'], check=True)
subprocess.run(['git', 'push', '-q', 'origin', 'main'], check=True)
PY
git commit -q -am 'sandbox: a stand-in for tools/jack'; git push -q origin HEAD:main; BASE=$(git rev-parse HEAD)
cat > $SB/bin/gh <<'SH'
#!/bin/bash
st=$SB/state; a="$*"
pop() { f=$st/$1; if [ -s "$f" ]; then head -n1 "$f"; sed -i 1d "$f"; else echo 0; fi; }
case "$a" in
  "api user --jq .login") cat $st/login;;
  "api repos/renavondata/jack/pulls?state=open&per_page=100 --jq"*) pop prs_seq;;
  "api repos/renavondata/opencode-runner/issues?state=open&labels=run&per_page=100 --jq"*) echo 0;;
  "api repos/renavondata/opencode-runner/actions/runs?status="*) echo 0;;
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
PATCH=$(git -C $SB/origin.git rev-parse counsel/c2a-3-patch)
reset() { rm -rf $SB/state; mkdir -p $SB/state; echo gfrmin > $SB/state/login
  git -C $SB/origin.git update-ref refs/heads/main $BASE; git -C $SB/origin.git update-ref refs/heads/counsel/c2a-3-patch $PATCH
  git -C $SB/origin.git update-ref -d refs/heads/opening-c2a-3 2>/dev/null
  cd $SB/home/git/jack-guy && git worktree prune && git fetch -q --prune origin && git checkout -q main && git reset -q --hard origin/main && git clean -qfd && git branch -q -D opening-c2a-3 2>/dev/null; cd /; }
other() { rm -rf $SB/o2; git clone -q $SB/origin.git $SB/o2; cd $SB/o2; git config user.name x; git config user.email x@example.invalid; }
run() { echo "== $1"; HOME=$SB/home PATH=$SB/bin:$PATH bash $SB/paste.sh > $SB/out.txt 2>&1; local x=$? b
  grep -v 'waiting for a quiet lane' $SB/out.txt | grep -v '^$' | cut -c1-150
  b=$(git -C $SB/origin.git rev-parse -q --verify refs/heads/opening-c2a-3 2>/dev/null)
  echo "   exit $x; verb calls: $(cat $SB/state/calls 2>/dev/null | wc -l); waits: $(cat $SB/state/sleeps 2>/dev/null | wc -l); grants on main: $(git -C $SB/origin.git show main:log.jsonl | grep -c 'promote_unmet: SPEC.md c4a5b44b'); branch: ${b:+published }${b:-none}; scratch checkouts left: $(git -C $SB/home/git/jack-guy worktree list | grep -c jack-c2a-3-read)"
  if [ -n "$b" ]; then echo "   the branch: $(git -C $SB/origin.git rev-list --count main..opening-c2a-3) commit over main; author $(git -C $SB/origin.git log -1 --format='%an' opening-c2a-3), committer $(git -C $SB/origin.git log -1 --format='%cn' opening-c2a-3); paths $(git -C $SB/origin.git diff --name-only main opening-c2a-3 | tr '\n' ' '); SPEC.md $(git -C $SB/origin.git show opening-c2a-3:SPEC.md | sha256sum | cut -c1-8); cap $(git -C $SB/origin.git show opening-c2a-3:judge/scope.json | python3 -c 'import json,sys; print(json.load(sys.stdin)["cap"])'); trailer lines $(git -C $SB/origin.git log -1 --format=%B opening-c2a-3 | grep -c -E '^(Proposer|Model|Co-Authored-By|Claude-Session):')"; fi; }
reset; printf '1\n0\n2\n0\n0\n0\n' > $SB/state/prs_seq; run "a. the whole path, with a lane that is busy, quiet once, busy, then quiet three times"
: > $SB/state/calls; : > $SB/state/sleeps; run "b. the same line pasted again"
reset; echo someone > $SB/state/login; run "c. gh is another login"
reset; git -C $SB/origin.git update-ref refs/heads/counsel/c2a-3-patch $BASE; run "d. counsel's patch branch is not at the commit named"
reset; other; echo x >> transcripts/BRIEF-C2a-3-draft.md; git commit -qam t; git push -q origin HEAD:main; cd /; run "e. the brief on main is not the text named"
reset; other; echo x >> spec/vectors/promotion-replay-c2a-3.json; git commit -qam t; git push -q origin HEAD:main; cd /; run "f. the table on main is not the one named"
reset; other; echo x >> SPEC.md; git commit -qam t; git push -q origin HEAD:main; cd /; run "g. SPEC.md on main is not the one the patch was written on"
reset; other; sed -i 's/"cap": 8400/"cap": 8401/' judge/scope.json; git commit -qam t; git push -q origin HEAD:main; cd /; run "h. the patch no longer applies to main (the scope file has changed)"
reset; touch $SB/state/grant_refuse; run "i. the verb refuses the grant"
reset; yes 1 | head -2000 > $SB/state/prs_seq; run "j. the lane is never quiet"
reset; printf '1\n0\n0\n0\n' > $SB/state/prs_seq; echo transcripts/BRIEF-C2a-3-draft.md > $SB/state/move; run "k. the brief changes on main while the paste waits"
reset; printf '1\n0\n0\n0\n' > $SB/state/prs_seq; echo README.md > $SB/state/move; run "l. main moves by another file while the paste waits"
reset; other; git checkout -q -b opening-c2a-3; echo x >> README.md; git commit -qam t; git push -q origin opening-c2a-3; cd /; run "m. a branch of that name is already published without the patch"
reset; chmod -w $SB/origin.git/refs/heads 2>/dev/null; printf '#!/bin/sh\ncase "$*" in *opening-c2a-3*) exit 1;; esac\n' > $SB/origin.git/hooks/update; chmod +x $SB/origin.git/hooks/update; chmod +w $SB/origin.git/refs/heads; run "n. the grant is entered and the branch's push is refused"
rm -f $SB/origin.git/hooks/update; : > $SB/state/calls; : > $SB/state/sleeps; run "o. pasted again after n: the grant is skipped and the branch published"
rm -rf $SB
