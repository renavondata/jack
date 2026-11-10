VERDICT: ACCEPT
Reviewed tree: bfd685ea3fc465bf34d792eb703f1670e16a173a
Reader: reviewer reviewer-2; model openai/gpt-6-astra; 2026-11-05

F1 — severity: RESOLVED — The opening-tree tuple obligation is discharged: `process_at` reads `WINDOW_FIX_FUNCTIONS` from `start`, and does not compare the tuple assignment merely for being that declaration. A tuple-only deletion leaves the process comparison true; deleting the tuple's names and editing `attributed_failure` makes it false. Re-anchoring the old mutant to change that lookup from `start` to `rev` now yields a behavioral kill, not a syntax or import failure. Witness: `tools/status.py:374-399`; `tests/test_c2a_prime.py:194-206`; isolated mutated run of `test_process_unchanged_from_opening` fails at line 206 with `assert True is False`; the unmodified twin passes.
F2 — severity: RESOLVED — Every commit in `origin/main..Reviewed tree` has a `Proposer:` trailer. Builder code and reviewer pins respect SPEC §10.8; counsel's cap-only trusted-base preparation follows C2a's opening precedent `cd9d8eb`, rather than claiming ordinary counsel proposal scope over those files. Witness: the complete commit audit below; `git show cd9d8eb`; BRIEF-C2a-prime v7 §The window.

No open code findings or pin-contract obligations remain in this read.

## Authority and scope

This is a fresh read of the re-cut opening branch, including builder commit
`05dfceee9820af4bd9a8eee26503d5481793107a`, counsel cap commit
`1c1b27f86f5812d783ddf210968e65f45b9e9281`, and the reviewer pins at the
reviewed head above.

The authorities are `transcripts/BRIEF-C2a-prime-draft.md` **v7**, particularly
§The code and §No item changes, and
`transcripts/RULING-20261104-window-fix.md`, corrections **2, 3, 5 and 6**, on
`origin/main` at `7b8dda5027e902751ec136c296254951d3b5aedf`.
Both documents are byte-identical here and at that main ref. SPEC §10.8's
party lists are unchanged by the cap commit.

Acceptance is of this code and its pins for carriage by the opening push.
The future sovereign acts, main update, opening-note checks and green tests
run on the actual opening commit remain the brief's prescribed procedure.

## Final code read

- **Change 1 — window and subject:** `second_opening` selects the first push
  strictly after V0's late end, provided no `promote C2a` occurred by that end.
  `prime_window` requires counsel's V5 below the opening and uses its own
  `resolves_by`. Missing V5 produces the specified refusal. `decision_window`
  assigns C2a promotion and C2a/C2a-prime vetoes by the opening instant; an
  equal-time veto does not veto the second window. Historical promotions are
  assessed on their own prefixes. Witnesses: `tools/status.py:49-81,255-293,435-445,578-612`;
  `test_second_window`; `pins/c2aprime.py::test_offlog_and_promotion`.
- **Criteria 3 and 7:** the second window uses 8,400 and its opening tree;
  scope/SPEC are checked through intervening commits, including an edit
  subsequently reverted. Acts counting starts at the second opening and
  includes every intersecting minute; the nine first-window rows do not
  carry into the new interval. Witnesses: `tools/status.py:340-373,407-432`;
  `test_assessment_cap_and_first_window_refusal`; reviewer `test_cap_history`.
- **Change 2 / corrections 2 and 5:** qualification is computed outside
  `item_process`. It requires the exact window-name prefix, absence of
  promotion through the late end, a veto by the early end or an attributed
  repair minute wholly inside the early interval, a fix after the late end
  and before the following push, and no earlier fix consuming that name.
  C2a's disputed early/late readings are preserved in the required directions;
  non-promotion alone never establishes failure. Witnesses:
  `tools/status.py:84-170`; `test_c2b_stated_ends`; reviewer `test_fix_cases`
  and `test_contains_name`.
- **Evidence provenance:** the fix's introducing commit is found using entry
  identity and all parents. Evidence must exist there, with its raw twin
  and hash of the specified classifier. CSV header, file-name boundaries
  and whole-minute containment are checked. Later evidence or replacement
  HEAD evidence cannot establish the earlier fix; missing history or files
  produce the unverified diagnostic and leave a repair. Witnesses:
  `tools/status.py:104-170`; `test_file_name_boundaries`; reviewer
  `test_fix_cases` including late-file, replacement, raw-only, bad-hash,
  missing-raw/classifier and unreadable-history cases.
- **No item changes / corrections 3 and 6:** fixes initially taint open
  writs. Only a push removes qualified fixes from still-open writs. Earlier
  finalised items are untouched; nonqualifying fixes remain repairs.
  The timely herald batch between fix and push keeps repairs `(369,)`,
  Y=0, stake 22/45 and wealth 11/15; the post-push batch is free of the fix.
  Qualified fixes add no late report. Witnesses: `tools/status.py:185-237`;
  reviewer `test_nonretroactive_batches`; both timing mutants are killed.
- **Change 3 — protected process:** comparison begins at the opening push's
  carrying tree. It covers the original process, clerk bytes, the opening
  tuple's change-2 functions, transitive named references, whole callers of
  the specified roots/item process, and the top-level assignments they read.
  The two-hop helper/leaf edit is detected. The tuple-source mutant's
  distinguishing deletion-plus-function-edit case is F1 above. Witnesses:
  `tools/status.py:360-404`; `test_process_unchanged_from_opening`; reviewer
  `test_guard_tuple_and_dependency`.
- **Continuity:** `tools/value.py`, `tools/clerk.py`, `score_items`,
  `sovereign_keys` and P0 retain their prior code. The real-prefix inertness
  test and `wealth_continues` pass. No score, null, stake rule or attack gate
  change accompanies the narrow boundary-fix exemption.

## Pins and checks

The requested pins diff was carried over from `origin/review-c2a-prime-pins`
relative to `origin/builder-c2a-prime-v4`. The only subsequent pin change is
the `tuple_from_assessed_tree` find-string re-anchor to the re-cut code;
the replacement still reads the assessed `rev`. No twin was weakened.

The first run reported 144 KILLED and one STALE (the old anchor), with a
matching registry-test failure. After re-anchoring, both required commands
were rerun in full, with temporary storage confined to this worktree using
`TMPDIR="$PWD/transcripts/.review-tmp"`:

```text
python3 -m pytest -q
337 passed, 1 skipped, 49 subtests passed in 126.29s (0:02:06)

python3 pins/run.py
KILLED 145, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0
```

All **99 pins** have passing twins. All **30 C2a-prime mutants** are killed:

| Pin | Killed mutants |
|---|---:|
| second_window_from_the_end | 2 |
| second_window_end_is_v5 | 2 |
| second_window_cap | 2 |
| offlog_from_second_opening | 2 |
| promote_refused_before_end | 2 |
| window_fix_is_decision | 13 |
| window_fix_not_retroactive | 2 |
| process_unchanged_from_opening | 5 |

The tuple-source kill was additionally inspected in isolation: the mutated
guard reports `True` for the changed function after tuple deletion, failing
the required `False` assertion at `tests/test_c2a_prime.py:206`. The
reviewer's single-name-drop and transitive-dependency twins also pass on
the unmodified implementation.

## Count

`judge.judge.counted_lines('.', Reviewed tree,
['sim/', 'harness/', 'tests/', 'pins/', 'tools/'])` is **8,362 / 8,400**,
leaving **38 lines**. The re-cut baseline was **8,204**, and the reviewer
pins add **158** physical Python lines. Kernel count is **450 / 500**.
This Markdown review adds no counted lines.

## Complete commit audit

The following is every commit from `git rev-list origin/main..HEAD` at
the reviewed head, newest first. Paths are each commit's changes, not a
net diff against a main branch that has subsequently advanced.

| Commit | Proposer trailer | Paths touched | SPEC §10.8 disposition |
|---|---|---|---|
| `bfd685ea3fc465bf34d792eb703f1670e16a173a` | `Proposer: reviewer reviewer-2` | `pins/c2aprime.py`, `pins/pins.py` | Within reviewer `pins/`. |
| `1c1b27f86f5812d783ddf210968e65f45b9e9281` | `Proposer: counsel counsel-2` | `SPEC.md`, `judge/scope.json` | Outside ordinary counsel proposal paths; expressly the opening cap preparation carried by the sovereign push under v7 §The window, following `cd9d8eba36180401c0c1bc4c23e52ded4eef9fd9`. Only cap/history changes; party scopes are unchanged. |
| `05dfceee9820af4bd9a8eee26503d5481793107a` | `Proposer: builder builder-2` | `tests/test_c2a_prime.py`, `tools/status.py` | Within builder `tests/` and `tools/`. |

The commit carrying this review is to have `Proposer: reviewer reviewer-2`
and touch only `transcripts/REVIEW-C2a-prime-code.md`, within reviewer
`transcripts/`. Its hash cannot be embedded in itself; the final push audit
checks that additional commit against this row's exact trailer and path.
There are no missing-trailer commits in the audited range. C2a's cap
precedent likewise has `Proposer: counsel counsel-2`, touching `SPEC.md`,
`judge/scope.json` and its opening note. It is a trusted-base push precedent,
not an expansion of counsel's ordinary proposal permissions.
