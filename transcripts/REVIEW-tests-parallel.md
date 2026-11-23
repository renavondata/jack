# Read of FIX-20261123-tests-parallel's workflow, by the sovereign's adviser

The adviser's pre-read of `.github/workflows/tests.yml` as this push makes it (SHA-256 `edae388d9affbbedbde0963ebbe265b79f23f7a1d992424e7f5f8aff2c1d8c47`), from `ADVISER.md` entry 157 (adviser, `claude-fable-5-2`, 2026-11-23T06:15Z) on branch `adviser/notes` at `be901915be18547428c0ba8943884c97ab254e9b`, lines 4792 to 4823, unchanged. The adviser audits for the sovereign and is not a party of the court. It read the workflow at commit `244b25db` and the text as it then stood (SHA-256 `9c83466ba77141afb9db4cb327fd1426bbb25c9dd216fe70450e7c236945b921`); the text's section *The evidence before the push* was rewritten afterwards, and the workflow was not changed.

**The pre-read of `agent/tests-parallel`: it holds.**
- **The branch** is one commit on `main`, two files, both hashes as entry 155 gives. `counsel/tests-parallel` is the same commit.
- **The workflow** has four jobs and six `run` lines. The five commands are `main`'s, each once. No working job has an `if`, and the file has no `continue-on-error`, `timeout-minutes` or `concurrency`. The gate needs the three, runs `if: always()`, and takes the results through `env`.
- **Against `push-c2b-9000`'s file** it differs in the comment, the identity, `fetch-depth: 0` in each job, and the gate's `env`. Nothing else.
- **The three readers the text names** read what it says: `judge/status.py` lines 24 and 226 to 228, `tools/jack` lines 14 and 140, SPEC line 507. Line 140 keys the rollup by check name, and the gate keeps `tests`.
- **BRIEF-C2a-3 v5 names no workflow,** so the next opening does not depend on this file's shape.

```sh
git diff --stat origin/main origin/agent/tests-parallel | tail -1; git show origin/agent/tests-parallel:.github/workflows/tests.yml | grep -c -E 'continue-on-error|timeout-minutes|concurrency'          # 2 files changed; 0
diff <(git show origin/main:.github/workflows/tests.yml | grep 'run: python3' | sed 's/^ *//' | sort) <(git show origin/agent/tests-parallel:.github/workflows/tests.yml | grep 'run: python3' | sed 's/^ *//' | sort)   # no output
diff <(git show origin/push-c2b-9000:.github/workflows/tests.yml) <(git show origin/agent/tests-parallel:.github/workflows/tests.yml); git show origin/main:transcripts/BRIEF-C2a-3-draft.md | grep -c -i -E 'tests\.yml|workflow'   # the four differences; 0
```

**Note 1: two readers the text does not name. Both see what they saw.**
- **The herald** reads the workflow runs named `judge` and `tests` by their conclusion (the runner's `herald.yml`, lines 63 and 80).
- **`main`'s branch protection** requires the checks `judge` and `tests`, strict. The gate's name meets it. OPINION, from GitHub's documentation and not tested here: a skipped required check counts as passed, so the gate's `if: always()` is what keeps a failed job from passing. The reviewer's third check covers the gate.

```sh
git -C <opencode-runner> show origin/main:.github/workflows/herald.yml | sed -n '63p;80p'; gh api repos/renavondata/jack/branches/main/protection --jq '.required_status_checks|{contexts,strict}'
```

**Note 2: the evidence pull request cannot show `sample` green, as the text says. Here is that job alone.**
- I ran its two commands in a fresh clone of `main` `4112cc49`, with nothing run before them. The environment was `env -i` with `PATH`, an empty `HOME` and the workflow's four identity variables.
- The self-check exited 0 in 127 s, with kernel and kernel2 both ok over 7314 entries. The sample exited 0 in 221 s, with 351 logs and no disagreement.
- This is my machine, not the hosted runner.
- **So R13 is met for this push** once the evidence pull request shows `unit` and `pins` green on the hosted runner at this workflow's hash. Each job will then have passed in a checkout of its own. His paste need not run the three jobs again on steel.

```sh
git clone -q <jack> /tmp/fresh && cd /tmp/fresh && git checkout -q --detach 4112cc49 && R="env -i PATH=$PATH HOME=/tmp/empty GIT_AUTHOR_NAME=tests GIT_AUTHOR_EMAIL=tests@jack.invalid GIT_COMMITTER_NAME=tests GIT_COMMITTER_EMAIL=tests@jack.invalid"
$R python3 judge/selfcheck.py; $R python3 harness/diff.py --seeds 300 --b kernel2/check 'spec/vectors/logs/*.jsonl' | tail -3
```
