VERDICT: BLOCK

# First read: BRIEF-C2b draft v1

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 2 November 2026.
Reviewed tree: `195415beaf6c3ce83d9755a8476a1b4605aafdfc` (after PR #114).
The requested texts were read in order. This is a text review, with numerical
and constructive witnesses, not certification of unbuilt tests or pins.

## Inherited state

`python3 tools/status.py` on this tree, as of `2026-11-02T05:11:48Z`, reports:

    counted 7650/7800; kernel 450/500; scope equals SPEC and unchanged: True
    criterion 4: attack green on main before first scored cutoff: unverified SHORT
    value: E 1.000000 over 0 events; window events 0
    liveness continued: E 1 over 0 items (including projected expiries)
    J7: 6 of 35 window forecasts unresolved past resolves_by
    promote C2a: refused: [unverified tests/attack evidence, value, liveness,
                          and missing off-log acts evidence]

The six overdue forecasts are 442–447, due `2026-11-02T05:00:00Z`.
The requested command

    python3 tools/value.py --table --attack-green 2026-11-01T15:59:44Z | head -40

reports 24 events; its first row is resolution 389, b=19/20, reviewer
p=49/50, q=.956, D/B=.000912, lambda=0. A second invocation with the same
arguments, projecting the JSON summary, reports:

    events 24; E_value 1.231747
    terminal_weights:
      guy .000002, counsel .000002, reviewer .999994,
      builder .000001, base .000002

The explicit attack-green input is an assumption supplied to that computation,
not independent verification of a CI run. The default status's missing
evidence is not proof that the historical promotions were unlawful or that
the actual wealth reset. C2b inherits a continuing ledger and unresolved
evidence duties, not an established current promotion verdict. The proposed
8,400 cap supplies **750** lines over this counted tree.

## Findings

F1: Forecast power for the clerk is lawful after the sovereign's grant; no new kernel type is required merely to carry an invitation — severity: OBLIGATION — witness: CHARTER.md:87–90,258–262,308–312; SPEC.md:101–106,193–212; log.jsonl:202; transcripts/BRIEF-C2b-draft.md:7–12,19–22,89–96; transcripts/PLAN-20261030.md:33–52.

**Question 1: none as a charter prohibition on clerk forecasting.** Choosing
and forecasting an invitation judges merit, not entry validity, and grants
no change power. The checker still adjudicates the signed `forecast` entry.
The herald sentence is explicitly introduced as **“Proposed default, Guy's
to decide”**, not an immutable ban on a later key declaration. The record
already has `herald-2` with `merge`, not `accept`/`wish`. SPEC §7 expressly
allows redeclaration of its powers. A valid sovereign grant of
`merge,forecast` therefore suffices; without it an invitation forecast is
`no_power`, and no window satisfying the stated preconditions has opened.

C2a's scope did promise a kernel change. It is a recorded deliverable, not
an amendment requiring speculative types regardless of need. C2b can
expressly revise that allocation before opening; record the deferral and
resolve any forecast of delivery honestly. The exact “codify ... never ...
in anticipation” instruction is PLAN §4, reinforced by CHARTER §4's
precedent row and A2.1/A3.1. It is not a verbatim sentence of CHARTER §4.
Deferring unused types respects that rule. This does not cure the invitation
probability or event-contract defects below.

The opening command in v1:91 is shorthand, not currently executable as
printed: RUNBOOK.md:59–64 and `tools/jack`:107–117 also require `--principal`
and `--pubkey`. Supply the existing herald principal and public key in the
sovereign's actual paste; do not create another identity. No new power is
needed in the kernel's type vocabulary.

F2: The stated EXP3 gain is not in [0,1]; ln 999 bounds a loss difference, not the absolute loss used here — severity: BLOCK (brief: “gain *gₖ,ₜ* = 1 − ℓ(*qₖ,ₜ*, *Yₜ*)/*B* ∈ [0, 1]”; criterion 1: “Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.”) — witness: transcripts/BRIEF-C2b-draft.md:41–48,132–133; CHARTER.md:354–360; numerical command below.

**Question 2: not EXP3 with its stated guarantee as written.** For a legal
per-mille forecast p=.001 and outcome 1:

    python3 -c 'import math; print(math.log(1000)); print(1-math.log(1000)/math.log(999))'
    6.907755278982137
    -0.000144858238875889

This is a conforming clipped forecast, yet `gain_bounded` fails before its
unclipped mutant is introduced. The small size of the violation is irrelevant
to the claimed interval. Two derived repairs are available: divide the
absolute loss by ln 1000, or retain B=ln 999 and use

    gain = (ln 1000 - loss) / ln 999.

The latter maps the legal loss endpoints [-ln .999, ln 1000] to [1,0].
Neither is permission to change **A4.4's** B or its value statistic.

There are six forecasts per freshness invitation. Define the election's
round loss, e.g. the mean of the six clipped losses, before normalizing it;
a six-loss sum divided by a single-event bound is not bounded either. State
what happens on a missing forecast, partial session or missing evidence,
without discarding a bad round. Endpoint losses give a rejecting witness;
the corrected normalized endpoints and an interior loss give passing twins.

F3: A fixed maximum horizon is lawful, but a public clock-seeded, delayed-feedback, growing-roster policy does not have the unqualified EXP3 guarantee claimed — severity: BLOCK (brief: “The regret bound is 2√((e − 1) *g K* ln *K*) against the best single entrant in hindsight.”; “A new entrant enters with Ĝ = 0 (the uniform share)”) — witness: transcripts/BRIEF-C2b-draft.md:36–59,63–64; CHARTER.md:376–384; transcripts/BRIEF-C2a-draft.md:269–277.

For the usual fixed-K EXP3 with bounded round gains, unbiased estimates
`1{I_t=k} gain_k,t / p_k,t`, and appropriate feedback timing, the standard
expected weak-regret bound is

    (e-1) gamma G_max + K ln K / gamma.

Choosing gamma as in v1 using a known upper bound g >= G_max gives the
advertised square-root bound (with the trivial bound covering the clipped
gamma=1 case). Since gains are at most one, an upper bound T_max on the
number of rounds is sufficient. **336 can be such a bound** for one
invitation per future hourly freshness window in at most fourteen days.
Early promotion only reduces the number of rounds; it does not make this
choice unlawful. Name g as an upper bound on cumulative gain/round count,
not the actual number that must occur. Derive it from the actual deadline
and eligible slots, and define a separate round count for HKJC; races,
meetings and freshness hours are not interchangeable rounds. A retry that
continues the election beyond its stated horizon also needs treatment.

A horizon-free method is **not required by A5**. Doubling or another
properly specified anytime version may give a better short-prefix guarantee.
EXP3.P is a high-probability variant, not automatically horizon-free merely
by name. The charter does not require either particular replacement.

The remaining defects are independent of early stopping:

* **Randomness:** seeding solely with public W0 makes the choice deterministic
  conditional on the prefix and the time. The actual conditional choice
  probability is then 0 or 1, not the displayed p_k. An adaptive environment
  can compute that choice, give the selected arm gain 0 and all other arms
  gain 1 before the round. The algorithm earns 0; some fixed arm earns at
  least T(1-1/K). For K=3,T=336 this is at least 224, exceeding the claimed
  bound 87.242818. Even an oblivious sequence can be constructed by simulating
  the completely deterministic policy in advance. Replayability is not a
  substitute for EXP3's randomness/non-anticipation assumptions. Specify a
  random draw and its recorded replay evidence, with outcomes not chosen
  using the unrevealed draw, or stop claiming the EXP3 theorem for this policy.
* **Delayed feedback:** at :20 a session forecasts [H+2,H+3), but the next
  hourly invitation occurs before those six outcomes resolve. Updating only
  from available resolutions is lawful; it is not the immediate-feedback
  theorem without a delay argument. Pre-state the update order and saved
  selection propensity, and give the bound for that protocol (or change the
  protocol). Never importance-weight an old gain using today's p_k.
* **Changing arms:** the theorem just quoted is for a specified fixed roster.
  “At least one resolved forecast” excludes an unseen model from K, while
  the exploration floor applies only to arms already in K. It cannot by
  itself admit `gpt-6-astra-fast`. Declare prospective eligibility/entry time
  and a finite roster or a valid changing-roster rule. If existing weights
  are 9 and 1, adding an arm with exp(eta*0)=1 gives weight share 1/11,
  not the uniform 1/3. The exploration component is uniform; the whole
  distribution is not. Correct that named quantity and pin its real meaning.

The standard e-1, eta=gamma/K and K ln K terms are theorem-derived, not
hand-tuned constants. The problems are their assumptions and the wrong gain
bound, not the mere existence of constants. Coverage is probabilistic, not
a promise of a switch or quick recovery. Evaluate it on a low-weight entrant
that starts forecasting well; do not reset the principal mixture to help it.

F4: The invitation's p names a selection propensity and defines it as confidence in a different event — severity: BLOCK (brief: “whose claim is that the invited entrant's log-loss on the window it is invited to beats the base rate's”; “`p` = *pₖ,ₜ* in per mille (the election's own probability of its choice: a proper-scored statement of how confident the record is)”; CHARTER §4: “a forecast under a strictly proper score”) — witness: transcripts/BRIEF-C2b-draft.md:7–9,54–62,104–106; SPEC.md:101–106.

P(select k | past) is not P(loss_k < loss_base | past, selected k). Suppose
two equally weighted entrants always forecast identically and beat the base
on an entirely predictable stream. Each can have selection probability 1/2,
while each success event has probability 1. Conversely, both can always tie
the base: selection is still 1/2 and success probability is 0. Scoring 1/2
against either success event is numerically possible, but does not score the
quantity the election computed. Strict propriety of log-loss does not supply
the missing probability model.

Keep selection propensity as replay/update data and separately specify an
entrant that forecasts the binary success claim, or explicitly define and
justify the forecast mapping without calling the quantities identical.
Forecasting the selection **after drawing it** would instead predict an
already-known event and violate the refusal list. Also define rounding and
clipping to 1–999 for the signed probability: K=1 has selection p=1, which
cannot be signed as 1000. The probability used for importance weighting must
be the actual sampling probability, not silently its rounded forecast field.

F5: Adaptive choice from prior scores does not by itself break C2a's conditional-null test — severity: OBLIGATION — witness: CHARTER.md:354–360; transcripts/BRIEF-C2a-draft.md:64–91,118–141; transcripts/REVIEW-C2a-am2.md:32–59,61–97; transcripts/BRIEF-C2b-draft.md:49–53.

**Question 3: none as a selection-induced failure of A4.4.** The election
changes the actual q_i by changing which principal supplies a forecast.
“Mixture untouched” means its algorithm/history are unchanged, not that its
future output is invariant to participation.

Construct two possible prefixes: A has performed better on one, B on the
other. Choose the next forecaster from that prefix, before its scheduled
event, and let all others abstain at b_i. If its continuing principal weight
is w_A, q_i = w_A p_A + (1-w_A)b_i when A is selected; similarly for B.
The resolved-prefix weights, available forecasts, selection and lambda_i
belong to the conditioning information before scoring Y_i. Under the
**actual** null E[D_i | F_(i-1)] <= 0,

    E[E_i | F_(i-1)]
      = E_(i-1) (1 + lambda_i E[D_i | F_(i-1)] / B)
      <= E_(i-1).

No independence or unchanged marginal event distribution is required. For
an explicit benign case, take fair next outcomes, b=.5, and two possible
selected forecasts .75 and .25; either convex mixture with the abstainers
has expected D <= 0. Selecting by past results preserves that inequality.
Selecting .75 **after** seeing Y=1 and .25 after Y=0 instead yields a positive
D on every trial: that is the forbidden post-outcome construction, not the
proposed past-only allocation. Keep the schedule, all six observations and
pre-outcome forecasts; never use a later successful page fetch in place of
the scheduled one (REVIEW-C2a-v2 F3).

The value-process argument does not validate F3's separate bandit-regret
claim. Nor does it prove recovery: a new model under a near-zero principal
weight still has near-zero mixture influence. Preserve all original
likelihoods, differences, stake state and wealth; measure recovery rather
than asserting it from the exploration floor alone.

F6: Procedure cutoffs either exclude their own forecasts or admit already-known outcomes; the herald also has no place in the unchanged C2a roster — severity: BLOCK (brief: “no event or invite chosen after its outcome is known”; “no change to C2a's statistic, mixture or clerk”; C2a: “A forecast whose `ts` is at or after the event's cutoff is listed as `rigged` and not used”) — witness: transcripts/BRIEF-C2b-draft.md:74–79,100–106,149–153; transcripts/BRIEF-C2a-draft.md:64–72,139–141; tools/value.py:44–50,74–80,96–111; transcripts/REVIEW-C2a-v1.md:48–103.

**Question 6:** own-ts cutoff plus the inherited strict-before rule excludes
every `counsel.programme`, `review.forecast` and `election.invite` forecast:
ts >= cutoff holds at equality. Permitting equality does not solve the
epistemic defect. A reviewer can enter “the already published tests run R
passed” at 12:00, with a future resolution deadline and a new args.id; a
counsel forecast can similarly predict an act already recorded at 11:00.
Both satisfy the proposed identity/own-ts recipe. An unentered resolution
is not an unknown outcome. Paraphrasing the claim or changing args.id can
also duplicate the same physical outcome.

Proposal entry time fares no better as a universal cutoff. A branch's tests
can already have run before a new proposal entry; `jack proposal` itself
runs the local check before signing (`tools/jack`:120–125). A counted-line
claim about an already-fixed commit is mechanically knowable before proposal.
Both can pass ts < proposal.ts after the relevant outcome is known.
The pin that rejects only **after-proposal** forecasts cannot kill these
cases. Use a future uncertain event with a real pre-outcome boundary and
stable identity, or leave such forecasts in C1's reported scores and out of
the promotion statistic. Give each supported procedure predicate its actual
contract; a broad type name does not provide one.

An invite can have a genuinely future outcome if fixed before its session
and scheduled physical windows. Use that boundary, not its own ts. Its
resolution is a function of six events, so pre-state the batch, completeness,
settlement and base-rate convention. Resolve once, not again under aliases.

There is another literal incompatibility: C2a's fixed roster is guy,
counsel, reviewer, builder and base. `herald` gains forecast power only at
C2b's opening. Keeping that mixture untouched rejects herald's forecast as
`not in opening roster`; on an invite-only event all original entrants
abstain, q=b and D=0. It does **not** make the election a scored mixture
entrant as v1:105–106 promises. Rebuilding a uniform roster at C2b would
discard the accumulated likelihood history, contrary to the inherited
continuation duty (REVIEW-C2a-v2 F7). Specify a lawful prospective treatment
of this new forecaster, with its actual bound, or report invites separately.

Adding genuinely pre-registered future event families to the same bounded-D
product need not reset wealth or spend another alpha. A4.4 works for the
actual conditional null across types. Retain the full C2a prefix and add
only eligible post-opening/attack-green events; no retrospective procedure
backfill, new uniform prior, discarded differences or product restart.
F6 blocks the proposed contracts and incompatible entrant promise, **not**
the abstract possibility of extending one ledger prospectively.

F7: The read gate and W5 have feasible mutant/twin witnesses, but they need provenance and completeness; W4 measures a different set from recommendations — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:65–73,127–128,142–146; transcripts/COUNSEL-OPEN.md:3–6,22–25,28–32; CHARTER.md:41–44,248,291–300; RUNBOOK.md:118–119.

**Question 4:** none of these predicates is inherently incapable of failing.
These are concrete tests the reviewer should require before claiming the
gates are witnessed:

| Predicate/mutant | Rejecting witness | Passing twin |
|---|---|---|
| push without read / always pushes | no matching REVIEW on main | independent ACCEPT or ACCEPT WITH OBLIGATIONS for this brief's exact bytes |
| read of this text / any REVIEW counts | reviewed commit holds previous brief bytes | same commit reference with the matching bytes |
| W5 / overdue never escalates | a present unfinished row with due < now | same row before due, or valid completion before due |
| recommendation forecast / unmatched acts ignored | sovereign act with no qualifying forecast | act with the corresponding prior counsel forecast |

An **empty review file does not satisfy** the proposed gate: it has neither
a Reviewed-tree commit nor a verdict. It satisfies today's weaker
`push --review FILE` hash requirement, which expressly accepts empty files;
the new check must actually be run, not inferred from that hash. Require an
explicit accepted verdict, a resolvable commit and an independently authored
review, rather than treating “missing verdict” as “not BLOCK”. A counsel
file with two fabricated headers is not the independent read CHARTER A1.7
requires, even if byte equality is true. This gate establishes provenance
and freshness of a read, not correctness of its legal reasoning.

W5 over zero rows has no overdue rows. However, v1 **also expressly requires**
migrating counsel's dated COUNSEL-OPEN obligations at opening. An empty file
while those duties exist is noncompliance, not lawful satisfaction of the
whole brief. Make completeness testable against a fixed opening inventory;
validate `done` against the named act and log seq, and preserve rows/history.
A bare non-null integer or deleting an overdue row must not discharge a
promise. Include those mutants; the current overdue-row mutant alone misses
them. Preserve escalation history when reporting timeliness: completing an
overdue item does not prove that it was escalated on time.

Finally W4's “sovereign acts ... with no counsel forecast” is only a proxy
for COUNSEL-OPEN 13's “every recommendation ... enters as a forecast”. A
recommendation that the sovereign declines has no act to scan, so disappears;
an unsolicited sovereign act creates a false positive. A forecast entered
after the act can also name it unless timing is checked. These witnesses
show the pin can pass while a recommendation remains unscored. Preserve the
standing recommendation-entry rule, link its prospective forecast to the
requested act, and report unmatched acts under their honest name; do not
claim W4 alone codifies all recommendations. Off-log advice still needs the
existing recording discipline. This is an enforcement obligation, not a
claim that every decidable proxy must solve semantic advice detection.

The opening's own read gate must already exist when that push is attempted.
V1's step 3 builds gates after step 2 opens. Pre-land the ordinary tool change
or explicitly arrange the opening preflight; later code cannot retroactively
be the check that refused an earlier push. Keep this separate from the
sovereign's authority to authorize the cap.

F8: A change of invited entrant is a gameable exercise witness, not §6 value; 24 is an unexplained exercise quota — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:123–126,146–147; transcripts/REVIEW-C2a-v1.md:228–243; transcripts/BRIEF-C2a-draft.md:200–203; CHARTER.md:94–104,272–274,376–381.

**Question 5:** an entrant can deliberately forecast badly, reduce its
weight, and make another entrant more likely on a subsequent draw. With
known draws it may even target that change; exploration can also change the
invite without any evidence of relative skill. A switch is therefore not
proof that the election improved anything. It is not automatically produced
by one bad forecast, either: the actual next draw may select the same arm.

A reproducible trace selecting A repeatedly fails; the same valid fixture
with a later draw selecting B passes. This kills `always true` and shows
nonvacuity, exactly the distinction REVIEW-C2a-v1 F7 made. “At least one
change” belongs naturally with witnessed implementation/coverage obligations,
not with the charter's statistical success tests. If retained as a numbered
criterion, A2.4 permits that tightening and A5 makes it binding at exit;
neither a switch nor 24 sessions substitutes for value/liveness >=20.

There is no derivation of **24** in v1. One day of hourly sessions explains
its units, not a statistical coverage bound. For K=3,g=336, the nominal
floor is about .025185 per arm; with valid fresh randomized draws a floor-
only bound on missing an arm for 24 rounds is (1-.025185)^24, about .542.
Thus 24 does not guarantee even one visit to each arm. State it as a
sovereign-authorized exercise budget, justify it from a coverage objective,
or move it to a reported obligation. As a workload quota, like the line
budget, it is not an unexplained constant **inside a score**; I do not invent
a charter prohibition on all finite exercise counts. Every invite's timely
resolution is independently meaningful and can fail.

F9: Electing the builder while keeping the builder as sole event resolver commands a self-judgement the kernel refuses — severity: BLOCK (SPEC §7: “A `resolution` whose `proposer` equals the recorded proposer of its `forecast` is **self_judged**”; CHARTER A3.3: “No party resolves its own forecast, judged by principal, not by key”) — witness: SPEC.md:228–233; CHARTER.md:318–320; transcripts/BRIEF-C2b-draft.md:36–38,60–64; transcripts/BRIEF-C2a-draft.md:271–278.

The builder is an eligible arm with positive exploration probability. When
chosen it signs the six world forecasts as principal builder. The unchanged
Amendment-2 stream assigns their resolution to builder. The kernel must
refuse those six resolutions, regardless of whether another model or another
builder key resolves them. Resolving the herald-authored **invite** as builder
is lawful; it does not resolve the six world entries or relieve W1. A passing
twin assigns those world resolutions to reviewer/counsel, a different
principal, with the same evidence. Pre-state resolver routing conditional
on the elected principal before opening; do not remove the builder from
coverage silently or evade principal-based self-judgement.

Also define the base arm's executable action: the base has no signing key
or model session, and C2a's b is computed at resolution, not invitation.
Specify how a base selection is recorded and resolved (including its strict
comparison tie), rather than dispatching a nonexistent principal or signing
a future resolution-prefix rate in advance. Define HKJC's unit and routing
too: “HKJC ... as C2a” retains two forecasters per race, whereas v1's bandit
justification says only the invited entrant forecasts. Extra observations
can be ignored for a specified bandit update; they cannot be silently
importance-weighted as if sampled by that update.

F10: The machinery has recorded witnesses; preserve the full exit and close the implementation gaps before a lawful opening — severity: OBLIGATION — witness: transcripts/PLAN-20261030.md:33–64,92–94; transcripts/COUNSEL-OPEN.md:22–32; transcripts/REVIEW-C2a-am2.md:90–97; transcripts/BRIEF-C2b-draft.md:80–98,108–168.

**Question 7, unforced new machinery: none independently requiring BLOCK.**
The losing/concentrated record witnesses election and recovery; the model
routing record witnesses model-level allocation; overdue promises witness
W5; the forbidden C2a-v1 statistic and its cold read witness requiring a
current read. Procedure identity/cutoff failures have explicit earlier
witnesses. These warrant small mechanisms, not their particular defective
definitions. Deferring a new law language, kernel types or a CI shortcut is
consistent with PLAN §4. Existing recorder/identity commitments in
COUNSEL-OPEN 15–20 still need an explicit disposition in the report; absence
from C2b is not evidence that they were delivered.

The numerical exit keeps safety, continued value >=20, continued liveness
>=20 and no veto. I found no deliberate lower numeric substitute for §6.
Implement the full exit verdict, including escalation failures, evidence
verification and all pre-stated criteria; the `decision promote` verb must
consume that verdict. Resolving every invite eventually is weaker than
resolving by deadline, and checking only outstanding W5 rows is weaker than
retaining escalation history. Use deliberately bad traces plus good twins,
not a historical fixture that cannot exercise the new behavior.

The attack replay must reconstruct weights and eligibility from the signed
**prefix**, then compare args: accepting a consistent draw from forged
args.weights proves only self-consistency. Equal timestamps need seq-order
handling. An invite after the session but before W0, an invite omitted from
the counting inventory, and procedure events admitted before their tests
are green each need distinguishing witnesses. `mixture_untouched` on the old
fixture is necessary but cannot establish continuation across the C2b
boundary: test carried likelihoods, prior differences and wealth there too.

**Before opening, v2 must repair F2, F3, F4, F6 and F9.** In particular:
derive the actual normalized session gain and correct the bandit guarantee;
separate selection probabilities from success predictions; supply genuine
prospective procedure contracts and a consistent treatment of herald;
route resolution away from the forecaster. F1/F5/F7/F8/F10 remain obligations,
not excuses to open with those conflicts. A correct forecast grant alone
cannot repair them, and implementation must not silently choose which
contradictory sentence to honor. No brief bytes were edited in this review.

## Forecasts

forecast: **p = 0.01** that C2b's window under BRIEF-C2b draft v1 ends in
promotion rather than failure: every pre-stated criterion holds on the exit
prefix by that window's end. Resolve 0 if v1 is superseded without such a
window, if no such window has promoted by `2026-12-31T00:00:00Z`, or if a
purported promotion lacks a criterion; a revised window's promotion does
not count as v1 success. Ledger type `review.forecast`,
`resolves_by = 2026-12-31T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

forecast: **p = 0.35** that by `2026-11-30T00:00:00Z` C2b's required
`tools/elect.py`, gates, tests and pins are delivered with the complete
counted set at or below 8,400, preserving required coverage, and its window
has ended with no second push inside it. Pre-opening corrections of this
review's defects may count; dropping required functionality/coverage,
failure to deliver, an unfinished window at that date, or a second in-window
push resolves 0. Ledger type `review.forecast`,
`resolves_by = 2026-11-30T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

The first probability reflects actual specification conflicts, not pessimism
about the continuing stream. The second allows a corrected pre-opening text
but prices only 750 lines of headroom for election, replay, gates, contracts,
status integration and meaningful tests/pins. It is not conditional on the
first forecast succeeding.
