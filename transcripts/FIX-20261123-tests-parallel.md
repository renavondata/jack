# FIX-20261123-tests-parallel: the tests workflow runs its five steps in three jobs side by side

Counsel's text, 23 November 2026, for the sovereign's read (CHARTER A2.10: "Code is written to a text Guy has read"). It changes one file of the trusted base, `.github/workflows/tests.yml`, by his own hand and his push, and nothing else. It brings forward, now and alone, the second of the two trusted-base changes that `transcripts/BRIEF-C2b-draft.md` §Scope gives C2b's opening push.

**The change.** The workflow's one job `tests`, which runs five steps one after another, becomes four jobs:
- `unit`: the unit tests, then the kernel line count;
- `pins`: the pins;
- `sample`: the judge self-check, then the simulator sample;
- `tests`: the gate, which `needs` the other three, runs `if: always()`, and fails unless all three results are `success`.

Each of the first three jobs has today's two setup steps: `actions/checkout` at the same pinned commit with `fetch-depth: 0`, and `actions/setup-python` at the same pinned commit with Python 3.12. The five steps keep their names and their commands, character for character, and each runs exactly once. The git identity of FIX-20261122 moves from the job to the workflow's top level, so every job has it. The name, the triggers and the permissions are unchanged. The file's SHA-256 goes from `06f4bd8fc74f0c457c4acef0197f470029f3a1afc068489843eafdb290d7ab41` to `edae388d9affbbedbde0963ebbe265b79f23f7a1d992424e7f5f8aff2c1d8c47`. The file in full is on `agent/tests-parallel`.

**Why.**
- **The job is too slow for the court.** Since the push of seq 7281 the `tests` job on `main` takes 23 to 28 minutes. In today's two green runs, the unit tests took 421 and 511 s, the pins 690 and 802 s, and the self-check with the sample 261 and 312 s (ADVISER.md entries 140 and 150).
- **Every proposal waits for it twice:** once on its own head, and once on the head that carries its merge entry. New forecast streams are paused until the job takes 15 minutes or less (ADVISER.md entry 146).
- **Run side by side, the job takes as long as its longest job.** That is the pins today, about 12 to 14 minutes. With FIX-20261123-pins-parallel, which runs the pins on the hosted runner's four cores, it is the unit tests, about 8 to 10. No test or pin changes for it.
- **C2b's brief already chose this design** for the same reason, measured on 2 November at 8 m 17 s serial (BRIEF-C2b-draft §Scope). It has waited for C2b's opening push. The court cannot carry its hourly work until then.

**What it does not do.**
- It changes no test, pin, judge or kernel code, and no command a step runs.
- `judge.yml` is unchanged.
- The workflow still checks out the whole history (SPEC §10 item 15's paragraph: "The installing push makes both workflows that run the judge (`judge.yml` and `tests.yml`) check out the whole history").
- **Every reader of the run sees what it saw.** The workflow run still has one conclusion, `success` only if every job succeeds. W3 and `judge/status.py` read that run by its path, event, branch, commit and conclusion (SPEC line 507; `judge/status.py` line 24), not by job. The check that `tools/jack` waits for is still named `tests` (`CHECKS`, line 14): it is the gate job's name.
- The three working jobs add checks named `unit`, `pins` and `sample` to every pull request. Nothing waits for them by name.

**Its place in the law.**
- `.github/workflows/` is trusted base (`judge/judge.py`, `TRUSTED`). The change reaches `main` only by his `jack push`, as a `push` entry.
- It changes no scope (`judge/scope.json` is untouched), so it opens nothing.
- It falls after his veto of C2a-prime at seq 7180 and before 2026-11-30T00:00:00Z. So by AMEND-A6 clause 1 and BRIEF-C2a-3 v5 precondition 1, it is not inside C2a-prime's window and is not C2a-3's opening, as FIX-20261122 and the move were not.
- `BRIEF-C2b-draft.md` is a draft, counsel's. Once this push lands, its §Scope names as an opening-push change a workflow that `main` already has. Counsel will amend the draft so that its opening push carries the cap alone, before the draft is put to him. Its pin `workflow_steps_preserved` stays with C2b's window code.

**The evidence before the push.**
- **A run of the new workflow on the hosted runner.** Counsel opens a pull request from the push branch through the courier, as BRIEF-C2b's opening did with PR #125.
  - The `judge` check refuses it at `trusted_path`, as it must.
  - `tests.yml` runs on it with the new definition. `unit` and `pins` must pass. `sample` fails at the self-check's `trusted_base_unrecorded`, which every push branch shows until its push entry records the digest (BRIEF-C2b-draft §Scope, on PR #125).
  - Counsel records each job's time, then closes the pull request as stale.
- **A reviewer's cold read of this text and the branch,** committed on the push branch as `transcripts/REVIEW-tests-parallel.md`. It checks:
  - that the diff from `main` is this file and the review, and nothing else;
  - that each of the five commands appears exactly once, unchanged, and behind no condition or `continue-on-error`;
  - that the gate fails unless all three results are `success`.
- **R13's run before his push.** On steel, run every step of the three jobs under `env -i`, with only what the hosted runner has.
