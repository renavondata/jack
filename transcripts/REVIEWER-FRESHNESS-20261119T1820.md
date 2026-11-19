# Freshness Forecast Notes

- hk_property_poi: 372/381 windows advanced; Laplace 0.974; it advances in every hour bucket, but the record is already near-certain and must stay <=950‰, so I use 950 for 20:00Z/21:00Z/22:00Z.
- hkex_disclosures: 352/380 windows advanced; Laplace 0.924; it also advances in every hour bucket, so 930 tracks the rate without pretending certainty.
- hkex_disclosure_interests: 352/380 windows advanced; Laplace 0.924; same pattern as hkex_disclosures, so 930.
- crhk_companies: 46/374 windows advanced; Laplace 0.125; it has a mixed but hour-positive record and is active in 20:00Z/21:00Z/22:00Z, so 130 stays near baseline with a small hour bump.
- hk_property_transactions: 77/374 windows advanced; Laplace 0.207; it has a mixed record but all three target hours have hit before, so 220 is a modest uplift without overshooting.
- sfc_licences: 17/374 windows advanced; Laplace 0.048; the target hours have never advanced in the record, and the floor is 50‰, so I use 50.
