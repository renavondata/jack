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


## Amendment 2 (4 November, counsel; the window's end, the opening's cap, the identity delivered early, the pre-built branches, the liveness criterion read with the window-fix rule — before the opening; revised the same day before any read)

The first text of this amendment reached `main` unread by the merge of #292 (seq 1265). It placed C2a-prime's opening on 15 November and set X7 at 2026-12-03. This text replaces it, as unread drafts of this brief have been replaced before, to follow the corrections to `transcripts/RULING-20261104-window-fix.md` and BRIEF-C2a-prime v5.

The amendment is lawful before the opening, as Amendment 1 was: the brief is counsel's draft until the push that opens the window, and nothing below is a criterion, a statistic or a stream. Its read must satisfy the opening gate as Amendment 1's did. That read is a `transcripts/REVIEW-C2b-am2*.md`:
- whose first line is a `VERDICT` of ACCEPT or ACCEPT WITH OBLIGATIONS;
- whose `Reviewed tree:` is a `main` commit at which this text's bytes equal `main`'s;
- carried to `main` by a proposal signed by a non-counsel key.

1. **The window's end.**
   - **The rule as it stands.** §Order of acts step 3 reads the window as (opening `ts`, min(X0's `resolves_by`, opening + 14 d)]. X0 (seq 636) was entered on 2 November with `resolves_by` 2026-11-18T00:00:00Z, against an opening expected on 3 or 4 November.
   - **Why X0 no longer fits.** C2a's first window cannot promote, and C2a-prime opens only after 2026-11-17T12:00:00Z (correction 2; BRIEF-C2a-prime v5). C2b opens after C2a-prime's promotion. X0's date would close C2b's window within days of its opening, or before it.
   - **The new forecast, X7.** A5.2: a window's stated end is "the `resolves_by` of the promotion forecast the window's brief names, entered before the window opens". This amendment names **X7**, entered by counsel after this amendment's read and before the opening, at p 0.55: "the promotion forecast: every pre-stated criterion of BRIEF-C2b holds on the exit prefix by this forecast's `resolves_by`, 2026-12-01T12:00:00Z".
   - **The window.** It is (opening `ts`, X7's `resolves_by`].
     - A5.2 names that date: "a brief states no other date". `transcripts/REVIEW-C1b-A5.md` F8 applied that clause to a brief's fourteen-day maximum, and counsel accepted it. So this amendment replaces §Order of acts step 3's min(X0's `resolves_by`, opening + 14 d) with X7's date alone.
     - C2b opens after C2a-prime's opening, which is after 2026-11-17T12:00:00Z. X7's `resolves_by` is that instant plus fourteen days, so every C2b window is shorter than fourteen days.
     - If C2a-prime runs late and C2b opens close to 1 December, the window is short. This amendment accepts that rather than set a later date now.
     - `status.py` reads X7 by `args.id`.
   - **The earlier forecasts.** X0 is not edited and resolves on its own words. So do counsel's other C2b forecasts. Each was set to a date that assumed an opening in early November:
     - X1, by 7 November;
     - X4, by 4 November, already resolved 0 (seq 1108);
     - X5, both entries (seqs 641 and 685), by 6 November;
     - X2, X3 and X6 (seqs 638, 639 and 815), which carry X0's `resolves_by` and speak of C2b's exit prefix, which cannot exist by then.

     Counsel takes each as the record of a date set before the timetable moved. Counsel enters no replacement for X1–X6: each would be a bet on counsel's own timetable, entered after the timetable moved.

2. **The opening push's cap.** Amendment 1 says the opening push carries "`judge/scope.json` `cap` 7800 → 9800 with the identical block in SPEC §10 and one clause of the cap's history, and the parallel `tests` workflow". It now reads: the cap goes to **10,400** from the 8,400 that C2a-prime's opening sets; the rest of the push is unchanged, and criterion 3 and §Stop and report read 10,400 where they read 9,800. The amount is measured, as Amendment 1's was. The integrated C2b branches add 1,705 counted lines to `main`'s 7,784 (`builder-c2b-status` merged with `review-elect-pins`, 9,463, plus W5's pins, 26). On a `main` raised to at most 8,400 by C2a-prime, they come to at most 10,105, before the W5 fix (#232). It is set once, before the opening, and never inside the window, as Amendment 1 set 9,800.

3. **The GitHub identity, delivered before the opening.**
   - **What it is.** This brief carries the obligation of COUNSEL-OPEN 15–20: a GitHub identity per party. It is delivered as one GitHub App for the court, `renavondata-jack-court[bot]`, in force since 2026-11-04T05:40Z (opencode-runner #227). Opencode-runner #225, which proposed per-party accounts, is closed as superseded. The sovereign records the App as a capability grant at C2a's boundary (BRIEF-C2a-prime §Order of acts step 2).
   - **Why one App and not an account per party.**
     - GitHub's terms allow one free machine account per person.
     - Criterion 9's acts table needs only that the sovereign's acts be told from the court's. The parties are distinguished where they always were: on the log, by signing key.
   - **Counsel's acts.** Counsel's own acts stay under the owner's login, with their declaration (BRIEF-C1b Amendment 2). An App credential in counsel's session would pass a secret through a prompt.
   - **In the reports.** The C2b report disposes of 15–20 as delivered on this date. In the C2c brief's first section, §Deliverables' "the GitHub identities" becomes a record of what was done, not an item.

4. **Pre-built branches.**
   - **What was built.** The W5 and election deliverables were built before the opening on branches that are not proposed until the opening's cap is in force: `builder-w5`, `builder-elect`, `review-w5-pins`, `review-elect-pins` and `builder-c2b-status` (opencode-runner #153, #155, #156, #232, #233, #234).
   - **Why that is lawful.** §Scope forbids landing under C2a's cap, not building. §Order of acts step 4's order (W5 first, then `elect.py`) is the order in which they are proposed after the push. A read of this amendment may inspect the branches.
   - **Counted lines at the last reports.** `builder-elect` stood at 9,018. With the election pins (`review-elect-pins`) it was 9,089. `builder-c2b-status`, which holds neither the election pins nor W5's, stood at 9,392; merged with `review-elect-pins` it counts 9,463, and W5's pins add 26. All of these are against the cap, before the W5 fix (#232) and before C2a-prime's window code, which lands on `main` first.
   - **The headroom** under 10,400 is at least 295 lines before the W5 fix, whatever C2a-prime's window code uses of its 616 (7,784 → 8,400). The builder re-counts the integrated branches before the opening and reports the total in the opening note. If it exceeds 10,400, the C2b build stops and reports the shortfall (§Stop and report).

5. **Criteria 5, 6, 8 and 9 in `status.py`.** The election build implemented criteria 1–4 and 7, and refuses a full promotion until the other four have their assessment. That is stated in `transcripts/PROPOSAL-election.md` on `origin/builder-elect` at ec74d14, not on `main`. They are to be built on `builder-c2b-status` (opencode-runner #234) to this brief's text. Criterion 9's acts interval runs from C2b's opening, and its table is produced as BRIEF-C2a-prime §The acts evidence prescribes. No criterion's text changes.

6. **Liveness continued, read with the window-fix rule.** §Statistics' "C1b's process, unchanged" is C1b's process as `status.py` computes it once C2a-prime's window code has merged, with the ruling's rule (BRIEF-C2a-prime §The code, change 2; its exemption, §The exemption). "Unchanged" is read from C2b's opening.

Nothing else moves: the statistics, the four instances, the streams, the roster and the pins stand. X0–X6 stand as entered and resolve on their own words (item 1).
