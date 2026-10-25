# kernel2 implementation notes

## Author and scope

- Model ID: **`google/gemini-4-argon`**.
- Session: `c1a-kernel2` room (`/home/g/git/worktrees/jack/c1a-kernel2`), 2026-10-25.
- Sources consulted: only `SPEC.md`, `spec/`, `tests/vectors/`, and `kernel2/`. No files outside those paths and no first-checker implementation were read.
- Implementation: Go standard library only. Production verification uses independently implemented Edwards arithmetic over `math/big`, canonical point decoding, `S < L`, reduced SHA-512 challenge, and the cofactorless equation. Small-order public keys are rejected at declaration, not by the signature verifier itself. `crypto/ed25519` appears only in tests.
- The checker makes no network, clock, or LLM calls. Its decisions depend solely on the log bytes.

## C1a changes and driving SPEC.md sentences

1. **Ten entry types and key powers (`forecast`, `resolution`)** (`kernel2/checker.go`: `isType`):
   - **§4 table (`type`)**: *"one of `genesis key proposal merge amend push decision spec_conflict forecast resolution`"*.
   - **§5 (`key declaration`)**: *"`powers`: array of entry-type names (any of the ten, possibly empty, repetition allowed)"*.
2. **`forecast` and `resolution` body schemas** (`kernel2/checker.go`: `bodyShape`):
   - **§5 table (`forecast`)**: *"`claim`: non-empty string; `p`: integer 1–999 (per mille; a boolean is not an integer); `resolves_by`: an instant in §4's `ts` form, not earlier than the entry's own `ts`"*.
   - **§5 prose**: *"`forecast.type` and `forecast.args` are optional members the tools read (RUNBOOK); the kernel never reads them and refuses nothing on their account."*
   - **§5 table (`resolution`)**: *"`forecast`: integer ≥ 0, the `seq` of an earlier valid `forecast` entry not already resolved; `outcome`: integer 0 or 1 (a boolean is not an integer); `evidence`: non-empty string"*.
   - **§5 prose**: *"Required members per type; **extra members are allowed** (any keys, any depth, including keys containing `.`); a required member with the wrong shape is **schema**."* and *"`integer ≥ 0` excludes booleans."*
3. **Non-decreasing timestamps (`ts_decreased` at §8 step 2a)** (`kernel2/checker.go`: `law.prevTS`, `checkEntry`):
   - **§7**: *"**Timestamps do not decrease** (CHARTER A2.2): entry i's `ts` is not earlier than entry i−1's, compared as strings, which for §4's fixed-width UTC form is chronological order. Genesis has no parent and is exempt. Refusal: **ts_decreased**, tested at §8 step 2a."*
   - **§8 step 2a**: *"`ts` earlier than the previous entry's `ts` (entry 0 exempt) → **ts_decreased**."* (Tested after step 2 `entryShape` and before step 3 `bad_seq`.)
   - **§8 step 9**: *"for every entry, record its `ts` as the previous `ts`."*
   - **§12 item 11**: *"A2.2's `ts_decreased` is implemented with them; scoring is outside the kernel; §12.4's sentence 'whose order is not checked at C0' is superseded."*
4. **Forecast and resolution state and refusals (`schema` at step 7; `self_judged` at step 8a)** (`kernel2/checker.go`: `law.forecasts`, `law.resolved`, `checkEntry`):
   - **§7**: *"**Forecasts** are recorded by seq with their `proposer`; **resolved** seqs are recorded. A `resolution` whose `forecast` is not a recorded forecast seq, or is already resolved, is **schema** (§8 step 7, before the signature). A `resolution` whose `proposer` equals the recorded proposer of its `forecast` is **self_judged** (§8 step 8a, after the signature, so the party is a verified fact): CHARTER §2 maxim 1, judged by principal so that two keys of one party cannot launder a judgement. Consequently a self-resolution with a bad signature is `bad_signature`, and a self-resolution of an already-resolved forecast is `schema`."*
   - **§8 step 7**: *"For `forecast`, `resolves_by` earlier than `ts` → **schema**. For `resolution`, a `forecast` member that is not a recorded forecast seq, or one already resolved → **schema**."*
   - **§8 step 8a**: *"For `resolution`, the entry's `proposer` equals the recorded proposer of its `forecast` → **self_judged**."*
   - **§8 step 9**: *"for `forecast`, record (seq, proposer); for `resolution`, mark its `forecast` resolved"*.
5. **Fourteen reason codes and unchanged CLI contract** (`kernel2/checker.go`, `kernel2/main.go`):
   - **§9**: *"Reason codes (closed set, fourteen): `malformed_json not_canonical schema bad_seq parent_mismatch genesis_misplaced no_proposer bad_key unknown_key proposer_mismatch no_power bad_signature ts_decreased self_judged`."*

## C1a test logs in `kernel2/` and the SPEC sentences they witness

In `kernel2/governance_test.go` (`TestC1aSignedLogs`, verified both in-process, over all proper prefixes per §9a.2, and through the `./check` CLI binary) and `kernel2/vectors_test.go` (`TestScoreVectorLog`):

| Test log | Verdict | SPEC.md sentence(s) witnessed |
|---|---|---|
| `40_forecast_valid` | `{"ok":true,"entries":2}` | §4 (`type` includes `forecast`); §5 (`forecast` required members `claim`, `p` in 1–999, `resolves_by`, and optional `type`/`args` ignored); §7 & §8 step 9 (`for forecast, record (seq, proposer)`). |
| `40b_forecast_equal_resolves_by_valid` | `{"ok":true,"entries":2}` | §5 (`resolves_by`: *"not earlier than the entry's own `ts`"* and `p: 1` boundary); §7 (*"entry i's `ts` is not earlier than entry i−1's"*). |
| `41_resolution_valid` | `{"ok":true,"entries":3}` | §4 (`type` includes `resolution`); §5 (`resolution` required members `forecast`, `outcome`, `evidence`); §7 & §8 step 9 (`for resolution, mark its forecast resolved`). |
| `42_resolution_self_bad` | `{"ok":false,"seq":2,"reason":"self_judged"}` | §7 & §8 step 8a (*"For `resolution`, the entry's `proposer` equals the recorded proposer of its `forecast` → **self_judged**"*). |
| `42b_resolution_self_second_key_bad` | `{"ok":false,"seq":2,"reason":"self_judged"}` | §7 (*"judged by principal so that two keys of one party cannot launder a judgement"*). |
| `43_resolution_dangling_bad` | `{"ok":false,"seq":1,"reason":"schema"}` | §7 & §8 step 7 (*"For `resolution`, a `forecast` member that is not a recorded forecast seq, or one already resolved → **schema**"*). |
| `44_resolution_double_bad` | `{"ok":false,"seq":3,"reason":"schema"}` | §7 & §8 step 7 (*"A `resolution` whose `forecast` is not a recorded forecast seq, or is already resolved, is **schema** (§8 step 7, before the signature)... and a self-resolution of an already-resolved forecast is `schema`"*). |
| `45_forecast_past_bad` | `{"ok":false,"seq":1,"reason":"schema"}` | §5 & §8 step 7 (*"For `forecast`, `resolves_by` earlier than `ts` → **schema**"*). |
| `46a_forecast_permille_0_bad` | `{"ok":false,"seq":1,"reason":"schema"}` | §5 (`forecast.p`: *"integer 1–999"* — 0 refused with `schema`). |
| `46b_forecast_permille_1000_bad` | `{"ok":false,"seq":1,"reason":"schema"}` | §5 (`forecast.p`: *"integer 1–999"* — 1000 refused with `schema`). |
| `47_forecast_boolean_bad` | `{"ok":false,"seq":1,"reason":"schema"}` | §5 (`forecast.p`: *"integer 1–999 (per mille; a boolean is not an integer)"* — `p: true` refused with `schema`). |
| `47b_resolution_outcome_boolean_bad` | `{"ok":false,"seq":2,"reason":"schema"}` | §5 (`resolution.outcome`: *"integer 0 or 1 (a boolean is not an integer)"* — `outcome: true` refused with `schema`). |
| `48_ts_decreased_bad` | `{"ok":false,"seq":1,"reason":"ts_decreased"}` | §7 & §8 step 2a (*"`ts` earlier than the previous entry's `ts` (entry 0 exempt) → **ts_decreased**"*). |
| `48b_ts_decreased_precedes_bad_seq` | `{"ok":false,"seq":1,"reason":"ts_decreased"}` | §8 order of checks: step 2a (`ts_decreased`) precedes step 3 (`bad_seq`), step 4 (`parent_mismatch`), step 5 (`genesis_misplaced`), step 6 (`no_proposer`), step 7 (`schema`), and step 8 (`bad_signature`). |
| `49_self_resolution_bad_signature` | `{"ok":false,"seq":2,"reason":"bad_signature"}` | §7 & §8 steps 8–8a (*"Consequently a self-resolution with a bad signature is `bad_signature`"*). |
| `tests/vectors/score.jsonl` | `{"ok":true,"entries":17}` | §4–§9 end-to-end over genesis, 10 forecasts, and 6 cross-principal resolutions, plus all 17 proper prefixes (§9a.2). |

## Probability of agreement on 10⁵ seeded logs at the first run of record

- **Probability: 0.98 (980 per mille)**.
- **Basis**: Every check order in §8 (steps 1, 2, 2a, 3, 4, 5, 6, 7, 8, 8a, 9, 10), every boundary (`p` in `1..999`, `outcome` in `{0, 1}`, booleans excluded from integers, string comparison of validated `YYYY-MM-DDTHH:MM:SSZ` timestamps for `ts_decreased` and `resolves_by < ts`, dangling/double resolution at step 7 before signature, and `self_judged` by `proposer` at step 8a after signature) is explicitly pinned in `SPEC.md` and exercised against all 40 existing log vectors, `tests/vectors/score.jsonl`, and the 15 C1a signed test logs in `kernel2/`. A 2% residual allowance accounts for any uninspected generator quirk outside this room.

## Retained specification guarantees

- §2: object/array nesting is capped at 32, counting the line object as depth 1.
  The parser refuses before descending into depth 33, bounding recursion even
  for arbitrarily deeper input. Long number tokens are scanned completely for
  JSON syntax but are not converted when longer than 20 characters. Malformed
  JSON, excessive depth and lone surrogates take precedence over noncanonical
  numbers and duplicate members.
- §4 (Q1): timestamps require ASCII digits, years 0001–9999, valid Gregorian
  dates and times, and seconds 00–59. Invalid timestamps yield `schema`.
- §5–6 (Q2): key declarations have exactly four members. Public-key text has
  exactly one ASCII space between its two fields. Base64 must decode to 51
  bytes for a key blob or 180 bytes for an SSHSIG container; these lengths
  require 68 and 240 alphabet characters respectively, with no padding or
  unused bits. Invalid key text yields `schema`; invalid signature containers
  yield `bad_signature` after the entry-shape check.
- §7: the lifetime blob-to-key_id ownership map retains rotated-out keys.
  Signature lookup additionally requires the blob to equal that identity's
  current key. Rotation thus makes the old key `unknown_key` for signing but
  never frees it for another identity; its original identity may restore it.
- §9 (Q3): removed the question helper and all undecided-input error paths.
  Entry validation now returns only a verdict or success. Only I/O failures
  propagate as errors from log checking.
- The launcher builds when its binary is absent/non-executable, or when a
  production Go source, the launcher itself, or `build.sh` is newer than the
  binary. Equal timestamps, unchanged sources, documentation and test files
  do not trigger a rebuild. The existing live reason-code mutation hook is
  preserved, with launcher edits included in freshness checks.

## Running

Requires a locally installed Go toolchain (Go 1.18 or later) and a POSIX shell.
From the project directory:

```sh
kernel2/check path/to/log.jsonl
```

The executable launcher conditionally calls `kernel2/build.sh`, then executes
the cached binary directly so statuses 0, 1, and 2 are preserved. Build steps are fully in
`build.sh`; no module downloads or manual build step are needed. `.cache/` is
gitignored. The directory must be writable when a build is needed.

For every log, stdout is exactly one JSON verdict; status 0 means valid,
1 means refused. Usage and I/O errors write a diagnostic to stderr and return
2. There are no question exits.

Run the test suite, including every supplied vector file and actual
launcher invocations:

```sh
kernel2/test.sh -vet=all
```

## Vector results

The command above **passed** on 2026-10-25, including all Go vet checks enabled
by `-vet=all` and every vector file in `spec/vectors/` and `tests/vectors/`.

| Input | Result |
|---|---|
| `spec/vectors/logs/*.jsonl` against `spec/vectors/verdicts.json` | **40/40 verdicts match**, excluding only `detail`; verified both in-process and through `kernel2/check`, including exit status |
| `tests/vectors/score.jsonl` | **17/17 entries valid** (`{"ok":true,"entries":17}`), plus all 17 proper prefixes (`0..16`), verified both in-process and through `kernel2/check` |
| `spec/vectors/canonical.json` | **6/6** canonical serializations and SHA-256 hashes; **12/12** refusal reasons; genesis-parent constant matches |
| `tests/vectors/rfc8032.json` | **5/5** signature verdicts match |
| `tests/vectors/speccheck.json` | **12/12** signature verdicts match (cases 0–3 valid, 4–11 invalid) |
| `tests/vectors/weak_keys.json` | **12/12** weak keys refused (`8` small-order + `4` non-canonical) |
| `tests/vectors/ssh_keygen_differences.json` | **2/2** named differences (`s_plus_L`, `reserved_nonempty`) refused with `bad_signature` |

Additional passing checks cover:

- Missing/wrong-shaped required fields for the four new types; amendment ID
  boundaries, booleans excluded from activation heights, extra body fields,
  nonempty strings without unstated trimming, and all six decision kinds.
- Duplicate amendment IDs and past/current activation heights rejected before
  malformed signature containers; immediate-next-position and maximum canonical
  activation heights accepted.
- Genesis charter/base initialization, separate promulgation and activation,
  exact activation boundaries, out-of-order heights, historical charter queries,
  latest push replacement, and idempotent transmutation recording.
- Each new type's signature/identity/power failures and absence of governance
  effects on refusal; head updates and inert-entry effects; later-declared
  decision signers and the checker/judge boundary.
- 32 deterministic ordinary signatures compared with `crypto/ed25519`, plus
  32 tampered signatures refused by both implementations.
- Failure precedence, including complete genesis-body schema validation
  before registering any key.
- Key rotation, lifetime ownership, old-key signing refusal, restoration to the
  original identity, future-only effects, refusal when a `key` entry would leave
  no declared key holding the `key` power (tested after weakness and ownership,
  for `key` entries only and never `genesis`), and full self-revocation when
  another declared key still holds `key`.
- Duplicate keys, malformed Unicode, number boundaries, code-point key order,
  object and array depths 31/32/33 and 100,001, 100,000-digit integers,
  malformed-input precedence, and signed lines over 64 KiB.
- Empty files/lines, optional final newline, CRLF refusal, first-failure
  short-circuiting, and refusal stability after appending malformed bytes.
- SSHSIG truncation at every byte boundary, trailing data, oversized wire
  lengths, and invalid base64 alphabet/padding.
- ASCII/calendar timestamp boundaries, leap centuries, single-space pubkey
  syntax, fixed base64 lengths, and verdicts for the former Q1/Q2 inputs.
- CLI usage/I/O status 2 and launcher freshness: initial build, cached reuse,
  equal timestamps, ignored test files, and a rebuild for each production source.
- A local mutation test changes the live `bad_signature` literal in a copy of
  the launcher and observes a changed verdict reason. The normal binary is
  restored afterward. This verifies the hook required by README.md; it is
  not a claim that the inaccessible project pin or differential harness ran.

## Questions and verification scope

`kernel2/QUESTIONS.md` records **none**. No remaining validity ambiguity was
identified during this revision. The historical "four entry types" summary in
§12 item 1 does not override the explicit eight-type list and schemas in §4–5
or the user's instruction to implement them. The §7 transmutation cross-reference
points to §10.11, while the actual judge requirement appears in §10 item 13;
the checker's recording obligation is explicit in §8 step 9.

The emoji illustration in §2 is resolved by the explicit surrogate-pair rule
and `canonical.json`: the canonical bytes use `\ud83d\ude00`.

Only the permitted vector suite and local supplementary tests were exercised.
Agreement on a real project log, the 10^5 simulation seeds, and the project's
actual `checker_drift` pin remains unverified in this restricted workspace.
