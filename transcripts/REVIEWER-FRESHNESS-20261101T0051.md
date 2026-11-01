# Freshness stream 2 — due audit and three forecasts

Reviewer: `reviewer-2`, party `reviewer`, model `openai/gpt-6-astra`.
Branch: `ops-stream-2`; starting head and fetched `origin/main`:
`2557dc00f93bd8542b3c7a9004a2ad3b2ebad0e7` (log through seq 255).
This note and the audit are written and committed before the new forecast entries.

## Resolution audit

Clock checked at **2026-11-01T00:51:34Z** (08:51:34 HKT).
The complete log has three forecasts of type `world.renavon` with stream
`freshness`, and no resolutions of those forecasts. None has a window end in
the past. The due list is therefore **empty**: **0 resolved, 0 advanced**.
These counts are not observations of failure to advance.

| Forecast seq | Dataset | Window UTC | resolves_by UTC | Disposition |
| --- | --- | --- | --- | --- |
| 251 | `hk_property_poi` | 00:00–01:00, 2026-11-01 | 2026-11-01T02:30:00Z | Not due; own principal |
| 252 | `hkex_disclosures` | 00:00–01:00, 2026-11-01 | 2026-11-01T02:30:00Z | Not due; own principal |
| 253 | `hkex_disclosure_interests` | 00:00–01:00, 2026-11-01 | 2026-11-01T02:30:00Z | Not due; own principal |

All three were proposed by `reviewer`; resolving them with this key would be
`self_judged`. They are skipped and require another principal to fetch evidence
after 01:00 UTC and resolve by 02:30 UTC. No resolution entry or resolution UTC
time exists for this session. With no due forecast, no resolution-page fetch
was made and no last-updated value, hash, or outcome is asserted.

The machine-readable audit is
`transcripts/evidence/renavon-freshness-20261101T0051-resolve.json`.

## Forecast rule and reasoning, before the entries

The latest freshness forecasts select `hk_property_poi`, `hkex_disclosures`,
and `hkex_disclosure_interests`. The catalogue and base-rate population remain
those in `transcripts/evidence/renavon-freshness-20261031-base.json`:
**48 datasets listed at 2026-10-31T23:01:26Z**, of which four had a page
last-updated instant in the preceding hour, giving **83 per mille** rounded.
That is a cross-sectional recency share, not a measured hourly transition rate.

There are **zero resolved freshness outcomes** in the log from which to update
dataset cadence. I retain **200 per mille (20%)** for each dataset: the 83 per
mille reference plus a discretionary 117 per mille premium for the activity
observed in the base snapshot. This is a judgmental prior carried forward, not
an empirical estimate of hourly delivery. The intervening unresolved forecasts
provide no positive or negative outcome evidence.

- **`hk_property_poi`, p = 200:** its base-snapshot update at 2026-10-31T22:35:42Z was the newest catalogue timestamp; retain a modest activity premium, with no resolved cadence evidence to justify increasing it for the next Sunday-morning hour.
- **`hkex_disclosures`, p = 200:** its base-snapshot update at 2026-10-31T22:30:29Z supports activity above the catalogue reference, but no resolved outcome establishes repeated hourly filing delivery, so retain 20%.
- **`hkex_disclosure_interests`, p = 200:** its same 2026-10-31T22:30:29Z timestamp and companion relationship to disclosures support the same 20% prior; their correlated observations are not independent cadence evidence.

## Next-hour contract

At the checked clock, now + 5 minutes is **08:56:34 HKT**. The first hour
boundary at or after that is **H = 2026-11-01 09 HKT**, or 01:00 UTC.

- `hour_hkt`: `2026-11-01 09`.
- `window_utc`: `["2026-11-01T01:00:00Z", "2026-11-01T02:00:00Z"]`.
- `resolves_by`: **2026-11-01T03:30:00Z** (11:30 HKT; H + 2h30m).
- Same claim template, `world.renavon` type, and args keys as seqs 251–253;
  only the hour/window/deadline change, with p stated above.
- Resolution observable: the literal Dataset `dateModified` instant printed
  in the public HTML, parsed with its explicit timezone, rather than rounded
  visible relative age. Fetch after 02:00 UTC; outcome 1 iff the instant is at
  or after 01:00 UTC, as the supplied threshold claim says. Missing timestamps
  or failed fetches do not support a resolution.

| Dataset | p (per mille) | resolves_by UTC |
| --- | ---: | --- |
| `hk_property_poi` | 200 | 2026-11-01T03:30:00Z |
| `hkex_disclosures` | 200 | 2026-11-01T03:30:00Z |
| `hkex_disclosure_interests` | 200 | 2026-11-01T03:30:00Z |

Another principal must resolve these new reviewer forecasts as well.
