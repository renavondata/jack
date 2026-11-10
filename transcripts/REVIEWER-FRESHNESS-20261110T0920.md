# Freshness Forecast Reasoning

- hk_property_poi: 171/174 windows advanced; Laplace 0.977; advanced at every recorded hour, so keep p at 980 across 11Z-13Z.
- hkex_disclosures: 163/173 windows advanced; Laplace 0.937; advanced at every recorded hour, so keep p at 940 across 11Z-13Z.
- hkex_disclosure_interests: 163/173 windows advanced; Laplace 0.937; advanced at every recorded hour, so keep p at 940 across 11Z-13Z.
- crhk_companies: 25/166 windows advanced; Laplace 0.155; it has target-hour advances at 11Z, 12Z and 13Z, so use 300/320/300.
- sfc_licences: 8/167 windows advanced; Laplace 0.053; only 01Z, 03Z and 04Z ever advanced, so keep p at 60 across 11Z-13Z.
- hk_property_transactions: 33/167 windows advanced; Laplace 0.201; target-hour history is 11Z and 12Z but not 13Z, so use 250/240/180.
