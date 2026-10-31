VERDICT: BLOCK

Fourth read, 31 October 2026. Reviewer `reviewer-2`, party `reviewer`, model
`openai/gpt-6-astra`. Read against
`df0b13f1f84e3f3bd57074e339ff21d86d1167ed` (log through seq 157).
The four requested texts were read in order, followed by the status command,
its implementation and the decision verb. This reviews the proposed text;
it does not call prospective pins KILLED or prospective code implemented.

The third read's evidence-bridge counterexample is fixed. The block below is
on the new removal of the repair condition, which the charter still requires.

## Findings

F1: (Q1: make the boundary and empty-batch cases explicit.) Immutable merge
items, ordered expirations and no evidence regrouping can define an
append-only item process. The old extension now appends a seventh success:
at v4's p0, E goes from 5.398765714286 to 8.503056, never backwards to the
five-item value 3.4992. No earlier lambda changes. However, the builder still
needs the boundary convention stated for the sovereign's direct-to-main
entries. `main_ending` is a verb operation, not an entry type. In particular,
`jack resolve` under the master key is itself a main-ending operation. A
timely resolution entered that way has discharged its writ but belongs to
no later merge's run if the boundary is exclusive. It therefore contributes
neither a merge success nor an expiry zero under the written definition.
This can remain a prefix process, but it is not evidence of autonomous
completion and must not silently become a herald success in the next merge.

State the boundary predicate, the treatment of a resolution at the boundary
itself, and the eligible-resolution filter. For a merge containing only
resolutions of already-finalised writs, “a later resolution of it adds no
item” must mean **no batch item**, not `all([]) == True`. Apply the same
filter to mixed batches: expired writs must not be counted again. At a
resolution which is itself the first entry after its deadline, finalise the
zero before processing that resolution. These are implementation obligations
on the stated rule, not a renewed allegation that evidence reuse regroups
v4's items. Witness fixtures: timely master-key resolution followed by an
unrelated merge; expired-only and mixed expired/fresh batches; resolution as
the first post-deadline entry. Passing controls: an ordinary timely batch
and a resolution entered exactly at the deadline. — severity: OBLIGATION —
witness: `transcripts/BRIEF-C1b-draft.md:59-63,81-88,147-156`,
`tools/jack:68-80,218-222`, `RUNBOOK.md:42-48,149-162`; arithmetic below.

F2: (Q2: seven herald acts are real, but are not the full v4 item series.)
The seven named merges and the four timely batches check out exactly; the
table below reproduces the record. Yet “the incumbent measured on this log
with this statistic” is not the calculation (4+1)/(7+2). Under v4's expiry
rule, forecast 45 already contributes zero at seq 50, forecasts 46 and 47
contribute separate zeros at seq 68, and forecast 56 contributes zero at
seq 103. Merges 58 and 71 then have no unfinalised resolutions; merge 110
still has the timely resolution of forecast 38. With the nonempty,
unfinalised-batch interpretation in F1, the historical replay is **five
successes among nine items**, Laplace 6/11, not four among seven. Keeping
the expired member in mixed batch 110's Y instead gives four among nine,
5/11; neither reading gives seven items. The historical batch-only rate
and the prospective expiry-plus-batch rate must not be called the same
measured quantity.

A4.2 expressly permits a constant measured on the incumbent's prefix,
committed before C1b. Thus 5/9 is not an inadmissible constant or a null
estimated from the window it judges. Counsel can identify it accurately as
a batch-rate-derived benchmark with an explicit mapping, or commit a
same-statistic derivation before opening; this review does not silently
change p0. Ville's guarantee is conditional on the specified fixed-null
inequality, not a confidence claim that seven observations establish the
incumbent's true conditional rate.

Dropping the grace is justified by the existing `resolves_by` obligation and
the actual late cases. The stronger claim that a perfect historical sample
“measures nothing” is false: future failures remain possible, and the same
Laplace convention gives 8/9, not 1, for seven successes. A deadline need
not be tuned to make the historical sample fail. Also qualify “ten with one
failure give 6.8”: ten total items with one zero give 4.5082–6.6788 depending
on its position; **ten successes followed by one failure**, eleven items,
give 6.7622. — severity: OBLIGATION — witness:
`transcripts/BRIEF-C1b-draft.md:60-63,81-96`,
`transcripts/REPLY-REVIEW-C1b-v3.md:17-24`,
`CHARTER.md:345-353`, `log.jsonl:46-59,68-72,104-111`; replay below.

F3: (Q3: timeliness is not completion without the sovereign's repair.) A
repair-assisted timely resolution scores Y = 1 under lines 88–90, exactly
as a repair-free timely resolution does. Nine such batches cross E >= 20
even if Guy has to repair every one. That measures resolution timeliness,
not the Purpose's “act on its own obligations without the sovereign”. The
charter is explicit: its §6 binary success includes **no repair by Guy**.
A4 changes the wealth, null and betting formulas; none of A3, A4 or A5
removes that condition. §6's separate instruction to report unbounded
repairs per merge does not remove the bounded indicator of no repair from
the bet. §7 also requires every sovereign act to be an entry.

The delayed, minute-resolution classifier is a real measurement defect,
but it does not authorise a brief to loosen the charter. Nor must an
outcome be known when its bet is chosen: the bet must precede the outcome;
once finalised, the outcome cannot be revised. V4 also calls a necessary
sovereign repair “a failed item” in its stop clause while its Y explicitly
ignores it. Retain a reproducible repair-free success condition, or obtain
the lawful amendment before substituting a timeliness-only test. A weekly
report alone does not discharge this requirement.

Mutant `repair_erased_from_success`: identical timely batches, but one
requires a recorded sovereign repair during discharge; omitting the repair
predicate makes that item successful. Passing twin: the same timely
completion without repair. Assert the individual Y as well as wealth; the
initial zero stake can otherwise hide the error. — severity: BLOCK
(CHARTER §6: “The share of items completed with no repair by Guy beats a
null rate *p₀*.”; A2.4: “They bind that layer only, and may tighten the
charter's bounds, never loosen them.”) — witness:
`CHARTER.md:97-102,108-111,272-274,330-365`,
`transcripts/BRIEF-C1b-draft.md:15-22,88-90,103-105,175,181-184`;
the nine-success arithmetic below gives 22.039921152 with or without repair
under v4's specified Y.

F4: (Q4: verify the run, and distinguish C1a's criterion 5 from C1b's.)
The `lawful`/`refused` contract fixes the old SHORT-or-STOP loophole:
a veto and an unverified criterion must now refuse. Every named refusal
branch is falsifiable, with an all-met passing twin. Supplying a run id is
not itself supplying a verdict: it is safe as an untrusted locator only
if the tool fetches and verifies the evidence. Specify repository,
workflow identity, successful completion, push-to-main provenance and
exact commit correspondence to the evaluated clean tree/log prefix;
missing, failed, pending, wrong-workflow, wrong-commit and PR-only runs
must leave the criteria unverified. The operator must not be able to
substitute a claimed success or local output for that check.

There is also a per-window distinction left implicit. C1a criterion 5 is
the score-vector test; C1b criterion 5 is **actual live wealth**. Green
regression tests proving that nine synthetic successes cross 20 do not
prove that this prefix has nine successes. The specified tests workflow
currently runs regression tests, pins, self-check, simulator samples and
the kernel count; its green conclusion alone is not a live E result.
Require the actual prefix-bound criterion result, or compute E directly
from the log. Exercise a green tests run with live E = 1: promotion must
refuse; the otherwise identical E >= 20 fixture may pass. Likewise,
criterion 7 (a C1b map row still hand) must reach the promotion refusal,
not just `map_printed`'s assertion. Do not make ordinary code admission
depend on live E already reaching 20: the attack test/code must be able
to land before items can count.

These are evidence-contract and coverage obligations, not a claim that
the presently absent implementation has already accepted a forged run.
The existing decision verb signs without any status check; v4 explicitly
orders its replacement. — severity: OBLIGATION — witness:
`transcripts/BRIEF-C1b-draft.md:48-50,73-78,107-125,139-142,169-170`,
`BRIEF-C1.md:198-220`, `.github/workflows/tests.yml:1-29`,
`tools/status.py:67-79`, `tools/jack:199-202`,
`CHARTER.md:376-381`. Mutant: accept an operator-selected unrelated green
run, or substitute regression success for the live criterion; passing
twin: verified current-main evidence and all live criteria met.

## Remaining questions

**Q5 — none intrinsically unkillable among the eighteen named pins.** These
are prospective fixtures, not claims of executed mutation tests. F1 and
F4 specify the boundary and refusal coverage the implementation must carry.

| pin | distinguishing witness and passing control |
|---|---|
| `overdue_strictly_after` | Equality kills `<=`; one second later is overdue. |
| `w1_from_entry` | Not-yet-due unresolved forecast raises W1; resolved one does not. |
| `self_holder` | Forecaster and another principal both hold resolution power; only the other is eligible. Assert both exclusion and inclusion. |
| `w3_unwitnessed` | Failed run plus a green run after merge still raises W3; same-commit green run before merge discharges it. |
| `w4_promote_unmet` | Unmet historical promotion prefix raises REPAIR despite later success; all-met historical prefix does not. |
| `promote_refused` | Veto, SHORT, STOP and absent run each prevent signature and append; verified all-met control signs. Add F4's run and live-criterion branches. |
| `escalated` | Past-deadline writ prints ESCALATED and sovereign; earlier writ is ordinary open. |
| `wealth_arithmetic` | Eight and nine successes straddle 20 at fixed 5/9; empirical re-estimation cannot match the numeric factors. |
| `item_before_open` | Pre-opening forecast resolved later adds nothing; post-opening control counts. Use seq to distinguish entries sharing the opening timestamp. |
| `item_is_batch` | Assert one item versus six, not merely threshold crossing: at 5/9 neither one nor six successes reaches 20. Six separate merges are the six-item control. |
| `regroup_scored_items` | Reused-evidence bridge preserves six prior items and appends one; fresh separate batches also append. Assert identities, count and wealth. The cited 30.07/14.39 values are v3's, not v4's. |
| `expired_writ_zero` | Assert the zero at the first later entry, and no further item at late resolution or an expired-only merge. A timely resolution is the passing control. Start after six successes to distinguish wealth too: 1.518402857143 after expiry, unchanged by late resolution; an erroneous extra success gives 2.125764. |
| `window_from_the_promote` | Latest budget AFTER promote changes the opening under the first mutant; latest non-L0 counsel forecast AFTER L0 changes the end under the second. Assert each boundary separately; an unambiguous single-promote/single-L0 control passes. |
| `evidence_unhashed` | Existing mismatching bytes do not count; matching hash/file does. |
| `ratio_misclassified` | World forecast's resolution is object; procedure forecast's resolution is procedure. |
| `flooding_bounded` | Two equal claim strings at distinct forecast seqs raise two writs; one forecast raises one. |
| `veto_c1b` | C1b veto fails; other-subject veto passes and kills removal of the subject filter. |
| `map_printed` | Required hand row fails; all required rows code passes even with excluded runner/election rows hand. |

**Q6 — none.** The new immutable-item and expiry pins answer the third
read's F1; the explicit promotion refusal answers its F4. PLAN §4's
witnesses still support W1, W3, W4 and A5 enforcement. Retaining the
existing simulator/vector tools and the Digest tests preserves present
uses. No new runner, election, writ class or anticipatory cap increase is
introduced. Removing the repair term is an unlawful weakening (F3), not
an excess of new machinery.

## Record checks and reproductions

`python3 tools/status.py`, run at `2026-10-31T07:37:33Z`, reported prefix
seq 157: 49 forecasts, four proposers, 19 resolutions, 12 world-typed
resolutions with evidence; no veto or overdue forecast; procedure 96 :
object 32 = 3.00 : 1. It still delegates criteria 1, 2, 3 and 5 to the
tests run. It does not yet implement the prospective C1b status contract.

### Seven acts, verified from log.jsonl

Lateness compares **resolution.ts**, not the later merge.ts, to the
forecast's `resolves_by`, exactly as v4 defines Y. Line number is seq + 1.

| merge seq | resolution seqs | forecast seqs | deadline / late entry, or timely result | batch Y |
|---|---|---|---|---:|
| 58 | 52 | 45 | due 26 Oct 08:00:00Z; entered 09:13:10Z: +4,390 s = 1.2194 h | 0 |
| 71 | 69–70 | 46, 47 | due 28 Oct 00:00:00Z; entered 08:13:44Z / 08:13:47Z: +29,624 / +29,627 s = 8.2289 / 8.2297 h | 0 |
| 102 | 96–101 | 73–75, 83–85 | entered 28 Oct 15:32:09–22Z; due 5 Nov 16:00:00Z | 1 |
| 106 | 104–105 | 76, 86 | entered 29 Oct 02:31:23–25Z; due 5 Nov 16:00:00Z | 1 |
| 110 | 108–109 | 56, 38 | 56 due 29 Oct 00:00:00Z, entered 03:49:31Z: +13,771 s = 3.8253 h; 38 timely | 0 |
| 140 | 139 | 121 | entered 30 Oct 10:00:39Z; due 8 Nov 16:44:10Z | 1 |
| 151 | 145–149 | 114, 115, 118, 123, 127 | all timely; latest relative entry is 127's, 20 h 00 m 57 s before deadline | 1 |

All late resolutions would be timely under a 48 h grace. These are the
seven nonempty resolution batches; the underlying resolution outcomes
(the claims being true or false) are not the liveness outcomes.

The following replay was executed on the reviewed log. It treats the
sovereign's non-merge entries as main-ending boundaries, expires before
processing a late entry, drops already-finalised writs from batches, and
emits no empty batch. These assumptions are explicit rather than a claim
that this probe is the future implementation. The replay is a historical
calibration check; C1b has not opened and none of these are its live items.

```python
import json
es = [json.loads(x) for x in open("log.jsonl")]
forecasts, resolved, final, pending, items = {}, set(), set(), [], []
for e in es:
    for f, fc in sorted(forecasts.items()):
        if f not in resolved and f not in final and e["ts"] > fc["body"]["resolves_by"]:
            items.append((e["seq"], "expired", [f], 0))
            final.add(f)
    if e["type"] == "forecast":
        forecasts[e["seq"]] = e
    if e["type"] == "resolution":
        f = e["body"]["forecast"]
        resolved.add(f)
        if f not in final:
            pending.append(e)
    if e["type"] == "merge":
        if pending:
            fs = [r["body"]["forecast"] for r in pending]
            y = int(all(r["ts"] <= forecasts[r["body"]["forecast"]]["body"]["resolves_by"]
                        for r in pending))
            items.append((e["seq"], "batch", fs, y))
            final.update(fs)
        pending = []
    elif e["proposer"] == "guy":
        pending = []
print(items)
```

Output, wrapped:

```text
[(50, 'expired', [45], 0),
 (68, 'expired', [46], 0), (68, 'expired', [47], 0),
 (102, 'batch', [73, 74, 75, 83, 84, 85], 1),
 (103, 'expired', [56], 0),
 (106, 'batch', [76, 86], 1),
 (110, 'batch', [38], 1),
 (140, 'batch', [121], 1),
 (151, 'batch', [114, 115, 118, 123, 127], 1)]
```

### F1 extension and betting arithmetic

Take six timely, separate merge batches with evidence a through f. A
seventh merge contains two new timely resolutions citing a and b. At
every intervening prefix the first six finalised items remain unchanged;
at the seventh merge exactly one new success appears. The old
evidence-component mutant instead joins the first two groups and leaves
five successful components. This arithmetic was executed with exact
rational intermediates:

```python
from fractions import Fraction as F
from functools import reduce
p = F(5, 9)
def wealth(ys):
    def step(a, y):
        E, s, n = a
        lam = max(F(0), (F(s + 1, n + 2) - p) / (p * (1 - p)))
        return E * (1 + lam * (y - p)), s + y, n + 1
    return float(reduce(step, ys, (F(1), 0, 0))[0])
for ys in ([1]*6, [1]*5, [1]*6+[0], [1]*7, [1]*8, [1]*9):
    print(f"{wealth(ys):.12f}")
print([round(wealth([1]*i+[0]+[1]*(9-i)), 12) for i in range(10)])
print(wealth([1]*10+[0]))
```

```text
5.398765714286
3.499200000000
1.518402857143
8.503056000000
13.604889600000
22.039921152000
[6.678763985455, 5.009072989091, 4.508165690182, 4.508165690182,
 4.508165690182, 4.508165690182, 4.508165690182, 4.508165690182,
 4.508165690182, 4.508165690182]
6.762248535272727
```

No window reset is introduced by v4; C1a had no liveness bets. The
statistic/null must remain fixed and wealth continue across any subsequent
failed C1b window, as A4.1 already requires.

## third read

F1: partly
The evidence-bridge block is closed; F1 above asks for explicit boundary/eligibility treatment on direct-to-main and already-finalised cases.

F2: partly
The classifier dependency is removed, but its replacement violates the repair-free success requirement (F3); the main-ending convention needs F1's explicit contract.

F3: answered

F4: partly
Veto and missing evidence now refuse; F4 above requires authenticated run evidence and per-window live-criterion coverage.

forecast: p = 0.25 that C1b's liveness reaches E >= 20 within 7 days of
the `decision promote C1a` opening it, under v4's statistic (item = the
herald's act with expiry-zero items, p0 = 5/9, deadline = resolves_by);
p = 0.75 that at least one item in C1b's window scores Y = 0 under that
statistic. Both resolve by 2026-11-30T00:00:00Z.

These price the requested v4 statistic, not an unannounced repair to it.
Nine consecutive successes are substantially more demanding than v3's six;
the record has seven resolution-bearing merges over roughly five days,
three containing late resolutions, and expiry now penalises individual
overdue writs. The clerk can improve that record, but pre-opening forecasts
do not provide its live successes. The second probability allows for an
early successful exit before any deadline is missed. These replace neither
the prior forecasts nor their recorded meanings.
