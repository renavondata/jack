# The closing market against hkjc.guru's model, under A4 clause 4 (28 October 2026)

Counsel's evidence for the `world.hkjc` type and for the base rates of its first forecasts. Read-only
over one committed artifact of `renavondata/renavon-monorepo`: `apps/hkjcguru/data/model/artifacts/
backtest_ratings.parquet` at monorepo commit `439058a`, the out-of-sample, walk-forward-by-season
ratings of hkjc.guru's LightGBM model (`win_prob`), its market blend (`win_prob_blend`), the final
WIN odds (`odds`) and the result (`won`) for every runner in 5,877 races from 2019-09-01 to
2026-07-15. Nothing was trained, fitted or tuned here; the artifact is the model's own report of
itself. The script is at the end and reproduces every figure.

## Question
Is any of the three forecasters an improvement on the closing market, under the test the charter
now uses for exactly this question — A4 clause 4, the bet on a bounded difference of log losses,
promotion at *E* ≥ 20 (§6, α = 0.05)?

## Method, as A4 clause 4 states it
Items are races in date order (5,855 of the 5,877: those with one winner and all three
probabilities present). The market's probability for a runner is 1/odds normalised within the race.
A forecaster's loss on a race is −ln of the probability it gave the winner, clipped to per mille
([0.001, 0.999]); B = ln 999. Dᵢ = incumbent's loss − challenger's loss;
*E* = ∏(1 + λᵢ Dᵢ / B), λᵢ = min(max(0, m₁ᵢ / m₂ᵢ), 1 − 1/(nᵢ + 2)), with m₁ᵢ and m₂ᵢ the mean of Dⱼ/B
and (Dⱼ/B)² over the prior items plus two pseudo-items at +B and −B. Under E[Dᵢ | past] ≤ 0 the
process is a test supermartingale; Ville's inequality gives P(sup E ≥ 20) ≤ 0.05.

## Result

| per race, mean log loss (nats) | |
|---|---:|
| uniform (1/n) | 2.4871 |
| hkjc.guru model (`win_prob`) | 2.1571 |
| closing market (1/odds normalised) | 2.0081 |
| blend (`win_prob_blend`) | 2.0061 |

| incumbent → challenger | mean D | E after 5,855 races | max E | first E ≥ 20 |
|---|---:|---:|---:|---:|
| market → blend | +0.0021 | 1.6 | 2.17 | never |
| market → model | −0.1490 | 0.99 | 1.00 | never |
| blend → market | −0.0021 | 0.99 | 1.01 | never |
| **model → market** | +0.1490 | 3.8 × 10⁴⁷ | 3.9 × 10⁴⁷ | **race 343** |
| uniform → market | +0.4790 | 2.3 × 10¹⁵³ | 2.6 × 10¹⁵³ | race 66 |
| model → blend | +0.1510 | 1.8 × 10⁴⁷ | 2.0 × 10⁴⁷ | race 353 |

Read: the market would displace the model as incumbent within 343 races, about four months of
racing. The blend's 0.002 nats per race over the market, after seven seasons, has not moved the
wealth past 2.2; under the charter the market stays incumbent and the blend is an unpromoted
challenger. The blend's year-by-year mean D (market − blend) is −0.0011, +0.0008, +0.0014, +0.0015,
+0.0027, +0.0029, +0.0059, −0.0005 for 2019 to 2026: small, mostly positive, and not enough.

The money reads the same way. Over the model's value-flagged bets (edge = win_prob × odds ≥ 1.15,
the rule hkjc.guru publishes with), the report's own flat return is −30 % over 12,028 bets at mean
odds 21; by meeting, a positive flat return occurred at 168 of 615 meetings (0.273), and at 37 of
176 (0.210) over the last two seasons.

## Base rates for the first `world.hkjc` forecasts (615 meetings, 2019–2026; last two seasons, 176, in brackets)

| claim, per meeting | rate |
|---|---:|
| favourite wins at least 3 races | 0.593 (0.608) |
| favourite wins at least 4 races | 0.327 (0.352) |
| model's top-ranked runner (by `win_prob`) wins at least 3 races | 0.460 (0.489) |
| at least one winner at final WIN odds ≥ 20 | 0.585 |
| hkjc.guru's value picks show a positive settled flat return | 0.273 (0.210) |

Favourite strike rate per race 0.305; model top pick 0.257; blend top pick 0.304. Meetings have
8 to 11 races (one of 6); 9 and 10 are the modes.

Counsel's first forecasts (same branch) are entered at these base rates, as the reference-class
default LITERATURE-20261026 item 10 prescribes when the forecaster has no card in hand: counsel had
no race card, no fixture list and no odds when it entered them. A forecaster who has those should
beat these numbers, and the ledger will say whether it does.

## Caveats
- The incumbent here is the *closing* market (final SP). hkjc.guru blends at the overnight
  checkpoint and bets into a pari-mutuel pool that settles at the final dividend, so the closing
  market is the right incumbent for the money question and the hardest one for the forecasting
  question.
- The backtest is the model's own artifact; this file trusts its walk-forward discipline and checks
  nothing about leakage. A live comparison on the ledger is the remedy, not a re-audit.
- Per-mille clipping binds on no row here (all probabilities lie inside [0.001, 0.999]); B is the
  charter's constant, not a fitted one.

## Script (Python 3, duckdb; run from `apps/hkjcguru` of the monorepo at 439058a)
```python
import duckdb, math
con = duckdb.connect()
rows = con.sql("""
with r as (select race_id, race_date, horse_id, win_prob, win_prob_blend, odds, won
           from 'data/model/artifacts/backtest_ratings.parquet'
           where odds is not null and odds > 0 and win_prob is not null and win_prob_blend is not null),
m as (select *, (1.0/odds)/sum(1.0/odds) over (partition by race_id) as p_mkt,
             count(*) over (partition by race_id) as n, sum(won) over (partition by race_id) as nw from r)
select race_id, race_date, p_mkt, win_prob, win_prob_blend, n from m where won = 1 and nw = 1
order by race_date, race_id""").fetchall()
B = math.log(999)
clip = lambda p: min(max(p, 1e-3), 1 - 1e-3)
def eproc(D):
    s1, s2, n, E, Emax, first = 0.0, 2.0, 2, 1.0, 1.0, None
    for i, d in enumerate(D):
        x = d / B; m1, m2 = s1 / n, s2 / n
        lam = min(max(0.0, m1 / m2), 1 - 1 / (n + 2))
        E *= 1 + lam * x
        if E >= 20 and first is None: first = i + 1
        Emax = max(Emax, E); s1 += x; s2 += x * x; n += 1
    return E, Emax, first
L = {'market': [-math.log(clip(r[2])) for r in rows], 'model': [-math.log(clip(r[3])) for r in rows],
     'blend': [-math.log(clip(r[4])) for r in rows], 'uniform': [math.log(r[5]) for r in rows]}
for k, v in L.items(): print(k, round(sum(v) / len(v), 4))
for inc, ch in [('market','blend'), ('market','model'), ('blend','market'), ('model','market'),
                ('uniform','market'), ('model','blend')]:
    D = [a - b for a, b in zip(L[inc], L[ch])]
    print(inc, '->', ch, round(sum(D) / len(D), 5), *eproc(D))
```
Base rates: group the same parquet by (race_date, first two characters of race_id) for meetings;
favourite = `arg_min(horse_id, odds)` per race, top pick = `arg_max(horse_id, win_prob)`; value
picks are the rows with `value_flag`, flat return per row `won * odds − 1`.

## Addendum, 28 October (after the reviewer's findings)
At the ledger's advised stakes (3 units at edge ≥ 1.50, 2 at ≥ 1.30, 1 at ≥ 1.15, edge = win_prob × odds),
a meeting's settled return is positive at 154 of 615 meetings (0.250), 33 of 176 over the last two seasons
(0.188); the flat (one unit) and advised signs disagree at 36 of 615 (0.059). The reading recorded in
`world-types.md` applies the advised-stake figure to the claims as entered.
