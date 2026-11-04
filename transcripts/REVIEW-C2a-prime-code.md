VERDICT: ACCEPT WITH OBLIGATIONS
Reviewed tree: 5ba12b1704bf3128ffe9167e1910f5df4584d300
Reader: reviewer reviewer-2; model openai/gpt-6-astra; 2026-11-05 (HKT)

F1: The named `process_unchanged_from_opening/tuple_from_assessed_tree` mutant survives the stipulated twins. The implementation derives roots separately in each tree, but also compares the `WINDOW_FIX_FUNCTIONS` assignment itself; dropping a name and editing its function still returns `unchanged False`, even with the mutant. With equal tuples, changing the tuple's source cannot distinguish the two guards. This is an unresolved pin-contract obligation, not a witnessed false acceptance by the code. Criterion 1's requirement, "Every pin of BRIEF-C2a's list and of §Pins below is KILLED, with a passing twin", is not satisfied by this run. Resolve the redundant named mutant with the brief's authority before the opening; the reviewer has kept it registered and reported SURVIVED, rather than removing the independent tuple check, weakening the twins, or counting a source-text assertion as a behavioral kill. — severity: OBLIGATION — witness: `tools/status.py:374-399`; `pins/pins.py:1115-1121`; `pins/c2aprime.py:66-81`; `python3 pins/run.py --only process_unchanged_from_opening` prints `KILLED 4, SURVIVED 1, STALE 0, TWIN FAILED 0, PENDING 0`.

F2: The opening's commit-attribution audit remains outstanding: inherited commits `566eae8` and `3c58d18` have no `Proposer:` trailer, and cap commit `b3ba60e` has `Proposer: builder builder-2` while touching trusted `SPEC.md` and `judge/scope.json`, outside the builder's listed paths. The brief requires the prebuilt commits to have their trailers and the opening note to record "each commit's `Proposer:` party against SPEC §10.8's scopes". The opening's responsible parties must address and record these facts; this code acceptance does not certify that audit or authorize a history rewrite. — severity: OBLIGATION — witness: `git show -s --format='%h%n%B' 566eae8 3c58d18 b3ba60e` prints only subjects for the first two and the builder trailer for the third; `git show --stat b3ba60e`; `judge/scope.json:4-7`.

## Scope and disposition

Read BRIEF-C2a-prime **v7**, including §The code, §No item changes and §Pins,
and the ruling with corrections 1–7, from counsel ref
`40adaaeb2e4514eb6c54e2d83f3280b291de09b3`. The worktree's older brief is not
the authority for this read. Reviewed the builder changes through `b3ba60e`
and the reviewer registrations at the reviewed tree above.

The code read accepts with the obligations above. **The opening is not ready:
the required all-KILLED pin result has not been obtained.** F1 is not a claim
that a changed process was accepted: the stipulated changed-tree twins all
refuse on the unmodified code, including the tuple-drop-plus-function-edit
twin. No behavioral BLOCK against the three specified code changes or
correction 6 was found. The literal tuple-source instruction and its named
mutant need resolution without fabricating a failure in otherwise protective
code. This report leaves that decision to the brief's authority.

## Code read

- **Change 1:** `second_opening` uses V0's late end and excludes a promotion
  at or before it. The three-push fixture selects the third push, not the
  first window's push or the push between the two readings. `prime_window`
  requires counsel's V5 below the opening and returns its own `resolves_by`;
  the missing/late-V5 refusal remains explicit. `status`, `decision_window`
  and `render` preserve first-window assessment before the second opening
  and apply the specified veto naming afterward (`tools/status.py:49-81`,
  `255-293`, `513-530`, `609-612`).
- **Criteria 3 and 7:** criterion 3 uses 8,400 and checks scope/SPEC against
  the opening and every intervening tree, so a changed cap and a later
  restoration both refuse. Criterion 7 uses the second opening and counts
  an intersecting minute, including the 00:00:31 repair after a 00:00:30
  opening. The nine first-window rows cease to count in the second window
  (`tools/status.py:340-349`, `360-373`, `408-433`).
- **Change 2:** the four conditions are computed outside `item_process`.
  Promotion exclusion and fix timing use the late end; veto and whole-minute
  attributed-row evidence use the early end. Evidence comes from the fix's
  carrying commit, with the raw twin and the specified classifier's hash;
  a raw-only name does not name its attributed twin. Missing history fails
  closed with the `unverified` diagnostic. An earlier fix consumes the name,
  and a fix after the next push is not qualified (`tools/status.py:84-170`).
- **No item changes / correction 6:** every fix initially taints open writs.
  The push removes only qualified fixes from writs still open; completed
  items are not edited. The intervening timely herald batch retains repairs
  `(369,)`, Y=0, stake 22/45 and wealth 11/15, exactly as the no-set process;
  the later batch is free of that fix. The first finalized item is identical
  in both runs. A qualifying fix adds no late report, and the free-text and
  other nonqualifying twins retain both taint and a late report
  (`tools/status.py:185-237`; `tests/test_c2a_prime.py:71-94`).
- **Change 3:** the comparison starts at the opening push's carrying tree.
  It protects the existing process, clerk bytes, change-2 functions,
  transitive named functions, whole callers and read top-level assignments.
  The reviewer adds a two-hop helper-to-leaf dependency to distinguish
  transitive traversal from merely collecting immediate references.
  The remaining tuple-source qualification is F1 (`tools/status.py:374-405`).
- **Continuity:** `tools/value.py`, `tools/clerk.py`, `score_items`,
  `sovereign_keys` and P0 are unchanged by the builder diff. The real-prefix
  inertness test passes, as does the existing `wealth_continues` pin. The
  exemption is confined to the stated boundary-fix treatment; no new score,
  threshold or retrospective item recalculation was found.

## Pin registration and killing reasons

All eight new names are registered. `VALUE_PINS` is exactly the eighteen
BRIEF-C2a names plus these eight; every name has a registration. The registry
has 99 pins in total. Each new mutant is a single-occurrence anchored edit
of `tools/status.py`, and every new pin's unedited twin passes.

The fixtures reuse the builder's committed synthetic-history helpers and
add reviewer witnesses under `pins/`. The boundary cases use genuinely
intermediate timestamps between the two stated ends, chronological
post-fix completions and timely **herald** batches. Their temporary git
repositories hold the attributed file, raw twin and classifier hash before
the carrying commit except in the explicit late-file twin.

| Pin | Mutants and observed reason | Result |
|---|---|---|
| `second_window_from_the_end` | `first_push_after_337` returns 367 instead of 369; `early_end_opens` returns the intermediate push 368 | 2 KILLED |
| `second_window_end_is_v5` | `v0_ends_second` returns 17 November instead of 30 November; `v5_after_opening` does not raise the required refusal | 2 KILLED |
| `second_window_cap` | `hardcoded_7800` rejects the 8,400 twin; `head_cap_only` accepts the changed-cap tree | 2 KILLED |
| `offlog_from_second_opening` | `first_window_acts` counts nine instead of zero; `minute_start_only` counts zero instead of the overlapping repair | 2 KILLED |
| `promote_refused_before_end` | `v5_alone_opens` selects C2a-prime before its push; `prime_veto_ignored` loses the post-opening veto | 2 KILLED |
| `window_fix_is_decision` | `fix_is_repair` loses qualified fixes; `nonpromotion_is_failure` admits absent/invalid failure evidence; `promotion_read_early`, `veto_read_late`, `acts_read_late`, `fix_read_early` each misclassify the corresponding two-end twin | 6 KILLED |
| `window_fix_is_decision` continued | `contains_window_name` admits free text; `next_push_unbounded` admits the after-push fix; `second_fix_allowed` admits the second fix; `head_carries_fix` uses late/replacement evidence or bypasses unavailable history; `attribution_dropped` admits missing raw/classifier or wrong hash; `substring_file_name` admits the raw-only name when the attributed twin also has a row; `push_clears_all_fixes` erases nonqualifying repairs | 7 KILLED |
| `window_fix_not_retroactive` | `rule_from_fix` changes the intervening item's Y and wealth; `rule_never_applied` leaves the third item's Y at zero | 2 KILLED |
| `process_unchanged_from_opening` | `fix_functions_omitted`, `references_not_followed`, `callers_omitted`, `assignments_omitted` accept their changed protected trees; `tuple_from_assessed_tree` still refuses all stipulated changed trees | 4 KILLED; 1 SURVIVED (F1) |

The 29 kills were checked for assertion failures on the named outcomes,
not syntax/import failures. The transitive-reference mutant is limited to
one-hop coverage; its kill is the later leaf-function edit. No extra mutant
that disables the tuple-assignment comparison was substituted for the
surviving tuple-source mutant.

## Verification and size

All temporary test storage was directed inside this worktree with
`TMPDIR="$PWD/transcripts/evidence/.review-tmp"`.

`python3 -m pytest -q`:

```text
337 passed, 1 skipped, 49 subtests passed in 123.91s (0:02:03)
```

`python3 pins/run.py` (also repeated with `--transcript
transcripts/evidence/pins-c2a-prime-review.txt` at the reviewed tree):

```text
KILLED 144, SURVIVED 1, STALE 0, TWIN FAILED 0, PENDING 0
```

The pin runner exits **1**, correctly, because of F1. Of the new mutants,
29 are KILLED and one SURVIVED; all eight new twins pass. The complete pin
table is retained at `transcripts/evidence/pins-c2a-prime-review.txt`.

`judge.judge.counted_lines('.', <reviewed tree>,
['sim/', 'harness/', 'tests/', 'pins/', 'tools/'])` is **8,359**, leaving
**41** of 8,400. The builder baseline was 8,201; the pins add 158 physical
Python lines. Kernel count is **450/500**. No builder test or production
code was trimmed. This review and its text evidence add no counted lines.
