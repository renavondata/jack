# Brief C1b — the clerk (draft v7, 31 October 2026; finalised from the C1a report at C1a's exit)

Counsel's text, in BRIEF-C1's form. v2 answered `transcripts/REVIEW-C1b-A5.md` (gpt-6-astra, BLOCK on
F5–F8); v3 answered `transcripts/REVIEW-C1b-v2.md` (gemini-4-argon, ACCEPT WITH OBLIGATIONS F1–F6); v4
answered `transcripts/REVIEW-C1b-v3.md` (gpt-6-astra, BLOCK on F1, regrouped outcomes); v5 answered
`transcripts/REVIEW-C1b-v4.md` (gpt-6-astra, BLOCK on F3: v4 dropped the charter's "no repair by Guy"
from the success condition); v6 answered `transcripts/REVIEW-C1b-v5.md` (gpt-6-astra, BLOCK on F1: an
unnamed repair attributed to the oldest open writ); v7 answers `transcripts/REVIEW-C1b-v6.md`
(gpt-6-astra, BLOCK on F1: a repair naming one beneficiary still let a second beneficiary score as
repair-free) as `transcripts/REPLY-REVIEW-C1b-v6.md` sets out: no named scope is trusted, and every
sovereign repair taints every writ open at its instant. Its spine is PLAN-20261030 §4's enforcement map: each criterion is a row that has a witness on the
record, in witnessed order. Where it names code, the builder builds it and the reviewer pins it;
counsel writes none.

## Precondition
A5 in force. `tools/status.py` on `main`. Every C1a criterion holding on the current prefix (the tool
prints it), so that the sovereign's `decision promote C1a` is lawful under A5 clause 1.

## Purpose
C1a made the record say things about the world and be scored for them. C1b makes the court act on
its own obligations without the sovereign: every obligation derived from state and the clock, with a
deadline, raised where a party reads it, escalated when the deadline passes (maxim 3). The clerk
decides nothing about validity and holds no change power (§5). Its forcing witness is the record of
counsel's hand-set reminders, measured on the log: four writs expired undischarged — seq 45 (resolved
1.2 h late), 46 and 47 (8.2 h), 56 (3.8 h) — against five herald acts whose every resolution was timely.

## Scope
No new entry type and no kernel change. Writs are *derived* state, recomputable by anyone from
`log.jsonl`, the tree, the clock and GitHub's REST view of the repository, discharged by entries that
already exist. `invite` and `accept` are C2's, with `wish`, in one kernel change and one run of record;
**until then a wish of the sovereign's is a `proposal` signed by him appending to
`transcripts/WISHES.md`** — on the log, under his key; every `proposal` his key signs is a wish and he
signs no other. A wish is never an item (§7: wishes are never scored); a wish not entered is not a
wish; counsel transcribes none. The acts table counts it once the classifier reads `log.jsonl` —
counsel's obligation, outside this brief. **The trusted base is not touched.** The clerk, its tests
and its pins are built under the cap of 6,200. `tools/genesis.py` (80 counted lines, unused since
seq 0; a second log is not this repository's) is deleted, and with it the genesis tests of
`tests/test_genesis.py`; that file's `Digest` class — `tools/digest.py` against the judge's digest, the
refusal of symbolic links and submodules in the trusted base — still serves `jack merge` and
`jack push` and is kept, in a file of its own. The builder reports the headroom this leaves.
`sim/run.py` and `tools/vectors.py` stay: `tests/test_sim.py` and `tests/test_vectors.py` exercise
them today, which is use, not anticipation. If the clerk does not fit, the builder stops and reports
the shortfall in lines; a push is decided on that number, never before it, and until then criterion 3
stands as written.

## Order of acts, and the clock
1. This brief merged with its seventh read on the record. Counsel enters **L0**, the promotion
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
  key with `resolution` power whose principal is not the forecaster's; deadline: `resolves_by` itself,
  the obligation the entry already carries (SPEC §5) — every late case on the record would be timely
  under a 48 h grace, which would leave the deadline no witness; discharged by a `resolution`. (A writ
  is overdue when the clock is *strictly after* `resolves_by`; at equality it is not.)
- **W3 unwitnessed merge**: a `merge` entry on `main` whose `commit` had no green `tests` run before the
  merge commit's time; holder: counsel; discharged by a COUNSEL-OPEN line naming it as precedent.
- **W4 window state**: every line of `status.py` that is not `met`, including the count of the
  sovereign's acts off the log (from the acts table; §7 requires none); holder: counsel; deadline: the
  window's end. A `decision promote` on the log entered while a criterion did not hold at its instant
  is printed as a sovereign REPAIR; since the verb refuses one, its presence means a hand-made entry.
There is no proposal writ: every herald merge since the herald's key (seq 51) completed within
seventeen minutes of its `proposal` entry, and a class with no witness is not built (PLAN §4).
Re-invitation of another party or model is C2's.

`status.py` reads C1b from the log: it opens at the `ts` of the `decision` with kind `promote` and
subject `C1a` and ends at L0's `resolves_by`. For `promote <window>` it prints one line, `lawful` or
`refused: <every criterion not established>`. From the tree and the log: criterion 3 (counted lines,
kernel within 500, `judge/scope.json` equal to SPEC §10's block), 4, 5 (**live E, computed from the
log by `status.py` itself** — a green test proving that nine synthetic successes cross 20 is not nine
successes on this prefix), 6 (a veto refuses), 7 (a C1b map row still hand refuses) and the ratio.
Criteria 1 and 2 from a `tests` run the verb fetches from the repository's Actions API for the
tree's exact commit — `status.py` verifies the workflow by its file path `.github/workflows/tests.yml`
(not its display name), `event` push, `head_branch` main, `head_sha` equal to the tree's commit,
`conclusion` success; absent, pending, failed, another workflow's, another commit's or a pull
request's run leaves them unverified and refuses; the operator types no run id. The verb reads that
line and nothing else.

## Liveness: the statistic, the null, the bet
- **Item**: the herald's act, under these conventions, applied entry by entry in log order:
  (i) before an entry is processed, every open writ whose `resolves_by` is strictly before the entry's
  `ts` is finalised as an item of its own with Y = 0, in forecast-seq order; (ii) a resolution of a
  writ already finalised is ignored for items; (iii) the eligible resolutions since the previous
  main-ending entry, ending at a `merge` entry, are one item finalised at that merge's seq, and a
  merge with no eligible resolution forms no item; (iv) a resolution signed by the sovereign's key of a
  writ not yet finalised is an item of its own at its entry with Y = 0 — completion by the sovereign is
  a repair — and never joins a batch; (i) and (ii) take priority, so an expired writ he resolves stays
  one zero; a `merge` signed by his key finalises its eligible batch as an item with Y = 0 under the
  repair term below, and none if the batch is empty; his other entries are boundaries that form no
  item, and a batch they clear is not resurrected as expiry items. Items are ordered by finalising
  seq, ties by forecast seq. **An item once
  finalised is never regrouped**: no later entry, evidence string or merge changes an earlier item or
  any bet already placed (A4.3). There is no evidence collapse — the batch is the collapse.
- **Yᵢ = 1** iff every resolution in the item was entered not after its forecast's `resolves_by` **and
  no repair by the sovereign is attributed to the item** (§6). A repair is what §7 makes it on the log,
  by its complement: every entry signed by the sovereign's key except `genesis`, `key`, `amend`, `push`,
  a `proposal` (a wish) and a `decision` of a kind other than `fix` — so a `decision fix`, a
  `resolution`, a `merge` and, by §7's letter, a `forecast` (C2 may reclassify the last; until then it
  counts). **Attribution trusts no scope**: every sovereign repair is attributed to **every writ open
  at its `ts`** — a `subject` naming one beneficiary does not establish that no other open writ needed
  the same act, so no named scope narrows the taint; the `subject` is for the record. A completion
  that may have needed the sovereign cannot count positively; the court's incentive is to need him
  not at all, which is §6's sentence. A repair at an instant with no open writ taints nothing. A repair
  entered after an item was finalised changes neither that item's Y nor any stake (A4.3) — it taints
  what is open at its own entry, and is a late report, a §7 violation in itself, printed by
  `status.py` as a W4 line `late-reported repairs: n` that refuses `promote` while n > 0 in the
  window. A repair made off the log is counted from the acts table as a W4 line, held by counsel, and
  never enters the bet. The sovereign's RUNBOOK line is `jack decision fix "<what>"`, entered when the
  act is made; a recorder that enters it for him (the C2 brief's first obligation) needs no precision
  about beneficiaries, since none is used.
- **Null, p₀ = 6/11**, committed with its provenance. The replay of the item rule over the log
  through seq 163 yields nine items — four expired writs (45 at seq 50; 46 and 47 at 68; 56 at 103)
  and five herald batches (merges 102, 106, 110, 140, 151), all five timely. Under v5's attribution
  (a repair to the oldest open writ) none of the five carried a repair, Laplace (5 + 1)/(9 + 2) =
  6/11; under this brief's attribution the sovereign's merge 44 and forecasts 45–47 taint every writ
  then open, among them 38, whose batch (merge 110) is therefore Y = 0 — four successes, Laplace 5/11.
  The brief commits the more demanding 6/11, a constant measured on the incumbent's prefix before the
  window (A4.2; a brief may tighten), and states that it is not this rule's own replay, which is 5/11.
  Under A4 clause 3 nine consecutive
  successes carry E to 25.5 and eight to 15.5; ten successes followed by one failure give 7.8.
  Assize's repairs per merge (3.6, 0.89, 2.9) are reported beside it, not bet on. Committed here;
  never re-estimated.
- **Flooding, bounded not stopped.** Any number of forecasts resolved in one merge are one item. Six
  trivial forecasts resolved in six merges are six items and cost six forecasts, six resolutions, six
  proposals and six merges — twenty-four procedure entries against no object, which the ratio reports
  (A3.4) and the record shows. No rule decidable from the log stops a determined flooder without a
  constant; what stops one is the veto (criterion 6), on the record. The programme's own flow —
  world-typed forecasts resolved from evidence by another principal — is not an attack.
- **Bet**: A4 clause 3, wealth continued (C1a bet nothing: it had no liveness statistic); λᵢ from the
  Laplace estimate over the items so far; E ≥ 20 promotes; α = 0.05.
- **Reported, not tested**: repairs per week on and off the log; the acts table's columns; assize's
  repairs per merge.

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
3. Counted lines within the cap of 6,900 — 6,200 as written at the seventh read, raised once by the
   measured push at seq 197 (`transcripts/PUSH-cap-6900.md`, 31 Oct) under §Scope's rule that a push is
   decided on the measured shortfall and never before it; the kernel within 500; `judge/scope.json` and
   SPEC §10's block unchanged since that push (Amendment 1 below).
4. The attack test green on `main` before the first counted item.
5. Liveness E ≥ 20 under the bet above on items finalised after the opening, computed from the log.
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
  named, and it is named; mutant: the filter dropped.
- `w3_unwitnessed`: a merge whose commit has no earlier green `tests` run is a W3 writ, on a synthetic
  runs listing holding a failed `tests` run and a green one *after* the merge's time; mutant: any run
  accepted; twin: a green run before the merge.
- `w4_promote_unmet`: a `decision promote` at a prefix where a criterion fails is a REPAIR writ, and a
  later success does not erase it; mutant: never raised; twin: all held at that prefix.
- `promote_refused`: a veto, a SHORT line, a STOP line, a hand C1b map row and live E below 20 each
  print `refused` and the verb signs nothing; all met prints `lawful` and signs; mutant: the check
  dropped; mutant: a green regression run substituted for live E.
- `run_verified`: an absent, pending, failed, other-workflow, other-commit or pull-request run leaves
  criteria 1 and 2 unverified and refuses, and the verb signs nothing; the `tests.yml` push-to-main run
  on the tree's commit with `conclusion` success verifies; mutant: any run accepted; mutant: `event`
  unchecked.
- `escalated`: a writ past its deadline prints ESCALATED and names the sovereign; before it, an
  ordinary open writ; mutant: silent.
- `wealth_arithmetic`: on a fixed sequence at p₀ = 6/11, nine successes give E ≥ 20 and eight do not;
  mutant: p₀ re-estimated from the sequence.
- `item_before_open`: a forecast entered before the `promote` and resolved after it adds no item; an
  otherwise identical one entered after does, distinguished by seq when the `ts` is shared; mutant:
  counted.
- `item_is_batch`: six timely resolutions in one merge are one item and six merges are six — asserted
  as counts; mutant: counted singly.
- `regroup_scored_items`: after six items are scored, a merge discharging two new writs that cite two
  of the old items' evidence strings appends one item and changes no earlier item or bet — at p₀ = 6/11
  a seventh success, never a return to the five-item wealth; mutant: evidence-component regrouping;
  twin: fresh evidence in separate merges appends outcomes. Assert identities, count and wealth.
- `expired_writ_zero`: a writ unresolved past `resolves_by` is a Y = 0 item at the first later entry,
  finalised before that entry is processed even when the entry is its own late resolution; the late
  resolution adds no item; a merge holding only finalised writs adds no item; a mixed batch keeps only
  its fresh writs; mutant: the late resolution counted as a success; mutant: `all([])` counted as a
  success.
- `repair_erased_from_success`: two identical timely batches, one with a `decision fix` entered while
  its writ is open; that item's Y is 0, asserted on Y and not only on wealth; mutant: the repair
  predicate dropped; twin: the same timely completion without repair.
- `repair_taints_all_open`: writs A and B open; a `decision fix` — naming A, naming B, or naming
  nothing — precedes B's timely resolution and herald merge; B's item scores 0 in all three cases, and
  A's when finalised; mutant: a named subject restricts the taint to the named writ; mutant: the
  repair sent to the oldest open writ alone; twin: the same B completion with no repair scores 1.
- `replay_merge_110`: on the real prefix through seq 163, merge 110's item is Y = 0 (writ 38 open at
  seqs 44–47) and the items number nine with four successes; mutant: oldest-only attribution gives it
  1; twin: the same prefix with the sovereign's entries 44–47 removed gives it 1.
- `late_report_immutable`: a `decision fix` naming an item already finalised changes no Y and no stake,
  and `status.py` prints `late-reported repairs: 1` and refuses `promote`; mutant: the item revised;
  mutant: the line not printed.
- `sovereign_resolution_zero`: a fresh resolution signed by the sovereign's key is its own Y = 0 item
  and adds nothing at the next merge; an expired writ he resolves stays one zero; a sovereign merge
  with an eligible batch finalises it at Y = 0; mutant: counted in the next merge's batch as a success.
- `window_from_the_promote`: C1b opens at the `ts` of `decision promote C1a` and ends at L0's
  `resolves_by`, on a fixture with a `budget` decision *after* the `promote` and a non-L0 counsel
  forecast *after* L0 with a different date, each boundary asserted separately; mutant: the latest
  decision; mutant: the latest counsel forecast.
- `evidence_unhashed`: a present file whose bytes do not hash to its name does not count; mutant: the
  re-hash skipped; twin: the matching file.
- `ratio_misclassified`: a world-typed forecast's resolution counts as object; mutant: counted as
  procedure; twin: a procedure forecast's resolution counts as procedure.
- `flooding_bounded`: two forecasts with identical claim text at distinct seqs raise two writs; mutant:
  deduplicated by claim text; twin: one forecast, one writ.
- `veto_c1b`: a veto with subject `C1b` fails criterion 6 and one on another subject does not; mutant:
  subject ignored.
- `map_printed`: a C1b row labelled hand fails criterion 7; all C1b rows code passes; excluded rows may
  stay hand; mutant: a hand row passes.

## Refusal list
No new entry type; no kernel or kernel2 change; no cap change and no touch of the trusted base; no LLM
call in the clerk; no state kept between runs; no writ class beyond W1, W3, W4 — no proposal writ; no
classifier input in the statistic; no success condition weaker than §6's; no invitation or election
logic; no change to A4's bet; no reminder set by counsel's session once the clerk is on `main`; no
wish transcribed by counsel. Counsel writes no code: this brief, the replies, the RUNBOOK section and
the report are counsel's; `tools/clerk.py`, `status.py`'s additions, the verb's refusal, the deletion
and `tests/` the builder's; the pins the reviewer's.

## Stop and report if
the clerk does not fit under the cap (report the shortfall in lines); a writ class not listed here is
needed; the two checkers disagree; a sovereign repair is needed to discharge an item (a Y = 0 item,
recorded — never a redefinition).

## Deliverables
`tools/clerk.py`; `status.py` reading `decision promote`, L0, the tree, the verified run and the map,
computing live E and printing the `promote` line; `tools/jack decision` fetching the run and reading
that line; `tests/test_clerk.py`; the pins; RUNBOOK `jack clerk` and the sovereign's `jack decision
fix "<what>"` when a hand repair is made (§7); the deletion of the genesis tool and its tests with the
`Digest` coverage kept; `transcripts/WISHES.md` as the sovereign's; L0–L5 entered; the C1b report in
REPORT.md's form; the C2 brief text, written at C1b's exit from the report.

## Counsel's forecasts on this window (entered after this brief's acceptance, before the `promote`)
| id | claim | p |
|---|---|---|
| L0 | **the promotion forecast**: every pre-stated criterion of this brief holds on the exit prefix by L0's `resolves_by`, which is the window's end — C1b promoted, not failed (the fifth and sixth reads say 0.30) | 0.35 |
| L1 | the attack test is green on its first `tests` run on `main` | 0.6 |
| L2 | liveness E ≥ 20 within 7 days of the `promote` — nine timely, repair-free herald acts in seven days (the fourth read says 0.25) | 0.25 |
| L3 | at least one item scores Y = 0 in the window (the fourth read says 0.75; under this attribution one hand repair of the sovereign's zeros every open writ) | 0.8 |
| L4 | A5 is cited by or refuses an act by 29 December (the first reader says 0.75) | 0.65 |
| L5 | the clerk, its tests and pins fit under 6,200 with no push (the reads say 0.25, 0.25, 0.20) | 0.3 |

## Amendment 1 (31 Oct, counsel; after the push at seq 197)
§Scope said "a push is decided on that number, never before it, and until then criterion 3 stands as
written." The number came in at 6,874 (PR #61, the pins on the consolidated clerk) and the sovereign pushed
the cap to 6,900 at seq 197; criterion 3 now reads 6,900 and "unchanged since that push". Nothing else in
the brief moves: the clerk, the statistic, p₀, the pins and L0–L5 stand, and L5 resolves 0 on the push, as
its own row said it would. `status.py`'s criterion 3 compares against the brief's number, so the builder
changes its constant to 6,900 on the record of this amendment (COUNSEL-OPEN 19); until that lands the
`promote` line reads `refused: criterion 3`, which is the correct reading of an unamended tool.
