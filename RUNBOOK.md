# Runbook — Guy's verbs on jack

Each verb is a fixed command sequence. Anything not here is not a verb and is done by a proposal.
`Proposer:` is the last paragraph of a commit message; git reads only the last paragraph.

## room — a cold reading by another family
```
cd ~/git/jack && git fetch origin && R=~/git/<name>-room && rm -rf "$R" && mkdir -p "$R"
git archive <ref> <the files the reader needs> | tar -x -C "$R"
git diff "$(git merge-base origin/main <ref>)" <ref> > "$R/DIFF.patch"
git -C "$R" init -q && git -C "$R" add -A && git -C "$R" -c user.name=room -c user.email=room@invalid commit -qm room
```
The prompt gives the text the code must match and asks whether it does, and whether the named pins kill
their mutants; the answer is a file, nothing else is written.

## build — a builder session on a branch
```
cd ~/git/jack && git pull --ff-only && git worktree add ~/git/jack-build-<name> -b <branch> main
```
The prompt names the text to build to, the paths it may touch, the tests to run, and the trailer
`Proposer: builder <model id> <session id>` as the last paragraph. The builder does not push.

## check
```
python3.12 -m unittest discover -s tests -t . && python3.12 pins/run.py | tail -1
```

## propose — a pull request (untrusted paths)
```
git push -u origin <branch>
gh pr create -R renavondata/jack --base main --head <branch> --title "<title>" --body "<text>"
```
If main has moved, bring it in by a merge of your own, never the button:
`git merge origin/main -m "Merge main into <branch>" -m "Proposer: guy" && git push`.

## merge
```
gh pr checks <n> -R renavondata/jack --watch && gh pr merge <n> -R renavondata/jack --merge
git -C ~/git/jack worktree remove ~/git/jack-build-<name>
```

## land — the trusted base, by your own push, after reading the diff
```
cd ~/git/jack && git switch main && git pull --ff-only && git merge --ff-only <branch> && git push
gh run list -R renavondata/jack --branch main -L 1
```

## record — the run of record (SPEC §9a), twelve ways
```
T=$(date -u +%Y%m%dT%H%MZ); for i in $(seq 0 11); do A=$((i*8334)); B=$(( (i+1)*8334 )); [ $B -gt 100000 ] && B=100000; nohup python3.12 harness/diff.py --seeds $A:$B --b kernel2/check > "transcripts/diff-100000-$T-part$(printf %02d $i).json" 2> "/tmp/diff-part$i.log" & done
```
Then the sum over the parts: logs 100000, disagreements 0, uncompared 0, ranges without gap, one commit.

## promote — a layer boundary (CHARTER §6, §7)
```
git switch main && git pull --ff-only
git -c gpg.format=ssh -c user.signingkey=~/.ssh/id_ed25519.pub tag -s <layer>-exit -m "<decision and rulings>" && git push origin <layer>-exit
```
Until C1, a tag outside the log; afterwards an entry.

## Never
`--admin`; force-push; deleting a remote branch; editing a builder's branch by hand; `key` entries before
C1's guard; a `Proposer:` trailer that is not the last paragraph.
