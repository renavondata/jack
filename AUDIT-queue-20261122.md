# Audit of QUEUE.md and queue_check.py at `bc689d4` (22 November 2026): VERDICT: FAIL

- **Who.** A fresh session of the adviser's own family (`claude-fable-5-2`), started by the adviser with a fixed list of defect classes A to F and no account of how the files were built. It worked on copies under `/tmp/audit-queue` in the adviser's workspace and changed nothing on the branch. Its report follows the adviser's reproduction, verbatim.
- **Standing.** Evidence, not a ruling. It binds nothing.

## The adviser's own reproduction of the four BLOCKs (09:39Z)

Run against `queue_check.py` at `bc689d4`, with made-up entry lists for the step tests and edited copies for the frozen-text tests.

| Finding | Input | The checker said | True |
|---|---|---|---|
| 1 | A6, no fresh veto, then his fix and a push after 2026-11-30T00:00:00Z | head Q2 | C2a-3 is open (head Q5) |
| 1 | A6, fresh veto, no move's push, then fix and opening push | head Q3 | C2a-3 is open (head Q5) |
| 2 | the page with its budget edited to 400/200/700 and a line `REVIEW <instant> sha256 <new hash>` appended under Later | "page unchanged", exit 0 | the page changed with no word of his |
| 3 | a line "*Exception (added):* part (b) is waived." added under row B1 | "predicate unchanged", exit 0 | the predicate changed |
| 4 | every step passed, `judge/status.py` then absent from `main` | head Q3 | the queue is finished |

Two more, reproduced:
- **Finding 7 and 23.** With the head's start set one day earlier, the real record gives `drafts 25/4, cold reads 14/2` and STOP.
- **Finding 15.** `transcripts/AMEND-A6.md` on `main` has "Before that push, counsel redrafts C2a-3's draft brief". That is work for Q4 ordered before Q3, which rule 1 forbids while the head is Q1.

## The audit's report, verbatim

VERDICT: FAIL (4 BLOCK, 16 FIX, 10 NOTE)

All tests ran on copies under /tmp/audit-queue; nothing under /home/claude/work/adviser-wt or /home/claude/repos/jack was edited (only the allowed fetches). The page's own run from /home/claude/repos/jack at 09:21Z gave HEAD Q1, drafts 0/4, cold reads 0/2, days 0/7, all three frozen texts unchanged, overrides 1, exit 0.

Reproduction shorthand:
- STEPS = `python3 -I /tmp/audit-queue/t/steps.py` (T1 to T17) and `.../t/extra.py` (T18 to T20). They import the copy and call the functions in STEPS on hand-built entries.
- REAL = `cd /tmp/audit-queue/jc && python3 -I /tmp/audit-queue/queue_check.py --no-fetch --now 2026-11-22T10:00:00Z` plus the option shown (jc is a copy of the jack clone).
- SYN = scratch origin and clones under /tmp/audit-queue/syn (synthetic log from mklog.py, real page, checker and predicate).
- "v5" = d3ea009c:transcripts/BRIEF-C2a-3-draft.md.

2. FINDINGS

1. A, BLOCK. queue_check.py:43-55; QUEUE.md:27-29. The queue hard-codes one lawful path: a fresh veto and the move's push, both before 2026-11-30T00:00:00Z. Neither Q2 nor Q3 has a bound at the stated end, and v5 requires neither (Precondition 1: C2a-prime ends at "the earlier of that instant and a `decision veto`"; §The window: C2a-3 "opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z").
   - T5: A6, no fresh veto, then fix and opening push on 30 Nov. Expected C2a-3 open (head Q5); actual head Q2.
   - T5b: the same, then `promote C2a` and C2b's push. Expected head Q7; actual head Q2.
   - T6: veto, move not pushed before 30 Nov, fix and opening push. Expected head Q5; actual head Q3.
   - T6b: the same, C2a promoted, the move arrives with C2b's push. Actual head Q4, with Q3 credited to C2a-3's opening push (seq 7901).
   - T7 and T16: a veto or a first push after 30 Nov. The push that opens C2a-3 is taken as Q3, and Q4 can then never pass.
   - T18: a later `veto C2a`, which v5 says names C2a-3, passes Q2 as "C2a-prime is ended".
   - Rule 5 then lapses the page on 7 Dec; from 30 Nov until then the head shown is wrong. AMEND-A6's own forecast gives p 0.7 that the move lands before 30 Nov.

2. B, BLOCK. queue_check.py:92-97,103. "page unchanged" and "adopted" mean only that the last hash-bearing line anywhere below the first "\n## Words" names the current hash. Such a line is unsigned, may sit under "## Later", may be a second ADOPTED, and needs no words. REVIEW lines are neither counted nor printed, and no hash is printed.
   - REAL `--page ../page_forge_later.md` (rule 1 reworded, budget 400/200/700, and `REVIEW 2026-11-23T03:00:00Z sha256 <new hash>` appended at the end of Later). Expected page CHANGED; actual "page unchanged", "adopted 2026-11-22T09:06:41Z", overrides 1, exit 0.
   - `page_adopt2.md` (a second ADOPTED line): the same result.
   - `page_unadopt.md` (ADOPTED line deleted, same edits): "NOT ADOPTED" but "page unchanged", exit 0.
   - `page_under_words.md` ("Rule 6: a session may skip any cold read…" placed under the Words heading): unchanged.
   - `page_no_override.md` (OVERRIDE line deleted): overrides 0, no flag.
   - `page_bare_override.md` (two bare `OVERRIDE <instant>` lines): overrides 3.
   - Append-only is stated at QUEUE.md:40,48 and not checked.

3. B, BLOCK. queue_check.py:100. The predicate hash covers only physical lines matching `- \*\*B\d `, split by `str.splitlines()`. Text appended to a row is not hashed.
   - REAL `--predicate ../pred_cont.md` (an indented line after B1: "*Exception (added):* part (b) is waived…"). Expected CHANGED; actual "predicate unchanged", exit 0.
   - `pred_ls.md` (U+2028 plus text appended to B3) and `pred_ff.md` (form feed plus text appended to B0): unchanged.
   - `pred_pre2.md` ("Rows B4 to B7 are waived for the bootstrap window." inserted before the promotion-claim sentence): unchanged. That sentence is outside rule 2's "eight rows", so this one is a gap in the page's definition.

4. A, BLOCK (latent). queue_check.py:47-49. Q3 tests today's tree (`git cat-file -e origin/main:judge/status.py`), not the tree at the push. Ruling of 20 November answer 4: "Move as is, then shrink".
   - T13: all 13 steps passed, then the file absent. Expected END; actual head Q3.
   - SYN (h4): the same on a scratch repo printed "HEAD Q3 … days 27/7 … LAPSED: … its test of 6 December has passed", exit 4.
   - T14: a push that is not the move (7150), then the move (7200). Q3 is credited to 7150.

5. A, FIX. queue_check.py:52-55. Q4 passes on logs where the record puts the opening elsewhere.
   - T8/T8b: push P1 after 30 Nov, then fix, then push P2. Checker: Q4 not done until P2, then done at P2. Record: C2a-3 opened at P1 (v5 §The window); a fix at or after that push is not the window's fix (origin/main:tools/status.py:387-388); P2 is a second push inside the window.
   - T9: a fix "C2a-prime: early" on 26 Nov, then a second after the end. Checker accepts the second; status.py:379-382 lets an earlier fix with the same prefix disqualify it. Not run against status.py (it needs signed entries): read from the code.
   - These logs break v5's order of acts, though the kernel admits them.

6. B, FIX. queue_check.py:100; QUEUE.md:12,50. Adding rows without touching B0 to B7 reports a change. REAL `--predicate ../pred_b8.md` (one new `- **B8 …` row): "predicate CHANGED", STOP, exit 2. A `- **B10 …` row is ignored (unchanged). It fails safe, but it will fire when his "Add B8 and B9" lands, and rule 2 defines the predicate as eight rows.

7. C, FIX. queue_check.py:123-124. Drafts include every non-merge commit reachable from a counsel/ or agent/ ref, so main's own commits count once a branch is cut from or merged with newer main.
   - SYN (d): one own draft, branch merged up to a main holding three stream reports. Expected 1; actual "drafts 4/4".
   - Real record with the ADOPTED instant set one day earlier (`--page ../page_adopt_early.md`): drafts 25/4, of which 10 are commits on origin/main, 8 of those `REVIEWER-FRESHNESS-*` stream reports. QUEUE.md:36 puts the streams "beside the queue".
   - The fix is `--not origin/main`.

8. C, FIX. queue_check.py:123. `--since` reads committer date and stops walking at an older commit. SYN (b): three drafts dated 22 Nov 10:00 to 12:00Z under one commit with committer date 2026-11-01. Expected 3 or 4; actual "drafts 0/4". `--since-as-filter` gives 3; by author date 4.

9. C, FIX. queue_check.py:85-86,123. Rebases recount and deleted branches persist.
   - SYN (e): two drafts committed 20 Nov, rebased 23 Nov with no new text: the count went from 0 to 5 (the two rebased copies plus three of main's reports).
   - SYN (f): after the branch was deleted on origin, the old clone still said 5/4 and a fresh clone 0/4. The fetch has no `--prune`.

10. C, FIX. queue_check.py:132 (`v > budget[n]`). STOP comes one past the budget.
    - SYN (a): "drafts 4/4", no STOP, exit 0; a fifth draft gives STOP, exit 3.
    - `--now 2026-11-30T09:06:40Z` (7 d 23 h 59 m): "days 7/7", no days STOP; one second later "days 8/7".
    - Rule 3 says "When a number is spent".

11. C, FIX. queue_check.py:121. Q4's 30 Nov floor is applied to drafts and reads as well as days. Rule 3 gives that floor to days only (QUEUE.md:14-16). SYN (g): Q3 passed 25 Nov, three drafts on 26 to 28 Nov; `--now 2026-11-29T12:00:00Z` and `--now 2026-12-06T23:59:59Z` both show "since 2026-11-30T00:00:00Z: drafts 0/4". Those drafts are charged to no head.

12. C, FIX. queue_check.py:123-124. The pathspec is wider than the page's words. SYN (c): one commit each on transcripts/sessions/x.md, transcripts/sub/REVIEW-x.md, transcripts/REPLY-REVIEW-x.md, transcripts/REVIEWER-FRESHNESS-1.md, transcripts/REVIEW-x.md, and a pure deletion gave "drafts 5/4"; only the top-level REVIEW- file was excluded. `transcripts/*.md` matches subdirectories (main has 30 such files), and the exclusion is top-level only.

13. C, FIX. queue_check.py:127-131,145. If `gh` fails, reads are "not counted" and the exit can still be 0. SYN (l2), bad token: "cold reads not counted (no gh access to the runner)". A budget that cannot be read exits as fine.

14. D, FIX. QUEUE.md:11,27-29. "The record's own order (CHARTER §8; … §3.2)" does not hold for Q1 to Q4. Neither cited text contains them; they come from AMEND-A6 §3 "Order" and the ruling of 20 November, answers 5, 12 and 17. Q2 and Q3 are one chosen route, not a required order (finding 1).

15. D, FIX. QUEUE.md:54. The Later line says rule 1's conflict "first bites at Q5". It bites now, at Q1 (this corrects the claim; it does not re-argue the conflict):
    - AMEND-A6 "Order": "Before that push, counsel redrafts C2a-3's draft brief" (Q4 work before Q3).
    - v5 Order of acts step 1 (brief merged with two reads, his read, cap, patch, build, pins, V8) must precede the paste of 30 Nov.
    - BRIEF-C2b step 3 puts `promote C2a` and C2b's opening push in one paste.
    - Dated obligations are off the head too: COUNSEL-DUE row `c2b-report` is due 2026-12-02T12:00:00Z. The preamble's saving sentence names only "a read, a grant or a wait".

16. E, FIX. QUEUE.md:17-18 against tools/jack:177-221 (the push read gate), AMEND-A6 "Order" ("a read that fails stops the order until a revised text passes a new read of the same family") and v5 Precondition 3. "Ship with the known defects listed" and "A read can inform that, and never decides it" can be read as leave to go on past a failed read the law makes decisive. A budget of 2 cold reads equals the legal minimum for A6 and for the v5 brief, so one failed read forces a STOP whose two options both omit the required re-read. The real record took 5 reads over 4 drafts for A6 alone.

17. E, FIX. QUEUE.md:40,44,48; queue_check.py:97.
    - Who appends under Later and who records his words is unstated; the checker accepts any line. ADVISER.md rule 10 on the same branch says no entry there carries his authority.
    - The one OVERRIDE records his "Maybe one cold read too?" (a question) as an override of rule 1 through the adviser's parenthesis.
    - An override without a hash names no rule, scope or expiry; "his overrides: 1" will stand for every later session.
    - "The session at work stops" is undefined with several sessions and scheduled streams.
    - "Cut the step down" can be read as leave to change a frozen step.

18. F, FIX. queue_check.py:136-145. Exit precedence hides conditions.
    - SYN (h1): lapse plus predicate CHANGED gives exit 4.
    - SYN (h3): queue finished plus CHANGED prints STOP and "LAPSED: the last step has passed", exit 0.
    - SYN (h2): CHANGED plus drafts 5/4 gives exit 2, and the spent line is not printed.

19. F, FIX. queue_check.py:142; QUEUE.md:20. The lapse is not sticky. SYN: q4 log at `--now 2026-12-07T00:00:00Z` gives LAPSED, exit 4; with Q4 passing on 8 Dec, `--now 2026-12-09T00:00:00Z` gives no LAPSED, exit 0. Rule 5 says the page lapsed if Q1 to Q4 had not passed "by then".

20. F, FIX. QUEUE.md:6; queue_check.py:102. The run command executes whatever the tip of adviser/notes holds, unpinned, and the hash check is done by the code it checks. A copy with STATED_END changed gives "checker CHANGED", exit 2; the same copy with line 102's test replaced by `True or` gives "checker unchanged", exit 0. Pin a commit or verify the sha256 before running. NOTE within this: /tmp/queue_check.py is a fixed path in a shared directory.

21. F, FIX. Exit 1 is undocumented and covers every "could not run" case, some by traceback.
    - `gh` not on PATH: FileNotFoundError, exit 1 (SYN l).
    - Uppercase hex in the page: AttributeError, exit 1 (`page_upper.md`).
    - Outside a clone, no origin, or `--no-fetch` in a single-branch clone: "git …: fatal …", exit 1.

22. C, NOTE. queue_check.py:96,121. The ADOPTED instant is unfrozen and sets `since`. `page_adopt_future.md` (2027-01-30) gives drafts 0, reads 0, days 0 with "page unchanged". Q1's start at adoption is not in rule 3; the A6 drafts and reads before 09:06:41Z are charged to nothing.

23. C, NOTE. Cold reads count every `reader:` issue. Of 14 in the 24 h before adoption, 7 were reads of the move's builder and reviewer sessions and 2 were refiles of failed runs. At the record's own rate (25 "drafts", 14 reads a day) a 4/2 budget is spent within hours; that calibration is his.

24. C, NOTE. queue_check.py:128-131. For Q5, Q7, Q9, Q11 and Q13, "its window's stated end governs" is printed and not computed. A window that fails at its end leaves the head unchanged with no flag.

25. C, NOTE. queue_check.py:133. "Sessions that wrote in the last 24 h" counts `Claude-Session` trailers only, includes main's history, and ignores `--now`.

26. A, NOTE. Smaller step defects.
    - T15: Q1 "A6 is in force" passes at the `amend` even when `--activate-at` is ahead of the log.
    - T12: a `promote C2a` before the opening push is ignored, while BRIEF-C2b keys C2b's opening on "the first `push` entry after `decision promote C2a`".
    - No step checks the signer (by inspection; status.py:376 does).

27. D, NOTE. QUEUE.md:20. Rule 5's test is possible under the law only if Q2 and Q3 both land before 2026-11-30T00:00:00Z. "After 6 December" is coded as UTC (2026-12-07T00:00:00Z); in Hong Kong time, where his profile in memory places him, the day ends 16:00Z.

28. D, NOTE. QUEUE.md:34. "Bootstrapped, B0 to B7 hold" is asserted at `promote C2c-3`. The paper's §1 makes it counsel's claim "resolved by a reviewer of another family"; the checker tests neither. Subject "C2c-3" is inferred by pattern. ADVISER.md rule 4 ("drafts no … code") is met only through the BUILT word.

29. F, NOTE. queue_check.py:85-86. The checker's fetch rewrites FETCH_HEAD to main. Rerunning `git show FETCH_HEAD:queue_check.py > file` then fails, leaves a 0-byte file, and `python3 -I` on it exits 0 with no output (SYN j).

30. B/F, NOTE.
    - `--page`, `--predicate` and `--now` leave no mark in the output; `--now` does not cut the log.
    - A CRLF copy of the checker (sha256 058b08b2…) reports "checker unchanged": text-mode reads, benign.
    - A U+2028 in an issue title splits into a false `reader:` line (Python behaviour tested; UNTESTED against GitHub).
    - A non-UTF-8 locale would misreport hashes (UNTESTED: none installed).

3. CHECKED AND FOUND SOUND
- A6 arithmetic: a veto at seq == activate_at passes, at activate_at − 1 fails (T19, T20); seq 5879 never counts (T2).
- Veto subjects "C2a" and "C2a-prime" match status.py:286-298 and v5 §The subject (T3); "C2a-3" and "C2a-prime " are refused (T4).
- The fix must begin "C2a-prime:" with ts strictly after the stated end (T10, T10b, T11), as status.py:379,384.
- `judge/status.py` is the record's path (RUNBOOK lines 200-206).
- "First push after `decision promote X`" and subjects C2a, C2b, C2c-1, C2c-2 match BRIEF-C2b Order steps 3 and 5 and BRIEF-C2c-1 §2, §5, §9; promote bodies with `acts` or `evidence` still match.
- Lexical ts comparison is valid: kernel/log.py:21 fixes the format, all 7,133 entries are 20 characters, none decreases, seq is contiguous.
- All three recorded hashes verify; the frozen hash is the same at all four commits of the notes branch; a plain edit to checker, page or predicate row gives exit 2; a malformed hash line fails safe.
- `--since=…Z` is read as UTC by git 2.43 under TZ UTC, Asia/Hong_Kong and America/Los_Angeles.
- The `gh` query is right: `since` (updated) is a superset of the `created_at` filter, pull requests are excluded, and `reader:` is the prefix in real use (96 of the last 300 issues).
- No shell is used; every interpolated instant is regex- or kernel-validated; no injection path found.
- A depth-1 clone and a single-branch clone work with the page's command; Python 3.11 to 3.13 run it and the syntax parses at the 3.6 feature level.
- The untimed steps are Q5, Q7, Q9, Q11, Q13 as rule 3 says; 29 Nov, 6 Dec and 31 Jan are Sundays; TEST_AFTER and LAPSE match rule 5 in UTC.

4. NOT CHECKED
- Runtime on Python older than 3.11, git older than 2.43, Windows, a non-UTF-8 locale.
- status.py executed on T8/T9 (read only); signature validity of main's log.
- SPEC.md §10, BRIEF-C2a-prime, COUNSEL-OPEN, CASES.md, CLERK.md entry 20, ADVISER.md entries 100 and 101.
- Who can push to adviser/notes; the runner's contents beyond issue titles; `gh` pagination beyond the real volume.
