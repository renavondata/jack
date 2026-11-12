# Freshness stream 106 reasoning

- `hk_property_poi`: 216/221 windows advanced, with advances in every UTC hour; keep it at the ceiling, so 950‰ for 14Z/15Z/16Z.
- `hkex_disclosures`: 208/220 windows advanced, also with advances in every UTC hour; keep it very high and stable at 950‰ for all three windows.
- `hkex_disclosure_interests`: 208/220 windows advanced, same all-hours pattern as `hkex_disclosures`; mirror it at 950‰ for all three windows.
- `crhk_companies`: 30/213 windows advanced, with hits in other hours but not 14Z/15Z/16Z; stay near Laplace at 150‰ for all three windows.
- `sfc_licences`: 10/214 windows advanced, with no prior advances in these hours; keep it low and near base rate at 50‰ for all three windows.
- `hk_property_transactions`: 42/214 windows advanced, with a hit at 14Z but not 15Z/16Z; lift the first window and taper after it: 220‰, 180‰, 170‰.
