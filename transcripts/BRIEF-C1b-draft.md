# Brief C1b — the clerk (draft v2, 30 October 2026; finalised from the C1a report at C1a's exit)

Counsel's text, in BRIEF-C1's form. v2 answers `transcripts/REVIEW-C1b-A5.md` (gpt-6-astra, BLOCK on
F5–F8) as `transcripts/REPLY-REVIEW-C1b-A5.md` sets out. Its spine is PLAN-20261030 §4's enforcement
map: each criterion is a row that has a witness on the record, in witnessed order. Where it names
code, the builder builds it and the reviewer pins it; counsel writes none.

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
`transcripts/WISHES.md`** — an entry, typed, counted as a decision by the acts classifier — and a wish
not entered is not a wish (§7). The trusted base is touched once, by the installing push: the counted
cap in `judge/scope.json` **and the identical block in SPEC §10** rise from 6,200 to 7,000, because
the clerk, its tests and the attack tests do not fit the 202 lines left. The 439 counted lines the
review found unused by criterion 2 (`sim/run.py`, `tools/genesis.py` with its test, `tools/vectors.py`)
are the reviewer's regeneration tools and the genesis tool, which C2's election vectors will need; they
are a C2 obligation to delete or defend, not a reason to keep the cap.

## Order of acts, and the clock
1. This brief merged with its second cold read on the record. Counsel enters **L0**, the promotion
   forecast, with `resolves_by` no later than fourteen days after the expected `promote` and in any
   case no later than the maximum the sovereign's budget decision names (seq 50); nothing in this
   brief states the window's end except by naming L0.
2. The installing push: `judge/scope.json`'s cap and SPEC §10's block, nothing else in the trusted
   base; no kernel source changes, so no run of record.
3. **One decision.** `decision promote C1a` closes C1a (A5 clause 1) and **opens C1b at its instant**.
   The window ends at the earlier of L0's `resolves_by` and a `decision promote C1b` entered once the
   criteria below hold (A5).
4. p₀, α and the attack list are committed here, before step 3, and never tuned after.

## The clerk (`tools/clerk.py`; the builder's)
Run on a timer or by hand; it keeps no state between runs (level-triggered: a missed tick costs
nothing). It prints every open writ — the obligation, who may discharge it, the deadline — and marks
one past its deadline **ESCALATED**, naming the sovereign. Writ classes, each with deadline and discharge:
- **W1 forecast**: every `forecast` entered after the opening is a writ from its entry; holders: every
  key with `resolution` power whose principal is not the forecaster's; deadline: 48 h after
  `resolves_by`; discharged by a `resolution`. (A forecast is overdue when the clock is *strictly after*
  `resolves_by`; at equality it is not.)
- **W2 proposal**: every open pull request with a `proposal` entry after the opening; holder: the
  herald; deadline: 24 h after its latest green `judge` and `tests` run; discharged by the merge or the
  PR's closure.
- **W3 unwitnessed merge**: a `merge` entry on `main` whose `commit` had no green `tests` run before the
  merge commit's time; holder: counsel; discharged by a COUNSEL-OPEN line naming it as precedent.
- **W4 window state**: `status.py`'s SHORT lines, a ratio above 5 : 1, and a `decision promote` entered
  while a criterion did not hold at its instant (printed as a sovereign REPAIR); holder: counsel;
  deadline: the window's end.
Re-invitation of another party or model is C2's.

## Liveness: the statistic, the null, the bet
- **Item**: a W1 or W2 writ raised after the opening — that is, every forecast and every proposal
  entered in the window, from its entry, not from its lateness.
- **Yᵢ = 1** iff the item is discharged before its deadline with no repair by the sovereign during its
  life (a repair is what the acts classifier types as one, in either repository).
- **Null, p₀ = 0.41**, and the map from the incumbent's series to this statistic, stated: assize's unit
  was the merged pull request and its measured series is repairs per merge (3.6, 0.89, 2.9 in three
  weeks); jack's unit is the item; the modelling assumption is repairs spread evenly over units, under
  which the share of units with none is e^{−r}: 0.03, 0.41, 0.06. The null takes the incumbent's best
  week. Under A4 clause 3 six consecutive successes carry E to 30.1 and five to 14.4; the mean week
  (0.09) would cross on three, which is why it is not the null. Committed here; never re-estimated.
- **Flooding, worked.** Six trivial forecasts resolved within 48 h would cross E ≥ 20. They are six
  procedure entries plus six resolutions of procedure against no object: A3.4's ratio moves toward
  the 5 : 1 stop with every one, and the stop is reported on the exit prefix. A flood of *object*
  items — world-typed forecasts resolved from evidence by a different principal — is not an attack but
  the programme. A resolution's principal differs from its forecast's by kernel; a proposal's herald
  differs from its proposer by key.
- **Bet**: A4 clause 3, wealth continued (C1a bet nothing: it had no liveness statistic); λᵢ from the
  Laplace estimate over the items so far; E ≥ 20 promotes; α = 0.05.
- **Reported, not tested**: repairs per week (unbounded); the acts table's columns.

## Safety: the attack run before any item counts
`tests/test_clerk.py` builds its own logs (not the simulator's seeds, four of whose first five
`stalling` cases carry no forecast) and asserts: a stalled forecast is a W1 writ from its entry and
ESCALATED strictly after `resolves_by` + 48 h; a flood of forecasts raises one writ each and leaves the
rest printed; two runs over the same inputs print byte-identical output. The simulator's `stalling`
and `flooding` kinds are run through both checkers as before (criterion 2). No item counts before the
first green run of this test on `main`.

## Pre-stated criteria for C1b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds (C1a criterion 2, unchanged).
3. Counted lines within the cap; the kernel within 500; `judge/scope.json` and SPEC §10's block
   unchanged after the installing push.
4. The attack test green on `main` before the first counted item.
5. Liveness E ≥ 20 under the bet above on items raised after the opening.
6. No `decision` of kind `veto` with subject `C1b`.
7. The enforcement map reprinted by `status.py` shows the rows C1b moves — obligations from state and
   clock (W1/W2), window state (W4), the herald's merge on green (W3), windows as maxima (A5) — with
   an enforcer that is code; the runner's rows and elections are outside this brief and are not read.
Reported: the procedure : object ratio (A3.4 applies); J7; the weekly acts table.

## Pins (the reviewer's), each with its named mutant and passing twin
- `overdue_strictly_after`: a forecast at `resolves_by` exactly is not overdue, one second after it is;
  mutant: `>=`; twin: the equality case.
- `w1_from_entry`: a forecast is a W1 writ at its entry, not at its lateness; mutant: raised only when
  overdue; twin: a resolved forecast is no writ.
- `self_holder`: a W1 writ never names the forecaster's principal; mutant: the filter dropped.
- `w2_deadline`: a proposal's deadline is 24 h after its latest green run; mutant: after its first.
- `w3_unwitnessed`: a merge whose commit has no earlier green `tests` run is a W3 writ, on a synthetic
  runs listing; mutant: any run accepted; twin: a green run before the merge.
- `w4_promote_unmet`: a `decision promote` at an instant where a criterion fails is a REPAIR writ;
  mutant: never raised; twin: one where all hold.
- `escalated`: a writ past its deadline prints ESCALATED and names the sovereign; mutant: silent.
- `wealth_arithmetic`: on a fixed sequence at p₀ = 0.41, six successes give E ≥ 20 and five do not;
  mutant: p₀ re-estimated from the sequence.
- `item_before_open`: an item raised before the `promote` is not counted; mutant: counted.
- `window_from_the_named_amend`, `evidence_unhashed`, `ratio_misclassified`: as in `status.py` today,
  pinned.
- `stalling_raises`, `flooding_bounded`, `clerk_deterministic`: the attack test's three assertions.
- `veto_c1b`: a veto with subject `C1b` fails criterion 6; mutant: subject ignored.
- `map_printed`: the map's C1b rows read "code" at the exit prefix; mutant: a hand row passes.

## Refusal list
No new entry type; no kernel or kernel2 change; no LLM call in the clerk; no state kept between runs;
no writ class beyond W1–W4; no invitation or election logic; no change to A4's bet; no reminder set by
counsel's session once the clerk is on `main`; no wish transcribed by counsel. Counsel writes no code:
this brief, the reply, the RUNBOOK section and the report are counsel's; `tools/clerk.py`, `status.py`'s
additions and `tests/` the builder's; the pins the reviewer's.

## Stop and report if
the cap would need to rise again; a writ class not listed here is needed; the two checkers disagree;
a sovereign repair is needed to discharge an item (a failed item, recorded — never a redefinition).

## Deliverables
`tools/clerk.py`; `status.py` reading `decision promote` and the map; `tests/test_clerk.py`; the pins;
RUNBOOK `jack clerk`; the push (cap and block); `transcripts/WISHES.md` as the sovereign's; L0–L4
entered; the C1b report in REPORT.md's form; the C2 brief text, written at C1b's exit from the report.

## Counsel's forecasts on this window (entered after this brief's acceptance, before the `promote`)
| id | claim | p |
|---|---|---|
| L0 | **the promotion forecast**: liveness E ≥ 20 on the exit prefix by L0's `resolves_by`, which is the window's end | 0.6 |
| L1 | the attack test is green on its first `tests` run on `main` | 0.6 |
| L2 | liveness E ≥ 20 within 7 days of the `promote` (a forecast about the window, not a term of it; the reviewer says 0.30) | 0.55 |
| L3 | at least one item is discharged only after a sovereign repair (Y = 0) | 0.5 |
| L4 | A5 is cited by or refuses an act by 29 December (the reviewer says 0.75) | 0.65 |
