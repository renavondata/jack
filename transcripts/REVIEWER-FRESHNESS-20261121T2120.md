# Freshness review notes

- hk_property_poi: 416/425 windows advanced, Laplace 0.977, advanced in every hour; the page is very fresh and I used p=945 for all three windows.
- hkex_disclosures: 385/424 windows advanced, Laplace 0.906, advanced in every hour; strong but not perfect freshness, so I used p=925 for all three windows.
- hkex_disclosure_interests: 385/424 windows advanced, Laplace 0.906, advanced in every hour; same record shape as hkex_disclosures, so I used p=925 for all three windows.
- crhk_companies: 46/418 windows advanced, Laplace 0.112, advanced at 23Z and 01Z but not 00Z; mixed and hour-sensitive, so I used p=160 at 23Z/01Z and p=100 at 00Z.
- sfc_licences: 19/418 windows advanced, Laplace 0.048, advanced only sparsely with 01Z in the live-hour set; very low base rate, so I used p=70 at 23Z, p=55 at 00Z, and p=80 at 01Z.
- hk_property_transactions: 85/418 windows advanced, Laplace 0.205, advanced at 23Z but not 00Z/01Z; moderate and hour-patterned, so I used p=230 at 23Z and p=170 at 00Z/01Z.
