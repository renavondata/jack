P=2026-11-05T07:00:00Z is saturated on main already, so the active windows are A=2026-11-05T08:00:00Z, B=2026-11-05T09:00:00Z, C=2026-11-05T10:00:00Z.

hk_property_poi: 68/71 advanced; Laplace 0.945; every UTC hour has advanced before, so keep this near-ceiling in all three windows (p=950, 950, 950).

hkex_disclosures: 68/71 advanced; Laplace 0.945; every UTC hour has advanced before, so keep this near-ceiling in all three windows (p=950, 950, 950).

hkex_disclosure_interests: 68/71 advanced; Laplace 0.945; every UTC hour has advanced before, so keep this near-ceiling in all three windows (p=950, 950, 950).

crhk_companies: 11/65 advanced; Laplace 0.179; advanced hours are 03Z, 09Z, 10Z, 11Z, 12Z, 13Z, 19Z, 23Z, so bias up for B/C and stay lower for A (p=140, 220, 210).

sfc_licences: 3/65 advanced; Laplace 0.060; only 04Z has ever advanced, so keep all three windows at the floor-ish end (p=55, 50, 50).

hk_property_transactions: 11/65 advanced; Laplace 0.179; advanced hours are 02Z, 05Z, 09Z, 10Z, 11Z, 23Z, so B/C get the hour bump while A stays lower (p=130, 220, 210).
