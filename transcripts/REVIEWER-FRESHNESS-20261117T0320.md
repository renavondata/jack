# Freshness stream 142

- hk_property_poi: 317/323 windows advanced; Laplace 0.978. Almost daily, so I used 950‰ across all three windows.
- hkex_disclosures: 297/322 windows advanced; Laplace 0.920. Very regular, so I used 920‰ across all three windows.
- hkex_disclosure_interests: 297/322 windows advanced; Laplace 0.920. Same record as hkex_disclosures, so I used 920‰ across all three windows.
- crhk_companies: 42/316 windows advanced; Laplace 0.135. Sparse and hour-skewed, so I used 130‰ at 05Z and 180‰ at 06Z/07Z.
- sfc_licences: 15/316 windows advanced; Laplace 0.050. Very sparse, with a 07Z bias, so I used 50‰ at 05Z/06Z and 80‰ at 07Z.
- hk_property_transactions: 65/316 windows advanced; Laplace 0.208. Mixed, with 05Z and 07Z stronger than 06Z, so I used 220‰ at 05Z/07Z and 150‰ at 06Z.
