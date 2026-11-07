# Requests — how counsel's acts are made (counsel's text, 7 November 2026; binds nothing until the courier runs it)

Counsel drafts in a session that holds no key. Its acts on the record are made on steel by the courier, from a
request that is itself in the tree, so that what was asked and what was signed are both on the record and can
be replayed against each other by anyone.

## The convention

- A counsel branch is named `counsel/<name>` and carries one request; a second request is a new branch. Its commits carry the hand trailer `Proposer: counsel <model id>
  <session id>` (RUNBOOK, Common: a commit made by hand) and, from C2c-2, `Model: <model id>` beside it (SPEC-PATCH
  §2: the drafter's commit names its model so that a reader can differ from it). Pushing it is not an act (COUNSEL-OPEN row 44).
- The branch holds exactly one request file, `transcripts/requests/<name>.jsonl`, one JSON object per line, in
  the order the verbs run:
  - `{"verb": "forecast", "claim": "...", "p": N, "by": "<instant>", "type": "<type>", "args": {...}}` —
    `tools/jack forecast` with those arguments; `type` and `args` optional. Entered only as a brief requires
    (the sovereign's direction of 3 November, row 24) until he directs otherwise.
  - `{"verb": "proposal", "title": "..."}` — `tools/jack proposal --title ...`; the last line, present once.
  No other verb is accepted. A file with any other line, or a branch with no request file, is left alone and
  reported.
- The courier (`transcripts/runner/counsel-courier.md`), on steel, holding `~/.ssh/jack-counsel-3` and the
  `assize-reviewer` token under the grant of seq 2131, runs when a trigger `requests/sign-<id>.json` naming the
  branch is pushed to `counsel-requests` in `renavondata/opencode-runner`. It reads the whole request before it
  runs anything, refuses a branch that changes any path outside counsel's scope or any object that is not a
  regular file (so the verbs it runs are `main`'s, never the branch's, and `log.jsonl` is the branch's own),
  refuses a log the kernel does not admit, merges `origin/main` only if the request's bytes survive the merge,
  runs the request's verbs in order in the branch's worktree at `~/git/worktrees/jack/counsel/<name>`, and
  signs nothing the file does not say. A content commit already
  proposed by counsel is not signed again; if its pull request did not open, the courier opens it (the verb's
  own unfinished ending). The verbs refuse what the law refuses (`self_judged`, a `p` outside 1–999, a dirty
  tree, a branch that does not contain `origin/main`); a refusal stops the request, is printed, and is filed as
  one issue on the runner.
- Each line is executed once: a run that stops after some lines leaves their entries standing on the branch
  (the courier pushes them on the next trigger, never resets them), and the next trigger skips a forecast whose
  entry already stands and continues from the first line without one — while `main` has not moved; once it has,
  the branch's entries conflict with `main`'s and the request is refused for good, and counsel starts a new
  branch from `main` with the same texts and a new request. To act again after the proposal, counsel pushes a
  new commit and a new request file; it pushes nothing to a branch while a run on it may be in flight (a push
  that lacks the run's commits diverges, and the courier refuses rather than reset).

## What this is for

Every act of counsel's is then: a text on a branch (evidence), a request in the tree (the ask), an entry
signed by a key that never leaves steel (the act), and a pull request opened by an identity under a grant
(the platform's record). The session that drafts can end and nothing is lost; the next session needs no
secret.

## Custody, disclosed

Whoever can push a `counsel/*` branch to jack and a trigger to `counsel-requests` is counsel — today, the
sovereign's git credentials, which the drafting session uses for pushes (not acts, COUNSEL-OPEN row 44). Two
other routes reach the key: every runner on steel runs as the login user `g`, whose home holds every party
key and a `gfrmin` login with admin scopes (`opencode-runner` #188), and `run.yml` exports whatever `key:` an
issue names to the session it starts — so any session on steel, and anyone who can file a `run` issue, can sign
as any party. This convention does not close those routes; #188's runner user does, and it is the sovereign's
act, once. Until then the courier is as strong as the host.

## Pin, when the courier is code in this repository

`courier_signs_only_the_request`: the entries on the branch after the content commit are exactly the request
file's lines, in order, signed by `counsel`, each once; a branch that changes `tools/`, or carries a symbolic
link among its changed paths, is refused unsigned; a request the merge changes is refused. Mutants: the
courier entering a forecast from its prompt; the branch's `tools/` run instead of `main`'s; a forecast
re-entered on a second run; the request read before the merge only.
