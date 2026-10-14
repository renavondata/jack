# kernel2 implementation notes

## Author and scope

- Model ID: **`openai/gpt-6-astra`** (OpenAI family).
- Session: this OpenCode implementation session in
  `/home/g/git/kernel2-room`, 2026-10-14. The harness did not expose a unique
  session identifier. No commits were made.
- Sources consulted: `kernel2/README.md` first, then `SPEC.md` and its named
  vector files under `spec/vectors/` and `tests/vectors/`.
- Implementation: Go standard library only. Production verification uses
  independently implemented Edwards arithmetic over `math/big`, canonical
  point decoding, `S < L`, reduced SHA-512 challenge, and the cofactorless
  equation. Small-order public keys are rejected at declaration, not by the
  signature verifier itself. `crypto/ed25519` appears only in tests.
- The checker makes no network, clock, or LLM calls. Its decisions depend on
  the log bytes. The launcher disables Go downloads and telemetry; build
  cache, temporary files, and the executable are confined to `kernel2/.cache/`.

## Running

Requires a locally installed Go toolchain (Go 1.18 or later) and a POSIX shell.
From the project directory:

```sh
kernel2/check path/to/log.jsonl
```

The executable launcher calls `kernel2/build.sh`, then executes the resulting
binary directly so statuses 0, 1, and 2 are preserved. Build steps are fully in
`build.sh`; no module downloads or manual build step are needed. `.cache/` is
gitignored. The directory must be writable for the build.

For decided inputs, stdout is exactly one JSON verdict; status 0 means valid,
1 means refused. Usage and I/O errors write a diagnostic to stderr and return
2. The exceptions for unresolved specification questions are described below.

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
| `spec/vectors/logs/*.jsonl` against `spec/vectors/verdicts.json` | **24/24 verdicts match**, excluding only `detail`; verified both in-process and through `kernel2/check`, including exit status |
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
- Key rotation, removal of the old blob from current state, future-only
  declaration effects, and self-revocation under previous powers.
- Duplicate keys, malformed Unicode, number boundaries, code-point key order,
  nesting beyond 10,000 levels, and signed lines over 64 KiB.
- Empty files/lines, optional final newline, CRLF refusal, first-failure
  short-circuiting, and refusal stability after appending malformed bytes.
- SSHSIG truncation at every byte boundary, trailing data, oversized wire
  lengths, and invalid base64 alphabet/padding.
- CLI usage/I/O status 2, and explicit stops at unresolved Q1/Q2 inputs.
- A local mutation test changes the live `bad_signature` literal in a copy of
  the launcher and observes a changed verdict reason. The normal binary is
  restored afterward. This verifies the hook required by README.md; it is
  not a claim that the inaccessible project pin or differential harness ran.

## Open questions and implementation boundary

See **`kernel2/QUESTIONS.md`** for section references, exact questions, and
the undecided input classes:

1. **Q1 (§4, §12.4):** ASCII versus Unicode `\d`, regex-only versus calendar
   validation of timestamps, year zero, and leap seconds.
2. **Q2 (§5–6):** whether nonzero unused base64 padding bits must be refused.
3. **Q3 (§9):** how the CLI should report an unresolved specification question.

No validity choice has been made for Q1/Q2. On reaching such a case, the
implementation stops with a question diagnostic on stderr and **no JSON
verdict**. It currently returns status 2; this stop mechanism is explicitly
outside §9's specified usage/I/O-only meaning of status 2 and awaits Q3.
Consequently this is **not yet a total checker for all possible logs**.
None of the supplied vector cases reaches an unresolved boundary.

The emoji illustration in §2 is resolved by the explicit surrogate-pair rule
and `canonical.json`: the canonical bytes use `\ud83d\ude00`.

Only the permitted vector suite and local supplementary tests were exercised.
Agreement on a real project log, the 10^5 simulation seeds, and the project's
actual `checker_drift` pin remains unverified in this restricted workspace.
