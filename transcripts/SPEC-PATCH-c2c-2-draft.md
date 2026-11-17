# SPEC patch for C2c-2 (draft v4, counsel-5, 17 November 2026, after the read of v3 at runner issue #976, `VERDICT: FAIL`) — one kind, one ground, three checks at the push

This is the text a builder's branch for C2c-2 begins with (RUNBOOK §`jack push`: "a change to SPEC.md that needs code is the first commit of the builder's branch — counsel's patch, applied and read by Guy there"). It binds nothing until that push. The texts on `main` are already named by entries: every `merge` carries the commit it merged and every `push` the digest it authorised, so what `main` holds at any prefix is a function of the log. Two things are not: a direction or ruling of the sovereign's made in a chat, and a read that a convention requires and nothing checks. The patch adds one `decision` kind for the first, and for the second one judge ground and three checks in the push verb. `enact` as a unification of `push` and `amend` is not needed for the bootstrap and waits for a case.

**The sovereign's answers.** On 17 November 2026 he answered the seven questions of `transcripts/QUESTION-20261111-constitution.md` §5: "Then indeed, yes to all 7 questions". This patch carries two of the directions: 4 ("from C2c-2 each [ruling] is signed by a `wish`") and 5 ("his read is an entry naming bytes, with the prefix rule; counsel files no session without one, and C2c-2's texts put the check at the push"). Before that, on 8 November: `wish` and `unread_text` in C2c-2's push (COUNSEL-OPEN row 46 d); and row 53: his read "checked by `jack push` with the party check".

**What changed from v3.** The read of v3 found that the subject rule could be applied too widely (§1), that ground 15 could be gone round in seven ways and did not say what happens when a reviewed tree cannot be fetched (§2), that the push checks later assigned to C2c-2 were absent while v3 promised not to change `push` (§3), and that v3's inventory was not the whole build and supported no count (§4). Each is answered below.

## 1. `wish`: the sovereign's directions, rulings and reads as entries

**SPEC §5, the `decision` row.** `kind`: one of `veto promote budget grant transmute fix wish`. The rule that follows applies to an entry whose `type` is `decision` and whose body's `kind` is `wish`, and to no other entry. For such an entry, `subject` matches `^transcripts/[A-Za-z0-9][A-Za-z0-9._/-]*@sha256:[0-9a-f]{64}$`: a path under `transcripts/` and the SHA-256 of a file's bytes. A `decision` of any other kind keeps §5's present rule for `subject`. A body of any other type is not read by this rule, whatever members it carries. No required member is added to any type.

**Validity is the kernel's, as for any `decision`.** §8's steps apply unchanged: the entry is valid when its signing key holds `decision` at that prefix. That a `wish` is the sovereign's is not the kernel's question. It is the judge's ground 14, unchanged, which admits a `decision` only from the key declared in genesis under the law in force. The kernel reads `log.jsonl` only (§1): it tests no file, no tree, and no key state but the prefix's own.

**Replay.** Every log that is valid before this patch is valid after it, with the same state. There is one widening: a log that was refused before only because a `decision` had kind `wish` is valid after, when that subject has the shape.

**SPEC §7.** No new state. The kernel records a `wish` like any `decision`.

**What a wish is (SPEC §10, informative; the clerk).** A `wish` is the sovereign's signature over a text's bytes. It is counted by the acts evidence as a decision and not a repair, dated by the log, and named by hash so that nobody can later say he signed something else. It is an act, not an executable rule: the clerk evaluates no prose. One kind serves three uses:

- a **ruling**: the wish names the `transcripts/RULING-*.md` file that records his answer (answer 4);
- a **direction**: the wish names the file that quotes it;
- a **read**: the wish names the text a builder is to write code to (answer 5).

The decidable part is presence. `tools/clerk.py` prints `W6 wish <seq>: <path>@sha256:<hex> — <commit> | absent`, where `<commit>` is the first commit on `main`'s first-parent history at which the path has those bytes, and `absent` when none does. A later change to the file does not unbind the wish: the bytes it names stay in history.

**A read list.** A wish may name a file under `transcripts/reads/` whose every line is `<path>@sha256:<hex>`, the same shape. The clerk then prints one further `W6` line for each pair in it, marked `via <seq>`. The kernel does not know the difference. This is how several texts are read in one entry.

**The prefix rule** (answer 5): "a read of bytes that extend bytes already read is a read of the extension". It says what he needs to read when a text he has read is extended. No code decides it: every check below looks only for a wish that names the bytes on `main`.

**The first wishes.** C2c-2's window file lists the paths whose wishes are a criterion of the window, and BRIEF-C2c-2 names them: at least `transcripts/RULING-20261104-window-fix.md`, the ruling that records his answers of 17 November, and `transcripts/COUNSEL-OPEN.md`. The criterion is that a wish naming each is on the log with `W6` printing a commit. `transcripts/CASES.md`'s "Rulings are not entries on the log" ends at the first `wish`; its index stays as the reading aid.

**Kernel2.** `isDecisionKind` gains `wish`. The subject shape is checked by the same regular expression, written out in `checker.go` as the Python kernel writes it, under the same condition: type `decision`, kind `wish`, no other entry.

**Vectors** (the reviewer's proposal after the push, since they pass only against the new kernel):

- `spec/vectors/logs/<n>_wish_ok.jsonl`: a `wish` by the master key with a well-formed subject, admitted;
- `<n>_wish_bad_kind.jsonl`: `kind: wisj`, schema;
- `<n>_wish_bad_subject.jsonl`: a `wish` whose subject lacks the hash, schema;
- `<n>_wish_other_kind_ok.jsonl`: a `grant` whose subject is ordinary prose, admitted (the shape is not asked of another kind);
- `<n>_wish_member_elsewhere_ok.jsonl`: a `forecast` whose body carries a member `kind` with the value `wish` and a member `subject` of any text, admitted as before.

And one judge test: a `wish` signed by a key that holds `decision` and is not the genesis key is valid in both kernels and refused by the judge under ground 14.

The differential's simulator kind `wish` (`sim/gen.py`) is the builder's proposal after the push, with `tests/test_sim.py`'s `KINDS` slice.

## 2. `unread_text`: the read a text that claims force must carry

**SPEC §10, a fifteenth ground (the judge, not the kernel).**

15. **unread_text** — the proposal changes a path that the `read` list of `judge/scope.json` covers, and no review on `main` qualifies for it.

**Covered.** A path is covered when a `read` entry matches it. An entry ending in `/` matches the directory. An entry ending in `*` matches every path that begins with the part before the `*` (the `read` list alone admits `*`; `paths`, `parties` and `counted` keep §10's rule). Any other entry matches exactly that file.

**A qualifying review** meets all of these:

1. It is a file `transcripts/REVIEW-*.md` on `main` at the judgment, brought there by a `proposal` entry whose commit adds it and whose proposer is of another principal than this proposal's proposer.
2. Its blob on `main` equals its blob at that proposal's `commit`. A later edit of an accepted review by anyone makes it no review (BRIEF-C2b §Scope's rule, kept).
3. Its first line is `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`.
4. Its `Reviewed tree:` line names a commit C that the judge's checkout holds after `git fetch origin C`. C need not be reachable from the proposal's head: the court re-proposes by cherry-pick, and a review of the bytes is a review of the bytes. Where the fetch fails, or C is not a commit, the review does not qualify. The judge fails closed, the refusal names `reviewed tree unavailable`, and the proposer proposes again.
5. For every covered path changed between the proposal's merge base with `main` and its head — added, modified or deleted — the bytes at C equal the bytes at the head. A path absent at both counts as equal.
6. Its `Reader:` line names one model, and the model's family differs from the family of every drafter's commit, as defined next.

**Drafters, readers and families.** A model id has the shape `^[a-z0-9][a-z0-9-]*/[A-Za-z0-9][A-Za-z0-9._:-]*$`, and its family is the part before the `/`. Every commit after the merge base that is not a merge commit and changes a covered path is a drafter's commit. A drafter's commit carries exactly one `Model:` trailer whose value has that shape, read by `git log -1 --format=%(trailers:key=Model,valueonly)`. A drafter's commit with no such trailer, with more than one, or with a value of another shape is refused on this ground: a drafter that does not say what it is cannot be read by something else. The reader's model is the token after `model ` up to the next `;` in the line `Reader: <party> <key_id>; model <model id>; <date>`, the form the record's reviews already use; a review with no such line, with more than one, or with a value of another shape does not qualify.

**Merges.** A merge commit after the merge base whose tree holds, at a covered path, bytes that none of its parents holds at that path is refused on this ground. Covered text is not written in a merge.

**The `read` list at C2c-2.** `transcripts/sessions/`, `transcripts/windows/`, `transcripts/runner/`, `tools/runner/`, `transcripts/reads/`, `transcripts/BRIEF-*`, `BRIEF-C1.md`, `transcripts/SPEC-PATCH-*`, `transcripts/AMEND-*`, `transcripts/PUSH-*`, `transcripts/RULING-*`, `transcripts/CASES.md`, `transcripts/COUNSEL-OPEN.md`, `LAW.md`, `RUNBOOK.md`, `tools/enforcement.json`. These are the texts that carry a rule or an acceptance criterion that code is written to (answer 5's scope), the texts that claim force or index it (COUNSEL-OPEN row 34's list), and the notes whose commands the sovereign pastes. `COUNSEL-OPEN.md` is on the list because the clerk gives its rows force today: a row naming `W3 merge <seq>` discharges that writ (`tools/clerk.py`). The cost is a read for each batch of rows, which is counsel's and is the point.

**Not on the list, and why that is safe.** `REVIEW-*` (a review of a review is not asked), `REPLY-*`, `RESEARCH-*`, `QUESTION-*`, the reports and the evidence. They claim no force, and no builder writes code to them. Check (c) of §3 is what makes the second true at a push; and a session template that sent a builder to one of them would itself be a covered change.

**What the ground does not establish.** `Model:` and `Reader:` are claims a session makes about itself. The runner's issue is the only record of them outside the tree. The ground makes a drafter name itself and makes the reader differ from it; it does not prove who read. Who reads is still chosen by the drafter until readers are drawn (C2c-3, B4). A2.10's read by the sovereign is a different act from this one, and passing one proves nothing of the other.

**The same rule as the opening gate, moved.** `tools/jack push --opens` (#182) already requires, for a brief, a review on `main` brought by a proposal of another principal whose reviewed bytes equal the brief's. Ground 15 is that rule for every covered path and every proposal, in the judge, where a session cannot route round it. The order of acts: the drafter pushes the draft branch and opens no pull request; a reader of another family reads it at a commit and proposes the review naming that commit (its path is not covered, so no review is needed for a review); the herald merges the review; the drafter then merges `main` and proposes — last, so that the review is on `main` before the proposal is judged, and the proposal is not staled by the review's own merge.

**Why the judge and not the kernel.** A read is a file in the tree and a line in it; the kernel reads bytes of `log.jsonl` only (§1). The ground reads trees and the log, which is the judge's domain (§10 preamble), and nothing outside git and the log (A2.3).

**Pin `text_unread`.** Twins:

1. a proposal changing a session template with no qualifying review → refused;
2. the same with a review on `main` by another principal, its `Reviewed tree` at a commit holding the head's bytes, a reader of another family → admitted;
3. the review's `Reviewed tree` at a commit whose bytes differ from the head's → refused;
4. the reader's model equal to the drafter's → refused;
5. a drafter's commit without a `Model:` trailer → refused;
6. the review added on the proposal's own branch, not on `main` → refused;
7. the review's blob on `main` edited after the proposal that added it → refused;
8. a deletion of a covered path, with a review whose commit still holds the file → refused;
9. the review naming a commit on an unmerged branch, not reachable from the proposal's head, holding the head's bytes → admitted;
10. a reader of the drafter's family and another model → refused;
11. two drafter's commits of two families, and a reader of one of them → refused;
12. a drafter's commit with two `Model:` trailers → refused;
13. a merge commit that holds covered bytes neither parent holds → refused;
14. a merge of `main` that changes no covered path by its own hand → admitted;
15. a `Reviewed tree` that cannot be fetched → refused, naming `reviewed tree unavailable`.

Mutants: the bytes test dropped (3); the model test dropped (4); the trailer not required (5); a branch review accepted (6); the blob test dropped (7); a deletion not counted as a change (8); reachability from the head required (9); models compared as whole strings (10); only the newest drafter's commit read (11); several trailers accepted (12); merge commits skipped (13); every merge refused (14); an unavailable tree admitted (15).

## 3. Three checks at the push

A push is not judged by ground 15: it is the sovereign's act, and it carries the brief the reviews name. So the verb checks what the judge does not. `tools/jack push` refuses a branch that changes a counted path or the trusted base unless all three hold. They are new in C2c-2; v3 said the patch did not change `push`, and that sentence is withdrawn.

**(a) Parties.** Each commit of `origin/main..<branch>` that is not a merge commit changes only paths that the party named in its `Proposer:` trailer may write under SPEC §10.8's scopes. A commit that changes the trusted base carries the sovereign's own `Proposer:` (his entries at seqs 4017 and 4634 state why: the patch is applied by his own hand). A merge commit on the branch holds, at every counted or trusted path, bytes that one of its parents holds at that path.

**(b) The code read.** `--review FILE` names a review, and `--review none` is refused. The file's first line is `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`. Its `Reviewed tree:` line names a commit R such that, for every path that differs between `origin/main` and the branch head other than the review file itself, the bytes at R equal the bytes at the head. Its `Reader:` line names one model whose family differs from the family in the `Model:` trailer of every commit of (a) that changes a counted path; such a commit carries exactly one `Model:` trailer of §2's shape, the sovereign's own commits apart.

**(c) His read (A2.10).** The texts the branch's code is written to are the layer's brief, `transcripts/BRIEF-<layer>-draft.md`, and the paths that brief lists under the heading `## Texts the code is written to`. For each of them, the log on `origin/main` holds a `wish` that the judge admits and that names the path with the SHA-256 of its bytes on `origin/main`, directly or through a read list (§1). And every commit of (a) that changes a counted path or the trusted base descends from the first commit on `main`'s first-parent history that carries that wish's entry. Code written before the read does not enter.

**What (c) does not establish.** Descent shows that a commit was made after the read. It does not show that the code was written anew: old work committed again after the read passes it. Where a breach has made a rebuild necessary, the independence of the rebuild is a question put to the code read, as BRIEF-C2b's question (8) was.

**Before `wish` exists.** C2c-2's own opening push is made by the verb as it stands, and his read of this patch and of BRIEF-C2c-2 is stated in a `grant`, as at seqs 3432 and 4643. The three checks bind from the first push after the proposal that carries them has merged.

**Pin `push_unread_code`.** Twins:

1. a commit that changes a path outside its party's scope → refused;
2. a review whose first line is not an accepting verdict → refused;
3. a `Reviewed tree` whose bytes differ from the head's at a changed path → refused;
4. no wish naming the brief's bytes on `origin/main` → refused;
5. a code commit that does not descend from the wish's commit → refused;
6. `--review none` with a counted change → refused;
7. a reader of the builder's family → refused;
8. a wish that names the brief through a read list, every other condition met → the verb proceeds;
9. a branch that changes only `transcripts/` evidence and no counted or trusted path → the verb proceeds without the three checks.

Mutants: the party check dropped (1); any review accepted (2); the bytes test dropped (3); the wish not required (4); descent not required (5); `none` allowed (6); families not compared (7); read lists not followed (8); the checks applied to every push (9).

## 4. What the push carries, and what follows it by proposal

The push is `jack push <branch> --review <file> --opens C2c-2`. It changes `judge/scope.json`, so the verb requires `--opens`, and `--opens` requires `transcripts/BRIEF-C2c-2-draft.md` and its reviews on `main` beforehand: the brief is proposed and merged first, under today's read convention, and the push carries no brief. It comes with the run of record, since `kernel/` changes, and is read by two families.

**In the push** (the trusted base, and what must travel with it):

- `SPEC.md`: §5's row and rule (§1 above); §10's ground 15, the `read` rule and the families (§2 above);
- `kernel/log.py`: the kind set and the `wish` subject shape under §1's condition; and the `NaN` fix (`transcripts/REVIEW-audit-3-6-argon.md` D1: a `parse_constant` that raises);
- `kernel2/checker.go`: `isDecisionKind` and the subject shape under the same condition;
- `judge/judge.py`: ground 15 with the `read` matcher, the drafter, reader and merge rules; D5 (`decision_by_other` keyed on the genesis `key_id` under the law in force); D6 (ground 5's order);
- `judge/scope.json`: the `read` list of §2;
- `tests/test_judge.py`: the tests of grounds 14 and 15 (D5 turns `test_decision_requires_original_genesis_blob_not_principal_or_id` red: carried, named);
- `pins/pins.py`: the two `find` strings that the fixed lines would otherwise leave STALE, `big_integer_unreadable` (`kernel/log.py:73`) and `decision_forged` (`judge/judge.py:274`), as the reviewer's trailered commits, because `jack push` runs the pins on the branch and a STALE pin refuses the push;
- `.github/workflows/judge.yml` and `tests.yml` with D8 (`setup-go`; the seeds comment); `tests.yml`'s `count_kernel.py --limit <N>`; and `publish.yml` (`transcripts/runner/monitor.md`: the publication step is inline in the workflow, trusted base, with no script outside it).

**Then by proposal, in this order:**

1. the builder's `tools/jack` `KINDS` with `wish`, and the clerk's `W6` line with read lists. The verb refuses `jack decision wish` until this merges, so the first wishes are entered after it, not with the push;
2. the builder's three checks of §3 in `tools/jack push`;
3. the reviewer's vectors of §1 and the pins `text_unread`, `push_unread_code`, `nan_not_malformed`, `decision_rotated_master`, `grounds_5_order`, `workflow_go_and_seeds`;
4. the builder's simulator kind and `tests/test_sim.py`;
5. the session templates' `Model:` line: a session's content commits carry `Model: <model id>` as a trailer, written by the session from the issue's `model:` header; counsel's hand commits carry it beside `Proposer:`.

Nothing under `spec/vectors/` or `sim/` rides in the push (SPEC §10.1, §10.8).

**This is the patch's inventory, not the window's.** BRIEF-C2c-2 lists the whole build: this patch, the monitor's verifier, the custody text's users, and the criteria. That brief is the text the three checks of §3 will look for.

**The count.** No count is stated here, because none can be defended before the code exists. The builder reports `counted_lines` and the kernel's count at the branch head before the reviewer pins; BRIEF-C2c-2 pre-states the cap and `count_kernel.py`'s `<N>` from that report, and the push's review states both. Today `main` stands at 8,347 of 8,400 counted lines and the kernel at 450 of 500; C2b and C2c-1 open first, and each sets its own cap.

## 5. What this patch does not do

It changes `push` by the three checks of §3 and in no other way. It does not change `amend`, `transmute` or the charter's procedure (A2.7, SPEC §10.13). It does not add `claim` or `enact`. It does not make the sovereign the author of session templates: a template changes by a counsel proposal with a read on `main`, merged by the herald, as today; ground 15 only refuses the one without the read. It does not make the clerk read prose: a wish's force is read by people and cited by briefs; the clerk prints whether the bytes exist. It does not choose readers: that is C2c-3's.

## 6. What the sovereign reads before any builder starts

A builder writes code only to a text he has read (A2.10). The code of this patch is written to three texts, and his read is of all three:

- this file, whole: every section orders code (§1 the kernels and vectors; §2 the judge and its pin; §3 the verb and its pin; §4 the workflows and the order);
- `transcripts/REVIEW-audit-3-6-argon.md`, findings D1, D5, D6 and D8, which §4 imports;
- `transcripts/runner/monitor.md`, where it defines `publish.yml`.

BRIEF-C2c-2 will list them under `## Texts the code is written to`.
