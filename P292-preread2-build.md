Counsel's second pre-read of transcripts/sessions/c2a-3-build.md, at 7af6f818 (blob 58633f14, 84 lines), by a fresh agent, 24 November 2026, about 13:44Z to 14:08Z. It built scratch repositories and ran the start's steps literally in eight cases, and the detached checks on stand-ins. The report as handed back:

VERDICT: FAIL

One wrong state passes step 8 (finding 1). The rest of the two failed areas held under bash.

FINDINGS

1. BLOCK, lines 30 and 42. A rename hides the path a file is taken from, so "names every path that any of those commits touched" is false.
   - Case A7e: inherited commits `git mv pins/pins.py tests/pins_moved.py` and `git mv tools/t.py tests/t_moved.py`, each with `Proposer: builder m runner-issue-7`.
   - Step 8's first command printed only `tests/pins_moved.py` and `tests/t_moved.py`; the second printed two `builder` lines. Both tests pass with pins/ and tools/ emptied.
   - Line 42's `git diff --cached --name-only` printed only `tests/pins_moved.py`. Git 2.43, default config.
   - Lesser, A7f: a merge commit that itself edits `pins/pins.py` is not listed.
   - Smallest change: add `--no-renames` to both commands (it then printed `pins/pins.py` and `tools/t.py`); add `-m` on line 30 for the merge.
   - Practical risk is low; it fails by your rule.

2. FIX, lines 57-58. The kill form works in bash 5.2 and fails in dash.
   - dash: `kill -TERM -- -$(cat .build/pins.pid)` gave `sh: 1: kill: Illegal number: -`, exit 2; `sh` and `sleep 300` stayed alive.
   - The KILL line sends the same error to `kill.err` and ends `true`. Line 58 calls an error "no fault" and then removes the pid file, so the group is left with no record.
   - I could not learn which shell opencode uses on the runner (line 11 says bash).
   - Smallest change: delete `-- ` from the four kill commands (`kill -TERM -$(cat ...)` ended the group under both shells), and narrow "gives an error" to "gives `No such process`".

3. NOTE, line 58. "a `.pid` file that is already there", before starting (b), also fits `unit.pid` of the (a) just finished. Read so, the session signals that old group id and removes `unit.out` and `unit.exit` before the report. A finished run's id is also signalled at the next session's start; if reused, another group dies (pid_max is 32768 here). Smallest change: "that check's `.pid` file".

4. NOTE, line 61. "If its detail names a row's output": `pins/run.py` keeps the traceback's last line, so an output drift shows the evaluator's last printed line, e.g. `(promote C2a: refused: ...)`, never `row N: output drift` (simulated with its `run_test` logic). Smallest change: "If its detail is anything else".

5. NOTE, line 69. (e) says what must be equal, not what to do when it is not; (a) and (b) say fix. Smallest change: end the line "; if not, fix your code".

6. NOTE, lines 55 and 66. Only "small files" keeps (e) out of the five-minute polls of (a) and (b); `.build/w` is a 17 MB checkout. Smallest change in line 55: "nothing but small files and no `.build/w`".

7. NOTE, lines 13 and 22. In A6 the stale group was signalled and `.build/unit.pid`, `.out` and `.exit` removed before step 3 classified. "change nothing in it" holds for the work, not for `.build/`.

8. NOTE, lines 57 and 74. The bound lives in the session; a session that dies leaves the check unbounded. If a self-bound is added: plain `timeout 1800` put the child in its own group and the template's kill left 2 processes; `timeout --foreground` kept the group.

CASES
- A1: bullet 2, reset to P; status `?? .build/`; step 8 prints nothing; `git push -q origin opening-c2a-3` later succeeded. Right.
- A2: bullet 1; clean; goes on. Right.
- A3: bullet 1; step 8 lists `judge/status.py`, `tests/test_c1.py` and two `builder` lines. Right.
- A4: bullet 3; the unpushed commit is kept and tested. Right.
- A5: bullet 3; status listed 8 entries; reset and clean removed staged, unstaged and untracked files under tests/ and tools/; the commit and `.build/` stayed; nothing staged after. Right.
- A6: bullet 4, stops; HEAD, index, diffs and untracked files identical before and after (finding 7 apart). Right. A clean local branch strictly behind the published one also stops.
- A7: pins/ touched then reverted: caught. No trailer: caught (`a5c2015 ` alone). `Proposer: reviewer`: caught. Rename and merge with its own edit: not caught.
- A8: absent: made. Stale pids: `No such process`, files removed, goes on. Live `sleep 300` group: ended, files removed, then step 1. The order works under bash, not under dash.
- Launch: the pid file is the group id under bash, dash, `set -m` and `-i`; `.exit` held 0 after `sleep 5`; TERM then KILL ended a group with a TERM-ignoring child; the launch returned in 7 ms.

TIME RULES
No rule is impossible and no two conflict. An order that meets all: (a) by 85, then (b), then (c), (d), (e). Hosted-runner times in the FIX-20261123 texts: unit 7 to 10 minutes, pins 11.5 to 15.5 serial. (e) is about 10 minutes at your 90 to 115 seconds a reading, each command under 15. If both detached checks use their 30 minutes, (b) cannot start after 115 or (e) cannot end by 150; the "unfinished" ending covers that. (e) after (b) works as written, given finding 6.

VERIFIED TRUE
- `SPEC.md` c4a5b44b… and `grep -c 9100` = 1 with f6d6db7d cherry-picked on origin/main 59c14584; the brief's and table's hashes; P's subject and trailer.
- His paste (`agent/pastes-work:c2a-3-read.sh`) begins the grant as line 27 and holds `the cap at C2a-3's opening is 9,100`; log entries carry `proposer`, `body.kind`, `body.subject`.
- Line 433 and mutant `marked_walk_regressed`; lines 436-437; `judge/evaluate.py`'s four calls; 773 rows, `marked` only at 735-772; `pins/replay.py` line 80, whose three rows end before seq 7180; `counted_lines(repo, sha, prefixes)`; SPEC's two quoted phrases.
- (e) run literally with the unchanged evaluator: row 4 exit 1 and no lines; row 734 exit 0 and 46 lines equal to `stdout`, 237 s on this 2-core machine; worktree add, checkout, remove and prune work.
- `run.yml`: the worktree rule, 180 and 15 minutes. `.build/` is not ignored.
- No double quote in a command; only {MODEL} and {BRANCH}; no command names an outside path; nothing of the reviewer's or counsel's is ordered.

COULD NOT VERIFY
- The runner's shell, pid_max and global gitignore.
- Runners #1144 to #1146.
- That (a) and (b) pass with `.build/` in the copied tree.
- Rows 735 and 772 against `marked`, which needs the built code.
