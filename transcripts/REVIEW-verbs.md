Model ID: `google/gemini-4-argon`

# Cold Review of `tools/jack` Against `RUNBOOK.md`

## 1. Test Execution and Line-Count Bound

- **Unit tests (`python3 -m unittest tests.test_jack`):** Ran 26 tests in 31.764s — `OK`.
- **Line-count bound (`RUNBOOK.md:146-150`, counted as `tools/count_kernel.py:16-17` counts via `sum(1 for _ in f)` in binary mode):**
  - `tools/jack`: **249 lines** (limit: **250 lines**).
  - Imports: Python standard library (`argparse, contextlib, datetime, functools, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time`) plus `judge.judge`, `kernel` (`check`, `log`), and `tools` (`entry`, `digest`) (`tools/jack:4-9`).
  - `--dry-run` is cut as explicitly permitted by `RUNBOOK.md:148-150` ("If a verb cannot be written within the bound, `--dry-run` is cut first and `gh run watch` second (printed as a command instead); the verbs are not.").

---

## 2. Contract Clauses: Preconditions, Effects, and Refusals (`yes` / `no` and `tools/jack` lines)

### Common to every verb (`RUNBOOK.md:12-52`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Setup | "The repository root is the directory above `tools/`; the log is `log.jsonl` there." | **yes** | `5`, `10` |
| Effect | "A verb acts on the log of the working copy it runs in, or of a temporary worktree it makes and removes (`merge`, `push`)." | **yes** | `10`, `50`, `104-109`, `149-151`, `195`, `202` |
| Precondition / Setup | "`--key PATH` names the private key; default `$JACK_KEY`, else `~/.ssh/id_ed25519`." | **yes** | `227` |
| Precondition / Effect | "The party is never an argument: the verb reads the matching `pubkey` from the keys declared in the log and takes its `principal` as the entry's `proposer` and as the `Proposer:` trailer's party." | **yes** | `36-42`, `54`, `63`, `229-236` |
| Refusal | "A key the log does not declare is refused before signing." | **yes** | `38-40` |
| Effect | "`ts` is the clock, UTC, `YYYY-MM-DDTHH:MM:SSZ`. The verb reads the clock; the kernel never does." | **yes** | `51` |
| Effect | "`ssh-keygen -Y sign -f KEY -n core-entry` over the canonical message (SPEC §6); the master key prompts for its passphrase, party keys do not." | **yes** | `53-55` |
| Precondition / Effect / Refusal | "Assembly is `tools/entry.py`'s: the line is appended only if `kernel.check` admits the log with it." | **yes** | `53-59` |
| Effect | "A verb's commit message is `<type>: <summary>` — `key: <KEY_ID>`, `proposal: <title>`, `spec_conflict: <section>`, `merge: #<N>`, `push: <BRANCH>`, `decision: <KIND> <SUBJECT>`, `amend: <ID>` — an optional body, and as its **last paragraph** `Proposer: <party> <key_id>`." | **yes** (see Finding 5) | `41-42`, `61-63`, `120-121`, `127`, `132`, `150`, `202`, `210`, `223` |
| Refusal | "A trailer containing `<` is refused." | **yes** | `43-44` |
| Effect | "Every verb begins with `git fetch origin`." | **yes** | `30`, `112`, `124`, `131`, `136`, `184`, `208`, `213` |
| Precondition / Refusal | "Main verbs require HEAD to equal `origin/main`; branch verbs require the branch to contain `origin/main`." | **yes** | `45-48` |
| Precondition / Refusal | "Every verb refuses if `git status --porcelain` lists anything but the files the verb itself stages;" | **yes** | `31-32` |
| Precondition / Refusal | "refuses on a detached HEAD in the working copy it is run in (its own temporary worktrees are detached by design);" | **yes** | `33`, `106` |
| Precondition / Refusal | "refuses on `main` for branch verbs and off `main` for `merge` and the main verbs." | **yes** | `34-35`, `112`, `124`, `131`, `136`, `184`, `208`, `213` |
| Effect | "`--dry-run` prints the entry it would sign and the effects it would perform, and does nothing; for `merge` and `push` it prints the preconditions it would evaluate and makes no worktree." | **no** (cut per `RUNBOOK.md:148-150`) | `3` |
| Refusal | "Refused in code, always: `--admin`; `--force` or `+` refspecs; deleting any remote branch; creating a tag; rewriting any commit — a verb only appends commits, and a push that is not a fast-forward is a refusal, never a retry with force." | **yes** | `25-27`, `63`, `155`, `185`, `196`, `238-239` |
| Effect | "Main verbs (`key`, `decision`, `amend`, `push`) run on `main` and end the same way: commit, `judge/selfcheck.py`, `git push origin main`, then `gh run watch` of the run the push started, printing its result." | **yes** | `65-73`, `75-86` |
| Refusal / Effect | "A failed self-check undoes the verb's commits with `git reset --hard origin/main` and prints the refusal; nothing was pushed." | **yes** (see Finding 6) | `80-84`, `243-245` |
| Effect | "Where the effect precedes the entry (`push`: the fast-forward, then the entry), both commits go up in one push, so the remote never shows one without the other." | **yes** | `85`, `196-202` |
| Effect | "`merge` runs on `main` but appends its entry to the proposal's branch, as SPEC §10.6 has it, and its effect is GitHub's merge, performed only after the judge has admitted the entry; it has no self-check and no undo, because nothing it does reaches `main` except through the judge." | **yes** | `136`, `149-156` |
| Effect / Refusal | "Branch verbs (`proposal`, `spec_conflict`) never touch `main` and run no self-check. If the push or the pull request fails after their commit, the verb prints the two commands that finish the act and undoes nothing; the commit is lawful as it stands." | **yes** | `88-98`, `124-133` |
| Effect | "Every act is an entry; every piece of evidence an entry relies on is referenced from it by hash (`push.digest`, `push.review`, `push.record`); files under `transcripts/` are evidence, never the record. A builder's objection is a `spec_conflict` entry, not a note." | **yes** | `130-133`, `197-202` |

---

### 1. `jack key KEY_ID --principal P --powers a,b,c --pubkey FILE` (`RUNBOOK.md:53-59`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition | Runs on `main`, up to date, clean tree (via `begin(a, True)`). | **yes** | `112` (`30-46`) |
| Refusal | "Refuses: a pubkey file that is not a two-field `ssh-ed25519` line;" | **yes** | `113-114` (and `entry.unsigned` -> `log.check_body` at `54`) |
| Refusal | "a power outside the eight;" | **yes** | `115-117` |
| Refusal | "a re-declaration of the signer's own `key_id` without `key` (the kernel's guard would refuse it too; the verb says so first)." | **yes** | `118-119` |
| Effect | "Entry: `key` with the declaration (SPEC §5)." | **yes** | `120` |
| Effect | "Effect: the main-verb ending." | **yes** | `120-121` (`75-86`) |
| Effect | "Revocation is this verb with `--powers \"\"`." | **yes** | `115`, `120` |

---

### 2. `jack proposal [--title T]` (`RUNBOOK.md:61-70`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Refusal | "On a branch other than `main`, with every change committed and the branch containing `origin/main` (otherwise refused with the merge command to run: `git merge origin/main -m \"Merge main into <branch>\" -m \"Proposer: <party> <key_id>\"`)." | **yes** | `124` (`31-35`, `47-48`) |
| Precondition / Refusal | "Runs the check first — `python3 -m unittest discover -s tests -t .`, `python3 pins/run.py`, `python3 tools/count_kernel.py` — and refuses on any failure." | **yes** | `12`, `100-102`, `125` |
| Effect | "Entry: `proposal` with `title` (default: the head commit's subject) and `commit` = the head's SHA (the work)." | **yes** | `126-127` |
| Effect | "Effect: commits `log.jsonl` on top of the work, pushes the branch (`git push -u origin <branch>`), and opens the pull request (`gh pr create --base main`) or, if one exists for the branch, does nothing more." | **yes** | `88-95`, `127-128` |
| Effect | "A proposal re-made after `main` moved (prefix broken) appends a new entry on top of a merge of `main`; the earlier one stands as history." | **yes** | `50-59`, `89-95`, `127` |

---

### 3. `jack spec_conflict --section S --text T` (`RUNBOOK.md:72-77`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Refusal | "On a branch, with the branch preconditions of `proposal` and no check: a conflict is filed exactly when the tests cannot be made to pass (A2 clause 9)." | **yes** | `131` (`30-48`) |
| Effect | "Entry: `spec_conflict` {section, text}." | **yes** | `132` |
| Effect | "Effect: commits `log.jsonl`, pushes the branch, opens a pull request titled `spec_conflict: <section>`, and prints \"stopped: the specification cannot be implemented as written; see PR #n\"." | **yes** (see Finding 7) | `88-95`, `132-133` |

---

### 4. `jack merge N` (`RUNBOOK.md:79-90`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Refusal | "On `main`, up to date." | **yes** | `136` (`30-46`) |
| Precondition / Refusal | "Preconditions, read with `gh pr view` and `gh pr checks`: PR N is open against `main`, mergeable, its required checks green on its current head;" | **yes** | `137-142` |
| Precondition / Refusal | "its head commit is one commit past the `commit` of a valid `proposal` entry in the PR's log, or — until the judge checks it — carries a filled `Proposer:` trailer." | **yes** (see Finding 8) | `23`, `144-147` |
| Effect / Refusal | "Act: in a temporary worktree of the PR's head branch, entry `merge` {proposal: N, commit: the PR's head SHA, checker: the trusted-base digest of `main`'s tree (`tools/digest.py`; SPEC §10.6 refuses any other)}, committed with message `merge: #N` and the trailer, pushed to the PR's branch as a fast-forward (a rejected push means the proposal moved: refused, run again)." | **yes** | `25-27`, `104-109`, `148-151` |
| Effect / Refusal | "Effect: `gh pr checks N --watch` until the judge and the tests have admitted the head that carries the entry, then `gh pr merge N --merge`, which GitHub performs only if they did; then `git pull --ff-only` on `main` and `gh run watch` of `main`'s run." | **yes** | `152-156` |

---

### 5. `jack push BRANCH --review FILE | --review none` (`RUNBOOK.md:92-112`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Refusal | "On `main`, up to date; BRANCH is a local branch another party built, and the verb never commits to it." | **yes** | `184-186` |
| Precondition | "Preconditions, each a refusal with its reason, evaluated on BRANCH's tree in a temporary worktree:" | **yes** | `187-195` |
| Precondition / Refusal | "BRANCH contains `origin/main`;" | **yes** | `187-188` |
| Precondition / Refusal | "BRANCH's trusted-base digest differs from `main`'s (otherwise \"nothing to push: propose and merge\");" | **yes** | `189-190` |
| Precondition / Refusal | "every commit on BRANCH not on `main` carries a filled `Proposer:` trailer;" | **yes** (see Finding 8) | `23`, `191-192` |
| Precondition / Refusal | "the check passes (as `proposal`);" | **yes** | `100-102`, `195` |
| Precondition / Effect / Refusal | "if `kernel/` or any kernel2 production source (`checker.go canonical.go ed25519.go signature.go main.go`) differs from `main`'s, the run of record exists or is made there: `kernel2/check` built once first (so the twelve do not race the build), then `harness/diff.py --seeds A:B --b kernel2/check` twelve ways into `transcripts/diff-100000-<T>-part00..11.json`, and the sum must be 100,000 logs, 0 disagreements, 0 uncompared, ranges without a gap; a complete run already under `transcripts/` on BRANCH counts if the checker sources at its commit equal BRANCH's." | **yes** (see Findings 1 & 2) | `10-11`, `158-181`, `194-195` |
| Effect | "`--review FILE` is copied to `transcripts/` and its SHA-256 is the entry's `review`; `--review none` records 64 zeros and prints a warning that this push was not read." | **yes** (see Finding 3) | `193`, `197-200` |
| Effect | "Effect, in this order: `git merge --ff-only BRANCH` on `main` (never a merge commit, never a rebase); the run's parts and the review placed under `transcripts/`; entry `push` {digest: `tools/digest.py` of the tree now on `main`; review; record: the SHA-256 of the twelve parts' bytes concatenated in name order, or 64 zeros when no run was required — an extra member until SPEC §5 names it}; committed with message `push: BRANCH`; the main-verb ending, whose self-check runs with the new trusted base and the entry both in place and whose undo returns `main` to `origin/main`, BRANCH untouched." | **yes** (see Findings 3 & 6) | `75-86`, `196-202` |
| Effect | "`--remove` removes BRANCH's own worktree afterwards." | **yes** | `203-205`, `230` |

---

### 6. `jack decision KIND SUBJECT` (`RUNBOOK.md:114-119`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Refusal | "On `main`." | **yes** | `208` (`30-46`) |
| Precondition / Refusal | "KIND is one of `veto promote budget grant transmute fix`;" | **yes** | `13`, `240-241` |
| Precondition / Refusal | "SUBJECT a non-empty string (for `transmute`, the amendment id; for `grant`, the capability, such as a sealed judge image by digest; for `promote`, the layer)." | **yes** | `209` |
| Effect | "Entry: `decision` {kind, subject}. Effect: the main-verb ending." | **yes** | `210` (`75-86`) |
| Refusal (via self-check) | "The judge admits a `decision` only from a key declared in genesis (SPEC §10.14)." | **yes** | `80-81` (`judge/selfcheck.py` -> `judge/judge.py:225-230`) |

---

### 7. `jack amend ID FILE [--activate-at N]` (`RUNBOOK.md:121-127`)

| Kind | Contract quote (`RUNBOOK.md`) | Implemented? | `tools/jack` line(s) |
|---|---|---|---|
| Precondition / Refusal | "On `main`." | **yes** | `213` (`30-46`) |
| Precondition / Refusal | "Preconditions: a valid `decision` of kind `transmute` with subject ID is in the log (otherwise refused: \"transmute first\");" | **yes** (see Finding 4) | `214-216` |
| Precondition / Refusal | "FILE's first line is `## Amendment ID:`;" | **yes** | `219-220` |
| Precondition / Refusal | "ID is not already an amendment." | **yes** | `217-218` |
| Effect | "Effect before the entry: a blank line and FILE appended to `CHARTER.md`." | **yes** | `221` |
| Effect | "Entry: `amend` {id, charter: the SHA-256 of the new `CHARTER.md`, activate_at: N, default the entry's seq + 1}." | **yes** (see Finding 4) | `222` |
| Effect | "Effect: commits `CHARTER.md` and `log.jsonl`; the main-verb ending (judge items 2, 12, 13 on the way in)." | **yes** | `223` (`75-86`) |

---

## 3. Adversarial Audit and Findings `(verb, line, contract sentence, how)`

### Forbidden-Effect Checks That Hold
- **Force push / branch deletion / tag creation:** `push()` (`tools/jack:25-27`) rejects any refspec argument starting with `+` or `:` and runs `git push -q` without `--force`, `-f`, `--delete`, or `--tags`; `main()` (`tools/jack:238-239`) rejects any argv element containing `--admin` or `--force`; all push call sites (`tools/jack:85, 92, 151`) push only `main`, `a.branch` (from `git symbolic-ref --short HEAD`), or `HEAD:refs/heads/{branch}`.
- **Entry signed as a party the key does not belong to:** `begin()` (`tools/jack:38-42`) derives `a.party` and `a.key_id` solely from the log's declared keys matching `a.key + ".pub"`, and `append()` (`tools/jack:56`) calls `entry.assemble()` which runs `kernel.check()` (`kernel/check.py:25-41`), extracting the public key blob embedded in `e["sig"]` by `ssh-keygen -Y sign` and refusing with `unknown_key` or `proposer_mismatch` if `e["proposer"]` does not match the signing key's declared `principal`.
- **Push to `main` skipping `judge/selfcheck.py`:** `main_ending()` (`tools/jack:80-85`) is the sole path that executes `push("origin", "main")`, and it runs `judge/selfcheck.py --repo ROOT` at line 80 immediately before line 85, refusing if `returncode != 0`.

### Findings

1. **`(push, 10, "then harness/diff.py --seeds A:B --b kernel2/check twelve ways into transcripts/diff-100000-<T>-part00..11.json, and the sum must be 100,000 logs, 0 disagreements, 0 uncompared, ranges without a gap", how)`**
   - **How:** Line 10 defines `SEEDS = int(os.environ.get("JACK_SEEDS", "100000"))`. If `JACK_SEEDS=0` (or any multiple of 12 less than `100000`, such as `JACK_SEEDS=12`) is present in the environment, `make_run` (`lines 175-177`) and `valid_run` (`lines 161-162`) require only `SEEDS` logs instead of `100,000`. With `JACK_SEEDS=0`, `harness/diff.py --seeds 0:0` compares 0 logs in each of the 12 parts, `valid_run` accepts `sum(logs) == 0 == SEEDS == edges[-1][1]`, and `jack push` pushes a `kernel/` or `kernel2/` change to `main` having skipped the 100,000-log run of record.

2. **`(push, 158-170, "and the sum must be 100,000 logs, 0 disagreements, 0 uncompared, ranges without a gap; a complete run already under transcripts/ on BRANCH counts if the checker sources at its commit equal BRANCH's.", how)`**
   - **How:**
     1. `existing_run(branch)` (`lines 165-170`) accepts any 12 JSON files committed on `BRANCH` matching `transcripts/diff-{SEEDS}-(.+)-part\d\d\.json` (not restricting part numbers to `00..11`) whose `"commit"` field resolves to a tree with the same `*SOURCES` as `BRANCH` (for example `"commit": "<BRANCH-head>"` or the branch name itself), without verifying that the files were produced by `harness/diff.py`. A branch author can commit 12 synthetic JSON files under `transcripts/` and cause `jack push` to skip running `harness/diff.py`.
     2. `valid_run(parts)` (`lines 161-162`) checks `sum(r["logs"] for r in reps) == SEEDS == edges[-1][1]` and `[e[0] for e in edges] == [0] + [e[1] for e in edges[:-1]]`, but never checks that each part's `r["logs"] == r["seeds"][1] - r["seeds"][0]` or `r["seeds"][0] <= r["seeds"][1]`.
     3. If `transcripts/` on `BRANCH` contains any run whose `"commit"` field is `null` (which `harness/diff.py:56` emits when `git rev-parse HEAD` fails), `c.pop()` is `None` and `fails("git", "diff", "--quiet", c.pop(), ...)` at line 170 raises an uncaught `TypeError` traceback instead of a clean refusal or ignoring that run.

3. **`(push, 193, "`--review FILE` is copied to `transcripts/` and its SHA-256 is the entry's `review`; `--review none` records 64 zeros and prints a warning that this push was not read.", how)`**
   - **How:** Line 193 sets `review = b"" if a.review == "none" else open(a.review, "rb").read()`, and lines 197, 199, 200, and 202 test the truthiness of `review` (`if review`, `review or print(...)`, `if review else ZERO`, `bool(place or review)`) rather than `a.review != "none"`. When `--review FILE` points to an empty (0-byte) file, `review` is `b""` (falsy), so `jack push` fails to copy `FILE` to `transcripts/`, prints `"WARNING: --review none: this push was not read"`, and records 64 zeros (`"0" * 64`) in `push.review` instead of the empty file's SHA-256 (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

4. **`(amend, 215 and 222, "Preconditions: a valid `decision` of kind `transmute` with subject ID is in the log (otherwise refused: \"transmute first\") ... Entry: `amend` {id, charter: the SHA-256 of the new `CHARTER.md`, activate_at: N, default the entry's seq + 1}.", how)`**
   - **How:**
     1. Line 222 computes `"activate_at": a.activate_at or len(entries) + 1` instead of `len(entries) + 1 if a.activate_at is None else a.activate_at`. Passing `--activate-at 0` evaluates `0` as falsy and silently substitutes `len(entries) + 1`, committing and pushing the amendment at `seq + 1` instead of passing `0` to the kernel and refusing (`activate_at <= seq`).
     2. Line 215 checks `e["body"] == {"kind": "transmute", "subject": a.id}` using exact dict equality. Because `SPEC.md §5` allows extra members on any entry body (and both `kernel/check.py:87` and `judge/judge.py:223` check `body["kind"] == "transmute"` and `body["subject"]`), a valid `transmute` decision whose `body` contains an extra member is falsely refused with `"transmute first"`.

5. **`(Common to every verb, 41-44 and 61-63, "A verb's commit message is `<type>: <summary>` ... and as its **last paragraph** `Proposer: <party> <key_id>`.", how)`**
   - **How:** `begin()` (`lines 41-44`) sets `a.trailer = f"Proposer: {state.keys[key_id].principal} {key_id}"` and checks only `"<" in a.trailer`. Because `kernel/log.py:22` defines the schema of `principal` as `NONEMPTY = re.compile(r".+", re.S)` (which permits `\n`), if a key is declared in the log with `\n\n` in `principal` (e.g. `"builder\n\nother"`), `git commit -m subject -m a.trailer` (`line 63`) creates a commit whose last paragraph is `"other <key_id>"` rather than `Proposer: <party> <key_id>`.

6. **`(push / amend, 82 and 196-201, "A failed self-check undoes the verb's commits with `git reset --hard origin/main` and prints the refusal; nothing was pushed. ... whose undo returns `main` to `origin/main`, BRANCH untouched.", how)`**
   - **How:** In `v_push`, `git("merge", "-q", "--ff-only", b)` (`line 196`) and writing files to `ROOT/transcripts/` (`lines 197-198`) happen before `main_ending()` (`line 202`) is entered; in `v_amend`, `CHARTER.md` is modified (`line 221`) before `main_ending()` (`line 223`). Moreover, `main_ending()` (`line 82`) only catches `(Refused, entry.Usage, subprocess.CalledProcessError)`, whereas `main()` (`line 243`) also catches `(OSError, log.Refuse)`. If an `OSError` occurs in `v_push` at lines 197-200 or inside `main_ending()` (e.g. `ssh-keygen` exits 0 without producing `path + ".sig"`), `main_ending()`'s `git reset -q --hard origin/main` is bypassed and `main()` exits 1 leaving `main` fast-forwarded to `BRANCH` or `CHARTER.md` modified in the working tree.

7. **`(spec_conflict, 93-95 and 132, "Effect: commits `log.jsonl`, pushes the branch, opens a pull request titled `spec_conflict: <section>`, and prints \"stopped: the specification cannot be implemented as written; see PR #n\".", how)`**
   - **How:** `v_spec_conflict` delegates to `branch_ending` (`lines 88-98`). If an open pull request already exists for `a.branch` (for example from an earlier `jack proposal` on that branch), line 93-94 (`n = run("gh", "pr", "list", ...); return n or run("gh", "pr", "create", ...)`) returns the existing PR number without opening or re-titling the PR to `spec_conflict: <section>`.

8. **`(merge / push, 23, 146 and 191, "carries a filled `Proposer:` trailer" / "every commit on BRANCH not on `main` carries a filled `Proposer:` trailer", how)`**
   - **How:** `trailer(rev)` (`line 23`) is `git("log", "-1", "--format=%(trailers:key=Proposer,valueonly)", rev).split()`. It checks only that `Proposer:` is non-empty, not that it has the two fields `<party> <key_id>`, that `<party>` is a recognised party, or that it contains no `<`. In `v_push` (`line 191`), because `judge/selfcheck.py` judges `HEAD` against `HEAD` (skipping `judge.py`'s `proposal_checks`), a commit on `BRANCH` with `Proposer: <party> <key_id>` (containing literal `<`) or a single token `Proposer: x` is admitted and pushed to `main`.

VERDICT: does not implement RUNBOOK
