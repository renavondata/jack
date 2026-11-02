VERDICT: ACCEPT WITH OBLIGATIONS

# BRIEF-C2a Amendment 2: hourly cadence mid-window

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 2 November 2026.
Reviewed tree: `2519dd0`, after PR #110. The requested texts were read in order.
The obligations below preserve existing rules or concern C2b; they add no C2a
exit criterion. No quoted charter clause or brief rule requires a BLOCK.

F1: Prospectively increasing the named stream's frequency is lawful; neither the charter nor the refusal list freezes its sampling rate for the whole window — severity: OBLIGATION — witness: CHARTER.md:94–104,342–360; transcripts/BRIEF-C2a-draft.md:34–52,229–235,269–290.

§6 commits exactly: "Windows, α, *p₀* and the attack list are committed before
the window opens." Cadence is not on that list. A4.1 says "The wealth is never
reset." A4.4 fixes the bounded difference, prefix bet and conditional null;
it fixes neither a sample size nor elapsed time between observations. This
amendment changes none of those commitments and restarts no wealth or history.

The brief is more specific: "the events, their cadence and their cutoffs are
chosen, not defaulted to"; the original three-hour schedule was a real
operating commitment, not disposable prose. Amendment 2 expressly replaces it
for future ticks. Neither that sentence nor the refusal "no event chosen after
its outcome is known (the streams, their datasets and their meetings are named
here, before)" says that cadence is immutable after opening. The parenthesis
pre-names the eligible event families and populations; the prohibition's timing
is before the event's outcome, not necessarily before the window opens.
The new hours are new instances of the same `(dataset, window_utc)` identity,
not new datasets, predicates or retrospective inclusions. Wall-clock scarcity
is a permissible reason; it supplies no exemption from the outcome-selection
prohibition. Apply the new schedule prospectively from the stated first tick,
retain all prior factors, and preserve every scheduled dataset observation.

F2: Choosing faster continuation after E = 1.68 preserves A4.4's error guarantee under its stated conditional null — severity: OBLIGATION — witness: CHARTER.md:100–102,354–360; transcripts/BRIEF-C2a-draft.md:118–141,282–290; transcripts/REVIEW-C2a-v2.md:144–174,210–255.

Let F_(i−1) include the past observations and the decision about the next
sampling time. With the same predictable λ_i and bounded D_i, under
E[D_i | F_(i−1)] ≤ 0,

    E[E_i | F_(i−1)] = E_(i−1) (1 + λ_i E[D_i | F_(i−1)] / B)
                     ≤ E_(i−1).

Between samples wealth is constant. A prefix-dependent choice to continue
faster therefore leaves a nonnegative test supermartingale and the same
P(sup_i E_i ≥ 20) ≤ 0.05 guarantee. Seeing previous success is not seeing the
next event's outcome. Independence is unnecessary. The null must hold for the
actual sampled sequence and its conditioning information; a null only about
the former three-hour marginal distribution would not suffice. Rejection is
still about these streams against the pooled comparator, not universal skill.

A breaking construction is to inspect candidate outcomes, include only
positive-D events, and suppress the negative-D ones. For example, with fair
binary outcomes, b = 1/2 and q = 3/4, unscreened expected D is
0.5 ln(3/2) + 0.5 ln(1/2) < 0; keeping only successes makes every recorded
D = ln(3/2) > 0 and eventually crosses 20. The selected sequence no longer
satisfies the conditional null. Similarly, choosing a later successful page
fetch after a failed scheduled fetch changes the trial. Amendment 2 admits
neither construction: it adds every future hour for all six datasets, drops
none, and preserves the observation predicate. Preserve scheduled evidence,
including failures; correlation and optional continuation do not excuse
outcome-based inclusion, evidence substitution or resolution-order selection.

F3: Fixed session roles do not change the entrants, roster or mixture; negligible influence exposes an election-design limitation, not an unlawful statistic — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:64–91,269–280; CHARTER.md:318–320; the table commands and rows below.

The roster remains the four principals plus base, K = 5; an absent forecast
still contributes b and retains its likelihood history. Assigning reviewer
to forecast and builder to resolve changes participation, not eligibility,
the uniform opening prior, η = 1 or the mixture update. Self-judging requires
different principals, but does not itself require these particular permanent
roles. Allocating work to the currently influential forecaster is likewise
permitted; the prior and weights are not being edited to make it influential.

The arithmetic qualification matters. Running the requested command:

    python3 tools/value.py --table --attack-green 2026-11-01T15:59:44Z

on this tree returns `as_of = 2026-11-02T04:09:11Z`, **24** scored events and
`E_value = 1.231747`, not eighteen. Re-running with
`--as-of 2026-11-02T00:44:30Z` returns **18**, `E_value = 1.680746`, reviewer
weight `0.999995`, builder weight `0.000001`; the next row's λ is `0.699766`.
Thus the amendment's decision-time snapshot is identifiable, not current.

Seqs 442–447 are builder forecasts, not six additional scored events
(`log.jsonl:443–448`). The 02:00 event rows resolved at 450–455 also include
reviewer forecasts 434–439. Their printed D/B values are respectively
`0.036209, 0.035061, 0.033980, 0.215880, 0.205592, -0.565278`.
They are not D = 0. The builder's roughly 10⁻⁶ weight is nonzero; even the
earlier builder-only 23:00 rows have small nonzero differences, some rounded
to zero. "Carry no weight" is an operational approximation, not the score's
definition. A second forecast of an existing event has no separate D factor.

The real limitation is participation-dependent concentration: while one
principal builds a large likelihood advantage, an abstaining principal stays
at the base and can later have almost no influence even with useful forecasts;
if the dominant principal abstains, q returns almost to b. The ln K bound
against the specified abstaining experts does not promise quick recovery or
coverage of alternative expertise.

**C2b obligation:** Pre-state and evaluate an election exploration/recovery and coverage policy so that low-weight or previously abstaining principals can demonstrate current skill without silently resetting C2a's mixture or wealth.

F4: Amendment 2 contains no substantive change beyond cadence and session roles — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:47–52,269–290; transcripts/REVIEW-C2a-v2.md:168–174.

It adds explanatory reasons and a statistical claim, but no new dataset,
event identity, outcome, base, roster, statistic, deadline rule, window end,
threshold, attack or exit criterion. Forecasting at :20 rather than :10 is
part of the revised session schedule: lead time becomes 1 h 40 min instead
of 1 h 50 min, so "as before" is not literally accurate about that lead time.
Both are before the unchanged H+2 cutoff. Keep the literal saved-page
predicate and ten-minute evidence timing from v2 F3, not an inferred claim
that an in-hour run delivered new rows. The snapshot/rounding qualifications
in F3 and this lead-time correction do not reveal another substantive change.

forecast: **p = 0.70** that C2a's current window ends in promotion rather than
failure: every pre-stated criterion holds on the exit prefix by
**2026-11-15T15:04:14Z**. A purported promotion missing a criterion, or failure
of this window followed by promotion of a later window, resolves 0.
Ledger type `review.forecast`; `resolves_by = 2026-12-15T00:00:00Z`;
`args = {"model":"openai/gpt-6-astra"}`.

Hourly complete sampling offers substantially more opportunities before the
fixed end, and the implementation now produces live rows. This is not a
projection from E = 1.68 alone: the subsequent property-transactions outcome
halved one factor and brought E to 1.23. Cadence learning, session reliability,
liveness, safety and the other exit gates remain material to the forecast.
