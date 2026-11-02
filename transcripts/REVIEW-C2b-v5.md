VERDICT: BLOCK
Reviewed tree: b1aee5ccf6b056e3c8d9a13d8ea968203a7f64b3

# Fifth read: BRIEF-C2b draft v5

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`, 2 November 2026.
I read REVIEW-C2b-v4, its reply, then the whole v5 brief in that order,
and checked CHARTER §2, §§4–6, A2.6, A4, A5 and SPEC §§5,7,10.
`origin/main` was the commit above, after PR #160. The separately fetched
push branch was `df4ca74b987467bae032030b7f487142cac0326d`; all push-branch
references below mean those bytes, not a moving ref. No brief or code edited.

**V5 repairs v4 F15: the represented gain is rational; the mathematical logarithmic gain is not claimed to be.**

The new antecedent proposal prevents acceptance. Its input exclusion omits
real consumers of the log; its promised fresh replay does not run on pushes
to main; an artifact's name is accepted without establishing its publisher's
tested tree; its script is not in the specified trusted base; and the retained
unconditional-step pin conflicts with the new conditional steps. These are
F16–F19, not a revival of the irrational-gain objection.

## Inherited state

`python3 tools/status.py`, as of `2026-11-02T13:44:01Z`, through seq 589:

```text
criterion 3: counted 7650/7800; kernel 450/500; scope equals SPEC and unchanged: True met
criterion 4: attack green on main before first scored cutoff: unverified SHORT
criterion 5: value E 1.000000 >= 20 SHORT
criterion 6: continued liveness E 1 >= 20; unchanged True; attack unverified; late repairs 0 SHORT
J7: 6 of 92 window forecasts unresolved past resolves_by
value: E 1.000000 over 0 events; window events 0
liveness continued: E 1 over 0 items (including projected expiries)
```

`promote C2a: refused` also names missing verified tests/checker evidence and
unknown off-log repairs. Forecasts 442–447 remain overdue. This invocation
has neither run nor acts evidence: its E=1 is not evidence that wealth was
reset, nor do its historical REPAIR lines establish unlawful promotions.
A lawful evidence-bearing C2a promotion is still a prerequisite. Headroom:
150 before opening; 1,350 total above this tree; 1,200 after a 150-line gate.

## F15 and the retained obligations

F15: The gain-representation conflict is repaired — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:65–77,91–114,133–143; arithmetic command below.

`Fraction(g)` exactly represents the computed binary64 number. Dividing it
by a positive rational grid mass and accumulating those increments in
`Fraction` is possible. For fixed represented rewards and an ideal uniform
grid draw, `E[1{I=k} g_k/pi_k | past,g] = g_k` exactly. The signature-hash
version retains the stated computational qualification and custody/reward
assumptions; it does not acquire an information-theoretic guarantee.

Question 1: **no remaining impossible command or false exactness claim in
this representation contract was found.** The ideal probability now has
its own name. The partial-round pin's mathematical 5/6 must be tested through
the expressly specified representation, not by demanding `Fraction(5,6)`
from a binary64 computation. Preserve that contract and the runtime used to
recompute the floating-point stages; rational accumulation alone does not
standardize different platforms' transcendental implementations.

Executed:

```sh
python3 -c 'import math; from fractions import Fraction as F; ns_cases=[[1]*6,[999]*6,[2]*6,[999]*5+[1]]; print([(ns,repr(g:=math.fsum(math.log(n) for n in ns)/6/math.log(999)),str(F(g))) for ns in ns_cases])'
```

```text
[([1, 1, 1, 1, 1, 1], '0.0', '0'), ([999, 999, 999, 999, 999, 999], '1.0', '1'), ([2, 2, 2, 2, 2, 2], '0.10035786744633397', '7231546470960117/72057594037927936'), ([999, 999, 999, 999, 999, 1], '0.8333333333333333', '3752999689475413/4503599627370496')]
```

Question 3, otherwise retained v4 text: **none** of the outstanding v4
obligations supplies an unmade, independent pre-opening text repair. The
F4 naming/representation request and F8 five-pin/150-line requests are now
made. The new third change does reopen coverage and workflow issues; those
are expressly identified below, rather than silently promoted from old
implementation obligations into new vetoes.

The following findings retain their v4 meaning and severity; references are
to v5. They do not certify that the future implementation exists or passes.

F1: Grant before invites and report the deferred dispositions — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:29–43,281–284,392–394; log.jsonl:202. Seq 201 grants herald-2 merge only; re-declaration must precede forecasting.

F2: Preserve the bounded gain, endpoints and missing-event imputation using the specified representation — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:65–77,337–341.

F3: Report evidence for the live reward-vector assumption; catalogue independence alone does not establish invariant forecast, delivery and resolver policies — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:120–143; transcripts/REVIEW-C2b-v4.md:61–98. The regret claim remains conditional.

F4: Keep success probability distinct from grid propensity, and encode large integers/rationals and float parameters as strings — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:91–114,144–158; SPEC.md:40–43,101–106. The text-level naming and rounding repairs are made.

F5: Continue value/liveness history and wealth and enforce every promotion condition — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:172–180,302–330; CHARTER.md:342–360,376–384. Neither invite scores nor regret replace §6 value.

F6: Preserve prospective invites/events, deadline-frozen imputations and the invite-owned W0 — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:144–180,324–326,389–391.

F7: Enforce provenance, historical principal and the verdict headers on the same authenticated review blob, including in the actual push path — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:181–203; transcripts/REVIEW-C2b-v4.md:131–155. No surviving later-header-edit route was found in that text.

F8: Measure gate fit, deliver W5 with five pins and preserve contemporaneous escalation evidence — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:181–223,247–251,327–329,368–382. The explicit 150-line stop rule repairs the delivery-note request; an opening main run and X0–X5 remain future acts, not accomplished facts.

F9: Keep resolver routing and the 24-round exercise budget as stated — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:167–171,324–326. Retain bad rounds even if they do not qualify as timely rounds.

F10: No additional unforced machinery objection — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:25–32,51–54,237–241,274–275; transcripts/REVIEW-C2b-v4.md:217–225. The repeated-CI cost is a real reason to consider reuse; it does not establish evidence equivalence.

F11: Keep the partial round, its six-event denominator and its frozen failure outcome — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:65–77,165–166,339–341. F15 explains the represented value of the 5/6 example.

F12: Require positive and failed/skipped-dependency execution witnesses for the workflow gate — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:233–251; push-branch .github/workflows/tests.yml:99–106. The new conditional reuse conflicts with the retained pin text (F19).

F13: The narrow path-list sample skip remains withdrawn; the new whole-worker reuse needs its own valid coverage contract — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:252–280; F16–F17 below. Whole-tree hashing fixes the omitted sim/vector paths but does not settle the new exclusions or provenance.

F14: Carry every trusted workflow change in the opening push and freeze it thereafter — severity: OBLIGATION — witness: transcripts/BRIEF-C2b-draft.md:290–295,318–320,366; CHARTER.md:278–282. That scheduling is lawful under A2.6; F18 concerns what the digest actually covers.

## The new antecedent job

F16: The excluded log is an input, and the promised substitute replay does not cover every head — severity: BLOCK (brief: “the **complete input tree** is identical” and “the **fresh log is replayed** on every head by the `judge` workflow”; CHARTER §6: “Safety, by independent replay.”) — witness: transcripts/BRIEF-C2b-draft.md:254–269; judge/selfcheck.py:14–26; judge/judge.py:227–245,257–275; tests/test_entry.py:88–101; tests/test_clerk.py:161–175; .github/workflows/judge.yml:7–9; push-branch .github/workflows/tests.yml:18–19,62–64,90–98.

Question 2: **this is not REVIEW-C2a-v1 F8's contract.** That review explicitly
says “The sample command does not consume `log.jsonl`; the self-check does”
(lines 255–269), and retains unit tests, pins and fresh-log replay. V5 skips
all three workers and calls the remaining tree their complete input.

* `judge/selfcheck.py` invokes the judge on HEAD against HEAD. The judge
  reads HEAD's log, runs both checkers, and checks the recorded trusted-base
  digest, amendment ordering and decision authority. These are not a
  log-independent “build”.
* `test_log_defaults_to_the_repository_root` reads the actual current log
  and checks the generated entry's sequence and parent against it.
  `test_real_prefix_and_semantic_twin` reads its historical prefix through
  seq 163. The latter prefix stays fixed under lawful appends, but the former
  consumes the new head. Neither supports “none of which reads the log”
  (push-branch antecedent.py:5–7).
* `judge.yml` has only `pull_request_target`, not `push`. This is unchanged
  on the push branch. `tests.yml` also runs on push to main and can reuse
  there. Therefore a log-only main head can get reused green workers with
  no fresh CI replay at that head. A PR judge run is not a new run over the
  resulting main commit. The verbs' local self-check is useful protection,
  but is not the workflow evidence this contract promises.

The rejecting witness is a previously green non-log tree followed by a
log-only head requiring a different self-check verdict (for example, a bad
signature or a last push entry naming a different digest). Identity stays
equal; `decide` does not read the new log; the workers skip. On a PR the
separate judge can refuse it; on a push this workflow supplies no such
replacement. This is a missing-coverage witness, not a claim that I pushed
an invalid entry or bypassed the verbs.

**Inputs outside the tree other than the runner image:** fresh OS entropy
for `ssh-keygen` in tests, pins and sample (`harness/keys.py:19–24`); the
live clock in verb tests (`tools/entry.py:85–87`, `tests/test_jack.py:634–663`);
Git checkout/index/HEAD metadata (`tests/test_digest.py:19–27`,
`tools/digest.py:19–28`, `harness/diff.py:55–56`). Fixture Git histories and
the `gh` responses in verb tests are constructed/stubbed by the tests, not
evidence that those tests consult the live GitHub API. The antecedent
decision itself additionally consumes live API/run/artifact state. V5
honestly permits reuse of the sample's old random trial; that repairs the
old sample-randomness overclaim, not the omitted real log/replay.

**Passing twin / repair:** restrict reuse to actually covered evidence and
keep current-log consumers fresh, including a both-checker self-check on
every main head; or specify and implement an equivalent fresh path before
opening. Keep the log-dependent unit coverage or give it its actual input
identity. The minimal F8 route is still fresh unit/pin/self-check jobs with
verified reuse of the sample. There is no blanket prohibition on broader
reuse once its real inputs and fresh obligations are accounted for.

F17: An artifact name is treated as proof of the tested tree without authenticating that claim — severity: BLOCK (brief: “so a change to any of them runs everything” and “the **complete input tree** is identical”; CHARTER §2.1: “No one judges their own cause”) — witness: push-branch .github/scripts/antecedent.py:37–46; .github/workflows/tests.yml:1–3,16–19,34–50 at the same push-branch commit; transcripts/BRIEF-C2b-draft.md:256–273.

`decide` verifies a workflow **path**, completion and success. It does not
verify the producing workflow's bytes, its checkout tree, or even read the
identity artifact's contents. A PR can change its own tests workflow to
publish `tree-<target identity>` and finish successfully without testing
that tree. Its judge may be red for the trusted-path edit; this does not
make its separate `tests` run unsuccessful. A later legitimate run's lookup
does not require that PR's admission and accepts the artifact. The original
workflow comment itself calls a PR's own tests informational.

Thus the attacker need not find a SHA-256 collision: the name is a claim
the publishing workflow chooses. The check still rejects red antecedents;
its defect is accepting a green non-covering antecedent. Likewise, reuse
chains are sound only after every equality link and an actual covering
root are established. Transitivity of claimed names is not that proof.

**Executed in-memory fake-API witness**, using the actual fetched function,
two real, unequal local tree identities, and no network or artifact upload:

```sh
python3 -c 'import subprocess; ns={"__name__":"review_probe"}; exec(compile(subprocess.check_output(["git","show","df4ca74b987467bae032030b7f487142cac0326d:.github/scripts/antecedent.py"],text=True),"antecedent.py","exec"),ns); ns["REPO"]="renavondata/jack"; ident=ns["identity"]("b1aee5ccf6b056e3c8d9a13d8ea968203a7f64b3"); other="df4ca74b987467bae032030b7f487142cac0326d"; calls=[]; artifact={"name":"tree-"+ident,"expired":False,"workflow_run":{"id":17}}; run={"path":".github/workflows/tests.yml","status":"completed","conclusion":"success","head_sha":other}; ns["api"]=lambda path: (calls.append(path) or ({"artifacts":[artifact]} if "/artifacts?" in path else run)); print("target identity:",ident); print("antecedent identity:",ns["identity"](other)); print("different trees:",ident!=ns["identity"](other)); print("decision:",ns["decide"](ident,18)); print("calls:",calls); run["conclusion"]="failure"; print("red:",ns["decide"](ident,18)); print("no actual API called")'
```

```text
target identity: d62a5aff093540c83afc28097d23226a023d0ce358ae7e619cc91cab7c910706
antecedent identity: be4c0f6b710b1000f30dd71251eec9597d015b88435b1dd9b449a0eb39ffd43a
different trees: True
decision: (True, 'df4ca74b987467bae032030b7f487142cac0326d', 17, 'a successful run published this tree identity')
calls: ['/repos/renavondata/jack/actions/artifacts?name=tree-d62a5aff093540c83afc28097d23226a023d0ce358ae7e619cc91cab7c910706&per_page=100', '/repos/renavondata/jack/actions/runs/17']
red: (False, '', '', 'no successful run published this tree identity')
no actual API called
```

Run 17 here is synthetic, not an allegation about a real GitHub run. The
pin must kill this forged-identity/green-workflow witness, not merely fake
an API returning no matching name when a file differs. The passing twin
binds a genuine covering run to the actual tested checkout and execution
configuration, with a named, verified chain if reuse is recursive. PR
`head_sha` and the default pull-request merge checkout also need their
correct meanings preserved; they are not automatically the same tree.

F18: The script's “trusted base” allocation is false under the current and proposed SPEC/digest — severity: BLOCK (SPEC §10.1: “The digest is SHA-256 over `path ‖ 0x00 ‖ content ‖ 0x00` for every file under `kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and the file `SPEC.md`, sorted by path.”; CHARTER A2.6: “A change to the trusted base is lawful only when a `push` entry names its digest”) — witness: transcripts/BRIEF-C2b-draft.md:254–255,318–320; SPEC.md:345–355; judge/judge.py:24,63–75; tools/digest.py:19–35; push-branch diff of SPEC.md and judge/.

Executed `from judge.judge import TRUSTED,is_under` and printed:

```text
TRUSTED: ('kernel/', 'kernel2/', 'judge/', '.github/workflows/', 'SPEC.md')
antecedent is trusted: False
```

The fetched branch changes SPEC's cap/history and `judge/scope.json`'s cap;
it does not add `.github/scripts/` to the digest or move the script into an
existing trusted path. Its bytes therefore are not named by the opening
push's trusted-base digest. Criterion 3's future freeze does not make that
statement true. This is not a claim that ordinary proposers can freely edit
the script: `.github/scripts/` is also outside their allowed scope. Nor is
uncounted Python inherently forbidden: SPEC §10.10 counts specified paths.
The error is calling this allocation digest-bound trusted base when it is
not, for code now deciding whether admission evidence runs.

Question 2, authority/allocation: **the opening push is the lawful time and
channel; this path is not the claimed trusted allocation.** Placing the
helper under an existing trusted prefix such as `judge/`, updating its
workflow reference and the brief's path, would make the intended allocation
real without inventing an in-window exception. Its builder test under
`tests/` and reviewer pin under `pins/` are counted and may lawfully arrive
with W5 as stated. Their deferred delivery cannot authorize a subsequent
trusted-base repair; the opening implementation must already be correct.

F19: The retained workflow pin forbids the conditions the third change requires — severity: BLOCK (CHARTER §2.2: “The law looks forward and never commands the impossible”; brief: “none behind a condition or `continue-on-error`” and criterion 1: “Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.”) — witness: transcripts/BRIEF-C2b-draft.md:235–245,259–260,316,357–358; push-branch .github/workflows/tests.yml:62–67,79–81,93–98.

All five commands in the actual branch are guarded by
`if: needs.antecedent.outputs.skip != 'true'`. A test implementing the
specified unconditional-step predicate fails on this intended twin. A test
that accepts these conditions silently weakens that predicate. This is
not the separate question whether the final `tests` gate fails closed: it
does include antecedent and all three workers and runs with `always()`.

State the reuse exception in the preservation pin before opening: which
steps remain unconditional and which may be covered by a verified
antecedent, with both execution branches and failed/skipped dependencies
witnessed. The blanket prohibition and blanket worker reuse cannot both
bind. Also reconcile the stale “two trusted-base changes and no other” at
lines 231–232 with the explicitly enumerated third; the numbering typo
alone would not be a separate BLOCK.

## What can open

Question 4: **I still block on F16–F19. Verdict: BLOCK.** F15 is repaired.
The missing-input/fresh-replay and artifact-provenance defects are substantive
repetitions of the problem F13 warned about, despite the improved path hash.
The opening-push scheduling itself is lawful; there is no demand for a
second push. Repair the antecedent contract, trusted placement and workflow
pin before freezing them. Existing v4 grant, read-gate, fit, escalation,
promotion and reporting obligations otherwise stand. This read does not
satisfy the brief's non-BLOCK opening gate.

## Forecasts

forecast: **p = 0.01** that C2b's window under the exact BRIEF-C2b draft v5
bytes at `b1aee5ccf6b056e3c8d9a13d8ea968203a7f64b3` ends in promotion
rather than failure, with every pre-stated criterion holding on the exit
prefix by the window's end. Resolve 0 if v5 is superseded without such a
window, no such window has promoted by `2026-12-31T00:00:00Z`, or a
purported promotion lacks a criterion. Promotion under repaired brief
bytes does not count. Type `review.forecast`,
`resolves_by = 2026-12-31T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

forecast: **p = 0.40** that by `2026-11-30T00:00:00Z` C2b's required
`tools/elect.py`, W5, read gate, workflow, tests and pins are delivered with
the complete counted set at or below **9,000**, preserving required
functionality and coverage, and its window has ended with **no second push
inside it**. Pre-opening corrections may count. Failure to deliver,
dropping required functionality/coverage, an unfinished window at that
date, or a second in-window push resolves 0. Type `review.forecast`,
`resolves_by = 2026-11-30T00:00:00Z`,
`args = {"model":"openai/gpt-6-astra"}`.

The first prices these exact bytes and their opening prerequisites. The
second allows pre-opening repairs, as v4's did; it falls from 0.50 because
the new reuse contract needs substantive correction and its tests before
the frozen workflow can support promotion. The 150-line gate, 1,200-line
remaining allowance and contemporaneous W5 history remain delivery risks.
Neither forecast is conditional on the other.

Proposer: reviewer reviewer-2
