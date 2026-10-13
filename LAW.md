# LAW — CHARTER §§2–3 read against the code

Each sentence of the charter's maxims (§2) and secondary rules (§3) is followed
by the file and function that enforces it, or by the layer that will. "C1",
"C2", "C3" mark sentences the charter assigns to later layers; "judge" marks
enforcement outside the checker, in `judge/judge.py` and the workflow, which run
from trunk and never execute a proposal's code. Nothing here adds law: it maps.

## §2 Four maxims

### 1. No one judges their own cause

*The checker that decides an entry's validity is fixed before the entry exists
and cannot be changed by it.* — `judge/judge.py:judge` refuses any proposal
whose diff touches the trusted base (`kernel/`, `judge/`, `.github/workflows/`,
`SPEC.md`) or `CHARTER.md` with `trusted_path`, before anything else runs;
`judge/judge.py:run_kernel` extracts the kernel from the **trunk commit** into
a temporary directory and runs that, never a checkout; `judge/judge.py:digest`
is the trusted-base digest a `merge` must name (`judge_from_proposal`);
`.github/workflows/judge.yml` runs on `pull_request_target`, so the workflow
and the judge come from `main`. Inside the log, `kernel/check.py:check_entry`
judges entry *i* by `kernel/check.py:in_force` and the keys of the state built
from entries 0..*i*−1 only. Until C1's `merge.installs`, the trusted base
changes only by a commit Guy makes himself; the founding pull request is the
stated exception (REPORT.md).

*A resolution's proposer differs from its forecast's.* — C2 (forecasts).

*The last judge of value is the world, through a judge no party can edit.* —
C3 (assize's sealed judge).

### 2. The law looks forward and never commands the impossible

*An entry is judged by the law in force before it.* —
`kernel/check.py:check_entry`: rules come from `in_force(state)` and keys from
`state.keys` **before** the entry's own effects are applied (a `rule` at *i*
does not judge *i*; a `key` at *i* does not sign *i*); only `violation(i, _)`
counts (`hits`), so later law never reaches back; `kernel/check.py:check` folds
the prefix in order.

*Every rule is admitted with a witness that violates it and one that satisfies
it: the first proves the rule can fail, the second that compliance is possible.*
— `kernel/log.py:BODY` (the `rule` schema requires `witnesses.violating` and
`witnesses.satisfying`); `kernel/check.py:witness_list` and
`kernel/check.py:check_witness` (non-empty, well-formed);
`kernel/check.py:admit_rule` refuses `vacuous_rule` unless every violating
witness derives `violation(m, R)` for the rule's own id, and `impossible_rule`
if any satisfying witness is violated under the law with the new rule. By
Guy's decision (REPORT.md), the same function also keeps every older rule
compliable: `orphans_rule` unless each rule in force retains a passing
satisfying witness, with `replacements` joining older rules' witnesses.

### 3. Whatever is held must be produced

*Every obligation is derived from present state and the clock, carries a
deadline, and escalates when the deadline passes.* — C1 (the clerk and writs).
At C0 the one obligation the record computes is the lapse candidate:
`kernel/check.py:lapse_candidates` derives it from present state at every
change entry and reports it; notice, deadline and lapse itself wait for C1.

*No component waits for an event; each reconciles state.* — C1. (The judge is
event-triggered by a pull request; the charter assigns reconciliation to the
clerk.)

### 4. Decide by expected value; forbid only the irreversible

*Reversible acts are priced and scored, never blocked.* — C2 (scores).

*Hard gates stand only before effects that cannot be undone, where waiting has
positive option value.* — The record is append-only and an admitted entry
binds all later law, so admission is the irreversible effect C0 gates:
`kernel/check.py:check` refuses or admits; `judge/judge.py:judge` gates the
trusted base and the byte-prefix of the log (`prefix_broken`) and genesis by
proposal (`genesis_by_proposal`). Nothing else is blocked.

*Corollary: every source of influence is scored, because an unscored source has
unknown value; no party, the sovereign's delegates and counsel included, acts
except through entries that carry its identity.* — Identity:
`kernel/check.py:check_entry` refuses `no_proposer`; `kernel/check.py:signer`
derives the signing key from the signature itself (`kernel/sig.py:parse_sshsig`),
requires its principal to equal `proposer` (`proposer_mismatch`) and records
`signed_by(seq, key_id)` as a fact; `judge/judge.py:fingerprint` reports the
signers of a proposal's entries from the signature blobs, never from the
proposal's claims. Scoring: C2. (The `Proposer:` git trailer on commits is a
convention, not enforced.)

## §3 The minimal law: three secondary rules

### Recognition

*An entry is valid iff (a) its parent is the head of the log* —
`kernel/check.py:check_entry` (`bad_seq`, `parent_mismatch`) against
`kernel/log.py:line_hash` of the previous line; genesis's parent is
`kernel/log.py:GENESIS_PARENT`.

*(b) it is signed by a key that the law in force grants for its type* —
`kernel/check.py:signer`: the embedded key must be declared
(`kernel/check.py:declare`; `unknown_key`), hold the entry's type among its
powers (`no_power`), and the signature must verify: `kernel/sig.py:parse_sshsig`,
`kernel/sig.py:signed_data`, `kernel/sig.py:verify`,
`kernel/sig.py:ed25519_verify` (`bad_signature`). Genesis certifies itself
with the keys its own body declares.

*(c) every rule in force at its parent accepts it.* —
`kernel/check.py:check_entry` evaluates `kernel/check.py:violations` over
`kernel/check.py:in_force` with `kernel/check.py:law_facts` via
`kernel/datalog.py:evaluate`; any `violation(i, r)` refuses with `violation`
and the earliest-admitted `r`.

### Change

*A rule enters or leaves only by a change entry signed by a key holding the
change power (at genesis, Guy's alone).* — `kernel/check.py:signer` (`no_power`
for `rule`/`repeal` without the power); `genesis.template.json` grants the
powers to Guy's master key alone; `kernel/check.py:check_entry` admits a rule
only through a `rule` entry and removes it only through a `repeal`
(`unknown_rule` otherwise).

*It binds from the next entry.* — `kernel/check.py:check_entry`: recognition
(c) uses the pre-admission state; the new rule enters `state.rules` afterwards.

*It carries its two witnesses.* — `kernel/log.py:BODY`,
`kernel/check.py:witness_list`.

*Rules are data in a decidable language (proposed: stratified Datalog), so the
law can grow while the trusted interpreter stays fixed.* —
`kernel/datalog.py:compile_rule` (JSON clauses, range restriction, arities),
`kernel/datalog.py:stratify` (`unstratifiable`), `kernel/datalog.py:evaluate`
(least model, stratum by stratum; no function symbols or arithmetic, so the
model is finite and evaluation terminates).

*Lapse: a rule all of whose violating witnesses the rest of the law already
rejects is a lapse candidate (tested oldest first, one at a time, so two rules
never lapse on each other's account).* — `kernel/check.py:lapse_candidates`,
reported in the verdict's `lapse` at every `rule` and `repeal` entry.

*It lapses at the end of a notice period unless some proposer enters a
counter-witness that it alone rejects, which then joins its witnesses.* — C1
(notice, lapse, counter-witness entries).

*Witness-redundancy is not subsumption, which is undecidable for recursive
Datalog; the notice is how a rule that still guards something unwritten is
defended.* — Explanatory; no code. *Law should not outlive its necessity, and
since the test and the defence are both entries, lapse costs Guy nothing.* — C1.

### Adjudication

*The checker is the only adjudicator of validity.* — `kernel/check.py:check` is
the verdict; `judge/judge.py:judge` adds only facts the log cannot carry (paths
touched, byte prefix, trunk's digest) and otherwise reports the kernel's verdict.

*Its digest is in the log; it runs from trunk, never from the proposal;* —
`genesis.template.json` records `body.checker`, required by `kernel/log.py:BODY`
and computed by `tools/digest.py` and `judge/judge.py:digest`;
`judge/judge.py:run_kernel` and `.github/workflows/judge.yml` run trunk's
kernel; `judge/judge.py:judge` refuses `trusted_path`.

*a second implementation by a different author replays every entry, and any
disagreement halts the clerk and raises a writ to Guy.* — `kernel2/README.md`
(pending: not written here, by design); `harness/diff.py:compare`;
`judge/judge.py:judge` refuses `checker_drift` on disagreement; the writ is C1.

*Questions of merit (is this work good?) are not questions of validity: they
are forecasts, scored when the world resolves them.* — C2.

*Statutes are confined to decidable properties, because non-trivial semantic
properties of programs are undecidable (Rice 1953).* —
`kernel/datalog.py:compile_rule` admits only stratified Datalog over the fixed
fact schema (`kernel/datalog.py:BASE`), a decidable language; rules are never code.
