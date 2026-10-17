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
6. **Second checker in CI.** Done in C0: `harness/diff.py` (SPEC §9a) runs 300 seeds
   and the vectors through both checkers on every push to main and every pull
   request; the judge refuses `checker_drift`. C1 adds its attack kinds and keeps it green.

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

## From C0's exit (counsel, 17 October 2026)

Scope for C1, each from a witnessed case; Guy strikes what he does not want.

0. **Already law.** SPEC §10.7–10 (a proposal names its party; counsel does not build; scope by path;
   a size cap) entered C0 after two witnessed cases of proposals beyond their authority (the founder's
   first draft; counsel's harness). C1's `judge/scope.json` sets its own paths, documents and cap.
1. **Keys for every party.** Items 7–8 check a claim. C1 declares a key per party (builder, reviewer,
   counsel, herald) by `key` entries with `proposal` power only, once the kernel refuses a `key` entry
   that leaves no key with the `key` power; a proposal is then signed, not labelled.
2. **A window, stated before it opens**, and a trusted-base defect inside it restarts it (CHARTER §6).
   C0 had neither.
3. **A charter-amendment entry type.** After genesis any edit to CHARTER.md makes the judge refuse every
   proposal. §5 of this report's proposed charter changes wait for it.
4. **`merge.installs`** (scope item 4): the digest in force becomes an entry, so the trusted base can
   change lawfully and the record can say which checker judged what.
5. **A byte-level simulator kind.** Every checker disagreement found in C0 came from reviews and byte
   probes, none from the simulator; the differential now compares every prefix, but the generator still
   never produces malformed lines, non-ASCII digits, a BOM, CRLF or deep nesting.
6. **Habits, not scope:** a spec change reruns the full differential before merge; the production path is
   what is tested; every layer is read cold by a party of another family; counsel writes text and reads
   verdicts, never code.

**A question for the brief's opening.** It assumes the first real case needs a rule language in the
kernel. C0's first two cases were judge-level, about paths and parties, and were met by data the judge
reads. Whether C1's first rule is a kernel rule (non-decreasing timestamps has no witnessed case yet) or
another judge-level one is for Guy to decide before the language is chosen.
