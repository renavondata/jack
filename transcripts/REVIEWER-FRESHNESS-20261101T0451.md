# Freshness stream 6 - due audit and three forecasts

Reviewer: `reviewer`, party `reviewer`, model `openai/gpt-5.4-mini`.
Branch: `ops-stream-6`; starting head `ops-stream-6`.
This note and the evidence are written and committed before the new forecast entries.

## Resolution audit

Clock checked at **2026-11-01T04:53:15Z** (12:53:15 HKT).
The open W1 freshness forecasts due now are the three `world.renavon` rows with
`args.stream == "freshness"` and `window_utc` ending at 04:00 UTC. All three
resolved cleanly: **3 resolved, 3 advanced**.

| Forecast seq | Dataset | Window UTC | resolves_by UTC | Outcome | Resolution UTC |
| --- | --- | --- | --- | ---: | --- |
| 272 | `hk_property_poi` | 03:00-04:00, 2026-11-01 | 2026-11-01T05:30:00Z | 1 | 2026-11-01T04:53:15Z |
| 273 | `hkex_disclosures` | 03:00-04:00, 2026-11-01 | 2026-11-01T05:30:00Z | 1 | 2026-11-01T04:53:15Z |
| 274 | `hkex_disclosure_interests` | 03:00-04:00, 2026-11-01 | 2026-11-01T05:30:00Z | 1 | 2026-11-01T04:53:15Z |

Observed `dateModified` instants were:

- `hk_property_poi`: `2026-11-01T03:43:47+00:00`.
- `hkex_disclosures`: `2026-11-01T03:29:45+00:00`.
- `hkex_disclosure_interests`: `2026-11-01T03:29:45+00:00`.

The machine-readable audit is
`transcripts/evidence/renavon-freshness-20261101T0451-resolve.json`.

## Forecast rule and reasoning, before the entries

The latest freshness forecasts still select `hk_property_poi`, `hkex_disclosures`,
and `hkex_disclosure_interests`. The catalogue and base-rate population remain
those in `transcripts/evidence/renavon-freshness-20261031-base.json`:
**48 datasets listed at 2026-10-31T23:01:26Z**, of which four had a page
last-updated instant in the preceding hour, giving **83 per mille** rounded.
That is a cross-sectional recency share, not a measured hourly transition rate.

The log now shows four consecutive hourly advances for each of the three selected
datasets. That is stronger cadence evidence than the prior snapshot, but still
not a guarantee of another hourly update.

- **`hk_property_poi`, p = 980:** four straight observed advances and the most
  recent timestamp is still close to the expected hourly cadence, so keep the
  probability very high without claiming certainty.
- **`hkex_disclosures`, p = 980:** the companion HKEX feed has matched the same
  hourly pattern and timestamp band, so the next hour stays highly likely.
- **`hkex_disclosure_interests`, p = 980:** it mirrors `hkex_disclosures` in
  both cadence and timestamp, so the same high but not absolute probability fits.

## Next-hour contract

Clock checked after H, so the next forecast hour is **2026-11-01 12 HKT**, or
**2026-11-01T04:00:00Z**.

- `hour_hkt`: `2026-11-01 12`.
- `window_utc`: `["2026-11-01T04:00:00Z", "2026-11-01T05:00:00Z"]`.
- `resolves_by`: **2026-11-01T06:30:00Z** (14:30 HKT; H + 2h30m).
- Same claim template, `world.renavon` type, and args keys as seqs 272-274;
  only the hour/window/deadline change, with p stated above.

| Dataset | p (per mille) | resolves_by UTC |
| --- | ---: | --- |
| `hk_property_poi` | 980 | 2026-11-01T06:30:00Z |
| `hkex_disclosures` | 980 | 2026-11-01T06:30:00Z |
| `hkex_disclosure_interests` | 980 | 2026-11-01T06:30:00Z |

Another principal must resolve these new reviewer forecasts as well.
