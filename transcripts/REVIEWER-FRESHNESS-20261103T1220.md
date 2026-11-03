# Freshness Forecast Reasoning

- `hk_property_poi`: 31/32 windows advanced, Laplace 0.941; 15Z is in the advanced-hour set but 14Z/16Z are not, so I’m using 930/950/930.
- `hkex_disclosures`: 31/32 windows advanced, Laplace 0.941; 15Z is in the advanced-hour set but 14Z/16Z are not, so I’m using 930/950/930.
- `hkex_disclosure_interests`: 31/32 windows advanced, Laplace 0.941; 15Z is in the advanced-hour set but 14Z/16Z are not, so I’m using 930/950/930.
- `crhk_companies`: 5/26 windows advanced, Laplace 0.214; none of 14Z/15Z/16Z has prior advances, so I’m using 200/180/160.
- `sfc_licences`: 1/26 windows advanced, Laplace 0.071; none of 14Z/15Z/16Z has prior advances, so I’m using 60/60/60.
- `hk_property_transactions`: 7/26 windows advanced, Laplace 0.286; none of 14Z/15Z/16Z has prior advances, so I’m using 250/230/210.
