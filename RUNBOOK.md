# Runbook — the verbs of jack

An act on the record is a verb of `tools/jack`, one verb per entry type, seven in all. Each verb validates its
arguments, prepares the entry on the head of the log it acts on, signs it with the caller's key, appends it
only if the kernel admits it, and then performs the git and GitHub effects the entry authorises — and nothing
else. What is not a verb is not done; a new verb needs a new entry type, which needs SPEC text and an `amend`.
The vocabulary is the same for every party, cut down by the powers its key holds: the kernel refuses an entry
the key may not sign (`no_power`), so the CLI decides nothing. `tools/jack` is outside the trusted base: an
entry written by hand gets the same verdict. (Authority: CHARTER §5, §7; SPEC §10.6; A2 clauses 6, 7, 9 and
10; the research of 18 October, (d).)

## Common to every verb

- **Root and log.** The repository root is the directory above `tools/`; the log is `log.jsonl` there. A verb
  acts on the log of the working copy it runs in, or of a temporary worktree it makes and removes (`merge`,
  `push`).
- **Key and party.** `--key PATH` names the private key; default `$JACK_KEY`, else `~/.ssh/id_ed25519`. The
  party is never an argument: the verb reads the matching `pubkey` from the keys declared in the log and takes
  its `principal` as the entry's `proposer` and as the `Proposer:` trailer's party. A key the log does not
  declare is refused before signing.
- **Time.** `ts` is the clock, UTC, `YYYY-MM-DDTHH:MM:SSZ`. The verb reads the clock; the kernel never does.
- **Signing.** `ssh-keygen -Y sign -f KEY -n core-entry` over the canonical message (SPEC §6); the master key
  prompts for its passphrase, party keys do not. Assembly is `tools/entry.py`'s: the line is appended only if
  `kernel.check` admits the log with it.
- **Commits.** A verb's commit message is `<type>: <summary>` — `key: <KEY_ID>`, `proposal: <title>`,
  `spec_conflict: <section>`, `merge: #<N>`, `push: <BRANCH>`, `decision: <KIND> <SUBJECT>`, `amend: <ID>` — an
  optional body, and as its **last paragraph** `Proposer: <party> <key_id>`. A trailer is **filled** when it is
  one line whose first field is one of SPEC §10.7's five party names, at least one field follows it, and no
  field contains `<`: the verbs write `<party> <key_id>`, and a commit made by hand carries
  `<party> <model id> <session id>`, as the judge read it at C0.
- **No environment variable** changes what a verb requires or does. `JACK_KEY` names a key and nothing else;
  the tests patch constants in-process, never through the environment.
- **Up to date.** Every verb begins with `git fetch origin`. Main verbs require HEAD to equal `origin/main`;
  branch verbs require the branch to contain `origin/main`.
- **Clean tree.** Every verb refuses if `git status --porcelain` lists anything but the files the verb itself
  stages; refuses on a detached HEAD in the working copy it is run in (its own temporary worktrees are
  detached by design); refuses on `main` for branch verbs and off `main` for `merge` and the main verbs.
- **`--dry-run`** prints the entry it would sign and the effects it would perform, and does nothing; for `merge`
  and `push` it prints the preconditions it would evaluate and makes no worktree.
- **Refused in code, always:** `--admin`; `--force` or `+` refspecs; deleting any remote branch; creating a tag;
  rewriting any commit — a verb only appends commits, and a push that is not a fast-forward is a refusal, never
  a retry with force.
- **Main verbs** (`key`, `decision`, `amend`, `push`) run on `main` and end the same way: commit,
  `judge/selfcheck.py`, `git push origin main`, then `gh run watch` of the run the push started, printing its
  result. Any failure after a main verb's first effect — a failed self-check, a refused entry, an error of
  any kind — returns `main` to `origin/main` with `git reset --hard origin/main`, removes the files the verb
  placed, and prints the refusal; nothing was pushed. Where the effect precedes the entry (`push`: the
  fast-forward, then the entry), both commits go up in one push, so the remote never shows one without the
  other.
- **`merge`** runs on `main` but appends its entry to the proposal's branch, as SPEC §10.6 has it, and its
  effect is GitHub's merge, performed only after the judge has admitted the entry; it has no self-check and
  no undo, because nothing it does reaches `main` except through the judge.
- **Branch verbs** (`proposal`, `spec_conflict`) never touch `main` and run no self-check. If the push or the
  pull request fails after their commit, the verb prints the two commands that finish the act and undoes
  nothing; the commit is lawful as it stands.
- **The ledger.** Every act is an entry; every piece of evidence an entry relies on is referenced from it by
  hash (`push.digest`, `push.review`, `push.record`); files under `transcripts/` are evidence, never the record.
  A builder's objection is a `spec_conflict` entry, not a note.

## `jack key KEY_ID --principal P --powers a,b,c --pubkey FILE`

Entry: `key` with the declaration (SPEC §5). Refuses: a pubkey file that is not a two-field `ssh-ed25519` line;
a power outside the eight; a principal that is not `[a-z0-9_-]+` (it becomes the trailer's first field); a
re-declaration of the signer's own `key_id` without `key` (the kernel's guard would refuse it too; the verb
says so first). Effect: the main-verb ending. Keys per party: `builder-1`
{proposal, spec_conflict}, `reviewer-1` {proposal}, `counsel-1` {proposal}; the master key holds the rest.
Revocation is this verb with `--powers ""`.

## `jack proposal [--title T]`

On a branch other than `main`, with every change committed and the branch containing `origin/main`
(otherwise refused with the merge command to run: `git merge origin/main -m "Merge main into <branch>" -m
"Proposer: <party> <key_id>"`). Runs the check first — `python3 -m unittest discover -s tests -t .`,
`python3 pins/run.py`, `python3 tools/count_kernel.py` — and refuses on any failure. Entry: `proposal` with
`title` (default: the head commit's subject) and `commit` = the head's SHA (the work). Effect: commits
`log.jsonl` on top of the work, pushes the branch (`git push -u origin <branch>`), and opens the pull request
(`gh pr create --base main`) or, if one exists for the branch, does nothing more. A proposal re-made after
`main` moved (prefix broken) appends a new entry on top of a merge of `main`; the earlier one stands as history.

## `jack spec_conflict --section S --text T`

On a branch, with the branch preconditions of `proposal` and no check: a conflict is filed exactly when the
tests cannot be made to pass (A2 clause 9). Entry: `spec_conflict` {section, text}. Effect: commits
`log.jsonl`, pushes the branch, opens a pull request titled `spec_conflict: <section>` — or, if the branch
already has one, retitles it so — and prints "stopped: the specification cannot be implemented as written;
see PR #n". The builder stops here.

## `jack merge N`

On `main`, up to date. Preconditions, read with `gh pr view` and `gh pr checks`: PR N is open against `main`,
mergeable, its required checks green on its current head; its head commit is one commit past the `commit` of
a valid `proposal` entry in the PR's log, or — until the judge checks it — carries a filled `Proposer:`
trailer. Act: in a temporary worktree of the PR's head branch, entry `merge` {proposal: N, commit: the PR's
head SHA, checker: the trusted-base digest of `main`'s tree (`tools/digest.py`; SPEC §10.6 refuses any other)},
committed with message `merge: #N` and the trailer, pushed to the PR's branch as a fast-forward (a rejected
push means the proposal moved: refused, run again). Effect: `gh pr checks N --watch` until the judge and the
tests have admitted the head that carries the entry, then `gh pr merge N --merge`, which GitHub performs only
if they did; then `git pull --ff-only` on `main` and `gh run watch` of `main`'s run. The merge commit GitHub
makes is the effect of the entry that precedes it. When the clerk holds `merge`, this verb is unchanged.

## `jack push BRANCH --review FILE | --review none`

The only way a change to the trusted base reaches `main`, and the only verb that pushes to `main` anything
but an entry. On `main`, up to date; BRANCH is a local branch another party built, and the verb never commits
to it. Preconditions, each a refusal with its reason, evaluated on BRANCH's tree in a temporary worktree:
BRANCH contains `origin/main`; BRANCH's trusted-base digest differs from `main`'s (otherwise "nothing to
push: propose and merge"); every commit on BRANCH not on `main` carries a filled `Proposer:` trailer; the
check passes (as `proposal`); if `kernel/` or any kernel2 production source (`checker.go canonical.go
ed25519.go signature.go main.go`) differs from `main`'s, the run of record is made there by the verb itself —
never accepted from BRANCH, since the accused does not write its own test (CHARTER §1, F1): `kernel2/check`
built once first (so the twelve do not race the build), then `harness/diff.py --seeds A:B --b kernel2/check`
twelve ways into `transcripts/diff-100000-<T>-part00..11.json`, and every part must report `commit` equal to
BRANCH's head, `logs` equal to the length of its range, no disagreement and nothing uncompared, with the
twelve ranges contiguous from 0 to 100,000. `--review FILE` is copied to `transcripts/` and its SHA-256 is
the entry's `review`, an empty file included; `--review none` records 64 zeros and prints a warning that this
push was not read. Effect, in this order: `git merge --ff-only BRANCH` on `main` (never a
merge commit, never a rebase); the run's parts and the review placed under `transcripts/`; entry `push`
{digest: `tools/digest.py` of the tree now on `main`; review; record: the SHA-256 of the twelve parts' bytes
concatenated in name order, or 64 zeros when no run was required — an extra member until SPEC §5 names it};
committed with message `push: BRANCH`; the main-verb ending, whose self-check runs with the new trusted base
and the entry both in place and whose undo returns `main` to `origin/main`, BRANCH untouched. `--remove`
removes BRANCH's own worktree afterwards.

## `jack decision KIND SUBJECT`

On `main`. KIND is one of `veto promote budget grant transmute fix`; SUBJECT a non-empty string (for
`transmute`, the amendment id; for `grant`, the capability, such as a sealed judge image by digest; for
`promote`, the layer). Entry: `decision` {kind, subject}. Effect: the main-verb ending. The judge admits a
`decision` only from a key declared in genesis (SPEC §10.14).

## `jack amend ID FILE [--activate-at N]`

On `main`. Preconditions: a valid `decision` of kind `transmute` with subject ID is in the log (otherwise
refused: "transmute first"); FILE's first line is `## Amendment ID:`; ID is not already an amendment.
Effect before the entry: a blank line and FILE appended to `CHARTER.md`. Entry: `amend` {id, charter: the
SHA-256 of the new `CHARTER.md`, activate_at: N as given, the entry's seq + 1 when omitted}. Effect: commits `CHARTER.md`
and `log.jsonl`; the main-verb ending (judge items 2, 12, 13 on the way in).

**Order of an amendment (A2 clause 7, the research's protocol):** `jack decision transmute ID` → the pushes
that build the amendment's mechanisms, each by `jack push` → `jack amend ID FILE` last, so the charter never
says what the code does not enforce. A2 was recorded before its mechanisms and is the one exception.

**Text lands with its mechanism.** A change to `SPEC.md` that needs code is the first commit of the builder's
branch — counsel's patch, applied and read by Guy there, with counsel's trailer — and reaches `main` in the
same `jack push` as the code built to it. `main` never carries a text its judge and checkers do not
implement, and is never red by design. A change to `SPEC.md` that needs no code (wording, a recorded
decision) is pushed to `main` on its own, with its `push` entry.

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
Its tests stub `gh` and `ssh-keygen` with scripts on `PATH` that record their arguments, and every finding of
a cold read becomes a test there before its fix. If a verb cannot be written within the bound, `--dry-run` is
cut first, `gh run watch` second and `--remove` third (each printed as a command instead); the verbs and
their refusals are not.
