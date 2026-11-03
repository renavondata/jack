# LAW — CHARTER §§2–3 read against the code

Each sentence of the charter's maxims (§2) and secondary rules (§3) is followed
by the file and function that enforces it, or by the layer that will. "C1",
"C2", "C3" mark sentences the charter assigns to later layers; "judge" marks
enforcement outside the checker, in `judge/judge.py` and the workflow, which run
from trunk and never execute a proposal's code. C0 was the record only (Guy's
decision on counsel's review, 14 October 2026); this text is kept at the current
layer — C2a, after C1a (the `forecast` and `resolution` types, seq 29), C1b (the
clerk, the writs, the liveness statistic) and C2a (the value statistic, the
streams) — and each sentence names what enforces it now or the layer that will.
Where a layer's brief promised a thing that has not arrived, the sentence says
so rather than naming the brief. Nothing here adds law: it maps. Brought from
C0 to C2a by counsel on 3 November 2026 (the author's F1).

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

*A resolution's proposer differs from its forecast's.* — `kernel/check.py:check_entry`
refuses `self_judged` when the resolution's signing key has the same principal
as the forecast's (by principal, not by key id), since C1a's installing push
(seq 29); `tools/jack resolve` refuses before signing with the kernel's reason.

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
— Not yet law in the kernel: `kernel/log.py:TYPES` still has no `rule` at C2a
(the type is deferred; COUNSEL-DUE `c2b-report`). The maxim is kept at the layer
of tools instead: every change to `tools/`, `harness/`, `sim/` or `pins/` carries
a pin in `pins/pins.py` whose named mutant it kills and whose passing twin it
admits, run by `.github/workflows/tests.yml` on every proposal and read by
`tools/status.py` as criteria 1–2 of each window. The impossible
is refused in one place already: `kernel/check.py:declare` refuses a public key
that no one could be the sole holder of (`kernel/sig.py:weak_key`; `bad_key`).

### 3. Whatever is held must be produced

*Every obligation is derived from present state and the clock, carries a
deadline, and escalates when the deadline passes.* — `tools/clerk.py`:
`forecast_writs` (W1, a writ per unresolved forecast with its `resolves_by`),
`merge_writs` (W3, a writ per unwitnessed merge) and `window_writs` (W4, the
window's criteria with its end) are computed from the log, the saved runs and
the clock; past the deadline the line reads ESCALATED. The escalation was a
printed word until 3 November 2026 (four writs expired while it printed); from
then the diary of `renavondata/opencode-runner` computes the due list at every
tick and files a resolver session (`transcripts/sessions/due-resolve.md`) — an
act off the log, which C2c's `UNATTENDED` line is to bring onto it.

*No component waits for an event; each reconciles state.* — The herald
(`herald.yml` in `renavondata/opencode-runner`, every two minutes) reconciles every open proposal from the bytes
of `main` and the branch: merge, re-propose as stale, or re-run a failed first
attempt; the diary (hourly) reconciles the writs against the clock. The judge
alone is event-triggered, by the pull request, and decides nothing but validity.

### 4. Decide by expected value; forbid only the irreversible

*Reversible acts are priced and scored, never blocked.* — Every forecast is
scored by `tools/jack score` (`tools/entry.py:score`, log-loss against the
per-type base rate); C1b's liveness is A4.3's bet in `tools/status.py:score_items`
and `item_process`; C2a's value is A4.4's bounded-difference bet against the
base rate in `tools/value.py:value`.

**Where practice departs from the sentence** (the author's F6, jack #244).
The gate is drawn by path and verb, not act by act. Anything under the trusted base
(`judge/`, `kernel/`, `kernel2/`, `.github/workflows/`, `SPEC.md`) changes only by a
sovereign `push`, so reversible content there is blocked as well: the counted-line cap in
`judge/scope.json` (raised by seqs 197 and 367), which BRIEF-C2a says "enters no score". So
is the weekly budget, a sovereign `decision` (seq 50). The reason is the one maxim 2's
sentence on adjudication gives: deciding reversibility edit by edit means judging the
content of the change, a semantic property no decidable check can be trusted with (Rice
1953). The cost is priced and recorded rather than removed: one sovereign act per cap
change: two so far (seqs 197 and 367), and a third at C2b's opening. A cap set by a non-sovereign key within a
bound the sovereign fixes is a C2c candidate. It is not law, and the charter's sentence
stands as the intent the practice approximates.

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
alone. Rules themselves: deferred (no `rule` type at C2a; see maxim 2).

*It binds from the next entry.* — `kernel/check.py:check_entry`: recognition
(b) uses the pre-entry keys; the declaration enters the state afterwards.

*It carries its two witnesses.* — For tools, the pin and its twin (maxim 2); for
rules in the kernel, deferred with the type.

*Rules are data in a decidable language (proposed: stratified Datalog), so the
law can grow while the trusted interpreter stays fixed.* — Not built. C1 did
not admit a rule language: the first real cases were brief rules enforced by
tools (`tools/status.py`'s criteria, `tools/jack`'s refusals) under a fixed
kernel; the stratified-Datalog draft remains on branch `c1-law-draft` as design
input, and whether a rule language is needed at all is a C2c question.

*Lapse: a rule all of whose violating witnesses the rest of the law already
rejects is a lapse candidate (tested oldest first, one at a time, so two rules
never lapse on each other's account). It lapses at the end of a notice period
unless some proposer enters a counter-witness that it alone rejects, which then
joins its witnesses. Witness-redundancy is not subsumption, which is
undecidable for recursive Datalog; the notice is how a rule that still guards
something unwritten is defended. Law should not outlive its necessity, and
since the test and the defence are both entries, lapse costs Guy nothing.* —
Not built (it presupposes the rule type).

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
`judge/judge.py:judge` refuses `checker_drift` on disagreement — the halt is
mechanical (no proposal merges), the writ to Guy is still a sentence (C2c).

*Questions of merit (is this work good?) are not questions of validity: they
are forecasts, scored when the world resolves them.* — The `forecast` and
`resolution` types (C1a, seq 29); `tools/jack score`; the two streams of C2a
(`world.renavon`, `world.hkjc`) resolved from hashed pages under
`transcripts/evidence/`; the election of C2b is to make the choice of proposer
itself such a forecast.

*Statutes are confined to decidable properties, because non-trivial semantic
properties of programs are undecidable (Rice 1953).* — At C0 the only statute
is this text, bound to the record by its hash: `genesis.template.json` records
`body.charter`, and `judge/judge.py:judge` refuses every proposal while trunk's
`CHARTER.md` does not hash to it (`charter_mismatch`). The decidable language
for primary rules has not arrived (maxim 2); the statutes in force are the
charter, SPEC, and the briefs' pre-stated criteria as `tools/status.py` reads them.

## Readings of the charter's citations

These are errata in the charter's reading of its sources, not amendments. They change no
mechanism, and the charter's text stays as the genesis hash binds it. A session reading the
charter as law reads these with it. They join the charter's text at the next amendment that
a witnessed brief rule calls for, and never by an amendment of their own (COUNSEL-OPEN
row 28). Checked against the texts by the author on 3 November 2026 (jack #244, #245).

- **§2.4, "forbid only the irreversible (Arrow & Fisher 1974)".** Arrow and Fisher price
  irreversibility; they do not forbid it ("Just because an action is irreversible does not
  mean that it should not be undertaken", p. 319). That a reversible act has no option value
  follows from their model only when reversal costs nothing, and they do not state it. Read
  the maxim as the court's policy, *after* Arrow and Fisher, not as their theorem.
- **§3, "fold(law, log) is the model every good regulator must contain (Conant & Ashby
  1970)".** The theorem concerns the *simplest* optimal regulator, which is a mapping of the
  reguland's events, with the distribution over them fixed. Optimal regulators that are not
  models exist; Conant and Ashby call them "unnecessarily complex". Read "…the model the
  simplest optimal regulator must contain".
- **§3, "the pool of proposers must carry at least the variety of the disturbances it
  absorbs (Ashby 1956)".** S.11/7 bounds the variety of outcomes below by V_D − V_R; it does
  not require the regulator's variety to equal the disturbances'. Read "…enough variety that
  the outcomes it lets through fit the acceptable set (Ashby 1956, S.11/7)". The case for
  several model families stands on that reading.
