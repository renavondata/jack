google/gemini-4-argon

# Findings (Most Serious First)

### 1. DIVERGES — Non-zero unused base64 padding bits in `pubkey` or `sig` abort with exit status 2 (`Q2`) instead of refusing with `schema` or `bad_signature`
- **Spec sections:** §5 (`SPEC.md:96-99`), §6 (`SPEC.md:111-125`), §8 steps 7–8 (`SPEC.md:194-199`), §9 (`SPEC.md:208-223`)
- **Code:** `kernel2/signature.go:12-14`, `kernel2/signature.go:18-32` (`decodeBase64`, specifically lines `28-30`), called from `kernel2/signature.go:86` (`parsePublicText`) and `kernel2/signature.go:97` (`parseSignature`), propagated via `kernel2/checker.go:106-109,125-128,133-134,204-207,218-221,273-276` and `kernel2/main.go:21-25`
- **Issue:** When `s` is valid standard base64 whose final padded quantum has non-zero unused padding bits (`base64.StdEncoding.EncodeToString(b) != s`), `decodeBase64` returns `question("Q2", "nonzero unused base64 padding bits")`. `main.go:21-25` prints this error to `stderr`, writes **no JSON** to `stdout`, and exits with status `2`.
  However, there is **no ambiguity** in the verdict or reason code under `SPEC.md` for any such input:
  1. Unused base64 padding bits can exist *only* when the base64 string has `=` or `==` padding, which decodes to a byte slice of length $3k + 2$ or $3k + 1$ ($\not\equiv 0 \pmod 3$).
  2. In §5 (`pubkey`), the decoded blob must be **exactly 51 bytes** (`string("ssh-ed25519") ‖ string(32 bytes)` = $15 + 36 = 51$). Because $51 = 3 \times 17 \equiv 0 \pmod 3$, a 51-byte blob never has `=` padding. Whether non-zero padding bits are rejected by base64 decoding or accepted by base64 decoding and rejected by the 51-byte wire check (`publicFromBlob` at `signature.go:75-79`), any `pubkey` with non-zero padding bits **must** be refused at §8 step 7 with `reason: "schema"` and exit status `1`.
  3. In §6 (`sig`), a valid SSHSIG blob has fixed length `"SSHSIG"` (6) + `uint32 1` (4) + `string(pubkey blob)` ($4+51=55$) + `string("core-entry")` ($4+10=14$) + `string("")` ($4+0=4$) + `string("sha512")` ($4+6=10$) + `string(inner)` ($4+15+68=87$) = **180 bytes**. Because $180 = 3 \times 60 \equiv 0 \pmod 3$, a valid SSHSIG blob never has `=` padding. Whether non-zero padding bits are rejected as "bad base64" or accepted by base64 decoding and rejected as wrong wire length/structure in §6, any `sig` with non-zero padding bits **must** be refused at §8 step 8 with `reason: "bad_signature"` and exit status `1`.
  4. Returning an error also breaks §8 check ordering when combined with another defect (e.g. `genesis.body.keys` having `"pubkey":"ssh-ed25519 AB=="` in element 0 and `{}` in element 1, or a `key` entry having `"sig":"AB=="` at step 8 and a weak key at step 9).
- **Inputs demonstrating divergence:**
  - `pubkey`:
    ```json
    {"body":{"charter":"1111111111111111111111111111111111111111111111111111111111111111","checker":"1111111111111111111111111111111111111111111111111111111111111111","keys":[{"key_id":"k","powers":[],"principal":"p","pubkey":"ssh-ed25519 AB=="}]},"parent":"0000000000000000000000000000000000000000000000000000000000000000","proposer":"p","seq":0,"sig":"AA==","ts":"2026-10-14T00:00:00Z","type":"genesis"}
    ```
    `SPEC.md` requires exit `1` and stdout `{"ok":false,"seq":0,"reason":"schema",...}`. `kernel2` exits `2` with empty stdout.
  - `sig`:
    ```json
    {"body":{"charter":"1111111111111111111111111111111111111111111111111111111111111111","checker":"1111111111111111111111111111111111111111111111111111111111111111","keys":[]},"parent":"0000000000000000000000000000000000000000000000000000000000000000","proposer":"p","seq":0,"sig":"AB==","ts":"2026-10-14T00:00:00Z","type":"genesis"}
    ```
    `SPEC.md` requires exit `1` and stdout `{"ok":false,"seq":0,"reason":"bad_signature",...}`. `kernel2` exits `2` with empty stdout.

### 2. DIVERGES — Regex-matching timestamps outside `0001..9999` Gregorian calendar / `00..59` time bounds or with escaped Unicode digits abort with exit status 2 (`Q1`), violating §9 and preempting §8 steps 3–9
- **Spec sections:** §4 (`SPEC.md:73`), §8 steps 2–9 (`SPEC.md:189-201`), §9 (`SPEC.md:208-223`), §12.4 (`SPEC.md:268-270`)
- **Code:** `kernel2/checker.go:19-20`, `kernel2/checker.go:27-45` (`timestampShape`), `kernel2/checker.go:69` (`entryShape`), `kernel2/checker.go:183-186` (`checkEntry`), `kernel2/checker.go:273-276` (`checkLog`), `kernel2/main.go:21-25` (`run`)
- **Issue:**
  1. `SPEC.md §4` specifies the `ts` requirement as `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z` with parenthetical note `(a UTC timestamp; the checker never reads a clock and does not order timestamps at C0)`, and §12.4 states "`ts` is a UTC string whose order is not checked at C0".
  2. When `m["ts"]` matches `digitTimestamp` (`^[\p{Nd}]{4}-[\p{Nd}]{2}-[\p{Nd}]{2}T[\p{Nd}]{2}:[\p{Nd}]{2}:[\p{Nd}]{2}Z$`) and either contains non-ASCII Unicode digits (via `\uXXXX` escapes in canonical JSON) or has `y == 0`, `m` outside `1..12`, `d` outside `1..daysInMonth(y, m)`, `hour > 23`, `minute > 59`, or `second > 59`, `timestampShape` returns `question("Q1", ...)`, causing `kernel2/check` to exit with status `2` and no JSON on `stdout`.
  3. This violates §9, which restricts exit status `2` (without JSON) to usage or I/O errors.
  4. It also breaks §8 check ordering when an entry has both a `Q1` timestamp and a defect at steps 3–9 (`bad_seq`, `parent_mismatch`, `genesis_misplaced`, `no_proposer`, body `schema`, `bad_key`, `bad_signature`, `unknown_key`, `proposer_mismatch`, `no_power`): under the regex-only reading of §4, `ts` is valid at step 2 and the later step's reason code must be returned (or `ok: true` if valid); under a calendar/ASCII-digit reading of §4, `reason: "schema"` (exit status `1`) must be returned at step 2. `kernel2` returns neither.
- **Inputs demonstrating divergence:**
  ```json
  {"body":{},"parent":"0000000000000000000000000000000000000000000000000000000000000000","proposer":"","seq":5,"sig":"AA==","ts":"2026-02-30T00:00:00Z","type":"proposal"}
  ```
  and
  ```json
  {"body":{},"parent":"0000000000000000000000000000000000000000000000000000000000000000","proposer":"","seq":5,"sig":"AA==","ts":"\u0662\u0660\u0662\u0666-10-14T00:00:00Z","type":"proposal"}
  ```
  `SPEC.md` requires exit `1` with JSON (`reason: "bad_seq"` if `ts` passes §4, or `reason: "schema"` if `ts` fails §4). `kernel2` exits `2` with no JSON on stdout.

### 3. DIVERGES — `kernel2/check` unconditionally runs `go build` into `kernel2/.cache/check` on every invocation
- **Spec sections:** §9 (`SPEC.md:208-219`), §10 steps 1 & 5 (`SPEC.md:230-244`), `kernel2/README.md:28-31`
- **Code:** `kernel2/check:8-9`, `kernel2/build.sh:4,10-13`
- **Issue:**
  1. `kernel2/check` runs `"$dir/build.sh" bad_signature || exit 2` on every invocation instead of only building in `build.sh` (or when the binary is absent). If `kernel2/` is on a read-only mount or non-writable directory, `kernel2/check` fails with exit status `2` and no JSON output even when `.cache/check` was already built.
  2. Creating/updating files under `kernel2/.cache/` at runtime writes inside `kernel2/`, which `SPEC.md §10` step 1 lists as a `trusted_path` directory ("every file under `kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and the file `SPEC.md`").
  3. Concurrent runs of `kernel2/check` overwrite `$dir/.cache/check` in place while sibling processes execute it.
  4. Invoking `go build` on every run adds ~100 ms per invocation (~3 hours for the $10^5$-seed differential run described in `README.md:39-40`).
- **Input demonstrating divergence:** Running `kernel2/check spec/vectors/logs/23_empty.jsonl` when `kernel2/` is read-only (`chmod -w kernel2 kernel2/.cache`) exits `2` instead of `0` with `{"ok":true,"entries":0}`.

### 4. AMBIGUOUS — Re-use of a replaced `pubkey` blob by a different `key_id` after key rotation
- **Spec section:** §7 (`SPEC.md:167-176`)
- **Code:** `kernel2/checker.go:155-162` (`law.declare`)
- **Ambiguity:** §7 defines state as "a map key_id → (principal, pubkey blob, powers)", states "A later declaration of the same key_id replaces the earlier", and states "A declaration is refused with **bad_key** if its public key is weak (§6), or if its pubkey blob equals that of a *different* key_id already declared (one key, one identity)."
  - **Reading picked by `kernel2` (`checker.go:158-160`):** When `d.id` is re-declared, `delete(s.byBlob, string(previous.blob))` removes its previous pubkey blob. Thus "already declared" checks only the current active `keys` map, allowing a different `key_id` to later claim the retired pubkey blob.
  - **Alternative reading:** "already declared (one key, one identity)" tracks all `(pubkey blob → key_id)` bindings ever declared in entries $0..i-1$, refusing with `bad_key` if `key_2` later declares a pubkey blob previously used by `key_1`.

### 5. AMBIGUOUS — Extra members in key declaration objects inside `genesis.body.keys`
- **Spec section:** §5 (`SPEC.md:81-100`)
- **Code:** `kernel2/checker.go:78-111` (`keyShape`)
- **Ambiguity:** §5 states "Required members per type; **extra members are allowed** (any keys, any depth, including keys containing `.`)" and "A **key declaration** is an object with `key_id`: ...; `principal`: ...; `powers`: ...; `pubkey`: ...".
  - **Reading picked by `kernel2` (`checker.go:78-111`):** Extra fields are allowed in any key declaration object, both when it is the `body` of a `key` entry and when it is an element of `genesis.body.keys`.
  - **Alternative reading:** Extra fields are allowed on `body` (so on a `key` entry's body), while key declaration objects inside `genesis.body.keys` are restricted to the four named keys (`else schema`).

### 6. AMBIGUOUS — Single ASCII space vs general whitespace splitting in `pubkey`
- **Spec section:** §5 (`SPEC.md:96-98`)
- **Code:** `kernel2/signature.go:81-85` (`parsePublicText`)
- **Ambiguity:** §5 defines `pubkey` as "a string of exactly two space-separated fields, the first `ssh-ed25519`, the second standard base64 (with padding)".
  - **Reading picked by `kernel2` (`signature.go:82`):** `strings.Split(s, " ")` requires a single `0x20` space character separating the two fields and rejects multiple spaces or leading/trailing spaces with `schema`.
  - **Alternative reading:** Splitting on arbitrary whitespace runs (e.g. Python `s.split()` without arguments or Go `strings.Fields`) would accept multiple spaces or tabs between `ssh-ed25519` and the base64 field.

---

# 1. Section-by-Section Review Against `SPEC.md`

## §1. The log file (`SPEC.md:22-30`)
- **Sequence of bytes; lines separated by `0x0A`; final `0x0A` optional; empty file has 0 lines:**
  - **ENFORCED:** `kernel2/checker.go:265-272`. `bufio.Reader.ReadBytes('\n')` reads up to `0x0A`; returns `{"ok": true, "entries": seq}` when `err == io.EOF && len(line) == 0` (handling both a 0-byte empty file and the EOF immediately following a trailing `0x0A`), and strips a single trailing `\n` via `bytes.TrimSuffix(line, []byte{'\n'})` (so a final line without `0x0A` is processed identically, while `\r\n` leaves `\r` to fail canonicalization).
- **Line decoded as UTF-8; invalid UTF-8 bytes → `malformed_json`:**
  - **ENFORCED:** `kernel2/canonical.go:241-243`, `kernel2/checker.go:179-182`. `utf8.Valid(line)` rejects ill-formed UTF-8 (including raw UTF-8 encoded surrogates) with `"malformed_json"`.
- **Line $i$ (0-based) is entry $i$; empty log is valid `{"ok":true,"entries":0}`:**
  - **ENFORCED:** `kernel2/checker.go:263,269-270,281`. `seq` starts at `0` and increments after each valid line; an empty reader returns `{"ok": true, "entries": int64(0)}`.
- **Entries checked in order; first failure determines verdict; nothing after it is examined:**
  - **ENFORCED:** `kernel2/checker.go:273-279`. `checkLog` checks each line as it is read and returns immediately on the first non-nil `verdict` without reading subsequent lines.

## §2. Canonical JSON (`SPEC.md:32-56`)
- **Every line must be the exact canonical serialisation of the JSON object it denotes; else `not_canonical`:**
  - **ENFORCED:** `kernel2/canonical.go:240-255,290-331`. `parseCanonical` parses the line into an `object` and checks `p.noncanonical || !bytes.Equal(canonical(m), line)`.
- **Object `{` members `}` separated by `,`, `"key":value`, keys sorted by Unicode code point of key string (not escaped form), no whitespace; array `[` values `]`:**
  - **ENFORCED:** `kernel2/canonical.go:292-317`. `sort.Strings(keys)` sorts valid UTF-8 strings by byte order, which is identical to Unicode scalar value (code-point) order of the unescaped key string. No whitespace is emitted.
- **Values are objects, arrays, strings, integers, `true`, `false`, `null`; numbers are integers only, optional `-`, no leading zeros, no fraction, no exponent, $|n| \le 2^{53}-1$ (`9007199254740991`); `-0`, `1.0`, `1e3`, and larger magnitudes are `not_canonical`:**
  - **ENFORCED:** `kernel2/canonical.go:118-160,162-238`. Leading zeros (`01`, `-01`) fail JSON syntax (`malformed_json`); fractions, exponents, `-0`, and integers outside `[-9007199254740991, 9007199254740991]` (including `strconv.ParseInt` overflow) set `p.noncanonical = true` (`not_canonical`).
- **Strings are ASCII-only: `\"`, `\\`, `\b`, `\f`, `\n`, `\r`, `\t`; all other code points outside `U+0020..U+007E` → `\uXXXX` lowercase hex, `> U+FFFF` as UTF-16 surrogate pair; `/` not escaped:**
  - **ENFORCED:** `kernel2/canonical.go:55-114,257-288`. `text()` rejects raw bytes `< 0x20` as `malformed_json` and decodes escapes; `appendText()` formats canonical escapes using `"0123456789abcdef"` and `utf16.EncodeRune`, leaving `0x20..0x7E` (including `/`) unescaped. Any deviation in input bytes fails `bytes.Equal(canonical(m), line)` with `not_canonical`.
- **Lone surrogate (`\uD800`..`\uDFFF` not forming a valid pair) → `malformed_json`:**
  - **ENFORCED:** `kernel2/canonical.go:96-107`. A high surrogate `0xD800..0xDBFF` not immediately followed by `\u` and a low surrogate `0xDC00..0xDFFF`, or an unpaired low surrogate `0xDC00..0xDFFF`, returns a parse error (`malformed_json`).
- **Duplicate keys in an object → `not_canonical`:**
  - **ENFORCED:** `kernel2/canonical.go:191-194`. Checks `_, exists := m[key]` on the unescaped key string and sets `p.noncanonical = true`.
- **Order of checks within one line (not valid JSON / not an object / lone surrogate → `malformed_json`; then non-integer or out-of-range number → `not_canonical`; then re-serialise and compare → `not_canonical`):**
  - **ENFORCED:** `kernel2/canonical.go:155-158,191-194,240-255`. `p.number()` and duplicate-key handling only flag `p.noncanonical = true` and continue parsing the full line, so any syntax error, non-object root, trailing tokens, or lone surrogate anywhere on the line returns `malformed_json` before `p.noncanonical` or `bytes.Equal` is consulted.

## §3. Hash chain (`SPEC.md:58-62`)
- **`parent` of entry $i \ge 1$ is lowercase hex SHA-256 of bytes of line $i-1$ (without line terminator); `parent` of entry 0 is 64 `0`s; `seq` of entry $i$ is $i$:**
  - **ENFORCED:** `kernel2/checker.go:190-195,262-263,272,280-281`.

## §4. Entry shape (`SPEC.md:64-78`)
- **Entry object has *exactly* keys `seq, parent, ts, type, proposer, body, sig` (else `schema`):**
  - **ENFORCED:** `kernel2/checker.go:47-55,183-189`.
- **`seq`: integer $\ge 0$ (not a boolean):**
  - **ENFORCED:** `kernel2/checker.go:25,56`. `nonnegative` requires type `jsonInteger` with `n >= 0`.
- **`parent`: `[0-9a-f]{64}`:**
  - **ENFORCED:** `kernel2/checker.go:15,24,56`.
- **`ts`: `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z`:**
  - **DIVERGES / AMBIGUOUS:** `kernel2/checker.go:19-20,27-45,69,183-186`. See **Finding 2**: strings outside both regexes return `schema`, ordinary Gregorian ASCII timestamps in years `0001..9999` with seconds `00..59` are accepted, and regex-matching strings outside that subset abort with exit status `2` (`Q1`) and no JSON output.
- **`type`: one of `genesis key proposal merge`:**
  - **ENFORCED:** `kernel2/checker.go:23,59-61`.
- **`proposer`: a string (emptiness checked at §8 step 6):**
  - **ENFORCED:** `kernel2/checker.go:63-65`.
- **`body`: an object:**
  - **ENFORCED:** `kernel2/checker.go:66-68`.
- **`sig`: `[A-Za-z0-9+/]+={0,2}` (decoded in §6):**
  - **ENFORCED:** `kernel2/checker.go:18,24,56`.

## §5. Body schemas (`SPEC.md:79-104`)
- **Required members per type; extra members allowed (any keys, any depth, including `.`); wrong shape → `schema`:**
  - **ENFORCED (with AMBIGUOUS note on `genesis.keys` sub-objects):** `kernel2/checker.go:78-142,204-210`. See **Finding 5**.
  - `genesis` (`charter`: hex64, `checker`: hex64, `keys`: array of key declarations): `kernel2/checker.go:115-131`.
  - `key` (a key declaration): `kernel2/checker.go:132-134`.
  - `proposal` (`title`: string, `commit`: hex40): `kernel2/checker.go:135-137`.
  - `merge` (`proposal`: integer $\ge 0$ not boolean, `commit`: hex40, `checker`: hex64): `kernel2/checker.go:138-140`.
- **Key declaration shape (`key_id`: `[a-z0-9_-]{1,64}`, `principal`: non-empty string, `powers`: array of entry-type names, possibly empty, repetition allowed, `pubkey`: two space-separated fields `ssh-ed25519` + standard base64 decoding to 51 bytes `string("ssh-ed25519") ‖ string(32 bytes)`):**
  - **ENFORCED for `key_id`, `principal`, `powers`, wire format:** `kernel2/checker.go:17,78-111`, `kernel2/signature.go:75-92`.
  - **AMBIGUOUS for space splitting:** `kernel2/signature.go:82` (`strings.Split(s, " ")`). See **Finding 6**.
  - **DIVERGES for base64 with non-zero unused padding bits:** `kernel2/signature.go:28-30,86-89`. Aborts with exit status `2` (`Q2`) instead of refusing with `schema`. See **Finding 1**.

## §6. Signatures (`SPEC.md:106-163`)
- **Signed message is UTF-8 bytes of canonical serialisation of entry object without `sig`:**
  - **ENFORCED:** `kernel2/checker.go:243-249`.
- **Container format (`"SSHSIG" ‖ uint32 1 ‖ string(pubkey blob) ‖ string("core-entry") ‖ string("") ‖ string("sha512") ‖ string(inner)` and nothing after; `inner = string("ssh-ed25519") ‖ string(64 bytes)`; `pubkey blob = string("ssh-ed25519") ‖ string(32 bytes)`), any deviation → `bad_signature`:**
  - **ENFORCED for wire format, alphabet, and padding structure:** `kernel2/signature.go:18-27,34-79,96-118`, `kernel2/checker.go:218-224`.
  - **DIVERGES for base64 with non-zero unused padding bits:** `kernel2/signature.go:28-30,97-100`. Aborts with exit status `2` (`Q2`) instead of refusing with `bad_signature`. See **Finding 1**.
- **Signed data (`"SSHSIG" ‖ string("core-entry") ‖ string("") ‖ string("sha512") ‖ string(SHA-512(message))`):**
  - **ENFORCED:** `kernel2/signature.go:120-127`.
- **Strict Ed25519 verification (steps 1–4) and weak-key predicate (`decodePoint` failure or $[8]A = (0,1)$):**
  - **ENFORCED:** `kernel2/ed25519.go:19-143`. Detailed in Section 3 below.

## §7. The law in force (`SPEC.md:165-182`)
- **State is head hash and `keys` map; later declaration of same `key_id` replaces earlier:**
  - **ENFORCED:** `kernel2/checker.go:144-164,262`.
- **Refused with `bad_key` if public key is weak (§6) or if pubkey blob equals that of a different `key_id` already declared; weakness tested first:**
  - **ENFORCED (with AMBIGUOUS note on retired pubkey blobs after rotation):** `kernel2/checker.go:151-157`. `weakKey(d.public)` is checked at line `152` before `s.byBlob[string(d.blob)]` at line `155`. See **Finding 4**.
- **Genesis is self-certifying: keys registered in array order before signature check:**
  - **ENFORCED:** `kernel2/checker.go:211-217` runs before `parseSignature` at `checker.go:218`.
- **A `key` entry at $i$ governs entries $> i$, never itself:**
  - **ENFORCED:** `kernel2/checker.go:252-256` registers a `key` entry's declaration at step 9, after step 8 signature verification.

## §8. The validity predicate (`SPEC.md:184-204`)
- **Exact 10-step check order per entry:**
  - **ENFORCED except when `Q1` or `Q2` aborts execution:** `kernel2/checker.go:177-282`. Detailed in Section 2 below.

## §9. Output: the CLI contract (`SPEC.md:206-223`)
- **One argument (log path), one JSON object on stdout (`{"ok":true,"entries":N}` or `{"ok":false,"seq":n,"reason":"<code>","detail":"<free text>"}`), exit 0 if ok, 1 if refused, 2 on usage or I/O error, closed set of 12 reason codes:**
  - **ENFORCED for decided inputs and usage/I/O errors:** `kernel2/check:4-9`, `kernel2/main.go:10-36`, `kernel2/checker.go:170-175,270`.
  - **DIVERGES on `Q1`/`Q2` inputs and read-only `kernel2/` directory:** Exits `2` with no JSON on stdout (see **Findings 1, 2, 3**).

---

# 2. Check Order Verification (`SPEC.md §2` and `§8`)

1. **Within §8 Step 1 (`malformed_json` before `not_canonical`, `SPEC.md:53-56`):**
   - `parseCanonical` (`kernel2/canonical.go:240-255`) checks UTF-8 validity first (`line 241`), then parses the full JSON value (`line 245`). Non-integer/out-of-range numbers (`line 156`) and duplicate object keys (`line 192`) only set `p.noncanonical = true` without halting parsing, whereas syntax errors and lone surrogates (`lines 98, 102, 106`) return an error. `err != nil || p.i != len(line) || !ok` (`line 248`) is checked before `p.noncanonical || !bytes.Equal(canonical(m), line)` (`line 251`).
   - Thus any combination of a `not_canonical` defect and a `malformed_json` defect on the same line always resolves to `malformed_json`.
2. **Across §8 Steps 1–10 (`kernel2/checker.go:177-282`):**
   - Step 1 (`malformed_json` / `not_canonical`): `checker.go:179-182`
   - Step 2 (§4 `schema`): `checker.go:183-189`
   - Step 3 (`bad_seq`): `checker.go:190-192`
   - Step 4 (`parent_mismatch`): `checker.go:193-195`
   - Step 5 (`genesis_misplaced`): `checker.go:196-199`
   - Step 6 (`no_proposer`): `checker.go:200-203`
   - Step 7 (§5 `schema`, then `genesis` key registration → `bad_key`): `checker.go:204-217`. Note that `bodyShape` (`checker.go:123-130`) validates the §5 schema of *every* declaration in `genesis.body.keys` before `checkEntry` (`checker.go:211-217`) registers any declaration, so a `genesis` entry with a weak first key and a schema-invalid second key yields `schema` rather than `bad_key`.
   - Step 8 (`bad_signature` container → `unknown_key` → `proposer_mismatch` → `no_power` → `bad_signature` Ed25519): `checker.go:218-251`
   - Step 9 (`key` registration → `bad_key`): `checker.go:252-256`
   - Step 10 (advance `parent` and `seq`): `checker.go:280-281`
   - **Order divergences:** Only those caused by `Q1` at step 2 (`checker.go:69,184-186`) and `Q2` at steps 7 and 8 (`signature.go:28-30`, `checker.go:204-207,218-221`), where `kernel2` aborts with exit status `2` instead of returning the first applicable reason code in §8 order (see **Findings 1 and 2**).

---

# 3. Ed25519 Verification Audit (`kernel2/ed25519.go`)

- **`S >= L` refused:** **ENFORCED** at `kernel2/ed25519.go:21,125-128`. `s := littleInteger(signature[32:])`; `if s.Cmp(orderL) >= 0 { return false }`.
- **Non-canonical encodings of `A` and `R` refused:** **ENFORCED** at `kernel2/ed25519.go:80-111,129-136`. `decodePoint` checks `y.Cmp(fieldP) >= 0` (`line 88`, rejecting $y \ge p$), checks that $u/v$ is a quadratic residue (`lines 96-103`), and checks `if x.Sign() == 0 && sign == 1 { return point{}, false }` (`line 104`, rejecting $x = 0$ with sign bit 1). Both `public` ($A$) and `signature[:32]` ($R$) are decoded via `decodePoint`.
- **Small-order public keys refused at declaration, not in the verifier:** **ENFORCED** at `kernel2/ed25519.go:113-119` and `kernel2/checker.go:151-154`. `weakKey` returns `true` iff `decodePoint` fails or `[8]A` encodes to the identity point (`encodePoint(scalarMultiply(p, big.NewInt(8))) == encodePoint(identity())`). `weakKey` is called in `law.declare` (`checker.go:152`) and is not called in `verifyEd25519` (`ed25519.go:121-143`).
- **`k` reduced mod `L`:** **ENFORCED** at `kernel2/ed25519.go:137-141`. Computes `SHA-512(R ‖ public ‖ message)`, interprets the 64-byte digest as a little-endian integer via `littleInteger`, and reduces modulo $L$ via `new(big.Int).Mod(..., orderL)`.
- **Cofactorless equation `[S]B = R + [k]A`:** **ENFORCED** at `kernel2/ed25519.go:48-66,142`. Uses complete twisted Edwards extended coordinates $(X:Y:Z:T)$ with $a=-1$ and compares canonical point encodings: `bytes.Equal(encodePoint(scalarMultiply(basePoint, s)), encodePoint(pointAdd(r, scalarMultiply(a, k))))`.
- **No use of a library verifier for the decision:** **ENFORCED**. `kernel2/ed25519.go` uses only `bytes`, `crypto/sha512`, and `math/big`. `crypto/ed25519` is imported only in `kernel2/checker_test.go:5` and `kernel2/vectors_test.go:5`.

---

# 4. Canonical-JSON Handling Audit (`kernel2/canonical.go`)

- **Key order:** **ENFORCED** (`kernel2/canonical.go:292-308`). Object keys are unescaped into valid UTF-8 Go `string`s and sorted with `sort.Strings(keys)`. Because UTF-8 is order-preserving with respect to Unicode scalar values, this sorts by Unicode code point of the unescaped key string (not by escaped text and not by UTF-16 code units).
- **Escapes (including `> U+007E` and lone surrogates):** **ENFORCED** (`kernel2/canonical.go:38-114,257-288`).
  - Unescaped control bytes `< 0x20` are rejected in `text()` (`line 66`) as `malformed_json`.
  - High surrogates `0xD800..0xDBFF` must be followed immediately by `\u` and a low surrogate `0xDC00..0xDFFF` (`lines 96-104`), and standalone low surrogates `0xDC00..0xDFFF` are rejected (`lines 105-107`), all producing `malformed_json`.
  - `appendText()` (`lines 257-288`) formats `\"`, `\\`, `\b`, `\f`, `\n`, `\r`, `\t`, leaves `0x20..0x7E` (including `/`) unescaped, escapes all other BMP code points (`0x00..0x1F`, `0x7F`, `0x80..0xFFFF`) as `\uXXXX` with lowercase hex, and encodes supplementary code points (`> U+FFFF`) via `utf16.EncodeRune` as a pair of lowercase `\uXXXX` escapes. Any input line with raw UTF-8 `> U+007E`, raw `0x7F`, uppercase hex in `\uXXXX`, `\/`, or unnecessary `\uXXXX` escapes fails `bytes.Equal(canonical(m), line)` (`line 251`) with `not_canonical`.
- **Integers only and their bounds:** **ENFORCED** (`kernel2/canonical.go:118-160`). Leading zeros (`01`, `-01`) fail JSON syntax (`malformed_json`). Fractions, exponents, `-0`, and integers outside `[-9007199254740991, 9007199254740991]` set `p.noncanonical = true` (`not_canonical`) while allowing the parser to continue so later `malformed_json` errors still take precedence.
- **Duplicate keys:** **ENFORCED** (`kernel2/canonical.go:191-194`). Checked on the unescaped key string (`_, exists := m[key]`), catching both identical raw keys and escape-equivalent keys (e.g. `"a"` and `"\u0061"`) and flagging `p.noncanonical = true` (`not_canonical`).
- **Final newline:** **ENFORCED** (`kernel2/checker.go:265-272`). `ReadBytes('\n')` + `bytes.TrimSuffix(line, []byte{'\n'})` makes the final `0x0A` optional, treats a 0-byte file as 0 entries, and treats empty lines (`\n` at start or `\n\n`) as `malformed_json`.

---

# 5. Execution of `kernel2/check` Over `spec/vectors/logs/`

`kernel2/check` was run over all 24 files in `spec/vectors/logs/*.jsonl` and compared against `spec/vectors/verdicts.json` (plus exit codes `0` for `ok: true` and `1` for `ok: false`):

- **24 / 24 files matched `spec/vectors/verdicts.json` (0 mismatches).**

| Log file | Expected & actual verdict (minus `detail`) | Exit |
|---|---|---|
| `00_genesis_only.jsonl` | `{"ok":true,"entries":1}` | 0 |
| `01_every_type_grant_revoke.jsonl` | `{"ok":true,"entries":7}` | 0 |
| `02_revoked_key_no_power.jsonl` | `{"ok":false,"seq":7,"reason":"no_power"}` | 1 |
| `03_redeclared_powers.jsonl` | `{"ok":true,"entries":9}` | 0 |
| `04_duplicate_pubkey_bad_key.jsonl` | `{"ok":false,"seq":1,"reason":"bad_key"}` | 1 |
| `05_small_order_key_bad_key.jsonl` | `{"ok":false,"seq":1,"reason":"bad_key"}` | 1 |
| `06_noncanonical_key_bad_key.jsonl` | `{"ok":false,"seq":1,"reason":"bad_key"}` | 1 |
| `07_genesis_weak_key_bad_key.jsonl` | `{"ok":false,"seq":0,"reason":"bad_key"}` | 1 |
| `08_no_power.jsonl` | `{"ok":false,"seq":1,"reason":"no_power"}` | 1 |
| `09_unknown_key.jsonl` | `{"ok":false,"seq":1,"reason":"unknown_key"}` | 1 |
| `10_proposer_mismatch.jsonl` | `{"ok":false,"seq":1,"reason":"proposer_mismatch"}` | 1 |
| `11_no_proposer.jsonl` | `{"ok":false,"seq":1,"reason":"no_proposer"}` | 1 |
| `12_bad_signature_tampered.jsonl` | `{"ok":false,"seq":1,"reason":"bad_signature"}` | 1 |
| `13_bad_signature_s_plus_L.jsonl` | `{"ok":false,"seq":1,"reason":"bad_signature"}` | 1 |
| `14_bad_signature_namespace.jsonl` | `{"ok":false,"seq":1,"reason":"bad_signature"}` | 1 |
| `15_bad_signature_reserved.jsonl` | `{"ok":false,"seq":1,"reason":"bad_signature"}` | 1 |
| `16_bad_seq.jsonl` | `{"ok":false,"seq":2,"reason":"bad_seq"}` | 1 |
| `17_parent_mismatch_fork.jsonl` | `{"ok":false,"seq":2,"reason":"parent_mismatch"}` | 1 |
| `18_genesis_misplaced.jsonl` | `{"ok":false,"seq":2,"reason":"genesis_misplaced"}` | 1 |
| `19_schema.jsonl` | `{"ok":false,"seq":2,"reason":"schema"}` | 1 |
| `20_schema_rule_type_gone.jsonl` | `{"ok":false,"seq":2,"reason":"schema"}` | 1 |
| `21_not_canonical.jsonl` | `{"ok":false,"seq":1,"reason":"not_canonical"}` | 1 |
| `22_malformed_json.jsonl` | `{"ok":false,"seq":1,"reason":"malformed_json"}` | 1 |
| `23_empty.jsonl` | `{"ok":true,"entries":0}` | 0 |

---

# 6. Spec Rules That No Vector Exercises

Across all vector files in `spec/vectors/` (`canonical.json`, `verdicts.json`, `logs/*.jsonl`) and `tests/vectors/` (`rfc8032.json`, `speccheck.json`, `weak_keys.json`, `ssh_keygen_differences.json`), the following rules in `SPEC.md` are never exercised:

### §1. The log file
1. **Non-empty log without a final `0x0A` (`SPEC.md:24-25`):** All 23 non-empty files in `spec/vectors/logs/*.jsonl` end with `0x0A`.
2. **Invalid UTF-8 bytes in a line → `malformed_json` (`SPEC.md:25-26`):** Every vector file is valid UTF-8.
3. **Nothing after the first failing entry is examined (`SPEC.md:28-30`):** Every refused log in `spec/vectors/logs/*.jsonl` fails on its final line; none has trailing entries after the first failed entry.

### §2. Canonical JSON
4. **Code-point key order vs escaped-form or UTF-16 order (`SPEC.md:38-39`):** No vector tests object keys whose Unicode code-point order differs from their escaped ASCII order (e.g. `"\b"` vs `"a"`, or `"\""` vs `"\\"`), or differs from UTF-16 code-unit order (e.g. BMP `U+E000` `\ue000` vs supplementary `U+10000` `\ud800\udc00`).
5. **Boolean literal `false` (`SPEC.md:40`):** `true` and `null` appear in `canonical.json` and `01_every_type_grant_revoke.jsonl`, but `false` never appears in any vector.
6. **Negative integer lower bound `-(2^53 - 1)` (`-9007199254740991`) and out-of-range `-9007199254740992` (`SPEC.md:42-43`):** `canonical.json` tests `9007199254740991` and `9007199254740992`, `-1`, and `-0`, but not the negative boundary.
7. **Leading zeros in numbers (`01`, `-01`) (`SPEC.md:42`):** No vector contains numbers with leading zeros.
8. **Short control-character escapes `\b` (`U+0008`), `\f` (`U+000C`), `\r` (`U+000D`), `\t` (`U+0009`) (`SPEC.md:44-45`):** `canonical.json` exercises only `\n`, `\"`, `\\`, and `\u0001`.
9. **Non-canonical escape encodings → `not_canonical` (`SPEC.md:44-48`):** No vector tests uppercase hex in `\uXXXX` (e.g. `\u00E9`), escaped slash `\/`, or `\uXXXX` used for printable ASCII or for `\b, \f, \n, \r, \t, ", \`.
10. **Lone low surrogate (`\uDC00`..`\uDFFF`) or high surrogate followed by non-low-surrogate (`\uD800\uD800` or `\uD800x`) → `malformed_json` (`SPEC.md:49-50`):** `canonical.json` only tests a single trailing high surrogate `"\ud800"`.
11. **Duplicate keys after unescaping (e.g. `"a"` and `"\u0061"`) (`SPEC.md:51`):** `canonical.json` only tests identical raw key tokens `{"a":1,"a":2}`.

### §3. Hash chain
12. **`parent` mismatch on entry 0 (`parent != "0"*64` at `seq == 0` → `parent_mismatch`) (`SPEC.md:61,191`):** `17_parent_mismatch_fork.jsonl` tests `parent_mismatch` only at `seq: 2`.

### §4. Entry shape
13. **Missing or extra top-level keys on an entry object → `schema` (`SPEC.md:66-67`):** Every log vector has the exact 7 top-level keys (`20_schema_rule_type_gone.jsonl` fails on `"type":"rule"`, and `19_schema.jsonl` fails on §5 `body` missing `"commit"`).
14. **Invalid `seq` type/range (`< 0`, boolean, string), invalid `parent` shape (not `[0-9a-f]{64}`), invalid `ts` shape (not matching `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z`), non-string `proposer`, non-object `body`, or `sig` not matching `[A-Za-z0-9+/]+={0,2}` → `schema` (`SPEC.md:69-77`):** None of these §4 field-shape failures is exercised by any vector.

### §5. Body schemas
15. **Invalid `genesis` body schema (`charter`, `checker`, `keys`), invalid `merge` body schema (`proposal`, `commit`, `checker`), or non-string `proposal.title` / non-hex40 `proposal.commit` → `schema` (`SPEC.md:85-92`):** Only a missing `proposal.commit` (`19_schema.jsonl`) is tested.
16. **Invalid key declaration schema (`key_id` not `[a-z0-9_-]{1,64}`, empty/non-string `principal`, invalid `powers` array or element, malformed `pubkey` string or 51-byte wire blob) → `schema` (`SPEC.md:94-100`):** No vector tests a malformed key declaration (`04`–`07` test `bad_key` on well-formed declarations).
17. **Repeated power names in `powers` (e.g. `["proposal","proposal"]`) (`SPEC.md:95-96`):** Allowed by §5 ("repetition allowed"), never exercised.

### §6. Signatures
18. **`sig` matching `[A-Za-z0-9+/]+={0,2}` (§4) but failing base64 decoding in §6 → `bad_signature` (`SPEC.md:111-123`):** Not exercised in any vector.
19. **SSHSIG container deviations other than namespace and reserved field → `bad_signature` (`SPEC.md:114-123`):** Wrong magic (`!= "SSHSIG"`), wrong version (`!= 1`), malformed embedded `pubkey blob`, wrong hash algorithm (`!= "sha512"`), wrong inner key type (`!= "ssh-ed25519"`), wrong signature length (`!= 64`), and trailing/truncated wire bytes are never exercised in `spec/vectors/logs/` (only `14_bad_signature_namespace.jsonl` and `15_bad_signature_reserved.jsonl` are present).
20. **Non-canonical $R$ in a signed log entry → `bad_signature` (`SPEC.md:138-144`):** Exercised in unit vector `tests/vectors/speccheck.json` (cases 8–9), but not in `spec/vectors/logs/*.jsonl`.

### §7. The law in force
21. **Re-declaration changing `principal` or `pubkey` blob for an existing `key_id` (`SPEC.md:171-173`):** `01`, `02`, and `03` re-declare `bob-1` and `ann-1` with changed `powers`, but always keep the same `principal` and `pubkey` blob.
22. **Duplicate `pubkey` blob or repeated `key_id` within `genesis.body.keys` (`SPEC.md:174-178`):** `04_duplicate_pubkey_bad_key.jsonl` tests duplicate `pubkey` only on a subsequent `key` entry (`seq: 1`), not within `genesis.body.keys`.
23. **Weakness tested before duplicate `pubkey` blob when a declaration is both weak and duplicate (`SPEC.md:176`):** No vector has a key declaration that is simultaneously weak and a duplicate of another `key_id`'s blob.
24. **A `key` entry at $i$ governs entries $> i$, never itself (`SPEC.md:179`):** No log vector has a `key` entry signed by the key it is declaring or modifying.

### §8. The validity predicate & §9. CLI contract
25. **`genesis_misplaced` at entry 0 (`seq == 0` with `type != "genesis"`) (`SPEC.md:192`):** `18_genesis_misplaced.jsonl` tests only `type == "genesis"` at `seq == 2`.
26. **Multi-defect precedence across steps 1–9 (`SPEC.md:186-201`):** Aside from `{"a":1.5,"b":"\ud800"}` in `canonical.json` (within step 1), no vector in `spec/vectors/logs/*.jsonl` contains an entry with two defects from different steps in §8.
27. **CLI exit status 2 on usage or I/O error (`SPEC.md:216`):** Not exercised by `spec/vectors/verdicts.json`.

agrees except the findings above
