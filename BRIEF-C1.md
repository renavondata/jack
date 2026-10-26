# Brief C1 — the ledger, then the clerk (v2)

Counsel's proposal of 25 October 2026 (`counsel-2`, Claude Fable 5.1, session
`013Ce38BiYZ9xMbMtFh7wzxX`), v2 after the cold read
`transcripts/REVIEW-brief-3.md` (`openai/gpt-6-astra`); v1 was proposal #23,
superseded unmerged. The reply to the review, finding by finding, is
`transcripts/REPLY-REVIEW-brief-3.md`. It follows Guy's ruling of 25 October
that C1 opens **ledger-first** (`transcripts/RULING-20261025-ledger-first.md`),
which Amendment A3 (`transcripts/AMEND-A3.md`) records in the charter. This
text binds nothing until Guy has accepted it by merge; everything in it that
depends on A3 is conditional on A3's lawful enactment and activation. The
law-language question stands as A2.1 settled it: no rule language until the
first real case; this brief adds none.

## Precondition

C0 promoted (tag `c0-exit`, 17 October). `decision transmute A3` on the log.
The kernel's bound for C1 is 500 lines (A2.4); it stands at 411.

## Purpose

A record that binds is C0. C1 makes it **say things about the world and be
scored for them**, then makes the court act on its own obligations without
Guy. Two windows, each with a pre-stated exit; the layer is promoted at the
end of the second.

- **C1a, the ledger.** Two entry types, `forecast` and `resolution`, under a
  proper score. Every party, Guy included, may forecast; no party resolves its
  own forecast; every resolution names its evidence. The score is computed
  outside the kernel by a tool this brief requires to be log-loss (A2.4); the
  tool is an entrant, not law.
- **C1b, the clerk.** Level-triggered writs, as the 14 October draft had them,
  with one change: the clerk's first writ class is **a forecast past its
  `resolves_by` with no resolution**, a real obligation derived from state and
  the clock, so the clerk is built against a case rather than an invention.

## Order of acts, and the clock (A2.7; review §1 "then `jack amend A3`", §3.1)

1. `decision transmute A3` (Guy).
2. The installing `push` (Guy): SPEC amended per `transcripts/SPEC-C1a-patch.md`
   and the code built to it, in one push, after its run of record. From this
   push the two types are **available**: recognition is additive and every
   earlier log replays unchanged. Nothing entered between this push and step 3
   counts toward the window.
3. `jack amend A3 transcripts/AMEND-A3.md` **immediately after** step 2, with
   the default `activate_at` (its own seq + 1). No `push` is lawful between the
   `amend` and its height (SPEC §10.12); none is needed.
4. **The window opens at A3's activation height.** Its start instant is the
   `ts` of the `amend` entry; its end is that instant plus fourteen days
   (`YYYY-MM-DDTHH:MM:SSZ` arithmetic on UTC). The **exit prefix** is the log on
   `main` up to and including the last entry whose `ts` is not after the end.
   Every criterion below is evaluated on the exit prefix and the tree at the
   commit that carries it. A later amendment cannot move the start.
5. Grants (Guy): `forecast` to every party's key; `resolution` to builder,
   reviewer and counsel; both to the master key (the key whose principal is
   `guy`; the verbs test the principal, not the key_id). The `jack key` verb admits any
   power named in the kernel's `TYPES`, so no verb change is needed beyond its
   text ("outside the ten").

**Failed window** (§6, A3.2; review §1 "restarts it"). A window fails if any
criterion is unmet at its end, or if a trusted-base defect is found inside it.
A failed window is a precedent: the failure is recorded in `REPORT.md`; the fix
enters by a lawful change (`push`, or `transmute` and `amend`); a new window is
pre-stated in this file before it opens; counsel's J1 is not extended.

## C1a: the ledger

### Entry types (SPEC §5; the patch is `transcripts/SPEC-C1a-patch.md`)

- `forecast`: `claim` (non-empty string); `p` (integer 1–999, per mille;
  booleans are not integers); `resolves_by` (an instant in §4's `ts` form, not
  earlier than the entry's own `ts`). Optional, by convention and read by the
  tools, never by the kernel: `type` (a string) and `args` (any object).
- `resolution`: `forecast` (integer, the `seq` of an earlier valid `forecast`
  not already resolved); `outcome` (integer 0 or 1; booleans are not
  integers); `evidence` (non-empty string).

### Recognition (SPEC §7–8)

- **Timestamps** (A2.2, inherited and unimplemented at C0): an entry whose `ts`
  is earlier than its parent's is **ts_decreased**, tested at a new step 2a,
  after shape and before `seq`. Pin `clock_runs_backward`.
- A `resolution` whose `forecast` is not the `seq` of an earlier valid
  `forecast`, or of one already resolved, is **schema** (step 7, before the
  signature).
- A `resolution` whose `proposer` equals the forecast's recorded `proposer` is
  **self_judged**, tested at a new step 8a after the signature (so the party
  is a verified fact): maxim 1, by principal, so two keys of one party cannot
  launder a judgement. A self-resolution with a bad signature is therefore
  `bad_signature`; a self-resolution of an already-resolved forecast is
  `schema`.
- The closed set of reason codes becomes **fourteen**: the twelve of C0,
  `ts_decreased`, `self_judged`. SPEC §9 and §9a are amended together.
- State gains: the proposer of every forecast by seq; the set of resolved
  seqs; the previous entry's `ts`. Nothing else.

### Scoring (outside the kernel; `jack score`, built by the builder to this text)

- Inputs: the log, and `--as-of TS` (an instant; required only for the
  overdue list, which needs a clock the kernel never has). No other input.
- A resolved forecast's loss: `−[o·ln(p/1000) + (1−o)·ln(1−p/1000)]`, natural
  logarithm. Bounded by the per-mille range; no clipping rule exists.
- Groups: every (`proposer`, `type`) pair with at least one resolved forecast
  (a forecast without `type` has type `free`); for each: resolved, mean p
  (over resolved, as a fraction), outcome rate, mean loss, and
  the **base-rate loss**: for the *k*-th resolution of forecasts of that type on
  the whole log in resolution-seq order, pooled across proposers, the base rate
  is Laplace, `(s + 1) / (n + 2)` with `s` and `n` the successes and count of
  the earlier resolutions of that type; its loss is the same formula at that
  rate; the group's base-rate loss is the mean over the group's resolved
  forecasts. Half before any resolution, by construction.
- Also printed: the same figures per `proposer` and per `type` alone, each
  row preceded by its count of forecasts (all, resolved or not); and,
  given `--as-of`, every unresolved forecast whose `resolves_by` is before it,
  ordered by `resolves_by` then seq. Numbers are printed to four decimals,
  rounded half to even.
- **The witness** (criterion 5): `spec/vectors/score.jsonl`, a signed log
  the reviewer builds containing exactly these ten forecasts and six
  resolutions in this order, and the expected table below, which `jack score`
  must print exactly. The builder's independent rebuild, `tests/vectors/score.jsonl`,
  must agree with it entry by entry in meaning (proposer, type, p; forecast,
  outcome; each resolver a party other than the forecaster); any difference is
  a finding against one of them (REVIEW-C1a-code §3).

  Forecasts, in seq order: F1 counsel `world.screen` 600; F2 builder
  `pins_green` 800; F3 counsel `world.screen` 300; F4 reviewer `pins_green`
  700; F5 builder `world.delivery` 900; F6 counsel `pins_green` 500; F7
  builder `pins_green` 650; F8 counsel `world.screen` 400; F9 guy
  `world.race` 200; F10 reviewer `world.screen` 550. Resolutions, in seq
  order: F2→1, F1→1, F4→0, F3→0, F6→1, F5→0, each by a party other than the
  forecaster.

  | proposer | type | resolved | mean p | rate | loss | base-rate loss |
  |---|---|---:|---:|---:|---:|---:|
  | builder | pins_green | 1 | 0.8000 | 1.0000 | 0.2231 | 0.6931 |
  | builder | world.delivery | 1 | 0.9000 | 0.0000 | 2.3026 | 0.6931 |
  | counsel | pins_green | 1 | 0.5000 | 1.0000 | 0.6931 | 0.6931 |
  | counsel | world.screen | 2 | 0.4500 | 0.5000 | 0.4338 | 0.8959 |
  | reviewer | pins_green | 1 | 0.7000 | 0.0000 | 1.2040 | 1.0986 |

  (F4's base rate is 2/3 after F2's success; F3's is 2/3 after F1's; F6's is
  1/2 after F2 and F4; F5's is 1/2, the first of its type.)

### Verbs (RUNBOOK, counsel's text; built by the builder)

`jack forecast`, `jack resolve`, `jack score`, and two changes to existing
text: `jack merge`'s precondition reads "its head is the `commit` of a valid
`proposal` entry in its log followed only by commits that touch `log.jsonl`"
(SPEC §10.7's own rule); `jack proposal`'s `commit` is the last commit on the
branch that changes a path other than `log.jsonl`. Consequences, stated so
that no builder chooses them:

- A forecast about a branch's first CI run is made **before** `jack proposal`,
  which is what pushes the branch: work commits, then `jack forecast` (a
  log-only commit), then `jack proposal`.
- Evidence for a resolution is a **work** commit: the resolver commits the
  file under `transcripts/evidence/<hex64>` (its own SHA-256 as the name),
  runs `jack proposal` (title "evidence for forecast N"), then `jack resolve N
  --evidence sha256:<hex64>` on the same branch. Evidence already on `main`
  needs no new proposal.
- For the master key these are main verbs and the sequence is the same minus
  the proposal.

### World types and their resolvers (counsel's text, before the first such forecast)

A forecast is **world-typed** iff its `type` begins `world.`. Before the first
forecast of a world type is entered, `transcripts/world-types.md` names the
type and its resolver rule in one paragraph each: what counts as outcome 1,
what file is the evidence, who may resolve. The first three: `world.screen`
(the nine candidate screens of 25 October: outcome 1 iff the screen's report
states its pre-registered condition met; evidence: the report), `world.ximenes`
(claims about `gfrmin/ximenes` results; evidence: the report file), and
`world.assize` (claims about `renavondata/assize` state; evidence: the GitHub
API response saved to a file). A type absent from that file is not
world-typed for criterion 4, whatever its name.

### The first forecasts (voluntary; none is a criterion)

Counsel's, entered inside the window; `resolves_by` instants are fixed when
the window's end is known (`W` below is the end instant):

| id | claim | p | resolves_by |
|---|---|---:|---|
| J1 | every C1a criterion is met on the exit prefix | 500 | W |
| J3 | assize's root `REPORT.md` carries an L2 verdict line | 300 | W |
| J5 | the kernel is within 500 lines at the exit prefix's commit | 700 | W |
| J6 | at least one disagreement between the checkers is recorded on a simulated log between the installing push and W | 500 | W |
| J7 | at W, at most one fifth of the window's forecasts are unresolved past their `resolves_by` | 600 | W |
| J2 | by 2027-01-31T00:00:00Z the ledger holds at least 50 resolved world-typed forecasts, and every model proposer with at least ten of them is within 0.05 of its base-rate loss | 600 | 2027-01-31T00:00:00Z |

The ruling's two probabilities (0.65 that (a) is right in hindsight; 0.70 that
Guy chooses (a)) were uttered before the ruling and are **not** entered: the
second has resolved and the first would be a retrospective entry presented as
prospective. Guy's and the builder's forecasts enter under their own keys; the
builder's minimum claims are assize's: tests green on the first CI run of its
branch (made before `jack proposal`), and the brief's criteria met at exit.

### Pre-stated criteria for C1a, evaluated on the exit prefix

1. Every pin below is KILLED with a passing twin in the `tests` run on `main`
   at the exit prefix's commit.
2. Both checkers agree, entry by entry and reason by reason, on the exit prefix
   and every proper prefix of it, and on 10⁵ seeded logs from a seed list
   committed before the installing push, with the simulator at the generator
   revision named in the push's review and extended by the kinds below; every
   new kind's refusing case is refused with its named reason and its twin
   admitted, not merely agreed upon. Any disagreement found after the
   installing run is a trusted-base defect inside the window.
3. Kernel within 500 lines, as `tools/count_kernel.py` counts. `judge/scope.json`
   is unchanged from the installing push. (A needed change to either is a
   stop-and-report, not an exception.)
4. Within the window (entries whose `ts` lies in [start, end]): at least 20
   `forecast` entries by at least three distinct `proposer` values; at least 10
   `resolution` entries; at least 5 of those resolving world-typed forecasts,
   each with `evidence` of the form `sha256:<hex64>` and a file
   `transcripts/evidence/<hex64>` whose SHA-256 is that value, present in the
   tree at the exit prefix's commit.
5. `jack score` on `spec/vectors/score.jsonl` prints the table above exactly.
6. The exit prefix contains no `decision` of kind `veto` whose `subject` is
   `C1a`.

Also reported, not criteria: whether a primary-rule case arose (A2.1); the
procedure/object accounting of A3.4, where an **object** entry is a `forecast`
or `resolution` whose type is world-typed and every other entry is procedure,
counted over the window (a ratio above 5 : 1 stops the layer and reports);
J7's figure with its denominator (forecasts entered in the window).

### Pins, each with its named mutant, KILLED with a passing twin

- `clock_runs_backward`: an entry with `ts` earlier than its parent's is
  admitted.
- `self_resolution_admitted`: a resolution by the forecast's own principal is
  admitted.
- `dangling_resolution_admitted`: a resolution naming a seq that is not a
  forecast is admitted.
- `double_resolution_admitted`: a second resolution of one forecast is admitted.
- `past_forecast_admitted`: a forecast whose `resolves_by` precedes its `ts` is
  admitted.
- `permille_out_of_range_admitted`: `p` of 0 is admitted; a second mutant, `p`
  of 1000.
- `boolean_integer_admitted`: `p: true` or `outcome: false` is admitted.
- `self_judged_uncoded`: the kernel refuses self-resolution under a code other
  than `self_judged`.
- `score_not_proper`: `jack score` with log-loss replaced by `1 − |o − p|`, or
  by a score that is minimised at p = 999 whatever the outcome, still prints
  the witness table.

Simulator kinds added: `ts_decreasing`, `forecast_valid`, `resolution_valid`,
`resolution_self`, `resolution_dangling`, `resolution_double`,
`forecast_past`, `forecast_permille_0`, `forecast_permille_1000`,
`forecast_boolean`. The extended simulator runs clean before the installing
push, as part of its run of record (§6: simulator first).

## C1b: the clerk

As the 14 October draft, items 1, 2 and 5, with these changes:

- The first writ class is the overdue forecast. The writ names the forecast,
  the parties holding `resolution` power other than its proposer, and a
  deadline; escalation: re-invite, re-invite another party or model, writ to
  Guy.
- Guy's acts typed by entry: `wish` enters as a type (never scored), with
  `decision` already present; `accept` and `invite` as the draft had them.
- The herald key (`accept`, `wish`, `resolution` by mechanism) is declared by
  Guy; it never holds `key` or the change power.
- Exit: a clean simulator run with stalling and flooding as liveness attacks;
  then E_t ≥ 20 against p₀ (assize's weekly `guy_acts.py` series) within 14
  days live; windows, α = 0.05, p₀ and the attack list committed before the
  window opens; zero checker disagreements throughout; no `veto` with subject
  `C1b`.

C1b's brief text is written at C1a's exit, by counsel, from C1a's report.

## Refusal list

No LLM call, network access or clock read in either checker; `ts` and
`resolves_by` enter only as entry fields, and `--as-of` is the score tool's
argument, never the kernel's. No scoring in the kernel. No new required member
on an existing type. Counsel writes no code: this brief, the SPEC patch text,
the RUNBOOK sections, `transcripts/world-types.md` and the ruling are
counsel's; the kernel, kernel2, tools and tests are the builder's and the
second family's; the pins and vectors are the reviewer's. No change to
`CHARTER.md` except by `jack amend A3` in the order above.

## Stop and report if

- the kernel would pass 500 lines, or `judge/scope.json` would need to change;
- the two checkers disagree about what this brief or the SPEC patch means (a
  `spec_conflict`, not a patch);
- the first real case for a primary rule arises (A2.1 then governs).

## Deliverables

C1a: SPEC amended per the patch (text first, by Guy's push, with the code built
to it); kernel and kernel2 with the two types and `ts_decreased`; the pins,
vectors (`40`–`47`, see the patch) and simulator kinds; `tools/jack forecast |
resolve | score` and the two text changes to existing verbs;
`transcripts/world-types.md`; the first forecasts; a C1a report in REPORT.md's
form, citing the exit prefix by seq and hash and the `tests` run that counts;
the brief text of C1b. This brief imposes, under A2.4, a cold read of the C1a
code by a party of another family before the installing push, recorded as the
push's `review`.
