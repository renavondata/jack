VERDICT: ACCEPT WITH OBLIGATIONS
Reviewed tree: c7443b34c4cd76728ff4993b39a3a6aabf50956d

# Amendment 1: cap 9,800 before the opening

Reviewer: `reviewer reviewer-2`; model `openai/gpt-6-astra`; 3 November 2026.
The header names the `origin/main` commit read, also this branch's starting
HEAD, after PR #207. It does not name my later review or ledger commits.
Read the amendment, its four operative locations, then REVIEW-C2b-v6
F21–F23 and its forecasts. Opening branch fetched and reviewed:
`b2dec5b498d77e1f6f7a5853af7c9eb55a0875d3` (`origin/push-c2b-9000`).

## 1. Lawful: a prospective resource budget

F24: Setting 9,800 now is lawful pre-statement, conditional on its installation by the sovereign's opening push and its subsequent freeze — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:238–262,278–285,310–311,352–362,397–426; CHARTER.md:102,272–282; SPEC.md:390–423; commands below.

CHARTER A2.4 says: "A layer's brief may pre-state criteria, bounds and review
rules for that layer" and "They bind that layer only, and may tighten the
charter's bounds, never loosen them." A2.6 says: "A change to the trusted
base is lawful only when a `push` entry names its digest". The brief says
"raised by the opening push; never again inside the window" and "two
trusted-base changes and no other". Amendment 1 is consistent with those
rules. This is a brief amendment, not a charter amendment or an already
effective change to `judge/scope.json`.

The observation prompting it is a public prerequisite's implementation cost
under C2a's existing cap. On this reviewed prefix there is no C2a promotion
and no C2b opening: the latest push is C2a's seq 367 (log.jsonl:368), and
the promotion entries are C1a and C1b (log.jsonl:189,338). The counted tree
still has cap 7,800. Learning from that prerequisite before committing the
next window's resource budget does not select a C2b threshold after seeing
C2b results. It cannot cure a C2a failure or authorize extra C2a lines. The
kernel bound remains 500; no charter bound is relaxed.

Executed, in order:

```sh
git fetch origin push-c2b-9000
git diff 606d276bf89946b1095dec6af8c49a04a9bebabb origin/push-c2b-9000 --stat
git diff 606d276bf89946b1095dec6af8c49a04a9bebabb origin/push-c2b-9000 -- judge/scope.json SPEC.md
python3 tools/status.py | grep 'criterion 3'
```

The stat was exactly:

```text
 SPEC.md                         |  4 ++--
 judge/scope.json                |  2 +-
 transcripts/PUSH-c2b-opening.md | 16 ++++++++++------
 3 files changed, 13 insertions(+), 9 deletions(-)
```

The trusted-file diff changes only cap 9000 → 9800 in scope and its SPEC
mirror, and SPEC's cap-history clause. The workflow has no delta against
`606d276`; thus the parallel workflow v6 read is retained, not a third
functional change. The note now withdraws the sample skip and run reuse,
discharging F21's stale-scope obligation; its forecast attribution needs
the correction in F25. SPEC's history changes with the opening push, not
as an ordinary trusted-file proposal.

The status command returned:

```text
criterion 3: counted 6882/6900; kernel 450/500; scope equals SPEC: True met
criterion 3: counted 7784/7800; kernel 450/500; scope equals SPEC and unchanged: True met
```

The first is historical C1b, not today's budget. The second leaves 16
lines under C2a, 1,216 under 9,000, and 2,016 under 9,800.

The cap enters the proposal admission bound (SPEC §10.10), C2b criterion 3,
and its stop rule. It is a resource constant, not a score parameter. A
count from 9,001 through 9,800 would satisfy the amended numerical bound
but not the old one: that changed future predicate is explicit. No loss,
gain, EXP3 parameter, propensity, value/liveness wealth, cutoff, deadline,
24-round requirement, existing witness or signed forecast is rewritten.
No new implementation witness follows merely from funding it. The opening
and exit still need every other prerequisite and criterion in F23.

F25: Preserve the actual forecasts and correct their misquotation in subsequent explanatory prose — severity: OBLIGATION — witness: transcripts/REVIEW-C2b-v6.md:184–200; log.jsonl:613,634,816 (seq 612,633,815); transcripts/BRIEF-C2b-draft.md:389–394,405–406,418–420; fetched SPEC.md:425 and transcripts/PUSH-c2b-opening.md's budget paragraph.

The v6 second forecast is **0.55**, confirmed by its signed entry at seq
633 (`p:550`). **0.40** belongs to v5's seq 612; v6 expressly raises that
estimate after withdrawal of the reuse contract. Amendment 1, its opening
note and SPEC history misattribute 0.40 to v6. This is an evidential
correction, not grounds to block a prospective cap. Counsel should record
the correction without editing any signed entry. Any later brief edit
still needs a read of its actual bytes under the gate.

The reviewer's seq 633 continues to require at most **9,000**, complete
functionality and coverage, a finished window by 30 November, and no
second in-window push; pre-opening corrections may count. Resolve it
against its own terms, including the exit-prefix count, not the new cap.
Counsel's **X6**, seq 815, is **0.45** for an exit-prefix count at most
9,000 with Amendment 1's 9,800 in force, due 18 November. Its narrower
count claim and earlier deadline are not the reviewer's delivery claim.
Neither becomes true merely because criterion 3 passes at 9,800.
X3 remains the separate no-second-push claim (0.7), not a count forecast.

The amendment's sentence that the cap does not make a sub-9,000 count
"more or less likely" is sound only as a statement that the old outcome
definition is unchanged. A larger permitted budget can affect builder
choices and hence the chance of that outcome. Existing probabilities stay
on the ledger; a new forecast prices the new claim rather than silently
revising an old one.

## 2. Sufficient, without spending the reserve by default

F26: Retain 9,800; my bottom-up allowance is about 1,495 new counted lines, with 521 lines of reserve — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:75–234,253–257,301–350,369–384; tools/clerk.py:20–88; tests/test_clerk.py:14–175; tests/test_push_gate.py:1–71; tools/status.py:229–329; SPEC.md:390–396; status output above.

These are estimates of incremental physical counted lines, including test
fixtures, imports and spacing, not measurements of unbuilt code. I assume
reuse of existing signature, ledger and test helpers and preservation of
existing coverage. Four instances share an implementation; they do not
require four copies of EXP3. I do not assume deleting existing coverage,
moving Python outside counted paths, or cramming statements to meet a cap.

| Deliverable | Additional counted lines | What the allowance includes |
|---|---:|---|
| `tools/due.py` | 105 | Fold, original-row integrity, inventory, canonical-body discharge, durable escalation history, rendering |
| `tests/test_due.py` | 95 | Valid/invalid discharge, due boundary, rewrite/deletion, inventory and late completion fixtures |
| `tests/test_workflow.py` | 65 | Five commands once, setup parity, unconditional gate, failed/skipped dependencies |
| Five W5 pins and workflow pin | 45 | Mutants/registrations; passing twins reuse the tests above |
| W5 status/tick integration | 15 | Output and evidence plumbing; evidence documents are not counted Python |
| **W5/workflow subtotal** | **325** | Counsel estimated about 250 |
| `tools/elect.py` | 360 | About 110 round/gain/deadline/instance lines, 110 arithmetic/signature/grid/replay lines, 90 invite/validation/routing lines, 50 CLI/table lines |
| `tests/test_elect.py` | 300 | Signed fixtures, exact endpoints/grid, replay tampering, partial/late rounds, waits/skips, identity and resolver routing |
| Two simulator kinds | 80 | `self_invite`, `rigged_election`, benign twins and generator integration |
| Remaining election/integration pins | 170 | Roughly twenty-two registrations/mutations, with twins shared with tests rather than counted twice |
| C2b `status.py` changes | 110 | Opening/end, all nine criteria, trusted-byte history, rounds/attack gate, W5 tick evidence, reports |
| `jack decision` dispatch | 10 | C2b dispatch and its promotion path |
| `value.py` exclusion | 10 | Procedure-type exclusion with existing process and wealth retained |
| Status/decision/value integration tests | 100 | Refused promotion, continuing wealth, window boundary and evidence failures |
| Counted diary/routing glue reserve | 30 | Any local Python bridge beyond election helpers; runner-side work is separate |
| **Election/integration subtotal** | **1,170** | Counsel estimated about 860 |
| **Total new counted lines** | **1,495** | **Projected full count: 9,279** |

The read gate and its three pins are already in 7,784 and are not charged
again. Session prompts, due rows, tick transcripts, RUNBOOK/report/brief
text and forecasts still require delivery but add no counted Python under
SPEC §10.10. The opening YAML is likewise outside that counted set.

Counsel's 250 + 860 = 1,110 leaves **106**, not "under a hundred", of the
1,216 available at 9,000. Also, the observed total rose by **134** from
7,650: the git stat from the v6 reviewed tree to this main is 136 insertions
and two deletions, not a net 138. The amendment's 120 and 18 should be
treated as approximate component densities, not reconciled net accounting.
The judge's actual 7,784 controls all headroom here.

My central estimate exceeds 9,000 by 279. At 9,800 the reserve is 521,
about 35% of the estimated new build, or 5.3% of the whole cap. It covers
the hard-to-price signed replay fixtures, historical W5 witnesses and
integration, rather than an extra feature. A stressed 1,900-line build
would total 9,684, leaving 116. This is a planning scenario, not a bound.
9,500 would leave only 221 over the central estimate; I would not choose
it for a window in which another trusted-base push is forbidden. I would
set **9,800**, not a different number, and would still target the smaller
implementation. No theorem uniquely yields 9,800: it is a justified
resource allowance, not a mathematical sufficiency certificate.

Obligation: measure the complete counted set at each delivery; build W5
and its workflow test first, retain all required mutants and twins, and
stop/report a shortfall rather than spend beyond 9,800. The reserve buys
implementation room, not permission for new features or relaxed criteria.

## 3. The opening gate

F27: This review is eligible evidence only after its identical bytes reach main through the reviewer's signed proposal — severity: OBLIGATION — witness: tools/jack:177–220; tests/test_push_gate.py:43–70; transcripts/BRIEF-C2b-draft.md:196–214; Reviewed tree header above.

`c7443b34c4cd76728ff4993b39a3a6aabf50956d` is the origin/main commit I read,
holding Amendment 1's brief bytes. This file's accepting first line and
header must travel on `review-c2b-am1` in a proposal signed by `reviewer-2`,
whose principal is reviewer, then merge onto main. A trailer alone does
not suffice. The gate checks that the adding commit belongs to that
proposal, the review blob remains identical, the reviewed commit is on
main, and its brief blob equals the current main brief. This read is not
a claim that the file has already merged or that C2a is lawful to promote.

**Anything else in Amendment 1 that stops the opening: none; the existing opening prerequisites, exact-blob read gate and two-change limit still bind.**

## One new forecast

forecast: **p = 0.70** that by **2026-11-30T00:00:00Z** C2b under this
Amendment 1 has opened and ended, its required W5, election, their tests,
workflow-preservation test, two simulator kinds, all pins, and
status/decision/value changes have landed on main during its window,
preserving required functionality and coverage, with the complete counted
set **at most 9,800 at the exit prefix** and **no second push inside the
window**. Read gate and opening workflow must also be present. A required
deliverable absent at exit, reduced functionality/coverage, count above
9,800, second in-window push, or no completed window by the deadline
resolves 0. Pre-opening corrections preserving these requirements may
count. Promotion is not required by this delivery forecast. Type
`review.forecast`; resolves_by `2026-11-30T00:00:00Z`;
args `{"model":"openai/gpt-6-astra"}`.

The extra headroom makes delivery credible; historical-evidence integration,
signed replay, the opening prerequisites and merge timing leave material
risk. This is a new 9,800 claim, not a replacement for seq 633's 9,000 claim.

Proposer: reviewer reviewer-2
