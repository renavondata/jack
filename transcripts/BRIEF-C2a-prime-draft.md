# BRIEF-C2a-prime — the second window of C2a (draft v7, 4 November 2026, counsel)

This file is `transcripts/BRIEF-C2a-prime-draft.md`. Wherever a tool reads a name the window is called `C2a-prime`, because `jack push --opens` does not admit `′`.

**How this draft came to stand here.**
- v2 answered counsel's cold read of v1. It reached `main` unread: the merge verb signed seq 1265 at 09:04:29Z, counsel withdrew #292 at 09:06:04Z, and GitHub merged it at 09:13:19Z while the verb was still waiting on checks (COUNSEL-OPEN row 34).
- v3, v4 and v5 were never proposed. Cold reads failed them.
- v6 reached `main` (#301). Its formal read `REVIEW-C2a-prime-astra.md` blocked it (F1): the window code landed after the `fix`, so items finalised between them would be recomputed, against BRIEF-C1b's "An item once finalised is never regrouped".
- v7, revised after two cold reads, replaces v6 and v2, as BRIEF-C2b's drafts v1–v6 replaced one another on `main` before their reads. It follows the corrections to `transcripts/RULING-20261104-window-fix.md`:
  - correction 2: condition 2 tested on criterion 7 alone; C2a's `fix` after 2026-11-17T12:00:00Z;
  - correction 3, as correction 6 corrects it: the rule's code lands with the opening push, under the exemption stated here;
  - correction 5: the sources of C2a's two readings;
  - correction 7: the ruling's Reasoning 6 bounds the re-typing route rather than closing it.

**Why there is a new window.** C2a's first window cannot now promote: criterion 7 is unmet on its acts evidence, and no later act removes a row. This brief pre-states the window that follows. A3.2 requires it: "a window that fails is a precedent, fixed by a lawful change and followed by a new pre-stated window; it is never patched in place". A4.1 permits it: "a window that fails and is followed by a new one continues the same wealth process on the same statistic under the same null".

**What the brief changes.** Of C2a's criteria, it:
- changes criterion 3's number;
- changes criterion 7's interval;
- adds §Pins to criterion 1;
- reads criterion 6 with the ruling's rule (§The exemption), its "unchanged" comparison covering the rule's code from the opening push;
- reads criterion 7's veto clause by §The subject.

Nothing else changes, and no stream changes. The brief also names:
- the lawful change that fixes the precedent;
- the entries that record the change and the fix;
- the instant the new window opens;
- the code that lets `status.py` read it, with the one change to C1b's item process that the ruling orders.

## C2a's stated end, read two ways
The question is unruled (correction 5; `transcripts/CASES.md`).
- **Early: 2026-11-15T15:04:14Z.** BRIEF-C2a's own pre-opening "fourteen days at most" (proposed at seq 355, merged at seq 356), which BRIEF-C2a Amendment 1 (seq 368) and `status.py`'s `c2a_window` read as min(V0's `resolves_by`, opening + 14 d).
- **Late: 2026-11-17T12:00:00Z.** A5.2: "the `resolves_by` of the promotion forecast the window's brief names, entered before the window opens; a brief states no other date". `REVIEW-C1b-A5.md` F8 applied that clause to a brief's fourteen-day maximum, and counsel accepted it. BRIEF-C2a says "V0's `resolves_by` is the window's end", and V0's claim (seq 361) says the same.

This brief never needs the answer. Every act it prescribes at C2a's boundary comes after the late instant, and its tests read each instant in the direction correction 2 prescribes. In this brief, "read late" and "read early" mean those two instants. For C2a-prime the two readings are one instant; for C2b, see §Stated ends under §The code.

## Precondition
1. **C2a's boundary has passed on both readings.**
   - It is after 2026-11-17T12:00:00Z.
   - No `decision promote C2a` has `ts` at or before that instant.
   - No `push` follows seq 367 before it.
2. **C2a's failure is witnessed as correction 2 tests it.** The attributed acts evidence `transcripts/evidence/acts-20261103T2144.csv` has been on `main` since #296, with its raw twin and `acts-20261103T2144-classifier.sha256` beside it. It holds nine rows with `repo` `renavondata/jack` and `class` `repair` inside C2a's window read early, from seq 367 at 2026-11-01T15:04:14Z to 2026-11-15T15:04:14Z. The earliest is at 2026-11-02 22:11 HKT. `transcripts/evidence/guy_acts3.py` on `main` has the SHA-256 that is the first token of that hash file, `ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b`.
3. **This brief and its two reads are on `main`.** The reads are by readers of different model families. Each is a `transcripts/REVIEW-C2a-prime-*.md` in the form `jack push --opens` reads:
   - first line `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`;
   - a `Reviewed tree:` at which this text's bytes equal `main`'s;
   - carried to `main` by a proposal signed by a non-counsel key.
4. **The ruling is on `main` with its corrections, and the sovereign has read corrections 1–4 and 6, and this brief's §The code and §No item changes, before the builder codes change 2's timing (correction 6, "Reading before coding"), and in any case before the push** (A2.10: "Code is written to a text Guy has read"). His reading of corrections 1–4 is recorded in COUNSEL-OPEN row 35, and the rest in the row that records it. Those texts carry the rules the code implements. Correction 5 corrects a citation in correction 2 and leaves its rule and last sentence standing; correction 7 corrects a word of the ruling's reasoning.
5. **Counsel's V5 is entered** after item 3 and before the opening.
6. **The sovereign's `decision grant` and `decision fix` are entered** as §Order of acts step 2 prescribes.

## The precedent, and the lawful change
At seq 1076 (2026-11-03T21:26:25Z), value *E* and continued liveness *E* stood at or above 20 on the same prefix for the first time:
- value *E* was 386.0 over 210 events (first at or above 20 at seq 789);
- continued liveness *E* was 24.5 over 62 items (first at or above 20 at seq 332).

Given the acts table of 21:44Z, `status.py` read `promote C2a: refused` on criterion 7: nine `repair` rows under the sovereign's login inside the window. That table is now `transcripts/evidence/acts-20261103T2144.csv`.

The nine rows, by hand:
- One was the sovereign's own hand at counsel's request: the draft conversion of #236, 3 Nov 14:31Z.
- The others were acts of the court's machinery under the owner's login, which the acts classifier can only type as the sovereign's:
  - the herald's re-run loop;
  - a closing keyword in a counsel pull request;
  - labels set when issues were filed;
  - closes whose hand is not established.

The failure is recorded as C2a's precedent in the C2a report. No row is re-attributed.

**The lawful change** (A3.2: "fixed by a lawful change") is to the machinery, not the law:
- From 2026-11-04T05:40Z every act of the court on jack's platform is made by a GitHub App, `renavondata-jack-court[bot]` (opencode-runner #227; #225, which proposed accounts per party, superseded). The first merge under it was PR #285 at 06:35:17Z.
- The herald re-runs nothing (opencode-runner #220).
- Counsel writes no closing keyword and asks the sovereign for no platform act.

The App is a capability grant (the ruling's §What this ruling does not decide). A2.6 makes a grant a `decision`, and none has been entered, so the sovereign enters `decision grant` for it at the boundary (§Order of acts step 2). `status.py` line 92 types a `decision` of a kind other than `fix` as no repair.

An act under the sovereign's login is now either his or counsel's, and counsel's carry their declaration (BRIEF-C1b Amendment 2). C2a-prime's window is the first whose record lets the criterion measure what §7 means.

**The fix** is recorded by the sovereign's `decision fix` whose `subject` begins `C2a:` (A2.6: "the fix of a failed window" is a `decision`). Under the ruling of 4 November 2026 as corrected, it is a decision and not a repair when it meets the ruling's four conditions, with condition 2 tested as correction 2 prescribes. §The code implements that rule.

## Scope
### The window
C2a-prime opens at the first `push` entry whose `ts` is after 2026-11-17T12:00:00Z, C2a's stated end read late. `status.py` reads that instant as V0's `resolves_by`, finding V0 by `args.id` `V0` with `seq` below seq 367, as `c2a_window` finds it now.

The window is (opening `ts`, V5's `resolves_by`], where V5 is counsel's forecast with `args.id` `V5` and a `seq` below the opening's. A5.2 names that date, and this brief states no other. V5's `resolves_by` is 2026-11-30T00:00:00Z, so every opening after 2026-11-17T12:00:00Z makes the window shorter than fourteen days.

The push is made by `jack push <branch> --opens C2a-prime --review <file>`. The branch is brought up to `main` after the `grant` and the `fix`, because `tools/jack` refuses a branch that does not contain `origin/main`; the merge commit that does so carries the sovereign's `Proposer:` trailer, because the verb refuses a commit without one. `jack push` fast-forwards `main` to the branch, so the push carries the branch's whole content. It changes three things in the trusted base:
- `judge/scope.json`'s `cap`, from 7,800 to **8,400**;
- SPEC §10's block, to match;
- one clause of SPEC §10's cap history: "8,400 at C2a-prime's opening, for the window code".

And it carries the window code (§The code), its tests and the reviewer's pins, built on branches before the opening, each commit with its `Proposer:` trailer. Its `--review` file is the reviewer's read of that code, `REVIEW-C2a-prime-code.md`, on the push branch and named by its path in that branch's worktree. Precedent: C1a's installing push (seq 29) carried the builder's code, the reviewer's pins and `REVIEW-C1a-code.md` as its `--review`.

`jack push` checks neither the `--review` verdict, nor counted lines, nor which party's commit touched which path: those checks run on proposals, and the code does not come by one. So the opening note records, at the branch head:
- the counted lines, `judge.counted_lines` over `counted`, at or under 8,400;
- each commit's `Proposer:` party against SPEC §10.8's scopes;
- `REVIEW-C2a-prime-code.md`'s first line, `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`.

8,400 is a resource constant of the 7,800 kind (BRIEF-C2a §The cap). It enters no score, and it is fixed here, not at the push. It is measured: the builder's draft of the window code to v4 (opencode-runner #242) stopped at 8,022 counted lines, 126 of code and 112 of tests, before v5's additions and before the reviewer's pins; 8,400 leaves room for those and no more than that. There is no second push inside the window.

### The subject
The promotion is `decision promote C2a`, entered by `jack decision` with body `{kind, subject}`. The subject stays `C2a` because BRIEF-C2b keys its opening on "the first `push` entry after `decision promote C2a`", and its read is on the record.

A5.1's "whose `subject` names the window" is read as the window open for that subject at the entry's instant. A `decision promote` with subject `C2a`, or a `decision veto` with subject `C2a` or `C2a-prime`, names C2a-prime when both hold:
- its `ts` is after C2a-prime's opening;
- no `promote C2a` has `ts` at or before 2026-11-17T12:00:00Z.

Otherwise a `promote` or `veto` with subject `C2a` names C2a's first window. `status.py` assesses a `promote C2a` against the window it names, and prints `window: C2a-prime (second window of C2a, opened seq <n>)` beside the promotion line.

### What continues
Value *E* and continued liveness *E* continue as they stand (A4.1; `wealth_continues`):
- the same events, base rate and mixture;
- the same item process from C1b's opening;
- the same attack gates.

The streams run as BRIEF-C2a Amendments 2 and 3 state; the HKJC stream ended with the meeting of 4 November (COUNSEL-OPEN row 30). Nothing in `tools/value.py`, `tools/clerk.py`, `item_process`, `score_items`, `sovereign_keys` or `P0` changes, except as §The exemption states.

### The code
The code is the builder's: one branch, pre-built before the opening and carried by the opening push (§The window). It makes three changes to `tools/status.py`.

**Change 1, the window.** When C2a-prime's opening push is on the prefix and no `promote C2a` has `ts` at or before 2026-11-17T12:00:00Z, the C2a assessment reads C2a-prime's window:
- the opening and V5 by the rules above;
- criterion 3 against 8,400, and "unchanged since the opening" against that push;
- criterion 7's acts interval from the opening, counting a row whose `time_hkt` minute, read as UTC+8, overlaps the window at all: the table drops seconds, and a proof of zero repairs may not lose a row at either edge;
- criterion 7's veto clause by §The subject: a `veto` with subject `C2a` or `C2a-prime` counts only when its `ts` is after C2a-prime's opening;
- the window line.

Otherwise it reads C2a's first window as now. With no V5 below the opening, it prints `promote C2a: refused: C2a-prime has no promotion forecast before its opening`.

**Change 2, the ruling's rule, as corrected.** A sovereign `decision fix` is typed a decision, not a repair, when and only when all four hold:
1. its `subject` begins with a window's name followed by `:`. The names are `C1a`, `C1b`, `C2a`, `C2a-prime`, `C2b`, and every later window a brief pre-states.
2. no `decision promote` naming that window has `ts` at or before its stated end read late, and one of these holds:
   - (b1) a `decision veto` naming the window has `ts` at or before its stated end read early;
   - (b2) an attributed acts file the `subject` names holds a row with `repo` `renavondata/jack` and `class` `repair` whose `time_hkt` minute, read as UTC+8 and spanning [t, t + 60 s), begins at or after the window's opening `ts` and ends at or before its stated end read early.
3. its `ts` is after the window's stated end read late, and its `seq` precedes the first `push` after that instant.
4. no earlier `decision fix` has a `subject` beginning with the same name and `:`.

The terms used above:
- **Attributed acts file** (BRIEF-C1b Amendment 2). A file under `transcripts/evidence/`, present in the tree of the commit that carries the `fix`, whose name ends `.csv` and not `-raw.csv`. In that same tree there must also be:
  - its raw twin (`.csv` replaced by `-raw.csv`);
  - its classifier hash file (`.csv` replaced by `-classifier.sha256`), whose first token equals the SHA-256 of `transcripts/evidence/guy_acts3.py` in that tree (`ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b` today).
- **Names a file.** A `subject` names a file when the file's name, with or without `.csv`, occurs in it with neither a letter, a digit, `-` nor `_` immediately before or after it. The ruling's Order 3 paste, "(acts-20261103T2144)", names `acts-20261103T2144.csv`, which holds nine rows inside C2a's window, and nothing else; a `subject` naming `acts-20261103T2144-raw` does not name the attributed file.
- **The commit that carries the `fix`.** The commit, among the ancestors of the commit `status.py` assesses, whose `log.jsonl` holds the `fix` entry while none of its parents' `log.jsonl` does. On `main`, that is the commit `jack decision` made.
- **A named file that holds no row.** One that does not parse as CSV with header `repo,time_hkt,class,kind,ref,note`.
- **Stated ends.**
  - C2a's: early, `c2a_window`'s end; late, V0's `resolves_by`.
  - C2a-prime's: V5's `resolves_by`, the same on both readings.
  - C2b's: the stated end and opening BRIEF-C2b gives when C2b opens; where that end is read two ways, (a) and condition 3 at the later instant and (b) at the earlier, as for C2a.
  - C1a and C1b promoted inside their windows (seqs 188 and 337), so no `fix` naming either meets condition 2.
- **Naming, for other windows.** For any window but C2a and C2a-prime, a `promote` or `veto` names it when its `subject` equals the window's name.
- **Change 2's functions.** The builder names them in one tuple in `tools/status.py`, which change 3's guard and the pins read. The guard reads the tuple from the tree of the opening push.

The test is computed outside `item_process`, which receives the set of `seq`s that meet the whole rule. For such a `fix`, `item_process` records it against the writs open at its instant as now, and at the first `push` after it removes it from the writs still open; it is never a late report. So a writ finalised between the `fix` and that push keeps the taint the code of its time gave it, and only writs finalised after the push, when the code is in force, are free of it (§No item changes). If the history or a named file cannot be read, the `fix` is typed a repair and `status.py` prints `window fix <seq>: unverified — <what is missing>`. The `fix` so typed is a late report on every prefix that holds it. Any other sovereign `decision fix` is BRIEF-C1b's repair.

**Change 3, criterion 6's "unchanged" comparison** (`c2a_tree_evidence`'s `process_at`) for C2a-prime.
- **Where it starts.** At the tree of the opening push, as C2a's comparison starts at its own. The code is there from the opening.
- **What it covers.** What it covers now (`item_process`, `score_items`, `sovereign_keys`, `P0`, `tools/clerk.py`), and:
  - change 2's functions, and every top-level function of `tools/status.py` they reference by name, transitively;
  - every top-level function of `tools/status.py` that calls `item_process` or one of change 2's functions, compared whole;
  - every top-level assignment of `tools/status.py` those functions read by name.

**Tests and size.** The new pins join `VALUE_PINS`, so criterion 1 requires them. There is a test for each change. A further test shows that on the real `log.jsonl`, up to its last entry before the first `decision fix` (the whole log if it holds none), `item_process` returns the same items with the set change 2 computes as with no set passed. Counted lines after the window code and the reviewer's pins together: at most 8,400.

### No item changes
BRIEF-C1b §Liveness: "An item once finalised is never regrouped: no later entry, evidence string or merge changes an earlier item or any bet already placed (A4.3)." The `fix` must precede the opening push (condition 3), and C2a's cap leaves no room for the code before that push, so the code lands at the push, minutes after the `fix`. Change 2 therefore takes effect at that push and not before. A writ open at the `fix` and finalised before the push is the item the code then in force made of it, tainted by the `fix`, and stays so; its `Y`, its stake and the wealth after it are unchanged by the push. The `fix` frees only writs finalised after the push. The sovereign pastes the `fix` and the push as §Order of acts step 2 prescribes, so that interval is normally empty.

Until the push, `status.py` as it stands assesses `promote C2a` against C2a's first window, and no `promote` can pass:
- criterion 7 refuses on the nine rows of `acts-20261103T2144` (criterion 3 is met until the push, which is the cap's only change);
- criterion 6 there does not see the `fix`, so its typing plays no part.

On prefixes between the `fix` and the push, the push changes nothing but criterion 6's late-report count, which is neither an item nor a bet.

### The exemption
Change 2 is exempt from three refusals:
- this brief's "nothing in … `item_process` … changes" (§What continues);
- this brief's "no change to any criterion's statistic or threshold" (§Refusal list);
- BRIEF-C2a's "no change to C1's statistics".

The grounds:
- A3.2 makes C2a-prime a new pre-stated window and this brief its pre-statement. Its criteria are C2a's, read on its window, and its refusal list is C2a's, entire, but for this exemption.
- The change is inert on the record as it stands. `log.jsonl` at 41f0d6c, seqs 0–1275, holds seven `decision` entries and no `fix`: four `transmute` (seqs 3, 28, 66, 136), one `budget` (seq 50) and two `promote` (seqs 188, 337). So on every prefix before the first `fix`, the items, the stakes and the wealth are those the code yields now.
- It decides only how the boundary `fix` is typed, and A2.6 typed that on 18 October 2026, before any window opened. BRIEF-C1b's reuse of `fix`, and the code that types every `fix` a repair, came after it (the ruling's Reasoning 2).
- A4.1's "same statistic under the same null" holds: the null p₀ = 6/11 and A4.3's stake rule do not change. What changes is that the one entry A2.6 names is read as A2.6 names it.

This is counsel's decision under corrections 3 and 6 (p 0.8). If the reads find the exemption beyond this brief's power, the question goes to the sovereign before the opening.

### The acts evidence
Criterion 7 reads one attributed table, produced by the committed classifier over exactly the window. The classifier is `transcripts/evidence/guy_acts3.py` (PR #232, SHA-256 `ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b`):

`python3 transcripts/evidence/guy_acts3.py renavondata/jack . <opening ts> <end ts> transcripts/evidence/acts-c2a2-<end>.csv`

and its raw twin by the committed collector (`transcripts/evidence/guy_acts2.py`, with its hash file beside it):

`python3 transcripts/evidence/guy_acts2.py renavondata/jack . <opening ts> <end ts> transcripts/evidence/acts-c2a2-<end>-raw.csv`

`<end>` is the table's end instant, in the file's name. Counsel commits both, with the classifier hash file, by a proposal; once it has merged, counsel re-runs the attributed command to the current instant, and the promotion may rest on the committed table only if that re-run holds no `repair` row after `<end>`. The table is named in the `decision`'s `--acts`. The C2a report re-runs both commands to the `decision`'s `ts`, commits the results beside the table, and prints any row between `<end>` and the `decision`; such a row does not undo a promotion entered on the prefix it read (A5.1), but it is a finding in the report and resolves V6 0.

What the table proves is limited, and the report says so. A table with no `repair` row is a measured zero for the acts the classifier sees on `renavondata/jack`. It does not see acts in other repositories, it cannot tell whose hand made an act under the owner's login beyond the declarations it reads, and a declaration can attribute a nearby act wrongly.

The command reads GitHub's current record: comment bodies, labels, deletions. Counsel therefore commits the raw table with the attributed one, so the evidence the promotion read stays on `main` whatever GitHub later shows.

The off-log acts between 2026-11-15T15:04:14Z and C2a-prime's opening fall, on the early reading, inside no window, and, on the late reading, inside C2a's window until 2026-11-17T12:00:00Z. The C2a report lists them under both.

## Order of acts, and the clock
1. **The brief and V5–V7.** This brief is merged with two reads on the record, by readers of different model families, neither returning a BLOCK. Counsel then enters V5–V7 (the ruling's Order 4, as corrected). V5's `resolves_by` is never moved.
2. **The sovereign's paste.** After 2026-11-17T12:00:00Z, with no `push` and no `promote C2a` since seq 367, the sovereign makes one paste:

   ```
   jack decision grant "GitHub App renavondata-jack-court[bot]: the court's platform acts on renavondata/jack (opencode-runner #227), in force since 2026-11-04T05:40Z"
   jack decision fix "C2a: criterion 7 unmet at the stated end — nine off-log repair rows (acts-20261103T2144); the court's platform acts moved to a GitHub App (opencode-runner #227)"
   ```

   The `fix` is the ruling's Order 3 paste, word for word. Then the push branch, which carries the cap change, the window code, its tests and the reviewer's pins, is brought up to `main` by a merge commit with the sovereign's `Proposer:` trailer, and the opening `push` follows at once (`jack push <branch> --opens C2a-prime --review <the push branch's worktree>/transcripts/REVIEW-C2a-prime-code.md`). The paste is made when no pull request is open on `renavondata/jack`: proposals opened before the `fix` are stale against it, and `jack push` refuses if `main` moves, so a writ finalised in the interval is rare. The clock alone does not ensure it: minutes 35–55 held 14 of the 57 batch items finalised from 2 to 4 November. The C2a report lists any such writ (§No item changes). Counsel writes the exact commands into the opening note before that day.
3. **The window code.** It is in force from the push. The `tests` run on `main` at the push's commit verifies it.
4. **The promotion.** `status.py` prints the window line, the value line, the liveness line and `promote C2a: lawful | refused: …`. Counsel commits the acts evidence. When the line reads `lawful`, the sovereign enters `decision promote C2a --acts <file>` (A5: at the crossing).
5. **C2b.** BRIEF-C2b's order of acts then begins at its step 3. Its `decision promote C2a` is the entry of step 4 above and is not entered again.

## Pre-stated criteria for C2a-prime, evaluated on the exit prefix
C2a's seven, read on C2a-prime's window:
1. Every pin of BRIEF-C2a's list and of §Pins below is KILLED, with a passing twin, in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines are within 8,400 and the kernel within 500. `judge/scope.json` and SPEC §10's block are unchanged since C2a-prime's opening push.
4. The attack tests are green on `main` before the first scored event's cutoff (unchanged: 2026-11-01T15:59:44Z).
5. **Value**: *E*ᵥ ≥ 20 on the one ledger, by `tools/value.py`, wealth continued.
6. **Liveness continued**: C1b's process, with the ruling's rule, at or above 20 on the exit prefix, wealth continued.
7. No `decision` of kind `veto` naming C2a-prime; **off-log repairs 0 on the acts evidence of C2a-prime's window**; A3.4 at or under 5 : 1.

This brief states no minimum length for the window. A5 makes a window a maximum, and a minimum would be a constant chosen by hand (BRIEF-C2a's refusal list; the withdrawn Amendment 4, COUNSEL-OPEN row 33). If every criterion holds an hour after the opening, the window closes in an hour, and the record says so.

## Pins (the reviewer's), each with its named mutant and passing twin
- **`second_window_from_the_end`**
  - Fixture: pushes at the analogues of seq 367, of an instant between 2026-11-15T15:04:14Z and 2026-11-17T12:00:00Z, and of an instant after it.
  - Requires: the opening is the first push after V0's `resolves_by`.
  - Mutants: the first push after seq 337, which is C2a's own (seq 367); the first push after `c2a_window`'s end.
- **`second_window_end_is_v5`**
  - Requires: the end is V5's `resolves_by`.
  - Mutants: V0's `resolves_by`; a V5 with `seq` above the opening accepted.
- **`second_window_cap`**
  - Requires: criterion 3 reads the cap the opening push set, and refuses a prefix whose tree changes it after the opening.
  - Mutants: 7,800 hard-coded, which refuses every prefix; the cap read at HEAD only, which accepts a later change.
- **`offlog_from_second_opening`**
  - Requires: criterion 7 counts rows from C2a-prime's opening, a row counting when its minute overlaps the window at all.
  - Mutants: from C2a's opening, which counts the nine; a row counted only when its minute begins inside the window, which loses a repair at 00:00:31Z in a window opened at 00:00:30Z.
- **`promote_refused_before_end`**
  - Requires: a `promote C2a` at a prefix before C2a-prime's opening is assessed against the first window, prints no `window: C2a-prime` line, and is refused on criterion 7; after the opening, a `veto` with subject `C2a-prime` refuses C2a-prime.
  - Mutants: assessed against C2a-prime whenever a V5 exists; a `veto` with subject `C2a-prime` after the opening ignored.
  - Twin: a `veto` with subject `C2a` before the opening does not refuse C2a-prime.
- **`window_fix_is_decision`**
  - Fixture:
    - a synthetic log on which W is C2a (an opening push above seq 337; V0 later than opening + 14 d, so its two readings differ);
    - one item finalised before the `fix`, and one writ open at its `ts` and finalised by a timely batch after the next `push`;
    - a temporary git repository holding W's attributed acts file (one `repair` row inside W read early), its raw twin and its classifier hash file, committed before the commit that carries the `fix`;
    - no `promote` naming W by its end read late;
    - then a `fix` whose `subject` begins `C2a:` and names the file, entered after the late end and before the next `push`, and the first `fix` naming W.
  - Requires: the open writ's item holds no `fix` in its repairs; the finalised item is unchanged; the `fix` is no late report.
  - Mutants:
    - the `fix` typed a repair;
    - condition 2 read as "ended without promotion";
    - (a) read early;
    - (b1) or the (b2) interval read late;
    - condition 3 read early;
    - condition 1 read as "contains the name";
    - the next-push bound of condition 3 dropped;
    - condition 4 dropped;
    - the carrying commit taken as the assessed head;
    - the attributed requirement dropped;
    - a file named by substring (`acts-X-raw` naming `acts-X.csv`);
    - the push removes every `fix`, qualifying or not.
  - Twins. Each is still a repair: it is in the open writ's repairs at its finalisation after the next push, and it is a late report:
    - a free-text `subject`;
    - a `subject` naming no attributed file;
    - the file committed only after the carrying commit;
    - a `subject` naming only the raw twin (`…-raw`), whose row lies inside W while the attributed file has none, and its twin in which the attributed file also has such a row and the `subject` still names only the raw twin;
    - the only `repair` row outside W, or in a minute that ends after W's early end;
    - a `promote` naming W between the two readings;
    - a `veto` naming W only between the two readings, with no file;
    - a `fix` entered between the two readings;
    - a `fix` entered after the next `push`;
    - a second `fix` naming W;
    - the history unreadable, which also prints the `unverified` line.
  - Further twin: a `veto` naming W at or before its early end, with no file, makes the `fix` a decision.
- **`window_fix_not_retroactive`**
  - Fixture: as `window_fix_is_decision`'s, with a second writ open at the `fix` and finalised by a timely herald batch before the next `push`, and a third open at the `fix` and finalised by a timely herald batch after the next `push`.
  - Requires: the second writ's item keeps the `fix` in its repairs, with `Y` 0 and the stake and wealth after it as the code before the rule computes them; the third is free of it.
  - Mutants: the rule applied from the `fix` (the second writ freed); the rule never applied (the third writ tainted).
- **`process_unchanged_from_opening`**
  - Twins: a tree identical to the opening push's reads `unchanged True`; a later tree that edits a change-2 function, a function one references, a caller of `item_process` (a widened set among them) or a top-level assignment one reads reads `unchanged False`.
  - Mutants of the guard: change 2's functions omitted; references not followed transitively; the callers omitted; the assignments omitted; the tuple read at the assessed tree.
  - Further twin: a later tree that drops a name from the tuple and edits that function reads `unchanged False`.
- **`wealth_continues`** (C2a's, unchanged).

## What the pins do not enforce
These rules bind and are not pinned; the reads and the C2a report check them:
- two reads by different model families (the gate admits one accepting read);
- the sovereign's reading of corrections 1–4 and 6 and of this brief's §The code and §No item changes;
- that the `decision`'s `--acts` file is the committed table, complete over the window: the verb takes any path, and the entry stores only `{kind, subject}`;
- that an attributed file was produced by the classifier from its raw twin: the hash file names the classifier, it does not attest a run;
- the App's custody of the court's platform acts, and the hand behind an act under the owner's login;
- counsel's platform acts in the window;
- no re-attribution of a row;
- the acts table's freshness, by the re-run of §The acts evidence.

The rule's four conditions bound the re-typing route the ruling's Order 2 asks about; they do not close it. The first `fix` naming a failed window, between its late end and the next push, is a decision whatever its `subject` says the sovereign did. So a fresh repair described as the boundary `fix` would be typed a decision. That route is one entry per failed window, it costs a failed window, and the report reads the `fix`'s `subject` against the acts table of the interval. R2, a distinct kind for the boundary act (BRIEF-C2c), types the boundary act by kind alone; it does not close the route either, since a repair can be entered under that kind as under a false `grant`. `window_fix_is_decision` proves the typing, not that the sovereign's hands did no work.

## Refusal list
C2a's, entire, but for §The exemption, plus:
- no change to any criterion's statistic or threshold as this brief states them;
- no change to `transcripts/evidence/guy_acts3.py` before C2a-prime's exit;
- no re-attribution of any row of C2a's acts evidence;
- no minimum window length;
- no second push inside the window;
- no code but §The code;
- no `decision fix` naming C2a recommended or prepared for entry before 2026-11-17T12:00:00Z;
- **counsel's platform acts on `renavondata/jack` in the window are `jack` verbs and declared closes of its own stale proposals, nothing else**: no labels, no edits, no closing keywords, no reviews, no re-runs.

## Stop and report if
- **The window code and the pins do not fit under 8,400, are not on the push's branch, or the code read does not accept.** Report the shortfall; the push is not made without them.
- **The opening push is refused after the `fix`.** Stop; the C2a report lists every writ finalised before the push lands, with its taint.
- **The `tests` run on `main` at the push's commit is not green, or a defect is found in a function change 3 covers.** The window cannot promote on a changed process. Stop; the next window is pre-stated.
- **The two checkers disagree.**
- **A `repair` row appears in C2a-prime's acts evidence.** Promotion has become impossible; the window fails at its stated end. The report names the row and its hand, and the next window is pre-stated by the same procedure.
- **V5's `resolves_by` passes with a criterion unmet, or with no opening push.** If C2a-prime fails on criteria 1–6 or on A3.4 alone, with no `repair` row and no veto, no `fix` names it until the sovereign has answered whether it failed (correction 2).
- **A `decision fix` naming C2a meets condition 1 but not the rest.** For example: entered at or before 2026-11-17T12:00:00Z, entered after the opening push, or naming no attributed acts file. It is a repair permanently (condition 4), and a late report that refuses criterion 6 at every later prefix. Stop; the question goes to the sovereign before any other act.
- **A `push` lands between 2026-11-15T15:04:14Z and 2026-11-17T12:00:00Z.** On the late reading it is a second push inside C2a's window. Stop and report before any other act.
- **A `push` after 2026-11-17T12:00:00Z precedes V5 or the `decision fix`, or does not set the cap to 8,400.** It opens a window with no end, no recorded fix or no room. Stop; the next window is pre-stated afresh by the same procedure.
- **The reads find §The exemption beyond this brief's power.** The question goes to the sovereign before the opening.

## Deliverables
- this brief and its reads;
- V5–V7;
- the opening note with the exact commands of §Order of acts step 2;
- the window code and its tests, and the pins, on the push's branch;
- the reviewer's read of the code, `REVIEW-C2a-prime-code.md`, the push's `--review` file;
- the acts evidence of C2a-prime's window, raw and attributed, with its classifier hash file;
- the C2a report, with:
  - a section on the first window's failure:
    - the nine rows as precedent;
    - the lawful change and its `grant`;
    - C2a's stated end, read two ways and unruled;
    - the off-log acts between 2026-11-15T15:04:14Z and C2a-prime's opening;
    - the sovereign's acts outside jack on 4 November: three runner merges and a runner label, as off-log repairs the instrument cannot see, and the App as a capability grant;
  - a section on C2a-prime's exit: its length, its acts count, and any writ finalised between the `fix` and the push, with its taint;
- LAW.md's count of the sovereign's cap-change pushes corrected: seqs 5, 9, 29, 197 and 367, not "two so far", and C2a-prime's opening added.

The first window's acts evidence has been on `main` since #296: `acts-20261103T2144` raw and attributed, its classifier hash, and `runs-tests-20261103T2144.json`.

## Counsel's forecasts on this window (entered after the reads, before the opening push)
| id | claim | p |
|---|---|---|
| V5 | the promotion forecast: every criterion of C2a-prime holds on the exit prefix by this forecast's `resolves_by`, 2026-11-30T00:00:00Z | 0.7 |
| V6 | the acts evidence of C2a-prime's window holds zero rows of class `repair` | 0.75 |
| V7 | `decision promote C2a` is entered within 48 hours of C2a-prime's opening push | 0.55 |

V0–V3 are not edited, and each resolves on its own words.
- **V0, V2 and V3.** They speak of C2a's exit prefix or window end. On the late reading, that instant is their own `resolves_by`, 2026-11-17T12:00:00Z. V0 resolves 0 on either reading, and a later `decision promote C2a` naming C2a-prime does not make its claim true; but when it may be resolved depends on the reading. This brief recommends no resolution of any of the three before that instant, and counsel takes the expiry each then risks. That interest is disclosed in the corrections to the ruling.
- **V1** ("within 7 days of the opening push") does not depend on the reading.

Counsel's forecasts on C2b likewise resolve on their own words (BRIEF-C2b Amendment 2).

## Amendment 1 (10 November, counsel-3; what criteria 5 and 6 are — before the opening, one clause, no code)

- **The question.** On 10 November counsel reported the two statistics as "far past the bar" and the sovereign asked whether the other agents' critiques had not said *E* was compromised; they had (`transcripts/RESEARCH-meta-jack-20261107.md` §2; `transcripts/RESEARCH-semantics-20261109.md` §§8, 10, 12, 16 and its map, rows 28, 34, 48). Counsel answered that it would proceed as pre-stated; he asked (13:50 HKT): "is it fine to 'promote on criteria you know to be empty'? I'm not against amending briefs!"
- **What a brief may do.** Not drop them: §6 requires "liveness and value reach *Eₜ* ≥ 20", and a brief tightens the charter's bounds and never loosens them (A2.4). Not change them here: C2a-prime follows C2a's failure, and A4.1 has it continue "the same wealth process on the same statistic under the same null". Say what they are, before the opening: that is this clause.
- **His read.** The clause carries no rule that code implements, so by row 35 it is not put to him as a text to read before a build; he asked the question it answers, and it is in the message that brings him BRIEF-C2b's Amendment 10.

**The clause.** Criteria 5 and 6 are the charter's condition; they stay conditions of this window's promotion, assessed unchanged, and are offered as nothing else. On 10 November value *E* stands near 2.6 × 10²⁰ and continued liveness near 5 × 10¹⁸²; of the 1,019 resolutions of forecasts entered since C2a's opening (seq 367), 984 are of `world.renavon`, the hourly freshness stream that a template of the court's schedules on datasets the sovereign operates; liveness stood at 0.135 at seq 2215 on 7 November — the same cadence, the other way. **What can fail in this window is criterion 7** — no repair of the sovereign's on the acts evidence of the window, which is what C2a failed — and criteria 1–3 with it. No report of this window, and no later text of counsel's, cites the promotion as evidence of value or of liveness; the C2a report carries this paragraph's first two sentences where it prints the two statistics. What *E* should count is the sovereign's ruling at C2c-3 (COUNSEL-OPEN row 49), made there as one pre-stated act with the old process retired; nothing in this window changes the statistic.

**What does not move.** Every criterion's wording, every pin, the code on `opening-c2a-prime` (`a17864c`), the opening note, V5–V7. The two formal reads of v7 were of bytes this clause changes, so the gate's reviews are read again at these bytes, by readers of two families, before the opening (§Precondition 3).

**Interests.** Counsel's V5 and V7 are neither likelier nor less likely by this clause. It costs counsel two reads and the claim it made that morning.

## Amendment 2 (10 November, counsel-3; a false figure in Amendment 1 corrected — before the opening, one clause, no code)

- **The error.** Amendment 1's clause says "continued liveness near 5 × 10¹⁸²". The figure is false. `tools/status.py --subject C2a --as-of 2026-11-10T07:00:00Z` on `main` prints criterion 6 as SHORT: the wealth is 0.63 over 267 items since the attack gate, 162 of them successes and 105 expiries. The tool prints the wealth as an exact fraction of two long integers; counsel reported its size wrongly, and did not set it against the tool's own verdict or against the 0.135 of 7 November that the same clause quotes two lines on.
- **How it was found.** By a rehearsal of the sitting of 17 November on a scratch copy of the repository, with the status tool run on simulated entries, an hour after the sovereign read the clause (14:27 HKT) and minutes after the clause reached `main` (COUNSEL-OPEN row 51). Four cold reads of the amendment had passed it; none ran the tool.

**The clause, corrected.** Amendment 1's clause stands with two of its sentences replaced.
- For "On 10 November value *E* stands near 2.6 × 10²⁰ and continued liveness near 5 × 10¹⁸²" read: "On 10 November value *E* stands near 3.6 × 10²⁰ over 981 events. Continued liveness stands at 0.63, below the charter's 20. At each day's end since 1 November it has stood between 0.14 and 154,000; its failed items are forecasts not resolved by their deadline, 57 of the 105 on 5 and 6 November and six on the 10th; at its present stake a batch resolved on time multiplies it by about 1.11 and an expiry by about 0.87".
- For "**What can fail in this window is criterion 7** — no repair of the sovereign's on the acts evidence of the window, which is what C2a failed — and criteria 1–3 with it" read: "**What can fail in this window is criterion 6 and criterion 7**, and criteria 1–3 with them. Criterion 6 is unmet on 10 November; with one batch resolved on time each hour it passes 20 in about a day, and it fails the window if the stream misses its deadlines in the days before the promotion. Criterion 7 fails on a repair of the sovereign's inside the window, which is what C2a failed".

The rest of the clause stands as written: both criteria are the charter's condition, assessed unchanged; what criterion 6 measures is the cadence of a stream that a template of the court's schedules on datasets the sovereign operates, and it is offered as that and as nothing else; no report of this window and no later text of counsel's cites the promotion as evidence of value or of liveness; what *E* should count is his ruling at C2c-3.

**Five expiries at the opening.** A forecast resolved after its `resolves_by` is an `expiry` item of the liveness process, scored 0 (`item_process`, as C1b fixed it). V0, V2 and V3 resolve on C2a's end, and RM-3 (seq 519: "a decision of kind promote with subject C2a is on main before 2026-11-17T12:00:00Z") cannot resolve before it; V1, whose outcome has been fixed since 8 November, expires with them unless a resolver other than counsel enters it first. So the first entry after 2026-11-17T12:00:00Z brings four or five failed items. They are the process's own and the C2a report lists them.

**What does not move.** Every criterion's wording, every pin, the code on `opening-c2a-prime` (`a17864c`), the opening note, V5–V7. The gate's two reviews, by readers of two families, are of the brief at these bytes (§Precondition 3).

**Interests.** Counsel's V5 (seq 1580, 0.7) and V7 (seq 1582, 0.55) need criterion 6 met, and the false figure made them look safer than they are. Counsel-3's own N5 (seq 2556, 8 November, 0.5) priced liveness reaching 20 before the stated end at even odds; two days later counsel reported the question as closed. The error is counsel-3's, listed in row 51.
