# SPEC — the record and the checker (C0)

This document specifies `log.jsonl` and the validity predicate precisely enough
that a second checker, written in another language by an author who never sees
the Python, produces the **same verdict on every log** (CHARTER §3 Adjudication,
§9 criterion 2). Where the charter left a choice, the choice made here is marked
**[decision]** and listed again in §12. The Python kernel in `kernel/` is one
implementation of this text; where they disagree, that is a finding (REPORT.md),
not a licence to copy.

**Scope (Guy's decision, 14 October 2026, on counsel's review).** C0 is the
record only. There is no rule language, no `rule` or `repeal` entry, no witness
and no lapse at C0; that language is C1's, when a first precedent needs it
(BRIEF-C1.md). The law at C0 is CHARTER §3's three secondary rules, in code:
recognition, change (over `key` entries) and adjudication.

Notation: `string(b)` is the SSH wire string, a big-endian uint32 length
followed by the bytes. `‖` is concatenation. "Refuse with X" means the checker
stops at the current entry with reason code X (§9). All regular expressions
must match the **whole** value.

## 1. The log file

- `log.jsonl` is a sequence of bytes. Lines are separated by the byte 0x0A; a
  final 0x0A is optional; an empty file has zero lines. A line is decoded as
  UTF-8; bytes that are not valid UTF-8 make the line **malformed_json**.
- Line *i* (0-based) is entry *i*. An empty log is valid: `{"ok":true,"entries":0}`.
- Entries are checked in order. The first entry that fails determines the verdict;
  nothing after it is examined (so appending anything to a refused log leaves the
  verdict unchanged).

## 2. Canonical JSON

Every line must be *exactly* the canonical serialisation of the JSON object it
denotes; otherwise **not_canonical**. The canonical serialisation is:

- An object is `{` members `}` with members separated by `,`, each `"key":value`,
  **keys sorted by Unicode code point** of the key string (not of its escaped
  form), no whitespace anywhere. An array is `[` values separated by `,` `]`.
- Values are objects, arrays, strings, integers, `true`, `false`, `null`.
  **Numbers are integers only**, written in decimal with an optional leading
  `-`, no leading zeros, no fraction, no exponent, and |n| ≤ 2^53 − 1
  (9007199254740991). `-0`, `1.0`, `1e3` and larger magnitudes are not canonical.
- Strings are ASCII-only: `"` → `\"`, `\` → `\\`, U+0008 → `\b`, U+000C → `\f`,
  U+000A → `\n`, U+000D → `\r`, U+0009 → `\t`; every other code point outside
  U+0020..U+007E (that is, all other control characters, U+007F and everything
  above) → `\uXXXX` with **four lowercase hex digits**, code points above
  U+FFFF as a UTF-16 surrogate pair (`😀` → `😀`). `/` is not escaped.
- A string containing a lone surrogate (an escape `\uD800`..`\uDFFF` not forming
  a valid pair) is **malformed_json**, not merely non-canonical.
- Duplicate keys in an object are **not_canonical** (the canonical form has none).

- Objects and arrays nest **at most 32 deep** (the line's own object is depth 1); deeper nesting is
  **malformed_json**, whatever else the line contains. A checker must return this verdict, never
  crash or run out of stack, for any depth.
- An integer token longer than 20 characters is out of range (**not_canonical**), however many digits
  it has; a checker must never fail to read a long number.

Order of these checks within one line: not valid JSON, or not an object, or nesting deeper than 32,
or any lone surrogate anywhere → **malformed_json**; then any non-integer or
out-of-range number → **not_canonical**; then re-serialise and compare with the
line → **not_canonical**. Vectors: `spec/vectors/canonical.json`.

## 3. Hash chain

`parent` of entry *i* ≥ 1 is the lowercase hex SHA-256 of the **bytes of line
*i*−1** (UTF-8, without the line terminator). `parent` of entry 0 is 64 `0`s.
`seq` of entry *i* is *i*.

## 4. Entry shape

An entry object has **exactly** the keys `seq, parent, ts, type, proposer, body, sig`
(else **schema**), with:

| key | requirement |
|---|---|
| `seq` | integer ≥ 0 (not a boolean) |
| `parent` | `[0-9a-f]{64}` |
| `ts` | `YYYY-MM-DDTHH:MM:SSZ` in **ASCII digits only** (`[0-9]`, never other Unicode digits), naming an instant that exists: year 0001–9999, a real Gregorian date (leap years included), hour 00–23, minute 00–59, second 00–59 (no leap seconds). The checker never reads a clock and does not order timestamps at C0. |
| `type` | one of `genesis key proposal merge` |
| `proposer` | a string (emptiness is checked later, §8 step 6) |
| `body` | an object |
| `sig` | `[A-Za-z0-9+/]+={0,2}` (decoded in §6) |

## 5. Body schemas

Required members per type; **extra members are allowed** (any keys, any depth,
including keys containing `.`); a required member with the wrong shape is
**schema**.

| type | required members |
|---|---|
| `genesis` | `charter`: hex64; `checker`: hex64; `keys`: array of key declarations |
| `key` | a key declaration (the body itself) |
| `proposal` | `title`: string; `commit`: hex40 |
| `merge` | `proposal`: integer ≥ 0; `commit`: hex40; `checker`: hex64 |

hex64 = `[0-9a-f]{64}`, hex40 = `[0-9a-f]{40}`. "integer ≥ 0" excludes booleans.

A **key declaration** (the body of a `key` entry, and each element of `genesis.keys`) is an object with
**exactly** these four members, and no others (else **schema**): `key_id`: `[a-z0-9_-]{1,64}`;
`principal`: non-empty string; `powers`: array of entry-type names (any of the
four, possibly empty, repetition allowed); `pubkey`: a string of exactly two fields
separated by exactly one ASCII space (U+0020; no other whitespace, no leading or trailing space), the first `ssh-ed25519`, the second standard base64
(with padding) decoding to exactly 51 bytes. 51 is a multiple of 3, so a correct encoding has no `=`
padding and no unused bits; any other encoding fails the length test (**schema**). Likewise a
`sig` whose decoded container is not exactly the 180 bytes of §6 is **bad_signature**. No base64 input
is undecidable. The 51 bytes are `string("ssh-ed25519") ‖ string(32 bytes)`.
The 32 bytes are the public key A (§6); whether A is usable is checked at
declaration (§7), not here.

`genesis.charter` is the SHA-256 of `CHARTER.md` and `genesis.checker` the
trusted-base digest at founding; the checker validates their shape only, the
judge their value (§10).

## 6. Signatures

**Message.** The signed message is the UTF-8 bytes of the canonical
serialisation (§2) of the entry object **without** its `sig` member.

**Container.** `sig` is standard base64 (strict: only the alphabet, correct
padding) of an SSHSIG blob (OpenSSH PROTOCOL.sshsig), which must be **exactly**:

```
"SSHSIG" (6 raw bytes) ‖ uint32 1 ‖ string(pubkey blob) ‖ string("core-entry")
‖ string("") ‖ string("sha512") ‖ string(inner)                          and nothing after
inner       = string("ssh-ed25519") ‖ string(64 bytes)                   and nothing after
pubkey blob = string("ssh-ed25519") ‖ string(32 bytes)                   and nothing after
```

Any deviation (bad base64, wrong magic or version, another namespace, a
**non-empty reserved field**, another hash algorithm, another key or signature
type, wrong lengths, trailing bytes) is **bad_signature**. **[decision]** sha512
only; ssh-ed25519 only; the reserved field must be empty, so that one signature
has exactly one encoding and a line cannot be re-encoded while staying valid.

**Signed data.** Ed25519 is verified over
`"SSHSIG" ‖ string("core-entry") ‖ string("") ‖ string("sha512") ‖ string(SHA-512(message))`.

**Ed25519, strict [decision].** With p = 2^255 − 19,
L = 2^252 + 27742317777372353535851937790883648493, d = −121665 · 121666^−1 mod p,
sqrt(−1) = 2^((p−1)/4) mod p, and base point
B = (15112221349535400772501151409588531511454012693041857206046113283949847762202,
46316835694926478169428394003475163141307993866256225615783033603165251855960):

1. Split the 64-byte signature into R (32) and S (32). S is the little-endian
   integer of its bytes. If S ≥ L the signature is invalid.
2. Decode A from the 32-byte public key and R from its 32 bytes with the
   **canonical** decoder: y = the little-endian integer with bit 255 cleared,
   sign = bit 255; if y ≥ p, invalid. u = y² − 1, v = d·y² + 1 (mod p);
   x = u·v³·(u·v⁷)^((p−5)/8) mod p; if v·x² ≡ u keep x; else if v·x² ≡ −u set
   x = x·sqrt(−1); else invalid. If x = 0 and sign = 1, invalid. If x mod 2 ≠
   sign, x = p − x. Small-order points are **not** rejected by the verifier
   itself (they are refused at key declaration, §7).
3. k = SHA-512(R bytes ‖ public key bytes ‖ signed data) as a little-endian
   integer, **reduced modulo L**.
4. Valid iff [S]B = R + [k]A as points of the curve (**cofactorless**; compare
   canonical encodings).

**Weak keys [decision].** A 32-byte public key is *weak* iff the canonical
decoder of step 2 rejects it, or the decoded point A has small order:
[8]A = identity, the point (0, 1), whose encoding is `01` followed by 31 zero
bytes. The twelve weak encodings in `tests/vectors/weak_keys.json` (the eight
torsion points; `y = p`, `y = p + 1`, `y = 2^255 − 1`, `x = 0` with the sign bit)
must all be weak; every key `ssh-keygen -t ed25519` makes is not.

Consequences the second author must reproduce: `S + L` (a malleated signature)
is invalid; a blob with a non-empty reserved field is invalid; ed25519-speccheck
cases 0–3 are valid and 4–11 invalid as *signatures* (`tests/vectors/speccheck.json`;
their small-order public keys could never be declared); the five RFC 8032 §7.1
vectors are valid. `ssh-keygen -Y verify` accepts some signatures this rule
refuses (`tests/vectors/ssh_keygen_differences.json`); the checkers follow this
rule, not ssh-keygen.

## 7. The law in force

The checker folds the log into a state: the head hash (§3) and the **keys**, a
map key_id → (principal, pubkey blob, powers). For entry *i* the law in force
is what entries 0..*i*−1 established:

- Genesis's `keys` and every valid `key` entry **declare**. A later declaration
  of the same key_id replaces the earlier (so empty `powers` revokes, and a
  re-declaration may change principal and powers).
- A declaration is refused with **bad_key** if its public key is weak (§6), or
  if its pubkey blob has **ever** been declared for a *different* key_id, even one since rotated
  or revoked (one key, one identity, for the life of the log). Weakness is tested first; the detail is free text.
- Genesis is self-certifying: for entry 0 the keys are those its own body
  declares, registered in array order before its signature is checked.
- A `key` entry at *i* governs entries > *i*, never itself.

Nothing else is state at C0. Recognition (c) of CHARTER §3 ("every rule in force
at its parent accepts it") holds vacuously: no rule can be admitted.

## 8. The validity predicate

For entry *i* with line text T, in this order; the first failure refuses:

1. §1–2 decoding and parsing → **malformed_json** / **not_canonical**.
2. §4 shape → **schema**.
3. `seq` ≠ *i* → **bad_seq**.
4. `parent` ≠ hash of line *i*−1 (or ≠ 64 zeros for *i* = 0) → **parent_mismatch**.
5. `type` is `genesis` and *i* ≠ 0, or `type` is not `genesis` and *i* = 0 → **genesis_misplaced**.
6. `proposer` = `""` → **no_proposer**.
7. §5 body schema → **schema**. For `genesis`, its key declarations are then
   registered in order (§7; a weak or duplicate pubkey → **bad_key**).
8. Signature: §6 container parse fails → **bad_signature**; the embedded pubkey
   blob equals no declared key's blob → **unknown_key**; that key's principal ≠
   `proposer` → **proposer_mismatch**; `type` ∉ that key's powers →
   **no_power**; Ed25519 fails → **bad_signature**.
9. Effect: for `key`, register the declaration (§7; → **bad_key**). `proposal`
   and `merge` have no effect on the state beyond the head hash.
10. The head becomes the hash of T.

`detail` is free text and is not compared between checkers.

## 9. Output: the CLI contract

Both checkers are invoked with one argument, the log path, and print exactly
one JSON object on stdout:

```
{"ok":true,"entries":N}
{"ok":false,"seq":n,"reason":"<code>","detail":"<free text>"}
```

Exit status 0 if ok, 1 if refused, 2 on usage or I/O error (no JSON required). Every log has a
verdict: a checker that cannot decide an input (a crash, a timeout, an unanswered question) is
defective, and the judge treats its silence as a refusal of the proposal.
Key order in the output is irrelevant; the differential harness compares the
parsed objects **minus `detail`**. The Python kernel is `python3 -m kernel.check <log>`;
the second checker is `kernel2/check <log>` (kernel2/README.md).

Reason codes (closed set, twelve): `malformed_json not_canonical schema bad_seq
parent_mismatch genesis_misplaced no_proposer bad_key unknown_key
proposer_mismatch no_power bad_signature`.

## 10. Outside the checker (informative)

`judge/judge.py` enforces what the log alone cannot (CHARTER §9.6), in this
order, each a refusal of the whole proposal:

1. **trusted_path** — the trusted-base digest of the proposal's head differs
   from trunk's, or `CHARTER.md` differs byte for byte. The digest is SHA-256
   over `path ‖ 0x00 ‖ content ‖ 0x00` for every file under `kernel/`,
   `kernel2/`, `judge/`, `.github/workflows/` and the file `SPEC.md`, sorted by
   path. Compared by content, so an edit, a rename, a deletion or an addition
   under those paths is refused alike; and a proposal must rebase after trunk's
   trusted base moves. Until C1 brings a lawful change path, these files change
   only by a commit Guy makes himself.
2. **charter_mismatch** — trunk has a genesis whose `body.charter` is not the
   SHA-256 of trunk's `CHARTER.md`. (Checked only when trunk's log has a line.)
3. **prefix_broken** — trunk's log is not a byte prefix of the proposal's.
4. **genesis_by_proposal** — the proposal supplies entry 0.
5. The kernel's verdict, trunk's kernel extracted from git and run over the
   proposal's whole log; then **checker_drift** if `kernel2/check` exists on
   trunk and disagrees (minus `detail`).
6. **judge_from_proposal** — an appended `merge` whose `checker` is not trunk's
   trusted-base digest.

## 11. Vectors

- `tests/vectors/rfc8032.json` — five Ed25519 vectors, all valid.
- `tests/vectors/speccheck.json` — twelve edge cases with expected outcomes.
- `tests/vectors/weak_keys.json` — twelve public keys that must be refused at declaration.
- `tests/vectors/ssh_keygen_differences.json` — tolerated differences from `ssh-keygen -Y verify`.
- `spec/vectors/canonical.json` — canonical-JSON and hash vectors.
- `spec/vectors/logs/*.jsonl` with `spec/vectors/verdicts.json` — signed logs
  (throwaway public keys embedded in their genesis) and the verdict each must
  produce: one per reason code, plus valid logs exercising every entry type,
  grant, revocation and re-declaration.

## 12. Decisions and resolved ambiguities

1. C0 is the record only (Guy, 14 October 2026): four entry types; the rule
   language, witnesses and lapse are C1's. Consequently the verdict carries no
   `rule` and no `lapse` member.
2. Signatures are verified in-kernel (standard library) by the strict rule of §6;
   `ssh-keygen -Y sign` makes them; `ssh-keygen -Y verify` is an oracle for tests only.
3. "Over the line without `sig`" = canonical re-serialisation of the object minus `sig`.
4. Genesis `parent` = 64 zeros; `seq` is the 0-based line index; `ts` is a UTC
   string whose order is not checked at C0 (non-decreasing timestamps are C1's
   first candidate rule).
5. The SSHSIG reserved field must be empty (counsel's review): otherwise one
   signature has many valid encodings.
6. Weak public keys (non-canonical or small-order) are refused at declaration
   with `bad_key`, as is a pubkey already declared under another key_id
   (counsel's review; the latter was `schema` before).
7. An empty log is valid. The judge, not the checker, refuses genesis-by-proposal.
8. `history_rewritten`: an edited line fails at that line by its signature; an
   edited **and re-signed** line fails at the next line (`parent_mismatch`).
9. `merge.checker` and `genesis.charter` are claims verified by the judge
   against git, not by the checker.
10. Body keys may contain `.` and bodies may carry any extra members: the
    checker reads only the required ones.
