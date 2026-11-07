# SPEC patch for C2c-2 (draft v1, counsel-3, 7 November 2026) — one kind, one ground

This is the text a builder's branch for C2c-2 begins with (RUNBOOK §`jack push`: "a change to SPEC.md that needs code is the first commit of the builder's branch — counsel's patch, applied and read by Guy there"). It binds nothing until that push. It is deliberately smaller than `transcripts/RESEARCH-self-similarity-20261105.md` §3.3 proposed: the texts on `main` are already named by entries — every `merge` carries the commit it merged and every `push` the digest it authorised, so what `main` holds at any prefix is a function of the log — and the two things that are not are a direction of the sovereign's made in a chat, and a read that a convention requires and nothing checks. The patch adds one `decision` kind for the first and one judge ground for the second. `enact` as a unification of `push` and `amend` is not needed for the bootstrap and waits for a case.

## 1. `wish`: the sovereign's directions and rulings as entries

**SPEC §5, the `decision` row.** `kind`: one of `veto promote budget grant transmute fix wish`. For `wish`, `subject` is `<path>@sha256:<hex64>`: a file under `transcripts/` and the SHA-256 of its bytes. No required member is added to any type; the row widens one member's set, so every earlier valid log replays unchanged (§5's own rule).

**SPEC §7.** No new state. The kernel records a `wish` like any `decision`; it reads nothing on its account.

**SPEC §10 (informative).** Ground 14, `decision_by_other`, already confines `wish` to the sovereign's keys. The clerk and `status.py` read a `wish`: a direction or ruling binds a party from the entry's seq when its file at `main` hashes to the subject; a file that does not, or a direction not on the log, binds nobody. `transcripts/CASES.md`'s "Rulings are not entries on the log" ends at the first `wish`; its index stays as the reading aid. The five directions of 4–7 November that rulings and COUNSEL-OPEN quote are entered as the first five `wish`es, by hash of the files that hold them, in C2c-2's opening sitting.

**Kernel2.** The same regex; nothing else.

**Vectors.** `spec/vectors/logs/<n>_wish_ok.jsonl` (a `wish` by the master key, admitted), `<n>_wish_bad_kind.jsonl` (`kind: wisj`, schema), and the differential's simulator kind `wish`.

## 2. `unread_text`: the read a text that claims force must carry

**SPEC §10, a fifteenth ground (the judge, not the kernel).**

15. **unread_text** — the proposal changes a path under a prefix in `judge/scope.json`'s `read` list (at C2c-2: `transcripts/sessions/`, `transcripts/windows/`, `tools/runner/`, `transcripts/BRIEF-*.md`) and the proposal's branch does not also add, in a commit the same proposal entry covers, a file `transcripts/REVIEW-*.md` that begins `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`, whose `Reviewed tree:` names a commit on the branch at which every changed path under the list has the bytes the head holds, and whose `Reader:` line names a model id that is not the id the proposal's trailer or trigger names. The read gate of `jack push --opens` (#182) is this ground for `judge/scope.json`; this generalises it to the texts the window file lists and moves it from the verb into the judge, where a session cannot route around it. Pin `text_unread`: a proposal changing a session template with no such review is refused; its twin, the same with the review file, is admitted; mutants: the `Reviewed tree` test dropped; the reader's model equal to the drafter's accepted.

**Why the judge and not the kernel.** A read is a file in the tree and a line in it; the kernel reads bytes of `log.jsonl` only (§1). The ground reads two trees and the log, which is the judge's domain (§10 preamble).

## 3. What the push carries

SPEC.md with §5's row and §10's ground 15; `kernel/log.py`'s regex and `kernel2`'s; the vectors; the simulator kind; `judge/judge.py`'s ground and the `read` list in `judge/scope.json`; the `NaN` vector and the kernel fix (`REVIEW-audit-3-6-argon.md` D1); `count_kernel.py --limit 450` in `tests.yml`; the monitor's publishing step in `tests.yml` (`transcripts/runner/monitor.md`). One push, read by two families, with the run of record (the kernel changes). Counted lines: the kernel grows by one regex alternative and shrinks by the `NaN` fix's `parse_constant`; the brief pre-states 450 as its bound.

## 4. What this patch does not do

It does not change `push`, `amend`, `transmute` or the charter's procedure (A2.7, SPEC §10.13). It does not add `claim` or `enact`. It does not make the sovereign the author of session templates: a template changes by a counsel proposal with a read, merged by the herald, as today — ground 15 only refuses the one without the read.
