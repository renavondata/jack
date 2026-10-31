# The cap push to 6,900 (31 October 2026) — counsel's note for the sovereign's `jack push`

Two edits, nothing else: `judge/scope.json` `cap` 6200 → 6900 and the identical block in SPEC §10, with
one clause added to §10's history of the cap. No kernel source changes; no run of record is due.

The number, measured and never anticipated (BRIEF-C1b v7 §Scope: "a push is decided on that number,
never before it"):
- PR #57 (31 Oct 10:51Z): W1 and the item process built, **6,223** — the builder stopped at the cap.
- PR #59 (11:40Z): the clerk complete, **6,813**; the judge refused it for `code_cap`.
- PR #60 (11:56Z): one consolidation pass under the sovereign's decision, **6,744**; every pin-named
  assertion kept, none omitted.
- PR #61 (12:25Z): the reviewer's 24 pins registered against that tree, 30 mutants KILLED with passing
  twins, **6,874** — the complete figure. `pins/pins.py` 820 → 950.
6,900 is the next fifty above it; 26 lines of headroom remain for fixes inside the window, and a fix that
needs more is a further measured push, which is what the cap is for.

What this push records against the pre-statement: v2 anticipated 7,000 and two readers called it
anticipation; v3–v7 said "no cap change" and bet 0.65 falling to 0.3 (L5) that the clerk would fit; four
readers priced that at 0.25, 0.25, 0.20, 0.25. L5 resolves 0 on this push. The clerk as specified by seven
reads is about 880 lines of code, tests and pins, and the specification was not shortened to fit the
cap; the readers' findings each added assertions, and the sovereign chose to keep them.

The branch `push-cap-6900` is one commit by counsel-2 on `main` at `1c4f8a3` (seq 196). After the push:
the builder re-proposes the clerk from the new `main` (its entries on #60 are stale), the herald merges
it, the reviewer re-proposes the pins, the herald merges them; counsel writes RUNBOOK `jack clerk`.
