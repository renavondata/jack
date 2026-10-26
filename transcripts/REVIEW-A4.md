# Cold read of Amendment A4 — PR #30

26 October 2026. Reader: OpenAI `openai/gpt-6-astra`, a different model family
from counsel. Reviewed branch `counsel-a4-text` at
`e05485735e91bde712e61e8bd01a49256f12ca35`. Attribution for Guy's commit:
`Proposer: reviewer reviewer-2`.

Read in the requested order: all of CHARTER (including A1–A3), SPEC §§7–10,
BRIEF-C1, AMEND-A4, PREDECESSORS-20261026, LITERATURE-20261026, COUNSEL-OPEN;
then the branch's log, seqs 0–61. References below are to those versions.
This is a text review, not an executed pin or an independent audit of the
predecessor repositories. No key was used. The only file produced is this review.

## Clause findings

### 1. Incumbents — UNENFORCEABLE

The distinction between an incumbent and a challenger is consistent with
CHARTER §0's entrants that can lose and §6's baseline tests. The universal
measurement claim is not implemented by the stated record:

> “Whatever is in force is an incumbent with a measured rate on the ledger”;
> its rate “is read from the log, never asserted.”

Safety replay is a property of the checkers running on adversarial logs, not a
rate recoverable from the accepted production entries. SPEC §9a puts that
evidence in the differential report. Liveness needs the obligation population,
deadlines and repair attribution; C1a's state does not contain those. A proper
score is a loss, not automatically a Bernoulli rate. No rule maps all the listed
incumbents, including a rule or a world, to a population, statistic and window.
The log's sole resolution so far, seq 52, resolves an assize CI forecast; it
does not supply these incumbent measurements.

**Layer:** a clerk could compute specified statistics from recorded observations;
a judge can verify referenced artifacts. Neither can derive the promised
universal rates from this text and log. No pin or explicit pricing treatment
for an unmeasured incumbent is named. This is more than delayed implementation:
the object of the required calculation is missing.

### 2. Challengers — CONTRADICTS

The forecast-first requirement fits prospective attribution and §2.1. The
claimed paired test conflicts with the statistical guarantee it invokes:

> A4.2: “the test is paired: the exponentiated cumulative difference of
> clipped log scores.”

> CHARTER §6: the specified process “is a non-negative supermartingale under
> H₀,” hence “P(supₜ Eₜ ≥ 1/α) ≤ α.”

An exponentiated score difference does not generally have that property under
the null of no improvement in conditional expected score. A concrete
counterexample is given in question (iii) below. Clipping makes increments
bounded; it does not supply the missing exponential compensation or change a
mean-score null into a likelihood-ratio null. The citations and literature
table do not specify such a construction.

The historical-rate alternative recognizes sampling uncertainty, but leaves
two further gaps. A confidence sequence for an old period does not establish
the new period's conditional baseline under drift. Also, if coverage failure
receives δ of a total α, the challenger test must use the remaining error
allocation for a total-α guarantee. “Its error pre-split from α” followed by
the unqualified threshold “1/α” does not distinguish the total from the
remaining allocation. Using the original α for both yields only an α + δ
bound by this argument.

There is also a substantive gate conflict:

> A4.2: “for a reversible incumbent … until one [EU rule] is elected the
> threshold is the same.”

> CHARTER §2.4: “Reversible acts are priced and scored, never blocked.”

A2.3 permits decidable proposal refusals costing only resubmission; it does
not by itself authorize withholding every reversible replacement until it
proves statistical superiority. A4 expressly purports to override earlier
text, so this is a change to that maxim, not a consequence of it.

**Layer:** forecast recognition and independent resolution are kernel checks;
scoring and deadlines belong outside the kernel, to the clerk. No sound,
fully specified comparison test or pin for the replacement threshold is
provided. The forecast-presence pins in clause 3 do not establish it.

### 3. Founding texts — UNENFORCEABLE

The trusted-base digest comparison is decidable from git and the log. A
properly identified unresolved forecast is also decidable. This part has an
explicit implementation boundary: **text-only until C1b's installing push**,
then **judge**, with `unforecast_push_admitted`; overdue handling belongs to
the **clerk**, for which `challenger_never_resolved` is named.

But “a text that founds a new core, repository, ladder or charter” has no
path, schema or other recognition predicate. A file can describe, propose,
quote or actually institute the same arrangement. Neither git nor a free-text
forecast distinguishes those cases mechanically. A2.3 requires judge grounds
“decidable from git and the log alone” and “over powers and paths”; the clause
does not meet that requirement for founding texts. It gives no price in place
of that undecidable-as-specified gate.

The stated mechanical gate is also weaker than clause 2: an unresolved
forecast can have no measurements or a losing wealth process and still open
the gate. Conversely, a challenger already resolved 1 can no longer satisfy
“unresolved” when its implementation is pushed. No ordering or binding of a
particular replacement digest to its winning forecast settles this seam.
The two named pins alone do not show that the incumbent can lose or that only
a winning replacement enters.

### 4. The sovereign is bound — UNFORCED

Equal attribution of the sovereign's ordinary acts is already supported by
§2.4, §7 and A2.6. The claimed empirical reason for this additional universal
founding gate is not established. In particular, the evidence does not trace
each of the six named predecessors through an owner's replacement decision
to a reason found only in its successor. Question (i) identifies the gaps.

COUNSEL-OPEN item 11 records a real defect: counsel caused unfiled repairs;
the log also contains resulting grants at seqs 48–49. That measurement does
not establish that all sovereign founding acts need this particular gate.
Seq 53 predicts jack's survival; it is not a measured comparison of foundations
or evidence that the proposed restriction improves it. The literature's final
paragraph explicitly calls owner-binding self-amendment “jack's own bets.”

**Layer limitation:** a `push` verb can refuse its own invocation, and the
judge can make an unauthorized in-repository change red. Neither controls
Guy's creation of a different repository or forces him to record it. SPEC
§10.11 supplies a self-check, not exclusive custody of every external founding
effect. Thus the proposed mechanism also does not establish the full reach
claimed by “a new repository … entered by him.”

### 5. The bootstrap, as a pin — UNENFORCEABLE

The liveness and forecast-value goals inherit §6, C1b and C2. The conjunction
is not a decidable exit from the specified log, for the reasons in question
(ii). Calling it “a pin” supplies neither a named mutant nor a passing twin.

Several extra conditions are unforced: an economically priced world, no
pending challenger anywhere, and zero counsel invitations in the last
window. The evidence contains no measured comparison supporting those vetoes.
One successful, externally scored arena is evidence for that arena, not a
measurement that all useful worlds must carry a price or market.

The counsel condition also sits against the existing generality requirement:

> A4.5: “counsel not invited in that window.”

> CHARTER §4: “rules quantify over entry types, never name a party.”

It excludes a named role regardless of its score, rather than demonstrating
that an election has learned to operate without repair. No bounded deadline
or escalation is assigned to this new bootstrap obligation if a conjunct
never becomes true (§2.3). C3's sealed-agent test is not expressly repealed;
this earlier bootstrap test therefore cannot itself certify C3 value.

**Layer:** the intended evaluator is the clerk, but no complete predicate,
named bootstrap pin, or price for unmet semantic conditions is given.

### 6. The price and lapse — UNENFORCEABLE

The two cited forecasts exist: seq 53 has p = 600 and seq 60 p = 500. Counting
A4 as the fourth amendment and continuing §12's procedure/object accounting
are consistent with A3.4. They do not define the proposed lapse test:

> “an e-process on its firing rate, against the rate clause 6 forecasts.”

Neither forecast gives a firing rate per opportunity. Seq 60 gives a 0.5
probability of **at least one** firing or citation by one calendar deadline;
seq 53 gives a 0.6 probability of continued foundation status. Neither defines
repeated trials, their denominator, their conditional null, or a post-C1b
population. A probability of any event in a horizon is not its per-item rate.

The direction also matters: §6's nonnegative λ construction tests for a rate
*above* p₀. Applied directly to firings, it would lapse a rule for firing
frequently, not for underperforming its forecast. No lower-tail construction
is stated. Non-firing alone also does not distinguish successful deterrence
from uselessness.

**Layer:** no kernel, judge or clerk can compute this lapse condition as
specified. Primary-rule admission/lapse machinery remains demand-gated by
A2.1; SPEC §7 says “no rule can be admitted.” The reference to §3 does not
provide its witnesses, notice procedure or an amendment-level removal act.
No lapse pin or alternative price closes these gaps.

### 7. Continued wealth and mechanical betting — UNENFORCEABLE

The continued-wealth correction is mathematically justified, and a
predictable bounded plug-in can be valid. The clause does not specify a unique
plug-in and truncation rule, however, so two implementations cannot derive
the same λ from its text alone. Details, including the distinction between
validity and power, appear in question (iv).

**Layer:** clerk/scoring code, never kernel (BRIEF-C1 refusal list). No pin is
named. Literature item 2 supports correcting restarts; item 5 supports
Laplace as a scoring reference, not a unique betting transformation or
truncation margin. The latter choices remain additional policy, not a
mechanical consequence of those citations.

### 8. Order of acts — HOLDS

The cold read follows A1.7's independent-review lesson and A2.4's authority
for layer review requirements. Transmutation before amendment, activation at
the next seq, and no intervening push agree with A2.7 and SPEC §§7, 10.12–13.
Default activation leaves no integer seq strictly between amend and activation;
a push at activation is consequently lawful.

**Layers:** the kernel checks amendment id uniqueness and a future activation
height; the judge checks transmutation, the freeze, charter hash and authorized
decisions. Clause 3's new grounds are expressly **text-only until C1b's
installing push**, with `unforecast_push_admitted` and
`challenger_never_resolved` promised there, killed with passing twins. This
sequencing holds; it does not make the substantive predicates in the preceding
clauses complete.

## The four specific questions

### (i) Does the predecessor evidence establish clause 4's factual claim?

**No.** The file's synthesis asserts the universal conclusion; the individual
entries do not demonstrate it. Its method is shallow clones, repository text
and `git log -1`, not a reconstruction of the owner's replacement decisions.

| Repository named in clause 4 | What the evidence actually establishes; what is missing |
|---|---|
| `credence` | An internal routing-collapse diagnosis, “Phase 1 should not start,” and “it is the user's call”; a later critique in `wald-charter`. It explicitly reports no in-repo abandonment statement, but supplies no owner's actual replacement decision. An invitation to decide is not that decision. |
| `life-agent` | A reset, prune, archived arc, inactive live-traffic exit and internal reasons for deleting its unified ledger. Its own ROADMAP swaps upstream engines; this is not evidence that life-agent itself was replaced, by whom, or with its reason only in a successor. |
| `proplang` | Repeated declared termini, reopenings and unfinished drafts. Adoption of its disciplines by tannen does not establish an owner's replacement decision or an exclusive successor-only reason. |
| `tannen` | M5's defective success criterion, an internal red-team finding and measured owner cost. No successor replacement decision is cited. |
| `wald` | Fourteen completed briefs/releases and author/builder separation. No retirement decision or successor's explanation is identified. The `wald-charter` and `wald-arena` sections do not fill that gap for wald either. |
| `assize` | The strongest case: owner wish #341, ending at the seal, and remaining content carried to jack. The file asserts the reason is in jack rather than assize, but does not quote the wish or establish that assize nowhere records the reason. It supports the owner decision, not the full “only in the successor” claim. |

Thus all six lack demonstration of at least one part of the conjunction;
the first five lack the explicit owner-replacement record shown for assize.
For the broader introductory claim about all predecessors, `credence-governor`
is particularly adverse evidence: the file quotes its failed waste bar,
demotion “because it blocked too often,” and retirement of shadow from its own
documents. That is an internal stopping account. The evidence supports
recurrent governance cost and some misleading exits, not the asserted
universal history.

### (ii) Is bootstrap decidable from log entries alone? Any extra constants?

**Not from the specified entries.** A signed resolution proves attribution,
not that an external mechanism actually determined the result or that the
world carries a market. Two external worlds can leave identical log entries
while only one satisfies that condition. The kernel expressly ignores
`forecast.type` and `args`; independent resolution checks principals, not
the provenance or truth of evidence.

The procedure/object count also depends on the world-type registry:
BRIEF-C1 says a type absent from `transcripts/world-types.md` does not count,
whatever its name. That file is outside the log. C1a has no invitation entry
or elected-action provenance; C1b/C2 have not yet specified the full records
needed for the election and no-repair predicates. No pending challenger is
checkable once challenger identity and resolution conventions are fixed,
but it can be kept false by repeated new challenges. “First reading” is
also a clock/observation event, not presently a recorded entry.

The inherited 20 is 1/α at 0.05; the window and p₀ are admitted parameters.
The 5 : 1 bound is already expressly in §12 and A3.4, even though it is not
in the question's five-item shorthand list. It is not newly smuggled in here.

New gates are **zero counsel invitations** and **zero pending challengers**;
“at least one” priced world and autonomous invitation are new existential
requirements. Their numeric form is simple but their veto power is real.
The price/market requirement is a categorical restriction, not a budget
amount. None follows from α, windows, p₀, attack list or budget. In particular,
a forecast that a priced world will be selected (seq 55) does not measure the
value of requiring one. There is no measured basis for the zero-counsel quota.

### (iii) Can clause 2 make the incumbent impossible to defeat?

**Yes, on its literal universal-rate reading.** Suppose the incumbent's
measurement is safety, scored 1 on every replay item, and its historical
confidence-sequence upper endpoint is 1. Under §6 with p₀ = 1, for every
possible challenger observation Y ∈ {0,1}:

    1 + λ(Y − 1) ≤ 1; therefore Eₜ ≤ E₀ = 1 < 20.

Even a perfect challenger cannot win. On a paired safety comparison two
perfect checkers tie forever. A useful replacement that preserves safety
while eliminating a repair or reducing cost remains inadmissible if safety
is the selected score. A4.1 explicitly includes the trusted base and safety;
the text gives no separate replacement route for this case.

**Mutant specification, not an implemented pin:**
`perfect_safety_incumbent_entrenched` changes the replacement selector to
return `keep_incumbent` for every candidate once the incumbent's safety
upper bound is 1. A fixture with a safe incumbent and a safe challenger that
removes a witnessed repair gets exactly the same outcome under the literal
clause. There is no passing promotion twin under that score. The inability
to kill this mutant exposes the green that cannot fail (§2.2), rather than
demonstrating protection of a genuinely superior incumbent.

There is a separate opposite defect: the specified paired test can promote
under its no-improvement null. Let Y be independent fair coin tosses, with
challenger probabilities 3/4 and incumbent probabilities 1/4, fixed in advance.
Their conditional expected log scores are equal. All probabilities are within
the existing per-mille range. For challenger-minus-incumbent log score D,
exp(D) is 3 or 1/3, each with probability 1/2, so:

    E[exp(D) | past] = (3 + 1/3)/2 = 5/3 > 1.

Three successive ones give wealth 27, crossing 20 with probability 1/8,
already greater than α = 0.05. Reversing the score sign just exchanges the
two outcomes. This is not an anytime-valid equal-score test. A likelihood
ratio would be valid under the different, stronger assumption that the
incumbent supplies the true conditional outcome distribution; equality of
expected scores does not imply that assumption.

### (iv) Is clause 7 a valid supermartingale construction? Extra constants?

**The continued-wealth principle is valid; the complete betting recipe is
not specified.** For 0 < p₀ < 1, a predictable λᵢ in [0, 1/p₀] gives
nonnegative factors and, under §6's conditional null,

    E[Eᵢ | Fᵢ₋₁]
      = Eᵢ₋₁ {1 + λᵢ(E[Yᵢ | Fᵢ₋₁] − p₀)} ≤ Eᵢ₋₁.

Continuing that wealth across windows preserves the bound, including with
predictable strategy changes, provided the same tested null still applies
to every new observation. Carrying a number forward does not justify
reusing it for a different estimand or a newly selected winning subsequence.
Alternatively, separate fresh processes with allocations αⱼ satisfying
Σαⱼ ≤ α control the union of crossings at thresholds 1/αⱼ. They need not
be independent. In that alternative each fresh process normally starts at
1; the literal “E is never set back to 1” is compatible only if it refers to
the same unsplit account, not to those separate allocated accounts.

The plug-in sentence leaves the following unresolved:

* Laplace gives a probability estimate q̂ᵢ = (sᵢ₋₁ + 1)/(nᵢ₋₁ + 2), not
  uniquely a betting fraction. Setting λᵢ = q̂ᵢ is one valid predictable
  interpretation; for interior p₀ it is already strictly inside the allowed
  interval. Mapping an estimated alternative probability to the Bernoulli
  log-optimal bet instead gives (q̂ᵢ − p₀)/(p₀(1 − p₀)). These differ, and
  the latter may be nonpositive. The text does not choose a map or precisely
  identify which observations contribute to s and n after a failed window.
* “Truncated strictly inside” gives no endpoints, margin or data-dependent
  rule. Clipping to an open interval is not a defined projection at its
  boundary. A fixed ε margin would be an additional constant outside the
  admitted list. A prefix-dependent margin could avoid a new tunable constant,
  but its rule is absent. An extra ε is therefore not mathematically
  inevitable; it is an unresolved implementation choice in this text.
* Laplace's unit pseudo-counts are fixed prior choices. They already appear
  in BRIEF-C1's base-rate scorer, but importing them into λ is a new betting
  policy, not a theorem from α or p₀. The error-allocation schedule for
  restarts is likewise unspecified, although it can fall within the admitted
  pre-statement of α and windows.

Strict interior bets avoid finite-time ruin from a zero factor; they do not
guarantee positive power against every alternative. Even a valid predictable
strategy can shrink wealth or fail to cross in its window. Finally, the
Bernoulli derivation above does not validate clause 2's raw exponential of
log-score differences. Those need their own null and construction.

## Disposition and forecast

The blockers are the invalid paired-test claim, the potentially undefeatable
incumbent, and substantive bootstrap/lapse/founding predicates without a
decidable specification. These are findings about the text as written, not
requests for a particular implementation or redraft.

Conditional on this text being amended as written, my probability that it is
cited or causes a refusal within 90 days of activation is **0.80**. The
text-only phase and broad trusted-base/founding scope make citation likely
even without a working statistical test. That forecast is not a probability
that the amendment improves the programme.

VERDICT: BLOCK — P(cited or refuses something within 90 days | amended as written) = 0.80
