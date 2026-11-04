# Freshness Forecast Reasoning

- `hk_property_poi`: 50/53 windows advanced, Laplace 0.927; 11Z/12Z/13Z are all in its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosures`: 51/53 windows advanced, Laplace 0.945; 11Z/12Z/13Z are all in its advanced-hour set, so I’m using 950/950/950.
- `hkex_disclosure_interests`: 51/53 windows advanced, Laplace 0.945; 11Z/12Z/13Z are all in its advanced-hour set, so I’m using 950/950/950.
- `crhk_companies`: 8/47 windows advanced, Laplace 0.184; 11Z/12Z/13Z are all hit hours, but the rate is still low overall, so I’m using 240/255/270.
- `sfc_licences`: 2/47 windows advanced, Laplace 0.061; none of 11Z/12Z/13Z has a prior hit, so I’m staying at the floor with 50/50/50.
- `hk_property_transactions`: 10/47 windows advanced, Laplace 0.224; 11Z has a prior hit while 12Z/13Z do not, so I’m using 260/220/210.
