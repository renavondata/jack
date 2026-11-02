VERDICT: ACCEPT WITH OBLIGATIONS
Reviewed tree: a8df329856e2e57695550b4f3b48294c9dab8b6f

# Sixth read: BRIEF-C2b draft v6

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 2 November 2026.
Read REVIEW-C2b-v5, its reply, then the whole v6 brief, in that order;
checked CHARTER §2, §§4–6, A2.6, A4, A5, SPEC §§5,7,10, and
REVIEW-C2a-am3 against Amendment 3 itself. The reviewed tree above was both
HEAD and `origin/main`, after PR #177. The fetched opening-push branch was
`569a2bdd38b35c6d148d39c78ed4808bcbbc566f`; branch references below mean
those bytes. No brief or code edited.

**V6 disposes of v5 F16–F19: the antecedent job is withdrawn from both the brief and the opening-push tree.**

## Inherited state

`python3 tools/status.py`, as of `2026-11-02T16:15:54Z`, through seq 631:

```text
criterion 3: counted 7650/7800; kernel 450/500; scope equals SPEC and unchanged: True met
criterion 4: attack green on main before first scored cutoff: unverified SHORT
criterion 5: value E 1.000000 >= 20 SHORT
criterion 6: continued liveness E 1 >= 20; unchanged True; attack unverified; late repairs 0 SHORT
J7: 6 of 108 window forecasts unresolved past resolves_by
value: E 1.000000 over 0 events; window events 0
liveness continued: E 1 over 0 items (including projected expiries)
```

`promote C2a: refused` also reports missing verified tests/checker evidence
and unknown off-log repairs. Forecasts 442–447 remain overdue. Bare status
has no Actions/acts evidence; these empty E=1 processes do not establish
either a reset or recovery. REVIEW-C2a-am3:131–160 records evidence-bearing
snapshots below one, not a fresh promotion certificate. A lawful C2a
promotion remains a prerequisite, not something this read supplies.
Headroom is 150 counted lines before opening, 1,350 total above this tree,
and 1,200 after a gate that consumes the whole 150.

## Findings

F20: The per-invite clock is compatible with Amendment 3, provided the stated feedback guard actually governs each draw — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:63–74,88–110,154–182,333–334,379–381; transcripts/BRIEF-C2a-draft.md:304–316; transcripts/REVIEW-C2a-am3.md:28–37,68–84,115–120.

For a round invited near H+0:15 and forecast near H+0:20, W0 is H+2,
the window ends H+3, the resolver starts H+3:10, and the brief estimates
feedback on main at H+3:25. Invites near H+1:15, H+2:15 and H+3:15 can
precede that feedback; the next use of this instance is H+4:15. That is
the stated three intervening draws and four-instance construction.

**The four-hour deadline extension is not a proof of a three-round maximum
delay.** This round's deadline is H+7, later than its next instance draw
at H+4:15 and even that next round's W0 at H+6. A concrete permitted slow
case is feedback arriving at H+6:30: the H+4 slot must wait and then skip
at H+6, even though the earlier round still resolves within its deadline.
It must not draw on stale weights or prematurely impute the earlier round
as a deadline failure. On the passing twin, feedback at H+3:25 is consumed
before the H+4:15 draw. At deadline, missing events are imputed under the
specified six-event rule and their represented gain is frozen.

The guard therefore supplies sequential, feedback-complete operation for
each instance even when the nominal delay estimate fails. Keep the hourly
slot index across skips; do not renumber surviving rounds. Each instance
has at most 84 slots in the fourteen-day budget. The undelayed reduction
applies to the rounds actually drawn, under the named reward-vector/draw
assumptions; it is no regret guarantee for opportunities skipped, nor a
promise of 24 timely rounds. Report waits and skips as the brief requires.

Amendment 3's three-window grouping is expressly superseded from the first
invite, before the affected sessions. Its hourly resolution cadence and
prospective +4 h deadlines remain. Its builder-only session routing is
replaced by C2b's explicit other-principal routing when the builder is the
invited arm; retaining builder-only resolution then would violate SPEC §7.
The six datasets, hourly windows, W0 cutoffs, evidence timing, value mixture
and null survive. Already issued forecasts retain their own deadlines and
first-forecast/revision treatment; changing session shape cannot erase
them, their losses or their writs. Four hours to resolve does not authorize
fetching a replacement evidence page four hours late.

The current session prompts are still C2a prompts. In particular,
`transcripts/sessions/stream-forecast.md:9` has a current-hour fallback and
`stream-resolve.md:9` is builder-routed. C2b expressly requires their
rewrite: the invite owns W0, and the resolver has the other principal.
Deliver that before the first election session; do not apply the old
fallback to an invite. This is a stated implementation obligation, not an
unmade repair to the v6 brief. **Remaining Amendment 3 text conflict: none.**

F21: The opening push carries the two promised functional changes, with one stale accompanying note to reconcile — severity: OBLIGATION — witness: commands below; fetched transcripts/PUSH-c2b-opening.md:3–24; fetched SPEC.md:425,437; transcripts/BRIEF-C2b-draft.md:238–272,310–311,352–356.

Executed:

```sh
git fetch origin push-c2b-9000
git diff 606d276bf89946b1095dec6af8c49a04a9bebabb origin/push-c2b-9000 --stat
git diff --quiet 606d276bf89946b1095dec6af8c49a04a9bebabb origin/push-c2b-9000
```

Both diffs produced no output; `--quiet` exited 0. The net branch delta
from its merge base with the reviewed main is exactly:

```text
M  .github/workflows/tests.yml
M  SPEC.md
M  judge/scope.json
A  transcripts/PUSH-c2b-opening.md
4 files changed, 62 insertions(+), 6 deletions(-)
```

The cap is 9,000 in scope and its SPEC mirror, with a cap-history clause.
The workflow has `unit`, `pins`, `sample`, and the `tests` gate. All five
commands are present once, with no step conditions or continue-on-error;
each worker has the same pinned checkout/Python setup; self-check precedes
the sample; the gate uses `always()` and tests all three results for
`success`. There is no antecedent job or helper in this net delta. Old
antecedent commits remain in branch history followed by their withdrawal;
they are not an additional effect in the tree the push installs.

Strictly, there is also the accompanying transcript, not just the three
trusted files. Its lines 13–14 still call the sample skip an in-window
item, and its budget list and SPEC's historical budget sentence still name
that skip. Those are stale descriptions, not an implemented third change
or authority to perform one: v6 explicitly withdraws it and freezes the
workflow. Counsel should reconcile the note with v6 and report the
withdrawal; this does not require an extra trusted-base operation. No
promised opening-push functionality is absent. The read gate must arrive
on main beforehand; W5, election code, tests and pins are expressly later
deliveries, not omissions from this branch's two-change patch.

F22: The retained arithmetic and draw contract remains implementable, conditional and distinct from promotion value — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:75–87,101–153,154–191,328–345; transcripts/REVIEW-C2b-v5.md:45–69,84–92; SPEC.md:40–43,101–106; CHARTER.md:342–360.

F15 stays repaired: `Fraction(g)` represents the specified binary64 gain,
not the mathematical logarithm. Preserve endpoint values, the six-event
denominator, deadline imputation, exact grid propensities and rational
accumulation. Test the partial-round 5/6 example through that representation.
Keep large integers/rationals and float parameters as strings; the invite's
per-mille success forecast is not its selection propensity. Recompute the
signed-prefix draw rather than trusting recorded gains; preserve the
runtime needed for the floating-point stages. Report evidence for custody,
hash and reward-vector assumptions without treating observed arm frequencies
as certification. Invitation scores and regret do not substitute for value.

F23: The opening prerequisites and full exit predicate still bind — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:35–44,192–234,278–292,307–325,358–384; CHARTER.md:94–104,278–282,376–384; log.jsonl:202; status output above.

Retain v5 F1–F14's surviving implementation/report obligations, as counsel
accepts in `REPLY-REVIEW-C2b-v5.md:8–19`. In particular: obtain C2a's lawful,
evidence-bearing promotion; re-declare herald-2 with forecast power before
invites (seq 201 grants merge only); authenticate the read's current blob,
headers, proposal and historical non-counsel principal on the actual push
path; fit the gate, tests and three pins within 150 lines or stop; enter
X0–X5 and seed W5 before opening. Deliver W5 first, with five pins and its
contemporaneous escalation evidence, then the election and attack tests
before counting rounds. The workflow pin remains unconditional again and
needs passing and failed/skipped-dependency witnesses; this read of YAML
does not supply the future green main execution.

Freeze criterion 3's trusted bytes after the opening push, preserve all
value/liveness history and wealth, retain bad rounds, and require all nine
criteria together at the exit prefix. Preserve the deadline and repair
rules, A3.4, no veto, no second push and the deferred-item report. X5 now
prices the parallel split alone; faster CI is a forecast, not an exemption
from any gate. No new machinery is needed to replace the withdrawn reuse.

## Answers and verdict

1. **Pre-opening text defect in v6 requiring repair: none.** The interleaving
   is sound with its wait/skip guard, not as an unconditional wall-clock
   delay bound. Amendment 3 leaves no contradictory election instruction.
2. **Opening push:** cap plus parallel workflow, with the accompanying note
   identified in F21. No extra functional change and no missing promised
   opening-push functionality; stale sample-skip prose is an obligation.
3. **Anything I would still block on: none. Verdict: ACCEPT WITH OBLIGATIONS.**
   This is the brief's non-BLOCK read, not a claim that the opening's still
   outstanding prerequisites or the exit's criteria already hold.

## Forecasts

forecast: **p = 0.35** that C2b's window under BRIEF-C2b draft v6 at
`a8df329856e2e57695550b4f3b48294c9dab8b6f` ends in promotion rather than
failure, with every pre-stated criterion holding on the exit prefix by
the window's end. Resolve 0 if v6 is superseded without such a window,
no such window has promoted by `2026-12-31T00:00:00Z`, or a purported
promotion lacks a criterion. Promotion under repaired brief bytes does
not count. Type `review.forecast`; resolves_by `2026-12-31T00:00:00Z`;
args `{"model":"openai/gpt-6-astra"}`.

forecast: **p = 0.55** that by `2026-11-30T00:00:00Z` C2b's required
`tools/elect.py`, W5, read gate, workflow, tests and pins are delivered
with the complete counted set at or below **9,000**, preserving required
functionality and coverage, and its window has ended with **no second
push inside it**. Pre-opening corrections may count. Failure to deliver,
dropping required functionality/coverage, an unfinished window at that
date, or a second in-window push resolves 0. Type `review.forecast`;
resolves_by `2026-11-30T00:00:00Z`;
args `{"model":"openai/gpt-6-astra"}`.

Withdrawal removes the four concrete blockers and an unnecessary build
burden. The first probability remains below counsel's 0.4 because C2a
must first qualify, the gate has only 150 lines, and W5 needs real timely
history. The second rises from v5's 0.40 because the authenticated-reuse
contract and helper are gone. Hourly congestion, the remaining 1,200-line
allowance after the gate, and first-push correctness still carry risk.
Neither forecast is conditional on the other.

Proposer: reviewer reviewer-2
