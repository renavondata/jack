VERDICT: ACCEPT

Seventh read, 31 October 2026. Reviewer `reviewer-2`, party `reviewer`, model
`openai/gpt-6-astra`. Reviewed commit
`2eee0d0cfc92a979bc3f616d0aa6b434c852594c`, merged log through seq 175.
Read CHARTER, the sixth read, counsel's reply and v7 in the requested order;
ran `python3 tools/status.py`, then read its source and the `decision` verb.
Also checked PLAN-20261030 §4, RUNBOOK and the v6-to-v7 diff.

Findings: none. The sixth reader's BLOCK and calibration obligation are
answered. No further text change is required by this review before lawful
opening. The implementation, its pins and the pre-opening checks remain the
work expressly required by the brief; this is acceptance of that contract,
not a claim that the current tools already implement it.

## 1. Sovereign repair and the shared runner — none

The sixth read's A and B both depend on a stopped runner. A is genuinely
named by the sovereign's restart, remains open, and B completes on time.
V7 attributes the repair to BOTH. B is zero. Repeating the construction
with nine B writs gives nine zeros, not nine successes. Naming A, naming B,
an unmatched subject and naming no writ cannot narrow the all-open set.
The subject still records the act; it is no longer a claim of exclusive scope.
Witness: `transcripts/BRIEF-C1b-draft.md:106-122,205-214`.

Executed semantic probe, with A older than each B, all deadlines in the
future and each B resolved and herald-merged after the shared repair:

```text
shared runner all [0, 0, 0, 0, 0, 0, 0, 0, 0] E=1.000000000000
shared runner named [1, 1, 1, 1, 1, 1, 1, 1, 1] E=25.524748633021
shared runner oldest [1, 1, 1, 1, 1, 1, 1, 1, 1] E=25.524748633021
shared runner no_repair [1, 1, 1, 1, 1, 1, 1, 1, 1] E=25.524748633021
```

`all` is v7; `named` and `oldest` are the two attribution mutants, not
alternative readings of v7. The no-repair stream is the passing twin.

A genuinely A-only repair also zeros an open B that did not need it.
That is the express conservative criterion, not retrospective attribution:
it costs B a success when B's item is finalised, but changes no previous
item or stake. The sixth read's optional exclusive-scope control is no
longer a requirement; it would contradict v7's deliberate tighter rule.
Broadcast taint does not require independent outcomes: A4 tests the
conditional-mean null, not an IID Bernoulli model.

There is no on-time, fully recorded version of the shared-repair escape
left. The qualification matters: a repair first reported AFTER a success
was finalised leaves that recorded Y = 1 intact by design. It instead
raises W4 and prevents lawful promotion; an off-log repair likewise enters
the acts-table W4 count, not a retroactive bet. Concealment discovered after
a signed promotion exposes a false exit claim; it cannot undo that entry
or license recomputing the stakes. This is the explicit late/off-log path,
not another attribution exception for an accurately recorded repair.

## 2. The two null calculations — none

Keeping 6/11 is lawful. A4.2 requires a pre-window constant taken from the
incumbent's series, not the live window's estimated rate; A2.4 allows a
brief to tighten its criterion. V7 now identifies the historical convention
that produced 6/11 and explicitly denies that it is the all-open replay's
estimate. It introduces no new class of constant. With nonnegative stakes,
the fixed-null supermartingale argument continues to hold under
E[Y_i | past] <= 6/11. This is a committed benchmark, not a confidence
statement about the incumbent's unknown population rate.
Witness: `CHARTER.md:272-274,342-353`; brief lines 123-142.

I re-ran the historical fold after `kernel.check` accepted the real log.
The rows below are identical through seq 163 and through HEAD, seq 175.

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

```text
v7 items 9 successes 4 Laplace 5/11 merge110 0
v5/oldest mutant items 9 successes 5 Laplace 6/11 merge110 1
semantic twin items 6 successes 5 Laplace 3/4 merge110 1
8 successes E=15.469544626073
9 successes E=25.524748633021
10 successes + failure E=7.799228748979
```

The twin removes events 44-47 in the semantic fixture. Removing forecasts
45-47 also removes their three expiry items; it is NOT a nine-item twin.
The specified twin assertion is merge 110's Y = 1, which holds. Such a
fixture must be replayed as semantic data or rebuilt with valid signatures,
parents and references for an end-to-end test. Deleting four lines from the
signed production log and expecting recognition to accept it is not a
passing twin. No production log was changed for these probes.

## 3. Items, late reports and sovereign boundaries — none

No remaining case tested requires changing a placed bet. The controlling
order is brief lines 92-122: expiry before entry processing; resolved and
finalised writs excluded from the open set; entry order breaks timestamp
ties; only a nonempty eligible batch can form a merge item. A sovereign
forecast taints the previously open writs, then opens its own writ; a later
entry at the same timestamp cannot be inserted ahead of it.

Executed boundary fixtures produced:

```text
fresh sovereign resolution                 [0]
expired sovereign resolution               [0]
sovereign eligible merge                   [0]
sovereign empty merge                      []
cleared pending stays discharged           []
mixed expired and fresh                    [0, 1]
repair between resolution and merge        []
no open repair then new writ               [1]
late report: prior items/stakes unchanged; outcomes [1,1,1,1,1,1,1,1,1,0]
prefix-extension invariants PASS
```

In particular, a repair after resolution but before herald merge cannot
launder a pending success: the sovereign non-merge boundary clears that
batch. A sovereign merge instead emits its eligible batch at zero. A
cleared resolution stays discharged, rather than becoming another expiry.
A repair with no open writ has no future taint; it is not a perpetual tax
on subsequently opened work.

For the late-report probe I first finalised NINE successes, including
nonzero stakes, then opened a new writ and reported a repair naming the
first completed writ. Every old item, lambda and wealth value stayed
identical; the new writ scored zero. The additional W4 refusal is required
by the text and `late_report_immutable`; this semantic arithmetic probe
does not claim to have executed a future `status.py` implementation.

Read literally, v7's late-report sentence is conservative: a repair entered
after an item has finalised is called a late report, with no new-beneficiary
exemption stated. That can cost promotion even when the repair cannot
affect an earlier item. It does not change that item or its bet, and no
narrowing of this criterion is necessary for lawful opening. In particular,
the subject must not be used to resurrect the named-scope exemption in
the taint computation.

The A4 continuation rule still binds failed windows: no wealth, outcome
history or Laplace counts reset, and no retuning from the live window.
The opening excludes pre-opening forecasts even at equal timestamps
(`item_before_open`); the closing is L0's deadline or lawful early promotion,
not a later budget or a later forecast. At the promotion entry, any newly
due expiries must be included before declaring the exit criteria met.

## 4. Can the pins distinguish their mutants with passing twins? — none

Yes, as prospective contracts. There are 24 pins. This is not a claim of
24 implemented mutation kills on today's tree.

The new attribution pin needs BOTH A's and B's assertions. My two-writ
probe resolved B first and A second, both timely:

| repair subject | v7: B,A | named-only mutant: B,A | oldest-only mutant: B,A |
|---|---|---|---|
| names A | 0,0 | 1,0 | 1,0 |
| names B | 0,0 | 0,1 | 1,0 |
| names neither | 0,0 | 0,0 | 1,0 |
| no repair (twin) | 1,1 | 1,1 | 1,1 |

Thus the named-B case kills named-only attribution through A, not B. The
unnamed case kills oldest-only attribution; it need not also kill the
named-only mutant's correct fallback. Assert identities and Y directly:
initial zero stakes would otherwise hide the difference. The shared-runner
case is now contained in `repair_taints_all_open`, rather than requiring
another pin. `replay_merge_110` kills oldest-only attribution and has the
passing semantic twin shown above. Witness: brief lines 208-214.

The remaining distinguishing witnesses and twins are still possible:

| pins | discriminating fixture / passing control |
|---|---|
| `overdue_strictly_after`, `w1_from_entry`, `escalated` | Equality versus one second late; open before deadline versus resolved; overdue sovereign escalation versus ordinary open writ. |
| `self_holder` | Both self and another eligible principal exist; name only the other, not an empty holder set. |
| `w3_unwitnessed`, `w4_promote_unmet` | Failed/later green run versus earlier green; unmet historical promotion versus all-met then. Later success cannot erase the historical defect. |
| `promote_refused`, `veto_c1b`, `map_printed` | Each unmet condition varied independently against all-met; another subject's veto and excluded hand map rows are controls. Stub the signing effect and assert no append on refusal. |
| `run_verified` | All valid run fields in the twin; corrupt each field separately. For the event-only mutant keep workflow path, SHA, successful conclusion AND `head_branch=main` correct while changing only `event` to `pull_request`. |
| `wealth_arithmetic`, `item_before_open`, `window_from_the_promote` | Fixed 6/11 arithmetic; same-timestamp forecasts on opposite sides of opening; later budget/non-L0 forecast must not move either boundary. |
| `item_is_batch`, `regroup_scored_items` | One six-resolution batch versus six batches; seventh batch reuses old evidence without changing the first six; fresh evidence is the twin. |
| `expired_writ_zero`, `sovereign_resolution_zero` | Own late resolution first expires; empty/expired-only merge emits none, mixed batch retains fresh members; fresh sovereign resolution emits one immediate zero, sovereign batch one zero; non-sovereign timely completion is the twin. |
| `repair_erased_from_success`, `late_report_immutable` | Pre-discharge repair versus no repair; late report of a prior SUCCESS after nonzero stakes, snapshot all prior state, W4 refusal and current-open taint. No report passes. |
| `evidence_unhashed`, `ratio_misclassified`, `flooding_bounded` | Matching versus mismatching evidence bytes; world/procedure resolution classification; identical claims at distinct seqs versus one forecast. |

## 5. New machinery without a recorded witness — none

V7 removes scope interpretation from the existing repair predicate. The
all-open requirement is forced by sixth-read F1's shared runner; the real
prefix regression by sixth-read F2. The late-report current-open taint was
already the sixth read's Q3 interpretation and now becomes explicit.
There is no new writ class, tuning constant, entry type, kernel mechanism
or anticipated cap increase. W1, W3, W4 and A5 retain the witnesses in
`transcripts/PLAN-20261030.md:33-52`. The deletion and retained Digest
coverage address the actual measured cap, not speculative machinery.

## 6. Anything left to block, or that a next version must change? — none

The text permits a lawful opening after its preconditions and order of
acts are met. The sovereign's `decision fix "<what>"` is a legal existing
command with a nonempty subject (`RUNBOOK.md:120-125`, `tools/jack:199-202`).
The new promotion refusal is explicitly builder work. Today's verb still
signs without consulting status, and today's status still reports C1a;
acceptance of v7 is not permission to open using those missing checks.
No eighth drafting round is required by this read.

## Reproduction and current state

The semantic probe used the sixth read's replay method with the named-scope
branch removed: maintain forecasts, discharged and finalised sets, pending
resolutions and per-writ repair seqs; expire before processing; broadcast
each repair to `forecasts - discharged - finalised`; process the entry;
emit nonempty merge batches and clear pending at other sovereign boundaries.
The two mutants replace that broadcast with a named target or the oldest
open writ. Fractions, not rounded floats, compute A4's lambda and wealth.
For every prefix of the historical stream and the boundary fixtures, its
item list and full `(Y, lambda, E)` history were compared to the corresponding
initial segment of the longer replay. All matched. These are probes of
the prospective text, not substitute production pin results.

`python3 tools/status.py` at `2026-10-31T09:31:58Z` reported prefix 175:
55 forecasts, four proposers, 19 resolutions, 12 world-typed resolutions
with evidence; no veto or overdue forecast; procedure 114 : object 32 =
3.56 : 1. Criteria 1, 2, 3 and 5 still delegate to the tests run.

```text
python3 -c 'from judge.judge import counted_lines; print(counted_lines(".", "HEAD", ["sim/", "harness/", "tests/", "pins/", "tools/"]))'
5998
```

There are 202 counted lines of headroom before the prescribed deletion.
The prior estimate of roughly 330 afterwards, retaining Digest, is still
a tight budget for the clerk, status changes, run verification and 24 pins.
Removing named-scope attribution simplifies the required implementation;
the additional historical replay pin consumes some of that gain.

## sixth read

F1: answered

F2: answered

forecast: p = 0.35 that C1b's window under BRIEF-C1b draft v7 ends in
promotion rather than failure: every pre-stated criterion holds on the
exit prefix by L0's `resolves_by`; resolves_by 2026-12-15T00:00:00Z.
p = 0.25 that the clerk, its tests and pins required by v7 fit under the
cap of 6,200 with no trusted-base push or cap increase; resolves_by
2026-11-21T00:00:00Z. Both are `review.forecast` entries.

Promotion includes the cap, verified main run, attack ordering, live E,
map, ratio and veto, not merely E crossing 20. Closing the textual defects
raises the first forecast from 0.30, but conservative taint, enough clean
post-opening batches and implementation under the cap remain substantial
risks. The second rises from 0.20 because the repair rule is now simpler,
not because more headroom has appeared. Its earlier resolution deadline
also differs from the promotion forecast's. "No push" means no trusted-base
`push` entry, not no ordinary git push of this proposal.
