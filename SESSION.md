model: openai/gpt-6.1-sol
key: ~/.ssh/jack-reviewer
branch: move-promotion-judge

# reviewer: the pins for the move of the promotion evaluator under `judge/` (SPEC §10 item 15 and `replay_drift`; grant seq 6851)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/move-promotion-judge` on branch `move-promotion-judge`. Do not read `~/git/jack` or anything outside this worktree; never `Read` or `Glob` a path outside it.

This branch is a **push branch**: the sovereign applies it to `main` with `jack push`, because it changes the trusted base. So you run no `tools/jack` verb at all, and open no pull request. You commit on this branch and push it with `git push origin move-promotion-judge`, nothing else.

**Quoting.** On this runner, double quotes in code copied from a prompt have reached bash, and files, as a literal `\"`, and the code failed (runners #1144 to #1146). Code a session composes itself has not done that. So put no double quote in any shell command you copy from here. Run `python3 -m py_compile` on each Python file you change.

**Where you start.** A builder session has built the move on this branch, ending at `7b03d75d4d3a429be9054d97136721feb605aaad`. Counsel's commit `57022d72e56fcf53015f949e0eae197b0a839a6b`, on `origin/counsel/move-paths`, follows it: it changes the evaluator's paths in `LAW.md`, `README.md` and `transcripts/sessions/due-resolve.md`, and nothing else.
1. Run `git fetch -q origin main move-promotion-judge counsel/move-paths`.
2. `git status --porcelain` must print nothing.
3. `git merge-base --is-ancestor 7b03d75d4d3a429be9054d97136721feb605aaad origin/move-promotion-judge` must succeed.
4. Then:
   - if `git rev-parse HEAD` equals `git rev-parse origin/move-promotion-judge`, go on;
   - otherwise, if `git merge-base --is-ancestor HEAD origin/move-promotion-judge` succeeds, run `git merge -q --ff-only origin/move-promotion-judge`;
   - otherwise the worktree holds other work: stop and report, and reset nothing.
5. If `git merge-base --is-ancestor 57022d72e56fcf53015f949e0eae197b0a839a6b HEAD` fails, take counsel's commit in:
   - `git rev-parse HEAD` must print `7b03d75d4d3a429be9054d97136721feb605aaad`;
   - `git rev-parse origin/counsel/move-paths` must print `57022d72e56fcf53015f949e0eae197b0a839a6b`;
   - `git diff --name-only HEAD origin/counsel/move-paths` must print exactly `LAW.md`, `README.md` and `transcripts/sessions/due-resolve.md`;
   - then run `git merge -q --ff-only origin/counsel/move-paths` and `git push origin move-promotion-judge`.
6. `sha256sum SPEC.md` must give `72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2`.
7. `python3 -m unittest tests.test_law` must pass.

If any check fails, stop and report. Never change `SPEC.md`: the sovereign's grant at log seq 6851 names it by that hash.

**If an earlier session of this prompt ran here,** `git log --oneline 57022d72..HEAD` lists its commits. Continue from them, and do not write again a pin that is committed and passes.

**The texts you write to** are on this branch:
- `SPEC.md` §10 item 15 (from `15. **promote_unmet**`), whose last sentences name six pins, from `Pins` `promote_while_unmet` to `promote_judged_once`, each with its passing twin;
- the paragraph headed **The promotion evaluator**, whose last sentence names the pin `replay_drift` and its twin.

Read them whole first. The sovereign read that text before the build (CHARTER A2.10; his grant, seq 6851). The builder's report is `transcripts/BUILD-move-promotion-judge.md`. Its section **(b) Pins** lists every pin that fails today, and why.

**What you do.** Commit each part as you finish it, so that nothing is lost if the session ends. Hand commits end with the paragraph `Proposer: reviewer openai/gpt-6.1-sol runner-issue-<the value of $ISSUE>` (use the branch name if `$ISSUE` is empty).

1. **The pins the move left behind.** The move put `tools/status.py` and `tools/value.py` at `judge/status.py` and `judge/value.py`. It also put `now`, `read_log` and `resolution_rates` from `tools/entry.py` into `judge/entries.py`.
   - Re-aim each mutant whose target moved at the code as it now stands, so that the same edit is made and killed. That covers the 68 PENDING mutants and `worked_table`'s STALE one.
   - Change each pin's own imports or runs of the old paths, among them `pins/c2a.py`'s, which `per_type_base`'s twin fails on.
   - A fixture that writes the evaluator's source into a synthetic history **at the path `tools/status.py`** keeps that path. The evaluator reads that path from a tree (`judge/status.py`, the two lines in `c2a_tree_evidence` that read `tools/status.py`).
2. **The seven twins the installation broke.** Every repository `harness/gitfix.make_repo` builds now carries a signed grant and an installing push after seq 5564, because item 15 refuses a trunk without one. The twins of `charter_edit_unrecorded`, `amend_stale`, `freeze_ignored`, `one_act_amendment`, `foreign_object_admitted`, `kernel2_unrunnable` and `selfcheck_blind` assumed a log of a few lines: fixed activation heights, a fixed entry count, or a genesis rebound under a signed suffix. Repair only that assumption, so that each twin again tests what its pin names on the longer log. Then run that pin and confirm that each of its mutants is KILLED by the behaviour the pin names.
3. **Item 15's six pins**, each with its passing twin, exactly as the text describes each:
   - `promote_while_unmet`;
   - `evidence_substituted`;
   - `promote_tree_changed`, which also covers an entry commit that changes another path while another entry commit of the same line does not;
   - `promote_retroactive`, which has two cases: a `promote` before the installing push that is judged, and a push whose `SPEC.md` no earlier grant names taken as the installing push;
   - `evaluator_not_in_force`;
   - `promote_judged_once`.

   Their mutants are edits to `judge/judge.py` (`installing_push`, `promotion_checks`). The builder's `tests/promotion_fixture.py` and `tests/test_promotion_judge.py` show how a synthetic repository with an installing push and a promotion is built. You may import from them, but change nothing under `tests/`.
4. **`replay_drift`**, as the paragraph's last sentence describes it, with three mutants of `judge/status.py` and its twin:
   - (i) an edit that changes an unmarked line of a row's output;
   - (ii) an edit that makes a marked line read otherwise than its mark states, such as removing the `--first-parent` this move added;
   - (iii) an edit that changes no output, such as a comment, which only the bytes check catches.

   Its test runs the evaluator in the copy on a few rows of `spec/vectors/promotion-replay.json`: at least one row before 593 (unmarked) and one from 593 on (marked). It compares their output with the rows under the marks the paragraph states. It also checks that `judge/status.py` and `judge/value.py` in the copy are the bytes the paragraph names, as they were in the move's parent, changed only as the paragraph allows: the imports, and the one `--first-parent`.
   - The pin runner's copy holds no `.git` and no `transcripts/`, so read history and the frozen blobs from the repository the runner runs in.
   - The evaluator reads a tree through `git` at the revision its `--root`'s `HEAD` names. A `git clone --shared --no-checkout` with `HEAD` set to the row's commit (`git update-ref --no-deref HEAD <commit>`) and that commit's `log.jsonl` written to a file is quicker than a checkout.
   - Keep the pin's whole run under five minutes.

**The rules for every pin.**
- Register each pin in `pins/pins.py` beside the others, and raise `EXPECTED` by the number you add.
- Each mutant is the edit the text describes, and its `find` string occurs exactly once in the code as it now stands.
- A mutant must be killed by the behaviour its pin names, not by an error elsewhere.
- Where a twin cannot pass on the builder's code, the code is wrong or the text is. Write the pin as the text states it, let it fail, and say which in your report, with the sentence. Never weaken a twin to make it pass.

**What you do not do.** Change nothing outside `pins/` and `transcripts/`, except as start step 5 takes counsel's commit in. That rules out `judge/`, `kernel/`, `tools/`, `tests/`, `harness/`, `SPEC.md`, `CHARTER.md`, `RUNBOOK.md`, `LAW.md`, `judge/scope.json` and `spec/vectors/`. Never commit a tree whose counted lines exceed the cap of 8,400. If the pins do not all fit, stop: commit what fits, push, and report the count and what is not written. Do not merge `main`.

**Time and long commands.** The job stops at 180 minutes, and a single command at 15. `python3 pins/run.py --only <names>` runs some pins. Run the full `pins/run.py` and the unit suite each in the background, with `nohup` and output to a file under `/tmp`, and poll the file. By minute 160, commit what you have and push the branch, even if unfinished, and say so.

**Checks before you push.** Run each and copy its result into your report:
- (a) `python3 -m unittest discover -s tests -t .`: every test passes, `tests/test_pins.py` and `tests/test_law.py` included;
- (b) `python3 pins/run.py --transcript transcripts/evidence/move-promotion-judge-pins-review.txt`: exit 0, with SURVIVED 0, STALE 0, TWIN FAILED 0 and PENDING 0. Give its counts and how long it took;
- (c) the lines under `judge/scope.json`'s `counted` prefixes, counted as judge item 10 counts them (`judge.judge.counted_lines`), at your head: at most 8,400. Also run `python3 tools/count_kernel.py`;
- (d) `git diff --name-only 57022d72e56fcf53015f949e0eae197b0a839a6b HEAD` lists only paths under `pins/` and `transcripts/`.

**Report.** Write it to `transcripts/PINS-move-promotion-judge.md`, commit it with the pin transcript, and push. Give:
- the branch head;
- checks (a) to (d);
- for each pin you changed in steps 1 and 2, what you changed and why;
- for each new pin, its mutants and what kills each;
- anything in the text you could not pin as it stands, quoted, with the reason.

End with one line: `PUSHED <head>` or `STOPPED: <reason>`.
