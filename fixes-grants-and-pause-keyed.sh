#!/bin/bash
# Counsel's file for the sovereign to run on steel, as gfrmin, in tmux (ADVISER.md on jack's adviser/notes).
# It does four things in order, and may be run again: a step already done is skipped.
#   1. his merge of the runner's branch named below, at the commit named below;
#   2. his two grants, for the fix texts FIX-20261123-check and FIX-20261123-pins-parallel, at the hashes named below,
#      each entered only after the lane has been quiet for three rounds running (it waits for that, up to 8 hours);
#   3. a wait, entering nothing, until both fixes are on jack's main and its two latest test runs are green in 15 minutes or less;
#   4. the removal of his timer's drop-in, which lifts the pause on new forecast streams.
# It acts under no party's key and removes no work of the court: the merge is his on his runner, the grants are his entries,
# and the timer is his own on steel.
set -u
R=renavondata/jack; RR=renavondata/opencode-runner
B=counsel/lane-hygiene-keyed
H=f67c721e7ccfec3e674e38b698b0f1c65f726e47
D="$HOME/.config/systemd/user/jack-diary.timer.d/pause-streams.conf"
T1=28bd85d9ac40250c09f349b935c4d18216b66b45b1b77d53896d79c9547fe7e3
T2=94bc785de936c5bd071f87f1db9d9c71d723067320c73973a5ae96dd46b9bced
F1=2aa014f9c16772d23cc5e49a09f712aaca8949f98f243347c903e355df3f0196
F2=1990b19c162f9ef224835eb2570c7c4c4850a81a0fa2caed856dcaa238a92644
G1="A2.10 for FIX-20261123-check. Before entering this I read transcripts/FIX-20261123-check.md at sha256 $T1 and approved it unchanged."
G2="A2.10 for FIX-20261123-pins-parallel. Before entering this I read transcripts/FIX-20261123-pins-parallel.md at sha256 $T2 and approved it unchanged."
die() { echo "Stopped: $*"; echo "Send counsel everything printed above before pasting anything again."; exit 1; }
on_main() { git show "origin/main:$1" | sha256sum | cut -c1-64; }

cd ~/git/jack-guy || die "there is no ~/git/jack-guy"
git switch -q main || die "cannot switch to main"
[ "$(gh api user --jq .login)" = gfrmin ] || die "gh is not signed in as gfrmin"
git pull -q --ff-only || die "main does not fast-forward"
[ -z "$(git status --porcelain)" ] || die "the tree is not clean"

# The two texts and the two templates on main must be the ones that were read.
[ "$(on_main transcripts/FIX-20261123-check.md)" = "$T1" ] || die "FIX-20261123-check.md on main is not the text named here"
[ "$(on_main transcripts/FIX-20261123-pins-parallel.md)" = "$T2" ] || die "FIX-20261123-pins-parallel.md on main is not the text named here"
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
    N=$(gh api "repos/$RR/pulls" -f title='The lane: no re-proposal of a transcript or evidence alone; the herald leaves a closed pull request alone; wider sweeps; the grant gate for fix templates; no body from counsel names a key' -f head="$B" -f base=main -f body="Counsel's change, audited in ADVISER.md on jack's adviser/notes (entries 154 to 193). Merged by the sovereign." --jq .number) || die "cannot open the runner's pull request"
  fi
  gh api -X PUT "repos/$RR/pulls/$N/merge" -f merge_method=merge -f sha="$H" > /dev/null || die "the runner's pull request #$N did not merge"
  [ "$(gh api "repos/$RR/compare/main...$H" --jq .ahead_by)" = 0 ] || die "the runner's main does not hold $H after the merge"
  echo "1. merged the runner's pull request #$N at $H"
fi

# 2. The two grants.
git fetch -q origin main || die "cannot fetch main"
for S in "$G1" "$G2"; do
  if git show origin/main:log.jsonl | grep -qF "$S"; then
    echo "2. already on main: ${S%%. Before*}"
  else
    quiet || die "waited 8 hours and the lane was never quiet for three rounds running, so this grant was not entered"
    git pull -q --ff-only || die "main does not fast-forward before the grant"
    tools/jack decision grant "$S" || die "the grant was refused"
    git pull -q --ff-only || die "main does not fast-forward after the grant"
    git show origin/main:log.jsonl | grep -qF "$S" || die "the grant is not on main"
    echo "2. entered: ${S%%. Before*}"
  fi
done
echo
echo "DONE SO FAR: the runner change is merged and both grants are on main. Counsel now files the two fix sessions."
echo "From here this only waits. It enters nothing more on jack."
echo

# 3. The wait.
if [ ! -f "$D" ]; then
  echo "4. the pause's drop-in is not there, so the pause is already lifted. Nothing more to do."
  exit 0
fi
[ -n "${TMUX:-}${STY:-}" ] || echo "Note: this is not inside tmux or screen. If the connection drops, the pause stays, and the same line can be pasted again."
RUNS="repos/$R/actions/workflows/tests.yml/runs?branch=main&event=push&status=completed&per_page=2"
n=0
until [ "$((n+=1))" -gt 960 ]; do
  if git fetch -q origin main \
     && git show origin/main:tools/jack | grep -q TMPDIR \
     && git show origin/main:pins/run.py | grep -q PINS_WORKERS \
     && [ "$(gh api "$RUNS" --jq '[.workflow_runs[]|select(.conclusion=="success")|((.updated_at|fromdate)-(.run_started_at|fromdate))|select(.<=900)]|length')" = 2 ] \
     && [ "$(gh api "$RUNS" --jq '.workflow_runs[0].head_sha')" = "$(git rev-parse origin/main)" ]; then
    break
  fi
  [ "$((n % 10))" = 1 ] && echo "3. waiting for both fixes on main and two green test runs of 15 minutes or less ($(date -u +%H:%MZ))"
  sleep 60
done
[ "$n" -le 960 ] || die "waited 16 hours and the condition does not hold, so the pause on new streams stays"
echo "3. both fixes are on main at $(git rev-parse --short=8 origin/main), and its two latest test runs are green in 15 minutes or less"

# 4. Lift the pause.
rm "$D" || die "cannot remove $D"
systemctl --user daemon-reload || die "daemon-reload failed"
systemctl --user restart jack-diary.timer || die "the timer did not restart"
C="$(systemctl --user show jack-diary.timer -p TimersCalendar)"
echo "$C"
[ "$(echo "$C" | grep -o 'OnCalendar=' | wc -l)" -ge 2 ] || die "the timer does not show its two calendars again"
echo "Done: the pause is lifted, and new forecast streams resume at the timer's next stream tick."
