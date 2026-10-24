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
  is not one of SPEC §10.7's five parties, is refused before anything is signed.
- **Time.** `ts` is the clock, UTC, `YYYY-MM-DDTHH:MM:SSZ`. The verb reads the clock; the kernel never does.
- **Signing.** `ssh-keygen -Y sign -n core-entry` over the canonical message (SPEC §6), through `tools/entry.py`;
  the line is appended only if `kernel.check` admits the log with it. The master key prompts for its
  passphrase; party keys do not.
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

Entry: `key` with the declaration (SPEC §5). Refuses: a pubkey file that is not a two-field `ssh-ed25519` line;
a power outside the eight; a principal that is not `[a-z0-9_-]+`; a re-declaration of the signer's own
`key_id` without `key` (the kernel's guard would refuse it too; the verb says so first). Keys per party:
`builder-1` {proposal, spec_conflict}, `reviewer-1` {proposal}, `counsel-1` {proposal}; the master key holds
the rest. Revocation is this verb with `--powers ""`.

## `jack proposal [--title T]`

On a branch other than `main`, every change committed, the branch containing `origin/main` (otherwise refused,
naming the merge to run: `git merge origin/main -m "Merge main into <branch>" -m "Proposer: <party> <key_id>"`).
Refuses unless the check passes: `python3 -m unittest discover -s tests -t .`, `python3 pins/run.py`,
`python3 tools/count_kernel.py`. Entry: `proposal` {title: T, default the head commit's subject; commit: the
head's SHA, the work}. Effect: `log.jsonl` committed on top of the work, the branch pushed, a pull request
against `main` opened — or, if the branch has one, nothing more. Nothing but `log.jsonl` may follow the
entry's `commit` on the branch (SPEC §10.7): work added later is proposed again, on top, and the earlier
entry stands as history.

## `jack spec_conflict --section S --text T`

On a branch, with `proposal`'s preconditions and no check: a conflict is filed exactly when the tests cannot
be made to pass (A2 clause 9). Entry: `spec_conflict` {section, text}. Effect: `log.jsonl` committed, the
branch pushed, a pull request titled `spec_conflict: <section>` opened or the branch's retitled so, and
"stopped: the specification cannot be implemented as written; see PR #n" printed. The builder stops here.

## `jack merge N`

On `main`. Preconditions: PR N is open against `main` and mergeable; its head is one commit past the `commit`
of a valid `proposal` entry in its log (or, until the judge checks it, carries a filled trailer); and GitHub
has admitted that head — the verb waits while `judge` or `tests` is unreported or running, and refuses if
either failed. Entry: `merge` {proposal: N, commit: that head, checker: the trusted-base digest of `main`'s
tree (`tools/digest.py`; SPEC §10.6 refuses any other)}, committed `merge: #N` with the trailer and pushed to
the PR's branch as a fast-forward only — a rejected push means the proposal moved: refused, run again. Effect:
GitHub's merge of exactly the commit the verb pushed, H, and only once GitHub reports `judge` and `tests`
passed on H; a head other than H, or a check that fails, is a refusal with the entry standing on the branch;
no other commit is ever merged (`--match-head-commit H`). Then `main` pulled and its run watched. The merge
commit GitHub makes is the effect of the entry that precedes it. GitHub's protection of `main` requires the
same two checks, independently of the verb. When the clerk holds `merge`, this verb is unchanged.

## `jack push BRANCH --review FILE | --review none`

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

## `jack decision KIND SUBJECT`

On `main`. KIND is one of `veto promote budget grant transmute fix`; SUBJECT a non-empty string (for
`transmute`, the amendment id; for `grant`, the capability, such as a sealed judge image by digest; for
`promote`, the layer). Entry: `decision` {kind, subject}. The judge admits a `decision` only from a key
declared in genesis (SPEC §10.14).

## `jack amend ID FILE [--activate-at N]`

On `main`. Refuses without a valid `decision` of kind `transmute` with subject ID in the log ("transmute
first"); FILE not beginning `## Amendment ID:`; ID already an amendment. Effect before the entry: a blank line
and FILE appended to `CHARTER.md`. Entry: `amend` {id, charter: the SHA-256 of the new `CHARTER.md`,
activate_at: N as given, the entry's seq + 1 when omitted}; `CHARTER.md` and `log.jsonl` in one commit (judge
items 2, 12, 13 on the way in).

**Order of an amendment (A2 clause 7, the research's protocol):** `jack decision transmute ID` → the pushes
that build the amendment's mechanisms, each by `jack push` → `jack amend ID FILE` last, so the charter never
says what the code does not enforce. A2 was recorded before its mechanisms and is the one exception.

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
`forecast: <claim, truncated>` on the current branch, after that branch's `proposal` entry, touching
`log.jsonl` only (SPEC §10.7), so the forecast reaches `main` with the proposal it rides; for the
master key a main verb. Refuses: N outside 1–999; TS not an instant or earlier than now; a claim that
is empty. A forecast is never edited; a wrong forecast is data.

## `jack resolve SEQ --outcome 0|1 --evidence E`

Entry: `resolution` {forecast: SEQ, outcome, evidence: E}. Branch or main verb as `forecast`.
Refuses before signing, each with the kernel's own reason: SEQ not a `forecast`, or already
resolved; the caller's principal equal to the forecast's (`self_judged`). E is a run id, a commit,
or `sha256:<hex64>` of a file the verb has just placed under `transcripts/evidence/` from `--file`;
with `--file` the verb commits the file in the same commit as the entry.

## `jack score [--since SEQ] [--by proposer|type]`

No entry. Reads the log and prints, per proposer and per `type`: forecasts, resolutions, mean p,
outcome rate, log-loss, and the base-rate log-loss of that type to date (½ before any resolution);
then the forecasts unresolved past `resolves_by`, oldest first, which are C1b's obligations. The
score is log-loss on p/1000; nothing else is admitted as a score (pin `score_not_proper`).

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

`tools/jack` is one Python file within 250 lines as `tools/count_kernel.py` counts, standard library plus
`tools/entry.py`, `kernel` and `judge` imports; it is untrusted, enters by pull request, and is read cold.
Its tests prove effects, not calls: `gh` and `ssh-keygen` are stubs on `PATH` that record their arguments and
answer as GitHub would from a fixture remote, the judge's check being the real judge's verdict on the live
head, and a test of a verb's ending asserts what the remote now holds. A fixture's proposal touches only
paths its party may touch. Every finding of a cold read becomes a test there before its fix. If a verb
cannot be written within the bound, `--dry-run` is cut first, `gh run watch` second and `--remove` third
(each printed as a command instead); the verbs and their refusals are not.
