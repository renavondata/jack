# Cold review: parties

Model: `openai/gpt-6-astra`

Reviewed `SPEC.md` §§7 and 10 in full, then `DIFF.patch`, followed by the requested implementation and pin files. SPEC in this directory is the authority.

## Executed checks

- `python3 -m unittest discover -s tests -t .`: exit 0; **196 tests, OK, one skipped**.
- `python3 pins/run.py`: exit 0; **46 KILLED, 0 SURVIVED, 0 STALE, 0 TWIN FAILED, 0 PENDING** across 36 pins.
- Both commands used `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=/tmp/opencode` to keep generated artifacts outside the working tree. The default interpreter was Python 3.14.7.
- Additional disposable-fixture checks reproduced finding F1 and the mutation-isolation limitations in F2–F3 below. Passing suites do not eliminate these findings.

## 1. Item 7: signed attribution

**Yes** to selecting the last qualifying appended entry, using its signing key under the law at that entry, and refusing missing attribution or later non-log changes. **No** to attribution to a different named party whose key did not sign that entry: I found no such construction within a kernel-valid log and the Git objects being judged.

SPEC §10.7 says:

> “**unattributed_proposal** — the entries the proposal appends to trunk's log contain no `proposal` whose `commit` is a commit of the proposal, or some commit of the proposal after that `commit` changes a path other than `log.jsonl`.” (`SPEC.md:341–343`)

> “The **party** is the `principal` of the key that signed the last such `proposal` entry, under the law in force at it (§7); the kernel has verified the signature, so the party is a fact, not a claim.” (`SPEC.md:343–346`)

And §7 specifies:

> “For entry *i* the law in force is what entries 0..*i*−1 established” (`SPEC.md:188–189`), and “A `key` entry at *i* governs entries > *i*, never itself.” (`SPEC.md:206`)

`judge/judge.py:264–267` filters to appended proposal entries naming commits reachable from the proposal but not trunk, then selects `named[-1]`. Lines 269–271 inspect intervening commits individually, including reverted changes; `changed_by` at lines 83–85 compares merges against each parent and disables rename collapsing. Lines 95–100 rebuild declarations by key ID through the entry's preceding state, and line 272 resolves the actual SSHSIG public-key blob. Kernel verification precedes this (`judge/judge.py:223–228`). The kernel enforces principal matching, signature validity and lifetime public-key ownership (`kernel/check.py:25–41,44–51`). Trailers do not participate.

## 2. Item 8: party scope

**Yes.** The implementation reads trunk's `scope.json` and uses its `parties` mapping directly. **Yes**, an absent party is unrestricted by item 8 but remains restricted by item 9's `paths`.

> “**party_scope** — the proposal touches a path not under a prefix in `judge/scope.json`'s `parties[party]`; a party absent from `parties` may touch anything in `paths`.” (`SPEC.md:349–351`, §10.8)

See `judge/judge.py:263,273–278`; prefix matching is at lines 56–57. An empty list is restrictive, not mistaken for an absent party. Rename source and destination are both considered. No hard-coded party list controls this check.

## 3. Item 10: identical Python counting

**No, not for every supported Git file.** Both implementations recognize ordinary extensionless Python-shebang files, and their physical-line counts agree for ordinary file bytes, including empty files and missing final newlines. They disagree on symlinks; F1 demonstrates an accepted over-cap proposal under the counting tool's semantics.

> “**code_cap** — at the proposal's head, the lines of every `.py` file, and of every file whose first line is a `#!` line naming `python`, under a prefix in `judge/scope.json`'s `counted`, counted as `tools/count_kernel.py` counts, exceed `judge/scope.json`'s `cap`.” (`SPEC.md:358–361`, §10.10)

The ordinary-file predicates match (`judge/judge.py:103–106`; `tools/count_kernel.py:10–14`). The divergence is between reading Git blob contents (`judge/judge.py:109–112`) and following filesystem symlinks with `open` (`tools/count_kernel.py:12–19`).

## 4. Scope block equality

**Yes.** `judge/scope.json:1–9` equals the block at `SPEC.md:394–402`, disregarding whitespace, including array order, the three party lists and cap 5500.

> “The file equals the block below, byte for byte less whitespace; a push that changes one without the other is refused by the tests.” (`SPEC.md:386–388`, §10)

The test also passed, although its JSON-object equality assertion is weaker than literal equality after removing insignificant whitespace. The actual files satisfy the stronger comparison.

## 5. The seven pins

> “Pins for items 7–10, each with its mutant and a passing twin: `unattributed_proposal_admitted` (a proposal with no signed `proposal` entry, or with a commit after it that touches more than `log.jsonl`, is admitted), `counsel_build_admitted`, `builder_pin_admitted`, `reviewer_code_admitted`, `scope_unguarded`, `cap_unguarded`, `shebang_uncounted` (a python file without `.py` under `counted` is not counted).” (`SPEC.md:405–410`, §10)

Here, “twin” means the complete fixture run against an unedited implementation, as implemented by `pins/run.py:59–62`. A valid positive control normally also passes a weakened implementation; its acceptance alone cannot prove enforcement. All seven complete twin runs passed, and every registered mutant was killed by an assertion about a verdict, rather than a syntax error or incidental crash.

| Pin | Does the fixture exercise the rule? | Does the mutant remove exactly it? | Does the complete twin depend on it? Could the mutant survive otherwise? |
|---|---|---|---|
| `unattributed_proposal_admitted` | **Yes** (`pins/pins.py:116–140`): trailer-only, trunk commit, later code change, and post-entry principal change. | **Yes for the individual targeted clauses**, not removal of the entire item: `commit_unchecked`, `later_commits_unchecked`, and `law_at_end` respectively change commit membership, later-change enforcement, and temporal key lookup (`595–599`). None directly removes the no-entry guard. | **Yes. No registered mutant survives.** The first two wrongly accept their negative fixtures; `law_at_end` wrongly refuses the valid rotation fixture. The corresponding admitted controls isolate membership/later-change behavior. A test containing only the trailer-only case would leave all three mutants alive. |
| `counsel_build_admitted` | **Yes** (`150–154`): counsel code is refused; counsel transcript and builder code are admitted. | **Yes for item 8's shared guard**, but it disables all parties' restrictions, not counsel alone (`600–602`). | **Yes. No**, the registered mutant wrongly admits counsel's code. The controls change the path or signing party, rather than tripping a different refusal. |
| `builder_pin_admitted` | **Yes** (`157–169`): the last signer is builder on a pin edit, with reviewer and builder-test controls. | **No.** `first_entry_attributes` changes item 7's last-entry selection; it leaves item 8's builder restriction intact (`603–604`). See F2. | **Yes**, but the twin depends on both attribution and scope. **No** survival in the registered fixture: it attributes to reviewer and admits. **Yes** with a sole builder entry instead: the mutant still refuses it, as reproduced. |
| `reviewer_code_admitted` | **Yes** (`172–175`): reviewer code is refused; a reviewer vector is admitted. | **No.** `party_by_key_id` corrupts attribution for every party; it does not remove the reviewer restriction (`605–606`). See F3. | **Yes**, through attribution plus scope. **No** survival with the registered `reviewer-1` key ID: the mutant admits code under an absent party. **Yes** when the reviewer's key ID is `reviewer`: the mutant still refuses reviewer code, as reproduced. |
| `scope_unguarded` | **Yes** (`178–191`): absent-from-parties signer `ann` isolates global scope; the rename tests its out-of-scope source. | `scope_unchecked`: **yes**. `rename_hides_source`: **not globally exact**, because the shared changed-path list also feeds item 8; this fixture's absent party isolates its item 9 effect (`607–611`). | **Yes. No registered mutant survives.** Both yield acceptance of the relevant forbidden path. The in-scope transcript passes; without the rename case the rename mutant would survive. |
| `cap_unguarded` | **Yes** (`194–199`): cap+1 is refused; exactly cap is admitted. | **Yes** (`612–614`): removes just the cap guard. | **Yes. No**, its over-cap proposal becomes accepted. The boundary control differs only in line count. |
| `shebang_uncounted` | **Yes for ordinary files** (`202–208`): extensionless Python at cap+1/cap, plus an over-cap shell script. | **Yes for the judge's shebang arm** (`615–617`); the counter tool is not mutated. | **Yes. No**, the registered mutant admits the over-cap Python script. **Yes for an independent counter-tool regression**, which this pin never invokes. The existing fixture also misses F1's symlink disagreement. |

F2–F3 are mutation-isolation findings under the question's “exactly it” criterion. They do not independently establish that the production item 8 predicate is wrong: the fixtures themselves genuinely exercise the named restrictions.

## 6. Items 11–14 unchanged

**Yes.** Their SPEC text and implementation predicates are unchanged. The implementation remains at `judge/judge.py:239–257`; the diff moves entry parsing before proposal checks but does not alter these predicates. Proposal fixtures now acquire the signed attribution required to reach them. Their mutants were all killed, and the unit tests passed.

- Item 11: “**trusted_base_unrecorded** — trunk's trusted-base digest (item 1) is not the trusted base in force at the end of trunk's log (§7).” (`SPEC.md:365–366`)
- Item 12: “**push_during_amendment** — a `push` entry whose `seq` lies strictly between an `amend`'s `seq` and its `activate_at`: the law changes first, the code waits for the height.” (`SPEC.md:370–372`)
- Item 13: “**amend_untransmuted** — an `amend` whose `id` is not in the transmuted set at its position: every amendment is two acts, a `decision` of kind `transmute` naming it and then the `amend` (Suber: an entrenched rule is first made mutable, as a separate move).” (`SPEC.md:373–376`)
- Item 14: “**decision_by_other** — a `decision` entry not signed by a key declared in genesis (the sovereign's acts are his own; CHARTER §7).” (`SPEC.md:377–378`)
- “Items 11–14 apply to every judged log, the self-check included.” (`SPEC.md:380`)

## 7. Changes outside the requested envelope

**No.** The edit envelope is imposed by the review request, not by a SPEC sentence. `DIFF.patch` contains exactly these eleven changed paths:

`SPEC.md`, `harness/build.py`, `harness/gitfix.py`, `judge/judge.py`, `judge/scope.json`, `pins/fixtures.py`, `pins/pins.py`, `tests/test_judge.py`, `tests/test_pins.py`, `tests/test_tools.py`, `tools/count_kernel.py`.

Their diff headers are at `DIFF.patch:1,102,128,151,264,282,303,557,990,1012,1050`. Every path is inside the supplied envelope.

## Findings

### F1 — Counter disagreement permits an over-cap Python symlink

**(file:** `judge/judge.py`; **line:** 111–112, together with `tools/count_kernel.py:12–19`; **SPEC §:** 10.10, `SPEC.md:358–361`; **what is wrong:** the judge classifies and counts the symlink's stored target-path bytes, while the tool follows the link and classifies/counts the target's contents. There is no SPEC exemption reconciling those two counts. With a target outside `counted`, this makes the judge accept a proposal that exceeds the cap under the prescribed tool's counting semantics; **fixture that shows it:** the following disposable fixture was executed.)

```python
import os
import tempfile
from harness import build, gitfix
from pins.fixtures import make_repo, propose
from judge import judge
from tools import count_kernel

with tempfile.TemporaryDirectory() as tmp:
    w = build.World(tmp)
    fx = make_repo(w, tmpdir=tmp)
    gitfix.write(fx.repo, "transcripts/long",
                 "#!/usr/bin/env python3\n" + "x = 1\n" * 5500)
    os.makedirs(os.path.join(fx.repo, "tools"))
    os.symlink("../transcripts/long",
               os.path.join(fx.repo, "tools/script"))
    propose(fx.repo, fx.log, w)

    path = os.path.join(fx.repo, "tools/script")
    assert count_kernel.is_python(path)
    assert count_kernel.lines(path) == 5501
    assert judge.counted_lines(fx.repo, "pr", ["tools/"]) == 0
    result = judge.judge(fx.repo, "main", "pr")
    assert (result["ok"], result["reason"], result["proposer"]) == (
        True, None, "builder")
```

Observed: tool **5501**, judge **0**, proposal **accepted**. Resolving the policy either way requires consistent handling in both implementations; the current code is not identical as §10.10 requires.

### F2 — Builder pin's mutant changes attribution, not the builder restriction

**(file:** `pins/pins.py`; **line:** 603–604; **SPEC §:** 10.7–8 and the pin requirement at `SPEC.md:405–409`; **what is wrong:** under the requested exact-rule isolation criterion, selecting `named[0]` tests last-entry attribution rather than removing the builder's pin restriction. Its kill is genuine but proves a conjunction of two rules; **fixture that shows it:** run `proposal_touching(mutated_root, "pins/p.py", "builder")` against this registered mutant, with only the helper's single signed proposal entry. Executed result: `ok=False`, `reason="party_scope"`, `proposer="builder"`. Thus the builder restriction remains enforced. The supplied two-entry fixture kills it because it first misattributes the proposal to reviewer.)

### F3 — Reviewer pin's mutant changes identity resolution, not the reviewer restriction

**(file:** `pins/pins.py`; **line:** 605–606; **SPEC §:** 10.7–8 and the pin requirement at `SPEC.md:405–409`; **what is wrong:** returning `key_id` instead of `principal` corrupts attribution globally. Admission depends on the fixture's key ID being absent from `parties`, rather than removal of reviewer scope; **fixture that shows it:** change only the reviewer's genesis declaration from key ID `reviewer-1` to `reviewer`, retain principal `reviewer`, and run `proposal_touching(mutated_root, "sim/x.py", "reviewer")` against the registered mutant. Executed result: `ok=False`, `reason="party_scope"`, `proposer="reviewer"`. The reviewer restriction still operates. The existing fixture kills the mutant by obtaining unrestricted party `reviewer-1`.)

VERDICT: does not implement SPEC
