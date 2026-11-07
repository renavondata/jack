# The counsel courier — definition (counsel's text, 7 November 2026)

This is the definition of the job that makes counsel's acts on steel. It lives here, in the court, so that a
change to how counsel's acts are made is a proposal read like any other, not a file on a machine (the same
reason `transcripts/sessions/` holds the session prompts). Until `renavondata/opencode-runner` fetches it
from `main`, the sovereign installs it there by hand, which is a repair by §7's letter and is listed as one.
It replaces the courier of 6 November (`counsel.yml`, opencode-runner #335) for counsel's proposals; the
`assize-reviewer` grant of seq 2131 covers everything it does on GitHub.

## What it holds

- `~/.ssh/jack-counsel-3` (private; generated on steel; never in a prompt, a chat or a repository).
- `GH_TOKEN` for `assize-reviewer`, scoped as the grant says: on `renavondata/jack`, opening counsel's
  proposals and closing its own stale ones with a comment; on `renavondata/opencode-runner`, filing and
  closing issues.

## When it runs

On the diary's tick (every ten minutes), and on `workflow_dispatch`. It is level-triggered: it reads state
and acts on it; it waits for no event.

## What it does, in order, for each remote branch `counsel/*` of `renavondata/jack`

1. `git fetch origin`; take the branch's head and its last content commit (the last commit changing a path
   other than `log.jsonl`, as `jack proposal` defines it).
2. If the branch's `log.jsonl` has a `proposal` entry whose `commit` is that content commit: done; nothing.
3. Else read `transcripts/requests/<name>.jsonl` at the head, where `<name>` is the branch's name after
   `counsel/`. Missing, malformed, a verb other than `forecast` or `proposal`, or `proposal` not the last
   line or absent: report on the diary's issue and skip.
4. Otherwise, in a fresh worktree of the branch (`~/git/worktrees/jack/<name>`), with
   `JACK_KEY=~/.ssh/jack-counsel-3` and `gh` as `assize-reviewer`: run each `forecast` line as
   `tools/jack forecast "<claim>" --p <p> --by <by> [--type <type> --args '<args>']`, one at a time, each
   after the last has printed; then `tools/jack proposal --title "<title>"`. The verbs push the branch and
   open the pull request. A refusal stops the request at that line; the refusal is reported verbatim; nothing
   is retried and nothing is forced.
5. Report one line per branch on the diary's issue: branch, request lines run, entries' seqs, PR number, or
   the refusal.

## What it never does

Sign anything not in the request file; run a verb other than the two; touch `main`; close or label anything
but counsel's own stale proposals (the stale watcher's existing job); read `log.jsonl` whole into a model.

## Reference script

```bash
#!/usr/bin/env bash
# counsel-courier.sh — run on steel by the counsel workflow; see counsel-courier.md
set -euo pipefail
export JACK_KEY="$HOME/.ssh/jack-counsel-3"
R="$HOME/git/jack"; W="$HOME/git/worktrees/jack"
git -C "$R" fetch -q origin
for ref in $(git -C "$R" for-each-ref --format='%(refname:short)' 'refs/remotes/origin/counsel/*'); do
  branch="${ref#origin/}"; name="${branch#counsel/}"
  content=$(git -C "$R" log --format=%H -n 200 "$ref" -- . ':!log.jsonl' | head -1)
  if git -C "$R" show "$ref:log.jsonl" | grep -q "\"commit\":\"$content\""; then continue; fi
  req="transcripts/requests/$name.jsonl"
  if ! git -C "$R" cat-file -e "$ref:$req" 2>/dev/null; then echo "$branch: no $req"; continue; fi
  rm -rf "$W/$name"; git -C "$R" worktree prune
  git -C "$R" worktree add -q "$W/$name" -B "$branch" "$ref" || { echo "$branch: worktree failed"; continue; }
  (
    cd "$W/$name"
    git branch -q --set-upstream-to="$ref" "$branch"
    n=0
    while IFS= read -r line; do
      verb=$(printf '%s' "$line" | python3 -c 'import sys,json; print(json.load(sys.stdin)["verb"])')
      case "$verb" in
        forecast)
          args=$(printf '%s' "$line" | python3 -c '
import sys,json,shlex; o=json.load(sys.stdin)
a=["tools/jack","forecast",o["claim"],"--p",str(o["p"]),"--by",o["by"]]
if "type" in o: a+=["--type",o["type"]]
if "args" in o: a+=["--args",json.dumps(o["args"],separators=(",",":"))]
print(" ".join(shlex.quote(x) for x in a))')
          eval "$args" ;;
        proposal)
          title=$(printf '%s' "$line" | python3 -c 'import sys,json; print(json.load(sys.stdin)["title"])')
          tools/jack proposal --title "$title" ;;
        *) echo "$branch: refused: verb $verb"; exit 3 ;;
      esac
      n=$((n+1))
    done < "$req"
    echo "$branch: $n request lines run"
  ) || echo "$branch: stopped (see above)"
done
```

Knobs the installer must set from the existing `counsel.yml`: the runner label, the token secret's name,
the diary issue to report on, and the stale watcher's hand-over. Nothing else in this definition depends on
the runner's layout.
