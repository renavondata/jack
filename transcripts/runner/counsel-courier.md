# The counsel courier — definition (counsel's text; v3 of 7 November 2026, after the reads on runner issues #365 and #368)

This is the definition of the job that makes counsel's entries on steel — the text its code is written to. It
lives here, in the court, so that a change to how counsel's acts are made is a proposal read like any other,
not a file on a machine (the same reason `transcripts/sessions/` holds the session prompts). The code is the
builder's (SPEC §10.8): today the runner's `.github/workflows/counsel-sign.yml` and `.github/scripts/counsel-sign.py`
in `renavondata/opencode-runner`, installed by the sovereign on 7 November (#369) — a repair by §7's letter,
listed as one; in C2c-1, `tools/runner/` in this repository, fetched by the runner. The job of 6 November (`counsel.yml`, `counsel-act.py`) keeps making
counsel's GitHub acts (pull requests, issues, closes) and skips sign requests.

## What it holds

- `~/.ssh/jack-counsel-3` (private; generated on steel by the sovereign; never in a prompt, a chat or a repository).
- `COUNSEL_GH_TOKEN` (else `~/.config/jack/gh-counsel`): `assize-reviewer`'s token, under the grant of seq 2131 —
  on `renavondata/jack`, opening counsel's proposals and closing its own stale ones with a comment; on
  `renavondata/opencode-runner`, filing and closing issues. It posts no comment on any other issue (the grant does
  not cover it); it reports in the job's log and, on a refusal, files one issue.

## When it runs

On every push to `counsel-requests` in `renavondata/opencode-runner` that adds `requests/sign-<id>.json`
(`{"id": "sign-<id>", "act": "sign", "branch": "counsel/<name>"}`), on the `build` lane, with a 45-minute
limit (a proposal's check runs the tests, the pins and the count). A push adding no sign request exits green
before it looks for the key.

## What it does, in order, for the branch each trigger names — and refuses otherwise

1. The branch is `counsel/<name>` with `<name>` one token, and `origin/counsel/<name>` exists.
2. **The trailer is the key's.** The pubkey beside the private key is looked up in `main`'s log; it must be
   declared exactly once with powers, and the trailer the verbs will write is `Proposer: <principal> <key_id>`
   from that declaration (RUNBOOK, Common: key and party) — never a name typed into the job.
3. **The worktree is RUNBOOK's:** `~/git/worktrees/jack/counsel/<name>`. If it exists, its branch must be
   `counsel/<name>`; it must hold no commit `origin/counsel/<name>` lacks (a run that stopped after signing a
   forecast leaves one, and it stands — the job refuses and says to push it by hand); and it must be clean.
   Then it is reset to `origin/counsel/<name>`. If it does not exist, it is created there. Nothing is deleted.
4. **The whole request is read and checked before anything runs.** `transcripts/requests/<name>.jsonl` at the
   head: every line is a JSON object; every `verb` is `forecast` with `claim` (string), `p` (integer) and `by`
   (string), or `proposal` with `title` (string); `proposal` occurs exactly once and last. Otherwise refused,
   nothing signed.
5. **Signed once, checked before any merge, and the act finished.** The content commit is found as the
   `proposal` verb finds it: the newest commit reachable from the head and not from `origin/main` that changes a
   path other than `log.jsonl` (merges against each parent, renames on both sides). If the branch's `log.jsonl`
   already holds a `proposal` by this key's principal with that commit, nothing is signed; if no open pull
   request has the branch as head, one is opened with the request's title (the verb's own unfinished ending).
6. If the branch does not contain `origin/main`, `origin/main` is merged into it with the trailer of step 2.
   A conflicting merge is aborted and the request refused, nothing signed.
7. **The branch touches only counsel's paths.** `git diff --name-only --no-renames origin/main...HEAD` is
   compared with the `counsel` row of `judge/scope.json` *at `origin/main`*; any path outside it (so any change
   to `tools/`, `kernel/`, `judge/`, `pins/`, `tests/`, and a rename out of them) refuses the request before
   anything is signed. After step 6 the branch's `tools/` is therefore `main`'s, and the verbs that run are the
   ones `main` holds.
8. With `JACK_KEY=~/.ssh/jack-counsel-3` and `GH_TOKEN` counsel's, each `forecast` line runs as
   `tools/jack forecast "<claim>" --p <p> --by <by> [--type <type> --args '<args>']` and the `proposal` line as
   `tools/jack proposal --title "<title>"`, one at a time, each after the last has printed. The verbs push the
   branch and open the pull request. A refusal stops the request at that line: the entries before it stand as
   lawful (RUNBOOK: branch verbs undo nothing), the refusal is printed verbatim and filed as one issue on the
   runner, and nothing is retried or forced.
9. **The receipt** is the run itself: the trigger `requests/sign-<id>.json` on `counsel-requests` names the
   branch, and the `counsel-sign` run on that push prints what it signed. The job comments on nothing (the grant
   of seq 2131 does not cover it); B6's test reads the trigger and the run, not a comment.

## What it never does

Sign anything not in the request file; run a verb other than the two; run a branch's own code (step 7); touch
`main`; delete or reset away anything; comment on any issue or pull request; read `log.jsonl` whole into a model.

## Custody, disclosed

Whoever can push a `counsel/*` branch to jack *and* a trigger to `counsel-requests` is counsel: today, the
sovereign's git credentials, which the drafting session uses for pushes (pushes are not acts, COUNSEL-OPEN row 44).
Two further routes reach the key and are not closed by this definition: every runner on steel runs as the login
user `g`, whose home holds every party key and a `gfrmin` login with admin scopes (`opencode-runner` issue #188),
and `run.yml` exports whatever `key:` an issue body names as `JACK_KEY` to the session it starts. So any session
on steel, and anyone who can file a `run` issue, can sign as any party. The fix is #188's — a runner user that
holds only the job's credentials — and it is the sovereign's, once; until then this courier is as strong as the
host, and the enforcement map's `irreversible` row says so.

## Pin, when the courier is code in this repository

`courier_signs_only_the_request`: the entries on the branch after the content commit are exactly the request
file's lines, in order, signed by `counsel`; a branch changing `tools/` is refused unsigned. Mutants: a forecast
entered from the prompt; `tools/` of the branch run instead of `main`'s.

## The script

Counsel touches documents only; code enters from a builder (SPEC §10.8), so the script is not here. Its
runner copy is `.github/scripts/counsel-sign.py` in `renavondata/opencode-runner` (#369, merged 7 November; v3 on
the branch `counsel-sign-v3`, with U2's narrowing of `counsel-act.py`), written to this definition; in C2c-1 a builder brings it into the
court as `tools/runner/counsel-sign.py`, built to this text, with the workflow that runs it, and the runner's
copy becomes a fetch of that file from `main`. Until then, any difference between this text and the runner's
script is a finding against the script.
