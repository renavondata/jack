# Freshness Stream 126 Review

Windows: 2026-11-15T05:00:00Z, 2026-11-15T06:00:00Z, 2026-11-15T07:00:00Z.

- hk_property_poi: 274/280 windows advanced, Laplace 0.975, and it advanced in every UTC hour, so this is near-certain across all three windows.
- hkex_disclosures: 254/279 windows advanced, Laplace 0.907, and it also advanced in every UTC hour, so keep it high and stable across all three windows.
- hkex_disclosure_interests: 254/279 windows advanced, Laplace 0.907, and it mirrors hkex_disclosures with universal hourly coverage, so it stays high and stable.
- crhk_companies: 39/273 windows advanced, Laplace 0.145, with advances concentrated in 06Z and 07Z but not 05Z, so the first window is weaker than the next two.
- sfc_licences: 13/273 windows advanced, Laplace 0.051, with advances only at 01Z/03Z/04Z and none in 05Z-07Z, so all three windows stay low.
- hk_property_transactions: 55/273 windows advanced, Laplace 0.204, with advances at 05Z and 07Z but not 06Z, so the middle window is weaker than the outer two.
