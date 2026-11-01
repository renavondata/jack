# builder freshness stream 8

Window resolved: 2026-11-01T17:00:00Z to 2026-11-01T18:00:00Z.
Forecast window: 2026-11-01T20:00:00Z to 2026-11-01T21:00:00Z.

Reasoning

- `hk_property_poi`: current page shows `dateModified` at 2026-11-01T17:33:00+00:00, which clears the window start, so this one advances.
- `hkex_disclosures`: current page shows `dateModified` at 2026-11-01T17:28:27+00:00, which clears the window start, so this one advances.
- `hkex_disclosure_interests`: current page shows `dateModified` at 2026-11-01T17:28:27+00:00, which clears the window start, so this one advances.
- `crhk_companies`: current page shows `dateModified` at 2026-11-01T16:27:31+00:00, which is still before the window start, so this one does not advance.
- `sfc_licences`: current page shows `dateModified` at 2026-10-31T04:32:32+00:00, far before the window start, so this one does not advance.
- `hk_property_transactions`: current page shows `dateModified` at 2026-11-01T11:27:34+00:00, still before the window start, so this one does not advance.

Forecast rows

- `hk_property_poi`: p=980, resolves_by=2026-11-01T20:00:00Z
- `hkex_disclosures`: p=980, resolves_by=2026-11-01T20:00:00Z
- `hkex_disclosure_interests`: p=980, resolves_by=2026-11-01T20:00:00Z
- `crhk_companies`: p=25, resolves_by=2026-11-01T20:00:00Z
- `sfc_licences`: p=15, resolves_by=2026-11-01T20:00:00Z
- `hk_property_transactions`: p=15, resolves_by=2026-11-01T20:00:00Z
