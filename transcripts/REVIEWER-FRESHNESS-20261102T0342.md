# Freshness Stream 15

- hk_property_poi: the log still shows repeated sub-daily refreshes, and the latest 02:48Z hit makes the 05:00Z window look near-certain.
- hkex_disclosures: the same repeated refresh pattern and the latest 02:40Z hit make the 05:00Z window look near-certain.
- hkex_disclosure_interests: the same repeated refresh pattern and the latest 02:40Z hit make the 05:00Z window look near-certain.
- crhk_companies: the log now shows irregular but frequent updates around 20:27Z, 22:28Z, and 01:28Z, so the 05:00Z window is plausible but not sure.
- sfc_licences: the latest page is still anchored at 2026-10-31T04:32:32Z, so the 05:00Z window still looks unlikely.
- hk_property_transactions: repeated sub-daily updates at 23:28Z and 02:40Z make another hit by 05:00Z likely.

Planned forecasts:

- hk_property_poi | p=980 | resolves_by=2026-11-02T08:00:00Z
- hkex_disclosures | p=980 | resolves_by=2026-11-02T08:00:00Z
- hkex_disclosure_interests | p=980 | resolves_by=2026-11-02T08:00:00Z
- crhk_companies | p=360 | resolves_by=2026-11-02T08:00:00Z
- sfc_licences | p=15 | resolves_by=2026-11-02T08:00:00Z
- hk_property_transactions | p=940 | resolves_by=2026-11-02T08:00:00Z
