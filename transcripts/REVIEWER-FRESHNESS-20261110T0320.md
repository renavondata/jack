# Freshness stream 87 reasoning

- `hk_property_poi`: 166/169 windows advanced, and it advanced in every UTC hour, so keep p very high across 05Z/06Z/07Z, capped below 950‰.
- `hkex_disclosures`: 158/168 windows advanced, and it advanced in every UTC hour, so keep p very high across 05Z/06Z/07Z, still within bounds.
- `hkex_disclosure_interests`: 158/168 windows advanced, and it advanced in every UTC hour, so keep p very high across 05Z/06Z/07Z, still within bounds.
- `crhk_companies`: 24/161 windows advanced, with advances concentrated at 01Z, 03Z, 06Z, 07Z, 09Z, 10Z, 11Z, 12Z, 13Z, 18Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p most in 06Z/07Z, less in 05Z.
- `sfc_licences`: 7/162 windows advanced, with advances only at 01Z, 03Z, 04Z, so keep p close to Laplace and low in 05Z/06Z/07Z.
- `hk_property_transactions`: 32/162 windows advanced, with advances at 01Z, 02Z, 03Z, 05Z, 07Z, 09Z, 10Z, 11Z, 12Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p more in 05Z/07Z than 06Z.
