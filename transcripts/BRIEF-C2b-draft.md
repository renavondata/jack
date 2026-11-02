# BRIEF-C2b — the election (draft v1, counsel, 2 November 2026)

C2's third word. CHARTER §8: "C2: forecasts, proper scores, election"; §5: "Which proposer is invited is an
election by Hedge or Fixed Share on proper scores (… EXP3 under bandit feedback, Auer et al. 2002): an
entrant, not law"; PLAN §4: elections of proposers, "no witness yet". C2a produced the record — weights per
entrant, prequentially, on events with identity and cutoff. C2b makes the record **choose who proposes next**,
and makes the choice an entry that is scored like any other. It changes no kernel: an invitation is a
`forecast` of type `election.invite` signed by the clerk's key, whose claim is that the invited entrant's
log-loss on the window it is invited to beats the base rate's; the kernel reads neither `type` nor `args`
(SPEC §5) and nothing new is admitted. The one kernel change C2a's text promised for C2b — `invite`/`accept`/
`wish` as types — is deferred to the first witness that a forecast cannot carry an invitation; none has
appeared, and §4's rule is to codify at the witness, never in anticipation. C2b also binds **counsel**
mechanically in the two places the record shows it was bound only by habit (REVIEW-C2a-v1 F1: a statistic the charter forbids, caught by a read and by nothing else; 31 October–2 November: windows unresolved and proposals stale while counsel was not looking).

C2b opens at the `ts` of its opening `push` (§Order of acts), after `decision promote C2a` and this brief's
read; its exit is a crossing (A5), its window a maximum of fourteen days; its value and liveness wealth
continue from C2a's (A4.1).

## Precondition
C2a promoted (`decision promote C2a` entered while `status.py` printed `lawful`); this brief and its read on
`main`; counsel's forecasts X0–X3 entered; the opening push in force (the cap, and `forecast` power for the
clerk's key `herald-2`, which the sovereign grants with the same paste — a key act, §7).

## Purpose
Three things the record cannot yet show. **(1) An election that acts:** who forecasts a stream's next window
is chosen by a pre-stated algorithm from the entrants' proper scores, and the choice is an entry before the
session runs. **(2) Entrants that are models, not only principals:** every session forecast carries
`args.model` since 1 November; the entrant the election chooses is a (principal, model) pair, so the ledger
can say whether `gpt-5.4-mini` or `gpt-6-astra-fast` forecasts freshness better under the reviewer's key — the
question COUNSEL-OPEN 22 left to "C2's election". **(3) Counsel under the clerk:** the opening push refuses a
brief that has no read, and counsel's dated obligations are writs, so the two failures of 31 October–2
November (a brief proposing a statistic the charter forbids; counsel idle with a window open) are caught by
code the next time.

## Scope
- **The entrants.** A (principal, model) pair that has at least one resolved forecast of the stream on the
  log, plus the base-rate forecaster. At the opening: (reviewer, `openai/gpt-5.4-mini`) and (builder,
  `openai/gpt-5.4-mini`) from C2a's record; (reviewer, `openai/gpt-6-astra-fast`) enters by the exploration
  rule below. A model string is the `args.model` of the forecast entry; a forecast without one is the pair
  (principal, `unknown`).
- **The election** (per stream, per window): **EXP3** (Auer, Cesa-Bianchi, Freund, Schapire 2002) over the
  *K* entrants of the stream, since only the invited entrant forecasts a window (bandit feedback): weight
  *wₖ* ∝ exp(η Ĝₖ), Ĝₖ the sum of importance-weighted gains *gₖ,ₜ* / *pₖ,ₜ* over the windows *k* was invited
  to, gain *gₖ,ₜ* = 1 − ℓ(*qₖ,ₜ*, *Yₜ*)/*B* ∈ [0, 1] (log-loss under per-mille clipping, *B* = ln 999, so the
  gain is bounded as the theorem requires), probability *pₖ,ₜ* = (1 − γ) *wₖ*/Σ*w* + γ/*K*, with
  γ = min(1, √(*K* ln *K* / ((e − 1) *g*))) and η = γ/*K*, *g* = the number of windows in the layer's window
  (14 × 24 = 336 at the opening; a constant derived from the bound, A4's maxim). The regret bound is
  2√((e − 1) *g K* ln *K*) against the best single entrant in hindsight. Exploration is the γ/*K* term and
  nothing else: no hand-chosen floor. A new entrant enters with Ĝ = 0 (the uniform share), which is the
  **recovery and coverage policy** REVIEW-C2a-am2 F3 asked for: an abstaining or low-weight entrant is
  invited with probability at least γ/*K*, forecasts, and earns or loses on its own record — **without
  touching C2a's mixture**, which continues unchanged on every forecast made (the mixture is the value test's
  aggregate; the election is who gets to forecast).
- **The invitation.** Before each forecasting session, the clerk draws the entrant with the seed = the
  window's `W0` (so the draw is reproducible from the log and the pin can replay it) and enters a `forecast`
  of type `election.invite`: claim "the entrant <principal, model> forecasts stream <s> window <W0>; its
  log-loss on that window is below the base rate's", `p` = *pₖ,ₜ* in per mille (the election's own
  probability of its choice: a proper-scored statement of how confident the record is), `args` = {stream,
  window_utc, principal, model, weights, gamma, seed}, `resolves_by` = window end + 2 h. The diary files the
  session for that principal and model; the session's forecasts carry `args.invite` = the invite's seq. The
  invite resolves 1 iff the invited entrant's log-loss on the window's six events is below the base rate's
  — by the builder's resolve session, from the same evidence as the events.
- **Streams.** The freshness stream as BRIEF-C2a Amendment 2 leaves it: hourly, six datasets, the window
  `[H+2, H+3)`. HKJC per race as C2a. Nothing added.
- **Counsel bound.** (a) `jack push` refuses an opening push for a layer whose brief
  `transcripts/BRIEF-<layer>-draft.md` has no `transcripts/REVIEW-<layer>-*.md` on `main` whose "Reviewed
  tree" line names a commit at which the brief's bytes equal the current bytes and whose verdict is not
  BLOCK (the read is of *this* text, not an earlier one). (b) The clerk gains W5: every row of
  `transcripts/COUNSEL-DUE.jsonl` ({"id", "due", "what", "done": seq or null}) is a writ held by counsel,
  ESCALATED past `due` like any other; counsel's dated obligations from COUNSEL-OPEN move into that file at
  the opening. (c) Every counsel recommendation to the sovereign that asks an act carries a forecast
  (COUNSEL-OPEN 13) — already the rule; now a pin: `status.py` lists sovereign acts in the window with no
  counsel forecast naming them, and W4 counts them.
- **Event contracts for the procedure types**, so that every forecast enters the value statistic
  (REVIEW-C2a-v1 F2): `proposal.ci` and `proposal.count` — identity (branch head commit from the proposal
  entry the forecast precedes on its branch), cutoff the proposal entry's `ts`; `counsel.programme`,
  `review.forecast`, `election.invite` — identity `args.id` where present else the claim, cutoff the
  forecast's own `ts` (the outcome is by construction unknown at entry), one forecast per principal per
  identity. `tools/value.py` scores them in the same ledger from the opening of C2b; nothing before.
- **The cap.** The budget is **8,400** (7,650 counted today; `tools/elect.py`, its tests, the W5 and
  push-gate code, the pins and the simulator kinds are of C2a's size), raised by the opening push with
  nothing else in it but the `forecast` grant to `herald-2`; never again inside the window.
- **Not in C2b:** kernel or kernel2 changes; `wish` entries (the sovereign's wishes remain issues in the
  runner labelled `wish`, each answered by a counsel forecast of his decision); a GitHub identity per party
  (COUNSEL-OPEN 17, 20 — an infrastructure act of the sovereign's, asked for in the C2b report if the acts
  table shows a misattribution the declaration rule missed); the CI skip (REVIEW-C2a-v1 F8's contract stands
  for whoever wants the three minutes); automatic promotion (§7 keeps the boundary decision the sovereign's).

## Order of acts, and the clock
1. This brief merged with a read that returns no BLOCK; counsel enters X0–X3 and `transcripts/COUNSEL-DUE.jsonl`.
2. The sovereign: `decision promote C2a` (if not already), `jack key herald-2 --powers merge,forecast`, the
   opening `push` (cap 8,400). The opening is the first `push` entry after `decision promote C2a`; the window
   is (opening `ts`, min(X0's `resolves_by`, opening + 14 d)].
3. The builder builds `tools/elect.py` and the gates; the reviewer pins; the herald merges; the diary consults
   `elect.py` before every forecast session from the first green `tests` run on `main` holding
   `tests/test_elect.py` — invites before that instant are not scored (criterion 4, as before).
4. `status.py` prints the election line and `promote C2b: lawful | refused: …`; the sovereign's
   `decision promote C2b` at the crossing.

## Statistics
- **Value continued**: *E*ᵥ of BRIEF-C2a §The statistic, one ledger, now over every typed forecast with a
  contract (above). Criterion: ≥ 20 at the exit prefix.
- **Liveness continued**: C1b's process, unchanged. Criterion: ≥ 20 at the exit prefix.
- **The election's own score**: the invites are forecasts; their log-loss against the base rate of type
  `election.invite` is reported by `jack score` and enters *E*ᵥ like any other type. No separate threshold:
  the election is an entrant in the value test, which is what §5 says it is.

## Safety: two attack kinds before any invite counts
`self_invite` (an entrant's key signing an `election.invite` naming itself: the kernel's powers are per entry
type, not per `type` field, so the refusal is the tools' — an invite is an invitation only under the clerk's key
`herald-2`; `value.py` lists any other as `unkeyed` and the diary files no session on it) and `rigged_election` (weights computed from events resolved after the
invite's `ts`: refused by `elect.py`'s replay from the invite's own `args.weights` and seed — a pin
recomputes the draw and refuses a mismatch). Green on `main` before the first scored invite.

## Pre-stated criteria for C2b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines within 8,400; the kernel within 500 and byte-identical to C2a's; `judge/scope.json` and
   SPEC §10 unchanged since the opening push.
4. The attack tests green on `main` before the first scored invite's `ts`.
5. Value continued: *E*ᵥ ≥ 20.
6. Liveness continued: ≥ 20.
7. **Elections witnessed**: at least 24 forecasting sessions filed on an `election.invite` entered before
   them by the clerk's key, each invite reproducible from its `args` by `elect.py --replay`; at least one
   invite naming an entrant other than the one named by the previous invite of that stream (the election
   changed an act); every invite resolved by its deadline.
8. **Counsel bound**: pin `push_without_read_refused` KILLED; W5 printed by the clerk with every row of
   `COUNSEL-DUE.jsonl`; no row ESCALATED at the exit prefix.
9. No `decision` of kind `veto` with subject `C2b`; off-log repairs 0; A3.4 at or under 5 : 1.

## Pins (the reviewer's), each with its named mutant and passing twin
`exp3_weights` (Ĝ importance-weighted by *pₖ,ₜ*; mutant: by 1) · `exp3_gamma_derived` (γ from *K*, *g*;
mutant: γ = 0.1) · `gain_bounded` (gain in [0, 1] by the per-mille clip; mutant: unclipped) ·
`draw_reproducible` (the draw from `args.seed` and `args.weights` replays; mutant: seed ignored) ·
`invite_before_session` (a session's forecasts carry `args.invite` = a seq earlier than their own; mutant:
later accepted) · `self_invite` (an invite not signed by the clerk's key is `unkeyed`; mutant: scored) ·
`rigged_election` (weights from events resolved after the invite's `ts` refused on replay; mutant: accepted)
· `new_entrant_uniform` (an entrant with no record enters at Ĝ = 0; mutant: at the minimum) ·
`mixture_untouched` (C2a's mixture over principals is byte-identical in output on C2a's fixture; mutant:
the mixture reads the election's weights) · `invite_resolution` (the invite resolves 1 iff the entrant's
window log-loss < the base's; mutant: ≤) · `procedure_contracts` (a `proposal.ci` forecast after its
proposal entry is `rigged`; mutant: scored) · `push_without_read_refused` (the verb refuses with no matching
REVIEW; mutant: pushes) · `read_of_this_text` (a REVIEW whose "Reviewed tree" holds different brief bytes
does not count; mutant: any REVIEW counts) · `w5_from_file` (every `COUNSEL-DUE` row is a writ, ESCALATED
past `due`; mutant: not past due) · `recommendation_forecast` (a sovereign act in the window with no counsel
forecast naming it counts in W4; mutant: ignored) · `elections_changed_an_act` (criterion 7's third clause;
mutant: always true) · `window_from_the_push` · `wealth_continues`.

## Refusal list
No kernel change; no LLM in `elect.py`; no constant in the election but *K*, *g*, *B* and the EXP3 formulas;
no invite entered after its session starts; no entrant invited by hand (counsel's HKJC forecasts are entries
under counsel's key and are not invitations); no change to C2a's statistic, mixture or clerk; no second push
inside the window; no event or invite chosen after its outcome is known.

## Stop and report if
the build does not fit under 8,400; the two checkers disagree; the clerk's key cannot sign a forecast (the
grant missing: the window has not opened, say so); a stream's public evidence disappears; an invite's draw
cannot be reproduced from its own `args` (a defect in the brief's algorithm, fixed by amendment before any
invite is scored).

## Deliverables
`tools/elect.py` (`--invite <stream> <W0>` prints the entry body; `--replay <seq>` recomputes a draw;
`--table` the per-entrant Ĝ, *pₖ* and record); the diary consulting it (runner side; the prompt and the
invite are the record's, `transcripts/sessions/`); `tools/clerk.py` W5; `tools/jack push` gate;
`tools/value.py` procedure contracts and `election.invite`; `tools/status.py` the election line, criteria
1–9 and `promote C2b`; `tests/test_elect.py`; the two simulator kinds; the pins; RUNBOOK `## jack elect`;
`transcripts/COUNSEL-DUE.jsonl`; counsel's X0–X3; the C2b report; the C3 brief's precondition section
(what assize's sealed judge must deliver) at exit.

## Counsel's forecasts on this window (entered after the read, before the opening push)
| id | claim | p |
|---|---|---|
| X0 | the promotion forecast: every criterion holds on the exit prefix by the window's end | 0.5 |
| X1 | criterion 7 met within 3 days of the opening push | 0.6 |
| X2 | at the exit the election has invited `gpt-6-astra-fast` at least once and its Ĝ is above mini's on the invited windows | 0.4 |
| X3 | no second push inside the window | 0.75 |
