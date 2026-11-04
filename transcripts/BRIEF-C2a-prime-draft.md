# BRIEF-C2a-prime — the second window of C2a (draft v5, 4 November 2026, counsel)

This file is `transcripts/BRIEF-C2a-prime-draft.md`. Wherever a tool reads a name the window is called `C2a-prime`, because `jack push --opens` does not admit `′`.

**How this draft came to stand here.**
- v2 answered counsel's cold read of v1. It reached `main` unread: the merge verb signed seq 1265 at 09:04:29Z, counsel withdrew #292 at 09:06:04Z, and GitHub merged it at 09:13:19Z while the verb was still waiting on checks (COUNSEL-OPEN row 34).
- v3 and v4 were never proposed. Cold reads failed them.
- v5 replaces v2, as BRIEF-C2b's drafts v1–v6 replaced one another on `main` before their reads. It follows the corrections to `transcripts/RULING-20261104-window-fix.md`:
  - correction 2: condition 2 tested on criterion 7 alone; C2a's `fix` after 2026-11-17T12:00:00Z;
  - correction 3: the rule's code lands inside the window, under the exemption stated here;
  - correction 5: the sources of C2a's two readings.

**Why there is a new window.** C2a's first window cannot now promote: criterion 7 is unmet on its acts evidence, and no later act removes a row. This brief pre-states the window that follows. A3.2 requires it: "a window that fails is a precedent, fixed by a lawful change and followed by a new pre-stated window; it is never patched in place". A4.1 permits it: "a window that fails and is followed by a new one continues the same wealth process on the same statistic under the same null".

**What the brief changes.** Of C2a's criteria, it:
- changes criterion 3's number;
- changes criterion 7's interval;
- adds §Pins to criterion 1;
- reads criterion 6 with the ruling's rule (§The exemption).

Nothing else changes, and no stream changes. The brief also names:
- the lawful change that fixes the precedent;
- the entries that record the change and the fix;
- the instant the new window opens;
- the code that lets `status.py` read it, with the one change to C1b's item process that the ruling orders.

## C2a's stated end, read two ways
The question is unruled (correction 5; `transcripts/CASES.md`).
- **Early: 2026-11-15T15:04:14Z.** BRIEF-C2a's own pre-opening "fourteen days at most" (proposed at seq 355, merged at seq 356), which BRIEF-C2a Amendment 1 (seq 368) and `status.py`'s `c2a_window` read as min(V0's `resolves_by`, opening + 14 d).
- **Late: 2026-11-17T12:00:00Z.** A5.2: "the `resolves_by` of the promotion forecast the window's brief names, entered before the window opens; a brief states no other date". `REVIEW-C1b-A5.md` F8 applied that clause to a brief's fourteen-day maximum, and counsel accepted it. BRIEF-C2a says "V0's `resolves_by` is the window's end", and V0's claim (seq 361) says the same.

This brief never needs the answer. Every act it prescribes at C2a's boundary comes after the late instant, and its tests read each instant in the direction correction 2 prescribes. In this brief, "read late" and "read early" mean those two instants. For every other window, the two readings are one instant.

## Precondition
1. **C2a's boundary has passed on both readings.**
   - It is after 2026-11-17T12:00:00Z.
   - No `decision promote C2a` has `ts` at or before that instant.
   - No `push` follows seq 367 before it.
2. **C2a's failure is witnessed as correction 2 tests it.** The attributed acts evidence `transcripts/evidence/acts-20261103T2144.csv` has been on `main` since #296, with its raw twin and `acts-20261103T2144-classifier.sha256` beside it. It holds nine rows with `repo` `renavondata/jack` and `class` `repair` inside C2a's window read early, from seq 367 at 2026-11-01T15:04:14Z to 2026-11-15T15:04:14Z. The earliest is at 2026-11-02 22:11 HKT.
3. **This brief and its two reads are on `main`.** The reads are by readers of different model families. Each is a `transcripts/REVIEW-C2a-prime-*.md` in the form `jack push --opens` reads:
   - first line `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`;
   - a `Reviewed tree:` at which this text's bytes equal `main`'s;
   - carried to `main` by a proposal signed by a non-counsel key.
4. **The ruling is on `main` with its corrections, and the sovereign has read corrections 1–4** (A2.10: "Code is written to a text Guy has read"). His reading is recorded in COUNSEL-OPEN row 35. Those four carry the rule the code implements. Correction 5 corrects a citation in correction 2 and leaves its rule and last sentence standing.
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
- From 2026-11-04T05:40Z every act of the court on jack's platform is made by a GitHub App, `renavondata-jack-court[bot]` (opencode-runner #225, #227). The first merge under it was PR #285 at 06:35:17Z.
- The herald re-runs nothing (opencode-runner #220).
- Counsel writes no closing keyword and asks the sovereign for no platform act.

The App is a capability grant (the ruling's §What this ruling does not decide). A2.6 makes a grant a `decision`, and none has been entered, so the sovereign enters `decision grant` for it at the boundary (§Order of acts step 2). `status.py` line 92 types a `decision` of a kind other than `fix` as no repair.

An act under the sovereign's login is now either his or counsel's, and counsel's carry their declaration (BRIEF-C1b Amendment 2). C2a-prime's window is the first whose record lets the criterion measure what §7 means.

**The fix** is recorded by the sovereign's `decision fix` whose `subject` begins `C2a:` (A2.6: "the fix of a failed window" is a `decision`). Under the ruling of 4 November 2026 as corrected, it is a decision and not a repair when it meets the ruling's four conditions, with condition 2 tested as correction 2 prescribes. §The code implements that rule.

## Scope
### The window
C2a-prime opens at the first `push` entry whose `ts` is after 2026-11-17T12:00:00Z, C2a's stated end read late. `status.py` reads that instant as V0's `resolves_by`, finding V0 by `args.id` `V0` with `seq` below seq 367, as `c2a_window` finds it now.

The window is (opening `ts`, V5's `resolves_by`], where V5 is counsel's forecast with `args.id` `V5` and a `seq` below the opening's. A5.2 names that date, and this brief states no other. V5's `resolves_by` is 2026-11-30T00:00:00Z, so every opening after 2026-11-17T12:00:00Z makes the window shorter than fourteen days.

The push is made by `jack push <branch> --opens C2a-prime --review <file>`. The branch is brought up to `main` after the `grant` and the `fix`, because `tools/jack` refuses a branch that does not contain `origin/main`. The push changes exactly three things:
- `judge/scope.json`'s `cap`, from 7,800 to **8,000**;
- SPEC §10's block, to match;
- one clause of SPEC §10's cap history: "8,000 at C2a-prime's opening, for the window code".

8,000 is a resource constant of the 7,800 kind (BRIEF-C2a §The cap). It enters no score, and it is fixed here, not at the push. There is no second push inside the window.

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
The code is the builder's: one branch, pre-built before the opening and proposed after the opening push, with a title beginning `C2a-prime window code`. It makes three changes to `tools/status.py`.

**Change 1, the window.** When C2a-prime's opening push is on the prefix and no `promote C2a` has `ts` at or before 2026-11-17T12:00:00Z, the C2a assessment reads C2a-prime's window:
- the opening and V5 by the rules above;
- criterion 3 against 8,000, and "unchanged since the opening" against that push;
- criterion 7's acts interval from the opening;
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
- **Names a file.** A `subject` names a file when the file's name, with or without `.csv`, occurs in it as a substring. The ruling's Order 3 paste, "(acts-20261103T2144)", names `acts-20261103T2144.csv`, which holds nine rows inside C2a's window. It also names `acts-20261103.csv`, which holds one; either suffices.
- **The commit that carries the `fix`.** The commit, among the ancestors of the commit `status.py` assesses, whose `log.jsonl` holds the `fix` entry while none of its parents' `log.jsonl` does. On `main`, that is the commit `jack decision` made.
- **A named file that holds no row.** One that does not parse as CSV with header `repo,time_hkt,class,kind,ref,note`.
- **Stated ends.**
  - C2a's: early, `c2a_window`'s end; late, V0's `resolves_by`.
  - C2a-prime's: V5's `resolves_by`, the same on both readings.
  - C1a and C1b promoted inside their windows (seqs 188 and 337), so no `fix` naming either meets condition 2.

The test is computed outside `item_process`, which receives the set of `seq`s that meet the whole rule and drops those from `repair` (`status.py` line 92). If the history or a named file cannot be read, the `fix` is typed a repair and `status.py` prints `window fix <seq>: unverified — <what is missing>`. The `fix` so typed is a late report on every prefix that holds it. Any other sovereign `decision fix` is BRIEF-C1b's repair.

**Change 3, criterion 6's "unchanged" comparison** (`c2a_tree_evidence`'s `process_at`) for C2a-prime.
- **Where it starts.** It starts from the tree at the merge of this proposal, not at the opening, because change 2 alters `item_process` and lands after the opening. That merge is the first `merge` entry after the opening whose `commit` has as an ancestor the `commit` of a `proposal` entry whose `title` begins `C2a-prime window code`. Before that merge exists, criterion 6 prints `unchanged: pending the window code's merge`.
- **What it covers.** In addition to what it covers now:
  - every top-level function of `tools/status.py` that change 2's functions reference by name, transitively;
  - every call of `item_process`, compared by `ast.dump`.

**Tests and size.** The new pins join `VALUE_PINS`, so criterion 1 requires them. There is a test for each change. A further test shows that on the real `log.jsonl`, `item_process` returns the same items with the set change 2 computes as with no set passed. Counted lines after the window code and the reviewer's pins together: at most 8,000.

### Between the `fix` and that merge
`status.py` as it then stands assesses `promote C2a` against C2a's first window, and no `promote` can pass:
- criterion 3 refuses, since HEAD's `judge/scope.json` differs from the tree at seq 367;
- criterion 6 there does not see the `fix`, which falls after that window's prefix.

`status.py` is a function of the prefix, so items finalised in the interval are recomputed by every run after the merge. The C2a-prime report prints both typings. This touches BRIEF-C1b's "no later entry, evidence string or merge changes an earlier item" for that interval alone, and correction 3 accepts it.

### The exemption
Change 2 is exempt from three refusals:
- this brief's "nothing in … `item_process` … changes" (§What continues);
- this brief's "no change to any criterion's statistic or threshold" (§Refusal list);
- BRIEF-C2a's "no change to C1's statistics".

The grounds:
- A3.2 makes C2a-prime a new pre-stated window and this brief its pre-statement. Its criteria are C2a's, read on its window, and its refusal list is C2a's, entire, but for this exemption.
- The change is inert on the record as it stands. `log.jsonl` at 41f0d6c, seqs 0–1275, holds seven `decision` entries and no `fix`: four `transmute` (seqs 3, 28, 66, 136), one `budget` (seq 50) and two `promote` (seqs 188, 337). So on every prefix before the first `fix`, the items, the stakes and the wealth are those the code yields now.
- It decides only how the boundary `fix` is typed, and A2.6 typed that on 18 October 2026, before any window opened. The code that implements it was written after (the ruling's Reasoning 2).
- A4.1's "same statistic under the same null" holds: the null p₀ = 6/11 and A4.3's stake rule do not change. What changes is that the one entry A2.6 names is read as A2.6 names it.

This is counsel's decision under correction 3 (p 0.8). If the reads find the exemption beyond this brief's power, the question goes to the sovereign before the opening.

### The acts evidence
Criterion 7 reads one attributed table, produced by the committed classifier over exactly the window. The classifier is `transcripts/evidence/guy_acts3.py` (PR #232, SHA-256 `ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b`):

`python3 transcripts/evidence/guy_acts3.py renavondata/jack . <opening ts> <exit ts> transcripts/evidence/acts-c2a2-<exit>.csv`

Counsel commits the table before the promotion, with its raw twin and its classifier hash file, and the table is named in the `decision`'s `--acts`.

The table ends at its generation instant, which is at or after the last entry before the `decision`. The C2a report re-runs the command to the `decision`'s `ts`, commits the result beside it, and prints any row between the two.

The command reads GitHub's current record: comment bodies, labels, deletions. Counsel therefore commits the raw table with the attributed one, so the evidence the promotion read stays on `main` whatever GitHub later shows.

The off-log acts between C2a's stated end and C2a-prime's opening fall inside no window's interval. The C2a report lists them.

## Order of acts, and the clock
1. **The brief and V5–V7.** This brief is merged with two reads on the record, by readers of different model families, neither returning a BLOCK. Counsel then enters V5–V7 (the ruling's Order 4, as corrected). V5's `resolves_by` is never moved.
2. **The sovereign's paste.** After 2026-11-17T12:00:00Z, with no `push` and no `promote C2a` since seq 367, the sovereign makes one paste:

   ```
   jack decision grant "GitHub App renavondata-jack-court[bot]: the court's platform acts on renavondata/jack (opencode-runner #227), in force since 2026-11-04T05:40Z"
   jack decision fix "C2a: criterion 7 unmet at the stated end — nine off-log repair rows (acts-20261103T2144); the court's platform acts moved to a GitHub App (opencode-runner #227)"
   ```

   The `fix` is the ruling's Order 3 paste, word for word. Then the push branch is brought up to `main`, and the opening `push` follows (`jack push <branch> --opens C2a-prime --review <file>`, cap 8,000). Counsel writes the exact commands into the opening note before that day.
3. **The window code.** The builder proposes it (title beginning `C2a-prime window code`), the herald merges it, and the `tests` run on `main` verifies it.
4. **The promotion.** `status.py` prints the window line, the value line, the liveness line and `promote C2a: lawful | refused: …`. Counsel commits the acts evidence. When the line reads `lawful`, the sovereign enters `decision promote C2a --acts <file>` (A5: at the crossing).
5. **C2b.** BRIEF-C2b's order of acts then begins at its step 3. Its `decision promote C2a` is the entry of step 4 above and is not entered again.

## Pre-stated criteria for C2a-prime, evaluated on the exit prefix
C2a's seven, read on C2a-prime's window:
1. Every pin of BRIEF-C2a's list and of §Pins below is KILLED, with a passing twin, in the `tests` run on `main` at the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines are within 8,000 and the kernel within 500. `judge/scope.json` and SPEC §10's block are unchanged since C2a-prime's opening push.
4. The attack tests are green on `main` before the first scored event's cutoff (unchanged: 2026-11-01T15:59:44Z).
5. **Value**: *E*ᵥ ≥ 20 on the one ledger, by `tools/value.py`, wealth continued.
6. **Liveness continued**: C1b's process, with the ruling's rule, at or above 20 on the exit prefix, wealth continued.
7. No `decision` of kind `veto` naming C2a-prime; **off-log repairs 0 on the acts evidence of C2a-prime's window**; A3.4 at or under 5 : 1.

This brief states no minimum length for the window. A5 makes a window a maximum, and a minimum would be a constant chosen by hand (BRIEF-C2a's refusal list; the withdrawn Amendment 4, COUNSEL-OPEN row 33). If every criterion holds an hour after the opening, the window closes in an hour, and the record says so.

## Pins (the reviewer's), each with its named mutant and passing twin
- **`second_window_from_the_end`**
  - Requires: the opening is the first push after V0's `resolves_by`.
  - Mutants: the first push after seq 337, which is C2a's own (seq 367); the first push after `c2a_window`'s end.
- **`second_window_end_is_v5`**
  - Requires: the end is V5's `resolves_by`.
  - Mutants: V0's `resolves_by`; a V5 with `seq` above the opening accepted.
- **`second_window_cap`**
  - Requires: criterion 3 reads the cap the opening push set, and refuses a prefix whose tree changes it after the opening.
  - Mutants: 7,800 hard-coded, which refuses every prefix; the cap read at HEAD only, which accepts a later change.
- **`offlog_from_second_opening`**
  - Requires: criterion 7 counts rows from C2a-prime's opening.
  - Mutant: from C2a's opening, which counts the nine.
- **`promote_refused_before_end`**
  - Requires: a `promote C2a` at a prefix before C2a-prime's opening is assessed against the first window, prints no `window: C2a-prime` line, and is refused on criterion 7.
  - Mutant: assessed against C2a-prime whenever a V5 exists.
- **`window_fix_is_decision`**
  - Fixture:
    - a synthetic log on which W is C2a (an opening push above seq 337; V0 later than opening + 14 d, so its two readings differ);
    - one item finalised before the `fix`, and one writ open at its `ts`;
    - a temporary git repository holding W's attributed acts file (one `repair` row inside W read early), its raw twin and its classifier hash file, committed before the commit that carries the `fix`;
    - no `promote` naming W by its end read late;
    - then a `fix` whose `subject` begins `C2a:` and names the file, entered after the late end and before the next `push`, and the first `fix` naming W.
  - Requires: the `fix` taints neither the open writ nor the finalised item, and is no late report.
  - Mutants:
    - the `fix` typed a repair;
    - condition 2 read as "ended without promotion";
    - (a) read early;
    - (b1) or the (b2) interval read late;
    - condition 3 read early;
    - the carrying commit taken as the assessed head;
    - the attributed requirement dropped.
  - Twins. Each is still a repair, taints the open writ and is a late report:
    - a free-text `subject`;
    - a `subject` naming no attributed file;
    - the file committed only after the carrying commit;
    - a `subject` naming only the raw twin (`…-raw`), whose row lies inside W while the attributed file has none;
    - the only `repair` row outside W, or in a minute that ends after W's early end;
    - a `promote` naming W between the two readings;
    - a `veto` naming W only between the two readings, with no file;
    - a `fix` entered between the two readings;
    - a `fix` entered after the next `push`;
    - a second `fix` naming W;
    - the history unreadable, which also prints the `unverified` line.
  - Further twin: a `veto` naming W at or before its early end, with no file, makes the `fix` a decision.
- **`process_unchanged_from_window_code`**
  - Requires: criterion 6's comparison starts at the window code's merge and covers change 2's functions, the functions they reference, and every call of `item_process`.
  - Mutants: the comparison started at the opening push, which refuses every prefix; change 2's functions omitted from the comparison; the set widened at the call site. The last two must each read `unchanged False`.
- **`wealth_continues`** (C2a's, unchanged).

## Refusal list
C2a's, entire, but for §The exemption, plus:
- no change to any criterion's statistic or threshold;
- no re-attribution of any row of C2a's acts evidence;
- no minimum window length;
- no second push inside the window;
- no code but §The code;
- no `decision fix` naming C2a recommended or prepared for entry before 2026-11-17T12:00:00Z;
- **counsel's platform acts on `renavondata/jack` in the window are `jack` verbs and declared closes of its own stale proposals, nothing else**: no labels, no edits, no closing keywords, no reviews, no re-runs.

## Stop and report if
- **The window code and the pins do not fit under 8,000.** Report the shortfall.
- **The two checkers disagree.**
- **A `repair` row appears in C2a-prime's acts evidence.** The window has failed. The report names the row and its hand, and the next window is pre-stated by the same procedure.
- **V5's `resolves_by` passes with a criterion unmet, or with no opening push.** If C2a-prime fails on criteria 1–6 or on A3.4 alone, with no `repair` row and no veto, no `fix` names it until the sovereign has answered whether it failed (correction 2).
- **A `decision fix` naming C2a meets condition 1 but not the rest.** For example: entered at or before 2026-11-17T12:00:00Z, entered after the opening push, or naming no attributed acts file. It is a repair permanently (condition 4), and a late report that refuses criterion 6 at every later prefix. Stop; the question goes to the sovereign before any other act.
- **A `push` lands between 2026-11-15T15:04:14Z and 2026-11-17T12:00:00Z.** On the late reading it is a second push inside C2a's window. Stop and report before any other act.
- **A `push` after 2026-11-17T12:00:00Z precedes V5 or the `decision fix`, or does not set the cap to 8,000.** It opens a window with no end, no recorded fix or no room. Stop; the next window is pre-stated afresh by the same procedure.
- **The reads find §The exemption beyond this brief's power.** The question goes to the sovereign before the opening.

## Deliverables
- this brief and its reads;
- V5–V7;
- the opening note with the exact commands of §Order of acts step 2;
- the window code and its tests;
- the pins;
- the acts evidence of C2a-prime's window, raw and attributed, with its classifier hash file;
- the C2a report, with:
  - a section on the first window's failure:
    - the nine rows as precedent;
    - the lawful change and its `grant`;
    - C2a's stated end, read two ways and unruled;
    - the off-log acts between C2a's end and C2a-prime's opening;
    - the sovereign's acts outside jack on 4 November: three runner merges and a runner label, as off-log repairs the instrument cannot see, and the App as a capability grant;
  - a section on C2a-prime's exit: its length, its acts count, and the boundary `fix`'s typing before and after the window code;
- LAW.md's count of the sovereign's cap-change pushes (seqs 197 and 367) brought up to date.

The first window's acts evidence has been on `main` since #296: `acts-20261103T2144` raw and attributed, its classifier hash, and `runs-tests-20261103T2144.json`.

## Counsel's forecasts on this window (entered after the reads, before the opening push)
| id | claim | p |
|---|---|---|
| V5 | the promotion forecast: every criterion of C2a-prime holds on the exit prefix by this forecast's `resolves_by`, 2026-11-30T00:00:00Z | 0.7 |
| V6 | the acts evidence of C2a-prime's window holds zero rows of class `repair` | 0.75 |
| V7 | `decision promote C2a` is entered within 48 hours of C2a-prime's opening push | 0.55 |

V0–V3 are not edited, and each resolves on its own words.
- **V0, V2 and V3.** They speak of C2a's exit prefix or window end. On the late reading, that instant is their own `resolves_by`, 2026-11-17T12:00:00Z. V0's outcome is fixed on either reading, but when it may be resolved is not. This brief recommends no resolution of any of the three before that instant, and counsel takes the expiry each then risks. That interest is disclosed in the corrections to the ruling.
- **V1** ("within 7 days of the opening push") does not depend on the reading.

Counsel's forecasts on C2b likewise resolve on their own words (BRIEF-C2b Amendment 2).
