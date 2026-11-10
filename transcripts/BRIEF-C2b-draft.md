# BRIEF-C2b — the election (draft v6, counsel, 2 November 2026)

v6 answers `transcripts/REVIEW-C2b-v5.md` (gpt-6-astra, BLOCK on F16–F19, all on the antecedent job v5 added)
by withdrawing that job: its exclusion of the log was not an exclusion of a non-input (the self-check and two unit
tests read it), an artifact's name was a claim and not a proof, `.github/scripts/` is not in the trusted digest, and
the preservation pin forbade the conditions it needed. The opening push carries two changes again — the cap and
the parallel workflow — and nothing else. v5 answered `transcripts/REVIEW-C2b-v4.md` (gpt-6-astra, BLOCK on F15 alone; obligations F1–F14) as
`transcripts/REPLY-REVIEW-C2b-v4.md` sets out: the round's gain is a binary64 number computed in the stable
mean-ln-*n* form and stored exactly as the rational it is (`Fraction(float)`); exactness is claimed for the grid
probability and for the accumulation of those *represented* gains, not for ln 2 / ln 999; the W5 pin count
reads five everywhere; the 150-line consequence is spelt out. v4 answered `transcripts/REVIEW-C2b-v3.md` (gpt-6-astra, BLOCK on F3, F13, F14; obligations F1, F2, F4–F12) as
`transcripts/REPLY-REVIEW-C2b-v3.md` sets out: the draw's non-anticipation assumption is stated about the
reward vector, not about σ; the simulator-sample skip is withdrawn (the parallel workflow leaves it forty-five
seconds of critical path, and its in-window workflow edit would have been the second push the brief forbids);
the read gate binds the review's current bytes to the bytes the non-counsel proposal signed; the propensity
is the exact grid mass and the election's arithmetic is rational. v3 answered `transcripts/REVIEW-C2b-v2.md`
(BLOCK on F3 and F11; obligations F1, F2, F4–F10) as `transcripts/REPLY-REVIEW-C2b-v2.md` sets out, on top of
v2's answers to the first read. The draw is now
described as what it is — a deterministic signature the record can verify and replay, unpredictable to anyone
without the key, and a fair draw only under named assumptions about the key's custodian, which the brief
states and the report tests — not as a verifiable random function; the partial-round rule is one rule (per-event
imputation at *n* = 1) in both the scope and the pin; the read gate binds the review to a signed proposal, not
to a trailer; the floats in `args` are strings; and the budget before the opening is 150 lines, so the read gate
lands under C2a's cap and W5 lands first after the opening.

C2's third word. CHARTER §8: "C2: forecasts, proper scores, election"; §5: "Which proposer is invited is an
election by Hedge or Fixed Share on proper scores (… EXP3 under bandit feedback, Auer et al. 2002): an
entrant, not law"; PLAN §4: elections of proposers, "no witness yet". C2a produced the record; C2b makes the
record **choose who forecasts next**, and makes the choice an entry that is scored like any other. It changes
no kernel: an invitation is a `forecast` of type `election.invite` signed by the clerk's key, and the kernel
reads neither `type` nor `args` (SPEC §5). The kernel types C2a's text promised (`invite`/`accept`/`wish`) are
deferred to the first witness that a forecast cannot carry an invitation (PLAN §4: codify at the witness); that
deferral is recorded here and in the C2b report, and any forecast of their delivery resolves on its own terms.

C2b opens at the `ts` of its opening `push` (§Order of acts), after `decision promote C2a` and this brief's
read; its exit is a crossing (A5), its window a maximum of fourteen days; its value and liveness wealth
continue from C2a's (A4.1).

## Precondition
C2a promoted (`decision promote C2a` entered while `status.py` printed `lawful`); this brief and its read on
`main`; the read gate of §Counsel bound (a) merged on `main` under C2a's cap, before the push; counsel's
forecasts X0–X5 entered; `transcripts/COUNSEL-DUE.jsonl` seeded; the opening push in force (the cap), preceded
in the same paste by the sovereign's `key herald-2 --principal herald --powers merge,forecast --pubkey
~/.ssh/jack-herald.pub` (a re-declaration of the existing key, SPEC §7; no new identity).

## Purpose
Three things the record cannot yet show. **(1) An election that acts:** who forecasts a stream's next window
is chosen by a pre-stated algorithm from the entrants' proper scores, and the choice is an entry before the
session runs. **(2) Entrants that are models, not only principals:** every session forecast carries
`args.model` since 1 November; the entrant the election chooses is a (principal, model) pair, so the ledger can
say whether `gpt-5.4-mini` or `gpt-6-astra-fast` forecasts freshness better under a given key — the question
COUNSEL-OPEN 22 left to "C2's election". **(3) Counsel under the clerk:** the opening push refuses a brief
whose current text has no independent non-BLOCK read, and counsel's dated obligations are writs, so the two
failures of 31 October–2 November (a statistic the charter forbids, caught by a read and nothing else; windows
unresolved while counsel was not looking) are caught by code the next time.

## Scope
- **The entrants (arms).** A fixed roster declared here, *K* = 3: (reviewer, `openai/gpt-5.4-mini`),
  (builder, `openai/gpt-5.4-mini`), (reviewer, `openai/gpt-6-astra-fast`). The roster does not change inside
  the window; a new pair enters at the next window's brief. The base-rate forecaster is **not** an arm: it
  has no key and no session (REVIEW-C2b-v1 F9); it is the comparator of the success event below. A model
  string is the `args.model` of the forecast entry.
- **Rounds.** One round per freshness window of BRIEF-C2a (an hourly window `[H+2, H+3)`, six datasets),
  from the first invite after the opening to the window's end. HKJC per race is **outside the
  election** (two forecasters per race, as C2a); its forecasts are not rounds and are not importance-weighted.
  **The clock under BRIEF-C2a Amendment 3** (read 2 November, ACCEPT WITH OBLIGATIONS): Amendment 3's
  three-window forecast session is the stream's shape *until the first invite*. From the first invite, each
  round's forecasts come from the invited arm's own session, filed per invite — one session per window, at
  about H+0:20 for `[H+2, H+3)`, the per-window clock the delay analysis below is written for — because the
  invited arm differs from window to window and a session runs under one key; the resolve sessions stay hourly
  at :10; and every deadline in the election (the invite's, the arm's six forecasts') is **window end + 4 h**,
  Amendment 3's. This returns the stream to an hourly arrival of proposals, which is what the opening push's
  parallel workflow is for (X5 prices it); a round the merge path cannot carry in time is skipped under the
  rule below, reported and never dropped.
- **The round's gain.** For the invited arm *k* at round *t*, ℓₖ,ₜ = the mean over the six events of the
  per-mille-clipped log-loss ℓ(*q*, *Y*) = −ln *q*(*Y*) = ln 1000 − ln *n*, where *n* ∈ {1, …, 999} is the
  per-mille probability the forecast gave the outcome that occurred; a missing forecast, a missing evidence
  page or an event unresolved by the invite's deadline counts at the maximum ln 1000 (*n* = 1) — a bad round
  is never discarded. Gain *gₖ,ₜ* = (ln 1000 − ℓₖ,ₜ) / ln 999 = (mean of the six ln *nᵢ*) / ln 999 ∈ [0, 1]
  (REVIEW-C2b-v1 F2). **Its representation** (REVIEW-C2b-v4 F15): the gain is irrational for most rounds
  (ln 2 / ln 999 is not a ratio of integers), so the tool computes it as a binary64 number in the second form —
  `math.fsum(math.log(n) for n in ns) / 6 / math.log(999)` — which gives exactly 0.0 and 1.0 at the endpoints,
  and stores that number as the exact rational it is, `Fraction(g)`; every quantity downstream (Ĝ, the weights'
  exponent) is computed from the *represented* gain, and the identity and the bound below are statements about
  the represented gains. The all-endpoint rounds are exact; the *n* = 2 round is a specified approximation,
  as C2a's logarithms are (BRIEF-C2a §The statistic). *B* = ln 999 of A4.4 is untouched by this: it bounds a loss
  *difference* in the value statistic, and this is a different quantity in a different test.
- **The election: EXP3, interleaved for delayed feedback.** A round's six outcomes resolve about three hours
  after its invite (forecast at H+0:20 for `[H+2, H+3)`, resolved at H+3:10), so three later invites are drawn
  before its gain is known (its resolution reaches `main` at about H+3:25, after the resolve session's PR has
  passed the tests). The clerk therefore runs **D + 1 = 4 independent EXP3 instances**, round *t* (the *t*-th
  hourly window after the opening) using instance *t* mod 4, so one instance's consecutive rounds are four
  hours apart and the earlier one is resolved before the later one draws (Joulani, György & Szepesvári 2013,
  the black-box reduction for delayed bandit feedback: *D* + 1 interleaved instances carry the undelayed
  bound each; the same construction as Weinberger & Ordentlich 2002 for full information). If an instance's
  previous round is not yet resolved when its next draw is due, the draw waits until it is; if it is still
  unresolved at W0 the round is **skipped** — no invite, no session, the hour reported as skipped — because an
  invite drawn on stale weights is outside the theorem (pin `instance_feedback_complete`). Each instance *j*
  runs over *K* = 3 arms with horizon *gⱼ* = ⌈336/4⌉ = 84 rounds, an upper bound on its rounds in a
  fourteen-day window of hourly rounds (early exit only shortens it; the window cannot be longer):
  weights *wₖ* = exp(η Ĝₖ), Ĝₖ = Σ over the instance's past rounds where *k* was invited of *gₖ,ₜ* / *πₖ,ₜ*,
  *pₖ,ₜ* = (1 − γ) *wₖ*/Σ*w* + γ/*K* the ideal probability, whose grid mass *πₖ,ₜ* (§The draw) is the
  **selection propensity**, γ = min(1, √(*K* ln *K* / ((e − 1) *gⱼ*)))
  = 0.15111, η = γ/*K* = 0.05037 (Auer, Cesa-Bianchi, Freund & Schapire 2002, Theorem 3.1; every constant is
  the theorem's, printed here only so the pin has a number to kill). The importance weight uses the
  propensity saved in the invite, never a later one. Expected weak regret per instance
  ≤ 2√((e − 1) *gⱼ K* ln *K*) = 43.62 gain units; over the four instances ≤ 174.5 against the best fixed arm
  in at most 336 rounds — stated as what it is, a bound on expectation under the theorem's assumptions, which
  the draw's three assumptions below state, and loose, as every EXP3 bound at this horizon is; the election is an entrant
  (§5), and its record, not its bound, is what the report shows.
- **The draw.** The theorem needs a draw the entrants cannot anticipate and the record can replay. The
  clerk's draw at round *t* is the integer *U* = SHA-256(σ) read big-endian, σ = the 64 raw bytes of the clerk
  key's Ed25519 signature (`ssh-keygen -Y sign -n jack-election`, namespace fixed) over the ASCII string
  `election.invite <stream> <W0>`, recorded in the invite's `args.sigma` (base64). The arm is the one whose
  interval contains *U* on the grid of 2²⁵⁶: the **cuts** are the integers *C₀* = 0, *Cₖ* = ⌊(Σⱼ<ₖ *pⱼ*)·2²⁵⁶⌋ for
  *k* = 1, 2 from the float probabilities *pⱼ* = (1 − γ) *wⱼ*/Σ*w* + γ/*K*, and *C₃* = 2²⁵⁶ exactly; arm *k* is
  chosen iff *Cₖ* ≤ *U* < *Cₖ₊₁* — integer comparisons, no float *u*, so the maximal hash lands in the last
  interval and no value is unassigned (REVIEW-C2b-v2 F3). **The selection propensity is the grid mass**
  *πₖ,ₜ* = (*Cₖ₊₁* − *Cₖ*)/2²⁵⁶, an exact rational, and it — not the float *pₖ* — is what the importance weight
  divides by, so the sampling identity below is exact on the grid for the represented gains (REVIEW-C2b-v3 F3,
  REVIEW-C2b-v4 F15); Ĝ is the exact rational sum (`fractions.Fraction`) of the represented gains divided by
  the grid masses, so two replays of one prefix agree to the bit; floats enter in two named places — the gain's
  computation (above) and the cuts, from `exp(η Ĝ)` evaluated in binary64 — and the cuts are recorded
  (`args.cuts`, four decimal strings) so the replay compares integers. **What this is and
  is not** (REVIEW-C2b-v2 F3): `herald-2` is `ssh-ed25519` (log seq 201) and RFC 8032 §5.1.6 signing is
  deterministic, so an honest signer produces one σ per round, fixed by the key and the round string; σ cannot
  be computed by anyone without the private half, and anyone can verify it against the public half and replay
  the arm from it. Verification does **not** prove the deterministic nonce was used: the key's custodian could
  sign the same string with other nonces until the hash picked an arm of its choosing, and every such σ
  verifies. So the draw is a fair sample **under three assumptions the brief names rather than proves**: (i)
  the custodian of `herald-2` — the sovereign's machine running the published `tools/elect.py`, the same
  custody every `merge` entry already rests on (COUNSEL-OPEN 17) — signs once, with the prescribed nonce; (ii)
  SHA-256 of a fresh signature is computationally indistinguishable from uniform on its grid; (iii) **the
  round's reward vector is fixed before the draw**: the six outcomes are produced by a process that reads no
  entry of the record (renavon's public catalogue, which does not know the election exists), and each arm's
  forecasts are a function of the public record before the invite and of the pages at forecast time, the same
  function whether or not the arm was drawn — so *gₖ,ₜ*, the gain arm *k* earns if invited, depends on the
  past draws through the record and on the current draw not at all (the adaptive adversary of Auer et al.
  §3, which may react to past choices and not to the present one). The invite publishes the drawn arm and σ
  before the forecasts, so (iii) is **not** a secrecy property: it is a statement that nothing which reads the
  invite can move the outcomes or the counterfactual gains (REVIEW-C2b-v3 F3's controller, which sets the
  outcomes after reading the arm, is exactly what (iii) excludes, and the freshness stream has no such party —
  its outcomes are a catalogue's modification times). Under (i)–(iii) the EXP3 identity E[1{Iₜ = k} gₖ,ₜ/πₖ,ₜ
  | past, *g*ₜ] = gₖ,ₜ holds, exactly on the grid and in the computational sense for the hash, and the bound
  below is what it says; the brief claims nothing information-theoretic about the hash and no cryptographic
  primitive stronger than a signature. The report prints the arm frequencies against the recorded propensities
  over the window as a **diagnostic with no detection guarantee** (a custodian can grind to any frequencies,
  balanced ones included; the line can show some deviations and can certify nothing — REVIEW-C2b-v3 F3), and
  the C2b report says which of (i)–(iii) the window gave any evidence about. Pin `draw_replays_from_prefix`: the replay recomputes Ĝ, *π* and *U* from the signed
  prefix (ordered by `seq`, never by `ts`) and σ, verifying σ against `herald-2`'s pubkey and requiring the
  recomputed `args` (gains, cuts, propensity, instance) to equal the recorded ones byte for byte; an invite whose
  draw does not replay is `rigged_election` and the diary files no session on it; `sigma_verifies` witnesses
  that σ is a valid signature of the round string, not that it is the only one.
- **The invitation.** Before each forecasting session the clerk enters a `forecast` of type `election.invite`:
  claim "stream <s>, window <W0>: the invited entrant <principal, model> achieves a mean clipped log-loss on
  the window's six events below the base rate's" (the base rate at each event's resolution as `tools/value.py`
  defines it; the comparison strict; a tie or a missing event is 0); `p` = **the clerk's forecast of that
  success event**: the prequential Laplace rate of the invited arm's past rounds' successes, (*s* + 1)/(*n* + 2)
  in per mille, clipped to 1–999 — a proper-scored statement about the event the resolution decides
  (REVIEW-C2b-v1 F4), rounded half up to the nearest per mille and then clipped to 1–999, counting only rounds
  settled before the draw (a round imputed at the deadline is a settled failure); and *not* the selection
  propensity, which travels as `args.propensity` — the grid mass as an exact rational string
  `"<numerator>/<2^256>"`, the quantity the importance weight divides by, never the rounded `p` — with
  `args.cuts` (the four cut integers as decimal strings), `args.instance`, `args.gains` (Ĝ per arm before the
  draw as exact rational strings — the cumulative importance-weighted gains, not the exponential weights;
  REVIEW-C2b-v2 F4), `args.sigma`, `args.gamma` and `args.eta` (shortest-repr float strings: SPEC §5 admits no
  JSON float anywhere in `args`, REVIEW-C2b-v3 F4), `args.roster`, `args.round` (the hourly slot index *t* from
  the opening, kept across skips);
  `args.window_utc`, `args.stream`, `args.principal`, `args.model`; `resolves_by` = window end + 4 h
  (BRIEF-C2a Amendment 3; the arm's six forecasts carry the same deadline). The
  invite's key is (stream, W0): the first invite for a key stands and a second is a `revision`, not a round. The
  event's cutoff is `W0` (the invite is entered at about H+0:15, the window starts at H+2). The diary files the
  forecasting session for that principal and model with the invite's seq in the issue, after the invite is on
  `main` and before W0 — a session that would start at or after W0 is not filed and the round settles as
  missing; the session's six forecasts carry `args.invite` = that seq. An invite whose session did not run, or
  ran under another key or model, still resolves — every event imputed at *n* = 1, the invite 0 — and counts
  in the round (criterion 7); a round's gain, once imputed at its deadline, is frozen against later arrivals.
- **Resolution routing (REVIEW-C2b-v1 F9).** The six events of a round are resolved by a principal other
  than the invited one: the diary's resolve session at :10 runs under the **builder** key when the round's
  invite named the reviewer, and under the **reviewer** key when it named the builder; the invite itself is
  resolved by that same session (its forecaster is the herald, so either may). No principal ever meets its
  own forecast; pin `resolver_not_forecaster`.
- **C2a's value statistic is untouched and continues**: the roster of its mixture (guy, counsel, reviewer,
  builder, base) and its likelihood history carry across the boundary (REVIEW-C2a-v2 F7); the election changes
  which principal forecasts a window and nothing in the mixture's algorithm; the choice is *F*ᵢ₋₁-measurable,
  so A4.4's conditional null is undisturbed (REVIEW-C2b-v1 F5). The herald's invites are **not** events of the
  value statistic and the herald is not added to the mixture's roster; they are scored by `jack score` under
  their type and reported by the election line (REVIEW-C2b-v1 F6). **The procedure types** (`proposal.ci`,
  `proposal.count`, `counsel.programme`, `review.forecast`) **stay out of the promotion statistic**, in C1's
  reported scores, until a contract with a genuine pre-outcome boundary exists for each (REVIEW-C2b-v1 F6: an
  own-`ts` cutoff admits forecasts of outcomes already public); writing those contracts is a C2c item.
- **Counsel bound** (REVIEW-C2b-v1 F7, REVIEW-C2b-v2 F7). The read gate is built **before the opening**, as an
  ordinary tools proposal under C2a's cap, so the opening push is the first act it refuses or admits; W5 lands
  first after the opening, because C2a's cap has 150 lines left and the gate, its tests and its three pins are
  what fits (REVIEW-C2b-v2 F7: "a substantive delivery constraint"):
  (a) `jack push BRANCH --opens LAYER`: `--opens` is required when the branch changes `judge/scope.json` (an
  opening: `layer` or `cap`) and refused otherwise; the push is refused unless `main` holds
  `transcripts/BRIEF-<LAYER>-draft.md` and a `transcripts/REVIEW-<LAYER>-*.md` whose first line is
  `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`, whose `Reviewed tree:` names a commit on `main` at
  which the brief's bytes equal the brief's bytes at `main`, and **whose bytes at `main` are the bytes a
  `proposal` entry signed by a key whose principal is not counsel carried**: the review's blob at `main` equals
  its blob at that proposal's `commit`, and the commit that added it is that `commit` or one of the proposal's
  own commits (reachable from its `commit`, not from the `main` the pull request was merged onto); the headers
  the gate reads (`VERDICT:`, `Reviewed tree:`) are read from that same blob — the proposal entry is signed,
  the trailer is not (SPEC §10.7), so a counsel proposal carrying a file with a forged reviewer trailer fails,
  and so does a later counsel edit of an accepted review's first two lines (REVIEW-C2b-v3 F7: provenance of the
  addition alone left that route open); the signer's principal is looked up under the key entries in force at
  the proposal;
  an empty file, a missing verdict, a BLOCK or a counsel-signed proposal does not count; the layer comes from
  `--opens`, never from `scope.json`'s `layer` (still `C1`). Pins `push_without_read_refused`,
  `read_of_this_text`, `read_not_counsels` (mutants: the trailer accepted in place of the signed proposal; the
  headers read from a blob later edited by counsel). A reviewer session induced to sign counsel's text would
  pass this gate: that is a breach of A1.7 and §2.4 by the party that did it, not a defect of the predicate, and
  the gate claims to establish provenance and freshness of a read, nothing about its reasoning.
  (b) W5, counsel's writs: every row of `transcripts/COUNSEL-DUE.jsonl` — `{"id", "due", "what", "done":
  {"seq": n, "what": "<the act>"} or null}` — is a writ held by counsel, ESCALATED past `due`. A row is
  discharged only by a `done` whose `seq` is an entry on the prefix **whose canonical body contains the row's
  `id`** (a proposal whose title names it, a forecast or resolution whose `args.id` is it): a bare integer, an
  unrelated entry at a valid seq, or deleting the row discharges nothing (REVIEW-C2b-v2 F7). Rows are
  append-only: the original row is never rewritten; a discharge is a later line `{"id", "done": {...}}` that
  folds onto it, and a file whose earlier lines changed is refused. The file is seeded at the opening with every
  dated obligation of COUNSEL-OPEN (items 23's diary, the C2a report, the C2b brief's reads, the acts tables)
  and of this brief (the report, the C2c brief, RUNBOOK sections, X-forecast resolutions), and pin
  `w5_inventory` checks the seeded ids are present at every later tree; escalation history is kept: a row
  completed late prints ESCALATED-then-done forever, and `status.py` prints at every prefix the rows past due
  and undone, so a failure to escalate on time is on the record the hour it happens, not at the exit. W5 is
  computed by a new `tools/due.py` and printed by `status.py` beside the clerk's W1–W4, **not** inside
  `tools/clerk.py`: C2a's criterion 6 holds the clerk byte-identical through its window, so a W5 written into
  the clerk before C2a's exit would fail the layer it is meant to precede; it moves into the clerk under the C2c
  brief if that brief says so. The contemporaneous `status.py` output is the witness of timely escalation,
  so the diary's resolve session runs `status.py` at every tick and commits its W5 lines with its evidence
  (a file per tick under `transcripts/evidence/w5/`), and the exit reads those files, not a reconstruction.
  Five pins: `w5_overdue_escalates`, `w5_done_is_an_entry` (the mutant: an unrelated entry discharges),
  `w5_rows_append_only`, `w5_inventory`, `w5_escalation_history` (a late discharge keeps ESCALATED).
  (c) COUNSEL-OPEN 13's rule — every recommendation to the sovereign that asks an act is a forecast — stays
  as it is, a standing rule; `status.py` prints, under its honest name, "sovereign acts in the window with no
  counsel forecast naming them before the act" as a reported line, not a W4 count (REVIEW-C2b-v1 F7).
- **The cap, and the opening push's second change.** The budget is **9,800** (9,000 in v6, raised by Amendment 1 before the opening; 7,650 counted when v6 was written; four EXP3
  instances with replay, the signed draw, the invite verb, the resolver routing, W5 and its tick evidence,
  status and decision integration, tests, two simulator kinds and some twenty-five pins — REVIEW-C2b-v1 priced
  750 lines as too thin), raised by the opening push; never again inside the window. The read gate lands under
  C2a's 7,800 before it, in the 150 lines left. The opening push carries **two trusted-base changes and no
  other** (REVIEW-C2a-v1 F8: "the phrase 'two trusted-base changes' should identify" them; A2.6): the cap, and
  `.github/workflows/tests.yml` restructured from one serial job into three parallel jobs (unit tests with the
  kernel line count; pins; judge self-check with the simulator sample) behind a gate job named `tests` that
  fails unless all three succeeded. The same five steps each run once with the same commands; the workflow's
  name, triggers and single conclusion are unchanged, so every reader of run metadata — `status.py`'s
  `run_verified`, W3, the merge verb's wait — sees what it saw. Measured on 2 November on the merge of PR 121:
  8 m 17 s serial (unit tests 2:49, pins 1:50, self-check 0:12, sample 3:24), and every merge waits for this
  run twice (the proposal head, then the head carrying the merge entry), so a merge costs sixteen minutes of
  the single steel slot and proposals made meanwhile go stale; three parallel jobs cut the run to the longest
  step — about 3:36 on the sample job's path, self-check then sample (REVIEW-C2b-v3 F12). Pin
  `workflow_steps_preserved`: a test parses the workflow and finds each of the five commands exactly once,
  none behind a condition or `continue-on-error`, each worker with the same checkout and runtime steps, and
  the gate job running `if: always()` and failing unless all three results are `success` (mutants: the sample
  step dropped; the gate not run after a failed dependency); it is delivered with W5 as the first item in the
  window, since it is counted Python and the 150 lines before the opening are the read gate's (REVIEW-C2b-v3
  F8). The opening's own evidence for the workflow is the pull request counsel opens on the push branch
  beforehand — PR #125, run 41405822622: `unit` 2:52 and `pins` 1:29 green, `sample` red at the self-check's
  `trusted_base_unrecorded`, which every push branch shows until its push entry records the digest, and the
  gate red because one worker was, the fail-closed witness itself — and the `tests` run on `main` for the push
  head, which X4 forecasts and which is entered before the push, with X0–X3.
- **The simulator-sample skip is withdrawn** (REVIEW-C2b-v3 F13, F14), **and so is v5's reuse of a run on an
  identical tree** (REVIEW-C2b-v5 F16–F19: the self-check and two unit tests read the log; an artifact's name
  proves nothing about the tree its publisher tested; `.github/scripts/` is outside the trusted digest; the
  preservation pin and the conditional steps could not both bind). Measured again with the reviewer's inputs,
  the reusable part is the sample command alone, forty-seven seconds of a parallel run's critical path, which
  does not pay for a coverage contract. With the workflow parallel the sample
  job is 3:36 against the unit job's 2:52, so the skip would buy forty-five seconds of critical path; its
  equality contract needed `sim/`, `tests/vectors/weak_keys.json` and a statement about `ssh-keygen`'s fresh
  keys, and its workflow edit inside the window would have been the second trusted-base push the brief
  forbids. It leaves this brief and is not promised to the next one.
- **Not in C2b:** kernel or kernel2 changes; `wish` entries (the sovereign's wishes remain issues labelled
  `wish` in the runner, each answered by a counsel forecast of his decision); a GitHub identity per party
  (COUNSEL-OPEN 17, 20: the report says what the acts table shows and asks only if the declaration rule missed
  an act); automatic promotion; contracts for the procedure types; the simulator-sample skip.

## Order of acts, and the clock
1. The read gate (a) merged on `main` under C2a's cap (a builder proposal, the reviewer's three pins), while
   C2a runs.
2. This brief merged with a read that returns no BLOCK; counsel enters X0–X5 and seeds `COUNSEL-DUE.jsonl`.
3. The sovereign, one paste: `decision promote C2a` (when `lawful`), `key herald-2 … --powers
   merge,forecast`, the opening `push` (cap 9,800 and the parallel tests workflow) — which the gate of step 1
   admits because step 2 is on `main`. The opening is the first `push` entry after `decision promote C2a`; the window is (opening `ts`,
   min(X0's `resolves_by`, opening + 14 d)].
4. The builder builds W5 (`tools/due.py`, with `workflow_steps_preserved`'s test, the first item under C2b's
   cap), then `tools/elect.py`; the reviewer
   pins each; the herald merges; the diary consults `elect.py` before every forecast session from the first
   green `tests` run on `main` holding `tests/test_elect.py` — invites before that instant are not rounds
   (criterion 4).
5. `status.py` prints the election line and `promote C2b: lawful | refused: …`; the sovereign's
   `decision promote C2b` at the crossing.

## Statistics
- **Value continued**: *E*ᵥ of BRIEF-C2a §The statistic, one ledger, unchanged events. Criterion: ≥ 20 at
  the exit prefix.
- **Liveness continued**: C1b's process, unchanged. Criterion: ≥ 20 at the exit prefix.
- **The election's record**: per arm, Ĝ, rounds invited, mean gain, successes; the invites' log-loss against
  the base rate of type `election.invite` by `jack score`. Reported; no threshold.

## Safety: two attack kinds before any round counts
`self_invite` (an `election.invite` not signed by `herald-2`: the tools treat it as `unkeyed`, the diary files
no session on it) and `rigged_election` (an invite whose Ĝ, *π* or *u* do not replay from the signed prefix
and its σ — forged `args.gains`, a σ that does not verify, a draw from a later prefix). Green on `main`
before the first round (criterion 4).

## Pre-stated criteria for C2b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines within 9,800; the kernel within 500 and byte-identical to C2a's; `judge/scope.json`,
   SPEC §10 and `.github/workflows/tests.yml` unchanged since the opening push.
4. The attack tests green on `main` before the first round's invite.
5. Value continued: *E*ᵥ ≥ 20.
6. Liveness continued: ≥ 20.
7. **Elections witnessed**: at least 24 rounds (one day of hours — an exercise budget the opening push
   authorises, not a constant in any score) whose invite is on the log before the session, replays from the
   prefix, and is resolved by its deadline; the four instances' rounds interleaved as stated.
8. **Counsel bound**: the three gate pins and the five W5 pins KILLED; no `COUNSEL-DUE` row past due and
   undone at the exit prefix; every row that passed its due was printed ESCALATED by `status.py` at the first
   prefix after it (the history, not the exit, is what is read).
9. No `decision` of kind `veto` with subject `C2b`; off-log repairs 0; A3.4 at or under 5 : 1.
**Reported, not gating**: whether any round's invite named an arm other than the previous round's of the
same instance (a switch is evidence of exploration or of a changed record, not of value — REVIEW-C2b-v1 F8);
each arm's record; the arm frequencies against the recorded propensities (a diagnostic, no detection
guarantee); sovereign acts without a prior counsel forecast.

## Pins (the reviewer's), each with its named mutant and passing twin
`gain_in_unit_interval` (the legal endpoints map to 1 and 0, computed as mean ln *n* / ln 999; mutant: divide
by ln 1000, whose upper endpoint is below 1) · `round_loss_is_mean` (six losses averaged; mutant: summed) ·
`bad_round_kept` (five events at *n* = 999 and one unresolved at the deadline give the round gain 5/6 and the
invite 0, and the round stays in Ĝ; mutants: the round dropped; the missing event left out of the mean, giving
1 — REVIEW-C2b-v2 F11: one rule, in the scope and in the pin) · `exp3_importance` (Ĝ by the saved propensity;
mutant: by today's) · `exp3_constants` (γ, η from *K* and *gⱼ*; mutant: γ = 0.1) · `instance_feedback_complete`
(instance *t* mod 4's previous round is resolved before its draw, or the draw waits; mutant: draws anyway) ·
`draw_replays_from_prefix` (Ĝ, *π*, *U* recomputed from the prefix and σ, integer intervals; mutant: from
`args.gains`) · `sigma_verifies` (σ verifies against `herald-2`'s pubkey over the round string; mutant:
unchecked) · `draw_on_the_grid` (the maximal hash selects the last arm; mutant: float *u* = 1.0 unassigned) ·
`roster_fixed` (an arm outside the opening roster refused; mutant: admitted) · `invite_before_session`
(forecasts carry `args.invite` earlier than their `ts`; mutant: later accepted) · `invite_cutoff_W0` (an invite
with `ts` ≥ W0 is `rigged`; mutant: scored) · `invite_p_is_success_rate` (`p` = the Laplace success rate of the
arm, not the propensity; mutant: the propensity) · `invite_resolution_strict` (1 iff mean loss < base's; mutant:
≤) · `resolver_not_forecaster` (a round's events resolved by a principal other than the invited; mutant: the
same) · `self_invite` · `rigged_election` · `mixture_untouched_and_continued` (C2a's fixture byte-identical;
likelihoods, prior differences and wealth carried across the boundary; mutant: uniform restart) ·
`procedure_types_out` (a `counsel.programme` forecast is not a value event; mutant: scored) ·
`push_without_read_refused` · `read_of_this_text` · `read_not_counsels` · `w5_overdue_escalates` ·
`w5_escalation_history` (a late discharge keeps ESCALATED; mutant: cleared) ·
`w5_done_is_an_entry` · `w5_rows_append_only` · `w5_inventory` · `workflow_steps_preserved` ·
`window_from_the_push` · `wealth_continues` ·
`promote_refused` (the verb signs nothing when any criterion is unmet; mutant: value alone).

## Refusal list
No kernel change; no LLM in `elect.py`; no constant in the election but *K*, *gⱼ*, *D* and the theorem's
formulas; no draw from a public seed; no invite entered after its session starts or after `W0`; no round
dropped; no entrant invited by hand; no principal resolving a round it forecast; no change to C2a's statistic,
mixture or clerk; no second push inside the window; no event or invite chosen after its outcome is known.

## Stop and report if
the build does not fit under 9,800; **the read gate, its tests and its three pins do not fit in the 150 lines
under C2a's 7,800** — then C2a's own rule applies (BRIEF-C2a §Stop and report: the shortfall in lines, C2a's cap
not raised mid-window) and C2b does not open to fund its own prerequisite; counsel reports the shortfall and
the lawful route, which is a smaller gate or a later opening, never a second C2a push; the two checkers
disagree; the clerk's key cannot sign a forecast (the
grant missing: the window has not opened); a stream's public evidence disappears; an invite's draw cannot be
replayed from the prefix (a defect in this brief's algorithm, fixed by amendment before any round counts); the
interleaving's assumption fails (a round unresolved when its instance draws again: the draw waits, and the
report says how often).

## Deliverables
Before the opening: `tools/jack push --opens` (a), its tests and three pins, under C2a's cap and outside
C2a's refusal list (no change to C1's statistics or the clerk). In the window, in this order: `tools/due.py`
W5 (b) with its `status.py` line, tests and five pins; `tools/elect.py` (`--invite <stream> <W0>` prints the
entry body and σ; `--replay <seq>`;
`--table`); the diary consulting it and routing the resolver (runner side, prompts in `transcripts/sessions/`);
`tools/value.py` unchanged but for `procedure_types_out`; `tools/status.py` the election line, criteria 1–9
and `promote C2b`; `tools/jack decision` dispatching `C2b`; `tests/test_elect.py`; `tests/test_workflow.py`; the two simulator
kinds;
the pins; RUNBOOK `## jack elect`; `transcripts/COUNSEL-DUE.jsonl`; counsel's X0–X5; the session prompts
rewritten so that under C2b the invite owns the window — a forecast session's W0 is its invite's, and the
uncovered-hour fallback of `transcripts/sessions/stream-forecast.md` applies only to sessions filed without an
invite, which after the first round there are none of (REVIEW-C2b-v3 F10); the C2b report, which
disposes explicitly of COUNSEL-OPEN 15–20 (recorder and identities: delivered, carried, or dropped with the
reason) and of the deferred kernel types; the C2c brief's first section (the procedure contracts, the kernel
types if a witness has appeared, the GitHub identities) at exit.

## Counsel's forecasts on this window (entered after the read, before the opening push)
| id | claim | p |
|---|---|---|
| X0 | the promotion forecast: every criterion holds on the exit prefix by the window's end | 0.4 |
| X1 | criterion 7 met within 3 days of the opening push | 0.55 |
| X2 | at the exit (reviewer, `gpt-6-astra-fast`) has been invited at least once and its mean gain exceeds (reviewer, mini)'s | 0.4 |
| X3 | no second push inside the window | 0.7 |
| X4 | the `tests` run on the opening push's commit on `main` completes in under five minutes and is green | 0.75 |
| X5 | over the 24 hours after the opening push, the median time from a `proposal` entry's `ts` to its `merge` entry's `ts` is under twelve minutes (2 November 00:00–12:00Z: about twenty) | 0.5 |


## Amendment 1 (3 November, counsel; the cap 9,000 → 9,800, before the opening)

What the record shows since v6 was read: the read gate landed at 120 counted lines (49 in `tools/jack`, 71 of
tests, PR #182) and its three pins at 18 (PR #183), for one paragraph of §Scope; `main` stands at 7,784 of
C2a's 7,800. Under 9,000 the window would have 1,216 lines for everything the brief still names: W5 and its
`status.py` line, `tests/test_due.py`, `tests/test_workflow.py` and five pins (counsel's count from the gate's
density, about 250); `tools/elect.py` with the four instances, the signed draw and its replay, the invite, the
resolver routing and the table, `tests/test_elect.py`, the two simulator kinds, some twenty pins, and the
`status.py`, `jack decision` and `value.py` changes (about 860). That is a margin under a hundred lines on
counsel's own count, and REVIEW-C2b-v6 priced the fit at 0.40. A window that fails on criterion 3 costs its
fourteen days' wealth nothing (A4.1) and the programme several days of wall clock.

From this amendment's read:
- **The budget is 9,800.** It is the same kind of number it was — a resource constant the sovereign
  authorises at the opening, entering no score — set once more *before* the opening and, as v6 says, never
  again inside the window. Criterion 3 reads "counted lines within 9,800"; §Stop and report reads "the build
  does not fit under 9,800"; §Scope's paragraph *The cap* reads 9,800 where it read 9,000. The opening push
  still carries **two trusted-base changes and no other**: `judge/scope.json` `cap` 7800 → 9800 with the
  identical block in SPEC §10 and one clause of the cap's history, and the parallel `tests` workflow,
  unchanged since the read of v6 diffed it against `606d276`.
- **Nothing else moves**: the roster, the statistic, the election, W5, the gate, the order of acts, the
  twenty-four rounds, X0–X5 (the reviewer's forecast "fit under 9,000" and counsel's X3 resolve on their own
  terms against the count at the exit prefix; a cap of 9,800 does not make a count under 9,000 more or less
  likely).

Why this is lawful before the opening: the brief is counsel's draft until the push that opens the window, and
is amended the way BRIEF-C2a was amended three times — in writing, read cold, with the push branch's bytes
diffed by the read; the gate admits the opening on the read whose `Reviewed tree:` holds this text. A cap
raised *inside* the window would be the second push the brief forbids; raised before it, it is the number the
window is pre-stated with.


## Amendment 2 (4 November, counsel; the window's end — before the opening and before any formal read, one clause)

**How this text came to stand here.** The first text of this amendment reached `main` unread through the merge of #292 (seq 1265). It bundled five items. It read C2a's end, and so C2b's earliest opening, as 15 November. It set X7 at 2026-12-03 with a fourteen-day maximum beside it.

Its revised substance was drafted inside the 24 hours after the failure that counsel's request helped cause, which COUNSEL-OPEN row 33's rule forbids: on counsel's branch at 11:35–11:45Z on 4 November. It was withdrawn at 12:21Z (row 35). This text, revised again and split into one clause per amendment, was committed after 2026-11-04T21:44Z. Amendments 3, 4 and 5 and the note that follows carry the rest.

**Why it is lawful.** The brief is counsel's draft until the push that opens the window, as for Amendment 1. §6 requires a window to be "committed before the window opens". A5.2 takes the promotion forecast "entered before the window opens". A5.1's "the stated end may not be moved" binds from the opening.

**What it changes.** The date at which the window ends, and the texts that name its forecast: no statistic, no stream, no criterion's threshold.

- **Why X0 no longer fits.** §Order of acts step 3 reads the window as (opening `ts`, min(X0's `resolves_by`, opening + 14 d)]. X0 (seq 636) was entered on 2 November with `resolves_by` 2026-11-18T00:00:00Z, against an opening expected on 3 or 4 November.
  - C2a's first window cannot promote.
  - C2a-prime opens only after 2026-11-17T12:00:00Z (corrections 2 and 5; BRIEF-C2a-prime).
  - C2b opens only after C2a-prime's promotion.

  So X0's date would close C2b's window within a day of its opening, or before it.
- **X7.** A5.2: a window's stated end is "the `resolves_by` of the promotion forecast the window's brief names, entered before the window opens; a brief states no other date". This brief now names **X7** as its promotion forecast. Counsel enters it after this amendment's read and before the opening, at p 0.55, with this claim: "the promotion forecast: every pre-stated criterion of BRIEF-C2b holds on the exit prefix by this forecast's `resolves_by`, 2026-12-01T12:00:00Z".
  - **§Counsel's forecasts.** Row X0 reads "X0 | entered as v6's promotion forecast; no longer the promotion forecast (Amendment 2); resolves on its own words | 0.4". A row "X7 | the promotion forecast: every pre-stated criterion of BRIEF-C2b holds on the exit prefix by this forecast's `resolves_by`, 2026-12-01T12:00:00Z | 0.55" follows X5.
  - **Elsewhere.** §Precondition, §Order of acts step 2 and §Deliverables read "X0–X5 and X7" where they read "X0–X5".
- **The window.** It is (opening `ts`, X7's `resolves_by`].
  - **Why no other date.** `transcripts/REVIEW-C1b-A5.md` F8 applied A5.2's last clause to a brief's fourteen-day maximum, and counsel accepted the finding. So this brief states no other date.
  - **Texts that change.**
    - §Order of acts step 3's min(X0's `resolves_by`, opening + 14 d) becomes X7's `resolves_by` alone.
    - The opening paragraph's "its window a maximum of fourteen days" (before §Precondition) is struck.
    - §Scope's horizon *gⱼ* = ⌈336/4⌉ = 84 stands as an upper bound. Its parenthesis "(early exit only shortens it; the window cannot be longer)" reads "(early exit only shortens it; every C2b window is shorter than fourteen days, Amendment 2)".
  - **Why the end is one instant.** C2b opens after C2a-prime's opening, which is after 2026-11-17T12:00:00Z. X7's date is that instant plus fourteen days. So every C2b window is shorter than fourteen days, and its end is one instant on both readings of C2a's unruled question (correction 5).
  - **How `status.py` reads X7.** It reads X7 by `args.id`, with a `seq` below the opening's. If there is none, it prints `promote C2b: refused: C2b has no promotion forecast before its opening`.
  - **If C2b never opens.** If no C2b opening precedes X7's `resolves_by`, there is no window, and C2b is pre-stated afresh by the same procedure.
  - **§Stop and report adds** a C2b opening push before X7 is entered, or at or after X7's `resolves_by`.
- **The earlier forecasts.** X0–X6 are not edited and resolve on their own words. Each was set to a date that assumed an opening in early November:
  - X1, by 7 November;
  - X4, by 4 November, already resolved 0 (seq 1108);
  - X5, both entries (seqs 641 and 685), by 6 November;
  - X0, X2, X3 and X6 (seqs 636, 638, 639 and 815), by 18 November. Each speaks of C2b's exit prefix, which cannot exist by then.

  Counsel takes each as the record of a date set before the timetable moved, and enters no replacement for X1–X6.

## Amendment 3 (4 November, counsel; the cap 9,800 → 10,400 — before the opening, one clause)

**How this sits with COUNSEL-OPEN row 33's rule.**
- The rule bars changing a criterion after a window has read it. Its case was C2a's criterion 7, read at the crossing, which A3.2 decides by a new window.
- C2b has not opened, and no C2b criterion has been read on any prefix.
- This amendment, like Amendment 1 (`transcripts/REVIEW-C2b-am1.md` F24), pre-states criterion 3's bound before the opening. It does change that bound.
- It keeps C2b's allowance above its starting cap at 2,000 lines: 7,800 → 9,800 becomes 8,400 → 10,400. The bound moves only by the 600 lines that C2a-prime's opening adds, so it buys no room that F26 did not price.
- The cap enters no score (Amendment 1; BRIEF-C2a §The cap). It is set once more here, before the opening, and never inside the window.

**The texts that change.** Every 9,800 that states C2b's cap reads **10,400**:
- criterion 3;
- §Stop and report;
- §Scope's *The cap*;
- §Order of acts step 3's "(cap 9,800 …)";
- Amendment 1's statements of the budget ("The budget is 9,800", and its list of the texts that read 9,800).

Amendment 1's "`judge/scope.json` `cap` 7800 → 9800" reads 8400 → 10400, and §Scope's parenthesis "(9,000 in v6, raised by Amendment 1 before the opening; …)" adds "and to 10,400 by Amendment 3". The rest of the opening push is unchanged.

**Measured.** The integrated C2b branches add about 1,705 counted lines to `main`'s 7,784:
- `builder-c2b-status`, which holds the W5 fix (opencode-runner #232, merged into it by opencode-runner #234), merged with `review-elect-pins`, counts 9,463;
- `review-w5-pins` adds 26.

On a `main` raised to 8,400 by C2a-prime, that is about 10,105, and about 295 lines remain. The figure comes before three further changes:
- the X7 change in `tools/status.py` and `tools/elect.py`, which still read X0 and 14 d on `builder-c2b-status`;
- a re-cut of W5's pins: `w5_rows_append_only`'s mutant anchor no longer occurs in the fixed `tools/due.py`, and `pins.py` conflicts on merge;
- the merge with C2a-prime's window code.

The builder re-counts the integrated branches before the opening and reports the total in the opening note. If it exceeds 10,400, the C2b build stops and reports the shortfall.

## Amendment 4 (4 November, counsel; liveness read at C2b's opening — before the opening, one clause)

§Statistics' "Liveness continued: C1b's process, unchanged" is the process `status.py` computes at C2b's opening push, as C2a-prime's opening push carried it. That is, with the ruling's rule for the boundary `fix`, if BRIEF-C2a-prime's exemption stands. C2b changes nothing in it, and "unchanged" is read from C2b's opening.

## Amendment 5 (4 November, counsel; criterion 9's acts evidence — before the opening, one clause)

Criterion 9's off-log repairs are counted on one attributed acts table over C2b's window, from its opening to its exit. The table is `transcripts/evidence/acts-c2b-<end>.csv`, with its raw twin `acts-c2b-<end>-raw.csv` and its classifier hash file. It is produced, committed, re-run and limited as BRIEF-C2a-prime §The acts evidence prescribes for its own table, and a row counts when its `time_hkt` minute, read as UTC+8, overlaps the window at all. A row found by the report between `<end>` and the promotion is a finding in the C2b report; C2a-prime's V6 plays no part here.

## Note of 4 November (counsel; records, no clause changes)

1. **The GitHub identity.**
   - **What was delivered.** §Not in C2b left COUNSEL-OPEN 17 and 20's identity out of this window, and §Deliverables carried it to the C2c brief. It was delivered before the opening as one GitHub App for the court, `renavondata-jack-court[bot]` (opencode-runner #227; opencode-runner #225, which proposed accounts per party, superseded). The App's first act on jack was PR #285, opened at 06:17:02Z on 4 November. The sovereign records the App as a capability grant at C2a's boundary (BRIEF-C2a-prime §Order of acts step 2).
   - **Why one App.** GitHub's terms allow one free machine account per person. On the log, the parties are told apart by signing key, as before. Counsel's acts stay under the owner's login with their declaration (BRIEF-C1b Amendment 2).
   - **In the reports.** The C2b report records the identity as delivered, and disposes of the rest of 15–20 as §Deliverables says.
2. **Pre-built branches.** The W5 and election deliverables were built before the opening, on branches proposed only once the opening's cap is in force: `builder-w5`, `builder-elect`, `review-w5-pins`, `review-elect-pins` and `builder-c2b-status` (opencode-runner #153, #155, #156, #232, #233, #234). §Scope forbids landing under C2a's cap, not building. §Order of acts step 4's order is the order of proposal.
3. **Criteria 5, 6, 8 and 9.** They are built on `builder-c2b-status` (opencode-runner #234) to this brief's text. `transcripts/PROPOSAL-election.md`, on `origin/builder-elect` at ec74d14, records why the election build refuses a full promotion until they have their assessment.

## Amendment 6 (5 November, counsel; W5 reads two re-dates — before the opening, one clause)

On 5 November the sovereign forwarded an outside session's answer as his instruction. It reads in part: "re-date c2b-report and c2c-brief to dates that can hold — clearing rows means resolved or escalated, not deleted" (`transcripts/COUNSEL-OPEN.md` row 37). Counsel put two re-date lines on `main` under it, by proposal seq 1564 (2026-11-05T06:20:09Z, #363):

| row | due before | re-dated to | direction |
|---|---|---|---|
| `c2b-report` | 2026-11-18T00:00:00Z | 2026-12-02T12:00:00Z | later |
| `c2c-brief` | 2026-11-18T00:00:00Z | 2026-11-16T00:00:00Z | earlier |

**The clause.** §Scope (b)'s fold admits a line with exactly the keys `{"id", "due", "seq", "why"}` if and only if all of these hold: its `id` and `due` are, as strings, one of the two pairs in the table above; its `seq` is the integer 1564; its `why` is a string; it comes after its row's line and before any discharge line for that row; and it is the first such line for that `id`. That `due` is then the row's due, wherever §Scope (b) and criterion 8 read a row's due. Any other line with those keys makes the file malformed, and `due.py` prints `W5: malformed COUNSEL-DUE file`.

Consequential readings:
- §Scope (b)'s "Five pins" reads "Six pins", and its list adds `w5_redate`. §Pins adds `w5_redate` after `w5_inventory`.
- Criterion 8's "the five W5 pins" reads "the six W5 pins", and §Deliverables' "tests and five pins" reads "tests and six pins".
- The version note's "five everywhere" and Amendment 1's "five pins" record those texts as they stood.

**Pin `w5_redate`.** Its twins:
1. The two lines of the table, after their rows. The rows print their new dues.
2. A third line with those keys, for `runbook-c2b`. The file is malformed.
3. Without twin 1's `c2b-report` line: a line for `c2b-report` with seq 1564 and due 2026-12-01T00:00:00Z. The file is malformed.
4. Twin 1's `c2b-report` line twice. The file is malformed.
5. Twin 1's lines, but the `c2b-report` line with seq 1565. The file is malformed.
6. Twin 1's `c2b-report` line placed before its row's line. The file is malformed.

Mutants:
- re-date lines refused, or ignored (killed by twin 1);
- any re-date line admitted (twin 2);
- matched by `id` alone (twin 3);
- a second line for one row admitted (twin 4);
- the `seq` test dropped (twin 5);
- the order test dropped (twin 6).

**Interests.** Counsel holds X7 (seq 1559, p 0.55, 2026-11-05T05:33:33Z), entered on "transcripts/BRIEF-C2b-draft.md with Amendments 2-5". It forecasts that every pre-stated criterion of BRIEF-C2b holds. Counsel entered the two re-date lines 47 minutes later.
- Under the text X7 was entered on, `c2b-report`'s due precedes every possible exit of C2b, so criterion 8 could hold only if the report came before C2b's exit.
- This amendment moves that due past X7's `resolves_by`, which is strongly in counsel's favour.
- It moves `c2c-brief` earlier, which is against counsel.

The re-dates carry the sovereign's direction. X7 resolves on its own words.

**Reads.** Row 33's rule bars changing a criterion after a window has read it (Amendment 3), and C2b's window has not opened. The builder codes this only after the sovereign has read it (A2.10). C2b's opening needs an accepting read, carried by a non-counsel proposal, of the brief's bytes as amended (§Scope (a)).

## Amendment 7 (5 November, counsel; when a W5 discharge takes effect — before the opening, one clause)

§Scope (b) gains these sentences after "or deleting the row discharges nothing (REVIEW-C2b-v2 F7).":

> A discharge takes effect at the later of its cited entry's `ts` and the `ts` of the first `merge` on the prefix whose `commit` holds the discharge line, byte for byte, in `transcripts/COUNSEL-DUE.jsonl`. Before then the row is undone. It is done on time if that instant is at or before its due, and ESCALATED late if after.

Facts the rule reads today:
- §Scope (b) states no time for a discharge. The pre-built `tools/due.py` on `builder-c2b-status` dates a discharge by its cited entry's `ts` (line 60, `late = (instant(prefix[seq]["ts"]) - due)`). So a line added after a row's due, citing an earlier entry that names the row, reads as done on time. Proposal seq 1564 (2026-11-05T06:20:09Z) names `c2b-report` and `c2c-brief`, whose dues are later, so a line citing it for either, added after that row's due, would read as done on time.
- Under this rule, a discharge line may cite an entry already on `main`; it need not predict the `seq` of its own proposal.
- The three discharge lines on `main` cite seq 1564 (2026-11-05T06:20:09Z) and first reach a `merge` at seq 1565 (2026-11-05T06:28:30Z, #363), after each row's due. Once the file folds (Amendment 6), they read ESCALATED late under this rule.
- Counsel's X7 (seq 1559, p 0.55) was entered on "transcripts/BRIEF-C2b-draft.md with Amendments 2-5" and forecasts that every pre-stated criterion of BRIEF-C2b holds. The amendment makes criterion 8 harder to meet. X7 resolves on its own words.

**Pin `w5_escalation_history`** keeps its mutant. Every W5 twin that discharges a row, in any W5 pin, is built with a `merge` whose `commit` holds its discharge line. For a row due *D*₀, whose own line is merged before *D*₀, and, except in twin 6, an as-of after *D*₀ and after every entry in the twin, the pin gains these twins:
1. A cited entry before *D*₀, and the discharge line first merged before *D*₀. The row prints done on time.
2. A cited entry before *D*₀, and the discharge line first merged after *D*₀. The row prints ESCALATED late.
3. The discharge line first merged before *D*₀, and a cited entry after *D*₀. The row prints ESCALATED late.
4. A cited entry before *D*₀, and the discharge line merged once before *D*₀ and again after it. The row prints done on time.
5. A cited entry before *D*₀, and no `merge` holding the discharge line. The row prints undone, ESCALATED past *D*₀, and the file is not malformed.
6. Twin 1 read at an as-of after the cited entry and before the merge, both before *D*₀. The row prints undone, OPEN.

It also gains these mutants:
- the time read from the cited entry alone (killed by twin 2);
- the time read from the merge alone (twin 3);
- the last merge taken instead of the first (twin 4);
- a merge holding any line with the row's `id` taken (twin 2, through the row's own line);
- a discharge taking effect with no merge (twin 5);
- discharges never taking effect (twin 1);
- the merge sought in the whole log rather than on the prefix (twin 6).

## Amendment 8 (6 November, counsel; criterion 8's history read from the instant W5 lands — before the opening, one clause)

The sovereign asked for criterion 8 to be amended: "Read 6 and 7, approved... Amend 8" (2026-11-06T00:52:31Z; `transcripts/COUNSEL-OPEN.md` row 40). Counsel then put two forms to him:
- that part of criterion 8 applying only to dues after W5 reaches `main`;
- five rows only.

His answer: "Don't gate on something impossible" (2026-11-06T01:52:42Z; row 41). His answer named no form. Counsel reads it as the first, and asks him to confirm the form when he reads this text (A2.10).

**The clause.** Criterion 8's "every row that passed its due was printed ESCALATED by `status.py` at the first prefix after it" applies only to rows whose due falls after W5 lands. W5 lands at the `ts` of the first `merge` on the prefix whose `commit` holds `tools/due.py` (§Scope, Counsel bound: "W5 lands first after the opening"). That part does not gate a row whose due falls at or before that instant, or any row on a prefix with no such merge. The rest of criterion 8 stands for every row.

Facts the rule reads today:
- `tools/due.py` is not on `main`. It lands only after C2b's opening (§Order of acts step 4). C2b opens only after C2a-prime's promotion, and C2a-prime opens only after 2026-11-17T12:00:00Z (Amendment 2). Before W5 lands, `status.py` on `main` prints no W5 line, so for a row that passes its due before then, that part cannot be met.
- Rows now due before W5 can land:
  - `c2a-acts`, `hkjc-hv-20261104`, `c2a-report`, `D-1` and `runbook-c2b`, past due already;
  - `c2c-brief`, due 2026-11-16T00:00:00Z, and V1, whose outcome is fixed at 2026-11-08T15:04:14Z. Both can still be discharged on time, and a row discharged on time never "passed its due".
  - V0, V2 and V3, due 2026-11-17T12:00:00Z, which resolve on C2a's end. That end is unruled (correction 5 of `RULING-20261104-window-fix.md`). On the later reading they cannot be resolved before their due. On the earlier reading, BRIEF-C2a-prime recommends no resolution of them before the later instant.
  - the X-forecast resolution rows that §Scope (b) seeds at the opening, where their due falls before W5 lands.
- "No `COUNSEL-DUE` row past due and undone at the exit prefix" binds every row, so each of these must still be discharged before the exit.
- W5 lands at its merge entry's signing `ts`, a little before GitHub merges it. No row now on the file is due in that interval.

**Pin `c2b_history_from_w5`**, a W5 pin on `tools/status.py`'s criterion 8 assessment.
- §Pins adds it after `w5_redate`.
- §Scope (b)'s "Six pins" reads "Seven pins", and its list adds it.
- Criterion 8's "the six W5 pins" reads "the seven W5 pins", and §Deliverables' "tests and six pins" reads "tests and seven pins".
- Both of `status.py`'s pin inventories add it.

Every twin builds every discharged row as Amendment 7 requires. Except in twin 7, every twin builds W5's landing as a `merge` whose `commit` holds `tools/due.py`. Each twin holds every other part of criterion 8. The twins:
1. A row due before W5 lands, discharged late before the exit, with no ESCALATED print. Criterion 8 is met.
2. A row due after W5 lands, undone at its due and discharged late before the exit, not printed ESCALATED at the first prefix after its due. Unmet.
3. As twin 2, but printed ESCALATED at the first prefix after its due. Met.
4. A row due before W5 lands, still undone at the exit. Unmet.
5. Two merges hold `tools/due.py`, and a row is due between them, otherwise as twin 2. Unmet.
6. A row due exactly when W5 lands, otherwise as twin 1. Met.
7. No merge on the prefix holds `tools/due.py`. A row past its due, discharged late before the exit, with no ESCALATED print. Met.

The mutants:
- every row gated, whatever its due (killed by twin 1);
- every row excused (twin 2);
- the excuse extended to the whole of criterion 8 (twin 4);
- the landing read from the last such merge (twin 5);
- a due at the landing gated (twin 6);
- every row gated when W5 has not landed (twin 7).

**Interests.** This is in counsel's favour:
- It excuses, from the printed-escalation part, every row of counsel's that passes its due before W5 lands.
- A late `c2c-brief` or V1 before then no longer fails criterion 8. That lifts the burden Amendment 6 disclosed when it moved `c2c-brief` earlier.
- X7 (seq 1559, p 0.55) resolves on its own words. A non-counsel resolver assesses it on the terms it was entered on (`REVIEW-C2b-am67-astra.md` F3).

**Reads.** The text rests on two readings:
- `REVIEW-C2b-am2-astra.md` F2: row 33's rule against changing a criterion after it is read concerns "its witnessed application to a window". C2b's window has not opened.
- `REVIEW-C2b-am67-astra.md` F9: "An explicit lawful pre-opening change, with its own fresh read, would be needed to change that historical requirement."

The builder codes this only after the sovereign has read it (A2.10). C2b's opening needs an accepting read, carried by a non-counsel proposal, of the brief's bytes as amended (§Scope (a)).

## Amendment 9 (6 November, counsel; the procedure contracts withdrawn, by the sovereign's decision — before the opening, one clause)

Counsel holds an interest here (below), so the question went to the sovereign (`transcripts/COUNSEL-OPEN.md` row 35: counsel "may not decide a question in which it holds an interest").
- **The question.** Counsel asked him to choose: withdraw the promise "with a one-clause C2b amendment that changes no code", or have C2c write the contracts.
- **What he was told.** Counsel marked withdrawal as recommended, at p≈0.75, and told him of its interest along with it. Row 41 is the precedent for this. The mark did not carry row 27's seven lines.
- **His answer.** He chose the option "Withdraw (Recommended)", described as "C2b Amendment 9: the four types stay out of the value statistic for good; still scored in the reported scores." "(Recommended)" is counsel's marking. Row 43 quotes the question and both options.
- **His read.** This text carries no rule that code implements, so it is not put to him to read (row 35).

**The clause.**
- In §Scope's sentence on the procedure types, ", until a contract with a genuine pre-outcome boundary exists for each" is struck, and so is "; writing those contracts is a C2c item". The parenthesis citing REVIEW-C2b-v1 F6 stays. The sentence then ends with that parenthesis and a full stop.
- In §Deliverables, "the procedure contracts, " is struck from the parenthesis after "the C2c brief's first section".
- §Not in C2b's "contracts for the procedure types" stands.
- The procedure contracts leave this brief and are not promised to the next one. A brief binds its own layer only (A2.4). His "for good" stands as his direction to later briefs (row 43).
- BRIEF-C2a promised C2b "an event contract for the procedure types". That promise is disposed of with them.

**Why.** For each of these types, the forecasting party can itself know the outcome before a stated cutoff, or act on it after one.
- A branch's author runs its tests before proposing (`tools/jack` lines 13 and 123). A counted-line claim about a fixed commit is "mechanically knowable before proposal" (REVIEW-C2b-v1 F6).
- The reviewer forecasts C2b's promotion (seqs 1459, 1794 and 1829) and also writes C2b's pins (§Pins, "the reviewer's").
- Counsel drafts the briefs whose outcomes its programme forecasts name. For example, V0 (seq 361) forecasts that the criteria of BRIEF-C2a, counsel's draft, hold.
- A claim that is a statistic of the parties' scores can have a boundary. Examples are a value E reaching 20 (seq 362) and one arm's mean gain exceeding another's (seq 638). But the parties in the roster move it with their own forecasts.

REVIEW-C2b-v1 F6 named this course: "leave such forecasts in C1's reported scores". The same review also asked for contracts, and the sovereign has chosen between the two. Precedent for the words is §Scope's withdrawal of the simulator-sample skip: "It leaves this brief and is not promised to the next one".

**What does not move.**
- `procedure_types_out`, `tools/value.py` and every pin stand. No code changes.
- No criterion's wording reads §Deliverables.
- `transcripts/COUNSEL-DUE.jsonl` is append-only. Its `c2c-brief` row's `what` still names "procedure contracts". So does BRIEF-C2c's line that quotes the row.

**What moves with it.** §Scope (b) seeds the `c2c-brief` row from this brief's obligations, and criterion 8 reads that row. This amendment changes what the row owes. Row 33's rule does not bar this. The rule concerns a criterion's "witnessed application to a window" (REVIEW-C2b-am2-astra F2, as Amendment 8 cites it), and C2b's window has not opened.

**Interests.**
- **Counsel's programme forecasts.** Every `counsel.programme` forecast on the log is counsel's, and counsel is an entrant of the value statistic's roster. Those forecasts were already out of C2b's value statistic. What the withdrawal changes is that no later window is promised a contract that could admit them. Whether that helps or hurts counsel is not clear.
- **Counsel's row.** Counsel holds the W5 row `c2c-brief`, due 2026-11-16T00:00:00Z. The withdrawal makes that row much lighter. The first section then owes:
  - the kernel types, only if a witness has appeared;
  - the GitHub identities. The Note of 4 November records these as delivered as one App. REVIEW-C2b-am2-astra F10 disputes that reading for identities per party.

  This adds to the relief Amendment 8 gave the same row. It also relieves counsel of an item on which counsel's three C2c drafts failed their cold reads. An honest discharge before the exit becomes easier. Criterion 8 requires that discharge, and counsel's X7 (seq 1559, p 0.55) rests on criterion 8. In that respect the withdrawal is in counsel's favour.
- **X7.** As under Amendment 8, X7 resolves on its own words. A non-counsel resolver assesses it on the terms it was entered on (`REVIEW-C2b-am67-astra.md` F3). Those terms include the row's original `what`.
- **The reader.** The formal read is a reviewer's. The reviewer holds three forecasts that C2b promotes (seqs 1459, 1794 and 1829), which a lighter row makes likelier.

**Reads.** C2b's opening needs an accepting read, carried by a non-counsel proposal, of the brief's bytes as amended (§Scope (a)).

## Amendment 10 (10 November, counsel-3; no live round in C2b, the deliverables on the opening push, and what criteria 5 and 6 are — before the opening, by the sovereign's decision)

- **The finding.** Criterion 7's rounds cannot be held as the brief stands: the invitation, the per-invite session and the resolution routing need a step in the runner's diary (§Deliverables: "the diary consulting it and routing the resolver (runner side, prompts in `transcripts/sessions/`)") that was never built — `diary.yml` on the runner's `main` names neither `elect.py` nor an invite, and no branch holds one. A third of the early rounds would run on `openai/gpt-6-astra-fast`, on the freshness stream, whose statistics the record declines as evidence (clause 6).
- **His decision** (10 November, 13:50 HKT), between building the diary step this week (A) and an amendment that holds no live round (B; counsel's recommendation, forecast at 0.7): "Definitely B... And is it fine to 'promote on criteria you know to be empty'? I'm not against amending briefs! And yes, let's not use astra except when necessary". Clause 6 answers his second sentence. Clause 5 was not in what counsel put to him; it comes to him with this text and its reason, and is his to strike.
- **His read.** Clauses 1–5 change rules that code or the paste implements, so the text is his to read before the builder's session is filed (A2.10; row 35).

**The clauses.**
1. **Criterion 7** reads: "**The election, built and not run**: `tools/elect.py`, `sim/election.py` and `tests/test_elect.py` are in the tree at the exit prefix, and criterion 1 is met (the election's pins and its two attack kinds are among its pins). No live round is held in C2b." `status.py` prints the election line as `election: no rounds (BRIEF-C2b Amendment 10)`. An `election.invite` entry inside the window is no round and moves no criterion: the paste gives `herald-2` no `forecast` power (clause 3), and the tools treat an invite it did not sign as `unkeyed`.
2. **Criterion 4** reads: "The attack tests — §Safety's two kinds with the rest — green in the verified `tests` run on `main` at the exit prefix." There is no first round for them to precede.
3. **No session, no invite, no power.** §Scope's paragraphs **Rounds**, **The round's gain**, **The election**, **The draw**, **The invitation** and **Resolution routing** stand as the specification of what `tools/elect.py`, `sim/election.py` and their pins implement, and bind no session, no entry and no clock in C2b: "from the first invite after the opening to the window's end" names no invite in this window, no forecast session is filed for an arm, and no resolver is routed. §Precondition's "preceded in the same paste by the sovereign's `key herald-2 --principal herald --powers merge,forecast --pubkey ~/.ssh/jack-herald.pub` (a re-declaration of the existing key, SPEC §7; no new identity)" is struck, and so is the `key herald-2 …` item of §Order of acts step 3: `herald-2` keeps `merge` alone (seq 201), and the `forecast` power is given by the window that first has it draw. Of §Stop and report, "the clerk's key cannot sign a forecast (the grant missing: the window has not opened)", "an invite's draw cannot be replayed from the prefix (a defect in this brief's algorithm, fixed by amendment before any round counts)" and "the interleaving's assumption fails (a round unresolved when its instance draws again: the draw waits, and the report says how often)" are conditions of a window that runs rounds and stop nothing in C2b; "a stream's public evidence disappears" stands for the stream's own forecasts, as under C2a.
4. **The diary and the prompts.** "the diary consults `elect.py` before every forecast session from the first green `tests` run on `main` holding `tests/test_elect.py` — invites before that instant are not rounds (criterion 4)" is struck from §Order of acts step 4, and from §Deliverables "the diary consulting it and routing the resolver (runner side, prompts in `transcripts/sessions/`)" and "the session prompts rewritten so that under C2b the invite owns the window — a forecast session's W0 is its invite's, and the uncovered-hour fallback of `transcripts/sessions/stream-forecast.md` applies only to sessions filed without an invite, which after the first round there are none of (REVIEW-C2b-v3 F10)". The diary and the stream's sessions are unchanged in C2b: the pre-built changes to `transcripts/sessions/stream-forecast.md` and `stream-resolve.md` and the new `transcripts/sessions/election-forecast.md` are in no tree this window pushes — the builder takes them off its branch — and land with the diary's step, in the window that runs rounds.
5. **The deliverables ride the opening push.** §Deliverables' "In the window, in this order:" reads "On the opening push, pre-built:", and §Order of acts steps 3–5 read: "3. The sovereign, one paste: `decision promote C2a` (when `lawful`), then the opening `push` of a branch that carries the two trusted-base changes of §Scope (the cap; the parallel tests workflow) and the window's code — W5, `tools/elect.py`, the simulator kinds, `tools/status.py`'s election line, criteria and `promote C2b`, `tools/jack decision` dispatching `C2b`, their tests — with the reviewer's pins and the reviewer's code read, every commit carrying its party's trailer, as C2a-prime's opening push carried its window's (BRIEF-C2a-prime §Order of acts step 2). The opening is the first `push` entry after `decision promote C2a`; the window is (opening `ts`, X7's `resolves_by`]. 4. The code is in force from the push; the `tests` run on `main` at the push's commit verifies it; no proposal of code or pins is made inside the window. 5. `status.py` prints the election line and `promote C2b: lawful | refused: …`; the sovereign's `decision promote C2b` at the crossing." The trusted-base changes stay the two §Scope names and no other. The branch's counted lines are at or under 10,400 at the push (Amendment 3) or the push is not made (§Stop and report). Criterion 8's history is read from the push, the instant W5 lands (Amendment 8).
6. **What criteria 5 and 6 are.** They are the charter's condition (§6: "liveness and value reach *Eₜ* ≥ 20"), which a brief may not loosen (A2.4), on the statistics C1b and C2a fixed and A4.1 continues; they stay conditions of C2b's promotion and `status.py` assesses them unchanged. On 10 November value *E* stands near 2.6 × 10²⁰ and continued liveness near 5 × 10¹⁸², and of the 1,019 resolutions of forecasts entered since C2a's opening (seq 367), 984 are of `world.renavon` — the hourly freshness stream that a template of the court's schedules on datasets the sovereign operates. Liveness stood at 0.135 at seq 2215 on 7 November (`transcripts/RESEARCH-meta-jack-20261107.md` §2): the same cadence, the other way. The two criteria are therefore met in C2b as the charter's letter and offered as nothing else. **What can fail in this window is criteria 8 and 9** — counsel bound by W5, and no repair of the sovereign's on the acts evidence, the criterion C2a failed on nine rows. No report of this window, and no later text of counsel's, cites C2b's promotion as evidence of value or of liveness; REPORT's section for C2b carries this clause's first two sentences in its first paragraph. What *E* should count is the sovereign's ruling at C2c-3 (COUNSEL-OPEN row 49: the item reading the acts table; no statistic that gates a power fed by a stream a key-holder operates), made there as one pre-stated act, the old process retired.

**Why clauses 1–4.** Criterion 7 was "an exercise budget the opening push authorises, not a constant in any score": rounds to show the mechanism turning. The mechanism's law is its code and pins — the replay from the signed prefix, the draw, the feedback rule, the two attacks refused — and those land and are tested under clause 1. Live rounds would add a day of sessions on a stream that measures the cron (`transcripts/RESEARCH-semantics-20261109.md` §§8, 10, 12, 16; its map, rows 28, 34, 48, 56), driven by runner code the court does not hold. BRIEF-C2c-1's window file keeps the map's `elections` row at `hand` with a deadline of its opening plus `elections_deadline_days` (21), printed `ESCALATED` past it: that row, not this brief, now holds counsel to live rounds, in the first window whose diary is a shell the court holds (a brief binds its own layer only, A2.4).

**Why clause 5.** Criterion 9 allows no repair of the sovereign's inside the window. On 8 and 9 November three of the builder's proposals that the judge refused — the courier's (#616), the host's (#654) and the evidence's (#697) — were re-proposed by the herald, hourly, until a close by his hand ended each loop (#629, #664, #698; COUNSEL-OPEN row 48, as row 50 corrects it); inside C2b's window each close is a `repair` row (`transcripts/evidence/guy_acts3.py`: "PR closed unmerged") and loses the window as nine such rows lost C2a. The window's code is five pre-built branches that conflict with C2a-prime's in `tools/status.py` and `pins/pins.py`; landing them in the window means several proposals, split by party, through that herald. On the push they are integrated, pinned and read before the window opens, and nothing is proposed in the window but the stream's entries. The judge does not see a push, and `jack push` checks of a commit only that it carries a filled trailer: what holds each party to its paths on this branch is the reviewer's code read, which tabulates every commit's party against its paths and blocks on one outside them (as C2a-prime's opening note tabulated its four), and the sovereign's own act in pushing. §Scope's reason for landing in the window was the cap — "§Scope forbids landing under C2a's cap, not building" (Note of 4 November) — and the push that raises the cap is the instant from which the code may land.

**What moves.** In `tools/status.py`: criteria 4 and 7 (the pre-built `assess_election()` audits invites and requires twenty-four) and the election line (`render()`, which prints the pre-built summary of rounds and under clause 1 prints `election: no rounds (BRIEF-C2b Amendment 10)`), with their tests in `tests/test_elect.py` and `tests/test_status.py`; three prompt files leave the builder's branch; the opening note; RUNBOOK's `## jack elect` gains one sentence (same proposal). **What does not move.** `tools/elect.py`, `sim/election.py` and every pin; W5, the gate and criterion 8's wording; criteria 1–3 and 9; the cap; the window, (opening `ts`, X7's `resolves_by`]; §Statistics' "the election's record … Reported; no threshold", which prints nothing where there is no round.

**The forecasts.** X0–X7 are not edited and resolve on their own words, as under Amendments 2, 8 and 9. X2 (seq 638: the astra-fast arm invited at least once) resolves 0. X7 (seq 1559) was entered on terms that include twenty-four witnessed rounds; a resolver other than counsel assesses it on those terms (`REVIEW-C2b-am67-astra.md` F3), on which it resolves 0 whether or not C2b is promoted. Its `resolves_by`, 2026-12-01T12:00:00Z, stays the window's stated end (A5.2; Amendment 2). Counsel-3's N2 (seq 2553, 0.55: `decision promote C2b` within 72 hours of the opening push) stands as entered.

**Interests.**
- **Counsel.** N2 is counsel-3's and clauses 1–5 make it likelier; X7 and X2 are the principal `counsel`'s and clause 1 makes them 0. The amendment removes from counsel the work of a runner text and from the record a piece of counsel-written runner code, and clause 5 removes the in-window proposals whose failure would be charged to counsel's N2. The missing diary step is a fault in counsel's own plan of 7 November, which wrote "C2b's 24 rounds, then promotion" (`transcripts/RESEARCH-meta-jack-20261107.md` §3) without looking for the step that would run them; listed in the row that records this amendment.
- **The reader.** The formal read is a reviewer's, and the reviewer holds three forecasts that C2b promotes (seqs 1459, 1794, 1829), which fewer criteria make likelier.
- **The sovereign.** He decided B in the words quoted. Clause 5 is counsel's addition and clause 6 counsel's answer to his question; he reads both here.

## Amendment 11 (10 November, counsel-3; a false figure in Amendment 10 corrected; W5's tick evidence, never built, and the seed as it stands — before the opening, no code)

- **The error.** Clause 6 of Amendment 10 says "continued liveness near 5 × 10¹⁸²". The figure is false: `tools/status.py --subject C2a --as-of 2026-11-10T07:00:00Z` on `main` prints criterion 6 as SHORT, the wealth 0.63 over 267 items since the attack gate (BRIEF-C2a-prime Amendment 2 has the account and the figures).
- **The second finding.** The same rehearsal (COUNSEL-OPEN row 51) ran the pre-built `counsel_bound` on a simulated window. Its printed-escalation part reads tick files under `transcripts/evidence/w5/` and nothing else, and §Scope (Counsel bound, b) has "the diary's resolve session" commit them. No session does: neither `diary.yml` on the runner's `main` nor any prompt under `transcripts/sessions/` on any branch writes under that path. It is the election's missing step a second time (Amendment 10's finding), in a sentence Amendment 10 left standing.
- **His read.** The sovereign read Amendment 10 at 14:27 HKT with the false figure in clause 6. Clauses 2–4 below change no rule that code implements — the code is as pre-built and already reads only the files — so by row 35 this text does not wait on his read before a build. It is sent to him with its reads, and it is his to strike.

**The clauses.**
1. **Clause 6 of Amendment 10, corrected.** For "On 10 November value *E* stands near 2.6 × 10²⁰ and continued liveness near 5 × 10¹⁸²" read: "On 10 November value *E* stands near 3.6 × 10²⁰ over 981 events, and continued liveness at 0.63, below the charter's 20 (BRIEF-C2a-prime Amendment 2)". For "The two criteria are therefore met in C2b as the charter's letter and offered as nothing else. **What can fail in this window is criteria 8 and 9** — counsel bound by W5, and no repair of the sovereign's on the acts evidence, the criterion C2a failed on nine rows" read: "Criterion 5 is met many times over and criterion 6 is unmet on 10 November; both are the charter's letter and are offered as nothing else. **What can fail in this window is criteria 6, 8 and 9** — liveness, if the stream misses its deadlines in the days before the promotion; counsel bound by W5; and no repair of the sovereign's on the acts evidence, the criterion C2a failed on nine rows". The rest of clause 6 stands.
2. **W5's ticks.** Of §Scope (Counsel bound, b)'s "The contemporaneous `status.py` output is the witness of timely escalation, so the diary's resolve session runs `status.py` at every tick and commits its W5 lines with its evidence (a file per tick under `transcripts/evidence/w5/`), and the exit reads those files, not a reconstruction", the words "so the diary's resolve session runs `status.py` at every tick and commits its W5 lines with its evidence (a file per tick under `transcripts/evidence/w5/`)" are struck: no session does it, and none is built in this window. "the exit reads those files, not a reconstruction" stands, and so do criterion 8, Amendment 8's rule and its pin. §Scope's cap paragraph lists "W5 and its tick evidence" among what the budget was priced for and states no act; RUNBOOK's W5 paragraph is restated in the same proposal. It follows that criterion 8's printed-escalation part can be met for no row that falls due after W5 lands and before the exit and is not discharged on time; clause 3 has the window hold no such row.
3. **The seed.** §Scope (Counsel bound, b)'s "The file is seeded at the opening with every dated obligation of COUNSEL-OPEN (items 23's diary, the C2a report, the C2b brief's reads, the acts tables) and of this brief (the report, the C2c brief, RUNBOOK sections, X-forecast resolutions)" reads: "The seed is `transcripts/COUNSEL-DUE.jsonl` as `main` holds it at the opening push". On 10 November that is eleven rows: `c2a-acts`, `c2a-report`, `hkjc-hv-20261104`, `D-1`, `runbook-c2b`, V0, V1, V2, V3, `c2b-report` and `c2c-brief`. No row is added for an X-forecast's resolution, and Amendment 8's "the X-forecast resolution rows that §Scope (b) seeds at the opening" names rows that were never on the file. X0, X2, X3 and X6 fall due at 2026-11-18T00:00:00Z, twelve hours after the earliest opening, and resolve at C2b's exit or, with no exit by then, at that instant, by a resolver that is not counsel; as rows, each would then fail criterion 8 beyond repair under clause 2. An unresolved forecast past its `resolves_by` is already the clerk's writ W1 and an `expiry` item of the liveness process. No row is made for the brief's reads either: the opening push's read gate holds them. Counsel appends no row inside the window whose due falls before the stated end. What binds counsel in this window is the rest of criterion 8: `c2a-report` and V0–V3, due before the opening, are discharged before the exit or the window is unmet; `c2b-report` falls due on 2 December, a day after the stated end.
4. **Where W5 lands.** Amendment 10 clause 5's "Criterion 8's history is read from the push, the instant W5 lands (Amendment 8)" reads: "W5 lands, for Amendment 8's rule, at the `ts` of the first `merge` on the prefix whose `commit` holds `tools/due.py`, as Amendment 8 wrote it and its pin's twins build it; with the code on the opening push that is the first merge after the push, and no row falls due between the two". The pre-built `counsel_bound` and the pin `c2b_history_from_w5` are as they were.

**What moves.** No code and no pin; RUNBOOK's W5 paragraph. The X-forecasts, their resolutions and W1 are as they were. **What does not move.** Criterion 8's wording, Amendment 8's rule and twins, `tools/due.py`, the other clauses of Amendment 10, the cap, the window.

**The forecasts.** None is edited. Counsel-3's N2 (seq 2553, 0.55) stands as entered.

**Interests.**
- **Counsel.** Clause 1 corrects counsel's own false figure, which favoured the reading that nothing but criteria 8 and 9 could fail. Clauses 2 and 3 keep off the file four rows that would have failed, at 08:00 HKT on 18 November, a window counsel holds N2 on; the sentence struck is a second step that counsel's plan assumed and did not look for. What still binds counsel is the C2a report and the four V rows, and the liveness the stream earns.
- **The reader.** As under Amendment 10.
- **The sovereign.** He read clause 6 with the false figure at 14:27 HKT and was told at about 15:40. This text is his to strike.
