# Cold read of AMEND-A6, draft 4, by argon (opencode-runner #1202)

The final report of runner #1202 (`google/gemini-4-argon`, read only, no key), as its last comment gives it, from its first heading to its verdict. The text read is `transcripts/AMEND-A6.md` at `3b141dae6e7657fd1f177db835653291ef324eae`, whose bytes this proposal puts on `main`.

### Answers to the Twelve Questions

1. **Decidability and definition of terms in Clause 1 (`transcripts/AMEND-A6.md:14-19`).**
   Clause 1 is decidable from `log.jsonl` alone, and each of its terms is defined by a text in force:
   - *"by the sovereign"*: a `decision` entry signed by a key declared in `genesis` (`SPEC.md:412-413`, §10.14; `tools/status.py:28-29`, `sovereign_keys`).
   - *"names it, as A5.1's naming is read for that window"*: `CHARTER.md:377-378` (A5.1) requires a `decision` whose `subject` names the window; `transcripts/BRIEF-C2a-prime-draft.md:102-106` (§The subject) and `:148` (§The code) define that naming for `C2a`, `C2a-prime`, and every other window (`tools/status.py:286-298`, `names_window`). For `C2a-prime`, a `decision veto` with subject `C2a` or `C2a-prime` names `C2a-prime` iff its `ts` is after `C2a-prime`'s opening (`2026-11-17T12:50:50Z`, seq 5564) and no `promote C2a` has `ts <= 2026-11-17T12:00:00Z`.
   - *"at or above this amendment's `activate_at`"*: `SPEC.md:97` (§5) and `:215-220` (§7) define an `amend` entry's integer `activate_at` as the `seq` from which the amendment is in force (`e["seq"] >= activate_at`).
   - *"as failed (§6, A3.2)"*: places the ended window in the failed-window category of `CHARTER.md:102` (§6), `:316-317` (A3.2), `:342-344` (A4.1) and `:380-381` (A5.1).

   Two readers applying Clause 1 to the same log cannot disagree about when a window ended: a window ends at the earliest of its stated end, a lawful `decision promote` naming it, and the first sovereign `decision veto` inside the window naming it with `seq >= activate_at`.

2. **Ranking against texts in force (`transcripts/AMEND-A6.md:4-5, 14-19, 44-45`).**
   The text ranks itself accurately against every text in force:
   - It explicitly overrides `CHARTER.md:102` (`§6 ("Windows … are committed before the window opens", as to a window's end)`), `CHARTER.md:376-381` (`A5.1`), and any brief where they conflict (`transcripts/BRIEF-C2a-prime-draft.md:83, 97, 309, 319`).
   - It leaves untouched and invokes the second sentence of `§6`, `A3.2` (`CHARTER.md:316-317`), `A4.1` (`CHARTER.md:342-344`), and `A5.2` (`CHARTER.md:382-384`), explicitly keeping a window's stated end and its promotion forecast's `resolves_by` unmoved (`transcripts/AMEND-A6.md:16-19`).
   - It leaves the three rulings untouched: `transcripts/RULING-20261104-window-fix.md` (whose conditions 2 and 3 stay keyed to the stated end, line 18), `transcripts/RULING-20261117-constitution.md` (under whose H3 a ruling yields to the charter), and `transcripts/RULING-20261120-promotion-judge.md` (whose answers 5, 12 and 17 and points 10–12 it implements). There is no text in force with which it conflicts that it neither overrides nor leaves untouched by its own words.

3. **The boundary `fix` and promotability of C2a-prime's successor (`transcripts/AMEND-A6.md:16-19`).**
   Under `transcripts/RULING-20261104-window-fix.md:49-57, 167-176` (conditions 2 and 3, as corrected by correction 2) and `transcripts/BRIEF-C2a-prime-draft.md:128-135` (change 2, implemented in `tools/status.py:371-402`, `window_fixes`), a sovereign `decision fix` naming a window ended by a veto under A6 is typed a **decision** (not a repair, and never a late report) when entered **after the window's stated end** (`ts > w_late`, for `C2a-prime` `2026-11-30T00:00:00Z`) and **before the first `push` after that stated end** (`e["seq"] < next_push["seq"]`, where `tools/status.py:387` defines `next_push` by `instant(p["ts"]) > instant(w_late)`).
   - Because condition 2(b1) requires a `decision veto` naming the window with `ts <= w_early`, both seq 5879 and the fresh veto at or above `activate_at` satisfy `veto_ok` (`tools/status.py:392`).
   - Because the move's `push` lands *before* `2026-11-30T00:00:00Z` (`w_late`), it is not `next_push` (`instant(p["ts"]) > instant(w_late)` is false) and in `item_process` (`tools/status.py:111-112`) a `push` is never a repair.
   - By keeping the boundary `fix` keyed to the stated end rather than moving condition 3 to the early-end veto, Clause 1 prevents the boundary `fix` from becoming a permanent repair or late report and does not make `C2a-prime`'s successor (`C2a-3`) unpromotable.

4. **Forward-only binding and reading of seq 5879 and V6 (`transcripts/AMEND-A6.md:3-4, 14-16, 23-24, 52-54`).**
   - The text is strictly forward-only (`CHARTER.md:42, 51, 283-285`, §2 maxim 2, §3, A2.7): Clause 1 applies only to a `decision veto` whose `seq` is at or above A6's `activate_at`.
   - It neither binds nor rereads seq 5879 (`2026-11-18T12:01:17Z`), which was entered before A6, still refuses `C2a-prime`'s criterion 7, and ends nothing (`transcripts/AMEND-A6.md:8-9, 23-24`).
   - It neither edits nor re-judges the validity of `V6` (`log.jsonl` seq 1581, `"V6: the acts evidence of C2a-prime's window (BRIEF-C2a-prime v7 §The acts evidence) holds zero rows of class repair"`, `p: 750`). Its reading of `V6` (`transcripts/AMEND-A6.md:53-54`) is sound: under `transcripts/BRIEF-C2a-prime-draft.md:186-188`, the acts evidence is collected `"over exactly the window"` (`<opening ts> <end ts>`), so ending `C2a-prime` early by a fresh veto after A6's activation shortens the interval over which `repair` rows are counted and benefits `V6`. `V5` (seq 1580) and `V7` (seq 1582) are already decidable 0 (by seq 5879 and by the passing of 48 hours after seq 5564 without a `promote`).

5. **Witnesses (`transcripts/AMEND-A6.md:20-24, 46-48`).**
   The witnesses satisfy `CHARTER.md:42` (§2, maxim 2):
   - *Violating witness*: a `push` entered after a qualifying veto (at or above `activate_at`) and before the window's stated end, read as a push inside the window (corresponding to the mutant of `vetoed_window_continues`, in which a veto at or above the height is ignored as an end).
   - *Satisfying witness*: `C2a-prime` vetoed again at or above A6's `activate_at`, followed by the move's `push` before `2026-11-30T00:00:00Z`, which opens nothing and falls outside the ended window (together with the boundary twin at seq 5879, where a veto below `activate_at` ends nothing).

6. **Completeness and truth of the Interests list (`transcripts/AMEND-A6.md:50-62`).**
   Inspection of all 26 unresolved forecasts with `proposer == "counsel"` on `log.jsonl` (through seq 7049) confirms that the list of 14 forecasts (`V5` seq 1580, `V6` seq 1581, `V7` seq 1582; `X2` seq 638, `X3` seq 639, `X6` seq 815, `X7` seq 1559, `N2` seq 2553, `N11` seq 2562; `N3` seq 2554; `N7` seq 2558, `N8` seq 2559; `N10` seq 2561; `L4` seq 184) is complete and accurate in every sequence number, probability and quotation. None of counsel's other 12 open forecasts (seqs 42, 53, 54, 55, 60, 124, 182, 2555, 2557, 2560, 2994, 2995) turns on a window's end, exit prefix, post-C2a timing, or A5.

7. **Completeness of stated departures (`transcripts/AMEND-A6.md:28-42`).**
   The departures are stated in terms and complete:
   - (a) Principle 5 of 5 November (`transcripts/A6-CASE-20261105.md:31, 48`) and `transcripts/COUNSEL-OPEN.md` row 39 (the `failed: criterion k cannot hold` clause stays a C2c item under another id);
   - (b) `transcripts/COUNSEL-OPEN.md` row 28 (line 37: no charter amendment whose rule has not lived in a brief and refused or decided an act);
   - (c) `transcripts/COUNSEL-OPEN.md` row 33 (line 42) and row 69 (line 78), enumerating every part of row 33's procedure (the pin following with code rather than preceding; readers named by counsel rather than elected by record; open forecasts on reached windows neither frozen nor forfeited; the forecast that can lose; the §12 count stated without a pre-stated budget) and row 33's unmet undertaking (`"the amendment procedure as a brief item with its pins, before any A6"`), and citing `transcripts/RULING-20261120-promotion-judge.md:237` (point 12);
   - (d) `RUNBOOK.md:217-220` (mechanisms reaching `main` before `amend`, with A2 as precedent).
   There is no unstated departure from any other text in force.

8. **Single rule vs. bundling (`transcripts/AMEND-A6.md:14-19`).**
   Clause 1 states one rule: a window also ends, as failed, at a sovereign `decision veto` naming it at or above `activate_at`. Its second sentence (`"Nothing else about the window changes..."`) adds no second rule; it bounds the single rule so that the window's stated end and acts keyed to the stated end are not disturbed.

9. **Whether the forecast can lose and when it is decidable (`transcripts/AMEND-A6.md:63-66`).**
   - At `p = 0.7` (700 per mille), the forecast is not an even-odds `p = 0.5` hedge: outcome 0 scores a log-loss of $-\ln(0.3) \approx 1.2040$ against $-\ln(0.7) \approx 0.3567$ on outcome 1, and it loses if the order stops (including if the sovereign answers that row 33 applies), if no fresh veto is entered at or above `activate_at`, or if the move's push does not land on `main` before `2026-11-30T00:00:00Z`.
   - Nothing about the forecast is decidable only at its own `resolves_by` (`2026-12-01T12:00:00Z`): the claim's cutoff is `2026-11-30T00:00:00Z`, 36 hours before `resolves_by`, so both outcome 1 (at the move's push) and outcome 0 (at `2026-11-30T00:00:00Z`) are decidable at least 36 hours before the resolution deadline.

10. **Lawfulness and completeness of the order of acts (`transcripts/AMEND-A6.md:67-77`).**
    The order is lawful and complete:
    - Two passing cold reads from two non-counsel families (each `VERDICT: PASS` with no BLOCK and no FIX) → the sovereign's read entry naming `AMEND-A6.md`'s SHA-256 and stating in terms that row 33's procedure does not apply → counsel's forecast → `decision transmute A6` (`SPEC.md:408-411`, §10.13) → `amend A6` with default `activate_at = seq + 1` (`tools/jack:295`; `SPEC.md:219-220`) → `decision veto C2a-prime` (at `seq >= activate_at`, ending `C2a-prime` under Clause 1) → counsel's redraft of `transcripts/BRIEF-C2a-3-draft.md:62` (precondition 1) → the move's `push` (already granted at seq 6851).
    - Because `amend A6` uses default `activate_at = seq + 1` and the next acts are `decision veto C2a-prime` and then the move's `push`, no `push` has `amend.seq < push.seq < activate_at` (`SPEC.md:405-407`, §10.12; `judge/judge.py:262-263`).
    - Because `decision veto C2a-prime` at `seq >= activate_at` ends `C2a-prime` before the move's `push`, the move's `push` does not fall inside `C2a-prime`'s window (`transcripts/RULING-20261120-promotion-judge.md:181, 256`, H2 and Order 4).

11. **Effects claimed for `decision` entries (`transcripts/RULING-20261117-constitution.md:47`, H1).**
    Nothing in the text claims an effect for any `decision` entry that the law in force does not give its kind. `transmute` unlocks `amend A6` under `SPEC.md:269, 408`; `veto` at or above `activate_at` ends a window because A6 itself is a charter amendment in force at that `seq`; and the entry recording the sovereign's read of `AMEND-A6.md` and his answer on row 33 is his signed statement of a fact and of a choice within his powers (H1: `"evidence of a fact, or of a choice he makes within powers he otherwise has"`).

12. **Anything else that should stop the sovereign reading it; and whether #1200's finding is answered.**
    Nothing should stop the sovereign reading `3b141dae:transcripts/AMEND-A6.md` as it stands.
    **#1200's finding is answered:** in draft 3 (`80a97ebb`), line 41 claimed that `"his read of this text answers"` whether row 33 applies, while line 70 required only `"an entry naming its SHA-256"`. In draft 4 (`3b141dae`), line 41 reads `"The entry that states his read of this text states his answer in terms"`, and lines 69–71 require `"his read of this text, stated by an entry naming its SHA-256 and saying in terms whether row 33's procedure applies to it, the order going on only if it says that it does not"`.

---

### Findings

1. **[NOTE]** `transcripts/AMEND-A6.md:41, 69-71` — Draft 4 resolves #1200's FIX on draft 3 by requiring the sovereign's read entry both to name the text's SHA-256 and to state in terms whether row 33's procedure applies, gating the rest of the order on a negative answer.
   > `transcripts/AMEND-A6.md:40-41`: "Whether row 33 applies to this amendment the ruling of 20 November leaves to him (its point 12). The entry that states his read of this text states his answer in terms."
   > `transcripts/AMEND-A6.md:69-71`: "his read of this text, stated by an entry naming its SHA-256 and saying in terms whether row 33's procedure applies to it, the order going on only if it says that it does not;"
   > `transcripts/RULING-20261120-promotion-judge.md:237`: "Answers 12 and 17 bring the early-end amendment forward to now. They do not say whether row 33's procedure still applies to it. That is not decided here; it is for the amendment's own text and for him."

2. **[NOTE]** `transcripts/AMEND-A6.md:73-76` — The order require counsel to redraft `transcripts/BRIEF-C2a-3-draft.md` v4 line 62 (`"no \`push\` follows seq 5564 before it"`) before the move's push; `BRIEF-C2a-3-draft.md` v4 also has `"no change inside it"` at line 7 and a stop condition `"A \`push\` lands between 2026-11-17T12:50:50Z and 2026-11-30T00:00:00Z. It is a second push inside C2a-prime's window"` at line 288, which the redraft of `BRIEF-C2a-3-draft.md` will naturally align when that draft brief is updated for his read. Because `BRIEF-C2a-3-draft.md` is an unread draft (`BRIEF-C2a-3-draft.md:3`), this does not affect `AMEND-A6.md`.
   > `transcripts/AMEND-A6.md:73-77`: "Before that push, counsel redrafts C2a-3's draft brief, whose precondition 1 has \"no `push` follows seq 5564 before it\" (`transcripts/BRIEF-C2a-3-draft.md` v4, line 62), so that a push after such a veto, which opens nothing, does not bar C2a-3 and is not its opening (the ruling of 20 November, point 7). That brief is a draft and binds nothing until he reads it (A2.10)."
   > `transcripts/BRIEF-C2a-3-draft.md:3`: "It is a draft: no read has passed it, nothing in it is proposed, and no builder session is filed on it before the sovereign has read it (A2.10: \"Code is written to a text Guy has read\")."

VERDICT: PASS
