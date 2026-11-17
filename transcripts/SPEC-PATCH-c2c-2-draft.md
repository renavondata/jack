# SPEC patch for C2c-2 (draft v6, counsel-5, 17 November 2026, after the read of v5 at runner issue #981, `VERDICT: FAIL`) — one kind, one ground, and a push that takes its facts from keys

This is the text a builder's branch for C2c-2 begins with (RUNBOOK §`jack push`: "a change to SPEC.md that needs code is the first commit of the builder's branch — counsel's patch, applied and read by Guy there"). It binds nothing until that push. The texts on `main` are already named by entries: every `merge` carries the commit it merged and every `push` the trusted digest it authorised. Two things have no entry at all: a direction or ruling of the sovereign's made in a chat, and a read that a convention requires and nothing checks. The patch adds one `decision` kind for the first, and for the second one judge ground and a set of checks in the push verb. `enact` as a unification of `push` and `amend` is not needed for the bootstrap and waits for a case.

**The sovereign's answers.** On 17 November 2026 he answered the seven questions of `transcripts/QUESTION-20261111-constitution.md` §5: "Then indeed, yes to all 7 questions". This patch carries two of the directions: 4 ("from C2c-2 each [ruling] is signed by a `wish`") and 5 ("his read is an entry naming bytes, with the prefix rule; counsel files no session without one, and C2c-2's texts put the check at the push"). Before that, on 8 November: `wish` and `unread_text` in C2c-2's push (COUNSEL-OPEN row 46 d); and on 10 November, to `jack push` running the party check: "You understood exactly" (row 52).

**What changed.** The read of v4 (runner #978) blocked the push's use of trailers, the routes by which a covered text could ride a push, the fetch in ground 15 and the drafter's own list of texts; v5 answered those by taking each party's part from a file its own key brought to `main`, by having a review name the bytes it read, and by making the list of texts the code reader's. The read of v5 (runner #981) passed the kernel rule, left ground 15 with fixes and blocked four things, answered here:

- *A text outside `transcripts/` could not be named by a wish.* The subject may now name any path of the repository (§1).
- *An old verb between the opening push and the new checks.* No push is made in that interval, and BRIEF-C2c-2 makes that a criterion read from the log (§3).
- *The bound could be measured only by code that could not be built before his read.* The rule is here; the number is fixed after the build and read by him before the opening (§4).
- *A rule taken from an unlisted text still passes.* It does, and no check can stop it. What follows that breach, who attests the list and where the obligation is to go are BRIEF-C2c-2's R6, row a, which is read with this patch.

## 1. `wish`: the sovereign's directions, rulings and reads as entries

**SPEC §5, the `decision` row.** `kind`: one of `veto promote budget grant transmute fix wish`. The rule that follows applies to an entry whose `type` is `decision` and whose body's `kind` is `wish`, and to no other entry. For such an entry, `subject` matches `^[A-Za-z0-9][A-Za-z0-9._-]*(/[A-Za-z0-9][A-Za-z0-9._-]*)*@sha256:[0-9a-f]{64}$`, whole (SPEC's notation: every regular expression matches the whole value): a path of the repository and the SHA-256 of bytes. The rule is that match and nothing else: the kernel normalises nothing and looks for no file. Each segment begins with a letter or a digit, so the shape itself admits no `.` or `..` segment, no empty segment, no leading or trailing `/` and no path under `.github/`. A `decision` of any other kind keeps §5's present rule for `subject`. A body of any other type is not read by this rule, whatever members it carries. No required member is added to any type.

**Validity is the kernel's, as for any `decision`.** §8's steps apply unchanged, every one of them. That a `wish` is the sovereign's is not the kernel's question. It is the judge's ground 14, as §4 below leaves it after finding D5. The kernel reads `log.jsonl` only (§1): it tests no file, no tree, and no key state but the prefix's own.

**Replay.** Every log that is valid before this patch is valid after it, with the same state. There is one widening: a log that was refused before only because a `decision` had kind `wish` is valid after, when that subject has the shape and nothing else refuses it.

**SPEC §7.** No new state. A `wish` advances the head and the previous `ts` and has no other effect (§8 step 9's "the other decisions").

**What a wish is (SPEC §10, informative; the clerk).** A `wish` is the sovereign's signed entry naming a path and the SHA-256 of a text's bytes. It is counted by the acts evidence as a decision and not a repair, dated by the log, and named by hash so that nobody can later say he signed something else. It is an act, not an executable rule: the clerk evaluates no prose. One kind serves three uses:

- a **ruling**: the wish names the `transcripts/RULING-*.md` file that records his answer (answer 4);
- a **direction**: the wish names the file that quotes it;
- a **read**: the wish names the text a builder is to write code to (answer 5), wherever it lies: a brief, a patch such as this one, `RUNBOOK.md`.

The decidable part is presence. `tools/clerk.py` prints `W6 wish <seq>: <path>@sha256:<hex> — <commit> | absent`, where `<commit>` is the first commit on `main`'s first-parent history at which the path has those bytes, and `absent` when none does. A later change to the file does not unbind the wish: the bytes it names stay in history.

**A read list.** A wish may name a path under `transcripts/reads/`. Its list is the bytes that wish names, taken from the `<commit>` of its `W6` line; when that line prints `absent`, the wish lists nothing. The list's bytes are split at line feeds; one line feed at the very end ends the last line and adds none. Every line is `<path>@sha256:<hex>` in the shape above, and no line names a path under `transcripts/reads/`: a list does not name a list. A list with any other line — a blank one, or one holding a carriage return — lists nothing, and its `W6` line says `malformed list`. A pair that appears twice counts once. The clerk prints one further `W6` line for each pair, marked `via <seq>`. The kernel does not know the difference. This is how several texts are read in one entry.

**The prefix rule** (answer 5): "a read of bytes that extend bytes already read is a read of the extension". It is a rule about what he must read, and its test is mechanical. Where a wish names `P@h`, an earlier wish names `P@h0`, and the bytes hashing to `h0` are a proper byte prefix of the bytes hashing to `h` (both taken from their `W6` commits), the later wish's `W6` line is marked `extends <seq>`, with the latest earlier wish that does so; a pair named through a read list is marked the same way. The record then shows that his later read was of an extension. A wish can only name a whole file's bytes, so every check below asks for a wish naming the bytes on `main`; a wish naming a prefix of them does not satisfy it, because the extension is unread.

**The first wishes.** C2c-2's window file lists the paths whose wishes are a criterion of the window, and BRIEF-C2c-2 names them: at least `transcripts/RULING-20261104-window-fix.md`, the ruling that records his answers of 17 November, and `transcripts/COUNSEL-OPEN.md`. The criterion is that a wish naming each is on the log with `W6` printing a commit. `transcripts/CASES.md`'s "Rulings are not entries on the log" is corrected by counsel's proposal after the first `wish` (§4); its index stays as the reading aid.

**Kernel2.** `isDecisionKind` gains `wish`. The subject shape is checked by the regular expression printed above, written into `checker.go` from this text, under the same condition: type `decision`, kind `wish`, no other entry.

**Vectors** (the reviewer's proposal after the push, since they pass only against the new kernel), each with its entry in `spec/vectors/verdicts.json`:

- `spec/vectors/logs/<n>_wish_ok.jsonl`: a `wish` by the master key with a well-formed subject, admitted;
- `<n>_wish_bad_kind.jsonl`: `kind: wisj`, schema;
- `<n>_wish_bad_subject.jsonl`: a `wish` whose subject lacks the hash, schema;
- `<n>_wish_dotdot_bad.jsonl`: a `wish` whose subject is `transcripts/a/../SPEC.md@sha256:` and a hash, schema;
- `<n>_wish_root_ok.jsonl`: a `wish` whose subject is `RUNBOOK.md@sha256:` and a hash, admitted;
- `<n>_wish_dotfile_bad.jsonl`: a `wish` whose subject begins `.github/`, schema;
- `<n>_wish_newline_bad.jsonl`: a well-formed subject followed by a line feed, schema;
- `<n>_wish_other_kind_ok.jsonl`: a `grant` whose subject is ordinary prose, admitted (the shape is not asked of another kind);
- `<n>_wish_member_elsewhere_ok.jsonl`: a `forecast` whose body carries a member `kind` with the value `wish` and a member `subject` of any text, admitted as before.

And one judge test: a `wish` signed by a key that holds `decision` and is not the genesis key is valid in both kernels and refused by the judge under ground 14.

The differential's simulator kind `wish` (`sim/gen.py`) is the builder's proposal after the push, with `tests/test_sim.py`'s `KINDS` slice.

## 2. `unread_text`: the read a text that claims force must carry

**SPEC §10, a fifteenth ground (the judge, not the kernel).**

15. **unread_text** — the proposal changes a path that the `read` list of `judge/scope.json` covers, and some such path has no qualifying review on trunk.

**Covered.** A path is covered when a `read` entry matches it. An entry ending in `/` matches the directory. An entry ending in `*` matches every path that begins with the part before the `*` (the `read` list alone admits `*`; `paths`, `parties` and `counted` keep §10's rule). Any other entry matches exactly that file. The ground looks at every covered path that differs between the proposal's merge base with trunk and its head: added, modified or deleted. Call these the proposal's covered changes. A proposal with more than one merge base with trunk is refused on this ground. A covered path that a branch changed and changed back is not among them, and nothing below reads it.

**A qualifying review for a path P** meets all of these. Each is decided from trunk's tree, the proposal's commits and the log; nothing is fetched.

1. It is a file `transcripts/REVIEW-*.md` in trunk's tree, brought there by a `proposal` entry on trunk's log whose signer's principal differs from this proposal's party (ground 7's party). "Brought" is the relation the opening gate already tests (`tools/jack`, `push_read_gate`): a commit that adds the file is that entry's `commit`, or an ancestor of it that was not on `main` before its merge.
2. Its blob in trunk's tree equals its blob at that entry's `commit`. That is the whole test: a review edited on `main` does not qualify while it differs, and qualifies again if the same bytes are restored.
3. Its first line is `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`.
4. It carries the line `Read: P@sha256:<hex>`, where `<hex>` is the SHA-256 of P's bytes at the proposal's head; or, when the proposal deletes P, the line `Read: P@absent`. Every line of the file that begins `Read: ` has one of those two forms, whole; a review with any other such line qualifies for no path. A covered path whose name holds a line feed can be named by no such line, and so has no qualifying review.
5. Its `Reader:` line names one model, and the model's family differs from the family of every drafter's commit that changes P, as defined next.

A review names bytes and no commit. So a proposal made again by cherry-pick keeps its reviews, a review qualifies only for the paths it lists, and two paths may be read by two reviews.

**Drafters, readers and families.** A model id has the shape `^[a-z0-9][a-z0-9-]*/[A-Za-z0-9][A-Za-z0-9._:-]*$`, and its family is the part before the `/`. Every commit after the merge base that is not a merge commit and changes one of the proposal's covered changes is a drafter's commit. A drafter's commit carries exactly one `Model:` trailer whose value has that shape, read by `git log -1 --format=%(trailers:key=Model,valueonly)`. A drafter's commit with no such trailer, with more than one, or with a value of another shape is refused on this ground. The reader's model is the token after `model ` up to the next `;` in the line `Reader: <party>; model <model id>; <date>`, the form the record's reviews already use; a review with no such line, with more than one, or with a value of another shape does not qualify. The reader of P must differ in family from every drafter's commit that changes P, including one whose change a later commit undid. That is strict on purpose: the ground cannot tell which drafter's words survive, so a path that two families have drafted on one branch is read by a third or drafted again.

**Merges.** A merge commit after the merge base whose tree holds, at one of the proposal's covered changes, bytes that none of its parents holds at that path is refused on this ground. Covered text is not written in a merge.

**The `read` list at C2c-2.** `transcripts/sessions/`, `transcripts/windows/`, `transcripts/runner/`, `tools/runner/`, `transcripts/reads/`, `transcripts/BRIEF-*`, `BRIEF-C1.md`, `transcripts/SPEC-PATCH-*`, `transcripts/AMEND-*`, `transcripts/PUSH-*`, `transcripts/RULING-*`, `transcripts/CASES.md`, `transcripts/COUNSEL-OPEN.md`, `LAW.md`, `RUNBOOK.md`, `tools/enforcement.json`. These are the texts that carry a rule or an acceptance criterion that code is written to (answer 5's scope b), the texts that claim force or index it (COUNSEL-OPEN row 34's list), and the notes whose commands the sovereign pastes. `COUNSEL-OPEN.md` is on the list because the clerk gives its rows force today: a row naming `W3 merge <seq>` discharges that writ (`tools/clerk.py`). The cost is a read for each batch of rows, which is counsel's and is the point. SPEC §10's block that mirrors `judge/scope.json` gains the same `read` member in the same push (the tests refuse a push that changes one without the other).

**Not on the list.** `REVIEW-*` (a review of a review is not asked), `BUILT-*` (§3), `REPLY-*`, `RESEARCH-*`, `QUESTION-*`, the reports and the evidence. They claim no force. Nothing here stops a builder writing code to one of them: that is A2.10's breach, and §3 says how far the push can see it.

**What the ground does not establish.** `Model:` and `Reader:` are claims a session makes about itself; the runner's issue is the only record of them outside the tree. The ground makes a drafter name itself, makes the review come from another principal than the proposal's, and makes the reader's named family differ from the drafter's. It does not prove which model read, or that it read. Who reads is still chosen by the drafter until readers are drawn (C2c-3, B4). It judges the tree a proposal would leave on `main`: a covered text added in one commit of a branch and deleted in a later one reaches `main`'s history and never `main`'s tree, and no check reads it there. A2.10's read by the sovereign is a different act from this one, and passing one proves nothing of the other.

**The same rule as the opening gate, moved.** `tools/jack push --opens` (#182) already requires, for a brief, a review on `main` brought by a proposal of another principal whose reviewed bytes equal the brief's. Ground 15 is that rule for every covered path and every proposal, in the judge, where a session cannot route round it. The order of acts: the drafter pushes the draft branch and opens no pull request; a reader of another family reads it and proposes the review with its `Read:` lines (its path is not covered, so no review is needed for a review); the herald merges the review; the drafter then merges `main` and proposes — last, so that the review is on trunk before the proposal is judged.

**Why the judge and not the kernel.** A read is a file in the tree and a line in it; the kernel reads bytes of `log.jsonl` only (§1). The ground reads trees and the log, which is the judge's domain (§10 preamble), and nothing outside git and the log (A2.3).

**Pin `text_unread`.** Twins:

1. a proposal changing a session template with no qualifying review → refused;
2. the same with a review on trunk by another principal, a `Read:` line naming the head's bytes, a reader of another family → admitted;
3. the `Read:` line's hash differing from the head's bytes → refused;
4. the reader's model equal to the drafter's → refused;
5. a drafter's commit without a `Model:` trailer → refused;
6. the review added on the proposal's own branch, not on trunk → refused;
7. the review's blob on trunk differing from its blob at the entry's commit → refused; the same bytes restored → admitted;
8. a deletion of a covered path with no `Read: P@absent` line → refused;
9. the proposal made again by cherry-pick, the same bytes at the head → admitted;
10. a reader of the drafter's family and another model → refused;
11. two drafter's commits of two families on one path, and a reader of one of them → refused;
12. a drafter's commit with two `Model:` trailers → refused;
13. a merge commit that holds covered bytes neither parent holds → refused;
14. a merge of `main` that changes no covered path by its own hand → admitted;
15. two covered paths, each named by a different qualifying review → admitted;
16. a review carrying one malformed `Read:` line beside a good one → refused;
17. the review brought by a proposal whose `commit` merged `main` after the commit that adds the file → admitted.

Mutants: the hash test dropped (3); the model test dropped (4); the trailer not required (5); a branch review accepted (6); the blob test dropped (7); a deletion not counted as a change (8); a commit required (9); models compared as whole strings (10); only the newest drafter's commit read (11); several trailers accepted (12); merge commits skipped (13); every merge refused (14); one review required for all paths (15); malformed lines ignored (16); the adding commit required to be the entry's `commit` itself (17).

## 3. The push takes its facts from keys

A push is not judged by ground 15: it is the sovereign's act. So the verb checks what the judge does not. Every `jack push` changes the trusted base (the verb refuses any other branch: "nothing to push: propose and merge"), and every one is checked as follows. These checks are new in C2c-2.

**No trailer is read.** A2.3: "until keys exist for every party, the `Proposer:` trailer stands in for the signing key, and that substitution ends when the party's key is declared." A fact about a party at a push is therefore a file on `main` that the party's own key brought there by a `proposal` entry, as ground 7 makes a proposal's party "a fact, not a claim". The verb's present refusal of a commit with no filled `Proposer:` trailer stays as it is and proves nothing.

**Names.** M is `origin/main` and H the branch head, both resolved once when the verb starts. A *code path* is a path under a prefix of `counted`, or a trusted path (SPEC §10.1) other than `SPEC.md`. The *reader's own prefixes* are the prefixes that M's `judge/scope.json` gives, under `parties`, to the principal that brought the review and to no other principal (today `pins/` and `spec/vectors/`). "Brought" is §2's relation, with its blob test.

The verb refuses unless all of these hold.

1. **The code read is on `main`.** `--review PATH` names a path matching `^transcripts/REVIEW-[A-Za-z0-9._-]+\.md$` that is a file in M's tree; `--review none` is refused. The file was brought by a `proposal` entry on M's log signed by a key whose principal, under the law in force at that entry (SPEC §7), has `pins/` in its `parties` list. Its first line is `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`. The verb no longer copies a review into `transcripts/`: today it writes the file given to `--review` under its basename, whatever that is, after its checks. The `push` entry's `review` member is the SHA-256 of the blob in M.
2. **The reviewed tree.** The review has exactly one line `Reviewed tree: <40 hex digits>`, naming a commit R1 that is an ancestor of H. So R1 is in the local repository, and nothing is fetched.
3. **The build is the builder's.** When H differs from M at a code path outside the reader's own prefixes, the review carries exactly one line `Built: <path>@sha256:<hex>`, naming a path matching `^transcripts/BUILT-[A-Za-z0-9._-]+\.md$` and the SHA-256 of that file's bytes in M. That file was brought by a `proposal` entry signed by a key whose principal has `tests/` in its `parties` list. Its first line is `Built tree: <40 hex digits>`, naming a commit R0 that is R1 or an ancestor of R1. R0 and M have exactly one merge base, B. At every path outside the reader's own prefixes where R0's bytes differ from B's, R1 holds R0's bytes: the reader read the builder's change as the builder adopted it. When H differs from M at no such code path — a change to `SPEC.md` that needs no code, with or without pins — the review carries no `Built:` line, and R0 below is R1.
4. **The pins are the reader's.** Every line `Own: <path>@sha256:<hex>` or `Own: <path>@absent` of the review names a path under the reader's own prefixes and is true of H: H's bytes at that path have that hash, or H has no such file. Every path under those prefixes at which H differs from M has such a line, and at each such path M's bytes are those of the merge base of R1 and M (exactly one, or the push is refused): where `main` has changed a pin since the read, the read is taken again. A build cannot change its own tests: a byte under those prefixes enters by a push only when the key that holds the pins has signed for that path and those bytes.
5. **Elsewhere the head is the build and `main`, and nothing else.** At every path outside the reader's own prefixes: where R0's bytes equal B's, H holds M's bytes; otherwise, where M's bytes equal B's or equal R0's, H holds R0's bytes; otherwise the push is refused, because both sides changed the path and the build is adopted and read again on a tree that has `main`'s change. `log.jsonl` is a path like any other: a branch adds no entry, and H holds M's log. A path absent from a tree has no bytes there, and two absences are equal.
6. **The texts.** The review carries at least one line `Text: <path>@sha256:<hex>`, each naming a file in M's tree and the SHA-256 of its bytes there; with `--opens LAYER`, one of them names `transcripts/BRIEF-<LAYER>-draft.md`. For each such pair, M's log holds a `wish` by the key ground 14 admits that names the pair, directly or through a read list (§1). A change to `SPEC.md` is written to the patch file that orders it, and that file is what the line names.
7. **Descent.** For each pair of 6, take the earliest such wish and the first commit W on M's first-parent history whose `log.jsonl` holds it. Every commit reachable from H and not from M has W as an ancestor.
8. **No covered text.** H differs from M at no path that the `read` list covers, in M's `judge/scope.json` or in H's. A covered text reaches `main` by a proposal, under ground 15.

**A new read or a new build is a new file.** "Brought" asks for the commit that added the file. A review or a `BUILT` file edited by a later proposal has other bytes than the proposal that added it and satisfies nothing. After a fix the builder adopts the new tree in a new `BUILT` file, and the reader reads it in a new review.

**How a push is assembled.** The builder's branch is cut from a commit of `main` that carries the wishes, and ends at R0. The builder proposes its `BUILT` file from a second branch that holds that file alone: the code branch cannot be proposed, since it changes the trusted base (ground 1). The reader adds its pins and vectors on R0, which gives R1, and proposes its review from a branch that holds the review alone. When both files are on `main`, `main` is merged into the code branch, which gives H, and the sovereign pushes H.

Every line of the review that begins `Built: `, `Own: ` or `Text: ` has its form, whole; a review with any other such line is refused.

**What these checks establish.** That the holder of the builder's key adopted the tree R0; that the holder of the pins' key accepted R1, which holds the builder's changes as adopted, and signed for every changed pin and vector; that what `main` receives is those bytes merged with `main` and no byte beside; that every commit `main` receives descends from the commits that carry the sovereign's wishes for the texts the reader named; and that no covered text came with it.

**What they do not establish.**

- *Who wrote a commit.* A party adopts a tree by its key; that a session of that party typed it rests on the runner's record. Sessions that cannot use one another's keys are the custody text's.
- *That the list of texts is complete.* The scope is answer 5's b: "every text that carries a rule or an acceptance criterion the code is written to". The `Text:` lines are the reader's signed statement of which those are, and the reader is asked for it in terms (the code-read template: name every text the code implements a rule of). A rule taken from a text the list omits passes every check here, and no check could stop it. BRIEF-C2c-2's R6, row a, names who is bound, what follows that breach (answer 2) and the rung the obligation stands on (answer 6): the fifth, attested by a party other than the one bound.
- *That the code was written after the read.* Descent shows what a commit was built on, not when it was typed. Old work committed again on top of W passes; where a breach has made a rebuild necessary, the independence of the rebuild is a question put to the code read, as BRIEF-C2b's question (8) was. And work typed after his read on a branch cut before W is refused: a builder begins from a commit that carries the wish.
- *Code that enters by proposal.* A builder's proposal under `tools/`, `tests/`, `sim/` or `harness/` is judged by grounds 1 to 15 and by none of these checks. For that code A2.10 rests on the session templates' refusal (#780), which is a prompt.
- *Families.* The push compares no model with another. That a code read is by another family than the build is the review rule of the layer's brief, kept by hand as today.

**A moved `main`.** The verb today refuses when `main` has moved. C2c-1 is to make the verbs merge a moved `main` and retry, "every check repeated" (COUNSEL-OPEN row 68). Under that retry these checks are among the repeated ones, on the new M and the new H. Some then refuse rightly: a text of 6 whose bytes changed on `main` needs a new wish and a new read, and a path both sides changed is refused by 5.

**Before `wish` exists.** C2c-2's own opening push is made by the verb as it stands, and his read of this patch and of the other texts of §6 is stated in a `grant`, as at seqs 3432 and 4643. These checks bind from the first push after the proposal that carries them has merged. Between the two the old verb is the only one, and it checks none of this. So no push is made in that interval: BRIEF-C2c-2 states it as a criterion of the window, read from the log and the tree — every `push` after the opening has the pin `push_unread_code` in the `pins/pins.py` of its parent commit.

**Pin `push_unread_code`.** Twins:

1. `--review none` → refused;
2. a review file in the working tree and not in M's tree → refused;
3. a review brought by a proposal of a principal without `pins/` → refused;
4. a review whose first line is not an accepting verdict → refused; a review with two `Reviewed tree:` lines → refused;
5. `--review` naming `transcripts/BRIEF-X-draft.md` → refused, and nothing is written under `transcripts/` by the verb for a review;
6. a code path outside the reader's own prefixes changed and no `Built:` line → refused; the `BUILT` file brought by a principal without `tests/` → refused; a `BUILT` file edited by a later proposal → refused;
7. a path outside the reader's own prefixes that R0 changed and at which R1 holds other bytes → refused; R1 made by merging a later `main` into R0 and adding pins → the checks pass;
8. a pin changed at H with no `Own:` line → refused; an `Own:` line whose hash is not H's → refused; an `Own:` line for a pin that `main` has since brought to the same bytes → the checks pass;
9. H holding an old pin where M holds a newer one → refused; a pin the reader changed and `main` changed too since the read → refused;
10. a path changed on both sides since B → refused; `main` moved only in `log.jsonl` and under `transcripts/` since the read → the checks pass;
11. no wish naming a `Text:` pair → refused; the pair's bytes changed on M since the read → refused; a wish naming a proper prefix of the bytes → refused; a `Text:` line naming `RUNBOOK.md` with a wish for its bytes → the checks pass;
12. a wish naming the pair through a read list → the checks pass; through a malformed list → refused;
13. a commit of the branch that does not descend from W → refused, whenever it was made; such a commit brought in by the merge that makes H, outside R1 → refused;
14. `--opens LAYER` and no `Text:` line for that layer's brief → refused;
15. H differing from M at a path covered by M's `read` list → refused; at a path covered only by H's → refused;
16. a `SPEC.md` change with no code path changed, a review, a `Text:` line naming its patch with a wish, and no `Built:` line → the checks pass, and the verb goes on to its other checks.

Mutants: one for each refusal a twin names, dropping its test; for 5, the copy restored; for 7 and 8, the stricter v5 rule restored (every path equal between R0 and R1; an `Own:` line refused where H equals M).

## 4. What the push carries, and what goes by proposal before and after it

The push is `jack push <branch> --review <file> --opens C2c-2`. It changes `judge/scope.json`, so the verb requires `--opens`, and `--opens` requires `transcripts/BRIEF-C2c-2-draft.md` and its reviews on `main` beforehand. It comes with the run of record, since `kernel/` changes, and is read by two families.

**Before the push, by counsel's proposal under today's read convention** (each is a text and changes no behaviour until the code exists):

- `transcripts/BRIEF-C2c-2-draft.md`, with its reviews;
- `RUNBOOK.md`'s text for `jack decision wish`, the `W6` line and the checks of §3, each in force "from the merge of the proposal that implements it", not from the push (RUNBOOK: "the text lands first, by counsel's `proposal`, and the builder builds to the text on `main`"; "a verb that departs from the text is a finding");
- the session templates: a session's content commits carry `Model: <model id>` as a trailer, written from the issue's `model:` header; a review of covered text carries its `Read:` lines; a build ends by proposing its `BUILT` file from a branch that holds it alone; a second build or read is a new file; a code read carries `Reviewed tree:`, `Built:`, `Own:` and `Text:`, and is asked to name under `Text:` every text the code implements a rule of. Counsel's hand commits carry `Model:` beside `Proposer:`.

**In the push** (the trusted base, and what must travel with it):

- `SPEC.md`: §5's row and rule, and §10's informative paragraphs on what a wish is, `W6`, read lists and the prefix mark (§1 above); §10's ground 15, the `read` rule, the families, and the `read` member in the block that mirrors `judge/scope.json` (§2 above);
- `kernel/log.py`: the kind set and the `wish` subject shape under §1's condition; and the `NaN` fix (`transcripts/REVIEW-audit-3-6-argon.md` D1: a `parse_constant` that raises);
- `kernel2/checker.go`: `isDecisionKind` and the subject shape under the same condition;
- `judge/judge.py`: ground 15 as §2 states it; D5 (`decision_by_other` keyed on the genesis `key_id` under the law in force, where `main` today compares the genesis public-key blob); D6 (ground 5's order);
- `judge/scope.json`: the `read` list of §2;
- `tests/test_judge.py`: the tests of grounds 14 and 15 (D5 turns `test_decision_requires_original_genesis_blob_not_principal_or_id` red: carried, named);
- `pins/pins.py`: the two `find` strings that the fixed lines would otherwise leave STALE, `big_integer_unreadable` (`kernel/log.py:73`) and `decision_forged` (`judge/judge.py:274`), as the reviewer's commits, because `jack push` runs the pins on the branch and a STALE pin refuses the push;
- `.github/workflows/judge.yml` and `tests.yml` with D8 (`setup-go`; the seeds comment); `tests.yml`'s `count_kernel.py --limit <N>`; and `publish.yml` (`transcripts/runner/monitor.md`: the publication step is inline in the workflow, trusted base, with no script outside it).

**After the push, by proposal, in this order:**

1. the builder's `tools/jack` `KINDS` with `wish`; the clerk's `W6` line with read lists and `extends`; the verb's own check calling `count_kernel.py --limit <N>` (today it calls it with no limit); and their tests. The verb refuses `jack decision wish` until this merges, so the first wishes are entered after it, not with the push;
2. the builder's checks of §3 in `tools/jack push`, with their tests, and `tests/test_jack.py`'s push tests changed where they admit no review or an empty one;
3. the reviewer's vectors of §1 with their `verdicts.json` entries, D1's log vector, verdict and `spec/vectors/canonical.json` entry, and the pins `text_unread`, `push_unread_code`, `nan_not_malformed`, `decision_rotated_master`, `grounds_5_order`, `workflow_go_and_seeds`;
4. the builder's simulator kind and `tests/test_sim.py`;
5. counsel's `LAW.md` lines for D5 and ground 15, and `CASES.md`'s sentence on rulings once the first `wish` is on the log.

Nothing under `spec/vectors/` or `sim/` rides in the push (SPEC §10.1, §10.8).

**The interval.** Ground 15 binds every proposal judged after the push. A drafting branch whose commits lack the `Model:` trailer is committed again by its drafter with the trailer; a review made before the templates changed has no `Read:` line and qualifies for nothing, so the text is read again. The checks of §3 bind from step 2's merge.

**This is the patch's inventory, not the window's.** BRIEF-C2c-2 lists the whole build: this patch, what `transcripts/runner/monitor.md` orders beyond `publish.yml` (the verifier, the clerk's `W4 monitor` line, its rows of the enforcement map), the custody text's users, and the criteria.

**The count.** The rule is here and the number is not, because no count can be defended before the code exists. The rule: the kernel's bound `<N>` is the count `tools/count_kernel.py` prints on the reviewed tree, and the counted cap is the lowest multiple of 100 at or above `counted_lines` there plus 100. The order that makes this possible without a circle: he reads the texts of §6, which state the rule; the builder builds on a branch and reports the two counts; counsel appends the two numbers to BRIEF-C2c-2 and sets them in its window file; that addition is read cold and then by him (by the prefix rule he reads the addition alone); only then does the builder commit the two lines that carry `<N>` — `tests.yml`'s and the verb's — and the reader read the tree. Today `main` stands at 8,347 of 8,400 counted lines and the kernel at 450 of 500; C2b and C2c-1 open first, and each sets its own cap.

## 5. What this patch does not do

It changes `push` by the checks of §3 and by ending the review copy, and in no other way. It does not change `amend`, `transmute` or the charter's procedure (A2.7, SPEC §10.13). A `wish` transmutes nothing, amends nothing, waives no rule and disposes of no finding. The patch does not add `claim` or `enact`. It does not make the sovereign the author of session templates: a template changes by a counsel proposal with a read on `main`, merged by the herald, as today; ground 15 only refuses the one without the read. It does not make the clerk read prose: a wish's force is read by people and cited by briefs; the clerk prints whether the bytes exist. It does not choose readers: that is C2c-3's.

## 6. What the sovereign reads before any builder starts

A builder writes code only to a text he has read (A2.10). This patch is one of six texts the code of C2c-2 is written to, and it starts no build alone:

- this file, whole: every section orders code (§1 the kernels and vectors; §2 the judge and its pin; §3 the verb and its pin; §4 the workflows and the order);
- `transcripts/REVIEW-audit-3-6-argon.md`, findings D1, D5, D6 and D8, which §4 imports;
- `RUNBOOK.md`, the paragraphs §4 has counsel propose before the push: the builder builds the verb to them;
- `transcripts/runner/monitor.md`, whole, after it has been brought to answer 6 (the paper's §3: a witnessed log for the published head, and a verifier on a forge that is not GitHub; the text on `main` puts the verifier on GitHub's runners). That revision is not yet drafted;
- `transcripts/BRIEF-C2c-2-draft.md` with its window file: the criteria, the paths whose wishes are a criterion (§1), the two numbers of §4, the review rule, and for each obligation left to hand what follows its breach and the rung it stands on (§3). In draft, on no branch;
- the custody text (the parties' keys under separate users). Not yet written.

The session templates of §4 are instructions to sessions and restate this patch. A template that adds a rule the code implements is a finding, and the code reader's `Text:` lines are where it would show.

No builder session is filed for C2c-2 until each of the six has been read cold and then read by him. His read of them is stated in the `grant` of §3's "Before `wish` exists".
