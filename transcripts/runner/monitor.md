# The monitor — definition (counsel's text, draft v2, 7 November 2026, after one read: runner issue #376; CHARTER A2.8)

A2.8 says three things: the head hash of the log is published on every push; a monitor that the owner does not operate verifies that each published hash extends the last and that both checkers accept the log; and it writs Guy on any failure. The first and third are code this text is written to; the second is partly a fact about who runs the code, and this text says which part is met, which is not, and how each is read from a record.

**The head hash** is SPEC §3's: the SHA-256 of the last line's bytes of `log.jsonl` (`kernel.log.line_hash`), the `parent` the next entry must name. `python3 -m kernel.check` prints `{"ok": true, "entries": N}` and not the hash (SPEC §9); the scripts below compute it from the file, and the kernel's `entries` ties it to a seq.

## Publication (jack's own workflow; a trusted-base change, so by `push`)

`.github/workflows/publish.yml`, its own workflow, **on push to `main` only** — never on `pull_request`, so no proposal's run holds a writing token — with `permissions: contents: write` (this repository only), `concurrency: group: hashes, cancel-in-progress: false` so appends are serialised, and one step that runs `tools/runner/publish.py` (a builder's, written to this text):

1. Check out the pushed commit; run both checkers over its `log.jsonl`; stop red, publishing nothing, unless both print `ok` with the same `entries`. A published line is a verified head.
2. Compute `<seq>` (`entries − 1`) and `<hash>` (the last line's SHA-256).
3. Fetch the branch `hashes`; append one line `<seq> <hash> <commit> <instant>` to its file `HASHES`; commit and push. A push rejected as not a fast-forward is fetched and retried once (two pushes to `main` a minute apart queue on the concurrency group; the retry covers a race the group does not). Lines are appended in the order the runs commit, so `seq` is strictly increasing along the file whenever `main`'s history is linear, which the ruleset requires.

The ruleset on `hashes` refuses force-pushes and deletion as `main`'s does, and requires no check (none exists for it). Who can write to it: this workflow's token, and the owner (`enforce_admins` off, REPORT.md §8.1). A proposal cannot add a workflow that writes to it: `.github/workflows/` is trusted base (SPEC §10.1) and the judge refuses a proposal that changes it, so a second writer comes only by the owner's push and is visible in the enforcement map's ledger as his act. Residue: the owner can bypass the ruleset as he can on `main`; the published line is as strong as the ruleset, which is as strong as his restraint — the same residue as `main`'s, and A2.8 adds the verifier for it.

## Verification (the verifier; a public script, run by whoever runs it)

`tools/runner/verify.py` (a builder's, written to this text), run on a schedule by `tools/runner/workflows/verify.yml` installed in a repository other than `renavondata/jack`, on GitHub-hosted runners (`runs-on: ubuntu-latest`), keeping its own record in that repository:

1. Clone `renavondata/jack` at `main`; fetch `hashes`.
2. Run both checkers over `main`'s `log.jsonl`; refuse unless both print `ok` with the same `entries`; compute the head's `<seq>` and `<hash>` as publication does.
3. Read `HASHES`: every line's `seq` exceeds the previous; every line's `commit` is on `main`'s first-parent history; for every line, `log.jsonl` at that commit has `seq + 1` entries and its last line's SHA-256 is the line's `hash` — recomputed from the tree, never trusted from the file.
4. Read the verifier's own record (step 6's file): the previous run's `HASHES` line count n and the SHA-256 of `HASHES`'s first n lines, and the previous run's verified head `(seq, hash)`. Refuse unless today's `HASHES` has those n lines as its prefix (append-only) and today's `log.jsonl` has, at that `seq`, a line whose SHA-256 is that `hash` (the log extends what was verified; a rewrite of `main` and `hashes` together is caught here, which is what A2.8's "each head extends the last" asks). The first run records and compares nothing.
5. Lag: if `main`'s head `seq` exceeds `HASHES`'s last `seq`, the publication is in flight or has failed; refuse only when the head commit's committer date is more than `lag` (one hour) before now. A head ahead of `HASHES` by less than that is not a failure.
6. Append one line to the verifier's record, a file in its own repository: `<instant> <main commit> <head seq> <head hash> <HASHES lines> <runner_environment> <login> ok | <failure>`, where `runner_environment` and `login` are read from the Actions API for the run itself (`github-hosted` or `self-hosted`; the repository owner's login). The record is append-only by the same ruleset rule as `hashes`.
7. On any failure, the writ: one issue on `renavondata/opencode-runner` titled `monitor: <failure>` with the verdict, under the account the verifier runs as — on the runner and not on jack, because the account the first instance runs as holds a grant for issues there and nowhere else (seq 2131). The clerk prints a `W4 monitor` line for an open issue so titled; the evidence session copies it with the record.

The verifier compares bytes it recomputes with bytes it recorded; it trusts no verdict of any earlier run of itself and nothing the publisher wrote except as a claim to check.

## Who runs it, and what "does not operate" means here

The script and its shell are public and anyone can install them in a repository of their own with an account of their own. The first instance runs from `renavondata/opencode-runner` under `assize-reviewer` on GitHub-hosted runners: the **host** is GitHub's, not the owner's — no machine of his runs it, and the shell's bytes are the court's (C2c-1 criterion 8 compares them) — but the **configuration** is his: he can disable the workflow or change its shell. A changed shell is visible (the runner evidence); a disabled verifier is visible only as a record that stops, and nothing in the court notices a record that stops except a reader. So A2.8's operator clause is read as two tests, and B7 (`transcripts/RESEARCH-meta-jack-20261107.md`) takes them as stated: (i) the newest line of the verifier's record is `github-hosted`, within twenty-four hours of the assessed instant, and `ok` — decidable from the monitor evidence; (ii) the account the record names is one the owner does not hold — not decidable from any record the court has, so it is a `hand` row of the enforcement map (`A2.8-operator`, with the deadline the sovereign sets, R7's rule), unmet until a second instance under another account exists and its record is copied in. The enforcement map says so, and the book's ch 12 §12.4 states the same residue and keeps stating it.

## Evidence the window file names

`transcripts/evidence/monitor-<stamp>.json`: the verifier's record copied into the court by the evidence session (read-only `gh api` on the verifier's repository: the record's lines, and for the newest run its `runner_environment` and the repository's owner login, from the Actions API), with any open `monitor:` issue; B7's test reads it.
