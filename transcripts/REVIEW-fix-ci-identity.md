# Cold read of FIX-20261122, by argon (opencode-runner #1232)

The final report of runner #1232 (`google/gemini-4-argon`, read only, no key), as its last comment gives it, from its first line to its verdict. The text read is `transcripts/FIX-20261122-ci-identity.md` at `61ef76a010ab531d0d7b5280390631912c99dfda`.

# Cold Read Report: `transcripts/FIX-20261122-ci-identity.md` (`61ef76a010ab531d0d7b5280390631912c99dfda`)

Reviewed branch head: `origin/fix-ci-identity` at `61ef76a010ab531d0d7b5280390631912c99dfda` (parent `origin/main` at `20c6b9ae1e1d17842b40ef5783b1679920d999db`).
Text under read: `transcripts/FIX-20261122-ci-identity.md` (41 lines).

---

## Answers to Questions

### 1. Verification of Every Statement of Fact in the Text

Every statement of fact in `transcripts/FIX-20261122-ci-identity.md` was checked against `origin/main` (`20c6b9ae1e1d17842b40ef5783b1679920d999db`), `log.jsonl`, and GitHub Actions run `45054277383` (job `137305948144`):

- **Authority and trusted-base status (`CHARTER.md:297`, `judge/judge.py:25`, `RUNBOOK.md:224–227`):**
  - `CHARTER.md:297` (A2.10): `"Code is written to a text Guy has read; questions of what the charter allows are put to Guy as rulings and recorded here."`
  - `judge/judge.py:25`: `TRUSTED = ("kernel/", "kernel2/", "judge/", ".github/workflows/", "SPEC.md")`.
  - `RUNBOOK.md:226–227`: ``"`main` never carries a text its judge and checkers do not implement, and is never red by design."``
- **Hashes before and after (`.github/workflows/tests.yml`):**
  - Before replacement (`origin/main:.github/workflows/tests.yml`, 31 lines): SHA-256 is `11682f7501ddde948f5e912cbc9e5eee7f2799be5fae1c29e8dcb6f2bbe71f3a`.
  - After replacement (36 lines): SHA-256 is `06f4bd8fc74f0c457c4acef0197f470029f3a1afc068489843eafdb290d7ab41`.
- **The failure (`log.jsonl` seq 7281, run `45054277383`, job `137305948144`, `tests/test_promotion_judge.py:151,172`):**
  - `log.jsonl` line 7282 (seq `7281`) is the `push` entry at `ts` `"2026-11-22T18:16:20Z"` with `digest` `"c77b07d7ec4d99298e3b47965aaa427aad358a6103672006d9fabfeb1e3d347b"`, committed at `20c6b9ae1e1d17842b40ef5783b1679920d999db` (`push: move-promotion-judge`).
  - GitHub Actions run `45054277383` (`event: "push"`, `head_sha: "20c6b9ae1e1d17842b40ef5783b1679920d999db"`, `path: ".github/workflows/tests.yml"`, `conclusion: "failure"`) ran job `137305948144`.
  - Job `137305948144` log lines 1921–1936 confirm 311 unit tests ran (`Ran 311 tests in 330.801s`, `FAILED (errors=1)`), with the single error in `tests.test_promotion_judge.Promotions.test_every_entry_commit_including_a_bad_side_branch_is_judged` at `tests/test_promotion_judge.py` line 151:
    ```
    subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmpa26qvsfl/repo', 'merge', '-q', '--no-ff', 'f18bd461600252ccbbe5b281c7f1bf31d7ea4b80', '-m', 'Join histories']' returned non-zero exit status 128.
    ```
  - In `tests/test_promotion_judge.py`:
    - Line 151 calls `gitfix.git(self.repo, "merge", "-q", "--no-ff", bad, "-m", "Join histories")` without `-c user.name=... -c user.email=...` (whereas `harness/gitfix.py:65` `commit_all` passes `"-c", "user.name=t", "-c", "user.email=t@t"`).
    - Line 172 (the sibling test `test_entry_line_anywhere_in_an_ancestors_log_counts_as_an_entry_commit`) calls `gitfix.git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "--no-ff", "-s", "ours", bad, "-m", "Keep valid head but retain the side entry commit")`.
  - Job `137305948144` steps 5–8 (`Pins`, `Judge self-check`, `Simulator sample through both checkers`, `Kernel line count`) all have `"conclusion": "skipped"`.
  - Running `tests.test_promotion_judge.Promotions.test_every_entry_commit_including_a_bad_side_branch_is_judged` under `env -i` with an empty `HOME` and without the four `GIT_*` variables reproduces exit status 128 at line 151; adding the four `GIT_*` variables makes all 15 tests in `tests/test_promotion_judge.py` pass.
- **Why nobody saw it before and what it blocks (`log.jsonl` seq 7280, `judge/status.py:101–109`):**
  - `.github/workflows/tests.yml:5–9` runs only on `pull_request` and `push` to `branches: [main]`, so it did not run on `move-promotion-judge` prior to `jack push`.
  - `log.jsonl` seq `7280` (`2026-11-22T17:49:05Z`, `merge` of proposal `#1324`) is the last `merge` entry on `main`; open proposals `#1326`–`#1332` have remained unmerged behind the failing `tests` check.
  - `judge/status.py:101–109` (`expire` inside `item_process`) finalises any open forecast with `forecast["body"]["resolves_by"] < e["ts"]` as `"expiry"` with `success=False` (`Y = 0`) at the first entry `e` after its `resolves_by`.
- **Why neither a push nor a proposal can carry a fix to the test (`tools/jack:229–230`, `judge/scope.json:4–7`, `transcripts/sessions/README.md:5,22–26`):**
  - `tools/jack:229–230` (`v_push`):
    ```python
    if commit_digest(ROOT, b) == commit_digest(ROOT, "HEAD"):
        refuse("nothing to push: propose and merge")
    ```
    A branch changing only `tests/test_promotion_judge.py` leaves the trusted-base digest equal to `HEAD`'s and is refused by `jack push`.
  - `judge/scope.json:4–7`: `"tests/"` is in `parties.builder` (`["sim/", "harness/", "tests/", "tools/", "transcripts/", "log.jsonl"]`) and not in `parties.counsel` or `parties.reviewer`.
  - `transcripts/sessions/README.md:5,22–26` and `transcripts/sessions/build.md:17`: builder sessions are dispatched from templates on `origin/main` under `transcripts/sessions/`. `build.md` reads `transcripts/windows/{WINDOW}.json` (where only `C2c-1.json` exists on `main`, printing `not yet`, which restricts `build.md` to pre-build branches that run no `tools/jack` verb), and the other builder templates on `main` are fixed to specific tasks (`due-resolve.md`, `stream-resolve.md`, `evidence.md`, `repropose.md`, `assemble.md`, `move-promotion-judge.md`, `c2a-prime-*`, `c2b-*`).
  - A proposal by counsel to add a new template under `transcripts/sessions/` cannot touch `tests/` (`party_scope`), so its own `tests` workflow run fails on `tests/test_promotion_judge.py:151` and `tools/jack:134–145` (`admitted`) refuses to merge it.
  - By contrast, `.github/workflows/tests.yml` is in `TRUSTED`, so changing it changes `commit_digest` and reaches `main` via `jack push`, which runs `the_check(tmp)` locally (`tools/jack:235`) and pushes `main` without waiting on a GitHub Actions run.
- **Check table counts (`log.jsonl`, `pins/pins.py`, `tools/count_kernel.py`):**
  - `log.jsonl` has `7282` lines (seqs `0`..`7281`); `pins/pins.py` has `158` mutants across `107` pins; `python3 tools/count_kernel.py` outputs `total 450`.

### 2. Verification of the Replacement on `.github/workflows/tests.yml`

Comparing `origin/main:.github/workflows/tests.yml` with the copy after the replacement:
- The diff adds exactly 5 lines after line 14 (`    runs-on: ubuntu-latest`) and before line 15 (`    steps:`):
  ```yaml
      env:  # the hosted runner has no git identity; tests and pins that commit or merge need one (FIX-20261122)
        GIT_AUTHOR_NAME: tests
        GIT_AUTHOR_EMAIL: tests@jack.invalid
        GIT_COMMITTER_NAME: tests
        GIT_COMMITTER_EMAIL: tests@jack.invalid
  ```
- Parsed with `yaml.safe_load`, the resulting structure is identical to `origin/main:.github/workflows/tests.yml` everywhere except for adding `jobs["tests"]["env"]` equal to `{'GIT_AUTHOR_NAME': 'tests', 'GIT_AUTHOR_EMAIL': 'tests@jack.invalid', 'GIT_COMMITTER_NAME': 'tests', 'GIT_COMMITTER_EMAIL': 'tests@jack.invalid'}` at the level of job `tests`.
- All steps, actions, triggers (`on.pull_request`, `on.push`) and `permissions` (`contents: read`) are unchanged.
- Its SHA-256 is `06f4bd8fc74f0c457c4acef0197f470029f3a1afc068489843eafdb290d7ab41`.

### 3. Effect of the Job Environment Identity on Tests, Pins, Self-Check, and Simulator

- **Precedence:** In git, `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, and `GIT_COMMITTER_EMAIL` in the process environment take precedence over `-c user.name=... -c user.email=...` and over `GIT_CONFIG_GLOBAL` (such as `harness/gitfix.py:36,65`, `tests/test_judge.py:489,526,571`, `tests/test_promotion_judge.py:160,172,233`, `tests/test_evaluator_move.py:54`, `tests/test_push_gate.py:21`, and `tests/test_jack.py:141–143`). As the text states, every commit created during the job carries `tests <tests@jack.invalid>`.
- **No code reads commit author or committer:**
  - `judge/judge.py` reads only tree modes/blobs (`ls-tree`, `show`), diff paths (`diff`, `diff-tree`), and commit parent topology (`rev-parse`, `rev-list`, `merge-base`). As `judge/judge.py:30` notes: `# the trailer's parties, for tools/jack; the judge reads keys, not trailers`.
  - `judge/status.py` reads blobs (`show`), commit topology (`rev-list --parents`, `rev-list --first-parent`), and in `carrying_commit` (`judge/status.py:329`) inspects `git cat-file -p <sha>` only for `ln.startswith("parent ")` to detect shallow history boundaries.
  - `tools/jack` reads only commit subjects (`--format=%s`, line 125), `Proposer:` trailers from commit messages (`--format=%(trailers:key=Proposer,valueonly)`, line 25), and commit hashes/ancestry (`rev-parse`, `rev-list`, `merge-base`, `log --format=%H`).
  - No test or pin reads `%an`, `%ae`, `%cn`, `%ce`, or commit author/committer headers.
- **No test or pin compares newly created commit hashes against fixed hashes across runs:**
  - Every newly created commit in a fixture repository (`harness/gitfix.py`, `tests/*`, `pins/*`) already gets the live wall-clock timestamp as its author/committer date (`GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` are not pinned), so its SHA-1 changes on every run anyway; fixtures capture `git rev-parse HEAD` dynamically and pass it into signed `proposal`/`merge` entries at runtime.
  - `pins/replay.py` and `tests/promotion_replay_spot.py` check fixed commit hashes from `spec/vectors/promotion-replay.json`, which are existing historical commits on `main`'s first-parent chain checked out from the repository (`git clone --shared --no-checkout`), never newly committed objects. (`SPEC.md:514–515` mentions committer time only for the first four historical commits of `main` that hold no `log.jsonl`, which are pre-existing commits in git history.)
  - `judge/selfcheck.py`, `harness/diff.py`, and `tools/count_kernel.py` create no git commits at all.

### 4. Interaction with the Judge, the Promotion Evaluator, and Windows

- **Trusted-base digest (`judge/judge.py:25,72–77,375–378`, `tools/jack:229–230,234,242`):**
  - `.github/workflows/tests.yml` is under `.github/workflows/` (`TRUSTED`). The replacement changes the trusted-base digest (`judge.digest`) from `c77b07d7ec4d99298e3b47965aaa427aad358a6103672006d9fabfeb1e3d347b` to `e1767212c648fd9e73c60b031abf622b0fd7f79f73bcf410914c76215ec5b188`.
  - Because neither `kernel/` nor `kernel2/*.go` (`tools/jack:12`, `SOURCES`) changes, `needs_run` (`tools/jack:234`) is `False`. `jack push` appends a `push` entry with the new `digest`, satisfying SPEC §10.11 (`judge/judge.py:375–378`).
  - `installing_push` (`judge/judge.py:212–237`) returns the *first* qualifying push after seq 5564 (`seq 7281`) and is unaffected by a subsequent `push` at seq 7282.
- **Workflow run matching (`judge/status.py:24,226–229`, `tools/jack:14,266`, `tools/clerk.py:48`):**
  - `WORKFLOW = ".github/workflows/tests.yml"`, the workflow `name: tests`, the job name `tests`, and the `push`/`pull_request` triggers on `main` are unchanged, so `run_verified`, `tools/clerk.py`, and `jack merge`/`jack decision promote` match runs identically.
- **`item_process` and `late_reports` (`judge/status.py:84–140`):**
  - In `item_process` (`judge/status.py:111–112`), `repair = royal and typ not in ("genesis", "key", "amend", "push", "proposal") and not (typ == "decision" and body["kind"] != "fix")`. Because `typ == "push"`, `repair` is `False`: the push is not an on-log repair, adds no taint to open forecasts, and appends nothing to `late_reports`.
- **No window opened and outside C2a-prime's window (`judge/scope.json`, `transcripts/AMEND-A6.md:14–19`, `transcripts/BRIEF-C2a-3-draft.md:62,75`):**
  - `judge/scope.json` is untouched, so `push_read_gate` (`tools/jack:180–183`) returns immediately (and refuses if `--opens` is given).
  - `amend` A6 was entered at seq `7179` (`activate_at: 7180`), and the sovereign entered `decision` `veto` `C2a-prime` at seq `7180` (`2026-11-22T11:44:05Z`, at `activate_at`).
  - Under `transcripts/AMEND-A6.md:14–19` (clause 1), C2a-prime ended, as failed, at seq `7180`, while its stated end stays `2026-11-30T00:00:00Z`.
  - Under `transcripts/BRIEF-C2a-3-draft.md:62` (precondition 1), C2a-prime's end is `"the earlier of that instant [2026-11-30T00:00:00Z] and a decision veto naming C2a-prime at or above AMEND-A6's activate_at. A push after such a veto and before 2026-11-30T00:00:00Z, such as the move's, is not inside the window and opens nothing (§The window)."` And under `transcripts/BRIEF-C2a-3-draft.md:75`, `"C2a-3 opens at the first push entry whose ts is after 2026-11-30T00:00:00Z, C2a-prime's stated end."`

### 5. What the Sovereign Should Know Before Reading and Pushing

See Findings 1–3 below (all `NOTE`s; none is a defect in the text or the replacement).

---

## Findings

1. **NOTE** — `tools/jack:231–232`, `origin/fix-ci-identity` (`61ef76a010ab531d0d7b5280390631912c99dfda`):
   `tools/jack`'s `v_push` checks that every commit in `origin/main..fix-ci-identity` carries a filled `Proposer:` trailer:
   ```python
   if bare := [s[:12] for s in git("rev-list", f"origin/main..{b}").split() if not trailer(s)]:
       refuse(f"commits on {b} without a filled Proposer: trailer: {', '.join(bare)}")
   ```
   Commit `61ef76a010ab531d0d7b5280390631912c99dfda` already carries `Proposer: counsel claude-opus-5-5 session_01VpB3Tknxi9JkERuANTGHDk`. When the sovereign commits the replacement to `.github/workflows/tests.yml` by hand on `fix-ci-identity`, that commit must likewise carry a filled `Proposer:` trailer (e.g. `-m "Proposer: guy guy-master"`), and `jack push` must be invoked without `--opens` (`tools/jack:182`).

2. **NOTE** — `judge/status.py:101–109` (`expire` in `item_process`) and `log.jsonl` seqs `7253`–`7264`:
   As `transcripts/FIX-20261122-ci-identity.md` line 21 notes (`"judge/status.py finalises an open forecast as failed at the first entry after its resolves_by, so each hour without merges costs the forecasts due in it"`), 12 open forecasts (seqs `7253`–`7258` due `2026-11-22T22:00:00Z` and seqs `7259`–`7264` due `2026-11-22T23:00:00Z`, whose resolutions are waiting in unmerged PRs `#1330` and `#1332`) are already past their `resolves_by`. When the `push` entry is appended to `log.jsonl`, `expire(e)` will finalise any forecast whose `resolves_by < e["ts"]` as `"expiry"` (`Y = 0`), just as any other entry appended at that instant would.

3. **NOTE** — `judge/judge.py:343–344,349–350`:
   Once `jack push` lands on `main`, currently open proposal PRs (`#1326`–`#1332`) branched from `20c6b9ae` will differ from `main` on `.github/workflows/tests.yml` (`trusted_path`) and `log.jsonl` (`prefix_broken`), and still hold the pre-fix `.github/workflows/tests.yml` on their branches. They will become green and mergeable once re-proposed onto the new `main` via `transcripts/sessions/repropose.md`.

VERDICT: PASS
