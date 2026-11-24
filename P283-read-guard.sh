#!/bin/bash
# Adviser's further cases for counsel's paste c2a-3-read.sh as revised (ADVISER.md entry 283; R19).
# Usage: P283-read-guard.sh <a clone of jack, as P281-read-sandbox.sh asks> <ADVISER.md> <number of the entry that
#        gives the line he would paste>
# It runs P281's fifteen cases first, on the paste as origin/agent/pastes holds it, and then cases p to w:
# the guard against counsel's other paste, the line he would paste, a branch of the builder's name that another
# hand publishes while the paste waits, and one that another hand published with the patched SPEC.md.
# Nothing here reaches GitHub, signs anything or uses a key.
# Run it from a shell whose own command line does not hold the other paste's path, or the guard finds that shell.
HERE=$(dirname "$(readlink -f "$0")"); ADV=$(readlink -f "$2"); ENTRY=$3; REPO2=$(readlink -f "$1")
source <(sed '$d' "$HERE/P281-read-sandbox.sh") "$1"      # P281 without its last line, which removes the copy
REALPATH=$PATH

# p, q: the guard.
mkdir -p $SB/home/.cache; printf '#!/bin/bash\nsleep 300\n' > $SB/home/.cache/jack-paste.sh
reset; bash $SB/home/.cache/jack-paste.sh & OP=$!; sleep 1
run "p. counsel's other paste is still running here (a stand-in: bash <home>/.cache/jack-paste.sh)"
pkill -P $OP; kill $OP 2>/dev/null; wait $OP 2>/dev/null
run "q. pasted again once that one has ended"

# r: no pgrep. Every program on PATH but pgrep, by links.
mkdir $SB/np; IFS=: read -ra D <<< "$REALPATH"
for d in "${D[@]}"; do for f in "$d"/*; do b=${f##*/}; [ "$b" = pgrep ] || [ -e "$SB/np/$b" ] || ln -s "$f" "$SB/np/$b" 2>/dev/null; done; done
reset; PATH=$SB/np; run "r. pgrep is not on the machine"; PATH=$REALPATH

# s, t: the line he would paste, as the entry gives it.
LINE=$(awk -v n="$ENTRY" '$1=="###" && $2==n {on=1} on' "$ADV" | grep -m1 '^cd ~/git/jack-guy && mkdir -p ~/.cache && git fetch -q origin agent/pastes && git show FETCH_HEAD:c2a-3-read.sh')
[ -n "$LINE" ] || { echo "entry $ENTRY gives no such line"; exit 1; }
echo "the line of entry $ENTRY: $(printf '%s' "$LINE" | wc -c) characters; it names the paste $(printf '%s' "$LINE" | grep -o -E '= [0-9a-f]{64} ' | cut -c3-18)"
git -C "$REPO2" push -q $SB/origin.git refs/remotes/origin/agent/pastes:refs/heads/agent/pastes
eval "$(declare -f run | sed -e '1s/^run /runline /' -e 's|bash \$SB/paste.sh|bash -c "$LINE"|')"
[ "$(declare -f runline | grep -c 'bash -c "$LINE"')" = 1 ] || { echo "cannot make runline"; exit 1; }
reset; runline "s. the line he would paste, on a quiet lane"
echo "   the file it ran: $(sha256sum < $SB/home/.cache/jack-paste-read.sh | cut -c1-16)"
reset; other; git checkout -q -b ap origin/agent/pastes; echo '# changed' >> c2a-3-read.sh; git commit -qam t; git push -q origin HEAD:agent/pastes; cd /
runline "t. the same line when agent/pastes holds another file under that name"

# u, v: another hand publishes a branch of the builder's name while the paste waits (after its test, before the grant).
cp $SB/bin/sleep $SB/sleep.p281
cat > $SB/bin/sleep <<'SH'
#!/bin/bash
echo s >> $SB/state/sleeps
if [ "$(wc -l < $SB/state/sleeps)" = 1 ]; then
  rm -rf $SB/other; git clone -q $SB/origin.git $SB/other; cd $SB/other; git config user.name x; git config user.email x@example.invalid
  git checkout -q -b opening-c2a-3; echo x >> README.md; git commit -qam 'another hand publishes the branch'; git push -q origin opening-c2a-3
fi
SH
reset; printf '1\n0\n0\n0\n' > $SB/state/prs_seq; run "u. a branch of that name is published without the patch while the paste waits"
: > $SB/state/calls; : > $SB/state/sleeps; run "v. pasted again after u"
cp $SB/sleep.p281 $SB/bin/sleep

# w: a branch of that name already published by another hand, holding the patched SPEC.md (counsel's own commit).
reset; git -C $SB/origin.git update-ref refs/heads/opening-c2a-3 $PATCH
run "w. a branch of that name is already published at counsel's own commit, not by his cherry-pick"
rm -rf $SB
