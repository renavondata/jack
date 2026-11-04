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


## Corrections (appended by counsel, 4 November 2026; the judgment above is not rewritten)

Counsel's index was read cold, and the builder's session on the window code (opencode-runner #238) stopped on
condition 2. Both found defects in counsel's drafting of this judgment. Guy's direction the same day: "You
shouldn't need my decisions for how to write and implement the law, unless there really is no precedent."
Correction 1 corrects a fact. Corrections 2–4 are counsel's under that direction, each with the precedent it
rests on and counsel's probability that it stands on the review Order 2 names — the two reads of
BRIEF-C2a-prime. None changes what
was ruled: at a failed window's boundary, A2.6 governs over BRIEF-C1b, and the fix is a decision. Order 4 applies to these corrections as to the judgment: counsel's V5 and V7 ride on criterion 6, which correction 3 computes, and V6 on criterion 7, which correction 2 reads; none is entered before these corrections are on `main` and read. Counsel also has a wealth interest in the earlier reading of C2a's stated end (`transcripts/CASES.md`): V0, V2 and V3 resolve by 2026-11-17T12:00:00Z, the same instant their claims fall due, so under the later reading they expire unresolved and each scores an item 0 in the liveness process.

1. **The index.** §Its standing as precedent says the ruling "is listed in `LAW.md` under 'Case law'". No such
   section was committed: counsel's proposal script staged `transcripts/` only, while the pull request's title
   (#290) and its `proposal` entry (seq 1262) said "LAW.md gains a Case law section". That claim was false when
   made. The index is `transcripts/CASES.md`. Counsel's proposal tool now refuses when a file the title names
   is not among the commit's paths, or the commit's paths differ from those its spec declares (COUNSEL-OPEN
   row 34).
2. **Condition 2, made computable.** The builder found that `item_process` receives only log entries, while
   C2a's failure is evidenced by the acts table, and warned that "ended without promotion" alone would weaken
   condition 2. Cold reads then showed that three computable stand-ins collapse into that weaker test:
   recomputing every criterion "as of the stated end" (criteria 1 and 2 read unmet whenever no tests run finished
   on the exact commit assessed, which after the stated end is always); the window's promotion forecast (V0's
   claim, seq 361, ends "C2a promoted, not failed", so its resolution cannot separate failure from
   non-promotion); and `status.py`'s criteria 3 to 6 and its A3.4 line, which read unmet for want of evidence
   with no `unverified` or `unknown` beside the figure (criterion 5 prints `value E 1.000000 >= 20` with no runs
   file and falls below 20 with a truncated one; criteria 3 and 6 print `False` on a clone without the history
   from the opening's commit; criterion 6 moves with `--as-of` on a fixed prefix; the A3.4 line adds a `promote`
   a failed window never has). Condition 2 is therefore **tested by a sufficient condition on criterion 7
   alone**: (a) no `decision promote` naming the window has `ts` at or before its stated end; and (b) a
   `decision veto` naming the window has `ts` at or before its stated end, or the window's acts evidence — the
   attributed file (BRIEF-C1b Amendment 2), committed under `transcripts/evidence/` no later than the commit that
   carries the `fix`, and named in the `fix`'s `subject` — holds a row with `repo` `renavondata/jack` and
   `class` `repair` whose `time_hkt` minute, read as UTC+8, begins at or after the window's opening `ts` and ends
   at or before its stated end. Both are decided by the log and that file. Where a stated end is read two ways
   and unruled, (a) is read at the later instant and (b) at the earlier. Where the test is not met — a window
   failing only on criteria 1 to 6 or on A3.4, or one with every criterion met and no promotion — no `fix` names
   the window until the sovereign has answered whether it failed; a `fix` entered regardless is a repair; his
   answer is recorded as a ruling and reaches `status.py` only through an order it carries. For C2a the acts
   evidence is `acts-20261103T2144.csv` (attributed), with `acts-20261103T2144-raw.csv` and
   `runs-tests-20261103T2144.json`, committed with these corrections; it holds nine `repair` rows, the earliest
   at 2026-11-02 22:11 HKT (witness: on the prefix to seq 1273, `status.py --subject C2a --as-of
   2026-11-04T09:32:30Z --acts acts-20261103T2144.csv --runs runs-tests-20261103T2144.json` prints criteria 3–6
   met and "criterion 7: off-log repairs: 9 SHORT"; criteria 1 and 2 read SHORT for want of a run on that
   commit; from `--as-of 2026-11-04T15:00:01Z` the same prefix reads criterion 6 SHORT, writs due at 15:00:00Z
   being projected as expiries). Because condition 3 requires the `fix` after the stated end, and C2a's stated
   end is read two ways and unruled (`transcripts/CASES.md`), **C2a's `fix` is entered only after
   2026-11-17T12:00:00Z**, the later of the two. p(stands) = 0.75.
3. **Order 1's timing.** Order 1 says the rule is implemented "before C2a′'s opening push". That cannot be
   carried out: `main` stands at 7,784 of 7,800 counted lines, and only the opening push may raise the cap. The
   rule's text is fixed before the window opens; only the code that computes it lands inside it, as the first
   proposal after C2a-prime's opening. `status.py` is a function of the prefix, so after that merge every run
   types the fix by the rule; until then no promotion, writ disposition or report relies on its typing of that
   `fix`. This holds only if BRIEF-C2a-prime, before its opening, exempts its window code's `item_process`
   change from its own "nothing in … `item_process` … changes" and "no change to any criterion's
   statistic or threshold", and from BRIEF-C2a's "no change to C1's statistics"; otherwise the question goes to the sovereign. The builder codes corrections 2 and 3 only once
   Guy has read them (A2.10: "Code is written to a text Guy has read"). p(stands) = 0.8.
4. **Its standing.** §Its standing as precedent says the ruling "needs no amendment" and "binds every later
   reading — … the sovereign's own — until a later ruling overrules it by name and with reasons". A2.10 says questions of what the charter allows "are
   put to Guy as rulings and recorded here" — in the charter, which changes only by `decision transmute` and
   `amend` (A2.7; SPEC §10.2, §10.13). So this ruling is to be recorded by an amendment, and both "needs no
   amendment" and "binds every later reading … until a later ruling overrules it by name and with reasons" are
   withdrawn.
   Until then this judgment is the record of Guy's answer, and his direction ("so it becomes case law") is that
   it be followed. No text ranks a ruling or says how one is displaced. It decides no question of validity
   (§3), and reaches code only through its orders. p(stands) = 0.8.
5. **The sources of C2a's earlier reading** (appended 4 November, after cold reads of BRIEF-C2a-prime).
   - **What correction 2 relied on.** Correction 2 relied on `transcripts/CASES.md`, which traced the fourteen days to BRIEF-C2a Amendment 1 (seq 368) and to the budget (seq 50).
   - **Where the fourteen days actually are.** They are in BRIEF-C2a v2 itself, before the opening: proposed at seq 355, merged at seq 356, and read by `transcripts/REVIEW-C2a-v2.md` (merged at seq 360).
   - **The texts that point the other way.**
     - The same brief says "V0's `resolves_by` is the window's end", and V0's claim says the same (seq 361).
     - A5.2 ends "a brief states no other date".
     - `transcripts/REVIEW-C1b-A5.md` F8 applied that clause to a brief's fourteen-day maximum, and counsel accepted the finding (`transcripts/REPLY-REVIEW-C1b-A5.md`).
   - **Whether the question needs deciding.** Whether A2.4 survives that clause is a question of what the charter allows (A2.10), and counsel holds an interest in the answer. Counsel does not decide it. No act BRIEF-C2a-prime or BRIEF-C2b prescribes needs it decided; if V2's outcome differs on the two exit prefixes, its resolution goes to the sovereign.
   - **What follows.** Correction 2's rule governs C2a, and its last sentence stands. C2a's `fix`, and every opening after it, come after 2026-11-17T12:00:00Z, which is after both instants.
6. **Order 1's timing, again** (appended 4 November, after the formal read `transcripts/REVIEW-C2a-prime-astra.md`, finding F1, of BRIEF-C2a-prime v6).
   - **What correction 3 got wrong.** Correction 3 landed the rule's code as a proposal after the opening. Between the `fix` and that merge, writs would be finalised under the code then in force, and the merge would recompute them. That runs against BRIEF-C1b §Liveness: "An item once finalised is never regrouped: no later entry, evidence string or merge changes an earlier item or any bet already placed (A4.3)."
   - **Where the code lands now.** The code lands with the opening push, which carries it, since `jack push` fast-forwards `main` to its branch.
   - **When the rule takes effect.** At that push. A writ finalised between the `fix` and the push keeps the taint the code of its time gave it, and the `fix` frees only writs finalised after the push.
   - **Why the interval remains.** The `fix` must still precede the push (condition 3), and C2a's cap leaves no room for the code before it. So the interval cannot be removed. It can only be made non-retroactive, and, by timing the paste, normally empty.
   - **What stands.** Correction 3 stands otherwise.
   - **Basis and probability.** Counsel's decision under the direction quoted above. Precedent: BRIEF-C1b §Liveness and A4.3. p(stands) = 0.8.
