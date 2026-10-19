# Second cold review: parties

Model: `openai/gpt-6.1-sol`

Authority: `SPEC.md` in this directory. Read §§7 and 10 in full, then `transcripts/REVIEW-parties.md`, then the whole `DIFF.patch`, then the requested implementation files. Line references below are to the current files unless explicitly labelled `DIFF.patch`.

## Executed checks

- `python3 -m unittest discover -s tests -t .`: exit 0, **200 tests, OK, one skipped**.
- `python3 pins/run.py`: exit 0, **49 KILLED, 0 SURVIVED, 0 STALE, 0 TWIN FAILED, 0 PENDING**, across 37 pins.
- Both commands used `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/opencode`. Additional disposable-repository probes reproduced F4–F5 below. No implementation or test file was changed.

## Closure of F1–F3

### F1 — Not fully closed

The original over-cap symlink admission is closed in the judge. The stronger claim that both implementations now agree for every object under a counted prefix is **false**.

The new governing sentence is:

> “A symbolic link under such a prefix is refused by this item whatever it points to: its lines cannot be counted from the tree it is in, and `tools/count_kernel.py` names it and exits 2 rather than follow it, so that the two never disagree.” — SPEC §10.10, `SPEC.md:361–364`.

`judge/judge.py:115–118` identifies mode 120000; `285–287` refuses it before counting. `tools/count_kernel.py:10–12` uses `O_NOFOLLOW`; `32–35` names and refuses links **that its enumeration discovers**. Without those changes, `tests/test_judge.py:604–621` (`Scope.test_code_cap_refuses_a_symlink_under_counted`), `tests/test_tools.py:42–60` (`CountKernel.test_refuses_to_follow_a_symlink`), and `pins/pins.py:220–232` (`t_symlink_counted`) would fail. These tests do not cover the tool's omission of counted prefixes or Git submodules.

| Git object under a counted prefix | Agreement now? |
|---|---|
| Regular file, mode 100644 | **Yes for per-file classification and physical-line arithmetic**: `judge/judge.py:103–112,148–150` and `tools/count_kernel.py:15–24`. The CLI does not enumerate all such files; see F5. |
| Executable file, mode 100755 | **Yes on the same per-file basis**: executable mode does not change either classifier or line count. A disposable fixture containing a nested `.py` and an executable extensionless Python script produced 3 lines in both implementations and was accepted. |
| Symlink, mode 120000 | **Judge yes; tool not universally**. The judge refuses links under counted prefixes, but the CLI can omit the link and exit 0. `is_python`/`lines` called directly on the link raise `OSError`; that is not the CLI's promised named exit 2. See F5. |
| Submodule/gitlink, mode 160000 | **No**. The judge treats the referenced commit's display as file contents, or crashes if the referenced commit is absent. The tool's `isfile` filter excludes the checked-out directory. See F4. |

Thus the precise original attack no longer succeeds, but F1's requested universal agreement is not established and has concrete counterexamples.

### F2 — Closed

> “`counsel_build_admitted`, `builder_pin_admitted`, `reviewer_code_admitted` (for these three the mutant removes that party's list from `judge/scope.json`, and nothing else)” — SPEC §10 pins, `SPEC.md:411–412`.

`pins/pins.py:593,634–635` now registers `builder_unlisted`, deleting exactly the builder list. `proposal_touching` at `54–57` and the builder fixture at `169` seed trunk from the mutated root, so the scope mutation actually reaches the judge. `t_builder_pin` at `166–178` refuses builder's pin edit and admits reviewer pins and builder tests. The former attribution mutant was moved to the attribution pin (`630`).

Tests that would fail without this repair: `PartyPins.test_the_mutant_removes_exactly_that_partys_list` (`tests/test_pins.py:56–65`) rejects the former judge-code mutation; `PartyPins.test_killed_only_by_admitting_the_forbidden_path` (`67–78`) requires the actual mutated verdict to be acceptance by **builder** of `pins/p.py`. Both passed; `builder_unlisted` was killed by precisely that admission.

### F3 — Closed

The same quoted SPEC sentence now explicitly governs reviewer mutation isolation. `pins/pins.py:594,636–637` registers `reviewer_unlisted`, deleting exactly the reviewer list; `181–184` exercises reviewer code refusal with a passing vector control. `party_by_key_id` is now an attribution mutant (`631`), not the reviewer-scope mutant.

The same two `PartyPins` tests (`tests/test_pins.py:56–78`) would fail with the former identity-resolution mutation. The second requires acceptance as **reviewer** of `sim/x.py`, rather than acceptance as an invented key-ID party. Both passed; the registered mutant was killed by that forbidden-path admission.

## Seven answers on the whole change

### 1. Item 7 — Yes to signed attribution and the refusal guards; no unsigned-party attribution found

> “**unattributed_proposal** — the entries the proposal appends to trunk's log contain no `proposal` whose `commit` is a commit of the proposal, or some commit of the proposal after that `commit` changes a path other than `log.jsonl`.” — `SPEC.md:341–343`.
>
> “The **party** is the `principal` of the key that signed the last such `proposal` entry, under the law in force at it (§7); the kernel has verified the signature, so the party is a fact, not a claim.” — `SPEC.md:344–346`.
>
> “For entry *i* the law in force is what entries 0..*i*−1 established” and “A `key` entry at *i* governs entries > *i*, never itself.” — SPEC §7, `SPEC.md:188–189,206`.

`judge/judge.py:78–80,269–273` restricts candidates to appended entries naming commits reachable from head but not trunk, and selects the last entry. `275–277` checks individual subsequent commits, including reverted changes; `83–85` includes both rename paths and compares merges against each parent. `278` resolves the actual SSHSIG blob using `88–100`, folding declarations by key ID only through entries preceding the selected entry.

Kernel acceptance precedes attribution (`229–234`). The kernel verifies declared-key membership, principal, power and signature (`kernel/check.py:25–41`), and lifetime blob ownership (`44–51`). **No**, within these kernel-validated inputs I found no construction attributing the proposal to a party whose in-force key did not sign the selected entry. A later principal reassignment does not change attribution; a newly declared authorized key does count. Trailers are irrelevant.

Coverage includes `tests/test_judge.py:409–517`: signer principal, trailer-only refusal, non-proposal/trunk commit refusal, appended-only eligibility, later code/revert/merge refusal, last-entry selection, temporal declarations and unknown signer refusal. The attribution pin's five mutants are all killed.

### 2. Item 8 — Yes

> “**party_scope** — the proposal touches a path not under a prefix in `judge/scope.json`'s `parties[party]`; a party absent from `parties` may touch anything in `paths`.” — `SPEC.md:349–351`.

`judge/judge.py:269` reads trunk's scope object; `279–282` uses its `parties` mapping directly. `allowed is not None` preserves the distinction between an absent party and an empty list. `283–284` separately enforces `paths`; prefix matching is `56–57`. **Yes**, an absent party is unrestricted by party scope within `paths`. The three scope-list mutants provide direct evidence against hard-coded party restrictions. Tests: `tests/test_judge.py:533–564`, especially `test_a_party_absent_from_parties_is_bounded_by_paths_only` at `548`.

### 3. Item 10 — No overall; yes for ordinary file arithmetic and the judge's symlink guard

> “**code_cap** — at the proposal's head, the lines of every `.py` file, and of every file whose first line is a `#!` line naming `python`, under a prefix in `judge/scope.json`'s `counted`, counted as `tools/count_kernel.py` counts, exceed `judge/scope.json`'s `cap`.” — `SPEC.md:358–361`.

The next sentence is the symlink requirement quoted under F1. The byte predicates agree (`judge/judge.py:103–106`; `tools/count_kernel.py:15–19`), as do LF-based physical-line counts, including empty files and a missing final LF (`judge/judge.py:112,148–150`; `tools/count_kernel.py:22–24`). `tests/test_tools.py:28–40` compares those primitives; `tests/test_judge.py:587–602,623–633` exercises caps, shebangs and whole-head counting.

**Yes**, the judge refuses an ordinary-named symlink under a counted prefix (`285–287`). **No**, the tool does not universally name and refuse it: its CLI scans only immediate non-hidden `kernel/*` entries (`tools/count_kernel.py:31–37`), not `scope.json`'s counted prefixes. Submodule treatment also disagrees. F4–F5 are executed counterexamples, not merely missing tests.

### 4. Scope block equality — Yes

> “The file equals the block below, byte for byte less whitespace; a push that changes one without the other is refused by the tests.” — SPEC §10, `SPEC.md:389–391`.

`judge/scope.json:1–9` equals `SPEC.md:397–405` after whitespace removal, including member order, prefix order, party lists and cap 5500. I checked this stronger textual comparison directly. `Scope.test_scope_json_is_the_specs` (`tests/test_judge.py:403–407`) also passes, although its parsed-object equality assertion does not itself enforce member order.

### 5. The eight pins — All exercised and killed; exact mutation scope is qualified below

> “Pins for items 7–10, each with its mutant and a passing twin” — `SPEC.md:408`.
>
> “`counsel_build_admitted`, `builder_pin_admitted`, `reviewer_code_admitted` (for these three the mutant removes that party's list from `judge/scope.json`, and nothing else)” — `SPEC.md:411–412`.
>
> “`scope_unguarded`, `cap_unguarded`, `shebang_uncounted` (a python file without `.py` under `counted` is not counted), `symlink_admitted` (a symbolic link under `counted` is admitted).” — `SPEC.md:413–415`.

Here “twin” is the **complete fixture** run on an unedited disposable copy (`pins/run.py:59–62`). Its refusal assertions depend on enforcement; a positive acceptance control alone normally also passes a weakened implementation. All eight complete twins passed. Each registered mutant failed a rule-relevant assertion, not a syntax error or unrelated process failure.

| Pin; fixture and mutant lines in `pins/pins.py` | Exercises rule? | Removes exactly it? | Twin dependence; survival otherwise? |
|---|---|---|---|
| `unattributed_proposal_admitted`; `116–149`, `624–631` | **Yes**: no entry, trunk commit, later code, post-entry principal change, last entry and signer principal. | **Yes for the five targeted clauses**, not one deletion of all item 7: commit membership, later-change refusal, temporal law, last-entry selection and principal resolution. | **Yes**. None survives this fixture. A trailer-only fixture would leave these mutants alive; principal/last-entry mutants are also killed by checking the returned party even where both parties may touch the path. |
| `counsel_build_admitted`; `159–163`, `632–633` | **Yes**: counsel code refused; counsel transcript and builder code admitted. | **Yes**: only counsel's scope list is deleted. | **Yes**. Mutant admits counsel's forbidden code. Neither another party's remaining list nor a different refusal masks it. |
| `builder_pin_admitted`; `166–178`, `634–635` | **Yes**: builder is last signer of a pin edit; reviewer pins and builder tests pass. | **Yes**: only builder's scope list is deleted. | **Yes**. Mutant admits as builder. The earlier reviewer signature is no longer needed to kill the scope mutant; a sole-builder proposal would also kill it. |
| `reviewer_code_admitted`; `181–184`, `636–637` | **Yes**: reviewer code refused; reviewer vector admitted. | **Yes**: only reviewer's scope list is deleted. | **Yes**. Mutant admits as reviewer, independently of the spelling of its key ID. |
| `scope_unguarded`; `187–200`, `638–642` | **Yes**: absent-party signer isolates global scope; rename source is checked. | **Yes** for `scope_unchecked`. **No globally** for `rename_hides_source`: its shared changed-path list also feeds party scope. The absent-party fixture isolates item 9's effect. SPEC mandates exact list-only mutation for the three party pins, not for this additional rename mutant. | **Yes**. Both are killed by forbidden-path admission; without the rename case the rename mutant could survive. |
| `cap_unguarded`; `203–208`, `643–645` | **Yes**: cap+1 refused, cap accepted. | **Yes**: only the numerical cap guard is removed. | **Yes**. Mutant admits cap+1. No survival on the supplied fixture. |
| `shebang_uncounted`; `211–217`, `646–648` | **Yes**: extensionless Python at cap+1/cap and an over-cap shell control. | **Yes for the judge's shebang classifier**; the tool is not mutated. | **Yes**. Mutant admits over-cap Python. A tool-only counting regression can survive this pin; F5 is outside its coverage. |
| `symlink_admitted`; `220–232`, `649–650` | **Yes for the judge**: counted link refused and named; outside-counted link admitted. | **Yes for the judge's symlink refusal guard**; the tool is not mutated. | **Yes**. Mutant admits the short-target counted link because its target-path bytes add no Python lines. A tool-only discovery defect survives this pin, as F5 does. |

The qualifications about extra mutant scope and tool coverage are not additional violations of the pins-list text. They limit what the green pin run proves about item 10.

### 6. Items 11–14 unchanged — Yes

Their SPEC text and enforcement predicates are unchanged by `DIFF.patch`. Parsing `entries` moves before proposal checks; fixtures gain signed attribution so they still reach the later rules.

- **11:** “**trusted_base_unrecorded** — trunk's trusted-base digest (item 1) is not the trusted base in force at the end of trunk's log (§7).” (`SPEC.md:368–369`.) Implemented at `judge/judge.py:245–248`.
- **12:** “**push_during_amendment** — a `push` entry whose `seq` lies strictly between an `amend`'s `seq` and its `activate_at`: the law changes first, the code waits for the height.” (`SPEC.md:373–375`.) Implemented at `judge/judge.py:249–251`.
- **13:** “**amend_untransmuted** — an `amend` whose `id` is not in the transmuted set at its position: every amendment is two acts, a `decision` of kind `transmute` naming it and then the `amend` (Suber: an entrenched rule is first made mutable, as a separate move).” (`SPEC.md:376–379`.) Implemented at `judge/judge.py:252–257`.
- **14:** “**decision_by_other** — a `decision` entry not signed by a key declared in genesis (the sovereign's acts are his own; CHARTER §7).” (`SPEC.md:380–381`.) Implemented at `judge/judge.py:258–263`.

“Items 11–14 apply to every judged log, the self-check included.” (`SPEC.md:383`.) They remain outside the `head != trunk` branch at `judge/judge.py:241–244`. Their four pins (`pins/pins.py:235–253,292–342,604–611`) passed twins and killed their mutants.

### 7. Anything outside the requested edit envelope — No

The envelope is the review request's constraint; no SPEC sentence defines that envelope. The complete diff touches only these twelve paths:

`SPEC.md`, `harness/build.py`, `harness/gitfix.py`, `judge/judge.py`, `judge/scope.json`, `pins/fixtures.py`, `pins/pins.py`, `tests/test_judge.py`, `tests/test_pins.py`, `tests/test_tools.py`, `tools/count_kernel.py`, `transcripts/REVIEW-parties.md`.

Their headers are `DIFF.patch:1,107,133,170,294,312,333,628,1080,1147,1207,1250`. All are within the allowed paths.

## New findings

### F4 — Gitlinks are counted as rendered commits, or crash the judge

**(file:** `judge/judge.py`; **line:** `111–112`, using `files` at `46–47`, `show` at `50–53` and `is_python` at `105`; **SPEC §:** 10.10; **what is wrong:** `ls-tree --name-only` includes mode-160000 gitlinks, but the counter does not filter by object type. `git show head:tools/vendor.py` renders a commit, not Python file bytes, if the referenced commit exists locally. The `.py` suffix then makes the judge count the commit header/message. The filesystem tool excludes the submodule directory at `tools/count_kernel.py:37`. If the submodule commit is absent from the superproject object database, `show` returns `None` and the judge crashes with uncaught `AttributeError` at `105`. A gitlink is neither a regular Python file nor the explicitly refused symbolic link; item 10 does not authorize counting commit messages. This violates the quoted “lines of every `.py` file … counted as `tools/count_kernel.py` counts” requirement. **Fixture that shows it:** both branches below were executed.)

```python
import os
import tempfile
from harness import build, gitfix
from pins.fixtures import make_repo, propose
from judge import judge

with tempfile.TemporaryDirectory() as tmp:
    w = build.World(tmp)
    for kind in ("large", "missing"):
        fx = make_repo(w, tmpdir=tmp)
        if kind == "large":
            gitfix.git(fx.repo, "-c", "user.name=t", "-c", "user.email=t@t",
                       "commit", "-q", "--allow-empty", "-m", "x\n" * 5501)
            target = gitfix.git(fx.repo, "rev-parse", "HEAD")
        else:
            target = "12" * 20  # not present in this fresh object database
        rel = "tools/vendor.py"
        gitfix.git(fx.repo, "update-index", "--add", "--cacheinfo",
                   f"160000,{target},{rel}")
        gitfix.git(fx.repo, "-c", "user.name=t", "-c", "user.email=t@t",
                   "commit", "-q", "-m", "gitlink")
        os.makedirs(os.path.join(fx.repo, rel))  # uninitialized submodule directory
        propose(fx.repo, fx.log, w)
        assert not os.path.isfile(os.path.join(fx.repo, rel))
        print(judge.judge(fx.repo, "main", "pr"))
```

Observed: `large` is refused with `code_cap`, **5505 counted lines** against cap 5500, although no Python blob was added. `missing` raises `AttributeError: 'NoneType' object has no attribute 'split'`; the judge CLI prints no JSON verdict and exits 1 with a traceback. The outcome depends on object-database availability rather than file contents at the proposal's head. Existing tests exercise neither gitlink case.

### F5 — Tool discovery does not implement the promised counted-prefix symlink refusal

**(file:** `tools/count_kernel.py`; **line:** `31–37`; **SPEC §:** 10.10; **what is wrong:** the new refusal scans only immediate `kernel/*` entries. It never discovers links under the actual counted prefixes (`sim/`, `harness/`, `tests/`, `pins/`, `tools/`), and it also skips nested and hidden entries in its own kernel traversal. `O_NOFOLLOW` on a directly requested leaf cannot repair an omitted path. Contrary to the sentence “`tools/count_kernel.py` names it and exits 2 … so that the two never disagree,” the tool exits 0 while the judge refuses the same counted link. **Fixture that shows it:** executed below.)

```python
import os
import shutil
import subprocess
import tempfile
from harness import build, gitfix
from pins.fixtures import make_repo, propose
from judge import judge

with tempfile.TemporaryDirectory() as tmp:
    w = build.World(tmp)
    fx = make_repo(w, tmpdir=tmp)
    os.makedirs(os.path.join(fx.repo, "tools"))
    shutil.copy2("tools/count_kernel.py",
                 os.path.join(fx.repo, "tools", "count_kernel.py"))
    gitfix.link(fx.repo, "tools/nested/link", "../../nowhere")
    propose(fx.repo, fx.log, w)
    assert judge.judge(fx.repo, "main", "pr")["reason"] == "code_cap"
    r = subprocess.run(["python3", "tools/count_kernel.py"], cwd=fx.repo,
                       capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout, r.stderr)  # required result is 2
    assert "tools/nested/link" not in r.stdout + r.stderr
```

Observed tool output ends with `total 435`, exit 0, no link named. An additional minimal tool-only fixture with `kernel/check.py` containing one line, `kernel/nested/a.py` containing 1001 lines and a dangling `kernel/nested/link` likewise exits 0 and reports total 1. Thus the discovery limitation includes nested Python files, not just scope-root selection. `tests/test_tools.py:42–60` tests only immediate visible kernel links; `t_symlink_counted` never invokes the tool. Both suites can remain green with this violation.

VERDICT: does not implement SPEC
