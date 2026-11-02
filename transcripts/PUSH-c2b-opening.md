# The opening push of C2b (counsel's note for the sovereign's `jack push --opens C2b`)

Two changes, pre-stated in BRIEF-C2b §Scope ("the cap, and the opening push's second change"; v3 named them,
v6 — the read that accepted, REVIEW-C2b-v6 — confirmed them by diff against this branch) and nothing else. **One:** `judge/scope.json` `cap` 7800 → 9000 and the identical block in SPEC §10, with one clause added
to the cap's history. **Two:** `.github/workflows/tests.yml` restructured from one serial job into three
parallel jobs — `unit` (unit tests, kernel line count), `pins`, `sample` (judge self-check, then the simulator
sample) — behind a gate job named `tests` that fails unless all three succeeded. The five commands are the
ones that ran on 2 November, each once, in the same relative order where order matters (self-check builds
the checker the sample uses); the workflow's name, triggers and single conclusion are unchanged, so
`status.py`'s `run_verified`, W3 and the merge verb read what they read before. Measured on the merge of PR
121: 8 m 17 s serial, waited for twice per merge; the parallel run is the longest step, about 3½ minutes.
This is a trusted-base change carried by the opening push under A2.6, as REVIEW-C2a-v1 F8 asked that the
"two trusted-base changes" be named; the simulator-sample skip F8 specified is **not** in this push and **not** in the window: v6 withdrew it
(REVIEW-C2b-v3 F13–F14), as it withdrew v5's reuse of a run on an identical tree (REVIEW-C2b-v5 F16–F19); the workflow is frozen by criterion 3 from this push. No kernel source changes; no run
of record is due. The branch was opened as pull request #125 before the push so the restructured workflow ran on it first:
run 41405822622 — `unit` green in 2:52, `pins` green in 1:29, `sample` red at the judge self-check with
`trusted_base_unrecorded`, which every push branch shows until its push entry records the new trusted digest
(the opening's own run on `main` is the one that counts, as C2a's was: 64d2e720, success), and the gate job
red because one of its three was — the structure's own witness that it fails closed.

9,000 is the budget two reads priced (REVIEW-C2b-v1: 750 lines "too thin"; REVIEW-C2b-v2: "150 lines before
opening and 1,250 total … pre-opening gates consume part of that same total"): four EXP3 instances with
replay, the signed draw, the invite verb, resolver routing, W5, status and decision
integration, tests, two simulator kinds and some twenty-five pins. It is a resource constant the sovereign
authorises here and enters no score. If the deliverables do not fit, the builder stops with the shortfall and
the window fails on criterion 3 (BRIEF-C2b §Stop and report); the value and liveness wealth carry into the
next window (A4.1).

C2b's window opens at this entry's `ts`: the first `push` entry after `decision promote C2a`.

Reconciled with v6 on 2 November after REVIEW-C2b-v6 F21 (prose only: this note and the cap-history clause in SPEC §10; the three trusted files' functional content is byte-for-byte what that read diffed against 606d276).
