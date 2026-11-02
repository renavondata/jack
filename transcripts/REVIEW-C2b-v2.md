VERDICT: BLOCK
Reviewed tree: 8bf4ef4e3fd8ae03174d981c39b3cf53e223d6da

# Second read: BRIEF-C2b draft v2

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 2 November 2026.
The reviewed commit is `origin/main`, after PR #118. The v1 review, counsel's
reply and the whole v2 brief were read in that order, then checked against
CHARTER §§4–6, A3.3, A4, A5 and SPEC §§5,7. This is a review of the text,
not certification of the implementation it proposes.

**The window cannot open under these exact bytes.** Four of the five old
blocking defects are repaired. F3's public-clock, delayed-feedback and roster
problems have substantial repairs, but the signature-hash construction is
still misnamed and its theorem claim overstates what replay establishes.
There is also a new, concrete contradiction between the repaired gain and
the required missing-event pin (F11). Neither calls for a charter amendment.

## Inherited state

`python3 tools/status.py`, on the reviewed tree at `2026-11-02T06:46:19Z`,
through seq 472, printed:

```text
criterion 3: counted 7650/7800; kernel 450/500; scope equals SPEC and unchanged: True met
criterion 4: attack green on main before first scored cutoff: unverified SHORT
criterion 5: value E 1.000000 >= 20 SHORT
criterion 6: continued liveness E 1 >= 20; unchanged True; attack unverified; late repairs 0 SHORT
J7: 6 of 37 window forecasts unresolved past resolves_by
value: E 1.000000 over 0 events; window events 0
liveness continued: E 1 over 0 items (including projected expiries)
```

`promote C2a: refused` additionally lists unverified tests/checker evidence
and unknown off-log repairs. Forecasts 442–447 remain overdue, due
`2026-11-02T05:00:00Z`. The bare command supplies no run/acts evidence;
its displayed E=1 is not proof that the actual continuing wealth reset or
that earlier promotions were unlawful. C2b inherits the evidence duties,
the outstanding forecasts and the continuing processes. Its opening still
requires a genuinely lawful C2a promotion. Headroom is **150 lines before
opening** and **1,250 lines total** over today's counted tree at cap 8,900;
pre-opening gates consume part of that same total.

## Disposition of the five v1 BLOCKs

- **F2: repaired** — six-event mean of ln n divided by ln 999 has endpoints 0 and 1; no legal six-forecast round leaves [0,1]. The separate contradictory pin is F11.
- **F3: partly repaired** — the public-clock exploit, stale-feedback updates and changing roster are addressed; a deterministic signature hash is not the publicly provable VRF/unqualified theorem randomness the text calls it.
- **F4: repaired** — `p` estimates binary success; the saved selection propensity is a separate importance-weight denominator.
- **F6: repaired** — procedure forecasts and herald invites stay outside value, with prospective invite identity, cutoff and settlement; no old own-ts or herald-roster conflict remains.
- **F9: repaired** — the opposite principal resolves the six forecasts and the herald's invite; no base arm is dispatched and HKJC stays outside the election.

## Findings and answers

F1: The sovereign's forecast grant and the deferred kernel types have a lawful route — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:16–19,25–30,159–162,240–243; CHARTER.md:87–90,258–262,308–312; SPEC.md:197–212; log.jsonl:202.

Seq 201 declares `herald-2` as principal herald with only `merge` power.
The printed redeclaration supplies principal, powers and public-key path;
it must actually precede the invite forecasts. Neither a text promise nor
the opening cap grants a power. The deferral and COUNSEL-OPEN dispositions
belong in the report, and delivery forecasts retain their original terms.

F2: The normalized six-event gain repairs the interval defect — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:52–59; SPEC.md:101–106; numerical witness below.

For each actual or imputed observation, 1 <= n_i <= 999, hence
0 <= ln(n_i) <= ln(999). Averaging six such numbers and dividing by the
positive ln(999) preserves [0,1]. All n_i=1 gives 0; all n_i=999 gives 1.
**Question 1, a legal six-forecast counterexample: none.** Missingness at
n=1 does not change this proof. Compute the mean stably in the stated
form; do not recover it by subtracting nearly equal floating-point losses.
The endpoints, not merely the interval, kill the ln(1000) denominator mutant:
that mutant remains bounded but its upper endpoint is below 1.

F3: Public verification of an Ed25519 signature does not establish the unique VRF output or exact bandit randomness claimed — severity: BLOCK (brief: “the uniform variate *u* = SHA-256(σ)/2²⁵⁶”; “a verifiable random function in its signature form”; “under the theorem's assumptions, which the next two items secure”) — witness: transcripts/BRIEF-C2b-draft.md:77–93; SPEC.md:153–174; signature witness below.

**(a) Randomness and replay.** V2 fixes a real defect: an entrant without
the key cannot simply calculate the next draw from W0 as in v1. Under
honest deterministic signing, private-key custody, suitable cryptographic
assumptions and a non-anticipating reward environment, this is a plausible
*computational pseudorandom implementation*. Those assumptions must be
stated as assumptions. They are not the information-theoretic conditional
sampling identity used by EXP3,

    E[1{I_t=k} g_k,t / pi_k,t | past, current reward vector] = g_k,t.

Hashing a deterministic signature under a fixed secret key does not by
itself prove that identity, nor does signature unforgeability prove VRF
uniqueness or pseudorandomness. Even an ideal 256-bit hash gives a discrete
variate, not an exact continuous uniform draw; computational/discretization
qualifications should be explicit rather than sold as the exact theorem.

More concretely, deterministic **signing** is not publicly verifiable
determinism. For secret scalar a, public A=aB and this fixed signed message
M, each nonce r gives R=rB and S=r+H(R,A,M)a mod L. Many different (R,S)
pairs verify under the same key and message. A public verifier cannot tell
that the signer used RFC 8032's prescribed secret-derived nonce. The
command below produces valid signatures whose hash draws select all three
different arms at the initial uniform weights. All pass the advertised
signature-verification step; recomputing the chosen signature's hash does
not detect this selection. A signature's one canonical *encoding* (SPEC
§6) does not make the valid signature unique.

The clerk/key custodian can anticipate all deterministic signatures for
future messages. **That fact alone does not invalidate the bound**: the
sampler necessarily knows its own draw. It matters if a party using that
knowledge can choose rewards, choose/withhold eligible rounds or grind
signatures. The record does not show such misconduct; this is a witness
against the claimed verification property, not an accusation. Unkeyed
entrants get no nonce-grinding ability from this witness. Conversely,
“the entrants do not hold the key” is not a complete non-anticipation
assumption about everyone able to affect the reward process.

Recorded sigma plus the public key *does* let anyone verify a signature,
recompute u, reconstruct weights in seq order and replay the selected
interval. It does not let the public regenerate the prescribed sigma from
the public half, or prove that it was the only permissible draw. Keep that
useful replay property. Repair the inaccurate VRF/theorem claim by stating
the actual computational and honest-sampler assumptions and their limits,
or specifying randomness with the claimed properties. The charter requires
an election entrant, not an unconditional EXP3 guarantee or a particular
cryptographic primitive; removing an unsupported guarantee is a possible
repair. This BLOCK concerns a term naming one quantity/property and
defining another, not a demand that the clerk be unable to see its own draw.

**(b) Interleaving and skips: no separate BLOCK.** Conditional on valid
sampling and non-anticipation, the numerical bound is correctly derived.
Each active instance has at most 84 rounds, bounded gains and its previous
gain before its next draw. Its standard bound is
(e-1) gamma G_max + K ln(K)/gamma, at most 43.62140915189854 with the
stated gamma. For any fixed arm, sum its four regrets; maximizing the sum
is at most the sum of the four per-instance maxima. Thus 174.48563660759416
is a valid conservative total under those assumptions. It concerns the
**executed rounds**, not hypothetical rewards in hours never invited.
The four instances need fresh conditional sampling; calling their states
independent does not prove their random streams independent.

Waiting for the earlier instance round is the important repair, not the
hope that a PR always lands in three hours. Skipping an **uninvited future
hour** for already observable feedback unavailability is predictable
scheduling; it is not dropping an invited round after seeing its gain.
The earlier invited round must still settle with the deadline imputation,
and its loss must remain. Fix t to the hourly slot index even across skips,
and let a delayed session run only after its invite and before W0. Do not
retroactively remove a losing round, or use current-hour outcomes to
choose which hour to skip. The prescribed skip rule itself does neither.

**(c) Fixed roster: none remaining from v1.** K=3 throughout, astra-fast
present at initialization, all weights initially exp(0)=1, no base arm.
The v1 nonuniform-newcomer and impossible-base-session findings do not
carry forward. The theorem constants are derived, not hand-tuned.

F4: The invite now forecasts its resolution event, while propensity remains sampling data — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:94–109; SPEC.md:40–43,101–106.

The prequential Laplace success estimate (s+1)/(n+2) is an estimator of
P(mean arm loss < mean base loss); no accuracy claim is needed for it to
be a forecast of the right event. Count only settled prior successes,
including the pre-stated failures. Specify the per-mille rounding rule.
Serialize the shortest float repr as a **string** in args: a JSON floating
number is forbidden even inside optional args. Replay and weighting must
use the saved actual sampling propensity, never the signed per-mille p.
**Question 3, a remaining p/propensity naming conflict: none.**
One misleading field name remains: `args.weights` explicitly stores the
cumulative estimates G-hat, not the exponential weights w=exp(eta G-hat)
(brief lines 73,102). Its payload is specified, so this is not a second
probability/event contradiction; implement and label that distinction
consistently in replay and reports rather than exponentiating twice.

F5: Predictable allocation preserves the form of A4.4's actual conditional-null argument; continuation still needs a boundary witness — severity: OBLIGATION — witness: CHARTER.md:342–360; transcripts/BRIEF-C2b-draft.md:115–123,169–174,213–214.

With the choice and stake in the pre-outcome information, conditional
expectation of the next factor is 1+lambda E[D|past]/B <= 1 under that
null. This does not assert the null is true or guarantee recovery of a
low-weight principal. Carry likelihoods, differences, stakes and wealth
across opening; report recovery rather than infer it from exploration.
An old-fixture comparison alone cannot witness the boundary carry.

F6: Prospective invite contracts and exclusion of procedure types repair the cutoff and mixture conflicts — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:94–123,208–215,220–224; tools/value.py:25–37,92–125; CHARTER.md:342–360.

**Question 4, an event or invite the stated rules permit choosing after
its outcome is known: none.** The invite precedes the session and W0;
the six datasets/window are fixed, (stream,W0) has one first invite,
strict loss comparison defines success, and ties/missingness define 0.
Use the existing physical-event resolution/base convention, not a later
favourable duplicate or page fetch. Reporting procedure forecasts by
`jack score` does not admit their known-outcome aliases into value.

**Disturbance to A4.1: none in the stated contract.** Herald is outside
the continued mixture, invites outside value, and procedure types already
return no event identity in today's value tool. Do not reconstruct a new
opening roster after herald gains forecast power. Freeze deadline-imputed
round results against later arrivals. The inconsistent *gain* of a partial
round is F11, not a revival of the repaired F6 event-identity defect.

F7: Pre-opening order is repaired; the gate has rejecting witnesses, but trailer-only provenance and W5 discharge need enforcement — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:124–150,157–162,193–194,234–236; SPEC.md:370–383,428–437; CHARTER.md:248,291–300; transcripts/COUNSEL-OPEN.md:3–6,22–32.

**Question 6:** the predicates are not inherently vacuous. An empty file,
missing verdict, BLOCK verdict, old brief bytes or counsel trailer fails;
an independently entered accepted review of the exact bytes can pass.
But a trailer is not authenticated authorship: SPEC §10.7 expressly says
the judge no longer reads it. A counsel-signed proposal can add a transcript
with ACCEPT, this main commit and a fabricated reviewer trailer on its
work commit. Those three syntactic checks alone pass. Bind the entry
commit to its signed proposal principal and preserved review content;
otherwise this remains a trivial provenance spoof, not an independent read.
Even authenticated headers establish provenance/freshness, not the quality
of the review's reasoning.

**This review will not satisfy the gate for v2's bytes:** its Reviewed-tree
commit matches, and its entry commit will carry `Proposer: reviewer
reviewer-2`, but its verdict is BLOCK. Merging it does not authorize the
opening. An accepted review of different brief bytes would not do so either.

Resolve the target layer from the actual opening: today's scope `layer`
is still `C1` (SPEC §10), whereas this review concerns C2b. A gate blindly
substituting scope.layer into the filename would seek BRIEF-C1-draft.md
rather than this brief. Pin the C2a-to-C2b cap-only opening itself.

W5 must distinguish a valid seq from an entry that actually performs the
named discharge: an unrelated forecast at a valid seq cannot close the
acts-table duty. Specify append-only completion records/folding so closing
a row is possible without rewriting its original null. Seed all dated
obligations, preserve late escalation history, and reject deleted duties.
Criterion 8's “no ... ESCALATED and undone” cannot erase a prior failure
to escalate on time; CHARTER §6's liveness rule still applies. Landing W5
outside the frozen clerk repairs the sequencing conflict, but 150 lines
for gates, integration, tests and pins is a substantive delivery constraint.

F8: The exercise count is now an authorized budget, and a switch is correctly only reported — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:190–198; CHARTER.md:94–104,272–274,376–381.

Twenty-four is not claimed as a coverage or significance constant inside
a score. The sovereign may authorize that workload. A switch, possibly
caused by exploration or strategic bad forecasts, proves no value; v2 no
longer says otherwise. Count actual qualifying rounds and keep the failed
ones in the inventory. Twenty-four good rounds do not excuse unreported
late invites, missing resolutions or failure of either E>=20 criterion.

F9: Opposite-principal routing repairs self-judgement, including for the herald's invite — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:44–51,110–114,212–213; CHARTER.md:318–320; SPEC.md:228–234.

**Question 5: no principal meets its own forecast under the stated
freshness routing.** Reviewer/mini and reviewer/astra-fast both resolve
through builder; builder/mini resolves through reviewer. Both resolvers
differ from herald. Thus “herald forecasts, builder or reviewer resolves”
is lawful for the invite itself after the grant. Different models alone
would not suffice; different principals do. HKJC retains its separate
C2a two-forecaster contract and gets no importance-weighted election update;
its resolver must still differ from each actual forecast's principal.

F10: No unforced new machinery found; the complete charter exit remains binding — severity: OBLIGATION — witness: transcripts/PLAN-20261030.md:33–64,92–94; transcripts/COUNSEL-OPEN.md:22–32; transcripts/BRIEF-C2b-draft.md:182–198,233–243; CHARTER.md:94–104,376–384.

**Question 7, machinery beyond the repairs and recorded obligations:
none independently requiring BLOCK.** The fixed roster, interleaving,
draw evidence and routing address the recorded v1 witnesses; the gates
and W5 address the read/overdue witnesses. No new kernel language or type
has been demanded in anticipation. Moving the switch to reporting and
calling 24 an exercise budget are legitimate dispositions, not substitute
value tests. The cap is an explicit sovereign budget, not a score constant.
The numbered exit retains safety, both continued E>=20 processes and no
veto. Implement all criteria plus §6's timely-escalation duty in the
promotion verdict. Evidence verification, report dispositions and the
pre-opening gates remain obligations, not claims of delivery by this text.

F11: The missing-event pin contradicts the repaired mean gain and cannot have the required conforming twin — severity: BLOCK (CHARTER §2: “Every rule is admitted with a witness that violates it and one that satisfies it: the first proves the rule can fail, the second that compliance is possible.”; brief criterion 1: “Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.”) — witness: transcripts/BRIEF-C2b-draft.md:52–59,201–203; numerical witness below.

The pin says **“an unresolved event gives the round gain 0 and the invite
0”**. The scope says an unresolved event contributes **one n_i=1** to the
six-event mean. Take five resolved forecasts with n=999 and one unresolved
at the deadline. The scope's gain is 5/6, not 0; the invite outcome is
indeed 0. No implementation can give this same round both gains. Making
all six n_i=1 in the test hides the contradiction rather than tests the
partial-session case it promises. Repair the pin to expect the averaged
gain with per-event imputation, or change the stated gain contract
explicitly before opening. Do not let the builder silently pick a rule.
This is new to v2's pin text; v1 F2's out-of-range formula is repaired.

## Reproducible witnesses (no repository code changes)

Numerical command:

```sh
python3 -c 'import math, statistics; B=math.log(999); gain=lambda ns: statistics.fmean(math.log(n) for n in ns)/B; print("gain endpoints:",gain([1]*6),gain([999]*6)); print("naive six-999 mean:",(sum([B]*6)/6)/B); print("five best, one missing:",gain([999]*5+[1])); gamma=math.sqrt(3*math.log(3)/((math.e-1)*84)); r=2*math.sqrt((math.e-1)*84*3*math.log(3)); print("gamma",gamma,"eta",gamma/3,"regret/instance",r,"four",4*r); print("missing-event pin demands",0,"but scope demands",gain([999]*5+[1])); print("float u at maximal hash:",(2**256-1)/2**256)'
```

```text
gain endpoints: 0.0 1.0
naive six-999 mean: 1.0
five best, one missing: 0.8333333333333333
gamma 0.15111097647155602 eta 0.050370325490518675 regret/instance 43.62140915189854 four 174.48563660759416
missing-event pin demands 0 but scope demands 0.8333333333333333
float u at maximal hash: 1.0
```

The last line is an implementation obligation: do not round a 256-bit
fraction to float 1.0 and then find no half-open interval. Use a comparison
that preserves the specified range, with its finite-grid behavior stated.
It is not evidence that a real draw has reached that boundary.

Signature witness: a synthetic secret scalar 7, no real private key, the
same SSHSIG payload and public key for all eight signatures. Tuple fields
are (nonce, verifies, selected arm index at uniform weights).

```sh
python3 -c 'import hashlib; from kernel import sig; a=7; A=sig._encode(sig._mul(a,sig._ext(sig.BASE))); m=b"SSHSIG"+sig._pack(b"jack-election")+sig._pack(b"")+sig._pack(b"sha512")+sig._pack(hashlib.sha512(b"election.invite freshness 2026-11-03T02:00:00Z").digest()); print("synthetic key weak:",sig.weak_key(A)); candidates=[(r,sig._encode(sig._mul(r,sig._ext(sig.BASE)))) for r in range(1,9)]; signatures=[(r,R+((r+int.from_bytes(hashlib.sha512(R+A+m).digest(),"little")*a)%sig.L).to_bytes(32,"little")) for r,R in candidates]; print([(r,sig.ed25519_verify(A,s,m),int.from_bytes(hashlib.sha256(s).digest(),"big")*3//2**256) for r,s in signatures])'
```

```text
synthetic key weak: False
[(1, True, 2), (2, True, 1), (3, True, 2), (4, True, 2), (5, True, 0), (6, True, 0), (7, True, 2), (8, True, 0)]
```

These are deliberately not outputs of RFC 8032's deterministic signing
procedure. That is precisely the distinction: verification accepts them
without proving which nonce procedure produced them. No signed ledger
entry or real-key experiment was needed for this witness.

## Forecasts

forecast: **p = 0.02** that C2b's window under these exact BRIEF-C2b draft
v2 bytes ends in promotion rather than failure, with every pre-stated
criterion holding on the exit prefix by the window's end. Resolve 0 if v2
is superseded without such a window, no such window has promoted by
`2026-12-31T00:00:00Z`, or a purported promotion lacks a criterion; promotion
under repaired brief bytes does not count. Type `review.forecast`,
`resolves_by = 2026-12-31T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

forecast: **p = 0.45** that by `2026-11-30T00:00:00Z` C2b's required
`tools/elect.py`, gates, tests and pins are delivered with the complete
counted set at or below **8,900**, preserving required functionality and
coverage, and its window has ended with **no second push inside it**.
Pre-opening corrections may count. Failure to deliver, dropping required
functionality/coverage, an unfinished window at that date or a second
in-window push resolves 0. Type `review.forecast`,
`resolves_by = 2026-11-30T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

The first prices the exact text's remaining conflicts. The second allows
their repair and credits the larger cap, but prices the 150-line
pre-opening bottleneck and the replay/routing/evidence integration work.
Neither forecast is conditional on the other. The brief was not edited.
