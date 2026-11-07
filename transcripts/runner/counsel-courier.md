# The counsel courier — definition (counsel's text; v4 of 7 November 2026, after the reads on runner issues #365, #368 and #375)

This is the definition of the two jobs that act for counsel on steel — the text their code is written to. It
lives here, in the court, so that a change to how counsel's acts are made is a proposal read like any other,
not a file on a machine (the same reason `transcripts/sessions/` holds the session prompts). The code is the
builder's (SPEC §10.8): today the runner's `.github/workflows/counsel-sign.yml`, `.github/scripts/counsel-sign.py`,
`.github/workflows/counsel.yml` and `.github/scripts/counsel-act.py` in `renavondata/opencode-runner`, the first
two installed by the sovereign on 7 November (#369) and all four revised on the branch `counsel-sign-v3`; in
C2c-1, `tools/runner/` in this repository, fetched by the runner. Whether #369 stands as a repair is the
sovereign's to say (the brief's §2 records the lapse; BRIEF-C2c-1 §11).

## What the jobs hold

- `~/.ssh/jack-counsel-3` (private; generated on steel by the sovereign; never in a prompt, a chat or a repository).
- `COUNSEL_GH_TOKEN` (else `~/.config/jack/gh-counsel`): `assize-reviewer`'s token, under the grant of seq 2131 —
  on `renavondata/jack`, opening counsel's proposals and closing its own stale ones with a comment; on
  `renavondata/opencode-runner`, filing and closing issues. Nothing else: no comment on any issue or pull
  request, no issue on `renavondata/jack`, no close of what the account did not open. The jobs report in their
  run logs and, on a refusal, file one issue on the runner.

## When they run

On every push to `counsel-requests` in `renavondata/opencode-runner` that adds a file under `requests/`. The sign
job (`counsel-sign`, the `build` lane, a 45-minute limit — a proposal's check runs the tests, the pins and the
count) takes the files `requests/sign-<id>.json`, `{"id": "sign-<id>", "act": "sign", "branch": "counsel/<name>"}`;
the acts job (`counsel`, the `opencode` lane, ten minutes) takes every other file and skips sign requests. A push
adding nothing for a job exits it green before it looks for the key or the token.

## The sign job, in order, for the branch each trigger names — and refuses otherwise

1. The branch is `counsel/<name>` with `<name>` one token, and `origin/counsel/<name>` exists.
2. **The trailer is the key's.** The pubkey beside the private key is looked up in `main`'s log; it must be
   declared exactly once with powers, and the trailer the verbs will write is `Proposer: <principal> <key_id>`
   from that declaration (RUNBOOK, Common: key and party) — never a name typed into the job.
3. **The worktree is RUNBOOK's:** `~/git/worktrees/jack/counsel/<name>`, holding the local branch
   `counsel/<name>`. If the worktree exists, its branch must be that one and it must be clean. If the local
   branch holds commits `origin/counsel/<name>` lacks — a run that stopped after signing a forecast leaves one,
   and it stands as lawful — they are pushed (never forced; a rejected push refuses the request); if the two
   have diverged, the request is refused. Then the worktree is reset to `origin/counsel/<name>`, which now
   contains everything it held. Nothing is deleted; nothing of a stopped run's is reset away.
4. **The whole request is read and checked before anything runs.** `transcripts/requests/<name>.jsonl` at the
   head: every line is a JSON object; every `verb` is `forecast` with `claim` (string), `p` (integer, not a
   boolean) and `by` (string), or `proposal` with `title` (string); `proposal` occurs exactly once and last.
   Otherwise refused, nothing signed. The file's bytes are kept for step 6.
5. **The branch is counsel's, and its log is the kernel's.** `git diff --name-only --no-renames
   origin/main...HEAD` is compared with the `counsel` row of `judge/scope.json` *at `origin/main`*: any path
   outside it (so any change to `tools/`, `kernel/`, `judge/`, `pins/`, `tests/`, and a rename out of them)
   refuses the request. Every changed path present at the head must be a regular file (git mode `100644` or
   `100755`; SPEC §10 item 9): a symbolic link named `log.jsonl` would make the verbs append to the file it
   points at, so it is refused before any verb runs. Then `python3 -m kernel.check log.jsonl` runs in the
   worktree (its `kernel/` is `main`'s, by the scope check); a log the kernel does not admit refuses the
   request. Only after this is the branch's log read for anything.
6. **Finished already?** The content commit is found as the `proposal` verb finds it: the newest commit
   reachable from the head and not from `origin/main` that changes a path other than `log.jsonl` (merges
   against each parent, renames on both sides). The branch's own entries are the lines of its `log.jsonl`
   after the fork point's (the merge base with `origin/main`). If they hold a `proposal` by this key's
   principal naming that commit, the act is finished: nothing is signed; if no open pull request has the
   branch as head, one is opened with the request's title (the verb's own unfinished ending).
7. **The verb's prerequisite.** If the branch does not contain `origin/main`, `origin/main` is merged into it
   with the trailer of step 2. A conflicting merge is aborted and the request refused. After a merge, the
   request file's bytes must equal step 4's — a merge that changes the request refuses it, nothing signed —
   and step 5's path check runs again on the merged head.
8. **Each line once.** With `JACK_KEY=~/.ssh/jack-counsel-3` and `GH_TOKEN` counsel's, each `forecast` line
   runs as `tools/jack forecast "<claim>" --p <p> --by <by> [--type <type> --args '<args>']` and the `proposal`
   line as `tools/jack proposal --title "<title>"`, one at a time, each after the last has printed — except
   that a forecast line whose entry already stands among the branch's own entries (same `claim`, `p`,
   `resolves_by`, `type` and `args`, by this principal) is not entered again: its entry is its receipt. The
   verbs commit on the branch; the proposal verb pushes it and opens the pull request. A refusal stops the
   request at that line: the entries before it stand as lawful (RUNBOOK: branch verbs undo nothing), the
   refusal is printed verbatim and filed as one issue on the runner, and nothing is retried or forced. The
   next trigger for the branch pushes what stood (step 3), skips it (this step) and continues.
9. **The receipt** is the run itself: the trigger `requests/sign-<id>.json` on `counsel-requests` names the
   branch, and the `counsel-sign` run on that push prints, last, the request's SHA-256, the commit the
   proposal entry names, the head it pushed and the pull request. The job comments on nothing (the grant
   of seq 2131 does not cover it); B6's test reads the trigger and the run, not a comment.

## The acts job, for each request file that is not a sign request

A request is one JSON object with `id` and `act`:

- `pr` {head, title, body}: a pull request on `renavondata/jack` from `head`, which must be `counsel/<name>`;
  otherwise refused.
- `issue` {title, body, labels, then_labels}: an issue on `renavondata/opencode-runner` — never on jack. The
  body carries `counsel-request: <id>`; a request whose marker is already on an issue is skipped, so a re-run
  files nothing twice. `then_labels` are added after the issue exists (so `run.yml` sees `build` when the
  `labeled run` event fires).
- `close` {repo, number, stale}: on `renavondata/jack`, a pull request whose head is `counsel/<name>` and which
  counsel's account opened; on `renavondata/opencode-runner`, an issue counsel's account opened. `stale` is the
  reason, required; the comment posted is `stale: <reason>`, then the close. Anything else — another author,
  another repository, no reason, a jack issue — is refused; one already closed is skipped.

No other act exists. A refusal makes the run red, with its reason in the log.

## What the jobs never do

Sign anything not in the request file; run a verb other than the two; run a branch's own code (step 5); touch
`main`; delete or reset away anything; comment on any issue or pull request except the `stale:` comment of a
declared close; file an issue on jack; read `log.jsonl` whole into a model.

## Custody, disclosed

Whoever can push a `counsel/*` branch to jack *and* a trigger to `counsel-requests` is counsel: today, the
sovereign's git credentials, which the drafting session uses for pushes (pushes are not acts, COUNSEL-OPEN row 44).
A branch must not be pushed while a run on it may be in flight: a push that does not include the run's commits
diverges from them, and step 3 refuses. Two further routes reach the key and are not closed by this definition:
every runner on steel runs as the login user `g`, whose home holds every party key and a `gfrmin` login with
admin scopes (`opencode-runner` issue #188), and `run.yml` exports whatever `key:` an issue body names as
`JACK_KEY` to the session it starts. So any session on steel, and anyone who can file a `run` issue, can sign as
any party. The fix is #188's — a runner user that holds only the job's credentials — and it is the sovereign's,
once. Until then this courier is as strong as the host. The enforcement map does not yet say so: its
`irreversible` row reads `code: keys, rulesets`; BRIEF-C2c-1 R7 makes the map a ledger and names this row as
`hand` with #188 as its deadline, and until that lands the disclosure is this paragraph and nothing in the tree.

## Pin, when the courier is code in this repository

`courier_signs_only_the_request`: the entries on the branch after the content commit are exactly the request
file's lines, in order, signed by `counsel`, each once; a branch changing `tools/`, or carrying a symbolic link
among its changed paths, is refused unsigned; a request changed by the merge is refused. Mutants: a forecast
entered from the prompt; `tools/` of the branch run instead of `main`'s; a forecast re-entered on a second run;
the request read before the merge only.

## The script

Counsel touches documents only; code enters from a builder (SPEC §10.8), so the script is not here. Its
runner copies are `.github/scripts/counsel-sign.py` and `.github/scripts/counsel-act.py` in
`renavondata/opencode-runner` (#369, merged 7 November; v4 of both on the branch `counsel-sign-v3`, with U2's
narrowing of the acts), written to this definition; in C2c-1 a builder brings them into the court as
`tools/runner/counsel-sign.py` and `tools/runner/counsel-act.py`, built to this text, with the workflows that
run them, and the runner's copies become a fetch of those files from `main`. Until then, any difference between
this text and the runner's scripts is a finding against the scripts.
