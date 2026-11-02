# builder freshness stream 12

Window resolved: 2026-11-01T23:00:00Z to 2026-11-02T00:00:00Z.
Forecast window: 2026-11-02T02:00:00Z to 2026-11-02T03:00:00Z.

Reasoning

- `hk_property_poi`: current page shows `2026-11-01T23:33:48+00:00`; it has held the hourly cadence in the record, so another advance by 03:00Z is likely.
- `hkex_disclosures`: current page shows `2026-11-01T23:28:56+00:00`; it has held the hourly cadence in the record, so another advance by 03:00Z is likely.
- `hkex_disclosure_interests`: current page shows `2026-11-01T23:28:56+00:00`; it has held the hourly cadence in the record, so another advance by 03:00Z is likely.
- `crhk_companies`: current page shows `2026-11-01T22:28:17+00:00`; it has behaved like a once-daily feed in the record, so another advance by 03:00Z is unlikely.
- `sfc_licences`: current page shows `2026-10-31T04:32:32+00:00`; it has behaved like a once-daily feed in the record, so another advance by 03:00Z is unlikely.
- `hk_property_transactions`: current page shows `2026-11-01T23:28:47+00:00`; it has behaved like a once-daily feed in the record, so another advance by 03:00Z is unlikely.

Skipped builder-owned due forecasts: 264-266, 272-274, 412-417.

Forecast rows

- `hk_property_poi`: p=980, resolves_by=2026-11-02T05:00:00Z
- `hkex_disclosures`: p=980, resolves_by=2026-11-02T05:00:00Z
- `hkex_disclosure_interests`: p=980, resolves_by=2026-11-02T05:00:00Z
- `crhk_companies`: p=25, resolves_by=2026-11-02T05:00:00Z
- `sfc_licences`: p=15, resolves_by=2026-11-02T05:00:00Z
- `hk_property_transactions`: p=15, resolves_by=2026-11-02T05:00:00Z
