# Freshness stream 125 note

- `hk_property_poi`: 270/276 advanced, Laplace 0.975, and it advances in every hour block; use `p=950`.
- `hkex_disclosures`: 250/275 advanced, Laplace 0.906, with advances across all hours; use `p=920`.
- `hkex_disclosure_interests`: 250/275 advanced, Laplace 0.906, with advances across all hours; use `p=920`.
- `crhk_companies`: 37/269 advanced, Laplace 0.140, with advances concentrated in the current 02Z/03Z/04Z band; use `p=150`.
- `hk_property_transactions`: 52/269 advanced, Laplace 0.196, with a mixed hour pattern and no 04Z advance; use `p=200`.
- `sfc_licences`: 12/269 advanced, Laplace 0.048, with advances only at 01Z/03Z/04Z and a colder 02Z window; use `p=60`.
