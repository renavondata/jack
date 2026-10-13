# Brief C1 — the clerk and writs (draft, for Guy to amend or discard)

CHARTER §8: *C1: clerk and writs; Guy's acts as typed entries. Exit: clean
simulator run, then E_t ≥ 20 against p₀ within 14 days live.* This draft is
counsel's proposal of scope; it binds nothing.

## Precondition

C0 promoted: genesis signed, both checkers agreeing on the real log and 10^5
seeded logs, every pin KILLED, kernel within 1,000 lines. If kernel2 is still
absent, C1 cannot open (§6 safety needs independent replay).

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
3. **Lapse completed.** Notice period as a writ; `counter_witness` entry type
   whose witness joins a rule's violating witnesses (C0's rule bodies are
   immutable, so counter-witnesses must be separate entries); the lapse itself
   as a change entry the clerk prepares and the change key signs — or, if Guy
   prefers, an automatic lapse at notice end recorded by the clerk's key.
4. **Lawful changes to the trusted base.** `merge.installs`: a merge entry
   signed by the change key names the trusted-base digest that is in force
   from the next entry; the judge then accepts proposals touching trusted paths
   only when a matching `installs` follows, and checks trunk's actual digest
   against the digest in force. Until then the trusted base changes only by
   Guy's own commits (C0 rule).
5. **Merge authorship.** The judge holds no secret, so C0 cannot sign `merge`
   entries; the clerk's herald key (`accept`, `wish`, and `merge`?) is Guy's
   decision. The herald key must not hold `rule`, `repeal` or `key`.
6. **Second checker in CI.** `sim/run.py --second kernel2/check`; the judge
   already refuses `checker_drift`.

## Questions C0 raised for C1 (see REPORT.md)

- Comparison built-ins (`≠`, `<`) are absent; uniqueness rules ("one merge per
  proposal") are inexpressible. Add `neq/2` by a kernel change entry, or keep
  such rules in the clerk?
- `pull_request` runs the proposal's own tests and pins (F1). Make the
  `push: main` run the one that counts, or drop the PR run to a report?
- A `key` entry that leaves no key with `key` power locks the log. Refuse it in
  the kernel, or leave it to Guy?
- Lapse candidacy is evaluated against the current prefix; a rule's witness can
  become redundant because of unrelated entries. Freeze the context at
  admission instead?
- Hardware keys (`sk-ssh-ed25519@openssh.com`) sign a different message; add
  the format by change entry if Guy's master key needs it.

## Pre-stated exit

Clean simulator run (attack list extended with stalling and flooding as
liveness attacks the clerk must answer); then E_t ≥ 20 against p₀ (assize's
weekly `guy_acts.py` series) within 14 days live; windows, α = 0.05, p₀ and
the attack list committed before the window opens; zero checker disagreements
throughout; Guy has not vetoed.
