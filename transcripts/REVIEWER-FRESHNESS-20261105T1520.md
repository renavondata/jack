freshness stream 51, windows 2026-11-05T17:00:00Z to 2026-11-05T20:00:00Z.

- hk_property_poi: 74/77 advanced, Laplace 0.949, and it has been hot in every hour bucket, so I am using p=950 for all three windows.
- hkex_disclosures: 74/77 advanced, Laplace 0.949, with advances in every hour bucket, so I am using p=950 for all three windows.
- hkex_disclosure_interests: 74/77 advanced, Laplace 0.949, with advances in every hour bucket, so I am using p=950 for all three windows.
- hk_property_transactions: 13/71 advanced, Laplace 0.192, with advances only at 02Z, 05Z, 09Z, 10Z, 11Z and 23Z, so I am using p=180 for all three windows.
- crhk_companies: 11/70 advanced, Laplace 0.167, with prior advances at 03Z, 09Z, 10Z, 11Z, 12Z, 13Z, 19Z and 23Z, so I am using p=170 for 17Z/18Z and p=260 for 19Z.
- sfc_licences: 3/71 advanced, Laplace 0.055, with a single advance at 04Z, so I am using p=70 for all three windows.
