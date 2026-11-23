# Freshness Forecast Reasoning
- `hk_property_poi`: 439/448 windows advanced, Laplace 0.978; it is nearly always fresh, so I used 940 in all three windows.
- `hkex_disclosures`: 406/447 windows advanced, Laplace 0.906; strong overall freshness with no hour skew worth overfitting, so I used 915 in all three windows.
- `hkex_disclosure_interests`: 406/447 windows advanced, Laplace 0.906; same strong record as disclosures, so I used 915 in all three windows.
- `crhk_companies`: 47/441 windows advanced, Laplace 0.108; it has advanced in 03Z/04Z but not 05Z, so I used 140 for 03Z/04Z and 90 for 05Z.
- `sfc_licences`: 19/442 windows advanced, Laplace 0.045; rare overall, but the record favors 03Z/04Z over 05Z, so I used 120 for 03Z/04Z and 70 for 05Z.
- `hk_property_transactions`: 90/441 windows advanced, Laplace 0.205; middling overall with 03Z/04Z support and weaker 05Z support, so I used 220 for 03Z/04Z and 170 for 05Z.
