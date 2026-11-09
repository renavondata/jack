# Session prompts

The texts the runner on steel hands to a session, kept in the record so that a change to how a party is asked
to act is a proposal like any other (counsel's path, read by anyone, merged by the herald) rather than a file
on a machine. `renavondata/opencode-runner`'s `diary.yml` and `herald.yml` read them from `origin/main` of this
repository at dispatch time. Placeholders in braces are filled by the dispatcher: `{N}` the stream number,
`{STAMP}` the UTC stamp `YYYYMMDDTHHMM`, for `repropose.md` `{BRANCH}`, `{KEY}`, `{PARTY}`, `{TITLE}`, and for
`due-resolve.md` `{PARTY}`, `{MODEL}`, `{NOW}`, `{COUNT}` and `{LIST}` (the writs the dispatcher computed as due).

- `stream-forecast.md` — the reviewer forecasts the freshness window two hours ahead for the six datasets of
  BRIEF-C2a §Scope (Amendment 2: hourly, at twenty past).
- `due-resolve.md` — a party resolves every writ the diary computed as due at the tick: freshness windows that
  have ended, races run, proposals whose first tests run has finished, any claim within two hours of its
  deadline — each by the procedure for its type; the diary lists them in the issue with their UTC instants and
  routes the builder's to the reviewer and everyone else's to the builder (hourly, at ten past). It supersedes
  `stream-resolve.md`, which is kept for the record: on 2 and 3 November sessions asked to work out what was due
  found nothing against a live window, and four writs expired while `status.py` printed ESCALATED and nothing was
  filed. A line that is not decided by evidence the session produces is left undecided and reported, never guessed.
- `stream-resolve.md` — the builder resolves the freshness forecasts whose window has ended (hourly, at ten past;
  superseded by `due-resolve.md`).
- `repropose.md` — a party re-enters a stale pull request's content and entries on a fresh prefix.
- `build.md` — the builder builds to named texts on `main` on a named branch (`{TEXTS}`, `{BRANCH}`, `{MODEL}`,
  `{WINDOW}`); filed by counsel through the courier's acts job in its template form, so that a builder-keyed
  session's prompt is always a text on `main` and never a body counsel wrote (C2c-1). Before the window opens the
  branch is pushed and not proposed: the deliverables ride the opening push (BRIEF-C2c-1 §2); after it, a proposal.
The templates in this directory are procedure (the sovereign's ruling of 9 November, 14:02 HKT): counsel proposes changes to them with readers' reads, and no read of the sovereign's precedes a session filed from them; what the sovereign reads before a build is a deliverable text — a brief, a window file, a runner text.

- `pins.md` — the reviewer writes the pins the named texts name, each twin passing on the builder's pre-built
  branches merged into the reviewer's worktree, each mutant the present code or the variant the text names; the
  same placeholders and the same rule on where the branch goes (C2c-1; filed by counsel through the courier's
  template form).
- `review.md` — the reviewer reads the named texts on `main` and, on PASS, writes and proposes the review file the
  opening gate reads (`VERDICT:` first, `Reviewed tree:` a commit on `main`; BRIEF-C2c-1 §2, precondition 3), under
  the reviewer's key; always a proposal, the file being a transcript (C2c-1; the same placeholders; filed by counsel
  through the courier's template form).
- `assemble.md` — the builder assembles a window's opening push branch `push-<window>` once the decision its window file's
  `opens` names is on `main`'s log: every `builder-<window>-*` branch and `reviewer-<window>-pins` merged under the merge rule, the
  one trusted-base change the brief allows (`judge/scope.json`'s `cap` at the file's `numbers.counted_cap`, SPEC §10's block and the
  cap's history clause), the opening note `transcripts/PUSH-<window>-opening.md`, tests, pins and the count against the cap; pushed,
  never proposed — the sovereign's `jack push <branch> --opens <window>` moves `main` (BRIEF-C2c-1 §2, §7; the same placeholders;
  filed by counsel through the courier's template form).
- `code-review.md` — the reviewer reads the assembled push branch cold against the texts and, on PASS, commits
  `transcripts/REVIEW-<window>-code.md` on that branch for the sovereign's `--review` (RUNBOOK, `jack push`; C2a-prime's precedent);
  not proposed (the same placeholders; filed by counsel through the courier's template form).
- `evidence.md` — the builder produces a window's evidence files (acts, escalations, runner) with the scripts
  under `tools/evidence/` and proposes them (C2c-1; counsel files it through the courier's acts job, daily and
  before a promotion — an issue on the runner, within the grant of seq 2131; `{WINDOW}`, `{STAMP}`, `{NOW}`,
  `{MODEL}`).
