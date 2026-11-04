# Freshness Forecast Reasoning

- `hk_property_poi`: 42/44 windows advanced, Laplace 0.935; 02Z/03Z/04Z all sit inside its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosures`: 42/44 windows advanced, Laplace 0.935; 02Z/03Z/04Z all sit inside its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosure_interests`: 42/44 windows advanced, Laplace 0.935; 02Z/03Z/04Z all sit inside its advanced-hour set, so I’m using 950/950/950.
- `crhk_companies`: 7/38 windows advanced, Laplace 0.200; none of 02Z/03Z/04Z has a prior hit, so I’m using 220/200/180.
- `sfc_licences`: 1/38 windows advanced, Laplace 0.050; 04Z is its only prior hit, so I’m using 50/50/60.
- `hk_property_transactions`: 8/38 windows advanced, Laplace 0.225; 02Z has a prior hit but 03Z/04Z do not, so I’m using 260/220/200.
