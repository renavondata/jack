# Freshness Forecast Reasoning

- `hk_property_poi`: 45/47 windows advanced, Laplace 0.939; 05Z and 06Z are the only non-hit hours in the target set, while 07Z is a hit hour, so I’m using 930/930/950.
- `hkex_disclosures`: 45/47 windows advanced, Laplace 0.939; 05Z and 06Z are the only non-hit hours in the target set, while 07Z is a hit hour, so I’m using 930/930/950.
- `hkex_disclosure_interests`: 45/47 windows advanced, Laplace 0.939; 05Z and 06Z are the only non-hit hours in the target set, while 07Z is a hit hour, so I’m using 930/930/950.
- `crhk_companies`: 7/41 windows advanced, Laplace 0.186; none of 05Z/06Z/07Z has a prior hit, so I’m staying near the Laplace rate with 170/180/190.
- `sfc_licences`: 1/41 windows advanced, Laplace 0.047; none of 05Z/06Z/07Z has a prior hit and the only hit hour is 04Z, so I’m staying at the floor with 50/50/50.
- `hk_property_transactions`: 9/41 windows advanced, Laplace 0.233; none of 05Z/06Z/07Z has a prior hit, so I’m using 200/210/220 near the Laplace rate.
