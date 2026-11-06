# W5 pins — BRIEF-C2b Amendments 6 and 7

Reviewer: reviewer reviewer-2; model openai/gpt-6-astra; 2026-11-06.
Builder base: `dc4120b23272c267bc1f77fdcc7fe037857892a6`.
Branch: `review-w5-pins-67`.
Texts read: `origin/main` at `7277a8706b34ed3252545f99292f65b9c7533c3c`,
`transcripts/BRIEF-C2b-draft.md` Amendments 6/7 and
`transcripts/REVIEW-C2b-am67-astra.md` F7/F8.

## Result

All 21 added amendment/F7 mutants are KILLED with passing twins. No needed twin
is missing from the builder's tests. No twin was written by the reviewer.
The full documented runner returns 0: **146 KILLED, 0 SURVIVED, 0 STALE,
0 TWIN FAILED, 0 PENDING**, across 100 pins.

The builder base did not contain the earlier W5 pin registrations. This change
carries forward the five W5 pins and workflow pin from `origin/review-w5-pins`,
re-anchors the unrelated-entry and append-only mutants to the builder's current
code, registers `w5_redate`, and extends `w5_escalation_history` while keeping
`late_escalation_cleared`. The existing election attack pins remain registered.

## Commands and passing twins

Every command below was run with `TMPDIR="$PWD/transcripts"` and
`PYTHONDONTWRITEBYTECODE=1`; the pin commands also set
`JACK_KEY="$HOME/.ssh/jack-reviewer"`. Disposable repositories were created
inside this worktree and cleaned up afterwards.

```sh
python3 pins/run.py --only w5_overdue_escalates w5_done_is_an_entry w5_rows_append_only w5_inventory w5_redate w5_escalation_history workflow_steps_preserved --transcript transcripts/W5-pins-am67-targeted.txt
python3 pins/run.py --transcript transcripts/W5-pins-am67-full.txt
python3 -m unittest -v tests.test_due tests.test_workflow tests.test_pins.Registry
```

The targeted run returns 0, with 28 KILLED and all other result counts zero.
The unit command returns 0, with 11 tests passing. Its relevant passing lines:

```text
test_w5_done_is_an_entry (tests.test_due.DueTest.test_w5_done_is_an_entry) ... ok
test_w5_escalation_history (tests.test_due.DueTest.test_w5_escalation_history) ... ok
test_w5_inventory (tests.test_due.DueTest.test_w5_inventory) ... ok
test_w5_overdue_escalates (tests.test_due.DueTest.test_w5_overdue_escalates) ... ok
test_w5_redate (tests.test_due.DueTest.test_w5_redate) ... ok
test_w5_rows_append_only (tests.test_due.DueTest.test_w5_rows_append_only) ... ok
test_workflow_steps_preserved (tests.test_workflow.WorkflowTest.test_workflow_steps_preserved) ... ok
test_pins_are_well_formed (tests.test_pins.Registry.test_pins_are_well_formed) ... ok
```

The runner also passes each unedited disposable twin before running that pin's
mutants; it cannot report KILLED after a failed twin.

## Per-mutant lines

These are the statuses in `W5-pins-am67-targeted.txt`. Every row's unedited
pin twin passes as listed above.

| Pin | Mutant | Result | Builder witness (`tests/test_due.py`) |
|---|---|---|---|
| w5_redate | redates_refused | KILLED | allowed re-dates, 106–114 |
| w5_redate | redates_ignored | KILLED | new dues printed, 106–114 |
| w5_redate | any_redate_admitted | KILLED | unlisted runbook-c2b, 115 |
| w5_redate | redate_id_only | KILLED | wrong due for c2b-report, 116 |
| w5_redate | second_redate_admitted | KILLED | duplicate, 117 |
| w5_redate | redate_seq_unchecked | KILLED | seq 1565, 117 |
| w5_redate | redate_before_row_admitted | KILLED | re-date before original, 118 |
| w5_redate | redate_after_done_admitted | KILLED | re-date after discharge, 118; lawful order, 107 |
| w5_redate | redate_why_unchecked | KILLED | non-string why, 119–121 |
| w5_redate | redate_seq_type_unchecked | KILLED | float 1564.0, 120 |
| w5_redate | redate_extra_keys_admitted | KILLED | extra key, 121 |
| w5_redate | redate_missing_keys_defaulted | KILLED | each missing key, 122; four failures |
| w5_redate | c2b_report_redate_refused | KILLED | allowed pair, 106; independent twin, 106 |
| w5_redate | c2c_brief_redate_refused | KILLED | allowed pair, 106; independent twin, 107 |
| w5_escalation_history | late_escalation_cleared | KILLED | late cases observed twice, 129–139 |
| w5_escalation_history | cited_entry_alone | KILLED | pre-due citation, post-due merge, 130 |
| w5_escalation_history | merge_alone | KILLED | pre-due merge, post-due citation, 131 |
| w5_escalation_history | last_merge | KILLED | first merge on time, second late, 132 |
| w5_escalation_history | any_line_with_id | KILLED | original-row merge precedes late discharge merge, 130/136 |
| w5_escalation_history | no_merge_required | KILLED | no discharge merge, 133/136–139 |
| w5_escalation_history | never_effective | KILLED | on-time discharge, 129 |
| w5_escalation_history | whole_log | KILLED | F8 equal-timestamp sequence prefix, 142–147 |
| w5_overdue_escalates | overdue_printed_open | KILLED | overdue and exact-due twins, 55–61 |
| w5_done_is_an_entry | unrelated_entry_discharges | KILLED | unrelated seq 8; naming-entry twins, 63–74 |
| w5_rows_append_only | earlier_row_edit_accepted | KILLED | edited what; append-only twins, 76–86 |
| w5_inventory | missing_seed_accepted | KILLED | missing seed and present twins, 93–98 |
| workflow_steps_preserved | sample_step_dropped | KILLED | test_workflow.WorkflowTest.test_workflow_steps_preserved |
| workflow_steps_preserved | gate_skipped_on_failure | KILLED | test_workflow.WorkflowTest.test_workflow_steps_preserved |

## F7 and F8 discrimination checked

The before-row mutant processes original rows first, preserving the relative
order of subsequent re-dates and discharges. It actually admits the illegal
before-row case rather than dying at a remaining key-existence check. A separate
diagnostic run confirmed the assertion at line 125 receives exit 0 and the new
`c2b-report` due, instead of exit 2 and `W5: malformed COUNSEL-DUE file`.

The whole-log mutant changes only the merge enumeration to the fixture's HEAD
log. Cited-entry validity still uses the supplied prefix; `effective <= now`
is unchanged. A separate diagnostic run confirmed its sole failure is at line
146: the prefix ends at seq 8 at 05:00, while the discharge merge is seq 9 at the
same timestamp. The mutant prints `done seq 7 on time`; the legal projection
prints `OPEN`. The full-prefix twin at line 147 passes on the unedited code.
Thus this is F8's discriminating case, not Amendment 7 twin 6's insufficient
earlier-as-of case.

The builder also supplies exact-due and byte-different same-id cases at lines
133–134 and 148–156. No amendment-specific coverage gap was found.

## Delivery

This is pre-opening branch work, committed with `Proposer: reviewer reviewer-2`
and pushed to `origin/review-w5-pins-67`. Proposal awaits C2b's opening cap.
No forecast is entered.
