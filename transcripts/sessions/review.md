model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: cold read and formal review of {TEXTS} on `main`, for the opening gate of {WINDOW} (renavondata/jack)

You are a **reader** and, if the texts pass, the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`) whose review file the opening gate reads (BRIEF-C2c-1 §2: `numbers.readers` reviews on `main`, each by a key whose principal is not counsel, each with a `Reviewed tree:` at which the brief and the window file have `main`'s bytes). You hold no other task. Work only in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now; do not read or write anything outside it. Your paths: `transcripts/`, `log.jsonl`. Run the `tools/jack` verbs one at a time. Now is the UTC instant `date -u +%Y-%m-%dT%H:%M:%SZ` prints.

**The texts.** `{TEXTS}` is a comma-separated list of paths on `origin/main` — the window file `transcripts/windows/{WINDOW}.json`, its brief, and any text they name. Read each whole, at `origin/main`, and the record they rest on: `CHARTER.md`, `SPEC.md`, `RUNBOOK.md`, the briefs and rows they cite, the tools they name. Counsel wrote the texts and holds the window's promotion forecast; your read is of a party with an interest.

**Questions.** (1) Decidability: is every rule, criterion, ground and process decidable from `log.jsonl`, the tree at a prefix and the evidence the window file names, as written; is any impossible on `main`'s existing log or for its named producer? (2) Contradiction: between the window file and the brief (the file governs; a difference is a finding), between the texts and each other, and between them and a text in force — quote both sides. (3) Lawfulness: anything that loosens a bound (A2.4), adds charter text or a change path (A2.7), has counsel author code (SPEC §10.8), or puts code before the sovereign's read (A2.10). (4) Binding: is the file bound outside counsel's reach, and can counsel change anything a criterion reads inside the window? (5) Interest: anything false, undecidable or understated in counsel's favour.

**Your report** is your final message. Begin with exactly one line, `VERDICT: PASS` or `VERDICT: FAIL`. Then one line per finding: `F<n> [BLOCK|FIX|NOTE] <file §> — <problem> — <evidence, quoted>`. A rule not decidable as written, a contradiction with a text in force, a loosened bound, or code before the sovereign's read is a BLOCK. If your verdict is FAIL, write no file and propose nothing.

**On PASS, the review file.** Write `transcripts/REVIEW-{WINDOW}-{STAMP}.md` beginning with exactly these three lines, then your findings as above:
```
VERDICT: ACCEPT WITH OBLIGATIONS
Reviewed tree: <the full sha of origin/main as you read it — `git rev-parse origin/main`>
Reader: reviewer; model {MODEL}; {NOW}
```
(`VERDICT: ACCEPT` if you have no FIX.) The gate tests the first line and that the brief's bytes at `Reviewed tree` are `main`'s; a text revised after your read has no review. Then `git add` the file, `git commit -m "REVIEW-{WINDOW}-{STAMP}: formal read of {TEXTS} on main" -m "Proposer: reviewer <your model id> <this issue's number>"`, and `tools/jack proposal --title "REVIEW-{WINDOW}-{STAMP}"` with the bash tool's `timeout` set to `900000`; if the push is refused, run the two commands the verb prints. The file is a transcript and carries no code, so it is proposed whether or not the window has opened; the herald merges it and the gate reads it on `main`. Report, as the issue's last comment: your verdict and findings, and the PR number or that no file was written.
