# Brief C1b — the clerk (draft v3, 30 October 2026; finalised from the C1a report at C1a's exit)

Counsel's text, in BRIEF-C1's form. v2 answered `transcripts/REVIEW-C1b-A5.md` (gpt-6-astra, BLOCK on
F5–F8); v3 answers `transcripts/REVIEW-C1b-v2.md` (gemini-4-argon, ACCEPT WITH OBLIGATIONS F1–F6) as
`transcripts/REPLY-REVIEW-C1b-v2.md` sets out. The six obligations are discharged in the text before
the window opens rather than carried into it, because each would otherwise be *built*: a statistic
shown inflatable, a writ class with no witness, a cap raised before any shortfall was measured. Its
spine is PLAN-20261030 §4's enforcement map: each criterion is a row that has a witness on the record,
in witnessed order. Where it names code, the builder builds it and the reviewer pins it; counsel
writes none.

## Precondition
A5 in force. `tools/status.py` on `main`. Every C1a criterion holding on the current prefix (the tool
prints it), so that the sovereign's `decision promote C1a` is lawful under A5 clause 1.

## Purpose
C1a made the record say things about the world and be scored for them. C1b makes the court act on
its own obligations without the sovereign: every obligation derived from state and the clock, with a
deadline, raised where a party reads it, escalated when the deadline passes (maxim 3). The clerk
decides nothing about validity and holds no change power (§5). Its forcing witness is the record of
counsel's hand-set reminders: two obligations discharged late (46/47 by six hours, 56 by four).

## Scope
No new entry type and no kernel change. Writs are *derived* state, recomputable by anyone from
`log.jsonl`, the tree, the clock and GitHub's REST view of the repository, discharged by entries that
already exist. `invite` and `accept` are C2's, with `wish`, in one kernel change and one run of record;
**until then a wish of the sovereign's is a `proposal` signed by him appending to
`transcripts/WISHES.md`** — on the log, under his key, distinguishable as the only `proposal` entries
that key signs (he signs no other). A wish is never an item (§7: wishes are never scored); a wish not
entered is not a wish; counsel transcribes none. The acts table counts it once the classifier reads
`log.jsonl` — counsel's obligation, outside this brief. **The trusted base is not touched.** The
clerk, its tests and its pins fit under the cap of 6,200: `tools/genesis.py` and
`tests/test_genesis.py` (181 counted lines) are deleted — the genesis tool has had no use since seq 0
and a second log is not this repository's — leaving 383 lines. The simulator runner and the vectors
tool stay: they are the run of record's and the reviewer's instruments under SPEC §6 and BRIEF-C1
criterion 5, in use, not anticipation. If the clerk does not fit, the builder stops and reports the
shortfall in lines; a push is decided on that number, never before it.

## Order of acts, and the clock
1. This brief merged with its third cold read on the record. Counsel enters **L0**, the promotion
   forecast, with `args.id` = `"L0"` so that `status.py` finds it, and `resolves_by` no later than
   fourteen days after L0's own `ts` — the maximum the sovereign's budget decision names (seq 50); the
   `promote` follows L0, so the bound holds from the `promote` too. Nothing in this brief states the
   window's end except by naming L0.
2. **One decision.** `decision promote C1a` closes C1a (A5 clause 1) and **opens C1b at its `ts`**.
   `tools/jack decision` refuses `promote <window>` before signing while `status.py` prints SHORT or
   STOP for that window, so an unlawful `promote` is not entered rather than detected. The window
   ends at the earlier of L0's `resolves_by` and a `decision promote C1b` entered once the criteria
   below hold (A5).
3. p₀, α and the attack list are committed here, before step 2, and never tuned after.

## The clerk (`tools/clerk.py`; the builder's)
Run on a timer or by hand; it keeps no state between runs (level-triggered: a missed tick costs
nothing). It prints every open writ — the obligation, who may discharge it, the deadline — and marks
one past its deadline **ESCALATED**, naming the sovereign. Writ classes, each with deadline and discharge:
- **W1 forecast**: every `forecast` entered after the opening is a writ from its entry; holders: every
  key with `resolution` power whose principal is not the forecaster's; deadline: 48 h after
  `resolves_by`; discharged by a `resolution`. (A forecast is overdue when the clock is *strictly after*
  `resolves_by`; at equality it is not.)
- **W3 unwitnessed merge**: a `merge` entry on `main` whose `commit` had no green `tests` run before the
  merge commit's time; holder: counsel; discharged by a COUNSEL-OPEN line naming it as precedent.
- **W4 window state**: `status.py`'s SHORT and STOP lines; holder: counsel; deadline: the window's end.
  A `decision promote` on the log entered while a criterion did not hold at its instant is printed as
  a sovereign REPAIR; since the verb refuses one, its presence means a hand-made entry.
There is no proposal writ: every herald merge since the herald's key (seq 51) completed within
seventeen minutes of its `proposal` entry, and a class with no witness is not built (PLAN §4).
Re-invitation of another party or model is C2's.

`status.py` reads C1b from the log: it opens at the `ts` of the `decision` with kind `promote` and
subject `C1a`, ends at L0's `resolves_by`, and evaluates criterion 3 from the tree (counted lines,
kernel within 500, `judge/scope.json` equal to SPEC §10's block) rather than deferring it to CI.

## Liveness: the statistic, the null, the bet
- **Item**: a W1 writ raised after the opening, collapsed: forecasts whose resolutions carry one
  `evidence` string are one item, and writs discharged by one `merge` entry are one item — the
  herald's act is the unit, as the merged pull request was assize's. A writ that expires undischarged
  is an item of its own.
- **Yᵢ = 1** iff every constituent writ was discharged before its deadline and no sovereign repair is
  attributed to the item. A repair is what the acts classifier types as one, in either repository;
  each is attributed to at most one item: the earliest-opened writ open at the repair's instant.
- **Null, p₀ = 0.41**, and the map from the incumbent's series to this statistic, stated: assize's unit
  was the merged pull request and its measured series is repairs per merge (3.6, 0.89, 2.9 in three
  weeks); jack's unit is the herald's act, so the units now correspond; the modelling assumption is
  repairs spread evenly over units, under which the share of units with none is e^{−r}: 0.03, 0.41,
  0.06. The null takes the incumbent's best week. Under A4 clause 3 six consecutive successes carry
  E to 30.1 and five to 14.4; the mean week (0.09) would cross on three, which is why it is not the
  null. Committed here; never re-estimated.
- **Flooding, bounded not stopped.** Six base-rate `world.hkjc` forecasts on one meeting, resolved
  against one evidence file in one merge, are one item: a flood of one event is one success. Six
  trivial procedure forecasts resolved one per merge are six items and cost six forecasts, six
  resolutions, six proposals and six merges — twenty-four procedure entries against no object, which
  the ratio reports (A3.4) and the record shows. No rule decidable from the log stops a determined
  flooder without a constant; what stops one is the veto (criterion 6), on the record. The
  programme's own flow — world-typed forecasts resolved from evidence by another principal — is not
  an attack.
- **Bet**: A4 clause 3, wealth continued (C1a bet nothing: it had no liveness statistic); λᵢ from the
  Laplace estimate over the items so far; E ≥ 20 promotes; α = 0.05.
- **Reported, not tested**: repairs per week (unbounded); the acts table's columns.

## Safety: the attack run before any item counts
`tests/test_clerk.py` builds its own logs (not the simulator's seeds, four of whose first five
`stalling` cases carry no forecast) and asserts: a stalled forecast is a W1 writ from its entry and
ESCALATED strictly after `resolves_by` + 48 h; a flood of forecasts raises one writ each and leaves the
rest printed; two runs over the same inputs print byte-identical output (a test, not a pin: a pure
function has no guard to weaken). The simulator's `stalling` and `flooding` kinds are run through both
checkers as before (criterion 2). No item counts before the first green run of this test on `main`.

## Pre-stated criteria for C1b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds (C1a criterion 2, unchanged).
3. Counted lines within the cap of 6,200; the kernel within 500; `judge/scope.json` and SPEC §10's
   block unchanged.
4. The attack test green on `main` before the first counted item.
5. Liveness E ≥ 20 under the bet above on items raised after the opening.
6. No `decision` of kind `veto` with subject `C1b`.
7. The enforcement map reprinted by `status.py` shows the rows C1b moves — obligations from state and
   clock (W1), window state (W4), the herald's merge on green (W3), windows as maxima (A5, by the
   verb's refusal) — with an enforcer that is code; the runner's rows and elections are outside this
   brief and are not read.
Reported: the procedure : object ratio (A3.4 applies); J7; the weekly acts table.

## Pins (the reviewer's), each with its named mutant and passing twin
- `overdue_strictly_after`: written `resolves_by < now`; a forecast at `resolves_by` exactly is not
  overdue; mutant: `<=`; twin: one second after is overdue.
- `w1_from_entry`: a forecast is a W1 writ at its entry, not at its lateness; mutant: raised only when
  overdue; twin: a resolved forecast is no writ.
- `self_holder`: a W1 writ never names the forecaster's principal; mutant: the filter dropped.
- `w3_unwitnessed`: a merge whose commit has no earlier green `tests` run is a W3 writ, on a synthetic
  runs listing holding a failed `tests` run and a green one *after* the merge's time; mutant: any run
  accepted; twin: a green run before the merge.
- `w4_promote_unmet`: a `decision promote` at an instant where a criterion fails is a REPAIR writ;
  mutant: never raised; twin: one where all hold.
- `promote_refused`: the verb refuses `promote` while `status.py` prints SHORT or STOP; mutant: the
  check dropped; twin: all met, the entry signed.
- `escalated`: a writ past its deadline prints ESCALATED and names the sovereign; mutant: silent.
- `wealth_arithmetic`: on a fixed sequence at p₀ = 0.41, six successes give E ≥ 20 and five do not;
  mutant: p₀ re-estimated from the sequence.
- `item_before_open`: an item raised before the `promote` is not counted; mutant: counted.
- `item_collapsed`: six forecasts resolved against one `evidence` string are one item; mutant: counted
  singly; twin: distinct evidence, distinct items.
- `repair_attributed_once`: one repair during the life of two open writs sets Y = 0 on the earlier
  only; mutant: on both.
- `window_from_the_promote`: C1b opens at the `ts` of `decision promote C1a`, on a fixture holding a
  `budget` decision and the `promote`; mutant: any decision; ends at L0's `resolves_by`, L0 found by
  `args.id`; mutant: the latest counsel forecast.
- `evidence_unhashed`: a resolution whose evidence file does not hash to its name does not count;
  mutant: the re-hash skipped; twin: the matching file.
- `ratio_misclassified`: a world-typed forecast's resolution counts as object; mutant: counted as
  procedure; twin: a procedure forecast's resolution counts as procedure.
- `flooding_bounded`: a flood raises one writ per forecast; mutant: writs deduplicated by claim text;
  twin: one forecast, one writ.
- `veto_c1b`: a veto with subject `C1b` fails criterion 6; mutant: subject ignored.
- `map_printed`: the map's C1b rows read "code" at the exit prefix; mutant: a hand row passes.

## Refusal list
No new entry type; no kernel or kernel2 change; no cap change and no touch of the trusted base; no LLM
call in the clerk; no state kept between runs; no writ class beyond W1, W3, W4 — no proposal writ; no
invitation or election logic; no change to A4's bet; no reminder set by counsel's session once the
clerk is on `main`; no wish transcribed by counsel. Counsel writes no code: this brief, the replies,
the RUNBOOK section and the report are counsel's; `tools/clerk.py`, `status.py`'s additions, the
verb's refusal, the deletion and `tests/` the builder's; the pins the reviewer's.

## Stop and report if
the clerk does not fit under the cap (report the shortfall in lines); a writ class not listed here is
needed; the two checkers disagree; a sovereign repair is needed to discharge an item (a failed item,
recorded — never a redefinition).

## Deliverables
`tools/clerk.py`; `status.py` reading `decision promote`, L0, the tree and the map; `tools/jack
decision` refusing an unlawful `promote`; `tests/test_clerk.py`; the pins; RUNBOOK `jack clerk`; the
deletion of the genesis tool and its test; `transcripts/WISHES.md` as the sovereign's; L0–L5 entered;
the C1b report in REPORT.md's form; the C2 brief text, written at C1b's exit from the report.

## Counsel's forecasts on this window (entered after this brief's acceptance, before the `promote`)
| id | claim | p |
|---|---|---|
| L0 | **the promotion forecast**: every pre-stated criterion of this brief holds on the exit prefix by L0's `resolves_by`, which is the window's end — C1b promoted, not failed | 0.55 |
| L1 | the attack test is green on its first `tests` run on `main` | 0.6 |
| L2 | liveness E ≥ 20 within 7 days of the `promote` (a forecast about the window, not a term of it; the readers say 0.30 and 0.65) | 0.55 |
| L3 | at least one item is discharged only after a sovereign repair (Y = 0) | 0.5 |
| L4 | A5 is cited by or refuses an act by 29 December (the first reader says 0.75) | 0.65 |
| L5 | the clerk, its tests and pins fit under 6,200 with no push | 0.65 |
