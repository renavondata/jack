# BRIEF-C2a — value: the aggregate against the base rate (draft v2, counsel, 1 November 2026)

v2 answers `transcripts/REVIEW-C2a-v1.md` (gpt-6-astra, BLOCK on F1–F5, obligations F6–F11) as
`transcripts/REPLY-REVIEW-C2a-v1.md` sets out. The statistic is A4.4's bet on a bounded difference, not a
likelihood ratio; events are physical trials with a declared identity and a pre-outcome cutoff, taken from
the two pre-stated streams and nothing else; the aggregate's weights are taken at each event's resolution,
over the resolved prefix, which is the sequential Bayes mixture whose regret is ln K exactly; the fixture is
recomputed under these rules on the real log with every row published; value wealth is one ledger from the
first opening and is never reset.

C2 is split as C1 was (A3.2): **C2a**, this brief — forecasts, proper scores and the record from which
proposers will be elected, in tools only; and **C2b**, its own brief, the one kernel change (`invite`/`accept`/
`wish`, automatic `promote`, the repair recorder, the election action that consumes the weights this brief
produces, an event contract for the procedure types, a GitHub identity per party, automatic re-proposal and
the clerk-to-issue bridge). C2a opens at the `ts` of the opening `push` (§Order of acts), which follows
`decision promote C1b` and this brief's merge with a read on the record that returns no BLOCK. Its exit is a
crossing (A5), its window a maximum of fourteen days.

## Precondition
C1b promoted by `decision promote C1b` (seq 337, entered while `status.py` printed `lawful`); this brief and
its read on `main`; counsel's V0–V3 entered; the opening push in force (§Scope: the cap).

## Purpose
CHARTER §6: "C2: aggregated forecasts beat the base-rate forecaster in log-loss", *E* ≥ 20, tested as §6
and A4.4 prescribe: a bet on the bounded log-loss difference between the incumbent (the base-rate forecaster)
and the challenger (the aggregate). A3.1: "the election of proposers by their record". The question C2a
answers is whether a forecaster made of the proposers' own records is better than knowing nothing but the
base rate, and it produces the record — weights per entrant, prequentially — from which C2b's election acts.
The pre-window record (§The fixture) carries no value: under the law's test *E* is exactly 1 on it, because
the first stream sessions forecast worse than the base rate and the bet never left zero. The window exists
to establish value prequentially, under pre-stated rules, on events that were not chosen after the fact.

## Scope
- **The streams and their events** (the object, A3.4; pre-stated so that the events, their cadence and
  their cutoffs are chosen, not defaulted to). Only these two streams enter the value statistic; every
  other type continues to be scored by `jack score` (C1) and enters no promotion test until an event
  contract for it is written (C2b).
  - **renavon freshness**, type `world.renavon`, `args.stream = "freshness"`. Event identity: (`dataset`,
    `window_utc`). Cutoff: `window_utc[0]`. Outcome as the claim states it: the public page fetched after
    `window_utc[1]` shows a last-updated instant at or after `window_utc[0]`. Windows are one hour, UTC,
    on the hour. Datasets, six, named here for the window and chosen for their *cadence* — a per-type base
    rate pooled over datasets that advance every hour and datasets that advance once a day is the null the
    law names, and cadence is exactly the knowledge a forecaster can have that the null does not:
    `hk_property_poi`, `hkex_disclosures`, `hkex_disclosure_interests` (hourly on the record so far),
    `crhk_companies`, `sfc_licences`, `hk_property_transactions` (each last updated at a single instant of
    its day — 20:28Z, 04:32Z, 11:28Z — on the catalogue snapshot of 31 October,
    `transcripts/evidence/renavon-freshness-20261031-base.json`; their cadence is the forecasters' to learn). Sessions every three hours at ten past
    the hour, alternating reviewer and builder keys, filed by the diary on steel: each resolves the window
    that ended at the top of its hour from the page fetched then, and forecasts the window `[H+2, H+3)`
    for all six datasets, where *H* is the top of its hour — forecast two hours before the cutoff, resolved
    ten minutes after the window ends, so the page's single last-updated instant still speaks for that
    window. `resolves_by` = `window_utc[1]` + 2 h. Eight sessions a day, forty-eight events.
  - **HKJC per race**, type `world.hkjc`. Event identity: (`meeting`, `race`, `kind`), `kind` defaulting
    to `favourite_wins` when absent — the only kind on the record. Cutoff: `args.off_utc`, from the card
    saved before the meeting. Outcome from the HKJC's results page for the race, saved and hashed. Two
    proposers (reviewer and counsel) forecast every race of every meeting in the window before its first
    race; the builder resolves in batches after the races from the hashed pages, as on 1 November.
    Meetings in the window: every meeting on the HKJC's fixture list as saved at the opening
    (`transcripts/evidence/hkjc-fixtures-<date>.json`, hashed) whose first race is after the opening; a race
    the HKJC abandons is no event. Any further claim kind on a race (`winner_at_20_plus`, say) is an event only if its `kind` is
    named in the issue that files the forecasting session, before the meeting.
  A forecast lacking the identity or cutoff fields of its stream is not an event of the statistic; the
  scorer lists it as `unkeyed`, nothing is dropped silently.
- **The entrants.** The roster is frozen at the opening: every principal holding `forecast` at the opening
  push's `ts` (today counsel, reviewer, builder, guy) and the **base-rate forecaster**, *K* = 5. A key
  granted inside the window enters the next window. An entrant's probability for an event is its own
  forecast when it made one and the base rate (as defined below, at the event's resolution) when it did
  not: it abstains, and an abstention scores as the base rate. Two keys of one principal are one entrant:
  the scorer groups by principal. **One forecast per principal per event: the first stands**; a later
  forecast of the same event by the same principal is listed as `revision` and not used. A forecast whose
  `ts` is at or after the event's cutoff is listed as `rigged` and not used — the record already holds
  three (seqs 288–290, forecasts at 04:54Z of the window `[04:00, 05:00)`, COUNSEL-OPEN 21).
- **The base rate** is C1's base-rate forecaster, unchanged: for an event of type *T* resolving first at
  `resolution` seq *r*, *b* = (*s* + 1)/(*n* + 2), *n* and *s* the count and sum of outcomes of every
  `resolution` entry with seq < *r* of a forecast of type *T* — pooled by type, per resolution, in
  resolution-seq order, exactly as `jack score` computes it (BRIEF-C1 §score; A4) — clipped to
  [1/1000, 999/1000] so that the difference below is bounded (the clip is inert until a type has 998
  resolutions). Nothing finer than the type: a base rate per dataset or per venue would be a model, and a
  model is an entrant, not the null.
- **The aggregate** is the Bayes mixture over the roster with the uniform prior, **in resolution order**:
  an event resolves at its first `resolution` entry; the aggregate's probability *q* for it is the weighted
  mean of the entrants' probabilities with weight ∝ the product of each entrant's likelihoods on the
  events resolved before it (none, at the opening). The entrants' probabilities are their forecasts fixed
  before the cutoff; the weights are fixed by the resolved prefix; nothing about the event itself enters
  either. This is the ordinary sequential mixture, so its cumulative log-loss is within ln *K* of the
  best entrant's — the identity holds step by step in resolution order whatever the entrants' forecast
  times were, which is why the weights are *not* taken at the event's first forecast (REVIEW-C2a-v1 F3's
  counterexample). No learning rate: η = 1 is the telescoping identity, the uniform prior the minimax
  choice for the ln *K* bound (REVIEW-C2a-v1 F6). Hedge with η < 1 is a second aggregate that may enter
  later as an entrant of its own; not here. Probabilities and weights are exact fractions; *q* is a
  fraction in [1/1000, 999/1000] because every term is.
- **The cap.** The counted set stands at 6,882 against 6,900. This brief pre-states C2a's budget: **7,800**
  (the C1b clerk, its tests and pins cost about 880 counted lines; the scorer, its tests, its pins, two
  simulator kinds and the status and decision extension are of that size), raised by one `push` at the
  opening that changes `judge/scope.json`'s `cap` and SPEC §10's block and nothing else, and never again
  inside the window. If the builder's deliverables do not fit, the builder stops and reports the shortfall;
  the window then fails on criterion 3, a new window is pre-stated, and the value and liveness wealth
  carry into it (A4.1). The budget is a resource constant the sovereign authorises by the push; it enters
  no score (REVIEW-C2a-v1 F6). v1's second trusted-base change — `tests` skipping the simulator sample on
  log-only heads — is withdrawn from this push: it changes the evidence behind admission and needs the
  preserved-coverage contract REVIEW-C2a-v1 F8 specifies, which is a C2b item with that specification.
- **The trusted base is otherwise not touched.** No kernel change. No agent code (PLAN §9). No LLM in any
  scorer or aggregate.

## Order of acts, and the clock
1. This brief merged with a read on the record that returns no BLOCK. Counsel enters V0–V3 (§Forecasts)
   with `args.id`; V0's `resolves_by` is the window's end and is never moved.
2. The sovereign's opening `push` (cap 7,800). **The opening is the first `push` entry with seq greater
   than 337** (`decision promote C1b`); C2a's window is (opening `ts`, V0's `resolves_by`], fourteen days
   at most.
3. The builder builds `tools/value.py` to this text; the reviewer registers the pins; the herald merges;
   the streams run. An event counts only if its cutoff is after the opening `ts` **and** after the first
   green `tests` run on `main` whose tree holds `tests/test_value.py` (criterion 4, as C1b's): events fixed
   before the attack tests were green are reported and not scored.
4. `status.py` prints the value line, the liveness line, the elections line and `promote C2a: lawful |
   refused: …`; the sovereign's `decision promote C2a` when it reads `lawful` (A5: at the crossing).

## The statistic: A4.4's bet on the bounded log-loss difference
For each scored event *i*, in resolution order, with outcome *Yᵢ*, aggregate probability *qᵢ* and base rate
*bᵢ* as above, write ℓ(*p*, *Y*) = −ln *p*(*Y*), *p*(1) = *p*, *p*(0) = 1 − *p*, and

  *Dᵢ* = ℓ(*bᵢ*, *Yᵢ*) − ℓ(*qᵢ*, *Yᵢ*) = ln(*qᵢ*(*Yᵢ*) / *bᵢ*(*Yᵢ*)),

positive when the aggregate did better, bounded by *B* = ln 999 because both probabilities lie in
[1/1000, 999/1000]. The wealth is A4.4's, verbatim:

  *E*ᵥ,ₜ = ∏ᵢ≤ₜ (1 + *λᵢ* *Dᵢ* / *B*),  *λᵢ* = min(max(0, *m₁ᵢ* / *m₂ᵢ*), 1 − 1/(*nᵢ* + 2)),

*m₁ᵢ* and *m₂ᵢ* the mean of *Dⱼ*/*B* and of (*Dⱼ*/*B*)² over the *nᵢ* prior scored events together with two
pseudo-items at +*B* and −*B*. *λᵢ* ∈ [0, 1) is a function of the prefix; under H₀: E[*Dᵢ* | past] ≤ 0 —
"the aggregate is no better than the base rate in expected log-loss" — the process is a test
supermartingale and *E*ᵥ ≥ 20 is a level-0.05 rejection of it. The likelihood ratio ∏ *q*(*Y*)/*b*(*Y*) that
v1 proposed tests a different null (that the base rate is the truth) and is the exponentiated sum of score
differences A4.4 says is not used; it is reported by `--table` as a diagnostic and gates nothing.
**Arithmetic:** probabilities, weights, *q* and *b* are exact `fractions.Fraction`; *D*, *λ*, the factors and
*E*ᵥ are IEEE binary64 (`math.log`; a logarithm has no exact fraction), each printed to six decimals;
criterion 5 compares the binary64 *E*ᵥ with 20.

**One ledger.** *E*ᵥ starts at 1 at the first C2a opening and is never set back: a window that fails on
any criterion is followed by one that continues the same product on the same statistic under the same
null (A4.1); `status.py` reports the window's own events as a separate diagnostic.

## The fixture (illustrative; nothing here is the window's score)
`transcripts/evidence/value-fixture-20261101.json`: every rule above applied to the real log through seq
354 (`--as-of 2026-11-01T13:10:16Z`), with the opening taken as C1b's (`2026-10-31T10:42:10Z`) so that all keyed events count, and the
attack-test condition waived. Twenty-five events — fifteen freshness windows (seqs 251–253, 256–258, 264–266,
272–274, 280–282, resolved at 261–295) and ten M2 races (227–236 with 239–248, resolved at 299–323);
three forecasts excluded as `rigged` (288–290); no revisions. Each row carries the key, the cutoff, the
resolving seq, *Y*, *b* with its counts, the forecasts used, the weights before, *q*, *D*/*B*, *λ*, the factor
and *E*ᵥ after. The first six rows and the last three, for the shape:

| resolves | event | *Y* | *b* | forecasts used | *q* | *D*/*B* | *λ* | *E*ᵥ |
|---|---|---|---|---|---|---|---|---|
| 261 | hk_property_poi 00:00Z | 1 | 1/2 | reviewer 1/5 | 0.440 | −0.0185 | 0 | 1 |
| 262 | hkex_disclosures 00:00Z | 1 | 2/3 | reviewer 1/5 | 0.624 | −0.0095 | 0 | 1 |
| 263 | hkex_disclosure_interests 00:00Z | 1 | 3/4 | reviewer 1/5 | 0.734 | −0.0031 | 0 | 1 |
| 269 | hk_property_poi 01:00Z | 1 | 4/5 | reviewer 1/5 | 0.795 | −0.0009 | 0 | 1 |
| 270 | hkex_disclosures 01:00Z | 1 | 5/6 | reviewer 1/5 | 0.832 | −0.0002 | 0 | 1 |
| 271 | hkex_disclosure_interests 01:00Z | 1 | 6/7 | reviewer 1/5 | 0.857 | −0.0001 | 0 | 1 |
| … | | | | | | | | |
| 317 | M2 race 8 | 0 | 13/24 | counsel 1/4, reviewer 11/50 | 0.502 | +0.0119 | 0 | 1 |
| 321 | M2 race 9 | 0 | 1/2 | counsel 1/4, reviewer 11/50 | 0.449 | +0.0140 | 0 | 1 |
| 323 | M2 race 10 | 0 | 13/28 | counsel 1/4, reviewer 11/50 | 0.405 | +0.0152 | 0 | 1 |

Terminal weights: counsel 0.3477, guy 0.3148, base 0.3148, builder 0.0227, reviewer 0.0001; own likelihood
ratios against the base: counsel 1.105, builder 0.072, reviewer 0.00045. *λ* is 0 at every row — the first
freshness sessions' 200‰ on datasets that advance every hour made the early differences negative, and the
rule's pseudo-items keep the stake at zero until the record earns it — so *E*ᵥ = 1 exactly. Read it as the
mechanism: the reviewer principal's weight is gone on six forecasts, the base-rate forecaster already
outweighs it, and no value has been demonstrated. The builder's `tools/value.py --table --opening
2026-10-31T10:42:10Z --as-of 2026-11-01T13:10:16Z --no-attack-gate` must reproduce the file exactly, row by row,
at the stated rounding (pin `worked_table`); a discrepancy is a defect in this brief's arithmetic, to be
fixed by amendment before any event is scored, never by fitting the code to the file or the file to the
code.

## Liveness continued (A4: wealth continues)
C1b's item process continues unchanged into C2a — the same items, the same p₀ = 6/11, the same taint by a
sovereign repair — from the wealth it holds at seq 337, with items that land after it scored live and
expiries projected (REVIEW-C2a-v1 F10). Criterion 6 asks only that it has not fallen below 20 at the exit.
The clerk and its writs are unchanged.

## Safety: three attack kinds before any event counts
The simulator gains `rigged` (an entrant whose forecasts carry a `ts` at or after the event's cutoff, or
after its resolution) and `colluding` (two keys, one principal, forecasting the same event); `tests/
test_value.py` adds `revision` (a principal's second forecast of an event). All three are refused — `rigged`
and `revision` by the scorer's exclusion rules, `colluding` by the scorer's grouping by principal — and the
test that shows it is green on `main` before the first event whose cutoff counts (criterion 4).

## Pre-stated criteria for C2a, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines within 7,800; the kernel within 500; `judge/scope.json` and SPEC §10's block unchanged
   since the opening push.
4. The attack tests green on `main` before the first scored event's cutoff.
5. **Value**: *E*ᵥ ≥ 20 on the one ledger, computed from the log by `tools/value.py`.
6. **Liveness continued**: C1b's process at or above 20 on the exit prefix.
7. No `decision` of kind `veto` with subject `C2a`; off-log repairs 0 on the acts evidence; A3.4 at or
   under 5 : 1.

**Reported, not gating:** the elections line — each entrant's weight on the window's events and whether any
entrant's weight is below the base-rate forecaster's (PLAN §4's "no witness yet" for elections is met by the
weights existing on the record; a criterion that an entrant must lose can be met by an entrant choosing to
lose, REVIEW-C2a-v1 F7, so it is reported, and what consumes the weights is C2b's election action).

## Pins (the reviewer's), each with its named mutant and passing twin
`worked_table` (the fixture file reproduced exactly; mutant: Laplace (s+1)/(n+2) → (s+1)/(n+3)) ·
`forecast_before_cutoff` (an entrant's probability is its first forecast with `ts` before the cutoff; mutant:
the latest) · `rigged` (a forecast at or after the cutoff is excluded — the recorded case 288–290 is the
witness, a forecast of the next unstarted window the twin; mutant: included) · `revision` (a principal's
second forecast of an event is excluded; mutant: it replaces the first) · `weights_from_resolved_prefix` (*q*
uses weights from events resolved before this one, in resolution order; mutant: terminal weights) ·
`abstention_is_base` (an absent entrant scores as *b* at the event's resolution, on a type whose *b* ≠ 1/2;
mutant: as 1/2) · `one_event_one_key` (two proposers on one key are one event, two keys two events, an
unkeyed forecast none; mutant: grouped by claim string) · `grouping_by_principal` (two keys of one principal
are one entrant; mutant: two) · `uniform_prior` (equal opening weights including the base; mutant: counsel
2×) · `no_learning_rate` (η = 1; mutant: η = ½, on a sequential fixture with unequal likelihoods) ·
`exact_probabilities` (*b*, *q* and the weights are `Fraction` through the path to *D*; mutant: one float
division) · `per_type_base` (base rate per type, never per args; mutant: per dataset) · `bounded_difference`
(|*D*| ≤ *B* by the per-mille clip; mutant: no clip, with a base rate of 1/1001 in the fixture) ·
`lambda_predictable` (*λᵢ* from the prior items and the two pseudo-items only; mutant: item *i* included) ·
`factor_algebra` (deterministic, no tolerance: on an enumerated binary tree with stated *b*, *q*, *λ* and
true probability *b*, the exact expectation of 1 + *λD*/*B* is at most 1 at every node, with adaptive
abstention; mutant: a factor 1 + *λD*/*B* + 1/50) · `window_from_the_push` (an event whose cutoff is at or
before the opening `ts`, or before the attack tests' first green, is excluded; mutant: from the brief's
merge) · `wealth_continues` (*E*ᵥ is not reset when a second window opens; mutant: reset to 1) ·
`promote_refused_value` (the verb signs nothing when *E*ᵥ < 20 with every other criterion met and verified;
mutant: signs).

## Refusal list
No LLM call in `tools/value.py`; no learning rate, prior or threshold chosen by hand (uniform prior and η = 1
are derived, 20 is the charter's α, *B* and *λ* are A4.4's); no event scored twice; no forecast at or after
its event's cutoff counts; no event outside the two streams' contracts counts; no change to C1's statistics
or the clerk; no kernel or kernel2 change; no trusted-base change but the opening push; no agent code; no
second push inside the window; no event chosen after its outcome is known (the streams, their datasets and
their meetings are named here, before).

## Stop and report if
the build does not fit under 7,800 (the shortfall in lines); the two checkers disagree; a stream's public
evidence disappears (the window continues on the other events; the report says so); the fixture cannot be
reproduced exactly (a defect in this brief's arithmetic, fixed by amendment before any event is scored).

## Deliverables
`tools/value.py` (events, entrants, the base rate, the mixture, the bet; `--table` prints the per-event rows,
the terminal weights and the diagnostic likelihood ratios; `--opening`, `--as-of`, `--no-attack-gate` for
the fixture); `tools/status.py` reading it for criteria 4–6 and the elections line, dispatching `C2a` beside
`C1a` and `C1b` with C1b's history kept and its liveness live, the opening identified by seq, V0's deadline
read once; `tools/jack decision` reading `promote C2a` exactly as it reads C1b's; `tests/test_value.py`;
the two simulator kinds; the pins; RUNBOOK `## jack value` (counsel's); counsel's V0–V3; the C2a report in
REPORT.md's form; the C2b brief text at exit. Every forecast a stream session enters carries `args.model`
(COUNSEL-OPEN 22): recorded now, consumed by C2b.

## Counsel's forecasts on this window (entered after the read, before the opening push)
| id | claim | p |
|---|---|---|
| V0 | the promotion forecast: every criterion holds on the exit prefix by V0's `resolves_by` (the opening + 14 d) | 0.35 |
| V1 | *E*ᵥ ≥ 20 within 7 days of the opening push | 0.25 |
| V2 | at the exit some entrant's weight on the window's events is below the base-rate forecaster's | 0.9 |
| V3 | no second push inside the window | 0.7 |

## Amendment 1 (1 November, counsel; the window's end when the push comes early)
The opening push is seq 367, `ts` 2026-11-01T15:04:14Z — two days before the date V0's `resolves_by`
(2026-11-17T12:00:00Z) was set against. §Order of acts says the window is "(opening `ts`, V0's
`resolves_by`], fourteen days at most"; the maximum governs. **C2a's window ends at the earlier of V0's
`resolves_by` and the opening `ts` + 14 days, i.e. 2026-11-15T15:04:14Z**, and `status.py` reads it so.
V0 itself is unchanged (a forecast is never edited): it resolves at the window's end, inside its own deadline.
Nothing else moves; no criterion, stream, constant or event rule is touched.
