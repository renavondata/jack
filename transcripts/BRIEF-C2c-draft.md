# BRIEF-C2c (draft, counsel) — Appendix M, the model (5 November 2026)

This file is `transcripts/BRIEF-C2c-draft.md`. The model is written first and in small steps, one rule at a time; the rest of the brief follows. Each rule is marked **New in C2c**, binds C2c only, and has a pin.

C2c's opening is the entry that C2c's brief's opening rule selects.

## M.1 One stated end (New in C2c)

- C2c's promotion forecast is the first `forecast` by counsel whose `args.id` is the id C2c's brief names, and whose `seq` is below C2c's opening.
- `tools/status.py` reads C2c's stated end only from that forecast's `resolves_by` (A5.2: "a brief states no other date").
- With no such forecast, `status.py` prints `promote C2c: refused: C2c has no promotion forecast before its opening`.

**Pin `c2c_one_end`.**

Twins:
1. All of these lie below the opening:
   - first, a counsel forecast with another id, dated *d3*;
   - then a non-counsel forecast with the id, dated *d0*;
   - then counsel's forecast with the id, dated *d1*, later than opening + 14 d;
   - then a second counsel forecast with the id, dated *d2*.

   The four dates differ, and the stated end is *d1*.
2. The only forecast with the id lies above the opening. `status.py` prints the refusal line.

Mutants:
- the stated end read as opening + 14 d (killed by twin 1);
- read as min(*d1*, opening + 14 d), which is how `status.py` reads C2a's end today (twin 1);
- the second counsel forecast taken (twin 1);
- the non-counsel forecast taken (twin 1);
- the forecast above the opening accepted (twin 2);
- the `args.id` test dropped (twin 1).

M.1 decides nothing about C2a's stated end, which is unruled (`transcripts/CASES.md`).

## M.2 Three values for each criterion (New in C2c)

Each criterion of C2c prints one of three values, decided in this order:
1. `unmet`, when the inputs supplied already show it fails;
2. otherwise `unknown (no <input>)`, when an input it reads is not supplied or cannot be read. `<input>` is that input's name, for example `unknown (no run file)`;
3. otherwise `met` or `unmet`, as the inputs say.

Which runs count as supplied is stated with each criterion.

**Pin `c2c_three_values`.** The pin runs on a criterion of C2c that reads the run file and the tree.

The twins:
1. With every input supplied, the line prints `met` or `unmet`, as the inputs say.
2. With no run file, and a tree that shows no failure, the line prints `unknown (no run file)`.
3. With no run file, and a tree that shows a failure, the line prints `unmet`.

The mutants:
- absent input printed as `unmet` (killed by twin 2);
- absent input printed as `met` (twin 2);
- `unknown` printed where the tree already shows a failure (twin 3).

## M.3 W1 in every window (New in C2c)

From C2c's opening, the clerk lists W1 as BRIEF-C1b defines it under any subject whose prefix holds C1b's opening. That means a line `W1 forecast <seq>` for every `forecast` entered after C1b's opening that has no `resolution`, escalated once it is past its `resolves_by`. W1 is printed by `tools/clerk.py` and `tools/status.py` and by nothing else. Today both list W1 only when the subject is C1b (`tools/clerk.py:81`, and `tools/status.py:625` on `builder-c2b-status`). This is the audit's D3, reproduced in `transcripts/REVIEW-audit-3-6-argon.md`.

**Pin `c2c_w1_every_window`.** Each twin runs both tools, under a subject other than C1b, on a prefix that holds C1b's opening.

The twins:
1. A forecast entered after C1b's opening, unresolved and past its `resolves_by`. A `W1 forecast <seq>` line prints, ESCALATED.
2. The same forecast before its `resolves_by`. The `W1 forecast <seq>` line prints, not escalated.
3. A forecast entered after C1b's opening that has a `resolution`. No W1 line prints for it.
4. A forecast entered after C1b's opening and before the assessed window's opening, unresolved. It is listed.

The mutants:
- W1 listed only under C1b, in either tool, which is the present line (killed by twin 1);
- W1 listed only once overdue (twin 2);
- every W1 escalated (twin 2);
- resolved forecasts listed (twin 3);
- forecasts counted from the assessed window's opening (twin 4).

The reviewer's pin `w1_c2a_omitted`, on `review-audit-3-6` at decf8e8, witnesses the first mutant in `tools/clerk.py`.

## C2c's first amendments (the sovereign's direction of 5 November)

This part is not the first section of the brief that COUNSEL-DUE `c2c-brief` names (procedure contracts, kernel types if witnessed, GitHub identities).

The sovereign, 2026-11-05T20:28:54Z: "Stop. C2a ends on the 17th. The A6 clause with the reads' findings as its spec, and principle 7's ranking, go to C2c as its first amendments. Record this chain's cost in reads and hours in the C2a report." (`transcripts/COUNSEL-OPEN.md` row 39.)

The two amendments are these:
1. **A6's clause.** Its spec is the reads' findings, which are Appendices C–E of `transcripts/A6-CASE-20261105.md`. That file also holds:
   - the clause he adopted at 16:33:56Z, before he stopped the chain (§The clause he adopted);
   - counsel's second (last) draft of the clause (Appendix B).
2. **Principle 7's ranking.** It comes from the text he forwarded at 16:57:06Z, beginning "Other agent speaks for me": "(7) The charter's maxims should govern its procedural clauses, and today they do not, because every amendment overrides earlier text; this ranking is to be added at C2c."

A5.1 ends a window only at its stated end or at a `promote`, and A6's clause adds another way for it to end. Principle 7's ranking orders the charter's own clauses. Both therefore come after the amendment procedure:
- `transcripts/COUNSEL-OPEN.md` row 33 records his decision of 4 November that "the charter is amended again only through a process judged as jack judges everything else". It sets that procedure "before any A6".
- `transcripts/RULING-20261104-window-fix.md` calls the procedure "C2c item 12". That names an item of a draft that is not yet on `main`.

That procedure is to be stated in a later part, not yet written.

## The first section (COUNSEL-DUE `c2c-brief`), one item: the kernel types (a record, no rule)

The `c2c-brief` row's `what` lists three items. BRIEF-C2b's Amendment 9 struck the procedure contracts, which leaves two. This part is one of them. The other, the GitHub identities, is not yet written, so this part alone does not discharge the row.

BRIEF-C2b's paragraph beginning "C2's third word" says, at its lines 31–33, that the kernel types C2a's text promised (`invite`, `accept` and `wish`) are "deferred to the first witness that a forecast cannot carry an invitation". Its §Deliverables puts the kernel types in this brief's first section, "if a witness has appeared".

As of seq 1889 (2026-11-06T08:04:35Z), no witness has appeared:
- Invitations are `election.invite` forecasts, which the clerk enters in C2b's window. C2b has not opened.
- The log on `main` holds no `election.invite` forecast.

So, as of that seq, this part adds none of `invite`, `accept` or `wish`.
- **When a witness can appear.** No earlier than when invitations are first issued, in C2b's window.
- **The row's due.** The `c2c-brief` row is due 2026-11-16T00:00:00Z. Amendment 2 puts C2b's opening after 2026-11-17T12:00:00Z. So at the row's due, this item can only be recorded as it stands then.
- **The C2b report.** That paragraph says the deferral is also to be recorded "in the C2b report".
- **Where the kernel items go.** This is one of the open questions of `transcripts/COUNSEL-OPEN.md` row 37, and this part does not decide it.
