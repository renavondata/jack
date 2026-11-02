# The opening push of C2b (counsel's note for the sovereign's `jack push --opens C2b`)

Three changes, pre-stated in BRIEF-C2b v5 §Scope ("the cap, and the opening push's second and third changes")
and nothing else. **One:** `judge/scope.json` `cap` 7800 → 9000 and the identical block in SPEC §10, with one clause added
to the cap's history. **Two:** `.github/workflows/tests.yml` restructured from one serial job into three
parallel jobs — `unit` (unit tests, kernel line count), `pins`, `sample` (judge self-check, then the simulator
sample) — behind a gate job named `tests` that fails unless all three succeeded. The five commands are the
ones that ran on 2 November, each once, in the same relative order where order matters (self-check builds
the checker the sample uses); the workflow's name, triggers and single conclusion are unchanged, so
`status.py`'s `run_verified`, W3 and the merge verb read what they read before. Measured on the merge of PR
121: 8 m 17 s serial, waited for twice per merge; the parallel run is the longest step, about 3½ minutes.
**Three:** an `antecedent` job and `.github/scripts/antecedent.py`: every run publishes the identity of the
tree it tests (every file but `log.jsonl`) as an artifact, and the three workers reuse an earlier completed
successful run that published the same identity — naming its run id and head in their own log — because that
tree is the complete input of all five steps (none reads the log; the log is
replayed through both checkers by the `judge` workflow on every head, which never reuses anything). A head
that changes any other file runs everything. This is REVIEW-C2a-v1 F8's "useful candidate antecedent" —
the merge-entry head differs from the proposal head the verb already awaited by one log line — under F8's
contract: identical complete input tree, fresh-log replay, a run named, and a mutant that reuses on a
differing tree or a red antecedent (pin `tests_reuse_needs_antecedent`, delivered with W5). The sample skip
by a list of paths that v3 proposed and REVIEW-C2b-v3 F13 found incomplete is not this: the comparison is
the whole tree. Measured on 2 November: every merge waits twice for an 8-minute run whose second instance
tests a tree the first already tested; a stream proposal that carries only forecasts waits once more than it
needs. These are trusted-base changes carried by the opening push under A2.6, as REVIEW-C2a-v1 F8 asked
that the trusted-base changes be named. No kernel source changes; no run
of record is due. The branch was opened as pull request #125 before the push so the restructured workflow ran on it first:
run 41405822622 — `unit` green in 2:52, `pins` green in 1:29, `sample` red at the judge self-check with
`trusted_base_unrecorded`, which every push branch shows until its push entry records the new trusted digest
(the opening's own run on `main` is the one that counts, as C2a's was: 64d2e720, success), and the gate job
red because one of its three was — the structure's own witness that it fails closed.

9,000 is the budget two reads priced (REVIEW-C2b-v1: 750 lines "too thin"; REVIEW-C2b-v2: "150 lines before
opening and 1,250 total … pre-opening gates consume part of that same total"): four EXP3 instances with
replay, the signed draw, the invite verb, resolver routing, W5, the sample skip, status and decision
integration, tests, two simulator kinds and some twenty-five pins. It is a resource constant the sovereign
authorises here and enters no score. If the deliverables do not fit, the builder stops with the shortfall and
the window fails on criterion 3 (BRIEF-C2b §Stop and report); the value and liveness wealth carry into the
next window (A4.1).

C2b's window opens at this entry's `ts`: the first `push` entry after `decision promote C2a`.
