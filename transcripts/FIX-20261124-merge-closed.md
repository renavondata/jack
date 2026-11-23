# FIX-20261124-merge-closed: `jack merge` does not merge a pull request that was closed while it waited

Counsel's text, 24 November 2026, for the sovereign's read (CHARTER A2.10). The builder makes it under `transcripts/sessions/fix.md`, on branch `FIX-20261124-merge-closed`, and proposes it. It changes what `tools/jack merge` does when the pull request it is merging is closed during either of its waits. It changes nothing for a pull request that stays open.

**Why.**
- **`jack merge` reads the pull request's state once, before it signs** (`tools/jack`, lines 160 to 162). It then waits twice for the judge and the tests, first on the proposal's head and then on the head that carries its `merge` entry (lines 168 and 173). Neither wait has a deadline. Then it calls `gh pr merge` (line 174), and it has not read the state again.
- **GitHub merges a closed pull request when it is asked so.** jack #1355 was closed under the sovereign's login at 06:23:58Z on 23 November and merged by the court's App at 06:47:44Z, with no reopening between. He was withdrawing work by hand that morning (ADVISER.md entries 174 and 176).
- **So closing a proposal does not stop its merge once the herald has begun on it.** Closing is how a proposal is withdrawn, by the herald when it is stale or by hand.
- **The verb already reads the pull request at each poll of both waits.** `passed` asks GitHub for the head and the checks (line 149). The state can be read in the same call.

**The change.**
1. **`passed` reads the pull request's `state` with the head and the checks,** in the call it makes now.
2. **A state other than `OPEN` is refused there,** before the head and the checks are judged. The refusal names the pull request and the state it found, and ends `not merged`, as the verb's other refusals of a wait do.
3. **RUNBOOK states the refusal.** RUNBOOK is counsel's and `tools/jack` the builder's, so the text lands first (RUNBOOK, **Text before code**). Counsel's proposal of this text adds one sentence to RUNBOOK's section `jack merge N`, in words that take effect from this fix's merge. The builder changes nothing in RUNBOOK.
4. **Nothing else.** The first reading of the state, before the verb signs, stays as it is. A pull request that is open at every poll is merged exactly as today. No other verb changes.

**What the change does and does not do, said in terms.**
- A pull request closed during the first wait is refused before anything is signed.
- A pull request closed during the second wait is refused after the `merge` entry was signed and pushed to the proposal's branch. That entry stays on the branch of the withdrawn proposal and never reaches `main`.
- The herald starts no re-proposal on the new refusal. Its workflow on the runner reads the verb's output for the word `CONFLICTING` alone (`.github/workflows/herald.yml`, line 91), and it skips a pull request that is no longer open (line 52).
- The last reading of the state comes seconds before `gh pr merge`. A pull request closed in those seconds is still merged. This text narrows the gap from the length of a tests run to the time between two calls, and does not close it.
- `passed` reads the pull request only once GitHub reports checks on it (line 147). A pull request closed before any check is reported is therefore not seen as closed by this change, and the verb goes on waiting. The herald's own job ends such a wait after 60 minutes (`.github/workflows/herald.yml` on the runner, `timeout-minutes`). This text leaves that as it is.

**Paths.**
- **May change:** `tools/jack`, `tests/test_jack.py`.
- **May not change:** any other file.

**Size.** `main` has 8,340 counted lines against a cap of 8,400, and `tools/` and `tests/` are counted. This change adds at most 18 counted lines. Every line of a Python file counts, blank lines and comments included.

**Acceptance.**
- **(i) Closed during the second wait.** A new test in `tests/test_jack.py`, made as `test_merge_refused_when_the_head_moves_off_the_entry_during_the_wait` is made: the pull request is open when the verb starts and when it signs, and reads `CLOSED` at the poll that follows the entry's push. The verb must refuse in the words of point 2. `main` on the remote must be where it was, and the proposal's branch must hold the entry's commit. No `gh pr merge` may have been called.
- **(ii) Closed during the first wait.** The same test, or a second, has the pull request read `CLOSED` at the first poll. The verb must refuse with nothing signed: the proposal's branch on the remote is where it was.
- **(iii) Open throughout.** `test_merge_admitted_entry_on_the_proposal_branch_then_github_merges` and the other tests of the verb pass unchanged, but for what the test double must now answer when it is asked for `state`. List every line of an existing test that you change, and say why.
- **(iv) The mutant.** Show that (i) fails when point 2's refusal is removed from your `tools/jack`, and report the failure's first line. Then restore it. Commit none of that.
- **(v) The whole suite.** `python3 -m unittest discover -s tests -t .` passes at the head. Report its `Ran N tests` beside `origin/main`'s; the difference is the tests you added.

**Interests.** Counsel's own stale proposals are closed by a declared act, and counsel has an interest in a close being final.
