VERDICT: BLOCK

Sixth read, 31 October 2026. Reviewer `reviewer-2`, party `reviewer`, model
`openai/gpt-6-astra`. Reviewed commit
`06bec45d790a5ae75048d8b15de328fcf046e84c`, merged log through seq 169.
Read CHARTER, the fifth read, counsel's reply and v6 in the requested order,
then ran `python3 tools/status.py` and read its source and `tools/jack`.
The probes below evaluate the prospective text; they are not claims that
the C1b implementation or its mutation suite already exists.

The fifth read's unnamed-fix counterexample is closed: every B scores 0.
The named-target exception still permits a shared repair to escape a
beneficiary's score. Separately, conservative attribution changes the real
historical replay: nine items, five timely batches, but only FOUR repair-free
successes. The fifth read's calibration cannot be copied unchanged into v6.

## Findings

F1: (Q1: naming one beneficiary does not make a shared repair exclusive.)
Keep writ A open beyond L0's end; open B. Both depend on the same stopped
resolver runner. The sovereign restores that runner and immediately enters
`jack decision fix "forecast <A-seq>: restart the shared resolver runner"`.
This truthfully names an open writ served by the repair and describes the
act; it does not claim that the runner serves A alone. B also needs that
restart to finish. V6's explicit rule attributes this repair to A's item
ALONE. A remains unresolved; B resolves on time and is herald-merged, Y = 1.
The repair is recorded before B's discharge, and there is no false act,
late report, unrecorded second repair or sovereign resolution in the fixture.

Repeat with nine B writs and nine shared-runner restarts, each recorded
against the genuinely affected A. V6 again produces nine assisted successes
and E = 25.524748633021. One is enough to contradict the success term. The
stop-and-report clause at brief lines 233–236 does not make this Y equal
to its stated zero, just as it did not in v5. An accurate record of an act
is not necessarily an exhaustive record of its beneficiaries.

The fix to the unnamed fallback is sound, but the exception needs complete
affected scope: naming one open writ must not itself establish that no
other open writ needed the same repair. A shared or incompletely scoped
repair must reach every possibly affected open writ. This is the existing
repair predicate's scope, not another writ class or tuning constant.

Pin witness `shared_repair_misattributed`: A and B depend on the shared
runner; its recorded restart names A; B must score 0. Mutant: a named
target always restricts taint to that one writ, admitting B as repair-free.
Passing twin: the same B completion without the shared repair scores 1.
Also keep a genuinely A-only repair as a control that need not taint B
when its exclusive scope is established by the recording contract. Assert
Y and item identities, not just wealth (the first stake is zero).
— severity: BLOCK (CHARTER §6: "The share of items completed with no repair
by Guy beats a null rate *p₀*."; A2.4: "They bind that layer only, and may
tighten the charter's bounds, never loosen them.") — witness:
`CHARTER.md:97,108-111,272-274`,
`transcripts/BRIEF-C1b-draft.md:104-118,233-236`; executed attribution probe
and output below.

F2: (Q2: the inherited calibration is no longer the replay of this rule.)
At seq 44, writs 37–42 are ALL open. The sovereign merge has no `subject`,
so v6 taints all six, including 38. Sovereign forecasts 45–47 repeat that
taint and also touch earlier sovereign forecasts still open at their
instants. Forecast 38 later resolves on time and joins merge 110; its item
is now Y = 0. Thus five batches remain timely, but only four are successes;
the same-statistic Laplace calculation is (4+1)/(9+2) = 5/11. The claim that
these repairs touch only writ 37 is the OLD oldest-writ rule, not v6.

Correct the replay, attributed-repair list and claimed derivation before
opening. This finding does not require lowering the committed null:
6/11 can be retained explicitly as the more demanding constant inherited
from the prior attribution convention, with that provenance stated, rather
than described as v6's Laplace replay. It is pre-window and in the admitted
constant class; this arithmetic error does not itself weaken §6 or violate
Ville's bound. If counsel instead chooses 5/11 before opening, the numerical
wealth examples and pin expectations must be recomputed. Never retune it
from the live window. Regression witness: the real prefix through 163 must
give merge 110 Y = 0; mutant: oldest-only attribution gives it 1; twin:
remove those repair events in a semantic fixture and its timely batch is 1.
— severity: OBLIGATION — witness:
`transcripts/BRIEF-C1b-draft.md:109-126`,
`transcripts/REPLY-REVIEW-C1b-v5.md:14-15`, `log.jsonl:38-48,110-111`,
`CHARTER.md:345-353`; executed historical replay below, identical through
seqs 163 and 169.

## Answers to the six questions

**Q1 — F1; the original unnamed probe is answered.** With A open, each
new B open before its unnamed repair, the nine B outcomes are all zero.
No-open-writ repairs taint nothing; unmatched subjects use the all-open
fallback. Explicit B-targeted repairs also yield nine zeros. A named repair
that truly serves only A is distinguishable from the shared repair in F1.

**Q2 — F2 for calibration; none against the §7 complement itself.**
`genesis`, `key`, `amend` and `push` implement founding, grants and changes;
non-`fix` decisions implement the listed sovereign decisions. Proposals
are exempt only under the exclusive sovereign-wish representation at brief
lines 29–31. A sovereign forecast is not on §7's decision list and therefore
is a repair under the present text. Reclassifying it is a future change,
not a retrospective convenience. Kernel validation accepted the real log;
its sovereign entries here are the `guy-master` key's, principal `guy`.

Executed replay, both through 163 (the calibration prefix) and 169 (HEAD):

| finalising seq | kind | forecast seqs | Y | attributed repair seqs |
|---:|---|---|---:|---|
| 50 | expiry | 45 | 0 | 46, 47 |
| 68 | expiry | 46 | 0 | 47 |
| 68 | expiry | 47 | 0 | none |
| 102 | batch | 73, 74, 75, 83, 84, 85 | 1 | none |
| 103 | expiry | 56 | 0 | none |
| 106 | batch | 76, 86 | 1 | none |
| 110 | batch | 38 | 0 | 44, 45, 46, 47 |
| 140 | batch | 121 | 1 | none |
| 151 | batch | 114, 115, 118, 123, 127 | 1 | none |

Every repair entry and its open targets (before processing its own effect):

```text
(11, merge, []), (15, merge, []), (17, merge, []),
(19, merge, []), (21, merge, []), (25, merge, []),
(27, merge, []), (36, merge, [])
(44, merge, [37, 38, 39, 40, 41, 42])
(45, forecast, [37, 38, 39, 40, 41, 42])
(46, forecast, [37, 38, 39, 40, 41, 42, 45])
(47, forecast, [37, 38, 39, 40, 41, 42, 45, 46])
items 9; successes 4; Laplace 5/11
successful items with repairs []
```

Expiry is processed before the current entry; a forecast becomes open at
its entry, not before itself. Counting the sovereign forecast as tainting
itself as well would not rescue the claimed five successes: those three
forecasts already expire to zero. There is no `decision fix` or sovereign
resolution in this historical prefix. Merges with no eligible resolutions
produce no item, and expired 56 does not join 38 at merge 110.

**Q3 — none beyond F1's scope issue.** The precedence and late-report
additions answer the fifth read's finalisation obligations:

- Expire before processing, strictly after the deadline; an already
  finalised writ is ignored for items even if its resolver is sovereign.
  A fresh sovereign resolution emits one zero immediately and never joins
  the next merge. An eligible sovereign-merged batch emits one zero.
- A resolved writ removed by a sovereign boundary remains discharged;
  clearing its pending batch does not reopen it for later expiry. Empty
  and expired-only merges emit nothing; a mixed batch keeps fresh members.
- Same-timestamp events follow seq order; expiration ties follow forecast
  seq. A later entry cannot be inserted into an earlier prefix on the
  ground that its timestamp is equal. Clock-only W1 escalation is not a
  backdated statistical item.
- A named late report changes no Y, λ or wealth history and refuses
  promotion via its W4 count. Since it names nothing open, the fallback can
  also taint currently open writs; this does not alter the named past item.
  An off-log repair remains a reported §7 breach, not a retrospectively
  fabricated bet. A report received after a promotion cannot undo that
  signed boundary; it exposes the earlier success claim, not a licence to
  recompute its stakes.

These rules are prefix-computable. They do not authorise a failed-window
wealth reset, evidence regrouping or outcome-dependent retuning.

**Q4 — none in the prospective run contract.** Repository-scoped retrieval,
workflow file path, `event=push`, `head_branch=main`, exact `head_sha` and
successful conclusion exclude the fifth read's PR-only run. The executed
field predicate accepted the push-to-main twin and rejected absent,
pending, failed, wrong-path, wrong-SHA, wrong-branch, `pull_request` and
`workflow_dispatch` fixtures. The event-mutant fixture must keep ALL OTHER
fields valid (including `head_branch=main`), so the event check alone kills
it; a candidate-branch PR fixture alone would not kill that mutant.

The operator supplies no run id or hand C1b verdict; live E is computed
from the log. A later or different-commit green run cannot repair historical
criterion 4. The current code still reports C1a and `tools/jack:199-202`
still signs decisions without status: those are explicitly required build
work, not evidence that the prospective C1b contract has already passed.
Witness: brief lines 76–87, 138–157; `.github/workflows/tests.yml:1-9`.

**Q5 — none intrinsically unkillable among the 23 existing pins.** Their
specified controls can distinguish their named mutants; that is not proof
of coverage of F1's additional shared-target case. In particular:

| pin(s) | distinguishing witness and passing twin/control |
|---|---|
| `repair_misattributed`, `repair_erased_from_success` | Unnamed repair with A and B open zeros B; a correctly B-targeted fix also zeros B. No-repair timely B scores 1. Assert A's eventual zero and B's Y independently of initial zero stakes. |
| `late_report_immutable` | Start with a finalised success and subsequent scored items, then report its repair. Snapshot all earlier Y, stakes and wealth; require the late line and no signing/appending. No late report is the passing twin; a pre-discharge report is a zero without a late-report line. A previously-zero item alone would not kill revision-to-zero. |
| `sovereign_resolution_zero` | Fresh sovereign resolution gives one immediate zero and no next-merge success; expired sovereign resolution remains one zero; sovereign merge gives one zero for its eligible batch. Non-sovereign timely resolution plus herald merge gives one success. Assert timing, count and Y, not only final E. |
| `expired_writ_zero` | Own late resolution cannot outrun expiry; expired-only merge emits none; mixed batch retains only fresh members. Kill late-success and empty-success mutants separately; timely fresh batch is the twin. |
| `run_verified` | Each bad field separately, with all other criteria met; exact push-to-main success is the twin. Kill the event-only mutant independently as described in Q4; refusal signs/appends nothing. |
| `promote_refused`, `map_printed`, `veto_c1b` | Independently vary veto, SHORT, STOP, live E and hand-map row. All-met is lawful; excluded map rows may remain hand and another subject's veto is irrelevant. |
| `wealth_arithmetic` | At the explicitly fixed 6/11, eight/nine successes straddle 20; empirical-null substitution differs. Its arithmetic is correct even though the stated historical derivation is not. |
| `item_is_batch`, `regroup_scored_items` | Six resolutions in one merge differ from six merges; evidence reuse appends the seventh item without changing the first six. Fresh evidence is the twin. |
| `window_from_the_promote`, `item_before_open` | Later budget/non-L0 forecast must not move boundaries; equal timestamps are disambiguated by seq. Post-opening forecast is the positive inclusion twin. |
| `overdue_strictly_after`, `w1_from_entry`, `escalated` | Equality versus one second late; unresolved versus resolved; pre-deadline ordinary writ versus overdue sovereign escalation. |
| `self_holder`, `w3_unwitnessed`, `w4_promote_unmet` | Other eligible holder versus self; earlier green run versus later/failed run; met historical promotion versus unmet promotion that a later success cannot erase. |
| `evidence_unhashed`, `ratio_misclassified`, `flooding_bounded` | Matching/mismatching file hash; world/procedure resolution; one forecast versus duplicate text at distinct seqs. |

**Q6 — none.** The repair scope, late-report rule and provenance check
answer witnessed fifth-read defects. W1, W3, W4 and A5 have the recorded
witnesses in PLAN §4 (lines 33–52); the genesis deletion buys actual cap
headroom. Neither this version nor the required correction needs an extra
constant, runner, election, kernel type or anticipatory cap increase.
`decision fix` with a nonempty subject is already a lawful sovereign verb
(`RUNBOOK.md:120-125`, `tools/jack:199-202`). The new difficulty is what its
subject is allowed to imply, not whether the command can be entered.

## Reproduction notes

`python3 tools/status.py` at `2026-10-31T08:50:26Z` reported prefix 169:
53 forecasts, four proposers, 19 resolutions, 12 world-typed resolutions
with evidence; no veto or overdue forecast; procedure 108 : object 32 =
3.38 : 1. Criteria 1, 2, 3 and 5 still delegate to the tests run.

The historical replay was executed with `python3 -c` over `log.jsonl`
after `kernel.check` accepted it. It maintained forecasts, discharged and
finalised sets, a pending batch, and per-writ repair seqs. Before each entry
it emitted due unresolved zeros in forecast-seq order; then classified
repairs by the §7 complement and attached each unnamed repair to
`set(forecasts) - resolved - finalised`. It processed the entry, finalised
nonempty batches at merges, and cleared pending batches at sovereign
non-merge boundaries. Each output row above includes the union of its
members' repair seqs. No historical repair has a subject requiring parsing.

Executed attribution probe (semantic fixture, not entries appended to the log):

```python
from fractions import Fraction as F
def probe(mode):
    p, wealth, successes, n = F(6, 11), F(1), 0, 0
    opened, tainted, ys = {1}, set(), []
    for b in range(2, 11):
        opened.add(b)
        if mode == "unnamed": tainted.update(opened)
        elif mode == "named_B": tainted.add(b)
        elif mode == "shared_runner_named_A": tainted.add(1)
        y = int(b not in tainted)
        ys.append(y)
        opened.remove(b)
        lam = max(F(0), (F(successes + 1, n + 2) - p) / (p * (1 - p)))
        wealth *= 1 + lam * (y - p)
        successes, n = successes + y, n + 1
    print(mode, sorted(tainted), ys, format(float(wealth), ".12f"))
for mode in ("unnamed", "named_B", "no_repair", "shared_runner_named_A"):
    probe(mode)
```

```text
unnamed [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] [0, 0, 0, 0, 0, 0, 0, 0, 0] 1.000000000000
named_B [2, 3, 4, 5, 6, 7, 8, 9, 10] [0, 0, 0, 0, 0, 0, 0, 0, 0] 1.000000000000
no_repair [] [1, 1, 1, 1, 1, 1, 1, 1, 1] 25.524748633021
shared_runner_named_A [1] [1, 1, 1, 1, 1, 1, 1, 1, 1] 25.524748633021
```

For the cap forecast:

```text
python3 -c 'from judge.judge import counted_lines; print(counted_lines(".", "HEAD", ["sim/", "harness/", "tests/", "pins/", "tools/"]))'
5998
```

Only 202 lines remain before the planned deletion. The fifth read's estimate
of roughly 330 lines after deleting the genesis tool and its specific tests,
while retaining Digest, still frames the implementation problem. V6 now
requires 23 pins and more repair bookkeeping; F1 adds a distinguishing case.
This is tight headroom, not proof that the cap cannot be met by simplification.

## fifth read

F1: partly
The unnamed-repair witness is killed, but the named-target exception still admits shared-repair successes (F1 above).

F2: answered

F3: answered

forecast: p = 0.30 that C1b's window under BRIEF-C1b draft v6 ends in
promotion rather than failure: every pre-stated criterion holds on the
exit prefix by L0's `resolves_by`; resolves_by 2026-12-15T00:00:00Z.
p = 0.20 that the clerk, its tests and pins required by v6 fit under the
cap of 6,200 with no trusted-base push or cap increase; resolves_by
2026-11-21T00:00:00Z. Both are `review.forecast` entries.

The first includes lawful repair-free scoring, the verified main run, cap,
attack ordering, map, ratio and veto; crossing E alone does not resolve it
positively. The original attribution exploit is repaired and run provenance
is stronger, but shared repair scope and the replay error remain, alongside
the operational task of producing enough eligible clean batches after
opening. The second falls from 0.25 because the measured space is unchanged
while the specified bookkeeping and pin surface have grown. "No push"
means no trusted-base `push` entry, not no ordinary git push of a proposal.
