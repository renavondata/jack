# Build notes: SPEC §10 items 7–10

Places where §10 left a choice open, and what the builder chose.

1. **What "touches" means (items 8, 9).** The report's `touched` uses git's rename
   detection, so a rename shows only its new path. Moving a file from outside
   scope to inside it would then pass. Items 8 and 9 use `git diff --no-renames`
   from the merge base instead, so additions, edits and deletions all count, and a
   rename counts under both of its paths. Pinned by `scope_unguarded/rename_hides_source`.
2. **Which trailer, and what counts as a party (item 7).** The party is the first
   word of the first `Proposer:` value that git's own trailer parser
   (`%(trailers:key=Proposer,valueonly)`) finds in the head commit's message.
   That means the last paragraph only: a subject line or a file in the tree never
   counts. The key is matched case-insensitively, as git does, but the party is
   matched exactly: `Builder` is not `builder`. A trailer that names no listed
   party is `unattributed_proposal`. Nothing after the party is required.
3. **Where scope.json is read.** It is read from trunk's commit. Item 1 has already
   made the proposal's copy byte-identical, so this changes nothing except that
   the proposal never supplies it. If trunk has no scope.json, the judge exits 2
   (a judge error).
4. **What the cap counts (item 10).** Every counted `.py` file in the head tree,
   not only the files the diff changes ("at the proposal's head").

**A consequence, left unchanged.** `judge/selfcheck.py` judges `HEAD` against
itself, so item 7 now needs `HEAD`'s message to carry a trailer. GitHub's merge
commits ("Merge pull request #N …") and the synthetic `refs/pull/N/merge`
checkout that `pull_request` CI runs on carry none, so the self-check will refuse
them with `unattributed_proposal`. That is Guy's call: a merge style that keeps
the trailer, or a self-check that judges the merged proposal head.
