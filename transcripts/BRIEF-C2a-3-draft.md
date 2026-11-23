# BRIEF-C2a-3 — the third window of C2a (draft v6, 23 November 2026, counsel, on v5 of 22 November and v4 of 18 November by counsel-5, after the reads of v1, v2 and v3 at runner issues #994, #998 and #1000, each `VERDICT: FAIL`)

This file is `transcripts/BRIEF-C2a-3-draft.md`. Wherever a tool reads a name the window is called `C2a-3`. It is a draft: no read has passed it, nothing in it is proposed, and no builder session is filed on it before the sovereign has read it (A2.10: "Code is written to a text Guy has read").

It is written on `transcripts/BRIEF-C2a-prime-draft.md` as `main` holds it, with its Amendments 1 to 11 ("the second brief" below). Every section that states a fact about this boundary is written out here. The read of v1 found that sections left standing by reference said things true of the second window and false of this one, so only rules are now taken by reference, and each place that does so names the sentences it replaces. The read of v2 found one statement of route B's still false: that the `fix` shows as a late report in the tool's assessment before the push. It does not, and §No item changes now says what the tool assesses there. The read of v3 found the last section still taken by reference, §The acts evidence, false in one sentence once this window's names were read into it; that section is now written out too. v5 changed v4 in five places, each to read C2a-prime's end as AMEND-A6 gives it (`transcripts/AMEND-A6.md`, read by him at seq 7132).

**What v6 changes.** v6 is the draft after the move: his push of seq 7281 put the promotion evaluator under `judge/`. Besides its heading and this note, it changes v5 in these places and no other:
- **§The code** is re-aimed at `judge/status.py`. The window's code is now a change to the promotion evaluator, which SPEC §10 accepts only by the replay test and his push (the ruling of 20 November, answer 3 and the drafter's checks 4 and 7).
- **The vetoed end is read** (§The code, change 6), with A6's pin `vetoed_window_continues` and the one mark it needs. AMEND-A6 orders that of the evaluator's next change, and this is that change.
- **The late-report rule** is pre-stated (§The late-report rule; the ruling's answers 11 and 12).
- **Route B is struck,** with its change 5, §The exemption and its pin. He chose his veto, and his vetoes are at seqs 5879 and 7180.
- **§The cap** is counted again from what `main` holds, and says why his answer 6 of 20 November cannot be applied as it reads.
- **The opening paste waits and does not stop:** for the stated end, for a quiet lane and for a gap between the diary's ticks; and it tries the push again when `main` has moved (§Order of acts step 2). His words of 19 November ask for a paste that waits.
- **His read, the cap and the scope's patch are one paste** (§Order of acts step 1), and his grant states the cap.
- **The pin `third_window_cap`** names two mutants, 8,400 and 7,800, where v5 named 8,400.
- **The new pins are required of C2a-3 alone,** in a tuple of their own, and the pin `replay_drift` is re-aimed, with two sentences of SPEC §10 in counsel's patch (§The code).
- **V8's `resolves_by`** is counted from the stated end when V8 is entered before it (§The window).
- Each sentence that named `tools/status.py`, or the code at `6ab25cd8`, as the evaluator in force now names `judge/status.py` as `main` holds it at `cbdac17b`; and each that spoke of C2a-prime's end as still to come now gives it as it fell.

Where this brief quotes an "answer" of 20 November, it quotes the ruling's record of the option he chose (its section *The answers in short*).

**Why there is a third window.** C2a-prime cannot be promoted. COUNSEL-OPEN row 69: "At `main` `b88d318e` and after, `tools/status.py --subject C2a` prints criterion 3 as 'scope equals SPEC and unchanged: False'; at the opening push's commit `6c0566c3` it printed True." The verb signs a promotion only when `status.py` prints `promote C2a: lawful`, and no later commit can make that line read so (§The precedent). The sovereign's words on 17 November: "I don't want unlawful revisions any more....". So C2a-prime fails. Under AMEND-A6 it ended, as failed, at his `decision veto` of seq 7180 (2026-11-22T11:44:05Z), the first naming it at or above A6's `activate_at`, which is 7180. The push that moved the promotion evaluator under `judge/` followed at seq 7281, and two pushes of his to the tests workflow at seqs 7283 and 7339. Each landed before 2026-11-30T00:00:00Z and opens nothing (the ruling of 20 November, answers 5 and 17; §The window). Its stated end, 2026-11-30T00:00:00Z, is not moved, and the `fix` and this window's opening stay keyed to it (A6, clause 1). A5.1: "A window that reaches its stated end with a criterion unmet has failed (§6, A3.2); the stated end may not be moved." A3.2 requires what follows: "A window that fails is a precedent, fixed by a lawful change and followed by a new pre-stated window; it is never patched in place (§6)." A4.1 permits it: "A window that fails and is followed by a new one continues the same wealth process on the same statistic under the same null; *E* is never set back to 1 and no α is split."

**What this brief changes.** Of the second brief's criteria, it:
- changes criterion 3's number, and states the test of its second sentence;
- changes which late reports refuse criterion 6 (§The late-report rule);
- changes criterion 7's interval and the window its veto clause names;
- adds §Pins to criterion 1.

It adds no criterion and removes none. It also reads C2a-prime's end at his veto, as A6 orders of the evaluator's next change (§The code, change 6), and names the lawful change, the entries that record the failure and the fix, the instant the window opens, the forecast that carries its end, and the change to the promotion evaluator that lets it read this window.

## The precedent, and the lawful change
*Replaces the second brief's section of this name.*

**The precedent.** The second brief's criterion 3 ends: "`judge/scope.json` and SPEC §10's block are unchanged since C2a-prime's opening push." `main`'s own tree has held the opening's `judge/scope.json` and SPEC §10's block at every instant since that push. The code tests more than the sentence. In `tools/status.py` as it then stood (`main` at `6ab25cd8`), `c2a_tree_evidence` compared the two files at the commit assessed and at every commit of `git rev-list <opening's commit>..<commit assessed>`: every commit reachable from the commit assessed and not from the opening's. Row 69: "Stream session 145 was re-proposed on a branch (`ops-stream-145-r`, jack #1071) whose first fourteen commits were made between 12:42:10Z and 12:51:53Z on the tree before the opening (cap 7,800), and which merged at 13:32:51Z. Those commits are in `main`'s history, so as the code stands no later commit reads met." The cold read of the finding (opencode-runner #965, sol, `VERDICT: PASS`) found that the code "imposes a stricter all-ancestor condition than the stated post-opening tree-preservation requirement", that the pin's twins and mutants omit the case, and that no ordinary descendant of `main` can recover.

The fault is counsel's twice over. The pin the second brief specified for that sentence, `second_window_cap`, requires that criterion 3 "refuses a prefix whose tree changes it after the opening", and has no twin for a branch cut before an opening and merged after it. And the opening paste waited until no proposal was open without looking for a session still building one: jack #1070 closed at 12:41:55Z, the session began its new branch at 12:42:10Z, the paste's `grant` was entered at 12:43:04Z, and #1071 was opened at 13:09:43Z.

**The lawful change** is to the machinery, not the law: "unchanged since the opening push" is tested on `main`'s own commits. It is made. The push of seq 7281 moved the evaluator under `judge/` with that one change, on his ruling of 20 November (answers 4 and 7). SPEC §10, **The promotion evaluator**: "one change is made: criterion 3's walk of the commits since an opening follows first parents only". A push is a change entry (A2.6; §6: "the failure is a precedent, the fix is a change entry, and the window starts again"). The sentence of criterion 3 is the one the sovereign read, word for word. §The code, change 2, states the test for this window, and its pin holds it there.

**The fix** is recorded by the sovereign's `decision fix` whose `subject` begins `C2a-prime:` (A2.6: "Veto, promotion, budget, grant, transmutation and the fix of a failed window are `decision` entries signed by a key declared in genesis"). Whether that entry is typed a decision or a repair is the subject of the next section.

## How C2a-prime's failure is witnessed: his veto
*Replaces v5's section of this name, which carried two routes. Row 69 owed him "the choice between his veto and his answer at the window's end put to him with what each needs". It was put to him on 18 November at about 01:06Z. He answered by entering the veto: `decision veto C2a-prime` at seq 5879 (2026-11-18T12:01:17Z), and again at seq 7180 (2026-11-22T11:44:05Z) under AMEND-A6. The other route, his answer after the stated end recorded as a ruling with an order of code, is struck.*

The ruling of 4 November, correction 2, tests a window's failure "by a sufficient condition on criterion 7 alone": "(a) no `decision promote` naming the window has `ts` at or before its stated end; and (b) a `decision veto` naming the window has `ts` at or before its stated end, or the window's acts evidence … holds a row with `repo` `renavondata/jack` and `class` `repair`" inside the window. And: "Where the test is not met — a window failing only on criteria 1 to 6 or on A3.4, or one with every criterion met and no promotion — no `fix` names the window until the sovereign has answered whether it failed; a `fix` entered regardless is a repair; his answer is recorded as a ruling and reaches `status.py` only through an order it carries."

C2a-prime failed on criterion 3, and his veto refuses its criterion 7. Condition (b) holds by its first limb: both vetoes have the window's name as their whole `subject`, and a `ts` before its stated end. `names_window` tests equality, so a subject with words after the name would name no window.

- *What the veto does.* The `fix` of §Order of acts step 2 is typed a decision by the evaluator `main` holds today; the third window's code does not change how this `fix` is typed: change 3 adds a name and a bound to functions that type a `fix`, and its test shows the record's set unchanged. The veto added an unmet criterion 7 to a window that already could not be promoted, and one entry to its A3.4 count. It does not name the third window (§The subject).
- *What it does not do.* The veto at seq 5879, entered before AMEND-A6, ended nothing early (A6, clause 2: "Not reached"). The veto at seq 7180, at A6's `activate_at`, ended C2a-prime, as failed, and moved nothing else (A6, clause 1): its stated end, the `fix` and the third window's opening stay keyed to 2026-11-30T00:00:00Z, so the third window opens only after that instant. COUNSEL-OPEN rows 39 and 69 sent an end before the stated end to C2c (row 69: C2c-3); for an end at his veto, his answer 12 of 20 November ("The one-clause early-end amendment (a window also ends, as failed, at his veto) proceeds now") brought it forward as AMEND-A6.
- *An entry of his and the item process.* `item_process` ends each entry with `if typ == "merge" or royal: pending = []` (line 135): any entry signed by a sovereign key, a veto or a `grant` as much as a `fix`, clears the resolutions that are waiting for their merge, and a resolution so cleared is in no batch. The read of v1 built such a log: 476 items without the veto, 475 with it placed between a resolution and its merge. On `main` that position does not arise by the verbs: a proposal's resolutions reach the log in one block that ends with its own `merge` entry (`tools/jack`, `v_merge`, appends it on the proposal's head), and a verb's entry is appended at `main`'s head, between blocks. The paste for the `fix` therefore enters nothing while a `resolution` entry follows the last `merge` on `main`'s log (§Order of acts step 2). Like every entry, the `fix` is also an instant at which a writ past its `resolves_by` is finalised as expired; the next entry would finalise it so in any case, with the same Y.
- *Evidence.* `judge/status.py` on `main` at `cbdac17b` (SHA-256 `0ac73f8ed1ba96e62081c146aed2a7543f41464eb91bc2af9f3820cafe5acce6`): `window_fixes` sets `veto_ok` from `names_window(es, x, "veto", name) and instant(x["ts"]) <= instant(w_early)` (line 392); `window_bounds` gives C2a-prime's bounds as `('2026-11-17T12:50:50Z', '2026-11-30T00:00:00Z', '2026-11-30T00:00:00Z')`. The same line stood in `tools/status.py` at `6ab25cd8`. There counsel's trial, which is not court code, ran `window_fixes` on the real log to seq 5738 with simulated entries carrying the signer of seq 5563. It printed: veto `C2a-prime` before the end, then `fix` after it → decision; veto `C2a` before the end, then `fix` → decision; veto with free text after the name → repair; veto after the end → repair; no veto → repair; `fix` before the end → repair. `tools/jack`'s `v_decision` checks nothing of a veto but that its subject is not empty.

## Precondition
*Replaces the second brief's section of this name.*

1. **C2a-prime's stated end has passed unpromoted.** It is after 2026-11-30T00:00:00Z; no `decision promote C2a` has `ts` after C2a-prime's opening (2026-11-17T12:50:50Z, seq 5564) and at or before that instant; no `push` falls inside C2a-prime's window: after seq 5564 and before C2a-prime's end, the earlier of that instant and a `decision veto` naming C2a-prime at or above AMEND-A6's `activate_at`. A push after such a veto and before 2026-11-30T00:00:00Z, such as the move's, is not inside the window and opens nothing (§The window).
2. **C2a-prime's failure is witnessed.** A `decision veto` with subject `C2a-prime` and `ts` at or before 2026-11-30T00:00:00Z is on the log: seqs 5879 and 7180.
3. **This brief and its two reads are on `main`.** The reads are by readers of different model families, neither returning a BLOCK. Each is a `transcripts/REVIEW-C2a-3-*.md` in the form `jack push --opens` reads: first line `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`; a `Reviewed tree:` at which this text's bytes equal `main`'s; carried to `main` by a proposal signed by a non-counsel key.
4. **The sovereign has read this brief before the builder's session is filed** (A2.10). His read is entered as his reads of BRIEF-C2b's Amendments 12 and 13 were (seqs 4714 and 4803): a `decision grant` whose subject says that he read this file at a stated SHA-256 and approved it unchanged. The same grant names the SHA-256 of the replay table of §The code, gives the one mark that section states and no other, names the SHA-256 of `SPEC.md` as counsel's patch leaves it (item 6), and states the cap (item 5). SPEC §10, **The promotion evaluator**, accepts a later change to the evaluator "against a table of the evaluator it changes and with the lines his grant for it marks". That asks, at the least, for a grant that names the table and its marks before the build. Whether "the same way" also asks that the grant's `subject` begin as item 15 states, the words leave open. So this grant begins so, as the grant of seq 6851 began: `promote_unmet: SPEC.md ` and the SHA-256 of `SPEC.md` as counsel's patch leaves it. Either reading is then met. Item 15 still finds the installing push at seq 7281, the first that qualifies (`judge/judge.py`, lines 212 to 237).
5. **The sovereign has stated the cap** (§The cap). The number is his, in terms, and it is on the log before the builder's session is filed: his grant of item 4 states it, in the words "the cap at C2a-3's opening is `<N3>`". SPEC §10 calls a cap that was not pre-stated before its build "a finding against the pre-statement".
6. **The scope's change is applied by the sovereign's own hand.** RUNBOOK, **Text before code**: such a change "is the first commit of the builder's branch — counsel's patch, applied and read by Guy there, with counsel's trailer". The patch holds the three changes to the scope and the two sentences of SPEC §10 that §The window lists, and nothing else. The evaluator's change is not in it: the builder builds that after his read, as the move was built (§The code). The second brief's Amendment 9 records what it cost when counsel applied such a patch itself (his entries at seqs 4016 and 4017).
7. **Counsel's V8 is entered** after item 3 and before the opening (§The window).
8. **The sovereign's `decision fix` is entered** as §Order of acts step 2 prescribes.
9. **Counsel's revision of RUNBOOK is on `main` before the opening push** (RUNBOOK, **Text before code**, as its revision for the move was). It is in words that take effect from that push, and it says two things. A late report refuses the promotion of the window it was entered in; RUNBOOK now says that one "prints as a late report that refuses `promote` while it stands" (line 425). And a window ended by a veto is read at that veto, while the W3 and W4 deadlines, which RUNBOOK gives as "the window's end" (lines 363 to 368), stay at its stated end.

## Scope
### The window
*Replaces the second brief's section of this name, whole.*

C2a-3 opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z, C2a-prime's stated end. `status.py` reads that instant as V5's `resolves_by`, finding V5 as `c2a_prime_window` finds it now.

The window is (opening `ts`, V8's `resolves_by`], where V8 is counsel's forecast with `args.id` `V8` and a `seq` below the opening's. A5.2 names that date, and this brief states no other. V8's claim is the promotion forecast's: every criterion of C2a-3 holds on the exit prefix by its `resolves_by`. Counsel enters it with `resolves_by` set to 2026-12-07T00:00:00Z, seven days after the stated end; or, if V8 is entered after the stated end, to 00:00:00Z on the date seven days after the UTC date of its entry. So the window can run for seven days at most, and no day before the stated end is taken from it. Two reasons. Nothing in the criteria needs days: each reads the prefix, the tree, one tests run and one acts table. And a window that cannot be promoted costs its remainder: C2a's first window ran thirteen days after its failure was known, and C2a-prime ran four days and twenty-two hours after its own, to his veto under A6. The sovereign's budget entry (seq 50) named fourteen days as a maximum; seven is inside it. Counsel enters V8 only when everything else the opening needs is on `main` or on the push's branch, so that the forecast is not spent on a wait.

Counsel enters no other forecast on this window. The sovereign's words on 17 November: "I just want you to stop making pointless forecasts. Everything should be under the law." V8 is the one A5.2 requires.

The push is made by `jack push <branch> --opens C2a-3 --review <file>`, the branch brought up to `main` after the `fix` by a merge commit with the sovereign's `Proposer:` trailer: `tools/jack` refuses a branch that does not contain `origin/main`, and a commit without a filled trailer. It changes the trusted base in five places. Three are the scope's: `judge/scope.json`'s `cap`, from 8,400 to the number of §The cap; SPEC §10's block, to match; and one clause of SPEC §10's cap history, "`<N3>` at C2a-3's opening, for the tests and pins of the window's code". The fourth is two sentences of SPEC §10's paragraph on the promotion evaluator, which §The code gives word for word. The fifth is the promotion evaluator, `judge/status.py`, changed as §The code states. And it carries the tests of that change and the reviewer's pins, built on branches before the opening, each commit with its `Proposer:` trailer. Its `--review` file is the reviewer's read of that code, `REVIEW-C2a-3-code.md`. There is no second push inside the window.

`jack push` as it stands checks neither the verdict of the `--review` file, nor counted lines, nor which party's commit touched which path: those checks run on proposals, and this code does not come by one. So the opening note records, at the branch head:
- the counted lines, `judge.counted_lines` over `counted`, at or under `<N3>`;
- each commit's `Proposer:` party against SPEC §10.8's scopes, two kinds of commit apart. The scope's change is counsel's patch with counsel's trailer, applied and read by the sovereign (§Precondition 6), and it holds the three changes to the scope and the two sentences of SPEC §10, and nothing else. The evaluator's change is the builder's, under `judge/`, which is in no party's paths and reaches `main` only by this push, as the move's commit `c9d2d9ba` did by the push of seq 7281;
- the replay of §The code: the reviewer's record that the changed evaluator printed every row of the table as §The code states, and every commit of `main`'s first-parent chain after *T* up to `main`'s head at the rehearsal. The paste replays the commits after that, up to `main`'s head when it merges;
- `REVIEW-C2a-3-code.md`'s first line, `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`, and the SHA-256 of `judge/status.py` that the read states. Three values must agree at the merged head: that one, the one the pin `replay_drift` holds, and the file's own.

### The cap
*New in v4; counted again in v6.*

`main` holds 8,340 counted lines under a cap of 8,400 (`judge.counted_lines` over `counted`, at `cbdac17b`). The evaluator's own lines are no longer among them: under `judge/` they left `counted` with the move (SPEC §10, **The promotion evaluator**: "its lines leave `counted`"). So of this brief's code only the tests and the reviewer's pins are counted. They do not fit in 60 lines, so the opening push raises the cap. The number, `<N3>`, is the sovereign's to state, and this draft does not state it for him. The verb asks for a change as well: `tools/jack push` refuses `--opens` on a branch that leaves `judge/scope.json` as it is (line 193).

**His answer 6 of 20 November cannot be applied as it reads.** "The move's push states the roughly 860 lines that leave the counted cap. The cap is lowered by that amount in the next window's opening push." What is measured:
- 883 counted lines left with the evaluator: 678 of `tools/status.py`, 181 of `tools/value.py` and 24 of `tools/entry.py`;
- the move added 781 elsewhere, for the judge's new ground, its tests and its pins: 581 under `tests/`, 173 under `pins/`, 20 under `tools/` and 7 under `harness/`. So the count went from 8,347 at `main`'s head before the push (`5b5f71ac`) to 8,245 at the push's commit (`20c6b9ae`);
- the two fixes of 23 November (seqs 7344 to 7347) added 95, to 8,340.

A cap of 8,400 less 883 is 7,517, which is under the count. So `<N3>` is a number he states afresh, and his statement of it stands in place of answer 6's subtraction for this opening. The question is put to him as one: the number, and that it replaces the subtraction.

What is measured of the need: C2a-prime's opening push took `main` from 7,784 counted lines (`391baaef`) to 8,347 (`045eff11`), 563 lines, for four changes and nine pins. By its diff, its tests and pins were `tests/test_status.py` +144, `pins/pins.py` +65, `tests/test_jack.py` +60 and `pins/c2a_prime.py` +58; the rest was the evaluator, then counted, and the verb. This brief orders six changes and eight pins, re-aims one pin, and changes no verb. A6 puts its own change, change 6, at "about 12 lines of code, 25 of tests and 30 of pin". Nothing of its code has been built, so its size is not measured; A2.10 forbids the build before his read. A fix that reaches `main` before the opening is counted too, each by its own text. If the tests and the pins do not fit under the number he states, §Stop and report if applies and the push is not made.

A cap is a resource constant (BRIEF-C2a §The cap). It enters no score.

**What follows for C2b.** `opening-c2b-3` (`6aa16322`) holds 10,321 counted lines under BRIEF-C2b's cap of 10,400, and it was built on the C2a-prime opening branch, before the move. So it holds neither the evaluator under `judge/` nor this brief's code, and its criterion 3 repeats the test the move corrected (opencode-runner #965). So BRIEF-C2b needs its own amendment before C2b opens: a rebuild on the evaluator as this window leaves it, a code read, and a cap that he states. That amendment is a separate text with its own read of his. It is not part of this brief, and this brief's window does not wait for it.

### The subject
*Replaces the second brief's section of this name.*

The promotion is `decision promote C2a`. The subject stays `C2a`: `tools/jack` admits a `promote` only for `C1a`, `C1b` and `C2a`, and BRIEF-C2b keys its opening on "the first `push` entry after `decision promote C2a`".

A5.1's "whose `subject` names the window" is read as the window open for that subject at the entry's instant. A `decision promote` with subject `C2a`, or a `decision veto` with subject `C2a` or `C2a-3`, names C2a-3 when both hold:
- its `ts` is after C2a-3's opening;
- no `promote C2a` has `ts` at or before 2026-11-30T00:00:00Z.

A `promote` with subject `C2a`, or a `veto` with subject `C2a` or `C2a-prime`, whose `ts` is after C2a-prime's opening and at or before C2a-3's opening names C2a-prime. That is the second brief's rule, bounded here by C2a-3's opening; the bound changes the typing of no `fix`, because the ruling's rule reads a `promote` or a `veto` only up to a window's stated end. So his vetoes at seqs 5879 and 7180 name C2a-prime and never C2a-3. A `veto` with subject `C2a-prime` entered after C2a-3's opening names no window. `status.py` assesses a `promote C2a` against the window it names, and prints `window: C2a-3 (third window of C2a, opened seq <n>)` beside the promotion line.

### What continues
*The second brief's rules, written out.* Value *E* and continued liveness *E* continue as they stand (A4.1; `wealth_continues`): the same events, base rate and mixture; the same item process from C1b's opening; the same attack gates. The streams run as BRIEF-C2a's Amendments 2 and 3 state, and this brief changes none. Nothing in `judge/value.py`, `tools/clerk.py`, `item_process`, `score_items`, `sovereign_keys` or `P0` changes. Nothing in the functions the second brief's change 2 names changes either, except as change 3 below states. The late-report rule changes none of them: `item_process` gathers late reports as it does now, and criterion 6 reads them by the rule (§The late-report rule). The streams must be running: A3.4's ratio needs world-typed entries inside the window (line 551: `exit_procedure <= 5 * s["object"]`), and a window with none is refused. The opening paste checks that his timer shows its stream calendar (§Order of acts step 2). C2a-3's reading runs the one item process and the one value ledger over the whole prefix from their first openings. So what is finalised between C2a-prime's end and C2a-3's opening is in the wealth C2a-3 continues, as the interval before C2a-prime's opening was in its (A4.1).

### The code
*Replaces the second brief's section of this name. That brief's four changes are on `main`, three in the evaluator as the move left it and the fourth in `tools/jack`, and stay as they are, except where a change below names them.*

The code is a change to the promotion evaluator, `judge/status.py` (SHA-256 `0ac73f8ed1ba96e62081c146aed2a7543f41464eb91bc2af9f3820cafe5acce6` on `main` at `cbdac17b`). The evaluator is trusted base. It changes only by the sovereign's push, and SPEC §10, **The promotion evaluator**, accepts a change to it only by replay: "A later change to the evaluator is accepted the same way, against a table of the evaluator it changes and with the lines his grant for it marks."

**The table.** A reviewer's session computes it and proposes it under `spec/vectors/`, as `promotion-replay-c2a-3.json`, in the form of `promotion-replay.json` (the ruling of 20 November, answer 9). Its evaluator is `judge/status.py` with `judge/value.py` as `main` holds them at the commit *T* that the table names, which is `main`'s head when the session starts. Its rows are every first-parent commit of `main` up to *T*, each run as SPEC §10 states a row's run. The adviser recomputes it independently, with its own driver, and posts any disagreement (answer 9: "A reviewer session computes it and proposes it under `spec/vectors/`. The adviser recomputes it independently and posts any disagreement here"). His grant names the table only after that.

**The marks: one kind, which A6 orders.** AMEND-A6, clause 3, *What reads it*: "Until the promotion evaluator's next change, `judge/status.py` reads every window to its stated end, and where it and this clause differ, this clause governs. That change reads the end, so that a window's items and the wealth it carries (A4.1) stop at such a veto, with a pin `vetoed_window_continues`." It comes "under the replay table that change carries, with the marks his grant gives it". This is that change: the pushes of seqs 7283 and 7339 changed the tests workflow alone. Change 6 below reads the end. So at every row whose log holds an entry after his veto of seq 7180 (2026-11-22T11:44:05Z), the lines from the one that begins `window C2a:` to the last are marked, the lines that begin `overdue forecast` apart. The row's output must be what the evaluator on `main` prints at the same commit with the row's arguments but for `--as-of 2026-11-22T11:44:05Z`, with that run's `overdue forecast` lines replaced by the row's own; the exit status is the row's. On this log that run reads the prefix that ends with the veto entry, because seq 7180 alone carries that `ts`; and the `sovereign REPAIR` lines are the same in both runs. The reviewer's session computes that output for each such row and records it in the table, in a member `marked` beside the row's `stdout`. So the mark is tested against the evaluator his grant reads, and not against the builder's code. On `main`'s chain today the marked rows are `bbfd0edf`, whose log runs to seq 7280, and every commit after it.

**No other line is marked,** for two facts of the record. No `push` on `main`'s log has `ts` after V5's `resolves_by`; so changes 1, 2, 4 and 5 and the tuple of new pins, which are read only on a prefix that holds C2a-3's opening push, are read on no row. And no `decision` on the log has a `subject` that is `C2a-3` or begins with it; so change 3, whose names `window_fixes` reads at line 379 and `names_window` at line 286, on every prefix, finds nothing on any row to read otherwise. Change 6 changes nothing at a row whose log ends at or before the veto, and nothing of C1a or C1b, which no veto at or above the height names. So the changed evaluator must print every unmarked line of every row byte for byte, and every marked line as its mark states, with the same exit status; the replay proves it row by row. After the rows it must print, at every commit of `git rev-list --first-parent` from *T* to `main`'s head when the paste merges, what the evaluator on `main` prints there, under the same mark. A push's merge has the pushed branch as its first parent, so that chain runs through each pushed branch and not through the commits `main` held beside it; the rows are the chain as git gives it, as the first table's are. His grant names the table's SHA-256 and gives this mark and no other (§Precondition 4).

**The pin `replay_drift` is re-aimed, and SPEC §10 says so.** As it stands the pin holds `judge/status.py` to the bytes of the move (`pins/replay.py`, line 80: "moved bytes differ"; mutant `other_source_bytes`), so no change to the evaluator can pass it. The reviewer re-aims it:
- it keeps its three rows of the first table, and the first table's SHA-256;
- it adds rows of the second table, one of them marked, and asserts the second table's SHA-256 as it asserts the first's;
- it holds `judge/status.py` to the SHA-256 of the evaluator the code read accepted, which `REVIEW-C2a-3-code.md` states, so that an edit that changes no output still dies there;
- it holds `judge/value.py` to the moved bytes, as now;
- its mutant `marked_walk_regressed` finds the first-parent line of `c2a_tree_evidence` (line 433), which change 2 therefore leaves byte for byte.

Counsel's patch changes two sentences of SPEC §10's paragraph on the promotion evaluator, and his grant names the patched `SPEC.md` (§Precondition 4). Before "Pin `replay_drift`:" it adds: "C2a-3's opening push changes the evaluator a second time, as `transcripts/BRIEF-C2a-3-draft.md` §The code states, against `spec/vectors/promotion-replay-c2a-3.json` and with the one mark his grant for it gives." And where the pin's sentence ends "or is moved from other bytes than those named, is admitted; twin, the moved evaluator passes", it will end "or whose bytes are not those the pin holds it to, is admitted; twin, the evaluator on `main` passes". The paragraph's account of the move ("as they are", "one change is made") stands as the history of the first change.

The builder builds the change on the push's branch after that grant, with its tests, as the move was built (commit `c9d2d9ba`, runner issue #1181). The reviewer runs the whole replay, and reads the code. No driver for the whole replay is on `main` (`tests/promotion_replay_spot.py` runs three rows), so the reviewer's session carries its own, and its record names it.

**Change 1, the window.** When the prefix assessed holds a `push` with `ts` after V5's `resolves_by`, and no `promote C2a` has `ts` at or before that instant, the C2a assessment reads C2a-3's window:
- the opening and V8 by the rules of §The window;
- criterion 3 against `<N3>`, and "unchanged since the opening" against that push, tested as change 2 states;
- criterion 7's acts interval from the opening, counting a row whose `time_hkt` minute, read as UTC+8, overlaps the window at all, as for C2a-prime;
- criterion 7's veto clause by §The subject;
- the window line.

Otherwise it reads C2a-prime's window or C2a's first window as now. With no V8 below the opening, it prints `promote C2a: refused: C2a-3 has no promotion forecast before its opening`.

**Change 2, criterion 3's test on this window.** "`judge/scope.json` and SPEC §10's block are unchanged since C2a-3's opening push" holds when the two are byte-equal to the opening push's commit's at the commit assessed and at every commit on the first-parent path from the commit assessed back to the opening push's commit (`git rev-list --first-parent <opening's commit>..<commit assessed>`). Those are the trees `main` itself has held since the opening: inside the window `main` moves only by the herald's merge commits and by the commits `jack`'s verbs make on it, and each has the previous `main` as its first parent. A commit that reached `main` only through a second or later parent of a merge was never `main`'s tree, and is not tested. The evaluator already walks first parents (`c2a_tree_evidence`, line 433): the move made that change for every window it reads. What this change adds for C2a-3 is the number. Criterion 3 reads `<N3>`, the opening's `cap` must equal it, and no `push` may follow the opening on the prefix, as lines 429 and 435 ask of the second window with its number. `c2a_tree_evidence` tells two windows apart today (`is_prime`, line 428), and gains the third.

C2a-prime's and C2a's assessments are not changed: on any instant inside either window the evaluator prints what the evaluator on `main` prints now. After C2a-prime's end at the veto, change 6 reads it as of that end, as A6 orders. A failed window is not patched in place (§6), and C2a's report part 2 quotes the tool as it read.

**Change 3, the names.** `WINDOW_NAMES` gains `C2a-3`. `window_bounds` gives its opening and V8's `resolves_by`, the same on both readings. `names_window` follows §The subject. So if C2a-3 fails, the ruling's rule as corrected can be applied to a `fix` naming it without another change of code. A test shows that on the real `log.jsonl`, up to its last entry before the opening push, `window_fixes` returns the set, and `item_process` the items, that the evaluator on `main` at `cbdac17b` returns. The test takes that evaluator from git, as the judge extracts the one it runs.

**Change 4, criterion 6's "unchanged" comparison** for C2a-3 starts at the tree of C2a-3's opening push and covers what the second brief's change 3 covers. It reads the evaluator's source where the move put it, `judge/status.py`, in both trees. Lines 436 and 437 on `main` read `tools/status.py`, which no tree after the move holds, so as they stand `c2a_tree_evidence` returns unmet for criteria 1, 3 and 6 alike at every commit after the move (lines 463 and 464; the ruling of 20 November, the drafter's check 4).

**Change 5, the late-report rule.** For C2a-3, criterion 6 is refused by a late report only when the report's `seq` is above C2a-3's opening push (§The late-report rule). `item_process` is not changed. The criterion's line prints the count it reads. The `late_reports` member that `--json` gives stays the whole list.

**Change 6, the vetoed end** (AMEND-A6, clause 3, *What reads it*). A window that the evaluator reads, of any subject, is ended by the earliest `decision veto` that names it (§The subject) and whose `seq` is at or above the `activate_at` of the `amend` entry with `id` `A6`. A window ends once: a later veto that names it ends nothing more. The window is chosen first, on the prefix at the instant assessed, as change 1 states; change 6 then applies to the window chosen. So once C2a-3's opening push is on the prefix, C2a-3 is read, whatever vetoes name C2a-prime.

When the prefix assessed holds an entry after that veto, the evaluator reads the window on the prefix that ends with the veto entry, as of the veto's `ts`. An entry that follows the veto is not read, even one that carries the veto's own `ts`: SPEC §7 asks only that timestamps do not decrease (lines 225 to 227). Every line the evaluator prints of the window is then the window's at its end: the window line, the criteria, A3.4, J7, the value, elections and liveness lines, any unverified `fix`, the window's name and the promotion line. So the window's items and the wealth it carries stop at the veto (A4.1). Reading at the veto cuts the log and not the tree: a figure read of the commit assessed, such as criterion 3's count, still follows the commit.

Three things the evaluator gives are not the window's. They are read as now, at the instant assessed and over the whole log:
- the list of overdue forecasts, which `tools/clerk.py` makes writs of (lines 54 to 56). A forecast that falls due after a veto must still be listed;
- the history of earlier promotions and the `sovereign REPAIR` lines, which `report` builds from every promotion on the log;
- the stated end. A6 does not move it, the window line prints it as before, and the status object's `end` stays that instant. So `tools/clerk.py`, which takes `end` as the deadline of its W3 and W4 writs (lines 56 and 82), reads what it reads today.

`--json` gives the same reading: `as_of`, `prefix`, `prefix_last_seq` and the figures are the window's at the veto, and `overdue`, `history`, `repairs` and `end` are as the list above says. A veto below the height ends nothing: seq 5879 is read as it is now. On the record the change is read for C2a-prime alone, from the veto of seq 7180, which is the only veto at or above the height. It would read C2a-3 the same way if he vetoed it.

**Tests and size.** The new pins are named in a tuple of their own, which criterion 1 reads when it reads C2a-3 and at no other time. `VALUE_PINS` is not changed: criterion 1 reads it at every commit of C2a's windows (line 461), and a name added to it would turn rows that read met to unmet. Each new pin is registered in `pins/pins.py` in the form `Pin("<name>"`, which is what that line looks for. There is a test for each change. Counted lines after the tests and the reviewer's pins together: at most `<N3>`.

### No item changes
*Written out for this boundary. The second brief's section of this name is not taken by reference: it speaks of C2a's first window and its nine rows.*

BRIEF-C1b §Liveness: "An item once finalised is never regrouped: no later entry, evidence string or merge changes an earlier item or any bet already placed (A4.3)." The `fix` must precede the opening push (the ruling's condition 3), and the push follows it by minutes.

Until the push, the evaluator as it stands assesses `promote C2a` against C2a-prime's window, and no `promote` can pass: criterion 3 reads unmet there, his veto refuses criterion 7, and the window has ended as failed (AMEND-A6).

The evaluator on `main` at the `fix` already types it a decision, by the veto. It records the `fix` against the writs open at its instant, and at the first `push` after it removes it from the writs still open; the `fix` is never a late report. A writ open at the `fix` and finalised before the push keeps the taint: it is the item the code made of it, and its Y, its stake and the wealth after it do not change at the push. The push changes no code that types a `fix` or makes an item, except the names of change 3, which that change's test shows to alter nothing on the record.

The sovereign pastes the `fix` and the push as §Order of acts step 2 prescribes, so the interval is minutes, and C2a's report lists any writ finalised in it.

### The late-report rule
*New in v6. It stands where v5's §The exemption stood, which was route B's.*

A late report is an entry by a sovereign key that the item process reads as a repair, entered when items exist and not typed a window's `fix` (`item_process`, line 114). Criterion 6 as the second brief stated it is refused by any late report on the prefix, whenever it was entered (`assess_value`, line 488: `not process["late_reports"]`). On `main` today the evaluator counts three: his `decision fix` entries at seqs 5877, 5878 and 5936, of 18 November, which record the `repropose` workflow disabled and re-enabled by hand and the interaction limit set. All three were entered inside C2a-prime's window. As the code stands they refuse criterion 6 on every later prefix, so no later window of C2a could be promoted.

**The rule for C2a-3.** A late report refuses criterion 6 of the window it was entered in, and of no other. For C2a-3 the criterion reads the late reports whose `seq` is above its opening push. One entered before the opening refuses nothing of C2a-3. One entered after it refuses C2a-3 to its end.

**Its ground.** His answer 11 of 20 November: "C2a-3's brief may pre-state that a repair refuses only the window it was made in. The rule is not in the charter, and A2.4 bars loosening the charter's bounds, not an earlier brief's" (the ruling's reading H4). His answer 12: "The late-report change waits and comes through the replay test after the move." Answer 7 foresaw "its own marked rows" for this change. As pre-stated here the rule is read for C2a-3 alone, so it changes no row, and no line is marked for it.

**What it does not change.**
- The items. A repair still taints every writ open at its entry, and a tainted writ's item has Y = 0, in this window as in any other. BRIEF-C1b §Liveness: "An item once finalised is never regrouped". The three entries of 18 November keep every taint they made, and the wealth after them is not recomputed.
- The statistic, the null and the threshold of criterion 6 (A4.1).
- What the evaluator prints of C1b, of C2a's first window or of C2a-prime. The three late reports are on C2a-prime's prefix alone, and there they refuse as before.
- A repair entered between windows. It is in no window, so it refuses none. It taints as any repair does.

**What it gives up.** A window is no longer refused by repairs made before it opened. What still binds a repair is its taint, which is paid in wealth.

### The acts evidence
*Written out for this window: the second brief's section as its Amendments 6, 7 and 11 leave it. Nothing of that section is taken by reference.*

Criterion 7 reads one attributed table, produced by the committed classifier over exactly the window. The classifier is `transcripts/evidence/guy_acts3.py` (SHA-256 `ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b`), unchanged before C2a-3's exit:

`python3 transcripts/evidence/guy_acts3.py renavondata/jack . <opening ts> <end ts> transcripts/evidence/acts-c2a3-<end>.csv`

and its raw twin by the committed collector (`transcripts/evidence/guy_acts2.py`, with its hash file beside it):

`python3 transcripts/evidence/guy_acts2.py renavondata/jack . <opening ts> <end ts> transcripts/evidence/acts-c2a3-<end>-raw.csv`

`<end>` is the table's end instant, in the file's name. Counsel commits both, with the classifier hash file, by a proposal; once it has merged, counsel re-runs the attributed command to the current instant, and the promotion may rest on the committed table only if that re-run holds no `repair` row after `<end>`. The table is named in the `decision`'s `--acts`, and the verb records it (the second brief's change 4, on `main`). The verb also commits, with the entry, the three evidence files SPEC §10 item 15 names (`run`, `runs` and `acts`), and the judge checks that each is present with its hash.

Criterion 7 holds on the exit prefix when three things do:
- (a) the body of the `promote` at which the exit prefix ends has a member `acts` with exactly the members `path`, `sha256` and `commit`, each a string, matching whole `transcripts/evidence/[A-Za-z0-9._-]+\.csv`, `[0-9a-f]{64}` and `[0-9a-f]{40}`;
- (b) `commit` is the parent of the first commit on `main` whose `log.jsonl` holds that `promote`, and the file at `path` in that commit's tree has that SHA-256;
- (c) `judge/status.py`, run on the exit prefix with `--acts` naming that file, prints criterion 7 met.

C2a's report runs the three and prints each. It also re-runs both commands with `<end ts>` one second after the `decision`'s `ts`, so that the collection holds every act up to that `ts`, its own second included, and none after it; it commits the results beside the table and prints any row from `<end>` to the `decision`, the `decision`'s own second included. Such a row does not undo a promotion entered on the prefix it read (A5.1), but it is a finding in the report.

What the table proves is limited, and the report says so. A table with no `repair` row is a measured zero for the acts the classifier sees on `renavondata/jack`. It does not see acts in other repositories, it cannot tell whose hand made an act under the owner's login beyond the declarations it reads, and a declaration can attribute a nearby act wrongly. The command reads GitHub's current record: comment bodies, labels, deletions. Counsel therefore commits the raw table with the attributed one, so the evidence the promotion read stays on `main` whatever GitHub later shows.

Between C2a-prime's end, at his veto of seq 7180 (2026-11-22T11:44:05Z), and C2a-3's opening no window of C2a is open, and the acts of that interval are in no window's acts evidence. C2a's report lists them. C2a-prime's own acts, from its opening at 2026-11-17T12:50:50Z to that veto, are collected by the same two commands for the report's account of the failed window.

## Order of acts
*Replaces the second brief's section of this name.*

1. **The brief, the table, his read, the build, V8.** This brief is merged with two reads on the record. A reviewer's session computes the replay table of §The code, it is merged, and the adviser recomputes it. The cap is put to him as one question (§The cap), and on his answer counsel writes the scope's patch for that number. Then the sovereign's read is one sitting and one paste. The paste waits for a quiet lane. It enters his `grant`, which names this file's SHA-256, the table's and the patched `SPEC.md`'s, gives the one mark and states the cap (§Precondition 4 and 5). Then it makes the builder's branch from `main` with counsel's patch as its first commit, applied by his hand, and publishes it (§Precondition 6), as he published the move's branch with his cherry-pick of counsel's text. The builder's session is then filed on that commit, and builds the evaluator's change and its tests. The reviewer's pins, the replay and the code read follow. Counsel proposes its revision of RUNBOOK (§Precondition 9), and enters V8.
2. **The sovereign's paste.** After 2026-11-30T00:00:00Z, with no `push` inside C2a-prime's window (§Precondition 1) and none after that instant, the sovereign makes one paste:

   ```
   jack decision fix "C2a-prime: criterion 3 read unmet from 2026-11-17T13:32:51Z to its end — its test walked every ancestor of main, and a branch cut before the opening was merged after it (jack #1071); for C2a-3 the test reads main's own commits"
   ```

   Then the push branch is brought up to `main` by a merge commit with the sovereign's `Proposer:` trailer, and the opening `push` follows at once (`jack push <branch> --opens C2a-3 --review <the push branch's worktree>/transcripts/REVIEW-C2a-3-code.md`). Counsel writes the exact commands into the opening note before that day.

   The paste waits, and does not stop while what it waits for can still come. His words to counsel of 19 November, in chat: "Always give a paste that waits for a quiet minute". They are on no file of `main`. Once started, the paste asks nothing of him: its first line says that he may leave it, and where the result will show, which is the `push` entry on `main`'s log or the line the paste stops with. It enters nothing until four things hold together.
   - **2026-11-30T00:00:00Z has passed.** The paste reads the clock for this. A `fix` with `ts` at or before that instant is typed a repair, and it bars every later `fix` that names the window (`window_fixes`, lines 380 to 384). The window's failure would then have no `fix` typed a decision, and the question would go to him (§Stop and report if).
   - **The lane is quiet:** no pull request is open on `renavondata/jack` but the three that stand open (#125, #316, #562), no session or re-proposal is in flight (no issue labelled `run` from the last 24 hours is open on the runner, and no run of `repropose`, `counsel-sign`, `counsel` or `opencode` is queued or running), and no `resolution` entry follows the last `merge` on `main`'s log (the `fix` is an entry of his, and clears what is pending as a veto would).
   - **No tick of the diary's timer is due before the push can land.** The paste reads the timer's next elapse on steel, and trusts no sentence for it. A tick that has not yet fired is not in flight, and a writ finalised between the `fix` and the push keeps the `fix`'s taint (§No item changes). The opening note states the time from `fix` to push as the rehearsal measures it. In the one such paste so far it was six minutes and twenty-one seconds (seqs 5563 and 5564), before the verb's check grew.
   - **The streams are running:** the diary's timer shows both its calendars (§What continues).

   **These waits are against the record's own lesson, and this brief says so for his read.** COUNSEL-OPEN row 68 records his complaint of 17 November at the second brief's paste, which waited about 42 minutes of his sitting on a clock and on the lane, and that both waits should go, "lawfully of course, and not now, but asap"; its lesson 5 is "No clock in his pastes". The lawful way was agreed the same day: C2c-1's verbs, which follow a moved `main`. They are not on `main`. Two days later he asked counsel for a paste that waits by itself and does not stop. So until C2c-1 this paste waits on the lane again, and it reads two times: the stated end, a date the law fixes (A6, clause 1), and his own timer's next elapse. If he would have it otherwise, his read is the place to say so.

   Then it checks that `judge/scope.json`'s `cap` on the branch is the number his grant states, enters the `fix`, brings the branch up to `main`, runs the opening note's tests and pushes. Those tests are the four records of §The window, taken at the merged head, the three hashes of the evaluator among them. Before the `fix`, while it waits, the paste replays every commit since the reviewer's record up to `main`'s head, so that after the `fix` only the commit that holds the `fix` is left to replay, and the time from `fix` to push stays short. If the verb refuses the push because `main` has moved, the paste brings his own `main` up to `origin/main`, which the verb asks before anything else (`tools/jack`, lines 31 to 47), then the branch up to `main`, runs the tests again and pushes again: no push was entered, and the `fix` is still the first that names C2a-prime and still precedes the next push. It waits and retries up to a bound that the opening note states, and at the bound it stops and says what it has entered. Criterion 3 needs none of this: by the test of change 2, a branch cut before the opening is not `main`'s tree, whenever it merges. The waits are for the `fix` and the push. Nothing in the code prevents a proposal from landing between them; the waits make it unlikely, and the second try answers it. The remedy the record names is C2c-1's: verbs that follow a moved `main` (row 68).
3. **The window code.** It is in force from the push. The `tests` run on `main` at the push's commit verifies it.
4. **The promotion.** `status.py` prints the window line, the value line, the liveness line and `promote C2a: lawful | refused: …`. Counsel commits the acts evidence. When the line reads `lawful`, the sovereign enters `decision promote C2a --acts <file>` (A5: at the crossing).
5. **C2b.** BRIEF-C2b's order of acts then begins at its step 3, on its amended text (§The cap). Its `decision promote C2a` is the entry of step 4 above and is not entered again.

## Pre-stated criteria for C2a-3, evaluated on the exit prefix
*Replaces the second brief's section of this name.*

C2a's seven, read on C2a-3's window:
1. Every pin of BRIEF-C2a's list, the nine of the second brief (its §Pins and its Amendment 7) and those of §Pins below is KILLED, with a passing twin, in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines are within `<N3>` and the kernel within 500. `judge/scope.json` and SPEC §10's block are unchanged since C2a-3's opening push. The second sentence is read of `main`, of the trees `main` itself has held since that push, and is tested as §The code, change 2, states.
4. The attack tests are green on `main` before the first scored event's cutoff (unchanged: 2026-11-01T15:59:44Z).
5. **Value**: *E*ᵥ ≥ 20 on the one ledger, by `judge/value.py`, wealth continued.
6. **Liveness continued**: C1b's process, with the ruling's rule, at or above 20 on the exit prefix, wealth continued. A late report refuses it when entered inside C2a-3's window, and not when entered before its opening (§The late-report rule).
7. No `decision` of kind `veto` naming C2a-3; **off-log repairs 0 on the acts evidence of C2a-3's window**; A3.4 at or under 5 : 1.

This brief states no minimum length for the window.

**What these criteria are worth.** The audit on `main` (`transcripts/AUDIT-criteria-20261117.md`) classes C2a-prime's seven as "2 sound, 3 narrow, 2 empty". Their statistics and thresholds are carried unchanged, but for what the head of this brief lists, because A4.1 requires "the same statistic under the same null", and because the sovereign decided on 17 November that a criterion is removed only by C2c-3's judged procedure (row 69). This brief adds no test that a system with no skill passes, and promotes C2a on no better evidence than the second brief would have.

## Pins (the reviewer's), each with its named mutant and passing twin
*Added to the second brief's nine, which stay registered.*

- `third_window_from_the_end`
  - Requires: C2a-3 opens at the first `push` whose `ts` is after V5's `resolves_by`, and is read only when no `promote C2a` has `ts` at or before that instant.
  - Mutants: opened by a `push` at or before that instant; read when C2a-prime was promoted.
  - Twin: a prefix that ends before that push is assessed against C2a-prime.
- `third_window_end_is_v8`
  - Requires: the end is V8's `resolves_by`; with no V8 below the opening, the promotion is refused in the words of change 1.
  - Mutants: V5's `resolves_by`; a V8 with `seq` above the opening accepted.
- `third_window_cap`
  - Requires: criterion 3 reads `<N3>`, and is unmet when the opening's `cap` is another number or a `push` follows the opening.
  - Mutants: 8,400, the second window's number; 7,800, the first's.
- `scope_unchanged_on_main`
  - Requires: on C2a-3, criterion 3's second sentence is tested on the first-parent path of change 2.
  - Twin: a branch cut before the opening push, whose commits hold the earlier `judge/scope.json`, is merged into `main` after it; criterion 3 reads met. This is the case of jack #1071.
  - Mutant: the walk over every commit reachable from the commit assessed and not from the opening's, which was the code on `main` at `6ab25cd8`, before the move.
  - Second requirement: a first-parent commit between the two at which either file differs, restored by a later one, reads unmet. Mutant: the two end trees compared alone.
- `veto_names_its_window`
  - Requires: §The subject. A `veto` with subject `C2a-prime` and `ts` before C2a-3's opening does not refuse C2a-3's criterion 7; a `veto` with subject `C2a` or `C2a-3` after the opening does.
  - Mutants: any `veto` with subject `C2a-prime` counted; a `veto` with subject `C2a-3` after the opening ignored.
  - Twin: a `veto` with subject `C2a` entered before C2a-3's opening names C2a-prime and does not refuse C2a-3.
- `offlog_from_third_opening`
  - Requires: criterion 7's acts interval begins at C2a-3's opening, with the overlap rule.
  - Mutant: C2a-prime's opening.
- `vetoed_window_continues` (AMEND-A6, clause 3, *What reads it*)
  - Requires: a window is ended by the earliest veto that names it at or above A6's `activate_at`, and is read, at every later instant, as of that veto's `ts` (change 6).
  - Mutant: a veto at or above the height is ignored as an end.
  - Twins: such a veto ends the window there; a veto below the height ends nothing; of two such vetoes the earlier ends it; an entry that follows the veto with the veto's own `ts` is not read; with C2a-prime so ended and C2a-3's opening push on the prefix, C2a-3 is read; the list of overdue forecasts is read at the instant assessed.
- `late_report_in_its_window`
  - Requires: on C2a-3, a late report whose `seq` is below the opening push does not refuse criterion 6, and one whose `seq` is above it does.
  - Twin: the record's three late reports of 18 November and none after the opening; criterion 6's late-report clause reads met.
  - Mutants: every late report on the prefix counted, which is the code on `main` at `cbdac17b`; none counted.
  - Second requirement: on C2a-prime, a late report whose `seq` is below C2a-prime's opening still refuses criterion 6, as the evaluator on `main` reads it. The fixture places one there, since the record's three are all above that opening. Mutant: the rule applied to every window.

**What the pins do not enforce.** *Written out; the second brief's list brought to this window.* These rules bind and are not pinned; the reads and C2a's report check them:
- two reads by different model families (the gate admits one accepting read);
- the sovereign's read of this brief (§Precondition 4), and his own application of the scope's patch (§Precondition 6);
- that the acts table the `promote` names is complete over the window: the verb records which table was read (the second brief's ninth pin), not that it is whole;
- that an attributed file was produced by the classifier from its raw twin: the hash file names the classifier, it does not attest a run;
- the App's custody of the court's platform acts, and the hand behind an act under the owner's login;
- counsel's platform acts in the window;
- no re-attribution of a row;
- the acts table's freshness, by the re-run of §The acts evidence;
- that `main` moves only by first-parent steps inside the window. That rests on what the herald and the verbs do, and on there being no push inside the window, which criterion 3 tests. Outside that discipline the first-parent path and `main`'s own past can part, in both directions: a fast-forward of `main` to a merge whose second parent holds `main`'s history would hide a tree `main` had held, and a first-parent branch holding another scope would refuse a `main` that never changed. Neither is made by the herald's merges or by any verb but `push`.
- the replay of §The code. The pin `replay_drift` holds a few rows of each table. The whole replay of this change, against the second table, is the reviewer's run: it is recorded, and it is not pinned.

The ruling's four conditions bound the re-typing route its Order 2 asks about; they do not close it. Once a window's failure is witnessed by his veto, the first `fix` naming it, between its stated end and the next push, is a decision whatever its `subject` says the sovereign did. C2a's report reads the `fix`'s `subject` against the record of the interval.

## Refusal list
*Written out; it is the second brief's list brought to this window, with three items added at the end.*

C2a's, entire, plus:
- no change to any criterion's statistic or threshold as this brief states them;
- no change to `transcripts/evidence/guy_acts3.py` before C2a-3's exit;
- no re-attribution of any row of C2a's acts evidence;
- no minimum window length;
- no second push inside the window;
- no code but §The code;
- no `decision fix` naming C2a-prime recommended or prepared for entry before 2026-11-30T00:00:00Z;
- **counsel's platform acts on `renavondata/jack` in the window are `jack` verbs and declared closes of its own stale proposals, nothing else**: no labels, no edits, no closing keywords, no reviews, no re-runs;
- no change to what `status.py` prints for an instant inside C2a's first window or C2a-prime's;
- no forecast of counsel's on this window but V8;
- no change to a verb of `tools/jack`: the verbs that follow a moved `main` are C2c-1's (row 68).

## Stop and report if
*Written out for this window.*

- **The tests and the pins do not fit under `<N3>`; or the evaluator's change, its tests or the pins are not on the push's branch; or the replay does not pass; or the code read does not accept.** Report the shortfall; the push is not made without them.
- **The opening push is refused after the `fix` for another reason than a moved `main`, or the paste's bound passes with the push not made.** Stop; C2a's report lists every writ finalised before the push lands, with its taint.
- **The `tests` run on `main` at the push's commit is not green, or a defect is found in a function change 4 covers.** The window cannot promote on a changed process. Stop; the next window is pre-stated.
- **The two checkers disagree.**
- **The streams are paused, or no world-typed entry falls inside the window.** A3.4 then refuses the promotion. Report it; the pause is his to lift.
- **A `repair` row appears in C2a-3's acts evidence.** Promotion has become impossible; the window fails at its stated end. The report names the row and its hand, and the next window is pre-stated by the same procedure.
- **V8's `resolves_by` passes with a criterion unmet.** If C2a-3 fails on criteria 1–6 or on A3.4 alone, with no `repair` row and no veto, no `fix` names it until the sovereign has answered whether it failed (correction 2).
- **V8's `resolves_by` passes with no opening push.** The forecast is resolved as it fell, and counsel enters no second V8: the next window is pre-stated afresh.
- **The `fix` is entered and `window_fixes`, run over the whole log, does not return its `seq`, or reports it unverified.** The tool's own assessment does not show this before the push, because it reads C2a-prime on the prefix that ends at its stated end; so the opening note has the paste run that one function on the whole log between the `fix` and the push, and stop there if the `seq` is missing. The question then goes to the sovereign.
- **A `decision fix` naming C2a-prime meets the ruling's condition 1 but not the rest**: entered at or before 2026-11-30T00:00:00Z, or after the opening push. It is a repair permanently (condition 4), and a late report. Entered before the opening push it taints the writs open at it and refuses nothing of C2a-3; entered after the push it refuses C2a-3's criterion 6 (§The late-report rule). Stop; the question goes to the sovereign before any other act.
- **A `push` lands after C2a-prime's opening (2026-11-17T12:50:50Z) and before its end, the earlier of 2026-11-30T00:00:00Z and a `decision veto` naming C2a-prime at or above AMEND-A6's `activate_at`.** It is a second push inside C2a-prime's window. Stop and report before any other act. A push after such a veto and before 2026-11-30T00:00:00Z, such as the move's, is outside the window and opens nothing.
- **A `push` after 2026-11-30T00:00:00Z precedes V8 or the `decision fix`, or does not set the cap to `<N3>`.** It opens a window with no end, no recorded fix or no room. Stop; the next window is pre-stated afresh by the same procedure.
- **The replay table cannot be computed as SPEC §10 states a row's run, or the reads find that a line must be marked which §The code does not mark.** A mark is his alone to grant (SPEC §10). Stop before the build; the question goes to the sovereign.

## Deliverables
- this brief and its reads; the sovereign's `grant` of his read; his statement of the cap; the scope's patch with the two sentences of SPEC §10, applied by his hand;
- his `veto` of C2a-prime (seqs 5879 and 7180);
- the replay table `spec/vectors/promotion-replay-c2a-3.json`, and the reviewer's record of the whole replay;
- counsel's revision of RUNBOOK (§Precondition 9);
- V8;
- the opening note with the exact commands of §Order of acts step 2;
- the evaluator's change and its tests, the pins, and `replay_drift` re-aimed, on the push's branch;
- the reviewer's read of the code, `REVIEW-C2a-3-code.md`;
- the acts evidence of C2a-3's window, raw and attributed, with its classifier hash file;
- C2a's report part 2, on C2a-prime's failure: the finding, the precedent, the four days and twenty-two hours the window ran after it, his veto under A6, any writ finalised between the `fix` and the push, and the table of the sovereign's acts in it;
- LAW.md's count of the sovereign's cap-change pushes, with C2a-prime's opening (seq 5564) and C2a-3's added.

## What this brief does not do
- It ends no window early and moves no stated end.
- It changes no criterion's statistic, and no threshold but criterion 3's number. Of criterion 6 it changes which late reports refuse it, and nothing else. It removes no criterion the audit found empty.
- It changes nothing in C2a-prime's window. Of what the tool prints of that window it changes one thing, which A6 orders: at an instant after the veto that ended it, the window is read as of that veto (change 6).
- It does not amend BRIEF-C2b (§The cap).
- It does not make the opening paste free of a quiet `main`. That is C2c-1's deliverable.

## Interests
Counsel's V8 needs this window to open and to promote. The precedent is counsel's fault (§The precedent), and this brief is the cost of it: two reads, the sovereign's read, a table, a build, a replay, a code read and a sitting of his. The late-report rule removes a refusal that stands against the window V8 forecasts, so counsel holds an interest in it. Its ground is his answers 11 and 12 of 20 November, not counsel's argument.
