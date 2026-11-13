# Freshness stream 110 reasoning

- `hk_property_poi`: 226/231 windows advanced, with advances in every UTC hour; keep it at the ceiling for all three windows, 950‰.
- `hkex_disclosures`: 217/229 windows advanced, with advances in every UTC hour; stay very high and steady at 940‰ for all three windows.
- `hkex_disclosure_interests`: 217/229 windows advanced, with advances in every UTC hour; mirror `hkex_disclosures` at 940‰ for all three windows.
- `crhk_companies`: 31/223 windows advanced, with advances at 02Z, 03Z, and 04Z among many sparse hours; stay near Laplace but lift the later hours, 180‰ at 02Z, 220‰ at 03Z, 240‰ at 04Z.
- `sfc_licences`: 10/223 windows advanced, with advances at 03Z and 04Z but not 02Z; keep it low, 50‰ at 02Z, then 120‰ at 03Z and 140‰ at 04Z.
- `hk_property_transactions`: 43/224 windows advanced, with advances at 02Z and 03Z but not 04Z; use 240‰ at 02Z, 260‰ at 03Z, then 150‰ at 04Z.
