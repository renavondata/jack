# Freshness Forecast Reasoning

hk_property_poi: 519/528 windows advanced; Laplace 0.981; support is broad across the record, so I used p=950 in all three windows, capped below certainty because the record has a few misses.

hkex_disclosures: 485/527 windows advanced; Laplace 0.919; it advances in every UTC hour in the record, so I used p=930 throughout.

hkex_disclosure_interests: 485/527 windows advanced; Laplace 0.919; it also advances in every UTC hour, so I used p=930 throughout.

crhk_companies: 62/521 windows advanced; Laplace 0.120; the record is sparse but includes 17Z, 18Z and 19Z, so I used p=180 in each window, staying near the mixed history while favoring seen hours.

sfc_licences: 22/522 windows advanced; Laplace 0.044; it only advanced at 01Z, 03Z, 04Z, 07Z and 10Z, so I used p=60 in each window because 17Z/18Z/19Z are weak but not impossible.

hk_property_transactions: 110/517 windows advanced; Laplace 0.214; 17Z and 19Z have prior advances but 18Z does not, so I used p=250, 210 and 250 across A/B/C.
