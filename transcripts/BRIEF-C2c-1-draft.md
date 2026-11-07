# BRIEF-C2c-1 (draft v1, counsel-3, 7 November 2026) — the window layer as data

This file is `transcripts/BRIEF-C2c-1-draft.md`. C2c is the self-similarity layer (the sovereign's direction of 5 November; `transcripts/RESEARCH-self-similarity-20261105.md`), run as three windows: **C2c-1** (this brief: the window layer, no kernel change), **C2c-2** (recognition and adjudication, one push), **C2c-3** (the charter restated; the bootstrap claim). Each is pre-stated by its own brief before it opens. This brief binds C2c-1 only. It carries counsel-2's Appendix M (`transcripts/BRIEF-C2c-draft.md`, M.1–M.3) as its rules R3, R2 and R4, and so discharges the `c2c-brief` row (COUNSEL-DUE, due 2026-11-16T00:00:00Z) together with that draft's two records (the kernel types; the identities).

## 0. The law of this window is a file

`transcripts/windows/C2c-1.json` is this window: its opening rule, its promotion forecast, its end, its numbers, its criteria and the evidence each reads. `tools/status.py` reads the window it assesses from `transcripts/windows/<subject>.json` and from nothing else; this prose is commentary. Where the prose and the file differ, the file governs and the difference is a finding for the next read. The file is bound by the opening push's digest like every text of the window (BRIEF-C2b Amendment 2); it is amended before the opening with reads, and inside the window not at all.

## 1. Purpose

Every failure of the court since 25 October has been in the window layer: two ends for one window, a decision kind with two meanings, unknown read as unmet, a writ class coded for one window, and constants in `status.py` that made each new window a code change inside the window it governed (`transcripts/AUDIT-20261104.md` §3.6, §5.3). This window makes that layer what the kernel already is: a text the code is written to, with one implementation of each rule, a witness that violates it and one that satisfies it. It adds no power to any party and no sentence to the charter.

## 2. Opening and precondition

- **Opening:** the first `push` after `decision promote C2b` (the window file's `opens`). The push carries this brief, the window file, and the deliverables of §6, each pre-built on branches and read before the push.
- **Precondition:** `counsel-3` declared with `proposal,forecast` and the courier (`transcripts/runner/counsel-courier.md`) on the runner's `main`, so that counsel's entries in this window are signed on steel. The window has not opened while either is missing.
- **The budget entry:** before the opening push, the sovereign enters `decision budget` with the text the window file's `budget.text` quotes. The file cites its seq. The numbers in the file are then his, pre-stated; `status.py` reads them from the file and nothing reads them from the entry's prose.

## 3. Rules (New in C2c-1)

Each rule binds C2c-1, is implemented once, and has a pin: twins the implementation must pass and mutants the pin must kill. Pins live in `pins/`, registered by the reviewer.

### R1 Numerals are housed

No numeral other than `0`, `1` and `-1` appears in `tools/status.py`, `tools/clerk.py` or `tools/value.py` outside a string that names a window file key. Every number a criterion needs — the null, a threshold, a cap, a grace, a maximum — is a key of the window file's `numbers`, named by a criterion's `args`. Dates and seqs of windows are not in code: the opening is found by the file's `opens` rule and the end by its `end` rule.

**Pin `numerals_housed`.** Twins: (1) the three files as proposed pass a scan for integer and fraction literals outside `{0, 1, -1}` and outside string literals; (2) the file's `numbers` resolve every `args` reference of every criterion. Mutants: `P0 = Fraction(6, 11)` restored in `status.py` (killed by twin 1); `6900` restored in a criterion (twin 1); a criterion whose `args` names a key the file lacks (twin 2).

### R2 Criteria are a closed set of kinds, each three-valued

A criterion is `{id, kind, args, text}`. `kind` is one of: `verified_run`, `tree_bounds`, `pins_killed`, `no_claim_past_due_unescalated`, `ratchet`, `count_zero`, `undertakings_kept`, `no_veto`, `ratio`. A kind not in the set refuses the whole assessment (`promote <w>: refused: unknown criterion kind <k>`). Each kind prints one of three values in this order (M.2): `unmet` when supplied inputs already show failure; `unknown (no <input>)` when an input it reads is absent; else `met` or `unmet`. Which inputs count as supplied is the file's `evidence` section.

**Pin `criteria_three_valued`.** Twins (on `count_zero` with `evidence: acts`): (1) acts supplied, zero repairs → `met`; (2) no acts file, tree shows no failure → `unknown (no acts)`; (3) acts supplied, one repair → `unmet`. Mutants: absent input printed `unmet`; absent input printed `met`; `unknown` printed when the input is supplied and shows failure.

**Pin `window_from_file`.** Twins: (1) `status.py --subject C2c-1` on a tree whose window file lists criteria 1–10 prints exactly ten criterion lines in the file's order with the file's `text`; (2) the same tree with criterion 6 removed from the file prints nine. Mutants: a criterion added in code that the file does not list (twin 2); the file's `text` ignored (twin 1); a kind outside the set accepted (a third twin: a file naming kind `x` → the refusal line).

### R3 One stated end (M.1, generalised)

A window's promotion forecast is the first `forecast` by the file's `promotion.proposer` whose `args.id` equals the file's `promotion.forecast_id` and whose `seq` is below the window's opening. The window's end is that forecast's `resolves_by` and nothing else (A5.2); the file's `numbers.max_days` bounds the `resolves_by` the forecast may state, not the end. With no such forecast, `promote <w>: refused: <w> has no promotion forecast before its opening`.

**Pin `one_stated_end`.** Counsel-2's twins and mutants for `c2c_one_end` (`transcripts/BRIEF-C2c-draft.md` M.1), with the subject read from the file. Mutants add: the end read from `max_days` (killed by twin 1).

### R4 One writ function (M.3, generalised)

The clerk lists, for the assessed window, every `forecast` on the prefix with no `resolution`, under one function, whatever the window: a line `W1 forecast <seq>` with its holders (resolution keys of other principals) and its deadline, `ESCALATED` once past `resolves_by`. `W2`–`W5` are retired as classes: W3 (an unwitnessed merge) and W4 (an unmet criterion line) are printed as the lines `status.py` already prints, and W5 (`COUNSEL-DUE.jsonl`) is retired by R5. `tools/clerk.py:81`'s `if s["subject"] == "C1b"` is the present mutant (`REVIEW-audit-3-6-argon.md`, pin `w1_c2a_omitted`).

**Pin `one_writ_function`.** Counsel-2's twins and mutants for `c2c_w1_every_window` (M.3), run under subject `C2c-1`, plus twin 5: a forecast with `type` `counsel.undertaking` is listed like any other.

### R5 Everything owed is a forecast

An undertaking of counsel's is a `forecast` of type `counsel.undertaking` with `args.id`, `p` (the probability counsel stands behind, COUNSEL-OPEN row 8) and `resolves_by` its due; it is resolved by a party other than counsel from the evidence the claim names. `transcripts/COUNSEL-DUE.jsonl` is retired at the opening: each open row is re-entered as such a forecast in the opening sitting's request, or closed with its reason in COUNSEL-OPEN. These are brief-required forecasts under the sovereign's direction of 3 November (row 24). Criterion 8 reads them.

**Pin `undertakings_are_forecasts`.** Twins (criterion 8): (1) two undertakings, both resolved 1 before `resolves_by` → `met`; (2) one resolved 0 → `unmet`; (3) one unresolved and past `resolves_by` plus the grace → `unmet`; (4) one unresolved and before its `resolves_by` → `met`. Mutants: a past-due unresolved undertaking counted as kept (twin 3); a 0 counted as kept (twin 2); undertakings of another proposer counted (a fifth twin: a builder forecast of the type, resolved 0 → `met`).

### R6 No claim past due goes unescalated

A forecast past `resolves_by` plus the file's `grace_hours` must have an escalation record: a row in the diary's `escalations` evidence naming its seq, the issue the diary filed for it, and the instant. Criterion 5 is `met` when every past-due forecast on the prefix has one, `unknown (no escalations)` when the evidence is absent, `unmet` otherwise. The diary writes the evidence (§6, the runner definition). This is the loop invariant of `RESEARCH-self-similarity-20261105.md` §2 at the layer the clerk reaches: an obligation nothing acts on is a line `status.py` prints as unmet, not a line it prints as escalated.

**Pin `escalation_recorded`.** Twins: (1) two past-due forecasts, both in the evidence → `met`; (2) one not in it → `unmet`; (3) no evidence file → `unknown (no escalations)`; (4) a forecast past due by less than the grace, not in the evidence → `met`. Mutants: grace ignored (twin 4); evidence absent read as met (twin 3); a resolved forecast required (a fifth twin: a resolved forecast past its date, absent from the evidence → `met`).

### R7 The enforcement map is a ledger, and the ratchet

Each row of `tools/enforcement.json` is `{enforcer: code:<path:fn> | hand:<who>, witness: <pin id or ''>, deadline: <instant or ''>}`. A `hand` row has a deadline. Criterion 6 is `met` when, between the opening and the assessed prefix, at least one row moved from `hand` to `code` and its `witness` pin is KILLED in the verified run; `unmet` otherwise. For C2c-1 the row that moves is `runner`: the session prompts are already in the court (`transcripts/sessions/`); the runner's workflow definitions join them (`transcripts/runner/`), and `opencode-runner`'s workflows fetch each from `origin/main` at dispatch, as `diary.yml` and `herald.yml` already fetch the prompts.

**Pin `ratchet_row_moves`.** Twins: (1) a map at the opening with `runner: hand` and at the prefix with `runner: code:transcripts/runner`, witness KILLED → `met`; (2) no row moved → `unmet`; (3) a row moved whose witness is not KILLED → `unmet`. Mutants: a row counted without its witness (twin 3); a `code` row at the opening recounted (a fourth twin: the same row `code` at both → `unmet`); a `hand` row with no deadline admitted (twin 5: the map's own check refuses it).

### R8 World types are declared

`transcripts/world-types.json` lists each forecast `type` the court admits as object, with `resolver_inputs`, `reads_record` (true/false) and `scheduled_by` (a session prompt path, or `none`). `status.py` prints the A3.4 ratio twice: as A3.4 defines object today (`type` starts `world.`), which criterion 10 tests, and excluding types whose `scheduled_by` is not `none`, which is reported and not tested. The second number is what the sovereign reads before deciding, at C2c-3, whether a scheduled stream is object. No criterion changes.

**Pin:** none — a reporting line. The reviewer's `sim` kind may carry it.

## 4. Criteria

The window file's ten, as listed. "Supplied" means: the run, as `tools/jack v_decision` supplies it (BRIEF-C2a's rule); the acts file, by the classifier over the window's interval, committed under `transcripts/evidence/`; the escalations file, written by the diary. Criteria 1–4 and 9–10 hold or fail from the tree, the log and the run; 5, 7 and 8 read evidence and print `unknown` without it. The promotion is lawful when every line is `met`.

## 5. The promotion forecast and the end

Before the opening push, counsel enters `forecast` type `window.promotion`, `args.id` `C2c-1-V0`: "every criterion of C2c-1 is met on some prefix of `main` at or before `resolves_by`", `p` 600, `resolves_by` the opening sitting's instant plus seven days (the file's `max_days`). That `resolves_by` is the window's end. The window ends at the earlier of that instant and `decision promote C2c-1` (A5.1); there is no minimum: if every line is `met` at the first prefix after the opening, the window closes there. The forecast is resolved by a reviewer from `status.py`'s output at the exit prefix.

## 6. Deliverables, each pre-built on a branch and read before the opening

- **Builder:** `status.py` reads the window file (R1, R2, R3); the nine criterion kinds; `clerk.py`'s one function (R4); criterion 5's reader (R6); the enforcement map's deadline check (R7); the two ratio lines (R8); tests for each. Estimated counted lines: +500; the cap pre-stated at 8,400 and restated in v2 of this brief after the first read, before the opening.
- **Reviewer:** the eight pins of §3, each with a passing twin on the builder's branch and a mutant that is the present code where one exists.
- **Counsel:** this brief, the window file, `transcripts/world-types.json`, `transcripts/runner/*.yml` (the diary, the herald, the courier and the session runner, moved from `opencode-runner` with their comments), the COUNSEL-DUE rows as forecasts, the C2b report's section on C2c.
- **The runner (a repair by §7's letter, once, listed in this window's report):** `opencode-runner`'s workflows reduced to fetching their definitions from `origin/main` of jack; the diary writing the escalations and spend evidence (`transcripts/evidence/escalations-<stamp>.json`, `transcripts/evidence/spend-<day>.json`) by proposal under the builder's key.

## 7. Scope and cap

Paths as `judge/scope.json` at the opening, plus `transcripts/windows/` and `transcripts/runner/` under counsel. Counted cap 8,400 (from 7,800), raised by the opening push and named in the budget entry; any further raise fails the window (BRIEF-C2a's rule). Kernel 450. Tools are frozen inside the window except by a proposal this brief names (a deliverable landing late, a pin's twin).

## 8. What this brief does not do

- No kernel or judge change: `claim`, `enact`, `wish`, and the kinds of `decision` are C2c-2's.
- No charter text: A6's clause and principle 7's ranking, which the sovereign directed to C2c as its first amendments (row 39), enter at C2c-3 by the `enact` path C2c-2 builds, so that the first amendment by the judged procedure (row 33) is also the first the charter's own text does not contradict.
- No change to A3.4's definition of object (R8 reports; the sovereign decides at C2c-3).
- No rule on the GitHub identities beyond COUNSEL-OPEN row 44.
- The freshness stream runs three-hourly from C2b's exit (BRIEF-C2a's cadence before its Amendment 2), so that criterion 10 has object entries; its cost is in the spend evidence.
- Nothing is built for C3.

## 9. C2c-2 and C2c-3, pre-stated and not designed

**C2c-2** opens with the first push after `decision promote C2c-1`; that push carries SPEC text and both kernels for two `decision` kinds — `enact` (a text in force: `<scope>@sha256:<hash> read:<hash> witness:<seq>`; the judge refuses a `main` whose scope's bytes do not hash to the latest `enact` for that scope) and `wish` (a direction of the sovereign's) — the `NaN` vector and fix, `count_kernel.py --limit 450` in CI, and the A2.8 monitor's script; its criteria are safety (two checkers, vectors, kernel ≤ 450), every text in force named by an `enact`, and the monitor publishing a verified head hash under an account that is not the owner's. **C2c-3** opens with the first push after `decision promote C2c-2`: one `enact` of scope `charter` restating §3, §6, A1–A5, A6's clause and principle 7's ranking; readers drawn by the clerk from the record; counsel's functions mapped to code, election or decision; and the promotion forecast "B0–B7 of `transcripts/RESEARCH-meta-jack-20261107.md` §1 hold on the exit prefix". Each has its own brief, written from this window's report.

## 10. Reads and interest

Counsel-3 wrote this brief and the research note it rests on, holds the promotion forecast, and is the party R5 and criterion 8 score. Readers: two, of families other than counsel's, chosen by the runner's rotation and not by counsel; each sees the brief and the record, not counsel's argument. A read's findings are fixed in v2 before the opening; a finding that a rule is undecidable as written drops the rule, never softens it.
