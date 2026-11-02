VERDICT: BLOCK
Reviewed tree: c712c035090d6f5381500bda9bbf356c48fe0113

# Third read: BRIEF-C2b draft v3

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 2 November 2026.
This is `origin/main` after PR #124. I read REVIEW-C2b-v2, the reply, and the
whole v3 brief in that order, then checked the specified charter and SPEC
sections, REVIEW-C2a-v1 F8, the current workflow and its consumers. References
are to this tree. This is a text review, not certification of unbuilt pins.

**The window cannot open under these exact bytes.** The two new workflow
items have a real cost witness, but the sample-skip contract omits inputs and
its in-window workflow edit has no lawful installation route under the
no-second-push rule. The signed draw is now correctly distinguished from a
VRF; its remaining conditional theorem claim needs a stronger, correctly
stated non-anticipation assumption, not a new cryptographic primitive.

- **v2 F3: partly repaired, not fully** — the VRF/uniqueness claim is withdrawn and the grid is covered, but assumptions (i)–(iii) still do not imply the EXP3 identity: knowing the selected arm suffices to make gains depend on the draw without knowing sigma.
- **v2 F11: repaired** — five events at n=999 and one imputed n=1 give gain 5/6, invite outcome 0, and a retained round in both Scope and Pins.

## Inherited state

`python3 tools/status.py`, at `2026-11-02T07:41:40Z`, through seq 478:

```text
criterion 3: counted 7650/7800; kernel 450/500; scope equals SPEC and unchanged: True met
criterion 4: attack green on main before first scored cutoff: unverified SHORT
criterion 5: value E 1.000000 >= 20 SHORT
criterion 6: continued liveness E 1 >= 20; unchanged True; attack unverified; late repairs 0 SHORT
J7: 6 of 39 window forecasts unresolved past resolves_by
value: E 1.000000 over 0 events; window events 0
liveness continued: E 1 over 0 items (including projected expiries)
```

`promote C2a: refused` also lists unverified tests/checker evidence and
unknown off-log repairs. Forecasts 442–447 remain overdue, due
`2026-11-02T05:00:00Z`. As in v2, the bare command lacks runs/acts evidence:
its E=1 and historical REPAIR diagnostics do not prove that wealth actually
reset or that previous promotions were unlawful. The evidence-bearing lawful
C2a exit is still a precondition. Headroom is **150** before opening and
**1,350 total** above today's tree at 9,000; using all 150 leaves **1,200**.

## Findings

F1: The herald grant and report dispositions remain obligations, not effects of this read — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:16–30,208–211,308–311; CHARTER.md:258–262,308–320; SPEC.md:197–212; log.jsonl:202.

Seq 201 grants herald-2 only merge power. The sovereign's re-declaration
must precede invites; the kernel must reject an earlier herald forecast as
`no_power`. Deferred kernel types and COUNSEL-OPEN 15–20 need the promised
report dispositions. Delivery forecasts retain their original terms.

F2: The bounded gain remains coherent — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:52–59,262–266; numerical witness below.

Each ln(n_i) is in [0, ln(999)], including an imputed n_i=1, so its six-event
mean divided by ln(999) is in [0,1]. Use a numerically stable mean in that
second form, and test both endpoints. The ln(1000) mutant is killed at the
upper endpoint, not by boundedness alone. No remaining interval
counterexample or Scope/Pins partial-round contradiction was found.

F3: The named assumptions still permit reward dependence on the disclosed arm, so they do not establish the claimed sampling identity — severity: BLOCK (brief: “Under (i)–(iii) the EXP3 identity E[1{Iₜ = k} gₖ,ₜ/πₖ,ₜ | past] = gₖ,ₜ holds in the computational sense”; standing review ground: a term that names one quantity and defines another) — witness: transcripts/BRIEF-C2b-draft.md:79–108,110–129; exact counterexample below.

The original cryptographic distinction is repaired: a verifier checks a
valid signature, not the prescribed nonce or a unique VRF output. Integer
intervals cover every hash, including 2^256−1. Honest signing, conditional
computational pseudorandomness and a genuinely non-anticipating reward
process are a permissible basis for an **entrant**. CHARTER §5 does not
require an unconditional regret proof or an untrusted-custodian VRF.

But (iii) only excludes knowledge of **sigma**, not knowledge of its selected
arm or other draw-dependent information. The invite expressly publishes the
arm before the forecasts. A party able to affect outcomes can read that
field without reading sigma, and make gains depend on the choice. This
passes the literal secrecy assumption and invalidates the identity even
with a perfectly uniform, honest sampler; a computational qualification
cannot hide an order-one discrepancy.

Concrete witness: at equal weights, let all six forecasts of arm 0 assign
p(1)=999 per mille, and those of arms 1 and 2 assign p(1)=1. An outcome
controller reads only the announced arm I and sets all six outcomes to
Y=1 if I=0, otherwise Y=0. It never obtains sigma. Then g_0=1{I=0},
E[g_0]=1/3, but E[1{I=0}g_0/(1/3)]=1. Conditional on the reward vector
with g_0=1, the estimator is 3, not 1. All probabilities and gains are
legal; honest prescribed-nonce signing and pseudorandomness can both hold.
This is a sufficiency counterexample, not an allegation about the freshness
stream's operator. The 256-bit grid changes it negligibly, not substantively.

There is also a timing limitation: sigma itself is public in `args.sigma`
before the session. Thus (iii) is not a secrecy property the protocol
provides even against a gain-affecting party that simply reads the invite.
State the actual condition on the potential reward vector/response policies
and **all information about the current draw**; do not assert the next two
items “secure” it. Alternatively withdraw the bound's application to this
protocol. Neither repair requires another kernel primitive.

One more overstatement remains at lines 101–104: grinding need not “show[]
up as a frequency the propensities do not explain.” With zero gains the
weights stay uniform; a custodian can grind to select 0,1,2 repeatedly and
finish with exactly balanced counts. Frequencies can expose some deviations;
they cannot certify nonce discipline or exclude reward-correlated selection.
Keep the reported line as a diagnostic, without a detection guarantee.

For replay, distinguish the stored floating propensity from its grid mass
(floor(c_(k+1)2^256)−floor(c_k2^256))/2^256. Their rounding difference is
less than 2^−256 for exact cuts; the importance-sampling identity using the
former is correspondingly approximate. This is negligible under the stated
computational interpretation, not a demand for continuous randomness. Set
c_3=1 explicitly and specify cumulative arithmetic consistently for replay.
The fixed roster, slot index across skips, feedback-complete interleaving
and frozen deadline imputation retain v2's repairs.

F4: Success probability, sampling propensity and cumulative estimates now have distinct names and encodings — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:109–129; SPEC.md:40–43,101–106.

The Laplace success estimate is rounded half up, then clipped; only settled
past rounds count. `args.gains` is G-hat, not exponential weights. Encode
gamma and eta as strings too: the canonical JSON restriction applies
throughout args, not only to propensity and gains. Replay must never divide
by the per-mille success forecast. No remaining p/propensity naming conflict.

F5: Continued value and liveness are still required across the boundary — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:21–23,135–143,229–231,248–249,277–284; CHARTER.md:342–360.

Carry likelihoods, prior differences, stakes and wealth, with the same
mixture roster. An old-fixture comparison alone cannot witness boundary
continuation. A predictable allocation does not change A4.4's conditional
null argument; it does not establish that the null is true. Both continued
E>=20 tests, safety, veto, repairs and the ratio must reach the promotion
verb. No reset is authorized by v3.

F6: The prospective event and invite contracts retain their repairs — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:49–59,109–143,235–259,286–290.

No new permission to choose a physical event or invite after its outcome is
known was found. Preserve the first (stream,W0) invite, strict comparison,
pre-W0 cutoff, failure for missingness, and deadline-frozen gains. Procedure
types and herald invites remain outside the value mixture. This is
separate from F3's reward non-anticipation requirement.

F7: Signed addition repairs trailer spoofing, but the gate must bind the accepted review's actual bytes, not just its original adding commit — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:144–159; transcripts/REVIEW-C2b-v2.md:1–2; log.jsonl:476; judge/scope.json:4–7; SPEC.md:370–383.

**Question 3:** counsel cannot newly add an accepted review through its own
signed proposal and pass the stated non-counsel-proposal check. But checking
only the **adding commit**, as the parenthetical specifies, leaves a trivial
later-edit route. The existing v2 review was added at
`6a997ad1db3a7c8b642899ac04878f8bdb1b20c2`, exactly the commit named by the
reviewer-signed proposal at seq 475. Counsel may edit `transcripts/`. If a
counsel proposal changes that file's first two lines to ACCEPT and this
reviewed tree, the original addition remains authenticated by seq 475, the
filename matches, and the new Reviewed-tree points to the current brief.
Every enumerated check passes if it reads headers from today's file but
provenance from the original addition. No forged signature is needed.

Match the current accepted review blob to the blob authenticated by the
non-counsel proposal, and inspect the headers in that same blob. Preserve
the “own commits, not already-main ancestry” restriction and look up the
principal under the law at the proposal. This closes a concrete provenance
hole; it is not a requirement to prove the quality of a review mechanically.
Like v2's trailer finding, it is an enforcement obligation, not a claim that
the predicate cannot fail: a new counsel-only review still fails.

A reviewer session can also be induced to sign counsel-supplied text
unknowingly. Even a correct blob-bound gate will authenticate that session's
act, not independent thought. Laundering counsel's review as a cold read
would violate CHARTER A1.7 (“Every layer is reviewed by a party that did not
write it.”) and the identity/custody rule of §2.4; it is a session-integrity
failure, not a broken signature predicate. No such act is established here,
and no new machinery to infer semantic authorship is required.

F8: The 150-line pre-opening allocation is real, but is not a complete estimate of all opening evidence; criterion 8 now retains timeliness — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:144–195,213–224,253–255,280–306; SPEC.md:417–437; status output above.

**Question 6:** the read gate, its integration/tests and three pins must
actually fit under 7,800. W5 may follow the opening without changing C2a's
frozen clerk. The opening also needs the parallel-workflow preservation
test/pin and candidate-run evidence described at lines 194–196; these are
not included in the named three gate pins or explicitly costed in that 150.
The text requires all pins at exit, so it does not itself require this
fourth pin already merged under C2a's cap. Specify when its opening evidence
is supplied and count its Python test/pin lines in the applicable tree; do
not silently claim the three-pin allowance includes it. The workflow YAML
itself is not counted Python. The cap change must update SPEC §10's mirror
as well as scope.json; that is part of the cap change, not a new authority.
Moving the sample wiring into the opening to fix F14 will also need an
explicit delivery/budget allocation. No measured proof of fit exists yet.

The sovereign grant, lawful C2a exit, accepted matching read, seeded due
file and counsel forecasts also precede opening; they are not counted code.
The brief's final table now includes X4 although the preconditions and order
still say X0–X3. Enter any X4 prediction before observing its run, with its
disposition stated. Do not backfill a known-outcome success forecast.

Criterion 8's “every row that passed its due was printed ESCALATED ... at
the first prefix after it” **does answer v2 F7's timely-escalation point**.
An exit with all rows done cannot erase a missed escalation. Implement the
historical predicate and retain evidence of the contemporaneous output;
printing a historical reconstruction only at exit is not that witness.
Seed pre-opening duties with their real history and do not reset due dates
when W5 lands. A mere occurrence of an id in an unrelated entry is still not
evidence the named act was performed. Note also that the Pins list now has
five W5 pins including `w5_escalation_history`, while Scope/Deliverables say
four; criterion 1 says every listed pin, so budget and deliver all five.

F9: Opposite-principal resolution and the exercise budget remain lawful — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:44–51,130–134,250–259; CHARTER.md:318–320,376–381.

Reviewer/mini and reviewer/astra-fast resolve through builder; builder/mini
through reviewer; either is different from herald for the invite. No
principal meets its own forecast under that routing. HKJC retains its
separate contract. Twenty-four is an authorized exercise budget, not a
derived score constant. A switch is only reported and cannot replace value.
Keep bad invited rounds in the inventory even when they cannot qualify as
timely rounds for criterion 7.

F10: No additional unforced machinery found in the brief beyond the repairs, workflow items and recorded obligations — severity: OBLIGATION — witness: transcripts/PLAN-20261030.md:33–64,66–75,92–94; transcripts/REPLY-REVIEW-C2b-v2.md:26–35; transcripts/BRIEF-C2b-draft.md:180–211,299–311.

**Question 7, new machinery outside those categories: none.** The recorded
serial-CI cost and stale proposals justify testing parallelism and evidence
reuse; their lawful contracts still matter. The read gate and W5 answer
recorded review/overdue failures. The election answers the losing-record
witness and §8/A3. No new kernel language, automatic promotion or identity
system is needed by this read. The additional blockers are F13–F14 below.

The merged tree also changes session prompts: the proposal timeout and an
uncovered-hour fallback (`git diff 81149b9..c712c03 -- transcripts/sessions`).
The latter is beyond the two workflow edits, but is a scheduling instruction,
not new machinery in this brief. For C2b the invite must own W0 and the slot
index; today's template at `transcripts/sessions/stream-forecast.md:9` must
not independently select another window after an invite. This is part of
the promised diary/session integration, not an extra score constant or a
new permission for post-outcome selection.

F11: The partial-round contradiction is repaired — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:52–59,127–129,264–266; numerical witness below.

**Question 2, a remaining Scope/Pins contradiction: none.** The specified
partial round has gain 5/6, not zero; its invite is zero. Dropping the round
or dropping the missing event from the denominator are distinct mutants.
Keep the deadline-imputed result frozen against later arrivals.

F12: The parallel split changes admission evidence, but the opening push is its lawful channel and the named metadata interfaces can be preserved — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:180–196; transcripts/REVIEW-C2a-v1.md:245–276; .github/workflows/tests.yml:4–29; tools/status.py:190–199; tools/clerk.py:44–50; tools/jack:133–162.

**Question 4:** yes, this is an admission-evidence change in F8's sense.
Yes, the opening A2.6 push is the lawful installation channel. Preserving
the five commands, their execution configuration and all-success dependency
is the right witness. Merely finding command strings in YAML is insufficient
if a condition makes a step unreachable or `continue-on-error` masks it.
The gate must execute even after an upstream failure/skip and fail unless
all three results are success. Test a dropped sample and a failed/skipped
dependency against the genuinely all-green twin. Each worker needs the
same checkout/runtime assumptions as the serial workflow.

The three readers observe different metadata levels:

| reader | actual predicate | effect of correct split |
|---|---|---|
| `status.run_verified` | workflow path, push event, main branch, exact SHA, success; callers also check completion time | unchanged; no job/step inspection |
| W3 | workflow path, merge-named SHA, success, updated_at <= merge ts | unchanged; no branch/event or step check |
| merge verb | `gh pr checks --watch`, then check-run names `judge` and `tests` with SUCCESS at the exact PR head | sees extra worker checks; the final `tests` job must preserve the required name and success semantics |

There is still one **workflow-run** conclusion, but not one job/check-run.
Thus “sees what it saw” is accurate for the acceptance predicates under the
stated gate, not literally the returned rollup. A correctly failing gate
prevents GitHub's successful/skipped-check semantics from hiding a failed
worker. The candidate PR run does not replace the later main push run for
promotion. Also, the stated grouping has self-check followed by sample in
one job: using the brief's measurements its critical path is about **3:36**
plus setup/gate, not the longest individual step's 3:24. X4 remains a
forecast, not a guaranteed timing result.

F13: The sample skip calls an incomplete path comparison an identical-input witness — severity: BLOCK (brief: “every input of the sample”; F8: “a successful run covers the identical complete input tree (both checkers/binary, generator, seeds, harness, vectors and relevant execution configuration)”) — witness: transcripts/BRIEF-C2b-draft.md:197–206; transcripts/REVIEW-C2a-v1.md:255–269; harness/diff.py:3–4,45–54; sim/gen.py:31–37,215–217,336–339; harness/keys.py:16,19–24,33–37.

**Question 5:** the failed/absent/mismatched-antecedent rule, named candidate,
and fresh head tests/pins/self-check are F8's contract. The enumerated input
set is **not** complete for today's command:

- `sim/` is absent, including both `sim/gen.py` and `sim/seeds.txt`.
- `tests/vectors/weak_keys.json` is absent. `sim.gen`'s weak-key case calls
  `harness.keys.weak_keys`, which reads that file. This is exercised within
  the first 300 seeds: seed 7 (`2606f1afc7e230da`) and seed 12
  (`943a8dbf4848b42f`) select `weak_key`.

Change only a generator case, a seed, or that vector file. All six named
path hashes in v3 stay equal, but the sample's input changes. A previously
green antecedent can therefore authorize skipping the only run of the new
sample. The proposed new election simulator kinds themselves change
`sim/gen.py`. Fresh tests elsewhere are not a proof that this specific
differential coverage was preserved. This is an actual missing-input
counterexample to the written equality contract, not a request to rerun
unchanged evidence indiscriminately.

“Deterministic in its inputs” also needs qualification. The command creates
a new `gen.KeyPool`; `harness/keys.py:19–24` calls unseeded `ssh-keygen` to
generate fresh keys. Fixed seed files do not fix generated signed log bytes.
The executable Go checker is built on demand (`kernel2/check:8–23`), and
the workflow uses `ubuntu-latest` and Python `3.12`, not immutable versions
of every external runtime. Reusing an earlier randomized trial can be an
explicit evidence policy, but is not byte-identical deterministic replay
proved solely by these git trees. State the intended evidence equivalence
and its runtime/randomness assumptions before claiming F8 verbatim. An API
failure must run the sample or fail closed; an antecedent whose own sample
was skipped needs a verified chain to an actual covering run.

F14: Installing the sample-skip workflow in the window requires the second trusted-base push the brief forbids — severity: BLOCK (CHARTER A2.6: “A change to the trusted base is lawful only when a `push` entry names its digest”; SPEC §10.1: “These files change only by Guy's `jack push`, recorded by a `push` entry (item 11).”; brief refusal: “no second push inside the window”) — witness: CHARTER.md:278–282; SPEC.md:345–355,400–404; transcripts/BRIEF-C2b-draft.md:184–207,244–246,286–290,300–307; judge/judge.py:24,224–226; tools/jack:176–197.

The opening push carries the cap and **parallelization**, with the same
five commands each running once. The sample skip and its workflow edit are
expressly delivered **in the window**. `.github/workflows/tests.yml` is
trusted base regardless of whether the sovereign taps merge. An ordinary
proposal changing it is refused `trusted_path`; a direct merge/push without
the authorizing log entry makes trunk `trusted_base_unrecorded`; a lawful
`jack push` is the second push and violates the brief. Criterion 3's local
exception for a sample-skip edit cannot loosen A2.6 (A2.4).

The opening needs all trusted workflow wiring authorized then, or the brief
needs a different lawful pre-opening disposition of this item. Calling an
in-window edit the sovereign's path does not supply its missing `push` or
remove it from the trusted digest. The runner repository's tap is not a
precedent that overrides jack's own SPEC. This conflict alone prevents the
window from opening as written, independent of forecast probabilities or
whether the implementation fits 9,000.

## Reproducible numerical witnesses

No repository code was changed. The following command returned the output
shown; the first three lines use ideal uniform sampling, which is stronger
than the computational sampler assumed in F3.

```sh
python3 -c 'from fractions import Fraction as F; rows=[(i, int(i == 0), int(i == 0)) for i in range(3)]; print("(selected arm, Y, arm-0 gain):", rows); print("E[g_0] =", sum(F(g,3) for i,y,g in rows)); print("E[1{I=0} g_0 / (1/3)] =", sum(F(int(i==0)*g,1) for i,y,g in rows)); print("E[estimator | g_0=1] = 3, but g_0 = 1"); import math, statistics; print("five 999, one missing:", statistics.fmean(math.log(n) for n in [999]*5+[1])/math.log(999)); N=2**256; cuts=[0,N//3,2*N//3,N]; print("maximal grid draw selects arm:",next(k for k in range(3) if cuts[k]<=N-1<cuts[k+1])); print("headroom pre-opening:",7800-7650,"total:",9000-7650,"after 150-line gate:",9000-7800)'
```

```text
(selected arm, Y, arm-0 gain): [(0, 1, 1), (1, 0, 0), (2, 0, 0)]
E[g_0] = 1/3
E[1{I=0} g_0 / (1/3)] = 1
E[estimator | g_0=1] = 3, but g_0 = 1
five 999, one missing: 0.8333333333333333
maximal grid draw selects arm: 2
headroom pre-opening: 150 total: 1350 after 150-line gate: 1200
```

## Forecasts

forecast: **p = 0.01** that C2b's window under the exact BRIEF-C2b draft v3
bytes at `c712c035090d6f5381500bda9bbf356c48fe0113` ends in promotion rather
than failure, with every pre-stated criterion holding on the exit prefix
by the window's end. Resolve 0 if v3 is superseded without such a window,
no such window has promoted by `2026-12-31T00:00:00Z`, or a purported
promotion lacks a criterion; promotion under repaired brief bytes does not
count. Type `review.forecast`, `resolves_by = 2026-12-31T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

forecast: **p = 0.30** that by `2026-11-30T00:00:00Z` C2b's required
`tools/elect.py`, W5, read gate, parallel workflow, sample skip, tests and
pins are delivered with the complete counted set at or below **9,000**,
preserving required functionality and coverage, and its window has ended
with **no second push inside it**. Pre-opening corrections may count.
Failure to deliver, dropping required functionality/coverage, an unfinished
window at that date, or a second in-window push resolves 0. Type
`review.forecast`, `resolves_by = 2026-11-30T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

The first prices the exact text's conflicts. The second allows their repair
before opening and credits 100 additional lines over v2, but the sample
dependency/evidence work, opening integration and 150-line gate bottleneck
remain substantial. Neither forecast is conditional on the other. This
BLOCK review does not satisfy the opening read gate. The brief was not edited.
