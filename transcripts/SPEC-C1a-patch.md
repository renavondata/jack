# SPEC patch for C1a (counsel's text; applied by Guy on the builder's branch, RUNBOOK "text before code")

`SPEC.md` is trusted base, so this text reaches it only by Guy's hand and `jack push`. Each item names
the section and gives the replacement or addition verbatim.

## §4 shape / `TYPES`
`TYPES` gains `forecast` and `resolution` (ten types). The sentence naming "the eight" entry-type
names in §5's key declaration reads "the ten".

## §5 body schemas — two rows added to the table
| `forecast` | `claim`: non-empty string; `p`: integer 1–999 (per mille); `resolves_by`: an instant (§4's `ts` form), not earlier than the entry's own `ts` |
| `resolution` | `forecast`: integer ≥ 0, the `seq` of an earlier valid `forecast` entry not already resolved; `outcome`: integer 0 or 1; `evidence`: non-empty string |

After the table: "`forecast.type` and `forecast.args` are optional members the tools read
(RUNBOOK); the kernel never does. `p` is per mille because canonical lines admit integers only
(§2); 1–999 bounds the log-loss without a clipping rule."

## §7 the law in force — two bullets added before "Nothing else is state"
- **Forecasts** are recorded by seq with their `proposer`; **resolved** seqs are recorded. A
  `resolution` whose `forecast` is not a recorded forecast seq, or is already resolved, is
  **schema** (tested at §8 step 7). A `resolution` whose `proposer` equals the forecast's
  `proposer` is **self_judged** (tested at §8 step 8, after the signature, so the party is a
  verified fact): CHARTER §2 maxim 1, judged by principal so that two keys of one party cannot
  launder a judgement.
- The sentence "Nothing else is state at C1's opening" reads "Nothing else is state at C1a".

## §8 the validity predicate
Step 7 adds: "For `forecast`, `resolves_by` earlier than `ts` → **schema**. For `resolution`, a
`forecast` member that is not a recorded forecast seq, or one already resolved → **schema**."
A new step 8a, after the signature: "For `resolution`, the entry's `proposer` equals the recorded
proposer of its `forecast` → **self_judged**."
Step 9 adds: "for `forecast`, record (seq, proposer); for `resolution`, mark its `forecast`
resolved."

## §9 reason codes
"Reason codes (closed set, thirteen): … `bad_signature self_judged`."

## §11 vectors
Signed logs added: `40_forecast_valid`, `41_resolution_valid`, `42_resolution_self_bad`,
`43_resolution_dangling_bad`, `44_resolution_double_bad`, `45_forecast_past_bad`,
`46_forecast_permille_bad` (p = 0 and p = 1000), each with its required verdict.

## §12 decisions
6. C1 opens ledger-first (Guy, 25 October 2026; A3): `forecast` and `resolution` precede the clerk;
   `p` is per mille; self-resolution has its own code; scoring is outside the kernel.
