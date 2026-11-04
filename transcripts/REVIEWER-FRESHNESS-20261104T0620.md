# Freshness Forecast Reasoning

- `hk_property_poi`: 47/50 windows advanced, Laplace 0.923; 08Z/09Z/10Z are all in its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosures`: 48/50 windows advanced, Laplace 0.942; 08Z/09Z/10Z are all in its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosure_interests`: 48/50 windows advanced, Laplace 0.942; 08Z/09Z/10Z are all in its advanced-hour set, so I’m using 950/950/950.
- `crhk_companies`: 8/44 windows advanced, Laplace 0.196; 09Z and 10Z have prior hits but 08Z does not, so I’m using 180/240/260.
- `sfc_licences`: 2/44 windows advanced, Laplace 0.065; none of 08Z/09Z/10Z has a prior hit, so I’m staying at the floor with 50/50/50.
- `hk_property_transactions`: 9/44 windows advanced, Laplace 0.217; 09Z and 10Z have prior hits but 08Z does not, so I’m using 190/240/260.
