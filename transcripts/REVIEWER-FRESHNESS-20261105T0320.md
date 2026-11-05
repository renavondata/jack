`P=2026-11-05T04:00:00Z` is saturated on `main` already (`grep -c` shows 6), so the active windows are `A=2026-11-05T05:00:00Z`, `B=2026-11-05T06:00:00Z`, `C=2026-11-05T07:00:00Z`.

`hk_property_poi`: 65/68 advanced; Laplace 0.943; every UTC hour has advanced before, so this is near-certain in all three windows (`p=950` each).

`hkex_disclosures`: 65/68 advanced; Laplace 0.943; every UTC hour has advanced before, so this is near-certain in all three windows (`p=950` each).

`hkex_disclosure_interests`: 65/68 advanced; Laplace 0.943; every UTC hour has advanced before, so this is near-certain in all three windows (`p=950` each).

`crhk_companies`: 11/62 advanced; Laplace 0.188; none of A/B/C match an advanced UTC hour, so keep it middling and slightly under the Laplace rate (`p=180, 170, 160`).

`sfc_licences`: 2/62 advanced; Laplace 0.047; only hour 04Z ever advanced and none of A/B/C match it, so stay at the floor (`p=55, 50, 50`).

`hk_property_transactions`: 11/62 advanced; Laplace 0.188; A=05Z matches a historical advanced UTC hour, B/C do not, so give A a small bump and keep B/C middling (`p=240, 170, 160`).
