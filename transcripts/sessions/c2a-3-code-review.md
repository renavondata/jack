model: {MODEL}
key: ~/.ssh/jack-reviewer
branch: {BRANCH}

# reviewer: read the code of C2a's third window on the push branch, and write `REVIEW-C2a-3-code.md` (BRIEF-C2a-3)

You are a **reader** and, if the branch passes, the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`) whose review file the sovereign names to `jack push opening-c2a-3 --opens C2a-3 --review`. You work in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it. Name no path outside the worktree in any command, `/tmp` included. Your scratch directory is `.review/` at the top of the worktree. Never `git add` that directory. Do not set `TMPDIR`, `TEMP` or `TMP`, in your shell or for any command you run. Never edit `log.jsonl`.

**The push branch.** The window's code, its tests and its pins are on `opening-c2a-3`, a branch the sovereign has published. You run no `tools/jack` verb at all, and open no pull request. You change no file of the code, its tests or its pins. On a pass you add one file, `transcripts/REVIEW-C2a-3-code.md`, in one commit, and publish it with `git push -q origin HEAD:opening-c2a-3`. You push nothing else, and never with force. If that push fails, stop and report git's message, and do not pull, merge or rebase.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here.

**The clock.** Step 1 writes the session's start, in seconds, to `.review/start`. Every minute named below is counted from it. The job stops at 180 minutes, and a single command at 15 unless this text gives it longer.

**Where you start.** The first commit of `opening-c2a-3` over `main` is the sovereign's cherry-pick of counsel's patch. The builder's session (runner #1322) put three commits on it, and its last is *B*, `7d7f89471a52c248ad9c3214645f7e936235ab4f`. The reviewer's pins follow *B*.
1. If `.review/` already exists, stop and report. Otherwise run `mkdir .review && date -u +%s > .review/start`.
2. Run `git fetch -q origin main opening-c2a-3`; if it fails, run it once more. Then `git status --porcelain --untracked-files=normal` must print `?? .review/` and nothing else, and `git merge-base --is-ancestor HEAD origin/main` must succeed. If the fetch fails twice, or either test fails, stop and report.
3. Run `git reset -q --hard origin/opening-c2a-3`, then `git rev-parse HEAD > .review/tree`. That commit is the tree you read. Begin every command that uses it with `R=$(cat .review/tree);`.
4. `git merge-base --is-ancestor 7d7f89471a52c248ad9c3214645f7e936235ab4f HEAD` must succeed, and `ls transcripts/REVIEW-C2a-3-code.md` must fail: no code read is on the branch yet.
5. `sha256sum transcripts/BRIEF-C2a-3-draft.md` must give `a5c331b40d1e81f959e147461884b3a55e11d829933bfd2296d660a526433945`, `sha256sum SPEC.md` must give `c4a5b44b8465f4be9cd4a5bbeb294cfd5c56a7397319e7f1c167853d7fd628a7`, and `sha256sum spec/vectors/promotion-replay-c2a-3.json` must give `943a79863df95479cc93085e0dc686b47f5940a34b5497372503937cb85f3e77`. The sovereign read the brief before the build: his grant is seq 7615 on `main`'s log.
6. **Another family than the builder's.** `R=$(cat .review/tree); git log --no-merges --format='%h %(trailers:key=Proposer,valueonly)' origin/main..$R` prints one line for each commit of the branch: its hash, then its trailer's fields. A line whose second field is `builder` names the builder's model as its third. A model's family is the part of its name before the `/`. Yours is the family of `{MODEL}`. If a `builder` line names a model of your family, stop and report that line: this code is read by a family that did not write it.

If any check fails, stop and report.

**The texts** are `transcripts/BRIEF-C2a-3-draft.md` on this branch, whole, and `SPEC.md` §10's paragraph headed **The promotion evaluator**. Read above all §The code, §The window, §The cap, §The subject, §The late-report rule, §No item changes, §Pins, and §Precondition items 4 to 6.

**What you read.** Every commit of the branch over `main`: `R=$(cat .review/tree); git diff origin/main...$R`, and each commit with `git show`. For each finding give the file and line, what is wrong, the sentence of the text it departs from, quoted, and the code, quoted.
1. **The scope's change.** The first commit is counsel's patch and changes `SPEC.md` and `judge/scope.json` alone: the cap at 9100, SPEC §10's block, one clause of its cap history, and the two sentences §The code gives word for word.
2. **The six changes** of §The code, each in `judge/status.py`: does the code do what each paragraph says, and nothing it does not? Is every line that no change needs left byte for byte, among them the first-parent line of `c2a_tree_evidence` and the two lines that read `tools/status.py`? Do `main`, `inputs`, `assess` and `promotion_line` keep the form `judge/evaluate.py` calls?
3. **The tests:** at least one for each change, and for change 3 the test the brief describes, on the real `log.jsonl`.
4. **The pins:** each of the eight of §Pins, with every requirement, mutant and twin it gives, registered as `Pin("<name>"`, and `EXPECTED` counting them. Is each mutant the edit the text describes, and is it killed by the behaviour its pin names?
5. **`replay_drift`,** re-aimed as the paragraph of §The code orders: the first table's three rows and its hash; rows of the second table, one marked, and its hash; `judge/status.py` held to a SHA-256; `judge/value.py` to the moved bytes; its three mutants.
6. **Parties and paths.** Each commit's trailer is filled, and its paths are its party's: the builder's under `judge/status.py` and `tests/`, the reviewer's under `pins/`, counsel's patch as item 1 says.

**Checks.** Run each and copy its result into your report. Run them one at a time, each as one command, with the bash tool's `timeout` set to `1800000` on that call, which is thirty minutes. If a command is ended at its limit, say so and do not run it again. Start neither check (a) nor check (b) after minute 115.
- (a) `python3 -m unittest discover -s tests -t .`. Every test must pass.
- (b) `python3 pins/run.py`. Every pin must be KILLED, none SURVIVED, STALE, TWIN FAILED or PENDING.
- (c) The counted lines at your tree, counted as `counted_lines` in `judge/judge.py` does over the `counted` list of `judge/scope.json`. They must be at most 9100.
- (d) `sha256sum judge/status.py`, and the SHA-256 that `pins/replay.py` holds `judge/status.py` to. The two must be equal.

The whole replay of the table is another session's, and you do not run it.

**Your verdict.** A change that does not do what a quoted sentence says, a twin the text lists that is absent or failing, a change outside a party's paths, an unfilled trailer, a check that fails, or (d)'s two hashes differing is a BLOCK. A sentence of the text that the code meets only in part, or a test or pin weaker than the text asks, is a FIX. Anything else you would mend is a NOTE.

**On FAIL** (any BLOCK): write no file and commit nothing.

**On PASS** (no BLOCK): write `transcripts/REVIEW-C2a-3-code.md` beginning with exactly these four lines, then a blank line, then your findings, one to a line in the form `F<n> [FIX|NOTE] <file:line> — <problem> — <the sentence of the text, quoted> / <the code, quoted>`:
```
VERDICT: ACCEPT WITH OBLIGATIONS
Reviewed tree: <the 40 hex digits in .review/tree>
Evaluator: judge/status.py sha256 <the 64 hex digits that sha256sum judge/status.py prints>
Reader: reviewer; model {MODEL}; {NOW}
```
Write `VERDICT: ACCEPT` instead if you have no FIX. Then:
- `git diff --name-only` must print nothing and `git status --porcelain --untracked-files=normal` must print `?? .review/` and `?? transcripts/REVIEW-C2a-3-code.md` and nothing else.
- Write the commit's message, without a trailer, into `.review/text`. Then run `git add transcripts/REVIEW-C2a-3-code.md && I=${ISSUE:-{BRANCH}}; { cat .review/text; printf '\n\nProposer: reviewer {MODEL} runner-issue-%s\n' $I; } > .review/msg && git commit -q -F .review/msg`.
- `git log -1 --format='%(trailers:key=Proposer,valueonly)'` must print `reviewer`, then at least one field more, with no `<`. If not, do not push: stop and report.
- Run `git push -q origin HEAD:opening-c2a-3`.

**Report.** Give:
- the tree you read, and the output of step 6;
- your verdict and every finding, in the form above, BLOCKs first;
- the results of checks (a) to (d);
- on a pass, the head after your commit.

End with one line: `ACCEPTED <head>`, `ACCEPTED WITH OBLIGATIONS <head>`, `FAILED: <the number of BLOCKs> BLOCK` or `STOPPED: <reason>`.
