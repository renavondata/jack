# Reviewer pins: promotion evaluator under judge/

Branch: `move-promotion-judge`. Reviewed pin-code head:
`edd9da0d1cc1c30eb6157fdee15f9e3d1f35a24a` (the report/transcript commit
follows it; the final response gives the pushed branch head). Reviewer:
`openai/gpt-6.1-sol`, runner issue 1198, continuing runner issue 1189.

## Custody and starting checks

The resumed session found HEAD `23df222721bda6a5078ab12e4d7e315b23bd2e5e`,
two reviewer commits ahead of `origin/move-promotion-judge`, with only
`pins/pins.py` modified and `pins/replay.py` untracked. The two commits were
`555e50da` (retargeting and installed fixtures) and `23df2227` (item 15 pins),
both with reviewer Proposer trailers from runner 1189. I read their changes,
kept them, and pushed them by the prescribed recovery rule. Counsel's
`57022d72e56fcf53015f949e0eae197b0a839a6b` was already their ancestor.
The builder's `7b03d75d4d3a429be9054d97136721feb605aaad` was an ancestor of
the fetched push branch. Fetch and all ancestry checks passed.

`sha256sum SPEC.md`:
`72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2`.
`python3 -m unittest tests.test_law`: exit 0, one test, OK.
No granted text was edited.

These pins ride the push with the code. This departs from RUNBOOK's cold,
history-free Working copies procedure: the pins cannot pass on main before
the trusted evaluator arrives, while the installing push itself checks them.
The precedent is `transcripts/sessions/c2a-prime-pins.md`: “the pins ride the
opening push with the code”. The replay pin also needs the runner's real git
history because its disposable code copy has neither `.git` nor transcripts.

## Required checks

### (a) Unit suite

`python3 -m unittest discover -s tests -t .`: **exit 0**, **311 tests**,
`OK (skipped=1)`. Test time **397.810 seconds**, command elapsed
**397.954 seconds**. This includes `tests/test_pins.py` and
`tests/test_law.py`. The full suite ran under `nohup` in the background and
its log was polled to completion.

### (b) Complete pin run

`python3 pins/run.py --transcript transcripts/evidence/move-promotion-judge-pins-review.txt`:
**exit 0**, elapsed **535.612 seconds** (8m55.612s):

```text
KILLED 158, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0
```

All 107 twins passed. The full run exercised every retargeted mutant and
all eight mutants of the seven repaired installation-prefix twins. Their
failures are the named behavioural assertions, including kernel2 execution
with the wrong extracted mode and the self-check exit code. The run used
`nohup` in the background; its completion log supplied exit and elapsed time.

Transcript: `transcripts/evidence/move-promotion-judge-pins-review.txt`.

### (c) Counted lines and kernel

`judge.judge.counted_lines` applied to git objects with the tree's own
`judge/scope.json` counted prefixes gives **8,248**, below **8,400**.
The staged tree was counted before committing the replay pin. Report and
transcript paths contribute no counted Python lines.

`python3 tools/count_kernel.py`: exit 0:

```text
kernel/__init__.py            0
kernel/check.py             138
kernel/log.py               172
kernel/sig.py               140
total                       450
```

### (d) Reviewer-only diff after counsel

`git diff --name-only 57022d72e56fcf53015f949e0eae197b0a839a6b HEAD`
at the report commit lists only reviewer paths:

```text
pins/c2a.py
pins/fixtures.py
pins/pins.py
pins/promotion.py
pins/replay.py
transcripts/PINS-move-promotion-judge.md
transcripts/evidence/move-promotion-judge-pins-review.txt
```

### (e) Explicit seven-pin check

All seven names are registered. `EXPECTED` and the registry length are both
**107**, up from 100 before the seven additions. This command exited 0:

```text
python3 pins/run.py --only promote_while_unmet evidence_substituted promote_tree_changed promote_retroactive evaluator_not_in_force promote_judged_once replay_drift
KILLED 11, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0
real 4m25.412s
```

Every twin passed. The whole seven-pin run, including replay's twin and all
three replay mutants, took less than five minutes. `python3 -m py_compile`
passed for every changed Python file: `pins/c2a.py`, `pins/fixtures.py`,
`pins/pins.py`, `pins/promotion.py`, and `pins/replay.py`.

## 1. Pins whose targets moved

For every row below the edit's find/replacement strings are retained;
only its target moves. Status targets move from `tools/status.py` to
`judge/status.py`, value targets from `tools/value.py` to `judge/value.py`,
and the two extracted-entry targets from `tools/entry.py` to
`judge/entries.py`. This preserves the same mutation and behavioural
distinction at the function's new home. The counts are changed mutant
registrations, including shared mutants used by more than one pin.

| Pin | Re-aimed mutants | Target now |
|---|---:|---|
| w4_promote_unmet | 1 | judge/status.py |
| promote_refused | 1 | judge/status.py |
| run_verified | 2 | judge/status.py |
| wealth_arithmetic | 1 | judge/status.py |
| item_before_open | 1 | judge/status.py |
| item_is_batch | 1 | judge/status.py |
| regroup_scored_items | 1 | judge/status.py |
| expired_writ_zero | 2 | judge/status.py |
| repair_erased_from_success | 1 | judge/status.py |
| repair_taints_all_open | 2 | judge/status.py |
| replay_merge_110 | 1 | judge/status.py |
| late_report_immutable | 2 | judge/status.py |
| sovereign_resolution_zero | 1 | judge/status.py |
| window_from_the_promote | 2 | judge/status.py |
| evidence_unhashed | 1 | judge/status.py |
| ratio_misclassified | 1 | judge/status.py |
| veto_c1b | 1 | judge/status.py |
| map_printed | 1 | judge/status.py |
| worked_table | 1 | judge/entries.py |
| forecast_before_cutoff | 1 | judge/value.py |
| rigged | 1 | judge/value.py |
| revision | 1 | judge/value.py |
| weights_from_resolved_prefix | 1 | judge/value.py |
| abstention_is_base | 1 | judge/value.py |
| one_event_one_key | 1 | judge/value.py |
| grouping_by_principal | 1 | judge/value.py |
| uniform_prior | 1 | judge/value.py |
| no_learning_rate | 1 | judge/value.py |
| exact_probabilities | 1 | judge/value.py |
| per_type_base | 1 | judge/entries.py |
| bounded_difference | 1 | judge/value.py |
| lambda_predictable | 1 | judge/value.py |
| factor_algebra | 1 | judge/value.py |
| window_from_the_push | 1 | judge/value.py |
| wealth_continues | 1 | judge/value.py |
| second_window_from_the_end | 2 | judge/status.py |
| second_window_end_is_v5 | 2 | judge/status.py |
| second_window_cap | 2 | judge/status.py |
| offlog_from_second_opening | 2 | judge/status.py |
| promote_refused_before_end | 2 | judge/status.py |
| window_fix_is_decision | 12 | judge/status.py |
| window_fix_not_retroactive | 2 | judge/status.py |
| process_unchanged_from_opening | 5 | judge/status.py |

That is 69 retargeted registrations. The builder's 68 PENDING rows included
the unchanged `tools/jack` mutant in `promote_refused`: one absent sibling
target made the runner label both PENDING. The other two retargetings are
`worked_table`'s STALE mutant and `per_type_base`'s `base_per_dataset`, hidden
by its failing twin.

`pins/c2a.py` now imports status/value from judge, repairing its own fixtures
for `per_type_base` and the other C2a cases. Synthetic histories still write
the historical evaluator source to `tools/status.py`; that is the tree path
the evaluator's two historical reads intentionally use. Score mutations
still target `tools/entry.py`, where that score code remains.

## 2. Seven twins adapted to signed installation prefixes

Only assumptions about the installed fixture's longer log changed. The
named behavioural assertions and mutant edits remain.

| Pin | Fixture repair and behavioural kill |
|---|---|
| charter_edit_unrecorded | `charter_judged` computes activation after the actual log length, rather than height 9. An unrecorded charter edit must refuse and a matching amendment must pass. `charter_unchecked` admits the former. |
| amend_stale | The same relative activation repair lets the twin reach the charter comparison. `genesis_charter_compared` ignores the latest amendment and admits a stale charter. |
| freeze_ignored | Use activation offsets 3 and 2 from the current prefix: a push strictly inside the freeze refuses, a push at activation passes. `amendment_freeze_unchecked` admits the inside push. |
| one_act_amendment | Activate after the actual prefix rather than at 9. An amend without transmutation refuses and one with it passes. `transmutation_unchecked` admits the one-act amendment. |
| foreign_object_admitted | Record a signed later push after modifying trunk's trusted base, preserving the installed signed suffix instead of rebinding genesis. Regular-file twins pass; `mode_unchecked` admits proposal foreign objects and `trusted_mode_unchecked` admits the trusted gitlink. |
| kernel2_unrunnable | The helper reports actual log length plus its recording push, and that push replaces rebinding genesis. `modes_ignored` loses the executable helper's git mode, so the healthy runnable-helper case fails specifically at kernel2 execution. |
| selfcheck_blind | Use the same actual count and recording push. The executable-helper twin passes; the nonexecutable-helper trunk must fail. `judge_errors_ignored` turns that self-check refusal into exit 0. |

## 3. Six item-15 pins

These use disposable signed histories with installing pushes. Tests run in
subprocesses rooted at the runner's disposable copy, so they exercise its
mutated judge. The builder's promotion fixtures are imported without editing
tests. Lawful promotion/attestation cases supply positive twins.

| Pin | Mutants and what kills them |
|---|---|
| promote_while_unmet | `refusal_admitted` removes the lawful-line check. A judged promotion whose synthetic evaluator returns a failed criterion is wrongly accepted, violating the expected `promote_unmet` refusal. The lawful self-check and attested evidence pass on the twin. |
| evidence_substituted | `hash_unchecked` removes evidence SHA-256 equality. The run file exists, but the signed entry names a different hash; admitting it fails the expected refusal. Valid evidence, including later replacements that do not alter the entry commit, passes. |
| promote_tree_changed | `other_paths_admitted` removes the exact changed-path set check; a promotion commit changing README is admitted. `side_entry_ignored` skips non-first-parent entry commits; the same signed line has a clean main entry commit and a bad side entry commit changing README, and must still refuse. Clean single-entry promotions pass. |
| promote_retroactive | `earlier_promotions_judged` removes the installation lower bound, wrongly judging a historical promotion without the new evidence shape. `ungranted_spec_installs` bypasses the earlier-grant hash match, wrongly accepting a push whose SPEC no earlier grant names. The twin leaves the old promotion unjudged and refuses the ungranted installation. |
| evaluator_not_in_force | `assessed_digest_unchecked` removes assessed-tree digest enforcement. A promotion after an unrecorded trusted change remains unlawful even when a later push records that base; admitting it fails the expected refusal. A lawful promotion still passes after a later evaluator is replaced with a raising evaluator: the old assessed evaluator alone judges it. |
| promote_judged_once | `old_promotions_skipped` restricts judging to entries added since trunk. A `[skip ci]` promotion is followed by an unrelated commit without any intervening judge run; both lawful and unlawful cases are checked then. Skipping the old unlawful promotion violates the required refusal. |

All these mutants edit `installing_push` or `promotion_checks` in
`judge/judge.py`; none relies on a missing path or syntax error.

## 4. replay_drift

The pin reads the frozen table and git blobs from the real runner repository,
not its history-free copy, and checks the table's granted SHA-256:
`6d647d09b0e02f0b3e1ac785bdf8e13fa223491501d6a24a1886783b9458c4dd`.
Rows are checked against T's first-parent chain:

| Row | Commit | Expected output |
|---:|---|---|
| 300 | 7f4d33b77e66eaebead1a0f2a221a4185cfb45a3 | 46 lines, unmarked, exact bytes and exit 0 |
| 400 | 09493f64a9b0c9bcfab437f13945c5ec2ecd6c79 | 41 lines, unmarked, exact bytes and exit 0 |
| 593 | b88d318ea9bba0c8701cd148a0d75e6f6af11f6a | 44 lines, only the two granted marks, exit 0 |

Each row runs the disposable copy's evaluator with the row's arguments and
evidence. A shared, no-checkout clone sets HEAD to the row's commit and the
pin writes that commit's log to the named log file. This supplies the tree
the evaluator reads through git without a full checkout. All unmarked stdout
bytes and exit status are compared; on row 593 only criterion 3's stipulated
replacement and the stipulated promotion-line failure removal are allowed.

After output comparison, the pin verifies the frozen parent blobs' named
status/value hashes and compares the disposable moved files byte for byte
against those blobs with precisely their allowed import substitutions and
the one first-parent walk substitution. The move's parent is fixed as
`2d99d2427296df1174a55f41459058d5f6b65a8f`, parent of the move commit
`c9d2d9ba3cd340ac5911cb7cea84d4f5afb34ae7`.

| Mutant of judge/status.py | Behavioural kill |
|---|---|
| unmarked_output_changed | Changes the printed J7 label. An unmarked row's stdout differs, failing before the bytes check. |
| marked_walk_regressed | Removes the added `--first-parent`. Row 593 prints criterion 3 as False and retains its promotion refusal, contrary to the grant's marks; fails before the bytes check. |
| other_source_bytes | Adds a comment to the parser definition. The sample outputs still match; the exact moved-source bytes check alone kills it. |

All find strings are single-occurrence edits in the current code. The
unmodified evaluator passes every row and both byte comparisons. The pin
also enforces a five-minute elapsed bound on each invocation.

## Text not pinned and outstanding sovereign work

No requested pin required weakening its twin, and no granted sentence was
found inconsistent with the builder's code by these pins.

Three pre-push requirements remain outstanding and were **not done here**:

1. **Full acceptance replay**: every row of
   `spec/vectors/promotion-replay.json`, and every first-parent commit after
   its T up to the move's parent. SPEC says, “The move passes only if, run as
   each row states, it prints every unmarked line byte for byte as recorded,
   every marked line as its mark states, and the same exit status; and if, at
   every first-parent commit after T up to its parent, its run prints what
   the frozen evaluator's run prints there, under the same marks, and exits
   with the same status.” `replay_drift` deliberately samples three rows;
   its pin run is not this complete acceptance replay.
2. **Merge fresh main into this branch immediately before the sovereign's
   push**, as `v_push` requires. Main moves hourly; no main merge was done
   in this reviewer session.
3. **The early-end amendment in force and a fresh veto ending C2a-prime**,
   which the 20 November ruling, answer 17, puts before the push. These are
   the sovereign's acts.

The handoff is a git push of this branch. The sovereign applies the trusted
base with his push procedure.
