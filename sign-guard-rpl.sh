#!/bin/bash
set -u
: "${DEADLINE:?set DEADLINE to a Unix time first}"
WT=/home/claude/wt-replay; RUN=/home/claude/opencode-runner; BR=counsel/c2a-3-replay-session
TODAY=$(date -u +%Y-%m-%d)
TRAILERS=$'Model: anthropic/claude-opus-5-5\nProposer: counsel claude-opus-5-5 session_01VpB3Tknxi9JkERuANTGHDk\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01VpB3Tknxi9JkERuANTGHDk'
while true; do
  now=$(date -u +%H:%M:%S)
  if [ $(date -u +%s) -gt $DEADLINE ]; then echo "$now past deadline; stop"; exit 2; fi
  prs=$(gh api 'repos/renavondata/jack/pulls?state=open&per_page=50' --jq '[.[].number]|sort|map(tostring)|join(",")')
  rp=$(gh api 'repos/renavondata/opencode-runner/actions/runs?per_page=30' --jq "[.workflow_runs[] | select(.name==\"repropose\") | select(.status!=\"completed\") | select(.created_at > \"$TODAY\")] | length")
  sess=$(gh api 'repos/renavondata/opencode-runner/issues?state=open&per_page=30' --jq "[.[] | select(.pull_request|not) | select(.created_at > \"$TODAY\") | select([.labels[].name]|index(\"run\"))] | length")
  inflight=$(gh api 'repos/renavondata/opencode-runner/actions/workflows/counsel-sign.yml/runs?per_page=10' --jq '[.workflow_runs[] | select(.status!="completed")] | length')
  since=$(date -u -d '-20 minutes' +%Y-%m-%dT%H:%M:%SZ)
  others=0
  for c in $(gh api "repos/renavondata/opencode-runner/commits?sha=counsel-requests&since=$since&per_page=20" --jq '.[].sha'); do
    gh api "repos/renavondata/opencode-runner/commits/$c" --jq '.files[].filename' | grep -q '^requests/sign-' && others=$((others+1))
  done
  echo "$now prs=[$prs] repropose_open=$rp open_run_issues_today=$sess counsel_sign_inflight=$inflight sign_requests_last_20min=$others"
  if [ "$others" != 0 ]; then echo "another sign request in the last 20 minutes; leave the slot"; exit 8; fi
  m=$((10#$(date -u +%M)))   # W5: push and request only outside minutes 07 to 25, clear of the diary's ticks and of steel's fetch
  if [ "$prs" = "125,316,562" ] && [ "$rp" = 0 ] && [ "$sess" = 0 ] && [ "$inflight" = 0 ] && { [ $m -lt 7 ] || [ $m -gt 25 ]; }; then break; fi
  sleep 45
done
cd $WT || exit 3
git status --porcelain | grep -q . && { echo "worktree not clean"; exit 3; }
git fetch -q origin main
if ! git merge-base --is-ancestor FETCH_HEAD HEAD 2>/dev/null; then
  git -c user.name=counsel -c user.email=counsel@jack.invalid merge -q --no-edit -m "Merge main into $BR" -m "$TRAILERS" FETCH_HEAD || { git merge --abort; echo "merge failed"; exit 4; }
fi
files=$(git diff --name-only FETCH_HEAD HEAD | LC_ALL=C sort | tr '\n' ' ')
echo "diff vs main: $files"
[ "$files" = "transcripts/requests/c2a-3-replay-session.jsonl transcripts/sessions/README.md transcripts/sessions/c2a-3-replay.md " ] || { echo "unexpected diff; stop"; exit 5; }
git -c push.negotiate=true push -q origin HEAD:refs/heads/$BR 2>&1 | grep -v '^remote' ; echo "branch pushed: $(git ls-remote origin refs/heads/$BR | cut -f1) local $(git rev-parse HEAD)"
[ $(date -u +%s) -le $(( DEADLINE + 60 )) ] || { echo "deadline passed before request; stop"; exit 6; }
cd $RUN && git fetch -q --depth 5 origin counsel-requests && git checkout -q -B counsel-requests FETCH_HEAD
STAMP=$(date -u +%Y%m%dT%H%M); ID="sign-$STAMP-sign-c2a-3-replay-session"
printf '{"id":"%s","act":"sign","branch":"%s"}\n' "$ID" "$BR" > requests/$ID.json
git add requests/$ID.json && git -c user.name=counsel -c user.email=counsel@jack.invalid commit -q -m "request: sign $BR" -m "$TRAILERS"
[ "$(git ls-remote origin refs/heads/counsel-requests | cut -f1)" = "$(git rev-parse HEAD~1)" ] || { echo "counsel-requests moved; stop"; exit 7; }
git -c push.negotiate=true push -q origin HEAD:counsel-requests 2>&1 | grep -v '^remote'
echo "request $ID pushed at $(date -u +%H:%M:%S): $(git ls-remote origin refs/heads/counsel-requests | cut -f1) local $(git rev-parse HEAD)"
