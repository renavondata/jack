<!-- Counsel-5's second draft of 18 November 2026: Part A of the delta to BRIEF-C2c-1 draft v20 (`counsel/c2c-1-host-truth`), the amendments to criteria 10 and 12 that the audit of 17 November calls for. It replaces Amendments 1 and 2 of the first draft (`transcripts/DRAFT-c2c-1-delta.md` at `ecd3f335`), which a cold read failed (runner #1012). Part B, the amendment on the verbs that end on `main`, is `transcripts/DRAFT-c2c-1-delta-B.md`. Written as amendments appended to the brief, so that the sovereign's read is of the additions alone; the window file's criteria 10 and 12 and its `numbers` change with them, and the file is final only at its proposal. The cap stays 14,500 until he states a number. -->

## Amendment 1 (18 November, counsel-5; criterion 10 asks for one row of the inventory kept inside the window — before the opening, one clause)

**Why.** The audit (`transcripts/AUDIT-criteria-20261117.md`, C2c-1 row 10) classes criterion 10 as "**empty** as an in-window delivery test when no undertaking falls due before exit": counsel can match every open row with a forecast due after the exit, keep none, and the criterion reads `met`. The first draft of this amendment required one undertaking due inside the window and kept. Its reader then named the weakest system that still passed: one undertaking that costs nothing to keep, resolved 1 by another party, due inside the window, with the forecast, what it promised and its resolution all entered before the opening (runner #1012).

**The clause.** Criterion 10 is also `unmet` unless at least `undertakings_due_min` undertakings each meet all five of these:
1. it is counsel's forecast of type `counsel.undertaking` with `args.window` `C2c-1`;
2. its `args.id` is the `id` of a row that is open in the inventory at the opening tree and due after the opening push's `ts` — one of the rows that R5 has counsel re-enter before the push;
3. its own entry precedes the opening push;
4. its `resolves_by` lies inside the window, at or before the assessed instant;
5. it is resolved 1 by an entry that lies inside the window: after the opening push, and at or before its `resolves_by`.

The window file's `numbers` gains `undertakings_due_min: 1`, and criterion 10's `args` gains `"due_min": "undertakings_due_min"`. Nothing else of R5 or of the criterion changes. The clause can only turn `met` into `unmet`: it tightens (A2.4).

**What it shows.** At the assessed prefix no undertaking of counsel's that is past due is unkept (R5, unchanged), and at least one obligation that stood open in counsel's inventory when the window opened has fallen due inside the window and been resolved 1, in time, by a party other than counsel, in an entry made inside the window.

**What it does not show.** That the obligation was worth owing, or that what was done for it is of use. The inventory is counsel's file, and a row says what counsel wrote. Of the system the reader named, this draft closes two parts: the resolution must be entered inside the window, and the undertaking must be a row of the inventory at the opening tree. It leaves the third: counsel can write into the inventory, before the opening, a row that costs nothing to keep, and that row then meets the clause. No test on the log tells a weighty row from an empty one. The check on that is outside this criterion: by R5 "the sovereign's check is one `git show` of the file at the opening tree".

**What follows from it.** The window cannot be promoted before one row of the inventory has fallen due inside it and been kept, so at the opening counsel's inventory holds at least one row due inside the seven days. The brief still states no minimum length: the first lawful prefix is the first at which such a row is resolved and every other criterion holds. One failure stays beyond repair, as in R5 before this amendment: an undertaking resolved after its `resolves_by`, whatever the cause, reads `unmet` at every later prefix (twin 5). The minimum itself adds no such latch; another row can meet it.

**Pin `undertakings_are_forecasts`.** The old twins 1, 4, 6 and 12 expect `met`. Each keeps that expectation only on a fixture that also holds one undertaking meeting the five conditions, and each gains a second form without one, expecting `unmet`. Added twins, each on a fixture that is otherwise `met`:
- (14) every undertaking of the window is due after the assessed instant, none resolved → `unmet`;
- (15) one row of the inventory, due inside the window, re-entered before the push and resolved 1 inside the window and in time; the other rows not yet due → `met`;
- (16) as 15, but that undertaking carries `args.window` `C2b` → `unmet`;
- (17) as 15, but its `args.id` is no row of the inventory at the opening tree → `unmet`;
- (18) as 15, but its forecast is entered after the opening push → `unmet`;
- (19) as 15, but its resolution is entered before the opening push → `unmet`;
- (20) as 15, but the row's `due` is at or before the opening push's `ts`, an expired row → `unmet`;
- (21) as 15, but it is resolved 1 after its `resolves_by` → `unmet`.

Mutants, each with the twins that kill it: the minimum dropped (14, and the second forms of 1, 4, 6, 12); another window's undertaking counted (16); the inventory not consulted (17); a forecast entered inside the window counted (18); a resolution from before the opening counted (19); an expired row counted (20); a late resolution counted toward the minimum (21).

## Amendment 2 (18 November, counsel-5; criterion 12 counts as object only what was declared and resolved — before the opening, one clause)

**Why.** The audit (the same file, C2c-1 row 12) classes criterion 12 as "**empty** as a check that substantive object work outweighs procedure; it establishes a label-count ratio": forecasts of any `world.` label, unanswered and with deadlines past the window, count as object, and an undeclared type prints a line and still counts.

**The clause.** For criterion 12 in this window, an entry is object only when it is (i) a `forecast` of a type that `transcripts/world-types.json` declares, entered inside the window, whose `resolution` is on the log at the assessed prefix, or (ii) that `resolution`. A forecast of a declared type that is unresolved at the assessed prefix is counted on neither side. A `forecast` inside the window of a type beginning `world.` that the file does not declare makes the criterion `unmet`, where R8 had it only printed. A type is not declared when it is absent from the file, or when the file holds it without one of the three fields or with a field of the wrong shape (R8 prints `undeclared: <type>`); and no type is declared when the file's bytes do not hash to `world_types.sha256` (R8 prints `undeclared: transcripts/world-types.json`). A3.4's bound and its count of procedure are unchanged, so the clause can only lower the object count or turn `met` into `unmet`: it tightens (A2.4). R8's second printed line, the ratio excluding scheduled types, is unchanged and still not tested.

**What it shows.** That inside the window the forecasts of declared types which were answered, with their answers, are at least a fifth of the procedure entries, counted as A3.4 counts them with the exit `promote` among them; and that no forecast of an undeclared `world.` type was entered inside the window.

**What it does not show.** That a forecast was worth making, or that its claim has anything to do with the type it carries. The clause reads a forecast's `type` and whether it was resolved; it does not read the claim. The reader of the first draft named the system that still passes: content-free claims entered under a declared type, each truthfully resolved by another party (a claim that two and two make five, resolved 0). Each such pair adds two object entries, and enough of them outweigh any count of procedure. Counsel looked for a test on the log that would refuse them and found none that spares honest work: on `main`'s log the 45 forecasts of `world.hkjc` fall on 21 pairs of meeting and race; in 12 of the pairs counsel and the reviewer each forecast, and two of them, which are whole meetings, hold four different claims each (seqs 73 to 90). Counting one forecast for each meeting and race would discard real ones. The price of the padding is one resolution by another party for each forecast, and the entries are on the log for anyone to read. Nor does the clause say that a scheduled stream is not object: that is reserved to the sovereign for C2c-3 (`reserved_to_the_sovereign`, row 37), and the second printed line is what he reads for it.

**Pin `object_declared`.** The old twins 1 and 3 expect a type's forecasts to be counted; each keeps that expectation only where the forecasts are entered inside the window and resolved at the assessed prefix. Twins 2, 5 and 6 keep their printed `undeclared` line, and on a fixture whose undeclared forecast is inside the window each now also reads criterion 12 `unmet`. Added twins:
- (7) ten forecasts of `world.renavon` inside the window, none resolved at the assessed prefix → counted on neither side, and the ratio read without them;
- (8) the same ten, each resolved by another party → counted as object, twenty entries;
- (9) one forecast of `world.padding` inside the window, a type the file does not hold → `unmet`;
- (10) the same forecast entered before the opening push → no effect on this window;
- (11) one forecast inside the window of a type the file holds without `resolver_inputs` → `unmet`;
- (12) one forecast of `world.renavon` inside the window, and the file's bytes do not hash to `world_types.sha256` → `unmet`.

Mutants, each with the twins that kill it: unresolved forecasts counted as object (7); a resolution not counted with its forecast (8); an undeclared type counted or only printed (9); the window's bound dropped (10); the three fields not checked for the criterion (11); the hash not checked for the criterion (12).

## For the sovereign, with these two amendments

1. Counsel's own rule since row 69 is that "counsel drafts no criterion that a system with no skill passes". Each criterion above still has a system that passes it without useful work, written out under "What it does not show". This draft keeps both as criteria of C2c-1, tightened, each claiming only what is written under "What it shows"; the brief's draft v20 has them as criteria, and to stop testing either is to relax a control, which only his word does. The other course is his to choose at his read: either criterion is printed by the status tool and not tested until C2c-3's judged procedure decides it.
2. Row 68 owes him a question it has not yet had an answer to on the record, "his word on lessons 1 and 2": "(1) A criterion needs a strawman as a pin needs a mutant: each criterion names the no-skill systems that must fail it, the court's code runs them, and a brief whose strawman passes is refused at its gate. (2) The drafter does not set his own bar: the reader names the weakest system that passes each criterion." Lesson 2 was followed for this draft. Lesson 1 would be code, under a cap; no draft of counsel's builds it yet.
