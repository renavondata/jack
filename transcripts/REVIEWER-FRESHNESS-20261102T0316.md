# Freshness Stream 13

- hk_property_poi: hourly cadence and the page's recent recency keep the 05:00Z-06:00Z window very likely to advance.
- hkex_disclosures: same hourly cadence and the same fresh timestamp band, so keep this very likely to advance.
- hkex_disclosure_interests: same hourly cadence and the same fresh timestamp band as hkex_disclosures, so keep this very likely to advance.
- crhk_companies: daily cadence around 20:28Z sits well away from the 05:00Z-06:00Z window, so this is low.
- sfc_licences: daily cadence around 04:32Z lands just before the window start, so the window is unlikely to catch a new update.
- hk_property_transactions: daily cadence around 11:28Z is far outside the window, so this is low.

Planned forecasts:

- hk_property_poi | p=980 | resolves_by=2026-11-02T08:00:00Z
- hkex_disclosures | p=980 | resolves_by=2026-11-02T08:00:00Z
- hkex_disclosure_interests | p=980 | resolves_by=2026-11-02T08:00:00Z
- crhk_companies | p=25 | resolves_by=2026-11-02T08:00:00Z
- sfc_licences | p=15 | resolves_by=2026-11-02T08:00:00Z
- hk_property_transactions | p=15 | resolves_by=2026-11-02T08:00:00Z
