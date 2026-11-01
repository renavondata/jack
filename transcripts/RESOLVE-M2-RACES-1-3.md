# M2 races 1–3 and pending freshness resolutions

Resolver: builder, openai/gpt-6-astra, branch `resolve-m2-races-1-3`.

## Evidence method

All nine HTML files were fetched with `curl -sL --max-time 90` and saved without editing their response bodies. The JSON manifests record SHA-256 hashes and UTC completion times from the saved files' modification times, truncated to seconds. The freshness directory's timestamp is a session label; the per-file `fetched_at` fields are the actual acquisition times.

HKJC's saved results pages identify the 1 November 2026 Happy Valley meeting and the respective race numbers. Each has completed placings, finish times, full-field final WIN odds, and declared dividends. The shortest positive numeric value in the results table's `Win Odds` column determines the favourite, not the WIN dividend. Race 1's SMART CITY (10) was withdrawn and has no final odds; all 11 starters have numeric odds. Races 2 and 3 each have numeric final odds for all 12 starters. Each race has one first-placed runner, with no winning dead heat or void race.

The saved hkjc.guru pages still say the races have not run and show overnight odds. They are retained and hashed as retrieval evidence only, and supply no final result or final-odds evidence. The authoritative completed HKJC tables support all three verdicts.

| Race | Winner | Shortest final WIN odds | Outcome | Reviewer seq | Counsel seq | resolves_by (UTC) |
|---|---|---|---:|---:|---:|---|
| 1 | FALCON HUNTER (1) | FALCON HUNTER (1), 1.3 | 1 | 227 | 239 | 2026-11-01T06:45:00Z |
| 2 | GRIT SPIRIT (3) | LUCK IS BACK (9), 3.3 | 0 | 228 | 240 | 2026-11-01T07:15:00Z |
| 3 | INCREDIBLE MOMENT (4) | INCREDIBLE MOMENT (4), 2.0 | 1 | 229 | 241 | 2026-11-01T07:45:00Z |

Race evidence manifest: `transcripts/evidence/hkjc-20261101-results-1-3.json`.

## Freshness ledger discrepancy

The clerk lists six pending reviewer forecasts: 280–282 and 288–290. Both triplets explicitly name hour `2026-11-01 12` HKT and window `[2026-11-01T04:00:00Z, 2026-11-01T05:00:00Z)`, with `resolves_by` 2026-11-01T06:30:00Z. The latter triplet is not a 13:00 HKT forecast. No pending 13:00 HKT triplet was listed. The recorded claims are resolved without changing their windows.

The parsed last-updated instant is the public page's JSON-LD `dateModified`, as in the stream's previous resolution evidence. The pages were fetched after the recorded window ended. The outcome rule is last-updated >= window start, with no upper bound on last-updated; later refreshes therefore satisfy these claims.

| Dataset | Forecast seqs | Last updated as printed | UTC | Outcome |
|---|---|---|---|---:|
| hk_property_poi | 280, 288 | 2026-11-01T05:34:00+00:00 | 2026-11-01T05:34:00Z | 1 |
| hkex_disclosures | 281, 289 | 2026-11-01T05:29:22+00:00 | 2026-11-01T05:29:22Z | 1 |
| hkex_disclosure_interests | 282, 290 | 2026-11-01T05:29:22+00:00 | 2026-11-01T05:29:22Z | 1 |

Freshness evidence manifest: `transcripts/evidence/renavon-freshness-20261101T061200Z-resolve.json`. Exact resolution times are recorded by the signed resolution entries in `log.jsonl`.
