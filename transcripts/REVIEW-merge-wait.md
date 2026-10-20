# Review: merge wait

## 1. The admitted fixture is refused by the real judge

**Location:** `tests/test_jack.py:336-341`, `384-390`; permissive responses at `118-120` and `37-39`.

**RUNBOOK sentence:** “Preconditions, read with `gh pr view` and `gh pr checks`: PR N is open against `main`, mergeable, its required checks green on its current head; its head commit is one commit past the `commit` of a valid `proposal` entry in the PR's log, or — until the judge checks it — carries a filled `Proposer:` trailer.” (`RUNBOOK.md:90-93`)

`proposed()` uses `branch()`'s default change to `README.md` and signs its proposal as builder. The fixture retains `judge/scope.json`, which excludes `README.md` from the builder's paths. Running the real judge against both the proposal head and the subsequently pushed merge-entry head produces `ok: false`, `reason: party_scope`, `detail: outside builder's paths: README.md`. Nevertheless, the required-checks stub returns success, and `LATE` returns success after two calls without inspecting either head or any verdict. The new admitted test exits zero and calls `gh pr merge` for a proposal GitHub's judge would refuse. Use an allowed builder path and make the check responses depend on admission of the actual pushed head.

## 2. The “then GitHub merges” test never performs or verifies a merge

**Location:** `tests/test_jack.py:120`, `344-358`; also `384-390`.

**RUNBOOK sentence:** “The merge commit GitHub makes is the effect of the entry that precedes it.” (`RUNBOOK.md:98-99`)

The `pr merge` response is an unconditional zero exit with no git effect. Thus `git pull --ff-only` succeeds as a no-op, and the printed run-watch command names the old main commit. The test named `test_merge_admitted_entry_on_the_proposal_branch_then_github_merges` checks the invocation but never checks that remote main gained a merge commit, that its proposal parent is the merge-entry head, or that local main pulled that effect. Its line 357 equality also passes when both refs remain at the original main. The new wait-success test inherits this stub and likewise stops at the branch entry. A stub that advances remote main through a merge, followed by assertions on the parents, pulled HEAD and watched SHA, is needed to test the claimed ending.

## 3. A partially registered check set ends the wait prematurely

**Location:** `tools/jack:153-158`; coverage gap at `tests/test_jack.py:37-39`, `384-390`.

**RUNBOOK sentence:** “Effect: `gh pr checks N --watch` until the judge and the tests have admitted the head that carries the entry, then `gh pr merge N --merge`, which GitHub performs only if they did; then `git pull --ff-only` on `main` and `gh run watch` of `main`'s run.” (`RUNBOOK.md:96-98`)

The loop retries only the completely empty-checks response. GitHub CLI's `--watch` exits successfully when all *reported* checks have finished without failure; it does not wait for an as-yet-unreported check to appear. If one workflow has registered and passed while the other has not registered, line 158 attempts the merge before both judge and tests have admitted the entry head. Required-check protection can then reject the merge, so the verb refuses instead of continuing its promised wait. The stub models only “no checks” followed by unconditional success and cannot catch partial registration. Verify that both expected checks have reported successful admission before leaving the wait.

Evidence: the installed CLI is v2.101.0; [`checks.go`](https://github.com/cli/cli/blob/v2.101.0/pkg/cmd/pr/checks/checks.go), `populateStatusChecks` and `checksRun`, distinguishes an empty rollup from a nonempty rollup and terminates watch when the latter has no pending checks.

## 4. The watched and merged head is not bound to the entry just pushed

**Location:** `tools/jack:150-158`.

**RUNBOOK sentence:** “Effect: `gh pr checks N --watch` until the judge and the tests have admitted the head that carries the entry, then `gh pr merge N --merge`, which GitHub performs only if they did; then `git pull --ff-only` on `main` and `gh run watch` of `main`'s run.” (`RUNBOOK.md:96-98`)

After pushing the merge-entry commit, the verb retains no expected post-push SHA. Every watch invocation selects the PR by number, and the merge command has no expected-head condition. Another actor can replace the PR head during the wait, including replacing it with a separately admitted proposal that lacks this merge entry. Checks can then succeed for that replacement and `gh pr merge` can merge it. Branch protection verifies the replacement's checks, not that it is the commit this invocation authorised. Record the pushed commit, verify the checks belong to that head, and use GitHub CLI's `--match-head-commit` condition for the final merge. The current stubs never move the head during the watch.

## 5. The new timeout cuts a required part of the verb without textual authority

**Location:** `tools/jack:14`, `153-156`; `tests/test_jack.py:392-402`.

**RUNBOOK sentences:** “Effect: `gh pr checks N --watch` until the judge and the tests have admitted the head that carries the entry, then `gh pr merge N --merge`, which GitHub performs only if they did; then `git pull --ff-only` on `main` and `gh run watch` of `main`'s run.” (`RUNBOOK.md:96-98`) “If a verb cannot be written within the bound, `--dry-run` is cut first, `gh run watch` second and `--remove` third (each printed as a command instead); the verbs and their refusals are not.” (`RUNBOOK.md:170-172`)

After 600 seconds without registered checks, the verb exits with a refusal and delegates the required check wait, merge and pull to printed commands. The text provides neither this deadline nor permission to replace these effects with commands. A head whose checks register after that deadline therefore cannot complete under the documented verb, despite having received no adverse verdict. The new timeout test confirms this departure rather than a stated refusal. Either retain the specified wait or obtain runbook text defining the bounded-wait outcome and its recovery contract.

## Verification

The five merge tests at `tests/test_jack.py:344-402` pass. Separately invoking `judge.judge` on the wait-success fixture before and after `jack merge` confirms finding 1; that invocation of `jack` returns zero, records `gh pr merge 7 --merge`, and leaves remote main unchanged. `tools/jack` has 250 physical lines, so the stated file-size bound is met.
