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
  `opens` names is on `main`'s log: `reviewer-<window>-pins` — checked to hold every `builder-<window>-*` head — brought in as one trailered commit, conflicts under the merge rule, the
  one trusted-base change the brief allows (`judge/scope.json`'s `cap` at the file's `numbers.counted_cap`, SPEC §10's block and the
  cap's history clause), the opening note `transcripts/PUSH-<window>-opening.md`, tests, pins and the count against the cap; pushed,
  never proposed — the sovereign's `jack push <branch> --opens <window>` moves `main` (BRIEF-C2c-1 §2, §7; the same placeholders;
  filed by counsel through the courier's template form).
- `code-review.md` — the reviewer reads the assembled push branch cold against the texts and, on PASS, commits
  `transcripts/REVIEW-<window>-code.md` on that branch for the sovereign's `--review` (RUNBOOK, `jack push`; C2a-prime's precedent);
  not proposed (the same placeholders; filed by counsel through the courier's template form).
- `review-brief.md` — the reviewer's gate review of `transcripts/BRIEF-<window>-draft.md` for a window that has a brief and no
  window file (C2a-prime, C2b): on PASS, `transcripts/REVIEW-<window>-<stamp>-<family>.md` proposed under the reviewer's key
  (placeholders `{WINDOW}`, `{MODEL}`, `{BRANCH}`, `{STAMP}`, `{NOW}`; no texts list, so the courier needs no window file).
- `review-reland.md` — a review already written by `{MODEL}` is re-landed byte for byte under a file name of its own, when
  `main` does not hold it as the commit that added it left it (13 November: two reviews given one name, one written over the
  other). One script, no read and no judgement; the same placeholders, and the session's own model is the template's.
- `c2b-build.md`, `c2b-pins.md`, `c2b-code-review.md` — C2b's window code on its opening push (BRIEF-C2b Amendment 10 clause 5):
  counsel's base `push-c2b-base` is C2a-prime's opening branch with the two trusted-base changes in one commit (the precedent of
  `1c1b27f`); the builder merges it, integrates the pre-built code on `builder-c2b-push-2` and makes it say the amended criteria,
  within its own paths (the first cut, `builder-c2b-push`, rewrote the tests workflow and is abandoned); the reviewer writes the
  pins on `reviewer-c2b-pins`; counsel cuts `push-c2b` from that with the opening note; the reviewer reads `push-c2b` cold and
  commits `REVIEW-C2b-code.md` on it. Pushed, never proposed; used once.
- `c2a-prime-build.md`, `c2a-prime-pins.md`, `c2a-prime-code-review.md` — the rebuild of C2a-prime's window code, its tests and its pins after the
  sovereign's read (his choice of 11 November; COUNSEL-OPEN row 54): the first build was written on 4 November before his read (seq 3432), and no
  session of these templates reads the branches that hold it. Each session first prints the sovereign's own `decision` entries from seq 3432 on and
  checks that the texts' bytes are those of draft v7 (`8a70dc8a`), and writes nothing to a text no entry of his states he read — the check row 53
  owed. Counsel's base `push-c2a-prime-base` is `main` and the one trusted-base commit (the cap at 8400, SPEC §10's block and clause); the builder
  merges it and builds §The code on `builder-c2a-prime-rebuild`; a reviewer of another family writes §Pins' pins on `reviewer-c2a-prime-rebuild-pins`;
  counsel sets `opening-c2a-prime-rebuild` at that branch's head; a reviewer of another family than the builder's reads it cold and commits
  `REVIEW-C2a-prime-code.md` on it. Pushed, never proposed; used for this rebuild only.
- `evidence.md` — the builder produces a window's evidence files (acts, escalations, runner) with the scripts
  under `tools/evidence/` and proposes them (C2c-1; counsel files it through the courier's acts job, daily and
  before a promotion — an issue on the runner, within the grant of seq 2131; `{WINDOW}`, `{STAMP}`, `{NOW}`,
  `{MODEL}`).
