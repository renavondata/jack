# Freshness stream 97 reasoning

- `hk_property_poi`: 193/197 windows advanced, and it advances in every UTC hour, so keep p at the ceiling but under the cap across all three windows.
- `hkex_disclosures`: 185/196 windows advanced, also with advances in every UTC hour, so keep p very high and steady across all three windows.
- `hkex_disclosure_interests`: 185/196 windows advanced, likewise with advances in every UTC hour, so mirror `hkex_disclosures` with very high p across all three windows.
- `crhk_companies`: 28/189 windows advanced, with prior advances at 11Z, 12Z, and 13Z as well as many other hours, so stay near Laplace but lift p in the hours that have already advanced before.
- `sfc_licences`: 9/190 windows advanced, with no prior advances at 11Z, 12Z, or 13Z, so keep p low and close to the base rate in all three windows.
- `hk_property_transactions`: 38/190 windows advanced, with prior advances at 11Z and 12Z but not 13Z, so keep p middling and a bit higher in the first two windows than the third.
