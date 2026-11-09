# Freshness stream 75 reasoning

- `hk_property_poi`: 135/138 windows advanced, with advances in every UTC hour, so keep p very high in all three windows.
- `hkex_disclosures`: 127/137 windows advanced, again with advances in every UTC hour, so keep p very high in all three windows.
- `hkex_disclosure_interests`: 127/137 windows advanced, again with advances in every UTC hour, so keep p very high in all three windows.
- `crhk_companies`: 22/130 windows advanced, with advances concentrated at 01Z, 03Z, 06Z, 07Z, 09Z, 10Z, 11Z, 12Z, 13Z, 18Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p only for the 18Z and 19Z windows.
- `hk_property_transactions`: 26/131 windows advanced, with advances at 01Z, 02Z, 03Z, 05Z, 07Z, 09Z, 10Z, 11Z, 19Z, 20Z, 22Z, 23Z, so stay near Laplace and lift p most for 19Z.
- `sfc_licences`: 7/131 windows advanced, with advances only at 01Z, 03Z, 04Z, so keep p close to Laplace and low in all three windows.
