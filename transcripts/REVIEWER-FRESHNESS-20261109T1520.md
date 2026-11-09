# Freshness stream 83 reasoning

- `hk_property_poi`: 156/159 windows advanced, and it advanced in every UTC hour, so keep p very high in all three windows but cap it below 950‰.
- `hkex_disclosures`: 148/158 windows advanced, and it advanced in every UTC hour, so keep p very high in all three windows but still within bounds.
- `hkex_disclosure_interests`: 148/158 windows advanced, and it advanced in every UTC hour, so keep p very high in all three windows but still within bounds.
- `crhk_companies`: 23/151 windows advanced, with advances concentrated at 01Z, 03Z, 06Z, 07Z, 09Z, 10Z, 11Z, 12Z, 13Z, 18Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p most in the hours that have advanced before.
- `sfc_licences`: 7/152 windows advanced, with advances only at 01Z, 03Z, 04Z, so keep p close to Laplace and low in the hours with no prior advance.
- `hk_property_transactions`: 30/152 windows advanced, with advances at 01Z, 02Z, 03Z, 05Z, 07Z, 09Z, 10Z, 11Z, 12Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p more in the matching hours.
