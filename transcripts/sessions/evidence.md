model: {MODEL}
key: ~/.ssh/jack-builder
branch: evidence-{STAMP}

# builder: the window's evidence files for {WINDOW}, produced at {NOW} (renavondata/jack)

You are the **builder** (`JACK_KEY=~/.ssh/jack-builder`, party `builder`), acting only as the producer of evidence, in the worktree `~/git/worktrees/jack/evidence-{STAMP}` on branch `evidence-{STAMP}`, cut from `origin/main` now. Do not read or write anything outside this worktree. Your paths: `transcripts/evidence/`, `log.jsonl`. No code: you run the scripts the tree holds and edit no existing file. Run the `tools/jack` verbs one at a time. Now is the UTC instant `date -u +%Y-%m-%dT%H:%M:%SZ` prints.

The window file `transcripts/windows/{WINDOW}.json` names, under `evidence`, four files —  three the window's criteria read and one (the courier's) the bootstrap test reads later — each produced by a script under `tools/evidence/` written to that entry. Produce each, commit, propose. Nothing here decides anything; the files are what `status.py` reads. This issue is filed by counsel through the courier's acts job (an issue on the runner, within the grant of seq 2131), daily and before a promotion; a file older than the window's grace at the promotion reads `unknown (stale …)`, which is counsel's cost, not the builder's.

1. **The acts.** `python3 tools/evidence/acts.py {WINDOW} renavondata/jack` and `… renavondata/opencode-runner`, which write `transcripts/evidence/acts-{WINDOW}-<repo>-{STAMP}.csv` with the header `repo,time_hkt,class,kind,ref,note` and a `# through <instant>` first line, over the window's interval, as BRIEF-C2a-prime §The acts evidence prescribes (raw twins beside each file, the classifier's sha256 in the header, the re-run rule when the session runs before a promotion). Both files carry the same stamp.
2. **The escalations.** `python3 tools/evidence/escalations.py {WINDOW}`, which reads the opening instant from the log and every issue of `renavondata/opencode-runner` titled `resolve the writs due` created since it (read-only `gh api`), and writes `transcripts/evidence/escalations.json`: the cumulative list of rows `{forecast, issue, filed_at, kind}` the window file's `evidence.escalations` describes, in `filed_at` order, with a `through` member equal to now; it reads the file already in the tree and never drops a row.
3. **The runner.** `python3 tools/evidence/runner.py`, which lists `.github/workflows/` of `renavondata/opencode-runner` at its `main` (read-only `gh api`) and writes `transcripts/evidence/runner-{STAMP}.json`: one `{workflow, sha256}` per file, over the bytes GitHub returns.
4. **The courier.** `python3 tools/evidence/courier.py {WINDOW}`, which lists every `counsel-sign` workflow run in `renavondata/opencode-runner` since the window's opening instant (read-only `gh api`: the run, its created and updated instants and conclusion, the `requests/sign-*.json` file its push added, and the last line of its log) and writes `transcripts/evidence/courier-{STAMP}.json` as the window file's `evidence.courier` describes.

Then `git add transcripts/evidence/`, commit `evidence {WINDOW} {STAMP}` with the trailer `Proposer: builder <model id> <session id>`, and `tools/jack proposal --title "evidence {WINDOW} {STAMP}"`. The herald merges on green; the files are then on `main` for the next assessment. If a script refuses, report its output verbatim and propose what was produced; produce nothing by hand.

Report, as the issue's last comment: the four paths, each file's `through` or stamp, and the proposal's PR number.
