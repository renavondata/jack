# Cold reads of c1-types

## kernel/, judge/, pins/, tests/, tools/, spec/ — Gemini

Model ID: `google/gemini-4-argon`

## Answers

### 1. `kernel/`

- **§4's type list**
  - **SPEC (§4, line 80):** ``| `type` | one of `genesis key proposal merge amend push decision spec_conflict` |``
  - **Code:** `kernel/log.py:11` (`TYPES = ("genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict")`), `kernel/log.py:21` (`TYPE = re.compile("|".join(TYPES))`), `kernel/log.py:93–94` (`spec.fullmatch(value)`), `kernel/log.py:133–134` (`"type": TYPE` in `check_shape`), `kernel/log.py:149` (`"powers": (TYPE,)` in `KEY_DECL`).
  - **Answer:** **Yes.**

- **§5's body schema for `amend` (`activate_at`)**
  - **SPEC (§5, lines 87–89, 97, 102; §7, lines 206–207):**
    - ``Required members per type; **extra members are allowed** (any keys, any depth, including keys containing `.`); a required member with the wrong shape is **schema**.``
    - ``| `amend` | `id`: `[A-Z][0-9]{1,3}` (A2, A3, …); `charter`: hex64, the SHA-256 of `CHARTER.md` with the amendment appended; `activate_at`: integer, the seq from which it is in force |``
    - ``hex64 = `[0-9a-f]{64}`, hex40 = `[0-9a-f]{40}`. "integer ≥ 0" excludes booleans.``
    - ``An `amend`'s `id` must not equal any earlier `amend`'s `id`, and its `activate_at` must exceed its own `seq` (**schema**).``
  - **Code:** `kernel/log.py:17` (`HEX64 = re.compile(r"[0-9a-f]{64}")`), `kernel/log.py:85–86` (`def _is_int(v): return isinstance(v, int) and not isinstance(v, bool)`), `kernel/log.py:99–106` (`_match` checks required dict keys and allows extra members), `kernel/log.py:156` (`"amend": {"id": re.compile(r"[A-Z][0-9]{1,3}"), "charter": HEX64, "activate_at": _is_int}`), and `kernel/check.py:68–69` (`if e["type"] == "amend" and (body["activate_at"] <= i or any(a == body["id"] for a, _, _ in state.amendments)): raise Refuse("schema", "amendment id reused or activation not above seq")`).
  - **Answer:** **Yes.**

- **§5's body schema for `push`**
  - **SPEC (§5, line 98):** ``| `push` | `digest`: hex64, the trusted-base digest (§10.1) of the trunk this entry authorises; `review`: hex64, the SHA-256 of the cold review the push was read against, or 64 zeros if none |``
  - **Code:** `kernel/log.py:17` (`HEX64 = re.compile(r"[0-9a-f]{64}")`), `kernel/log.py:157` (`"push": {"digest": HEX64, "review": HEX64}`), `kernel/log.py:165` (`_match(BODY[type_], body, type_)`).
  - **Answer:** **Yes.**

- **§5's body schema for `decision`**
  - **SPEC (§5, line 99):** ``| `decision` | `kind`: one of `veto promote budget grant transmute fix`; `subject`: non-empty string (for `transmute`, the `id` of the amendment it unlocks) |``
  - **Code:** `kernel/log.py:22` (`NONEMPTY = re.compile(r".+", re.S)`), `kernel/log.py:158` (`"decision": {"kind": re.compile(r"veto|promote|budget|grant|transmute|fix"), "subject": NONEMPTY}`), `kernel/log.py:93–94` (`spec.fullmatch(value)`).
  - **Answer:** **Yes.**

- **§5's body schema for `spec_conflict`**
  - **SPEC (§5, line 100):** ``| `spec_conflict` | `section`: non-empty string; `text`: non-empty string (what the builder could not reconcile) |``
  - **Code:** `kernel/log.py:22` (`NONEMPTY = re.compile(r".+", re.S)`), `kernel/log.py:159` (`"spec_conflict": {"section": NONEMPTY, "text": NONEMPTY}`).
  - **Answer:** **Yes.**

- **§7's state: the promulgated charter**
  - **SPEC (§7, lines 202–203):** ``**The promulgated charter** is the `charter` of the latest valid `amend` entry, or of genesis if there is none.``
  - **Code:** `kernel/check.py:16` (`class State(namedtuple("State", "head keys owners charter amendments trusted_base transmuted")):`), `kernel/check.py:22` (`EMPTY = State(log.GENESIS_PARENT, {}, {}, None, (), None, frozenset())`), `kernel/check.py:80–84` (`if e["type"] == "genesis": charter, trusted = body["charter"], body["checker"] ... elif e["type"] == "amend": charter, amendments = body["charter"], amendments + ((body["id"], body["activate_at"], body["charter"]),)`), `kernel/check.py:89`.
  - **Answer:** **Yes.**

- **§7's state: the charter in force at a position**
  - **SPEC (§7, lines 203–206):** ``**The charter in force** at position *i* is the `charter` of the latest valid `amend` with `activate_at` ≤ *i*, or of genesis if there is none (CHARTER §3: a change binds forward; an amendment decides now and takes effect at its height).``
  - **Code:** `kernel/check.py:18–19` (`def charter_at(self, position): return next((c for _, height, c in reversed(self.amendments) if height <= position), self.charter)`), `kernel/check.py:82` (`amendments = ((None, 0, charter),)` at genesis), `kernel/check.py:84` (`amendments + ((body["id"], body["activate_at"], body["charter"]),)` at `amend`). (Because `activate_at > seq` is enforced at `kernel/check.py:68`, any amendment with `height <= position` necessarily has `seq < height <= position`.)
  - **Answer:** **Yes.**

- **§7's state: the trusted base in force**
  - **SPEC (§7, lines 208–209):** ``**The trusted base in force** is the `digest` of the latest valid `push` entry, or genesis's `checker` if there is none.``
  - **Code:** `kernel/check.py:16` (`trusted_base` field of `State`), `kernel/check.py:80–81` (`if e["type"] == "genesis": charter, trusted = body["charter"], body["checker"]`), `kernel/check.py:85–86` (`elif e["type"] == "push": trusted = body["digest"]`), `kernel/check.py:89`.
  - **Answer:** **Yes.**

- **§7's state: the transmuted set**
  - **SPEC (§7, lines 210–211):** ``**Transmuted amendments** are the `subject`s of valid `decision` entries of kind `transmute`. The kernel records them; the judge enforces them (§10.11).``
  - **Code:** `kernel/check.py:16` (`transmuted` field of `State`), `kernel/check.py:22` (`frozenset()` in `EMPTY`), `kernel/check.py:87–88` (`elif e["type"] == "decision" and body["kind"] == "transmute": transmuted = transmuted | {body["subject"]}`), `kernel/check.py:89`.
  - **Answer:** **Yes.**

- **§7's state: the last-key guard as a third cause of `bad_key`, tested after weakness and ownership, for `key` entries only**
  - **SPEC (§7, lines 188–194):**
    - ``A declaration is refused with **bad_key** if its public key is weak (§6), or if its pubkey blob has **ever** been declared for a *different* key_id, even one since rotated or revoked (one key, one identity, for the life of the log). Weakness is tested first; the detail is free text.``
    - ``A `key` entry is refused with **bad_key** if, with its declaration registered, no declared key's `powers` would include `key`: the power to declare keys, once lost, can be regained by no entry (CHARTER §2.4: forbid only the irreversible). Tested after weakness and ownership; for `key` entries only, never for genesis.``
  - **Code:** `kernel/check.py:44–51` (`declare` tests `sig.weak_key(blob[-32:])` at line 47, then `owners.get(blob, d["key_id"]) != d["key_id"]` at line 49), `kernel/check.py:71–73` (for `genesis`, calls `declare` without the last-key guard), and `kernel/check.py:75–78` (for `e["type"] == "key"`, calls `declare` first at line 76, then checks `if not any("key" in k.powers for k in keys.values()): raise Refuse("bad_key", "no declared key would keep the power to declare keys")` at lines 77–78).
  - **Answer:** **Yes.**

- **§8 step 9's effects**
  - **SPEC (§8, lines 232–238):** ``9. Effect: for `key`, register the declaration (§7; a weak or owned pubkey, or the last `key` power lost → **bad_key**); for `amend`, the promulgated charter becomes its `charter` and it is in force from `activate_at` (§7); for `push`, the trusted base in force becomes its `digest`; for `decision` of kind `transmute`, its `subject` joins the transmuted set. `proposal`, `merge`, `spec_conflict` and the other decisions have no effect on the state beyond the head hash.``
  - **Code:** `kernel/check.py:75–89`.
  - **Answer:** **Yes.**

- **No reason code outside §9's twelve**
  - **SPEC (§9, lines 260–262):** ``Reason codes (closed set, twelve): `malformed_json not_canonical schema bad_seq parent_mismatch genesis_misplaced no_proposer bad_key unknown_key proposer_mismatch no_power bad_signature`.``
  - **Code:** `kernel/log.py:73, 75, 78, 80, 104, 116, 132, 168` and `kernel/check.py:30, 33, 35, 37, 40, 48, 50, 59, 61, 63, 65, 69, 78`. Every `Refuse(...)` raised in `kernel/` uses one of the twelve reason codes in §9.
  - **Answer:** **Yes.**

---

### 2. Differential harness over `spec/vectors/logs/*.jsonl`

- **SPEC (§9a, lines 276–278, 291–295):**
  - ``2. **What is compared.** For each log, the whole log and every proper prefix of it (lengths 0 to n−1), each written to a file and given to both checkers by their command lines.``
  - ``5. **Report.** The number of logs and of prefixes compared; every disagreement with its seed (or path), the prefix length, and both outputs; the commit of the working tree (or null if git cannot answer), and the SHA-256 of the seed file. Exit 0 iff there was no disagreement and every requested log was compared.``
- **Code:** `harness/diff.py:24–59`.
- **Answer:** **Yes** (0 disagreements across 40 logs and 98 proper prefixes; exit status 0).
- **Last four lines of `python3 harness/diff.py --b kernel2/check 'spec/vectors/logs/*.jsonl'`:**
```json
 "commit": "c9688bfb6d553c52d11d0826d88b8a9d9083fe0a",
 "seeds_sha256": "011b2ee01a4bb4207b92b8d3d128ec4ce5210f3dc5c1de72dd58436911b14386",
 "disagreements": []
}
```

---

### 3. `judge/judge.py`

- **Item 2 against the promulgated charter**
  - **SPEC (§10, lines 318–320):** ``2. **charter_mismatch** — the SHA-256 of trunk's `CHARTER.md` is not the promulgated charter at the end of trunk's log (§7: the latest valid `amend`, else genesis). (Checked only when trunk's log has a line.)``
  - **Code:** `judge/judge.py:102–113` (`promulgated_charter` runs trunk's kernel on trunk's log, takes `valid = lines if verdict["ok"] else lines[:verdict["seq"]]`, and returns the `charter` of the last entry in `valid` of type `genesis` or `amend`) and `judge/judge.py:185–186` (`if old and promulgated_charter(repo, trunk, trunk_log) != hashlib.sha256(show(repo, trunk, CHARTER) or b"").hexdigest(): return refuse("charter_mismatch", ...)`).
  - **Answer:** **Yes** (in `judge/judge.py`; note that the two pins named in §10 item 2 are missing from `pins/pins.py`, see Question 4 and Findings).

- **Item 11 (`trusted_base_unrecorded`), including on the self-check (`head == trunk`)**
  - **SPEC (§10, lines 349–353, 364):**
    - ``11. **trusted_base_unrecorded** — trunk's trusted-base digest (item 1) is not the trusted base in force at the end of trunk's log (§7). Applies to the self-check too: a push to `main` that changes the trusted base without a `push` entry naming the new digest turns `main` red (CHARTER §7: every act of Guy's is an entry). Pin `push_unrecorded`.``
    - ``Items 11–14 apply to every judged log, the self-check included.``
  - **Code:** `judge/judge.py:208–211` (runs `proposal_checks` only when `head != trunk`, without returning early when `head == trunk`) and `judge/judge.py:212–216` (`trusted = next((e["body"]["digest"] for e in reversed([json.loads(l) for l in old]) if e["type"] == "push"), entries[0]["body"]["checker"] if entries else None)` followed by `if old and trusted != report["trusted_digest"]: return refuse("trusted_base_unrecorded", ...)`).
  - **Answer:** **Yes.**

- **Item 12 (`push_during_amendment`), including that 12 means strictly between**
  - **SPEC (§10, lines 354–356, 364):**
    - ``12. **push_during_amendment** — a `push` entry whose `seq` lies strictly between an `amend`'s `seq` and its `activate_at`: the law changes first, the code waits for the height. Pin `freeze_ignored`.``
    - ``Items 11–14 apply to every judged log, the self-check included.``
  - **Code:** `judge/judge.py:217–219` (`amendments = [e for e in entries if e["type"] == "amend"]` and `if any(a["seq"] < e["seq"] < a["body"]["activate_at"] for e in entries if e["type"] == "push" for a in amendments): return refuse("push_during_amendment", "push strictly between amendment and activation")`).
  - **Answer:** **Yes.**

- **Item 13 (`amend_untransmuted`), including on the self-check (`head == trunk`)**
  - **SPEC (§10, lines 357–360, 364):**
    - ``13. **amend_untransmuted** — an `amend` whose `id` is not in the transmuted set at its position: every amendment is two acts, a `decision` of kind `transmute` naming it and then the `amend` (Suber: an entrenched rule is first made mutable, as a separate move). Pin `one_act_amendment`.``
    - ``Items 11–14 apply to every judged log, the self-check included.``
  - **Code:** `judge/judge.py:220–225` (iterates `entries` in order, refusing with `amend_untransmuted` at lines 222–223 if `e["type"] == "amend" and e["body"]["id"] not in transmuted`, and adding `e["body"]["subject"]` to `transmuted` at lines 224–225 when `e["type"] == "decision" and e["body"]["kind"] == "transmute"`).
  - **Answer:** **Yes.**

- **Item 14 (`decision_by_other`), including on the self-check (`head == trunk`)**
  - **SPEC (§10, lines 361–364):**
    - ``14. **decision_by_other** — a `decision` entry not signed by a key declared in genesis (the sovereign's acts are his own; CHARTER §7). Pin `decision_forged`.``
    - ``Items 11–14 apply to every judged log, the self-check included.``
  - **Code:** `judge/judge.py:226–231` (`founders = {d["pubkey"].split(" ")[1] for d in entries[0]["body"]["keys"]} if entries else set()`, then for each entry `e` extracts the SSHSIG-embedded pubkey blob `blob[14:14 + n]` and refuses with `decision_by_other` if `e["type"] == "decision"` and its base64 pubkey blob is not in `founders`; runs for both `head != trunk` and `head == trunk`).
  - **Answer:** **Yes.**

---

### 4. `pins/pins.py`

- **`push_unrecorded`**
  - **SPEC (§10, lines 349–353):** ``11. **trusted_base_unrecorded** — trunk's trusted-base digest (item 1) is not the trusted base in force at the end of trunk's log (§7). Applies to the self-check too: a push to `main` that changes the trusted base without a `push` entry naming the new digest turns `main` red (CHARTER §7: every act of Guy's is an entry). Pin `push_unrecorded`.``
  - **Code:** `pins/pins.py:153–171` (`t_push_unrecorded`), `pins/pins.py:473–474` (`Pin("push_unrecorded", ...)`), mutating `judge/judge.py:215`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:157–165` edits `SPEC.md` on `main` without a `push` entry and verifies `trusted_base_unrecorded` on both `"main"` and `"pr"`, then records the `push` entry at lines `167–171` and verifies `ok` is `True`).
    - Does the mutant remove exactly that rule and nothing else? **Yes** (`pins/pins.py:474` replaces `if old and trusted != report["trusted_digest"]:` at `judge/judge.py:215` with `if False:`).
    - Does the twin pass only because the rule is present? **Yes** (without line 215, the unrecorded trusted-base change on `main` and `pr` is accepted with `ok: True`).
    - Could the mutant survive by failing for another reason? **No** (`judge_refuses` at `pins/pins.py:60–61, 165` asserts `(r.get("ok"), r.get("reason")) == (False, "trusted_base_unrecorded")`, and under the mutant the judge returns `ok: True`, killing the mutant on the exact refusal check).

- **`freeze_ignored`**
  - **SPEC (§10, lines 354–356):** ``12. **push_during_amendment** — a `push` entry whose `seq` lies strictly between an `amend`'s `seq` and its `activate_at`: the law changes first, the code waits for the height. Pin `freeze_ignored`.``
  - **Code:** `pins/pins.py:174–187` (`t_freeze_ignored`), `pins/pins.py:475–476` (`Pin("freeze_ignored", ...)`), mutating `judge/judge.py:218`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:176–187` places `amend` at `seq` 2 and `push` at `seq` 3: refused with `push_during_amendment` when `activate_at` is 4, and accepted when `activate_at` is 3).
    - Does the mutant remove exactly that rule and nothing else? **Yes** (`pins/pins.py:476` replaces `if any(a["seq"] < e["seq"] < a["body"]["activate_at"]` at `judge/judge.py:218` with `if any(False and a["seq"] < e["seq"] < a["body"]["activate_at"]`).
    - Does the twin pass only because the rule is present? **Yes** (the `height = 4` log is otherwise valid and passes all kernel and judge checks when line 218 is disabled).
    - Could the mutant survive by failing for another reason? **No** (`judge_refuses` at `pins/pins.py:185` checks exact reason `"push_during_amendment"` first; under the mutant `height = 4` returns `ok: True`).

- **`one_act_amendment`**
  - **SPEC (§10, lines 357–360):** ``13. **amend_untransmuted** — an `amend` whose `id` is not in the transmuted set at its position: every amendment is two acts, a `decision` of kind `transmute` naming it and then the `amend` (Suber: an entrenched rule is first made mutable, as a separate move). Pin `one_act_amendment`.``
  - **Code:** `pins/pins.py:190–203` (`t_one_act_amendment`), `pins/pins.py:477–478` (`Pin("one_act_amendment", ...)`), mutating `judge/judge.py:222`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:192–203` tests an `amend` without a prior `transmute` decision, expecting `amend_untransmuted`, and with a prior `transmute` decision, expecting `ok: True`).
    - Does the mutant remove exactly that rule and nothing else? **Yes** (`pins/pins.py:478` replaces `if e["type"] == "amend" and e["body"]["id"] not in transmuted:` at `judge/judge.py:222` with `if False:`).
    - Does the twin pass only because the rule is present? **Yes** (the kernel does not enforce transmutation, so without `judge/judge.py:222` the untransmuted amendment returns `ok: True`).
    - Could the mutant survive by failing for another reason? **No** (`judge_refuses` at `pins/pins.py:203` asserts exact reason `"amend_untransmuted"` on `transmute = False` first; under the mutant it returns `ok: True`).

- **`decision_forged`**
  - **SPEC (§10, lines 361–362):** ``14. **decision_by_other** — a `decision` entry not signed by a key declared in genesis (the sovereign's acts are his own; CHARTER §7). Pin `decision_forged`.``
  - **Code:** `pins/pins.py:206–224` (`t_decision_forged`), `pins/pins.py:479–480` (`Pin("decision_forged", ...)`), mutating `judge/judge.py:230`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:208–224` grants `"decision"` power to non-genesis key `stranger-1` and signs a `decision` with `w.stranger` vs `w.guy`, checking `decision_by_other` vs `ok: True` on both proposal and self-check).
    - Does the mutant remove exactly that rule and nothing else? **Yes** (`pins/pins.py:480` replaces `if e["type"] == "decision" and base64.b64encode(blob[14:14 + n]).decode() not in founders:` at `judge/judge.py:230` with `if False:`).
    - Does the twin pass only because the rule is present? **Yes** (`stranger-1` has `"decision"` power and matching principal `"guy"`, so the kernel admits the entry; only `judge/judge.py:230` refuses it).
    - Could the mutant survive by failing for another reason? **No** (`judge_refuses` at `pins/pins.py:218, 224` checks exact reason `"decision_by_other"` on `sovereign = False` first; under the mutant it returns `ok: True`).

- **`last_key_revocable`**
  - **SPEC (§7, lines 191–197):** ``A `key` entry is refused with **bad_key** if, with its declaration registered, no declared key's `powers` would include `key`: the power to declare keys, once lost, can be regained by no entry (CHARTER §2.4: forbid only the irreversible). Tested after weakness and ownership; for `key` entries only, never for genesis. Pin `last_key_revocable`: a re-declaration of the only key holding `key` without it is refused at its seq with bad_key; its twin, the same re-declaration keeping `key`, is admitted.``
  - **Code:** `pins/pins.py:352–358` (`t_last_key_revocable`), `pins/pins.py:559–561` (`Pin("last_key_revocable", ...)`), mutating `kernel/check.py:77`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:355–358` re-declares `guy-master` without `"key"` and asserts `refused(..., 1, "bad_key")`, then re-declares `guy-master` keeping `"key"` and asserts `admitted(..., 2)`).
    - Does the mutant remove exactly that rule and nothing else? **Yes** (`pins/pins.py:560–561` replaces `if not any("key" in k.powers for k in keys.values()):` at `kernel/check.py:77` with `if False:`).
    - Does the twin pass only because the rule is present? **Yes** (without `kernel/check.py:77`, the re-declaration without `"key"` is admitted with `{"ok": True, "entries": 2}`).
    - Could the mutant survive by failing for another reason? **No** (`refused` at `pins/pins.py:36–38, 356` asserts `(False, 1, "bad_key")` first; under the mutant it returns `{"ok": True, "entries": 2}`).

- **`charter_edit_unrecorded`**
  - **SPEC (§10, lines 318–324):** ``2. **charter_mismatch** — the SHA-256 of trunk's `CHARTER.md` is not the promulgated charter at the end of trunk's log (§7: the latest valid `amend`, else genesis). (Checked only when trunk's log has a line.) An amendment therefore lands as one push by Guy: the text appended to `CHARTER.md` and the `amend` entry appended to `log.jsonl`, together. Pins: `charter_edit_unrecorded` (an edited `CHARTER.md` with no `amend` is refused), `amend_stale` (an `amend` whose `charter` is not trunk's `CHARTER.md` is refused).``
  - **Code:** `pins/pins.py:472–579` (`PINS` — absent), `tests/test_pins.py:24–33` (`Registry.test_pins_are_well_formed` — absent).
  - **Answers:**
    - Does the fixture exercise the rule named? **No** (`charter_edit_unrecorded` is missing from `pins/pins.py`).
    - Does the mutant remove exactly that rule and nothing else? **No** (no mutant is defined).
    - Does the twin pass only because the rule is present? **No** (no pin exists).
    - Could the mutant survive by failing for another reason? **No** (no mutant exists).

- **`amend_stale`**
  - **SPEC (§10, lines 318–324):** ``Pins: `charter_edit_unrecorded` (an edited `CHARTER.md` with no `amend` is refused), `amend_stale` (an `amend` whose `charter` is not trunk's `CHARTER.md` is refused).``
  - **Code:** `pins/pins.py:472–579` (`PINS` — absent), `tests/test_pins.py:24–33` (`Registry.test_pins_are_well_formed` — absent).
  - **Answers:**
    - Does the fixture exercise the rule named? **No** (`amend_stale` is missing from `pins/pins.py`).
    - Does the mutant remove exactly that rule and nothing else? **No** (no mutant is defined).
    - Does the twin pass only because the rule is present? **No** (no pin exists).
    - Could the mutant survive by failing for another reason? **No** (no mutant exists).

---

### 5. `tools/entry.py`

- **Is the unsigned message byte-identical to §2's canonical form of the entry without `sig`, with `seq` and `parent` as §3–§4 require?**
  - **SPEC (§2, lines 34–35; §3, lines 66–68; §4, lines 72–73; §6, lines 121–122):**
    - ``Every line must be *exactly* the canonical serialisation of the JSON object it denotes; otherwise **not_canonical**.``
    - `` `parent` of entry *i* ≥ 1 is the lowercase hex SHA-256 of the **bytes of line *i*−1** (UTF-8, without the line terminator). `parent` of entry 0 is 64 `0`s. `seq` of entry *i* is *i*.``
    - ``An entry object has **exactly** the keys `seq, parent, ts, type, proposer, body, sig` (else **schema**)``
    - ``**Message.** The signed message is the UTF-8 bytes of the canonical serialisation (§2) of the entry object **without** its `sig` member.``
  - **Code:** `tools/entry.py:24–26` (`read_log`), `tools/entry.py:42–45` (`entry = dict(seq=len(lines), parent=log.line_hash(lines[-1]), ts=a.ts, type=a.type, proposer=a.proposer, body=body)` and `message = log.canonical(entry)`), `tools/entry.py:54–55` (writes `message` encoded as UTF-8 to `a.out`).
  - **Answer:** **Yes.**

- **Does `prepare` refuse before signing on a bad `ts`, `body` or shape?**
  - **SPEC (§4, lines 72–83; §5, lines 87–114):**
    - ``An entry object has **exactly** the keys `seq, parent, ts, type, proposer, body, sig` (else **schema**)``
    - ``Required members per type; **extra members are allowed** (any keys, any depth, including keys containing `.`); a required member with the wrong shape is **schema**.``
  - **Code:** `tools/entry.py:34–48` (`if not log.instant(a.ts): raise Usage(...)`, `body = json.loads(a.body_json)`, `if not isinstance(body, dict): raise Usage(...)`, `message = log.canonical(entry)`, `log.check_shape(dict(log.parse_line(message), sig="AAAA"))`, `log.check_body(a.type, body)`), called at `tools/entry.py:53` before `open(a.out, "w", encoding="utf-8")` at line 54, and caught at `tools/entry.py:100–102` (exiting 2 on stderr with nothing written).
  - **Answer:** **Yes.**

- **Does `assemble` refuse, print nothing on stdout and exit 1 when the kernel refuses the line?**
  - **SPEC (§9, lines 249–253):**
    - ``{"ok":false,"seq":n,"reason":"<code>","detail":"<free text>"}``
    - ``Exit status 0 if ok, 1 if refused, 2 on usage or I/O error (no JSON required).``
  - **Code:** `tools/entry.py:72–76` (`verdict = check.check(read_log(a.log) + [line])`; `if not verdict["ok"]: print(json.dumps(verdict, sort_keys=True), file=sys.stderr); return 1`).
  - **Answer:** **Yes.**

- **Is the printed `ssh-keygen` namespace `core-entry`?**
  - **SPEC (§6, lines 129, 141–142):** ``"SSHSIG" (6 raw bytes) ‖ uint32 1 ‖ string(pubkey blob) ‖ string("core-entry")``
  - **Code:** `tools/entry.py:56` (`sign = shlex.join(["ssh-keygen", "-Y", "sign", "-f", re.sub(r"\.pub$", "", a.pubkey), "-n", "core-entry", a.out])`).
  - **Answer:** **Yes.**

---

### 6. `spec/vectors/`

- **Does each vector's verdict in `verdicts.json` follow from SPEC, and is there a vector for the last key power lost (§11)?**
  - **SPEC (§11, lines 392–395):** ``- `spec/vectors/logs/*.jsonl` with `spec/vectors/verdicts.json` — signed logs (throwaway public keys embedded in their genesis) and the verdict each must produce: one per reason code, plus valid logs exercising every entry type, grant, revocation and re-declaration, and the last `key` power lost.``
  - **Code:** `spec/vectors/verdicts.json:3–194` and `spec/vectors/logs/00_genesis_only.jsonl` through `spec/vectors/logs/39_push_without_power.jsonl`; in particular `spec/vectors/logs/32_last_key_power_lost_bad_key.jsonl:1–2` and `spec/vectors/verdicts.json:159–163` (`{"ok": false, "seq": 1, "reason": "bad_key"}`), with twin `spec/vectors/logs/33_last_key_power_kept.jsonl:1–2` and `spec/vectors/verdicts.json:164–167` (`{"ok": true, "entries": 2}`). (Note: `tools/vectors.py:87–95` omits vectors 32 and 33 from its generator function `logs(w)`; see Findings.)
  - **Answer:** **Yes.**

---

### 7. Touched paths and kernel line count

- **Does the change touch any path outside `kernel/`, `kernel2/`, `judge/`, `pins/`, `tests/`, `spec/` and `tools/`?**
  - **SPEC (§10, lines 310–314, 372–378):**
    - ``The digest is SHA-256 over `path ‖ 0x00 ‖ content ‖ 0x00` for every file under `kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and the file `SPEC.md`, sorted by path.``
    - ``"paths": ["sim/", "harness/", "tests/", "pins/", "tools/", "transcripts/", "REPORT.md", "BRIEF-C1.md", "LAW.md", "README.md", "RUNBOOK.md", "log.jsonl"]``
  - **Code:** `DIFF.patch:1, 106, 157, 181, 336, 344, 572, 650, 882, 925, 951, 1203, 1211, 1219, 1228, 1236, 1244, 1252, 1260, 1268, 1315, 1448, 1614, 1766, 1814, 1834, 1946` (touches only files under `judge/`, `kernel/`, `kernel2/`, `pins/`, `spec/`, `tests/`, and `tools/`).
  - **Answer:** **No.**

- **Is the kernel within 500 lines?**
  - **SPEC (§9a.6, lines 296–297; CHARTER §9 criterion 3 / Amendment A1.5):** ``counted as `tools/count_kernel.py` counts the kernel.``
  - **Code:** `tools/count_kernel.py:15–21` counts `kernel/__init__.py` (0), `kernel/check.py` (127), `kernel/log.py` (168), and `kernel/sig.py` (140), for a total of **435 lines** (≤ 500).
  - **Answer:** **Yes.**

---

## Findings

1. (`pins/pins.py`, line `472`, SPEC `§10` item 2, `pins/pins.py` (and `tests/test_pins.py:24–33`) omits the two required pins `charter_edit_unrecorded` and `amend_stale` specified by SPEC §10 item 2 ("Pins: `charter_edit_unrecorded` (an edited `CHARTER.md` with no `amend` is refused), `amend_stale` (an `amend` whose `charter` is not trunk's `CHARTER.md` is refused)"), leaving `judge/judge.py:102–113` (`promulgated_charter`) and `judge/judge.py:185` (`if old and promulgated_charter(repo, trunk, trunk_log) != hashlib.sha256(show(repo, trunk, CHARTER) or b"").hexdigest():`) unpinned against mutation, Fixture: in a repo created with `fx = make_repo(world())`, (a) for `charter_edit_unrecorded`, writing `CHARTER.md` = `"# charter\n\namended\n"` on `main` without appending an `amend` entry to `log.jsonl` causes `judge(fx.repo, "main", "main")` to return `{"ok": False, "reason": "charter_mismatch", ...}`, and (b) for `amend_stale`, appending `{"type": "decision", "body": {"kind": "transmute", "subject": "A2"}}` at `seq: 1` and `{"type": "amend", "body": {"id": "A2", "charter": "ff" * 32, "activate_at": 20}}` at `seq: 2` on `main` without updating `CHARTER.md` causes `judge(fx.repo, "main", "main")` to return `{"ok": False, "reason": "charter_mismatch", ...}`, whereas mutating `judge/judge.py:185` to `if False:` (or replacing `promulgated_charter(repo, trunk, trunk_log)` with `genesis_charter(old[0])`) survives `python3 pins/run.py` with `SURVIVED 0` because neither pin is in `pins.PINS`.)

2. (`tools/vectors.py`, line `88`, SPEC `§11`, `tools/vectors.py` jumps from `out["31_genesis_key_extra_member"]` (`tools/vectors.py:87`) directly to `for n, (type_, body) in enumerate(bodies.items(), 34):` (`tools/vectors.py:94`), omitting `32_last_key_power_lost_bad_key` and `33_last_key_power_kept`, while `main()` (`tools/vectors.py:112–113`) deletes all `spec/vectors/logs/*.jsonl` before regenerating them from `logs(w)`, so running `python3 tools/vectors.py` deletes the §11 vector for the last `key` power lost (`spec/vectors/logs/32_last_key_power_lost_bad_key.jsonl`) and its twin (`spec/vectors/logs/33_last_key_power_kept.jsonl`) and drops them from `spec/vectors/verdicts.json`, Log/fixture: `spec/vectors/logs/32_last_key_power_lost_bad_key.jsonl` (`seq: 0` `genesis` with `guy-master` holding all 8 powers and `ann-1` holding `["proposal"]`, followed by `seq: 1` `key` re-declaring `guy-master` with `powers: ["genesis","proposal","merge","amend","push","decision","spec_conflict"]` → `{"ok": false, "seq": 1, "reason": "bad_key"}`) and `spec/vectors/logs/33_last_key_power_kept.jsonl` (`{"ok": true, "entries": 2}`) are missing from `tools.vectors.logs(build.World(tmp))`, which returns only 38 logs instead of 40.)

VERDICT: does not implement SPEC
## kernel2/ — Claude Code

# REVIEW — kernel2 against SPEC.md (cold read)

Reviewer model id: **claude-opus-5-5** (Anthropic). Date 2026-10-18.

Read: SPEC.md §1–§12 in full; kernel2/checker.go, canonical.go, signature.go,
ed25519.go, main.go (plus the launcher `check`, `build.sh`, `test.sh`, and the
kernel2/ hunks of DIFF.patch). **kernel/ was not read** (neither the files nor
DIFF.patch's kernel/ hunks), and the Python kernel was not run.

Line references are to the files as they stand at commit `c9688bf`.

## `sh kernel2/test.sh`

```
PASS
ok  	_/home/g/git/types-room/kernel2	4.916s
```
142 `--- PASS` lines, no `--- FAIL`. (It builds into the gitignored `kernel2/.cache/`.)

## §4 entry shape

| SPEC sentence | Go | Yes/No |
|---|---|---|
| "An entry object has **exactly** the keys `seq, parent, ts, type, proposer, body, sig` (else **schema**)" | checker.go:61–68 (`len(m) != 7` + presence of each) | yes |
| "`seq` integer ≥ 0 (not a boolean)" | checker.go:41, 69 (`jsonInteger` is a distinct type from `bool`) | yes |
| "`parent` `[0-9a-f]{64}`" | checker.go:15, 69 | yes |
| "`ts` `YYYY-MM-DDTHH:MM:SSZ` in ASCII digits only … year 0001–9999, a real Gregorian date (leap years included), hour 00–23, minute 00–59, second 00–59" | checker.go:20, 43–58 (Go RE2 `[0-9]` is ASCII; `y == 0` refused; 400/100/4 leap rule) | yes |
| "`type` one of `genesis key proposal merge amend push decision spec_conflict`" | checker.go:23–29, 72–75 | yes |
| "`proposer` a string (emptiness is checked later, §8 step 6)" | checker.go:76–78 | yes |
| "`body` an object" | checker.go:79–81 | yes |
| "`sig` `[A-Za-z0-9+/]+={0,2}`" | checker.go:19, 69 (RE2 `$` is end-of-text only) | yes |

## §5 body schemas (the four asked for)

| SPEC sentence | Go | Yes/No |
|---|---|---|
| "`amend` \| `id`: `[A-Z][0-9]{1,3}` (A2, A3, …); `charter`: hex64 …; `activate_at`: integer, the seq from which it is in force" | checker.go:18, 153–155 (`activate_at` must be `jsonInteger`, so booleans/strings/floats are schema) | yes |
| "`push` \| `digest`: hex64 …; `review`: hex64 …, or 64 zeros if none" | checker.go:156–157 (64 zeros is hex64) | yes |
| "`decision` \| `kind`: one of `veto promote budget grant transmute fix`; `subject`: non-empty string (for `transmute`, the `id` of the amendment it unlocks)" | checker.go:31–37, 158–159 | yes (the parenthesis is read as descriptive, not as a shape test; I agree — the "required members" column says only "non-empty string") |
| "`spec_conflict` \| `section`: non-empty string; `text`: non-empty string" | checker.go:160–161 | yes |
| "**extra members are allowed** (any keys, any depth, including keys containing `.`)" | checker.go:126–163 read only required members | yes |

## §7 state

| SPEC sentence | Go | Yes/No |
|---|---|---|
| "**The promulgated charter** is the `charter` of the latest valid `amend` entry, or of genesis if there is none." | checker.go:312–313 (genesis), 320 (each valid amend, after signature) | yes |
| "**The charter in force** at position *i* is the `charter` of the latest valid `amend` with `activate_at` ≤ *i*, or of genesis if there is none" | checker.go:192–200 `charterAt`: scans amendments newest-first in **log order**, requires `a.seq < position && a.activateAt <= position` | yes, on the reading "latest" = latest in log order (see Finding 2; not verdict-bearing) |
| "An `amend`'s `id` must not equal any earlier `amend`'s `id`, and its `activate_at` must exceed its own `seq` (**schema**)." | checker.go:274–278, ids recorded at 322 only for valid amends | yes (placement in §8 order: see Finding 1) |
| "**The trusted base in force** is the `digest` of the latest valid `push` entry, or genesis's `checker` if there is none." | checker.go:314, 324 | yes |
| "**Transmuted amendments** are the `subject`s of valid `decision` entries of kind `transmute`." | checker.go:325–328 | yes |
| "A declaration is refused with **bad_key** if its public key is weak (§6), or if its pubkey blob has **ever** been declared for a *different* key_id … Weakness is tested first" | checker.go:211–217; `byBlob` (174) is never pruned, so rotated/revoked blobs stay owned | yes |
| "A `key` entry is refused with **bad_key** if, with its declaration registered, no declared key's `powers` would include `key` … Tested after weakness and ownership; for `key` entries only, never for genesis." | checker.go:218–229 (after 212 and 215); called with `true` only at 316 (key, step 9) and `false` at 281 (genesis). The loop excludes `d.id` because that key's powers after registration are `d.powers`, already known to lack `key` | yes |
| Pin `last_key_revocable`: "a re-declaration of the only key holding `key` without it is refused at its seq with bad_key; its twin … keeping `key`, is admitted" | vectors 32/33 pass in test.sh; my logs `guard_rotate_lose` (bad_key @1) / `guard_rotate_keep` (ok 2) agree | yes |
| "A later declaration of the same key_id replaces the earlier" | checker.go:230–231 | yes |
| "Genesis is self-certifying: … registered in array order before its signature is checked." | checker.go:279–285 precede 286 | yes |
| "A `key` entry at *i* governs entries > *i*, never itself." | checker.go:286–309 use pre-entry state; registration at 315–318 | yes |

## §8 order of tests

| SPEC step | Go | Yes/No |
|---|---|---|
| 1 "§1–2 decoding and parsing → malformed_json / not_canonical" | checker.go:248–251; canonical.go:253–268 (UTF-8 at 254; syntax/non-object/depth/lone surrogate → malformed at 261–262; non-integer/out-of-range/duplicate flagged and then re-serialise compare at 264) | yes |
| 2 "§4 shape → schema" | checker.go:252–254 | yes |
| 3 "`seq` ≠ *i* → bad_seq" | checker.go:255–257 | yes |
| 4 "`parent` ≠ hash of line *i*−1 (or ≠ 64 zeros for *i* = 0) → parent_mismatch" | checker.go:185, 258–260, 330 | yes |
| 5 "`type` is `genesis` and *i* ≠ 0, or … not `genesis` and *i* = 0 → genesis_misplaced" | checker.go:262–264 | yes |
| 6 "`proposer` = `""` → no_proposer" | checker.go:265–268 | yes |
| 7 "§5 body schema → schema. For `genesis`, its key declarations are then registered in order (§7; a weak or duplicate pubkey → bad_key)." | checker.go:269–285 (whole genesis body validated before any registration) | yes |
| 8 "container parse fails → bad_signature; … no declared key's blob → unknown_key; … principal ≠ `proposer` → proposer_mismatch; `type` ∉ … powers → no_power; Ed25519 fails → bad_signature." | checker.go:286–309 in exactly that order; unknown_key checks the *current* blob of the owning id (291) | yes |
| 9 "Effect: for `key`, register the declaration (§7; a weak or owned pubkey, or the last `key` power lost → bad_key); for `amend`, the promulgated charter becomes its `charter` and it is in force from `activate_at`; for `push`, the trusted base in force becomes its `digest`; for `decision` of kind `transmute`, its `subject` joins the transmuted set. `proposal`, `merge`, `spec_conflict` and the other decisions have no effect" | checker.go:310–329 | yes |
| 10 "The head becomes the hash of T." | checker.go:330 (only reached on success) | yes |

## §6 signatures (checked because step 8 depends on it)

| SPEC | Go | Yes/No |
|---|---|---|
| Strict base64, exact container, empty reserved, sha512, ssh-ed25519 inner, nothing after | signature.go:13–24, 88–110 (alphabet check before `DecodeString`, so Go's tolerance of `\r\n` is unreachable; exact length 180 / 51) | yes |
| Signed data `"SSHSIG" ‖ string("core-entry") ‖ string("") ‖ string("sha512") ‖ string(SHA-512(message))` | signature.go:112–119; message = canonical(entry − sig), checker.go:301–307 | yes |
| S ≥ L invalid; canonical decoder; k reduced mod L; cofactorless compare of encodings | ed25519.go:121–143, 80–111 | yes |
| Weak = decoder rejects or [8]A = identity | ed25519.go:113–119 | yes |
| pubkey: exactly two fields, one U+0020, `ssh-ed25519`, base64 of exactly 51 bytes = `string("ssh-ed25519") ‖ string(32)` | signature.go:67–84 | yes |

## §9 output and the twelve reason codes

"print exactly one JSON object … Exit status 0 if ok, 1 if refused, 2 on usage or I/O error": main.go:10–34 (usage 11–14, open/read error 15–24, exit 30–33); launcher `check` exits 2 on usage. **yes**.

| Code | Emitted at | Yes/No |
|---|---|---|
| malformed_json | canonical.go:255, 262 | yes |
| not_canonical | canonical.go:265 | yes |
| schema | checker.go:253, 272, 276 | yes |
| bad_seq | checker.go:256 | yes |
| parent_mismatch | checker.go:259 | yes |
| genesis_misplaced | checker.go:263 | yes |
| no_proposer | checker.go:267 | yes |
| bad_key | checker.go:282, 317 | yes |
| unknown_key | checker.go:292 | yes |
| proposer_mismatch | checker.go:296 | yes |
| no_power | checker.go:299 | yes |
| bad_signature | checker.go:288, 308 via `refused` 239–244; `badSignatureReason` (237) defaults to the literal and `build.sh` passes `bad_signature` | yes |

No other code can be produced (every `fail` call site is listed above).

## Attempts to break it

I built signed logs with an independent Python signer (cryptography's Ed25519 +
a hand-built SSHSIG blob; scratchpad only, not committed) and raw lines for the
§1–2 layer, and ran each through `kernel2/check`. **Every one of 93 logs got the
verdict SPEC requires.** Covered:

- amend: valid with transmute/push/spec_conflict/fix after; duplicate id;
  `activate_at` = seq, negative, boolean; id `A999` ok, `A1000`, `A`, `a2`,
  `"A2\n"` schema; duplicate id with a garbage sig (schema, step 7) and with an
  unpowered signer (schema).
- decision/spec_conflict/push: wrong-case kind, list kind, empty/int subject,
  empty text, missing member, missing `review`, uppercase digest, push without
  power (no_power).
- last-key guard: two holders, revoking one then the other (bad_key at the
  second); revoking another id's `key` then one's own; new holder then
  self-revocation (ok); genesis with no `key` holder (ok, guard never at
  genesis); ownership before guard; rotation keep/lose.
- keys: old blob after rotation (unknown_key); revoked key (no_power);
  genesis duplicate key_id replace (no_power); genesis duplicate blob, and a
  blob reused after its id was re-pointed within genesis (bad_key).
- ts: 2100-02-29 / 0000 / second 60 schema; 2000-02-29 ok.
- signatures: padded sig, short sig (bad_signature); sig with space (schema);
  pubkey with `=`, double space, trailing space, tab (schema); tampered body
  (bad_signature); genesis signed by an undeclared key / wrong principal.
- §1–2: NaN, ±Infinity, BOM, UTF-8-encoded surrogate, lone/reversed
  surrogates (also after a float, malformed wins), `-0`, 2^53, 5000-digit and
  20-digit integers, `01`, `1.`, uppercase `é`, `\/`, raw 0x7F, unsorted,
  duplicate keys, surrounding whitespace / `\r`, non-object top level, depth
  32 (schema) / 33 / 200 000 unclosed (malformed), astral-vs-BMP key order,
  empty file (ok 0) and a file of one `\n` (malformed at 0).

No BREAK-*.jsonl is written, because no log was found on which kernel2's
verdict differs from one SPEC determines.

## Findings

No finding is a kernel2 defect against SPEC. These are recorded so the next round can close them:

1. **(SPEC.md:206–207 and :226 / checker.go:274–278, §7 and §8; ambiguity in SPEC, not a kernel2 defect.)**
   SPEC gives the amend constraints ("id must not equal any earlier amend's id",
   "activate_at must exceed its own seq") the reason **schema** in §7 but does
   not place them in §8's order: step 7 names only "§5 body schema", and step 9
   lists no refusal for `amend`. kernel2 tests them at step 7, before the
   signature. A checker that reads them as a step-9 effect check would return
   `no_power` / `bad_signature` instead. A log that tells the two readings apart (genesis key `a` with all powers,
   key `b` with only `proposal`; entry 1 `amend` A2 by `a`; entry 2 `amend` A2
   signed by `b`): kernel2 → `{"ok":false,"seq":2,"reason":"schema"}`; the other
   reading → `no_power`. I think step 7 is the better reading (schema is a shape
   reason, and §8 has no schema step after 7), but SPEC should say so in step 7.
2. **(SPEC.md:203–204 / checker.go:192–200, §7; ambiguity, no effect on verdicts.)** "the latest valid `amend` with
   `activate_at` ≤ *i*" does not say whether "latest" is by log position or by
   height. kernel2 picks log position (so an earlier amend with a later height
   cannot override a newer one that is already in force). The checker never
   outputs this, so no verdict depends on it, but the judge (§10.2/§10.12) and
   C1 will.
3. **(SPEC.md:211, §7; editorial.)** "the judge enforces them (§10.11)": the
   rule is §10 item **13** (`amend_untransmuted`). kernel2/NOTES.md already says this.
4. **(kernel2/check:8–21; operational, outside §9's verdict but inside "every log has a verdict".)**
   The launcher compiles on first use or whenever a source is newer than the
   binary, so it needs a Go toolchain wherever it runs, and two concurrent first
   invocations race on `kernel2/.cache/check`. A failed build exits 2 (a
   non-verdict, which §9a counts as a disagreement). This is not a SPEC
   violation as long as runs are sequential and Go is installed, as on
   ubuntu-latest, but `harness/diff.py` should not start running checkers in parallel without a pre-build step.

VERDICT: implements SPEC

## Round 2, the two findings answered — Gemini

Model ID: `google/gemini-4-argon`

## Answers

### 1. `SPEC.md` §7 and §8 step 7 wording changes

- **SPEC (`SPEC.md:206–208`, `SPEC.md:211–212`, `SPEC.md:227–230`):**
  - `"Latest" is by position in the log, never by height. An amend's id must not equal any earlier amend's id, and its activate_at must exceed its own seq (**schema**, tested at §8 step 7).`
  - `Transmuted amendments are the subjects of valid decision entries of kind transmute. The kernel records them; the judge enforces them (§10.13).`
  - `7. §5 body schema → **schema**. For genesis, its key declarations are then registered in order (§7; a weak or duplicate pubkey → **bad_key**). For amend, §7's two constraints (an unused id; activate_at above its seq) are tested here, before the signature → **schema**.`
- **Code:**
  - `kernel/check.py:18–19` (`State.charter_at` iterates `reversed(self.amendments)`, which is appended in log order at `kernel/check.py:82, 84`) and `kernel2/checker.go:192–200` (`charterAt` iterates `s.amendments` in reverse log order).
  - `kernel/check.py:66–74` and `kernel2/checker.go:270–286` test `amend`'s `id` uniqueness and `activate_at > seq` with reason `"schema"` immediately after body schema validation and before signature verification (`signer(e, keys)` / `parseSignature`).

---

### 2. `pins/pins.py`: `charter_edit_unrecorded` and `amend_stale`

- **`charter_edit_unrecorded`**
  - **SPEC (`SPEC.md:321–327`, §10 item 2):** ``2. **charter_mismatch** — the SHA-256 of trunk's `CHARTER.md` is not the promulgated charter at the end of trunk's log (§7: the latest valid `amend`, else genesis). (Checked only when trunk's log has a line.) An amendment therefore lands as one push by Guy: the text appended to `CHARTER.md` and the `amend` entry appended to `log.jsonl`, together. Pins: `charter_edit_unrecorded` (an edited `CHARTER.md` with no `amend` is refused), `amend_stale` (an `amend` whose `charter` is not trunk's `CHARTER.md` is refused).``
  - **Code:** `pins/pins.py:175–200` (`charter_judged`, `t_charter_edit_unrecorded`), `pins/pins.py:509–513` (`Pin("charter_edit_unrecorded", ...)`), `tests/test_pins.py:29, 34`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:194–200` edits `CHARTER.md` on `main` without an `amend` entry and asserts `judge_refuses(r, "charter_mismatch")` on both `"main"` and `"pr"`, then records a `transmute` decision and an `amend` entry carrying the edited `CHARTER.md`'s SHA-256 and asserts `r.get("ok") is True` on both `"main"` and `"pr"`).
    - Does the mutant remove exactly that rule? **Yes** (`Mutant("charter_unchecked", ...)` at `pins/pins.py:512–513` replaces `if old and promulgated_charter(repo, trunk, trunk_log) != hashlib.sha256(show(repo, trunk, CHARTER) or b"").hexdigest():` at `judge/judge.py:184` with `if False:`, disabling only the `charter_mismatch` check).
    - Does the twin pass only because the rule is present? **Yes** (with `judge/judge.py:184` present, the unrecorded edit to `CHARTER.md` is refused with `charter_mismatch`; when replaced with `if False:`, both `"main"` and `"pr"` are accepted with `ok: True`).
    - Could the mutant survive by failing for another reason? **No** (`judge_refuses(r, "charter_mismatch")` at `pins/pins.py:61–62, 198` checks `(r.get("ok"), r.get("reason")) == (False, "charter_mismatch")` first; because `CHARTER.md` is not in `TRUSTED` (`judge/judge.py:23`) and `pr` is reset to `main`, no other check refuses the fixture, so the mutant returns `ok: True` and is killed on the first assertion).

- **`amend_stale`**
  - **SPEC (`SPEC.md:321–327`, §10 item 2):** ``Pins: `charter_edit_unrecorded` (an edited `CHARTER.md` with no `amend` is refused), `amend_stale` (an `amend` whose `charter` is not trunk's `CHARTER.md` is refused).``
  - **Code:** `pins/pins.py:175–191, 203–208` (`charter_judged`, `t_amend_stale`), `pins/pins.py:514–516` (`Pin("amend_stale", ...)`), `tests/test_pins.py:29, 34`.
  - **Answers:**
    - Does the fixture exercise the rule named? **Yes** (`pins/pins.py:203–208` appends a transmuted `amend` with `charter: "ff" * 32` on `main` while leaving `CHARTER.md` at genesis's charter text and asserts `judge_refuses(r, "charter_mismatch")` on both `"main"` and `"pr"`, then appends a transmuted `amend` with `charter: gitfix.CHARTER_SHA256` and asserts `r.get("ok") is True` on both `"main"` and `"pr"`).
    - Does the mutant remove exactly that rule? **Yes** (`Mutant("genesis_charter_compared", ...)` at `pins/pins.py:514–516` replaces `promulgated_charter(repo, trunk, trunk_log)` with `genesis_charter(old[0])` at `judge/judge.py:184`, removing the requirement that trunk's `CHARTER.md` match the latest valid `amend` rather than genesis).
    - Does the twin pass only because the rule is present? **Yes** (`CHARTER.md` still matches `genesis_charter(old[0])`, so only `promulgated_charter` returning the `amend`'s `"ff" * 32` causes `judge/judge.py:184` to refuse with `charter_mismatch`).
    - Could the mutant survive by failing for another reason? **No** (the `amend` is preceded by a genesis-signed `transmute` decision for `"A2"` and has `activate_at: 9 > seq: 2` with no `push`, so all kernel and judge checks pass when `genesis_charter(old[0])` is compared; the mutant returns `ok: True` and fails `judge_refuses(r, "charter_mismatch")` at `pins/pins.py:206`).

---

### 3. `tools/vectors.py`

- **Does `logs(w)` now produce all forty vectors with the recorded verdicts?**
  - **SPEC (`SPEC.md:395–398`, §11):** ``- `spec/vectors/logs/*.jsonl` with `spec/vectors/verdicts.json` — signed logs (throwaway public keys embedded in their genesis) and the verdict each must produce: one per reason code, plus valid logs exercising every entry type, grant, revocation and re-declaration, and the last `key` power lost.``
  - **Code:** `tools/vectors.py:88–91` adds `32_last_key_power_lost_bad_key` and `33_last_key_power_kept` to `logs(w)`, and `tests/test_vectors.py:48–58` (`test_generator_produces_every_log`) verifies that `vectors.logs(build.World(tmp))` produces all 40 log names in `spec/vectors/verdicts.json` and that `check.check(lines)` (minus `detail`) equals the recorded verdict for all 40 vectors.
  - **Answer:** **Yes.**

---

### 4. Verification runs

- `python3 -m unittest discover -s tests -t .`: **Ran 152 tests, OK (skipped=1).**
- `python3 pins/run.py`: **KILLED 41, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0.**

---

## Findings

None.

VERDICT: implements SPEC
