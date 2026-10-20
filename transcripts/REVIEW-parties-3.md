# Third cold review: parties

Model: `google/gemini-4-argon`

Authority: `SPEC.md` in this directory. Read `SPEC.md` §§7 and 10 in full, `DIFF.patch`, `judge/judge.py`, `judge/scope.json`, `tools/count_kernel.py`, and `pins/pins.py` (with `transcripts/REVIEW-parties.md` and `transcripts/REVIEW-parties-2.md` treated as history).

## Executed checks

- `python3 -m unittest discover -s tests -t .`: exit 0 (`Ran 205 tests in 93.829s`, `OK (skipped=1)`).
- `python3 pins/run.py`: exit 0 (`KILLED 50, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0` across 37 pins).

## 1. Item 7 (`unattributed_proposal`)

**Yes** — the party is taken from the signature of the last `proposal` entry whose `commit` is on the proposal, under the keys in force at that entry. **Yes** — a proposal is refused when no such entry exists or when a later commit touches anything other than `log.jsonl`. **No** — a proposal cannot be attributed to a party whose key did not sign it, by any construction.

> "7. **unattributed_proposal** — the entries the proposal appends to trunk's log contain no `proposal` whose `commit` is a commit of the proposal, or some commit of the proposal after that `commit` changes a path other than `log.jsonl`. The **party** is the `principal` of the key that signed the last such `proposal` entry, under the law in force at it (§7); the kernel has verified the signature, so the party is a fact, not a claim." (`SPEC.md:344–349`)

> "For entry *i* the law in force is what entries 0..*i*−1 established:
> - Genesis's `keys` and every valid `key` entry **declare**. A later declaration of the same key_id replaces the earlier (so empty `powers` revokes, and a re-declaration may change principal and powers).
> - A declaration is refused with **bad_key** if its public key is weak (§6), or if its pubkey blob has **ever** been declared for a *different* key_id, even one since rotated or revoked (one key, one identity, for the life of the log)." (`SPEC.md:188–196`)
>
> "- Genesis is self-certifying: for entry 0 the keys are those its own body declares, registered in array order before its signature is checked.
> - A `key` entry at *i* governs entries > *i*, never itself." (`SPEC.md:204–206`)

In `judge/judge.py`:
- Kernel acceptance of `head_log` runs first (`judge/judge.py:242–247`), verifying every entry's canonical JSON, SSHSIG container, Ed25519 signature, `proposal` power, `proposer` match, and lifetime pubkey-to-`key_id` uniqueness (`kernel/check.py:25–51,70–75`).
- `commits_of(repo, trunk, head)` (`judge/judge.py:85–87`) runs `git rev-list --topo-order head --not trunk`, returning commits reachable from `head` and not from `trunk` with children before parents.
- `proposal_checks` (`judge/judge.py:282–285`) filters to appended entries (`i >= first`, where `first = len(old)`) with `e["type"] == "proposal"` and `e["body"]["commit"] in commits`, refuses with `unattributed_proposal` if `named` is empty, and selects `seq, last = named[-1]`.
- Because `--topo-order` places every descendant of `last["body"]["commit"]` before `last["body"]["commit"]` in `commits`, `itertools.takewhile(lambda c: c != last["body"]["commit"], commits)` (`judge/judge.py:287–289`) visits every commit after `last["body"]["commit"]`, and `changed_by` (`judge/judge.py:89–92`, `git diff-tree -r -m --root --no-commit-id --name-only --no-renames`) inspects each commit individually against every parent (including reverted edits and merges). Any path outside `{"log.jsonl"}` refuses with `unattributed_proposal`.
- `signer_blob(last)` (`judge/judge.py:95–99`) extracts the SSHSIG public-key blob from `last["sig"]`, and `principal_at(entries, seq, blob)` (`judge/judge.py:102–107`) folds `entries[0]["body"]["keys"]` followed by `[e["body"] for e in entries[1:seq] if e["type"] == "key"]` by `key_id` (later replacing earlier, excluding entry `seq` and anything after `seq`) and resolves the unique declaration whose pubkey blob matches `blob` (`judge/judge.py:290`).

## 2. Item 8 (`party_scope`)

**Yes** — `party_scope` reads `judge/scope.json`'s `parties` mapping directly, and **yes** — a party absent from `parties` is unrestricted within `paths`.

> "8. **party_scope** — the proposal touches a path not under a prefix in `judge/scope.json`'s `parties[party]`; a party absent from `parties` may touch anything in `paths`." (`SPEC.md:352–354`)

In `judge/judge.py:281,291–296`:
- `scope` is parsed from trunk's `judge/scope.json` (`json.loads(show(repo, trunk, SCOPE) or b"")`).
- `changed = touched(repo, trunk, head, "--no-renames")` includes both sides of any rename.
- `allowed = scope["parties"].get(report["proposer"])` looks up the party in `scope["parties"]`. When `allowed is not None`, any path `p` in `changed` failing `is_under(p, allowed)` (`judge/judge.py:63–64`) is refused with `party_scope`. When the party is absent from `scope["parties"]`, `allowed` is `None`, so item 8 imposes no restriction and item 9 (`scope["paths"]`) bounds the proposal.

## 3. Item 9 (`out_of_scope` and foreign objects)

**Yes** — every object under `paths` that is not a regular file (symlink `120000` and submodule `160000` alike, whether the submodule commit is present or absent) is refused without the judge crashing, and **yes** — the mode is read before any content.

> "9. **out_of_scope** — the proposal touches a path not under a prefix in `judge/scope.json`'s `paths`, or its head holds, under any prefix in `paths`, an object that is not a regular file: a symbolic link or a submodule (git modes 120000 and 160000) is refused whatever it points to, since the court's repository holds regular files only. (Trusted paths are refused by item 1 whatever the list says.)" (`SPEC.md:358–363`)

And for trusted paths in item 1:

> "The trusted base is regular files only: an object under those paths that is not one (a symbolic link or a submodule, git modes 120000 and 160000) is refused as **trusted_path** at either commit, before any digest is taken, and `tools/digest.py` refuses to digest a tree holding one." (`SPEC.md:325–328`)

In `judge/judge.py`:
- `REGULAR = ("100644", "100755")` (`judge/judge.py:28`).
- `modes(repo, sha)` (`judge/judge.py:51–54`) runs `git ls-tree -r -z <sha>`, which reads only tree objects and reports `(mode, path)` for every leaf entry without dereferencing blobs or looking up submodule commits (`160000`) in the object database.
- `foreign(repo, sha, prefixes)` (`judge/judge.py:124–126`) selects every path under `prefixes` with `mode not in REGULAR`.
- In `judge()` (`judge/judge.py:220–224`), `foreign_base` checks both `trunk` and `head` under `TRUSTED` and refuses with `trusted_path` before `digest()` calls `show()`.
- In `proposal_checks()` (`judge/judge.py:298–301`), `objects = foreign(repo, head, scope["paths"])` refuses with `out_of_scope` before `counted_lines()` runs, and `counted_lines()` itself filters `if mode in REGULAR` (`judge/judge.py:120`) before calling `show()`.

## 4. Item 10 (`code_cap`)

**Yes** — exactly the regular `.py` and python-shebang files under `counted` are counted, by the stated arithmetic, from git objects, with no reference to `tools/count_kernel.py`. **No head can be constructed** on which the judge's count differs from the SPEC's arithmetic.

> "10. **code_cap** — at the proposal's head, the lines of every regular file under a prefix in `judge/scope.json`'s `counted` that is a `.py` file or whose first line is a `#!` line naming `python`, read from the git object, exceed `judge/scope.json`'s `cap`. A file's lines are its `0x0A` bytes, plus one if it is not empty and its last byte is not `0x0A`. The judge is the only counter the cap depends on; `tools/count_kernel.py` applies the same arithmetic to the kernel for CHARTER §9 criterion 3 and binds nothing here." (`SPEC.md:364–370`)

In `judge/judge.py:110–121,155–157,301–302`:
- `modes(repo, sha)` enumerates all tree entries at `head` using `git ls-tree -r -z`, and `counted_lines` keeps only entries with `mode in REGULAR` (`"100644"` or `"100755"`) and `is_under(p, prefixes)`.
- For each such entry, `show(repo, sha, p)` (`judge/judge.py:57–60`) reads the raw blob bytes via `git show <sha>:<path>`.
- `is_python(p, data)` (`judge/judge.py:110–113`) checks `path.endswith(".py") or (first.startswith(b"#!") and b"python" in first)` where `first = data.split(b"\n", 1)[0]` (the bytes before the first `0x0A`, or the whole file if it has no `0x0A`).
- `len(split_lines(data))` (`judge/judge.py:155–157`) splits on `b"\n"` (`0x0A`) and drops a trailing `b""` if present:
  - If `data == b""`, `data.split(b"\n")` is `[b""]`, `lines[:-1]` is `[]`, count is `0` (`0` `0x0A` bytes + `0`).
  - If `data` is non-empty and ends with `0x0A` (`k` `0x0A` bytes), `data.split(b"\n")` has length `k + 1` with `lines[-1] == b""`, so `lines[:-1]` has length `k` (`k` `0x0A` bytes + `0`).
  - If `data` is non-empty and does not end with `0x0A` (`k` `0x0A` bytes), `data.split(b"\n")` has length `k + 1` with `lines[-1] != b""`, so `lines` has length `k + 1` (`k` `0x0A` bytes + `1`).
- This is an exact mathematical identity on `bytes` for every git blob; no commit tree at `head` can produce a different count. `tools/count_kernel.py` is never imported or invoked by `judge/judge.py`.

## 5. `judge/scope.json` vs `SPEC.md`

**Yes** — `judge/scope.json` (`judge/scope.json:1–9`) equals the block in `SPEC.md:402–412` (both byte-for-byte and byte-for-byte less whitespace).

> "The file equals the block below, byte for byte less whitespace; a push that changes one without the other is refused by the tests." (`SPEC.md:395–397`)

## 6. The eight pins

> "Pins for items 7–10, each with its mutant and a passing twin: `unattributed_proposal_admitted` (a proposal with no signed `proposal` entry, or with a commit after it that touches more than `log.jsonl`, is admitted), `counsel_build_admitted`, `builder_pin_admitted`, `reviewer_code_admitted` (for these three the mutant removes that party's list from `judge/scope.json`, and nothing else), `scope_unguarded`, `cap_unguarded`, `shebang_uncounted` (a python file without `.py` under `counted` is not counted), `foreign_object_admitted` (a symbolic link, or a submodule whose commit is present or absent, under `paths` is admitted, or under a trusted path is digested rather than refused)." (`SPEC.md:414–422`)

For each of the eight pins in `pins/pins.py`:

| Pin | Does the fixture exercise the rule? | Does the mutant remove exactly it? | Does the twin pass only because of it? | Could the mutant survive otherwise? |
|---|---|---|---|---|
| `unattributed_proposal_admitted` (`pins/pins.py:116–150, 653–660`) | **Yes.** Exercises: trailer-only with no `proposal` entry (`120`), entry naming trunk's commit (`121–125`), commit after the named commit touching `sim/y.py` (`126–131`), key re-declared to another principal after the entry (`132–139`), two entries naming the work (`ann` then `builder`, `140–148`), and a valid proposal (`149`). | **Yes.** Each of the five mutants (`commit_unchecked`, `later_commits_unchecked`, `law_at_end`, `first_entry_attributes`, `party_by_key_id`) removes one specific clause of item 7 (`judge/judge.py:105,107,282,285,288`). | **Yes.** The unmutated twin passes only because all five clauses hold on their respective sub-fixtures. | **No** on this fixture (each mutant flips its targeted sub-fixture's verdict or `proposer`). A narrower fixture omitting one of those sub-cases would let the corresponding clause mutant survive. |
| `counsel_build_admitted` (`pins/pins.py:159–163, 661–662`) | **Yes.** Refuses `counsel` touching `sim/gen.py` (`party_scope`), and admits `counsel` touching `transcripts/t.txt` and `builder` touching `sim/gen.py`. | **Yes.** `counsel_unlisted` removes `"counsel": [...]` from `judge/scope.json` and nothing else (`pins/pins.py:624–625`, verified by `tests/test_pins.py:50–78`). | **Yes.** The refusal of `sim/gen.py` by `counsel` passes only because `counsel`'s list is present in `judge/scope.json`. | **No.** With `counsel` removed from `parties`, `counsel` is bounded only by `paths` (which includes `sim/`), so `sim/gen.py` is admitted. |
| `builder_pin_admitted` (`pins/pins.py:166–178, 663–664`) | **Yes.** Refuses a proposal touching `pins/p.py` whose last `proposal` entry is `builder`'s (`party_scope`), and admits `reviewer` touching `pins/p.py` and `builder` touching `tests/t.py`. | **Yes.** `builder_unlisted` removes `"builder": [...]` from `judge/scope.json` and nothing else (`pins/pins.py:622`). | **Yes.** The refusal of `pins/p.py` by `builder` passes only because `builder`'s list is present in `judge/scope.json`. | **No.** With `builder` removed from `parties`, `pins/p.py` is under `paths`, so the proposal is admitted. |
| `reviewer_code_admitted` (`pins/pins.py:181–184, 665–666`) | **Yes.** Refuses `reviewer` touching `sim/x.py` (`party_scope`), and admits `reviewer` touching `spec/vectors/v.json`. | **Yes.** `reviewer_unlisted` removes `"reviewer": [...]` from `judge/scope.json` and nothing else (`pins/pins.py:623`). | **Yes.** The refusal of `sim/x.py` by `reviewer` passes only because `reviewer`'s list is present in `judge/scope.json`. | **No.** With `reviewer` removed from `parties`, `sim/x.py` is under `paths`, so the proposal is admitted. |
| `scope_unguarded` (`pins/pins.py:187–200, 667–671`) | **Yes.** Using unlisted party `ann` (isolating item 9 from item 8), refuses `docs/x.md` and refuses renaming `notes.txt` into `transcripts/notes.txt` (`out_of_scope`), and admits `transcripts/notes.txt`. | **Yes.** `scope_unchecked` removes the `scope["paths"]` guard (`judge/judge.py:296`); `rename_hides_source` removes `"--no-renames"` from `changed` (`judge/judge.py:291`), whose item 9 effect is isolated by using unlisted party `ann`. | **Yes.** Both refusals depend on item 9's path check and `--no-renames`. | **No** on this fixture (`scope_unchecked` admits `docs/x.md`; `rename_hides_source` admits the rename from `notes.txt`). Without the rename sub-fixture, `rename_hides_source` would survive. |
| `cap_unguarded` (`pins/pins.py:203–208, 672–674`) | **Yes.** Refuses `sim/big.py` with `cap + 1` lines (`code_cap`), and admits `sim/big.py` with `cap` lines. | **Yes.** `cap_unchecked` removes `if counted_lines(repo, head, scope["counted"]) > scope["cap"]:` (`judge/judge.py:301`). | **Yes.** The `cap + 1` refusal passes only because of the cap check. | **No.** Removing the cap check admits `sim/big.py` at `cap + 1` lines. |
| `shebang_uncounted` (`pins/pins.py:211–217, 675–677`) | **Yes.** Refuses extensionless `tools/big` with `#!/usr/bin/env python3\n` and `cap` more lines (`cap + 1` total, `code_cap`), and admits `cap` total lines or `#!/bin/sh\n` with `cap + 1` total lines. | **Yes.** `py_suffix_only` replaces `return path.endswith(".py") or (first.startswith(b"#!") and b"python" in first)` with `return path.endswith(".py")` (`judge/judge.py:113`). | **Yes.** The refusal of extensionless `tools/big` passes only because python-shebang files are counted. | **No.** Under `py_suffix_only`, `tools/big` contributes 0 counted lines and is admitted. |
| `foreign_object_admitted` (`pins/pins.py:220–261, 678–680`) | **Yes.** Under `paths`, tests a symlink (`tools/script`), a present submodule (`tools/vendor.py`), and an absent submodule (`transcripts/sub`), each refused as `out_of_scope` and named, paired with a regular file twin at the same path that is admitted (`233–243`). Under `TRUSTED`, tests trunk self-check holding a present submodule at `kernel/vendor` (refused as `trusted_path`, with a regular-file twin passing self-check, `244–255`) and a proposal adding an absent submodule at `kernel/vendor` (refused as `trusted_path` without crashing, `256–261`). | **Yes.** `mode_unchecked` removes `if objects:` (`judge/judge.py:299`, item 9), and `trusted_mode_unchecked` removes `if foreign_base:` (`judge/judge.py:222`, item 1). | **Yes.** The `out_of_scope` refusals pass only because of `if objects:` (since `counted_lines` skips non-regular modes, even the symlink to a 9001-line file and the 9000-line submodule commit are otherwise admitted), and the `trusted_path` refusals pass only because of `if foreign_base:` (otherwise the present submodule on trunk is digested and passes self-check, and the absent submodule crashes `digest`). | **No.** Both mutants are killed directly by their respective fixtures. |

## 7. Items 11–14 unchanged

**Yes** — items 11–14 are unchanged in both `SPEC.md` (`SPEC.md:374–390`) and `judge/judge.py` (`judge/judge.py:258–276`; `DIFF.patch:249–260` only hoists `entries = [json.loads(line) for line in new]` above `if head != trunk:` so `entries` can be passed to `proposal_checks`).

- Item 11: "**trusted_base_unrecorded** — trunk's trusted-base digest (item 1) is not the trusted base in force at the end of trunk's log (§7). Applies to the self-check too: a push to `main` that changes the trusted base without a `push` entry naming the new digest turns `main` red (CHARTER §7: every act of Guy's is an entry). Pin `push_unrecorded`." (`SPEC.md:374–378`)
- Item 12: "**push_during_amendment** — a `push` entry whose `seq` lies strictly between an `amend`'s `seq` and its `activate_at`: the law changes first, the code waits for the height. Pin `freeze_ignored`." (`SPEC.md:379–381`)
- Item 13: "**amend_untransmuted** — an `amend` whose `id` is not in the transmuted set at its position: every amendment is two acts, a `decision` of kind `transmute` naming it and then the `amend` (Suber: an entrenched rule is first made mutable, as a separate move). Pin `one_act_amendment`." (`SPEC.md:382–385`)
- Item 14: "**decision_by_other** — a `decision` entry not signed by a key declared in genesis (the sovereign's acts are his own; CHARTER §7). Pin `decision_forged`." (`SPEC.md:386–387`)
- "Items 11–14 apply to every judged log, the self-check included." (`SPEC.md:389`)

## 8. Anything outside `SPEC.md`, `transcripts/`, `judge/`, `tools/count_kernel.py`, `pins/`, `tests/`, `harness/` touched?

**Yes** — `tools/digest.py` is touched (`DIFF.patch:1482–1538`) to implement `SPEC.md` §10 item 1's requirement on `tools/digest.py`:

> "The trusted base is regular files only: an object under those paths that is not one (a symbolic link or a submodule, git modes 120000 and 160000) is refused as **trusted_path** at either commit, before any digest is taken, and `tools/digest.py` refuses to digest a tree holding one." (`SPEC.md:325–328`)

The full set of fifteen paths in `DIFF.patch` is: `SPEC.md`, `harness/build.py`, `harness/gitfix.py`, `judge/judge.py`, `judge/scope.json`, `pins/fixtures.py`, `pins/pins.py`, `tests/test_genesis.py`, `tests/test_judge.py`, `tests/test_pins.py`, `tests/test_tools.py`, `tools/count_kernel.py`, `tools/digest.py`, `transcripts/REVIEW-parties-2.md`, and `transcripts/REVIEW-parties.md`. Nothing outside the listed paths other than `tools/digest.py` is touched.

## Findings

None.

VERDICT: implements SPEC
