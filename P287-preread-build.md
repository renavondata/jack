Counsel's own pre-read of transcripts/sessions/c2a-3-build.md at 5adcaa3e (blob 56b2ad51), by a fresh agent, 24 November 2026, about 12:17Z to 12:34Z. The report as handed back:

VERDICT: FAIL

Both failing findings are checks that can pass when they should fail (kind 2). I found no false statement and no check that fails in the normal case.

1. FIX — line 25 (step 6): "`git show origin/main:log.jsonl | grep -c 'promote_unmet: SPEC.md c4a5b44b…'` must print 1".
   - Wrong: the check ties the log to SPEC.md's hash only, yet line 36 cites it as his A2.10 read of the brief ("his grant, step 6").
   - Evidence: the brief's Precondition 4 has the grant say "that he read this file at a stated SHA-256", name the table's SHA-256 and state the cap. A grant naming other brief or table bytes passes. So does any log line holding the string: proposal entries carry a free-text `title` (seq 7540). `transcripts/sessions/fix.md` line 16 asks for proposer `guy`, kind `grant` and the text's hash.
   - Smallest change: `git show origin/main:log.jsonl | grep 'promote_unmet: SPEC.md c4a5b44b…' | grep a5c331b4… | grep -c 943a7986…` must print 1, with the two full hashes of step 7. The same form on seq 6851's grant with its table hash prints 1. Appending `| grep 9100` would cover Precondition 5.

2. FIX — line 27 (step 8), reused by line 53 (d) and line 68: "`git diff --name-only <P> HEAD`".
   - Wrong: the command carries a placeholder, and `c2a-3-table.md` line 22 records that this runner's shell keeps no variable between commands. A session that sets `P=` in one command and uses `$P` in the next runs `git diff --name-only  HEAD`.
   - Evidence: I ran that here on a clean tree and it prints 0 lines. So check 8 and check (d) pass whatever the commits touched. The move's session committed a report and a pins transcript under `transcripts/` (BUILD-move-promotion-judge.md, lines 3–5 and 82), which is the kind of commit (d) exists to catch. Copied literally, bash reads `<P>` as a redirect.
   - Smallest change: write it whole: `git diff --name-only $(git rev-list --reverse origin/main..origin/{BRANCH} | head -1) HEAD`.

3. NOTE — line 56: "`worktree add -q --detach .build/w <commit>`".
   - An earlier session that ended before line 60 leaves `.build/w`. The add then fails, and line 49's "nothing but small files" is already broken when (a) and (b) start.
   - Smallest change: "If `.build/w` exists, remove it first, as below."

4. NOTE — lines 54–59, check (e): nothing says one row per command.
   - `c2a-3-table.md` line 68 measured one run at main's head at 114 s alone and 225 s under load, and change 6 makes two readings at rows 735 and 772. Three long rows in one command could pass 15 minutes if (a) or (b) is still running.
   - Smallest change: add "one row per command".

5. NOTE — line 45: "at least one for each of the six changes, and the test of change 3 that the brief describes".
   - This reads as either one or two tests for change 3. The brief asks "a test for each change", and line 52 calls counted lines scarce.
   - Smallest change: replace ", and the test of change 3 that the brief describes," with "; for change 3, the test the brief describes,".

6. NOTE — line 41: "the line of `c2a_tree_evidence` that walks first parents".
   - Lines 417 and 433 both do; the mutant `marked_walk_regressed` finds only 433.
   - Smallest change: add "(line 433)".

Verified true:
- Hashes: SPEC.md at f6d6db7d hashes to c4a5b44b…, and main's SPEC.md and scope.json equal the patch's parent's, so a cherry-pick reproduces it. `grep -c 9100` prints 1. The brief (a5c331b4…) and table (943a7986…) hashes hold at origin/main.
- Start checks: P's subject begins `push: C2a-3 opening`; the step 3 commands run on counsel's patch branch return P; step 4's four cases cover a fresh cut, a pushed head, an unpushed head and other work.
- Table: 773 rows; indexes 4, 734, 735 and 772 are the first-parent chain's commits; `marked` is on 735..772 only; row 4 is exit 1 with no stdout; row 734's log ends at seq 6851.
- SPEC holds both quoted phrases (lines 504 and 516).
- Code: `counted_lines(repo, sha, prefixes)` is in judge/judge.py and gives 8340 at origin/main; judge/evaluate.py calls exactly `main`, `inputs`, `assess` and `promotion_line`; status.py lines 436–437 read `tools/status.py`; the brief's line numbers match status.py.
- Pins: `replay_drift` holds the moved bytes (pins/replay.py line 80); all 55 status.py mutants are in pins/pins.py and pins/replay.py; no unit test holds the evaluator's bytes, only tests/test_pins.py's exactly-once check; §Pins adds eight names, none registered today.
- The RUNBOOK trailer form matches; no command has a double quote or names an outside path; the README lines agree with the template.

Could not verify:
- The grant: step 6 prints 0 today.
- Whether `nohup … &` without `setsid` outlives the tool call on this runner (the table template used `nohup setsid`).
- The runner's git config, on which step 2's `?? .build/` depends.
- Run times of (a), (b) and (e), which I did not run.
- That a correct build prints `marked` at rows 735 and 772.
