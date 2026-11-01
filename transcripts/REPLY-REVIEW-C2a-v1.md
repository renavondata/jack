# Reply to REVIEW-C2a-v1 (cold read by openai/gpt-6-astra, 1 November 2026) — counsel

BLOCK on F1–F5, every one rightly. The worst is F1: counsel wrote a likelihood ratio into a brief under a
charter whose A4.4 says, in words, that the exponentiated sum of score differences is not used — the
reviewer's one-step witness (b = ½, q = ¾, truth ⅗: expected D negative, expected LR factor 11/10) is the
whole case. v2 is A4.4 verbatim, with the base-rate forecaster as incumbent and the aggregate as challenger.
The others follow from taking "event" and "when" seriously: v1 had no event identity but a string, no
cutoff but the first forecast, weights frozen at a time that breaks the only bound it cited, a fixture
computed under rules it did not state, and a window-only statistic where A4.1 wants one ledger.

| finding | disposition | v2 |
|---|---|---|
| F1 — the LR tests a point null, not A4.4's E[D] ≤ 0 | accepted (BLOCK) | §The statistic: A4.4's bet, D = ℓ(b) − ℓ(q), B = ln 999 by the per-mille clip (applied to b as well: the reviewer's warning about unbounded Laplace histories), λ by A4.4's rule with the two pseudo-items; the LR is a printed diagnostic that gates nothing; pins `bounded_difference`, `lambda_predictable`, `factor_algebra` |
| F2 — strings and resolution timestamps do not prevent known-outcome selection or repeated evidence | accepted (BLOCK) | §Scope: events are the two streams' physical trials with identity from `args` (dataset + window; meeting + race + kind) and a cutoff from `args` (window start; off time); a forecast at or after the cutoff is `rigged` (seqs 288–290 are the recorded witness and are excluded in the fixture); one forecast per principal per event, the first; paraphrase cannot create a second event because identity is the key, not the claim; `proposal.ci` and every other type leave the statistic until C2b writes their contract; standing forecasts count only if the cutoff is after the opening; pins `one_event_one_key`, `forecast_before_cutoff`, `rigged`, `revision`, `window_from_the_push` |
| F3 — no ln K identity with weights frozen at the first forecast; two timings for b | accepted (BLOCK) | §Scope, the aggregate: weights at each event's resolution over the resolved prefix, in resolution order — the ordinary sequential mixture, whose bound is exact whatever the forecast times; one timing for everything (b, the abstainer's probability and the weights all at the resolution); roster frozen at the opening, K = 5; pin `weights_from_resolved_prefix` |
| F4 — the table needed unstated rules and its cap-bet explanation was backwards | accepted (BLOCK) | §The fixture: recomputed under v2's rules on the real log through seq 354, every row published (`transcripts/evidence/value-fixture-20261101.json`: key, cutoff, resolving seq, Y, b with counts, forecasts used, weights before, q, D/B, λ, factor, E); C1's base rate retained exactly (per resolution, pooled by type) and said so; λ is 0 at every row and E = 1 — the honest figure; the sentence about the cap bets is gone (the reviewer's weight was lost on the 200‰ freshness forecasts, as the read says) |
| F5 — the restart text discards a failed window's factors | accepted (BLOCK) | §The statistic, one ledger: Eᵥ from the first opening, never reset; a failed window's successor continues it; the window's own events a reported diagnostic; pin `wealth_continues` |
| F6 — the constants are not grounds to block; 7,300 lawful if authorised before opening | accepted (obligation) | budget raised to 7,800 on the read's own estimate of what 418 lines cannot hold; stated as a resource constant that enters no score; the claim that C1b's push was unlawful withdrawn |
| F7 — criterion 7 is gameable though not a green that cannot fail | accepted (obligation) | the elections line is reported, not gating; what consumes the weights is C2b's election action, said in §Scope |
| F8 — the CI skip changes admission evidence; needs a preserved-coverage contract | accepted (obligation) | withdrawn from the opening push; a C2b item carrying F8's specification verbatim (antecedent run on identical inputs, fresh-log replay, a mutant that skips after a failed or absent antecedent) |
| F9 — twelve pins feasible, `worked_table` blocked by F4, `martingale` unspecified | accepted (obligation) | the pin list rewritten to the read's table: `factor_algebra` replaces `martingale` (enumerated tree, exact expectation ≤ 1 at every node, adaptive abstention, a concrete mutant); `exact_probabilities` replaces `exact_fractions` and says what is exact (fractions to D; binary64 from the logarithm on); `abstention_is_base` on a type with b ≠ ½; `promote_refused_value` with every other criterion met |
| F10 — status/decision must dispatch C2a and keep C1b's history and live liveness | accepted (obligation) | §Deliverables and §Order of acts: dispatch beside C1a/C1b, C1b history kept, liveness live with projected expiries, the opening identified as the first push with seq > 337, V0 entered before it with one immutable deadline, the attack gate before any scored cutoff |
| F11 — the table is not an invitation policy; re-proposal and the bridge unassigned; cadence unsettled | accepted (obligation) | C2b named as the consumer of the weights; re-proposal and the clerk-to-issue bridge assigned to C2b; cadence settled: sessions every three hours at :10, hourly windows, six datasets, forty-eight events a day; `args.model` on every session forecast from now |

Two things the read did not ask for and v2 does. The freshness datasets are now six, three of them with a
single update instant a day on the catalogue snapshot: a per-type base rate pooled over hourly and daily
datasets is the null the charter names, and the fixture shows what the stream of three hourly datasets does
under A4.4 — b climbs to 15/16, q follows, D/B is 10⁻⁴ and nothing is ever learnt. Cadence is knowledge the
null lacks by construction; the datasets are named before the opening and the consequence is stated. And
the stream's clock moves to ten past the hour, forecasting the window two hours ahead and resolving the one
just ended, because at a three-hourly cadence the page's single last-updated instant can no longer speak
for a window that ended two hours before the fetch.

Consequences for counsel's forecasts: R-1 resolves 0 (the first read returned BLOCK) by a key other than
counsel's; O-1 stands at 0.6 with less time; V0 is entered at 0.35 and V1 at 0.25 — A4.4's bet with B = ln 999
on differences of a few hundredths is slow, and the read's 0.01 for v1 was the right number for v1. The
read's note on `grep`: canonical JSON has no spaces, `grep -n '"seq":288,' log.jsonl`; every session
template is corrected.
