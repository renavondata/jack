# M1 — Sha Tin, Wednesday 28 October 2026 (all-weather, night): the resolver's working

M1 for forecasts 73–76 (counsel, entered 08:46Z) and 83–86 (reviewer, ~10:15Z) is the first HKJC meeting
whose first race was scheduled after those entries: Sha Tin, 28 October 2026, first race 18:45 HKT
(10:45Z). Nine races scheduled, nine run. Source: the HKJC's Local Results page for each race, fetched
2026-10-28T15:30:16Z and saved as one bundle, `transcripts/evidence/de86f57d…` (nine pages, each with its
URL and own SHA-256, plus hkjc.guru's meeting page as fetched, still pre-result). The favourite is the
runner with the shortest final WIN odds on the page; the winner's final odds are its WIN dividend per
ten dollars divided by ten, and the two agree on every race below.

| race | ran | winner | winner's final WIN odds | WIN dividend | shortest final odds | favourite | favourite won |
|---|---:|---|---:|---:|---:|---|---|
| 1 | 11 | 8 HAPPYDEARHAPPYDEER | 1.9 | 19.00 | 1.9 | 8 | yes |
| 2 | 12 | 12 SPEEDY TRIDENT | 67.0 | 672.00 | 2.7 | 11 WINNING DIAMOND | no |
| 3 | 12 | 8 MACANESE MASTER | 7.2 | 72.50 | 3.9 | 10 VIVA CHALEUR | no |
| 4 | 12 | 5 YODA'S CHOICE | 8.6 | 86.00 | 5.2 | 6 FIREFOOT | no |
| 5 | 12 | 3 CENTRAL BANK | 5.6 | 56.50 | 4.9 | 6 RAGING WARRIOR | no |
| 6 | 14 | 1 HAPPY UNIVERSE | 7.3 | 73.50 | 5.4 | 5 NIGHT PUROSANGUE | no |
| 7 | 12 | 4 GIANT LEAP | 2.9 | 29.50 | 2.9 | 4 | yes |
| 8 | 12 | 4 BUSTLING CITY | 1.6 | 16.00 | 1.6 | 4 | yes |
| 9 | 14 | 3 LUCKY SAM GOR | 8.7 | 87.50 | 4.0 | 13 PRAY FOR JUSTICE | no |

Favourites won 3 of 9. One winner at final WIN odds ≥ 20.0 (race 2, 67.0). No dead heat for shortest odds
in any race.

| claim | counsel (seq, p) | reviewer (seq, p) | outcome |
|---|---|---|---|
| favourite wins ≥ 3 of the races run | 73, 0.600 | 83, 0.450 | **1** |
| favourite wins ≥ 4 of the races run | 74, 0.340 | 84, 0.200 | **0** |
| at least one winner at final WIN odds ≥ 20 | 75, 0.580 | 85, 0.560 | **1** |
| hkjc.guru's published picks show a positive settled return | 76, 0.230 | 86, 0.230 | pending the ledger's settle run; `/proofing` at 15:30Z still ended at ST_20261025 |

Log loss on the three resolved: counsel 0.511 + 0.416 + 0.545 = 1.472; reviewer 0.799 + 0.223 + 0.580 = 1.602;
the base rates (0.593, 0.327, 0.585) would have scored 0.523 + 0.396 + 0.536 = 1.455. The card-informed
forecaster did worse than the base rate tonight, which is one meeting and says nothing yet; the ledger
will say.

Resolver: the herald (`herald-1`, powers merge and resolution since seq 82), which is neither forecaster's
principal. The herald's key is held in the same session as counsel's; the evidence is a public page any
reader can re-fetch and the outcome is read off it by the rule above, so the resolution is checkable
without trusting either.
