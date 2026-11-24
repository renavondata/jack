#!/bin/bash
# Counsel's file for the sovereign to run on steel, as gfrmin, in tmux (ADVISER.md on jack's adviser/notes).
# It does two things in order, and may be run again: a step already done is skipped.
#   1. his merge of the runner's branch named below, at the commit named below: the diary's fetch of jack is
#      tried three times before a tick gives up;
#   2. his one grant, for the fix text FIX-20261124-pins-worker at the hash named below, entered only after the
#      lane has been quiet for three rounds running (it waits for that, up to 8 hours).
# It acts under no party's key and removes no work of the court: the merge is his on his runner, and the grant
# is his entry. After it, counsel files the reviewer's session that builds the fix.
#
# What the grant says he read, and what counsel tells him of it before he pastes:
#   - The fix: a pins run ends, with a message and exit status 1, when a worker dies while it runs a task or
#     waits for one; and a pin's test that exits is recorded as KILLED or TWIN FAILED, where today a run with
#     one worker ends with status 0 and no table.
#   - It leaves three ways a run can still hang: a worker that dies while sending a large result, a worker
#     that hangs, and a survivor that ignores the signal to end.
#   - His read of the text is the only read before the herald merges the fix on green
#     (transcripts/sessions/README.md on main). Counsel reads the reviewer's diff afterwards and reports.
set -u
R=renavondata/jack; RR=renavondata/opencode-runner
B=counsel/diary-fetch-retry
H=8915c4323910dbd81a0757aea0e11e95b7c05749
T1=ddef2c29282f6c5b1519e6df914dea744fb584d7c251efd976c55fff6b505aa2
F1=454e343a23e4ee093da67f9886f81e71da5ff50051fb8573985cd2a020e75b74
F2=c1f75bb89585a862d3a87f1d7507c6f419aff9cb072d040776f19632fa71ba2b
G1="A2.10 for FIX-20261124-pins-worker. Before entering this I read transcripts/FIX-20261124-pins-worker.md at sha256 $T1 and approved it unchanged."
die() { echo "Stopped: $*"; echo "Send counsel everything printed above before pasting anything again."; exit 1; }
on_main() { git show "origin/main:$1" | sha256sum | cut -c1-64; }

cd ~/git/jack-guy || die "there is no ~/git/jack-guy"
git switch -q main || die "cannot switch to main"
[ "$(gh api user --jq .login)" = gfrmin ] || die "gh is not signed in as gfrmin"
git pull -q --ff-only || die "main does not fast-forward"
[ -z "$(git status --porcelain)" ] || die "the tree is not clean"

# The text and the two templates on main must be the ones that were read.
[ "$(on_main transcripts/FIX-20261124-pins-worker.md)" = "$T1" ] || die "FIX-20261124-pins-worker.md on main is not the text named here"
[ "$(on_main transcripts/sessions/fix.md)" = "$F1" ] || die "sessions/fix.md on main is not the template named here"
[ "$(on_main transcripts/sessions/fix-reviewer.md)" = "$F2" ] || die "sessions/fix-reviewer.md on main is not the template named here"

# His rule of 19 November: a paste that enters something on jack waits for a quiet minute, and does not stop.
# A round is quiet when no proposal is open on jack (the three old ones named here apart), no session issue of the
# last 24 hours is open on the runner, and no run of the lane's four workflows is queued or running.
# quiet waits for three quiet rounds running, 30 seconds apart, for at most 8 hours. A call that fails counts as not quiet.
quiet_round() {
  local s c t=0
  [ "$(gh api "repos/$R/pulls?state=open&per_page=100" --jq 'map(select(.number!=125 and .number!=316 and .number!=562))|length')" = 0 ] || return 1
  [ "$(gh api "repos/$RR/issues?state=open&labels=run&per_page=100" --jq 'map(select(.pull_request==null and ((.created_at|fromdate) > (now-86400))))|length')" = 0 ] || return 1
  for s in queued in_progress requested waiting pending; do
    c=$(gh api "repos/$RR/actions/runs?status=$s&per_page=100" --jq '[.workflow_runs[]|select(.name=="repropose" or .name=="counsel-sign" or .name=="counsel" or .name=="opencode")]|length') || return 1
    t=$((t+c))
  done
  [ "$t" = 0 ]
}
quiet() {
  local n=0 q=0
  while :; do
    if quiet_round; then q=$((q+1)); else q=0; fi
    [ "$q" -ge 3 ] && return 0
    n=$((n+1)); [ "$n" -ge 960 ] && return 1
    echo "2. waiting for a quiet lane before the grant ($(date -u +%H:%MZ); quiet rounds $q of 3)"
    sleep 30
  done
}

# 1. The runner merge.
if [ "$(gh api "repos/$RR/compare/main...$H" --jq .ahead_by)" = 0 ]; then
  echo "1. the runner's main already holds $H"
else
  [ "$(gh api "repos/$RR/git/ref/heads/$B" --jq .object.sha)" = "$H" ] || die "the runner's $B is not at $H"
  N=$(gh api "repos/$RR/pulls?state=open&head=renavondata:$B" --jq '.[0].number // empty')
  if [ -z "$N" ]; then
    N=$(gh api "repos/$RR/pulls" -f title='The diary: its fetch of jack is tried three times, ten seconds apart, before a tick gives up' -f head="$B" -f base=main -f body="Counsel's change, audited in ADVISER.md on jack's adviser/notes (entries 239 and 262). Merged by the sovereign." --jq .number) || die "cannot open the runner's pull request"
  fi
  gh api -X PUT "repos/$RR/pulls/$N/merge" -f merge_method=merge -f sha="$H" > /dev/null || die "the runner's pull request #$N did not merge"
  [ "$(gh api "repos/$RR/compare/main...$H" --jq .ahead_by)" = 0 ] || die "the runner's main does not hold $H after the merge"
  echo "1. merged the runner's pull request #$N at $H"
fi

# 2. The grant.
git fetch -q origin main || die "cannot fetch main"
S="$G1"
if git show origin/main:log.jsonl | grep -qF "$S"; then
  echo "2. already on main: ${S%%. Before*}"
else
  quiet || die "waited 8 hours and the lane was never quiet for three rounds running, so the grant was not entered"
  git pull -q --ff-only || die "main does not fast-forward before the grant"
  [ "$(on_main transcripts/FIX-20261124-pins-worker.md)" = "$T1" ] || die "FIX-20261124-pins-worker.md on main changed while this waited"
  tools/jack decision grant "$S" || die "the grant was refused"
  git pull -q --ff-only || die "main does not fast-forward after the grant"
  git show origin/main:log.jsonl | grep -qF "$S" || die "the grant is not on main"
  echo "2. entered: ${S%%. Before*}"
fi
echo
echo "Done: the runner change is merged and the grant is on main. Counsel now files the reviewer's session for the fix."
