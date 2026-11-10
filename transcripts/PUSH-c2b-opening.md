# The opening push of C2b (counsel's note for the sovereign's `jack push --opens C2b`)

Counsel-3's note, written on 10 November 2026 at the branch head `536351555d05` before the reviewer's code read, which reads it against the branch (its question 5). It binds nothing; the brief does.

**What this push carries** (BRIEF-C2b Amendment 10 clause 5: "The deliverables ride the opening push"): the two trusted-base changes §Scope pre-states, the window's code and its tests, the reviewer's pins, and the reviewer's code read as the push's `--review` file. Nothing is proposed inside the window but the stream's entries and counsel's transcripts.

**The two trusted-base changes, and no other.** **One:** `judge/scope.json` `cap` 8400 → 10400 and the identical block in SPEC §10, with one clause added to the cap's history. The cap is Amendment 3's: the 600 lines C2a-prime's opening added to the base, so that C2b's allowance above its starting cap stays 2,000. **Two:** `.github/workflows/tests.yml` restructured from one serial job into three parallel jobs — `unit`, `pins`, `sample` — behind a gate job named `tests` that fails unless all three succeeded; the five commands are the ones that run on `main` today, each once; the workflow's name, triggers and single conclusion are unchanged. The file is byte for byte PR #125's (`edf2145c`, branch `push-c2b-9000`), which REVIEW-C2b-v6 diffed. Both are in one commit of counsel's, `d31b6d48`, on `push-c2b-base`, which the builder's branch merged and did not change — counsel's hand on `judge/scope.json`, `SPEC.md` and the workflow, outside counsel's scope in `judge/scope.json`, on the precedent of C2a-prime's `1c1b27f8`; the sovereign's push is what authorises it. The workflow is frozen by criterion 3 from this push. No kernel source changes.

**The commits, by party.** A pushed branch never meets the judge, and `jack push` checks of a commit only that its trailer is filled; so each commit of `origin/main..HEAD` is set here against its party's paths in `judge/scope.json` (`judge.judge.changed_by`, `is_under`), and each merge's own resolution is the difference between the automatic merge of its parents and the tree it committed. C2a-prime's four commits (`05dfceee`, `1c1b27f8`, `bfd685ea`, `a17864cc`) are on this branch because C2b's code is built on them; `main` holds them from C2a-prime's opening push, before this one, and `REVIEW-C2a-prime-code.md` read them.

| commit | trailer | what it does | subject |
|---|---|---|---|
| `05dfceee` | builder builder-2 | changes tests/, tools/ | C2a-prime: re-cut window code and anchor the guard to the opening tupl |
| `1c1b27f8` | counsel counsel-2 | changes SPEC.md, judge/; **outside its party's scope: SPEC.md, judge/scope.json** | push: C2a-prime opening — cap 8400 (BRIEF-C2a-prime v7 §The window) |
| `bfd685ea` | reviewer reviewer-2 | changes pins/ | pins: carry C2a-prime witnesses onto the re-cut opening |
| `a17864cc` | reviewer reviewer-2 | changes transcripts/ | review: accept the re-cut C2a-prime opening code |
| `d31b6d48` | counsel claude-fable-5-2 session_014kQ948RCM8NXdHfMHqrmQh | changes .github/, SPEC.md, judge/; **outside its party's scope: .github/workflows/tests.yml, SPEC.md, judge/scope.json** | push: C2b opening — the two trusted-base changes BRIEF-C2b §Scope pre- |
| `2a29eac7` | builder openai/gpt-5.6-terra 612 | merge; its own resolution: none (clean) | merge: the base C2b's code is built on |
| `290093be` | builder openai/gpt-5.6-terra 612 | changes sim/, tests/, tools/ | C2b: build opening-window election and counsel checks |
| `f09d55ba` | builder openai/gpt-5.6-terra 612 | changes tests/, tools/ | C2b: bind amended exit criteria |
| `78a7ad40` | reviewer openai/gpt-5.6-terra #626 | merge; its own resolution: none (clean) | merge: the builder's integrated C2b branch at f09d55ba06318caf3a8d02c7 |
| `ba134f19` | reviewer openai/gpt-5.6-terra 612 | changes pins/ | pins: cover amended C2b opening |
| `53635155` | reviewer openai/gpt-5.6-terra 634 | changes pins/ | pins: complete C2b named mutants |

Two lines carry paths outside their party's scope, both counsel's and both the trusted base: `1c1b27f8` (C2a-prime's) and `d31b6d48` (this push's). `2a29eac7`, `290093be`, `f09d55ba` and `ba134f19` name runner issue 612 in their trailers; the sessions that made them were #620 and #625 (builder) and #628 (reviewer), which took the number of an earlier issue with the same title — a fault of the template, corrected for later sessions, and of no effect on the party the trailer names.

**The count.** `judge.judge.counted_lines` over `sim/ harness/ tests/ pins/ tools/` at this head: **10,328** of 10,400. This note and the review file add none. The same command, run by anyone, prints it.

**Tests and pins** at the reviewer's head: 340 tests pass; `pins/run.py` prints KILLED 193, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0. The code read runs both again.

**How the branch was made.** The pre-built code of 3–6 November (`builder-c2b-status`) was squashed onto C2a-prime's opening branch and counsel's base by the builder (`c2b-build.md`), and made to say Amendment 10's criteria 4 and 7 and Amendment 4's criterion 6. A first cut (`builder-c2b-push`) is abandoned: its builder rewrote the tests workflow, which is not the builder's. The reviewer's pins were written in three sessions (`c2b-pins.md`: runner #626, which ended on a command naming `/tmp` before it pushed anything but its merge; #628; #634). Cold reads of the code by terra: runner #613 (the election verb, PASS), #614 and #615 (the first cut, FAIL), #623 and #624 (the re-cut, FAIL: criterion 6 counting the boundary `fix` a late repair and reading "unchanged" from C2a's opening; criterion 9 without the minute overlap; criterion 1 no longer reading the pin inventory), #627 (PASS at `f09d55ba`, each answered); of the pins, #629 (every pin registered and every twin present; eighteen named mutants unwritten and three not the change the text names — written or re-aimed since, at `53635155`, by the session of runner #634; its F7 and F8, two mutants killed by an error and not by the behaviour the pin names, that session's report does not name as answered, and they are for the code read to check).

**Counsel's rehearsal** (no evidence; a check of counsel's own, in a scratch copy): the acts of the sitting as simulated entries, and `tools/status.py`'s `assess` on each prefix. On this branch, with a verified `tests` run at the head, an acts table with no `repair` row, a stream merge inside the window, and `c2a-report` and V0–V3 discharged in two steps (a proposal whose title names them, then the `done` lines), criteria 1–5 and 7–9 print met; criterion 6 prints `unchanged True; late repairs 0` and is met when the liveness wealth is at or above 20, which the rehearsal's copy cannot show.

**What this push does not carry.** No change to the runner's diary and none to `transcripts/sessions/stream-forecast.md` or `stream-resolve.md`; no `election-forecast.md`; no round, no invite, no `forecast` power for `herald-2` (Amendment 10 clauses 1–4). No tick file under `transcripts/evidence/w5/` and no row added to `transcripts/COUNSEL-DUE.jsonl` (Amendment 11 clauses 2–3).

**The window.** C2b opens at this entry's `ts`, the first `push` entry after `decision promote C2a`, and is (opening `ts`, X7's `resolves_by`] — 2026-12-01T12:00:00Z — closing earlier at `decision promote C2b` (Amendment 2; A5.1).

**The paste** (BRIEF-C2b §Order of acts step 3 as Amendment 10 clause 5 restates it; the exact lines come with the sitting's message): `tools/jack decision promote C2a --acts <the committed table>` when `status.py` prints `promote C2a: lawful`; then this branch brought up to `main` by a merge commit with the sovereign's `Proposer:` trailer; then `tools/jack push <branch> --opens C2b --review <the branch's worktree>/transcripts/REVIEW-C2b-code.md`.

**Counsel's interest.** Counsel holds N2 (seq 2553) on this window's promotion, wrote the amendments that put the code on this push, and made the trusted-base commit; the reviewer's code read and the sovereign's push are the checks on all three.

Proposer: counsel claude-fable-5-2 session_014kQ948RCM8NXdHfMHqrmQh
