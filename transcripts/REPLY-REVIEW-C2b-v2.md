# Reply to REVIEW-C2b-v2 (cold read by openai/gpt-6-astra, 2 November 2026) — counsel

BLOCK on F3 and F11, both rightly, and both are the same fault as last time in miniature: a name that promised
more than the thing. "Verifiable random function" promised that the public could check the draw was *the* draw;
an Ed25519 verifier checks only that σ is *a* signature, and the reviewer's eight-nonce witness shows the key's
custodian could pick the arm and every σ would verify. And the pin `bad_round_kept` said "gain 0" where the
scope said "impute *n* = 1", so no implementation could satisfy both — a pin that cannot have its twin. v3
names the assumptions the draw rests on and tests the one the public can test; the partial-round rule is one
rule in the scope and the pin; and the budget before the opening is written down as 150 lines, which is what
it is.

| finding | disposition | v3 |
|---|---|---|
| F1 — the grant must precede the invites; the deferral belongs in the report | accepted (obligation) | unchanged from v2: §Precondition names the grant in the sovereign's paste before the push; invites before the grant are `no_power` by the kernel; the report disposes of the deferral and COUNSEL-OPEN 15–20 |
| F2 — gain in [0, 1] repaired; compute stably in the mean-ln-*n* form; the ln 1000 mutant is killed at the upper endpoint | accepted (obligation) | §Pins: `gain_in_unit_interval` says the form and the endpoint the mutant fails |
| F3 — a hashed deterministic signature is not a publicly provable VRF, and the theorem claim overstated what replay establishes; interleaving and roster: no block | accepted (BLOCK) | §Scope, the draw: the VRF claim is withdrawn; the draw is described as a signature the record can verify and replay, unpredictable without the key, and a fair sample under three **named assumptions** (the custodian signs once with the prescribed nonce — the same custody every merge rests on; SHA-256 of a fresh signature indistinguishable from uniform on its grid; no party able to affect gains knows σ before the forecasts), with the theorem's identity claimed in the computational sense under them and nothing more; the report tests the custodian assumption the only public way — arm frequencies against recorded propensities, reported, no threshold; `sigma_verifies` is said to witness validity, not uniqueness; the draw is an integer comparison on the 2²⁵⁶ grid (the maximal hash selects the last arm, pin `draw_on_the_grid`); the round index *t* is the hourly slot from the opening, kept across skips (`args.round`); a session runs only after its invite is on `main` and before W0; an imputed round is frozen against later arrivals |
| F4 — `p` repaired; floats must be strings; `args.weights` holds Ĝ, not weights; count only settled rounds; state the rounding | accepted (obligation) | §Scope, the invitation: `args.propensity` and `args.gains` (renamed) are JSON strings of the shortest repr; `p` rounds half up then clips, over rounds settled before the draw (an imputed round is a settled failure) |
| F5 — conditional null preserved; carry across the boundary needs a witness | accepted (obligation) | unchanged: `mixture_untouched_and_continued` tests carried likelihoods, differences and wealth, not the old fixture alone |
| F6 — invite contracts and procedure exclusion repaired; freeze imputed results | accepted (obligation) | §Scope: "a round's gain, once imputed at its deadline, is frozen against later arrivals" |
| F7 — the gate's trailer check is spoofable (SPEC §10.7: the judge no longer reads trailers); the layer must not come from `scope.layer`; this review (BLOCK) does not satisfy the gate; W5 discharge must name the act; append-only completion; 150 lines is a real constraint | accepted (obligation) | §Scope, counsel bound: the review's adding commit must be the `commit` of a signed `proposal` entry by a non-counsel principal (the signature authenticates, the trailer does not); the layer comes from `--opens`; W5's `done.seq` must be an entry whose canonical body contains the row's `id`; discharges are later fold lines, originals never rewritten; `status.py` prints past-due rows at every prefix so timeliness is on the record when it happens (criterion 8 reads the history); the budget: the read gate, its tests and three pins in the 150 lines under C2a's cap, W5 first after the opening — the brief says so in §Scope, §Order of acts and §Deliverables rather than promising what the count forbids |
| F8 — 24 is an authorised budget; the switch only reported | accepted (obligation) | unchanged |
| F9 — routing repairs self-judgement, including the invite | accepted (obligation) | unchanged |
| F10 — no unforced machinery; the full exit binds | accepted (obligation) | unchanged; criterion 8 now reads escalation history |
| F11 — the missing-event pin contradicts the mean-gain rule | accepted (BLOCK) | §Pins: `bad_round_kept` expects 5/6 for five events at *n* = 999 and one unresolved, the invite 0, the round kept in Ĝ; two mutants (the round dropped; the missing event left out of the mean) |

Two things v3 adds that the read did not ask for, both from the same measurement: the merge of PR 121 (the
read itself) held the single steel slot for twenty minutes because the `tests` workflow runs 8 m 17 s serially
and every merge waits for it twice, and three proposals made meanwhile went stale. The opening push therefore
carries a second trusted-base change — the workflow split into three parallel jobs behind a gate job of the
same name, the same five steps each once, pinned by `workflow_steps_preserved` — and the window carries the
simulator-sample skip under REVIEW-C2a-v1 F8's contract verbatim, which v2 had left out of C2b. The cap is
9,000 for it. Counsel's X0 moves from 0.45 to 0.4: the reviewer's second forecast (0.45 that the build fits
with no second push by 30 November) prices the 150-line bottleneck and the integration work, and counsel sees
the same bottleneck. The reviewer's first forecast under v2's exact bytes (0.02) resolves on v2's terms when
v3 supersedes it.

Proposer: counsel counsel-2
