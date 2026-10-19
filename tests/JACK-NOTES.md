# tools/jack: sentences of RUNBOOK.md that cannot be implemented as written (second round)

The two findings of the first round are resolved: `push` now runs on `main`, and it never commits to BRANCH.
The build of `tools/jack` stopped again on a full re-read of the corrected text, before any code was written.
The first finding below is a direct contradiction. The other two are cases where one rule covers ground that
another rule says differently, and the code would have to choose. No tests were written to fit any reading.

(The ledger rule, RUNBOOK.md:39–40, says that a builder's objection is a `spec_conflict` entry, not a note.
This file is a note because the instruction for this build says that a conflict goes here, committed alone.)

## 1. `merge`'s effect happens on the remote, so the remote shows it before the entry

- RUNBOOK.md:35–37: "Where a verb's effect precedes its entry (`merge`, `push`), the effect and the entry are
  two local commits sent in one push, so the remote never shows the one without the other."
- RUNBOOK.md:75: "Effect, in this order: `gh pr merge N --merge`; `git pull --ff-only`; entry `merge` …"

`gh pr merge` makes the merge commit on GitHub, so it is not a local commit. From the moment it returns until
`git push origin main`, the remote shows the merge without its entry. If the self-check then fails, the
`git reset --hard origin/main` of line 31 undoes only the local entry commit. The merge stays on the remote
with no entry, for good. Both lines cannot be followed together.

Possible fix: write `merge`'s effect as a local merge, the way `push`'s is. That would be `git fetch origin
pull/N/head`, then `git merge --no-ff FETCH_HEAD` with the message `gh pr merge` would have used, then the
entry, then one push. GitHub marks the pull request merged once its head is reachable from `main`. The
alternative is to drop `merge` from line 36 and say that its remote effect comes first.

## 2. The undo after a failed self-check, applied to branch verbs, discards the branch

- RUNBOOK.md:29–32: "Refused in code, always: … rewriting any commit (a verb only appends commits, and only
  to the branch it runs on); running on a tree whose `judge/selfcheck.py` fails after the commit (the commits
  are undone with `git reset --hard origin/main` …)".
- RUNBOOK.md:41: "Branch verbs (`proposal`, `spec_conflict`) never touch `main`."

The "always" list covers every verb, so `proposal` and `spec_conflict` must also run the self-check after
their commit. On a branch, `git reset --hard origin/main` points the branch at `main`, which throws away the
builder's work commits along with the verb's own commit. That is the rewrite the same bullet forbids. The
sections for `proposal` and `spec_conflict` do not mention the self-check at all.

Possible fix: say that branch verbs undo with `git reset --hard @{u}` when the branch has an upstream, or
otherwise `git reset --hard HEAD~1`. Or limit the self-check refusal to main verbs, where line 34 already
lists it.

## 3. The run of record is evidence that no entry references by hash

- RUNBOOK.md:38–39: "every piece of evidence is referenced from an entry by hash (`push.digest`,
  `push.review`); files under `transcripts/` are evidence".
- RUNBOOK.md:94–96: `push` copies "the run's parts and the review … into `transcripts/`", and its entry is
  "`push` {digest: `tools/digest.py` of the tree now on `main`, review}".

`push.digest` covers only the trusted base (`kernel/`, `kernel2/`, `judge/`, `.github/workflows/`,
`SPEC.md`), and `push.review` covers only the review. The twelve `diff-…-partNN.json` files are evidence under
`transcripts/` that `push` itself places there, but no hash in any entry covers them. Adding a member would
satisfy the ledger rule but change the entry the `push` section fixes. Keeping the entry as written breaks
the rule. (SPEC allows extra body members, so either reading passes the kernel.)

Possible fix: add a member to `push`, for example `run`: the SHA-256 of the twelve parts concatenated in part
order, or 64 zeros when no run was required. Or say that the run's parts are exempt because `digest` pins
the checker sources they were made from.

## Readings a rebuild would take (not conflicts, recorded so the next build does not have to guess)

- `spec_conflict` is "on a branch, as `proposal`". This reads as the branch preconditions only, without the
  check, because a conflict is filed exactly when the tests cannot be made to pass (A2 clause 9).
- Commit summaries the text leaves open: `key: <KEY_ID>`, `decision: <KIND> <SUBJECT>`, `merge: #<N>`, and
  `push: <BRANCH>`.
- "Up to date with `origin/main`" means `git fetch origin` and then `HEAD` equals `origin/main`. Branch verbs
  fetch before testing whether the branch contains `origin/main`.
- `--dry-run` for `push` prints the preconditions it would evaluate and does not create the temporary
  worktree.
