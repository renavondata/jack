VERDICT: BLOCK
Reviewed tree: ec74d1464dae37d8f79cda1f5d4cea6d3a60cc4a (origin/builder-elect)

# Election pins — reviewer, before C2b's opening

Reviewer: `reviewer-2`, party `reviewer`, model `openai/gpt-6-astra`, branch
`review-elect-pins`. This is a pushed pre-build review, not a proposal or a
promotion assessment. No forecast, proposal entry or PR was entered.

## Base, scope and result

The supplied worktree initially pointed at `c48435e` / `origin/main`, rather than
the requested builder branch. It was clean; after fetching `builder-elect`,
`git reset --keep origin/builder-elect` aligned this branch with the requested
base. All subsequent work was inside this worktree. The branch-local brief is
v6 without Amendment 1; its election scope and pins match the requested contract.
The current live cap remains 7,800; the handoff anticipates 9,800 at the opening.

Compared against `origin/builder-w5` at
`3dea34b52bf44d468358bb539e936a48d74bfe91`. Election actually descends from the
earlier W5 head `c347114779d6e2088870d38a2955fa1db59dd3c6`. Thus the W5 regressions
below are an omitted upstream fix, not evidence of an intentional rollback in
the election commit.

All 19 requested election pins are registered once, with 21 mutant patches and
passing unedited twins. The registry contains 110 pins; `EXPECTED` is 110.
Changes here are confined to `pins/pins.py` and this transcript. The defects and
missing witnesses below remain builder work.

## Commands and results

Temporary files for the runners and their subprocesses were directed by
`TMPDIR=$PWD/transcripts/.review-elect-tmp`, inside the worktree, not `/tmp`.
The test runs used `JACK_KEY=$HOME/.ssh/jack-reviewer`; fixtures use throwaway
keys, not the reviewer's key to enter anything on the record.

`python3 pins/run.py` exited 0:

```text
KILLED 136, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0
```

After that full run, the draw mutant was strengthened from accepting the
recorded gain field to recomputing the entire draw using recorded gains.
`python3 pins/run.py --only draw_replays_from_prefix` on that final mutation
exited 0, with `KILLED 1, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`.
No production source or test changed between these runs. F7 explains the
important limitation of that kill, and the separate SURVIVED coverage probe.

`python3 -m pytest -q tests/test_elect.py` exited 0:

```text
.......................                                                  [100%]
23 passed in 19.69s
```

`git diff --check` passed. Registry checks confirmed exact equality between the
19 names in `tools.elect.PINS` and `C2B_ELECTION_PINS`, and 110 total registrations.

Counted total for the final Python tree: **9,089**. The report adds no counted
lines. The required post-commit command is:

```sh
python3 -c 'from judge.judge import counted_lines; print(counted_lines(".", "HEAD", ["sim/", "harness/", "tests/", "pins/", "tools/"]))'
```

This pre-build is 1,289 above the still-live 7,800 cap, 89 above the branch-local
v6 brief's 9,000, and 711 below the handoff's anticipated 9,800. It cannot be
proposed under C2a's cap.

## Election pins table

Except for the continuation wrapper, each witness is
`tests.test_elect.Election.test_<pin name>`. A passing twin means that same
witness passes in the runner's unedited disposable copy. Multiple listed
mutants each have the displayed result.

| Pin | Mutant(s) | Status | Twin |
|---|---|---|---|
| `gain_in_unit_interval` | `divide_by_ln1000` | KILLED | PASS |
| `round_loss_is_mean` | `six_losses_summed` | KILLED | PASS |
| `bad_round_kept` | `incomplete_round_dropped`; `missing_event_out_of_mean` | KILLED ×2 | PASS |
| `exp3_importance` | `todays_propensity` | KILLED | PASS |
| `exp3_constants` | `gamma_point_one` | KILLED | PASS |
| `instance_feedback_complete` | `draw_on_stale_feedback` | KILLED | PASS |
| `draw_replays_from_prefix` | `from_args_gains` | KILLED; diagnostic-only distinction, F7 | PASS |
| `sigma_verifies` | `sigma_unchecked` | KILLED | PASS |
| `draw_on_the_grid` | `float_u_unassigned` | KILLED | PASS |
| `roster_fixed` | `outside_roster_admitted` | KILLED | PASS |
| `invite_before_session` | `later_invite_accepted` | KILLED; forecast timestamps only, F1 | PASS |
| `invite_cutoff_W0` | `late_invite_scored` | KILLED | PASS |
| `invite_p_is_success_rate` | `p_is_propensity` | KILLED | PASS |
| `invite_resolution_strict` | `tie_is_success` | KILLED | PASS |
| `resolver_not_forecaster` | `same_principal_resolves` | KILLED; routing/events only, F2 | PASS |
| `self_invite` | `non_clerk_invite_admitted` | KILLED | PASS |
| `rigged_election` | `recorded_gains_trusted`; `sigma_unchecked` | KILLED ×2 | PASS |
| `mixture_untouched_and_continued` | `uniform_restart` | KILLED | PASS |
| `procedure_types_out` | `counsel_programme_scored` | KILLED | PASS |

`t_election_continued` restores the existing immutable JSON fixture that
`pins/run.py` excludes with `transcripts/`, runs `tests.test_value.Value.test_worked_table`,
then the builder's continuation test. It creates no new test or fixture.
The gain mutant omitting the sixth event keeps the six-input gain validation;
the cutoff mutant admits the late invite rather than merely falling through to
the redundant cutoff guard in `ready`. Today's propensity is computed from all
settled feedback, not from the initial zero-gain vector.

Missing builder witnesses are named beside the corresponding registrations,
and precisely below. They are not registered as nonexistent unittest methods:
doing so would fabricate a TWIN FAILED instead of providing a passing twin.

## Ownership of every builder pin diff line

The requested diff has 15 additions and one deletion: 16 changed lines, including
the blank separator. Line numbers here are those in the builder head (or the
old W5 version for the deleted line). Every line has been reviewed and adopted
or rewritten by this reviewer.

| # | Builder diff line | Decision |
|---|---|---|
| 1 | `-EXPECTED = 91` at old 664 | Keep its removal: the 91-pin baseline excludes the election. |
| 2 | `+EXPECTED = 93` at 664 | Rewrite to `110`: 91 baseline + all 19 election pins. |
| 3 | blank at 1062 | Keep as the section separator. |
| 4 | simulator-registration comment at 1063 | Rewrite: this section now owns all election pins. |
| 5 | `elect_attacks = functools.partial(...)` at 1064 | Keep: runs the disposable tree's builder witnesses. |
| 6 | `PINS += [` at 1065 | Rewrite to `C2B_ELECTION_PINS = [`; append that collection once after its closing bracket. |
| 7 | `Pin("self_invite", ...)` at 1066 | Keep: signed non-herald attack and honest twin. |
| 8 | `Mutant("non_clerk_invite_admitted", ...)` at 1067 | Keep: correct target, `tools/elect.py`. |
| 9 | public-key guard patch at 1068 | Keep: one occurrence, removes the herald-key restriction, KILLED. |
| 10 | `Pin("rigged_election", ...)` at 1069 | Keep: all three simulator variants and honest twins are exercised. |
| 11 | `Mutant("recorded_gains_trusted", ...)` at 1070 | Keep: valid gain-field trust mutant for this attack pin. |
| 12 | field-loop find string at 1071 | Keep: unique, matches the replay comparison. |
| 13 | recorded-gains replacement at 1072 | Keep: bypasses gain comparison; KILLED. It is narrower than the separate full draw-from-recorded-gains mutant. |
| 14 | `Mutant("sigma_unchecked", ...)` at 1073 | Keep: correct signature-verification mutant. |
| 15 | signature-check replacement at 1074 | Keep: unique, valid patch, KILLED. |
| 16 | closing `]` at 1075 | Keep as the collection terminator, moved below the added continuation/procedure registrations. |

## Required cross-checks

**Criterion 7 is looser than the stated witness.** Replay, settlement, matching
success and the resolution deadline are checked. Session-start ordering is not
established; the routed invite resolver is not required; the count is not
filtered to invites after attack green. See F1–F2. A 342-entry kernel-valid
signed fixture with 24 wrongly routed invite resolutions produced:

```text
wrong-resolver signed log: {'ok': True, 'entries': 342}
(True, 'criterion 7: elections witnessed 24/24; refused invites 0')
value attached: False continued liveness attached: False
```

This probe used the builder's 24-round construction from
`tests/test_elect.py:341–365`, but signed each invite resolution with the invited
principal's key. Its six event resolutions still used the correct opposite key.
Only tree/cap/CI evidence was stubbed, as in that test; signature replay, kernel
checking, gains, deadlines, outcomes and the counting predicate were real.

**C2a fixture: byte-identical.** The diff of both `tests/test_value.py` and
`transcripts/evidence/value-fixture-20261101.json` against `origin/builder-w5`
is empty. Their Git blobs are respectively
`537fe9190949e0b82886e65bc53812d17c719547` and
`104e25779a5c952fbd98cba77f2552a07f0e8cef` in both trees. The JSON SHA-256 is the
test's literal `0b3fd0937bd727ac3f4c7fb5d78bc6ef37657436f098c7c3e31d3a69634e736f`.

**Continuation: the value engine carries history.** The only `tools/value.py`
diff is procedure-type exclusion. Comparing the worked ledger with and without
`window_opening="2026-11-01T03:00:00Z"` gives identical rows, terminal weights,
wealth, own likelihood ratios and mixture likelihood ratio. That worked
ledger's wealth is 1.0, so its equality alone cannot witness a wealth reset.
The existing `pins/c2a.py:80–93` non-unit-wealth witness, exercised by the full
pin run, supplies the distinction: wealth before the second boundary is
`1.0001603772572065`; terminal original/continued wealth is
`1.0003524436502307` in both; the continuing lambda is
`0.018203233799388534`; all rows agree. C2b status integration is still absent
(F6), distinct from this correctly continuing value engine.

**Procedure types: excluded.** `event(forecast(1, type="counsel.programme"))`
returns `None`; the builder test also checks zero value events and a world-event
twin. Invites stay outside value, and herald is not added to its opening roster.

**Scope comparison.** All 16 paths in the requested builder-W5/election diff
are scope-named deliverables or their direct test support: `tools/elect.py`,
`tests/test_elect.py`, `sim/election.py`, `sim/gen.py`, `tools/value.py`,
`tools/status.py`, `tools/jack`, `pins/pins.py`; simulator dependency support in
`tests/test_jack.py` and historical-seed preservation in `tests/test_sim.py`;
the handoff and three session prompts; and the stale W5 files `tools/due.py` and
`tests/test_due.py`. The latter two contain the unwanted differences F4–F5.
No kernel, kernel2, harness, judge, SPEC, workflow, clerk, value fixture or log
change appears in that comparison. The simulator's new attacks are
kernel-valid by design; the election replay is their rejecting layer.

## Findings for the builder

1. **F1 — Criterion 7 lacks the session-order witness and includes pre-green invites.**
   `tools/status.py:376–385` and `tests/test_elect.py:202–226,341–365`.
   Brief: “at least 24 rounds ... whose invite is on the log before the session,
   replays from the prefix, and is resolved by its deadline” (315–317), and
   “invites before that instant are not rounds” (287–290). Counting checks no
   session start/filed time or durable link to it. The named test checks forecast
   entry timestamps, not when their session began. A session beginning before
   the invite but entering its forecasts afterwards is indistinguishable here.
   The green instant is checked separately under criterion 4 but is not a filter
   on `witnessed`. Add **`test_criterion7_session_start_order`** and
   **`test_criterion7_excludes_pre_green_invites`** in `tests/test_elect.py`.
   Preserve the brief's explicit exception for a genuinely missing session:
   that round is imputed and retained, not silently dropped.

2. **F2 — The invite itself can be resolved by the wrong principal and count.**
   `tools/status.py:383–384`; `tests/test_elect.py:262–275,349–351`.
   Brief: “the invite itself is resolved by that same session” (178–182).
   The predicate accepts either builder or reviewer rather than
   `elect.resolver(f)`. The signed 24-round probe above passes criterion 7 with
   every invite resolved by its invited arm; kernel acceptance is expected
   because the invitation's forecaster is herald. The current resolver pin
   checks the routing helper and event resolutions, not this status path.
   Missing: **`test_criterion7_invite_resolver_routed`**.

3. **F3 — A nonempty evidence string stands in for an existing evidence page.**
   `tools/elect.py:157–170`; `tests/test_elect.py:258–260`;
   `sim/election.py:58`. Brief: “a missing forecast, a missing evidence page or
   an event unresolved by the invite's deadline counts at the maximum ln 1000
   (n = 1)” (77–79). Only truthiness of `body.evidence` is checked. There is no
   page-presence/hash check or validated-evidence input in this path. With the
   fixture's literal `"saved public page"`, no corresponding saved page, all six
   events yield `gain=Fraction(1,1), success=1, complete=True`. The existing test
   covers an empty string, not a missing referenced page. Missing:
   **`test_missing_evidence_page_imputed`**, with an actual-present page twin.

4. **F4 — The stale W5 base lets an unrelated entry discharge a writ.**
   `tools/due.py:36,46–50`; `tests/test_due.py:51–60`.
   Brief: a discharge seq must name an entry “whose canonical body contains the
   row's id”; “an unrelated entry at a valid seq ... discharges nothing”
   (217–219). `prefix` stores timestamps, discarding bodies; any timely existing
   integer seq passes. Reproduced `report` discharged by seq 7 with
   `body.args.id="other"`: `done seq 7 on time`, malformed flag False.
   `origin/builder-w5` commit `3dea34b` already fixes this and supplies the
   stronger `test_w5_done_is_an_entry`; carry that fix forward.

5. **F5 — The stale W5 base permits in-place completion and rejects the required append form.**
   `tools/due.py:24–30,37–40`; `tests/test_due.py:62–70`.
   Brief: “the original row is never rewritten; a discharge is a later line
   {id, done: {...}} that folds onto it” (220–222). `unchanged` explicitly
   permits replacing `done=None` in the original row, and `project` requires
   every row to contain all four fields, so the append-only discharge form is
   malformed. Reproduced acceptance of an in-place rewrite. The requested diff
   also loses byte-prefix checks and `test_malformed_discharge_lines` from the
   newer W5 head. Carry forward `3dea34b` and its tests; no pin/test workaround.

6. **F6 — Full C2b exit/status integration is not delivered.**
   `tools/status.py:294–295,399`; `transcripts/PROPOSAL-election.md:9`.
   Brief: “tools/status.py the election line, criteria 1–9 and promote C2b”
   (375–376); value and liveness “continue from C2a's” (35–37).
   `assess_election` permanently returns False for criteria 5, 6, 8, 9 and
   attaches neither value nor continued liveness. This is honestly disclosed
   by the handoff and fails closed, but the promised exit assessment cannot
   become lawful. Deliver the integration and a
   **`test_c2b_full_exit_continues_wealth_and_enforces_all_criteria`** witness.
   The engine/fixture continuation checks above pass; they do not complete
   this missing integration.

7. **F7 — The full recorded-gains draw mutant has only a diagnostic kill.**
   `tests/test_elect.py:153–156,290–292`; `sim/election.py:66–80`.
   Brief: replay “recomputes G, pi and U from the signed prefix ... requiring
   the recomputed args ... to equal the recorded ones byte for byte”
   (149–152); named mutant “from args.gains” (335–336).
   The final mutant clones `invite_body` with only its `state` dependency
   replaced by the recorded gain vector, so cuts, arm, propensity, claim and p
   are genuinely recalculated from that vector. The named test fails only at:
   `AssertionError: 'args.gains' not found in 'rigged_election: args.cuts differs'`.
   Its forged gains are inconsistent with the other saved fields, so the
   mutant still rejects that attack. Running this same mutant against existing
   `test_rigged_election` gives **SURVIVED**, twin PASS:

   ```text
   coherent_draw_coverage_probe  from_args_gains  SURVIVED
   KILLED 0, SURVIVED 1, STALE 0, TWIN FAILED 0, PENDING 0
   ```

   Missing: **`test_draw_replays_coherent_forgery`** — a validly signed invite
   with fabricated gains and *all* their dependent fields internally
   consistent, on a feedback-complete prefix, rejected solely because those
   gains are not the prefix's. Keep an honest replay twin. This is a coverage
   finding, not a claim that the unmutated replay currently trusts those gains.

No registered election mutant is STALE or SURVIVED; the separately labelled
behavioral coverage probe is SURVIVED as reported in F7. Green registered pins
therefore do not remove the production/integration findings or the named
missing-witness obligations.
