# Freshness stream 77 reasoning

- `hk_property_poi`: 141/144 windows advanced, with advances in every UTC hour, so keep p very high across A/B/C but not above the 950‰ cap.
- `hkex_disclosures`: 133/143 windows advanced, also with advances in every UTC hour, so keep p very high across A/B/C but still within the 50–950‰ bound.
- `hkex_disclosure_interests`: 133/143 windows advanced, again with advances in every UTC hour, so keep p very high across A/B/C but still within the 50–950‰ bound.
- `crhk_companies`: 22/136 windows advanced, with advances concentrated at 01Z, 03Z, 06Z, 07Z, 09Z, 10Z, 11Z, 12Z, 13Z, 18Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p most in the hours that have advanced before.
- `hk_property_transactions`: 26/137 windows advanced, with advances at 01Z, 02Z, 03Z, 05Z, 07Z, 09Z, 10Z, 11Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p more in the matching hours.
- `sfc_licences`: 7/137 windows advanced, with advances only at 01Z, 03Z, 04Z, so keep p close to Laplace and low in the hours with no prior advance.
