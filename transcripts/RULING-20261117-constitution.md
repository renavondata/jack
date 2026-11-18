# Ruling of 17 November 2026: what a `decision` can do, the last word at a pre-stated gate, where a ruling is recorded, and whether seq 3432 is A2.1's first real case

Put to Guy by counsel (`counsel-5`, `claude-fable-5-2`) in `transcripts/QUESTION-20261111-constitution.md` (the paper; proposed at seq 3515, merged at seq 3516, jack #782), whose §5 asks seven answers. Four of the seven ask, in whole or in part, a **reading**: his ruling on what the charter as it stands allows (A2.10). This file records those four readings and his answer to them. The paper's directions and its amendment material are not rulings, and this file records them only as things it does not decide.

## The questions

1. **Dispensation** (the paper's §2.1; answer 1). Can a `decision` suspend a rule for a case, or make a past breach lawful? And what, on the answer, is the effect of the entry at seq 3432?
2. **The last word** (§2.3; answer 3). When a reader's finding blocks an opening push whose gate a brief has pre-stated, does a `decision` of the sovereign's dispose of the finding?
3. **The record** (§2.4; answer 4). Where is a ruling recorded, and how does it stand against the charter until an amendment carries it?
4. **A2.1's first real case** (§3; answer 6). Is seq 3432 "the first entry Guy wants refused that recognition does not refuse"?

## The facts on the record

- **A2.10**: "Code is written to a text Guy has read; questions of what the charter allows are put to Guy as rulings and recorded here."
- **A2.7**, "Amendment is two acts and a wait": "A `decision` of kind `transmute` names the amendment; the `amend` follows and is in force from its `activate_at`, never before, and never over earlier entries (§3: the law looks forward)."
- **A2.4**: a layer's brief "may tighten the charter's bounds, never loosen them".
- **A2.6**: "Veto, promotion, budget, grant, transmutation and the fix of a failed window are `decision` entries signed by a key declared in genesis (§10.14)."
- **A2.1**: the law language "enters at the layer in which the first real case arises: the first entry Guy wants refused that recognition does not refuse. Until then no primary rule exists, and no layer is required to build the language in advance of it. Each layer's report states whether a case arose."
- **§3, Change**: "A rule enters or leaves only by a change entry signed by a key holding the change power (at genesis, Guy's alone). It binds from the next entry."
- **§2, maxim 1**: "No one judges their own cause". **Maxim 4**: "Reversible acts are priced and scored, never blocked. Hard gates stand only before effects that cannot be undone".
- **SPEC §5**: a `decision`'s `kind` is "one of `veto promote budget grant transmute fix`", and its `subject` a "non-empty string (for `transmute`, the `id` of the amendment it unlocks)".
- **SPEC §8, step 9**: "for `decision` of kind `transmute`, its `subject` joins the transmuted set"; and "`proposal`, `merge`, `spec_conflict` and the other decisions have no effect on the state beyond the head hash and the previous `ts`."
- **`tools/jack`, `push_read_gate`** (the gate of `jack push --opens`): it reads the brief, the review files on `origin/main` and the `proposal` entries that brought them, and it passes on the first review that is accepting, at `main`'s bytes of the brief, and brought by a principal other than counsel. It reads no `decision`, counts no families, and a failing review beside an accepting one refuses nothing in it. Pins `push_without_read_refused`, `read_of_this_text`, `read_not_counsels`.
- **The case.** On 4 November window code was written before the sovereign had read its text. On 11 November he entered seq 3432, a `decision` of kind `grant`, whose subject says, among other things: "a breach of A2.10. The breach stands, listed. The re-cut made after my read and what was built on it (commits 05dfceee, 1c1b27f8, bfd685ea, a17864cc on opening-c2a-prime) may enter by the opening push of C2a-prime. This is no precedent for building before a read. The eight obligations under What the pins do not enforce stand for this window as obligations enforced by hand and reported in the C2a report. Gate read findings on these two grounds (opencode-runner 638, 656, 666) are answered by this entry." A gate read at those bytes then failed the brief (runner #669, F1): "Code was written before the sovereign read its operative text, contrary to A2.10; a later grant cannot loosen the charter". Put the listed breach against a rebuild, he chose the rebuild: "Yes, b, that's the price." (COUNSEL-OPEN row 54). The code was written again after his read (rows 56 and 57).
- **Rulings so far.** `transcripts/CASES.md`: "where a judgment and the charter differ, the charter's text stands, since it changes only by amendment (A2.7)"; "No text ranks a ruling before it is recorded"; "Rulings are not entries on the log". Correction 4 of `transcripts/RULING-20261104-window-fix.md`: "Until then this judgment is the record of Guy's answer, and his direction ("so it becomes case law") is that it be followed. No text ranks a ruling or says how one is displaced. It decides no question of validity (§3), and reaches code only through its orders."
- **The openings.** C2a-prime was opened by the `push` at seq 5564 (2026-11-17T12:50:50Z), before the answer recorded here. C2b has not been opened: no `push` follows seq 5564 on `main` at `19b7726f`.

## Options as put

The paper sets each option against the charter in a table: §2.1 (a to d), §2.3 (a to d), §2.4 (a to d), and for the fourth question the two readings of §3's paragraph on A2.1. Those tables are the options as he had them and are not repeated here. Counsel's recommendations were: §2.1 a; §2.3 a for the openings of C2a-prime and C2b; §2.4 b now; and that seq 3432 is not a first real case.

## The ruling

Guy, 17 November 2026, at about 22:00Z, in conversation: "Then indeed, yes to all 7 questions".

He had asked counsel the same day: "What's your advice on the 7 questions?" Counsel advised yes to all seven as the paper puts them, with one departure on answer 7 (below, under what this ruling does not decide), and gave no advice on answer 3, where it holds an interest. Counsel read his answer back to him at once and he has not corrected the reading. The exchange is recorded in COUNSEL-OPEN row 70.

The four readings he answered yes to, in the paper's words (§5):

1. "R: §2.1 a, with its reading of seq 3432."
2. "R: no `decision` disposes of a reviewer's finding, and a pre-stated gate binds until its own terms are met; so §2.3 a for the two openings."
3. "R: a ruling is a `RULING-*.md` file, the record of his answer, followed until carried into the charter, and yielding to the charter meanwhile."
4. "R: seq 3432 is not A2.1's first real case, because he does not want it refused."

**The holdings.** None is decidable as put: the paper says of its seven answers that "readings and directions are prose", and that their decidable forms are C2c-2's texts. Each holding below says what code holds of it today.

**H1. Dispensation.** §2.1 a: "A `decision` has the effect the law in force gives its kind, and no other. What else it says is his signed statement: evidence of a fact, or of a choice he makes within powers he otherwise has". No `decision` suspends a rule for a case or makes a past breach lawful.

Of seq 3432, in the paper's words:

> it is a valid entry. Its words on his read, on the breach, that the breach stands listed, that it is no precedent and that the eight obligations stand are his signed statements — evidence, and no exercise of a power. "May enter by the opening push" and "are answered by this entry" have no effect in law: no kind of `decision` admits code or disposes of another party's finding. Nothing is struck from the log

*Enforced by:* no pin of its own. Both checkers implement SPEC §8 step 9, under which no `decision` but a `transmute` has an effect on the state "beyond the head hash and the previous `ts`". The judge refuses when trunk's trusted-base digest is not the trusted base in force at the end of trunk's log (SPEC §10.11), which §7 defines as "the `digest` of the latest valid `push` entry, or genesis's `checker` if there is none"; it also refuses an `amend` that no `transmute` names (§10.13). `push_read_gate` reads no `decision`. What a `decision`'s prose claims beyond that is read by people, and this holding is how they read it.

**H2. The last word at a pre-stated gate.** No `decision` disposes of a reader's finding. A gate that a brief pre-stated for an opening binds until its own terms are met. For the openings of C2a-prime and C2b that is §2.3 a: "The gate as pre-stated: a BLOCK bars the opening until two families accept".

*Enforced by:* in part. `push_read_gate`, with the three pins named above, refuses an opening whose brief has no accepting review at `main`'s bytes brought by a principal other than counsel, and it reads no `decision`. It does not hold the rest of the gate: it passes on the first such review, so that a BLOCK bars the opening until two families accept is each brief's rule and its reply file's, kept by hand. The gate's terms are each brief's own, and this ruling restates none of them.

**H3. The record of a ruling.** A ruling is a `transcripts/RULING-*.md` file, the record of his answer. It is followed until it is carried into the charter, and it yields to the charter meanwhile.

*Enforced by:* nothing. The file reaches `main` by counsel's proposal, as this one does.

**H4. Seq 3432 and A2.1.** Seq 3432 is not A2.1's first real case: he does not want it refused.

*Enforced by:* nothing, and nothing could: A2.1 turns on what he wants refused.

## Reasoning

The reasons are the paper's, which he had before him; nothing is added to them here.

1. **H1 is the law as it stands** (§2.1). "SPEC §8 gives no `decision` but `transmute` an effect on the state; the charter changes only by A2.7's path; no clause gives any entry a power to suspend a rule or to make a past breach lawful". (SPEC §8's own words except the head hash and the previous `ts`, which every entry moves.) It is "the only reading that can later bind an agent with no back door", and A2.10 ends: "nothing is imposed on the agent that was not first imposed on us." Its price is stated: "a true emergency waits for A2.7's two acts".
2. **The other options are not open as readings** (§2.1). A waiver power granted in advance (b) is open "Only by amendment, for the future". An amendment that makes the writing of 4 November lawful (c) is barred by A2.7's "never over earlier entries". "Met in substance" (d) "is the dispensing power", and A2.4 does not let a brief loosen.
3. **Seq 3432 loses nothing it could have had** (§2.1). Its statements stand as his signed evidence. The two clauses that claim an effect claim one no kind of `decision` has. His choice of 11 November, the rebuild, had already made the first of them moot.
4. **H2: the gate is the brief's own rule** (§2.3). The paper: "it is the brief's own pre-stated rule, and nothing changes it for a window it already governs". That his reasoned decision should dispose of a BLOCK (b) fails twice: "no kind of `decision` has that effect (SPEC §8), and on his own compliance maxim 1 forbids it". A hard gate is in place at an opening because "an opening push is not cheaply undone, so maxim 4 allows a hard gate there". The price is stated: "a model's reading of a fixed text is unstable", "so the gate may not converge".
5. **H3 is what is done already** (§2.4). It "is correction 4 of the ruling of 4 November". A2.10 has rulings "recorded here", in the charter, which changes only by A2.7's path; until an amendment carries a ruling, the file is the record and the charter's text governs where they differ. The price is stated: "it binds nothing by its own words", and "counsel's key carries it to `main`".
6. **H4 follows from H1 and from his answer** (§3). A2.1 asks what he wants refused, "and only he can answer". By H1 seq 3432 "is a valid entry whose surplus words have no effect, and an entry of no effect needs no refusing". Had he answered that he wants such entries refused, "then on A2.1's words the rule language enters at this layer, with its cost in kernel lines and a push."

## What this ruling does not decide

- **The directions** he answered yes to (answers 2, 5 and 6, and the direction halves of 3 and 4): every brief from now on names what follows the breach of each obligation it leaves to hand, and where it names nothing else, §2.2 b ("The product does not enter; the work is done again after the cure"); from C2c-2 a BLOCK suspends and he rules, the reader scored on his ruling (his words of 11 November, row 57: "Yes, I end disagreements"); from C2c-2 each ruling is signed by a `wish`; counsel and every brief from now on take scope b, his read as an entry naming bytes, and the prefix rule, and counsel files no session without such an entry, and, as a deliverable apart from counsel's own practice, "C2c-2's texts put the check at the push" (the paper's answer 5); the ladder, tamper-evidence as the monitor's aim, and no emergency path. A direction "binds no party until a brief he has read pre-states it for its layer" (the paper's head). They go into C2c-2's texts, each read by him before any build.
- **Whose ground it is when the finding is about his own compliance.** The paper's §2.3 c leaves it to "a decidable check", or the ground stands. That is part of the direction and of C2c-2's brief.
- **The amendment material**: the principle's two halves, with §2.2 b as the charter's default; the rank of a ruling against a brief and against code, its displacement by name, and codify-or-lapse; the scope of the read, the entry naming bytes and the prefix rule as charter text; and the carrying of these four readings into the charter, as A2.10 requires. The paper's answer 7 asked for "one amendment for C2c-2's boundary". Counsel advised otherwise before he answered, and read his answer back to him so: "For the amendment part of point 7 I follow your decision of today and rows 28 and 33: separate clauses at C2c-3, each only after its rule has lived in a brief." No amendment is made or drafted by this file.
- **A waiver power** (§2.1 b). Not asked. It could come only by amendment.
- **The scope of A2.10.** The paper: "No reading of A2.10 is asked."
- **Whether any gate's terms were met** at seq 5564 or will be at C2b's opening, and anything about C2a-prime's criteria (COUNSEL-OPEN row 69).
- **Whether any other entry is A2.1's first real case.** Each layer's report says whether one arose.

## Orders

1. This file is read cold before it is proposed, by a reader counsel does not instruct beyond the questions (the paper's answer 7; COUNSEL-OPEN row 34).
2. `transcripts/CASES.md` gains this case under "Cases in force", in the same proposal.
3. Counsel's report on C2a states, under A2.1, that seq 3432 was put to him as a candidate first real case and that he answered it is not one.
4. Counsel carries the directions into C2c-2's texts (the SPEC patch, the monitor text, a custody text, the brief). No builder session is filed for any of them before his read of it (A2.10).
5. Counsel offers no option, and drafts no entry for him, that rests on a `decision` doing what H1 says it cannot.

## Its standing as precedent

It stands as H3 says: this file is the record of his answer; it is followed by counsel, builders and reviewers until an amendment carries it into the charter; where it and the charter's text differ, the charter's text governs. It interprets the charter and changes none of its words. It decides no question of validity and reaches code only through its orders. The amendment that carries it is for C2c-3's procedure (COUNSEL-OPEN rows 28 and 33).

## Disclosure

The recommendations were counsel's, in the paper. Counsel's interests, as the paper and row 55 state them: counsel-5 held forecasts (V5 to V7) that needed C2a-prime to open, and its predecessor drafted the text of seq 3432, two of whose clauses H1 finds to have no effect; both interests ran against the recommendations. The paper printed counsel's probabilities for his answers; they are in its text and in no entry of the log, and the sovereign has since directed that counsel give no forecast outside the law (row 68). On answer 3 counsel gave no advice on 17 November: the direction lowers a bar that readers set on counsel's own texts. H2 is not that direction. It keeps the higher bar, and counsel had acted on it since 11 November.
