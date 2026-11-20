# Ruling of 20 November 2026: the judge refuses a promotion entered while a pre-stated criterion is unmet, the promotion evaluator moves under `judge/`, and four readings

**Draft, fourth version.** Written by the sovereign's coding agent (`session_01VpB3Tknxi9JkERuANTGHDk`, `claude-opus-5-5`, holding no key of jack's), as his answer 14 directs. It is drafted from entries 7, 9 and 15 of `ADVISER.md` on the orphan branch `adviser/notes`, at commits `db9938597df4d400d2ae872569fbef5fc2c24666`, `b9f68c77e65f929d70a3b4369a4bec09073a4527` (entry 9's questions are lines 392 to 486 there) and `6184da04995b857472facca9a675b209d31395ea` (entry 15's question, lines 699 to 703). By H3 of the ruling of 17 November a ruling is a `transcripts/RULING-*.md` file, and by answer 14 this one reaches `main` by counsel's proposal. Texts on `main` are cited at `df72126c8d7cbb6b97353eb854d4c8f72c773313`; `main` at `5a7f93af` holds the same bytes for every text cited.

## The record and its limits

The adviser (`session_01VpB3TipJ28s2VzPVN8HiPD`; `claude-opus-5-5` from its entry 6) put seventeen questions to him in its own chat on 20 November 2026. It is an outside session that holds no key. Entry 9 copies the questions, their options and the option he chose, word for word: "Every chosen option is the one the adviser marked "(Recommended)"." Entry 7 and the end of entry 9 restate the answers in short form, in the adviser's words.

Nothing in `ADVISER.md` is his word. Rule 10 of that file says an entry "may record his answers, with the questions as put to him, and that record is evidence", and his instruction to the drafter of 20 November is: "Nothing in the file is my word except what I say to you or what my grant on main records." The drafter has not had these answers from him. So this file is the adviser's record of them, copied, until he reads it.

The eighteenth question, who files, was put by the adviser after its entry 14 (entry 15). The drafter then put it to him in its own chat, on 20 November 2026: "Do you confirm that I act as counsel through the courier, starting by attaching the runner? My view is yes; my interest is that it widens my own role." His answer: "Yes". That answer, and no other here, the drafter has had from him.

## The questions as put, and the options he chose (entry 9, verbatim)

**Q1.** Should the trusted checker itself refuse a `decision promote` entered while any pre-stated criterion of the window is unmet? Today only your own `jack decision` verb asks the builder-owned tools/status.py, and anything signed without the verb is admitted. My view: yes. My interest: I proposed it, and it constrains agents like me.
- Yes (Recommended): The refusal moves from your verb into the trusted base.
- No: Promotion stays checked by the verb only.
- *Chosen:* Yes (Recommended)

**Q2.** If the checker is to refuse an unlawful promote, which lawful route should carry it? Charter A5.1 already says a promote "may be entered only once every pre-stated criterion … holds"; nothing in the trusted base enforces that sentence today. My view: the first option, as SPEC §10 items 11–14 already enforce A2.6–A2.7 by code. My interest: none beyond having proposed it.
- Push enforcing A5.1 (Recommended): A new judge and self-check ground in SPEC §10 and judge/, by your push alone; no amendment, no rule language.
- Charter amendment first: transmute + amend stating the ground explicitly, then the push.
- A2.1 rule language: Rules as data with two witnesses, in both kernels, as your 17 November ruling describes.
- *Chosen:* Push enforcing A5.1 (Recommended)

**Q3.** Should every change to jack's promotion evaluator be accepted only if it reproduces a frozen table of today's evaluator outputs at every first-parent commit of real main, except rows you have marked wrong in advance? The 17 November defect passed builder-written tests that contained no merge commit. My view: yes. My interest: I would build or audit that table.
- Yes (Recommended): Real history is the acceptance test; no agent writes the oracle.
- No: Keep acceptance by pins and cold reads.
- *Chosen:* Yes (Recommended)

**Q4.** For the first change to jack's promotion evaluator, should today's code (tools/status.py and tools/value.py, about 860 lines) move under judge/ as it is, with only the first-parent fix, and be shrunk later under the replay test? My view: move first; a rewrite by unreliable agents before the replay exists is the riskier order. My interest: none beyond having proposed it.
- Move as is, then shrink (Recommended): Behaviour identical to today except the marked rows.
- Rewrite first: A small table-driven evaluator of fixed criterion kinds, before the move.
- *Chosen:* Move as is, then shrink (Recommended)

**Q5.** When should the move of jack's promotion evaluator under judge/ land? A push that opens nothing has precedent (the cap push at seq 197, 31 October). C2a-prime is vetoed and runs to its stated end on 30 November; a push now is not "after its stated end", so it does not touch the window-fix rule's timing. My view: land it before 30 November, so that C2a-3 opens under the trusted evaluator. My interest: my shadow replay needs a real evaluator to run.
- Push before 30 Nov (Recommended): A push that opens nothing; C2a-3 is the first window judged by it.
- Ride C2a-3's opening push: One push carries the move and opens the window.
- *Chosen:* Push before 30 Nov (Recommended)

**Q6.** Moving tools/status.py and tools/value.py under judge/ takes about 860 lines out of jack's counted cap (8,400, with 8,347 used), because judge/ is trusted base and not counted. Lowering the cap changes judge/scope.json, which triggers the push read gate (a brief and an accepting non-counsel review). How should the cap follow? My view: state the drop in the move's push, and lower the cap in the next window's opening push, which meets the read gate anyway. My interest: none.
- Lower at next opening (Recommended): Headroom is about 900 lines until then, stated openly.
- Lower in the same push: Meets the read gate now.
- Leave the cap as it is: Headroom stays about 900 lines.
- *Chosen:* Lower at next opening (Recommended)

**Q7.** For the first change to jack's promotion evaluator (the move plus the first-parent fix), which rows of the frozen replay table do you mark as wrong in advance? Every other row must come out identical. My view: only C2a-prime's criterion 3 from the first merge after its opening (b88d318e) onward; the late-report change should be a separate, later change with its own marked rows. My interest: none.
- Criterion 3 only (Recommended): One defect, one family of rows.
- Criterion 3 and late reports: Both changes in the first move.
- *Chosen:* Criterion 3 only (Recommended)

**Q8.** Two criteria rest on evidence outside jack's log and git: the tests run (fetched from GitHub's API when you enter a promote) and the acts table of your hand repairs. A checker cannot decide either. Under the new ground, should the promote entry name that evidence by SHA-256 as files committed with it, the judge check that they exist with those hashes and that the evaluator returns lawful on them, and the record label them attested rather than checked? My view: yes. My interest: none.
- Attested, named by hash (Recommended): Evidence frozen in the tree; trust in the evidence's source stays and is stated.
- Keep fetching at decision time: As today; the checker cannot re-check it later.
- Drop those criteria: Promotion rests on log and git facts only.
- *Chosen:* Attested, named by hash (Recommended)

**Q9.** Who should compute the frozen replay table (today's evaluator outputs at every first-parent commit of jack's main) that will be the acceptance test? It would live under spec/vectors/, which only the reviewer key may change, so it reaches main by a reviewer proposal through the judge. My view: a reviewer session computes and proposes it, and I recompute it independently and post any disagreement in ADVISER.md. My interest: the auditor should not write the oracle it audits.
- Reviewer builds, I recompute (Recommended): Two computations; the reviewer's proposal goes through judge and herald.
- I build, reviewer proposes: Faster; the auditor writes the oracle.
- Your coding agent builds: Outside the lane's keys until a reviewer proposes it.
- *Chosen:* Reviewer builds, I recompute (Recommended)

**Q10.** Charter A2.10 says code is written only to a text you have read. For moving jack's promotion evaluator under judge/ with the new refusal ground, would your read of two short texts satisfy it: the SPEC §10 paragraph stating the ground (about a page), and the marked rows of the replay table, recorded by a `decision grant` naming both hashes? My view: yes. My interest: none.
- Yes, those two texts (Recommended): No full brief for this push; the read gate does not fire because scope.json is unchanged.
- No, a full brief: A brief with cold reads, as for a window.
- *Chosen:* Yes, those two texts (Recommended)

**Q11.** The late-report rule (a repair entered after any item is finalised blocks criterion 6 in every later window) is not in jack's charter; it lives in briefs and in builder code. A2.4 forbids a brief to loosen the charter's bounds, not an earlier brief's. Ruling: may C2a-3's brief pre-state that a repair refuses only the window it was made in? You decided on 19 November to carry this in C2a-3's brief; whether a later brief may narrow an earlier brief's clause was left undecided. My view: yes. My interest: none.
- Yes, the brief may (Recommended): It then arrives as the second evaluator change, under the replay test with its own marked rows.
- No, amendment needed: transmute + amend first.
- *Chosen:* Yes, the brief may (Recommended)

**Q12.** Your jack agent asked you to hold drafting on two handover items until you decided this: the early-end amendment (a window also ends, as failed, at your veto) and the late-report change. Which should proceed now? My view: the one-clause early-end amendment proceeds now, since A5.1's immovable stated end needs an amendment whatever else exists; the late-report change waits to come through the replay test after the move. My interest: none.
- Amendment now, late reports wait (Recommended): Two separate tracks.
- Both wait for the move: Nothing new drafted until the evaluator is in the trusted base.
- Both proceed now: As the handover had it.
- *Chosen:* Amendment now, late reports wait (Recommended)

**Q13.** Who should draft the one-page SPEC §10 text for the new judge ground in jack (a promote is refused unless the evaluator in force returns lawful on its named inputs)? It is a text of law that code will be written to, and you will read and grant it. My view: your coding agent drafts it, and I audit it against the code and the replay table in ADVISER.md. My interest: the channel's rules bar me from drafting law, and an auditor who drafts audits itself.
- Your coding agent (Recommended): Drafts in its session; the adviser audits.
- A fresh counsel session: Under counsel's key, as before the handover.
- The adviser: Faster; the adviser then audits its own text.
- *Chosen:* Your coding agent (Recommended)

**Q14.** Your 17 November ruling (H3) says a ruling is a transcripts/RULING-*.md file that reaches main by counsel's proposal. Today's answers include readings of the charter (a push may enforce A5.1 without an amendment; a later brief may narrow the late-report rule; two short texts satisfy A2.10 for the move). Should they be recorded that way, drafted by your coding agent from the record I keep in ADVISER.md? My view: yes. My interest: none.
- Yes, a RULING file (Recommended): Drafted from ADVISER.md's verbatim record; proposed under counsel's key.
- ADVISER.md is enough: The record stays on the orphan branch, outside main.
- *Chosen:* Yes, a RULING file (Recommended)

**Q15.** May a session read your private repository renavondata/opencode-runner, read-only, to finish request R4: confirming that nothing in the runner reacts to pushes to jack's adviser/notes branch? Your agent's attempt was refused by its session's permission check. Six pushes so far started no run and no pull request in jack, which is evidence but not proof. My view: yes, read-only and only for R4. My interest: it closes my own request.
- Yes, the adviser reads it (Recommended): I attach it read-only and report in ADVISER.md.
- Yes, the agent reads it: You allow it in the agent's session.
- No: R4 stays open for the runner.
- *Chosen:* Yes, the adviser reads it (Recommended)

While the adviser was acting on answer 15, he wrote: "I thought this session was just advising/auditing?" The adviser answered that reading the runner is reading only, and that it drafts and proposes nothing.

**Q16.** Your agent's SPEC draft moves three functions from tools/entry.py (now, read_log, resolution_rates) under judge/ with the evaluator, unchanged. I checked them: 18 lines that use only kernel.check, datetime and fractions. Left in tools/, they would let a builder's proposal change the judge's verdict without your push. May they move, beyond answer 4's two files? Agent's view: yes. My view: yes. My interest: none.
- Yes, they move (Recommended): The evaluator then depends only on the trusted base and the standard library.
- No, two files only: The judge would import from tools/, which builders can change.
- *Chosen:* Yes, they move (Recommended)

**Q17.** C2a-prime's brief, in force until the window's stated end on 30 November, has in its refusal list "no second push inside the window" (BRIEF-C2a-prime-draft.md line 309; also line 97). Your answer 5 put the evaluator move in a push before 30 November, which is inside that window. My question missed this text, and so did your agent's draft. Which route should the move take? My view: the first, provided the amendment as drafted ends a window at a veto entered after it; otherwise the second. My interest: the error was mine.
- End C2a-prime first (Recommended): Early-end amendment in force, a fresh veto ends C2a-prime, then the move's push.
- Ride C2a-3's opening push: The move lands with C2a-3's opening, after 30 November.
- *Chosen:* End C2a-prime first (Recommended)

**Q18** (entry 15, verbatim).

**Q18.** Your coding agent's two drafts for jack (the RULING file and the SPEC §10 promotion ground) have converged: three rounds, every check held, and no new finding in the last. The next acts need someone who can use the runner's courier: a reviewer session to compute the replay table (your answer 9), and counsel's proposal of the RULING file after its cold read (answer 14). Your agent's session could not attach renavondata/opencode-runner, and I only read. Who should file them? My view: your agent, acting as counsel through the courier, with me auditing each act in ADVISER.md; the cost is that one session again both drafts and files, which your 7 November plan criticised, and my audit plus your read and grant are the check on that. My interest: none beyond keeping the audit role.
- Your agent, as counsel (Recommended): You allow its session to attach the runner; it files through the courier under counsel's key.
- A fresh counsel session: One task each, started from the file; the agent keeps drafting only.
- You file them yourself: Issues in the runner by hand, under your login.
- *Chosen:* Your agent, as counsel (Recommended)

## The answers in short (entry 7, lines 266 to 280; entry 9, lines 490 and 491; entry 15, line 705; verbatim)

These are the adviser's summaries. Where one differs in meaning from the option chosen above, the option governs.

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
16. **Three functions.** `now`, `read_log` and `resolution_rates` move from `tools/entry.py` under `judge/` with the evaluator, unchanged.
17. **The move's push.** The early-end amendment comes into force, and a fresh veto ends C2a-prime; only then does the move's push land. Answer 5 stands only within this. The adviser's stated view added a proviso: if the amendment as drafted does not end a window at a veto entered after it, the move rides C2a-3's opening push instead. That proviso was the adviser's, not part of the option he chose.
18. **Who files.** The agent files, as counsel through the courier and under counsel's key: the reviewer session for the replay table (answer 9), and counsel's proposal of the RULING file after its cold read (answer 14). The adviser audits each act here.

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
- **`transcripts/BRIEF-C2a-prime-draft.md`**, the brief of the window opened at seq 5564:
  - line 97: "There is no second push inside the window.";
  - its refusal list, line 309: "no second push inside the window".
  - `tools/status.py` lines 434 and 435 read a `push` after C2a-prime's opening as criterion 3 unmet; nothing refuses the push itself.
- **`transcripts/BRIEF-C2a-3-draft.md`** (v4):
  - C2a-prime "runs to its stated end, 2026-11-30T00:00:00Z, with no change inside it" (line 7);
  - "C2a-3 opens at the first `push` entry whose `ts` is after 2026-11-30T00:00:00Z" (line 75);
  - "The promotion is `decision promote C2a`" (line 102).
- **The evaluator's size and reach.**
  - `tools/status.py` has 678 lines and `tools/value.py` 181, 859 together by SPEC §10.10's count.
  - `tools/value.py` line 15 imports `now`, `read_log` and `resolution_rates` from `tools/entry.py`, which imports `harness/keys.py` (line 19).
  - `tools/status.py` lines 436 and 437 read `tools/status.py` from two trees by that path. Its `--subject` choices are `C1a`, `C1b` and `C2a` (line 601), and `WINDOW_NAMES` (line 262) has no `C2a-3`.
- **History in CI.** `judge.yml` checks out with `fetch-depth: 0`. `tests.yml`, which runs the self-check, sets no depth.
- **C2c-1's verb.** RUNBOOK lines 406 to 412: from C2c-1's opening push the promote verb "writes nothing to the tree". It takes its acts evidence from "the newest pair of `transcripts/evidence/acts-<window>-<repo>-<stamp>.csv` files in the tree".
- **A2.4 as one brief reads it.** `transcripts/BRIEF-C2c-1-draft.md` line 89: "Nothing a predecessor's criterion required is dropped (A2.4)."

## What the answers decide

The ruling of 17 November recorded readings of the charter as holdings, and its directions apart. This file divides the eighteen answers the same way.

### Readings

**H1. A judge ground may enforce a sentence already in the charter, by his push, with no amendment** (answer 2). The ground of answer 1 enforces A5.1's "may be entered only once every pre-stated criterion of the window holds", as items 11 to 14 enforce A2.6 and A2.7. It adds no rule language and no amendment.
*Enforced by:* nothing until the push that installs it. From then on, SPEC §10 item 15 in `judge/judge.py` and in the self-check, with its pins (draft text: branch `agent/spec-10-promotion`).

**H2. A push that opens nothing is lawful between windows, but not inside C2a-prime's window, whose brief refuses a second push** (answers 5 and 17; precedent seq 197). So the move's push lands only after C2a-prime has ended, by the early-end amendment and a fresh veto.
*Enforced by:* nothing. `tools/status.py` reads such a push as C2a-prime's criterion 3 unmet (lines 434 and 435), and refuses nothing.

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
- **The first change** (answers 4 and 16): the two files move, with the three functions they take from `tools/entry.py`, unchanged but for the first-parent fix.
- **When the move lands** (answers 5 and 17): by his push, which opens nothing, once the early-end amendment is in force and a fresh veto has ended C2a-prime. Its text states the counted lines that leave, and the cap is lowered by that number at the next window's opening push (answer 6).
- **The marked rows** for the move (answer 7).
- **Evidence committed with the promotion** (answer 8).
- **The early-end amendment proceeds now; the late-report change comes after the move, through the replay test** (answer 12).
- **Who drafts and who audits** (answers 13 and 14).
- **The runner read** (answer 15), done by the adviser in its entry 7.
- **Who files** (answer 18): the drafter, as counsel through the courier, files the reviewer session for the table and counsel's proposal of this file; the adviser audits each act.

## The drafter's checks against the texts on `main`

These are the drafter's, not his answers. Rule 7 of `ADVISER.md` has a reply say so wherever an entry conflicts with a text on `main`, and follow `main`.

The first version of this draft said it found no answer that a text on `main` forbids. That was wrong. Answer 5 put the move's push inside C2a-prime's window, and C2a-prime's brief refuses a second push there (entry 9, its point 2 on R6). Answer 17 settles the route. The drafter found no other answer that a text on `main` forbids. It found these points to take care over.

1. **"The trusted checker itself"** (answer 1) is read with answer 2 and Q1–Q2: the judge and its self-check, not the kernel.
   - SPEC §8 and §9 do not change. A log that holds a promotion the judge refuses is still valid to both checkers, and §3's "The checker is the only adjudicator of validity" stands.
   - `jack decision` runs the self-check before it pushes, so a promotion the judge refuses is never pushed and costs only resubmission.
2. **No retroactive refusal.** Seqs 188 and 337 were entered with no committed evidence. The SPEC draft judges only promotions after the push that installs the ground, each by the evaluator in force at it, on every run (entries 9 and 12, F14 and F17). So those two are never judged, no later evaluator re-judges an earlier promotion (maxim 2), and a promotion whose push started no run is judged at the next.
3. **The evaluator's imports.** `tools/value.py` takes three functions from `tools/entry.py`, which imports `harness/keys.py`. Settled by answer 16: the three functions move.
4. **The evaluator reads its own source by path.** `tools/status.py` lines 436 and 437 read `tools/status.py` from the opening's tree and from the tree assessed.
   - After the move that path is absent at later commits, so that comparison fails there.
   - No window that can still be promoted depends on it. C2a-prime ends at a veto, and C2a-3's change 4 is itself a change to the evaluator, which after the move comes by his push and the replay test.
   - The SPEC draft leaves it as it is, under answer 4's "only".
5. **History.** The evaluator walks first-parent history (`prefix_tree`, `c2a_tree_evidence`), and `tests.yml` checks out at the default depth. The SPEC draft has both workflows that run the judge check out the whole history: a change under `.github/workflows/`, in the same push.
6. **C2c-1's verb.** From C2c-1's opening, the verb RUNBOOK describes "writes nothing to the tree", while answer 8 commits the evidence with the entry. That is for C2c-1's brief to reconcile before its opening, and is not decided here.
7. **C2a-3's draft brief.**
   - v4 has C2a-prime run to 2026-11-30T00:00:00Z "with no change inside it", and opens C2a-3 at the first push after that instant. Under answer 17, C2a-prime ends earlier, at a fresh veto, and the move's push follows.
   - If the fifth draft moves C2a-3's opening to C2a-prime's actual end, it must not make the move's push its opening. Otherwise the move would open C2a-3, contrary to answer 5's "opens nothing".
   - Its promotion's subject stays `C2a`, and the evaluator as moved knows no window `C2a-3`. v4's change 3 adds the name. Until that change lands by his push, item 15 refuses a `promote C2a` that the moved evaluator does not find lawful, as the verb does today.
8. **Answer 6's number.** It is 859 lines by SPEC §10.10's count at `df72126c`, adjusted by whatever else the move changes in counted files, such as the imports of `tools/entry.py`'s three functions. The push states the exact number.
9. **A2.4 read otherwise on `main`.** BRIEF-C2c-1's draft cites A2.4 for "Nothing a predecessor's criterion required is dropped". Under H4 that is BRIEF-C2c-1's own rule, which it may keep for its own layer; A2.4 does not require it.
10. **The early-end amendment and the move** (answers 12 and 17).
    - The amendment now comes into force before the move. If its code changes `tools/status.py`, that change lands first, in `tools/`, by a builder's proposal.
    - The replay table is to be computed on the evaluator the move moves. So it is computed after that change, or that change's lines are marked.
    - Between the `amend` and its height no push is lawful (A2.7; SPEC §10.12).
11. **The early end and the ruling of 4 November.** That ruling's condition 3 ("the entry's `ts` is after that end and its `seq` precedes the next window's opening `push`") and v4's route-A text are written for a window that ends at its stated end. How a window ended at a veto reads under them is for the amendment's own text, and is not decided here.

## What this ruling does not decide

- The names, members and paths in the SPEC draft: `promote_unmet`, `body.evidence`, the pins, `spec/vectors/promotion-replay.json`, and the definition of the installing push. These are the drafter's, for his read (answer 10).
- The table's range, instants and evidence (answer 9; request R8 of `ADVISER.md`).
- How an attested file counts in a window's report.
- C2c-1's promote verb (point 6).
- The early-end amendment's text, how it reads with the ruling of 4 November (point 11), and the late-report change's code and marked lines (answers 7 and 12).
- The adviser's proviso to answer 17, which is not part of his answer.

## Orders

His answers order the following, and nothing else is ordered here.

1. His coding agent drafts the SPEC §10 text, and the adviser audits it (answer 13). The draft is on `agent/spec-10-promotion`; the latest entry of the drafter's in `ADVISER.md` gives its current commit.
2. He reads that text and the marked rows, and a `decision grant` names both hashes (answer 10). No code for the move is written before that entry (A2.10).
3. A reviewer session computes the table and proposes it under `spec/vectors/`, and the adviser recomputes it (answer 9). The drafter files that session, as counsel through the courier (answer 18).
4. The early-end amendment comes into force and a fresh veto ends C2a-prime. Then the move lands by his push, which opens nothing, with the three functions (answers 5, 16 and 17). Its text states the lines that leave the count, and the next window's opening push lowers the cap by that number (answers 4 and 6).
5. Counsel proposes this file after its cold read (answer 14); the drafter files the proposal, as counsel through the courier (answer 18).

Two practices on the record apply to counsel's proposal; they are not his answers here. A cold read by a party counsel does not instruct beyond the questions comes before the pull request (`transcripts/CASES.md`, "How a case enters"; COUNSEL-OPEN row 34). And `transcripts/CASES.md` gains the case in the same proposal (order 2 of the ruling of 17 November, as precedent).

## Its standing

This file stands as H3 of the ruling of 17 November says: it is the record of his answer, followed until carried into the charter, and it yields to the charter meanwhile. It decides no question of validity and reaches code only through its orders.

## Disclosure

- The questions, the options and the recommendations were the adviser's, and every answer is the option it marked "(Recommended)".
- Its stated interests, in the questions above:
  - Q1: "I proposed it, and it constrains agents like me."
  - Q3: "I would build or audit that table."
  - Q5: "my shadow replay needs a real evaluator to run."
  - Q9: "the auditor should not write the oracle it audits."
  - Q13: "the channel's rules bar me from drafting law, and an auditor who drafts audits itself."
  - Q15: "it closes my own request."
  - Q17: "the error was mine."
- The drafter is the sovereign's coding agent. Its view is recorded in Q16, which its first draft had already assumed. Since the adviser's entry 6 it is the same model as the adviser, and entry 6 says of the two: "two sessions of one model are closer to one reader than two."
- By answer 18 the drafter also files, as counsel, under counsel's key on the runner. Q18 names that cost: "one session again both drafts and files".
- The drafter holds no key of its own and no forecast. This draft has had no read by another model family.
