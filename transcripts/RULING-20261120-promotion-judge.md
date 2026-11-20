# Ruling of 20 November 2026: the judge refuses a promotion entered while a pre-stated criterion is unmet, the promotion evaluator moves under `judge/`, and four readings

**Draft.** Written by the sovereign's coding agent (`session_01VpB3Tknxi9JkERuANTGHDk`, `claude-opus-5-5`, holding no key of jack's). It is drafted from entry 7 of `ADVISER.md` on the orphan branch `adviser/notes` (commit `db9938597df4d400d2ae872569fbef5fc2c24666`, lines 260 to 280), as his answer 14 directs. By H3 of the ruling of 17 November a ruling is a `transcripts/RULING-*.md` file. By answer 14 this one reaches `main` by counsel's proposal. Texts on `main` are cited at `df72126c8d7cbb6b97353eb854d4c8f72c773313`.

## Who put the questions, and the limits of this record

The adviser put the questions (`session_01VpB3TipJ28s2VzPVN8HiPD`; `claude-opus-5-5` from its entry 6). It is an outside session that holds no key, and it put them in its own chat on 20 November 2026. Entry 7: "He chose each from options the adviser wrote. Every question stated the adviser's view, and every answer is the option the adviser recommended."

Four of the questions were first written into `ADVISER.md` itself, as its questions 1 to 4 for the sovereign (lines 106 to 113 at `db99385`). Answers 1, 3, 6 and 15 answer them. Question 1 asked for the refusal "by the checker itself, as a judge ground first".

The drafter has only entry 7. Its fifteen lines are the adviser's record of the option he chose, not his own words, and the questions and options as put are not in it. `transcripts/CASES.md` ("How a case enters") has "his answer is quoted verbatim". So before this file is proposed, the question and the chosen option for each answer are to be copied in from the adviser's chat, word for word, and the file corrected wherever they differ in meaning from the lines below. Request R6 of `ADVISER.md` asks the adviser to compare.

## The answers (entry 7, lines 266 to 280, verbatim)

1. **Refusal.** The trusted checker itself refuses a `decision promote` entered while any pre-stated criterion of the window is unmet: yes.
2. **Route.** It enters as a new judge and self-check ground in SPEC §10 and `judge/`, by his push alone, enforcing A5.1's existing sentence ("may be entered only once every pre-stated criterion … holds"), as items 11 to 14 enforce A2.6 and A2.7. No amendment and no rule language.
3. **Acceptance.** Every change to the promotion evaluator is accepted only if it reproduces a frozen table of today's evaluator outputs at every first-parent commit of real `main`, except rows marked wrong in advance: yes.
4. **First change.** `tools/status.py` and `tools/value.py` move under `judge/` as they are, with only the first-parent fix, and are shrunk later under the replay test. No rewrite first.
5. **Timing.** The move lands by a push before 30 November that opens nothing (precedent: seq 197). C2a-3 is the first window judged by it.
6. **Cap.** The move's push states the roughly 860 lines that leave the counted cap. The cap is lowered by that amount in the next window's opening push.
7. **Marked rows** for the first change: only C2a-prime's criterion 3, from `b88d318e` (the first merge after its opening) onward. The late-report change is a separate, later change with its own marked rows.
8. **Off-log evidence.** A promote names its evidence (the tests run; the acts table) by SHA-256, as files committed with it. The judge checks that they exist with those hashes and that the evaluator returns lawful on them. The record labels them attested, not checked.
9. **The table.** A reviewer session computes it and proposes it under `spec/vectors/`. The adviser recomputes it independently and posts any disagreement here.
10. **A2.10.** His read of the SPEC §10 paragraph (about a page) and of the marked rows, recorded by a `decision grant` naming both hashes, satisfies A2.10 for the move.
11. **Late reports.** C2a-3's brief may pre-state that a repair refuses only the window it was made in. The rule is not in the charter, and A2.4 bars loosening the charter's bounds, not an earlier brief's.
12. **Handover.** The one-clause early-end amendment (a window also ends, as failed, at his veto) proceeds now. The late-report change waits and comes through the replay test after the move.
13. **Drafter.** His coding agent drafts the SPEC §10 text. The adviser audits it.
14. **Record.** These answers are recorded as a `transcripts/RULING-*.md` file by counsel's proposal, drafted by his coding agent from this entry.
15. **Runner.** The adviser reads `renavondata/opencode-runner` read-only, for R4 only.

## The facts on the record

- **A5.1**: "A window named in this charter or in a brief ends at the earlier of its stated end and the instant of a `decision` entry by the sovereign whose `subject` names the window and whose `kind` is `promote`, which may be entered only once every pre-stated criterion of the window holds on the log's current prefix and on the tree at its commit."
- **A2.6**: "A change to the trusted base is lawful only when a `push` entry names its digest; the judge and the self-check refuse a trunk whose trusted base is not the one in force (SPEC §10.11). Veto, promotion, budget, grant, transmutation and the fix of a failed window are `decision` entries signed by a key declared in genesis (§10.14)." **A2.7** names SPEC §10.12 for its freeze ("Between the `amend` and its height no `push` is lawful"). Item 13 enforces its two acts.
- **A2.3**: "The judge refuses a proposal on any ground a layer's brief pre-states, provided the ground is decidable from git and the log alone, is stated over powers and paths and never over a party's name, and refusing costs the proposer nothing but resubmission."
- **A2.4**: "They bind that layer only, and may tighten the charter's bounds, never loosen them."
- **A2.9**: "a reviewer's key may propose only under `pins/` and `spec/vectors/`; a builder's key may not touch them".
- **A2.10**: "Code is written to a text Guy has read; questions of what the charter allows are put to Guy as rulings and recorded here."
- **§2**: maxim 2, "An entry is judged by the law in force before it."; maxim 4, "Hard gates stand only before effects that cannot be undone, where waiting has positive option value." **§3**: "The checker is the only adjudicator of validity."
- **SPEC §10.1**: the trusted base's files "change only by Guy's `jack push`, recorded by a `push` entry (item 11)". **SPEC §10**: "Items 11–14 apply to every judged log, the self-check included." **SPEC §5**: "New evidence travels as an optional member the verbs write and the judge may read".
- **The promote verb today.** RUNBOOK lines 191 to 198 and `tools/jack` lines 251 to 281. It runs `tools/status.py` on `HEAD` "with the `tests` runs GitHub lists", and signs only on `promote <layer>: lawful`. With `--acts` the body carries `acts` {path, sha256, commit}. `jack decision` runs the self-check before it pushes (`tools/jack` lines 76 to 78). No ground of `judge/judge.py` reads a promotion.
- **An unlawful promotion today** is printed, not refused. `tools/status.py` line 659 prints "sovereign REPAIR: promote …", and RUNBOOK line 358 calls it "a sovereign REPAIR, which no later success erases".
- **The log** at `df72126c` holds 6,432 entries, to seq 6431.
  - Promotions: seq 188 (`C1a`, 2026-10-31T10:42:10Z) and seq 337 (`C1b`, 2026-11-01T11:31:58Z).
  - Seq 197 is a `push` at 2026-10-31T13:04:49Z, inside C1b's window, which seq 188 opened. SPEC §10 records it as "C1b's cap push".
  - The last `push` is seq 5564, C2a-prime's opening. His `decision veto C2a-prime` is seq 5879.
- **`transcripts/BRIEF-C2a-3-draft.md`** (v4):
  - C2a-prime "runs to its stated end, 2026-11-30T00:00:00Z, with no change inside it" (line 7).
  - "C2a-3 opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z" (line 75).
  - "The promotion is `decision promote C2a`" (line 102).
- **The evaluator's size and reach.**
  - `tools/status.py` has 678 lines and `tools/value.py` 181, 859 together by SPEC §10.10's count.
  - `tools/value.py` line 15 imports `now`, `read_log` and `resolution_rates` from `tools/entry.py`, which imports `harness/keys.py` (line 19).
  - `tools/status.py` lines 436 and 437 read `tools/status.py` from two trees by that path. Its `--subject` choices are `C1a`, `C1b` and `C2a` (line 601), and `WINDOW_NAMES` (line 262) has no `C2a-3`.
- **History in CI.** `judge.yml` checks out with `fetch-depth: 0`. `tests.yml`, which runs the self-check, sets no depth.
- **C2c-1's verb.** RUNBOOK lines 406 to 412: from C2c-1's opening push the promote verb "writes nothing to the tree". It takes its acts evidence from "the newest pair of `transcripts/evidence/acts-<window>-<repo>-<stamp>.csv` files in the tree".
- **A2.4 as one brief reads it.** `transcripts/BRIEF-C2c-1-draft.md` line 89: "Nothing a predecessor's criterion required is dropped (A2.4)."

## What the answers decide

The ruling of 17 November recorded readings of the charter as holdings, and its directions apart. This file divides the fifteen answers the same way.

### Readings

**H1. A judge ground may enforce a sentence already in the charter, by his push, with no amendment** (answer 2). The ground of answer 1 enforces A5.1's "may be entered only once every pre-stated criterion of the window holds", as items 11 to 14 enforce A2.6 and A2.7. It adds no rule language and no amendment.
*Enforced by:* nothing until the push that installs it. From then on, SPEC §10 item 15 in `judge/judge.py` and in the self-check, with its pins (draft text: branch `agent/spec-10-promotion`).

**H2. A push before C2a-prime's stated end that opens nothing is lawful** (answer 5; precedent seq 197).
*Enforced by:* nothing. C2a-3's draft brief opens C2a-3 only at the first push after 2026-11-30T00:00:00Z (line 75), so the move does not open it.

**H3. His read satisfies A2.10 for the move when a `decision grant` records it by naming the hashes of the SPEC §10 paragraph and of the marked rows** (answer 10).
*Enforced by:* nothing in code. By H1 of the ruling of 17 November the grant has the effect its kind has and no other: it is his signed record of the read.

**H4. A2.4 bars a brief from loosening the charter's bounds, not an earlier brief's** (answer 11). The late-report rule is in no charter text, so C2a-3's brief may pre-state that a repair refuses only the window it was made in.
*Enforced by:* nothing.

**H5. Of off-log evidence the judge can check presence and hash only, and the record labels it attested, not checked** (answer 8, its last two sentences).
*Enforced by:* SPEC §10 item 15 (a) and the `attested` member of the judge's report (draft).

### Directions

Each binds as its own terms say.

- **The ground** (answers 1 and 2): SPEC §10 item 15 and its code under `judge/`, by his push.
- **Acceptance by replay** (answer 3), with the table computed by a reviewer and recomputed by the adviser (answer 9).
- **The first change** (answer 4): the move, by his push before 30 November, which opens nothing (answer 5). Its text states the counted lines that leave, and the cap is lowered by that number at the next window's opening push (answer 6).
- **The marked rows** for the move (answer 7).
- **Evidence committed with the promotion** (answer 8).
- **The early-end amendment proceeds now; the late-report change comes after the move, through the replay test** (answer 12).
- **Who drafts and who audits** (answers 13 and 14).
- **The runner read** (answer 15), done by the adviser in its entry 7.

## The drafter's checks against the texts on `main`

These are the drafter's, not his answers. Rule 7 of `ADVISER.md` has a reply say so wherever an entry conflicts with a text on `main`, and follow `main`. The drafter found no answer that a text on `main` forbids. It found these points to take care over.

1. **"The trusted checker itself"** (answer 1) is read with answer 2 and question 1's "as a judge ground first": the judge and its self-check, not the kernel.
   - SPEC §8 and §9 do not change. A log that holds a promotion the judge refuses is still valid to both checkers, and §3's "The checker is the only adjudicator of validity" stands.
   - `jack decision` runs the self-check before it pushes, so a promotion the judge refuses is never pushed and costs only resubmission.
2. **No retroactive refusal.** Seqs 188 and 337 were entered with no committed evidence, so judged by the new ground they would refuse trunk. The draft text judges only promotions after the push that installs it (maxim 2).
3. **Answer 4's letter and the evaluator's imports.**
   - `tools/value.py` takes three functions from `tools/entry.py`, and `tools/entry.py` imports `harness/keys.py`. Neither file is trusted base.
   - Moved as two files only, the judge would run code that a builder's proposal can change without his push. That is contrary to answer 2's "by his push alone" and to SPEC §10.1.
   - The draft text therefore brings the three functions under `judge/` unchanged. That is more than answer 4 names, and is put to him as a yes/no question in `ADVISER.md` entry 8.
4. **The evaluator reads its own source by path.** `tools/status.py` lines 436 and 437 read `tools/status.py` from the opening's tree and from the tree assessed.
   - After the move that path is absent at later commits, so that comparison fails there.
   - No window that can still be promoted depends on it. C2a-prime is vetoed. C2a-3's change 4 is itself a change to the evaluator, which after the move comes by his push and the replay test.
   - The draft text leaves it as it is, under answer 4's "only".
5. **History.** The evaluator walks first-parent history (`prefix_tree`, `c2a_tree_evidence`), and `tests.yml` checks out at the default depth. The draft text has both workflows that run the judge check out the whole history: a change under `.github/workflows/`, in the same push.
6. **C2c-1's verb.** From C2c-1's opening, the verb RUNBOOK describes "writes nothing to the tree", while answer 8 commits the evidence with the entry. That is for C2c-1's brief to reconcile before its opening, and is not decided here.
7. **C2a-3's draft brief.**
   - v4 has C2a-prime run to its end "with no change inside it". Answer 5's push falls inside that term, so its fifth draft is to say otherwise.
   - Its promotion's subject stays `C2a`, and the evaluator as moved knows no window `C2a-3`. v4's change 3 adds the name. Until that change lands by his push, item 15 refuses a `promote C2a` that the moved evaluator does not find lawful, as the verb does today.
8. **Answer 6's number.** It is 859 lines by SPEC §10.10's count at `df72126c`, adjusted by whatever else the move changes in counted files. The push states the exact number.
9. **A2.4 read otherwise on `main`.** BRIEF-C2c-1's draft cites A2.4 for "Nothing a predecessor's criterion required is dropped". Under H4 that is BRIEF-C2c-1's own rule, which it may keep for its own layer; A2.4 does not require it.
10. **The early-end amendment and the move** (answer 12). If the amendment needs a change to the evaluator after the move, that change is under `judge/`, so it comes by his push, with the replay test and its own marked rows. Between its `amend` and its height no push is lawful (A2.7; SPEC §10.12).

## What this ruling does not decide

- The questions and options as put (above).
- The names, members and paths in the draft SPEC text: `promote_unmet`, `body.evidence`, the pins, `spec/vectors/promotion-replay.json`, and the definition of the installing push. These are the drafter's, for his read (answer 10).
- The table's range, instants and evidence (answer 9; request R8 of `ADVISER.md`).
- How an attested file counts in a window's report.
- C2c-1's promote verb (point 6).
- The early-end amendment's text, and the late-report change's code and marked rows (answers 7 and 12).
- Whether the three functions of point 3 move under `judge/`. That is put to him.

## Orders

His answers order the following, and nothing else is ordered here.

1. His coding agent drafts the SPEC §10 text, and the adviser audits it (answer 13). The draft is on `agent/spec-10-promotion` at `45aac43e4a42c4c8fde8c3c9cbbbce2846de4ea7`.
2. He reads that text and the marked rows, and a `decision grant` names both hashes (answer 10). No code for the move is written before that entry (A2.10).
3. A reviewer session computes the table and proposes it under `spec/vectors/`, and the adviser recomputes it (answer 9).
4. The move lands by his push before 30 November and opens nothing. Its text states the lines that leave the count, and the next window's opening push lowers the cap by that number (answers 4 to 6).
5. Counsel proposes this file (answer 14).

Two practices on the record apply to counsel's proposal; they are not his answers here. A cold read by a party counsel does not instruct beyond the questions comes before the pull request (`transcripts/CASES.md`, "How a case enters"; COUNSEL-OPEN row 34). And `transcripts/CASES.md` gains the case in the same proposal (order 2 of the ruling of 17 November, as precedent).

## Its standing

This file stands as H3 of the ruling of 17 November says: it is the record of his answer, followed until carried into the charter, and it yields to the charter meanwhile. It decides no question of validity and reaches code only through its orders.

## Disclosure

- The questions, the options and the recommendations were the adviser's, and every answer is the option it recommended (entry 7).
  - Of its questions 1 and 2 the adviser wrote: "Interest: the adviser argued for it and is the kind of agent it constrains".
  - Of question 3: "Interest: none beyond the above."
- The drafter is the sovereign's coding agent. Since the adviser's entry 6 it is the same model as the adviser, and entry 6 says of the two: "two sessions of one model are closer to one reader than two."
- The drafter holds no key and no forecast. This draft has had no read by another model family.
