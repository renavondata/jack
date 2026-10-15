# Brief C1 — the clerk, writs, and the first law (draft, for Guy to amend or discard)

CHARTER §8: *C1: clerk and writs; Guy's acts as typed entries. Exit: clean
simulator run, then E_t ≥ 20 against p₀ within 14 days live.* This draft is
counsel's proposal of scope; it binds nothing. On Guy's decision of 14 October
2026, on counsel's review, **the law language is C1's**: C0 is the record only.

## Precondition

C0 promoted: genesis signed, both checkers agreeing on the real log and 10^5
seeded logs, every pin KILLED, kernel within 1,000 lines. If kernel2 is still
absent, C1 cannot open (§6 safety needs independent replay).

## The law language: start from the first precedent

CHARTER §3 says primary rules accrete as precedent, each from a witnessed case.
C1 therefore does **not** begin by choosing a rule language. It begins when
the first real case arrives: the first entry Guy wants refused that recognition
(a)(b) does not refuse. The language is then the **smallest** that expresses
that one rule with its two witnesses, admitted by a change entry; it grows only
when a later case cannot be written in it. Each growth is itself a change entry
to the trusted base (`merge.installs`, below), read by Guy.

The candidates, in increasing size:

1. **A fixed menu of rule schemas**, each a few lines of checker code
   parametrised by data: `forbid(type, field, value)`, `require(type, field)`,
   `monotone(field)`, `at_most(type, n, per)`. Decidable by construction; a
   schema is admitted once, by Guy, and instantiated by `rule` entries. Smallest
   interpreter; the law can grow only along the menu.
2. **Conjunctive queries** over the facts of the prefix and the candidate
   entry (no recursion, no negation), plus a short list of built-in comparisons
   (`=`, `≠`, `<` on integers and on fixed-width timestamps). Still decidable
   and fast; expresses uniqueness ("one merge per proposal") and ordering.
3. **Stratified Datalog with witnesses, replacements, orphan check and lapse**
   — the C0 draft, preserved whole on branch `c1-law-draft` (fe5c2f2) with its
   tests, pins, simulator kinds and SPEC sections. The largest candidate (about
   280 kernel lines) and, without comparison built-ins, unable to express the
   first candidate rule below. Design input, not a starting point.

### The first candidate rule: non-decreasing timestamps

`ts` is a fixed-width UTC string (`YYYY-MM-DDTHH:MM:SSZ`), so lexicographic
order is chronological order. The rule: entry *i*'s `ts` is not earlier than
entry *i*−1's. Its violating witness is an entry whose `ts` precedes its
parent's; its satisfying witness an entry whose `ts` equals or follows it.
C0 records `ts` and never orders it (SPEC.md §12.4); C1 admits this rule first,
in whichever language is chosen, and it decides which: candidate 1 needs a
`monotone(ts)` schema, candidate 2 a `<` on strings, candidate 3 cannot say it.

## Scope

1. **Clerk (§5).** Level-triggered, on a timer (GitHub Actions `schedule` and
   `workflow_dispatch`, from trunk, read-only token plus the herald key's
   capability). Reads state = fold(law, log) and the clock, computes
   obligations, issues writs and invitations, escalates along the pre-stated
   ladder: re-invite; re-invite on another runner or model; writ to Guy. Holds
   no change power; decides nothing about validity.
2. **Writs as entries.** New types, admitted at C1's genesis-of-layer by change
   entry: `writ` (obligation, deadline, escalation level), `discharge`,
   `invite`, `accept`, `wish`, and Guy's acts typed by entry and key (§7) so
   decisions and repairs split mechanically.
3. **Rules, witnesses and lapse** in the language chosen above: `rule` and
   `repeal` entries signed by a key with the change power; each rule with a
   violating and a satisfying witness; the pins C0 set aside return
   (`final_law_for_all`, `vacuous_rule_admitted`, `impossible_rule_admitted`,
   `redundancy_unreported`); the notice period as a writ; a `counter_witness`
   entry type whose witness joins a rule's violating witnesses; the lapse
   itself as a change entry the clerk prepares and the change key signs.
4. **Lawful changes to the trusted base.** `merge.installs`: a merge entry
   signed by the change key names the trusted-base digest that is in force
   from the next entry; the judge then accepts proposals touching trusted paths
   only when a matching `installs` follows, and checks trunk's actual digest
   against the digest in force. Until then the trusted base changes only by
   Guy's own commits (C0 rule), including `kernel2/`.
5. **Merge authorship.** The judge holds no secret, so C0 cannot sign `merge`
   entries; the clerk's herald key (`accept`, `wish`, and `merge`?) is Guy's
   decision. The herald key must not hold `key`, nor the change power.
6. **Second checker in CI.** Done in C0: `tests` runs the first 2,000
   committed seeds through both checkers on every push (`--second`,
   `--complete`); the judge already refuses `checker_drift`. C1 adds the rule
   attacks to the simulator and keeps the sample green.

## Questions C0 raised for C1 (see REPORT.md)

- `pull_request` runs the proposal's own tests and pins (F1). Make the
  `push: main` run the one that counts, or drop the PR run to a report?
- A `key` entry that leaves no key with `key` power locks the log. Refuse it in
  the kernel, or leave it to Guy?
- Hardware keys (`sk-ssh-ed25519@openssh.com`) sign a different message; add
  the format by change entry if Guy's master key needs it.
- If C1 flattens bodies into facts, decide whether keys containing `.` are
  escaped or refused from C1's genesis-of-layer; C0 allows them.
- A proposal must rebase whenever trunk's trusted base moves; with
  `merge.installs` the judge could instead compare against the digest in force.

## Pre-stated exit

Clean simulator run (attack list extended with the rule attacks — vacuous,
impossible — and with stalling and flooding as liveness attacks the clerk must
answer); then E_t ≥ 20 against p₀ (assize's weekly `guy_acts.py` series)
within 14 days live; windows, α = 0.05, p₀ and the attack list committed
before the window opens; zero checker disagreements throughout; Guy has not
vetoed.

## Lessons from C0 for this brief (counsel, 15 October 2026)

Each is a pre-stated criterion or a scope item for C1 unless Guy strikes it.

1. **A byte-level simulator kind.** Every checker disagreement in C0 came from reviews and byte probes,
   none from the simulator (REPORT.md §8.3.3). Add a kind that mutates lines at the byte level: the
   edge cases of counsel's probes (empty, CRLF, BOM, NUL, invalid UTF-8, `1e2`, `-0`, 2^53, duplicate
   keys, lone surrogates, upper-case `\u` hex, `\/`, raw DEL, top-level array, depth 32/33/5,000/100,000,
   5,000-digit integers, non-ASCII digits in `ts`) and random byte flips, with the oracle's verdict where
   SPEC.md decides it and checker agreement alone where it does not.
2. **Full line coverage of the trusted base** (`kernel/`, `judge/`; stdlib `trace`), reported in CI, as a
   pre-stated criterion: a line no test reaches is a line no test defends.
3. **Test the production path, not a proxy.** The judge-modes defect passed every test that ran the
   checker directly. Every C1 component is tested as it runs in production (the clerk as the scheduled
   workflow runs it).
4. **A spec change carries a simulator run.** The `rewriting` oracle went stale when SPEC round 2 changed
   what a valid key entry is. The CI sample (2,000 seeds, both checkers, every push) now catches this;
   a SPEC change also reruns the full 10⁵ before merge.
5. **A charter-amendment entry type.** After genesis any edit to CHARTER.md makes the judge refuse every
   PR (`charter_mismatch`). C1 adds an entry, signed with the change power, that records the new
   charter hash, and the judge checks trunk's CHARTER.md against the latest one.
6. **Attribution is checked, not conventional.** Two C0 commits carry unfilled `Proposer:` placeholders
   (REPORT.md §8.3.4). When proposals become entries, a missing or placeholder proposer is refused
   (`unattributed_entry` already does this for log entries).
7. **Cold review by another party, per layer**, stays: in C0 the builders' own tests and mutants found
   none of the defects that reviews, probes and counsel's runs found (REPORT.md §8.2).
