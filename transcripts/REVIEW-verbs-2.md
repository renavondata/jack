Model ID: `google/gemini-4-argon`

# Second Cold Review of `tools/jack` Against `RUNBOOK.md`

## 1. Test Execution and Line-Count Bound

- **Unit tests (`python3 -m unittest tests.test_jack`):** Ran 34 tests in 43.176s — `OK`.
- **Line-count bound (`RUNBOOK.md:155-160`, counted as `tools/count_kernel.py:16-17` counts via `sum(1 for _ in f)` in binary mode):**
  - `tools/jack`: **245 lines** (limit: **250 lines**).
  - Imports: Python standard library (`argparse, contextlib, datetime, functools, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time`) plus `judge.judge`, `kernel` (`check`, `log`), and `tools` (`entry`, `digest`) (`tools/jack:5-10`).
  - `--dry-run` and `gh run watch` are cut as explicitly permitted by `RUNBOOK.md:158-160` (`gh run watch` is printed as a command at `tools/jack:67-69`).

---

## 2. Verification of the Eight Findings from `transcripts/REVIEW-verbs.md`

### Finding 1 — `JACK_SEEDS` environment variable bypassing the 100,000-seed requirement
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_no_environment_variable_changes_the_seed_count` (`tests/test_jack.py:166-169`) loads `tools/jack` with `JACK_SEEDS="0"` in the environment and asserts `jack.SEEDS == 100000` (and test runs now patch `jack.SEEDS = 12` in-process at `tests/test_jack.py:41`). On the old `tools/jack` (`SEEDS = int(os.environ.get("JACK_SEEDS", "100000"))`), `JACK_SEEDS="0"` yielded `0`, failing the assertion.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:30-31` states: *"No environment variable changes what a verb requires or does. `JACK_KEY` names a key and nothing else; the tests patch constants in-process, never through the environment."* `tools/jack:11` sets `SEEDS = 100000` as a constant, and `os.environ` is read nowhere else except for `JACK_KEY` (`tools/jack:223`).

### Finding 2 — Accepting a pre-existing run of record from `BRANCH`, unverified per-part `logs` count, and `commit: null` handling
- **Test that would fail on the old behaviour:** **Yes.**
  1. `Jack.test_push_makes_the_run_of_record_itself_never_accepting_one_from_the_branch` (`tests/test_jack.py:409-423`) commits 12 valid-looking `transcripts/diff-12-20261019T0000Z-part00..11.json` files on `tb` and asserts that `jack push` still generates 12 new run parts (`len(made) == 12`) and records their SHA-256 in `push.record`. On the old behaviour, `existing_run` accepted the branch's files without running `harness/diff.py`, so `len(made)` would be `0`.
  2. `Jack.test_push_refuses_a_run_whose_parts_are_not_of_the_branch_head_or_not_their_range` (`tests/test_jack.py:424-438`) tests three sub-cases (`"other"` with `"commit": "0" * 40`, `"null"` with `"commit": None`, and `"uneven"` where part 0 has 2 logs and part 1 has 0 logs while still summing to 12) and asserts refusal with `"the run of record is not"`. On the old `valid_run(parts)`, all three were accepted.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:107-113` requires that the run of record be made in the temporary worktree by the verb itself (*"never accepted from BRANCH"*) and that *"every part must report `commit` equal to BRANCH's head, `logs` equal to the length of its range, no disagreement and nothing uncompared, with the twelve ranges contiguous from 0 to 100,000."* `tools/jack:157-174, 188` removes `existing_run`, always runs `make_run(tmp, head)` when `needs_run` is true, and verifies in `valid_run(parts, head)` (`tools/jack:159-160`) that `len(reps) == 12`, `[e[0] for e in edges] == [0] + [e[1] for e in edges[:-1]]`, `edges[-1][1] == SEEDS`, and for every part `r["commit"] == head and r["logs"] == r["seeds"][1] - r["seeds"][0] and r["disagreements"] == [] == r["uncompared"]`.

### Finding 3 — Empty review file (`--review FILE` with 0 bytes) treated as `--review none`
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_push_review_of_an_empty_file_hashes_the_empty_file` (`tests/test_jack.py:439-448`) passes a 0-byte `REVIEW-empty.md` to `jack push tb --review` and asserts that `"WARNING"` is not in `stderr`, `body["review"] == hashlib.sha256(b"").hexdigest()`, and `transcripts/REVIEW-empty.md` is committed on `HEAD`. On the old behaviour (which tested truthiness of `review = b""`), all three assertions would fail.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:113-115` specifies: *"`--review FILE` is copied to `transcripts/` and its SHA-256 is the entry's `review`, an empty file included; `--review none` records 64 zeros and prints a warning that this push was not read."* `tools/jack:186, 189-195` sets `review = None if a.review == "none" else open(a.review, "rb").read()` and tests `review is None`.

### Finding 4 — `jack amend` falsiness of `--activate-at 0` and exact dict equality on `transmute` decision body
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_amend_takes_activate_at_as_given_and_counts_a_transmute_with_an_extra_member` (`tests/test_jack.py:532-544`) appends a `transmute` decision carrying an extra `"note"` member, verifies that `jack amend A3 text --activate-at 0` is not refused with `"transmute first"` and is instead refused by the kernel (`activate_at <= seq`) rather than silently defaulting to `seq + 1`, and then verifies admission with `--activate-at 99`. Both the extra-member check and the `--activate-at 0` check would fail on the old behaviour.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:132-135` requires a valid `decision` of kind `transmute` with subject `ID` in the log and `activate_at: N as given, the entry's seq + 1 when omitted`. `tools/jack:209` checks `a.id not in a.state.transmuted` (from `kernel.check`'s folded state), and `tools/jack:218` uses `len(a.lines) + 1 if a.activate_at is None else a.activate_at`.

### Finding 5 — `principal` containing newlines or invalid tokens corrupting the `Proposer:` trailer paragraph
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_a_trailer_is_filled_only_with_a_party_and_a_key_id` (`tests/test_jack.py:174-180`) tests `jack decision` with `nl-1` (whose `principal` in genesis is `"builder\n\nother"`) and asserts refusal with `"is not a filled trailer"`, and tests `jack key` with `principal` in `("builder\n\nother", "Re Viewer", "x<y", "")` asserting refusal with `"principal ... is not [a-z0-9_-]+"`. On the old behaviour, both `jack decision` with `nl-1` and `jack key` with `"builder\n\nother"` or `"Re Viewer"` succeeded.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:27-29` defines a filled trailer as having two fields where the first is one of `SPEC §10.7`'s five party names and neither contains `<`, refusing anything else when written or read; `RUNBOOK.md:62` also requires `jack key` to refuse a `principal` that is not `[a-z0-9_-]+`. `tools/jack:24, 45-46` enforces `filled()` on the signer's trailer in `begin()`, and `tools/jack:113` enforces `re.fullmatch("[a-z0-9_-]+", a.principal)` in `v_key`.

### Finding 6 — Failure after a main verb's first effect leaving `main` fast-forwarded or `CHARTER.md` / `transcripts/` dirty
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_any_failure_after_a_main_verbs_first_effect_returns_main_to_origin_main` (`tests/test_jack.py:493-505`) stubs `ssh-keygen` with `SILENT` (exiting 0 without creating `.sig`, so `entry.assemble` raises `FileNotFoundError`, an `OSError`) and runs `jack push tb --review review` and `jack amend A3 text`. It asserts both refuse with `"git reset --hard origin/main"` and leave `HEAD == origin/main` and `CHARTER.md` and `transcripts/` clean. On the old behaviour, `effect` ran outside `main_ending`'s `try` block and `OSError` was not caught by `main_ending`, leaving `main` fast-forwarded and files modified/untracked.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:44-46` states: *"Any failure after a main verb's first effect — a failed self-check, a refused entry, an error of any kind — returns `main` to `origin/main` with `git reset --hard origin/main`, removes the files the verb placed, and prints the refusal; nothing was pushed."* `tools/jack:71-82` executes `body = effect()` inside `main_ending`'s `try` block and catches `BaseException`, running `git("reset", "-q", "--hard", "origin/main")` and `git("clean", "-fdq", "--", "transcripts/")` before refusing.

### Finding 7 — `jack spec_conflict` not retitling an existing open PR for the branch
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_spec_conflict_retitles_the_branch_s_open_pr` (`tests/test_jack.py:321-329`) stubs `gh pr list` to return `"5\n"`, runs `jack spec_conflict --section "RUNBOOK merge" --text cannot`, and asserts `gh pr edit 5 --title "spec_conflict: RUNBOOK merge"` was called. On the old behaviour, `gh pr edit` was never called.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:83-84` states: *"opens a pull request titled `spec_conflict: <section>` — or, if the branch already has one, retitles it so"*. `tools/jack:85-91, 131` passes `retitle=True` from `v_spec_conflict` to `branch_ending`, which runs `retitle and n and run("gh", "pr", "edit", n, "--title", title)`.

### Finding 8 — `trailer(rev)` in `merge` and `push` accepting non-filled `Proposer:` trailers
- **Test that would fail on the old behaviour:** **Yes.** `Jack.test_push_and_merge_read_only_filled_trailers` (`tests/test_jack.py:471-482`) tests commits with `"Proposer: x"`, `"Proposer: <party> <key_id>"`, `"Proposer: claude builder-1"`, and `"Proposer: builder b-1 extra"` against both `jack push` and `jack merge`, asserting refusal on each. On the old behaviour (`trailer(rev)` checking only non-empty `.split()`), all four were accepted.
- **Does the tool now do what the contract says?** **Yes.** `RUNBOOK.md:27-29, 91-92, 106` requires a filled `Proposer:` trailer (two fields, party in `SPEC §10.7`'s five names, no `<`) when read by `merge` and `push`. `tools/jack:24-25, 145, 184` validates commit trailers via `filled()`.

---

## 3. Adversarial Audit of the New `tools/jack`

- **Forbidden effects:** `--admin` and `--force` are refused on any argument before dispatch (`tools/jack:234-235`); `push()` (`tools/jack:27-29`) refuses any `+` or `:` refspec and any non-fast-forward push without retrying; no verb creates a tag, deletes a remote branch, or rewrites a commit; every push to `main` goes through `main_ending` (`tools/jack:71-82`) after `judge/selfcheck.py` succeeds.
- **Required effects and preconditions:** Every verb fetches `origin`, checks for a clean working tree, non-detached HEAD, and the required branch (`main` vs branch), validates the signing key against the log's declared keys before signing, signs via `ssh-keygen -Y sign -f KEY -n core-entry`, assembles via `tools/entry.py` (which checks admission with `kernel.check`), and performs the exact git/GitHub effects specified in `RUNBOOK.md`.
- **Knobs (arguments, environment, files on `BRANCH`):** No environment variable other than `JACK_KEY` is read; `SEEDS` is fixed at `100000`; `jack push` always builds `kernel2/check` and runs `harness/diff.py` twelve ways in a temporary worktree when `SOURCES` differ from `main`, never accepting pre-existing transcripts from `BRANCH`.
- **New findings:** None.

VERDICT: implements RUNBOOK
