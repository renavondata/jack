# Ruling of 4 November 2026: the fix of a failed window is a decision, not a repair

Put to Guy by counsel (`counsel-2`) in conversation on 4 November 2026, after a cold read of counsel's
draft of BRIEF-C2a′ (finding F1) showed that the entry the charter requires at a failed window would, as
`tools/status.py` is written, be scored as a repair and refuse liveness for every later window. A
question of what the charter allows, put to Guy as a ruling (A2.10).

## The question

When a window fails, A2.6 requires its fix to be a `decision` entry. C1b's liveness process, and the code
that implements it, type every sovereign `decision` of kind `fix` as a repair. Which governs the entry that
closes a failed window: is it one of the sovereign's decisions, or one of his repairs?

## The facts on the record

- **A2.6** (18 October 2026, in force): "Veto, promotion, budget, grant, transmutation **and the fix of a
  failed window** are `decision` entries signed by a key declared in genesis."
- **§7**: "Decisions: a wish; a signature on genesis, a change entry or a capability grant …; a veto or
  promotion at a layer boundary; the budget. Repairs: every other act. … A repair means a layer has found
  a defect, and the repair is recorded as a precedent case."
- **§6**: "A layer that fails its window is not patched in place: the failure is a precedent, the fix is a
  change entry, and the window starts again."
- **BRIEF-C1b §Liveness**: a repair is "every entry signed by the sovereign's key except `genesis`, `key`,
  `amend`, `push`, a `proposal` (a wish) and a `decision` of a kind other than `fix` — so a `decision fix` …"
  is a repair; "every sovereign repair is attributed to every writ open" at its entry; a repair entered
  after an item was finalised is a late report, which refuses `promote` while any exists.
  RUNBOOK: "repairs are entered as `jack decision fix "<what>"` when made."
- **`tools/status.py`** lines 92–96 implement C1b's reading for every `fix`; `assess_value` (line 271)
  refuses criterion 6 while any late report exists anywhere in the process from C1b's opening.
- **The log**: seven `decision` entries (four `transmute`, one `budget`, two `promote`); no `fix` has ever
  been entered. The two readings have never met a case.
- **The case**: C2a's first window reaches its stated end on 2026-11-15T15:04:14Z with criterion 7 unmet
  (nine off-log repair rows; seq 1076; COUNSEL-OPEN row 33). It is the first failed window in jack's history.

## Options as put

| | Reading | Consequence |
|---|---|---|
| R1 | A2.6 governs at a boundary: a `fix` naming a window that has failed is a decision; any other `fix` stays C1b's repair | decidable from the log; a few lines and a pin in `status.py`; no kernel change |
| R2 | a distinct `decision` kind for the boundary act | typing by kind alone, as §7 prefers; a SPEC and kernel change, so a trusted-base push with its own reads |
| R3 | the code is right: every `fix` is a repair | the entry A2.6 requires refuses liveness for every later window; not viable without amending the charter |
| R4 | the fix recorded off the log | contradicts §7 ("every act of Guy's is an entry") and A2.6 |

## The ruling

**R1, now; R2 as a C2c item.** Guy, 4 November 2026: "Good … Let's write our decision clearly including the
reasoning so it becomes case law."

**The rule.** A sovereign `decision` of kind `fix` is a **decision**, not a repair, when and only when:
1. its `subject` begins with the name of a window as `status.py` names it (`C1a`, `C1b`, `C2a`, and every
   later window a brief pre-states), followed by `:`;
2. that window reached its stated end with a pre-stated criterion unmet and with no `decision promote`
   closing it (A5.1: it "has failed");
3. the entry's `ts` is after that stated end and its `seq` precedes the opening `push` of the window that
   follows; and
4. it is the first `fix` naming that window.

Every other sovereign `decision fix` is what BRIEF-C1b says it is: a repair, attributed to every writ open
at its entry, and a late report if any item has been finalised.

## Reasoning

1. **What the dichotomy is for.** It prices the sovereign. §7 splits his acts into those the design reserves
   to him by role — wishes, money, keys, the law, layer boundaries — and those in which the loop needed his
   hands. Liveness asks, item by item, whether the court completed a writ without them (§6). The split is
   binary because the liveness item is binary, and it is typed by entry and key, fixed in advance, because
   judging each act on its merits is a semantic question no decidable check can be trusted with (Rice 1953;
   §12). Nothing here departs from that.
2. **The text was pre-stated.** A2.6 named the fix of a failed window as a decision on 18 October 2026,
   before any window opened. C1b's brief, read later, reused the kind `fix` for a different act — the
   record of a mid-window repair — and the code implemented only that reuse, with no pin for A2.6's case.
   R1 implements a rule stated before any score existed. It is not a re-typing after the fact (§12's
   guard), and it is not a rule chosen after seeing which way a score went.
3. **One kind, two meanings.** C1b's `fix` says: my hand did the loop's work while writs were open. A2.6's
   says: I am closing a failed window and naming its precedent — judgement at a layer boundary, the
   sovereign's second role. §7 itself relates them: "a repair means a layer has found a defect, and the
   repair is recorded as a precedent case." The fix of a failed window is that recording.
4. **No double pricing.** The defect that failed the window is already priced: the window failed. To charge
   the entry that records it as a further repair — tainting every open writ and refusing criterion 6 for
   every later window — prices one event twice, and makes the act the charter requires a sentence on every
   layer that follows.
5. **The absurdity test.** C1b's taint is deliberately severe for mid-window repairs: no scope narrows it,
   and a late report refuses promotion. It is right for those. Applied to a boundary act it produces a
   result no reader of A2.6 could intend: the required entry would make every later window unpromotable.
   When a rule is absurd on one class of input and sound on the rest, the input is in the wrong class.
6. **Narrowness closes the re-typing route.** The four conditions are each decidable from the log; they
   admit at most one decision per failed window, only in the interval between the failure and the next
   opening, only for a window that actually failed. Any other `fix` — including any the sovereign might
   wish to re-type — stays a repair.
7. **R1 rather than R2 now.** R2 is the cleaner form: typing by kind alone. It needs a new kind in SPEC §5,
   which the kernel checks, so a trusted-base push and its own reads; it cannot land before C2a′ opens
   without changing the trusted base inside a window. R1 gives the same classification now, in code the
   reads can check, and R2 replaces it at C2c.

## What this ruling does not decide

- **A distinct kind (R2)** — a C2c item.
- **Rulings as entries.** This ruling is itself an act of the sovereign's of a third sort: adjudication of
  what the law allows. Today it is a transcript, not an entry. It should be an entry, counted as a decision
  for liveness and as procedure for §12's ratio; that needs a kind the SPEC does not have — a C2c item.
- **A judge below the sovereign.** Whether rulings should first be given by a scored party (a reader
  elected by record, forecasting the sovereign's answer, with the sovereign affirming or reversing) — a C2c
  item, deferred until rulings are frequent enough to score (three in seventeen days so far).
- **The court's reach.** The acts table sees only `renavondata/jack`. On 4 November the sovereign merged
  three pull requests in `renavondata/opencode-runner`, created a GitHub App and labelled a runner: the App
  is a capability grant (a decision); the merges and the label are his hand doing the court's machinery
  work — repairs by §7's letter, outside the instrument. Guy's direction: the runner comes under the court
  (C2c), and the C2a report lists those acts as off-log repairs outside jack.

## Orders

1. The builder implements the rule in `tools/status.py`'s `item_process` before C2a′'s opening push, with
   tests; the reviewer registers pin `window_fix_is_decision` (mutant: a fix meeting all four conditions
   typed as a repair) and its twin (a `fix` with a free-text subject, or naming a window that did not fail,
   or entered after the next opening, still taints every open writ and is a late report).
2. The rule and this ruling go to the two cold reads of BRIEF-C2a′, with the question: does R1 admit a
   re-typing route of the kind §12 warns against?
3. The sovereign's opening paste for C2a′ carries, before the opening push:
   `jack decision fix "C2a: criterion 7 unmet at the stated end — nine off-log repair rows (acts-20261103T2144); the court's platform acts moved to a GitHub App (opencode-runner #227)"`.
4. Counsel enters its forecasts on C2a′ (V5–V7) only after this ruling is on `main`, so that no forecast of
   counsel's can be read as the reason for it.

## Its standing as precedent

This ruling interprets the charter; it does not change it. A2.6 and BRIEF-C1b are both in force, and the
ruling decides which governs one class of entry. It therefore needs no amendment, and it binds every later
reading — counsel's, builders', reviewers', and the sovereign's own — until a later ruling overrules it by
name and with reasons. A ruling that would add to the charter or contradict its text is not a ruling but an
amendment, and goes by the amendment path. Earlier rulings (18 and 25 October) changed the text and were
recorded by amendments A2 and A3; this one joins the charter's text, as a reading, with the next amendment
that passes the procedure of C2c item 12, and until then is listed in `LAW.md` under "Case law".

## Disclosure

The recommendation was counsel's. Counsel has an interest: its request on 3 November caused one of the nine
rows; its draft of BRIEF-C2a′ omitted the `fix` entry, which would have protected its own forecasts on
criterion 6 (cold read F1 called it a rescue by omission); and its forecasts V5–V7 on C2a′ will ride on
criterion 6. Counsel argued against itself in conversation (the §12 re-typing worry) before Guy ruled.
