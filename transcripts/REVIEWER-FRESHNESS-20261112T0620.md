# Freshness stream 104 reasoning

- `hk_property_poi`: 210/215 windows advanced, with advances in every UTC hour; keep it near the ceiling but under the surprise cap, so 950‰ for 08Z/09Z/10Z.
- `hkex_disclosures`: 202/214 windows advanced, with advances in every UTC hour; keep it very high and stable at 940‰ for all three windows.
- `hkex_disclosure_interests`: 202/214 windows advanced, with advances in every UTC hour; mirror `hkex_disclosures` at 940‰ for all three windows.
- `crhk_companies`: 30/207 windows advanced, with advances at 09Z and 10Z but not 08Z; stay near Laplace and lift the later two hours: 120‰ at 08Z, 260‰ at 09Z, 240‰ at 10Z.
- `sfc_licences`: 10/208 windows advanced, with advances only at 01Z, 03Z, and 04Z; keep it low and near base rate at 50‰ for all three windows.
- `hk_property_transactions`: 41/208 windows advanced, with advances at 09Z and 10Z but not 08Z; use 150‰ at 08Z, 240‰ at 09Z, 240‰ at 10Z.
