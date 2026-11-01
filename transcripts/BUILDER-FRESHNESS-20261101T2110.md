# builder freshness stream 10

Window resolved: 2026-11-01T20:00:00Z to 2026-11-01T21:00:00Z.
Forecast window: 2026-11-01T23:00:00Z to 2026-11-02T00:00:00Z.

Reasoning

- `hk_property_poi`: current page is already at `2026-11-01T20:33:07+00:00`, and the record still treats this feed as hourly, so it should advance again by the target window.
- `hkex_disclosures`: current page is already at `2026-11-01T20:28:29+00:00`, and the hourly cadence has held across prior resolves, so it should advance again by the target window.
- `hkex_disclosure_interests`: current page is already at `2026-11-01T20:28:29+00:00`, and the hourly cadence has held across prior resolves, so it should advance again by the target window.
- `crhk_companies`: current page is at `2026-11-01T19:30:48+00:00`; the log has shown one daily advance per day for this feed, not hourly churn, so a second advance by 23:00Z is unlikely.
- `sfc_licences`: current page is still at `2026-10-31T04:32:32+00:00`, well outside the target window, so it should stay unchanged.
- `hk_property_transactions`: current page is still at `2026-11-01T11:27:34+00:00`, well outside the target window, so it should stay unchanged.

Forecast rows

- `hk_property_poi`: p=980, resolves_by=2026-11-02T02:00:00Z
- `hkex_disclosures`: p=980, resolves_by=2026-11-02T02:00:00Z
- `hkex_disclosure_interests`: p=980, resolves_by=2026-11-02T02:00:00Z
- `crhk_companies`: p=25, resolves_by=2026-11-02T02:00:00Z
- `sfc_licences`: p=15, resolves_by=2026-11-02T02:00:00Z
- `hk_property_transactions`: p=15, resolves_by=2026-11-02T02:00:00Z
