# The opening push of C2b (counsel's note for the sovereign's `jack push --opens C2b`)

Two changes, pre-stated in BRIEF-C2b v3 §Scope ("the cap, and the opening push's second change") and nothing
else. **One:** `judge/scope.json` `cap` 7800 → 9000 and the identical block in SPEC §10, with one clause added
to the cap's history. **Two:** `.github/workflows/tests.yml` restructured from one serial job into three
parallel jobs — `unit` (unit tests, kernel line count), `pins`, `sample` (judge self-check, then the simulator
sample) — behind a gate job named `tests` that fails unless all three succeeded. The five commands are the
ones that ran on 2 November, each once, in the same relative order where order matters (self-check builds
the checker the sample uses); the workflow's name, triggers and single conclusion are unchanged, so
`status.py`'s `run_verified`, W3 and the merge verb read what they read before. Measured on the merge of PR
121: 8 m 17 s serial, waited for twice per merge; the parallel run is the longest step, about 3½ minutes.
This is a trusted-base change carried by the opening push under A2.6, as REVIEW-C2a-v1 F8 asked that the
"two trusted-base changes" be named; the simulator-sample skip F8 specified is **not** in this push — it is an
in-window item under F8's preserved-coverage contract (BRIEF-C2b v3 §Scope). No kernel source changes; no run
of record is due. The branch was opened as a pull request before the push so the restructured workflow ran on
it first; the run is named in the C2b report.

9,000 is the budget two reads priced (REVIEW-C2b-v1: 750 lines "too thin"; REVIEW-C2b-v2: "150 lines before
opening and 1,250 total … pre-opening gates consume part of that same total"): four EXP3 instances with
replay, the signed draw, the invite verb, resolver routing, W5, the sample skip, status and decision
integration, tests, two simulator kinds and some twenty-five pins. It is a resource constant the sovereign
authorises here and enters no score. If the deliverables do not fit, the builder stops with the shortfall and
the window fails on criterion 3 (BRIEF-C2b §Stop and report); the value and liveness wealth carry into the
next window (A4.1).

C2b's window opens at this entry's `ts`: the first `push` entry after `decision promote C2a`.
