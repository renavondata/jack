# Runbook — the verbs of jack

An act on the record is a verb of `tools/jack`, one verb per entry type, seven in all. A verb prepares the
entry on the head of the log it acts on, signs it with the caller's key, appends it only if the kernel admits
it, and then performs the effects the entry authorises — and nothing else. What is not a verb is not done; a
new verb needs a new entry type, which needs SPEC text and an `amend`. The vocabulary is the same for every
party, cut down by the powers its key holds: the kernel refuses an entry the key may not sign (`no_power`),
so the CLI decides nothing. `tools/jack` is outside the trusted base: an entry written by hand gets the same
verdict. (Authority: CHARTER §5, §7; SPEC §10.6; A2 clauses 6, 7, 9 and 10; the research of 18 October, (d).)

This text states what each verb must do, must refuse and may never do. How a verb does it is the builder's,
pinned by the tests; a cold read measures the code against this text, and a builder who finds the text
cannot be implemented files `spec_conflict` rather than deciding.

## Common to every verb

- **Root and log.** The repository root is the directory above `tools/`; the log is `log.jsonl` there. A verb
  acts on the log of the working copy it runs in, except `merge` and `push`, which act on another branch's
  log in a copy of their own and leave the caller's copy as they found it.
- **Key and party.** `--key PATH` names the private key; default `$JACK_KEY`, else `~/.ssh/id_ed25519`. The
  party is never an argument: it is the `principal` of the key the log declares for that public key, and it
  is the entry's `proposer` and the trailer's first field. A key the log does not declare, or whose principal
  is not one token of `[a-z0-9_-]+` (the rule the `key` verb applies at declaration), is refused before anything
  is signed; the verbs keep no list of parties of their own (PR #66, 31 Oct — until then `tools/jack` whitelisted
  five and refused the herald's key, COUNSEL-OPEN 18).
- **Time.** `ts` is the clock, UTC, `YYYY-MM-DDTHH:MM:SSZ`. The verb reads the clock; the kernel never does.
- **Signing.** `ssh-keygen -Y sign -n core-entry` over the canonical message (SPEC §6), through `tools/entry.py`;
  the line is appended only if `kernel.check` admits the log with it. The master key (the key whose
  principal is `guy`; the verbs test the principal) prompts for its passphrase; party keys do not.
- **Commits.** A verb's commit message is `<type>: <summary>` — `key: <KEY_ID>`, `proposal: <title>`,
  `spec_conflict: <section>`, `merge: #<N>`, `push: <BRANCH>`, `decision: <KIND> <SUBJECT>`, `amend: <ID>` — an
  optional body, and as its **last paragraph** `Proposer: <party> <key_id>`. A trailer is **filled** when it is
  one line whose first field is one of the five party names, at least one field follows it, and no field
  contains `<`: the verbs write `<party> <key_id>`, and a commit made by hand carries
  `<party> <model id> <session id>`, as the judge read it at C0. An unfilled trailer is refused, written or read.
- **No environment variable** changes what a verb requires or does. `JACK_KEY` names a key and nothing else;
  the tests patch constants in-process, never through the environment.
- **Up to date and clean.** Every verb fetches first. Main verbs require HEAD to equal `origin/main`; branch
  verbs require the branch to contain `origin/main`. A tree with anything the verb does not itself stage, a
  detached HEAD in the caller's copy, `main` for a branch verb or any other branch for a main verb: refused.
- **Refused in code, always:** `--admin`; `--force` or `+` refspecs; deleting any remote branch; creating a
  tag; rewriting any commit. A verb only appends commits, and a push that is not a fast-forward is a refusal,
  never a retry with force.
- **Main verbs** (`key`, `decision`, `amend`, `push`) run on `main`: effect, entry, commit, `judge/selfcheck.py`,
  push, in that order, and `main`'s run watched. Whatever fails before the push leaves `main` equal to
  `origin/main` with nothing of the verb's left in the tree and nothing pushed; the remote never shows an
  effect without its entry or an entry without its effect.
- **`merge`** runs on `main` but appends its entry to the proposal's branch (SPEC §10.6); its effect is
  GitHub's merge, performed only after the judge has admitted the entry. It has no undo: nothing it does
  reaches `main` except through the judge.
- **Branch verbs** (`proposal`, `spec_conflict`) never touch `main`. If the push or the pull request fails after
  their commit, the commit stands as lawful and the verb says how to finish the act; it undoes nothing.
- **The ledger.** Every act is an entry; every piece of evidence an entry relies on is referenced from it by
  hash (`push.digest`, `push.review`, `push.record`); files under `transcripts/` are evidence, never the record.
  A builder's objection is a `spec_conflict` entry, not a note.
- **Liveness.** A verb waiting on GitHub waits as long as GitHub takes and says what it is waiting for; it
  never turns a pending verdict into a refusal. An interrupted wait undoes nothing.

## `jack key KEY_ID --principal P --powers a,b,c --pubkey FILE`

Entry: `key` with the declaration (SPEC §5). Refuses: a pubkey file that is not a two-field `ssh-ed25519` line
(`ssh-keygen` writes three — strip the comment first: `cut -d' ' -f1,2 ~/.ssh/x.pub > /tmp/x.pub`, or generate with `-C ""`);
a power outside the kernel's `TYPES` (ten from C1a); a principal that is not `[a-z0-9_-]+`; a re-declaration of the signer's own
`key_id` without `key` (the kernel's guard would refuse it too; the verb says so first). Keys per party:
from C1a (seqs 31–34), `builder-2` {proposal, spec_conflict, forecast, resolution}, `reviewer-2` {proposal,
forecast, resolution}, `counsel-2` {proposal, forecast, resolution}; the master key holds every power. Earlier key_ids
(`builder-1`, `reviewer-1`, `counsel-1`) stay declared with their C0 powers and are not used. Revocation is
this verb with `--powers ""`. The herald is `herald-2` {merge} (seq 201), principal `herald`, whose private key lives
on steel at `~/.ssh/jack-herald` and is used only by the `herald` workflow of `renavondata/opencode-runner` (every
ten minutes: `jack merge N` on each open pull request whose head GitHub has admitted); `herald-1` {merge, resolution}
and `builder-3`, counsel's, are revoked once `herald-2` has merged once (COUNSEL-OPEN 17).

## `jack proposal [--title T]`

On a branch other than `main`, every change committed, the branch containing `origin/main` (otherwise refused,
naming the merge to run: `git merge origin/main -m "Merge main into <branch>" -m "Proposer: <party> <key_id>"`).
Refuses unless the check passes: `python3 -m unittest discover -s tests -t .`, `python3 pins/run.py`,
`python3 tools/count_kernel.py`. Entry: `proposal` {title: T, default the subject of the work commit; commit: the
last commit on the branch that changes a path other than `log.jsonl`, the work}. Effect: `log.jsonl` committed on top of the work, the branch pushed, a pull request
against `main` opened — or, if the branch has one, nothing more. Nothing but `log.jsonl` may follow the
entry's `commit` on the branch (SPEC §10.7): work added later is proposed again, on top, and the earlier
entry stands as history.

## `jack spec_conflict --section S --text T`

On a branch, with `proposal`'s preconditions and no check: a conflict is filed exactly when the tests cannot
be made to pass (A2 clause 9). Entry: `spec_conflict` {section, text}. Effect: `log.jsonl` committed, the
branch pushed, a pull request titled `spec_conflict: <section>` opened or the branch's retitled so, and
"stopped: the specification cannot be implemented as written; see PR #n" printed. The builder stops here.

## `jack merge N`

On `main`. Preconditions: PR N is open against `main` and mergeable; its head is the `commit` of a valid
`proposal` entry in its log followed only by commits that touch `log.jsonl` (SPEC §10.7; or, until the judge
checks it, carries a filled trailer); and GitHub
has admitted that head — the verb waits while `judge` or `tests` is unreported or running, and refuses if
either failed. Entry: `merge` {proposal: N, commit: that head, checker: the trusted-base digest of `main`'s
tree (`tools/digest.py`; SPEC §10.6 refuses any other)}, committed `merge: #N` with the trailer and pushed to
the PR's branch as a fast-forward only — a rejected push means the proposal moved: refused, run again. Effect:
GitHub's merge of exactly the commit the verb pushed, H, and only once GitHub reports `judge` and `tests`
passed on H; a head other than H, or a check that fails, is a refusal with the entry standing on the branch;
no other commit is ever merged (`--match-head-commit H`). Then `main` pulled and its run watched. The merge
commit GitHub makes is the effect of the entry that precedes it. GitHub's protection of `main` requires the
same two checks, independently of the verb. When the clerk holds `merge`, this verb is unchanged.

## `jack push BRANCH --review FILE | --review none [--opens LAYER]`

The only way a change to the trusted base reaches `main`, and the only verb that pushes to `main` anything
but an entry. On `main`; BRANCH is a local branch another party built, and the verb never commits to it.
Refuses, each with its reason: BRANCH not containing `origin/main`; a trusted-base digest equal to `main`'s
("nothing to push: propose and merge"); a commit on BRANCH not on `main` without a filled trailer; the check
(as `proposal`) failing on BRANCH's tree. **The run of record** is required when `kernel/` or any kernel2
production source (`checker.go canonical.go ed25519.go signature.go main.go`) differs from `main`'s, and is
made by the verb itself, never accepted from BRANCH (the accused does not write its own test, CHARTER §1 F1):
`kernel2/check` built once, then `harness/diff.py --seeds A:B --b kernel2/check` in twelve parts,
`transcripts/diff-100000-<T>-part00..11.json`, contiguous from 0 to 100,000, each reporting `commit` equal to
BRANCH's head, `logs` equal to its range, no disagreement, nothing uncompared; anything else is a refusal.
`--review FILE` is copied to `transcripts/` and its SHA-256 is the entry's `review`, an empty file included;
`--review none` records 64 zeros and warns that this push was not read. Effect: BRANCH fast-forwarded onto
`main` (never a merge commit, never a rebase), the parts and the review placed under `transcripts/`, and
entry `push` {digest: `tools/digest.py` of the tree now on `main`; review; record: the SHA-256 of the twelve
parts' bytes concatenated in name order, or 64 zeros when no run was required — an optional member, SPEC §5},
committed `push: BRANCH`; the self-check runs with the new trusted base and the entry both in place. On any
failure `main` returns to `origin/main`, BRANCH untouched. `--remove` removes BRANCH's worktree afterwards.

**`--opens LAYER`, the read gate** (#182, 2 November; BRIEF-C2b §Scope (a)). Required when BRANCH changes
`judge/scope.json`, refused when it does not; LAYER is letters, digits, `_` and `-`, and the layer is read
from `--opens`, never from `scope.json`'s `layer`. The verb then requires, on `origin/main`,
`transcripts/BRIEF-LAYER-draft.md` and at least one `transcripts/REVIEW-LAYER-*.md` that
- begins `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`;
- has a `Reviewed tree:` line naming a commit on `origin/main` at which the brief's bytes equal
  `origin/main`'s; and
- was brought to `main` by a `proposal` entry signed by a key whose principal is not counsel, whose
  commit adds the file with the blob `main` now holds.

Each review that fails a test is reported, and the push is refused only when every one fails. So a brief
edited after its reads makes them stale, a read carried by counsel's key never counts, and a later edit of
an accepted review's first lines breaks it. The gate establishes the provenance and freshness of a read,
nothing about its reasoning. Example, C2a-prime's opening: `jack push opening-c2a-prime --opens C2a-prime
--review <worktree>/transcripts/REVIEW-C2a-prime-code.md`, after the sovereign's `decision grant` and
`decision fix` (BRIEF-C2a-prime v7 §Order of acts).

**A layer with a window file (BRIEF-C2c-1 §2 and §6; in force for every opening push after C2c-1's, whose
own push carries this extension and so is gated by the rule above and the sovereign's check at the
sitting).** When `transcripts/windows/LAYER.json` is on `origin/main`, the verb requires as many distinct
`transcripts/REVIEW-LAYER-*.md` files as that file's `numbers.readers` says, each passing the three tests
above and each with a `Reviewed tree:` at which the window file's bytes, as well as the brief's, equal
`origin/main`'s — in place of the refusal rule above: fewer such files refuses the push, however many
others are on `main`. The number comes from the window file and from nowhere else. Without a window file
the rule above stands, one review of the brief.

## `jack decision KIND SUBJECT`

On `main`. KIND is one of `veto promote budget grant transmute fix`; SUBJECT a non-empty string (for
`transmute`, the amendment id; for `grant`, the capability, such as a sealed judge image by digest; for
`promote`, the layer). Entry: `decision` {kind, subject}. The judge admits a `decision` only from a key
declared in genesis (SPEC §10.14).

**`promote`.** The verb runs `tools/status.py` for the layer on `HEAD`, at the instant it will sign and
with the `tests` runs GitHub lists, and refuses unless that prints `promote <layer>: lawful`. `--acts FILE`
gives the status tool the acts table that criterion 7 reads. From C2a-prime's opening push, with `--acts`
the verb also refuses unless FILE as given matches `transcripts/evidence/[A-Za-z0-9._-]+\.csv` whole and
its bytes are the blob at that path in `HEAD`'s tree, and the entry's body has a third member, `acts`
{path, sha256, commit}: the path as given, the SHA-256 of those bytes, and `HEAD`, the parent of the
commit that carries the entry (BRIEF-C2a-prime, change 4, as its Amendment 7 states it). Without `--acts`
the body is {kind, subject}.

## `jack amend ID FILE [--activate-at N]`

On `main`. Refuses without a valid `decision` of kind `transmute` with subject ID in the log ("transmute
first"); FILE not beginning `## Amendment ID:`; ID already an amendment. Effect before the entry: a blank line
and FILE appended to `CHARTER.md`. Entry: `amend` {id, charter: the SHA-256 of the new `CHARTER.md`,
activate_at: N as given, the entry's seq + 1 when omitted}; `CHARTER.md` and `log.jsonl` in one commit (judge
items 2, 12, 13 on the way in).

**Order of an amendment (A2 clause 7, the research's protocol):** `jack decision transmute ID` → the pushes
that build the amendment's mechanisms, each by `jack push` → `jack amend ID FILE` last, so that an amendment's own
mechanisms are on `main` before its text is in force (A3.5 is the order's precedent; A2 was recorded before
its mechanisms and is the one exception). This is not a claim that the charter never says what the code
does not enforce: A2.8's monitor is unbuilt (`LAW.md`), and §3's witnesses and lapse wait on A2.1. A2.7's
separate rule, no `push` between an `amend` and its height (SPEC §10.12), is enforced.

**Text before code.** A change to `SPEC.md` that needs code is the first commit of the builder's branch —
counsel's patch, applied and read by Guy there, with counsel's trailer — and reaches `main` in the same
`jack push` as the code built to it: `main` never carries a text its judge and checkers do not implement, and
is never red by design. A change to `SPEC.md` that needs no code is pushed on its own, with its `push` entry.
This runbook is counsel's and `tools/jack` the builder's, so they cannot share a proposal (`party_scope`):
the text lands first, by counsel's `proposal`, and the builder builds to the text on `main` (A2 clause 9);
a verb that departs from the text is a finding, whichever of the two moved last.

## `jack forecast "CLAIM" --p N --by TS [--type T --args JSON]`

Entry: `forecast` {claim, p: N (an integer 1–999, per mille), resolves_by: TS, and, when given, type
and args}. For every party but the master key a **branch verb**: it appends the entry and commits
`forecast: <claim, truncated>` on the current branch, touching `log.jsonl` only, before or after that
branch's `proposal` entry (SPEC §10.7 admits log-only commits on either side); a forecast about the
branch's first CI run is made **before** `jack proposal`, which is what pushes the branch. For the
master key a main verb. Refuses: N outside 1–999; TS not an instant, or earlier than the verb's clock;
an empty claim. A forecast is never edited; a wrong forecast is data.

## `jack resolve SEQ --outcome 0|1 --evidence E`

Entry: `resolution` {forecast: SEQ, outcome, evidence: E}. Branch or main verb as `forecast`. Refuses
before signing, each with the kernel's own reason: SEQ not a `forecast`, or already resolved; the
caller's principal equal to the forecast's (`self_judged`). E is a run id, a commit, or
`sha256:<hex64>` naming a file `transcripts/evidence/<hex64>` already in the tree (the verb checks the
hash). Evidence files are **work**: the resolver commits the file, runs `jack proposal` (title
"evidence for forecast SEQ"), then `jack resolve` on the same branch; evidence already on `main` needs
no new proposal.

## `jack score [--as-of TS]`

No entry, no signing, no fetch; reads `log.jsonl` of the working copy. Prints, per (`proposer`,
`type`) with at least one resolved forecast: resolved, mean p over resolved (as a fraction), outcome rate, mean log-loss, and the base-rate
log-loss, all as `BRIEF-C1.md` defines them (natural logarithm; prequential Laplace base rate
pooled by type in resolution-seq order; four decimals, half to even); then the same per `proposer`
and per `type` alone, each row preceded by its count of forecasts, resolved or not. With `--as-of TS` it also
lists every unresolved forecast whose `resolves_by` is before TS, by `resolves_by` then seq. The
witness is `spec/vectors/score.jsonl` (the reviewer's; the builder's `tests/vectors/score.jsonl` must agree
with it in meaning) and its expected table in the brief (pin `score_not_proper`).

## `jack elect` — `python3 tools/elect.py --invite STREAM W0 | --replay SEQ | --resolve-plan SEQ | --table [--as-of T] [--sigma B64] [--log FILE]`

C2b's election (BRIEF-C2b §Scope: the entrants, the round's gain, the election, the draw; §Order of acts
step 4). **C2b holds no live round** (BRIEF-C2b Amendment 10): `tools/elect.py` rides C2b's opening push with W5 and their
pins (clause 5) and is tested, not run — no invite is entered, no per-invite session is filed, `herald-2` holds no
`forecast` power, and the stream's shape stays the three-window forecast session the diary files. The rest of this
section describes the verb, and the window that first runs rounds: there the diary consults it before every
forecast session, invites entered before the attack tests are green are not rounds, and from the first invite
each round's forecasts come from the invited arm's own session, filed per invite, and no session is filed
without one.
The roster is fixed in the file, *K* = 3 arms — (reviewer, `openai/gpt-5.4-mini`), (builder,
`openai/gpt-5.4-mini`), (reviewer, `openai/gpt-6-astra-fast`) — and does not change inside the window (pin
`roster_fixed`). Four EXP3 instances; round *t*, the *t*-th hourly window after the opening, draws on
instance *t* mod 4, and only once that instance's previous round is resolved (pin `instance_feedback_complete`).
The stream is `freshness`; a round's loss ℓ is the mean log-loss over its six events, a missing forecast, a
missing evidence page or an event unresolved by the invite's deadline counting ln 1000, and the gain is
(ln 1000 − ℓ) / ln 999 (pins `gain_in_unit_interval`,
`round_loss_is_mean`, `bad_round_kept`).

- `--invite STREAM W0` — the diary's call for the stream's hourly window starting at W0, before the arm's
  session is filed. Reads the prefix at `--as-of` (default now; the log must pass the kernel), runs
  `tests.test_elect.Election.test_self_invite` and `test_rigged_election` and refuses on a red tree; refuses
  a (stream, W0) already invited (`revision`), a W0 outside the window or a stream other than `freshness`, and
  a call at or after W0 (`skipped: W0` — the round is skipped, no invite and no session, the hour reported as
  skipped); exits 3 with `wait: instance j round t unresolved` while the instance's previous round is
  unresolved, to be called again before W0. Otherwise it prints the round string `election.invite STREAM W0`,
  signs it under `~/.ssh/jack-herald` (σ; `--sigma` supplies a signature made elsewhere; one that does not
  verify is `rigged_election`), draws the arm on the 2^256 grid from σ, and prints the entry body — `claim`,
  `p` (the invite's success event, prequential Laplace over the settled invites, (*s* + 1)/(*n* + 2) in
  permille; pin `invite_p_is_success_rate`), `type`, `resolves_by`, `args` with `round`, `instance`,
  `gains`, `cuts`, `propensity`, `gamma`, `eta`, `sigma` — which the diary enters under the herald's key before filing the arm's session (pins
  `invite_before_session`, `draw_on_the_grid`, `sigma_verifies`, `self_invite`, `rigged_election`). The
  importance weight divides by the propensity saved in the invite, never a later one. Every other refusal
  exits 1.
- `--replay SEQ` — recomputes the invite at seq SEQ from the prefix before it and verifies σ; prints
  `election invite SEQ: replay verified` or the first error (pin `draw_replays_from_prefix`). Read-only.
- `--resolve-plan SEQ` — prints the resolver the invite at SEQ routes to, never the arm that forecast
  (pin `resolver_not_forecaster`). Read-only.
- `--table` — per arm: rounds invited, Ĝ summed over the instances, mean gain, successes, frequency, mean
  recorded propensity; per instance: last round and whether it is resolved; the skipped rounds, the
  diagnostic, the `election.invite` lines of `jack score`, and any invite the audit refused. Read-only.

Only `--invite` signs, and only with the herald's key (`~/.ssh/jack-herald`, held on steel, the sovereign's
machine); the verb checks no host. No mode writes to the tree or to `log.jsonl`.
The twins are `tests/test_elect.py`'s; the pins are BRIEF-C2b's §Pins.

## `jack clerk` — `python3 tools/clerk.py [--as-of T] [--runs FILE] [--acts FILE] [--counsel-open FILE]`

C1b's clerk (BRIEF-C1b v7): every open writ of classes W1–W4 (W5 below is `status.py`'s), derived from `log.jsonl`, the tree and the clock, printed with
its class, obligation, holders and deadline; one past its deadline reads `ESCALATED to guy`. Read-only,
level-triggered, no state, no signing, no network: run it on a timer or by hand, and a missed tick costs
nothing. Writ classes: **W1** — every `forecast` on the prefix with no `resolution`, **from the log's first
entry and under every subject** (BRIEF-C2c-1 R4, from C2c-1's opening push; until then `tools/clerk.py`
computes it only when the window is C1b, jack #350, and under a later window a forecast appears only once
overdue, as a W4 line); holders are
the keys with `resolution` power whose principal is not the forecaster's; deadline `resolves_by`,
overdue strictly after it; discharged by a `resolution`. **W3** — a `merge` entry whose `commit` has no
`tests.yml` run with `conclusion` success and `updated_at` not after the merge entry's `ts` in `--runs FILE`
(a JSON array in the shape of the Actions API's `workflow_runs`); holder counsel; deadline the window's end;
discharged by a row of `transcripts/COUNSEL-OPEN.md` containing the literal `W3 merge <seq>`. **W4** — every
line of `status.py` that is not `met`, including `off-log repairs: n` from `--acts FILE` (the weekly acts
CSV saved under `transcripts/evidence/`; absent, the line reads `unknown` and is a writ) and a `decision
promote` entered while a criterion did not hold at its instant (a sovereign REPAIR, which no later success
erases); holder counsel; deadline the window's end. Evidence not supplied is unverified, never green.

**W5** — counsel's dated writs, the class that scores counsel's own obligations (BRIEF-C2b §Scope (b) and
Amendments 6–8; on 8 November 2026 two of its rows, `c2a-report` and `runbook-c2b`, are past due and undone): every row of
`transcripts/COUNSEL-DUE.jsonl`, `{"id", "due", "what", "done": null}`, is a writ held by counsel. W5 lands at
the `ts` of the first `merge` on the prefix whose `commit` holds `tools/due.py`, after C2b's opening push and
first under its cap; the file is seeded at the opening with every dated obligation of COUNSEL-OPEN and of
BRIEF-C2b, and pin `w5_inventory` checks the seeded ids are present at every later tree. It is computed by
`python3 tools/due.py [--rev R] [--as-of T] [--root DIR] [--inventory COMMIT]`, **not** by `tools/clerk.py`,
and printed by `status.py` beside W1–W4. `--rev` names the commit whose file and `log.jsonl` are read (its
parent's file for the append-only check); `--inventory COMMIT` fails with `W5: missing <id>` when an id seeded
in that commit's file is absent from the one read. One line per row: `W5 <id> due <due> <what>: OPEN`,
`ESCALATED <h>h past due`, `done seq <n> on time` or `done seq <n> ESCALATED <h>h late`; `W5: no COUNSEL-DUE
file` when the tree has none.

Rows are append-only — a file whose earlier lines changed is refused. A row is
discharged only by a later line `{"id", "done": {"seq": n, "what": "<the act>"}}` whose `seq` is an entry on
the prefix whose canonical body contains the row's `id` (a proposal whose title names it; a forecast or
resolution whose `args.id` is it); a bare integer, an unrelated entry or a deleted row discharges nothing. The
discharge takes effect at the later of the cited entry's `ts` and the `ts` of the first `merge` on the prefix
whose `commit` holds the discharge line byte for byte (Amendment 7): before then the row is undone; on time
if that instant is at or before the due, ESCALATED late if after, and a late discharge prints
ESCALATED-then-done forever.

The fold also admits a re-date line with exactly the keys `{"id", "due", "seq", "why"}` for exactly
the two rows Amendment 6 names (`c2b-report` → `2026-12-02T12:00:00Z`, `c2c-brief` → `2026-11-16T00:00:00Z`,
`seq` 1564, first such line for its id, after the row and before any discharge); any other line with those
keys, or a malformed `done`, exits 2 — `W5: malformed COUNSEL-DUE file`, or `W5: <error>` where the fold itself fails. Seven pins:
`w5_overdue_escalates`, `w5_done_is_an_entry`, `w5_rows_append_only`, `w5_inventory`, `w5_redate`,
`w5_escalation_history`, `c2b_history_from_w5`. BRIEF-C2b's criterion 8 reads tick files under
`transcripts/evidence/w5/` (`status.py`'s W5 lines as of an instant, committed at the first prefix after a row's
due), not a reconstruction, and no session commits them: the step was never built and is struck for C2b
(Amendment 11). Its printed-escalation clause applies only to rows whose due falls after W5 lands — the first
merge on the prefix whose commit holds `tools/due.py`, which with the code on C2b's opening push is the first
merge after it — and not at all on a prefix with no such merge (Amendment 8); so C2b's window holds no row that
falls due inside it (Amendment 11 clause 3: the seed is the file as `main` holds it at the opening push).
BRIEF-C2c-1 (draft v18, on `main`) R5 retires W5 from C2c-1's opening push, if that push is made as the
brief states: what it tracked becomes claims on the log.

`python3 tools/status.py` now reads C1b from the log — opened by `decision promote C1a`, ended by the counsel
forecast with `args.id` `L0` — and prints the item process of §Liveness (the herald's act as the item, every
sovereign repair tainting every writ open at its instant, p₀ = 6/11, exact fractions), `late-reported
repairs: n`, criterion 3 from the tree, criterion 7 from `tools/enforcement.json`, and one line `promote
<window>: lawful` or `refused: <every criterion not established>`; criteria 1 and 2 come only from `--run
FILE`, the `tests.yml` push-to-main run for the tree's exact commit, verified field by field.

`jack decision promote <window>` fetches that run itself with `gh api`, runs `status.py` with it, and signs
only when the line reads `lawful`; on `refused` it prints the line and signs nothing. From C2c-1's opening
push (BRIEF-C2c-1 §6) the verb promotes any `<window>` whose file `transcripts/windows/<window>.json` is on
the tree, and no other — the list of names it promotes today (`C1a`, `C1b`, `C2a`) goes — takes no `--acts`
(the acts evidence is the newest pair of `transcripts/evidence/acts-<window>-<repo>-<stamp>.csv` files in
the tree, as the window file's `evidence.acts` defines it), writes nothing to the tree, and refuses
`promote` when no pair exists or the newest pair's stamp is not within the file's
`numbers.acts_fresh_minutes` before the decision's `ts`. The sovereign's hand
repairs are entered as `jack decision fix "<what>"` when made (§7): a repair taints every writ open at its
instant whatever its subject says, so the subject is for the record, and one entered after the item it
concerns was finalised changes no score but prints as a late report that refuses `promote` while it stands.

## Working copies (no verbs; nothing here touches the record)

Working copies live under `~/git/worktrees/jack/`: a branch's worktree at `~/git/worktrees/jack/<branch>`, a
room at `~/git/worktrees/jack/<name>-room`. Nothing else goes there, and nothing of jack's goes anywhere else
but `~/git/jack`.

- A builder works in a worktree cut from a pulled `main`: `git worktree add ~/git/worktrees/jack/<branch> -b
  <branch> main`, with `JACK_KEY=~/.ssh/jack-builder` in its environment. It reads the text it builds to,
  touches only the paths that text names, and ends with `jack proposal` or `jack spec_conflict`.
- A reviewer reads cold in a copy with no history: `R=~/git/worktrees/jack/<name>-room`, `git archive <ref> |
  tar -x -C $R`, `git diff <merge-base> <ref> > $R/DIFF.patch`, `git init` there. Its findings are pins,
  proposed under `~/.ssh/jack-reviewer` with `jack proposal`; a round that adds no pin ends the review (A2
  clause 9).
- The kernel2 author works in a room holding only `SPEC.md`, `spec/`, `tests/vectors/` and `kernel2/`, reads
  nothing else, and leaves `QUESTIONS.md` saying `none`; its work enters by `jack push`.

## Bound and custody

`tools/jack` is one Python file, standard library plus `tools/entry.py`, `kernel` and `judge` imports. It was
written to a bound of 250 lines. It is 329 as `tools/count_kernel.py` counts (5 November 2026), and no test or pin
holds it to any bound (the audit's §3.6 D4; `REVIEW-audit-3-6-argon.md`, whose pin `jack_bound_250` is on
`review-audit-3-6`). Whether a bound is restated and enforced is for the C2c brief. It it is untrusted, enters by pull request, and is read cold.
Its tests prove effects, not calls: `gh` and `ssh-keygen` are stubs on `PATH` that record their arguments and
answer as GitHub would from a fixture remote, the judge's check being the real judge's verdict on the live
head, and a test of a verb's ending asserts what the remote now holds. A fixture's proposal touches only
paths its party may touch. Every finding of a cold read becomes a test there before its fix. If a verb
cannot be written within the bound, `--dry-run` is cut first, `gh run watch` second and `--remove` third
(each printed as a command instead); the verbs and their refusals are not.
