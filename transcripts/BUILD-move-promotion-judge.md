# Builder report: move-promotion-judge

Built to the SPEC granted at seq 6851. Checked code commit:
`42d7ced8025a1c92cd65c9a33b13f9b867fd1ff6`. The final response records the
branch tip after this report and the pin transcript are committed.
`origin/main` for the comparisons below is
`3282d035834b21cc9a2470b980e2c96a5e4a10a0`.

## Starting checks and custody

- `git fetch -q origin main move-promotion-judge`: exit 0.
- `git status --porcelain`: empty.
- `git log --oneline origin/main..origin/move-promotion-judge`: exactly
  `2d99d242 SPEC §10 item 15 promote_unmet ...`.
- HEAD and origin/move-promotion-judge both named
  `2d99d2427296df1174a55f41459058d5f6b65a8f`; no reset was necessary.
- SPEC SHA-256:
  `72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2`.
- Required RUNBOOK paragraph on origin/main: count 1.
- No builder change to SPEC.md, CHARTER.md, RUNBOOK.md, LAW.md,
  judge/scope.json, pins/ or spec/vectors/. Comparing those paths with the
  starting commit `2d99d242` is empty. The SPEC change against origin/main
  is the sovereign's initial counsel commit.
- No jack verb was run against this checkout, no proposal or PR was opened.
  Verb tests operate only on their disposable synthetic repositories.

## Built

1. Moved status/value under judge/, extracted now/read_log/resolution_rates
   unchanged to judge/entries.py, and updated live callers. Historical
   synthetic-tree paths and the evaluator's two historical source reads
   remain tools/status.py.
2. Item 15 runs after items 11–14, including on the self-check path. It finds
   the installing push by its oldest first-parent push commit and earlier
   SPEC grant; checks every entry commit of every later promotion on every
   run; checks evidence shape, paths, modes, hashes, parent, exact prefix,
   changes and assessed digest; extracts the assessed kernel/ and judge/;
   uses the evaluator's own main to build and run its subject parser, then
   inputs and assess with decision unset; never runs report. Errors and
   absent history refuse as promote_unmet. No evaluator timeout is set.
   The judge report lists the checked files under attested.
3. Promote requires acts evidence, retains its existing acts attestation,
   and adds body.evidence {run,runs,acts}, each {path,sha256}. It commits the
   exact three assessed byte streams at fresh paths with log.jsonl, on the
   assessed HEAD, and nothing else.
4. tests.yml fetches full history. Tests cover installing-push provenance,
   conditions (a)–(d), unknown subjects, evaluator errors, later evaluator
   changes, skipped CI, multiple entry commits, malformed ancestor logs,
   merge parents, attested reporting, the real promote ending and the
   first-parent merge regression.

The older synthetic judge fixtures now include actual signed grants and
pushes past seq 5564. Their large, valid padding prefixes are generated
with standard-library ctypes bindings to OpenSSL. Only disposable kernels
memoise those verified signatures; all other kernel checks still run,
uncached signatures use the real kernel verifier, and the first and last
generated lines are cross-checked with that verifier. Production kernel
files are unchanged.

## Required checks

### (a) Unit suite

`python3 -m unittest discover -s tests -t .`: exit 1, 311 tests,
two permitted failures:

- `tests.test_law.Citations.test_every_citation_resolves`: LAW.md still
  cites tools/status.py, which moved. Counsel must update it.
- `tests.test_pins.Registry.test_pins_are_well_formed`: the first stale
  target is w4_promote_unmet's tools/status.py. Reviewer must update it.

Neither test was edited. No other test fails. Preliminary runs exceeded
the command bound while fixtures repeatedly checked the long installation
prefixes; the final complete run took 405.442 seconds, with one skip
(this OpenSSH build also rejects S >= L, so that named difference is absent).
The committed-tree digest parity passed both separately and in the final suite.

### (b) Pins

`python3 pins/run.py`: exit 1.
Final repeated run, with a saved table:
`python3 pins/run.py --transcript transcripts/evidence/move-promotion-judge-pins.txt`.

Result: **KILLED 69, SURVIVED 0, STALE 1, TWIN FAILED 8, PENDING 68**.
The saved table lists every mutant, including every PENDING row. PENDING
is the runner's label for a missing target, not a passing acceptance test.

Nonpassing pins other than the missing-path group:

| Pin | Status | Only a moved path/text? | Cause |
|---|---|---|---|
| worked_table | STALE | Yes | Its resolution_rates mutation text left tools/entry.py for judge/entries.py. |
| per_type_base | TWIN FAILED | Yes | pins/c2a.py still imports value and status from tools. |
| charter_edit_unrecorded | TWIN FAILED | No | Its positive amendment uses fixed activate_at 9, below the new installed fixture's seq; the amendment is invalid, leaving charter_mismatch. |
| amend_stale | TWIN FAILED | No | Fixed activate_at 9 is below the installed fixture's seq. |
| freeze_ignored | TWIN FAILED | No | Fixed activation heights 3/4 are below the installed fixture's seq. |
| one_act_amendment | TWIN FAILED | No | Fixed activate_at 9 is below the installed fixture's seq. |
| foreign_object_admitted | TWIN FAILED | No | The trusted-file twin rebinds genesis after the installed fixture already has a signed suffix, breaking that suffix's parent link. |
| kernel2_unrunnable | TWIN FAILED | No | Its helper hard-codes entries 1 although an installed fixture has 5566 entries, and it also rebinds genesis after the signed suffix. |
| selfcheck_blind | TWIN FAILED | No | Its healthy helper has the same entries-1/rebound-genesis assumptions. |

All **68 PENDING mutants** fail to exercise their target only because the
evaluator paths moved. Their pin names, grouped by missing target:

- **tools/status.py:** w4_promote_unmet, promote_refused, run_verified,
  wealth_arithmetic, item_before_open, item_is_batch, regroup_scored_items,
  expired_writ_zero, repair_erased_from_success, repair_taints_all_open,
  replay_merge_110, late_report_immutable, sovereign_resolution_zero,
  window_from_the_promote, evidence_unhashed, ratio_misclassified,
  veto_c1b, map_printed, second_window_from_the_end,
  second_window_end_is_v5, second_window_cap, offlog_from_second_opening,
  promote_refused_before_end, window_fix_is_decision,
  window_fix_not_retroactive, process_unchanged_from_opening.
- **tools/value.py:** forecast_before_cutoff, rigged, revision,
  weights_from_resolved_prefix, abstention_is_base, one_event_one_key,
  grouping_by_principal, uniform_prior, no_learning_rate,
  exact_probabilities, bounded_difference, lambda_predictable,
  factor_algebra, window_from_the_push, wealth_continues.

The runner also labels promote_refused/promotion_check_dropped PENDING
with the misleading detail tools/jack does not exist yet: tools/jack
exists, but that pin's other mutant targets the missing tools/status.py,
and the runner marks every mutant PENDING when any target is absent.

The seven non-path-only twin failures above require reviewer fixture
updates too. No reviewer-owned pin was changed to conceal them.

### (c) Counts

`python3 tools/count_kernel.py`: exit 0:

```
kernel/__init__.py            0
kernel/check.py             138
kernel/log.py               172
kernel/sig.py               140
total                       450
```

Using judge.judge.counted_lines on git objects, with each tree's counted
prefixes, exactly as item 10 does:

| Tree | Counted lines |
|---|---:|
| origin/main | 8347 |
| checked code HEAD | 8072 |
| difference, HEAD minus origin/main | **-275** |

The move's push should therefore state a **net drop of 275 counted lines**.
The current cap remains 8400; neither cap nor scope was changed. Report
and pin-table files under transcripts/ add no counted lines.

### (d) Exact move diff

`git diff -M origin/main -- tools/status.py tools/value.py judge/status.py judge/value.py`
shows two 99%-similar renames and exactly these three changed lines:

```diff
diff --git a/tools/status.py b/judge/status.py
rename from tools/status.py
rename to judge/status.py
@@ imports
-from tools import value as val  # noqa: E402
+from judge import value as val  # noqa: E402
@@ c2a_tree_evidence
-        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", f"{start}..{rev}").decode().split())
+        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", "--first-parent", f"{start}..{rev}").decode().split())
diff --git a/tools/value.py b/judge/value.py
rename from tools/value.py
rename to judge/value.py
@@ imports
-from tools.entry import now, read_log, resolution_rates
+from judge.entries import now, read_log, resolution_rates
```

The two historical tree reads at tools/status.py are unchanged.
The move's parent holds the specified status/value hashes, respectively
`b255520996cef0ec20691c46cbc236ce5826dc166d16697762fa85f30fe86acb`
and `11440c89429513b49922658d419b0bc6c8e625b15701b335576eedf537cf9992`.
AST source-segment comparison of each of read_log, now and resolution_rates
against tools/entry.py in that parent is byte-identical, including its body.

### (e) Three replay rows

`python3 tests/promotion_replay_spot.py`: exit 0. The runner reads the table
from origin/main, verifies each index against T's first-parent chain,
checks out each assessed tree in a disposable local clone, supplies the
specified run/runs/acts, and invokes this checkout's moved evaluator.

| Row | Commit | Result |
|---:|---|---|
| 592 | 6c0566c3d5b23bde453cda5c016de4cec9c79bc4 | Exact stored stdout, 44 lines, exit 0. |
| 593 | b88d318ea9bba0c8701cd148a0d75e6f6af11f6a | 44 lines, exit 0; only 0-based lines 26 and 43 differ. |
| 705 | 8130c751c1df85df4063d4174a3a886098530912 | 46 lines, exit 0; only 0-based lines 26 and 45 differ. |

At 593/705 criterion 3 changes False SHORT to True met. At 593 the promotion
line becomes lawful; at 705 only criterion 3 and one adjoining separator
leave the refusal list. Every other line is byte-identical. The full replay
acceptance test remains the reviewer's work, as requested.

## RUNBOOK on origin/main: remaining old descriptions/paths

Line references are at the origin/main commit named above.

- **188:** decision body described generally as {kind,subject}; promotions
  now also carry evidence (and retain their prior acts attestation).
- **191–198:** tools/status.py invocation, optional --acts and the old
  body shapes, including {kind,subject} without --acts. Superseded for the
  installing push by the paragraph immediately following it, 200–207.
- **202:** tools/status.py remains as the explicitly replaced old path in
  the transition paragraph itself.
- **207:** the transition says tools/jack does not yet implement it until
  the push; this ceases to describe the installed code after that push.
- **365–368:** the clerk description still describes an unlawful promote
  as a printed sovereign REPAIR. The moved evaluator retains this history
  reporting byte for byte; item 15 separately refuses post-installation acts.
- **408:** the sample command still begins python3 tools/status.py, though
  its parenthesis explicitly gives judge/status.py after the move.
- **415–425:** the older overview does not mention committing evidence;
  its future C2c-1 clauses take no --acts and say the verb writes nothing
  to the tree (418–420), contrary to the new evidence commit requirement.
  Those later-window clauses were not built here.

## Unimplemented text

No sentence of the granted item 15 or the granted evaluator-move paragraph
was found unimplementable. The reviewer-owned pins and counsel-owned LAW
citations remain outstanding as listed above. No C2a-3, C2c-1 or later-window
mechanism was built.

The literal git diff --stat origin/main is included in the final response.
Since this branch starts at the published counsel commit rather than at
origin/main's newer tip, that two-tree stat also shows main-only log and
transcript additions as deletions. They are ancestry differences, not
builder deletion commits; git diff 2d99d242 HEAD isolates the builder's work.
