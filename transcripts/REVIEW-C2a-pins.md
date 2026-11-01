# C2a pins: 18 registered, 18 mutants KILLED (7,650 counted lines)

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 1 November 2026.
Branch: `review-c2a-pins`; baseline: `b5b445d` (PR #92 merged).
Contract: BRIEF-C2a draft v2 with Amendment 1, §Scope, §The statistic and
§Pins; REVIEW-C2a-v2 F7/F9.

## Measurements

* Before: **7,462** counted lines. After: **7,650**. Added: **188**;
  remaining under 7,800: **150**. All eighteen fit in the stated order.
* `EXPECTED = 88`: 70 existing pins plus 18 C2a pins.
* `python3 pins/run.py`: **112 KILLED**, **0 SURVIVED**, **0 STALE**,
  **0 TWIN FAILED**, **0 PENDING**. Every unedited twin passed.
* C2a subset: **18 pins, 18 mutants KILLED**.
* `python3 -m unittest discover -s tests -q`: **284 tests**, **OK (skipped=1)**.
* `git diff --check`: passed.

Line measurements use the judge's `counted_lines` and the counted set in
`judge/scope.json`; the staged-tree measurement was 7,650 before committing.
The requested HEAD command is run before and after the implementation commit:

```sh
python3 -c "from judge.judge import counted_lines; import json; s=json.load(open('judge/scope.json')); print(counted_lines('.', 'HEAD', s['counted']))"
```

## Registered mutants

Each test callable's docstring names its target path and exact
single-occurrence guard. Mutants edit disposable copies of the builder's
implementation. The fixtures execute that copy's imports in a subprocess.

| Pin | Named mutant | Result |
|---|---|---|
| worked_table | laplace_n_plus_3 | KILLED |
| forecast_before_cutoff | latest_forecast | KILLED |
| rigged | cutoff_forecast_included | KILLED |
| revision | second_replaces_first | KILLED |
| weights_from_resolved_prefix | terminal_weights | KILLED |
| abstention_is_base | abstention_half | KILLED |
| one_event_one_key | grouped_by_claim | KILLED |
| grouping_by_principal | two_keys_two_entrants | KILLED |
| uniform_prior | counsel_double | KILLED |
| no_learning_rate | eta_half | KILLED |
| exact_probabilities | one_float_division | KILLED |
| per_type_base | base_per_dataset | KILLED |
| bounded_difference | no_clip | KILLED |
| lambda_predictable | current_item_in_lambda | KILLED |
| factor_algebra | factor_plus_one_fiftieth | KILLED |
| window_from_the_push | from_brief_merge | KILLED |
| wealth_continues | reset_at_second_window | KILLED |
| promote_refused_value | signs_below_twenty | KILLED |

## Distinguishing witnesses

* `worked_table` uses the builder's independent entry reconstruction and exact
  published fixture comparison, including the three exact q fractions. Its
  wrapper supplies the published JSON to the disposable tree because the
  runner excludes `transcripts/` when copying.
* `rigged` retains the reconstructed 288–290 witness, the cutoff-equality and
  post-resolution attacks, and the signed simulator checks. Its additional
  twin moves just those three forecasts to the next unstarted window: 25
  events become 28, and all three forecasts are used. An initial reviewer
  fixture failure exposed shared args dictionaries in the reconstruction;
  the twin now replaces each moved forecast's args independently.
* `abstention_is_base` tests b=2/3, q=52/75 and the abstainer's likelihood and
  terminal weight. `one_event_one_key` uses genuinely distinct races for the
  two-event twin, and rejects an unkeyed forecast.
* The terminal-weight mutant recomputes the complete admissible-event
  likelihood product before q, including future resolutions; it does not
  substitute uniform or current-outcome-only weights for terminal weights.
* `per_type_base` adds two named freshness datasets plus a same-dataset,
  later-window twin. Both must retain the type-pooled b=2/3 on the second row.
* `factor_algebra` enumerates 21 nodes across three depth-three binary trees:
  b=1/2, 1/1000 and 999/1000. The next q abstains after outcome 1; actual
  preceding x values determine the stake. Opposite endpoints give exact
  x=±1, equality gives zero, and Fraction comparisons certify expectations
  without tolerance, including an adaptive equality node with positive stake.
  The +1/50 mutant violates the equality expectation, 51/50 > 1. This finite
  true-probability-b oracle complements F7/F1's general conditional-null proof.
* `window_from_the_push` includes both a brief merge and an opening push,
  cutoff equality at opening/attack-green, an admitted later event, missing
  attack evidence, and Amendment 1's fourteen-day maximum.
* `wealth_continues` reaches E>1 before a second-window boundary and checks
  unchanged rows, stakes, terminal weights and wealth, with separate window
  diagnostics. Its mutant resets capital at the first event of the new window.
* `promote_refused_value` reuses the signed/evidence-backed builder fixture:
  the only unmet criterion is value E=1, and the verb calls neither the
  signing/effect path nor append. Removing the refusal guard is detected.

No named mutant survived; there is no surviving-mutant defect to report.
