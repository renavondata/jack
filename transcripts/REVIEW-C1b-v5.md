VERDICT: BLOCK

Fifth read, 31 October 2026. Reviewer `reviewer-2`, party `reviewer`, model
`openai/gpt-6-astra`. Reviewed commit
`a8e2dc20e2af703600ea219a6e546ff69d0539fe`, merged log through seq 163.
The charter, fourth read, reply and v5 brief were read in the requested
order, then `python3 tools/status.py`, its source and the decision verb.
This is a review of the prospective contract, not a claim that its clerk
or new mutation tests already exist.

V5 restores the predicate removed in v4. The historical calibration now
checks out. The remaining block is narrower: attributing an unspecified
repair to the oldest open writ can certify repair-assisted completions as
repair-free. The fourth reader therefore cannot close F3 in full.

## Findings

F1: (Q1: the oldest-writ fallback weakens repair-free success.) Take an
open post-opening writ A whose deadline is beyond L0's end. Open writ B,
then let the sovereign restart the runner needed to discharge B and
immediately record `jack decision fix "restart runner"`. This is precisely
the generic hand-repair recording the brief permits: it is signed, timely,
and names neither a forecast seq nor a PR. V5 attributes it to A. Resolve
B on time and merge it separately: B's item has no attributed repair and
scores Y = 1, although it needed Guy's repair. The fix is entered BEFORE
the resolution, so neither the classifier's delay nor retrospective
reporting causes this counterexample.

Repeat for nine newer writs while A remains open. All nine repairs accrue
to A; all nine repair-assisted batches score 1; E = 25.524748633021.
There is no zero for A before its deadline. One such false success is
already a violation; nine show that the promotion bound does not catch it.
The stop clause calls a necessary repair a Y = 0 item, but the executable
attribution rule assigns the zero condition elsewhere. Reporting and
stopping do not make these two definitions agree.

The fallback is prefix-decidable, but that is not sufficient: the charter
requires completion **with no repair**, not completion with no repair
assigned to it by an unrelated-oldest-writ convention. Require the actual
affected subject to be recorded before finalisation, or treat an
unidentified repair conservatively so that a possibly affected completion
cannot count positively. This needs no new constant or writ class.

Pin witness `repair_misattributed`: A remains open; a generic recorded fix
needed for B precedes B's timely resolution and herald merge; B must not
score 1. Mutant: send the repair only to A and admit B as repair-free.
Passing twin: the same B completion without a repair. Also retain an
explicitly B-targeted repair as a zero control. Assert Y, not just wealth.
— severity: BLOCK (CHARTER §6: "The share of items completed with no repair
by Guy beats a null rate *p₀*."; A2.4: "They bind that layer only, and may
tighten the charter's bounds, never loosen them.") — witness:
`CHARTER.md:97,108-111,272-274`,
`transcripts/BRIEF-C1b-draft.md:97-104,209-212`; executed probe below.

F2: (Q1/Q3: finish the repair classification and finalisation contract.)
The governing definition, "an entry signed by the sovereign's key that
§7 does not list as a decision", must control its examples. A sovereign
`forecast` is not a wish or another §7 decision; the real log has three
at seqs 45–47. They are absent from the parenthetical `fix`, `resolution`,
`merge` list, and the attribution sentence only specifies `decision fix`.
Do not implement those three examples as an exhaustive repair allowlist.
Key grants and lawful changes remain decisions under the amended charter.

Specify the remaining interactions without modifying a finalised item:

- A sovereign merge containing eligible resolutions must finalise a
  repair-assisted zero batch. Convention (iii) and the repair definition
  support that reading; (iv)'s "his other entries ... form no item" must
  not erase that batch. A sovereign merge with none eligible forms none.
- An already-expired writ stays one zero when the sovereign resolves it;
  (i) and (ii) take priority over (iv). A fresh sovereign resolution is its
  own zero and never joins the next merge. A mixed expired/fresh batch
  retains only the fresh writs. These are consistent readings of v5.
- A named `decision fix` can currently name an already-finalised forecast
  or PR, and the prescribed RUNBOOK recording is **after** the hand act.
  State what that late report does. Changing the earlier Y or its later
  lambdas violates A4.3; ignoring it cannot establish that the earlier
  success was repair-free. Distinguish the immutable statistic from an
  invalidated success claim/promotion assessment. Also specify unmatched
  subjects, no open writ, and equal-timestamp ordering by seq. None may
  revise a finalised item or retune a stake using its outcome. A repair
  occurring after a predictable stake but before its outcome is finalised
  is not itself a predictability violation.

For ordinary batches the four conventions now fix expiry-before-process,
the empty batch, the mixed batch and direct sovereign resolution. Evidence
reuse cannot regroup items; no clock-only expiry may later be redated onto
an earlier log prefix. A sovereign boundary can clear a pending batch;
the implementation must not subsequently resurrect its resolved writs as
expiry items. There is no executed-code allegation here: these are totality
and pin-coverage obligations on the new repair term. — severity: OBLIGATION
— witness: `transcripts/BRIEF-C1b-draft.md:87-104,176-184,217-218`,
`log.jsonl:46-48`, `CHARTER.md:108-111,348-353`,
`RUNBOOK.md:120-125`, `tools/jack:199-202`.

F3: (Q4: keep push-to-main provenance in the verified-run contract.) Live
E from the log and refusal on a hand C1b map row answer those parts of the
fourth read. The operator no longer supplies a run id, and missing,
pending, failed, wrong-workflow and wrong-commit runs can all fail. However,
the three named comparisons alone do not distinguish a PR-only run from
trunk evidence: `tests`, matching `head_sha`, and `conclusion=success` can
all hold on an Actions run whose `event` is `pull_request`. This repository
runs that workflow on both events, and expressly calls the PR run the
proposal's own informational test.

Have the repository-scoped fetch select the actual `tests.yml` workflow's
completed **push to main** run for the evaluated commit, and have the
verifier preserve/check that provenance. Do not use display name alone as
workflow identity. A clean exact commit is necessary, not sufficient.
Add PR-only success to `run_verified`'s refusing controls; twin: successful
push-to-main run for the same evaluated commit, with all other criteria
met. Assert the verb signs/appends nothing on refusal. The criteria already
require the main run, so this is completion of that contract, not another
block on the text. — severity: OBLIGATION — witness:
`transcripts/BRIEF-C1b-draft.md:75-84,131-142,157-162`,
`.github/workflows/tests.yml:1-9`,
`transcripts/REVIEW-C1b-v4.md:113-148`; three-field probe below.

## Requested questions not otherwise answered by findings

**Q1, wishes — none as a prospective reserved representation.** The text
reserves sovereign proposals for wishes in `transcripts/WISHES.md` and says
he signs no others. That is a fixed type/key convention, not a retrospective
classification by prose. The log presently contains no sovereign proposal.
This convention is sound only with that exclusive use: a sovereign proposal
performing a code repair is a breach of it, not a repair magically converted
to a wish. Wishes themselves remain unscored. The off-log acts table belongs
in W4, not in a delayed recalculation of prior bets. Its exclusion from the
bet does not excuse §7 violations or prove the original completions were
repair-free; the late-report obligation is F2.

**Q2 — none against nine items, five successes, p₀ = 6/11.** The merged
extension from 157 through 163 contains two reviewer forecasts, two
proposals and two herald merges, no resolutions or new expirations.
The item list is unchanged:

| finalising seq | kind | forecast seqs | Y |
|---:|---|---|---:|
| 50 | expiry | 45 | 0 |
| 68 | expiry | 46 | 0 |
| 68 | expiry | 47 | 0 |
| 102 | batch | 73, 74, 75, 83, 84, 85 | 1 |
| 103 | expiry | 56 | 0 |
| 106 | batch | 76, 86 | 1 |
| 110 | batch | 38 | 1 |
| 140 | batch | 121 | 1 |
| 151 | batch | 114, 115, 118, 123, 127 | 1 |

Merges 58 and 71 add no item; the expired member 56 does not contaminate
merge 110's fresh member 38. Each successful batch was timely and had no
sovereign repair attributed. "No sovereign repair" must mean **none for
these successes**, not no sovereign repair entries anywhere in the log:
the earlier sovereign merges exist, as do his three forecasts. Even applying
the general §7 complement and earliest-open-writ fallback to those acts
does not change this list: the affected open writ is 37, still unresolved.
There is no `decision fix` or sovereign resolution to parse in this replay.

The Laplace constant (5+1)/(9+2) is committed from the incumbent prefix,
not fitted on C1b. It is admissible under A4.2. It does not claim to estimate
a guaranteed conditional rate from nine observations. With this fixed null,
the executed rational-arithmetic calculation gives:

```text
eight successes                       15.469544626073
nine successes                        25.524748633021
ten successes followed by one failure   7.799228748979
six successes                          5.917511757790
seven successes                        9.492675111454
five successes                         3.765689300412
```

Thus the evidence-bridge control appends the seventh success; it does not
return to five. V5's rounded figures check out. No failed-window wealth
reset is authorised; C1a supplied no previous liveness bets.

**Q3 — F2; otherwise none.** On an ordered prefix with repair attribution
settled before finalisation, the four conventions define immutable items
and predictable A4 stakes. Equality is timely; expiry zeros precede the
current entry and are ordered by forecast seq. The defect in F1 changes
which quantity is measured, not whether the oldest-writ calculation can
be performed from a prefix.

**Q4 — F3; otherwise none intrinsically unfalsifiable.** Each criterion
can fail and an all-met control can pass. Live E is no longer replaced by
a green synthetic test; a hand map row reaches refusal; veto, SHORT, STOP
and absent evidence refuse. Fetching evidence removes run-id selection,
but is not itself authentication of its provenance. Selecting forecasts
and batch sizes still influences the live statistic, as the flooding
paragraph openly admits; this is not a new hidden operator-provided
promotion verdict. The existing `tools/jack:199-202` still signs without
status: the brief orders its replacement, rather than claiming it is done.

**Q5 — none intrinsically unkillable among the 21 named pins.** They remain
prospective. In particular:

| pin | distinguishing test and passing control |
|---|---|
| `repair_erased_from_success` | A correctly targeted fix before timely discharge gives Y=0; identical completion without it gives Y=1. It kills dropping the predicate, but does not kill F1's wrong-attribution mutant. |
| `sovereign_resolution_zero` | Fresh eligible sovereign resolution emits its own zero; a non-sovereign timely resolution emits one success only at its merge. Check no extra success at the next merge. Add the expired sovereign-resolution control from F2. |
| `run_verified` | Each named bad/missing run refuses; verified current-main push run passes. Add F3's PR-only case. |
| `promote_refused` | Independently vary veto, SHORT, STOP, required hand row and live E<20, keeping all other criteria met. Assert no signing and no append. All-met twin signs. Green synthetic tests with E=1 must still refuse. |
| `expired_writ_zero` | Zero is emitted before the first post-deadline entry, including its own resolution; expired-only merge emits none. A timely fresh resolution/merge passes. Exercise both named mutants separately and a mixed batch. |
| `wealth_arithmetic` | Fixed 6/11 gives the exact factors above; nine/eight straddle 20. An empirical-null mutant is distinguishable. |
| `item_is_batch`, `regroup_scored_items` | Assert identities and counts as well as E; one six-resolution merge differs from six merges; reused evidence appends rather than rewrites. |
| `window_from_the_promote` | Later budget and later non-L0 forecast each tempt a different mutant; assert opening and end separately. Single unambiguous opening/L0 is the twin. |

The remaining twelve have the same distinguishing controls as the fourth
read: equality/one-second-late; unresolved/resolved; self/other eligible
holder; later/earlier green run; unmet/met historical promotion; overdue/
not overdue escalation; pre/post-opening seq; bad/good evidence hash;
world/procedure resolution; duplicate-text distinct seqs/single seq; and
C1b/other-subject veto, with the map's hand/code control also as stated.
No test may substitute wealth alone where a zero initial stake would mask
a wrong Y.

**Q6 — none.** W1's late forecasts, W3's #31 lapse, W4's hand evaluation
and A5's idle window are PLAN §4's recorded witnesses. The new repair
predicate and boundary pins answer the fourth read; the run pin answers
its evidence obligation. `jack decision fix` already exists, accepts a
nonempty subject and is sovereign-only under SPEC §10.14. A2.6's failed-
window use is not a syntactic restriction prohibiting other repair subjects.
The proposed RUNBOOK line records §7's required act using that existing
verb; it is not a new type or a command the law makes impossible. F1 is
about its attribution, not about forbidding the recording. COUNSEL-OPEN
item 11 already witnesses unrecorded repair instructions and hand repairs.
No new runner, election or anticipatory cap increase is introduced.

## Reproduction notes

`python3 tools/status.py` at `2026-10-31T08:15:21Z` reported prefix 163:
51 forecasts, four proposers, 19 resolutions, 12 world-typed resolutions
with evidence; no veto and no overdue forecast; procedure 102 : object 32
= 3.19 : 1. Criteria 1, 2, 3 and 5 still delegate to the tests run. These
are current C1a outputs, not prospective C1b results.

The historical replay was executed against `log.jsonl`, using the
kernel-verified sovereign principal (only `guy-master` signs for it here).
Before each entry it expired unresolved/unfinalised forecasts in seq order;
resolutions marked their writ discharged; only unfinalised resolutions
entered the pending batch; a merge finalised its nonempty batch; a sovereign
non-merge cleared the boundary. Sovereign resolution would finalise zero.
The broad §7 repair complement recorded these `(seq, type, open target)`
pairs; the log has no named fix requiring a subject parser:

```text
(11, merge, none), (15, merge, none), (17, merge, none),
(19, merge, none), (21, merge, none), (25, merge, none),
(27, merge, none), (36, merge, none), (44, merge, 37),
(45, forecast, 37), (46, forecast, 37), (47, forecast, 37)
items 9; successes 5; Laplace 6/11
attributed repairs in successful items: []
```

F1's minimal attribution probe, executed with `python3 -c`:

```python
from fractions import Fraction as F
p, E, s, n = F(6, 11), F(1), 0, 0
open_writs, tainted, ys = {1}, set(), []
for b in range(2, 11):
    open_writs.add(b)
    # B needs a runner restart; its signed fix says "restart runner".
    tainted.add(min(open_writs))  # v5's generic-subject fallback
    y = int(b not in tainted)    # B then resolves on time in its own merge
    ys.append(y)
    open_writs.remove(b)
    lam = max(F(0), (F(s + 1, n + 2) - p) / (p * (1 - p)))
    E *= 1 + lam * (y - p)
    s, n = s + y, n + 1
print(sorted(tainted), ys, float(E))
```

```text
[1] [1, 1, 1, 1, 1, 1, 1, 1, 1] 25.52474863302088
```

These are semantic fixtures, not forged entries appended to the record.
There is no restriction in the brief requiring writ 1's deadline to precede
L0's end. With no repairs the all-one twin is legitimate; explicitly naming
each affected B yields nine zeros instead.

F3's field-check probe also returned `True` for the named three checks on
`{"name":"tests", "head_sha":sha, "conclusion":"success",
"event":"pull_request", "head_branch":"candidate"}` with `sha` equal
to the evaluated commit. This exhibits missing provenance checking, not a
claim that the absent future verb has already accepted such a run.

For the cap forecast, the actual judge's counter was called:

```text
python3 -c 'from judge.judge import counted_lines; print(counted_lines(".", "HEAD", ["sim/", "harness/", "tests/", "pins/", "tools/"]))'
5998
```

That leaves 202 lines before the planned deletion. Removing the 80-line
genesis tool and the genesis-specific tests buys roughly another 125,
while Digest coverage must remain. The clerk, status/evidence integration
and 21 pins compete for roughly 330 lines unless existing code is reduced.
This is a forecast input, not a proof that the bound is impossible.

## fourth read

F1: answered

F2: answered

F3: partly
The repair predicate is restored, but the unrelated-oldest-writ attribution still admits repair-assisted successes (F1 above).

F4: partly
Live E and the hand-map refusal are explicit; push-to-main run provenance still needs the verification and control in F3 above.

forecast: p = 0.30 that C1b's window under BRIEF-C1b draft v5 ends in
promotion rather than failure: every pre-stated criterion holds on the
exit prefix by L0's `resolves_by`; resolves_by 2026-12-15T00:00:00Z.
p = 0.25 that the clerk, its tests and pins required by v5 fit under the
cap of 6,200 with no trusted-base push or cap increase; resolves_by
2026-11-21T00:00:00Z. Both are `review.forecast` entries.

The first is promotion, not merely E crossing: it includes implementation,
the verified main run, cap, attack ordering, map and veto, and does not
count a promotion based on misclassified repair-assisted successes as
lawful. Nine clean batches are attainable, but the pre-opening forecasts
are ineligible and the historical record has four expirations. The second
prices the measured headroom and preservation of existing coverage. It
does not use "no push" to mean no ordinary git push of a proposal.
