# Freshness stream 114 reasoning

- `hk_property_poi`: 241/247 windows advanced, with advances in every UTC hour, so keep it at the ceiling for 17Z, 18Z, and 19Z: 950‰.
- `hkex_disclosures`: 229/242 windows advanced, also with advances in every UTC hour, so keep it very high and stable at 940‰ for all three windows.
- `hkex_disclosure_interests`: 229/242 windows advanced, again with advances in every UTC hour, so mirror `hkex_disclosures` at 940‰ for all three windows.
- `crhk_companies`: 35/238 windows advanced, with advances at 17Z, 18Z, and 19Z among other hours, so stay near the Laplace rate but keep the three target hours lifted at 220‰.
- `sfc_licences`: 11/236 windows advanced, with advances only at 01Z, 03Z, and 04Z, so keep it low and near base rate at 50‰ for all three windows.
- `hk_property_transactions`: 47/238 windows advanced, with advances at 17Z and 19Z but not 18Z, so stay middling and keep the three target windows at 190‰.
