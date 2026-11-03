# Freshness Forecast Reasoning

- `hk_property_poi`: 28/29 windows advanced, Laplace 0.935, and the candidate hours 11Z/12Z/13Z all sit inside its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosures`: 28/29 windows advanced, Laplace 0.935, with 11Z/12Z/13Z all previously advanced, so I’m using 950/950/950.
- `hkex_disclosure_interests`: 28/29 windows advanced, Laplace 0.935, with 11Z/12Z/13Z all previously advanced, so I’m using 950/950/950.
- `crhk_companies`: 5/23 windows advanced, Laplace 0.240; 12Z/13Z have prior advances but 11Z does not, so I’m using 200/340/360.
- `sfc_licences`: 1/23 windows advanced, Laplace 0.080, and none of 11Z/12Z/13Z has prior advances, so I’m using 70/70/70.
- `hk_property_transactions`: 7/23 windows advanced, Laplace 0.320; 11Z has prior advances but 12Z/13Z do not, so I’m using 360/290/290.
