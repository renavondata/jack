# Requests — how counsel's acts are made (counsel's text, 7 November 2026; binds nothing until the courier runs it)

Counsel drafts in a session that holds no key. Its acts on the record are made on steel by the courier, from a
request that is itself in the tree, so that what was asked and what was signed are both on the record and can
be replayed against each other by anyone.

## The convention

- A counsel branch is named `counsel/<name>`. Its commits carry the hand trailer `Proposer: counsel <model id>
  <session id>` (RUNBOOK, Common: a commit made by hand). Pushing it is not an act (COUNSEL-OPEN row 44).
- The branch holds exactly one request file, `transcripts/requests/<name>.jsonl`, one JSON object per line, in
  the order the verbs run:
  - `{"verb": "forecast", "claim": "...", "p": N, "by": "<instant>", "type": "<type>", "args": {...}}` —
    `tools/jack forecast` with those arguments; `type` and `args` optional. Entered only as a brief requires
    (the sovereign's direction of 3 November, row 24) until he directs otherwise.
  - `{"verb": "proposal", "title": "..."}` — `tools/jack proposal --title ...`; the last line, present once.
  No other verb is accepted. A file with any other line, or a branch with no request file, is left alone and
  reported.
- The courier (`transcripts/runner/counsel-courier.md`), on steel, holding `~/.ssh/jack-counsel-3` and the
  `assize-reviewer` token under the grant of seq 2131, reconciles state on every tick: for each remote branch
  `counsel/*` whose request file has not been executed (no `proposal` entry on the branch at or after its last
  content commit), it checks the branch out fresh, runs the request's verbs in order, and reports. The verbs
  themselves refuse what the law refuses (`self_judged`, a `p` outside 1–999, a dirty tree, a branch that does
  not contain `origin/main`); the courier adds nothing to them and signs nothing the file does not say.
- A request is executed once. To act again, counsel pushes a new commit and a new request file.

## What this is for

Every act of counsel's is then: a text on a branch (evidence), a request in the tree (the ask), an entry
signed by a key that never leaves steel (the act), and a pull request opened by an identity under a grant
(the platform's record). The session that drafts can end and nothing is lost; the next session needs no
secret. Whoever can push a `counsel/*` branch is counsel — today, the sovereign's credentials, which this
convention discloses rather than fixes; a deploy key per counsel session is the C2c-1 item that fixes it.

## Pin, when the courier is code in this repository

`courier_signs_only_the_request`: a branch whose request file omits a forecast the courier nonetheless
enters is refused by the courier's own replay (the entries on the branch after the content commit must be
exactly the request file's lines, in order); mutant: the courier entering a forecast from its prompt.
