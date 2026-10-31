# Brief C1b — the clerk (draft v4, 31 October 2026; finalised from the C1a report at C1a's exit)

Counsel's text, in BRIEF-C1's form. v2 answered `transcripts/REVIEW-C1b-A5.md` (gpt-6-astra, BLOCK on
F5–F8); v3 answered `transcripts/REVIEW-C1b-v2.md` (gemini-4-argon, ACCEPT WITH OBLIGATIONS F1–F6); v4
answers `transcripts/REVIEW-C1b-v3.md` (gpt-6-astra, BLOCK on F1: the collapsed item regrouped
outcomes already bet on, against A4.3) as `transcripts/REPLY-REVIEW-C1b-v3.md` sets out. Its spine is
PLAN-20261030 §4's enforcement map: each criterion is a row that has a witness on the record, in
witnessed order. Where it names code, the builder builds it and the reviewer pins it; counsel writes
none.

## Precondition
A5 in force. `tools/status.py` on `main`. Every C1a criterion holding on the current prefix (the tool
prints it), so that the sovereign's `decision promote C1a` is lawful under A5 clause 1.

## Purpose
C1a made the record say things about the world and be scored for them. C1b makes the court act on
its own obligations without the sovereign: every obligation derived from state and the clock, with a
deadline, raised where a party reads it, escalated when the deadline passes (maxim 3). The clerk
decides nothing about validity and holds no change power (§5). Its forcing witness is the record of
counsel's hand-set reminders, measured on the log: of the seven herald acts that have discharged
forecasts (merge entries 58, 71, 102, 106, 110, 140, 151), three discharged one late — seq 45 by
1.2 h, 46/47 by 8.2 h, 56 by 3.8 h after `resolves_by`.

## Scope
No new entry type and no kernel change. Writs are *derived* state, recomputable by anyone from
`log.jsonl`, the tree, the clock and GitHub's REST view of the repository, discharged by entries that
already exist. `invite` and `accept` are C2's, with `wish`, in one kernel change and one run of record;
**until then a wish of the sovereign's is a `proposal` signed by him appending to
`transcripts/WISHES.md`** — on the log, under his key, distinguishable as the only `proposal` entries
that key signs (he signs no other). A wish is never an item (§7: wishes are never scored); a wish not
entered is not a wish; counsel transcribes none. The acts table counts it once the classifier reads
`log.jsonl` — counsel's obligation, outside this brief. **The trusted base is not touched.** The
clerk, its tests and its pins are built under the cap of 6,200. `tools/genesis.py` (80 counted lines,
unused since seq 0; a second log is not this repository's) is deleted, and with it the genesis tests
of `tests/test_genesis.py`; that file's `Digest` class — `tools/digest.py` against the judge's digest,
the refusal of symbolic links and submodules in the trusted base — still serves `jack merge` and
`jack push` and is kept, in a file of its own. The builder reports the headroom this leaves. `sim/run.py`
and `tools/vectors.py` stay: `tests/test_sim.py` and `tests/test_vectors.py` exercise them today, which
is use, not anticipation. If the clerk does not fit, the builder stops and reports the shortfall in
lines; a push is decided on that number, never before it, and until then criterion 3 stands as written.

## Order of acts, and the clock
1. This brief merged with its fourth read on the record. Counsel enters **L0**, the promotion
   forecast, with `args.id` = `"L0"` so that `status.py` finds it, and `resolves_by` no later than
   fourteen days after L0's own `ts` — the maximum the sovereign's budget decision names (seq 50); the
   `promote` follows L0, so the bound holds from the `promote` too. Nothing in this brief states the
   window's end except by naming L0.
2. **One decision.** `decision promote C1a` closes C1a (A5 clause 1) and **opens C1b at its `ts`**.
   `tools/jack decision` signs `promote <window>` only when `status.py` prints `promote <window>:
   lawful`, and refuses otherwise, so an unlawful `promote` is not entered rather than detected. The
   window ends at the earlier of L0's `resolves_by` and a `decision promote C1b` entered once the
   criteria below hold (A5).
3. p₀, α and the attack list are committed here, before step 2, and never tuned after.

## The clerk (`tools/clerk.py`; the builder's)
Run on a timer or by hand; it keeps no state between runs (level-triggered: a missed tick costs
nothing). It prints every open writ — the obligation, who may discharge it, the deadline — and marks
one past its deadline **ESCALATED**, naming the sovereign. Writ classes, each with deadline and discharge:
- **W1 forecast**: every `forecast` entered after the opening is a writ from its entry; holders: every
  key with `resolution` power whose principal is not the forecaster's; deadline: `resolves_by` itself
  — the witnesses above are failures only under that deadline, and a grace period would make the
  incumbent's record perfect; discharged by a `resolution`. (A writ is overdue when the clock is
  *strictly after* `resolves_by`; at equality it is not.)
- **W3 unwitnessed merge**: a `merge` entry on `main` whose `commit` had no green `tests` run before the
  merge commit's time; holder: counsel; discharged by a COUNSEL-OPEN line naming it as precedent.
- **W4 window state**: every line of `status.py` that is not `met`; holder: counsel; deadline: the
  window's end. A `decision promote` on the log entered while a criterion did not hold at its instant
  is printed as a sovereign REPAIR; since the verb refuses one, its presence means a hand-made entry.
There is no proposal writ: every herald merge since the herald's key (seq 51) completed within
seventeen minutes of its `proposal` entry, and a class with no witness is not built (PLAN §4).
Re-invitation of another party or model is C2's.

`status.py` reads C1b from the log: it opens at the `ts` of the `decision` with kind `promote` and
subject `C1a` and ends at L0's `resolves_by`. For `promote <window>` it prints one line, `lawful` or
`refused: <every criterion not established>`: criteria 3 (counted lines, kernel within 500,
`judge/scope.json` equal to SPEC §10's block), 4, 6 (a veto refuses) and the ratio from the tree and
the log; criteria 1, 2 and 5 from a `tests` run on the tree's commit supplied to it (`--run`), absent
which they are unverified and refuse. The verb reads that line and nothing else.

## Liveness: the statistic, the null, the bet
- **Item**: the herald's act. The resolutions landed by one `merge` entry — the run of entries since the
  previous main-ending entry, ending at that merge — are one item, finalised at that merge's seq. A
  writ whose `resolves_by` passes undischarged is an item of its own, Y = 0, finalised at the first
  entry whose `ts` is strictly after `resolves_by`; a later resolution of it adds no item. Items are
  ordered by finalising seq, expired writs before a batch at the same seq, by forecast seq. **An item
  once finalised is never regrouped**: no later entry, evidence string or merge changes an earlier
  item or any bet already placed (A4.3). There is no evidence collapse — the batch is the collapse.
- **Yᵢ = 1** iff every resolution in the item was entered not after its forecast's `resolves_by`. The
  statistic has no repair term: the sovereign's repairs are counted weekly from the acts table, which
  arrives days after the acts and names minutes, and an outcome must be fixed when its bet is.
- **Null, p₀ = 5/9**, the incumbent measured on this log with this statistic: of the seven herald acts
  above, four were timely (merges 102, 106, 140, 151) and three were not (58, 71, 110); Laplace gives
  (4 + 1)/(7 + 2). This replaces v3's mapping from assize's repairs per merge (0.41), which both
  readers called a modelling assumption; assize's figure is reported beside it, not bet on. Under A4
  clause 3, nine consecutive timely acts carry E to 22.0 and eight to 13.6; ten with one failure give
  6.8. Committed here; never re-estimated.
- **Flooding, bounded not stopped.** Any number of forecasts resolved in one merge are one item. Six
  trivial forecasts resolved in six merges are six items and cost six forecasts, six resolutions, six
  proposals and six merges — twenty-four procedure entries against no object, which the ratio reports
  (A3.4) and the record shows. No rule decidable from the log stops a determined flooder without a
  constant; what stops one is the veto (criterion 6), on the record. The programme's own flow —
  world-typed forecasts resolved from evidence by another principal — is not an attack.
- **Bet**: A4 clause 3, wealth continued (C1a bet nothing: it had no liveness statistic); λᵢ from the
  Laplace estimate over the items so far; E ≥ 20 promotes; α = 0.05.
- **Reported, not tested**: repairs per week; the acts table's columns; assize's repairs per merge.

## Safety: the attack run before any item counts
`tests/test_clerk.py` builds its own logs (not the simulator's seeds, four of whose first five
`stalling` cases carry no forecast) and asserts: a stalled forecast is a W1 writ from its entry and
ESCALATED strictly after `resolves_by`; a flood of forecasts raises one writ each and leaves the rest
printed; two runs over the same inputs print byte-identical output (a test, not a pin: a pure function
has no guard to weaken). The simulator's `stalling` and `flooding` kinds are run through both checkers
as before (criterion 2). No item counts before the first green run of this test on `main`.

## Pre-stated criteria for C1b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds (C1a criterion 2, unchanged).
3. Counted lines within the cap of 6,200; the kernel within 500; `judge/scope.json` and SPEC §10's
   block unchanged.
4. The attack test green on `main` before the first counted item.
5. Liveness E ≥ 20 under the bet above on items finalised after the opening.
6. No `decision` of kind `veto` with subject `C1b`.
7. The enforcement map reprinted by `status.py` shows the rows C1b moves — obligations from state and
   clock (W1), window state (W4), the herald's merge on green (W3), windows as maxima (A5, by the
   verb's refusal) — with an enforcer that is code; the runner's rows and elections are outside this
   brief and are not read.
Reported: the procedure : object ratio (A3.4 applies); J7; the weekly acts table.

## Pins (the reviewer's), each with its named mutant and passing twin
- `overdue_strictly_after`: written `resolves_by < now`; a writ at `resolves_by` exactly is not
  overdue; mutant: `<=`; twin: one second after is overdue.
- `w1_from_entry`: a forecast is a W1 writ at its entry, not at its lateness; mutant: raised only when
  overdue; twin: a resolved forecast is no writ.
- `self_holder`: both the forecaster and another principal hold `resolution` power; only the other is
  named; mutant: the filter dropped.
- `w3_unwitnessed`: a merge whose commit has no earlier green `tests` run is a W3 writ, on a synthetic
  runs listing holding a failed `tests` run and a green one *after* the merge's time; mutant: any run
  accepted; twin: a green run before the merge.
- `w4_promote_unmet`: a `decision promote` at a prefix where a criterion fails is a REPAIR writ, and a
  later success does not erase it; mutant: never raised; twin: all held at that prefix.
- `promote_refused`: a veto, a SHORT line, a STOP line and a missing `--run` each print `refused` and
  the verb signs nothing; all met with a green run prints `lawful` and signs; mutant: the check dropped.
- `escalated`: a writ past its deadline prints ESCALATED and names the sovereign; before it, an
  ordinary open writ; mutant: silent.
- `wealth_arithmetic`: on a fixed sequence at p₀ = 5/9, nine successes give E ≥ 20 and eight do not;
  mutant: p₀ re-estimated from the sequence.
- `item_before_open`: a forecast entered before the `promote` and resolved after it adds no item; an
  otherwise identical one entered after does; mutant: counted.
- `item_is_batch`: six timely resolutions in one merge are one item; mutant: counted singly; twin: six
  merges, six items.
- `regroup_scored_items`: after six items are scored, a merge discharging two new writs that cite two
  of the old items' evidence strings appends one item and changes no earlier item or bet; mutant:
  evidence-component regrouping (the reviewer's extension: E 30.07 to 14.39); twin: fresh evidence in
  separate merges appends outcomes.
- `expired_writ_zero`: a writ unresolved past `resolves_by` is an item with Y = 0 at the first later
  entry, and its late resolution adds no item; mutant: the late resolution counted as a success.
- `window_from_the_promote`: C1b opens at the `ts` of `decision promote C1a` and ends at L0's
  `resolves_by`, on a fixture with a `budget` decision *after* the `promote` and a non-L0 counsel
  forecast *after* L0 with a different date; mutant: the latest decision; mutant: the latest counsel
  forecast.
- `evidence_unhashed`: a present file whose bytes do not hash to its name does not count; mutant: the
  re-hash skipped; twin: the matching file.
- `ratio_misclassified`: a world-typed forecast's resolution counts as object; mutant: counted as
  procedure; twin: a procedure forecast's resolution counts as procedure.
- `flooding_bounded`: two forecasts with identical claim text raise two writs; mutant: deduplicated by
  claim text; twin: one forecast, one writ.
- `veto_c1b`: a veto with subject `C1b` fails criterion 6 and one on another subject does not; mutant:
  subject ignored.
- `map_printed`: a C1b row labelled hand fails criterion 7; all C1b rows code passes; excluded rows may
  stay hand; mutant: a hand row passes.

## Refusal list
No new entry type; no kernel or kernel2 change; no cap change and no touch of the trusted base; no LLM
call in the clerk; no state kept between runs; no writ class beyond W1, W3, W4 — no proposal writ; no
repair term and no classifier input in the statistic; no invitation or election logic; no change to
A4's bet; no reminder set by counsel's session once the clerk is on `main`; no wish transcribed by
counsel. Counsel writes no code: this brief, the replies, the RUNBOOK section and the report are
counsel's; `tools/clerk.py`, `status.py`'s additions, the verb's refusal, the deletion and `tests/`
the builder's; the pins the reviewer's.

## Stop and report if
the clerk does not fit under the cap (report the shortfall in lines); a writ class not listed here is
needed; the two checkers disagree; a sovereign repair is needed to discharge an item (a failed item,
recorded — never a redefinition).

## Deliverables
`tools/clerk.py`; `status.py` reading `decision promote`, L0, the tree, a `--run` and the map, and
printing the `promote` line; `tools/jack decision` reading it; `tests/test_clerk.py`; the pins; RUNBOOK
`jack clerk`; the deletion of the genesis tool and its tests with the `Digest` coverage kept;
`transcripts/WISHES.md` as the sovereign's; L0–L5 entered; the C1b report in REPORT.md's form; the C2
brief text, written at C1b's exit from the report.

## Counsel's forecasts on this window (entered after this brief's acceptance, before the `promote`)
| id | claim | p |
|---|---|---|
| L0 | **the promotion forecast**: every pre-stated criterion of this brief holds on the exit prefix by L0's `resolves_by`, which is the window's end — C1b promoted, not failed | 0.5 |
| L1 | the attack test is green on its first `tests` run on `main` | 0.6 |
| L2 | liveness E ≥ 20 within 7 days of the `promote` — nine timely herald acts in seven days (the readers say 0.30, 0.65 and 0.40 on v2/v3's statistics) | 0.3 |
| L3 | at least one item scores Y = 0 in the window | 0.7 |
| L4 | A5 is cited by or refuses an act by 29 December (the first reader says 0.75) | 0.65 |
| L5 | the clerk, its tests and pins fit under 6,200 with no push (the third reader says 0.25) | 0.5 |
