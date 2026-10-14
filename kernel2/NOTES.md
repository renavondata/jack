# kernel2 implementation notes

## Author and scope

- Model ID: **`openai/gpt-6-astra`** (OpenAI family).
- Session: this OpenCode revision session in
  `/home/g/git/kernel2-room`, 2026-10-14. The harness did not expose a unique
  session identifier. No commits were made.
- Sources consulted: the current `SPEC.md` in full first, then the existing
  implementation, tests and documentation in `kernel2/`, and the named vector
  files under `spec/vectors/` and `tests/vectors/`. This revision read no files
  outside `/home/g/git/kernel2-room` and no first-checker implementation.
- Implementation: Go standard library only. Production verification uses
  independently implemented Edwards arithmetic over `math/big`, canonical
  point decoding, `S < L`, reduced SHA-512 challenge, and the cofactorless
  equation. Small-order public keys are rejected at declaration, not by the
  signature verifier itself. `crypto/ed25519` appears only in tests.
- The checker makes no network, clock, or LLM calls. Its decisions depend on
  the log bytes. The launcher disables Go downloads and telemetry; build
  cache, temporary files, and the executable are confined to `kernel2/.cache/`.

One revision attempt ran outside the room (in the jack checkout) on 14 Oct and was discarded; it listed directory names but read no file of the first checker.

## Changes for the current specification

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

Run the complete test suite, including every permitted vector file and actual
launcher invocations:

```sh
kernel2/test.sh -vet=all
```

## Vector results

The command above **passed**, including all Go vet checks enabled by
`-vet=all`.

| Input | Result |
|---|---|
| `spec/vectors/logs/*.jsonl` against `spec/vectors/verdicts.json` | **32/32 verdicts match**, excluding only `detail`; verified both in-process and through `kernel2/check`, including exit status |
| `spec/vectors/canonical.json` | **6/6** canonical serializations and SHA-256 hashes; **12/12** refusal reasons; genesis-parent constant matches |
| `tests/vectors/rfc8032.json` | **5/5** valid signatures accepted |
| `tests/vectors/speccheck.json` | **12/12** outcomes match: cases 0–3 accepted, 4–11 refused |
| `tests/vectors/weak_keys.json` | **12/12** public keys classified weak |
| `tests/vectors/ssh_keygen_differences.json` | **2/2** named differences exercised through the corresponding signed log fixtures: `S + L` and nonempty reserved field both yield `bad_signature` |

The last file contains descriptions and references rather than signature
bytes. Tests consume it and map its two names to supplied log fixtures 13 and
15; they do not inspect its referenced Python tests or invoke ssh-keygen.

Additional passing checks cover:

- 32 deterministic ordinary signatures compared with `crypto/ed25519`, plus
  32 tampered signatures refused by both implementations.
- Failure precedence, including complete genesis-body schema validation
  before registering any key.
- Key rotation, lifetime ownership, old-key signing refusal, restoration to the
  original identity, future-only effects, and self-revocation under previous powers.
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

`kernel2/QUESTIONS.md` now records **none**. The current specification resolves
Q1–Q3, and no remaining validity ambiguity was identified during this revision.

The emoji illustration in §2 is resolved by the explicit surrogate-pair rule
and `canonical.json`: the canonical bytes use `\ud83d\ude00`.

Only the permitted vector suite and local supplementary tests were exercised.
Agreement on a real project log, the 10^5 simulation seeds, and the project's
actual `checker_drift` pin remains unverified in this restricted workspace.
