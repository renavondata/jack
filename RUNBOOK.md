# Runbook — the verbs of jack

An act on the record is a verb of `tools/jack`, one verb per entry type, seven in all. Each verb validates its
arguments, prepares the entry on the head of `log.jsonl`, signs it with the caller's key, appends it only if the
kernel admits it, and then performs the git and GitHub effects the entry authorises — and nothing else. What is
not a verb is not done; a new verb needs a new entry type, which needs SPEC text and an `amend`. The vocabulary
is the same for every party, cut down by the powers its key holds: the kernel refuses an entry the key may not
sign (`no_power`), so the CLI decides nothing. `tools/jack` is outside the trusted base: an entry written by
hand gets the same verdict. (Authority: CHARTER §5, §7; A2 clauses 6 and 10; the research of 18 October, (d).)

## Common to every verb

- **Root and log.** The repository root is the directory above `tools/`; the log is `log.jsonl` there. Verbs
  run inside the working copy they act on (a branch's worktree for branch verbs, the `main` checkout for main
  verbs).
- **Key and party.** `--key PATH` names the private key; default `$JACK_KEY`, else `~/.ssh/id_ed25519`. The
  party is never an argument: the verb reads the matching `pubkey` from the keys declared in the log and takes
  its `principal` as the entry's `proposer` and as the `Proposer:` trailer's party. A key the log does not
  declare is refused before signing.
- **Time.** `ts` is the clock, UTC, `YYYY-MM-DDTHH:MM:SSZ`. The verb reads the clock; the kernel never does.
- **Signing.** `ssh-keygen -Y sign -f KEY -n core-entry` over the canonical message (SPEC §6); the master key
  prompts for its passphrase, party keys do not. Assembly is `tools/entry.py`'s: the line is appended only if
  `kernel.check` admits the log with it.
- **Commits.** A verb's commit message is `<type>: <summary>`, an optional body, and as its **last paragraph**
  `Proposer: <party> <key_id>`. A trailer containing `<` is refused.
- **Clean tree.** Every verb refuses if `git status --porcelain` lists anything but the files the verb itself
  stages; refuses on a detached HEAD; refuses on `main` for branch verbs and off `main` for main verbs.
- **`--dry-run`** prints the entry it would sign and the effects it would perform, and does nothing.
- **Refused in code, always:** `--admin`; `--force` or `+` refspecs; deleting any remote branch; creating a tag;
  rewriting any commit; editing a branch the caller's key did not propose; running on a tree whose
  `judge/selfcheck.py` fails after the commit (the commit is undone with `git reset --soft HEAD~1` and the
  refusal printed).
- **Main verbs** (`key`, `push`, `decision`, `amend`, `merge`) end the same way: commit, `judge/selfcheck.py`,
  `git push origin main`, then `gh run watch` of the run the push started, printing its result. A refused
  self-check means nothing was pushed.
- **Branch verbs** (`proposal`, `spec_conflict`) never touch `main`.

## `jack key KEY_ID --principal P --powers a,b,c --pubkey FILE`

Entry: `key` with the declaration (SPEC §5). Refuses: a pubkey file that is not a two-field `ssh-ed25519` line;
a power outside the eight; a re-declaration of the signer's own `key_id` without `key` (the kernel's guard
would refuse it too; the verb says so first). Effect: the main-verb ending. Keys per party: `builder-1`
{proposal, spec_conflict}, `reviewer-1` {proposal}, `counsel-1` {proposal}; the master key holds the rest.
Revocation is this verb with `--powers ""`.

## `jack proposal [--title T]`

On a branch other than `main`, with every change committed and the branch containing `origin/main`
(otherwise refused with the merge command to run: `git merge origin/main -m "Merge main into <branch>" -m
"Proposer: <party> <key_id>"`). Runs the check first — `python3 -m unittest discover -s tests -t .`,
`python3 pins/run.py`, `python3 tools/count_kernel.py` — and refuses on any failure. Entry: `proposal` with
`title` (default: the head commit's subject) and `commit` = the head's SHA (the work). Effect: commits
`log.jsonl` on top of the work with message `proposal: <title>` and the trailer, pushes the branch
(`git push -u origin <branch>`, never forced), and opens the pull request (`gh pr create --base main`) or,
if one exists for the branch, does nothing more. A proposal re-made after `main` moved (prefix broken)
appends a new entry; the earlier one stands as history.

## `jack spec_conflict --section S --text T`

On a branch, as `proposal`. Entry: `spec_conflict` {section, text}. Effect: commits `log.jsonl` with message
`spec_conflict: <section>`, pushes the branch, opens a pull request titled `spec_conflict: <section>`, and
prints "stopped: the specification cannot be implemented as written; see PR #n". The builder stops here; it
does not make the tests pass (A2 clause 9).

## `jack merge N`

On `main`, up to date with `origin/main`. Preconditions: PR N is open against `main`, its required checks
are green and it is mergeable (`gh pr view`, `gh pr checks`); the PR's head commit is the `commit` of a valid
`proposal` entry in the PR's log plus one commit (the entry's own), or — until the judge checks it — carries a
`Proposer:` trailer. Effect, in this order: `gh pr merge N --merge`; `git pull --ff-only`; entry `merge`
{proposal: N, commit: the new head's SHA, checker: the trusted-base digest of the tree (`tools/digest.py`)};
the main-verb ending. The merge precedes its entry by one commit because a `merge` entry on `main` would
break the prefix of every open proposal; the entry is the record of the act, appended at once.

## `jack push BRANCH --review FILE | --review none`

The only way a change to the trusted base reaches `main`. Runs inside BRANCH's worktree, with `main`
checked out in the repository's main working copy (`git worktree list`). Preconditions, each a refusal with
its reason: clean tree; BRANCH contains `origin/main`; BRANCH's trusted-base digest differs from `main`'s
(otherwise "nothing to push: propose and merge"); every commit on BRANCH not on `main` carries a filled
`Proposer:` trailer; the check passes (as `proposal`); if `kernel/` or any kernel2 production source
(`checker.go canonical.go ed25519.go signature.go main.go`) differs from `main`'s, the run of record exists
or is made: `kernel2/check` built once first (so the twelve do not race the build), then `harness/diff.py
--seeds A:B --b kernel2/check` twelve ways into `transcripts/diff-100000-<T>-part00..11.json`, and the sum
must be 100,000 logs, 0 disagreements, 0 uncompared, ranges without a gap; a complete run already in
`transcripts/` counts if the checker sources at its commit equal BRANCH's. `--review FILE` copies FILE to
`transcripts/` and its SHA-256 is the entry's `review`; `--review none` records 64 zeros and prints a
warning that this push was not read. Entry: `push` {digest: `tools/digest.py` of BRANCH's tree, review}.
Effect: commits `log.jsonl` and `transcripts/` on BRANCH with message `push: <summary>` and the trailer;
`judge/selfcheck.py` on BRANCH; in the main working copy `git switch main && git pull --ff-only && git merge
--ff-only BRANCH && git push origin main`; `gh run watch`; then `git worktree remove` of BRANCH's worktree if
`--remove`. Never a merge commit, never a rebase.

## `jack decision KIND SUBJECT`

On `main`. KIND is one of `veto promote budget grant transmute fix`; SUBJECT a non-empty string (for
`transmute`, the amendment id; for `grant`, the capability, such as a sealed judge image by digest; for
`promote`, the layer). Entry: `decision` {kind, subject}. Effect: the main-verb ending. The judge admits a
`decision` only from a key declared in genesis (SPEC §10.14).

## `jack amend ID FILE [--activate-at N]`

On `main`. Preconditions: a valid `decision` of kind `transmute` with subject ID is in the log (otherwise
refused: "transmute first"); FILE's first line is `## Amendment ID:`; ID is not already an amendment.
Effect before the entry: a blank line and FILE appended to `CHARTER.md`. Entry: `amend` {id, charter: the
SHA-256 of the new `CHARTER.md`, activate_at: N, default the entry's seq + 1}. Effect: commits `CHARTER.md`
and `log.jsonl` with message `amend: ID`; the main-verb ending (judge items 2, 12, 13 on the way in).

**Order of an amendment (A2 clause 7, the research's protocol):** `jack decision transmute ID` → the pushes
that build the amendment's mechanisms, each by `jack push` → `jack amend ID FILE` last, so the charter never
says what the code does not enforce. A2 was recorded before its mechanisms and is the one exception.

## Working copies (no verbs; nothing here touches the record)

- A builder works in a worktree cut from a pulled `main`: `git worktree add ~/git/jack-build-<name> -b <branch>
  main`, with `JACK_KEY=~/.ssh/jack-builder` in its environment. It reads the text it builds to, touches only
  the paths that text names, and ends with `jack proposal` or `jack spec_conflict`.
- A reviewer reads cold in a copy with no history: `git archive <ref> | tar -x -C <room>`, `git diff
  <merge-base> <ref> > <room>/DIFF.patch`, `git init` there. Its findings are pins, proposed under
  `~/.ssh/jack-reviewer` with `jack proposal`; a round that adds no pin ends the review (A2 clause 9).
- The kernel2 author works in a room holding only `SPEC.md`, `spec/`, `tests/vectors/` and `kernel2/`, reads
  nothing else, and leaves `QUESTIONS.md` saying `none`; its work enters by `jack push`.

## Bound and custody

`tools/jack` is one Python file within 250 lines as `tools/count_kernel.py` counts, standard library plus
`tools/entry.py`, `kernel` and `judge` imports; it is untrusted, enters by pull request, and is read cold.
Its tests stub `gh` and `ssh-keygen` with scripts on `PATH` that record their arguments. If a verb cannot be
written within the bound, `--dry-run` is cut first and `gh run watch` second (printed as a command instead);
the verbs are not.
