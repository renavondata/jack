# Freshness Stream 11

- hk_property_poi: hourly cadence still holds; the live page is fresh within the last hour, so I keep this near-certain for the 02:00Z window.
- hkex_disclosures: hourly cadence still holds and the page is fresh within the last hour, so I keep this near-certain for the 02:00Z window.
- hkex_disclosure_interests: same hourly cadence and same last-hour freshness, so I keep this near-certain for the 02:00Z window.
- crhk_companies: the record shows a daily cadence around the late-evening update, so the 02:00Z window is unlikely to catch a new row.
- sfc_licences: the record shows a daily cadence around 04:32Z, which sits after the 02:00Z window, so I rate this low.
- hk_property_transactions: the record shows a daily cadence around 11:28Z, which sits after the 02:00Z window, so I rate this low.

Planned forecasts:

- hk_property_poi | p=980 | resolves_by=2026-11-02T05:00:00Z
- hkex_disclosures | p=980 | resolves_by=2026-11-02T05:00:00Z
- hkex_disclosure_interests | p=980 | resolves_by=2026-11-02T05:00:00Z
- crhk_companies | p=25 | resolves_by=2026-11-02T05:00:00Z
- sfc_licences | p=15 | resolves_by=2026-11-02T05:00:00Z
- hk_property_transactions | p=15 | resolves_by=2026-11-02T05:00:00Z
