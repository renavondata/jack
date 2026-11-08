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
- `pins.md` — the reviewer writes the pins the named texts name, each twin passing on the builder's pre-built
  branches merged into the reviewer's worktree, each mutant the present code; the same placeholders and the same
  rule on where the branch goes (C2c-1; filed by counsel through the courier's template form).
- `evidence.md` — the builder produces a window's evidence files (acts, escalations, runner) with the scripts
  under `tools/evidence/` and proposes them (C2c-1; counsel files it through the courier's acts job, daily and
  before a promotion — an issue on the runner, within the grant of seq 2131; `{WINDOW}`, `{STAMP}`, `{NOW}`,
  `{MODEL}`).
