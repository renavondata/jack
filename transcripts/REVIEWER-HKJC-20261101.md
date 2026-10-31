# M2: the 1 November 2026 card and ten per-race forecasts

Reviewer (`reviewer-2`), branch `review-m2-races`. Written before entering any of
these forecasts. Read `HKJC-EPROCESS-20261028.md`, the family's forecasts in
`REVIEWER-HKJC-20261028.md` (M2 seqs 87–90), and RUNBOOK's forecast verb first.

## Card and custody

M2 is **Sunday 1 November 2026, Happy Valley, Turf, C+3, Good as published**,
ten races. First off is **12:45 HKT = 2026-11-01T04:45:00Z**.
The machine-readable card and complete URL/SHA-256/fetch-time manifest are in
[`evidence/hkjc-20261101-card.json`](evidence/hkjc-20261101-card.json).
Raw response bodies are in `evidence/hkjc-20261101/`, saved directly with
`curl -sL --max-time 90 URL -o FILE`. Fetches ran from
`2026-10-31T17:11:58Z` through `2026-10-31T17:13:57Z`, well before first off.

The hkjc.guru meeting page and all ten race pages carry off times; their
SportsEvent timestamps agree with HKJC's official race cards. HKJC's cards
were also necessary to correct the **starter/standby distinction**: guru's
14-entry counts (13 in R8) include number-0 standby horses. The official
`racecardlist` has **12 starters in R1–6 and R8–10, 10 in R7**; `standbylist`
is separate. Counts are the fetched declarations, subject to later withdrawals.

The two home-page attempts returned Cloudflare challenges and are retained,
hashed and labelled. Direct meeting/race URLs worked. The saved M2 cards have
no WIN market quotes. R1's model **Rated price** is not a WIN quote, so neither
it nor the unpublished R2–10 model boards supplies a market-shape adjustment.

## Measured favourite strike rate

I fetched every race page linked from six Happy Valley meeting pages in the
2026–27 season: 9, 16 and 23 September; 7, 14 and 21 October 2026. These are
**52 completed races, with 12 favourite wins: 12/52 = 23.0769%, rounded to
231 per mille**. This is a recent six-meeting sample, not the seven-season
population reported by counsel or the 2,344-race population used on 28 October.
Those older numbers have not been re-measured here.

| Meeting | Races counted | Favourite wins | Races won by a favourite |
|---|---:|---:|---|
| 2026-09-09 | 8 | 2 | 4, 7 |
| 2026-09-16 | 8 | 4 | 4, 5, 6, 8 |
| 2026-09-23 | 9 | 1 | 8 |
| 2026-10-07 | 9 | 1 | 9 |
| 2026-10-14 | 9 | 2 | 2, 8 |
| 2026-10-21 | 9 | 2 | 1, 4 |
| **Total** | **52** | **12** | |

Reproduction rule: for each `guru-history-*r[0-9]*.html`, read the completed
race's results table (`Pos`, `No.`, …, `Odds`, `Margin`), find the minimum
positive numeric Odds among starters, and record 1 if any horse at that minimum
finished first, otherwise 0. Count a dead-heating first as a win. Withdrawn
horses with no odds do not enter the field-size denominator. Every numbered
finisher in this sample has numeric odds; every race has one first-place row.
The two tied-minimum races (9 September R6 and 14 October R9) both lost, so
co-favourite handling does not change the measured numerator. For the new
claims, a win by any joint shortest-price runner counts as a favourite win.

Each constituent page has its own URL and hash in the JSON; its singular
`source_url`/`source_sha256` fields identify the first constituent, with the
full source-set rule explicitly supplied. The official HKJC 21 October R1
results/dividends page provides a spot-check: #6 ACE won at 2.9, the shortest
WIN odds. The official all-results page is retained too, but is not a substitute
for the all-runner odds tables used for the calculation.

## Forecast rule and ten pre-entry probabilities

The base rate in every entry is **231**. I give the measured exact-field-size
subgroup only 20% weight and the overall rate 80%, rounding to the nearest
per mille: **p = round(0.8 × 1000 × 12/52 + 0.2 × subgroup rate)**.
This is my conservative, judgmental shrinkage weight, not a fitted or validated
coefficient. The subgroup observations overlap the overall sample.

The 12-starter subgroup has **7/40 = 175 per mille**, giving **220**;
the 10-starter subgroup has **2/8 = 250 per mille**, giving **235**.
For completeness, the other fields are 9 starters: 0/1, and 11: 3/3.
The small recent sample and day-meeting versus historical evening-meeting
difference limit transfer. I make no separately estimated class, distance,
going or C+3 adjustment; those card details identify each reference-class
application below. I do not infer ten independent outcomes from these numbers
or revise the already-entered meeting-level M2 forecasts.

All times below are on **2026-11-01**. Each deadline is off + two hours.

| Race | Off HKT | off_utc | Runners | p (per mille) | resolves_by (UTC) | One-line justification |
|---|---|---|---:|---:|---|---|
| 1 | 12:45 | 2026-11-01T04:45:00Z | 12 | 220 | 2026-11-01T06:45:00Z | Class 5, 1200m C+3: 12 declared starters select the 7/40 field-size rate, shrunk 80% toward 12/52. |
| 2 | 13:15 | 2026-11-01T05:15:00Z | 12 | 220 | 2026-11-01T07:15:00Z | Class 4, 1650m C+3: the full 12-runner field selects the same 7/40 subgroup and 220 forecast. |
| 3 | 13:45 | 2026-11-01T05:45:00Z | 12 | 220 | 2026-11-01T07:45:00Z | Class 4, 1200m C+3: 12 starters justify the modest field-size reduction from 231 to 220. |
| 4 | 14:15 | 2026-11-01T06:15:00Z | 12 | 220 | 2026-11-01T08:15:00Z | Class 4, 1000m C+3: use the measured 12-runner subgroup at 20% weight, without an unmeasured sprint adjustment. |
| 5 | 15:10 | 2026-11-01T07:10:00Z | 12 | 220 | 2026-11-01T09:10:00Z | Class 4, 1200m C+3: 12 starters again select 175 per mille before shrinkage, hence 220. |
| 6 | 15:40 | 2026-11-01T07:40:00Z | 12 | 220 | 2026-11-01T09:40:00Z | Class 4, 1800m C+3: retain the 12-runner adjustment only; the fetched evidence does not calibrate a staying-distance effect. |
| 7 | 16:10 | 2026-11-01T08:10:00Z | 10 | 235 | 2026-11-01T10:10:00Z | Class 2, 1200m C+3: the smaller 10-runner field selects 2/8 = 250 per mille, shrunk to 235. |
| 8 | 16:40 | 2026-11-01T08:40:00Z | 12 | 220 | 2026-11-01T10:40:00Z | Class 3, 1000m C+3: HKJC's 12 starters, excluding guru's extra standby, select the 220 field-size forecast. |
| 9 | 17:15 | 2026-11-01T09:15:00Z | 12 | 220 | 2026-11-01T11:15:00Z | Class 3, 1650m C+3: use the same 12-runner history and 80/20 shrinkage, giving 220. |
| 10 | 17:50 | 2026-11-01T09:50:00Z | 12 | 220 | 2026-11-01T11:50:00Z | Class 3, 1200m C+3: 12 declared starters select 7/40, shrunk toward 12/52 to give 220. |

## Entry and resolution

Each entry uses the requested claim verbatim with its race number:

> At the HKJC meeting of 2026-11-01 (HKT), race &lt;r&gt;: the runner with the shortest final WIN odds wins (a dead-heat involving it counts as a win; a race not run, or run without a WIN market, resolves 0)

Type is `world.hkjc`, incumbent is `the closing WIN market`, and evidence is
`transcripts/evidence/hkjc-20261101-card.json`. Resolution evidence is the HKJC
results and dividends page for the race, to be saved and hashed under
`transcripts/evidence/hkjc-20261101/` after racing; today's future results have
not been fetched or claimed. A different principal must resolve these entries.

The work commit comes before the forecast verbs because RUNBOOK requires a
clean tree; this table therefore precedes all ten signed entries. Before each
entry, check the clock against both first off and its deadline. The subsequent
proposal pushes the evidence and signed forecasts together.
