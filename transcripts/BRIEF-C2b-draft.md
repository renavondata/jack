# BRIEF-C2b — the election (draft v2, counsel, 2 November 2026)

v2 answers `transcripts/REVIEW-C2b-v1.md` (gpt-6-astra, BLOCK on F2, F3, F4, F6, F9; obligations F1, F5, F7,
F8, F10) as `transcripts/REPLY-REVIEW-C2b-v1.md` sets out. The gain is normalised to [0, 1] from the legal
loss endpoints; the draw is a verifiable random function of the clerk's key, not the public clock; delayed
feedback is handled by the interleaving reduction with its own bound; the roster is fixed at the opening and
holds no base arm; the invitation's `p` forecasts the success event and the selection propensity travels
separately in `args`; the procedure types leave the value statistic; the resolver is routed away from the
elected principal; the gates that bind counsel are built *before* the opening, under C2a's cap, so that the
opening push is the first act they gate.

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
`main`; the two gates of §Counsel bound merged on `main` under C2a's cap, before the push; counsel's
forecasts X0–X3 entered; `transcripts/COUNSEL-DUE.jsonl` seeded; the opening push in force (the cap), preceded
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
- **Rounds.** One round per freshness window of BRIEF-C2a Amendment 2 (hourly, six datasets, the window
  `[H+2, H+3)`), from the first invite after the opening to the window's end. HKJC per race is **outside the
  election** (two forecasters per race, as C2a); its forecasts are not rounds and are not importance-weighted.
- **The round's gain.** For the invited arm *k* at round *t*, ℓₖ,ₜ = the mean over the six events of the
  per-mille-clipped log-loss ℓ(*q*, *Y*) = −ln *q*(*Y*) = ln 1000 − ln *n*, where *n* ∈ {1, …, 999} is the
  per-mille probability the forecast gave the outcome that occurred; a missing forecast, a missing evidence
  page or an event unresolved by the invite's deadline counts at the maximum ln 1000 (*n* = 1) — a bad round
  is never discarded. Gain *gₖ,ₜ* = (ln 1000 − ℓₖ,ₜ) / ln 999 = (mean of the six ln *nᵢ*) / ln 999 ∈ [0, 1]
  exactly, in floating point too, because it is computed in the second form (*n* = 1 gives 0, *n* = 999 gives
  ln 999 / ln 999 = 1; REVIEW-C2b-v1 F2). *B* = ln 999 of A4.4 is untouched by this: it bounds a loss
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
  *πₖ,ₜ* = (1 − γ) *wₖ*/Σ*w* + γ/*K* the **selection propensity**, γ = min(1, √(*K* ln *K* / ((e − 1) *gⱼ*)))
  = 0.15111, η = γ/*K* = 0.05037 (Auer, Cesa-Bianchi, Freund & Schapire 2002, Theorem 3.1; every constant is
  the theorem's, printed here only so the pin has a number to kill). The importance weight uses the
  propensity saved in the invite, never a later one. Expected weak regret per instance
  ≤ 2√((e − 1) *gⱼ K* ln *K*) = 43.62 gain units; over the four instances ≤ 174.5 against the best fixed arm
  in at most 336 rounds — stated as what it is, a bound on expectation under the theorem's assumptions, which
  the next two items secure, and loose, as every EXP3 bound at this horizon is; the election is an entrant
  (§5), and its record, not its bound, is what the report shows.
- **The draw.** The theorem needs a draw the entrants cannot anticipate and the record can replay. The
  clerk's draw at round *t* is the uniform variate *u* = SHA-256(σ)/2²⁵⁶, σ = the 64 raw bytes of the clerk
  key's Ed25519 signature (`ssh-keygen -Y sign -n jack-election`, namespace fixed) over the ASCII string
  `election.invite <stream> <W0>` — `herald-2` is `ssh-ed25519` (log seq 201) and Ed25519 signing is
  deterministic (RFC 8032 §5.1.6), so σ is a function of the key and the round and nothing else,
  unpredictable to anyone without the private half and verifiable by anyone from the public half (a
  verifiable random function in its signature form, Micali, Rabin & Vadhan 1999). σ is recorded in the
  invite's `args.sigma` (base64); the arm is the one whose cumulative propensity interval contains *u* (arms
  in roster order, half-open intervals). Pin `draw_replays_from_prefix`: the replay recomputes Ĝ, *π* and *u*
  from the signed prefix (ordered by `seq`, never by `ts`) and σ, verifying σ against `herald-2`'s pubkey and
  requiring the recomputed `args` (weights, propensity, instance) to equal the recorded ones byte for byte;
  an invite whose draw does not replay is `rigged_election` and the diary files no session on it.
- **The invitation.** Before each forecasting session the clerk enters a `forecast` of type `election.invite`:
  claim "stream <s>, window <W0>: the invited entrant <principal, model> achieves a mean clipped log-loss on
  the window's six events below the base rate's" (the base rate at each event's resolution as `tools/value.py`
  defines it; the comparison strict; a tie or a missing event is 0); `p` = **the clerk's forecast of that
  success event**: the prequential Laplace rate of the invited arm's past rounds' successes, (*s* + 1)/(*n* + 2)
  in per mille, clipped to 1–999 — a proper-scored statement about the event the resolution decides
  (REVIEW-C2b-v1 F4), and *not* the selection propensity, which travels as `args.propensity` (the float's
  shortest round-trip repr, the quantity the importance weight divides by; never the rounded `p`) with
  `args.instance`, `args.weights` (Ĝ per arm before the draw, same repr), `args.sigma`, `args.gamma`,
  `args.eta`, `args.roster`; `args.window_utc`, `args.stream`, `args.principal`, `args.model`; `resolves_by`
  = window end + 2 h. The invite's key is (stream, W0): the first invite for a key stands and a second is a
  `revision`, not a round. The event's cutoff is `W0` (the invite is entered at about H+0:15, the window starts
  at H+2). The diary files the forecasting session for that principal and model with the invite's seq in the
  issue; the session's six forecasts carry `args.invite` = that seq. An invite whose session did not run, or
  ran under another key or model, still resolves — at the maximum loss, 0 — and counts in the round
  (criterion 7).
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
- **Counsel bound** — built **before the opening**, as ordinary tools proposals under C2a's cap, so the
  opening push is the first act the gate refuses or admits (REVIEW-C2b-v1 F7):
  (a) `jack push` refuses a push whose branch changes `judge/scope.json`'s `layer` or `cap` (an opening) unless
  `main` holds, for the layer's `transcripts/BRIEF-<layer>-draft.md`, a `transcripts/REVIEW-<layer>-*.md`
  whose `VERDICT:` line is `ACCEPT` or `ACCEPT WITH OBLIGATIONS`, whose `Reviewed tree:` names a commit on
  `main` at which the brief's bytes equal the current bytes, and whose entry commit carries a `Proposer:`
  trailer of a party other than counsel; an empty file, a missing verdict or a counsel-authored review does
  not count. Pins `push_without_read_refused`, `read_of_this_text`, `read_not_counsels`.
  (b) The clerk gains W5: every row of `transcripts/COUNSEL-DUE.jsonl` — `{"id", "due", "what", "done":
  {"seq": n, "what": "<the act>"} or null}` — is a writ held by counsel, ESCALATED past `due`; a row is
  discharged only by a `done` whose seq is a valid entry on the prefix (not by a bare integer, not by deleting
  the row — rows are append-only and the clerk refuses a file whose earlier rows changed); the file is seeded
  at the opening with every dated row of COUNSEL-OPEN (items 23's diary, the C2a report, the C2b brief's
  reads, the acts tables), and pin `w5_inventory` checks the seeded rows are present; escalation history is
  kept in the clerk's output (a row completed late shows ESCALATED-then-done). Pins `w5_overdue_escalates`,
  `w5_done_is_an_entry`, `w5_rows_append_only`, `w5_inventory`.
  (c) COUNSEL-OPEN 13's rule — every recommendation to the sovereign that asks an act is a forecast — stays
  as it is, a standing rule; `status.py` prints, under its honest name, "sovereign acts in the window with no
  counsel forecast naming them before the act" as a reported line, not a W4 count (REVIEW-C2b-v1 F7).
- **The cap.** The budget is **8,900** (7,650 counted today; four EXP3 instances with replay, the VRF draw,
  the invite verb, the resolver routing, the two gates, status and decision integration, tests, two simulator
  kinds and some twenty pins — REVIEW-C2b-v1 priced 750 lines as too thin), raised by the opening push with
  nothing else in it; never again inside the window. The gates land under C2a's 7,800 before it.
- **Not in C2b:** kernel or kernel2 changes; `wish` entries (the sovereign's wishes remain issues labelled
  `wish` in the runner, each answered by a counsel forecast of his decision); a GitHub identity per party
  (COUNSEL-OPEN 17, 20: the report says what the acts table shows and asks only if the declaration rule missed
  an act); the CI skip; automatic promotion; contracts for the procedure types.

## Order of acts, and the clock
1. The two gates and W5 merged on `main` under C2a's cap (builder proposals, reviewer pins), while C2a runs.
2. This brief merged with a read that returns no BLOCK; counsel enters X0–X3 and seeds `COUNSEL-DUE.jsonl`.
3. The sovereign, one paste: `decision promote C2a` (when `lawful`), `key herald-2 … --powers
   merge,forecast`, the opening `push` (cap 8,900) — which the gate of step 1 admits because step 2 is on
   `main`. The opening is the first `push` entry after `decision promote C2a`; the window is (opening `ts`,
   min(X0's `resolves_by`, opening + 14 d)].
4. The builder builds `tools/elect.py`; the reviewer pins; the herald merges; the diary consults `elect.py`
   before every forecast session from the first green `tests` run on `main` holding `tests/test_elect.py` —
   invites before that instant are not rounds (criterion 4).
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
and its σ — forged `args.weights`, a σ that does not verify, a draw from a later prefix). Green on `main`
before the first round (criterion 4).

## Pre-stated criteria for C2b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines within 8,900; the kernel within 500 and byte-identical to C2a's; `judge/scope.json` and
   SPEC §10 unchanged since the opening push.
4. The attack tests green on `main` before the first round's invite.
5. Value continued: *E*ᵥ ≥ 20.
6. Liveness continued: ≥ 20.
7. **Elections witnessed**: at least 24 rounds (one day of hours — an exercise budget the opening push
   authorises, not a constant in any score) whose invite is on the log before the session, replays from the
   prefix, and is resolved by its deadline; the four instances' rounds interleaved as stated.
8. **Counsel bound**: the three gate pins and the four W5 pins KILLED; no `COUNSEL-DUE` row ESCALATED and
   undone at the exit prefix.
9. No `decision` of kind `veto` with subject `C2b`; off-log repairs 0; A3.4 at or under 5 : 1.
**Reported, not gating**: whether any round's invite named an arm other than the previous round's of the
same instance (a switch is evidence of exploration or of a changed record, not of value — REVIEW-C2b-v1 F8);
each arm's record; sovereign acts without a prior counsel forecast.

## Pins (the reviewer's), each with its named mutant and passing twin
`gain_in_unit_interval` (the legal endpoints map to 1 and 0; mutant: divide by ln 1000) · `round_loss_is_mean`
(six losses averaged, a missing one at ln 1000; mutant: summed) · `bad_round_kept` (an unresolved event gives
the round gain 0 and the invite 0; mutant: round dropped) · `exp3_importance` (Ĝ by the saved propensity;
mutant: by today's) · `exp3_constants` (γ, η from *K* and *gⱼ*; mutant: γ = 0.1) · `instance_feedback_complete`
(instance *t* mod 4's previous round is resolved before its draw, or the draw waits; mutant: draws anyway) ·
`draw_replays_from_prefix` (Ĝ, *π*, *u* recomputed from the prefix and σ; mutant: from `args.weights`) ·
`sigma_verifies` (σ verifies against `herald-2`'s pubkey over the round string; mutant: unchecked) ·
`roster_fixed` (an arm outside the opening roster refused; mutant: admitted) · `invite_before_session`
(forecasts carry `args.invite` earlier than their `ts`; mutant: later accepted) · `invite_cutoff_W0` (an invite
with `ts` ≥ W0 is `rigged`; mutant: scored) · `invite_p_is_success_rate` (`p` = the Laplace success rate of the
arm, not the propensity; mutant: the propensity) · `invite_resolution_strict` (1 iff mean loss < base's; mutant:
≤) · `resolver_not_forecaster` (a round's events resolved by a principal other than the invited; mutant: the
same) · `self_invite` · `rigged_election` · `mixture_untouched_and_continued` (C2a's fixture byte-identical;
likelihoods, prior differences and wealth carried across the boundary; mutant: uniform restart) ·
`procedure_types_out` (a `counsel.programme` forecast is not a value event; mutant: scored) ·
`push_without_read_refused` · `read_of_this_text` · `read_not_counsels` · `w5_overdue_escalates` ·
`w5_done_is_an_entry` · `w5_rows_append_only` · `w5_inventory` · `window_from_the_push` · `wealth_continues` ·
`promote_refused` (the verb signs nothing when any criterion is unmet; mutant: value alone).

## Refusal list
No kernel change; no LLM in `elect.py`; no constant in the election but *K*, *gⱼ*, *D* and the theorem's
formulas; no draw from a public seed; no invite entered after its session starts or after `W0`; no round
dropped; no entrant invited by hand; no principal resolving a round it forecast; no change to C2a's statistic,
mixture or clerk; no second push inside the window; no event or invite chosen after its outcome is known.

## Stop and report if
the build does not fit under 8,900; the two checkers disagree; the clerk's key cannot sign a forecast (the
grant missing: the window has not opened); a stream's public evidence disappears; an invite's draw cannot be
replayed from the prefix (a defect in this brief's algorithm, fixed by amendment before any round counts); the
interleaving's assumption fails (a round unresolved when its instance draws again: the draw waits, and the
report says how often).

## Deliverables
Before the opening: `tools/jack push` gate (a), `tools/clerk.py` W5 (b), their tests and pins, under C2a's
cap. In the window: `tools/elect.py` (`--invite <stream> <W0>` prints the entry body and σ; `--replay <seq>`;
`--table`); the diary consulting it and routing the resolver (runner side, prompts in `transcripts/sessions/`);
`tools/value.py` unchanged but for `procedure_types_out`; `tools/status.py` the election line, criteria 1–9
and `promote C2b`; `tools/jack decision` dispatching `C2b`; `tests/test_elect.py`; the two simulator kinds;
the pins; RUNBOOK `## jack elect`; `transcripts/COUNSEL-DUE.jsonl`; counsel's X0–X3; the C2b report, which
disposes explicitly of COUNSEL-OPEN 15–20 (recorder and identities: delivered, carried, or dropped with the
reason) and of the deferred kernel types; the C2c brief's first section (the procedure contracts, the kernel
types if a witness has appeared, the GitHub identities) at exit.

## Counsel's forecasts on this window (entered after the read, before the opening push)
| id | claim | p |
|---|---|---|
| X0 | the promotion forecast: every criterion holds on the exit prefix by the window's end | 0.45 |
| X1 | criterion 7 met within 3 days of the opening push | 0.55 |
| X2 | at the exit (reviewer, `gpt-6-astra-fast`) has been invited at least once and its mean gain exceeds (reviewer, mini)'s | 0.4 |
| X3 | no second push inside the window | 0.7 |
