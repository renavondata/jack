# Brief C1 — the ledger, then the clerk

Counsel's proposal of 25 October 2026 (`counsel-2`, Claude Fable 5.1, session
`013Ce38BiYZ9xMbMtFh7wzxX`), replacing the draft of 14 October. It follows
Guy's ruling of 25 October that C1 opens **ledger-first** (option (a) of
`transcripts/RULING-20261025-ledger-first.md`), which Amendment A3
(`transcripts/AMEND-A3.md`) records in the charter. It binds nothing until a
party of another model family has read it cold (A2.10) and Guy has accepted it
by merge. The earlier draft's law-language section stands as A2.1 settled it:
no rule language until the first real case; this brief adds none.

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
  own forecast; every resolution names its evidence. Assize's scoring
  (`harness.ledger`) is ported as the first entrant, outside the kernel.
- **C1b, the clerk.** Level-triggered writs, as the 14 October draft had them,
  with one change: the clerk's first writ class is **a forecast past its
  `resolves_by` with no resolution**, a real obligation derived from state and
  the clock, so the clerk is built against a case rather than an invention.

## C1a: the ledger

### Entry types (SPEC §5; the patch is `transcripts/SPEC-C1a-patch.md`)

- `forecast`: `claim` (non-empty string); `p` (integer 1–999, per mille: the
  canonical line admits integers only, and 1–999 bounds the log-loss without a
  clipping rule); `resolves_by` (an instant, not earlier than the entry's `ts`).
  Optional, by convention and read by the tools, never by the kernel: `type`
  and `args`, as assize's Amendment 4 rule 3 has them, so a resolver can be
  mechanical later.
- `resolution`: `forecast` (the `seq` of an earlier `forecast` entry);
  `outcome` (integer 0 or 1); `evidence` (non-empty string: a run id, a commit,
  or the SHA-256 of a file under `transcripts/evidence/` committed alongside).

### Recognition (SPEC §7–8)

- A `resolution` whose `forecast` is not the `seq` of an earlier valid
  `forecast`, or of one already resolved, is **schema**.
- A `resolution` whose `proposer` equals the forecast's `proposer` is
  **self_judged**, a thirteenth reason code: maxim 1, by principal, so two keys
  of one party cannot launder a judgement.
- State gains two things: the proposer of every forecast by seq, and the set of
  resolved seqs. Nothing else.
- Powers are entry-type names as before; `forecast` and `resolution` are granted
  by `key` entries. Proposed grants, Guy's to make: every party `forecast`;
  builder, reviewer and counsel `resolution`; the master key both.

### Scoring (outside the kernel)

`tools/jack score` (builder) reports, from the log alone, per proposer and per
`type`: forecasts, resolutions, mean p, outcome rate, log-loss, and the
base-rate log-loss (the empirical outcome frequency of that type to date, ½
before any resolution), as assize's STATUS does. The score is law because it
carries a proof (Gneiting & Raftery 2007); the base-rate comparator is an
entrant. Unresolved forecasts past `resolves_by` are counted and listed: they
are C1b's first obligations.

### Verbs (RUNBOOK; built by the builder to the text)

`jack forecast`, `jack resolve`, `jack score`. Forecast and resolve are branch
verbs for every party but Guy: their entries ride a proposal's branch as
`log.jsonl`-only commits after the `proposal` entry (SPEC §10.7 admits this)
and reach `main` by merge; for the master key they are main verbs.

### The first forecasts

Counsel's, entered within the window so that counsel is scored from the first
week; each has a `resolves_by` and a type a resolver can settle:

| id | claim | p | resolves_by |
|---|---|---:|---|
| J1 | C1a's exit criteria are met within 14 days of the push that installs the types | 500 | +14 days |
| J2 | the first 50 resolved world-typed forecasts in this ledger show every model proposer within 0.05 of base-rate log-loss | 600 | when n = 50 |
| J3 | assize records an L2 verdict line before C1a exits | 300 | C1a exit |
| J5 | the kernel is within 500 lines at C1a's exit | 700 | C1a exit |
| J6 | the two checkers disagree on at least one simulated log before C1a's exit | 500 | C1a exit |
| J7 | at C1a's window end, at most a fifth of its forecasts are unresolved past `resolves_by` | 600 | window end |

(J4, an act-alone class on a world act by 30 November, waits for C1b's typed
acts.) Guy's and the builder's forecasts enter under their own keys; the
builder's minimum claims are assize's: tests green on the first CI run of its
branch, the brief's criteria met at exit.

### Pre-stated criteria for C1a

1. Every pin below KILLED with a passing twin, in CI, from trunk.
2. Both checkers agree, entry by entry and reason by reason, on the real log and
   on 10⁵ seeded logs whose seed list is committed before the first run, with
   the simulator extended by the kinds below.
3. Kernel within 500 lines; `judge/scope.json` cap unchanged unless a
   `spec_conflict` says why.
4. Within the window: at least 20 forecasts by at least three parties; at least
   10 resolutions, none refused as `self_judged` on `main`; at least 5
   resolutions of world-typed forecasts carrying an evidence hash whose file is
   in the tree.
5. `jack score` reproduces assize's scoring on a copied assize ledger converted
   to entries (the port's witness), to the third decimal.
6. Guy has not vetoed.

### Pins, each with its named mutant, KILLED with a passing twin

- `self_resolution_admitted`: a resolution by the forecast's own principal is
  admitted.
- `dangling_resolution_admitted`: a resolution naming a seq that is not a
  forecast is admitted.
- `double_resolution_admitted`: a second resolution of one forecast is admitted.
- `past_forecast_admitted`: a forecast whose `resolves_by` precedes its `ts` is
  admitted.
- `permille_out_of_range_admitted`: `p` of 0 or 1000 is admitted.
- `score_not_proper`: `jack score` with log-loss replaced by accuracy, or by a
  score that rewards p = 999 regardless of outcome, is not caught by the test.
- `self_judged_uncoded`: the kernel refuses self-resolution under a code other
  than `self_judged`, so the two checkers could agree on the verdict and differ
  on the reason.

Simulator kinds added: `forecast_valid`, `resolution_valid`,
`resolution_self`, `resolution_dangling`, `resolution_double`,
`forecast_past`, `forecast_permille`.

### Window

Fourteen days from the `push` that installs the two types on `main`. Stated
here before it opens, as CHARTER §6 requires. A trusted-base defect found inside
the window restarts it (REPORT §8, scope item 2).

## C1b: the clerk

As the 14 October draft, items 1, 2 and 5, with these changes:

- The first writ class is the overdue forecast. The writ names the forecast,
  the parties holding `resolution` power other than its proposer, and a
  deadline; escalation: re-invite, re-invite another party or model, writ to
  Guy.
- Guy's acts typed by entry: `wish` enters as a type (never scored, A3 of
  assize), with `decision` already present; `accept` and `invite` as the draft
  had them.
- The herald key (`accept`, `wish`, `resolution` by mechanism) is declared by
  Guy; it never holds `key` or the change power.
- Exit: a clean simulator run with stalling and flooding as liveness attacks;
  then E_t ≥ 20 against p₀ (assize's weekly `guy_acts.py` series) within 14
  days live; windows, α = 0.05, p₀ and the attack list committed before the
  window opens; zero checker disagreements throughout; Guy has not vetoed.

C1b's brief text is written at C1a's exit, by counsel, from C1a's report:
what the ledger's overdue forecasts actually looked like decides the writ's
shape.

## Refusal list

No LLM call, network access or clock read in either checker; `ts` and
`resolves_by` enter only as entry fields. No scoring in the kernel. No new
required member on an existing type. No `float` anywhere in an entry. Counsel
writes no code: this brief, the SPEC patch text, the RUNBOOK sections and the
ruling are counsel's; the kernel, kernel2, tools and tests are the builder's
and the second family's; the pins are the reviewer's. No change to `CHARTER.md`
except by `jack amend A3`, after the installing push, as A2.7 orders.

## Stop and report if

- the kernel would pass 500 lines;
- the two checkers disagree about what this brief or the SPEC patch means (a
  `spec_conflict`, not a patch);
- a forecast anyone wants to make cannot be stated without a non-integer;
- the first real case for a primary rule arises (A2.1 then governs, and the
  language question reopens with a witnessed case).

## Deliverables

C1a: SPEC §5, §7, §8, §9, §11 and §12 amended per the patch (text first, by
Guy's push, with the code built to it); kernel and kernel2 with the two types;
the pins and simulator kinds; `tools/jack forecast | resolve | score`; the
first forecasts; `transcripts/REVIEW-brief-3.md`, a cold read of this brief by
a party of another family, before the builder starts; a C1a report in
REPORT.md's form; the brief text of C1b. Then `jack amend A3`.
