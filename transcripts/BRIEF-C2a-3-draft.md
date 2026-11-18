# BRIEF-C2a-3 — the third window of C2a (draft v2, 18 November 2026, counsel-5, after the read of v1 at runner issue #994, `VERDICT: FAIL`)

This file is `transcripts/BRIEF-C2a-3-draft.md`. Wherever a tool reads a name the window is called `C2a-3`. It is a draft: no read has passed it, nothing in it is proposed, and no builder session is filed on it before the sovereign has read it (A2.10: "Code is written to a text Guy has read").

It is written on `transcripts/BRIEF-C2a-prime-draft.md` as `main` holds it, with its Amendments 1 to 11 ("the second brief" below). Every section that states a fact about this boundary is written out here. The read of v1 found that sections left standing by reference said things true of the second window and false of this one, so only rules are now taken by reference, and each place that does so names the sentences it replaces.

**Why there is a third window.** C2a-prime cannot be promoted. COUNSEL-OPEN row 69: "At `main` `b88d318e` and after, `tools/status.py --subject C2a` prints criterion 3 as 'scope equals SPEC and unchanged: False'; at the opening push's commit `6c0566c3` it printed True." The verb signs a promotion only when `status.py` prints `promote C2a: lawful`, and no later commit can make that line read so (§The precedent). The sovereign's words on 17 November: "I don't want unlawful revisions any more....". So C2a-prime runs to its stated end, 2026-11-30T00:00:00Z, with no change inside it. A5.1: "A window that reaches its stated end with a criterion unmet has failed (§6, A3.2); the stated end may not be moved." A3.2 requires what follows: "A window that fails is a precedent, fixed by a lawful change and followed by a new pre-stated window; it is never patched in place (§6)." A4.1 permits it: "A window that fails and is followed by a new one continues the same wealth process on the same statistic under the same null; *E* is never set back to 1 and no α is split."

**What this brief changes.** Of the second brief's criteria, it:
- changes criterion 3's number, and states the test of its second sentence;
- changes criterion 7's interval and the window its veto clause names;
- adds §Pins to criterion 1.

It adds no criterion and removes none. It also names the lawful change, the entries that record the failure and the fix, the instant the window opens, the forecast that carries its end, and the code that lets `status.py` read it.

## The precedent, and the lawful change
*Replaces the second brief's section of this name.*

**The precedent.** The second brief's criterion 3 ends: "`judge/scope.json` and SPEC §10's block are unchanged since C2a-prime's opening push." `main`'s own tree has held the opening's `judge/scope.json` and SPEC §10's block at every instant since that push. The code tests more than the sentence. In `tools/status.py`, `c2a_tree_evidence` compares the two files at the commit assessed and at every commit of `git rev-list <opening's commit>..<commit assessed>`: every commit reachable from the commit assessed and not from the opening's. Row 69: "Stream session 145 was re-proposed on a branch (`ops-stream-145-r`, jack #1071) whose first fourteen commits were made between 12:42:10Z and 12:51:53Z on the tree before the opening (cap 7,800), and which merged at 13:32:51Z. Those commits are in `main`'s history, so as the code stands no later commit reads met." The cold read of the finding (opencode-runner #965, sol, `VERDICT: PASS`) found that the code "imposes a stricter all-ancestor condition than the stated post-opening tree-preservation requirement", that the pin's twins and mutants omit the case, and that no ordinary descendant of `main` can recover.

The fault is counsel's twice over. The pin the second brief specified for that sentence, `second_window_cap`, requires that criterion 3 "refuses a prefix whose tree changes it after the opening", and has no twin for a branch cut before an opening and merged after it. And the opening paste waited until no proposal was open without looking for a session still building one: jack #1070 closed at 12:41:55Z, the session began its new branch at 12:42:10Z, the paste's `grant` was entered at 12:43:04Z, and #1071 was opened at 13:09:43Z.

**The lawful change** is to the machinery, not the law: for the third window, "unchanged since the opening push" is tested on `main`'s own commits (§The code, change 2). The sentence of criterion 3 is the one the sovereign read, word for word. The change is carried by the third window's opening push, which is a `push` entry (A2.6; §6: "the failure is a precedent, the fix is a change entry, and the window starts again").

**The fix** is recorded by the sovereign's `decision fix` whose `subject` begins `C2a-prime:` (A2.6: "Veto, promotion, budget, grant, transmutation and the fix of a failed window are `decision` entries signed by a key declared in genesis"). Whether that entry is typed a decision or a repair is the subject of the next section.

## How C2a-prime's failure is witnessed: the choice the sovereign is owed
*New. Row 69 owes him "the choice between his veto and his answer at the window's end put to him with what each needs", by 2026-11-27T12:00Z. This draft carries both routes, each written out. The choice was put to him on 18 November at about 01:06Z, with counsel's interest declared and no recommendation; his answer strikes one route before this brief's gate reads.*

The ruling of 4 November, correction 2, tests a window's failure "by a sufficient condition on criterion 7 alone": "(a) no `decision promote` naming the window has `ts` at or before its stated end; and (b) a `decision veto` naming the window has `ts` at or before its stated end, or the window's acts evidence … holds a row with `repo` `renavondata/jack` and `class` `repair`" inside the window. And: "Where the test is not met — a window failing only on criteria 1 to 6 or on A3.4, or one with every criterion met and no promotion — no `fix` names the window until the sovereign has answered whether it failed; a `fix` entered regardless is a repair; his answer is recorded as a ruling and reaches `status.py` only through an order it carries."

C2a-prime fails on criterion 3 alone, as far as the record shows today. So one of two things witnesses its failure.

**Route A: his veto before the stated end.** The sovereign enters, at any time before 2026-11-30T00:00:00Z:

```
jack decision veto C2a-prime
```

The `subject` is the window's name and nothing else: `names_window` tests equality, and a subject with words after the name names no window.

- *What it does.* Condition (b) holds by its first limb. The `fix` of §Order of acts step 2 is then typed a decision by the code `main` holds today; nothing in the third window's code touches how a `fix` is typed. The veto adds an unmet criterion 7 to a window that already cannot be promoted, and one entry to its A3.4 count. It does not name the third window (§The subject).
- *Its effect on the item process.* The read of v1 showed that v1's "it moves no statistic and no item" was false of the code. `item_process` ends each entry with `if typ == "merge" or royal: pending = []`: any entry signed by a sovereign key, a veto or a `grant` as much as a `fix`, clears the resolutions that are waiting for their merge, and a resolution so cleared is in no batch. The reader built such a log: 476 items without the veto, 475 with it placed between a resolution and its merge. On `main` that position does not arise: a proposal's resolutions reach the log in one block that ends with its own `merge` entry (`tools/jack`, `v_merge`, appends it on the proposal's head), and a verb's entry is appended at `main`'s head, between blocks. On the log to seq 5738, 63 entries are signed by sovereign keys and none has a resolution pending before it (counsel's count, not court code). The paste for the veto therefore checks first that no `resolution` entry follows the last `merge` on `main`'s log, and enters nothing otherwise. Like every entry, the veto is also an instant at which a writ past its `resolves_by` is finalised as expired; the next entry would finalise it so in any case, with the same Y.
- *What it does not do.* It ends nothing early. The window still runs to its stated end (A5.1), and the third window opens only after it. An end before the stated end is the clause that goes to C2c-3 (COUNSEL-OPEN rows 39 and 69).
- *Evidence.* `tools/status.py` on `main` at `6ab25cd8` (SHA-256 `b255520996cef0ec20691c46cbc236ce5826dc166d16697762fa85f30fe86acb`): `window_fixes` sets `veto_ok` from `names_window(es, x, "veto", name) and instant(x["ts"]) <= instant(w_early)`; `window_bounds` gives C2a-prime's bounds as `('2026-11-17T12:50:50Z', '2026-11-30T00:00:00Z', '2026-11-30T00:00:00Z')`. Counsel's trial, which is not court code, ran that `window_fixes` on the real log to seq 5738 with simulated entries carrying the signer of seq 5563. It printed: veto `C2a-prime` before the end, then `fix` after it → decision; veto `C2a` before the end, then `fix` → decision; veto with free text after the name → repair; veto after the end → repair; no veto → repair; `fix` before the end → repair. `tools/jack`'s `v_decision` checks nothing of a veto but that its subject is not empty.
- *Cost.* One paste of one verb by the sovereign, once, before the end. No code, no further text.
- *Reversible.* No. A veto is an entry on the log.

**Route B: his answer after the stated end.** Nothing is entered before the end. After 2026-11-30T00:00:00Z the sovereign answers that C2a-prime failed on criterion 3. Counsel records the answer as a ruling, `transcripts/RULING-<date>-c2a-prime-failed.md`, which a cold read passes before it is proposed (row 34). The ruling carries an order of code.

- *What it needs.* A fifth change to the code (§The code, change 5): `window_fixes` types the first `fix` whose subject begins `C2a-prime:` a decision on the ruling's order. `window_fixes` is one of the functions the second brief's change 2 names, and the code that types the `fix` lands with the opening push, minutes after the `fix`, as the second brief's change 2 did on 17 November. In the interval the code then on `main` types the `fix` a repair: a taint on every writ open at its entry, and a late report, since items exist. §No item changes and §The exemption below state what follows on route B, on the second brief's argument.
- *Cost.* His answer and his read of the ruling's order (A2.10), both after the end; a ruling with its cold read and its proposal; one more change, its pin and its tests under the cap; the opening later by the time those take.
- *Reversible.* The ruling, by a later ruling. The `fix`, no.

**If neither.** No `fix` names C2a-prime (correction 2), the precondition below is unmet, and no third window opens.

**Counsel's interest (row 35).** Route A spares counsel a ruling, a change of code and their reads, and opens the window that counsel's V8 forecasts sooner. Counsel therefore recommends neither route. The choice is the sovereign's.

## Precondition
*Replaces the second brief's section of this name.*

1. **C2a-prime's stated end has passed unpromoted.** It is after 2026-11-30T00:00:00Z; no `decision promote C2a` has `ts` after C2a-prime's opening (2026-11-17T12:50:50Z, seq 5564) and at or before that instant; no `push` follows seq 5564 before it.
2. **C2a-prime's failure is witnessed.** Route A: a `decision veto` with subject `C2a-prime` and `ts` at or before 2026-11-30T00:00:00Z is on the log. Route B: the ruling is on `main`, and the sovereign has read its order.
3. **This brief and its two reads are on `main`.** The reads are by readers of different model families, neither returning a BLOCK. Each is a `transcripts/REVIEW-C2a-3-*.md` in the form `jack push --opens` reads: first line `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`; a `Reviewed tree:` at which this text's bytes equal `main`'s; carried to `main` by a proposal signed by a non-counsel key.
4. **The sovereign has read this brief before the builder's session is filed** (A2.10). His read is entered as his reads of BRIEF-C2b's Amendments 12 and 13 were (seqs 4714 and 4803): a `decision grant` whose subject says that he read this file at a stated SHA-256 and approved it unchanged.
5. **The sovereign has stated the cap** (§The cap). The number is his, in terms.
6. **The trusted-base change is applied by the sovereign's own hand.** RUNBOOK, **Text before code**: such a change "is the first commit of the builder's branch — counsel's patch, applied and read by Guy there, with counsel's trailer". The patch holds the three changes §The window lists and nothing else. The second brief's Amendment 9 records what it cost when counsel applied such a patch itself (his entries at seqs 4016 and 4017).
7. **Counsel's V8 is entered** after item 3 and before the opening (§The window).
8. **The sovereign's `decision fix` is entered** as §Order of acts step 2 prescribes.

## Scope
### The window
*Replaces the second brief's section of this name, whole.*

C2a-3 opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z, C2a-prime's stated end. `status.py` reads that instant as V5's `resolves_by`, finding V5 as `c2a_prime_window` finds it now.

The window is (opening `ts`, V8's `resolves_by`], where V8 is counsel's forecast with `args.id` `V8` and a `seq` below the opening's. A5.2 names that date, and this brief states no other. V8's claim is the promotion forecast's: every criterion of C2a-3 holds on the exit prefix by its `resolves_by`. Counsel enters it with `resolves_by` set to 00:00:00Z on the date seven days after the UTC date of its entry, so the window can run for seven days at most. Two reasons. Nothing in the criteria needs days: each reads the prefix, the tree, one tests run and one acts table. And a window that cannot be promoted costs its remainder: C2a's first window ran thirteen days after its failure was known, and C2a-prime runs twelve days and ten hours after its own. The sovereign's budget entry (seq 50) named fourteen days as a maximum; seven is inside it. Counsel enters V8 only when everything else the opening needs is on `main` or on the push's branch, so that the forecast is not spent on a wait.

Counsel enters no other forecast on this window. The sovereign's words on 17 November: "I just want you to stop making pointless forecasts. Everything should be under the law." V8 is the one A5.2 requires.

The push is made by `jack push <branch> --opens C2a-3 --review <file>`, the branch brought up to `main` after the `fix` by a merge commit with the sovereign's `Proposer:` trailer: `tools/jack` refuses a branch that does not contain `origin/main`, and a commit without a filled trailer. It changes three things in the trusted base: `judge/scope.json`'s `cap`, from 8,400 to the number of §The cap; SPEC §10's block, to match; and one clause of SPEC §10's cap history, "`<N3>` at C2a-3's opening, for the window code". And it carries the window code (§The code), its tests and the reviewer's pins, built on branches before the opening, each commit with its `Proposer:` trailer. Its `--review` file is the reviewer's read of that code, `REVIEW-C2a-3-code.md`. There is no second push inside the window.

`jack push` as it stands checks neither the verdict of the `--review` file, nor counted lines, nor which party's commit touched which path: those checks run on proposals, and this code does not come by one. So the opening note records, at the branch head:
- the counted lines, `judge.counted_lines` over `counted`, at or under `<N3>`;
- each commit's `Proposer:` party against SPEC §10.8's scopes, the commit of the trusted-base change apart: that one is counsel's patch with counsel's trailer, applied and read by the sovereign (§Precondition 6), and it holds the three changes above and nothing else;
- `REVIEW-C2a-3-code.md`'s first line, `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`.

### The cap
*New.*

`main` holds 8,347 counted lines under a cap of 8,400 (`tree_facts` of `tools/status.py`, at `6ab25cd8`). The window code and its pins do not fit in 53 lines, so the opening push raises the cap, as the second brief's did. The number, `<N3>`, is the sovereign's to state, and this draft does not state it for him.

What is measured: C2a-prime's opening push took `main` from 7,784 counted lines (`391baaef`) to 8,347 (`045eff11`), 563 lines, for four changes and eight pins: `tools/status.py` +266 −38, `tests/test_status.py` +144, `pins/pins.py` +65, `tests/test_jack.py` +60, `pins/c2a_prime.py` +58, `tools/jack` +12. This brief orders four changes on route A, none of them the size of the second brief's change 2 (the typing of a `fix`) or its change 4 (the `promote` entry names its table), and six pins. Nothing of this brief's code has been built, so its size is not measured; A2.10 forbids the build before his read. If the code and the pins do not fit under the number he states, §Stop and report if applies and the push is not made.

A cap is a resource constant (BRIEF-C2a §The cap). It enters no score.

**What follows for C2b.** `opening-c2b-3` (`6aa16322`) holds 10,321 counted lines under BRIEF-C2b's cap of 10,400, and it was built on the C2a-prime opening branch, so it holds none of this brief's code. Its criterion 3 repeats the test this brief corrects (opencode-runner #965). So BRIEF-C2b needs its own amendment before C2b opens: the same correction, a rebuild on this window's code, a code read, and a cap that he states. That amendment is a separate text with its own read of his. It is not part of this brief, and this brief's window does not wait for it.

### The subject
*Replaces the second brief's section of this name.*

The promotion is `decision promote C2a`. The subject stays `C2a`: `tools/jack` admits a `promote` only for `C1a`, `C1b` and `C2a`, and BRIEF-C2b keys its opening on "the first `push` entry after `decision promote C2a`".

A5.1's "whose `subject` names the window" is read as the window open for that subject at the entry's instant. A `decision promote` with subject `C2a`, or a `decision veto` with subject `C2a` or `C2a-3`, names C2a-3 when both hold:
- its `ts` is after C2a-3's opening;
- no `promote C2a` has `ts` at or before 2026-11-30T00:00:00Z.

A `promote` with subject `C2a`, or a `veto` with subject `C2a` or `C2a-prime`, whose `ts` is after C2a-prime's opening and at or before C2a-3's opening names C2a-prime. That is the second brief's rule, bounded here by C2a-3's opening; the bound changes the typing of no `fix`, because the ruling's rule reads a `promote` or a `veto` only up to a window's stated end. So a veto entered on route A names C2a-prime and never C2a-3. A `veto` with subject `C2a-prime` entered after C2a-3's opening names no window. `status.py` assesses a `promote C2a` against the window it names, and prints `window: C2a-3 (third window of C2a, opened seq <n>)` beside the promotion line.

### What continues
*The second brief's rules, written out.* Value *E* and continued liveness *E* continue as they stand (A4.1; `wealth_continues`): the same events, base rate and mixture; the same item process from C1b's opening; the same attack gates. The streams run as BRIEF-C2a's Amendments 2 and 3 state, and this brief changes none. Nothing in `tools/value.py`, `tools/clerk.py`, `item_process`, `score_items`, `sovereign_keys` or `P0` changes. On route A nothing in the functions the second brief's change 2 names changes either, except as change 3 below states; on route B change 5 changes one of them, under §The exemption.

### The code
*Replaces the second brief's section of this name. That brief's four changes are on `main` and stay as they are, except where a change below names them.*

The code is the builder's: one branch, built after the sovereign's read and before the opening, and carried by the opening push. It changes `tools/status.py`.

**Change 1, the window.** When the prefix assessed holds a `push` with `ts` after V5's `resolves_by`, and no `promote C2a` has `ts` at or before that instant, the C2a assessment reads C2a-3's window:
- the opening and V8 by the rules of §The window;
- criterion 3 against `<N3>`, and "unchanged since the opening" against that push, tested as change 2 states;
- criterion 7's acts interval from the opening, counting a row whose `time_hkt` minute, read as UTC+8, overlaps the window at all, as for C2a-prime;
- criterion 7's veto clause by §The subject;
- the window line.

Otherwise it reads C2a-prime's window or C2a's first window as now. With no V8 below the opening, it prints `promote C2a: refused: C2a-3 has no promotion forecast before its opening`.

**Change 2, criterion 3's test on this window.** "`judge/scope.json` and SPEC §10's block are unchanged since C2a-3's opening push" holds when the two are byte-equal to the opening push's commit's at the commit assessed and at every commit on the first-parent path from the commit assessed back to the opening push's commit (`git rev-list --first-parent <opening's commit>..<commit assessed>`). Those are the trees `main` itself has held since the opening: inside the window `main` moves only by the herald's merge commits and by the commits `jack`'s verbs make on it, and each has the previous `main` as its first parent. A commit that reached `main` only through a second or later parent of a merge was never `main`'s tree, and is not tested. The other conditions of the code stand: the opening's `cap` equals `<N3>`, and no `push` follows the opening on the prefix.

C2a-prime's and C2a's assessments are not changed: on any instant inside either window `status.py` prints what it prints now. A failed window is not patched in place (§6), and C2a's report part 2 quotes the tool as it read.

**Change 3, the names.** `WINDOW_NAMES` gains `C2a-3`. `window_bounds` gives its opening and V8's `resolves_by`, the same on both readings. `names_window` follows §The subject. So if C2a-3 fails, the ruling's rule as corrected can be applied to a `fix` naming it without another change of code. A test shows that on the real `log.jsonl`, up to its last entry before the opening push, `window_fixes` returns the set, and `item_process` the items, that the code on `main` at `6ab25cd8` returns.

**Change 4, criterion 6's "unchanged" comparison** for C2a-3 starts at the tree of C2a-3's opening push and covers what the second brief's change 3 covers.

**Change 5, route B only: the ruling's order.** The first sovereign `decision fix` whose subject begins `C2a-prime:`, with `ts` after 2026-11-30T00:00:00Z and `seq` below the first `push` after that instant, is typed a decision when no `promote` names C2a-prime at or before that instant. The ruling's file and SHA-256 are named in the pin. On route A this change is not built.

**Tests and size.** The new pins join `VALUE_PINS`, so criterion 1 requires them. There is a test for each change. Counted lines after the window code and the reviewer's pins together: at most `<N3>`.

### No item changes
*Written out for this boundary. The second brief's section of this name is not taken by reference: it speaks of C2a's first window and its nine rows.*

BRIEF-C1b §Liveness: "An item once finalised is never regrouped: no later entry, evidence string or merge changes an earlier item or any bet already placed (A4.3)." The `fix` must precede the opening push (the ruling's condition 3), and the push follows it by minutes.

Until the push, `status.py` as it stands assesses `promote C2a` against C2a-prime's window, and no `promote` can pass: criterion 3 reads unmet there, and after 2026-11-30T00:00:00Z the window has failed (A5.1).

*Route A.* The code on `main` at the `fix` already types it a decision, by the veto. It records the `fix` against the writs open at its instant, and at the first `push` after it removes it from the writs still open; the `fix` is never a late report. A writ open at the `fix` and finalised before the push keeps the taint: it is the item the code made of it, and its Y, its stake and the wealth after it do not change at the push. The push changes no code that types a `fix` or makes an item, except the names of change 3, which that change's test shows to alter nothing on the record.

*Route B.* The code on `main` at the `fix` types it a repair: a taint on every writ open at its entry and, since items exist, a late report, so that criterion 6 reads unmet on the prefixes between the `fix` and the push. Change 5 takes effect at the push and not before. A writ open at the `fix` and finalised before the push is the item the code then in force made of it, tainted, and stays so. The `fix` frees only the writs finalised after the push, and from the push it is a late report on no prefix. On the prefixes between the `fix` and the push, the push changes nothing but criterion 6's late-report count, which is neither an item nor a bet.

On either route the sovereign pastes the `fix` and the push as §Order of acts step 2 prescribes, so the interval is minutes, and C2a's report lists any writ finalised in it.

### The exemption
*Route B only. On route A no refusal is touched and no exemption is claimed.*

Change 5 is exempt from three refusals: this brief's "nothing in … the functions the second brief's change 2 names changes" (§What continues); "no change to any criterion's statistic or threshold" (§Refusal list); and BRIEF-C2a's "no change to C1's statistics". The grounds are those on which the second brief's change 2 was read and accepted:
- A3.2 makes C2a-3 a new pre-stated window and this brief its pre-statement.
- The change is inert on the record as it stands. The log to seq 5738 holds one `fix`, seq 5563, whose subject begins `C2a:`, and change 5 reads only a `fix` whose subject begins `C2a-prime:`. So on every prefix before such a `fix` the items, the stakes and the wealth are those the code yields now, and change 3's test shows it.
- It decides only how the boundary `fix` is typed, and A2.6 typed that before any window opened: "the fix of a failed window" is a `decision`.
- A4.1's "same statistic under the same null" holds: the null and A4.3's stake rule do not change.

The order that carries the sovereign's answer to the code is the ruling's (correction 2: "his answer is recorded as a ruling and reaches `status.py` only through an order it carries"). If the reads find the exemption beyond this brief's power, the question goes to the sovereign before the opening.

### The acts evidence
*The second brief's section stands as its Amendments 6 and 7 leave it, with three replacements.* For `acts-c2a2-<end>` read `acts-c2a3-<end>` in both commands. For C2a-prime's window and opening read C2a-3's. And for "it is a finding in the report and resolves V6 0" read "it is a finding in the report": this window has no V6. The classifier is `transcripts/evidence/guy_acts3.py`, unchanged before C2a-3's exit.

## Order of acts
*Replaces the second brief's section of this name.*

1. **The brief, his read, the build, V8.** This brief is merged with two reads on the record. The sovereign reads it and enters his `grant` (§Precondition 4), and states the cap. Counsel writes the trusted-base patch for that number, and the sovereign applies it with his own hand as the first commit of the builder's branch (§Precondition 6). The builder's session is then filed on that commit; the reviewer's pins and code read follow. Counsel enters V8.
2. **The sovereign's paste.** After 2026-11-30T00:00:00Z, with no `push` since seq 5564, the sovereign makes one paste:

   ```
   jack decision fix "C2a-prime: criterion 3 read unmet from 2026-11-17T13:32:51Z to the stated end — its test walked every ancestor of main, and a branch cut before the opening was merged after it (jack #1071); for C2a-3 the test reads main's own commits"
   ```

   Then the push branch is brought up to `main` by a merge commit with the sovereign's `Proposer:` trailer, and the opening `push` follows at once (`jack push <branch> --opens C2a-3 --review <the push branch's worktree>/transcripts/REVIEW-C2a-3-code.md`). Counsel writes the exact commands into the opening note before that day.

   The paste checks once that no pull request is open on `renavondata/jack` but the three that stand open (#125, #316, #562), and that no `resolution` entry follows the last `merge` on `main`'s log (the `fix` is an entry of his, and clears what is pending as a veto would). If either fails, it says which and stops, having entered nothing. It holds no clock and no loop: the second brief's paste waited about 42 minutes of his sitting (row 68). Row 69 listed "an opening guard that looks for sessions in flight" for this brief. This brief orders none, and says so here for his read. Criterion 3 needs none: by the test of change 2, a branch cut before the opening is not `main`'s tree, whenever it merges. What a session in flight can still do is move `main` between the `fix` and the push, if a proposal it opens passes its checks in that interval. Nothing in the code prevents that; the record shows only that it did not happen in the one such paste so far (seqs 5563 and 5564, six minutes and twenty-one seconds apart). The verb then refuses the push, the stop condition for a push refused after the `fix` applies, and the opening costs the sovereign a second sitting. The remedy the record names is C2c-1's: verbs that follow a moved `main` (row 68).
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
5. **Value**: *E*ᵥ ≥ 20 on the one ledger, by `tools/value.py`, wealth continued.
6. **Liveness continued**: C1b's process, with the ruling's rule, at or above 20 on the exit prefix, wealth continued.
7. No `decision` of kind `veto` naming C2a-3; **off-log repairs 0 on the acts evidence of C2a-3's window**; A3.4 at or under 5 : 1.

This brief states no minimum length for the window.

**What these criteria are worth.** The audit on `main` (`transcripts/AUDIT-criteria-20261117.md`) classes C2a-prime's seven as "2 sound, 3 narrow, 2 empty". They are carried unchanged because A4.1 requires "the same statistic under the same null", and because the sovereign decided on 17 November that a criterion is removed only by C2c-3's judged procedure (row 69). This brief adds no test that a system with no skill passes, and promotes C2a on no better evidence than the second brief would have.

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
  - Mutant: 8,400.
- `scope_unchanged_on_main`
  - Requires: on C2a-3, criterion 3's second sentence is tested on the first-parent path of change 2.
  - Twin: a branch cut before the opening push, whose commits hold the earlier `judge/scope.json`, is merged into `main` after it; criterion 3 reads met. This is the case of jack #1071.
  - Mutant: the walk over every commit reachable from the commit assessed and not from the opening's, which is the code on `main` at `6ab25cd8`.
  - Second requirement: a first-parent commit between the two at which either file differs, restored by a later one, reads unmet. Mutant: the two end trees compared alone.
  - Third requirement: an instant inside C2a-prime's window reads criterion 3 as the code on `main` at `6ab25cd8` reads it. Mutant: change 2 applied to every window.
- `veto_names_its_window`
  - Requires: §The subject. A `veto` with subject `C2a-prime` and `ts` before C2a-3's opening does not refuse C2a-3's criterion 7; a `veto` with subject `C2a` or `C2a-3` after the opening does.
  - Mutants: any `veto` with subject `C2a-prime` counted; a `veto` with subject `C2a-3` after the opening ignored.
- `offlog_from_third_opening`
  - Requires: criterion 7's acts interval begins at C2a-3's opening, with the overlap rule.
  - Mutant: C2a-prime's opening.
- Route B only: `answered_fix_is_decision`, for change 5. Mutant: every `fix` naming C2a-prime typed a decision, including one entered before the end or after the push.

**What the pins do not enforce.** The second brief's section stands for its nine pins. In addition: no pin shows that `main` moves only by first-parent steps inside the window. That rests on what the herald and the verbs do, and on there being no push inside the window, which criterion 3 tests. Outside that discipline the first-parent path and `main`'s own past can part, in both directions: a fast-forward of `main` to a merge whose second parent holds `main`'s history would hide a tree `main` had held, and a first-parent branch holding another scope would refuse a `main` that never changed. Neither is made by the herald's merges or by any verb but `push`.

## Refusal list
*Written out; it is the second brief's list brought to this window, with three items added at the end.*

C2a's, entire, but for §The exemption where route B is taken, plus:
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

- **The window code and the pins do not fit under `<N3>`, are not on the push's branch, or the code read does not accept.** Report the shortfall; the push is not made without them.
- **The opening push is refused after the `fix`.** Stop; C2a's report lists every writ finalised before the push lands, with its taint.
- **The `tests` run on `main` at the push's commit is not green, or a defect is found in a function change 4 covers.** The window cannot promote on a changed process. Stop; the next window is pre-stated.
- **The two checkers disagree.**
- **A `repair` row appears in C2a-3's acts evidence.** Promotion has become impossible; the window fails at its stated end. The report names the row and its hand, and the next window is pre-stated by the same procedure.
- **V8's `resolves_by` passes with a criterion unmet.** If C2a-3 fails on criteria 1–6 or on A3.4 alone, with no `repair` row and no veto, no `fix` names it until the sovereign has answered whether it failed (correction 2).
- **V8's `resolves_by` passes with no opening push.** The forecast is resolved as it fell, and counsel enters no second V8: the next window is pre-stated afresh.
- **Route A: the `fix` is entered and `status.py` prints `window fix <seq>: unverified`, or types it a repair.** Stop before the push; the question goes to the sovereign. On route B the `fix` is typed a repair until the push, by design (§No item changes), and this condition does not apply.
- **A `decision fix` naming C2a-prime meets the ruling's condition 1 but not the rest**: entered at or before 2026-11-30T00:00:00Z, or after the opening push. It is a repair permanently (condition 4), and a late report that refuses criterion 6 at every later prefix. Stop; the question goes to the sovereign before any other act.
- **A `push` lands between 2026-11-17T12:50:50Z and 2026-11-30T00:00:00Z.** It is a second push inside C2a-prime's window. Stop and report before any other act.
- **A `push` after 2026-11-30T00:00:00Z precedes V8 or the `decision fix`, or does not set the cap to `<N3>`.** It opens a window with no end, no recorded fix or no room. Stop; the next window is pre-stated afresh by the same procedure.
- **Route B: the reads find §The exemption beyond this brief's power.** The question goes to the sovereign before the opening.

## Deliverables
- this brief and its reads; the sovereign's `grant` of his read; his statement of the cap; the trusted-base patch, applied by his hand;
- route A: his `veto`; route B: the ruling, its read and his read of its order;
- V8;
- the opening note with the exact commands of §Order of acts step 2;
- the window code and its tests, and the pins, on the push's branch;
- the reviewer's read of the code, `REVIEW-C2a-3-code.md`;
- the acts evidence of C2a-3's window, raw and attributed, with its classifier hash file;
- C2a's report part 2, on C2a-prime's failure: the finding, the precedent, the twelve days and ten hours the window ran after it, the route taken, any writ finalised between the `fix` and the push, and the table of the sovereign's acts in it;
- LAW.md's count of the sovereign's cap-change pushes, with C2a-prime's opening (seq 5564) and C2a-3's added.

## What this brief does not do
- It ends no window early and moves no stated end.
- It changes no criterion's statistic, and no threshold but criterion 3's number. It removes no criterion the audit found empty.
- It changes nothing in C2a-prime's window or in what the tool prints of it.
- It does not amend BRIEF-C2b (§The cap).
- It does not make the opening paste free of a quiet `main`. That is C2c-1's deliverable.

## Interests
Counsel's V8 needs this window to open and to promote. The precedent is counsel's fault (§The precedent), and this brief is the cost of it: two reads, the sovereign's read, a build, a code read and a sitting of his. Counsel holds an interest in route A and recommends neither route.
