# tools/jack: sentences of RUNBOOK.md that cannot be implemented as written

The build of `tools/jack` stopped here. Both points below are about `jack push`. In each, a general rule in
"Common to every verb" refuses something that `jack push`'s own section requires. If `tools/jack` keeps the
rule, `jack push` can never run. If it drops the rule for `push`, the code is choosing an exception the text
does not state. Nothing has been built, and no tests were changed to fit either reading.

## 1. `push` is a main verb, but it runs off `main`

- RUNBOOK.md:13–14: verbs run "in the working copy they act on (… the `main` checkout for main verbs)".
- RUNBOOK.md:27: every verb "refuses … off `main` for main verbs".
- RUNBOOK.md:33: "**Main verbs** (`key`, `push`, `decision`, `amend`, `merge`)".
- RUNBOOK.md:77: `jack push BRANCH` "Runs inside BRANCH's worktree, with `main` checked out in the
  repository's main working copy". BRANCH is never `main`, because it "contains `origin/main`" and must have
  a different digest.

Taken together, line 27 refuses every call that line 77 describes. A related point: line 33's ending
("commit, `judge/selfcheck.py`, `git push origin main`, then `gh run watch`") is not `push`'s own ending
(RUNBOOK.md:89–92). That ending commits on BRANCH, runs the self-check on BRANCH, and fast-forwards `main` in
another working copy.

Possible fix: take `push` out of the main-verb list on lines 14, 27 and 33 and give it a class of its own.
It would run on BRANCH (not `main`), with `main` checked out in the main working copy, and end as its own
section says.

## 2. `push` edits a branch the caller's key did not propose

- RUNBOOK.md:29–30: "Refused in code, always: … editing a branch the caller's key did not propose".
- RUNBOOK.md:43: `push` is held only by the master key ("the master key holds the rest").
- RUNBOOK.md:80–81: BRANCH's commits need only "a filled `Proposer:` trailer", from any party.
- RUNBOOK.md:89: "Effect: commits `log.jsonl` and `transcripts/` on BRANCH".
- RUNBOOK.md:122: the kernel2 author's "work enters by `jack push`".

When the master key pushes a branch that another party built (the case on line 122), the commit on line 89
edits a branch the caller's key did not propose. The "always" rule refuses that commit.

A second problem, smaller but in the same rule: the code cannot tell which *key* proposed a branch. The only
evidence in git is the `Proposer:` trailers. RUNBOOK.md:25 fixes their form only for verb commits
(`<party> <key_id>`). Work commits in practice carry `Proposer: <party> <model> <session>`, which names a
party and no key. So the most this rule can enforce is "party". Whether that is enough depends on the rule
of one key per party (RUNBOOK.md:42–43) still holding.

Possible fix: state that `push`'s commit on BRANCH is the one permitted edit of another party's branch. Also
say whether "the caller's key" is checked by the party in each commit's trailer, or by a key-bearing trailer
that the RUNBOOK requires on work commits too.

## Readings the build would have taken (not conflicts, recorded so the next build does not have to guess)

- `jack spec_conflict` is "on a branch, as `proposal`". The build reads this as the branch preconditions
  only, without the check. The builder files a conflict precisely when it cannot make the tests pass (A2
  clause 9).
- The commit summaries the text leaves open would be: `key: <KEY_ID>`, `decision: <KIND> <SUBJECT>` and
  `merge: #<N>`. For `push: <summary>`, a `--summary` flag that defaults to BRANCH head's subject, the same
  default `proposal` uses for `title`.
- `jack push`'s `--remove` (RUNBOOK.md:92) is a flag, although the verb's heading on line 75 does not list it.
