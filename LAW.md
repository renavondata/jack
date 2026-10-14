# LAW — CHARTER §§2–3 read against the code

Each sentence of the charter's maxims (§2) and secondary rules (§3) is followed
by the file and function that enforces it, or by the layer that will. "C1",
"C2", "C3" mark sentences the charter assigns to later layers; "judge" marks
enforcement outside the checker, in `judge/judge.py` and the workflow, which run
from trunk and never execute a proposal's code. C0 is the record only (Guy's
decision on counsel's review, 14 October 2026): sentences about rules,
witnesses and lapse are C1's, and the record is built so that they can arrive
without touching what is enforced here. Nothing here adds law: it maps.

## §2 Four maxims

### 1. No one judges their own cause

*The checker that decides an entry's validity is fixed before the entry exists
and cannot be changed by it.* — `judge/judge.py:judge` refuses any proposal
whose trusted-base digest (`judge/judge.py:digest` over `kernel/`, `kernel2/`,
`judge/`, `.github/workflows/`, `SPEC.md`) differs from trunk's, or whose
`CHARTER.md` differs byte for byte, with `trusted_path`, before anything else
runs; `judge/judge.py:differing` names the files, by content, so a rename or a
deletion is caught like an edit. `judge/judge.py:run_kernel` extracts the kernel
from the **trunk commit** into a temporary directory and runs that, never a
checkout; `.github/workflows/judge.yml` runs on `pull_request_target`, so the
workflow and the judge come from `main`. Inside the log,
`kernel/check.py:check_entry` judges entry *i* by the keys of the state built
from entries 0..*i*−1 only. Until C1 brings a lawful change path, the trusted
base changes only by a commit Guy makes himself; the founding pull request is
the stated exception (REPORT.md).

*A resolution's proposer differs from its forecast's.* — C2 (forecasts).

*The last judge of value is the world, through a judge no party can edit.* —
C3 (assize's sealed judge).

### 2. The law looks forward and never commands the impossible

*An entry is judged by the law in force before it.* —
`kernel/check.py:check_entry`: `kernel/check.py:signer` reads `state.keys`
**before** the entry's own effect is applied (a `key` at *i* does not sign *i*,
and a revocation at *j* never reaches an entry before *j*);
`kernel/check.py:check` folds the prefix in order, so later law cannot reach back.

*Every rule is admitted with a witness that violates it and one that satisfies
it: the first proves the rule can fail, the second that compliance is possible.*
— C1. No rule can be admitted at C0 (`kernel/log.py:TYPES` has no `rule`); the
first rule arrives with its two witnesses in C1 (BRIEF-C1.md). The impossible
is refused in one place already: `kernel/check.py:declare` refuses a public key
that no one could be the sole holder of (`kernel/sig.py:weak_key`; `bad_key`).

### 3. Whatever is held must be produced

*Every obligation is derived from present state and the clock, carries a
deadline, and escalates when the deadline passes.* — C1 (the clerk and writs).
At C0 the record holds no obligation: it computes none.

*No component waits for an event; each reconciles state.* — C1. (The judge is
event-triggered by a pull request; the charter assigns reconciliation to the
clerk.)

### 4. Decide by expected value; forbid only the irreversible

*Reversible acts are priced and scored, never blocked.* — C2 (scores).

*Hard gates stand only before effects that cannot be undone, where waiting has
positive option value.* — The record is append-only and an admitted entry binds
all later law, so admission is the irreversible effect C0 gates:
`kernel/check.py:check` refuses or admits; `judge/judge.py:judge` gates the
trusted base (`trusted_path`), the binding of genesis to the charter text
(`charter_mismatch`, via `judge/judge.py:genesis_charter`), the byte-prefix of
the log (`prefix_broken`) and genesis by proposal (`genesis_by_proposal`).
Nothing else is blocked.

*Corollary: every source of influence is scored, because an unscored source has
unknown value; no party, the sovereign's delegates and counsel included, acts
except through entries that carry its identity.* — Identity:
`kernel/check.py:check_entry` refuses `no_proposer`; `kernel/check.py:signer`
derives the signing key from the signature itself (`kernel/sig.py:parse_sshsig`),
requires it to be declared (`unknown_key`) and its principal to equal `proposer`
(`proposer_mismatch`); `kernel/check.py:declare` keeps one key to one identity
(`bad_key` for a pubkey already declared under another key_id);
`judge/judge.py:fingerprint` reports the signers of a proposal's entries from
the signature blobs, never from the proposal's claims. Scoring: C2. (The
`Proposer:` git trailer on commits is a convention, not enforced.)

## §3 The minimal law: three secondary rules

### Recognition

*An entry is valid iff (a) its parent is the head of the log* —
`kernel/check.py:check_entry` (`bad_seq`, `parent_mismatch`) against
`kernel/log.py:line_hash` of the previous line; genesis's parent is
`kernel/log.py:GENESIS_PARENT`.

*(b) it is signed by a key that the law in force grants for its type* —
`kernel/check.py:signer`: the embedded key must be declared
(`kernel/check.py:declare`; `unknown_key`), hold the entry's type among its
powers (`no_power`), and the signature must verify: `kernel/sig.py:parse_sshsig`
(exact container, empty reserved field), `kernel/sig.py:signed_data`,
`kernel/sig.py:verify`, `kernel/sig.py:ed25519_verify` (`bad_signature`).
Genesis certifies itself with the keys its own body declares.

*(c) every rule in force at its parent accepts it.* — Vacuous at C0: no rule
is in force and none can enter (`kernel/log.py:TYPES`). C1 adds the rules and
the engine that evaluates them; recognition (a) and (b) do not change.

### Change

*A rule enters or leaves only by a change entry signed by a key holding the
change power (at genesis, Guy's alone).* — At C0 what enters or leaves the law
is a key declaration, by a `key` entry: `kernel/check.py:signer` refuses a `key`
entry whose signing key lacks the `key` power (`no_power`);
`kernel/check.py:declare` applies it (grant, re-declaration, revocation by empty
powers); `genesis.template.json` grants the `key` power to Guy's master key
alone. Rules themselves: C1.

*It binds from the next entry.* — `kernel/check.py:check_entry`: recognition
(b) uses the pre-entry keys; the declaration enters the state afterwards.

*It carries its two witnesses.* — C1.

*Rules are data in a decidable language (proposed: stratified Datalog), so the
law can grow while the trusted interpreter stays fixed.* — C1. BRIEF-C1.md
starts from the smallest language that expresses the first real case; the
stratified-Datalog draft is preserved on branch `c1-law-draft` as design input.

*Lapse: a rule all of whose violating witnesses the rest of the law already
rejects is a lapse candidate (tested oldest first, one at a time, so two rules
never lapse on each other's account). It lapses at the end of a notice period
unless some proposer enters a counter-witness that it alone rejects, which then
joins its witnesses. Witness-redundancy is not subsumption, which is
undecidable for recursive Datalog; the notice is how a rule that still guards
something unwritten is defended. Law should not outlive its necessity, and
since the test and the defence are both entries, lapse costs Guy nothing.* — C1.

### Adjudication

*The checker is the only adjudicator of validity.* — `kernel/check.py:check` is
the verdict; `judge/judge.py:judge` adds only facts the log cannot carry (the
trusted base, the charter text, the byte prefix, trunk's digest) and otherwise
reports the kernel's verdict.

*Its digest is in the log; it runs from trunk, never from the proposal;* —
`genesis.template.json` records `body.checker`, required by `kernel/log.py:BODY`
and computed by `tools/digest.py:digest` and `judge/judge.py:digest`;
`judge/judge.py:run_kernel` and `.github/workflows/judge.yml` run trunk's
kernel; `judge/judge.py:judge` refuses `trusted_path` and, for an appended
`merge` naming another checker, `judge_from_proposal`.

*a second implementation by a different author replays every entry, and any
disagreement halts the clerk and raises a writ to Guy.* — `kernel2/README.md`
(pending: not written here, by design); `harness/diff.py:compare`;
`judge/judge.py:judge` refuses `checker_drift` on disagreement; the writ is C1.

*Questions of merit (is this work good?) are not questions of validity: they
are forecasts, scored when the world resolves them.* — C2.

*Statutes are confined to decidable properties, because non-trivial semantic
properties of programs are undecidable (Rice 1953).* — At C0 the only statute
is this text, bound to the record by its hash: `genesis.template.json` records
`body.charter`, and `judge/judge.py:judge` refuses every proposal while trunk's
`CHARTER.md` does not hash to it (`charter_mismatch`). The decidable language
for primary rules is C1's.
