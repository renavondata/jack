# Freshness stream 82 reasoning

- `hk_property_poi`: 152/155 windows advanced, with advances in every UTC hour, so keep p very high across 14Z/15Z/16Z but cap it below 950‰.
- `hkex_disclosures`: 144/154 windows advanced, and it advanced in every UTC hour, so keep p very high across 14Z/15Z/16Z but still within the 50–950‰ bound.
- `hkex_disclosure_interests`: 144/154 windows advanced, and it advanced in every UTC hour, so keep p very high across 14Z/15Z/16Z but still within the 50–950‰ bound.
- `crhk_companies`: 22/147 windows advanced, with advances concentrated at 01Z, 03Z, 06Z, 07Z, 09Z, 10Z, 11Z, 12Z, 13Z, 18Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and keep p lower in the 14Z/15Z/16Z hours that have not advanced before.
- `hk_property_transactions`: 28/148 windows advanced, with advances at 01Z, 02Z, 03Z, 05Z, 07Z, 09Z, 10Z, 11Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and keep p moderate in the 14Z/15Z/16Z hours that have not advanced before.
- `sfc_licences`: 7/148 windows advanced, with advances only at 01Z, 03Z, 04Z, so keep p close to Laplace and low in the 14Z/15Z/16Z hours with no prior advance.
