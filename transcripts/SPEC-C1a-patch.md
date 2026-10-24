# SPEC patch for C1a, v2 (counsel's text; applied by Guy on the builder's branch, RUNBOOK "text before code")

`SPEC.md` is trusted base, so this text reaches it only by Guy's hand and `jack push`. Each item names
the section and gives the replacement or addition. v2 answers `transcripts/REVIEW-brief-3.md` §5.

## §4 shape / `TYPES`
`TYPES` gains `forecast` and `resolution` (ten types). §5's "any of the eight" reads "any of the ten".

## §5 body schemas — two rows added to the table
| `forecast` | `claim`: non-empty string; `p`: integer 1–999 (per mille; a boolean is not an integer); `resolves_by`: an instant in §4's `ts` form, not earlier than the entry's own `ts` |
| `resolution` | `forecast`: integer ≥ 0, the `seq` of an earlier valid `forecast` entry not already resolved; `outcome`: integer 0 or 1 (a boolean is not an integer); `evidence`: non-empty string |

After the table: "`forecast.type` and `forecast.args` are optional members the tools read (RUNBOOK);
the kernel never reads them and refuses nothing on their account. `p` is per mille because canonical
lines admit integers only (§2); 1–999 bounds the log-loss without a clipping rule."

## §7 the law in force — three bullets added before "Nothing else is state"
- **Timestamps do not decrease** (CHARTER A2.2): entry *i*'s `ts` is not earlier than entry *i*−1's,
  compared as strings, which for §4's fixed-width UTC form is chronological order. Genesis has no
  parent and is exempt. Refusal: **ts_decreased**, tested at §8 step 2a.
- **Forecasts** are recorded by seq with their `proposer`; **resolved** seqs are recorded. A
  `resolution` whose `forecast` is not a recorded forecast seq, or is already resolved, is **schema**
  (§8 step 7, before the signature). A `resolution` whose `proposer` equals the recorded proposer of
  its `forecast` is **self_judged** (§8 step 8a, after the signature, so the party is a verified
  fact): CHARTER §2 maxim 1, judged by principal so that two keys of one party cannot launder a
  judgement. Consequently a self-resolution with a bad signature is `bad_signature`, and a
  self-resolution of an already-resolved forecast is `schema`.
- **Availability.** The two types are recognised from the checker that implements them; recognition
  is additive and every earlier valid log replays unchanged. Which entries count toward a window is
  the brief's business (BRIEF-C1.md), not the checker's.
- "Nothing else is state at C1's opening" reads "Nothing else is state at C1a".

## §8 the validity predicate
New step 2a, after step 2: "`ts` earlier than the previous entry's `ts` (entry 0 exempt) →
**ts_decreased**."
Step 7 adds: "For `forecast`, `resolves_by` earlier than `ts` → **schema**. For `resolution`, a
`forecast` member that is not a recorded forecast seq, or one already resolved → **schema**."
New step 8a, after step 8: "For `resolution`, the entry's `proposer` equals the recorded proposer of
its `forecast` → **self_judged**."
Step 9 adds: "for `forecast`, record (seq, proposer); for `resolution`, mark its `forecast` resolved;
for every entry, record its `ts` as the previous `ts`."

## §9 reason codes, and §9a
§9: "Reason codes (closed set, fourteen): … `bad_signature ts_decreased self_judged`."
§9a.3: "`reason` one of §9's fourteen codes" (replacing "twelve"). Every other normative reference to
the count of codes is updated with it; the harness's strict parser admits exactly the fourteen.

## §11 vectors
Signed logs added, each with its required `(seq, reason)` verdict: `40_forecast_valid`,
`41_resolution_valid`, `42_resolution_self_bad` (`self_judged`), `43_resolution_dangling_bad`
(`schema`), `44_resolution_double_bad` (`schema`), `45_forecast_past_bad` (`schema`),
`46a_forecast_permille_0_bad` (`schema`), `46b_forecast_permille_1000_bad` (`schema`),
`47_forecast_boolean_bad` (`schema`, `p: true`), `48_ts_decreased_bad` (`ts_decreased`),
`49_self_resolution_bad_signature` (`bad_signature`, not `self_judged`). Each refused log stops at
its first bad entry, so each witnesses one refusal.

## §12 decisions — appended as the next number
C1 opens ledger-first (Guy, 25 October 2026; A3): `forecast` and `resolution` precede the clerk; `p`
is per mille; self-resolution has its own code; A2.2's `ts_decreased` is implemented with them;
scoring is outside the kernel; §12.4's sentence "whose order is not checked at C0" is superseded.
