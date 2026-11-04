# Self-similarity within the law: what collapses, at which layer, enforced by what

*5 November 2026. A design note for the C2c brief, following the audit of 4 November. Nothing here is law; every proposed change is placed at the layer of law it belongs to, with the witness that already exists for it on the record and the mechanism that would enforce it. Order of entry follows the method: brief rule with a pin first, charter by amendment only after the rule has refused or decided an act (COUNSEL-OPEN row 28), kernel changes by push with reads and a run of record.*

## 1. The layers, as jack already has them

jack's law is five layers, each with its own change path and its own enforcer. Naming them is the first act of self-similarity, because every later question — "where does this change go?" and "what enforces it?" — is answered by the row.

| layer | what it decides | where it lives | changes by | enforced by | strength today |
|---|---|---|---|---|---|
| **L0 recognition** | what is a valid entry | `kernel/`, SPEC §1–9 | `push` with a run of record and reads | two checkers, 100k seeds, vectors, pins, CI from trunk | strong |
| **L1 adjudication** | what may reach `main` | `judge/`, SPEC §10, `.github/workflows/` | `push` | the judge from trunk on every proposal and on `main` itself | strong |
| **L2 the charter** | maxims, secondary rules, build order, falsifiers | `CHARTER.md` | `transmute` + `amend` | only where L0/L1/L3 code implements a sentence; otherwise prose | mixed: `tools/enforcement.json` says which |
| **L3 the window** | criteria, nulls, thresholds, writ classes, scope | briefs, `tools/status.py`, `tools/clerk.py`, `pins/` | a proposal merged; the brief "binds from the opening push" | `status.py` and the pins; `party_scope` | code with constants; the constants *are* the brief |
| **L4 procedure** | how parties act | RUNBOOK, CASES, COUNSEL-OPEN, session templates, rulings | prose, merged or not | hand | weak; every incident since 25 Oct is here |

The audit's finding, restated by layer: L0 and L1 hold; the failures are at L3 (two ends for a window, `fix` with two meanings, unknown read as unmet, W1 coded for one window, constants in code) and L4 (rulings off the log, promises past due with nothing escalating them, amendments drafted and read-selected by one party). So the collapses below aim at L3 and L4, and most of them are *removals*: they make a term at L3/L4 into an instance of something L0 already recognises.

## 2. The loop underneath, stated as an invariant

Chapter 11 §11.0 of the book says what a closed loop is; here it is as a property the law can test.

> **The loop invariant.** The state is a fold over the ledger. Every obligation the state implies is itself an entry on the ledger — a *claim* with a proposer, a deadline and a set of principals who may resolve it — and its discharge is a *resolution* by one of them, with evidence, once. The clerk is the function `fold(log) × clock → claims past deadline`, and nothing else is an obligation. Escalation is a claim about a claim.

Everything that is an obligation today and is *not* such an entry is where the loop is open. The inventory, from the record: W3 writs (discharged by a sentence in COUNSEL-OPEN), W4 writs (discharged by `status.py` lines), W5/`COUNSEL-DUE.jsonl` rows (four past due, nothing escalates them), COUNSEL-OPEN `by` columns, the enforcement map's `hand` rows, the diary's due list (computed in another repository), the ladder's third rung (a printed word), rulings and their orders, the acts classifier's repairs. Each of these is a place where "the loop is closed" is a sentence rather than a fold. The invariant turns the question "is everything a ledger and a closed loop?" into a decidable one: *is there an obligation that `fold(log)` does not return?* — and that is the pin.

## 3. The collapses, by layer

Each row: what jack has now; what it is underneath; what it becomes; the layer the change enters at; what enforces it afterwards; the witness already on the record (the incident that would have been prevented).

### 3.1 Everything owed is a claim (L0 shape; L3 clerk)

| now | underneath | becomes |
|---|---|---|
| `forecast` {claim, p, resolves_by} | a claim with a deadline, resolved by another principal | `claim` {text, p (optional; 1–999), by, holders (principals or "any")} |
| W1 forecast overdue | the same claim past `by` | the clerk's one function |
| W3 unwitnessed merge | a claim "this merge's commit had a green run before it", resolver = the runs file | a `claim` the merge verb enters with its `merge`; resolved by the clerk from the committed runs file |
| W4 criterion unmet | a claim "criterion k holds by the window's end" | the brief's criteria entered as `claim`s at the opening, holders = the clerk, resolver evidence = `status.py` output hash |
| W5 / `COUNSEL-DUE.jsonl` rows | counsel's promises with a `due` | `claim`s by `counsel-2` — scored as items when they expire |
| COUNSEL-OPEN `by` | the same | the same; the file keeps only what is not a claim (rules, which are §3.4) |
| the promotion forecast V0/L0 | a claim "every criterion holds by T" | unchanged: it is already a claim |
| the item Y_i | a claim resolved on time by a holder who is not the sovereign | unchanged, now over every claim, so every party's promises are items |

*Layer.* L0 for the shape (one `claim` type where `forecast` is; `p` optional so a promise without a probability is still a claim — or `p` required, and a promise is a forecast at the probability its maker will stand behind, which is COUNSEL-OPEN row 8's rule). L3 for the clerk: `forecast_writs` becomes the only writ function, over every window (retiring the `subject == "C1b"` line). *Enforced by.* The kernel (double and self resolution refused as now); `status.py`'s item process over all claims; a pin whose mutant restores a second writ class. *Witness.* `tools/clerk.py:81`; four COUNSEL-DUE rows past due on 4 Nov; the six writs of seqs 442–447.

### 3.2 A window is a claim; promotion is its resolution (L0 types; L1 ground; L3)

| now | underneath | becomes |
|---|---|---|
| `decision promote W` | the sovereign resolving the window's promotion claim → 1 | `resolution` of V0 with outcome 1, evidence = the `status.py` output hash at that prefix |
| `decision veto W` | resolving it → 0 early | `resolution` of V0 with outcome 0, evidence "veto" |
| `decision fix "W: …"` (A2.6) | resolving it → 0 at its `by`, naming the precedent | `resolution` of V0 with outcome 0 and the precedent as evidence |
| `decision fix "<what>"` (BRIEF-C1b) | a repair: the sovereign's hand on an item | any `resolution` by `guy-master` of a claim whose holders exclude him — Y = 0 by the item rule, no kind needed |
| "the stated end" | V0's `by` | V0's `by`; a brief that states another date is ill-formed (§4) |
| "the window opened" | the opening `push` | unchanged |
| "the exit prefix" | the prefix at V0's resolution | unchanged |

*Layer.* L0: three decision kinds retire; `decision` keeps `budget` and `grant` (§3.5) and `transmute` if §3.3 keeps it. L1: `decision_by_other` becomes "the promotion claim is resolved only by a genesis key, or by the clerk's key when §3.5's inequality holds on the prefix" — one ground. L3: `status.py` reads the window from V0 and nothing else. *Enforced by.* kernel (one resolution per claim, never by its proposer), judge, `status.py`, pin `window_end_is_by` (mutant: a second date read from the brief). *Witness.* The window-fix ruling and its five corrections; `transcripts/CASES.md`'s two readings of C2a's end; counsel's wealth interest in which reading governs (RULING correction 2, last paragraph), which disappears when there is one.

### 3.3 One way a text enters: `enact` (L0 shape; L1 ground; L2)

| now | underneath | becomes |
|---|---|---|
| `push` {digest, review, record} | "the trusted base is hash H, read by R, run of record S" | `enact` {scope: "trusted-base", hash, review, record} |
| `transmute` + `amend` {id, charter, activate_at} | "the charter is hash H, read by R" | `enact` {scope: "charter", hash, review, witness} |
| a brief, merged by proposal, "binds from the opening push" | "the window's text is hash H, read by R" | `enact` {scope: "transcripts/BRIEF-<w>.md", hash, review} — the brief in force is on the log; a draft on `main` binds nothing |
| a ruling, a transcript | "this reading binds, read by R" | `enact` {scope: "transcripts/RULING-<…>.md", hash, review, witness} |
| a counsel rule (COUNSEL-OPEN "Rule:" lines) | a text that binds counsel | an `enact` with scope "counsel", or it binds nobody |
| `charter_mismatch`, `trusted_base_unrecorded` (two grounds) | "main's copy of an enacted scope hashes to what the log says" | one ground, `enacted_mismatch`, over every enacted scope |
| `activate_at`, the no-push wait, `push_during_amendment`, `charter_at` | the wait between text and code | retired: amend-last is the practice (RUNBOOK; Guy's rule of 19 Oct), so an `enact` binds from the next entry like every other effect |
| `transmute` | Suber's move; in practice the same key, within a minute, four times | retired, *or* kept as the one entry that makes a read mandatory — in which case the `review` hash on the `enact` is the mechanism, and `transmute` is a name for "review ≠ zeros" |

*Layer.* L0: one `enact` shape where `push` and `amend` are. L1: one ground. L2: the charter's §3 Change sentence, A2.6–A2.7 and A5.2 restated once the rule has decided an act. *Enforced by.* The judge refusing any `main` whose enacted scope's bytes do not hash to the latest `enact` for that scope — which is exactly what it does today for two scopes. *Witness.* COUNSEL-OPEN row 34 (two briefs on `main` as unread drafts "in force only after their reads" — a sentence, today); rulings off the log (CASES.md: "No text ranks a ruling before it is recorded"); row 33's verdict on amendments.

What this gives the amendment path specifically: a charter change and a brief change go through the *same* entry, the same `review` requirement, the same `witness` field (row 28's rule becomes a kernel/judge check: an `enact` with scope "charter" needs a `witness` seq that is a resolved claim), and the same pricing — counsel's claim about the text is a `claim` like any other. That is the whole of row 33's "an amendment judged as jack judges everything else", by construction.

### 3.4 One notion of witness (L2 reading; L3 registration)

| now | underneath |
|---|---|
| spec vectors (`spec/vectors/logs/*.jsonl` + `verdicts.json`) | (input → required verdict) against the checkers |
| pins (mutant + twin) | (input → required verdict) against a mutant of the code |
| simulator kinds | (generator → required verdict) against the checkers |
| `status.py` criteria | (prefix → met/unmet) against the window |
| tests | (input → expected) against a function |

All are what CHARTER §3 calls a rule's two witnesses: the case that must be refused and the case that must be admitted. Registered as one table (`witnesses/`: id, kind, input, required verdict, what it guards), the charter's "every rule is admitted with a witness that violates it and one that satisfies it" is *already in force* for every rule jack has — LAW.md's maxim-2 row reads `code` instead of "not yet law", and the rule language of A2.1, when a case for it arrives, is a witness file plus the mutant that fails it. *Layer.* L3 (the table and `pins/run.py` reading it); L2 only as the reading. *Witness.* LAW.md §2.2; REPORT.md's note that criterion 7 of C2a "has a test and no pin".

### 3.5 Thresholds are the owner's budget lines (L2 §6; L3)

| now | underneath | becomes |
|---|---|---|
| E ≥ 20 (α = 0.05) | a gate on a *reversible* act (A4.1 carries the wealth; a failed window is followed) — maxim 4 says price it | promote when prior odds × E > L_wrong / L_wait; the two ratios are `budget` entries by the sovereign |
| p₀ = 6/11 | the null's rate, a constant in `status.py` | a `budget` entry the brief names by seq; `status.py` reads the log |
| 5 : 1 | assize's ratio as a stop | the same |
| the counted-line cap in `judge/scope.json` | a resource budget inside the trusted base, so raised by `push` | a `budget` entry the judge reads from the log (`code_cap` compares against the latest budget for scope "counted"), so a cap change is a reversible, priced act, not a trusted-base push |
| 14 days | the budget of seq 50 | unchanged — it already is one |

E_t is a likelihood ratio against the null, so "promote iff posterior odds exceed the loss ratio" is the decision rule every other act in the court is held to; α = 0.05 is what that rule looks like when the odds and losses are left implicit. Written as budgets, "20" decomposes into two numbers that are the owner's — a prior that the layer works and a cost of a wrong promotion against a late one — entered under the kind the charter already reserves to him (§7: "the budget"). Ville's bound still holds at whatever threshold the odds imply. The same move retires the LAW.md commentary on maxim 4 (cap raises as sovereign pushes) and the book's §12.2 "theorem" row for α. *Layer.* L2 (§6 restated by amendment, after the rule has decided a promotion); L3 (`status.py`, `judge/scope.json` read budgets from the log; a pin whose mutant hard-codes a number). *Witness.* COUNSEL-OPEN row 28 ("the 20s, p₀ … conventions dressed as rules"); three cap raises as pushes; the audit §2.1–2.2.

A further step, if wanted: the promotion resolution is entered by the clerk's key when the inequality holds on the prefix, the sovereign's veto being the one act that stops it — which is row 16(a) of COUNSEL-OPEN, now a three-line rule instead of a widening of §10.14.

### 3.6 One machine principal (L0 keys)

`herald-2`, the diary, the runner and "the clerk's key" are one level-triggered process on steel. One principal `clerk` with powers {merge, claim, resolution}: it merges (the herald), files and resolves mechanical claims (the diary's due list, the stream resolver, W3's check), draws the election (C2b), and — if §3.5's further step is taken — resolves V0. Its escalation to the sovereign is a `claim` of kind `guy_answers` with the sovereign as holder, so the third rung is an item on his record. *Witness.* The book's ch 5/ch 7 contradiction on "the clerk"; the ladder's printed word; RUNBOOK's two names for one workflow.

### 3.7 "Object" is a property of the resolver, declared (L3 world types)

| now | underneath | becomes |
|---|---|---|
| object := the forecast's type starts `world.` | "an outcome produced by a process that reads no entry of the record" | each world type in `transcripts/world-types.md` is a record {name, resolver inputs, `reads_record: false`, `scheduled_by`}; a stream the court schedules is object for the *value* test and procedure for the *ratio* |

The ratio guard then measures what A3.4 meant (court writing about itself) instead of cadence; the value test keeps every world event. *Witness.* 324 of 342 `world.renavon` forecasts from one cron template; C2a's ratio 320 : 649 while twelve COUNSEL-OPEN rows were added in two days.

### 3.8 The enforcement map is a ledger (L3; the ratchet)

`tools/enforcement.json`'s rows are claims: "principle P is enforced by code at `path:fn`, witnessed by pin Q". A row saying `code` whose pin is not KILLED in the run that counts is a resolution 0; a row saying `hand` is an open claim with a deadline, held by counsel, due at the next window's exit — a writ like any other (it already is W4's shape; this makes it a claim). C1b's criterion 7 ("the rows this layer moves read `code`") generalises to the **ratchet**: every window moves at least one `hand` row to `code` with its pin, or its report says why none can. That is PLAN-20261030 §4's "recorded → scored → codified at the first witness" as a criterion rather than a sentence, and it is the answer to "how do we make sure the law is enforced": a sentence of the charter is enforced when its row is `code` and its pin kills; until then it is a claim counsel owes, scored when it expires.

## 4. Where formalisation sits in this

The audit's §5 model (state, step, grounds, `Window` with one `end`, three-valued criteria, a sum type for decision kinds) is the *statement* of L0 + L1 + L3 in one place. With the collapses above it is smaller than it would be today: five entry types (`genesis`, `key`, `claim`, `resolution`, `enact`), one ground for enacted scopes, one writ function, one witness table, budgets read from the log. Its three jobs:

1. **Vocabulary control.** Every term a brief uses must be a field of the model or it is a finding — "stated end", "inside the window", "repair", "late report", "finalised item", "object", "window code" are the first seven. This is the mechanical form of "too many special terms": a term with no field is a special case by definition.
2. **The invariants that the record has shown matter**, checked rather than argued: one `by` per window; a resolution's proposer is never the claim's; `fold(log)` returns every obligation (the loop invariant of §2); an `enact`ed scope on `main` hashes to the log; a `hand` row has a deadline.
3. **The third artefact for the second family.** kernel2 is written from SPEC; `status.py`'s successor is written from the model's L3 section the same way, by another family, from the text alone — so the window layer gets what the kernel has had since C0: two implementations and a differential.

What the model does not do: make L2 prose binding. A charter sentence binds exactly when it has a `code` row (§3.8); the model lists the rows that should exist.

## 5. Order of entry, by the method

1. **C2c brief (L3), no kernel change:** the clerk's one writ function over all forecasts (retires W-classes; pin); `status.py` reads p₀, the ratio stop and the thresholds from `budget` entries (pin: a hard-coded constant); the enforcement rows as claims with deadlines and the ratchet as a criterion; world types as data with `scheduled_by`; COUNSEL-DUE retired into claims. Witnesses: §3.1, §3.5, §3.7, §3.8 above.
2. **Then the kernel (L0), one push with reads and a run of record:** `claim` replacing `forecast` (holders optional, p optional); `enact` replacing `push` and `amend` (`activate_at` dropped); `decision` reduced to `budget`, `grant`, `veto`. Witnesses: §3.2, §3.3.
3. **Then the judge (L1), the same push or the next:** `enacted_mismatch` over every scope; the promotion resolution's signer; `code_cap` against the latest budget. 
4. **Then the charter (L2), by one `enact` of scope "charter" after each rule above has refused or decided an act** — §3, §6, A2.6–A2.7, A5 restated in fewer words, with the `witness` seqs that row 28 requires.
5. **The formal model (§4)** is written at step 1 as the C2c brief's own appendix — so the brief is the first text written to it — and kept beside SPEC thereafter.

Two things are the sovereign's and nobody else's: the budget entries of §3.5 (the prior odds and the loss ratio, or the decision to keep "20" as a single budget line until a utility exists), and whether `transmute` survives as the name for a mandatory read.
