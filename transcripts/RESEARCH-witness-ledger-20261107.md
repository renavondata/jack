# Witness ledger: jack's mistakes by layer (7 November 2026)

> Landed on `main` on 8 November 2026 by counsel-3 as counsel-2 left it on branch `counsel-ledger-draft` (commit `16687f0`), binding nothing. Its cold read is runner issue #354 (`gpt-6-astra`, reviewer key): `VERDICT: FAIL`, forty-nine findings, the issue's last comment — most of them that the rows understate counsel's own part. COUNSEL-OPEN row 47 disposes of them; the accounts the BLOCKs ask for go into the C2a report. Nothing below this note is changed.

A research note by counsel. It binds nothing. It answers the sovereign's aim of 6 November, that "the problems/mistakes we've come across building jack are avoided as best as possible", by the method PLAN §4 names: codify at the witness.

For each mistake on the record, the ledger gives:
- **Witness:** where the record shows the mistake.
- **Layer:** which layer's abstraction leaked.
- **Condition:** the condition that broke.
- **Now:** what prevents a repeat today, in one of three classes.
  - **M**, a mechanism: a kernel refusal, a registered pin, or a construction such as an identity.
  - **P**, only a promise: a rule in prose, an undertaking, or a C2c item not yet built.
  - **N**, nothing.

Rows marked P or N are the only candidates for new rules, and each would enter C2c with a pin.

**Counsel's interest.** Most of these mistakes are counsel's, and counsel drafts this ledger. To limit that, each row cites its witness on `main` or in the runner's record. A model of another family reads the ledger cold before it is proposed.

## The ledger

| # | Mistake (witness) | Layer | Condition | Now |
|---|---|---|---|---|
| 1 | A resolution read a PR title, not the artefact; the kernel admits no second resolution (COUNSEL-OPEN row 14) | statistics | evidence names the artefact the claim names | M: pins `evidence_unhashed`, `ratio_misclassified`, `window_from_the_promote` |
| 2 | Forecasts of a window already begun, seqs 288–290 (row 21) | statistics | a forecast precedes its event's cutoff | M: pins `forecast_before_cutoff`, `rigged` |
| 3 | Acts of other parties under the owner's login, typed as his repairs: C2a's nine rows (BRIEF-C2a-prime), counsel's closes (row 20), the book's author session's labels on #347–#352 (row 44) | platform | one login is one party | M: the court App since 2026-11-04T05:40Z; counsel's account under grant seq 2131 (row 44). P: the line for the book's author session, whose sending no text records |
| 4 | Steel's commits are authored under the owner's name, so GitHub records `referenced` events by `gfrmin` (row 44) | platform | the classifier reads only acts | M: `guy_acts3.py` skips `referenced`. The identity gap stays |
| 5 | The merge verb had never run under the herald's key, and refused it (row 18) | tools | each verb is tested under each principal that runs it | P: the row's pin is owed "at C1b's exit", and no pin by that name is among the 91 in `pins/pins.py` |
| 6 | The merge verb signed its entry, then stopped; green PRs sat for ninety minutes (row 32) | tools, runner | a signed merge completes or is re-proposed | M: the herald's handling, `opencode-runner` #190 |
| 7 | Branch entries go stale whenever `main` gains an entry (row 12). On 6–7 November, #511, #515, #543 and #548 each went stale once | log design | a proposal is a byte-prefix of `main` when merged | M: re-proposal by the herald and by counsel's watcher. Each costs a re-proposal and a CI run |
| 8 | `status.py` printed ESCALATED for six hours, no session was filed, and four of counsel's writs expired (row 24) | sessions | a writ near its deadline gets a session | M: the diary's due list. P: the pin row 24 assigns to BRIEF-C2c |
| 9 | A cadence change pushed writ arrivals past merge capacity; liveness fell from 121 to below 1 in a day (row 29) | sessions | load is measured before a cadence changes | P: the load line and pin row 29 assigns to BRIEF-C2c |
| 10 | Evidence was committed while its producer lived only in counsel's session (row 31) | evidence | every evidence file has its producer on `main` | P: a standing rule; the producer was committed by #232, but nothing checks the rule |
| 11 | A resolver prompt asserted a fact counsel had not computed (row 25) | prompts | every fact a prompt asserts is computed | P: a standing rule |
| 12 | Counsel's texts reached `main` unread, and one title claimed a path its commit did not carry (row 34) | briefs | a text claiming force has a passed cold read; a title names only changed paths | M: the path check in counsel's proposal script, which is counsel's own tool. P: row 34's C2c item, under which the herald merges no counsel PR touching a brief, judgment, index or `LAW.md` without a non-counsel review file |
| 13 | Amendments were drafted, prompted and read-selected by one party, five times in seventeen days (row 33) | charter | an amendment is judged as jack judges everything else | P: the amendment procedure, C2c item 12 |
| 14 | A window that cannot pass stays open to its stated end (row 39) | charter | a settled verdict is entered when it is settled | P: C2c's first amendments |
| 15 | Options put to the sovereign had no decidable reading. Witnesses: the identities item (ten cold reads, rows 43–44); the procedure contracts (four failed reads before his choice, row 43); the C2c inventory (three failed reads) | briefs | each option is a predicate the record can decide | P: counsel's discipline, stated in conversation on 6 November, not on `main` |
| 16 | C2a's stated end can be read two ways and is unruled (`transcripts/CASES.md`) | statistics | a window has one stated end | P: M.1 of the C2c draft |
| 17 | The paid API balance ran out and every OpenAI session failed with "You have no credits remaining" (`opencode-runner` #320–#324, 6 November) | sessions | paid capacity is monitored | N |
| 18 | A push-triggered workflow runs the pushed copy of its own file (`counsel.yml`), so anyone who can push to `opencode-runner` can run code beside steel's tokens | runner | code that holds a secret runs only from `main` | N; the exposure predates the courier |
| 19 | The courier can label, comment and close on jack beyond the grant of seq 2131 (row 44) | runner | the courier does only what the grant names | P: row 44's U2 |
| 20 | Sessions ended their turn after reading, with nothing committed (`opencode-runner` #317, re-run as #318) | sessions | a long task runs to its end | P: prompt wording ("This is one long task") |
| 21 | A discharge line was drafted with the `seq` of its own future proposal, which an open PR already held (7 November; avoided by citing seq 1564) | W5 | a discharge cites an entry that names the row | P: the pre-built `due.py` refuses an unrelated seq, but it is not on `main` until W5 lands |
| 22 | Counsel asked the sovereign for three platform acts on 6 November (row 44) | the sovereign's channel | counsel "asks the sovereign for no platform act" (BRIEF-C2a-prime) | P: the rule and row 11 |

## What the ledger shows

- **The mechanisms are where trust is highest.** The kernel and the statistics layer, rows 1 and 2, are pinned. The platform layer, row 3, is held by construction since 6 November.
- **Most mistakes are counsel's drafting**: rows 11, 12, 13, 15, 21 and 22. These are held by promises and cold reads, which catch an error but do not prevent it. Row 15 alone cost about twenty reads in two days.
- **Two rows have nothing**: row 17, an alarm, and row 18, a trust boundary. Both are operational, and outside jack's law.

## Candidates for C2c, each to enter only with a pin

Rows 8, 9 and 12 already have C2c items promised by their own COUNSEL-OPEN rows. This ledger adds:
- **Row 5:** a pin that runs each verb under each principal that the runbook says runs it.
- **Row 10:** a pin under which an evidence file without a committed producer fails.
- **Row 21:** a W5 twin with a discharge citing a seq that does not name its row, which must be refused. This is satisfied once W5 lands with its pins.

**Outside jack's law**, for the runner and the sovereign:
- Row 17: a session that fails on capacity files one issue to the sovereign.
- Row 18: workflows that hold secrets trigger only from `main`.
- Row 19: U2.

**Row 15 has no pin.** It is a discipline in counsel's drafting, and the cold read is its only check.
