<!-- Carried for the sovereign, binding nothing (A2.10: a question of what the charter allows is his). Written by an outside session (claude-fable-5-1, session_014kQ948RCM8NXdHfMHqrmQh) on 7 November 2026, before it held any key; proposed by counsel-3 under COUNSEL-OPEN row 34 (a cold read by a party counsel does not instruct, before any pull request). Its probabilities enter the ledger only as C2c's brief requires (the sovereign's direction of 3 November, row 24). Where it and the record differ, the record governs. -->

# meta-jack: a fresh read of how jack was built, and the shortest lawful path to its bootstrap

*7 November 2026, an outside session holding no key on the court. Read against `renavondata/jack` `main` at `3277ef1` (seq 2215, 2026-11-07T06:46:36Z), the lead session's transcript of 24 October–7 November (1,146 messages, 291 of them the sovereign's), its handoff of 7 November, the book at `gfrmin/agent-court` `57c7ed0`, the audit of 4 November and the self-similarity note of 5 November. Nothing here is on the record; every claim names the seq, file or turn it rests on. Probabilities are this session's, for whoever enters them.*

## 0. The verdict in six lines

1. **The court works. The process that builds the court does not keep the court's law.** The kernel, the judge, the pins and the keys have not failed once in 24 days. Every failure since 25 October is in the layer the law does not reach: the briefs, the amendments, the rulings, and the chat in which they are made.
2. **jack has had no litigant but meta-jack.** 718 of its 842 forecasts (85 %) are a cron template's; its value wealth stands at 10⁷ and its liveness at 10⁶ on a stream the court schedules for itself. The only criteria with teeth, C2a's 7 (zero sovereign repairs) and C2b's 8 (counsel's promises kept), judge the process that builds the court. The court should say so and measure that.
3. **Counsel is the seed agent, unelected.** One session drafts the charter, the briefs, the rulings, the corrections, the readers' prompts and the session templates, chooses the models and advises the sovereign in a chat the record does not hold; it is scored only on forecasts it was told to stop entering. Forty-four self-made rules in twelve days is proplang's "every incident minted a clause" one level up (book ch 14 §14.8; audit §4.3), and ten cold reads on one row is what prose law costs.
4. **"Law as computation" stopped at the kernel.** Briefs are English programs compiled by LLM readers; windows are Python constants; the charter's thresholds are conventions. The book's thesis was available for the window layer from C1 and was applied there on 5 November, as a draft.
5. **The sovereign is the clerk of the meta-process.** 57 of his 291 turns ask what to do next, 34 paste terminal errors, 14 ask for exact commands, 24 say that time or attention is being wasted or that a constant is arbitrary. He holds 49 entries on the log and is asked for a decision roughly once a day; the rest is operation the law said would be the clerk's (CHARTER §5).
6. **The bootstrap is one predicate away, and it is the same event as counsel's exit.** Stated as a decidable claim with a date, it can be the stated end of the next real window. Done in the order the law already prescribes, it needs five or six sittings of yours between 17 November and mid-December, each a read and a paste. My probability that it holds on the record by 15 December is 0.35; by 15 January, 0.6.

## 1. What "bootstrapped" has to mean

The record holds three definitions. The 26 October process (lead transcript, turn 179) gave "the bootstrap as a pin": liveness and value at 20, an invitation decided without you, no challenger pending, ratio within 5 : 1, counsel not invited that window. PLAN-20261030 §4 gave: "no row in the hand column has a witness, the sovereign's column holds decisions only, and the map is printed by code". The self-similarity note §2 gave the loop invariant: every obligation the state implies is a claim on the ledger, and the clerk is `fold(log) × clock`. The book's own test is ch 11 §11.0 — a judgement is closed into a loop only when "the act [is] an entry, the outcome an entry, and the relation between them a number that moves" — and its definition of self-governing is §11.10: a system that "governs itself under a law it can change only by its own procedure, and … grants powers only by its own record, with one party outside the scoring — the owner of the utility".

Read together, those say one thing the record has not yet made decidable. The construction is bootstrapped when *every function that today lives in a chat session is either code the clerk runs, an elected session acting under a key, or a sovereign decision* — and the record can show it. Counsel's functions, listed from the transcript and the handoff: draft briefs; draft amendments and rulings; choose readers and write their prompts; file and route sessions; track obligations (`COUNSEL-DUE.jsonl`); write reports; route procedures to models and watch the spend; answer the sovereign's "what now?"; and hold the only copy of its own key and tools (handoff §First acts: both lived in a scratchpad and must be rebuilt). While any of those is a session's habit rather than a loop, the law is followed by a person's vigilance, which is the thing the charter was written to retire (§7; book ch 11 §11.8).

**The predicate (B0–B7), each decidable from the log, the tree and the runner's record:**

- **B0 Safety.** Both checkers agree on the prefix; the trusted base changed only by `push` with a read. (Holds today.)
- **B1 One change path.** Every text in force — charter, SPEC, the window's brief, a ruling, a session template, counsel's rules — is named by an entry carrying its hash, its read's hash and the seq of the witness that forced it; `main`'s copy hashes to that entry; a text with no such entry binds nothing and the judge says so. (Self-similarity note §3.3, `enact`.)
- **B2 The loop invariant.** Every obligation is a claim on the log; `fold(log) × clock` lists every claim past due; no claim is past due without an escalation entry — a claim about it, held by a party other than its proposer. (Note §2, §3.1.)
- **B3 Windows are data.** `status.py` reads a window's criteria, null, thresholds and end from an entry or a committed window file; outside it the only numerals are 0 and 1 (wald's rule S3, lead transcript turn 666); a new window is an entry, not a code change inside the window it governs. (Audit §3.6 item 9; note §3.5.)
- **B4 Readers are drawn.** For every text that claims force, the reader is drawn by the clerk from the record, is of another family than the drafter, and never sees the drafter's argument. (Your decision of 4 Nov, COUNSEL-OPEN row 33.)
- **B5 The sovereign is priced.** Over the window every act under your login is a `decision` (wish, veto, grant, budget, enact); repairs 0; decisions within a budget line you entered. (CHARTER §7; A2.6.)
- **B6 Counsel is a role.** Every function in the list above is code on the runner, an elected session under a key, or a sovereign decision; no entry in the window originates in an unkeyed chat; counsel's key and tools are in the court, not a scratchpad. (This is the enforcement map's first `hand` row, "no party acts except through entries, enforced by sessions", which the book itself names as what still stands between jack and "self-governing": ch 8 §8.4.)
- **B7 The monitor.** A party the owner does not operate verifies the head hash and both checkers on every push to `main` and writs on failure. (A2.8, unbuilt; LAW.md's last section.)

The bootstrap window's promotion claim is "B0–B7 hold on the exit prefix", entered by counsel, resolved by a reviewer of another family. The first act of the bootstrapped court is then the kernel collapse of the note's §3.1–§3.3 (`claim`, `enact`, ten types to five) — *not* a step on the way to the bootstrap but its first self-modification, judged by the loop alone. That is the demonstration the book's ch 11 §11.12 asks for ("a level at which adding another changes nothing in the law"), and it is why the collapse should wait: done before, it is counsel redesigning the kernel by hand; done after, it is the court changing itself. The book's one-sentence rule says the same: "self-modification is permissible exactly where the modifier cannot reach the court that scores it" (ch 11 §11.9a) — and today the modifier, counsel, reaches that court through the chat.

## 2. Where it could have been done better

### 2.0 The book's own test, applied to the process that built it

Chapter 14 §14.8 states the lesson the lineage does not capture: "In every predecessor the governance was right about the artifact and blind about itself … Each law held its subject to a standard it did not hold itself to, and each owner was the one party outside the record." It then claims jack's two additions are "exactly those two: the law is under the same test as the artifact … and the owner is inside the record". On the record of 25 October–7 November the first claim holds for the artifact and fails for the process: the kernel and judge are under pins, twins and two implementations; the briefs, amendments, rulings, readers' prompts and counsel's rules — the texts that have actually decided every contested question — are under none. The owner is inside the record for his 49 entries and outside it for the 291 turns in which the law was made. The same section says why: "writing the discipline down does not install it; only a mechanism that forces the failure to be seen changes the catch rate." COUNSEL-OPEN's 44 rows are the discipline written down. Every predecessor's table row (ch 14 §14.7) has a jack reading one level up: credence's "score with no ground truth" is the value wealth on a cron stream; proplang's "law in prose, no priced world" is the briefs; tannen's "prose law satisfied by a pipeline that computes nothing" is *E* = 10⁷ on a stream nobody uses; wald's "the owner the referee" is the sovereign answering "what now?" 57 times. None of that is a reason to doubt the thesis; it is the thesis's own prediction about a process it was not applied to, and the rest of this section is the inventory.

Ordered by what it cost in days and in your attention. Each names the lesson the book already states and the witness on the record.

### 2.1 A court built before its litigant, measuring itself

The build order (§8) puts the agent at C3 and lets C0–C2 "contain no agent". So C1b and C2a needed something to count, and counsel invented it: HKJC races, then an hourly cron template under the reviewer key forecasting whether a Renavon dataset page's `dateModified` advances. By seq 2215 the log holds 673 `world.renavon` and 45 `world.hkjc` forecasts against 62 `counsel.programme` and 41 `review.forecast`; the builder's 690 resolutions are the same stream's. Value *E* ≈ 10⁷ and continued liveness ≈ 10⁶ (REPORT.md C2a §1) are numbers no threshold can gate. The audit's §2.3 already names this as the Goodhart case of the book's ch 2 §2.5; the fresh point is what it says about the *object*. The acts the court has actually judged — the ones that failed windows, forced rulings and cost reads — are counsel's texts and your repairs. C2a failed on criterion 7 (nine repair rows under your login, seq 1076); C2b's criterion 8 is "counsel bound". **The litigant jack has had since 25 October is meta-jack** — which is also what the book says the construction is for: "repairs are the quantity the whole construction is built to drive to zero" (ch 0 §0.1). The honest instrument measures that: the sovereign's repairs, the drafter's texts passing their reads first time, the obligations discharged on time, the dollars per entry. Every one of those is on the record now and none is a `world.*` type.

The book's lesson: ch 14's lineage ends six repositories on the same note — the criteria measured the artefact, not its use (lead transcript, turn 179: tannen's M5 "computes nothing" passing 128 laws; life-agent's exit test that "has not started counting"). A cron stream beating a base rate is the artefact measuring itself. You said it four times: "HKJC is just the means to an end" (turn 467), "we keep forgetting what we're trying to achieve" (660), "at this point we don't really care how good you are at predicting" (654), "the aim is the system, not the forecasting" (row 30).

*What it cost:* the hourly stream's dollars (OpenAI's $250 cap reached on 6 Nov, raised to $500; the budget entry seq 50 says $300 and nothing on the record counts against it); 2–3 November's liveness collapse from 121 to below 1 when BRIEF-C2a Amendment 2 raised the cadence past the merge path (row 29); and a value test that will promote C2a-prime on numbers that mean nothing.

### 2.2 Counsel: the unelected seed agent

The charter's §5 makes every model, counsel included, an untrusted proposer, elected by record, scored. On the record counsel holds `proposal, forecast, resolution` and nothing else — and in practice drafted every binding text (A1–A5, every brief, both rulings, every correction, CASES.md, LAW.md), wrote the readers' prompts and chose which models read, decided model routing and session templates (rows 22–25), tracked its own obligations in a file it alone writes, and answered 291 chat turns, most of which steered the court. The book's ch 11 §11.7 reports the counsel loop closed ("The designer is scored and escalated like anyone"), on 40 resolved programme forecasts. The record says otherwise: on 3 November you ruled that counsel "enters no forecast beyond the brief-required X-series" (row 24), so the scored stream stopped; the chat recommendations that actually moved the court — A6 twice, "prepare C3 now", the 14-day window, the hourly cadence, the identity plan — were never entries. The 26 October process (turn 179) had rule 5, *an instrument that has refused nothing in two windows lapses*, and rule 6, *counsel's standing role ends when liveness crosses 20 for the clerk; from then I am invited per claim type by the election or not at all*. Liveness crossed on 1 November (seq 337). Neither rule was built, and counsel's role grew instead: COUNSEL-OPEN went from 23 rows on 1 November to 44 on 7 November, twelve of them on 3–4 November.

This is the book's own diagnosis of proplang (ch 14 §14.8: "every incident minted a clause and none retired"), applied to counsel's rules, which bind counsel alone, are not pinned, and have no lapse. It is also maxim 1 violated at the layer where it matters most: the party that drafts the brief chooses its readers, drafts the ruling on the brief's failure, drafts the corrections to its ruling, and holds forecasts on the outcome (RULING-20261104 correction 2, last paragraph). Counsel disclosed all of it, which is to its credit, and you named it on 4 November (row 33). But disclosure is not a mechanism — the book says exactly this of itself in ch 16 §16.1, and ch 9 §9.6 names the residue in one line: "The thing that changes [the law] is still a person and his counsel, through a passage with sessions in it." Even the ruling that stopped counsel's forecasts "is in counsel's session, not on the log" (ch 12 §12.3) — a sovereign act that A2.6 says is an entry.

*What it cost:* the identities item took ten cold reads (turns 1152–1160); BRIEF-C1b seven versions; BRIEF-C2b 10,700 words and nine amendments; 41 `REVIEW-*.md` files and 15 replies to them; and your attention, because a party that cannot decide questions in its own interest sends them to you, and counsel had an interest in nearly every question (window end, criterion 7, criterion 8, the identities, the contracts).

### 2.3 Prose where the law needed data

The charter's §4 says law is computation and the kernel honours it: SPEC §8's ten steps are `check.py`'s ten steps, and two implementations agree on 636,392 prefixes. The window layer never got the same treatment. A brief is a prose document; its criteria become Python with constants (`P0 = 6/11`, 7,800, 14 days, the window names, `if s["subject"] == "C1b"`), so each new window is a code change inside the window it governs and each read is an LLM asked whether 10,000 words have one operational meaning (turn 1141: "today's failed cold reads were compilation failures"). The two-valued end of C2a, the `fix` kind with two meanings, "unknown read as unmet", W1 coded for one window — every ruling since 25 October is a type error a window record with one `end` field would have refused at the brief (audit §5.3). You had this rule in September: wald's S3, no numeral outside a declared table; tannen's laws; the C0 decision that a kernel ambiguity is "a finding, not a patch". It was not carried to the briefs until BRIEF-C2c Appendix M on 5 November — which is the right shape (M.1–M.3 are rules with twins and mutants) and should have been the shape of BRIEF-C1. tannen's lesson applies verbatim: "writing the discipline down does not install it — the production rate of this class does not fall with attention, only the catch rate does, and only when something mechanically forces the failure to be seen" (ch 14 §14.3). A cold read is a catch; a window record with one `end` field is the mechanism.

*What it cost:* most of the reads, the ruling of 4 November with seven corrections, and thirteen days in which no window can open, over which of two dates a brief meant.

### 2.4 Conventions where the law needed budgets — maxim 4 unapplied to the court itself

Maxim 4 says reversible acts are priced, never blocked. The court's own promotions are reversible (a failed window is followed; wealth is carried, A4.1) and are gated at *E* ≥ 20 — α = 0.05 copied from the charter's one example onto every layer. Windows were given fourteen-day terms (A3.2) until A5 made them maxima; C1a met every criterion on 29 October and would have sat idle to 8 November under A3's text (A5's own preamble). The window-end question then produced the opposite failure: C2a's verdict settled on 3 November at 21:26Z (seq 1076) and its window runs to 17 November because A5.1 gives a window no exit for having already failed, and the amendment that would add one was drafted twice by the party that caused the failure and stopped by you (row 39). Thirteen days of November — your scarcest month — at zero option value, which your principle 3 of 5 November calls a defect (A6-CASE, turn 1040). The audit §2.2 and the note §3.5/§6.1 settle the design: thresholds are the sovereign's budget lines, the promotion rule is "prior odds × *E* > *L*_wrong/*L*_wait", and *k* in 3–5 is the honest range for a layer that grants no power. The fresh point is about *order*: the three tests were run in series on the same activity (turn 481, cost "measured in weeks") when nothing in Ville's inequality requires it, and the pipelining rule (PLAN §3) was found on 30 October rather than written into §8.

### 2.5 Operator before executive: the cage came last

wald in September began with the cage — a builder user, a deploy key, a ruleset that refused the builder's push to master before a line of kernel was written (overview, 20 Sep). jack's charter §5 named the same architecture on 13 October (clerk as executive, keys by role, a monitor the owner does not operate) and §8 put none of it before C1. The herald lived in counsel's session until 31 October (row 17); the verb had never been run by the herald's own key (row 18); counsel's GitHub acts ran under your login until 6 November (rows 20, 44); the runner, diary and courier live in another repository the court does not judge (your words, 4 Nov: "the runner should be under the court too"). The consequence was mechanical: C2a's nine repair rows were the court's machinery acting under your login, criterion 7 refused, and the window was lost. Your priority was stated on 20 October — "stop the process depending on him as its operator" — and the mechanism arrived on 30 October–3 November, after the windows that measured you.

*What it cost:* C2a; the key-declaration refusals (turns 67, 271, 457), the runner installs (367–379), the token updates — all repairs by §7's letter, all off the instrument; and the 291 turns, of which about a fifth are you asking for the next command. The meta-process has no clerk; you are it. The book's assize rule — "a session that asks the owner something it could have decided and recorded has failed" (ch 14 §14.6) — was adopted for jack on 4 November (row 34, rule 4) and is kept by promise, not by a pin.

### 2.6 The meta-process is off the record

Maxim 3 says whatever is held must be produced from state and clock. The things that govern jack's building are held in a chat: the priors "lost to context compaction before they were entered" (row 3); the acts classifier that lived in a Project doc until a builder could not obtain it (row 31); counsel's key and tools in a scratchpad, to be rebuilt by the next session (handoff §First acts 1–2); the foundation note you could not find on 1 November (turn 490); rulings as transcripts, outside recognition and the hash chain (audit §4.2; CASES.md: "Rulings are not entries on the log"); the outside session's audit, which the author session read from `~/Downloads` "because it could not reach the Project" (QUESTIONS.md); counsel's obligations in a file counsel writes. The layer below the charter — your question of 3 November — is, mechanically, genesis and the keys (turn 664), and in practice *this chat*. The law is made in conversation and recorded afterwards by the party that made it. The book's lesson is the record's own first rule ("the record, not the recollection, is the memory", row 3) and ch 11 §11.0's test; the bootstrap is complete when the chat layer is empty.

### 2.7 Money and cadence

The budget is on the log (seq 50: $300 a month) and nothing reads it. Fourteen astra sessions cost about $50 in a day, most of it reading the whole log (row 22); the hourly stream chosen to speed liveness and then found to saturate the merge path; the OpenAI balance ran dry on 6 November with no alarm (handoff §5). A spend line per session on the record — a claim resolved by the diary — is a few lines and would have made every cadence decision a priced one, as row 29's load line does for writs.

### 2.8 What was right, and should not be touched

The kernel/judge/second-checker/pins discipline, which has refused nothing it should have admitted and admitted nothing it should have refused; keys by party and the closed set of verbs; the ledger-first reordering (A3), which was correct and cheap; windows as maxima (A5); the cold-read habit, expensive but the only thing that caught counsel's errors; the honesty of COUNSEL-OPEN, which indicts its author on every row; the refusal to design C3 early; and your own interventions, which were right every time they were made — "no amendment now", "stop", "don't gate on something impossible", "why 24 hours", "smaller steps", "the runner under the court too". The 5 November note's collapses are the right design for the window layer and should be built as written.

## 3. The lawful path to the predicate

### 3.1 What binds now, and what is free

Binding: the charter through A5; SPEC and the trusted base; C2a's window until 2026-11-17T12:00:00Z (its verdict is settled; its end may not be moved, A5.1); your directions of 4 and 5 November (C2a-prime pre-stated with wealth carried; the charter amended only by a judged procedure; C2c is the self-similarity layer; A6's clause and principle 7's ranking as C2c's first amendments). Not binding: every unopened brief. BRIEF-C2a-prime and BRIEF-C2b are counsel's drafts until their opening push (BRIEF-C2b Amendment 2, "the brief is counsel's draft until the push that opens the window"; CASES.md), and a pre-opening amendment with reads is lawful. That is the whole design freedom, and it is large. What constrains it is not law but the price of re-reading texts that have passed their reads: C2a-prime v7 and C2b v6 + 9 have each passed two formal reads; re-litigating them costs more reads than running them. So:

### 3.2 The order

**Now to 17 November — no law moves; everything that can be built is built.** The pipelining rule (PLAN §3) and the C2b precedent ("§Scope forbids landing under C2a's cap, not building") make this lawful. On branches, by builder and reviewer sessions through the runner, read by another family before any opening:

1. *The window layer as data* (B3): `tools/status.py` reads one committed window file per window — opening rule, promotion-claim id, criteria as predicates over prefix and tree, null, thresholds, the ratio stop — and the pin `numerals_housed` whose mutant is an inline constant. The C2c-1 window file is the first text written to it.
2. *One writ function* over every forecast in every window (B2; BRIEF-C2c M.3), and the enforcement map as claims with deadlines (note §3.8).
3. *A `ruling` kind for `decision`* (or the note's `enact`), SPEC text first, kernel2 by the other family from the text alone, the differential, a run of record — on a branch, for C2c-2's push (B1). The smallest form: a `decision` of kind `enact` whose subject is `<scope>@sha256:<hash> read:<hash> witness:<seq>`; the judge refuses a `main` whose scope's bytes do not hash to the latest `enact`. This is one ground generalised from the two the judge already has (`charter_mismatch`, `trusted_base_unrecorded`).
4. *The monitor* (B7): ~50 lines that fetch `main`, verify the head extends the last published hash and that both checkers accept the log, and publish the hash; run on a schedule under the `assize-reviewer` account rather than your login, with the script public so that anyone — the book's readers first — can run it. Owner-independence is partial until someone else does; the book says so in ch 12 §12.4 and should keep saying so.
5. *The `NaN` vector, kind and kernel fix* (audit §3.6.1), with `count_kernel.py --limit 500` in CI.
6. *Counsel's key and tools in the court* (B6): the courier's `req.py` and the proposal tool as files under `tools/` (or the runner's repository, which comes under the court in C2c-1 by moving its workflow definitions into `transcripts/sessions/` where the templates already are), so the next session rebuilds nothing from a scratchpad.
7. *A spend line* in the diary: dollars per session as a claim the diary resolves daily against seq 50.
8. *The witness ledger* counsel began (handoff §5), read cold, binding nothing — it is the list of B-rows and the C2c-1 brief's §Precedents.

Your acts in this period: one paste if you want a counsel key declared now (counsel-3 declared, counsel-2 revoked — the verb needs `--principal` and `--pubkey` for a revocation too, so the paste writes counsel-2's pubkey out of the log first), none otherwise.

**17 November, after 12:00Z — C2a closes, C2a-prime opens.** Exactly the pre-stated paste (`transcripts/PUSH-c2a-prime-opening.md`): the `grant`, the `fix`, the opening push. One sitting.

**18 November — C2a-prime promotes at its first lawful prefix.** The brief "states no minimum length … If every criterion holds an hour after the opening, the window closes in an hour." Criteria 1–6 hold at the opening with the runs evidence supplied; criterion 7 needs an acts file over the window showing zero repair rows, which it will if only you act under `gfrmin` and you make no platform act. Counsel's proposal carrying the evidence merges by the herald; you enter `decision promote C2a` and, in the same sitting, the herald's re-declaration with `forecast` (BRIEF-C2b §Precondition) and C2b's opening push (its cap, W5, the election code, the reviewer's pins, all pre-built on `builder-c2b-status` and `review-w5-pins-8`). One sitting.

**19–20 November — C2b's 24 rounds, then promotion.** Hourly rounds need a day; criterion 8 needs counsel's rows discharged on time, criterion 9 zero repairs. The stream runs hourly for exactly this day and is cut back after it. You enter `decision promote C2b` and C2c-1's opening push. One sitting.

**C2c-1 — the window layer (L3), no kernel change.** Items 1, 2, 6, 7 and 8 above land from its opening push; the brief is the window file plus Appendix M; its criteria are B2 and B3 plus the ratchet (every `hand` row of the map moves to `code` with its pin or the report says why none can) and B5; its promotion claim is counsel's, resolved by a reviewer; its end is that claim's `resolves_by`, with no minimum. Budget: five days. Your acts: the budget lines of the note §6.1 (the prior odds and the loss ratio, or "20 as one budget line" if you would rather not price it yet) in the opening paste; read the window file (A2.10: code is written to a text you have read); promote at the crossing and open C2c-2. One sitting.

**C2c-2 — recognition and adjudication (L0 + L1), one push.** Items 3, 4 and 5 ride the opening push with their reads and run of record. Criteria: safety (two checkers, vectors, the kernel ≤ 450 — it should shrink), B1 (every text in force named by an `enact`; rulings on the log), B7 (the monitor publishing). Budget: three days. Your acts: sign the push after its reads; promote at the crossing. One sitting.

**C2c-3 — the bootstrap window.** The charter restated by one `enact` with its read and witnesses, A1–A5 folded in and §6's thresholds moved to budget lines (the first amendment to go by the path you described on 4 November); readers drawn by the clerk (B4); counsel's functions mapped row by row to code, election or decision (B6); the promotion claim "B0–B7 hold". Budget: a week. Your acts: read and `enact`; promote. One or two sittings.

**Then C3.** §8's C3 exit reads "assize's sealed judge: beats random on held-out seeds in both Worlds". Assize's record (`REPORT.md` at `ff41aaa`, 28 Oct) says: "L2 — SEALED (L2c); Crafter FIT under the sealed judge; NetHack carried". One World is sealed; the other was carried to jack and will not be built in a frozen court. So the row as written cannot be met, the witness is already on a record (and counsel's J3, seq 38, resolves 1 against that line on 8 November), and "don't gate on something impossible" (your words, 6 Nov; maxim 2) is the ground for the one-word amendment — "both Worlds" to "the sealed World" — by the `enact` path once it exists. C3 then stays what the charter says: the seed agent in Crafter under the sealed judge image, with NetHack as a later World if ever. Two things make this cheaper than it looks. The agent that acts on *your wishes* — the thing you asked for on 24 October — is not C3's Crafter agent; it is the elected drafter of B6, which the bootstrap window already builds: a session that takes a wish, drafts the proposal, forecasts its acceptance (passes its first read; merges; you accept without correction) and is scored on those outcomes against counsel's record as the incumbent. The court itself is that agent's first world, and it needs no §8 change because it is C2's election applied to the drafting role. C3's own brief is written from C2's report and not before (book ch 10 §10.5; PLAN §3 forbids pipelining C3), so nothing of it is built in C2c. Spends: one witnessed amendment; the Crafter harness assize already has. Reversible: yes. Stop condition for the court-as-world: a reviewer finding that "the sovereign accepts" is not a boundary the drafter cannot move — then the scored outcomes are the reads and the merges alone.

### 3.3 Your acts, complete

| when | act | kind |
|---|---|---|
| any time before 17 Nov | declare counsel-3, revoke counsel-2 (optional now; needed before C2c-1) | grant |
| 17 Nov, after 20:00 HKT | the pre-stated paste: `grant`, `fix`, opening push | decision ×3 |
| ~18 Nov | `promote C2a`; `key herald-2 … --powers merge,forecast` (BRIEF-C2b §Precondition, a re-declaration); C2b's opening push | decision ×3 |
| ~20 Nov | `promote C2b`; C2c-1's opening push with the budget lines | decision ×3 |
| ~25 Nov | read the window file; `promote C2c-1`; C2c-2's push after its reads | read, decision ×2 |
| ~28 Nov | `promote C2c-2`; C2c-3's opening | decision ×2 |
| ~early Dec | read and `enact` the restated charter; `promote C2c-3` | read, decision ×2 |
| after C2c-2 | the §8 C3 amendment (one word), after its reads | read, enact |

Six or seven sittings; no rulings, if the briefs are written to the window record so that no question of what a text means can arise. Every date is a budget (PLAN §6: "dates are budgets; exits are crossings"); every one can be beaten and none may be extended without a failed window.

### 3.4 Counsel's functions, mapped

| function today | becomes | by |
|---|---|---|
| tracks obligations (`COUNSEL-DUE.jsonl`, COUNSEL-OPEN `by`) | claims on the log; the clerk's one function | C2c-1 |
| answers "what now?" | the diary files a `sovereign-due` issue with the exact paste when and only when a decision is reserved to him; nothing else reaches him | C2c-1 (runner) |
| files and routes sessions; chooses models | the diary, from the window file and the election's weights; the spend line | C2c-1; C2b |
| chooses readers and writes prompts | readers drawn by the clerk from the record; prompts are session templates on `main`, changed by proposal | C2c-3 (B4) |
| drafts briefs | the window file is the brief; prose is commentary; the drafter is an elected session from C3 | C2c-1; C3 |
| drafts amendments and rulings | `enact` with read and witness; rulings are entries | C2c-2 |
| writes reports | `status.py` prints the report; counsel adds the precedent cases | C2c-1 |
| holds its key and tools in a scratchpad | both in the court | now |
| advises in chat | a proposal with a forecast, or nothing | C2c-3 (B6) |

### 3.5 What to stop now

- The hourly freshness stream beyond what C2b's 24 rounds need; after C2b it is cost with no object. Wealth is carried; no bet is placed on a stream that does not run.
- Reads of any text no act depends on (row 35's rule, kept).
- Re-narrating threads; a pointer and one row (adopted 6 Nov).
- astra sessions that read the whole log; the clerk prints what is due.
- Any charter amendment before C2c-2's `enact` path exists — your decision of 4 November, kept.
- Chat recommendations without an entry: from C2c-3, a recommendation that is not a proposal with a forecast is not made.

### 3.6 Claims, for whoever enters them

| claim | p | resolves by |
|---|---|---|
| C2a-prime promotes within 48 h of its opening | 0.6 | 2026-11-20 |
| C2b promotes within 72 h of its opening | 0.55 | 2026-11-24 |
| C2c-1's window file is the first text its code is written to, and `status.py` holds no window constant at its exit | 0.6 | C2c-1's exit |
| rulings are entries on the log (an `enact` or equivalent) | 0.6 | 2026-12-15 |
| the monitor publishes a verified head hash on every push to `main` under an account other than the owner's | 0.6 | 2026-12-15 |
| B0–B7 hold on a window's exit prefix | 0.35 / 0.6 | 2026-12-15 / 2027-01-15 |
| §8's C3 row is amended ("both Worlds" → "the sealed World") by the `enact` path | 0.55 | 2026-12-31 |
| another window fails at its stated end before the bootstrap claim resolves | 0.4 | the bootstrap claim's `resolves_by` |
| the hourly stream is stopped within a week of C2b's exit | 0.6 | 2026-12-01 |

### 3.7 Stop conditions for this plan

- A cold read finding that B1–B7 is not decidable as written: the row is rewritten or dropped, never softened in prose.
- C2c-1 failing its window: the next window is pre-stated, wealth carried, and the failure's precedent is the ledger's first row.
- The ratio of procedure to object staying above 5 : 1 once "object" means what §3.7 of the note says (a stream the court did not schedule) — then the court has not converged and C3 waits (book ch 11 §11.12).

## 4. On the handoff

Counsel's handoff of 7 November asks the next session to generate a key, rebuild its tools from a Project this session cannot see, and resume with the witness ledger. Two of those three are §2.6's lesson in one paragraph: the key and the tools belong in the court — the private key on steel beside the herald's, used by the courier under the grant of seq 2131, so that it survives the session that drafts with it; the tools under `tools/` or the runner's repository, changed by proposal. If this session is to be counsel-3, its first proposal should be this note (binding nothing, read cold by another family) and the bootstrap claim of §1, entered under its key; its first build items are §3.2's 1–8; and its first rule for itself is B6 — nothing it says to you is a recommendation unless it is also an entry.

## Appendix: the book's lessons, checked against the process

Each rule as the book states it (ch 14 unless marked), whether jack's artefact keeps it, whether meta-jack keeps it, and the row of §3 that would close the gap.

| lesson (chapter) | the artefact | the process | closed by |
|---|---|---|---|
| a score with no world behind it is not a score (§14.1, credence) | kept: forecasts resolve on hashed pages | not kept: the value and liveness wealths are the court's own stream (audit §2.3) | §3.5 stop the stream; note §3.7 `scheduled_by` |
| "a framework dies of a thousand locally reasonable patches" (§14.1) | kept: no `rule` type, three secondary rules | not kept: 44 counsel rules, 9 brief amendments, 5 charter amendments in 17 days | B1, lapse for counsel's rules |
| pins: "a green that cannot fail is a non-functional alarm" (§14.2, proplang) | kept: 115 pins, twins | not kept: amendments priced by near-unlosable forecasts (row 33) | B1 `enact` with a witness; B4 |
| "I don't want to rely on prose and vigilance any more, ever" (§14.2) | kept in the kernel | not kept: briefs, rulings, COUNSEL-OPEN | B3 windows as data |
| "every incident minted a clause and none retired" (§14.2, §14.8) | kept: the ratio guard, as far as it sees | not kept: COUNSEL-OPEN rows 24–44 | lapse; the ratio counting counsel's texts as procedure |
| a pipeline that computes nothing can pass every law (§14.3, tannen) | kept: differential testing, 100k seeds | not kept: *E* = 10⁷ measures a cron job | §3.5; B2 liveness over all claims |
| "rigorous but too slow"; the owner's cost measured (§14.3) | kept: acts tables weekly | partly: the chat's cost unmeasured; 291 turns | B5; the `sovereign-due` issue as the only channel |
| writing the discipline down does not install it (§14.3, §14.8) | kept: law is code | not kept: row 27's seven lines, row 34's rules, the 24-hour rule | B1–B6 as pins |
| the cage first; housed numerals; single exit (§14.4, wald) | partly: keys by party; `status.py` holds constants | not kept: the runner and identities came last; `P0`, caps, 14 d inline | B3; §3.2 item 6 |
| "the owner the referee" (§14.4) | kept: the sovereign's acts are entries | not kept: he rules, reads and operates between entries | B4, B5, the diary's `sovereign-due` |
| derive, never decide; ask only when the ruling blocks (§14.5, §14.3) | kept: `status.py` derives | not kept: rows 35, 37, 41–44 — questions put and withdrawn | B4; row 35's rules as code |
| "a session that asks the owner something it could have decided and recorded has failed" (§14.6, assize) | — | adopted as a promise (row 34) | a pin on the `sovereign-due` channel |
| the loop closed: act, outcome and relation on the record (ch 11 §11.0) | kept for proposals and forecasts | not kept for rulings, counsel's advice, the runner's acts | B1, B2 |
| the modifier cannot reach the court that scores it (ch 11 §11.9a) | kept for builders | not kept for counsel | B6 |
| someone other than the owner checks the record (A2.8; ch 12 §12.4) | not built | — | B7 |

## Residue

Three things this note does not settle and says so. *The loss ratio* is yours (note §6.1; it is life-agent's u_wrong). *Owner-independence* of the monitor is partial until a third party runs it. *The object before C3* is thin on any honest reading: meta-jack is a litigant, but a small one; the court earns its name when C3's drafter is scored against counsel on wishes you actually have.
