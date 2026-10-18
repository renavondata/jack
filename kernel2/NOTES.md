# kernel2 implementation notes

## Author and scope

- Model ID: **`google/gemini-4-argon`** (updating prior `openai/gpt-6-astra` revision).
- Session: this OpenCode revision session in
  `/home/g/git/kernel2-room`, 2026-10-18. The harness did not expose a unique
  session identifier. No commits were made.
- Sources consulted: the current `SPEC.md` in full first, then the existing
  implementation, tests and documentation in `kernel2/`, and the supplied vector
  files under `spec/vectors/` (including `spec/vectors/logs/34_*.jsonl` through `39_*.jsonl`) and `tests/vectors/`.
  This revision read no files outside `/home/g/git/kernel2-room` and no
  first-checker implementation.
- Implementation: Go standard library only. Production verification uses
  independently implemented Edwards arithmetic over `math/big`, canonical
  point decoding, `S < L`, reduced SHA-512 challenge, and the cofactorless
  equation. Small-order public keys are rejected at declaration, not by the
  signature verifier itself. `crypto/ed25519` appears only in tests.
- The checker makes no network, clock, or LLM calls. Its decisions depend on
  the log bytes. The launcher disables Go downloads and telemetry; build
  cache, temporary files, and the executable are confined to `kernel2/.cache/`.

## Changes for the current specification

- §4–5: entry types and key powers accept all eight names: `genesis`, `key`,
  `proposal`, `merge`, `amend`, `push`, `decision`, `spec_conflict`. Empty and
  repeated powers remain valid. The four new body schemas enforce their exact
  required shapes while permitting extra members, including dotted keys.
- §5, §7, §8 step 7: amendments require an ID matching `[A-Z][0-9]{1,3}`, a
  hex64 charter and an integer activation height. Reused IDs and heights not
  strictly greater than the entry's sequence yield `schema` before signature
  parsing. No amendment-number ordering or activation-height ordering is imposed.
- §7, §8 step 9 (`last_key_revocable`): a `key` entry is refused with `bad_key`
  if, with its declaration registered, no declared key's `powers` would include
  `key`. This check runs at §8 step 9 after public-key weakness and lifetime
  blob ownership, applies to `key` entries only (never `genesis`), and does not
  mutate key state (`keys` or `byBlob`) when refused.
- §7, §8 steps 9–10: the folded law now contains the head, current keys and
  lifetime blob ownership, genesis charter, promulgated charter, amendment
  history and IDs, trusted base, and transmuted set. Genesis establishes the
  initial charter and trusted base. A valid amendment immediately updates the
  promulgated charter; `charterAt(position)` selects the latest amendment in
  **log order** with `activate_at <= position`, falling back to genesis.
  Pending amendments cannot displace the active charter, and an older amendment
  activating later cannot override a newer already-active amendment.
- A valid push updates the trusted base immediately. A valid `transmute`
  decision adds its nonempty subject to a set, with repetition harmless; the
  subject need not match an amendment ID or refer to an existing amendment.
  Other decision kinds (`veto`, `promote`, `budget`, `grant`, `fix`), proposals,
  merges and specification conflicts change only the head. In particular,
  a `grant` decision is not a key declaration.
- All new entries use the existing strict SSHSIG/Ed25519 path and current-key
  powers. Effects occur after successful signature verification. The twelve
  reason codes and CLI verdict format are preserved.
- §10's judge-only checks remain outside the validity predicate: the kernel
  accepts an otherwise valid untransmuted amendment, a push during a pending
  amendment, or a decision signed by an empowered key declared after genesis.
  Digest values are claims here; only their shape is checked.
- The vector runner checks every file in `spec/vectors/logs/` against
  `spec/vectors/verdicts.json`, in-process and through the launcher, as well as the
  cryptographic and canonical-JSON vector files under `spec/vectors/` and
  `tests/vectors/`.

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

The command above **passed** on 2026-10-18, including all Go vet checks enabled
by `-vet=all` and every vector file in `spec/vectors/` and `tests/vectors/`.

| Input | Result |
|---|---|
| `spec/vectors/logs/*.jsonl` against `spec/vectors/verdicts.json` | **40/40 verdicts match**, excluding only `detail`; verified both in-process and through `kernel2/check`, including exit status |
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
