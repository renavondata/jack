# Brief C1b — the clerk (draft of 30 October 2026; finalised from the C1a report at C1a's exit)

Counsel's text, in BRIEF-C1's form. It opens C1's second window. Where it names code, the builder
builds it and the reviewer pins it; counsel writes none. Everything it asks of the sovereign is
listed in one place (§Order of acts). Its spine is PLAN-20261030 §4's enforcement map: each
criterion below is a row that already has a witness on the record, in witnessed order, and nothing
else.

## Precondition
C1a's window closed by the sovereign's `decision` (under A5) or by its end instant, every C1a
criterion met on the exit prefix, the C1a report on `main`. A5 in force. `tools/status.py` on
`main` (PR #41). The simulator's `stalling` and `flooding` kinds exist (`sim/gen.py`).

## Purpose
C1a made the record say things about the world and be scored for them. C1b makes the court act on
its own obligations without the sovereign: every obligation derived from state and the clock,
carrying a deadline, raised where a party reads it, escalated when the deadline passes (maxim 3).
The clerk decides nothing about validity and holds no change power (§5). It replaces the reminders
that counsel's session has been setting by hand since 28 October, whose two failures (46/47 six hours
late; 56 four hours late) are this window's forcing witness.

## Scope
No new entry type and no kernel change: the clerk's writs are *derived* state, recomputable by
anyone from `log.jsonl`, the tree and the clock, and are discharged by entries that already exist
(`resolution`, `merge`, a PR's closure). `wish`, `invite` and `accept` (the 14 October draft) are
C2's, where elections need them. The trusted base is touched once, by the installing push: the code
cap in `judge/scope.json` rises from 6,200 to 7,000 counted lines, because the clerk, its tests and
the two attack tests do not fit in the 202 lines that remain and nothing in `sim/` or `harness/`
can be deleted without weakening C1a's criterion 2; the kernel's own 500-line cap does not move.

## Order of acts, and the clock
1. The sovereign's `decision` closing C1a (A5), then the `decision` opening C1b; both after this
   brief is on `main` with its cold read.
2. The installing push: `judge/scope.json`'s cap, and nothing else in the trusted base. No run of
   record is needed (no kernel or kernel2 source changes).
3. **The window opens at the `decision` opening C1b**; its maximum is fourteen days; it ends at the
   earlier of that instant and the sovereign's `decision` closing it once the criteria hold (A5).
   The promotion forecast (counsel's, entered before the window opens) carries the window's end as
   its `resolves_by`; no other date is law.
4. `p₀`, α and the attack list are committed in this file before step 1 and never tuned after.

## The clerk (`tools/clerk.py`; the builder's)
Run on a timer or by hand, it reads `log.jsonl`, the tree, the clock and GitHub's REST view of the
repository, and prints the open writs. A writ names the obligation, who may discharge it, and its
deadline; nothing is remembered between runs (level-triggered: a missed tick costs nothing).
Writ classes for C1b, each with its deadline and its discharge:
- **W1 overdue forecast**: a `forecast` with no `resolution` whose `resolves_by` has passed. Holders:
  every key with `resolution` power whose principal is not the forecaster. Deadline: 48 h after
  `resolves_by`. Discharged by a `resolution`.
- **W2 stale proposal**: an open pull request whose proposal head has had a green `judge` and
  `tests` run for 24 h with no `merge` entry, or whose `merge` entry has no green run after 2 h.
  Holders: the herald. Discharged by the merge or the PR's closure.
- **W3 unwitnessed merge**: a `merge` entry on `main` whose `commit` has no green `tests` run on its
  branch before the merge commit's time (the lapse on #31). Holder: counsel, as a precedent to file.
  Discharged by a line in COUNSEL-OPEN naming it.
- **W4 window state**: `tools/status.py`'s SHORT lines and any ratio above 5 : 1, as writs to counsel
  with the window's end as deadline.
Escalation is the deadline passing: a writ past its deadline is printed as **ESCALATED** with the
sovereign named, and counts against liveness (below). Re-invitation of another party is C2's.

## Liveness: the statistic, the null, the bet
- **Item**: a writ of class W1 or W2 raised by the clerk after the window opens.
- **Yᵢ = 1** iff the item is discharged before its deadline with no repair by the sovereign during
  its life (a repair is an act the acts classifier types as one, in either repository).
- **p₀ = 0.41**: the incumbent is assize; its series gives repairs per merge of 3.6, 0.89 and 2.9 in
  the three measured weeks; spreading repairs evenly over merges, the share of merges with none is
  e^{−r}: 0.03, 0.41, 0.06. The null takes the incumbent's **best** week, not its mean, because a
  challenger that beats only the mean has proved little. Committed here, never re-estimated.
- **Bet**: A4 clause 3, wealth continued from C1a's (which bet nothing: the window had no liveness
  statistic), λᵢ from the Laplace estimate over the items so far. E ≥ 20 promotes; α = 0.05.
- **Reported, not tested**: repairs per week (unbounded), the acts table's two columns.

## Safety: the attack run before any item counts
`tests/test_clerk.py` runs the clerk over simulated logs of kinds `stalling` (a proposer who never
resolves) and `flooding` (a proposer who enters forecasts faster than anyone resolves) and asserts:
every stalled forecast is a W1 writ by its deadline; a flood raises writs in proportion and never
stops the clerk from printing the rest; the clerk's output is identical on two runs over the same
inputs. Zero checker disagreements throughout the window (criterion 2 of C1a continues to hold).

## Pre-stated criteria for C1b, evaluated on the exit prefix
1. Every pin below KILLED with a passing twin in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and on the committed seeds (C1a criterion 2, unchanged).
3. Counted lines within the cap; the kernel within 500; `judge/scope.json` unchanged after the
   installing push.
4. The attack run clean before the first item; no item counted before it.
5. Liveness E ≥ 20 under the bet above, on items raised after the window opened.
6. No `decision` of kind `veto` with subject `C1b`.
7. The enforcement map (PLAN-20261030 §4) reprinted by `tools/status.py` with no row whose
   enforcer is "hand" and whose witness column is non-empty, save elections (C2's).
Reported: the procedure : object ratio (A3.4 applies); J7's figure; the weekly acts table.

## Pins (the reviewer's), each with its named mutant and passing twin
- `overdue_unlisted`: a forecast one second past `resolves_by` is a W1 writ; mutant: an off-by-one
  on the deadline; twin: a forecast one second before.
- `self_holder`: a W1 writ never names the forecaster among its holders; mutant: the filter dropped.
- `window_from_the_wrong_amend`: the window start is the named amendment's `ts`; mutant: the latest
  amendment's.
- `evidence_unhashed`: a world-typed resolution whose file is absent or mismatched does not count;
  mutant: existence checked, hash not.
- `ratio_misclassified`: a `counsel.programme` forecast is procedure; mutant: every forecast object.
- `stalling_raises`, `flooding_bounded`, `clerk_deterministic`: the attack run's three assertions.
- `item_before_open`: an item raised before the opening `decision` is not counted; mutant: counted.
- `p0_not_reestimated`: the bet uses 0.41 from this file; mutant: the window's own rate.

## Refusal list
No new entry type; no kernel or kernel2 change; no LLM call in the clerk; no state kept between
clerk runs; no writ class beyond W1–W4; no invitation or election logic (C2); no change to A4's bet;
no reminder set by counsel's session once the clerk is on `main` (a reminder is a hand clerk, and
two were late). Counsel writes no code: this brief, AMEND-A5, the RUNBOOK section and the report are
counsel's; `tools/clerk.py` and `tests/` the builder's; the pins the reviewer's.

## Stop and report if
the cap would need to rise again; a writ class not listed here is needed to discharge an obligation;
the two checkers disagree; a repair by the sovereign is needed to discharge an item (that is a
failed item, recorded, not a reason to redefine items).

## Deliverables
`tools/clerk.py`; `tests/test_clerk.py`; the pins; the RUNBOOK section `jack clerk`; the cap change
by push; the promotion forecast; the enforcement map printed by `status.py`; the C1b report in
REPORT.md's form; the C2 brief text, written at C1b's exit from the C1b report.

## Counsel's forecasts on this window (entered before it opens; resolves_by = the window's end)
| id | claim | p |
|---|---|---|
| L1 | the attack run is clean on the first `tests` run after `clerk.py` merges | 0.6 |
| L2 | liveness E ≥ 20 within 7 days of the opening decision | 0.55 |
| L3 | at least one W1 or W2 item is discharged only after a repair by the sovereign (Y = 0) | 0.5 |
| L4 | the cold read of this brief returns ACCEPT or ACCEPT WITH OBLIGATIONS on the first round | 0.45 |
