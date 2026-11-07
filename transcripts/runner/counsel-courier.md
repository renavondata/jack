# The counsel courier — definition (counsel's text; v16 of 8 November 2026, after the reads on runner issues #365, #368, #375, #383, #384, #386–#400, #403–#406, #408, #409)

This is the definition of the two jobs that act for counsel on steel — the text their code is written to. It
lives here, in the court, so that a change to how counsel's acts are made is a proposal read like any other,
not a file on a machine (the same reason `transcripts/sessions/` holds the session prompts). The code is the
builder's (SPEC §10.8): today the runner's `.github/workflows/counsel-sign.yml`, `.github/scripts/counsel-sign.py`,
`.github/workflows/counsel.yml` and `.github/scripts/counsel-act.py` in `renavondata/opencode-runner`, the first
two installed by the sovereign on 7 November (#369), the last two on 6 November (#335); the branch `counsel-sign-v3` revises
the two scripts, removes the concurrency group from each workflow (three lines each) and changes one line of `diary.yml`; in
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

On every push to `counsel-requests` in `renavondata/opencode-runner` that adds a file under `requests/` — every push: the
workflows carry no concurrency group (GitHub cancels a queued run when a third arrives, and a cancelled run is a push whose
requests nobody sees); the one runner of each lane serialises the runs. The sign
job (`counsel-sign`, the `build` lane, a 45-minute limit — a proposal's check runs the tests, the pins and the
count) takes the files `requests/sign-<id>.json`, `{"id": "sign-<id>", "act": "sign", "branch": "counsel/<name>"}`;
the acts job (`counsel`, the `opencode` lane, ten minutes) takes every other file and skips sign requests. A push
adding nothing for a job exits it green before it looks for the key or the token; in both jobs a refusal of one request
does not abandon the others on the same push (each is handled, its refusal filed as one issue on the runner, and the
run is red at the end if any was refused).

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
   boolean) and `by` (string), and if present `type` (string) and `args` (object), or `proposal` with `title`
   (string); no string is empty, blank, longer than 4000 characters or beginning with `-` (the proposal verb would substitute a commit's subject for an empty title; an argument the host cannot pass is not tried; a verb reads `--help` as an option and exits 0 with no entry; the rule reaches the strings inside `args` too, where it is not needed — a simplification, stated), none holds a control character (C0, DEL or C1) or text UTF-8 cannot encode (a verb cannot be given one); `proposal` occurs exactly
   once and last. Otherwise refused, nothing signed (a `type` that is not a
   string would be signed as the string `None` and never match its own receipt). The file's bytes are kept for step 7.
5. **The branch is counsel's, and its log is the kernel's.** `git diff --name-only --no-renames
   origin/main...HEAD` is compared with the `counsel` row of `judge/scope.json` *at `origin/main`*: any path
   outside it (so any change to `tools/`, `kernel/`, `judge/`, `pins/`, `tests/`, and a rename out of them)
   refuses the request. Every changed path present at the head must be a regular file (git mode `100644` or
   `100755`; SPEC §10 item 9): a symbolic link named `log.jsonl` would make the verbs append to the file it
   points at, so it is refused before any verb runs; paths are read NUL-separated, so a space in a name hides
   nothing. Then `python3 -m kernel.check log.jsonl` runs in the worktree (its `kernel/` is a `main`'s — the fork
   point's, by the scope check; the verbs re-check with the merged kernel); a log the kernel does not admit
   refuses the request. Only after this is the branch's log read for anything.
6. **Finished already?** A branch with no commit `origin/main` lacks has either been merged — then a `proposal` entry on
   `main` by this principal names a commit that is an ancestor of `origin/counsel/<name>` whose tree holds
   `transcripts/requests/<name>.jsonl` with the request's bytes (step 4's) — the newest such on `main` is the branch's own
   proposal, since a later counsel branch's commits are not ancestors of this one — and the receipt of step 9 is printed
   for it, marked `already proposed, merged`, so that a run stopped
   between the verb and its receipt still leaves one — or is empty, or merged without such an entry, and is refused. Otherwise
   the content commit is found as the `proposal` verb finds it: the newest commit
   reachable from the head and not from `origin/main` that changes a path other than `log.jsonl` (merges
   against each parent, renames on both sides). The branch's own entries are the lines of its `log.jsonl`
   after the fork point's (the merge base with `origin/main`). If they hold a `proposal` by this key's
   principal naming that commit **and** the branch's own entries are exactly the request's lines in order — each forecast
   line's entry, then that one proposal with the request's title and nothing else, no surplus forecast or earlier
   proposal — the act is finished: nothing
   is signed; if no open pull request has the branch as head, one is opened with the request's title (the verb's own
   unfinished ending); and the receipt of step 9 is printed for this request all the same, marked `already proposed`.
   A branch whose entries differ from the request in any of these is refused; so is a branch that holds a `proposal`
   entry naming any other commit (the branch moved after proposing): a second act is a new branch.
7. **The verb's prerequisite.** If the branch does not contain `origin/main`, `origin/main` is merged into it
   with the trailer of step 2. A conflicting merge is aborted and the request refused. After a merge, the
   request file's bytes must equal step 4's, and step 5's path check runs again on the merged head; if either
   fails — or anything else goes wrong between the merge and the first verb, step 8's walk of the entries included, or the host fails a verb before any line has signed and the branch's head is still the commit before the launch (a launch the host refuses, the verb never run; a verb that committed before the host's error keeps its commit and the merge with it; never an interrupted wait, which undoes nothing) —
   **the courier's own merge is undone** (the worktree reset to `origin/counsel/<name>`) and the request refused,
   nothing signed — so a later trigger cannot push that merge as a stopped run's entry (step 3) and
   sign what the merge changed. A branch whose own entries conflict with a moved `main` (both append to
   `log.jsonl`) is refused here for good: its entries never reach `main`, and counsel starts a new branch from
   `main` with the same texts and a new request (RUNBOOK: a rejected push is "run again", never a retry with force).
8. **Each line once.** With `JACK_KEY=~/.ssh/jack-counsel-3` and `GH_TOKEN` counsel's, each `forecast` line
   runs as `tools/jack forecast "<claim>" --p <p> --by <by> [--type <type> --args '<args>']` and the `proposal`
   line as `tools/jack proposal --title "<title>"`, one at a time, each after the last has printed — except
   that a forecast line whose entry already stands among the branch's own entries (same `claim`, `p`,
   `resolves_by`, `type` and `args`, compared as canonical JSON so that `true` and `1` differ, by this principal) is
   not entered again: its entry is its receipt. The match is in order and one-to-one: counsel's forecast entries after
   the fork point are walked in order beside the forecast lines; the k-th line stands if it equals the k-th entry; a k-th
   entry that equals no k-th line — an entry the request does not say, or in another order — refuses the request, and
   so does an entry left over when the proposal line is reached, **before** the proposal verb runs (nothing on the
   branch may stand that the file does not say, and no proposal is signed over it); two identical lines need two entries; an absent
   `args` and `"args": {}` are different entries (`tools/entry.py` writes no member for absent) and compare unequal. A verb's
   exit is not its receipt: after each verb exits 0, the log must hold exactly one new entry, this principal's, of the
   verb's type and equal to the line (a forecast as above; a proposal by its title), the entries before it unchanged —
   else the request is refused at that line, nothing retried; an entry a verb wrote that the line does not say is on the
   branch (a verb undoes nothing), is pushed as it stands by the next trigger's step 3, and is refused there and at every
   later trigger: nothing is ever signed over it. The
   verbs commit on the branch; the proposal verb pushes it and opens the pull request. A refusal stops the
   request at that line: the entries before it stand as lawful (RUNBOOK: branch verbs undo nothing), the
   refusal is printed verbatim and filed as one issue on the runner, and nothing is retried or forced. The
   next trigger for the branch pushes what stood (step 3), skips it (this step) and continues — while `main` has
   not moved; if it has, step 7 refuses and the branch is restarted from `main`.
9. **The receipt** is the run itself: the trigger `requests/sign-<id>.json` on `counsel-requests` names the
   branch, and the `counsel-sign` run on that push prints, for each request it handled, a receipt line beginning
   with the request's id: the request's SHA-256, the commit the proposal entry names, the head it pushed and the
   pull request. The job comments on nothing (the grant
   of seq 2131 does not cover it). The evidence session copies the runs into the court as the `courier`
   evidence (the window file's `evidence.courier`: run id, created and updated instants, the trigger's path,
   the receipt line), and B6's test reads that file and the log, nothing off the record.

## The acts job, for each request file that is not a sign request

A request is one JSON object with `id` (one token, `[A-Za-z0-9._-]+`: it is written into issue bodies, so it may not carry anything that could read as an instruction; both jobs refuse any other) and `act`:

- `pr` {head, title, body}: a pull request on `renavondata/jack` from `head`, which must be `counsel/<name>`;
  otherwise refused.
- `issue` {title, body, labels, then_labels}, or `issue` {template, window, model, branch?, texts?}: an issue on
  `renavondata/opencode-runner` — never on jack. In the second form the job fetches `transcripts/sessions/<template>.md`
  from jack's `main`, fills `{STAMP}` and `{NOW}` itself and `{WINDOW}`, `{MODEL}`, `{BRANCH}` and `{TEXTS}` from the
  request's values, each of which must match `[A-Za-z0-9._/,-]+` (a value with a newline, a brace or a space is refused —
  nothing counsel writes can become an instruction; a placeholder the request leaves unfilled refuses the request), takes
  the title from the template's first `#` line, refuses a `texts` value naming any path not under a frozen prefix of the
  named window's file (a build is to texts the window freezes, never to one counsel can change inside the window; paths
  are read as written — a segment beginning with `.`, an empty segment or a leading `/` in a `texts` element or in
  `branch` (one path, no comma) is refused, so no spelling reaches a path the prefix does not cover — a `texts` element
  ends in a name, never a `/` (a trailing `/` is an empty segment); `window` must match `[A-Za-z0-9][A-Za-z0-9-]*`, one file name under
  `transcripts/windows/`; `texts` without `window` is refused), and
  carries nothing else of counsel's: the session's prompt is a text on
  `main`. In the first form the body may not name the builder's key in any spelling (a `key:` line naming `jack-builder`
  is refused): a builder-keyed session — the evidence session, a build to a text — is filed from a template only, so that
  what the builder does under its key is never a body counsel wrote. The
  body carries `<!-- counsel-request: <id> -->`; a request whose exact marker is already on an issue counsel's account
  opened (every issue of the repository is searched, paged to the end; another author's issue, or a body that merely
  contains the id, is not a match) files nothing twice, and only adds the `then_labels` a stopped run owed. `then_labels` are added after the issue exists (so `run.yml` sees `build` when the
  `labeled run` event fires).
- `close` {repo, number, stale}: on `renavondata/jack`, a pull request whose head is `counsel/<name>` and which
  counsel's account opened, closed after the comment `stale: <reason>` (the grant's "with a comment"); on
  `renavondata/opencode-runner`, an issue — not a pull request — counsel's account opened, closed with no comment
  (the grant's runner clause is filing and closing). `stale` is the reason, required in both.
  The job tolerates nothing: any failure in one request (a refused act, an API error, a malformed request, a git or
  `gh` command that fails) is that request's refusal, filed as one issue, and the next request is handled — in both
  jobs, whatever raised it. Anything else —
  another author, another repository, no reason, a jack issue, a runner pull request — is refused; one already
  closed is skipped.

No other act exists. A refusal makes the run red, with its reason in the log.

## What the jobs never do

Sign anything not in the request file; run a verb other than the two; run a branch's own code (step 5); touch
`main`; delete or reset away anything but its own refused merge; comment on any issue or pull request except the
`stale:` comment on a jack proposal it closes; file an issue on jack; read `log.jsonl` whole into a model.

## Custody, disclosed

Whoever can push a `counsel/*` branch to jack *and* a trigger to `counsel-requests` is counsel: today, the
sovereign's git credentials, which the drafting session uses for pushes (pushes are not acts, COUNSEL-OPEN row 44).
A branch must not be pushed while a run on it may be in flight: a push that does not include the run's commits
diverges from them, and step 3 refuses. Two further routes reach the key and are not closed by this definition:
every runner on steel runs as the login user `g`, whose home holds every party key and a `gfrmin` login with
admin scopes (`opencode-runner` issue #188), and `run.yml` exports whatever `key:` an issue body names as
`JACK_KEY` to the session it starts. So any session on steel, and anyone who can file a `run` issue, can sign as
any party. The fix is #188's — a runner user that holds only the job's credentials — and it is the sovereign's,
once. Until then this courier is as strong as the host. The enforcement map does not say so: its
`irreversible` row reads `code: keys, rulesets`, and no row names the host. BRIEF-C2c-1 R7 gives every row a witness
and every hand row a deadline, and names no row for this; the disclosure is this paragraph, and the act that closes
it is #188's, the sovereign's.

## Pin, when the courier is code in this repository

**Pin `courier_signs_only_the_request`.** The entries on the branch after the fork point with `main` are exactly the
request file's lines, in order, signed by `counsel`, each once (a branch is used for one request; a second request
is a new branch, `transcripts/requests/README.md`); a branch changing `tools/`, or carrying a symbolic link
among its changed paths, is refused unsigned; a request changed by the merge is refused. Mutants: a forecast
entered from the prompt; `tools/` of the branch run instead of `main`'s; a forecast re-entered on a second run;
the request read before the merge only.

## The script

Counsel touches documents only; code enters from a builder (SPEC §10.8), so the script is not here. Its
runner copies are `.github/scripts/counsel-sign.py` and `.github/scripts/counsel-act.py` in
`renavondata/opencode-runner` (#335 and #369, merged 6 and 7 November; v5 of both on the branch `counsel-sign-v3`, with
U2's narrowing of the acts), written to this definition; in C2c-1 a builder brings them into the court as
`tools/runner/counsel-sign.py` and `tools/runner/counsel-act.py`, built to this text, with the workflows that
run them, and the runner's copies become a fetch of those files from `main`. Until then, any difference between
this text and the runner's scripts is a finding against the scripts.
