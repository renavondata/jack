# The monitor — definition (counsel's text, draft v1, 7 November 2026; CHARTER A2.8)

A2.8 says three things: the head hash of the log is published on every push; a monitor that the owner does not operate verifies that each published hash extends the last and that both checkers accept the log; and it writs Guy on any failure. The first and third are code this text is written to; the second is partly a fact about who runs the code, and this text says which part.

## Publication (jack's own CI; a trusted-base change, so by `push`)

A step in `.github/workflows/tests.yml`, on every push to `main`, after the checkers pass: append one line `<seq> <head hash> <commit> <instant>` to the file `HASHES` on the branch `hashes` of `renavondata/jack`, with the workflow's own token (contents: write, this repository only). The ruleset on `hashes` refuses force-pushes and deletion as `main`'s does. The line is the kernel's head hash of `log.jsonl` at that commit (`python3 -m kernel.check` prints it). Nothing else writes to `hashes`. Residue: the owner can bypass the ruleset as he can on `main` (`enforce_admins` off, REPORT.md §8.1); the published line is as strong as the ruleset.

## Verification (the verifier; a public script, run by whoever runs it)

`tools/runner/verify.py` (a builder's, written to this text), run on a schedule by a workflow in a public repository that is not `renavondata/jack`:

1. Clone `renavondata/jack` at `main` and fetch `hashes`.
2. Run both checkers over `log.jsonl`; refuse unless both print `ok` with the same head hash.
3. Read `HASHES`: every line's seq exceeds the previous; the last line's hash equals the head hash and its commit is on `main`'s first-parent history; every earlier line's hash is the head hash of the log at that line's commit (a prefix of today's log — recomputed, not trusted).
4. Append the verdict to the verifier's own record (a file in its repository: instant, `main`'s commit, the hash checked, `ok` or the failure).
5. On any failure, file one issue on `renavondata/jack` titled `monitor: <failure>` with the verdict — the writ — under the account the verifier runs as.

## Who runs it

The script is public and its workflow is a template anyone can install in a repository of their own with an account of their own. The first instance runs under `assize-reviewer` from `renavondata/opencode-runner`'s `main` on GitHub-hosted runners — which is the owner's account on the owner's repository, so A2.8's "a monitor that the owner does not operate" is **not met** by it, and the enforcement map says so (`A2.8-operator: hand`). It is met when a run under an account the owner does not hold is on the verifier's record; the report names the account and the date, and until then says that none has run it. The book's ch 12 §12.4 states the same residue and keeps stating it.

## Evidence the window file names

`transcripts/evidence/monitor-<stamp>.json`: the verifier's record copied into the court by a builder session (read-only `gh api` on the verifier's repository), with the account it ran under; B7's test reads it.
