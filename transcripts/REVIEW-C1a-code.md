# REVIEW-C1a-code — the cold read of the C1a code (reviewer, `reviewer-1`)

Reviewer: `anthropic/claude-opus-5-5` (Claude Code), session of 25 October 2026, key `~/.ssh/jack-reviewer`
(principal `reviewer`). Branch `c1a-review`, cut from `c1a-ledger` at `7ae10a3` (the builder's commits, counsel's
rulings, the cap ruling and kernel2's commits, merged by Guy). Read: `SPEC.md` (C1a text), `BRIEF-C1.md` (C1a),
`RUNBOOK.md` (the verbs), `transcripts/BUILD-C1a.md`, `kernel2/NOTES.md`, `kernel2/QUESTIONS.md` ("none"),
`pins/`, `spec/vectors/verdicts.json`; then the code: `kernel/check.py`, `kernel/log.py`, `tools/entry.py`,
`tools/jack`, `harness/diff.py`, `sim/gen.py` (kinds only), `judge/judge.py` (`commits_of`, `changed_by`),
`kernel2/checker.go` (the C1a lines only), `tests/test_score.py`, `tests/test_pins.py`, `tests/test_vectors.py`.

A finding of mine is a pin, a vector or a replay disagreement; every `no` below that is not one is written down
for Guy to decide (A2.9). Nothing outside `pins/`, `spec/vectors/` and this file is touched.

## 1. What this branch adds

- **Vectors** `spec/vectors/logs/40`–`49` (eleven logs, with `46a`/`46b`) and their verdicts in
  `spec/vectors/verdicts.json` (additions only; no existing log or verdict changed). Each refused log is valid on
  every proper prefix and refused at exactly one entry, its required `(seq, reason)`; both checkers were run on
  every log and every prefix and agree with the required verdict:

  | log | required | what it holds |
  |---|---|---|
  | `40_forecast_valid` | ok, 4 | `p` 1 with `resolves_by` = `ts`; `p` 999 with `type`, `args` (a key with `.`); guy's forecast with a non-string `type` and an extra member |
  | `41_resolution_valid` | ok, 5 | two forecasts, each resolved by another party, outcomes 0 and 1, one by the master key |
  | `42_resolution_self_bad` | 2, `self_judged` | ann forecasts under `ann-1`, resolves under `ann-2`: two keys of one principal |
  | `43_resolution_dangling_bad` | 2, `schema` | resolves seq 0, the genesis |
  | `44_resolution_double_bad` | 3, `schema` | bob resolves, then guy resolves again |
  | `45_forecast_past_bad` | 1, `schema` | `resolves_by` one second before `ts` |
  | `46a_forecast_permille_0_bad` | 1, `schema` | `p` 0 |
  | `46b_forecast_permille_1000_bad` | 1, `schema` | `p` 1000 |
  | `47_forecast_boolean_bad` | 1, `schema` | `p: true` |
  | `48_ts_decreased_bad` | 2, `ts_decreased` | an otherwise valid forecast one second earlier than its parent (not genesis) |
  | `49_self_resolution_bad_signature` | 2, `bad_signature` | ann's self-resolution under `ann-1`, its `evidence` edited after signing |

  `python3 -m pins.fixtures` regenerates them from fresh throwaway keys and asserts each against the verdict
  written in `pins/fixtures.py` (`ledger_cases`), which is the SPEC's, not the kernel's output; it rewrites only
  these logs, `spec/vectors/score.jsonl` and their verdicts.

- **The score witness**, `spec/vectors/score.jsonl`, rebuilt from the brief's text alone (§3).

- **Pins** (§4): nine, with fourteen mutants, all KILLED with a passing twin.

## 2. Findings that are not pins (Guy decides)

1. **`tests/test_pins.py:37` fails on this branch: `self.assertEqual(len(names), 37)` → `46 != 37`.** The
   builder's registry test counts the pins exactly, so the nine pins the brief requires turn `tests` red the
   moment they land. The reviewer may not touch `tests/` (`party_scope`) and the builder may not touch `pins/`, so
   the fix is the builder's: `37` → `46`, and the nine C1a names added to its `required` tuple. Until then
   criterion 1 ("in the `tests` run on `main`") cannot be met, and the judge's `tests` check fails on the merge of
   this branch. Every other test passes: `python3 -m unittest discover -s tests -t .` → `Ran 229 tests …
   FAILED (failures=1, skipped=1)`, the one failure this, the skip the pre-existing `s_plus_L` environment skip.
2. **The witness's home.** BRIEF-C1.md (Scoring, "The witness") says `tests/vectors/score.jsonl` is "a signed log
   the reviewer builds"; RUNBOOK (`jack score`) and criterion 5 name the same path. `judge/scope.json` gives the
   reviewer no `tests/`, so the text cannot be done as written: the builder built that file, and the reviewer's
   independent rebuild is `spec/vectors/score.jsonl` (Guy's instruction for this session). The two agree in
   meaning (§3), and `jack score` prints byte-identical output on both. Criterion 5 should name which file counts;
   the pin `score_not_proper` runs on the reviewer's.
3. **`jack score`'s pair table has no `forecasts` column**, where the brief says each group carries "forecasts
   (all)". Counsel's ruling of 25 October (BUILD-C1a §5.3) settles it in the code's favour, since the witness
   table has no such column; the brief's sentence is not yet corrected. Text, not code.
4. **`jack forecast` reads the clock twice.** `--by` is checked against `entry.now()` once
   (`tools/jack:221` → `tools/entry.py:97`), and the entry's `ts` is a second `entry.now()` (`tools/jack:53`). With
   `--by` equal to the clock to the second and the second ticking between the two, the kernel refuses the entry
   at assembly (`schema`: `resolves_by` earlier than `ts`) and nothing is appended. Fail-safe; only the message is
   the kernel's verdict instead of the verb's refusal. No pin: it needs a clock.
5. **Evidence "already in the tree"** is the file's presence in the working tree under `begin`'s clean-tree
   precondition (`tools/entry.py:110-113`, `tools/jack:32`), not its presence in `HEAD`. Untracked files make the
   tree unclean, so only a gitignored file would pass unseen; `.gitignore` ignores nothing a `<hex64>` name can be
   today. The builder's reading 8 (0.6) says the same.
6. **Text left behind by the patch** (BUILD-C1a §6, still true): SPEC §4's `ts` row ends "does not order
   timestamps at C0" (`SPEC.md:79`); §8 step 9's last sentence says `proposal`, `merge`, `spec_conflict` have "no
   effect on the state beyond the head hash", but every entry now records its `ts`; RUNBOOK `jack key`'s "Keys per
   party" lists no `forecast`/`resolution`, which the brief's step 5 grants. Counsel's texts; no code is wrong.
7. **The dangling mutant crashes rather than admits.** The one-edit mutant that drops the step-7 dangling test
   (`kernel/check.py:75`) is caught as a crash: step 8a indexes `state.forecasts[...]` (`kernel/check.py:82`) on
   the strength of step 7. The pin demands the exact `(seq, schema)`, so a crash or an admission both kill it; the
   coupling is correct while step 7 stands.

## 3. The witness, rebuilt

`spec/vectors/score.jsonl`: genesis (guy's master key; `builder-1`, `reviewer-1`, `counsel-1`), F1–F10 at seqs
1–10, then six resolutions at 11–16, built by `pins/fixtures.py` `witness()` from the brief's sentence, without
reading `tests/test_score.py`'s builder first. Compared entry by entry with `tests/vectors/score.jsonl`:

| what | brief fixes it | builder | reviewer | same meaning |
|---|---|---|---|---|
| forecasts' (proposer, `type`, `p`), seq order | yes | the brief's ten | the brief's ten | **yes, all ten** |
| resolutions' (`forecast` seq, `outcome`), seq order | yes | 2→1, 1→1, 4→0, 3→0, 6→1, 5→0 | the same | **yes, all six** |
| each resolver a party other than the forecaster | yes | yes | yes | **yes** |
| which party resolves | no | reviewer, builder, counsel, reviewer, builder, counsel | counsel, reviewer, guy, builder, reviewer, guy | free choice |
| claims, `ts`, `resolves_by`, `evidence` text | no | `F1`…, `2026-10-26T00:0N:00Z`, `2026-11-08`, `run N` | longer claims, `08:0N`, `2026-11-09`, `FN resolved O` | free choice |
| genesis powers of the three parties | no | `forecast, resolution` | `proposal, forecast, resolution` | free choice |

No entry differs in meaning. Both logs are valid on every prefix under both checkers (17 entries). `jack score`
prints the same bytes on both, and its first table equals the brief's. My own arithmetic (floats, `%.4f`,
independent of `tools/entry.py`) gives the brief's five rows exactly, so the brief's table is right as printed.
The only behaviour the free choices touch is `--as-of` (the builder's overdue test pins `2026-11-08`).

## 4. Pins

| pin | mutant (one text edit) | killed by |
|---|---|---|
| `clock_runs_backward` | `ts_unchecked`: step 2a removed (`kernel/check.py:59`) | `48` admitted; twin: equal `ts` admitted; a decreasing `ts` with a bad `seq` is `ts_decreased` (step 2a before step 3) |
| `self_resolution_admitted` | `self_unchecked`: step 8a removed (`kernel/check.py:82`) | `42` (second key) and a same-key self-resolution admitted; twin: bob resolves |
| `dangling_resolution_admitted` | `target_unchecked`: "not a recorded forecast" dropped (`kernel/check.py:75`) | `43` (genesis), the resolution's own seq, a later seq, 2^53−1, a resolution's seq; twin: an open forecast |
| `double_resolution_admitted` | `resolved_unchecked`: "already resolved" dropped (`kernel/check.py:75`) | `44` admitted; a self-resolution of a resolved forecast becomes `self_judged`, not `schema`; twin: a second open forecast resolved |
| `past_forecast_admitted` | `resolves_by_unchecked` (`kernel/check.py:73`) | `45` and 400 days back admitted; twin: `resolves_by` = `ts` |
| `permille_out_of_range_admitted` | `p_0_admitted`, `p_1000_admitted` (`kernel/log.py:162`) | `46a`, `46b`; twins `p` 1 and 999 |
| `boolean_integer_admitted` | `p_boolean_admitted`, `outcome_boolean_admitted` (`kernel/log.py:162-163`), `booleans_are_integers` (`kernel/log.py:87`) | `47`, `p: false`, `outcome: true/false`, `forecast: true` (which is seq 1 if booleans were integers); twins `p` 1, `outcome` 0 and 1 |
| `self_judged_uncoded` | `self_judged_as_schema` (`kernel/check.py:83`); `judged_before_signature`: step 8a moved above the signature | `42` coded `schema`; `49` coded `self_judged` instead of `bad_signature`; twin: bob resolves |
| `score_not_proper` | `linear_score`: loss `1 − |o − p|`; `minimised_at_999`: loss `(1000 − p)/1000`, least at p = 999 whatever o (`tools/entry.py:143`) | `jack score` on `spec/vectors/score.jsonl`, in a copy of the tools, must print the brief's table first, exactly |

The logs are `pins/fixtures.py` `ledger_cases` (thirty, built once per run); each kernel pin demands an exact
`(seq, reason)` or exact acceptance, so a mutant cannot survive by failing for another reason. The thirty also give
their required verdict on `kernel2/check` (run once by hand, not part of the pins).

Counted lines (SPEC §10.10, the judge's arithmetic over `sim/ harness/ tests/ pins/ tools/`): **5813** of 6200.
`tools/count_kernel.py`: 450.

`python3 pins/run.py`:

```
pin                              mutant                       status
------------------------------------------------------------------------
charter_edit_unrecorded          charter_unchecked            KILLED  (AssertionError: {'appended': 0, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '6a0ff292f2022c220b)
amend_stale                      genesis_charter_compared     KILLED  (AssertionError: {'appended': 0, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': 'f3f3ff5aa70ab68a7c)
push_unrecorded                  trusted_base_unchecked       KILLED  (AssertionError: {'appended': 0, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '892e255a5f4c671369)
freeze_ignored                   amendment_freeze_unchecked   KILLED  (AssertionError: {'appended': 4, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '3fd008ae0165a97976)
one_act_amendment                transmutation_unchecked      KILLED  (AssertionError: {'appended': 2, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': 'cc6f34c5fdf37bda05)
decision_forged                  sovereign_unchecked          KILLED  (AssertionError: {'appended': 3, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '403c8b2b80f4c87aad)
trusted_path_unguarded           guard_removed                KILLED  (AssertionError: ('kernel/check.py', {'appended': 0, 'detail': 'no appended proposal entry names a commit of th)
trusted_path_unguarded           judge_dir_untrusted          KILLED  (AssertionError: ('judge/judge.py', {'appended': 0, 'detail': 'no appended proposal entry names a commit of the)
trusted_rename_admitted          path_guard_only              KILLED  (AssertionError: ('SPEC.md', 'docs/SPEC.md', {'appended': 0, 'detail': 'no appended proposal entry names a comm)
judge_from_proposal              digest_unchecked             KILLED  (AssertionError: {'appended': 2, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '96b49043b396ff7e4a)
unattributed_proposal_admitted   commit_unchecked             KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '47dcd96449cd2b3cd7)
unattributed_proposal_admitted   later_commits_unchecked      KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '411ea13efd3aa6b234)
unattributed_proposal_admitted   law_at_end                   KILLED  (AssertionError: {'appended': 2, 'detail': "outside reviewer's paths: sim/x.py", 'kernel2': 'absent', 'ok': Fal)
unattributed_proposal_admitted   first_entry_attributes       KILLED  (AssertionError: {'appended': 2, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '7c94a15f22ce4e9087)
unattributed_proposal_admitted   party_by_key_id              KILLED  (AssertionError: {'appended': 2, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': 'a8710be156a57b85db)
counsel_build_admitted           counsel_unlisted             KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '8554050012362af4c3)
builder_pin_admitted             builder_unlisted             KILLED  (AssertionError: {'appended': 2, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '5161a669296b65393a)
reviewer_code_admitted           reviewer_unlisted            KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '3f4f5ac642f6bcd14a)
scope_unguarded                  scope_unchecked              KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': 'd5d3e3d3a30846dfe0)
scope_unguarded                  rename_hides_source          KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '60b9c95c829d6127a7)
cap_unguarded                    cap_unchecked                KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': 'c58bfb10ca48be46d6)
shebang_uncounted                py_suffix_only               KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '0384b0e7ae5bd87274)
foreign_object_admitted          mode_unchecked               KILLED  (AssertionError: {'appended': 1, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '080f3df8a246fb2649)
foreign_object_admitted          trusted_mode_unchecked       KILLED  (AssertionError: {'appended': 0, 'detail': '', 'kernel2': 'absent', 'ok': True, 'proposal': '83db2f09e10673cbdf)
unsigned_change                  power_unchecked              KILLED  (AssertionError: expected (1, 'no_power'), got {'entries': 2, 'ok': True})
history_rewritten                signature_always_valid       KILLED  (AssertionError: expected (1, 'bad_signature'), got {'detail': '', 'ok': False, 'reason': 'parent_mismatch', 's)
fork_admitted                    parent_unchecked             KILLED  (AssertionError: expected (3, 'parent_mismatch'), got {'entries': 4, 'ok': True})
unattributed_entry               empty_proposer_admitted      KILLED  (AssertionError: expected (1, 'no_proposer'), got {'detail': 'key ann-1 belongs to ann', 'ok': False, 'reason':)
unattributed_entry               unknown_key_trusted          KILLED  (AssertionError: expected (1, 'unknown_key'), got {'entries': 2, 'ok': True})
forged_signature_admitted        s_bound_unchecked            KILLED  (AssertionError: expected (1, 'bad_signature'), got {'entries': 2, 'ok': True})
weak_key_admitted                noncanonical_key_admitted    KILLED  (AssertionError: expected (1, 'bad_key'), got {'entries': 2, 'ok': True})
weak_key_admitted                small_order_key_admitted     KILLED  (AssertionError: expected (1, 'bad_key'), got {'entries': 2, 'ok': True})
reserved_bytes_admitted          reserved_unchecked           KILLED  (AssertionError: expected (1, 'bad_signature'), got {'entries': 2, 'ok': True})
ts_not_an_instant                unicode_digits_admitted      KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
ts_not_an_instant                calendar_unchecked           KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
deep_nesting_crashes             depth_unbounded              KILLED  (AssertionError: expected (0, 'malformed_json'), got {'detail': 'top-level keys', 'ok': False, 'reason': 'schem)
deep_nesting_crashes             recursion_uncaught           KILLED  (AssertionError: expected (0, 'malformed_json'), got {'ok': False, 'reason': 'crash', 'detail': 'le "/tmp/tmpi5)
big_integer_unreadable           int_digits_limited           KILLED  (AssertionError: expected (0, 'not_canonical'), got {'detail': '', 'ok': False, 'reason': 'malformed_json', 'se)
pubkey_reused                    ownership_forgotten          KILLED  (AssertionError: expected (2, 'bad_key'), got {'entries': 3, 'ok': True})
key_decl_extra_member            extra_members_allowed        KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
last_key_revocable               last_key_unguarded           KILLED  (AssertionError: expected (1, 'bad_key'), got {'entries': 2, 'ok': True})
kernel2_unrunnable               modes_ignored                KILLED  (AssertionError: {'ok': False, 'reason': 'crash', 'detail': 'judge error: /tmp/tmpr10nciya/kernel2/check failed)
selfcheck_blind                  judge_errors_ignored         KILLED  (AssertionError: self-check passed a trunk whose kernel2 cannot run)
checker_drift                    reason_code_flipped          KILLED  (AssertionError: [('/tmp/tmpuj7cthi8/tree/spec/vectors/logs/12_bad_signature_tampered.jsonl', 2, {'ok': False, )
whole_log_only                   prefixes_uncompared          KILLED  (AssertionError)
loose_parse                      ok_not_boolean               KILLED  (AssertionError: n=$(($(wc -l < "$1"))); [ $n -eq -1 ] && n=9; echo "{\"ok\":1,\"entries\":$n}")
loose_parse                      exit_status_ignored          KILLED  (AssertionError: n=$(($(wc -l < "$1"))); [ $n -eq -1 ] && n=9; echo "{\"ok\":true,\"entries\":$n}"; exit 1)
crash_as_agreement               like_failures_agree          KILLED  (AssertionError: exit 3)
prefix_skipped                   empty_prefix_skipped         KILLED  (AssertionError: 0)
prefix_skipped                   prefix_off_by_one            KILLED  (AssertionError: 0)
clock_runs_backward              ts_unchecked                 KILLED  (AssertionError: expected (2, 'ts_decreased'), got {'entries': 3, 'ok': True})
self_resolution_admitted         self_unchecked               KILLED  (AssertionError: expected (2, 'self_judged'), got {'entries': 3, 'ok': True})
dangling_resolution_admitted     target_unchecked             KILLED  (AssertionError: expected (2, 'schema'), got {'ok': False, 'reason': 'crash', 'detail': 'Traceback (most recent)
double_resolution_admitted       resolved_unchecked           KILLED  (AssertionError: expected (3, 'schema'), got {'entries': 4, 'ok': True})
past_forecast_admitted           resolves_by_unchecked        KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
permille_out_of_range_admitted   p_0_admitted                 KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
permille_out_of_range_admitted   p_1000_admitted              KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
boolean_integer_admitted         p_boolean_admitted           KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
boolean_integer_admitted         outcome_boolean_admitted     KILLED  (AssertionError: expected (2, 'schema'), got {'entries': 3, 'ok': True})
boolean_integer_admitted         booleans_are_integers        KILLED  (AssertionError: expected (1, 'schema'), got {'entries': 2, 'ok': True})
self_judged_uncoded              self_judged_as_schema        KILLED  (AssertionError: expected (2, 'self_judged'), got {'detail': 'ann made forecast 1', 'ok': False, 'reason': 'sch)
self_judged_uncoded              judged_before_signature      KILLED  (AssertionError: expected (2, 'bad_signature'), got {'detail': 'ann made forecast 1', 'ok': False, 'reason': 's)
score_not_proper                 linear_score                 KILLED  (| world.screen | 4 | 2 | 0.4500 | 0.5000 | 0.6500 | 0.8959 |)
score_not_proper                 minimised_at_999             KILLED  (| world.screen | 4 | 2 | 0.4500 | 0.5000 | 0.5500 | 0.8959 |)

KILLED 64, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0
```

## 5. Cold read: does the code do what the text says

### BRIEF-C1.md, C1a scope

| sentence | yes/no | where |
|---|---|---|
| `forecast`: `claim` a non-empty string | yes | `kernel/log.py:162` (`NONEMPTY`, `:24`); kernel2 `checker.go:164` |
| `p` an integer 1–999, per mille; booleans are not integers | yes | `kernel/log.py:162`, `_is_int` `:86-87`; `checker.go:163-164` |
| `resolves_by` an instant in §4's form, not earlier than the entry's `ts` | yes | form `kernel/log.py:162` (`instant`); order `kernel/check.py:73-74`, step 7, before the signature; `checker.go:293` |
| `type` and `args` optional, read by the tools, never by the kernel | yes | absent from `kernel/`; read at `tools/entry.py:138` (`type`, non-string → `free`) |
| `resolution`: `forecast` an integer, the seq of an earlier valid forecast not already resolved | yes | shape `kernel/log.py:163` (`int` = integer ≥ 0, no booleans, `:96-97`); state `kernel/check.py:75-76`; `checker.go:298` |
| `outcome` 0 or 1, booleans not integers; `evidence` non-empty | yes | `kernel/log.py:163`; `checker.go:166-167` |
| `ts` earlier than the parent's is `ts_decreased`, at step 2a, after shape and before `seq` | yes | `kernel/check.py:58-62`; genesis exempt by `state.ts is None` (`EMPTY`, `:23`); kernel2 by line index, `checker.go:266` |
| dangling or double resolution is `schema`, step 7, before the signature | yes | `kernel/check.py:75` before `signer` at `:81` |
| self-resolution is `self_judged` at 8a, after the signature, by principal | yes | `kernel/check.py:81-83`; `proposer` equals the signing key's principal after `signer` (`:35`), so `ann-2` cannot launder `ann-1`'s forecast (vector `42`) |
| a self-resolution with a bad signature is `bad_signature`; of a resolved forecast, `schema` | yes | order `:75` → `:81` → `:82`; vector `49`, pin case `self_of_resolved` |
| fourteen reason codes; §9 and §9a together | yes | `kernel/log.py:12-13`; `harness/diff.py:5-6`; equality asserted by `tests/test_vectors.py` |
| state gains forecast proposers by seq, resolved seqs, previous `ts`; nothing else | yes | `kernel/check.py:16`, effects `:89-90`, `:100` |
| score inputs: the log and `--as-of`, no other | yes | `tools/jack:223`; `tools/entry.py:132-136` |
| loss `−[o·ln(p/1000) + (1−o)·ln(1−p/1000)]`, natural log, no clipping | yes | `tools/entry.py:143` |
| groups: every (`proposer`, `type`) with ≥ 1 resolved; no `type` → `free` | yes | `tools/entry.py:138`, `:149` |
| for each: forecasts (all), resolved, mean p, rate, mean loss, base-rate loss | **no, as ruled** | the pair table has no `forecasts` column (`tools/entry.py:146-147`); counsel's ruling; §2.3 |
| base rate: prequential Laplace `(s+1)/(n+2)` by type, pooled across proposers, in resolution-seq order | yes | `tools/entry.py:140-144`; ½ before any resolution |
| per `proposer` and per `type` alone | yes | `tools/entry.py:146` |
| with `--as-of`, unresolved forecasts with `resolves_by` before it, by `resolves_by` then seq | yes | `tools/entry.py:154-157` (strictly before) |
| four decimals, half to even | yes | `tools/entry.py:126-129`, exact value of the float or Fraction |
| the witness: `tests/vectors/score.jsonl`, built by the reviewer, prints the table exactly | **no, as to who** | built by the builder; the reviewer cannot write `tests/`; §2.2. The table: yes, on both witnesses |
| `jack merge`: the head is a valid proposal's `commit` followed only by `log.jsonl` commits | yes | `tools/jack:150-154`, the judge's `commits_of` (newest first, `judge/judge.py:85-87`) and `changed_by`; the trailer alternative kept |
| `jack proposal`'s `commit`: the last commit changing a path other than `log.jsonl` | yes | `tools/jack:122`; HEAD on a forecast-only branch |
| a forecast on a branch is a log-only commit, made before `jack proposal` | yes | `tools/jack:218-221` commits `log.jsonl` only and pushes nothing |
| evidence: `transcripts/evidence/<hex64>`, its SHA-256 the name, checked | yes | `tools/entry.py:110-113`; "in the tree" read as the working tree, §2.5 |
| the master key's verbs are main verbs | yes | `tools/jack:44`, `:219` |
| `jack key` admits any power in `TYPES` | yes | `tools/jack:112-113` |
| simulator kinds: the ten | yes | `sim/gen.py:20-21`; their refusals and twins are BUILD-C1a §4's table (not re-run here) |
| no clock read in either checker; no scoring in the kernel | yes | `kernel/` has no `datetime.now`/`time`; kernel2 NOTES; scoring only in `tools/entry.py` |

### RUNBOOK verbs

| verb | yes/no | where |
|---|---|---|
| `jack key` | yes | `tools/jack:106-117` |
| `jack proposal` | yes | `tools/jack:119-125` |
| `jack spec_conflict` | yes | `tools/jack:127-130` |
| `jack merge` | yes | `tools/jack:145-161` |
| `jack push` | yes, but `--remove` is cut | `tools/jack:175-197`; RUNBOOK says "`--remove` removes BRANCH's worktree afterwards", but RUNBOOK's cut order (`RUNBOOK.md:199`) allows the cut, and the verb prints the command |
| `jack decision` | yes | `tools/jack:199-202` |
| `jack amend` | yes | `tools/jack:204-216` |
| `jack forecast` | yes | `tools/jack:221`, `tools/entry.py:90-101`: refuses N outside 1–999, TS not an instant or before the clock, an empty claim (and `--args` not an object: builder's reading 10); clock read twice, §2.4 |
| `jack resolve` | yes | `tools/jack:222`, `tools/entry.py:104-114`: `schema` and `self_judged` before signing, with the kernel's reasons |
| `jack score` | yes | `tools/jack:223`: no entry, signing, fetch or clean tree; working copy's `log.jsonl`; a refused log or bad `--as-of` is exit 1 with nothing on stdout |

## 6. Agreement, and the run of record

- Every vector in `spec/vectors/logs/` (51) and both witnesses: both checkers give the recorded verdict;
  `kernel2/test.sh -run 'TestLogVectors|TestScoreVectorLog'` passes with the new logs counted.
- The thirty ledger cases: identical verdicts on both checkers.
- kernel2's C1a lines read against the kernel's: the same step order (2a by line index, 7 before 8, 8a after),
  the same bounds, booleans excluded the same way, the same string order for `ts` and `resolves_by`.
- A sample differential, `harness/diff.py --seeds A:B --b kernel2/check` over seeds 0–5999 in six parts:
  6,000 logs, 38,584 prefixes compared, **0 disagreements**, nothing uncompared, every part exit 0 (working
  tree at `7ae10a3` plus this branch's uncommitted pins and vectors; no checker file changed).

**My probability that the run of record (10⁵ seeds, both checkers) is clean: 0.95.** The basis: no
disagreement in any vector, case or sampled seed; kernel2's C1a code is short and line-for-line the SPEC's order;
the C0 runs of record were clean twice. The residue is the simulator's reach (10⁵ seeds draw the ledger kinds
about 10⁴ times each, so a disagreement that only a rare combination reaches would show there, not here) and
the run's own mechanics (a per-call timeout across twelve parallel parts).
