# Freshness reasoning

hk_property_poi: 399/408 windows advanced; Laplace 0.976; the record is almost always hot across all hours, so p 950 stays near the ceiling without overclaiming.
hkex_disclosures: 379/407 windows advanced; Laplace 0.929; it advances in every hour bucket, so p 930 is the right high-but-not-max setting.
hkex_disclosure_interests: 379/407 windows advanced; Laplace 0.929; the same all-hours pattern holds, so p 930 matches the record.
crhk_companies: 46/401 windows advanced; Laplace 0.117; it is sparse overall but does fire in 01-04, so p 130 keeps close to the base rate with a small hour lift.
hk_property_transactions: 81/401 windows advanced; Laplace 0.203; the history is modest and favors 01-03 more than 04, so p 220 for the first three windows and 180 at 04 fits the pattern.
sfc_licences: 18/401 windows advanced; Laplace 0.047; only a few hour buckets advance at all, so p 60 with a 50 floor on the weakest window is the cautious call.
