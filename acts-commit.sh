#!/bin/bash
# Counsel's acts evidence for C2a-3 (BRIEF-C2a-3 §The acts evidence): the attributed table by the committed classifier
# and its raw twin by the committed collector, over exactly the window from its opening push to END, on a counsel
# branch with the classifier's hash file and a request record; the sign request is a separate step (a guard).
# usage: acts-commit.sh <END as YYYY-MM-DDTHH:MM:SSZ>
set -u
END=${1:?END}
REPO=/home/claude/jack-complete
CLS=ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b   # guy_acts3.py, as the brief names it
TRAILERS=$'Model: anthropic/claude-opus-5-5\nProposer: counsel claude-opus-5-5 session_01VpB3Tknxi9JkERuANTGHDk\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01VpB3Tknxi9JkERuANTGHDk'
die() { echo "stopped: $*"; exit 1; }
cd "$REPO" && git fetch -q origin main || die "fetch"
OPEN=$(git show origin/main:log.jsonl | python3 -c '
import json, sys
es = [json.loads(l) for l in sys.stdin]
p = [e for e in es if e["type"] == "push" and e["ts"] > "2026-11-30T00:00:00Z"]
print(p[0]["ts"] if p else "")')
[ -n "$OPEN" ] || die "no opening push on main's log"
[[ "$END" > "$OPEN" ]] || die "END $END is not after the opening $OPEN"
E=$(echo "$END" | tr -d ':-'); NAME="c2a-3-acts-$E"; BR="counsel/$NAME"; WT=/home/claude/wt-$NAME
git worktree prune; [ -e "$WT" ] && die "$WT exists"
git worktree add -q -B "$BR" "$WT" origin/main || die "worktree"
cd "$WT" || die "cd"
[ "$(sha256sum < transcripts/evidence/guy_acts3.py | cut -c1-64)" = "$CLS" ] || die "the classifier on main is not the one the brief names"
[ "$(sha256sum < transcripts/evidence/guy_acts2.py | cut -c1-64)" = "$(tr -d ' \n' < transcripts/evidence/guy_acts2.sha256)" ] || die "the collector does not match its hash file"
A="transcripts/evidence/acts-c2a3-$E.csv"; RAW="transcripts/evidence/acts-c2a3-$E-raw.csv"
python3 transcripts/evidence/guy_acts3.py renavondata/jack . "$OPEN" "$END" "$A" || die "the classifier failed"
python3 transcripts/evidence/guy_acts2.py renavondata/jack . "$OPEN" "$END" "$RAW" || die "the collector failed"
[ -e transcripts/evidence/guy_acts3.sha256 ] || echo "$CLS" > transcripts/evidence/guy_acts3.sha256   # the form of guy_acts2.sha256: the hash alone
echo "repair rows: $(grep -c ',repair,' "$A")"; grep ',repair,' "$A"
printf '{"verb": "proposal", "title": "acts evidence of C2a-3, %s to %s (BRIEF-C2a-3 \\u00a7The acts evidence): attributed and raw tables"}\n' "$OPEN" "$END" > "transcripts/requests/$NAME.jsonl"
git add -A transcripts && git -c user.name=counsel -c user.email=counsel@jack.invalid commit -q -m "acts evidence of C2a-3 to $END: attributed and raw tables (BRIEF-C2a-3, The acts evidence)" -m "$TRAILERS" || die "commit"
echo "branch $BR at $(git rev-parse --short=8 HEAD); files: $(git diff --name-only origin/main | tr '\n' ' ')"
echo "push with: git -C $WT push -q origin HEAD:refs/heads/$BR   (then the sign guard)"
