# W5 pins — BRIEF-C2b Amendment 8

Reviewer: reviewer reviewer-2; model openai/gpt-6-astra; 2026-11-06.
Branch: `review-w5-pins-8`.
Base: `bd6e483d7bbca8bfffd245df004273293f3d498b` (`review-w5-pins-67`).
Builder: `43042a7301a318d26c8d73040f20aa857cedff0b` (`builder-c2b-status`).
Integration: `57a5b02` (merge, carrying `Proposer: reviewer reviewer-2`).
Texts read on `origin/main`: BRIEF-C2b-draft Amendment 8,
REVIEW-C2b-am8-astra F6/F7, and COUNSEL-OPEN row 42.

## Result

Registered `c2b_history_from_w5` against the builder's
`tests.test_status.C2bCounselTest.test_c2b_history_from_w5`, with 19 mutants.
**16 KILLED, 3 SURVIVED.** All six explicitly named Amendment 8 mutants are
KILLED. All 20 existing builder subtests pass on the unedited implementation.
The all-mutants-KILLED requirement is not met: the three surviving mutants below
lack distinguishing builder twins. They remain registered and fail the runner.
No builder test or twin was changed or added.

The full documented runner reports **162 KILLED, 3 SURVIVED, 0 STALE,
0 TWIN FAILED, 0 PENDING**, across 101 pins, and exits 1. Every pre-existing
mutant, including all Amendment 6/7 mutants, remains KILLED after the merge.
The complete runner output is `transcripts/PINS-C2b-am8-full.txt`.

## Commands

Commands ran with `TMPDIR="$PWD/transcripts/.w5-pin-tmp"`,
`PYTHONDONTWRITEBYTECODE=1`, and for the pin runner
`JACK_KEY="$HOME/.ssh/jack-reviewer"`. Scratch data stayed within this worktree's
`transcripts/` directory; it was removed after verification.

```sh
python3 pins/run.py --only c2b_history_from_w5 --transcript transcripts/PINS-C2b-am8-focused.txt
python3 pins/run.py --transcript transcripts/PINS-C2b-am8-full.txt
python3 -m unittest -v tests.test_status.C2bCounselTest.test_c2b_history_from_w5 tests.test_due tests.test_workflow tests.test_pins.Registry
```

The initial focused run found the same 16/3 split. The full runner was repeated
after making the whole-criterion mutant bypass the complete conjunction and
updating the registry count to 101; the committed full transcript is that final
run. The initial focused transcript was removed. The unit command passes all
12 tests, including the registry's unique-name, count and single-occurrence
mutation-anchor checks. KILLED results in the runner require a passing unedited
disposable twin first.

## New mutant results

All rows belong to `c2b_history_from_w5`. Witness names below are the builder's
existing subtests at `tests/test_status.py:333–414`.

| Mutant | Result | Distinguishing witness or gap |
|---|---|---|
| every_row_gated | KILLED | twin 1: pre-landing late discharge |
| every_row_excused | KILLED | twin 2: missing post-landing history |
| whole_criterion_excused | KILLED | twin 4: overdue and still undone |
| last_landing | KILLED | twin 5: due between the first and second landings |
| landing_equality_gated | KILLED | twin 6: due equals landing |
| no_landing_gated | KILLED | twin 7: no landing |
| timely_history_required | KILLED | on time; exactly due |
| exact_due_history_required | KILLED | exactly due; changes the projection's late classification at equality |
| first_supplied_tick_accepted | KILLED | skipped prefix; equal-ts skipped prefix |
| tick_clock_lower_unchecked | KILLED | backdated clock |
| tick_clock_upper_unchecked | KILLED | late clock |
| equal_ts_first_tick_rejected | KILLED | equal-ts first prefix |
| tick_sequence_unchecked | KILLED | wrong sequence |
| unavailable_tick_tree_accepted | SURVIVED | no missing historical-prefix tree twin |
| unauthored_tick_accepted | KILLED | late-authored tick, absent at the first prefix |
| tick_bytes_unchecked | SURVIVED | no present-but-different historical tick bytes twin |
| landing_beyond_prefix | KILLED | equal-ts excluded landing; equal-ts excluded unreadable |
| nonmerge_landing | KILLED | non-merge marker |
| unreadable_landing_is_absent | SURVIVED | unreadable merge rejected earlier by due.project |

## Surviving mutants and missing discrimination

1. **Unavailable tick tree.** `status.prefix_tree` can return `None` when no
   ancestor contains exactly the required first-prefix log. The mutant accepts
   the supplied tick in that case while preserving its clock, sequence and
   ESCALATED-text checks. The builder commits a log tree for every action
   (`test_status.py:395`), so the required historical prefix exists in all its
   relevant fixtures. A distinguishing twin must have a valid opening and exit
   tree but no ancestor with that exact first-prefix log, and otherwise valid
   supplied tick text. This fixture is absent.

2. **Historical bytes.** The mutant removes only the comparison of the tick's
   historical bytes with the supplied exit-tree bytes. The late-authored case
   creates the path only later (`test_status.py:391–394`), so the separate
   historical-path-presence guard still rejects it. A distinguishing twin needs
   the path already present at the first prefix, with different bytes, then
   replaced by a purported historical ESCALATED print. This fixture is absent.

3. **Unreadable landing tree.** The mutant catches a failed `ls-tree` inside
   the landing scan and treats it as no marker. The builder's unreadable-tree
   fixture names an all-zero missing commit. Before the landing scan,
   `status.counsel_bound` calls `due.project` (`status.py:454`), which reads every
   merge through `due.merge_lines` and rejects that commit as unverified
   (`due.py:60–64,92–100`). The scan's altered error handling is never reached.
   Thus the existing fixture verifies whole-assessment refusal, but does not
   distinguish this landing-specific mutant. Testing that guard independently
   needs a landing-read failure that reaches it (for example a path-specific
   read failure after successful discharge reads), or an explicit determination
   that it is redundant under the immutable-tree assumptions. Survival here is
   not evidence that the current implementation accepts a missing git object.

These gaps belong with the builder; the reviewer has not supplied replacement
twins or weakened a mutant merely to obtain a green run.

## Existing builder twins

All these subtests pass unedited. “Met/unmet” is the expected criterion-8
outcome, not the test outcome.

```text
1 pre-landing                 PASS (met)
2 missing history             PASS (unmet)
3 first-prefix print          PASS (met)
4 undone                      PASS (unmet)
5 two landings                PASS (unmet)
6 equality                    PASS (met)
7 no landing                  PASS (met)
on time                       PASS (met)
exactly due                   PASS (met)
skipped prefix                PASS (unmet)
equal-ts skipped prefix       PASS (unmet)
equal-ts first prefix         PASS (met)
backdated clock               PASS (unmet)
late clock                    PASS (unmet)
late-authored tick            PASS (unmet)
wrong sequence                PASS (unmet)
equal-ts excluded landing     PASS (met)
equal-ts excluded unreadable  PASS (met)
non-merge marker              PASS (met)
unreadable tree               PASS (unmet/unverified)
```

## Amendment 6/7 and carried W5 results after integration

Each line is also present in the final full-run transcript. Their unedited
twins pass, both in the pin runner and in the 12-test unit run.

```text
w5_redate              redates_refused                KILLED
w5_redate              redates_ignored                KILLED
w5_redate              any_redate_admitted            KILLED
w5_redate              redate_id_only                 KILLED
w5_redate              second_redate_admitted         KILLED
w5_redate              redate_seq_unchecked           KILLED
w5_redate              redate_before_row_admitted     KILLED
w5_redate              redate_after_done_admitted     KILLED
w5_redate              redate_why_unchecked           KILLED
w5_redate              redate_seq_type_unchecked      KILLED
w5_redate              redate_extra_keys_admitted     KILLED
w5_redate              redate_missing_keys_defaulted  KILLED
w5_redate              c2b_report_redate_refused      KILLED
w5_redate              c2c_brief_redate_refused       KILLED
w5_escalation_history  late_escalation_cleared        KILLED
w5_escalation_history  cited_entry_alone              KILLED
w5_escalation_history  merge_alone                    KILLED
w5_escalation_history  last_merge                     KILLED
w5_escalation_history  any_line_with_id               KILLED
w5_escalation_history  no_merge_required              KILLED
w5_escalation_history  never_effective                KILLED
w5_escalation_history  whole_log                      KILLED
w5_overdue_escalates   overdue_printed_open           KILLED
w5_done_is_an_entry    unrelated_entry_discharges     KILLED
w5_rows_append_only    earlier_row_edit_accepted      KILLED
w5_inventory          missing_seed_accepted          KILLED
workflow_steps_preserved sample_step_dropped          KILLED
workflow_steps_preserved gate_skipped_on_failure      KILLED
```

## Delivery

Pre-opening reviewer branch work, with trailer `Proposer: reviewer reviewer-2`.
The branch is for push only; proposal awaits C2b's opening cap. No forecast or
ledger entry is part of this change.

## Re-run on a829a27

Merged builder commit `a829a274770f3fdb0c2a04098a84548ff14abdf0` as
`9ebb3a08709168392f2be5bcd9f620fb29d76528`, carrying
`Proposer: reviewer reviewer-2`. The builder adds the three distinguishing
twins in `tests/test_status.py`; no mutant or file under `tools/` changed.

Ran the full documented pin runner with reviewer credentials and temporary
files confined to this worktree:

```sh
TMPDIR="$PWD/transcripts" PYTHONDONTWRITEBYTECODE=1 JACK_KEY="$HOME/.ssh/jack-reviewer" python3 pins/run.py --transcript transcripts/PINS-C2b-am8-a829a27-full.txt
```

The three previously surviving mutants now report:

```text
c2b_history_from_w5              unavailable_tick_tree_accepted KILLED  (FAILED (failures=1))
c2b_history_from_w5              tick_bytes_unchecked         KILLED  (FAILED (failures=1))
c2b_history_from_w5              unreadable_landing_is_absent KILLED  (FAILED (failures=1))
```

All **19** mutants of `c2b_history_from_w5` are **KILLED**, and every other
pin retains its KILLED results. The unedited twins pass. The full runner exits
**0**, across **101 pins**, with totals:

```text
KILLED 165, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0
```

Full output: `transcripts/PINS-C2b-am8-a829a27-full.txt`.
