# Cold read of the push that moves the promotion evaluator under judge/, by argon (opencode-runner #1216)

The final report of runner #1216 (`google/gemini-4-argon`, read only, no key), as its last comment gives it, from its first line to its verdict. The branch read is `move-promotion-judge` at `bd05ed5c1acc58993b8063bcb92dea6f09af2ed3`.

# Cold Read: `move-promotion-judge` (`bd05ed5c`)

## Custody and Hashes Checked

- `git rev-parse origin/move-promotion-judge`: `bd05ed5c1acc58993b8063bcb92dea6f09af2ed3` (begins `bd05ed5c`).
- `bd05ed5c:SPEC.md` SHA-256: `72eeea02a320a56f5be03a1de9bc50a2624b53e0538cdbc529c877b0274aaba2` (matches `main` log seq 6851 `decision grant`).
- `bd05ed5c:spec/vectors/promotion-replay.json` SHA-256: `6d647d09b0e02f0b3e1ac785bdf8e13fa223491501d6a24a1886783b9458c4dd` (matches `main` log seq 6851 `decision grant`).
- `origin/main:tools/status.py` SHA-256: `b255520996cef0ec20691c46cbc236ce5826dc166d16697762fa85f30fe86acb`.
- `origin/main:tools/value.py` SHA-256: `11440c89429513b49922658d419b0bc6c8e625b15701b335576eedf537cf9992`.

---

## Answers to Questions

### 1. The law (`SPEC.md` §10 item 15 and *The promotion evaluator* vs `judge/judge.py`)

`judge/judge.py` (with `judge/evaluate.py`) implements every sentence of `SPEC.md` §10 item 15 (lines 414–484) and its paragraph:

- **Refusal reason and checkers unchanged:**
  - `SPEC.md` lines 414–418:
    > `15. **promote_unmet** — a decision of kind promote that the promotion evaluator in force at it does not find lawful. It enforces CHARTER A5.1, under which a promotion "may be entered only once every pre-stated criterion of the window holds on the log's current prefix and on the tree at its commit"; the checkers' verdict (§8) does not change.`
  - `judge/judge.py` lines 325–326, 394–396 (`kernel/` and `kernel2/` are untouched):
    ```python
    except (JudgeError, OSError, ValueError, KeyError, TypeError, IndexError) as x:
        return "promote_unmet", str(x)
    ...
    failure = promotion_checks(repo, trunk, head, entries, [json.loads(l) for l in old], report["attested"])
    if failure:
        return refuse(*failure)
    ```
- **The installing push and non-retroactivity:**
  - `SPEC.md` lines 418–427:
    > `On every run the item judges each promote whose seq exceeds that of the *installing push*: the first push of trunk's log after seq 5564 whose *push commit*, the oldest commit on trunk's first-parent chain whose log.jsonl holds the push's line, both has the push's digest as its trusted-base digest (item 1) and holds a SPEC.md whose SHA-256, in 64 lowercase hex digits, follows promote_unmet: SPEC.md  at the start of the subject of an earlier decision of kind grant. If trunk's log has no installing push, the item refuses: the judge running it came in by no push of a SPEC.md his grant names (answer 10). The promotions at seqs 188 and 337 come before it and are not judged: an entry is judged by the law in force before it (CHARTER §2, maxim 2).`
  - `judge/judge.py` lines 212–237 (`installing_push`) and lines 243–247 (`promotion_checks`):
    ```python
    for e in entries:
        if e["type"] == "decision" and e["body"].get("kind") == "grant":
            match = re.match(r"promote_unmet: SPEC.md ([0-9a-f]{64})(?![0-9a-f])", e["body"]["subject"])
            if match:
                grants.add(match[1])
        if e["type"] != "push" or e["seq"] <= 5564 or not grants:
            continue
        if chain is None:
            chain = git(repo, "rev-list", "--first-parent", "--reverse", trunk).splitlines()
        push_line = json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
        line = None
        for sha in chain:
            data = show(repo, sha, LOG)
            lines = split_lines(data) if data else []
            if push_line in lines:
                line = sha
                break
        if line and not foreign(repo, line, TRUSTED) and digest(repo, line) == e["body"]["digest"]:
            spec = show(repo, line, "SPEC.md")
            if spec is not None and hashlib.sha256(spec).hexdigest() in grants:
                return e["seq"]
    ...
    installation = installing_push(repo, trunk, trunk_entries)
    if installation is None:
        raise JudgeError("trunk has no installing push")
    promotions = [e for e in entries if e["seq"] > installation and e["type"] == "decision"
                  and e["body"].get("kind") == "promote"]
    ```
- **Entry commits reachable from *H*:**
  - `SPEC.md` lines 427–431:
    > `Let *H* be the commit judged (trunk for the self-check, the proposal's head otherwise), and an *entry commit* of a promote any commit reachable from *H* whose log.jsonl holds the entry's line and none of whose parents' does. A judged promote at seq *i* is refused unless, for every entry commit it has, all four hold:`
  - `judge/judge.py` lines 250–264, 277:
    ```python
    parents = dict((p[0], p[1:]) for ln in git(repo, "rev-list", "--parents", head).splitlines() if (p := ln.split()))
    if git(repo, "rev-parse", "--is-shallow-repository") == "true":
        raise JudgeError("promotion history is shallow")
    for e in promotions:
        i, line = e["seq"], split_lines(show(repo, head, LOG))[e["seq"]]
        membership = {}
        def holds(sha):
            if sha not in membership:
                lines = split_lines(show(repo, sha, LOG) or b"")
                membership[sha] = line in lines
            return membership[sha]
        carrying = [c for c, ps in parents.items() if holds(c) and not any(holds(p) for p in ps)]
        if not carrying:
            raise JudgeError(f"promote seq {i}: no entry commit")
        ...
        for c in carrying:
    ```
- **Condition (a):**
  - `SPEC.md` lines 432–435:
    > `(a) its body.evidence is an object with exactly the members run, runs and acts, each an object with exactly path, a path under transcripts/evidence/, and sha256, hex64; and at the entry commit each path is a regular file whose bytes have that SHA-256;`
  - `judge/judge.py` lines 265–273, 278–282:
    ```python
    evidence = e["body"].get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != {"run", "runs", "acts"}:
        raise JudgeError(f"promote seq {i}: evidence must name run, runs and acts")
    for name, ev in evidence.items():
        if (not isinstance(ev, dict) or set(ev) != {"path", "sha256"} or
            not isinstance(ev["path"], str) or not ev["path"].startswith("transcripts/evidence/") or
            any(p in ("", ".", "..") for p in ev["path"].split("/")) or
            not isinstance(ev["sha256"], str) or not re.fullmatch("[0-9a-f]{64}", ev["sha256"])):
            raise JudgeError(f"promote seq {i}: malformed {name} evidence")
    ...
    tree = dict((p, mode) for mode, p in modes(repo, c))
    data = {n: show(repo, c, ev["path"]) for n, ev in evidence.items()}
    for name, ev in evidence.items():
        if tree.get(ev["path"]) not in REGULAR or data[name] is None or hashlib.sha256(data[name]).hexdigest() != ev["sha256"]:
            raise JudgeError(f"promote seq {i} at {c}: {name} evidence absent, nonregular or wrong hash")
    ```
- **Condition (b):**
  - `SPEC.md` lines 436–438:
    > `(b) the entry commit has one parent, the *assessed commit*, whose log.jsonl is exactly lines 0 to *i*−1; and against it the entry commit changes log.jsonl by appending line *i* alone, adds the three evidence paths, and changes nothing else;`
  - `judge/judge.py` lines 274–276, 284–296:
    ```python
    paths = {ev["path"] for ev in evidence.values()}
    if len(paths) != 3:
        raise JudgeError(f"promote seq {i}: evidence paths are not three added files")
    ...
    if len(parents[c]) != 1:
        raise JudgeError(f"promote seq {i} at {c}: entry commit must have one parent")
    assessed = parents[c][0]
    assessed_modes = dict((p, mode) for mode, p in modes(repo, assessed))
    prefix_lines = split_lines(show(repo, head, LOG))[:i]
    prefix = b"".join(l + b"\n" for l in prefix_lines)
    if (tree.get(LOG) != assessed_modes.get(LOG) or
        split_lines(show(repo, assessed, LOG) or b"") != prefix_lines or
        split_lines(show(repo, c, LOG) or b"") != prefix_lines + [line]):
        raise JudgeError(f"promote seq {i} at {c}: entry is not appended alone to its exact prefix")
    added = {p for p in paths if show(repo, assessed, p) is None}
    if added != paths or changed_by(repo, c) != paths | {LOG}:
        raise JudgeError(f"promote seq {i} at {c}: entry commit changes other paths or does not add evidence")
    ```
- **Condition (c):**
  - `SPEC.md` lines 439–440:
    > `(c) the assessed commit's trusted-base digest (item 1) is the trusted base in force at seq *i* (§7);`
  - `judge/judge.py` lines 297–300:
    ```python
    trusted = next((x["body"]["digest"] for x in reversed(entries[:i]) if x["type"] == "push"),
                   entries[0]["body"]["checker"])
    if foreign(repo, assessed, TRUSTED) or digest(repo, assessed) != trusted:
        raise JudgeError(f"promote seq {i}: assessed evaluator is not the trusted base in force")
    ```
- **Condition (d), no timeout, refusal on inability to decide, `attested` list, and self-check coverage:**
  - `SPEC.md` lines 441–451, 458–470, 484:
    > `(d) the assessed commit's own judge/status.py, extracted from git as the kernel is (item 5), accepts the entry's subject and finds every criterion met for this promotion alone. It accepts the subject if its argument parser, built as its main builds it, parses --subject with that value without exiting; a subject it does not list is refused, never assessed by another window's criteria. Its assess, called with decision unset (as its report calls it when no promotion yet closes the window), with subject the entry's subject, rev the assessed commit, as_of the entry's ts, lines 0 to *i*−1 as the log, and the three files read as its --run, --runs and --acts are read, gives a promotion_line of promote <subject>: lawful. report's re-assessment of earlier promotions is not run.`
    > `An evaluator that cannot decide (an error, absent history, a window it does not know) refuses, as a checker's silence does (§9). ... The item sets no time limit ... and the judge's report lists each such file under attested.`
    > `Items 11–15 apply to every judged log, the self-check included.`
  - `judge/judge.py` lines 283, 301–324, 333, 394–396 and `judge/evaluate.py` lines 9–28:
    - Extracts `kernel/` and `judge/` from `assessed` into `tmp` (`judge/judge.py` lines 302–303), writes `judge/evaluate.py`, `prefix.jsonl`, and `run`, `runs`, `acts` into `tmp` (lines 305–318), and runs `[sys.executable, "-E", "-s", "-m", "judge.evaluate", os.path.abspath(repo), assessed, e["ts"], e["body"]["subject"], log_path, *evidence_files]` with `cwd=tmp` and no `timeout` (lines 319–321).
    - Appends `dict(seq=i, commit=c, name=name, **ev)` to `report["attested"]` (`judge/judge.py` lines 283, 333, 394).
    - Runs unconditionally after `if head != trunk:` (`judge/judge.py` lines 371–396), so `judge/selfcheck.py` runs it too.
- **Does `judge/judge.py` do anything those sentences do not say?**
  - Every check in `installing_push` and `promotion_checks` implements a clause of item 15:
    - `git(repo, "rev-parse", "--is-shallow-repository") == "true"` (`judge/judge.py` line 252) prevents a shallow boundary from hiding parents in `git rev-list --parents` and implements line 459 (`"absent history"` refuses).
    - `any(p in ("", ".", "..") for p in ev["path"].split("/"))` (`judge/judge.py` line 271) ensures `ev["path"]` is a normalized relative path under `transcripts/evidence/` (line 434).
    - `tree.get(LOG) != assessed_modes.get(LOG)` (`judge/judge.py` line 290) ensures `log.jsonl`'s git file mode is unchanged between `assessed` and `c` (line 437–438: `"changes log.jsonl by appending line i alone ... and changes nothing else"`).
    - See Finding 1 (NOTE) on the unescaped `.` in `re.match(r"promote_unmet: SPEC.md ([0-9a-f]{64})(?![0-9a-f])", ...)` at `judge/judge.py` line 218.

---

### 2. The move (`judge/status.py`, `judge/value.py`, `judge/entries.py` vs `main`'s `tools/status.py`, `tools/value.py`)

`git diff origin/main:tools/status.py bd05ed5c:judge/status.py` and `git diff origin/main:tools/value.py bd05ed5c:judge/value.py` show only three changed lines across the two files:

1. **`judge/status.py` line 20** (import path change, no behavioural difference):
   - `-from tools import value as val  # noqa: E402`
   - `+from judge import value as val  # noqa: E402`
   - Authorised by `SPEC.md` lines 488–492 (`"The evaluator imports nothing outside the standard library and the trusted base ... Besides that and the import paths, one change is made"`) and `RULING-20261120-promotion-judge.md` answers 4 and 16.
2. **`judge/status.py` line 433** (the single behavioural difference):
   - `-        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", f"{start}..{rev}").decode().split())`
   - `+        unchanged = all(scope_at(c) == original for c in [rev] + git_bytes(root, "rev-list", "--first-parent", f"{start}..{rev}").decode().split())`
   - Authorised by `SPEC.md` lines 491–494 (`"Besides that and the import paths, one change is made: criterion 3's walk of the commits since an opening follows first parents only (git rev-list --first-parent), as the same function's other walk already does."`) and `RULING-20261120-promotion-judge.md` answers 4 and 7.
3. **`judge/value.py` line 15** (import path change, no behavioural difference):
   - `-from tools.entry import now, read_log, resolution_rates`
   - `+from judge.entries import now, read_log, resolution_rates`
   - And `judge/entries.py` lines 8–29 hold `read_log`, `now`, and `resolution_rates` moved verbatim from `origin/main:tools/entry.py` lines 29–31, 85–87, 132–143, with `tools/entry.py` line 20 re-importing them (`from judge.entries import now, read_log, resolution_rates`).
   - Authorised by `SPEC.md` lines 489–491 (`"so the three functions judge/value.py takes from tools/entry.py (now, read_log, resolution_rates) come under judge/ with it, unchanged (answer 16)"`) and `RULING-20261120-promotion-judge.md` answer 16.

---

### 3. The driver (`judge/evaluate.py`)

- **Exact named inputs:** `judge/judge.py` lines 319–320 invoke `judge.evaluate` with `[os.path.abspath(repo), assessed, e["ts"], e["body"]["subject"], log_path, *evidence_files]`. `judge/evaluate.py` lines 20–21 pass `["--root", repo, "--as-of", ts, "--subject", subject, "--log", log_path, "--run", run, "--runs", runs, "--acts", acts]` to `status.main(...)`, line 26 calls `context = status.inputs(a)`, line 27 sets `context["rev"] = rev` (the assessed commit `assessed`), and line 28 calls `status.promotion_line(status.assess(**context, decision=None))`. These are the exact inputs `SPEC.md` lines 441–451 name (`subject`, `rev`, `as_of`, lines `0..i-1` as `--log`, `--run`, `--runs`, `--acts`, and `decision=None`).
- **Isolation (no clock, environment, network, or outside file):**
  - Invoked with `sys.executable -E -s` (`judge/judge.py` line 319) and `cwd=tmp` (line 321), so environment variables and user site-packages are ignored and `from judge import status` imports the assessed commit's extracted `judge/` and `kernel/`.
  - Although `status.parser` constructs `--as-of`'s default with `dt.datetime.now(dt.timezone.utc).strftime(FMT)` (`judge/status.py` line 600), `--as-of ts` is explicitly passed on line 20 of `judge/evaluate.py`, so the default is overwritten by `parse_args` and never read.
  - Because `context["rev"] = rev` sets `rev` to the assessed commit SHA (never `None`), `tree_bytes(root, rev, path)` (`judge/status.py` lines 212–216) and `counted_lines(root, rev, ...)` (`judge/judge.py` lines 117–121) read exclusively from git objects via `git -C root show`/`ls-tree` and never read any working-tree file outside `tmp`. No network calls exist in `judge/` or `kernel/`.
- **Soundness of `argparse` capture:**
  - `judge/evaluate.py` lines 11–25 replace `argparse.ArgumentParser.parse_args` with `capture(ap, *args, **kwargs)`, which delegates to the original `parse_args(ap, *args, **kwargs)` and raises `Parsed(...)` with the returned namespace.
  - Because `status.main` passes its explicit `argv` list to `ap.parse_args(argv)` (`judge/status.py` line 663), the parser cannot read `sys.argv`.
  - If `--subject` is not accepted by `ap`, `parse_args` exits with status 2 via `ap.error(...)` before `Parsed` is raised; `judge/judge.py` line 322 sees `result.returncode != 0` and refuses with `promote_unmet`.
  - If `parse_args` succeeds, `Parsed` unwinds out of `status.main` before `inputs` or `report` can run inside `status.main`, and the `finally:` block restores `argparse.ArgumentParser.parse_args`.

---

### 4. The verb (`tools/jack` and `RUNBOOK.md`)

- **`tools/jack` (`v_decision`, lines 247–302, and `main`, lines 329–332):**
  - Consistent with `SPEC.md` §10 item 15 (lines 432–438, 470–471) and counsel's paragraph in `origin/main:RUNBOOK.md` lines 200–207:
    - Requires `--acts` on `promote` (`tools/jack` line 255: `a.acts is not None or refuse("promote requires --acts: run, runs and acts evidence must all be committed")`).
    - Keeps C2a-prime's `body["acts"] = {"path": a.acts, "sha256": ..., "commit": head}` verification (`tools/jack` lines 256–265).
    - Runs `judge/status.py` with `--subject`, `--run`, `--runs`, `--acts`, and `--as-of` (`tools/jack` lines 273–282).
    - Sets `body["evidence"]` to `{"run": {"path": ..., "sha256": ...}, "runs": {"path": ..., "sha256": ...}, "acts": {"path": ..., "sha256": ...}}`, where each path is `transcripts/evidence/promote-<seq>-<name>-<sha256>` verified absent in `HEAD` (`tools/jack` lines 283–291).
    - Writes the three files in `effect()` and commits `["log.jsonl", *placed]` in one commit on `HEAD` (the assessed commit) via `main_ending`, which then runs `judge/selfcheck.py` before pushing (`tools/jack` lines 295–301, 70–82).
- **Does any verb change beyond it?**
  - No. Outside `v_decision` (when `a.kind == "promote"`), the only change in `tools/jack` is lines 330–331 updating `from tools import status, clerk` to `from judge import status` / `from tools import clerk` for the read-only `jack status` dispatch. All other `decision` kinds (`veto`, `budget`, `grant`, `transmute`, `fix`) and all other verbs are unchanged.

---

### 5. The rest of the trusted base and other changed files outside `transcripts/`

Every changed file outside `transcripts/` (apart from one standalone helper test script noted below) is needed by item 15, by its pins, or by the move's paths:

- **`.github/workflows/tests.yml` (lines 17–18):** adds `with: fetch-depth: 0` to `actions/checkout`. Needed directly by item 15 (`SPEC.md` lines 471–473: `"The installing push makes both workflows that run the judge (judge.yml and tests.yml) check out the whole history; tests.yml does not today."`).
- **`tools/enforcement.json` (line 4):** updates W4's enforcer string from `tools/status.py assess` to `judge/status.py assess`. Needed by the move's paths.
- **`tools/entry.py` (lines 6, 20, 29–31, 85–87, 132–143):** removes the definitions of `read_log`, `now`, and `resolution_rates` (moved to `judge/entries.py`) and re-imports them from `judge.entries`. Needed by item 15's paragraph (`SPEC.md` lines 489–491) and the move's paths.
- **`tools/clerk.py` (lines 16–17):** updates `from tools import status` / `from tools.status import c1b_window` to import from `judge`. Needed by the move's paths.
- **`harness/gitfix.py` (lines 78–80, 89–92):** when `with_log=True`, calls `prepare(repo, world)` and `install(repo, lg, world)` so synthetic judge/pin repositories carry a signed grant and an installing push after seq 5564. Needed by item 15 and its pins because item 15 runs on every `judge()` call and refuses any trunk without an installing push (`SPEC.md` lines 424–425, 484).
- **`CHARTER.md`:** unchanged on the branch (`git diff origin/main...bd05ed5c -- CHARTER.md` is empty; `origin/main` has since added Amendment A6).
- **`LAW.md` (lines 65, 93, 95, 173, 220):** updates five citations from `tools/status.py` and `tools/value.py` to `judge/status.py` and `judge/value.py`. Needed by the move's paths (checked by `tests/test_law.py`).
- **`README.md` (line 55):** updates `python3 tools/status.py` to `python3 judge/status.py`. Needed by the move's paths.
- **`pins/c2a.py` (line 6) and `pins/fixtures.py` (lines 14–18):** `pins/c2a.py` updates its import to `from judge import value as v, status as st` (move's paths); `pins/fixtures.py` adds `record_push` so pins that alter a fixture's trusted base record a `push` after the 5,566-entry installed prefix rather than re-creating genesis (needed by pins under item 15).
- **`tests/clerk_fixture.py`, `tests/test_clerk.py`, `tests/test_status.py`, `tests/test_value.py`, `tests/test_promotion.py`, `tests/test_jack.py`, `tests/test_judge.py`, `tests/fixture_signatures.py`, `tests/promotion_fixture.py`, `tests/test_evaluator_move.py`, `tests/test_promotion_judge.py`:** update imports/paths for the move, provide the 5,566-entry installation prefix and relative amendment activation heights, and test item 15, the verb, and the move.
- **`tests/promotion_replay_spot.py` (lines 1–65):** see Finding 2 (NOTE). This 65-line script was written for the builder's session check (e) (spot-checking rows 592, 593, 705); it is not discovered by `unittest` (its name does not begin `test_`) and is not imported by `pins/replay.py`.

---

### 6. The pins (`pins/promotion.py`, `pins/replay.py`, `pins/pins.py`)

All seven pins required by `SPEC.md` §10 item 15 (lines 473–483) and its paragraph (lines 535–537) are registered in `pins/pins.py` (lines 1145–1177, raising `EXPECTED` from 100 to 107 at line 667), and each kills a mutant that breaks its corresponding sentence:

1. **`promote_while_unmet`** (`pins/pins.py` lines 1146–1149): mutant `refusal_admitted` replaces `if result.returncode != 0 or json.loads(result.stdout) != f"promote {e['body']['subject']}: lawful":` with `if False:` (`judge/judge.py` line 322). Killed by `test_unmet_criteria_and_skipped_ci_are_refused_on_later_runs`.
2. **`evidence_substituted`** (`pins/pins.py` lines 1150–1152): mutant `hash_unchecked` removes ` or hashlib.sha256(data[name]).hexdigest() != ev["sha256"]` (`judge/judge.py` line 281). Killed by `test_evidence_shape_hash_presence_and_regular_files`.
3. **`promote_tree_changed`** (`pins/pins.py` lines 1153–1157): mutant `other_paths_admitted` removes ` or changed_by(repo, c) != paths | {LOG}` (`judge/judge.py` line 295), and mutant `side_entry_ignored` skips non-first-parent commits in `for c in carrying:` (`judge/judge.py` line 277). Killed by `test_entry_must_append_alone_add_evidence_and_change_nothing_else` and `test_every_entry_commit_including_a_bad_side_branch_is_judged`.
4. **`promote_retroactive`** (`pins/pins.py` lines 1158–1161; `pins/promotion.py` lines 9–24): mutant `earlier_promotions_judged` drops `e["seq"] > installation and ` (`judge/judge.py` line 246), and mutant `ungranted_spec_installs` replaces `hashlib.sha256(spec).hexdigest() in grants` with `True` (`judge/judge.py` line 235). Killed by `test_preinstallation` and `test_ungranted_installation`.
5. **`evaluator_not_in_force`** (`pins/pins.py` lines 1162–1164): mutant `assessed_digest_unchecked` replaces `if foreign(repo, assessed, TRUSTED) or digest(repo, assessed) != trusted:` with `if False:` (`judge/judge.py` line 299). Killed by `test_assessed_digest_must_be_in_force`.
6. **`promote_judged_once`** (`pins/pins.py` lines 1165–1167; `pins/promotion.py` lines 26–34): mutant `old_promotions_skipped` restricts `promotions` to `e["seq"] >= len(trunk_entries)` (`judge/judge.py` line 246). Killed by `test_skipped_promotion_on_later_run`.
7. **`replay_drift`** (`pins/pins.py` lines 1172–1177; `pins/replay.py` lines 40–80): mutants `unmarked_output_changed`, `marked_walk_regressed`, and `other_source_bytes` in `judge/status.py` are killed by the replay check on rows 300, 400, 593 and the exact moved-bytes comparison against `2d99d242:tools/status.py` and `2d99d242:tools/value.py`.

**Sentences/sub-clauses of item 15 covered by unit tests (`tests/test_promotion_judge.py`, `tests/test_jack.py`) rather than a pin mutant in `pins/pins.py`:**
- In the installing push (lines 418–425): that the push must have `seq > 5564`, that its push commit is the *oldest* commit on trunk's first-parent chain holding the line (rather than a later commit), and that the push commit's trusted-base digest equals the push's `digest` (unit-tested in `test_installation_requires_prior_grant_matching_spec_and_push_commit_digest` and `test_installation_uses_oldest_first_parent_push_commit_not_later_repair`).
- In condition (a) (lines 432–435): the schema of `body.evidence` (`run`, `runs`, `acts`, `path` under `transcripts/evidence/`, `sha256` hex64) and the regular-file mode check `tree.get(ev["path"]) in REGULAR` (unit-tested in `test_evidence_shape_hash_presence_and_regular_files`).
- In condition (b) (lines 436–438): that the entry commit has a single parent (`len(parents[c]) == 1`), that `log.jsonl` is lines `0..i-1` in `assessed` and `0..i` in `c` with unchanged mode, and that the three evidence paths were absent in `assessed` (`added == paths`) (unit-tested in `test_entry_commit_with_two_parents_is_refused`, `test_entry_must_append_alone_add_evidence_and_change_nothing_else`, and `test_appending_the_entry_does_not_authorise_a_log_mode_change`).
- In condition (d) and lines 458–460: that `--subject` acceptance comes from `main`'s argument parser without running `report`, and that an evaluator error or unknown subject refuses (unit-tested in `test_subject_acceptance_comes_from_main_not_a_separate_choices_list` and `test_unknown_subject_and_evaluator_error_refuse`).
- In lines 467–473: populating `report["attested"]` (checked by the positive twin `test_lawful_and_attested_on_selfcheck`, no dedicated mutant), `tools/jack` committing the three evidence files with the entry (unit-tested in `tests/test_jack.py:test_decision_promote_names_committed_table`), and `.github/workflows/tests.yml` setting `fetch-depth: 0`.

---

### 7. Paths left behind (`tools/status.py` and `tools/value.py`)

 separating live readers (that run or instruct) from historical text:

1. **`judge/status.py` lines 436–437** (live code in `c2a_tree_evidence`):
   ```python
   start_nodes = ast.parse(tree_bytes(root, start, "tools/status.py")).body
   rev_nodes = ast.parse(tree_bytes(root, rev, "tools/status.py")).body
   ```
   - **Behaviour:** **Fails (returns `(False, False, False)` from `c2a_tree_evidence`) when `rev` is a commit after the move push** (since `tools/status.py` is absent in `rev`'s tree), **harmless for promotion and required for replay**. Up to the move's parent, `tools/status.py` exists in both `start` and `rev`, so keeping this literal path is required for `spec/vectors/promotion-replay.json` and `replay_drift`. After the move push, C2a and C2a-prime are both closed (C2a-prime ended at the post-A6 veto at seq 7180), and `RULING-20261120-promotion-judge.md` point 4 (lines 219–222) explicitly leaves these two lines unchanged for C2a-3's future evaluator change.
2. **`tests/test_status.py` lines 106–107, 190, 205; `tests/test_value.py` lines 248–249; `tests/test_evaluator_move.py` lines 25, 47; `pins/replay.py` line 70** (live test/pin code):
   - **Behaviour:** **Harmless.** They read the live checkout's `judge/status.py` and populate `"tools/status.py"` inside synthetic git trees so `judge/status.py` lines 436–437 can parse it, assert that `tools/status.py` and `tools/value.py` no longer exist in the live checkout, or read `2d99d242:tools/{name}.py` by commit SHA.
3. **`RUNBOOK.md` lines 191, 202, 408** (live runbook on `origin/main`):
   - **Behaviour:** **Harmless.** Line 191 describes pre-move `promote` (`"The verb runs tools/status.py"`), immediately qualified by lines 200–207 (`"**From the push that moves the promotion evaluator under judge/** ... the verb runs judge/status.py in place of tools/status.py"`), and line 408 reads `` `python3 tools/status.py` (`judge/status.py` from the push that moves it, SPEC §10 item 15) ``.
4. **Session templates under `transcripts/sessions/`:**
   - `transcripts/sessions/due-resolve.md` (the active hourly resolver template) was updated at lines 49, 58, 59, 84, 86 to `judge/status.py` and `judge/value.py`.
   - `transcripts/sessions/move-promotion-judge.md` (lines 36, 41–43, 69), `c2a-prime-build.md` (line 18), `c2a-prime-code-review.md` (line 15), `c2a-prime-pins.md` (line 26), `c2b-build.md` (line 13), `c2b-code-review.md` (line 13): **harmless** historical/one-off templates already executed or retired per `transcripts/sessions/README.md` lines 53–75.
   - `transcripts/sessions/c2b-rebuild.md` (lines 18, 22), `c2b-rebuild-pins.md` (line 24), `c2b-rebuild-code-review.md` (line 22): written for the pre-move `builder-c2b-3` branch (`transcripts/sessions/README.md` lines 67–75); **harmless** as records of that rebuild, though if ever re-dispatched against a post-move `main` tree they would **mislead** by naming `tools/status.py` under builder scope rather than `judge/status.py` under the replay test.
5. **Historical text (`SPEC.md` line 496, `CHARTER.md` line 372, `REPORT.md` lines 324, 343, 409, 445, 533, and historical transcripts/briefs/rulings):**
   - Record past runs or name the pre-move files at the move's parent; **harmless**.

---

### 8. Counted lines

Using `judge.judge.counted_lines` with `judge/scope.json`'s `counted` prefixes (`["sim/", "harness/", "tests/", "pins/", "tools/"]`):
- Count at `bd05ed5c`: **8,245** lines (down 102 lines from `origin/main`'s **8,347** lines: 858 lines left `tools/`, while 756 lines were added under `harness/`, `tests/`, `pins/`, and `tools/`).
- `judge/scope.json`'s `cap`: **8,400** lines.
- **8,245 ≤ 8,400** (155 lines under `cap`).

---

### 9. The merge (`git merge-tree --write-tree origin/main bd05ed5c`)

- `git merge-tree --write-tree origin/main bd05ed5c` exits `0` with tree `743dc428f5975a12dac9b53ced1b5c9668f7b70f`: **no conflict**.
- Comparing `bd05ed5c` with `743dc428f5975a12dac9b53ced1b5c9668f7b70f`, the merge changes only `CHARTER.md`, `RUNBOOK.md`, `log.jsonl`, and files under `transcripts/` (**no file outside those four paths**).

---

### 10. Anything else that should stop the sovereign pushing this branch?

No:
- On `origin/main`, Amendment A6 has been transmuted (seq 7178) and entered (seq 7179, `activate_at: 7180`), and a fresh `decision veto C2a-prime` has been entered at seq 7180 (`>= activate_at`), fulfilling `RULING-20261120-promotion-judge.md` answer 17 and leaving no active amendment freeze (`SPEC.md` §10 item 12).
- Every commit in `origin/main..bd05ed5c` carries a valid `Proposer:` trailer within its party's paths.
- Across all 706 rows of `spec/vectors/promotion-replay.json` and all 48 first-parent commits on `origin/main` after *T* (`8130c751`), criterion 3's `--first-parent` walk in `c2a_tree_evidence` agrees with the all-parent walk on rows 0–592 and flips C2a-prime's `unchanged` from `False` to `True` on every commit from row 593 (`b88d318e`) onward, matching the grant's marks.

---

## Findings

1. **NOTE** — `judge/judge.py:218`: unescaped `.` in `SPEC.md` in the grant subject regular expression.
   - `SPEC.md` lines 422–424:
     > `and holds a SPEC.md whose SHA-256, in 64 lowercase hex digits, follows promote_unmet: SPEC.md  at the start of the subject of an earlier decision of kind grant.`
   - `judge/judge.py` line 218:
     ```python
     match = re.match(r"promote_unmet: SPEC.md ([0-9a-f]{64})(?![0-9a-f])", e["body"]["subject"])
     ```
   - The `.` in `SPEC.md` is not escaped as `\.`, so it matches any non-newline character between `SPEC` and `md`. Because grants are signed by a genesis key (`SPEC.md` §10.14) and literal `"SPEC.md"` matches `"SPEC.md"`, this is harmless.

2. **NOTE** — `tests/promotion_replay_spot.py:1–65`: standalone spot-check script under `tests/` is not run by `unittest` or `pins/run.py`.
   - `tests/promotion_replay_spot.py` line 1:
     ```python
     """Run the three SPEC promotion replay spot checks using origin/main's frozen table."""
     ```
   - The file was created to run check (e) of `transcripts/sessions/move-promotion-judge.md` (rows 592, 593, 705). Because its filename does not match `test*.py`, `python3 -m unittest discover -s tests -t .` does not run it, and `pins/replay.py` independently implements the `replay_drift` pin. It is harmless and takes 65 counted lines (leaving total counted lines at 8,245 / 8,400).

VERDICT: PASS
