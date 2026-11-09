# Freshness stream 81 reasoning

- `hk_property_poi`: 150/153 windows advanced, and it advanced in every UTC hour, so keep p very high across 11Z/12Z/13Z but stay under the 950‰ cap.
- `hkex_disclosures`: 142/152 windows advanced, and it advanced in every UTC hour, so keep p very high across 11Z/12Z/13Z but still within bounds.
- `hkex_disclosure_interests`: 142/152 windows advanced, and it advanced in every UTC hour, so keep p very high across 11Z/12Z/13Z but still within bounds.
- `crhk_companies`: 22/145 windows advanced, with advances concentrated at 01Z, 03Z, 06Z, 07Z, 09Z, 10Z, 11Z, 12Z, 13Z, 18Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p most in the hours that have advanced before.
- `sfc_licences`: 7/146 windows advanced, with advances only at 01Z, 03Z, 04Z, so keep p close to Laplace and low in the hours with no prior advance.
- `hk_property_transactions`: 28/146 windows advanced, with advances at 01Z, 02Z, 03Z, 05Z, 07Z, 09Z, 10Z, 11Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p more in the matching hours.
