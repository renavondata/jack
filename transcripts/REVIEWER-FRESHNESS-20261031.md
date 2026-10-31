# Freshness stream 1 — public evidence and three forecasts

Reviewer: `reviewer-2`, party `reviewer`, model `openai/gpt-6-astra`.
Branch: `ops-stream-1`; starting head `644b934` (`origin/main`).
This note and the evidence are written and committed before the forecast entries.

## Evidence and observable

Catalogue: <https://renavon.com/datasets>, fetched without authentication at
**2026-10-31T23:01:26Z**. Its 48 dataset cards enumerate 48 distinct dataset URLs,
matching the catalogue's stated count. All 48 pages returned HTTP 200 at their
dataset URLs, without login, between 23:01:40Z and 23:02:00Z. Paid downloads were
not accessed: a public description page can be evidence even when its dataset
download is paid.

Raw homepage, catalogue, and all dataset HTML pages are preserved under
`transcripts/evidence/renavon-freshness/20261031T230126Z/`.
Response statuses were checked before discarding headers that set anonymous
session cookies; no cookie jar or authentication was used.
The per-dataset URL, SHA-256, fetch time, literal timestamp, parsed UTC timestamp,
and visible refresh label are in
`transcripts/evidence/renavon-freshness-20261031-base.json`.

The precise observable is the **Dataset `dateModified` field embedded in each
public page's HTML**, which includes seconds and an explicit `+00:00` offset.
The visible “Last refreshed” label prints a date plus a rounded relative age;
that rounded age is not the parser's input. `last_updated` in the evidence JSON
preserves the raw `dateModified` string; `visible_last_refreshed` separately
preserves the displayed wording. These are public-page timestamps, not HTTP
response dates or sample rows' event times. All 48 pages supply this field, so
the no-hourly-evidence stop condition does not apply.

This is a single snapshot. It establishes recency, not a measured series of
hour-to-hour advances. The page timestamp is the specified public proxy for new
rows; these observations do not independently establish pipeline internals.

## Cross-sectional base rate and selection

Population: **48 datasets listed at 2026-10-31T23:01:26Z**.
Four have a last-updated instant within the preceding hour
`[2026-10-31T22:01:26Z, 2026-10-31T23:01:26Z]`:
`crhk_documents`, `hkex_disclosures`, `hkex_disclosure_interests`, and
`hk_property_poi`. The same four qualify against their individual fetch times.
Thus **4/48 = 8.333…% = 83.333…‰**, rounded to **83‰**. This is explicitly a
cross-sectional recency share, not an empirical next-hour transition rate.
It is neither 0 nor 1000, so the 500‰ fallback is not used.
`icac_wanted_persons` at 22:01:24Z misses the catalogue-time threshold by two
seconds; rounding “1 hour ago” into a qualifying instant would be wrong.

The three most recent are:

| Dataset | Last updated UTC | Age at its fetch |
| --- | --- | --- |
| `hk_property_poi` | 2026-10-31T22:35:42Z | 26m 15s |
| `hkex_disclosures` | 2026-10-31T22:30:29Z | 31m 20s |
| `hkex_disclosure_interests` | 2026-10-31T22:30:29Z | 31m 20s |

The second and third tie and both fit in the selection, so no cadence-based
tie-break excludes another dataset. The HKEX pages describe companion datasets
and share their timestamp: their outcomes should not be treated as independent.

## Rule and reasoning, stated before the entries

Start at 83‰ and add a discretionary **117‰ recency premium**, giving **200‰**
for each selected dataset. All three show an update in the last completed UTC
hour, 22:00–23:00 (06:00–07:00 HKT), rather than only an older update. This makes
them more plausible repeat updaters than a randomly selected catalogue member.
The premium is judgment, not a fitted or calibrated cadence estimate. One
timestamp does not show repeated hourly capture; retain substantial probability
of no advance rather than treating a recent refresh as proof of hourly delivery.

- **`hk_property_poi`, 200‰:** 22:35:42Z lies in the hour immediately before the fetch and is the newest catalogue timestamp; raise 83‰ by 117‰ for that observed activity, but its amenities description supplies no measured hourly cadence to justify a larger increase.
- **`hkex_disclosures`, 200‰:** 22:30:29Z also lies in the preceding hour; raise 83‰ by 117‰ for this recent refresh, while a single filing-data snapshot does not show that the next Sunday-morning run will find new rows.
- **`hkex_disclosure_interests`, 200‰:** the same preceding-hour 22:30:29Z refresh warrants the same 117‰ uplift; its stated companion relationship to disclosures and identical timestamp support the same probability, not a separate claim of independent hourly activity.

## Forecast window and resolution

Clock checked at **2026-10-31T23:02:19Z** (2026-11-01 07:02:19 HKT).
Now plus ten minutes is 07:12:19 HKT; the next hour boundary is therefore
**H = 2026-11-01 08 HKT = 2026-11-01T00:00:00Z**.

- Window: `[2026-11-01T00:00:00Z, 2026-11-01T01:00:00Z)` (08:00–09:00 HKT).
- Fetch resolution evidence after **2026-11-01T01:00:00Z**.
- Resolve by **2026-11-01T02:30:00Z** (10:30 HKT), H + 2h30m.
- Each entry uses type `world.renavon`, stream `freshness`, the exact dataset
  URL below, base rate 83‰, and the population stated above.

| Dataset | Public URL | p (‰) | resolves_by (UTC) |
| --- | --- | ---: | --- |
| `hk_property_poi` | https://renavon.com/data/property/hk_property_poi | 200 | 2026-11-01T02:30:00Z |
| `hkex_disclosures` | https://renavon.com/data/hkex/hkex_disclosures | 200 | 2026-11-01T02:30:00Z |
| `hkex_disclosure_interests` | https://renavon.com/data/hkex/hkex_disclosure_interests | 200 | 2026-11-01T02:30:00Z |

The claim in each entry is the requested public-page threshold: fetched after
01:00Z, the page shows a last-updated instant at or after 00:00Z. Preserve the
same page's raw HTML, fetch time and SHA-256 under
`transcripts/evidence/renavon-freshness/` for resolution, using its Dataset
`dateModified` field. Fetch as soon after the window as practical: the supplied
claim has no upper bound on the displayed instant, so a later update could
satisfy that literal threshold without identifying which hourly run delivered
the rows. The `window_utc` records the intended hour; it does not silently
change the supplied claim. Resolution must be entered by another principal.
