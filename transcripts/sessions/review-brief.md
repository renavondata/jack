model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: cold read and formal review of transcripts/BRIEF-{WINDOW}-draft.md on `main`, for the opening gate of {WINDOW} (renavondata/jack)

You are a **reader** and, if the brief passes, the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`) whose review file the opening gate reads: `tools/jack push --opens {WINDOW}` requires a `transcripts/REVIEW-{WINDOW}-*.md` on `main`, brought by a proposal signed by a key whose principal is not counsel, whose first line is `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS` and whose `Reviewed tree:` holds the brief with `main`'s bytes (RUNBOOK, `jack push`). This template is for a window that has a brief and no window file (C2a-prime, C2b); a window with a file is read from `review.md`. You hold no other task. Work only in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now; do not read or write anything outside it. Your paths: `transcripts/`, `log.jsonl`. Run the `tools/jack` verbs one at a time. Now is the UTC instant `date -u +%Y-%m-%dT%H:%M:%SZ` prints.

**The text** is `transcripts/BRIEF-{WINDOW}-draft.md` at `origin/main`, whole, with every amendment appended to it — an amendment governs the body it amends — and the record it rests on: `CHARTER.md`, `SPEC.md`, `RUNBOOK.md`, the briefs, rulings and COUNSEL-OPEN rows it cites, the tools it names. Counsel wrote it and holds forecasts on the window; your read is of a party with an interest. The newest amendment is what no earlier review has read: `git log --format='%h %ad %s' --date=short -5 origin/main -- transcripts/BRIEF-{WINDOW}-draft.md` shows it, and `ls transcripts/REVIEW-{WINDOW}-*.md` the earlier reviews.

**Questions.** (1) Decidability: is every rule, criterion and act of the brief as amended decidable from `log.jsonl`, the tree at a prefix and the evidence it names; is any impossible on `main`'s log or for its named producer? (2) Contradiction: between an amendment and the body it leaves standing (a sentence it neither strikes nor addresses), between the brief and a text in force — quote both sides. (3) Lawfulness: anything that loosens a bound of the charter (A2.4), changes a window already open or moves a stated end (A3.2, A5), has counsel author code (SPEC §10.8), or puts code before the sovereign's read (A2.10). (4) Interest: anything false, undecidable or understated in counsel's favour, and any fact the newest amendment states that the log or the tree contradicts.

**Your report** is your final message. Begin with exactly one line, `VERDICT: PASS` or `VERDICT: FAIL`. Then one line per finding: `F<n> [BLOCK|FIX|NOTE] <§ or amendment> — <problem> — <evidence, quoted>`. A rule not decidable as written, a contradiction with a text in force, a loosened bound, or code before the sovereign's read is a BLOCK. If your verdict is FAIL, write no file and propose nothing.

**On PASS, the review file.** Write `transcripts/REVIEW-{WINDOW}-{STAMP}.md` beginning with exactly these three lines, then your findings as above:
```
VERDICT: ACCEPT WITH OBLIGATIONS
Reviewed tree: <the full sha of origin/main as you read it — `git rev-parse origin/main`>
Reader: reviewer; model {MODEL}; {NOW}
```
(`VERDICT: ACCEPT` if you have no FIX.) Then `git add` the file, `git commit -m "REVIEW-{WINDOW}-{STAMP}: formal read of BRIEF-{WINDOW} on main" -m "Proposer: reviewer <your model id> <this issue's number>"`, and `tools/jack proposal --title "REVIEW-{WINDOW}-{STAMP}"` with the bash tool's `timeout` set to `900000`; if the push is refused, run the two commands the verb prints. The file is a transcript and carries no code, so it is proposed whether or not the window has opened. Report, as the issue's last comment: your verdict and findings, and the PR number or that no file was written.
