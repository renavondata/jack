Model: `openai/gpt-6-astra`

## 1. Does each item follow from its cited charter authority?

No. Classifications below apply to each item as a whole; where an item mixes warranted work with an additional condition, the distinction is stated. CHARTER Amendment A1 overrides the earlier text. REPORT records findings and SPEC specifies machinery; neither by itself supplies a charter amendment.

### §3 — Scope

| Item | Finding | Reason |
|---|---|---|
| Opening paragraph: trusted changes by Guy; builder and independent reader | EXCEEDS | A1.1 reserves the trusted base against proposals, and A1.7 requires review by someone other than the writer. Requiring every code change to be read by another model family adds to A1.7: §5 requires different-family authors for the two checkers, not a different-family reader for every change. The builder-only restriction comes from SPEC §10, rather than an express charter requirement. |
| 1. Key guard | EXCEEDS | REPORT §8.5 records a restriction pending a guard, but the cited report is not charter authority for a new validity rule. A1.1 expressly provides key declaration, re-declaration and revocation; it does not require retaining a key with change power. Preventing accidental loss is understandable under §2.2, but an unconditional prohibition on relinquishing that power is an additional restriction. The mandatory full 10⁵ rerun is also stronger than §6's C1 safety requirement. |
| 2. Three entry types | EXCEEDS | `writ`, `discharge` and `wish`, their schemas and matching checks implement §§5 and 7. The additional 500-line C1 promotion bound is not supplied by those sections: §5 gives a 1,000-line checker design, while A1.5's 450-line bound applies to C0. Three types also do not suffice to implement all of §7; see item 6. |
| 3. Keys per party | FOLLOWS | Signed identity and separation by key follow from §§2.4 and 5. The named keys and powers are a concrete proposed allocation requiring Guy's grant. The charter's `accept`/`wish`-only herald is explicitly a proposed default for Guy to decide, so a different proposed allocation is not itself a contradiction. Signatures replacing attribution claims address REPORT §8.3.5. |
| 4. The record used | FOLLOWS | Recording proposals and merges implements §9.1's types, §9.6's externally derived proposal facts, and §2.4's attributed entries. Binding a proposal to the preceding commit is a concrete way to avoid a self-referential commit identifier. It must continue to use the pre-existing checker, as A1.1 and §2.1 require. |
| 5. Clerk | CONTRADICTS | Timer-driven reconciliation and writs follow from §5. The prescribed escalation table does not implement §5's pre-stated ladder: re-invite, re-invite on another runner or model, then writ to Guy. W1 jumps from dispatch to Guy; W4 gives one unspecified next level and then Guy. The 300-line and standard-library-only clerk constraints are additional requirements; the charter's standard-library restriction is on the kernel. The unresolved protected-branch append mechanism is an implementation gap. |
| 5.W1 | CONTRADICTS | Redispatching a missing judge is consistent with reconciliation, but the stated escalation omits §5's alternate runner/model step. |
| 5.W2 | FOLLOWS | Asking Guy to decide merge or close is a possible obligation under §§5 and 7. The particular 24-hour deadline is a proposed operational choice, not a charter-prescribed value. |
| 5.W3 | FOLLOWS | Reconciling an unrecorded merge implements the record and the level-triggered clerk. |
| 5.W4 | CONTRADICTS | “Once at the next level; then writ to Guy” neither states nor guarantees the full §5 ladder. It also needs an explicit terminal treatment for an overdue writ already addressed to Guy. |
| 6. Guy's acts typed | CONTRADICTS | §7 requires every Guy act to be an entry and classifies every non-decision as a repair. Signed tags are not those entries. Counting only `guy-master` discharges misses repairs such as manual dispatches, pushes, fixes and re-signings. The decision list also omits the budget and capability grants for money/releases. REPORT's temporary C0 workaround does not amend §7 for C1. |
| 7. Simulator | FOLLOWS | §6 requires synthetic attacks before live operation and agreement on adversarial logs. Clerk attacks and byte-level regressions discovered in C0 are relevant concrete cases, not an unrelated subsystem. Keeping the differential implementation unchanged is acceptable only if it still implements the checker contract after C1 changes. |
| 8. Judge and scope | EXCEEDS | Protecting the clerk's implementation is consistent with a clerk that cannot change its own authority. SPEC §10, however, supplies C0's path lists and cap, not charter authority for a new 4,000-line C1 requirement. CHARTER §6 does not make a total-code cap a C1 promotion condition. Any expanded path/cap refusal also needs justification under §2.4's restriction on hard gates; merely inheriting SPEC's machinery does not supply it. |

The scope additionally omits obligations expressly assigned to C1 by the signed amendment: A1.3 moves rules as data, witnesses, lapse and the Fuller checks to C1; A1.6 assigns non-decreasing timestamps to C1. “Smallest language that expresses the first real case” limits the language's size, not the amendment's allocation of that work. The brief's §1 deferrals cannot repeal those instructions. The proposed key guard is itself a concrete new constraint requiring a decision about its lawful admission.

### §4 — Exit

| Item | Finding | Reason |
|---|---|---|
| Opening commitment/amendment sentence | FOLLOWS | §6 requires the window, α, baseline and attack list to be committed before the window opens. This is a procedure for doing so, not evidence that the missing baseline has already been committed. |
| Safety | EXCEEDS | Zero disagreements and attacked/twin safety follow from §6. Requiring 10⁵ logs after every kernel change extends C0's §9 exit-run requirement into a repeated C1 obligation not called for by §6. |
| Simulator first | FOLLOWS | Directly required by §6. “Clean” still needs an operational definition. |
| Liveness, live, 14 days | CONTRADICTS | The window, threshold, e-process and assize-derived baseline follow from §§6, 8 and 10.3. But §6's success is completion with **no repair by Guy**, not a discharge signed by somebody else. A herald discharge after Guy manually repairs a stall scores 1 under this brief. That changes the measured outcome and defeats §12's explicit safeguard against retyping repairs. The fixed λ is allowed when the baseline is nonzero; the draft provides no handling for a zero baseline. Reporting durations rather than testing their unbounded mean follows §6. |
| Size | EXCEEDS | The 65-line differential bound is inherited from SPEC §9a. The 500/300/4,000 bounds add C1 exit conditions beyond CHARTER §6; A1.5's numerical amendment is scoped to C0. |
| Procedure | FOLLOWS | It repeats §12's procedure/object ratio and stop-and-report threshold. The brief inherits the charter's lack of an operational classification. |
| Trusted-base defect restarts the window | CONTRADICTS | Restarting and recording a precedent are consistent with §6, but the item omits §6's requirement that the fix be a change entry and covers only trusted-base defects rather than every failed window. Read with §1's own-push-only change path, it substitutes an unrecorded fix path for the prescribed one. |
| Guy has not vetoed | FOLLOWS | Expressly required by §6. |

## 2. What in §3 is unnecessary to reach §4's exit?

Relative to the exit **as written**:

- The `wish` type in §3.2. The exit measures writs and discharges, not intake or processing of wishes. It is nevertheless justified by the charter's broader C1 obligations.
- The complete `counsel`/`builder`/`reviewer` key rollout in §3.3. The written success test requires a non-`guy-master` discharge, which the herald can supply; it does not require these three separate proposal identities to operate during the window.
- The ongoing replacement of assize's weekly measurement with a log count in §3.6. §4 uses a fixed pre-window assize baseline and window-specific writ outcomes; it does not require an ongoing weekly replacement series.

The key guard and byte-level simulator kind cannot honestly be called unnecessary to the literal exit: §4 requires every introduced pin to be killed and every C1 simulator kind to run. Those clauses make added work part of its own acceptance condition. Necessity under that expanded exit does not establish charter authority.

## 3. What needed to reach §4's exit is missing from §3?

- **An executable measurement protocol.** No §3 item computes and records the writ outcomes, baseline, e-process path or threshold crossing. It needs a precommitted window start/end, outcome ordering, treatment of pending writs at stopping/end, and a non-outcome-selective inclusion rule. Recording early successes while leaving pending failures out cannot silently become the sequential test.
- **A defined baseline calculation and edge cases.** The weekly act counts must identify which individual assize merges needed repairs, not merely total decisions and repairs. The amendment must supply the numerical baseline and handle zero merges, *p₀* = 0 (undefined λ), and *p₀* = 1 (the stated process cannot reach 20).
- **Discharge evidence.** A matched writ identifier alone does not establish that the obligation was completed, who performed the work, or when. The clerk needs explicit predicates for opening, completing and escalating each obligation, including deadlines and terminal escalation. Charter-compliant measurement additionally needs attribution of every Guy repair, even when someone else signs the final discharge.
- **A working append path.** §3.5 leaves the branch-protection choice unanswered. Signed, serialized, retry-safe appends must actually reach the protected log, including the clerk's own merge/discharge entries, before there can be a live window.
- **A simulator acceptance contract.** The listed kinds need workload/clock inputs and expected outcomes, including a benign completion path. Checker agreement alone cannot detect two checkers accepting entries from a clerk that failed to issue or escalate a writ.
- **Procedure accounting.** There is no classification of procedure versus object entries, rolling-window calculation, zero-denominator treatment or stop/report implementation.
- **Window failure and restart handling.** The work list needs the record of a failure, the lawful fix and the new committed window. It also lacks §3 adjudication's explicit clerk halt and writ to Guy upon checker disagreement; making a judge run red is not the same operation.

These gaps concern execution and evidence for the exit. The omitted A1.3/A1.6 work identified in answer 1 is additionally necessary for a charter-compliant C1, even though this draft's weakened exit does not test it.

## Undecidable sentences in §4

- **“Simulator first: a clean run over all C1 kinds before the clerk goes live.”** “Clean” has no specified verdict for clerk behaviour, workload or simulated time; listing attack names does not supply one.
- **“Liveness, live, 14 days: Yᵢ = 1 if writ i was discharged by a party other than `guy-master` before its deadline, else 0, over every writ issued in the window.”** The window's start is unspecified, as is the treatment of writs whose deadlines extend beyond the window or a proposed early stop. The distinction between signer and performing party is also unresolved.
- **“p₀ = the share of assize merges in 14–20 October that needed no repair by Guy, from the weekly measurement of 21 October, written into this brief by amendment before the window opens.”** There is no numerical value yet and no rule assigning repairs to merges. The named future amendment could resolve this; the present text cannot.
- **“Eₜ = ∏ (1 + λ(Yᵢ − p₀)) with λ = 1/(2p₀) fixed; promotion at Eₜ ≥ 20 (α = 0.05), stopping any time.”** Which outcomes are included at a proposed stopping time is unspecified, and λ is undefined for an unexcluded zero baseline. It must also be read conjunctively with the other exit conditions, not as sufficient by itself.
- **“Procedure: entries that change procedure against entries that do work are counted; at more than 5 : 1 in any 14 days, stop and report [§12].”** No reproducible classification covers mixed-purpose entries, and no treatment is given for a zero object count.
- **“A trusted-base defect inside the window restarts it [§6]; the defect is a precedent, recorded.”** No criterion identifies a qualifying defect, when it counts as inside the window, or the restart instant. Those choices can change which outcomes qualify for promotion.

exceeds or contradicts the charter
