#!/bin/bash
# Adviser's further cases for counsel's paste c2a-3-read.sh as revised for R39 (ADVISER.md entry 286; R19).
# Usage: P286-read-hand.sh <a clone of jack, as P281-read-sandbox.sh asks> <ADVISER.md> <number of the entry that
#        gives the line he would paste>
# It runs P283's cases a to w first, on the paste as origin/agent/pastes holds it, and then x, y and z: a branch of
# the builder's name that is found published after his grant is on main.
# Nothing here reaches GitHub, signs anything or uses a key.
HERE=$(dirname "$(readlink -f "$0")")
source <(sed '$d' "$HERE/P283-read-guard.sh") "$1" "$2" "$3"      # P283 without its last line, which removes the copy
clear_counts() { : > $SB/state/calls; : > $SB/state/sleeps; }

# x: his grant is on main and no branch is (as case n leaves it); then the name stands at counsel's own commit.
reset; printf '#!/bin/sh\ncase "$*" in *opening-c2a-3*) exit 1;; esac\n' > $SB/origin.git/hooks/update; chmod +x $SB/origin.git/hooks/update
run "x0. the grant is entered and the branch's push is refused (as n)" > /dev/null
rm -f $SB/origin.git/hooks/update; git -C $SB/origin.git update-ref refs/heads/opening-c2a-3 $PATCH; clear_counts
run "x. after his grant, a branch of that name stands at counsel's own commit"

# y: the same, but the name holds another hand's cherry-pick of the patch on main: the right SPEC.md, the wrong hand.
git -C $SB/origin.git update-ref -d refs/heads/opening-c2a-3
other; git checkout -q -b opening-c2a-3 origin/main; git cherry-pick $PATCH > /dev/null 2>&1; git push -q origin opening-c2a-3; cd /; clear_counts
run "y. after his grant, another hand's cherry-pick of the patch is published under that name"

# z: his own publication, then a builder's commit on the branch and a commit on main; pasted again.
reset; run "z0. the whole path on a quiet lane" > /dev/null
other; git checkout -q opening-c2a-3; echo '# built' >> judge/status.py; git commit -qam 'a commit of the builder'; git push -q origin opening-c2a-3
git checkout -q main; echo x >> README.md; git commit -qam 'main moves'; git push -q origin HEAD:main; cd /; clear_counts
run "z. pasted again after a builder's commit on the branch and a commit on main"
rm -rf $SB
