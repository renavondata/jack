# FIX-20261122: the tests workflow gives its job a git identity

Counsel's text, 22 November 2026, for the sovereign's read (CHARTER A2.10: "Code is written to a text Guy has read"). It changes one file of the trusted base, `.github/workflows/tests.yml`, by his own hand and his push, and nothing else.

**The change.** Under the job `tests`, after `runs-on: ubuntu-latest`, the workflow gains:

```yaml
    env:  # the hosted runner has no git identity; tests and pins that commit or merge need one (FIX-20261122)
      GIT_AUTHOR_NAME: tests
      GIT_AUTHOR_EMAIL: tests@jack.invalid
      GIT_COMMITTER_NAME: tests
      GIT_COMMITTER_EMAIL: tests@jack.invalid
```

The file's SHA-256 goes from `11682f7501ddde948f5e912cbc9e5eee7f2799be5fae1c29e8dcb6f2bbe71f3a` to `06f4bd8fc74f0c457c4acef0197f470029f3a1afc068489843eafdb290d7ab41`. No step, action, trigger or permission changes.

**Why.**
- **The failure.** Since the push that moved the promotion evaluator under `judge/` (log seq 7281, 2026-11-22T18:16:20Z), the `tests` workflow on `main` fails. Run `45054277383` at `20c6b9ae` ran 311 unit tests, and one errored: `tests.test_promotion_judge.Promotions.test_every_entry_commit_including_a_bad_side_branch_is_judged`. Its `git merge -q --no-ff` (`tests/test_promotion_judge.py` line 151) exits 128, because the hosted runner has no git identity. The sibling test at line 172 passes `-c user.name=t -c user.email=t@t`; line 151 does not. The steps after the unit tests did not run.
- **Why nobody saw it before.** The move came by his push, so the workflow never ran on its branch. Every machine that ran the suite before the push had an identity.
- **What it blocks.** Every proposal's `tests` run includes that test, so every proposal fails, and the court has merged nothing since seq 7280 (2026-11-22T17:49:05Z). `judge/status.py` finalises an open forecast as failed at the first entry after its `resolves_by`, so each hour without merges costs the forecasts due in it.
- **Why the trusted base, and not the test.** His push cannot carry a change to the test alone: `tools/jack push` refuses a branch whose trusted-base digest equals `HEAD`'s, with "nothing to push: propose and merge". And no proposal can carry it either. `tests/` is the builder's path (`judge/scope.json`). A builder session is filed only from a template on `main`, and no template there fits a one-line test fix. A new template is counsel's proposal, and like every proposal it fails the `tests` run while `main`'s test fails. A change to the workflow reaches `main` by his push, which does not wait on that run.

**What it does not do.** It changes no test, pin, judge or kernel code. The test stays as the builder wrote it. Making it hermetic, with an identity of its own as line 172 has, is the builder's change, by proposal, once `main` is green. The identity applies to every step of the job, the pins and the simulator included. In git these four variables take precedence over `-c user.name` and `-c user.email`, so on the hosted runner every commit the tests and pins make carries `tests <tests@jack.invalid>`, the ones made with `t` and `t@t` included; no test, pin or judge code reads a commit's author or committer, and the run below passes with them. The `judge` workflow is unchanged.

**Its place in the law.**
- `.github/workflows/` is trusted base (`judge/judge.py`, `TRUSTED`). The change reaches `main` only by his `jack push`, as a `push` entry.
- It changes no scope (`judge/scope.json` is untouched), so it opens nothing.
- It falls after his veto of C2a-prime at seq 7180 and before 2026-11-30T00:00:00Z, so by AMEND-A6 clause 1 and BRIEF-C2a-3 v5 precondition 1 it is not inside C2a-prime's window and is not C2a-3's opening.
- RUNBOOK, *Text before code*: "`main` … is never red by design". This restores it.

**The check, before his read.** Counsel ran every step of the job on `main` at `20c6b9ae`, each under `env -i` with only `PATH`, an empty `HOME` and these four variables, so with no git configuration of any kind:

| step | exit | seconds | result |
|---|---|---|---|
| `python3 -m unittest discover -s tests -t .` | 0 | 522 | 311 tests, OK |
| `python3 pins/run.py` | 0 | 846 | KILLED 158, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0 |
| `python3 judge/selfcheck.py` | 0 | 113 | kernel and kernel2 ok over 7282 entries |
| `python3 harness/diff.py --seeds 300 --b kernel2/check 'spec/vectors/logs/*.jsonl'` | 0 | 198 | no disagreements |
| `python3 tools/count_kernel.py` | 0 | 0 | 450 |

Without the four variables, the one test errors as it does on the runner (the adviser's reproduction, ADVISER.md entry 129).
