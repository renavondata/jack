VERDICT: ACCEPT WITH OBLIGATIONS

# Second read: BRIEF-C2a draft v2

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 1 November 2026.
Reviewed tree: `5d30c91`, after PR #87. Required texts read in the requested
order. Log evidence was selected by type/seq, not a whole-log dump. This is
a review of the text and its arithmetic, not a claim that the future pins or
implementation have passed.

The five blocking defects in v1 have been repaired in substance. No remaining
charter conflict requires a v3 before opening. The obligations below constrain
implementation, session evidence and the interpretation of the resulting
value claim; they are not additional promotion criteria.

## Findings and the six questions

F1: A4.4's statistic is preserved; no blocking addition, omission or renaming — severity: OBLIGATION — witness: CHARTER.md:354–360; transcripts/BRIEF-C2a-draft.md:73–91,118–141,218–223.

**Question 1: none, as a conflict with A4.4.** Clause by clause:

| A4.4 requirement | v2 |
|---|---|
| incumbent loss minus challenger loss, positive for challenger improvement | base loss minus aggregate loss, with exactly that sign |
| bounded by B = ln 999 under per-mille clipping | b explicitly clipped to [1/1000,999/1000]; q is a convex combination of probabilities in that interval, hence is clipped by construction; both outcome probabilities are bounded |
| product of 1 + λ D/B | same product, not the former likelihood ratio |
| min(max(0,m1/m2),1−1/(n+2)) | same rule and n counts prior scored events |
| two pseudo-items at +B and −B | retained: their normalized values are +1 and −1, contributing zero to the first-moment sum and two to the second-moment sum |
| λ predictable, in [0,1) | same, with no current outcome in the moments |
| under E[D_i \| past] ≤ 0, a test supermartingale | same conditional null and claim |
| exponentiated score difference not used as this test | printed only as a diagnostic; it gates nothing |

For x_i=D_i/B, positivity follows from 1+λ_i x_i ≥ 1−λ_i > 0;
conditional expectation is 1+(λ_i/B)E[D_i|past] ≤ 1. This is the required
argument, with no independence assumption. The binary64 implementation and
six-decimal display are added numerical conventions, not a replacement null.
Use unrounded arithmetic for decisions and weights; do not feed the printed
six-decimal rows back into the process. Test the clip on b as well as the
entrant path. The LR diagnostic is not itself evidence for promotion.

F2: The fixture follows the stated scoring arithmetic, including the three excluded forecasts and E = 1 — severity: OBLIGATION — witness: log.jsonl:97–106,228–249,252–299,300–325; transcripts/evidence/value-fixture-20261101.json:35–70,628–664,932–968; calculations below.

**Question 2: yes.** Counts below are `(s,n)`, not `(n,s)`. The base uses
every earlier resolution of the type; mixture weights update once per keyed
event. Those are deliberately different ledgers. In particular the second
resolution of race 1 changes the next base but does not update weights again.

Hand reconstruction:

* **261:** no earlier `world.renavon` resolution: `(s,n)=(0,0)`, b=1/2.
  Forecast 251 supplies reviewer p=1/5. The other four entrants use b;
  weights are all 1/5. Thus q=(1/5+4×1/2)/5=11/25 and Y=1 gives
  x=ln(22/25)/ln(999)=−0.01850845666405693. With no prior items,
  m1=0, m2=1, cap=1/2, λ=0 and E=1.
* **301:** earlier HKJC resolutions are
  `96:1,97:0,98:1,99:1,100:0,101:1,104:0,105:0,299:1,300:1`.
  Hence `(s,n)=(6,10)`, b=7/12. Forecasts 240 (counsel 1/4) and
  228 (reviewer 11/50) are used; builder, guy and base use 7/12.
  Y=0. The weights and their derivation are below. They give
  q=1777827743896729/3428747920370700=0.5185064009326527 and
  x=ln((1−q)/(5/12))/ln(999)=0.020936952363673347.
* **323:** start with the eight older resolutions above, `(4,8)`, and
  add both resolutions of each of M2 races 1–9. Their outcomes are
  `1,0,1,0,0,1,1,0,0`, four successes twice: `(s,n)=(12,26)`, b=13/28.
  The added seq pairs are `(299,300),(301,302),(303,304),(307,308),
  (309,310),(311,312),(315,316),(317,318),(321,322)`.
  Forecasts 248 (counsel 1/4) and 236 (reviewer 11/50) are used;
  the other three use 13/28. Y=0 gives
  q=465556277223067128664965551/1149033951561021100421363300
  =0.40517190687932697 and
  x=ln((1−q)/(15/28))/ln(999)=0.015154942968291844.

Here is an independently reconstructible route to the updated weights,
without using the fixture's rounded weights as inputs. Divide each entrant's
likelihood by the base entrant's likelihood; the common factor cancels when
normalizing. After the fifteen freshness events, reviewer and builder have
relative likelihoods R and U:

    R = (7/5^6) × (97/100)^3 × (16/13)
      = 6388711/12695312500
    U = (9/25)^3 × (47/50)^3 × (13/7)
      = 983930571/13671875000.

The first six base success probabilities telescope to 1/7. Builder's two
blocks telescope to 7/10 and 10/13; reviewer's last block to 13/16.
Abstention contributes relative likelihood 1. This derives R and U directly
from forecasts 251–258, 264–266, 272–274 and 280–282 and their resolutions.

At 301, normalize `(1/2, (11/25)R, U, 1, 1)` in the order
`(counsel, reviewer, builder, guy, base)`: race 1 contributes 1/2 to
counsel's relative likelihood and 11/25 to reviewer's.

At 323, the base's outcome likelihood over the first nine races is 77/65536.
Normalize

    ((1/4)^4(3/4)^5 / (77/65536),
     R(11/50)^3(47/200)(39/50)^5 / (77/65536), U, 1, 1).

The 47/200 is forecast 233 for race 7; omitting that exception gives the
wrong last-row weight. The first component simplifies to 243/308.

| before row | counsel | reviewer | builder | guy | base |
|---|---:|---:|---:|---:|---:|
| 261 | .200000 | .200000 | .200000 | .200000 | .200000 |
| 301 | .194387 | .000086 | .027979 | .388774 | .388774 |
| 323 | .275741 | .000108 | .025153 | .349499 | .349499 |

For the stake let S=sum(prior x), T=2+sum(prior x²); then m1/m2=S/T.

| row | prior events | S | T | m1 | m2 | cap | λ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 261 | 0 | 0 | 2 | 0 | 1 | 1/2 | 0 |
| 301 | 16 | −.096236319229 | 2.001774616969 | −.005346462179 | .111209700943 | 17/18 | 0 |
| 323 | 24 | −.080817047059 | 2.004720427409 | −.003108347964 | .077104631823 | 25/26 | 0 |

I also independently folded selected world forecasts and resolutions using
`Fraction` probabilities/weights, grouping by args, first pre-cutoff forecast
per principal, resolution-prefix counts, and binary64 logs. Comparison of
all 25 rows' counts, forecasts, weights, b, q, x, λ, factors and E against
the fixture at six decimals returned:

    rows 25 mismatches []
    sum_x_terminal -0.06566210409108257
    largest_nonempty_prior_sum -0.01850845666405693
    terminal_weights {'counsel': 0.347673, 'reviewer': 0.000142,
                      'builder': 0.022653, 'guy': 0.314766, 'base': 0.314766}

Thus every nonempty prior S is negative. The symmetric pseudo-items do not
create a negative numerator or a positive hurdle: λ is zero because S≤0,
not because the two pseudo-items require some positive minimum S. Their
effect is to enlarge the denominator when S becomes positive. Every factor
is exactly 1, so E=1 is honest, not a hidden reset or rounding artifact.

Seqs 288–290 have ts 04:54:00Z/05Z/09Z ≥ cutoff 04:00Z; they are also
later same-principal forecasts of the keys of 280–282. Both exclusion rules
apply; `rigged` is a valid diagnostic label. Their resolutions still belong
to C1's per-resolution base history, but create no additional C2 event.

The fixture explicitly waives the attack gate and uses the earlier opening;
its hourly historical sessions are illustrative keyed events, not proof of
compliance with the future three-hour diary. Do not apply that retrospective
fixture admission to live C2 wealth.

F3: The freshness outcome is a page-state predicate, not a reconstruction of an hourly run — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:38–52; log.jsonl:252,281,294–299; transcripts/COUNSEL-OPEN.md:30.

**Question 3, freshness:** at H+0:10 the specified outcome is
`displayed_last_updated >= H−1`. It remains a defined Bernoulli observation
on the saved page. It does not establish that new rows arrived in `[H−1,H)`.

* If no update occurred in that hour but one occurs in `[H,H+0:10]`, the
  predicate is 1: a false positive for the in-hour claim, not for the literal
  page predicate. An update exactly at H is already outside the half-open hour.
* If an update occurred inside the hour and another afterward overwrites its
  timestamp, the predicate is still 1. The outcome survives, but the page
  alone no longer proves when the earlier update occurred.
* A cached/stale page, delayed publication, a timestamp rollback, or differing
  timestamp semantics can report an older instant despite an in-hour update.
  Conversely metadata refresh without new rows can satisfy the page predicate.
* If the evidence is absent, there is no observed page predicate to resolve;
  the brief's disappearance/report rule applies. Choosing a later successful
  fetch after seeing an unsuccessful scheduled fetch would change the trial.

This is already visible on the record: resolution 293 uses a displayed
05:34Z instant for `[04:00,05:00)`, and 294–295 use 05:29:22Z. These satisfy
the literal lower-bound predicate; they do not establish the parenthetical
"the hourly run ... delivered new rows" in the older forecasts.

The ten-minute schedule reduces delay but does not logically eliminate these
cases. Preserve the explicit page predicate in session claims, save the
scheduled observation and its fetch time, and do not claim actual in-hour
delivery from it. The brief itself explicitly defines the observable at
lines 39–40, so this is not a reason to substitute another outcome or block
opening. H+0:10 forecasts `[H+2,H+3)` 1 h 50 min before its cutoff; it is
genuinely pre-outcome despite the prose's rounded "two hours".

F4: The event contract repairs the recorded selection/revision defect; pre-meeting kind declarations must preserve physical identity — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:34–72,108–114,207–215,229–235; log.jsonl:281–291.

**Question 3, identity and timing:** the six named datasets and scheduled
windows, and every meeting from the opening's saved fixture list, are chosen
before their outcomes. The earliest forecast per principal stands. A changed
claim string cannot create a new event with the same key, and the first
resolution settles it once. Standing forecasts need a cutoff after opening
and the attack gate. These are real repairs to v1, including its known-outcome
but not-yet-resolved witness.

A new, genuinely different race predicate such as `winner_at_20_plus`, named
and defined in the session issue before the meeting, is pre-outcome; it need
not have been individually named at opening when the brief pre-states this
extension rule. Dependence on another predicate of the race is not itself
duplicate counting or a violation of A4.4.

However a new label for `favourite_wins` is not a new physical trial. Listing
both `favourite_wins` and `shortest_final_WIN_odds_wins` before the meeting
does not license two factors for the same Bernoulli outcome. Nor does an
editable issue's present body prove what it said before the meeting.
Preserve the dated pre-meeting declaration and the meaning of each kind;
canonicalize aliases to the existing event or refuse the duplicate under
the already-written "no event scored twice" rule. The pin's "two keys two
events" must use two genuinely different events as its twin, not bless any
two arbitrary labels. A second resolution of the same event must never
change its outcome or add another factor.

Thus pre-statement is sufficient for the timing of a future race predicate,
not sufficient by itself for its identity or meaning. There is no lawful
exception here to the brief's explicit no-duplicates/no-known-outcome rules.
No new semantic kernel or general registry is called for; preserve and use
the small session contract. An implementation accepting aliases, forged
cutoffs, post-meeting issue edits or replacement forecasts would fail it.

F5: Six pre-stated datasets against the per-type base are lawful; the result has the scope of that comparator — severity: OBLIGATION — witness: CHARTER.md:98–102,345–360; transcripts/BRIEF-C2a-draft.md:41–47,73–79,130–134; transcripts/evidence/renavon-freshness-20261031-base.json:12–24,28,65,72.

**Question 4:** lawful, not a conflicting null chosen to lose. The base's
algorithm is pre-stated and unchanged: it pools the type, rather than being
retuned per dataset after the window. The alternative can use cadence as
information the comparator omits. §6 requires beating the base-rate
forecaster, not the strongest cadence-aware incumbent one could invent.
That makes the test potentially easy and its conclusion narrow; it does not
make it a test that cannot fail. Abstention or q=b throughout gives E=1.

The null is E[D_i|past]≤0, not "all six datasets have one true probability",
nor "the fitted Laplace rate is the truth". Online prefix updates of b are
the forecaster's stated algorithm; they are not estimating A4.2's fixed
binary liveness p0 from its test window. p0=6/11 remains separate.

The snapshot proves three last-updated instants, not that each dataset has
exactly one update every day. Cadence is a forecastable hypothesis, as the
brief acknowledges, and an incorrect cadence belief can lose. Report success
as value over this pooled comparator on these streams, not evidence of
general model superiority or of accurate hourly-run reconstruction.

F6: Resolution-prefix weighting restores the ln K bound and is compatible with the conditional null, including correlated outcomes — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:73–91,119–132; transcripts/REVIEW-C2a-v1.md:105–131; F2's calculations.

**Question 5:** yes, for the comparison now defined. Let L_k,t be entrant
k's product of outcome probabilities on the first t scored events, with
abstentions evaluated at that event's b. With uniform initial weights:

    w_k,t−1 = L_k,t−1 / sum_j L_j,t−1
    q_t(Y_t) = sum_k L_k,t / sum_k L_k,t−1
    product_t q_t(Y_t) = (1/K) sum_k L_k,t.

Hence loss_mix ≤ min_k loss_k + ln K. It is a bound, not a claim that actual
regret equals ln K. This is a pathwise identity; correlated datasets, races,
delayed forecast submission and adaptive abstention do not break it. The
failure in v1 was using earlier frozen weights, not correlation.

Both b and q now consume the same resolution prefix. Earlier correlated
outcomes may help both. A4.4 conditions on that past, so independence is not
needed and its conditional expectation proof still applies. Do not describe
the aggregate as a probability actually issued before the physical event:
it is a sequential, resolution-order comparator of pre-cutoff entrant
forecasts. The identity remains valid even on an arbitrary realized order;
the test claim additionally requires its stated conditional null for that
order. It does not turn post-outcome selection of events, labels or evidence
into prequential forecasting. Session completeness and the no-selection
contract must be preserved, not replaced by the algebra.

F7: Remaining implementation duties are witnessed and achievable; no new mandatory machinery or weaker exit was found — severity: OBLIGATION — witness: transcripts/PLAN-20261030.md:33–62,92–94; transcripts/BRIEF-C2a-draft.md:11–21,92–116,139–141,176–250; transcripts/REPLY-REVIEW-C2a-v1.md:18–23.

**Question 6: none** as an unforced new C2a mechanism or remaining BLOCK.
Weighting has the freshness losing-record witness; cutoff/revision handling
has seqs 288–290; status and the aggregate implement the charter's existing
tests. Six data sources and a different session clock are prospective
experimental choices, not a new law language or orchestration framework.
The CI skip, automatic re-proposal, bridge and election action are explicitly
assigned to C2b. No new code for them is required here.

Implementation obligations retained from the first read:

* Authorize 7,800 before opening; this is a budget, not a fitted score
  constant. The headroom is 918 counted lines over 6,882. A shortfall fails
  the window rather than licensing an in-window push.
* Continue the entire value calculation over retries: prior x's and stake
  state as well as E. Keep entrant likelihood history for the continuing
  aggregate; do not infer a fresh uniform prior from a retry's opening.
  The proposed admission of a newly granted principal at a subsequent window
  must be reconciled with the continuing statistic and its stated bound,
  not silently treated as another first opening. This is not a reset needed
  to open the first window.
* Keep C1b history distinct from live continued liveness, including projected
  expiries, repairs, evidence verification and exit-prefix checks. Actually
  dispatch `decision promote C2a` to its complete verdict. Missing evidence
  must not become success. Keep all §6/A5 gates, not value alone.
* Implement `factor_algebra` with a genuine distinguishing witness. The
  true-probability-b tree has E[D]=−KL(b||q)≤0 and is a valid subcase of the
  null, not a proof of the whole composite null. Include an equality node
  (q=b, including abstention): the added 1/50 mutant then has expectation
  1.02 and must fail. On general rational b,q the logarithms are not rational;
  an "exact" oracle needs symbolic identities/certified inequalities or
  specially chosen exact cases, rather than asserting that binary64 is
  exact. There is no impossibility: e.g. clipped opposite endpoints give
  D/B=±1, and q=b gives zero exactly. Use the general proof in F1 alongside
  these implementation checks.

The numbered exit retains safety, continued liveness ≥20, value ≥20,
no veto and the tighter brief obligations. Removing the live-loser gate
does not weaken §6: a deliberately manufactured loser was never its value
test. The unchanged whole-CI path also removes v1's evidence-preservation
uncertainty. No amendment to A4.4 and no replacement fixture are needed.

## First read

| finding in REVIEW-C2a-v1 | disposition |
|---|---|
| F1 | answered |
| F2 | answered |
| F3 | answered |
| F4 | answered |
| F5 | answered |
| F6 | answered |
| F7 | answered |
| F8 | answered |
| F9 | partly |
| F10 | answered |
| F11 | answered |

F9: the replacement pins have feasible witnesses, but `factor_algebra` still
owes its exact finite oracle and distinguishing equality case; see F7 above.

"Answered" means the text supplies the correction or assigns the obligation;
it does not certify future implementation, session evidence or successful CI.

## Forecasts

forecast: **p = 0.30** that C2a's window under BRIEF-C2a draft v2 ends in
promotion rather than failure: every pre-stated criterion holds on the exit
prefix by V0's original `resolves_by`. A purported promotion missing a
criterion is failure. Resolve 0 if v2 is superseded without such a window;
a later revised window is not v2 success. Ledger type `review.forecast`,
`resolves_by = 2026-12-15T00:00:00Z`.

forecast: **p = 0.55** that by `2026-11-21T00:00:00Z` the required C2a
`tools/value.py`, its tests and pins are delivered with the complete counted
set at or below 7,800, preserving required coverage, and no second push
inside the window. Incomplete or shortened scope and failure to deliver by
that date resolve 0. Ledger type `review.forecast`,
`resolves_by = 2026-11-21T00:00:00Z`.

The first rises sharply from v1's 0.01 because the legal statistic and timing
are now coherent. Heterogeneous cadences can provide useful differences
against a pooled base, but implementation time, actual forecast quality,
complete observations and all exit gates still matter. The second rises
from 0.20 because the budget grew and the CI change was removed; eighteen
pins, two simulator kinds and status/decision integration still compete for
918 lines. Neither probability treats this illustrative E=1 as a failed
live window: the first C2a window has not opened.
