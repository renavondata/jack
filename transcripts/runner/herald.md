# The herald — definition (counsel's text, C2c-1; today `.github/workflows/herald.yml`)

## What it holds
`~/.ssh/jack-herald` (key_id `herald-2`, power `merge`); `~/git/jack`; the App's identity for `gh`.

## When it runs
Every ten minutes, and on dispatch. One at a time (concurrency group `herald`).

## What it does, in order, for each open pull request against `main`, oldest first
1. Fetch its head; read the last entry of its `log.jsonl`. A draft is skipped.
2. If the last entry is a `merge`: if `main`'s log is no longer a prefix of the head's, close it as stale with the declaration BRIEF-C1b Amendment 2 reads and dispatch `repropose` for a builder's or reviewer's branch; else if the judge and tests on that head are both `success`, complete the merge GitHub was waiting for (`gh pr merge --match-head-commit`) and pull `main`; else wait.
3. If the last entry is a `proposal`: if `main`'s log is no longer a prefix, close as stale and dispatch `repropose`; if the judge and tests on the head are not both `success`, skip; else `tools/jack merge N` under the herald's key — the verb signs the merge entry, pushes it to the branch, waits for the checks on that head, merges exactly that head, pulls `main`. A `CONFLICTING` refusal closes the PR as stale and dispatches `repropose`.
4. Anything else as the last entry: skip, saying what it was.
5. Prune worktrees; sweep this user's stale temp directories older than an hour.

## What it never does
Decide anything about a proposal's merit; merge a head the judge has not admitted; force, rebase or delete; act under the owner's login where the App's files exist.
