# BRIEF-C2c-1 (draft v2, counsel-3, 7 November 2026, after `REVIEW-C2c-1-v1-astra.md`'s 29 findings) — the window layer as data

This file is `transcripts/BRIEF-C2c-1-draft.md`. C2c is the self-similarity layer (the sovereign's direction of 5 November; `transcripts/RESEARCH-self-similarity-20261105.md`), run as three windows: **C2c-1** (this brief: the window layer, no kernel change), **C2c-2** (recognition and adjudication, one push), **C2c-3** (the charter amended by its own procedure; the bootstrap claim). Each is pre-stated by its own brief before it opens. This brief binds C2c-1 only. It carries counsel-2's Appendix M (`transcripts/BRIEF-C2c-draft.md`, M.1–M.3) as rules R3, R2 and R4. The `c2c-brief` row of COUNSEL-DUE was discharged by that draft's two records (its discharge line); what that discharge left owed — the kernel types if a witness appears in C2b, and the sovereign's reserved questions — this brief carries in §10 and §11.

## 0. The law of this window is a file

`transcripts/windows/C2c-1.json` is this window: its opening rule and preconditions, its promotion forecast, its end, its numbers, its processes, what is frozen, its criteria, the evidence each reads, its reads, and what is reserved to the sovereign. `tools/status.py` reads the window it assesses from `transcripts/windows/<subject>.json` and from nothing else; this prose is commentary. Where the prose and the file differ, the file governs and the difference is a finding for the next read.

**How the file is bound.** The trusted-base digest does not cover `transcripts/` (SPEC §10.1), so the file is bound through the log instead: the promotion forecast's `args.window_sha256` is the file's hash as proposed, entered before the opening, and criterion 5 refuses a prefix at which the file's bytes hash to anything else. Inside the window the file does not change (`frozen`); a change before the opening is a new hash in a new forecast, with reads.

## 1. Purpose

Every failure of the court since 25 October has been in the window layer: two ends for one window, a decision kind with two meanings, unknown read as unmet, a writ class coded for one window, and constants in `status.py` that made each new window a code change inside the window it governed (`transcripts/AUDIT-20261104.md` §3.6, §5.3). This window makes that layer what the kernel already is: a text the code is written to, with one implementation of each rule and a witness that violates it and one that satisfies it. It adds no power to any party and no sentence to the charter.

## 2. Opening, preconditions and the sovereign's read

- **Opening:** the first `push` after `decision promote C2b` (`opens`). The push carries this brief, the window file, the counted-line cap of §7 and the deliverables of §6, each pre-built on branches and read before the push.
- **Preconditions** (`preconditions`): counsel-3 declared (seq 2254, done); the counsel-sign job on the runner's `main` (#369, done); **the sovereign has read this file and §3 before any builder session is filed to implement them** — A2.10, "code is written to a text Guy has read"; COUNSEL-OPEN row 35 permits parallel building only where the rule is in a text he has read. The instant of his read is a COUNSEL-OPEN row; builder sessions for §6 are filed after it and not before. Reads by other models before or after do not stand in for it.
- **The budget entry:** before the opening push the sovereign enters `decision budget` with the text `budget.text` quotes, the cap figure filled in from v3 (§7). The file cites its seq. `status.py` reads the numbers from the file; nothing reads the entry's prose.

## 3. Rules (New in C2c-1)

Each rule binds C2c-1, is implemented once, and has a pin: twins the implementation must pass and mutants the pin must kill. Pins live in `pins/`, registered by the reviewer; a mutant that is the present code is named as such.

### R1 Numerals are housed

No numeral other than `0`, `1` and `-1` appears in `tools/status.py`, `tools/clerk.py` or `tools/value.py`, and no string literal in them parses as an integer or a fraction, except a string that is exactly a key of the window file's `numbers`. Every number a criterion needs is a key of `numbers`, named by a criterion's `args`; `min_rows` and the like are keys, never literals (the file's `ratchet_min_rows`). Dates and seqs of windows are not in code: the opening is found by `opens` and the end by `end`.

**Pin `numerals_housed`.** Twins: (1) the three files as proposed pass the scan — integer and fraction literals outside `{0, 1, −1}`, and string literals that parse as a number, are both findings unless the string is a `numbers` key; (2) every `args` reference of every criterion resolves to a `numbers` key. Mutants: `P0 = Fraction(6, 11)` restored (killed by twin 1); `6900` restored (twin 1); `int("6900")` (twin 1, the string scan); a criterion whose `args` names a key the file lacks (twin 2).

### R2 Criteria are a closed set of kinds, each three-valued

A criterion is `{id, kind, args, text}`; `kind` is one of `verified_run`, `tree_bounds`, `pins_killed`, `window_file_fixed`, `eprocess`, `no_claim_past_due_unescalated`, `ratchet`, `count_zero`, `undertakings_kept`, `no_veto`, `ratio` (eleven). A kind outside the set refuses the whole assessment (`promote <w>: refused: unknown criterion kind <k>`). Each prints one of three values in this order (M.2): `unmet` when the inputs supplied already show failure; `unknown (no <input>)` when an input it reads is absent; else `met` or `unmet` as the inputs say. Which inputs count as supplied is the file's `evidence` section. The line printed is the file's `text`, prefixed by the criterion's id and suffixed by the value.

**Pin `criteria_three_valued`** (on `count_zero` with `evidence: acts`, and on `tree_bounds`, which reads the tree). Twins: (1) acts supplied, zero repairs → `met`; (2) no acts file, nothing else failing → `unknown (no acts)`; (3) acts supplied, one repair → `unmet`; (4) M.2's distinguishing twin — no run file, and the tree already shows a failure (counted lines over the cap) → that criterion prints `unmet`, not `unknown`. Mutants: absent input printed `unmet` (twin 2); absent input printed `met` (twin 2); `unknown` printed when a supplied input shows failure (twin 3); `unknown` printed wherever any input is absent, even when a supplied one shows failure (twin 4).

**Pin `window_from_file`.** Twins: (1) `status.py --subject C2c-1` on a tree whose file lists criteria 1–13 prints exactly thirteen criterion lines in the file's order carrying the file's `text`; (2) the same with criterion 9 removed from the file prints twelve; (3) the same with criterion 10's `text` changed to a different sentence prints that sentence; (4) a file naming kind `x` → the refusal line. Mutants: a criterion added in code that the file does not list (twin 2); the file's `text` ignored, the code's copy printed (twin 3); a kind outside the set accepted (twin 4).

### R3 One stated end (M.1, generalised)

A window's promotion forecast is the first `forecast` on the prefix whose `proposer`, `type` and `args.id` are the file's `promotion.proposer`, `promotion.type` and `promotion.forecast_id`, and whose `seq` is below the window's opening. The window's end is that forecast's `resolves_by` and nothing else (A5.2). With no such forecast, `promote <w>: refused: <w> has no promotion forecast before its opening`. The file states no maximum length: the seven days of §5 are counsel's commitment at entry, not a rule.

**Pin `one_stated_end`.** M.1's twins and mutants with the subject read from the file, plus twin 3: a counsel forecast with the right `args.id` and the wrong `type`, below the opening, is not selected (mutant: the type test dropped).

### R4 One writ function for forecasts (M.3, generalised)

The clerk lists, under one function and for any assessed window, every `forecast` on the prefix with no `resolution`, from the log's first entry — not from C1b's opening — with its holders (resolution keys of other principals) and its deadline, `ESCALATED` once past `resolves_by`. `W1` is that list. `W3` (an unwitnessed merge, `tools/clerk.py merge_writs`) and `W4` (an unmet criterion line, `window_writs`) stay as the clerk prints them today, holders and deadlines unchanged; they are not forecasts and this brief does not pretend they are (CHARTER §2.3: every obligation carries a deadline and escalates). `W5` (`COUNSEL-DUE.jsonl`) is retired by R5. `tools/clerk.py:81`'s `if s["subject"] == "C1b"` is the present mutant (`REVIEW-audit-3-6-argon.md`, pin `w1_c2a_omitted`).

**Pin `one_writ_function`.** M.3's twins and mutants under subjects `C2a` and `C2c-1`, plus twin 5: a forecast entered before C1b's opening, unresolved, is listed (mutant: the C1b cutoff kept); twin 6: a `counsel.undertaking` forecast is listed like any other; twin 7: W3 and W4 lines still print for an unwitnessed merge and an unmet criterion (mutant: the two functions removed).

### R5 Everything counsel owes is a forecast

An undertaking of counsel's is a `forecast` of type `counsel.undertaking` with `args.id`, `args.window` (the window it is owed in), `p` (the probability counsel stands behind, COUNSEL-OPEN row 8) and `resolves_by` its due; it is resolved by a party other than counsel from the evidence the claim names, and "kept" means resolved 1 at or before `resolves_by` — a 1 entered later is not kept. These are brief-required forecasts under the sovereign's direction of 3 November (row 24). `transcripts/COUNSEL-DUE.jsonl` is retired at the opening: every row open at the opening prefix is re-entered as such a forecast with the row's `id` as `args.id`, in the opening sitting's request (row 37: clearing rows means resolved or escalated, not deleted — so no row is "closed with a reason"); a row already discharged stays discharged in COUNSEL-OPEN. Criterion 11 reads them and also requires the due file absent from the tree.

**Pin `undertakings_are_forecasts`.** Twins (criterion 11): (1) two undertakings for the window, both resolved 1 at or before `resolves_by` → `met`; (2) one resolved 0 → `unmet`; (3) one unresolved and past `resolves_by` → `unmet`; (4) one unresolved and before `resolves_by` → `met`; (5) one resolved 1 after `resolves_by` → `unmet`; (6) a builder forecast of the type resolved 0 → `met` (not counsel's); (7) an undertaking with `args.window` of another window → not counted; (8) the due file present in the tree → `unmet`; (9) the file present at the opening prefix with a row whose `id` matches no undertaking forecast on the prefix → `unmet` (the inventory). Mutants: late 1 counted as kept (twin 5); a past-due unresolved counted as kept (twin 3); other proposers counted (twin 6); other windows counted (twin 7); the due file ignored (twins 8, 9).

### R6 No claim past due goes unescalated

A forecast that is unresolved and past `resolves_by` plus `grace_hours` must have an escalation row — `{forecast, issue, filed_at}` in the `escalations` evidence — with `filed_at` at or before `resolves_by` plus the grace. A forecast that has a resolution is not past due, whenever it was resolved. Criterion 8 is `met` when every such forecast has such a row, `unknown (no escalations)` when the evidence is absent, `unmet` otherwise. The diary writes the evidence (§6).

**Pin `escalation_recorded`.** Twins: (1) two unresolved past-due forecasts, both with timely rows → `met`; (2) one without a row → `unmet`; (3) no evidence file → `unknown (no escalations)`; (4) a forecast past due by less than the grace, no row → `met`; (5) a resolved forecast past its date, no row → `met`; (6) a row whose `filed_at` is after `resolves_by` plus the grace → `unmet`. Mutants: grace ignored (twin 4); absent evidence read as met (twin 3); resolved forecasts required (twin 5); a late row accepted (twin 6).

### R7 The enforcement map is a ledger, and the ratchet

Each row of `tools/enforcement.json` is `{enforcer: code:<path:fn> | hand:<who>, witness: <pin id or ''>, deadline: <instant or ''>}`; a `hand` row has a deadline, and the map's own check refuses one without. Criterion 9 reads the rows the file names (`runner`) and is `met` when, between the opening and the assessed prefix, each named row moved from `hand` to `code`, its `witness` pin is KILLED in the verified run, **and** the `runner` evidence shows every workflow of `renavondata/opencode-runner` at its `main` fetching its definition from jack's `main` (the path and sha the evidence records exist in jack's tree at the assessed prefix); `unknown (no runner)` without the evidence; `unmet` otherwise. The precedent is `diary.yml`, which fetches `transcripts/sessions/*.md` from `origin/main` at dispatch; `herald.yml` runs inline code and `tools/jack` and is the first definition to move.

**Where the definitions live.** Counsel touches documents only; code enters from a builder (SPEC §10.8). So the runner's definitions — the workflows and the courier's script — enter under a builder's path, `tools/runner/`, built to the texts counsel writes (`transcripts/runner/*.md`: what each job holds, when it runs, what it does in order, what it never does). The YAML and the Python are the builder's; the prose is counsel's; the opencode-runner workflows reduce to fetching and running `tools/runner/<job>` from jack's `main`.

**Pin `ratchet_row_moves`.** Twins: (1) map at the opening `runner: hand` and at the prefix `runner: code:tools/runner`, witness KILLED, runner evidence showing each workflow fetching a definition that exists in the tree → `met`; (2) the row not moved → `unmet`; (3) moved, witness not KILLED → `unmet`; (4) moved and KILLED, no runner evidence → `unknown (no runner)`; (5) moved and KILLED, evidence showing one workflow fetching nothing → `unmet`; (6) a `hand` row with no deadline → the map's check refuses. Mutants: a label change counted without the evidence (twin 5); a row counted without its witness (twin 3); any moved row accepted instead of the named one (a seventh twin: another row moved, `runner` not → `unmet`); a `hand` row without a deadline admitted (twin 6).

### R8 Object is declared

`transcripts/world-types.json` lists each forecast `type` the court admits as object, with `resolver_inputs`, `reads_record` (true/false) and `scheduled_by` (a session prompt path, or `none`). `status.py` prints the A3.4 ratio twice: as A3.4 defines object today (`type` starts `world.`), which criterion 13 tests, and excluding types whose `scheduled_by` is not `none`, which is printed and not tested. The second number is what the sovereign reads before deciding, at A9, whether a scheduled stream is object. No criterion changes.

**Pin `object_declared`.** Twins: (1) `world.renavon` declared with `scheduled_by: transcripts/sessions/stream-forecast.md` → the second ratio excludes its entries and the first includes them; (2) a type on the log that the file does not declare → the second line prints `undeclared: <type>`; (3) a type declared `scheduled_by: none` → counted in both. Mutants: both lines equal (twin 1); undeclared types silently counted (twin 2).

### R9 The window file is fixed (criterion 5)

`window_file_fixed` reads the promotion forecast R3 selects and compares `sha256` of `transcripts/windows/<w>.json` at the assessed prefix with its `args.window_sha256`; `met` iff equal, `unmet` otherwise (no `unknown`: both inputs are always on the prefix once the forecast exists).

**Pin `window_file_fixed`.** Twins: (1) equal → `met`; (2) one byte changed in the file → `unmet`; (3) the forecast's `args` lacking the key → `promote <w>: refused: <w>'s promotion forecast names no window_sha256`. Mutants: the comparison dropped (twin 2); a missing key read as met (twin 3).

## 4. Criteria

The window file's thirteen, as listed. Criteria 1–4, 5, 6, 7, 12 and 13 hold or fail from the tree, the log and the run; 8, 9, 10 and 11 read evidence and print `unknown` without it. Criteria 6 and 7 are CHARTER §6's tests, unchanged at 20 (A2.4: a brief tightens, never loosens), on the processes BRIEF-C2b Amendment 4 continues with wealth carried. The promotion is lawful when every line is `met`.

## 5. The promotion forecast and the end

Before the opening push, counsel enters the forecast `promotion` describes: "every criterion of C2c-1 is met at the prefix at which `decision promote C2c-1` is entered, at or before `resolves_by`", `p` 600, `resolves_by` the opening sitting's instant plus seven days, `args` `{id, window, window_sha256}`. That `resolves_by` is the window's end; the window ends at the earlier of that instant and `decision promote C2c-1` (A5.1); there is no minimum. It is resolved by a reviewer: 1 iff a `decision promote C2c-1` is on the log at or before `resolves_by` and `status.py` at that decision's prefix prints every criterion `met`; 0 otherwise (no promote by the end, or a promote whose prefix shows a line not met).

Counsel's interest, stated: criterion 11 can be `met` with every undertaking unresolved and not yet due, and the window can close before any falls due. The criterion measures that none was missed by the exit, not that any was performed; the undertakings themselves resolve on their own dates and are scored as items whatever the window did.

## 6. Deliverables, each pre-built on a branch after the sovereign's read, read cold before the opening

- **Builder:** `status.py` reads the window file (R1, R2, R3, R9); the eleven criterion kinds; `clerk.py`'s one forecast function with W3 and W4 kept (R4); criterion 8's reader (R6); the map's deadline check and criterion 9's reader (R7); the two ratio lines (R8); `tools/jack v_decision` promoting any subject with a window file, and `--escalations`, `--runner` beside `--acts`; `tools/runner/` — the workflows and the courier's script, built to `transcripts/runner/*.md`; tests for each.
- **Reviewer:** the ten pins of §3, each with a passing twin on the builder's branch and a mutant that is the present code where one exists.
- **Counsel:** this brief; the window file; `transcripts/world-types.json`; `transcripts/runner/*.md` (one per job: diary, herald, session runner, courier — what it holds, when it runs, what it does in order, what it never does); the COUNSEL-DUE rows as undertakings in the opening request; the C2b report's section on C2c.
- **The runner, once, a repair by §7's letter listed in this window's report:** `opencode-runner`'s workflows reduced to fetching and running `tools/runner/<job>` from jack's `main`; the diary writing the escalations evidence; a builder session writing the runner evidence.

## 7. Scope and cap

Paths as `judge/scope.json` at the opening, plus `transcripts/windows/` under counsel and `tools/runner/` under the builder. The counted cap: C2b's cap is 10,400 (BRIEF-C2b Amendment 3); this window's figure is pre-stated in v3 of this brief from the pre-build's count, before the opening, and raised by the opening push if it exceeds 10,400; `cap_raises_inside_the_window: 0` (a further raise fails the window, BRIEF-C2a's rule). Kernel 450. `frozen` names what does not change inside the window and the one exception.

## 8. What this brief does not do

- No kernel or judge change: `enact`, `wish` and the kinds of `decision` are C2c-2's.
- No charter text, and no new change path for the charter: the charter changes by `transmute` and `amend` (A2.7; SPEC §10.13), one clause each (row 33, kept by row 38). At C2c-3 the amendments are **A7**, A6's clause with the reads' findings as its spec, and **A8**, principle 7's ranking — the sovereign's first amendments for C2c (row 39) — and then **A9**, which restates §3, §6 and A1–A8 in fewer words, moves §6's thresholds to budget lines, decides scheduled streams, and names `enact` as the path for every scope other than the charter *after* it. Each under row 33 in full.
- No change to A3.4's definition of object (R8 reports; A9 decides).
- No rule on the GitHub identities beyond COUNSEL-OPEN row 44.
- The freshness stream runs three-hourly from C2b's exit (`stream_cadence_hours`), so criterion 13 has object entries; its cost is in the spend evidence.
- Nothing is built for C3.

## 9. C2c-2 and C2c-3, pre-stated and not designed

**C2c-2** opens with the first push after `decision promote C2c-1`; that push carries SPEC text and both kernels for two `decision` kinds — `enact` (a text in force for a scope other than the charter: `<scope>@sha256:<hash> read:<hash> witness:<seq>`; the judge refuses a `main` whose scope's bytes do not hash to the latest `enact` for that scope) and `wish` (a direction of the sovereign's, by hash) — the `NaN` vector and fix, `count_kernel.py --limit 450` in CI, and the monitor's publication step and verifier script; its criteria are safety (two checkers, vectors, kernel ≤ 450), every text in the window file's scope list named by an `enact`, and a verified head hash published on every push and checked under an account that is not the owner's. **C2c-3** opens with the first push after `decision promote C2c-2`: A7, A8 and A9 by `transmute` and `amend`, each read by a reader the clerk draws; counsel's functions mapped to code, election or decision; and the promotion forecast "B0–B7 of `transcripts/RESEARCH-meta-jack-20261107.md` §1 hold on the exit prefix". Each has its own brief, written from this window's report.

## 10. What C2b may hand this brief

If a witness appears in C2b's window that a forecast cannot carry an invitation (BRIEF-C2b's deferral of `invite`, `accept`, `wish`), the kernel types go to C2c-2's push with that witness named; if none appears, C2c-2's `wish` rests on the witness already on the record — rulings and directions that are not entries (`transcripts/AUDIT-20261104.md` §4.2).

## 11. Reads, interest and what is the sovereign's

Counsel-3 wrote this brief, the window file and the research note it rests on, holds the promotion forecast, and is the party R5 and criterion 11 score. Readers: two before the opening, of families other than counsel's, chosen by the runner's rotation and not by counsel; each sees the texts and the record, not counsel's argument. A read's findings are fixed in the next version before the opening; a finding that a rule is undecidable as written drops the rule, never softens it. With this brief's read the sovereign is asked the five questions `reserved_to_the_sovereign` lists — row 37's three (the promotion budget, `transmute`, scheduled streams) and row 44's two (what `repair` means; whether a brief may narrow the attribution) — as yes/no lines; nothing in this window turns on the answers except the budget entry's text.
