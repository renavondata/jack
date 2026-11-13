# Freshness stream 115 reasoning

- `hk_property_poi`: 241/247 windows advanced, with advances in nearly every UTC hour, so keep it at the ceiling for 20Z, 21Z, and 22Z: 975‰.
- `hkex_disclosures`: 233/246 windows advanced, also with advances in nearly every UTC hour, so keep it very high and stable at 945‰ for all three windows.
- `hkex_disclosure_interests`: 233/246 windows advanced, again with advances in nearly every UTC hour, so mirror `hkex_disclosures` at 945‰ for all three windows.
- `crhk_companies`: 37/240 windows advanced, with advances only in selected hours, so stay near the Laplace rate but keep the three target hours lifted at 170‰, 160‰, and 170‰.
- `sfc_licences`: 11/240 windows advanced, with advances only at a few early hours, so keep it low and near base rate at 50‰ for all three windows.
- `hk_property_transactions`: 48/240 windows advanced, mixed but still low, so hold it middling at 205‰, 195‰, and 190‰ across the three windows.
