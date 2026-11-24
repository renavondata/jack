# FIX-20261124-merge-closed: `jack merge` refuses a pull request it finds closed while it waits

Counsel's text, 24 November 2026, for the sovereign's read (CHARTER A2.10). The builder makes it under `transcripts/sessions/fix.md`, on branch `FIX-20261124-merge-closed`, and proposes it. It changes what `tools/jack merge` does when it finds, during either of its waits, that the pull request it is merging is no longer open. It changes nothing for a pull request that stays open.

**Why.**
- **`jack merge` reads the pull request's state once, before it signs** (`tools/jack`, lines 160 to 162). It then waits twice for the judge and the tests, first on the proposal's head and then on the head that carries its `merge` entry (lines 168 and 173). Neither wait has a deadline. Then it calls `gh pr merge` (line 174), and it has not read the state again.
- **GitHub merges a closed pull request when it is asked so.** jack #1355 was closed under the sovereign's login at 06:23:58Z on 23 November and merged by the court's App at 06:47:44Z, with no reopening between. Its `merge` entry, seq 7315, had been signed at 06:15:05Z.
- **It has happened once, and it was rated as able to wait.** Counsel wrote of it: "it can wait. It bit only because he was withdrawing work by hand" (ADVISER.md entry 174), and the adviser agreed (entry 176). It is brought now because the fix of `transcripts/FIX-20261124-pins-worker.md` needs his grant in any case, and one sitting of his can carry both.
- **Closing is how a proposal is withdrawn,** by the herald when it is stale or by hand. While the verb does not read the state again, a close does not stop a merge whose entry is signed.
- **The verb already reads the pull request during both waits.** At each poll at which GitHub reports checks, `passed` asks for the head and the checks (line 149, after the test of line 147). The state can be read in the same call.

**When it may be made.** Before C2a-3 opens or after it has ended, and never while it is open. `transcripts/BRIEF-C2a-3-draft.md` on `main` refuses, inside its window, any code but its own: "no code but §The code", and "no change to a verb of `tools/jack`". Before anything else, read `main`'s log.
- C2a-3 opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z. If the log holds none, go on.
- If it holds one, C2a-3 has ended when the log holds, after that entry, a `decision` of kind `promote` with subject `C2a`, or a `decision` of kind `veto` with subject `C2a` or `C2a-3`; or when the instant now is after the `resolves_by` of the forecast whose `args.id` is `V8`. If C2a-3 has not ended, stop, report that the window is open, and change nothing.

**The change.**
1. **`passed` reads the pull request's `state` with the head and the checks,** in the call it makes now at line 149.
2. **A state other than `OPEN` is refused there,** before the head is compared and the checks' conclusions are read (lines 150 to 152). The refusal's words are `PR #<n> is <state>, not OPEN, during the wait; this verb merges nothing`, with the pull request's number and the state GitHub gave. A pull request whose watched checks failed is refused for that at line 148, as today, whatever its state.
3. **RUNBOOK states the refusal.** RUNBOOK is counsel's and `tools/jack` the builder's, so the text lands first (RUNBOOK, **Text before code**). Counsel's proposal of this text adds one sentence to RUNBOOK's section `jack merge N`, in words that take effect from this fix's merge. The builder changes nothing in RUNBOOK.
4. **Nothing else.** The first reading of the state, before the verb signs, stays as it is. A pull request that is open at every poll is merged exactly as today. No other verb changes.

**What the change does and does not do, said in terms.**
- A pull request found closed in the first wait is refused before anything is signed.
- A pull request found closed in the second wait is refused after the `merge` entry was signed and pushed to the proposal's branch. That entry stays on the branch. While the pull request stays closed it does not reach `main`.
- **A reopened pull request can still be merged outside the verb.** The herald's workflow on the runner completes a merge itself when an open pull request's head ends with a `merge` entry and both checks are green (`.github/workflows/herald.yml`, lines 57 to 70), having read the state at line 52. This text does not change that path.
- The herald starts no re-proposal on the new refusal. Its workflow reads the verb's output for the word `CONFLICTING` alone (line 91), and it skips a pull request that is no longer open (line 52).
- A state of `MERGED` is refused in the same words. Someone else merged it, and the verb says that it merged nothing.
- The last reading of the state comes seconds before `gh pr merge`. A pull request closed in those seconds is still merged. This text narrows the gap from the length of a tests run to the time between two calls, and does not close it.
- `passed` reads the pull request only once GitHub reports checks on it (line 147). A pull request closed before any check is reported is therefore not seen as closed by this change, and the verb goes on waiting. The herald's own job ends such a wait after 60 minutes (`herald.yml`, `timeout-minutes`). This text leaves that as it is.
- **Its pin is owed, and comes later.** LAW.md says that every change to `tools/` carries a pin in `pins/pins.py` (lines 61 to 64). `pins/` is the reviewer's path and not the builder's, and the cap leaves no room for a pin now (**Size**). The pin is `merge_refuses_closed`, the reviewer's, with the mutant `closed_state_unread`. `transcripts/FIX-20261124-fix-pins.md` specifies it, and it is made after C2a-3 has ended, under the cap that its opening push sets. Until then what holds the change is the one test below, in the builder's own path, and acceptance (iv). His grant of this text is his word on that interval.

**Paths.**
- **May change:** `tools/jack`, `tests/test_jack.py`.
- **May not change:** any other file.

**Size.** `main` has 8,340 counted lines against a cap of 8,400, and `tools/` and `tests/` are counted. This change adds at most 18 counted lines. Every line of a Python file counts, blank lines and comments included. `transcripts/FIX-20261124-pins-worker.md` adds at most 30, so the two together take at most 48 of the 60 lines left.

**Acceptance.**
- **This text adds one test by name,** and no other: `test_merge_refused_when_the_pull_request_is_closed_during_a_wait` in `tests/test_jack.py`, with a sub-test for each of (i), (ii) and (iii).
- **(i) Closed in the second wait.** The pull request reads `OPEN` when the verb starts and at every poll of the first wait, and `CLOSED` at the first poll that follows the entry's push. The verb must refuse in the words of point 2. `main` on the remote must be where it was, and the proposal's branch must hold the entry's commit. No `gh pr merge` may have been called.
- **(ii) Closed in the first wait.** The pull request reads `OPEN` when the verb starts and `CLOSED` at the first poll. The verb must refuse in the words of point 2 with nothing signed: the proposal's branch on the remote is where it was.
- **(iii) Merged by another hand.** As (i), with `MERGED` for `CLOSED`. The refusal must give `MERGED` as the state.
- **The test double.** It answers `state` on every `gh pr view` already, from one answer fixed for the whole call of the verb (`tests/test_jack.py`, lines 46 and 47, and line 155). It may gain what it needs to give another state from a chosen call on, as its `move` does for the head. Say what you added to it. No line of an existing test changes; if you find that one must, stop and report it.
- **(iv) The mutant.** Show that the new test fails when point 2's refusal is removed from your `tools/jack`, and report the failure's first line. Then restore it. Commit none of that.
- **(v) The whole suite.** `python3 -m unittest discover -s tests -t .` passes at the head, and its `Ran N tests` is `origin/main`'s plus one.

**Interests.** Counsel's own stale proposals are closed by a declared act, and counsel has an interest in a close being final. Counsel rated this fault as able to wait and brings it now for the convenience of one sitting; his read is the place to say that it should wait longer.
