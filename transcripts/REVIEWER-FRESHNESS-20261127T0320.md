# freshness stream 218

- hk_property_poi: 507/516 windows advanced, Laplace 0.981; it has advanced in all target hours, so I pinned it at 950 for 05Z/06Z/07Z.
- hkex_disclosures: 474/515 windows advanced, Laplace 0.919; it has advanced in all hours, so I kept it high at 920 for all three windows.
- hkex_disclosure_interests: 474/515 windows advanced, Laplace 0.919; same shape as hkex_disclosures, so 920 for all three windows.
- crhk_companies: 61/509 windows advanced, Laplace 0.121; it has advanced at 06Z and 07Z but not 05Z, so I used 110 at 05Z and 130 at 06Z/07Z.
- sfc_licences: 22/510 windows advanced, Laplace 0.045; it has advanced at 07Z but not 05Z/06Z, so I held the floor at 50 for 05Z/06Z and raised to 75 at 07Z.
- hk_property_transactions: 107/505 windows advanced, Laplace 0.213; it has advanced at 05Z and 07Z but not 06Z, so I used 230 at 05Z/07Z and 190 at 06Z.
