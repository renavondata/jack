# BRIEF-C2a — value: the aggregate against the base rate (draft v1, counsel, 1 November 2026)

C2 is split as C1 was (A3.2): **C2a**, this brief — forecasts, proper scores and the election of proposers
by their record, in tools only; and **C2b**, its own brief, the one kernel change (`invite`/`accept`/`wish`,
automatic `promote`, the repair recorder). C2a opens at the `ts` of the opening `push` (§Order of acts),
which follows `decision promote C1b` and this brief's merge with one cold read on the record. Its exit is a
crossing (A5), its window a maximum of fourteen days.

## Precondition
C1b promoted by a `decision promote C1b` entered while `status.py` printed `lawful`; this brief and its read
on `main`; the opening push in force (§Scope: the cap).

## Purpose
CHARTER §6: "C2: aggregated forecasts beat the base-rate forecaster in log-loss", *E* ≥ 20. A3.1: "the election
of proposers by their record". The question C2a answers is whether a forecaster made of the proposers' own
records is better than knowing nothing but the base rate — and whether the record, left to itself, demotes a
proposer who should lose. Both are already visible in the pre-window data (§Statistic, the worked table):
the point of the window is to establish them prequentially, under pre-stated rules, on events that were not
chosen after the fact.

## Scope
- **The entrants.** Every principal that holds `forecast` (today counsel, reviewer, builder, guy) and the
  **base-rate forecaster** itself. An entrant's probability for an event is its own forecast when it made one
  and the base rate when it did not (it abstains, and an abstention scores as the base rate). The base-rate
  forecaster is an entrant like the others: it can win the election.
- **The aggregate** is the Bayes mixture over the entrants with the uniform prior: weight ∝ exp(−cumulative
  log-loss) = the product of the entrant's past likelihoods on resolved events; the aggregate's probability
  for an event is the weighted mean of the entrants' probabilities at the instant the event is fixed. No
  learning rate: with η = 1 the mixture's cumulative log-loss is within ln K of the best entrant's, K = the
  number of entrants, which is the bound the law needs (CHARTER A4 maxim: a constant derived from a bound).
  Hedge with η < 1 is a second aggregate that may enter later as an entrant of its own; not here.
- **The events.** Every `forecast` entry resolved after the opening, of every type, grouped by (type, claim):
  two proposers on one claim are one event. An event is **fixed** at the `ts` of its first forecast; the
  aggregate's probability for it is computed from the record at that instant, so nothing resolved later can
  move it (pin `fixed_before_resolution`). A forecast whose `ts` is after its event's resolution `ts` is not a
  forecast of that event (pin `rigged`). Forecasts standing at the opening are events of the window if their
  resolution falls inside it; their probability is fixed at the opening.
- **The base rate** is C1's: prequential Laplace per `type`, in resolution-`seq` order, exact fractions
  (BRIEF-C1 §score; A4). Nothing finer than the type: a base rate per dataset or per venue would be a model,
  and a model is an entrant, not the null.
- **The streams** (the object, A3.4; pre-stated so that the cadence is chosen, not defaulted to): the
  renavon freshness stream, hourly, alternating builder and reviewer keys, three datasets, resolved from the
  public page's `dateModified` hashed into `transcripts/evidence/`; the HKJC per-race stream on race days,
  counsel and reviewer, resolved by the builder from hashed results pages; jack's own `proposal.ci` and
  `proposal.count` on every proposal; `counsel.programme` and `review.forecast` as they arise. The brief does
  not require a proposer to forecast any event; it requires that whoever forecasts does so before the event
  is fixed, and that the runner's sessions resolve what is due (W1, unchanged from C1b).
- **The cap.** The counted set stands at 6,882 against 6,900. This brief pre-states C2a's budget: **7,300**,
  raised by one `push` at the opening together with the two trusted-base changes the loop needs (`tests`
  skipping the heavy diff on log-only commits; nothing else) and never again inside the window. If the
  builder's deliverables do not fit, the builder stops and reports the shortfall; the window then fails on
  criterion 3 and a new window is pre-stated — a mid-window push is the C1b lesson, not to be repeated.
- **The trusted base is otherwise not touched.** No kernel change: `invite`, `accept`, `wish`, automatic
  `promote` and the recorder are C2b's. No agent code (PLAN §9). No LLM in any scorer or aggregate.

## Order of acts, and the clock
1. This brief merged with its read on the record. Counsel enters V0–V3 (§Forecasts) with `args.id`.
2. The sovereign's `decision promote C1b` (if not already), then the opening `push` (cap 7,300, the CI skip).
   C2a's window opens at the `push` entry's `ts` and ends at V0's `resolves_by`, fourteen days later at most.
3. The builder builds `tools/value.py` to this text; the reviewer registers the pins; the herald merges;
   the streams run. No event resolved before step 2's `ts` counts; forecasts standing at it count as §Scope says.
4. `status.py` prints the value line and the `promote C2a: lawful | refused: …` line; the sovereign's
   `decision promote C2a` when it reads `lawful` (A5: at the crossing, not the deadline).

## The statistic: value as a likelihood ratio
For each event *i* resolved in the window, in resolution order, with outcome *Yᵢ*, aggregate probability *qᵢ*
(fixed as above) and base rate *bᵢ* (Laplace, fixed before *Yᵢ* is seen):

  *E*ᵥ,ₜ = ∏ᵢ≤ₜ [ *qᵢ*(*Yᵢ*) / *bᵢ*(*Yᵢ*) ],  where *q*(1) = *q*, *q*(0) = 1 − *q*.

Under H₀ "the base rate is the truth" *E*ᵥ is a test martingale (each factor has expectation 1), so
*E*ᵥ ≥ 20 is a level-0.05 rejection of "the aggregate knows nothing the base rate does not" — the charter's
sentence, literally. No λ, no p₀: the margin by which a forecast beats the base rate is the stake. Exact
fractions; `p` in per-mille as entered. (The alternative, *Yᵢ* = 1 iff the aggregate's log-loss on *i* is below
the base rate's with p₀ = ½ in A4's betting form, is weaker by construction — it discards the margin — and is
named here so a read can prefer it with a reason.)

**Worked table, pre-window, on the real log to seq 268 (illustrative; nothing here is the window's score).**
29 events (claims), 34 resolutions, base rate per type as above:

| entrant | events forecast | own LR against the base | mixture weight at seq 268 |
|---|---|---|---|
| counsel | 17 | 7.34 | 0.573 |
| builder | 2 | 2.42 | 0.189 |
| guy | 3 | 1.68 | 0.131 |
| base-rate forecaster | — | 1 | 0.078 |
| reviewer | 12 | 0.358 | 0.028 |
| **Bayes mixture** | 29 | **2.56** | — |

Read it as the mechanism, not as a result: the reviewer's four bets that the clerk would fit under 6,200
cost it its weight; the base-rate forecaster already outweighs it; the mixture is better than the base rate
and worse than the best entrant by less than ln 5. By type the picture is uneven — `world.hkjc` 17.3 over
eight events, `world.renavon` 0.03 over three (the first freshness forecasts said 200‰ for datasets that
advance every hour; the sessions learnt, the base rate per type had not) — which is what a prequential
score is for. The builder's `tools/value.py` must reproduce this table from the log at seq 268 exactly
(pin `worked_table`): it is the fixture.

## Liveness continued (A4: wealth continues)
C1b's item process continues unchanged into C2a — the same items, the same p₀ = 6/11, the same taint by a
sovereign repair — from the wealth it holds at C1b's promotion. Criterion 6 asks only that it has not fallen
below 20 at the exit. The clerk and its writs are unchanged.

## Safety: two attack kinds before any event counts
The simulator gains `rigged` (an entrant whose forecasts carry a `ts` after the resolution's, or whose
probability is revised after the event is fixed) and `colluding` (two keys, one principal, forecasting the
same claim to double a weight). Both are refused — `rigged` by the scorer's fixing rule, `colluding` by the
kernel's principal rule and the scorer's grouping by principal — and the run that shows it is on `main`
before the first event is scored (criterion 4).

## Pre-stated criteria for C2a, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines within 7,300; the kernel within 500; `judge/scope.json` and SPEC §10's block unchanged
   since the opening push.
4. `rigged` and `colluding` refused in the simulator on `main` before the first scored event.
5. **Value**: *E*ᵥ ≥ 20 on the window's events, computed from the log by `tools/value.py`.
6. **Liveness continued**: C1b's process at or above 20 on the exit prefix.
7. **Elections witnessed**: at the exit at least one entrant's weight is below the base-rate forecaster's
   on the window's events alone (PLAN §4: "no witness yet").
8. No `decision` of kind `veto` with subject `C2a`; off-log repairs 0 on the acts evidence; A3.4 at or
   under 5 : 1.

## Pins (the reviewer's), each with its named mutant and passing twin
`worked_table` (the fixture above reproduced exactly; mutant: Laplace prior 1/2 → 1/3) · `fixed_before_resolution`
(an event's *q* uses only forecasts and weights from before its first forecast's `ts`; mutant: weights read at
resolution) · `rigged` (a forecast with `ts` after the resolution is excluded; mutant: included) · `abstention_is_base`
(an absent entrant scores as the base rate; mutant: as ½) · `grouping_by_claim` (two proposers on one claim are
one event; mutant: two events) · `grouping_by_principal` (two keys of one principal are one entrant; mutant:
two) · `uniform_prior` (initial weights equal; mutant: counsel 2×) · `no_learning_rate` (η = 1; mutant: η = ½)
· `exact_fractions` (no float on the path to *E*ᵥ; mutant: one division in float) · `per_type_base` (base
rate per type, never per args; mutant: per dataset) · `martingale` (on a simulated log where outcomes are
drawn from the base rate, *E*ᵥ's mean over seeds is within the bound; mutant: a factor with expectation > 1)
· `elections_witnessed` (criterion 7's check; mutant: always true) · `window_from_the_push` (events before the
opening push's `ts` excluded; mutant: from the brief's merge) · `promote_refused_value` (the verb signs nothing
when *E*ᵥ < 20; mutant: signs).

## Refusal list
No LLM call in `tools/value.py`; no learning rate, prior or threshold chosen by hand (uniform prior and η = 1
are derived, 20 is the charter's α); no event scored twice; no forecast made after the event's resolution
counts; no change to C1's statistics or the clerk; no kernel or kernel2 change; no trusted-base change but the
opening push; no agent code; no second push inside the window; no event chosen after its outcome is known
(the streams are named here, before).

## Stop and report if
the build does not fit under 7,300 (the shortfall in lines); the two checkers disagree; a stream's public
evidence disappears (the window continues on the other events; the report says so); the worked table cannot
be reproduced exactly (a defect in this brief's arithmetic, to be fixed by amendment before any event is scored).

## Deliverables
`tools/value.py` (the scorer and the aggregate; a `--table` mode that prints the worked table; `status.py`
reads it for criteria 5–7 and the `promote C2a` line); `tests/test_value.py`; the two simulator kinds; the pins;
RUNBOOK `## jack value`; counsel's V0–V3; the C2a report in REPORT.md's form; the C2b brief text at exit.

## Counsel's forecasts on this window (entered after the read, before the opening push)
| id | claim | p |
|---|---|---|
| V0 | the promotion forecast: every criterion holds on the exit prefix by V0's `resolves_by` (the opening + 14 d) | 0.55 |
| V1 | *E*ᵥ ≥ 20 within 7 days of the opening push | 0.45 |
| V2 | at the exit some entrant's weight is below the base-rate forecaster's | 0.8 |
| V3 | no second push inside the window | 0.75 |
