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
| `type` | one of `genesis key proposal merge amend push decision spec_conflict forecast resolution` |
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
| `amend` | `id`: `[A-Z][0-9]{1,3}` (A2, A3, …); `charter`: hex64, the SHA-256 of `CHARTER.md` with the amendment appended; `activate_at`: integer, the seq from which it is in force |
| `push` | `digest`: hex64, the trusted-base digest (§10.1) of the trunk this entry authorises; `review`: hex64, the SHA-256 of the cold review the push was read against, or 64 zeros if none |
| `decision` | `kind`: one of `veto promote budget grant transmute fix`; `subject`: non-empty string (for `transmute`, the `id` of the amendment it unlocks) |
| `spec_conflict` | `section`: non-empty string; `text`: non-empty string (what the builder could not reconcile) |
| `forecast` | `claim`: non-empty string; `p`: integer 1–999 (per mille; a boolean is not an integer); `resolves_by`: an instant in §4's `ts` form, not earlier than the entry's own `ts` |
| `resolution` | `forecast`: integer ≥ 0, the `seq` of an earlier valid `forecast` entry not already resolved; `outcome`: integer 0 or 1 (a boolean is not an integer); `evidence`: non-empty string |

`forecast.type` and `forecast.args` are optional members the tools read (RUNBOOK);
the kernel never reads them and refuses nothing on their account. `p` is per mille because canonical
lines admit integers only (§2); 1–999 bounds the log-loss without a clipping rule.

hex64 = `[0-9a-f]{64}`, hex40 = `[0-9a-f]{40}`. "integer ≥ 0" excludes booleans.

A body schema never gains a required member: the kernel judges every entry by one
schema, so a member required today would refuse the entries of yesterday (CHARTER §2.2).
New evidence travels as an optional member the verbs write and the judge may read —
`push.record`, hex64, the SHA-256 of the run of record's parts concatenated in name order,
or 64 zeros when the checkers did not change (RUNBOOK, `jack push`) — or as a new type.

A **key declaration** (the body of a `key` entry, and each element of `genesis.keys`) is an object with
**exactly** these four members, and no others (else **schema**): `key_id`: `[a-z0-9_-]{1,64}`;
`principal`: non-empty string; `powers`: array of entry-type names (any of the
ten, possibly empty, repetition allowed); `pubkey`: a string of exactly two fields
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
- A `key` entry is refused with **bad_key** if, with its declaration registered, no
  declared key's `powers` would include `key`: the power to declare keys, once lost,
  can be regained by no entry (CHARTER §2.4: forbid only the irreversible). Tested
  after weakness and ownership; for `key` entries only, never for genesis. Pin
  `last_key_revocable`: a re-declaration of the only key holding `key` without it is
  refused at its seq with bad_key; its twin, the same re-declaration keeping `key`, is
  admitted.
- Genesis is self-certifying: for entry 0 the keys are those its own body
  declares, registered in array order before its signature is checked.
- A `key` entry at *i* governs entries > *i*, never itself.

- **The promulgated charter** is the `charter` of the latest valid `amend` entry, or
  of genesis if there is none. **The charter in force** at position *i* is the
  `charter` of the latest valid `amend` with `activate_at` ≤ *i*, or of genesis if
  there is none (CHARTER §3: a change binds forward; an amendment decides now and
  takes effect at its height). "Latest" is by position in the log, never by
  height. An `amend`'s `id` must not equal any earlier `amend`'s `id`, and its
  `activate_at` must exceed its own `seq` (**schema**, tested at §8 step 7).
- **The trusted base in force** is the `digest` of the latest valid `push` entry, or
  genesis's `checker` if there is none.
- **Transmuted amendments** are the `subject`s of valid `decision` entries of kind
  `transmute`. The kernel records them; the judge enforces them (§10.13).
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

Nothing else is state at C1a. Recognition (c) of CHARTER §3 ("every rule in force
at its parent accepts it") holds vacuously: no rule can be admitted.

## 8. The validity predicate

For entry *i* with line text T, in this order; the first failure refuses:

1. §1–2 decoding and parsing → **malformed_json** / **not_canonical**.
2. §4 shape → **schema**.
2a. `ts` earlier than the previous entry's `ts` (entry 0 exempt) → **ts_decreased**.
3. `seq` ≠ *i* → **bad_seq**.
4. `parent` ≠ hash of line *i*−1 (or ≠ 64 zeros for *i* = 0) → **parent_mismatch**.
5. `type` is `genesis` and *i* ≠ 0, or `type` is not `genesis` and *i* = 0 → **genesis_misplaced**.
6. `proposer` = `""` → **no_proposer**.
7. §5 body schema → **schema**. For `genesis`, its key declarations are then
   registered in order (§7; a weak or duplicate pubkey → **bad_key**). For
   `amend`, §7's two constraints (an unused `id`; `activate_at` above its `seq`)
   are tested here, before the signature → **schema**. For `forecast`, `resolves_by` earlier
   than `ts` → **schema**. For `resolution`, a `forecast` member that is not a recorded forecast
   seq, or one already resolved → **schema**.
8. Signature: §6 container parse fails → **bad_signature**; the embedded pubkey
   blob equals no declared key's blob → **unknown_key**; that key's principal ≠
   `proposer` → **proposer_mismatch**; `type` ∉ that key's powers →
   **no_power**; Ed25519 fails → **bad_signature**.
8a. For `resolution`, the entry's `proposer` equals the recorded proposer of its `forecast` →
   **self_judged**.
9. Effect: for `key`, register the declaration (§7; a weak or owned pubkey, or the
   last `key` power lost → **bad_key**); for `amend`,
   the promulgated charter becomes its `charter` and it is in force from
   `activate_at` (§7); for `push`, the trusted base in force becomes its `digest`;
   for `decision` of kind `transmute`, its `subject` joins the transmuted set;
   for `forecast`, record (seq, proposer); for `resolution`, mark its `forecast` resolved;
   for every entry, record its `ts` as the previous `ts`.
   `proposal`, `merge`, `spec_conflict` and the other decisions have no effect on the
   state beyond the head hash.
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

Reason codes (closed set, fourteen): `malformed_json not_canonical schema bad_seq
parent_mismatch genesis_misplaced no_proposer bad_key unknown_key
proposer_mismatch no_power bad_signature ts_decreased self_judged`.

## 9a. The differential (binding for `harness/diff.py`)

The evidence for CHARTER §9 criterion 2 is produced by `harness/diff.py` and
by nothing else. Its behaviour is this text; an implementation that does more
or less is wrong.

1. **Inputs.** `--seeds N` takes the first N lines of `sim/seeds.txt`, in
   order, and `--seeds A:B` seeds A to B−1 (zero-based), so that a run may be
   split across processes; the report then carries `seeds: [A, B]`. Each
   seed produces one log through `sim/gen.py`'s generator. Log
   files given on the command line are compared as they are. `--a` and `--b`
   name the two checkers' commands; the defaults are §9's.
2. **What is compared.** For each log, the whole log and every proper prefix
   of it (lengths 0 to n−1), each written to a file and given to both
   checkers by their command lines.
3. **What counts as a verdict.** An output is a verdict only if it is exactly
   one of §9's two objects: `ok` a JSON boolean; on acceptance exactly the
   members `ok` and `entries`, `entries` a non-negative integer (not a
   boolean), and exit status 0; on refusal exactly the members `ok`, `seq`,
   `reason` and `detail`, `seq` a non-negative integer (not a boolean),
   `reason` one of §9's fourteen codes, `detail` a string, and exit status 1;
   the output is UTF-8 without a byte-order mark, one JSON object with no
   duplicate members and no `NaN` or `Infinity`.
4. **Agreement.** Two outputs agree iff both are verdicts and they are equal
   after removing `detail`. Anything else — a non-verdict, any other exit
   status, a crash, a checker that cannot be run, or no output within the
   timeout (default 120 s per call) — is a disagreement.
5. **Report.** The number of logs and of prefixes compared; every
   disagreement with its seed (or path), the prefix length, and both
   outputs; the commit of the working tree (or null if git cannot answer),
   and the SHA-256 of the seed file. Exit 0 iff there was no disagreement
   and every requested log was compared.
6. **Bound.** `harness/diff.py` is within sixty-five lines, counted as
   `tools/count_kernel.py` counts the kernel.
7. **Pins** (each with its mutant and a passing twin, run by `pins/run.py`):
   `whole_log_only` — a second checker wrong only on a proper prefix passes;
   `loose_parse` — `{"ok":1,"entries":n}`, or a correct object with the
   wrong exit status, passes;
   `crash_as_agreement` — a crash, a missing checker or a timeout passes;
   `prefix_skipped` — some proper prefix is not compared.

## 10. Outside the checker (informative)

`judge/judge.py` enforces what the log alone cannot (CHARTER §9.6), in this
order, each a refusal of the whole proposal:

1. **trusted_path** — the trusted-base digest of the proposal's head differs
   from trunk's, or `CHARTER.md` differs byte for byte. The digest is SHA-256
   over `path ‖ 0x00 ‖ content ‖ 0x00` for every file under `kernel/`,
   `kernel2/`, `judge/`, `.github/workflows/` and the file `SPEC.md`, sorted by
   path. Compared by content, so an edit, a rename, a deletion or an addition
   under those paths is refused alike; and a proposal must rebase after trunk's
   trusted base moves. The trusted base is regular files only: an object under
   those paths that is not one (a symbolic link or a submodule, git modes 120000
   and 160000) is refused as **trusted_path** at either commit, before any digest
   is taken, and `tools/digest.py` refuses to digest a tree holding one. These
   files change only by Guy's `jack push`, recorded by a `push` entry (item 11).
2. **charter_mismatch** — the SHA-256 of trunk's `CHARTER.md` is not the promulgated
   charter at the end of trunk's log (§7: the latest valid `amend`, else genesis).
   (Checked only when trunk's log has a line.) An amendment therefore lands as one
   push by Guy: the text appended to `CHARTER.md` and the `amend` entry appended to
   `log.jsonl`, together. Pins: `charter_edit_unrecorded` (an edited `CHARTER.md`
   with no `amend` is refused), `amend_stale` (an `amend` whose `charter` is not
   trunk's `CHARTER.md` is refused).
3. **prefix_broken** — trunk's log is not a byte prefix of the proposal's.
4. **genesis_by_proposal** — the proposal supplies entry 0.
5. The kernel's verdict, trunk's kernel extracted from git and run over the
   proposal's whole log; then **checker_drift** if `kernel2/check` exists on
   trunk and disagrees (minus `detail`).
6. **judge_from_proposal** — an appended `merge` whose `checker` is not trunk's
   trusted-base digest.
7. **unattributed_proposal** — the entries the proposal appends to trunk's log
   contain no `proposal` whose `commit` is a commit of the proposal, or some commit
   of the proposal after that `commit` changes a path other than `log.jsonl`. The
   **party** is the `principal` of the key that signed the last such `proposal`
   entry, under the law in force at it (§7); the kernel has verified the signature,
   so the party is a fact, not a claim. (At C0 a `Proposer:` trailer on the head
   commit stood in for the key, A2 clause 3; the verbs still write the trailer, but
   the judge no longer reads it.)
8. **party_scope** — the proposal touches a path not under a prefix in
   `judge/scope.json`'s `parties[party]`; a party absent from `parties` may touch
   anything in `paths`. At C1 a builder may not touch the pins and vectors that
   judge it, a reviewer may touch nothing else, and counsel touches documents only:
   code enters from a builder, written to a text Guy has read; findings enter from a
   reviewer, as pins (A2 clause 9).
9. **out_of_scope** — the proposal touches a path not under a prefix in
   `judge/scope.json`'s `paths`, or its head holds, under any prefix in `paths`, an
   object that is not a regular file: a symbolic link or a submodule (git modes
   120000 and 160000) is refused whatever it points to, since the court's
   repository holds regular files only. (Trusted paths are refused by item 1
   whatever the list says.)
10. **code_cap** — at the proposal's head, the lines of every regular file under a
    prefix in `judge/scope.json`'s `counted` that is a `.py` file or whose first line
    is a `#!` line naming `python`, read from the git object, exceed
    `judge/scope.json`'s `cap`. A file's lines are its `0x0A` bytes, plus one if it
    is not empty and its last byte is not `0x0A`. The judge is the only counter the
    cap depends on; `tools/count_kernel.py` applies the same arithmetic to the
    kernel for CHARTER §9 criterion 3 and binds nothing here.

Items 7–10 apply only to a proposal whose head differs from trunk; the self-check, which judges trunk against itself, skips them.

11. **trusted_base_unrecorded** — trunk's trusted-base digest (item 1) is not the
    trusted base in force at the end of trunk's log (§7). Applies to the self-check
    too: a push to `main` that changes the trusted base without a `push` entry
    naming the new digest turns `main` red (CHARTER §7: every act of Guy's is an
    entry). Pin `push_unrecorded`.
12. **push_during_amendment** — a `push` entry whose `seq` lies strictly between an
    `amend`'s `seq` and its `activate_at`: the law changes first, the code waits
    for the height. Pin `freeze_ignored`.
13. **amend_untransmuted** — an `amend` whose `id` is not in the transmuted set at
    its position: every amendment is two acts, a `decision` of kind `transmute`
    naming it and then the `amend` (Suber: an entrenched rule is first made
    mutable, as a separate move). Pin `one_act_amendment`.
14. **decision_by_other** — a `decision` entry not signed by a key declared in
    genesis (the sovereign's acts are his own; CHARTER §7). Pin `decision_forged`.

Items 11–14 apply to every judged log, the self-check included.

`judge/scope.json` is under `judge/`, so it is trusted base and changes only
by Guy's own push. Its members are `layer` (a string), `paths` and `counted`
(lists of path prefixes; a prefix ending in `/` matches a directory, otherwise
exactly one file), `parties` (party name → such a list) and `cap` (an integer).
The file equals
the block below, byte for byte less whitespace; a push that changes one without
the other is refused by the tests. At C0 the layer was `C0` and the cap 3000. C1
opened at 4500 on 19 October and was raised to 5500 the same day, when the tests
of the verbs exceeded it, a finding against the pre-statement for the C1 report; raised to 6200 on 25 October by C1a's installing push, when the ledger's tests and simulator kinds reached 5614 before the reviewer's pins, a second finding against the pre-statement (transcripts/BUILD-C1a.md §0);
at C1 it is:

```
{"layer": "C1",
 "paths": ["sim/", "harness/", "tests/", "pins/", "tools/", "spec/vectors/", "transcripts/",
           "REPORT.md", "BRIEF-C1.md", "LAW.md", "README.md", "RUNBOOK.md", "log.jsonl"],
 "parties": {"builder": ["sim/", "harness/", "tests/", "tools/", "transcripts/", "log.jsonl"],
             "reviewer": ["pins/", "spec/vectors/", "transcripts/", "log.jsonl"],
             "counsel": ["REPORT.md", "BRIEF-C1.md", "LAW.md", "README.md", "RUNBOOK.md",
                         "transcripts/", "sim/runs/", "log.jsonl"]},
 "counted": ["sim/", "harness/", "tests/", "pins/", "tools/"],
 "cap": 6200}
```

Pins for items 7–10, each with its mutant and a passing twin:
`unattributed_proposal_admitted` (a proposal with no signed `proposal` entry, or
with a commit after it that touches more than `log.jsonl`, is admitted),
`counsel_build_admitted`, `builder_pin_admitted`, `reviewer_code_admitted` (for these
three the mutant removes that party's list from `judge/scope.json`, and nothing else),
`scope_unguarded`, `cap_unguarded`, `shebang_uncounted` (a python file without `.py`
under `counted` is not counted), `foreign_object_admitted` (a symbolic link, or a
submodule whose commit is present or absent, under `paths` is admitted, or under a
trusted path is digested rather than refused).

## 11. Vectors

- `tests/vectors/rfc8032.json` — five Ed25519 vectors, all valid.
- `tests/vectors/speccheck.json` — twelve edge cases with expected outcomes.
- `tests/vectors/weak_keys.json` — twelve public keys that must be refused at declaration.
- `tests/vectors/ssh_keygen_differences.json` — tolerated differences from `ssh-keygen -Y verify`.
- `spec/vectors/canonical.json` — canonical-JSON and hash vectors.
- `spec/vectors/logs/*.jsonl` with `spec/vectors/verdicts.json` — signed logs
  (throwaway public keys embedded in their genesis) and the verdict each must
  produce: one per reason code, plus valid logs exercising every entry type,
  grant, revocation and re-declaration, and the last `key` power lost.
  Signed logs added, each with its required `(seq, reason)` verdict: `40_forecast_valid`,
  `41_resolution_valid`, `42_resolution_self_bad` (`self_judged`), `43_resolution_dangling_bad`
  (`schema`), `44_resolution_double_bad` (`schema`), `45_forecast_past_bad` (`schema`),
  `46a_forecast_permille_0_bad` (`schema`), `46b_forecast_permille_1000_bad` (`schema`),
  `47_forecast_boolean_bad` (`schema`, `p: true`), `48_ts_decreased_bad` (`ts_decreased`),
  `49_self_resolution_bad_signature` (`bad_signature`, not `self_judged`). Each refused log stops at
  its first bad entry, so each witnesses one refusal.

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
11. C1 opens ledger-first (Guy, 25 October 2026; A3): `forecast` and `resolution` precede the clerk; `p`
    is per mille; self-resolution has its own code; A2.2's `ts_decreased` is implemented with them;
    scoring is outside the kernel; §12.4's sentence "whose order is not checked at C0" is superseded.
