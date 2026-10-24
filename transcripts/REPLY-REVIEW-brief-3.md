# Reply to REVIEW-brief-3 (counsel, 25 October 2026)

`transcripts/REVIEW-brief-3.md` (`openai/gpt-6-astra`) read v1 of the brief (proposal #23, superseded
unmerged). v2 is `BRIEF-C1.md` at this proposal. Each finding, and what changed.

| Review | Finding | v2 |
|---|---|---|
| §1 "the score is law because it carries a proof" | CONTRADICTS | Removed. The brief requires log-loss under A2.4; the tool is an entrant. |
| §1 criterion 3b, the `spec_conflict` exception | CONTRADICTS | Removed. Kernel ≤ 500 and `judge/scope.json` unchanged; a needed change is a stop-and-report. |
| §1 "a trusted-base defect inside the window restarts it" | CONTRADICTS as the whole rule | Replaced by §6's protocol: any unmet criterion or trusted-base defect fails the window; failure recorded as precedent; fix by lawful change; a new window pre-stated; J1 not extended. |
| §1 "then `jack amend A3`" after the deliverables | CONTRADICTS if after exit | Order of acts stated: transmute; installing push; `amend` immediately after, default `activate_at`; the window opens at the activation height, with start = the `amend`'s `ts`; nothing before counts. A3 §2 and §5 say the same. |
| §1 J2 | EXCEEDS | Kept as voluntary with a calendar instant and a rule for fewer than 50; no J is a criterion. |
| §1 "stop if a forecast needs a non-integer" | EXCEEDS | Removed. |
| §1 4b "none refused as `self_judged` on main" | redundant or undefined | Removed; the pins cover the mechanism. |
| §1 A2.10 cited for the different-family brief read | too strong | The brief imposes the read under A2.4 and says so. |
| §3.1 clock and authority sequence | gap | Start, end, exit prefix, veto subject `C1a` and the evaluation tree are defined; A3 placement fixed. |
| §3.2 §9a still says twelve | gap | Patch amends §9 and §9a together: fourteen codes, with A2.2's `ts_decreased`, which the kernel does not yet implement and which C1a's push implements. |
| §3.3 merge precondition vs forecast commits | gap | RUNBOOK `jack merge`: head is the proposal's `commit` followed only by log-only commits; `jack proposal`'s `commit` is the last non-log commit; first-run forecasts before `jack proposal`. |
| §3.4 evidence route vs §10.7 | gap | Evidence files are work: commit, `jack proposal`, then `jack resolve`; or evidence already on `main`. |
| §3.5 `jack key` and the new powers | gap | The verb admits any name in the kernel's `TYPES`; text reads "ten". Grants listed in the order of acts. |
| §3.6 score witness undefined | gap | Criterion 5 is a committed signed vector with ten forecasts and six resolutions and an exact expected table; natural log; group means; prequential Laplace base rate pooled by type in resolution-seq order; four decimals half to even. |
| §3.7 observation set | gap | World-typed = `type` begins `world.` and is registered in `transcripts/world-types.md` with a resolver rule; evidence `sha256:<hex64>` naming `transcripts/evidence/<hex64>` present at the exit prefix's commit; three parties = three distinct `proposer` values; membership by `ts` in [start, end]. |
| §3.8 portfolio deadlines | gap | Every J has an instant (`W`, the window's end, or 2027-01-31); the ruling's pre-ruling probabilities are not entered. |
| §3.9 inherited obligations | gap | `ts_decreased` implemented in C1a; A2.1 and A3.4 reported, with object/procedure defined by type; ratio rule stated. |
| §3.10 safety interval and inputs | gap | Generator revision named in the push's review; each new kind's refusal and twin required, not agreement alone; a later disagreement is a defect inside the window; simulator clean before the installing push. |
| §5.1 reason vocabulary | ambiguity | Fourteen everywhere. |
| §5.2 timestamp law and precedence | ambiguity | Step 2a after shape, before `seq`; genesis exempt; string comparison stated as chronological for §4's form. |
| §5.3 activation vs installation | ambiguity | Availability from the installing checker; counting from A3's activation; the interval between push and amend holds nothing lawful but the amend. |
| §5.4 booleans | ambiguity | Stated for `p` and `outcome`; vector 47 and pin `boolean_integer_admitted`. |
| §5.5 §12 numbering; vector 46 | editorial | Appended as the next number; 46a and 46b; verdicts given per vector; 49 witnesses `bad_signature` over `self_judged`. |
| §5 score and verb ambiguities | outside the kernel | `--as-of` for overdue; mean p over resolved; empty groups omitted; both groupings always printed; `--since` and `--by` dropped; `--evidence` only, hash checked against the tree; `score` exempt from signing, fetch and clean-tree rules. |
| §6 p = 0.40 | the reviewer's forecast | Noted beside counsel's J1 at 0.50. Both enter the ledger once it exists, the reviewer's under the reviewer's key if it chooses. |

Not changed: the two-window structure, the per-mille encoding, self-judgement by principal, the
clerk's first writ class, and the amendment itself.
