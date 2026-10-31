VERDICT: BLOCK

Third cold read, 31 October 2026. Reviewer `reviewer-2`, party `reviewer`, model
`openai/gpt-6-astra`. Read against `b60c6fd7b56a0a8b8e4e4ac1c744e2ca9d5cd587`.
The required texts were read in the requested order. This is a review of the
specification, not a claim that its prospective code or pins already exist.

F1: (Q1: collapsed items must not regroup already-bet outcomes.) The two collapse
relations, read literally over the growing log, do not define an immutable
sequence of outcomes for A4's bet. Let six separate merges discharge six
repair-free, timely writs with distinct evidence strings a, b, c, d, e, f. The
brief counts six successes, E = 30.0745279702. Now a seventh merge discharges two
new timely writs, one citing a and one citing b. Shared evidence joins each new
writ to an old item; shared merge joins the two new writs. Thus the old a and b
items become one, leaving five successful components, E = 14.3856492124. This
is neither appending a failure (E = 6.3717220276) nor appending a success
(E = 64.1834438388) to the prescribed process: it deletes a previous outcome and
recomputes subsequent bets. All the new resolutions are permitted by SPEC §5;
the brief forbids neither evidence reuse nor a merge containing distinct
evidence. Ignoring those joins instead violates its collapse rule. Waiting for
the end does not supply the live prefix process required for early promotion.
The specification must state an immutable item-finalisation and ordering rule,
including later evidence reuse, a bridge between previously scored groups, and
a resolution after an expired writ has already contributed zero. Do not leave
this choice to the builder. The resulting unit should be named accurately:
global evidence components can span several herald acts, so they are not
necessarily "the herald's act". Mutant: `regroup_scored_items`; witness: the
extension above; passing twin: later discharges with fresh evidence in separate
merges append outcomes without changing any earlier item or bet. — severity:
BLOCK (CHARTER.md A4.3: "The bet is a function of the prefix." and
"λᵢ is determined by the prefix, and no λ is entered after its outcome.") —
witness: `transcripts/BRIEF-C1b-draft.md:74-97`, `SPEC.md:96,102`,
`CHARTER.md:348-353`; the actual record already contains a merge of resolutions
with distinct evidence (`log.jsonl:109-111`, seqs 108–110). The arithmetic below
reproduces the distinguishing values. No reset at a window boundary or
re-estimation of p₀ is alleged: the defect is regrouping inside the window.

F2: (Q1: inputs for collapse and repair attribution.) Equality of evidence
strings is decidable from the log. Membership in the *discharging merge* is
not specified by a log field: a resolution names its forecast and evidence,
while `merge.proposal` is a PR number and `merge.commit` a git object name, not
a list of resolution seqs. The tree/history can establish which resolutions
first landed together; choosing the next merge in log order is a different
convention, especially for the sovereign's direct-to-main resolutions, and
the brief does not state it. Thus the full grouping is not presently defined
by `log.jsonl` plus the classifier's output alone. Once membership and repair
instants are supplied, choosing one earliest open writ is mechanical (use the
log's order for equal opening timestamps), and its eventual group receives
the repair only once. However, the recorded classifier's CSV truncates act
times to minutes. Two writs can open and close within the same minute, so
that output cannot decide which was open at the repair's instant. Preserve
the source instant, identify the classifier revision and input snapshot, and
state the merge-membership and equality conventions before counting items.
"A repair is what the acts classifier types as one" does make Y depend on
an input outside the log. That is an expressly reported measurement dependency,
not by itself a forbidden kernel input or a reason to block; the defect is
the missing reproducible input contract. It does not waive §7's requirement
to record the sovereign's acts. — severity: OBLIGATION — witness:
`transcripts/BRIEF-C1b-draft.md:24-31,74-80`, `SPEC.md:95-102`,
`RUNBOOK.md:91-98,159-165`, `tools/jack:218-222`, and
`transcripts/evidence/c85f3dfc2fd2cfe9deb5757faa7817ef273f0900e64a7958a4183749fb88595a:179-199,354-359`.

F3: (Q2: delete the spent tool, preserve the live digest checks.) The distinction
between existing instruments and anticipation is sound, but the proposed
deletion is too broad. `tests/test_genesis.py` is not just a genesis test:
its `Digest` class checks `tools/digest.py` against the judge's digest and
checks refusal of symbolic links and submodules in the trusted base. Those
checks still serve `jack merge` and `jack push`. Retain that coverage when
removing the spent genesis path and report the resulting headroom, rather
than counting the entire 101-line test file as dead. Retaining `sim/run.py`
and `tools/vectors.py` is defensible on present use: the former is imported
and exercised by `tests/test_sim.py`, the latter by `tests/test_vectors.py`.
The brief's citations are inaccurate: SPEC §6 specifies signatures, the run
of record is `harness/diff.py` under SPEC §9a, and BRIEF-C1 criterion 5 reads
the score vector rather than generating it with `tools/vectors.py`. Cite
the actual present uses. The measured count is 5,998; deleting 80 + 101
lines would indeed leave 383 below 6,200, before retaining digest coverage.
"Stops and reports the shortfall; a push is decided on that number" is
consistent with §7 and A5: the shortfall informs a sovereign decision,
not an automatic cap increase or permission to promote with criterion 3
unmet. Any changed scope needs the lawful push and matching SPEC text;
it cannot silently relax this window's unchanged-cap criterion or move its
end. — severity: OBLIGATION — witness: `tests/test_genesis.py:22-53`,
`tools/jack:156,194`, `tests/test_sim.py:9,115-127,130-144`,
`tests/test_vectors.py:12,48-57`, `SPEC.md:299-332,417-437`,
`transcripts/BRIEF-C1b-draft.md:31-37,111-112,163-166`; counted-lines output
`5998`, component counts `80, 101, 125, 133` as reproduced below.

F4: (Q3: make the promotion gate cover the criteria, not just two words.)
The proposed check can fail: the `promote_refused` mutant drops the
pre-signing check, and a SHORT or STOP fixture then signs/appends where the
unmutated verb refuses; an all-met fixture signs in the unmutated tree.
Putting this in the verb preserves §5's kernel domain: the kernel remains
the deterministic recognition checker, and the verb can consult the tree,
clock and run evidence. But the specified textual trigger is not yet a
complete encoding of A5. The existing renderer prints a veto as `YES`,
without SHORT or STOP, and sends criteria 1, 2, 3 and 5 to a tests run
without expressing whether that run establishes them. A renderer state
with the numerical criteria met, ratio within bounds and a veto therefore
passes a literal SHORT-or-STOP guard. Require an unmet veto criterion and
every other unmet or unverified criterion to produce a refusing status;
exercise this through the verb with no signature or appended entry on
refusal. Checking criterion 3 locally, as v3 now orders, is necessary but
does not by itself close the other branches. The absence of prospective
code today is not this finding; the unsafe output convention is its witness.
— severity: OBLIGATION — witness: `tools/status.py:67-79`,
`tools/jack:199-202`, `transcripts/BRIEF-C1b-draft.md:45-49,69-71,133-134`,
`CHARTER.md:376-381`; the renderer probe below prints
`criterion 6: veto on the subject: YES` and
`SHORT-or-STOP guard refuses: False`.

## Answers with no additional finding

**Q4 — none.** On the stipulated record (counsel's named L0 before the
opening promotion), the start is `ts(decision promote C1a)`, the stated end
is `L0.body.resolves_by`, and the actual end is its minimum with a lawful
`decision promote C1b` timestamp. The exit prefix stops at that decision's
seq, not at later entries sharing its timestamp. The inequality
`L0.resolves_by <= L0.ts + 14 days <= opening.ts + 14 days` gives the
budget bound without an "expected promote" date. L0 now claims every
criterion on the exit prefix. Its claim is not its own resolver and need
not be resolved to determine the window end. There is no other window-end
date in the brief. `status.py` still needs the ordered implementation v3
explicitly requires. An expired L0 is not permission to move its end.

**Q5 — none intrinsically unkillable.** These are specifications of future
pins, not a report of KILLED results. All seventeen admit discriminating
fixtures and passing unmutated twins. The following details are essential;
in particular "distinct evidence" alone does not imply distinct items.

| pin | fixture that distinguishes its named mutant; unmutated passing control |
|---|---|
| `overdue_strictly_after` | Equality distinguishes `<` from `<=`; +1 second is overdue. |
| `w1_from_entry` | Unresolved, not-yet-overdue forecast already raises W1; resolved forecast does not. |
| `self_holder` | Give both the forecaster and another principal resolution power; only the other is named. |
| `w3_unwitnessed` | Failed run plus late green run still raises W3; an earlier green `tests` run for the same commit discharges the condition. |
| `w4_promote_unmet` | An unmet criterion at the historical promote prefix raises REPAIR; all met at that prefix does not. Later success must not erase it. |
| `promote_refused` | SHORT and STOP each prevent signing; all met signs. F4 requires real criterion-to-status coverage as well. |
| `escalated` | An overdue writ names the sovereign and ESCALATED; before its deadline it is an ordinary open writ. |
| `wealth_arithmetic` | Fixed p₀ = 0.41 gives the numeric E₅ and E₆ below; an empirical p₀ from six successes is 1 and cannot give those values. |
| `item_before_open` | A pre-opening forecast resolved after opening contributes nothing; an otherwise identical post-opening one contributes. |
| `item_collapsed` | Six timely resolutions sharing evidence count once; distinct evidence must also be in separate discharging merges for the stated distinct-item control. Include distinct evidence in one merge for the other collapse relation. F1 remains. |
| `repair_attributed_once` | Two open writs in distinct eventual items, with strictly ordered opening instants: the repair affects only the earlier; no repair leaves both successful. If both writs collapse to one item, broadcasting is observationally indistinguishable and that fixture cannot kill the mutant. |
| `window_from_the_promote` | For a latest-match selector, put the budget decision AFTER `promote C1a`, and a non-L0 counsel forecast AFTER L0 with a different end. Dropping either selector then changes an asserted boundary. A budget followed by promote would not kill that first mutant. |
| `evidence_unhashed` | A present file whose bytes mismatch its digest does not count; the matching file does. |
| `ratio_misclassified` | A resolution of a world forecast is object; a resolution of a procedure forecast is procedure. |
| `flooding_bounded` | Two distinct forecasts with identical claim text raise two writs; one forecast raises one. |
| `veto_c1b` | A C1b veto fails criterion 6; a veto on another subject does not. It is the latter control that kills removal of the subject filter. |
| `map_printed` | A C1b row still labelled hand fails criterion 7; all required C1b rows labelled code pass. Excluded runner/election rows may remain hand. |

**Q6 — none.** The two added pins (`item_collapsed`, `repair_attributed_once`)
codify the second read's F1 witnesses; they are not anticipatory machinery.
W1, W3, W4 and the promotion check trace respectively to the late forecasts,
the #31 merge lapse, hand-evaluated window criteria and the fixed-window
idle period in PLAN §4. W2 and the speculative cap increase were removed.
Existing simulator/vector instruments have present uses (F3). The defects
above concern the meaning, inputs and coverage of witnessed mechanisms,
not a request to add an election, runner or new writ class.

## Checks and reproductions

`python3 tools/status.py` at `2026-10-31T07:01:21Z` reported prefix seq 151:
47 forecasts, four proposers, 19 resolutions, 12 world-typed resolutions
with evidence, no veto, no overdue forecast; procedure 90 : object 32 =
2.81 : 1. It also printed that criteria 1, 2, 3 and 5 require the tests run
on main. This output alone is not proof that all C1a criteria hold.

Requested count:

```sh
python3 -c "from judge.judge import counted_lines; import json; s=json.load(open('judge/scope.json')); print(counted_lines('.', 'HEAD', s['counted']))"
# 5998
python3 -c 'from judge.judge import counted_lines; print({p:counted_lines(".","HEAD",[p]) for p in ["tools/genesis.py","tests/test_genesis.py","sim/run.py","tools/vectors.py"]})'
# {'tools/genesis.py': 80, 'tests/test_genesis.py': 101, 'sim/run.py': 125, 'tools/vectors.py': 133}
```

F1 arithmetic, applying A4.3 with exact fractions to each candidate sequence:

```python
from fractions import Fraction as F
from functools import reduce
p = F(41, 100)
def wealth(ys):
    def step(a, y):
        E, s, n = a
        lam = max(F(0), (F(s + 1, n + 2) - p) / (p * (1 - p)))
        return E * (1 + lam * (y - p)), s + y, n + 1
    return float(reduce(step, ys, (F(1), 0, 0))[0])
print([wealth(ys) for ys in ([1]*6, [1]*5, [1]*6+[0], [1]*7)])
# [30.074527970162677, 14.385649212394481, 6.371722027576839, 64.18344383876182]
```

F4 renderer probe: synthetic entries, with the already-verified evidence
count supplied directly so the probe isolates rendering rather than hashing.
This is not a claim that these unsigned test dictionaries are a valid log.

```python
from tools.status import status, render
from tests.test_status import e
es = [e(0, "2026-10-25T00:00:00Z", "amend", "guy", id="A3", activate_at=1)]
es += [e(i+1, "2026-10-26T00:00:00Z", "forecast",
         ("counsel", "builder", "reviewer")[i%3], p=500,
         resolves_by="2026-11-01T00:00:00Z", type="world.x") for i in range(20)]
es += [e(i+21, "2026-10-27T00:00:00Z", "resolution", "herald",
         forecast=i+1, outcome=1, evidence="fixture") for i in range(10)]
es += [e(31, "2026-10-28T00:00:00Z", "decision", "guy", kind="veto", subject="C1a")]
s = status(es, "A3", 14, "2026-10-31T00:00:00Z")
s["world_resolutions_with_evidence"] = 10
text = render(s)
print(text)
print("SHORT-or-STOP guard refuses:", any(x in text for x in ("SHORT", "STOP")))
# criterion 6: veto on the subject: YES
# SHORT-or-STOP guard refuses: False
```

## second read

F1: partly
The collapse and one-repair rule are adopted, but F1–F2 above identify a prefix-wealth conflict and missing measurement inputs.

F2: answered

F3: answered

F4: answered

F5: partly
W2 and the pre-emptive cap increase are gone; the claimed dead test file also holds live digest coverage (F3).

F6: partly
The pre-signing refusal and local criterion-3 check are ordered, but SHORT/STOP must represent every unmet criterion, including veto (F4).

forecast: p = 0.40 that C1b's liveness reaches E >= 20 within 7 days of the
`decision promote C1a` that opens it (resolves_by 2026-11-30T00:00:00Z);
p = 0.25 that the clerk, its tests and pins fit under the cap of 6,200 with
no push (resolves_by 2026-11-21T00:00:00Z).

The first allows for six genuinely distinct timely discharge items after
opening, rather than six correlated forecasts from one batch. The second
prices the small headroom against seventeen pins, clerk tests, the status
extensions, the verb change and preservation of the live digest checks.
