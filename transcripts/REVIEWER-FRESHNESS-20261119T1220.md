# Freshness stream 161

- `hk_property_poi`: 366/375 windows advanced; Laplace 0.973; advanced in every hour, so keep all three windows near the ceiling at 980‰, 980‰, 980‰.
- `hkex_disclosures`: 346/374 windows advanced; Laplace 0.923; advanced in every hour, so keep all three windows high at 930‰, 930‰, 930‰.
- `hkex_disclosure_interests`: 346/374 windows advanced; Laplace 0.923; advanced in every hour, so keep all three windows high at 930‰, 930‰, 930‰.
- `crhk_companies`: 46/368 windows advanced; Laplace 0.127; it has advanced in some hours but not 14Z/15Z/16Z, so stay near base at 110‰, 110‰, 110‰.
- `sfc_licences`: 17/368 windows advanced; Laplace 0.049; it has surprised before but not in 14Z/15Z/16Z, so keep the floor at 50‰, 50‰, 50‰.
- `hk_property_transactions`: 76/368 windows advanced; Laplace 0.208; 14Z is a historically active hour while 15Z/16Z are not, so use 250‰, 180‰, 160‰.
