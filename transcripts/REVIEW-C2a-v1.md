VERDICT: BLOCK

# First read: BRIEF-C2a draft v1

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 1 November 2026.
Read against `7c1384e`, brief `transcripts/BRIEF-C2a-draft.md` v1. References
below are to that tree. No brief or code changed. The required texts were read
in the requested order; log inspection used selected entries, not a whole-log
dump. In this checkout canonical JSON has no spaces: the requested
`grep -n '"seq": 288,' log.jsonl` returns nothing; the matching form is
`rg -n '"seq":288,' log.jsonl` (line 289).

## Findings

F1: The likelihood ratio tests a different null from the charter's mandated comparison — severity: BLOCK (CHARTER A4.4: "Comparisons of two forecasters are bets on a bounded difference." and "An exponentiated sum of score differences is not one under that null and is not used.") — witness: CHARTER.md:354–360; transcripts/BRIEF-C2a-draft.md:65–76,116.

The mathematical claim, suitably qualified, is true. Let F(i−1) include all
information used to select the event, select/abstain, choose its probability,
and order its settlement. If q_i and b_i are measurable there, 0 < b_i < 1,
and P(Y_i=1 | F(i−1)) = b_i, then

    E[q_i(Y_i)/b_i(Y_i) | F(i−1)]
      = b_i q_i/b_i + (1−b_i)(1−q_i)/(1−b_i) = 1.

The product starting at 1 is a nonnegative test martingale. Independence is
unnecessary; the *conditional* null is necessary. An earlier-frozen q is fine.
Estimating b from strictly earlier outcomes is also fine for this particular
point null; that fact does not establish that the conditional null is true.

It is not A4.4's test of E[D_i | past] ≤ 0, where D is base loss minus
aggregate loss. Concrete one-step witness: b=1/2, q=3/4, true success
probability 3/5. Expected D = (3/5)ln(3/2)+(2/5)ln(1/2) =
−0.03397980735907949, but the expected LR factor is 11/10. Thus the aggregate
can be worse in expected log-loss while this factor fails the required
supermartingale inequality. Calling rejection of the point null rejection of
"the aggregate knows nothing the base rate does not" changes the claim being
certified. A realised positive log-loss difference is not the missing
anytime-valid test under the charter's null.

A2.4 allows tightening, not replacing this requirement with a different null.
Use A4.4 for promotion, with its bounded comparator made explicit, or obtain
an amendment before opening. In particular, unbounded-history exact Laplace
rates need not stay in [1/1000,999/1000]; do not silently apply B=ln(999) to
them. C1's reported scores need not be changed to define a bounded promotion
comparison. The sign-win alternative at v1:75 is not the mandated A4.4 test
either. This is an existing-law conflict, not a preference between tests.

F2: Resolution timestamps and literal claim strings do not prevent known-outcome selection or repeated evidence — severity: BLOCK (brief refusal: "no event scored twice" and "no event chosen after its outcome is known"; CHARTER §6: "Liveness and value are tested by betting e-processes") — witness: transcripts/BRIEF-C2a-draft.md:32–47,104–108,138–142; transcripts/COUNSEL-OPEN.md:30; log.jsonl:289–291 (seqs 288–290).

The four requested adversaries have different answers:

* **Selective abstention:** predictable abstention alone does not break the
  proof. Its factor is 1 if it uses the same b, and a predictable choice
  between two normalized forecasts still has conditional expectation 1.
  However, freezing at the first forecast rather than before outcome
  availability allows a party to inspect Y, forecast 900 on successes, and
  abstain on failures. With b=1/2 the expected factor is
  (1/2)(9/5)+(1/2)(1)=7/5. That is a selection failure, not a counterexample to
  the correctly conditioned theorem.
* **Different wording:** one physical Bernoulli outcome can be entered as A
  and paraphrase B, both at 900, and both resolved to that same outcome.
  Literal grouping treats these as two events. Starting at Laplace 1/2,
  after A the base for B is 2/3 on success and 1/3 on failure. The two-factor
  product has expectation (1/2)(9/5)(27/20)+(1/2)(1/5)(3/20)=123/100.
  Once A is known B is deterministic, not a draw from that Laplace rate.
  No independence assumption fixes counting the same revealed fact again.
* **Earlier forecast than another proposer's "first":** the earliest
  forecast of the grouped event must win, regardless of whose record a loop
  visits first. A forecast at 09:00 fixes it before another party's 10:00
  forecast; the latter cannot change q. A subsequently appended 09:00
  entry after a 10:00 entry is already refused by `ts_decreased`; the real
  ambiguity is cutoff interpretation, not lawful backdating. Define the
  inclusive first entry and seq tie-break. The pin's literal "before its
  first forecast's ts" excludes even that first forecast; all earlier
  forecasts of that event are absent by definition.
* **Standing forecast fixed at opening:** authorship of the old record
  alone is not self-judgement. Using only legitimately available information
  to forecast an unresolved future outcome is permissible. But an
  unresolved *entry* may concern an already public outcome. The author can
  help choose the opening/weights after seeing that outcome, then lodge its
  resolution after the push. Fixing q at opening does not make that wager
  pre-outcome. Require a previously committed pre-outcome prediction and
  event eligibility, not merely a later resolution entry.

The recorded freshness case is sharper than a hypothetical: seq 288's ts is
04:54:00Z for the window [04:00,05:00), with 980 per mille; seqs 289–290 follow
at 04:54:05Z and 04:54:09Z. COUNSEL-OPEN 21 says the run had finished and the
page may already have shown its result. These first forecasts would pass
both proposed temporal pins when their resolutions are entered later. The
record establishes the vulnerability, not proof that this forecaster
actually inspected those outcomes. A satisfying twin forecasts the next
unstarted hour. A rejecting witness forecasts after the public result is
available but before the resolution entry.

Literal strings also collapse *different* events: seqs 198 and 202 have the
same `proposal.ci` claim, "the tests workflow is green on the first run of
this branch's proposal head", but belong to different proposals. Their
forecast ts values are 13:08:23Z and 13:54:50Z. Conversely the four cap claims
153/165/171/177 use different wording for closely related outcomes. Neither
string equality nor type alone defines a physical trial. State stable event
identity, the pre-outcome cutoff, resolution/duplicate handling and settlement
order before opening. This requires a witnessed event contract, not a new
kernel language or an LLM that guesses semantic equivalence.

F3: The stated aggregate lacks the Bayes-mixture regret identity under its own delayed forecasts — severity: BLOCK (CHARTER §2.2: "The law looks forward and never commands the impossible"; brief: "with η = 1 the mixture's cumulative log-loss is within ln K of the best entrant's") — witness: transcripts/BRIEF-C2a-draft.md:26–39; the overlapping first freshness forecasts at log.jsonl:252–254 (seqs 251–253).

For a fixed K, synchronized sequential predictions and updates, uniform
Bayes weights give mixture likelihood (1/K) sum_k L_k and hence regret at
most ln K. Uniform is the minimax prior for this worst-entrant bound:
min_pi max_k ln(1/pi_k)=ln K. Eta=1 gives the likelihood telescoping identity;
it is not an unexplained tuning parameter.

But v1 freezes q when events are first forecast, while previous outstanding
events have not resolved. The ordinary sequential identity no longer holds.
Even granting that all entrant forecasts are available at fixation, consider
the five entrants: four principals forecast .9,.1,.1,.1 on each
of two events opened before either settles, and the base entrant at fixation
is .5. Both mixture predictions are .34. On two successes regret to the .9
entrant is 2 ln(.9/.34)=1.9468982914282074 > ln(5)=1.6094379124341003.
These are valid per-mille probabilities. The example concerns the advertised
regret guarantee, independently of F1's null question.

There is a second timing conflict: an absent entrant cannot both use the
later resolution-prefix b_i as its probability and contribute that number
to an aggregate frozen before intervening resolutions. A model that issues
a probability at opening is not a forecaster that later substitutes a new
Laplace value. Distinguish forecast-time and settlement-time base rates and
state which one each operation uses. Freeze the roster/prior too, or state
how new grants and revocations preserve the bound. A delayed-feedback
aggregate can be defined, but it needs its actual bound; future weights
cannot be substituted to recover ln K.

F4: The worked table is reproducible only with unstated rules, and its explanation reverses the cap bets — severity: BLOCK (brief criterion 1: "Every pin below KILLED with a passing twin"; brief refusal: "no change to C1's statistics or the clerk"; CHARTER §4: "each satisfying witness passes the law in force plus its rule") — witness: BRIEF-C1.md:103–111; transcripts/BRIEF-C2a-draft.md:78–96,124–126,140; log.jsonl entries listed below.

I selected resolutions through seq 268 with:

    rg '"seq":([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-5][0-9]|26[0-8]),.*"type":"resolution"' log.jsonl

Projected output is 34 resolutions. Their forecast seqs are
45,46,47,73,74,75,83,84,85,76,86,56,38,121,114,115,118,123,127,
37,39,40,41,117,122,198,202,153,165,171,177,251,252,253.
Reading only those forecasts gives 29 literal `(type,claim)` groups. Counts:

| type | resolutions | literal events |
|---|---:|---:|
| world.assize | 4 | 4 |
| world.hkjc | 8 | 4 |
| counsel.programme | 8 | 8 |
| proposal.ci | 3 | 2 |
| free | 4 | 4 |
| review.forecast | 4 | 4 |
| world.renavon | 3 | 3 |

Compute one Laplace update per *group*, order groups by first resolution,
include **all** resolved forecasts in a group even if later than its first
forecast, impute the group's base for abstainers, and average terminal entrant
LRs with uniform weights. That gives:

| entrant | LR | normalized terminal weight |
|---|---:|---:|
| counsel | 7.340015 | 0.573400 |
| builder | 2.422500 | 0.189245 |
| guy | 1.680000 | 0.131241 |
| reviewer | 0.358353 | 0.027994 |
| base | 1.000000 | 0.078120 |
| arithmetic mean of the five LRs | 2.560174 | — |

This explains the printed table; it does not implement v1. C1 updates per
*resolution*, pooled across proposers, not once per claim. For example the
first paired HKJC claim's base is 1/2 for forecast 73 at resolution 96, then
3/5 for forecast 83 at resolution 99. The corresponding paired rates are
(2/3,2/3), (1/2,4/7), (5/8,5/9); proposal forecasts 198/202 have (2/3,3/4).
Using those C1 per-forecast rates gives counsel LR 7.829349 and reviewer LR
0.209039, not the fixture. Even assigning each group its *first* C1 rate
gives 7.829349 and 0.382243. The fixture needs the unannounced event-level
update.

Reviewer forecasts 83–86 were entered roughly 96 minutes after counsel's
73–76. Including them in the table contradicts the first-forecast cutoff;
the table's 2.56 additionally uses the terminal-average identity F3 shows
cannot generally be substituted for the product of frozen predictions.
The text's "eight events" of `world.hkjc` are eight resolutions, four literal
events. Finally cap forecasts 153/165/171/177 had p=.25,.25,.20,.25 and all
resolved 0: their type-specific LR product is 27/16=1.6875. They *increased*
the reviewer's relative weight. The three .20 freshness successes give
.4 × .3 × (4/15)=.032, which actually hurts it.

Do not tune the implementation until this fixture passes. Publish the exact
event rows, cutoffs, b, q and accumulated products for a corrected fixture,
with its rounding rule. Either explicitly define a distinct C2 base or retain
C1's; calling the former the latter leaves no conforming twin for
`worked_table` plus the other requirements.

F5: The restart instruction omits continued value wealth and literally scores only the new window — severity: BLOCK (CHARTER A4.1: "A window that fails and is followed by a new one continues the same wealth process on the same statistic under the same null; E is never set back to 1 and no α is split.") — witness: CHARTER.md:342–344; transcripts/BRIEF-C2a-draft.md:48–52,66–69,98–101,116.

Starting the first C2 value process at 1 is lawful. Continuing C1b liveness
from 214358881/8398080 is also right. However, v1 explicitly starts a new
window on budget failure while criterion 5 tests value "on the window's
events" and the product includes events "resolved in the window". Applying
that definition on the next window discards the failed window's factors.
Specify one value ledger from the first C2 opening, with wealth and update
state retained over failures. A window-only diagnostic can remain a separate
reported quantity. Do not turn a changed null/statistic into an implicit
fresh alpha allowance; such a change needs its lawful treatment stated.

F6: The four named constants are not an independent ground to block; the budget is lawful when authorized before opening — severity: OBLIGATION — witness: CHARTER.md:102,108,272–274,345–347; transcripts/BRIEF-C1b-draft.md:35–44,123–134,270–276; transcripts/BRIEF-C2a-draft.md:26–30,48–59.

* Uniform prior and η=1 have the exact minimax/telescoping justification in
  F3, under its assumptions. They pass scores through a specified algorithm,
  not a hand-tuned smoothing constant. The invalid application of the bound
  is F3, not a demand for a different numerical eta.
* 20 is the charter's pre-stated 1/α at α=.05, not a fitted threshold.
* p0=6/11 is a committed incumbent-prefix measurement, conservatively kept
  over the 5/11 replay under the final attribution rule. It is not estimated
  from C2a and belongs to continued **liveness**, not the value LR.
* 7,300 is a pre-stated resource budget, not a derived statistical bound.
  Against 6,882 it supplies 418 counted lines. A2.4 permits a layer's own
  bounds; §7 assigns the budget to Guy. Counsel can propose it; the sovereign
  must authorize the opening push. It does not enter score arithmetic.

The premise that C1b's 6,200→6,900 push was unlawful is not supported by the
standing brief/report: C1b expressly allowed a push *after measured shortfall*,
and Amendment 1 recorded it. It lost the no-push forecasts. C2a can pre-state
a stricter no-second-push rule without retroactively condemning that act.
Neither an early budget nor a missing rationale for the last 400 lines is
an unadmitted score constant. F1/F3 must still be fixed independently.

F7: Criterion 7 is gameable, but it is not a green that cannot fail — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:118–119,133; CHARTER.md:42,96–102,243.

An entrant can deliberately choose a very bad forecast and lose weight;
e.g. p=.999 on a predictable failure against b=.5 yields LR=.002. Criterion
7 then passes without discovering a previously unknown bad proposer. But a
trace with everyone abstaining, or every forecast equal to the base, leaves
all weights tied and must fail. That is a concrete kill for the named
`always true` mutant; the losing trace is its passing twin. Thus "can choose
to satisfy" is not "cannot fail". The check provides a demotion demonstration,
not statistical evidence of aggregate value, and cannot substitute for §6.

It is an extra brief criterion (hence binding under A5 while numbered there),
not one of §6's three success tests. Prefer a witnessed implementation
obligation or explicitly say why a live loser must gate promotion. It is not
an independent BLOCK. Citation correction: A1.4 in this charter is the
genesis/required-checks clause; the nonvacuity maxim is §2.2 and its §4 rows.

F8: The CI skip changes the evidence behind admission; it needs an explicit preserved-coverage contract — severity: OBLIGATION — witness: .github/workflows/tests.yml:20–29; harness/diff.py:24–38,45–54; judge/selfcheck.py:14–26; tools/jack:133–162; tools/clerk.py:44–50; tools/status.py:180–201,226–241.

Today `tests` runs unit tests, pins, current-head self-check through both
checkers, and the synthetic/vector differential sample. `jack merge` waits
for both checks on the proposal head and again on the merge-entry head.
W3 examines the run metadata for the commit the merge entry names; it does
not inspect which steps ran. Status likewise treats successful `tests.yml`
metadata as evidence for criteria 1/2. Green after a skip is therefore not
automatically the same witness as green today.

Skipping only the deterministic synthetic/vector sample can preserve the
substantive evidence if a successful run covers the identical complete input
tree (both checkers/binary, generator, seeds, harness, vectors and relevant
execution configuration), while unit tests, pins and both-checker replay of
the **new log** still run. The sample command does not consume `log.jsonl`;
the self-check does. A log-only last commit is not sufficient: it may sit
above changed simulation/scorer/pin code whose earlier run failed or never
ran. Missing evidence must run the sample or refuse, never inherit green.

At the second merge-entry head there is a useful candidate antecedent: the
first head whose CI the verb already awaited. Specify and verify that link,
including the push-to-main evidence needed by promotion; do not generalize
"only the last diff is log" into coverage of the entire proposal. Name a
mutant which skips after a failing/absent or input-mismatched antecedent and
a passing twin with a verified identical-input run plus fresh-log replay.

This is a trusted-base/admission-evidence change, not merely an operational
cost claim (§8's system-that-works-before-next-layer requirement applies).
The authorized opening push is the right channel under A2.6. No blanket
charter prohibition on reusing unchanged deterministic evidence was found;
the future implementation, not yet present, must establish preservation.
The phrase "two trusted-base changes" should identify cap and CI skip.

F9: Twelve named pins have straightforward distinguishing witnesses; two cannot yet certify what v1 claims — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:123–135; F1–F4 above.

These are feasibility assessments, not claims that unbuilt pins were run.
Each row gives the conforming twin and how the named mutant is killed:

| pin | twin / distinguishing witness |
|---|---|
| worked_table | **Blocked as written by F4.** A corrected row-by-row oracle can distinguish Laplace +1/+2 from +1/+3 on the first outcome. Specify the mutant's numerator/denominator, not just its initial decimal. |
| fixed_before_resolution | Keep q unchanged when an intervening resolution changes weights; the resolution-time mutant changes q. Also test first-entry inclusion, equal-ts seq ties, earlier proposer, and overlapping events. F2/F3 must define the target first. |
| rigged | Pre-outcome forecast admitted, post-resolution forecast excluded; including the latter is killed. Add the actual recorded post-outcome/pre-resolution witness: the currently named mutant alone misses it. |
| abstention_is_base | Use an absent principal on a type with base 2/3, not 1/2; the half-imputation mutant differs. Fix the time at which that base is taken (F3). |
| grouping_by_claim | Same identified event with two principals counts once; double counting changes wealth. Add different-event/same-words and same-event/different-words twins per F2. |
| grouping_by_principal | Two declared keys for one principal leave one weight, not two; a genuinely different principal has a separate weight. The kernel prevents self-resolution, not two forecasts from two keys of one principal; the scorer owns this collapse. |
| uniform_prior | Equal opening weights including base; doubling counsel's makes the first deliberately unequal forecast vector produce a different q. |
| no_learning_rate | Unequal post-outcome likelihoods yield different weights at η=1 and η=1/2. A sequential fixture tests that rule, not the false delayed-feedback guarantee. |
| exact_fractions | A non-dyadic value such as 1/3 must remain a Fraction through the factor/product path; a float division fails exact value/type assertions. A four-decimal display-only comparison will not kill it. |
| per_type_base | Two datasets of one type share counts, while a different type starts fresh; a per-dataset reset disagrees. Define whether counts are resolutions or events first. |
| martingale | **Unspecified.** No horizon, sample size, tolerance, seed list or concrete biased-factor mutant is stated. See below. |
| elections_witnessed | All equal/abstaining refuses; one strict loser passes. Always-true is killed on the equal trace. |
| window_from_the_push | Event between merge and push excluded; event after push included. Include same-ts seq boundary and an explicitly eligible standing event; do not reset across retries (F5). |
| promote_refused_value | Supply every other criterion and verified evidence: value below 20 signs nothing, value at 20 signs. Otherwise another failure could mask the mutant. |

For `martingale`, "within the bound" currently names no bound at all. A
finite random seed mean cannot certify expectation 1 or reliably distinguish
every expectation 1+epsilon. With fresh seeds it can reject a correct
implementation or accept a biased one; with fixed seeds it is repeatable but
can still encode either error. The size of the product grows with horizon
and inverse base rates, so a concentration tolerance also needs those bounds.
Committing selected seeds after observing outcomes would not repair this.

A deterministic replacement is available without a tuning tolerance: at each
node of a small enumerated binary tree check exactly
b*f(1)+(1−b)*f(0)=1 for the stated point-null LR, and the appropriate ≤1
condition for the actual promotion process. Name a concrete mutant (e.g. an
extra factor 2), and retain the legal normalized twin. Use exact branch
probabilities and include adaptive abstention. This tests implementation
algebra, while the proof and F1 establish which null it covers. If Monte
Carlo remains, pre-state seeds, horizon, sample count, bound and error budget
before running it; it remains a limited regression check, not the theorem.

F10: The status/decision extension must preserve every current refusal, and cannot rely on its present C1b dispatch — severity: OBLIGATION — witness: tools/status.py:30–36,55–104,122–138,214–263,303,340–356; tools/jack:200–225; transcripts/BRIEF-C2a-draft.md:62–63,110–121,149–152.

`python3 tools/status.py` returned `promote C1b: refused`, E=1, items=0,
with unverified run/attack and unknown acts evidence. It did not show that
C1b really failed. Running the report's evidence-bearing command:

    python3 tools/status.py --as-of 2026-11-01T11:31:58Z --runs transcripts/evidence/runs-tests-20261101b.json --acts transcripts/evidence/acts-20261101.csv

returned `promote C1b: lawful`, nine items,
E=214358881/8398080, counted 6882/6900, kernel 450/500, off-log repairs 0,
ratio 67:82, and attack green at 2026-10-31T13:32:21Z. Thus the inheritance
has an actual verified prefix; keep its missing-evidence-is-unverified rule.

At present `v_decision` explicitly refuses any promote subject except C1a
and C1b, the status parser has the same choices, and historical C1b status
ends at seq 337. Extending these is ordinary in-scope tools work, not an
impossible command or a reason for a second trusted-base push. But merely
adding a printed C2a line is insufficient: the verb must dispatch C2a and
read that exact verdict; liveness must include subsequent items and projected
expiries, rather than freeze the already-green C1b exit forever. Retain the
entire prior item/stake history, evidence validation, late-reported-repair
refusal, veto and promotion-entry ratio projection. Keep historical C1b
assessment separate from the live C2a calculation.

Opening identification must use a named push/seq, with an explicit same-ts
tie rule, and V0 must be entered before it with its one immutable deadline.
The attack gate must precede eligible live observations, not merely delayed
execution of a scorer on already-known observations. Missing authority or
evidence must still prevent signing. Pin these inherited paths alongside
`promote_refused_value`; otherwise a value-only pin does not establish all of
A5's criteria. No need to widen genesis-only decision authority in C2a.

F11: The core scorer is witnessed; optional new orchestration needs its own recorded scope, and a table is not yet an invitation policy — severity: OBLIGATION — witness: transcripts/PLAN-20261030.md:33–52,54–62,92–94; REPORT.md:483–500; transcripts/COUNSEL-OPEN.md:26–32; transcripts/BRIEF-C2a-draft.md:21–54,149–152.

There is a real losing-record witness for weighting: the reviewer's first
freshness predictions, not the four cap bets. §6 already requires aggregate
value, and §8/A3 names election by record. `value.py`, exact accounting,
status and their tests are justified by those witnesses. The rigged case is
recorded; principal-based grouping is a small guard against double weights,
not grounds to build new identity machinery. No independently blocking
unforced machinery was found in those deliverables.

Do not treat a terminal weight table as an implemented choice of the next
proposer/model. PLAN §5 currently requires that choice by record to be
written in the invitation; C2a must say what consumes weights, or explicitly
carry the remaining election action to C2b. The log does not even record
model identity today (COUNSEL-OPEN 22). Do not infer model performance from
principal performance. This is a scope/claim obligation, not permission to
invent `invite`/`accept` semantics before their amendment.

Automatic re-proposal and clerk-to-issue dispatch have witnesses (six stale
closures, idle counsel) in the C1b report, which calls them C2a items. They
are absent from v1's deliverables and 418-line budget account. Assign them
explicitly rather than silently loading them into this build. The opening
CI optimization has the PLAN calendar entry but still owes F8's preservation
witness. The budget mismatch between hourly freshness here and three-hourly
from 2 November in COUNSEL-OPEN 23 should be settled before opening; it
changes power/cadence, not a law of probability. No broad new procedure is
needed to resolve these points.

## What must change before opening

F1–F5 are the blockers: a charter-compatible promotion statistic (or an
effective amendment); genuinely pre-outcome, uniquely identified events;
one coherent forecast/update timing rule with its actual aggregate bound;
a conforming worked fixture; and continued value wealth over failures.
Those changes must be settled in text before the builder is asked to make
the pins pass. F6–F11 specify implementation/review obligations and factual
corrections, not additional charter vetoes. In particular neither the
pre-opening 7,300 budget nor a deliberately losing entrant alone is a BLOCK.

## Forecasts

forecast: **p = 0.01** that C2a's window ends in promotion rather than failure
under BRIEF-C2a draft v1: every criterion holds on the exit prefix by V0's
original `resolves_by`. A purported promotion lacking those criteria is not
success; a later version's successful window is not v1's success. Resolve 0
if v1 is superseded without such a window. Ledger type `review.forecast`,
`resolves_by = 2026-12-15T00:00:00Z`.

forecast: **p = 0.20** that by `2026-11-21T00:00:00Z` the required C2a
`tools/value.py`, tests and pins are delivered with the complete counted
set at or below 7,300, preserving required coverage, and with no second
push inside the window. Count a shortened or incomplete implementation as
failure, not a budget success; failure to deliver by that date resolves 0.
Ledger type `review.forecast`, `resolves_by = 2026-11-21T00:00:00Z`.

The first probability reflects the text conflicts, not pessimism about
whether these streams are predictable. The second reflects the 418-line
headroom for scorer, tests, fourteen pins, two simulator kinds and the
status/decision integration; there is no measured implementation shortfall
yet.
