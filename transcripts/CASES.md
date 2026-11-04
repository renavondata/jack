# CASES — an index of the sovereign's rulings, and where the law is

Counsel's index, at `transcripts/CASES.md`. It binds nothing. Rulings since 25 October have a judgment at
`transcripts/RULING-<date>-<slug>.md`, with any corrections appended; the two earlier ones are recorded only in
the charter's text (below). Where this index and a judgment
differ, the judgment governs, and where a judgment and the charter differ, the charter's text stands, since it
changes only by amendment (A2.7). A ruling is the
sovereign's answer to a question of what the charter allows, to be recorded in the charter (A2.10: "questions
of what the charter allows are put to Guy as rulings and recorded here"); until it is, it is listed here.
Rulings are not entries on the log (BRIEF-C2c's draft item 13, on no branch yet, proposes that they become entries); a judgment on
`main` carries counsel's key on its proposal.

## Where the law is, and which governs

- **The record.** The law in force at entry *i* is what entries 0..*i*−1 establish (CHARTER §4; SPEC §7): keys
  and powers, the charter in force, the trusted base in force, the transmuted set. The sovereign's `decision`
  entries are his acts on it (A2.6).
- **The charter**, `CHARTER.md`: the genesis text through A1 (seq 0 hashes it), then A2–A5 (amend seqs 4, 30,
  67, 137); trunk's `CHARTER.md` must hash to the latest `amend`'s `charter` (SPEC §7, §10.2). A1–A3 each
  override "earlier text where they conflict"; A4 overrides §6, and A5 "§6, A3.2 and any brief", where they
  conflict. It changes only by `decision transmute`, then `amend`, with text and entry in one push (A2.7; SPEC
  §10.2, §10.13).
- **Validity: SPEC and the trusted base.** "The checker is the only adjudicator of validity" (§3; A1.1).
  SPEC §§1–9 is the text both checkers implement; a kernel that departs from it is a finding, not a licence.
  SPEC §10 is marked informative; A2.3 lets a brief pre-state the judge's grounds, and records SPEC §10.7–10,
  "adopted on 16 October", as the first. The trusted base changes only by the
  sovereign's `push` naming its digest (A2.6; SPEC §10.1, §10.11), never between an `amend` and its height
  (A2.7). 
- **Windows: the briefs.** A brief pre-states criteria, bounds and review rules, binds its layer only, and "may
  tighten the charter's bounds, never loosen them" (A2.4). Which entries count toward a window is "the brief's
  business (BRIEF-C1.md), not the checker's" (SPEC §7). C1a's brief is `BRIEF-C1.md`; later briefs are
  `transcripts/BRIEF-<window>-draft.md` with their appended amendments. No text says when a brief begins to
  bind (BRIEF-C2b Amendment 1 reads a brief as counsel's draft until the push that opens its window); the charter
  requires a window, α, p₀ and the attack list to be committed before the window opens (§6; A4.2 for p₀), and its
  stated end is the `resolves_by` of the brief's promotion forecast (A5.2), which may not be moved (A5.1) — C2a's
  is read two ways: 2026-11-15T15:04:14Z by BRIEF-C2a Amendment 1 (seq 368, entered after the opening, unread)
  and `status.py`, as min(V0's `resolves_by`, opening + 14 d), the fourteen days from the budget (seq 50); and
  2026-11-17T12:00:00Z by A5.2's letter and V0's own claim (seq 361: "this forecast's resolves_by, which is the
  window's end"). That question is unruled; counsel takes no act that depends on it before the later instant,
  and recommends no act of another's that depends on it — V0's resolution, the boundary `fix`, the next opening
  push — before that instant; other brief text has been
  amended inside windows (BRIEF-C1b Amendments 1–2; BRIEF-C2a Amendments 1–3).
- **SPEC and a brief are ranked by no text.** They govern different questions (validity; what counts toward a
  window). A conflict between them, or between any two texts the charter does not reconcile, goes to the
  sovereign (A2.10); a builder who finds the specification contradictory enters `spec_conflict` and stops
  (A2.9); a checker disagreement halts and writs the sovereign (§3).
- **Rulings.** A2.10: questions of what the charter allows "are put to Guy as rulings and recorded here". No
  text ranks a ruling before it is recorded. A ruling decides no question of validity and reaches code only
  through its orders, carried out by a proposal or the sovereign's push.
- **Procedure.** `RUNBOOK.md` states what each verb must do, must refuse and may never do; the session prompts
  under `transcripts/sessions/` instruct sessions. Neither is law.

**Not law**, and cited only as such: `LAW.md` (the map CHARTER §9.7 asks for, of the charter's sentences to the
code that enforces them, with counsel's commentary marked); `REVIEW-*.md` (a finding binds as a pin, A2.9; a
read gates a brief where the brief or `jack push --opens` requires it); `REPORT.md` (each window's verdict, and
the precedent cases of its repairs in the charter's sense — §3, §6, §7, A2.1: the witnessed cases from which
primary rules are to enter; none has entered); `COUNSEL-OPEN.md` (counsel's undertakings, whose "Rule" lines
bind counsel alone, and records of the sovereign's directions); wishes (§7: preferences, never scored).

## How a case enters (counsel's practice; no text prescribes it)

The question, the facts on the record, the options, and counsel's recommendation and interest go to the
sovereign; his answer is quoted verbatim, and the judgment records only what he answered. Questions of how to
write and implement the law are counsel's where the law or a ruling already decides them (Guy, 4 November 2026:
"You shouldn't need my decisions for how to write and implement the law, unless there really is no
precedent"); counsel decides them, records the precedent relied on and its probability that the decision stands
on review, and appends the record to the judgment it implements. A builder writes code to a judgment only once
the sovereign has read the text it implements (A2.10). The holding is stated as a predicate decidable from the
log and the tree, with the code and the pin that enforce it, or says that it has none. No judgment, index or brief of
counsel's goes to a pull request before a cold read by a party counsel does not instruct beyond the questions has
passed it, nor before every question it records has its answer (COUNSEL-OPEN row 34). Corrections are appended, never rewritten. Counsel marks a holding displaced when a later
ruling names it, an amendment changes the text it reads, or the change it anticipates lands, and keeps its entry
here; no text says what displaces a ruling.

## Cases in force

### [2026-11-04] window-fix — the fix of a failed window is a decision, not a repair
Judgment: `transcripts/RULING-20261104-window-fix.md` (PR #290), with the corrections appended to it.
- **Question.** A2.6 makes "the fix of a failed window" a `decision`; BRIEF-C1b §Liveness and `tools/status.py`
  type every sovereign `decision fix` as a repair. Which governs the entry that closes a failed window?
- **Answer.** Guy, 4 November 2026: "Good … Let's write our decision clearly including the reasoning so it
  becomes case law" — to counsel's recommendation R1.
- **Holding, as corrected.** A sovereign `decision` of kind `fix` is a decision, not a repair, when and only
  when (1) its `subject` begins with a window's name and `:`; (2) that window reached its stated end with a pre-stated
  criterion unmet and with no `decision promote` closing it — tested, as correction 2 prescribes, by a sufficient condition on criterion 7 alone: no `decision promote`
  naming the window at or before its stated end, and either a `decision veto` naming it at or before that end or
  a `repair` row inside the window in its attributed acts evidence, committed and named in the `fix`'s `subject`
  (for an unruled end, the promotion is read at the later instant and the rest at the earlier); (3) the entry's `ts` is after that end and its `seq` precedes the next window's
  opening `push`; (4) it is the first `fix` naming that window. Every other `fix` is BRIEF-C1b's repair. Where that test is not met, no `fix` names the window until the sovereign has answered whether
  it failed, and a `fix` entered regardless is a repair (correction 2).
- **Reads.** A2.6 against BRIEF-C1b §Liveness; §7 ("the repair is recorded as a precedent case"); A5.1.
  Conditions (1), (3) and (4) are not in A2.6's words. Order 2 puts to the reads of BRIEF-C2a-prime (a draft
  on `main` since #292, seq 1265, unread) whether R1 admits a re-typing route of the kind §12 warns against.
- **Enforced by.** `tools/status.py` `item_process` and pin `window_fix_is_decision` — **not built**. Lands as
  the first proposal after C2a-prime's opening if that brief exempts it from its refusals, else the question goes
  to the sovereign (correction 3). Until it lands `status.py` types every `fix` as a repair, and no promotion,
  writ disposition or report relies on that typing of the boundary `fix`.
- **Not decided.** A distinct kind for the boundary act; rulings as entries; a judge below the sovereign; the
  court's reach outside `renavondata/jack` (BRIEF-C2c's draft items 13 and 14, on no branch yet).

## Rulings recorded in the charter's text

Answers of the sovereign that changed the charter, and where each is recorded.
- **[2026-10-14] c0-record** — Guy's decision on counsel's review of PR #1: C0 is the record, with no language
  for primary rules. Part of the genesis text (seq 0 hashes `CHARTER.md` through A1); SPEC §12 item 1; REPORT.md §1 ("Scope change: C0 is the record only").
- **[2026-10-18] c1-opening** — Guy's rulings on the cold reads of C1's brief and counsel's research of that
  day. Recorded as A2 (transmute seq 3, amend seq 4). A2's citation `REVIEW-brief-2.md` is on no branch.
- **[2026-10-25] ledger-first** — `transcripts/RULING-20261025-ledger-first.md`: C1 opens ledger-first, in two
  windows. Recorded as A3 (seqs 28, 30; `transcripts/AMEND-A3.md`); SPEC §12 item 11.

A4 and A5 are counsel's texts, not rulings (seqs 66–67, 136–137; `transcripts/AMEND-A4.md`, `AMEND-A5.md`).

## Directions of the sovereign recorded elsewhere, not indexed as cases

SPEC §10.7–10 as the judge's grounds, adopted on 16 October 2026 (recorded in A2.3);
the budget, `decision` seq 50; COUNSEL-OPEN row 33 (no amendment now; C2a fails at its stated end; C2a-prime
pre-stated; the identity fix first; amendments judged as jack judges everything else) and row 34 (the direction
of 4 November 2026 quoted under "How a case enters").
