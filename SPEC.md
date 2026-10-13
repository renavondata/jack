# SPEC — the record and the checker (C0)

This document specifies `log.jsonl`, the law as data, and the validity predicate
precisely enough that a second checker, written in another language by an author
who never sees the Python, produces the **same verdict on every log** (CHARTER
§3 Adjudication, §9 criterion 2). Where the charter left a choice, the choice
made here is marked **[decision]** and listed again in §16. The Python kernel in
`kernel/` is one implementation of this text; where they disagree, that is a
finding (REPORT.md), not a licence to copy.

Notation: `string(b)` is the SSH wire string, a big-endian uint32 length
followed by the bytes. `‖` is concatenation. "Refuse with X" means the checker
stops at the current entry with reason code X (§13). All regular expressions
must match the **whole** value.

## 1. The log file

- `log.jsonl` is a sequence of bytes. Lines are separated by the byte 0x0A; a
  final 0x0A is optional; an empty file has zero lines. A line is decoded as
  UTF-8; bytes that are not valid UTF-8 make the line **malformed_json**.
- Line *i* (0-based) is entry *i*. An empty log is valid: `{"ok":true,"entries":0,"lapse":[]}`.
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
  U+FFFF as a UTF-16 surrogate pair (`😀`). `/` is not escaped.
- A string containing a lone surrogate (an escape `\uD800`..`\uDFFF` not forming
  a valid pair) is **malformed_json**, not merely non-canonical.
- Duplicate keys in an object are **not_canonical** (the canonical form has none).

Order of these checks within one line: not valid JSON, or not an object, or any
lone surrogate anywhere → **malformed_json**; then any non-integer or
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
| `ts` | `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z` (a UTC timestamp; the checker never reads a clock) |
| `type` | one of `genesis key rule repeal proposal merge` |
| `proposer` | a string (emptiness is checked later, §10 step 8) |
| `body` | an object |
| `sig` | `[A-Za-z0-9+/]+={0,2}` (decoded in §6) |

## 5. Body schemas

Required members per type; **extra members are allowed**; a required member
with the wrong shape, or any object key at any depth of `body` containing `.`,
is **schema**.

| type | required members |
|---|---|
| `genesis` | `charter`: hex64; `checker`: hex64; `keys`: array of key declarations |
| `key` | a key declaration (the body itself) |
| `rule` | `rule_id`: `[a-z0-9_-]{1,64}`; `clauses`: array; `witnesses`: object with `violating`: array and `satisfying`: array; optional `replacements`: object |
| `repeal` | `rule_id`: `[a-z0-9_-]{1,64}` |
| `proposal` | `title`: string; `commit`: hex40 |
| `merge` | `proposal`: integer ≥ 0; `commit`: hex40; `checker`: hex64 |

hex64 = `[0-9a-f]{64}`, hex40 = `[0-9a-f]{40}`. "integer ≥ 0" excludes booleans.

A **key declaration** is an object with `key_id`: `[a-z0-9_-]{1,64}`;
`principal`: non-empty string; `powers`: array of entry-type names (any of the
six, possibly empty); `pubkey`: a string of exactly two space-separated fields,
the first `ssh-ed25519`, the second standard base64 (with padding) decoding to
exactly 51 bytes `string("ssh-ed25519") ‖ string(32 bytes)`. (`genesis.checker`
records the trusted-base digest at founding, see judge/judge.py; the checker
only validates its shape.)

## 6. Signatures

**Message.** The signed message is the UTF-8 bytes of the canonical
serialisation (§2) of the entry object **without** its `sig` member.

**Container.** `sig` is standard base64 (strict: only the alphabet, correct
padding) of an SSHSIG blob (OpenSSH PROTOCOL.sshsig), which must be **exactly**:

```
"SSHSIG" (6 raw bytes) ‖ uint32 1 ‖ string(pubkey blob) ‖ string("core-entry")
‖ string(reserved: any bytes) ‖ string("sha512") ‖ string(inner)        and nothing after
inner       = string("ssh-ed25519") ‖ string(64 bytes)                   and nothing after
pubkey blob = string("ssh-ed25519") ‖ string(32 bytes)                   and nothing after
```

Any deviation (bad base64, wrong magic or version, another namespace, another
hash algorithm, another key or signature type, wrong lengths, trailing bytes)
is **bad_signature**. **[decision]** sha512 only; ssh-ed25519 only.

**Signed data.** Ed25519 is verified over
`"SSHSIG" ‖ string("core-entry") ‖ string("") ‖ string("sha512") ‖ string(SHA-512(message))`
(the reserved field of the signed data is empty regardless of the blob's).

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
   sign, x = p − x. Small-order points are **not** rejected by themselves.
3. k = SHA-512(R bytes ‖ public key bytes ‖ signed data) as a little-endian
   integer, **reduced modulo L**.
4. Valid iff [S]B = R + [k]A as points of the curve (**cofactorless**; compare
   canonical encodings).

Consequences the second author must reproduce: `S + L` (a malleated signature)
is invalid; ed25519-speccheck cases 0–3 are valid and 4–11 invalid
(`tests/vectors/speccheck.json`); the five RFC 8032 §7.1 vectors are valid.
`ssh-keygen -Y verify` may accept some signatures this rule refuses
(`tests/vectors/ssh_keygen_differences.json`); the checkers follow this rule,
not ssh-keygen.

## 7. The law in force

The checker folds the log into a state. For entry *i* the **law in force** is
what entries 0..*i*−1 established:

- **Keys.** A map key_id → (principal, pubkey blob, powers). Genesis's `keys`
  and every valid `key` entry *declare*: a later declaration of the same key_id
  replaces the earlier (so empty `powers` revokes). A declaration whose pubkey
  blob equals that of a *different* key_id already declared is **schema**.
  Genesis is self-certifying: for entry 0 the keys are those its own body
  declares. A `key` entry at *i* governs entries > *i*, never itself.
- **Rules in force.** rule_id → (seq admitted, clauses, violating witnesses,
  satisfying witnesses), for `rule` entries at seq < *i* not repealed by a
  `repeal` at seq < *i*. **Used ids:** every rule_id ever admitted, repealed or not.
- **Facts.** The base facts of entries 0..*i*−1 (§8).

## 8. Facts

Base predicates and arities (fixed; rules may not define them):

| predicate | one fact per | arguments |
|---|---|---|
| `entry/3` | entry | seq, type, proposer |
| `ts/2` | entry | seq, ts |
| `field/3` | scalar in body | seq, path, value (see flattening) |
| `signed_by/2` | entry | seq, key_id of the key that signed it |
| `key/3` | (key_id, power) in a **current** declaration | key_id, principal, power |
| `rule/2` | rule ever admitted | rule_id, seq admitted |
| `repealed/2` | repeal | rule_id, seq of the repeal |
| `candidate/1` | — | the seq of the entry under judgement |

**Flattening** of `body`: for each member k with value v, `flat(k, v)` where
`flat(path, v)` = if v is an object: ∪ over its members m of `flat(path.m, v[m])`;
if v is an array: for each index j, if v[j] is an object or array then
`flat(path.j, v[j])` else the fact `field(seq, path, v[j])` (atoms of an array are
emitted **at the array's own path**); otherwise the fact `field(seq, path, v)`.
Empty objects and arrays emit nothing. Example: `{"a":1,"b":{"c":"x"},"d":[1,2],"e":[{"f":true}],"g":{},"h":null}` →
`field(s,"a",1) field(s,"b.c","x") field(s,"d",1) field(s,"d",2) field(s,"e.0.f",true) field(s,"h",null)`.

**Constants are compared by type and value**: the integer 1, the boolean
`true`, the string `"1"` and `null` are four distinct constants. (A Python
implementation must guard against `1 == True`.)

For entry *i* the facts available are: the facts of entries 0..*i*−1, plus
`key/3` facts for the current declarations (law in force before *i*), plus the
`entry`, `ts`, `field` and `signed_by` facts of entry *i* itself, plus
`candidate(i)`. A **witness** evaluated as virtual entry *m* contributes
`entry(m, type, proposer)`, its `field` facts, `ts(m, ts)` only if it carries
`ts`, and no `signed_by`; plus `candidate(m)`.

## 9. Rules: syntax and semantics

A rule body's `clauses` is a non-empty array of objects with exactly the keys
`head` and `body` (`body` an array, possibly empty). A **literal** is a JSON
array whose first element is a string predicate name followed by arguments, or
`["not", literal]` (negation; not nestable). **Arguments**: a string beginning
with `?` is a variable and must match `\?[A-Za-z_][A-Za-z0-9_]*`; a variable
beginning `?_` is **anonymous** (every occurrence is a distinct variable); any
other string, any integer, `true`, `false`, `null` is a constant; arrays and
objects are not allowed. (A string constant beginning with `?` cannot be written.)

Well-formedness of a rule with id R (else **rule_malformed**):

- Every body predicate is a base predicate used with **exactly** its arity, or
  `violation` with 2 arguments, or a helper matching `[a-z0-9_-]{1,64}\.[a-z0-9_]+`
  (any arity; it may belong to another rule, in force or not — an undefined
  helper is simply empty).
- Every head is not negated and is either `violation` with second argument the
  **string constant R**, or a helper whose part before `.` is exactly R.
- **Range restriction:** every named variable occurring in the head or in a
  negated literal also occurs in a positive literal of the same clause.
  Anonymous variables may occur in negated literals (wildcards) and positive
  literals, never in the head.

**Stratification.** Over the clauses of all rules in force plus the rule being
admitted, build the dependency graph on predicate names (an edge from each body
predicate to the head, negative if the literal is negated). If any cycle
contains a negative edge the law is **unstratifiable**. Equivalent iterative
form: assign every head predicate stratum 0; repeatedly set
stratum(head) = max over body literals of stratum(pred) (+1 if negated and pred
is a head somewhere); if no fixpoint after (number of head predicates + 1) full
passes, unstratifiable. Base predicates are stratum 0 and negating them costs
nothing. Note `not violation(...)` in a rule that derives `violation` is
therefore always unstratifiable.

**Semantics.** The least model, stratum by stratum: a clause fires for every
substitution θ of its variables such that each positive literal θ is a fact and,
for each negated literal, **no** fact matches literal θ (unbound anonymous
variables in it match anything). Derived facts of a stratum are complete before
the next begins. `violation(s, r)` facts are what the checker reads.

## 10. The validity predicate

For entry *i* with line text T, in this order; the first failure refuses:

1. §1–2 decoding and parsing → **malformed_json** / **not_canonical**.
2. §4 shape → **schema**.
3. `seq` ≠ *i* → **bad_seq**.
4. `parent` ≠ hash of line *i*−1 (or ≠ 64 zeros for *i* = 0) → **parent_mismatch**.
5. `type` is `genesis` and *i* ≠ 0, or `type` is not `genesis` and *i* = 0 → **genesis_misplaced**.
6. `proposer` = `""` → **no_proposer**.
7. §5 body schema → **schema**. For `genesis`, its key declarations are then
   registered (a duplicate pubkey among them → **schema**).
8. Signature: §6 container parse fails → **bad_signature**; the embedded pubkey
   blob equals no declared key's blob → **unknown_key**; that key's principal ≠
   `proposer` → **proposer_mismatch**; `type` ∉ that key's powers →
   **no_power**; Ed25519 fails → **bad_signature**.
9. Recognition (c): evaluate the rules in force over the facts of §8 for
   candidate *i*. If any `violation(i, r)` is derived → **violation**, with
   `rule` = the r with the **earliest admission seq** among those derived.
   (Violations derived for other seqs are ignored.)
10. Per type:
    - `key`: register the declaration (duplicate pubkey → **schema**).
    - `repeal`: `rule_id` not in force → **unknown_rule**; else remove it and add `repealed(rule_id, i)`.
    - `rule`: §11.
    - `proposal`, `merge`: nothing further.
11. Record entry *i*'s facts, hash and effects. If `type` ∈ {`rule`, `repeal`},
    compute lapse candidates (§12) and append them to the verdict's `lapse`.

`rule` in a refusal is the rule id for **violation** and `null` for every other
reason. `detail` is free text and is not compared between checkers.

## 11. Rule admission (§9.3 of the charter, with [decision] 7b)

Let the rule entry be at seq n, R its id, m = n + 1. In this order:

1. R ∈ used ids → **duplicate_rule**.
2. Clauses well-formed (§9) → else **rule_malformed**.
3. `witnesses.violating` and `witnesses.satisfying` are non-empty arrays of
   well-formed witnesses; `replacements`, if present, maps rule ids to non-empty
   arrays of well-formed witnesses → else **rule_malformed**. A witness is an
   object with keys `type`, `proposer`, `body` and optionally `ts`; `type` one
   of the six; `proposer` a non-empty string; `body` satisfying the §5 schema
   for `type` (shallow: a `rule`-typed witness's clauses are not compiled);
   `ts` matching §4's pattern if present.
4. Provisionally admit R: rules in force ∪ {R}; add `rule(R, n)`; the facts
   now include entry n's own facts. Stratify all clauses → **unstratifiable**.
5. For each violating witness w: evaluate the law (with R) for virtual entry m;
   unless `violation(m, R)` is derived → **vacuous_rule**.
6. For each satisfying witness w: if any `violation(m, _)` is derived → **impossible_rule**.
7. For each `replacements` target T: T not in force → **rule_malformed**; for
   each of its witnesses, if any `violation(m, _)` is derived → **impossible_rule**;
   otherwise the witnesses **join** T's satisfying witnesses from now on.
8. **Non-contradiction, weak form [decision]:** for every rule Q in force
   (including R and after step 7's joins), at least one satisfying witness of Q
   must derive no `violation(m, _)` under the whole law with R; else **orphans_rule**.

"Evaluate for virtual entry m" means: facts of entries 0..n, current `key/3`
facts, the witness's facts as entry m (§8), `candidate(m)`.

## 12. Lapse candidates (charter §3, reported only)

At each change entry n (`rule` or `repeal`; a `key` entry is not a change
entry), after its effects: let `remaining` be the rules in force ordered by
admission seq. For each rule R in that order: let `others` = remaining − {R}. R
is a candidate iff for **every** violating witness w of R, evaluating `others`
for virtual entry n+1 derives some `violation(n+1, _)`. If R is a candidate,
append `[n, R]` to `lapse` and set remaining = others before testing the next
rule (so two rules never lapse on each other's account). Witnesses are
evaluated against the **current** prefix, not the prefix at R's admission.

## 13. Output: the CLI contract

Both checkers are invoked with one argument, the log path, and print exactly
one JSON object on stdout:

```
{"ok":true,"entries":N,"lapse":[[seq,"rule_id"],...]}
{"ok":false,"seq":n,"rule":"rule_id"|null,"reason":"<code>","detail":"<free text>"}
```

Exit status 0 if ok, 1 if refused, 2 on usage or I/O error (no JSON required).
Key order in the output is irrelevant; the differential harness compares the
parsed objects **minus `detail`**. The Python kernel is `python3 -m kernel.check <log>`;
the second checker is `kernel2/check <log>` (kernel2/README.md).

Reason codes (closed set): `malformed_json not_canonical schema bad_seq
parent_mismatch genesis_misplaced no_proposer unknown_key proposer_mismatch
no_power bad_signature violation rule_malformed duplicate_rule unstratifiable
vacuous_rule impossible_rule orphans_rule unknown_rule`.

## 14. Outside the checker (informative)

`judge/judge.py` enforces what the log alone cannot (CHARTER §9.6): a proposal
may not touch the trusted base (`kernel/`, `judge/`, `.github/workflows/`,
`SPEC.md`) or `CHARTER.md` (**trusted_path**); trunk's log must be a byte
prefix of the proposal's (**prefix_broken**); a proposal may not supply genesis
(**genesis_by_proposal**); trunk's kernel, never the proposal's, is run; both
checkers must agree (**checker_drift**); an appended `merge` must name trunk's
trusted-base digest (**judge_from_proposal**). The digest is SHA-256 over
`path ‖ 0x00 ‖ content ‖ 0x00` for every trusted-base file sorted by path.

## 15. Vectors

- `tests/vectors/rfc8032.json` — five Ed25519 vectors, all valid.
- `tests/vectors/speccheck.json` — twelve edge cases with expected outcomes.
- `tests/vectors/ssh_keygen_differences.json` — tolerated differences from `ssh-keygen -Y verify`.
- `spec/vectors/canonical.json` — canonical-JSON and hash vectors.
- `spec/vectors/logs/*.jsonl` with `spec/vectors/verdicts.json` — signed logs
  (throwaway public keys embedded in their genesis) and the verdict each must
  produce, one per reason code plus valid logs exercising every entry type,
  replacements and lapse.

## 16. Decisions and resolved ambiguities

1. Signatures are verified in-kernel (standard library) by the strict rule of §6;
   `ssh-keygen -Y sign` makes them; `ssh-keygen -Y verify` is an oracle for tests only.
2. "Over the line without `sig`" = canonical re-serialisation of the object minus `sig`.
3. Genesis `parent` = 64 zeros; `seq` is the 0-based line index; `ts` is a UTC string.
4. "Its violating witness yields a violation" = derives `violation(m, R)` for R's **own** id.
5. Witnesses are judged by recognition (c) only (no signature, no chain); the
   rule being admitted is part of "the rest of the law" for the lapse test of older rules.
6. A `repeal` carries no witnesses; `key` is not a change entry; lapse is
   tested at both `rule` and `repeal` entries.
7. An empty log is valid. The judge, not the checker, refuses genesis-by-proposal.
8. §4's Fuller row "satisfying witnesses pass the whole law together" is built
   in the weak form of §11 step 8 (orphans_rule, replacements), not as strict joint compliance.
9. `history_rewritten`: an edited line fails at that line by its signature; an
   edited **and re-signed** line fails at the next line (`parent_mismatch`).
10. No comparison or arithmetic built-ins at C0; a rule over `signed_by` can
    have no satisfying witness and is therefore inadmissible.
11. Several rules deriving `violation(i, _)`: the earliest admitted is reported.
12. `merge.checker` is a claim verified by the judge against git, not by the checker.
