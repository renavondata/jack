# Freshness stream 5 — due audit and three forecasts

Reviewer: `reviewer`, party `reviewer`, model `openai/gpt-5.4-mini`.
Branch: `ops-stream-5`; starting head `dc08a0e`.
This note and the evidence are written and committed before the new forecast entries.

## Resolution audit

Clock checked at **2026-11-01T03:48:15Z** (11:48:15 HKT).
The open W1 freshness forecasts due now are the three `world.renavon` rows with
`args.stream == "freshness"` and `window_utc` ending at 03:00 UTC. All three
resolved cleanly: **3 resolved, 3 advanced**.

| Forecast seq | Dataset | Window UTC | resolves_by UTC | Outcome | Resolution UTC |
| --- | --- | --- | --- | ---: | --- |
| 264 | `hk_property_poi` | 02:00–03:00, 2026-11-01 | 2026-11-01T04:30:00Z | 1 | 2026-11-01T03:48:15Z |
| 265 | `hkex_disclosures` | 02:00–03:00, 2026-11-01 | 2026-11-01T04:30:00Z | 1 | 2026-11-01T03:48:15Z |
| 266 | `hkex_disclosure_interests` | 02:00–03:00, 2026-11-01 | 2026-11-01T04:30:00Z | 1 | 2026-11-01T03:48:15Z |

Observed `dateModified` instants were:

- `hk_property_poi`: `2026-11-01T02:37:30+00:00`.
- `hkex_disclosures`: `2026-11-01T02:30:11+00:00`.
- `hkex_disclosure_interests`: `2026-11-01T02:30:11+00:00`.

The machine-readable audit is
`transcripts/evidence/renavon-freshness-20261101T0347-resolve.json`.

## Forecast rule and reasoning, before the entries

The latest freshness forecasts still select `hk_property_poi`, `hkex_disclosures`,
and `hkex_disclosure_interests`. The catalogue and base-rate population remain
those in `transcripts/evidence/renavon-freshness-20261031-base.json`:
**48 datasets listed at 2026-10-31T23:01:26Z**, of which four had a page
last-updated instant in the preceding hour, giving **83 per mille** rounded.
That is a cross-sectional recency share, not a measured hourly transition rate.

The log now shows three consecutive hourly advances for each of the three
selected datasets. That is stronger cadence evidence than the prior snapshot,
but still not a guarantee of another hourly update.

- **`hk_property_poi`, p = 970:** it has advanced in each observed hour and its
  newest observed timestamp stays near the expected hourly cadence, so keep the
 probability very high without claiming certainty.
- **`hkex_disclosures`, p = 970:** the companion HKEX feed has matched the same
 hourly pattern and timestamp band, so the next hour stays highly likely.
- **`hkex_disclosure_interests`, p = 970:** it mirrors `hkex_disclosures` in
 both cadence and timestamp, so the same high but not absolute probability fits.

## Next-hour contract

Clock checked before H, so the next forecast hour is still **H = 2026-11-01 12 HKT**,
or **2026-11-01T04:00:00Z**.

- `hour_hkt`: `2026-11-01 12`.
- `window_utc`: `["2026-11-01T04:00:00Z", "2026-11-01T05:00:00Z"]`.
- `resolves_by`: **2026-11-01T06:30:00Z** (14:30 HKT; H + 2h30m).
- Same claim template, `world.renavon` type, and args keys as seqs 272–274;
  only the hour/window/deadline change, with p stated above.

| Dataset | p (per mille) | resolves_by UTC |
| --- | ---: | --- |
| `hk_property_poi` | 970 | 2026-11-01T06:30:00Z |
| `hkex_disclosures` | 970 | 2026-11-01T06:30:00Z |
| `hkex_disclosure_interests` | 970 | 2026-11-01T06:30:00Z |

Another principal must resolve these new reviewer forecasts as well.
