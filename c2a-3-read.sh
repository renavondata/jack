#!/bin/bash
# Counsel's file for the sovereign to run on steel, as gfrmin, in tmux (ADVISER.md on jack's adviser/notes).
# It is his read of BRIEF-C2a-3 (the brief's Precondition, items 4 to 6, and Order of acts, step 1).
# It does three things in order, and may be run again: a step already done is skipped.
#   1. a rehearsal that publishes nothing: counsel's patch is applied to main in a scratch checkout, and the
#      SPEC.md it leaves must have the hash his grant will name;
#   2. his one grant, entered only after the lane has been quiet for three rounds running (it waits for that,
#      up to 8 hours);
#   3. the builder's branch, made from main with counsel's patch as its one commit, applied by his hand (his
#      cherry-pick), and published.
# It acts under no party's key and removes no work of the court: the grant is his entry and the branch is his.
# It opens nothing: the opening is another paste, after 30 November. After it, counsel files the builder's session.
#
# What the grant says, and what counsel tells him of it before he pastes:
#   - that he read transcripts/BRIEF-C2a-3-draft.md at the hash named below and approved it unchanged;
#   - the replay table's hash, and the one mark: at each row whose log holds an entry after his veto of
#     seq 7180, the lines from the window's line to the last, the overdue-forecast lines apart;
#   - the hash of SPEC.md as counsel's patch leaves it, at the grant's start, as his grant of seq 6851 began;
#   - the cap at C2a-3's opening, 9100, and what else that number holds;
#   - that the two fixes of 23 November stand on main without their pins until C2a-3 has ended.
set -u
R=renavondata/jack; RR=renavondata/opencode-runner
BR=a5c331b40d1e81f959e147461884b3a55e11d829933bfd2296d660a526433945
TB=943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77
S0=72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2
SP=c4a5b44b8465f4be9cd4a5bbeb294cfd5c56a7397319e7f1c167853d7fd628a7
PC=f6d6db7dbf79e7bfb86372a771af8884951d9740
NB=opening-c2a-3
G="promote_unmet: SPEC.md $SP; table spec/vectors/promotion-replay-c2a-3.json $TB. A2.10 for BRIEF-C2a-3: before entering this I read transcripts/BRIEF-C2a-3-draft.md at sha256 $BR and approved it unchanged. The table's one mark, as that file's section The code states it, and no other: at every row whose log holds an entry after my veto of seq 7180 (2026-11-22T11:44:05Z), the lines from the one that begins window C2a: to the last are marked, the lines that begin overdue forecast apart. I state that the cap at C2a-3's opening is 9100, which also holds at most 55 lines for the pins fix before the opening and at most 82 for the merge fix and three pins after the window. The two fixes of 23 November stand on main without their pins until C2a-3 has ended."
die() { echo "Stopped: $*"; echo "Send counsel everything printed above before pasting anything again."; exit 1; }
on_main() { git show "origin/main:$1" | sha256sum | cut -c1-64; }
texts_on_main() {
  [ "$(on_main transcripts/BRIEF-C2a-3-draft.md)" = "$BR" ] || die "BRIEF-C2a-3-draft.md on main is not the text named here"
  [ "$(on_main spec/vectors/promotion-replay-c2a-3.json)" = "$TB" ] || die "the replay table on main is not the one named here"
  [ "$(on_main SPEC.md)" = "$S0" ] || die "SPEC.md on main is not the text counsel's patch was written on"
}
# Counsel's patch applied to origin/main in the checkout $1: one commit, two files, and the SPEC.md named above.
patched() {
  ( cd "$1" && git cherry-pick "$PC" > /dev/null 2>&1 ) || return 1
  [ "$(sha256sum < "$1/SPEC.md" | cut -c1-64)" = "$SP" ] || return 1
  [ "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["cap"])' "$1/judge/scope.json")" = 9100 ] || return 1
  [ "$(git -C "$1" diff --name-only origin/main HEAD | sort | tr '\n' ' ')" = "SPEC.md judge/scope.json " ] || return 1
  [ "$(git -C "$1" rev-list --count origin/main..HEAD)" = 1 ]
}

cd ~/git/jack-guy || die "there is no ~/git/jack-guy"
git switch -q main || die "cannot switch to main"
[ "$(gh api user --jq .login)" = gfrmin ] || die "gh is not signed in as gfrmin"
git pull -q --ff-only || die "main does not fast-forward"
[ -z "$(git status --porcelain)" ] || die "the tree is not clean"
git fetch -q origin main counsel/c2a-3-patch || die "cannot fetch main and counsel's patch"
[ "$(git rev-parse origin/counsel/c2a-3-patch)" = "$PC" ] || die "counsel/c2a-3-patch is not at the commit named here"
W=~/.cache/jack-c2a-3-read.$$
mkdir -p ~/.cache || die "cannot make ~/.cache"

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

if git show origin/main:log.jsonl | grep -qF "$G"; then
  echo "1. skipped: the grant is already on main"
  echo "2. already on main: ${G%%. A2.10*}"
else
  # 1. The rehearsal: nothing is published and no branch is made.
  texts_on_main
  git worktree add -q --detach "$W" origin/main || die "cannot make the scratch checkout"
  if patched "$W"; then ok=1; else ok=0; fi
  git worktree remove --force "$W"; git worktree prune
  [ "$ok" = 1 ] || die "counsel's patch does not leave the SPEC.md named here on today's main, so the grant was not entered"
  echo "1. rehearsed: counsel's patch on main leaves SPEC.md at $SP"

  # 2. The grant.
  quiet || die "waited 8 hours and the lane was never quiet for three rounds running, so the grant was not entered"
  git pull -q --ff-only || die "main does not fast-forward before the grant"
  texts_on_main
  tools/jack decision grant "$G" || die "the grant was refused"
  git pull -q --ff-only || die "main does not fast-forward after the grant"
  git show origin/main:log.jsonl | grep -qF "$G" || die "the grant is not on main"
  echo "2. entered: ${G%%. A2.10*}"
fi

# 3. The builder's branch: main with counsel's patch as its one commit, by his cherry-pick.
git fetch -q origin main || die "cannot fetch main"
if git ls-remote --exit-code origin "refs/heads/$NB" > /dev/null 2>&1; then
  git fetch -q origin "$NB" || die "cannot fetch $NB"
  [ "$(git show FETCH_HEAD:SPEC.md | sha256sum | cut -c1-64)" = "$SP" ] || die "$NB is published and its SPEC.md is not the one the grant names"
  echo "3. already published: $NB"
else
  git worktree add -q -B "$NB" "$W" origin/main || die "cannot make the branch's checkout"
  if patched "$W"; then ok=1; else ok=0; fi
  if [ "$ok" = 1 ]; then git -C "$W" push -q origin "$NB" || ok=2; fi
  H=$(git -C "$W" rev-parse HEAD)
  git worktree remove --force "$W"; git worktree prune
  [ "$ok" != 0 ] || die "the grant is on main, and counsel's patch no longer leaves the SPEC.md it names; nothing was published"
  [ "$ok" != 2 ] || die "the grant is on main, and the branch $NB could not be pushed"
  [ "$(git ls-remote origin "refs/heads/$NB" | cut -f1)" = "$H" ] || die "$NB on jack is not the commit made here"
  echo "3. published: $NB at $H"
fi
echo
echo "Done: the grant is on main and the builder's branch is published. Counsel now files the builder's session."
