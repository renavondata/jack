# Freshness Stream 167

- `hk_property_poi`: 384/393 windows advanced; Laplace 0.975. Hours 08Z/09Z/10Z all sit in its advanced-hour set, but the cap for a dataset that has surprised at least once keeps this below 950, so `p=945` for each window.
- `hkex_disclosures`: 364/392 windows advanced; Laplace 0.926. It advances in all hours, including 08Z/09Z/10Z, so keep it high but below the surprise cap: `p=930` for each window.
- `hkex_disclosure_interests`: 364/392 windows advanced; Laplace 0.926. Same record shape as `hkex_disclosures`, and the target hours are in its advanced set, so `p=930` for each window.
- `crhk_companies`: 46/386 windows advanced; Laplace 0.121. The record is sparse, but 08Z/09Z/10Z are among the hours where it has advanced before, so use middling probabilities near that rate: `p=150`, `160`, `170`.
- `sfc_licences`: 18/386 windows advanced; Laplace 0.049. 08Z is not an advanced hour; 09Z is also absent; 10Z is an advanced hour, so stay low but above 50: `p=60`, `70`, `90`.
- `hk_property_transactions`: 79/386 windows advanced; Laplace 0.206. 08Z/09Z/10Z are all advanced hours for this dataset, so keep it above the Laplace baseline but still moderate: `p=230`, `240`, `250`.
