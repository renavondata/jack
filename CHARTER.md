# A small core that governs — charter

Counsel's draft, 13 October 2026 (Claude, model `claude-opus-5-5`), for Guy Freeman. **Binds nothing until Guy signs it**, whole or in part, as the genesis text of a new repository. Its forecasts (§11) are scored like anyone's.

## 0. Scope

This charter governs the repository CLAUDE.md already requires at L3: *"Agents live elsewhere and are judged by a released judge image pinned by digest."* It amends nothing in assize. Assize finishes L2, freezes, and becomes this core's judge of last resort.

It contains four maxims, three secondary rules, one architecture, three tests, a promotion rule and a build order. Every primary rule, threshold, model and heuristic enters later, by precedent, as an entrant that can lose.

## 1. Evidence from assize

Guy's recorded acts on `renavondata/assize`, classified mechanically from GitHub's record by `guy_acts.py` (in this project beside the charter, with every act listed in `guy-acts-6-13oct.csv`):

| HKT | 10 Oct | 11 Oct | 12 Oct | 13 Oct | 4 days |
|---|---:|---:|---:|---:|---:|
| decisions | 27 | 35 | 14 | 12 | 88 |
| repairs | 36 | 22 | 32 | 31 | 121 |
| merges to master | 3 | 5 | 6 | 10 | 24 |
| repairs per merge | 12.0 | 4.4 | 5.3 | 3.1 | 5.0 |

- **Decision:** a wish filed (18), a draft signed (21) or declined (10), an instruction filed (11) or withdrawn (11), a first Accept on a PR (15), a ruleset (2).
- **Repair:** anything else the loop needed from him: stop or failure issues closed (39), re-fires and re-signs (21), dispatches and re-runs (19), unmerged PRs closed (13), re-Accepts after a push dismissed the first (7), other label and issue events (22).
- Four of the 24 merges discharged brief obligations (L2a 2–5); twenty changed the court's own procedure. L1 left 55 obligations on L2; five are discharged; L2b (NetHack) and L2c (the seal) have not begun.
- Caveats: acts counsel took with Guy's token count as Guy's (F6); issue-body edits are invisible to the REST API and are not counted; before 10 October sessions were often started by hand and left no record, so earlier days are not comparable.

Each recurring failure is a broken maxim (§2):

| | Failure | Witness | Maxim |
|---|---|---|---|
| F1 | A PR's `pins` runs the PR's own harness: the accused writes the test that judges it | #176 | 1 |
| F2 | One draft signed without a `Price:` line turned every branch red, because P0x reads live issue bodies: all pending work became non-compliant after the fact | STATUS of #171, 13 Oct | 2 |
| F3 | Labels applied to conflicted PRs fired nothing; queued runs were dropped; stalls were found by a human watching a phone | W1 (#110), #126, HERALD-6 | 3 |
| F4 | Three review rounds spent on how a STATUS cites a green run, the code green throughout; the PR then closed and rebuilt from master | #143, closed 13 Oct | 4 |
| F5 | Force-push and deletion of every branch but master, and all tags, were ungated until 13 October, while STATUS bookkeeping blocked merges | rulesets 25000488, 25000713 | 4 |
| F6 | Counsel acted through Guy's token: unscored, unattributed | issue-body edits; #162 | 4, corollary |
| F7 | Procedure crowded out the object: 20 of 24 merges were procedure | table above | §8 |

## 2. Four maxims

1. **No one judges their own cause** (*nemo iudex in causa sua*; Dr Bonham's Case, 1610). The checker that decides an entry's validity is fixed before the entry exists and cannot be changed by it. A resolution's proposer differs from its forecast's. The last judge of value is the world, through a judge no party can edit.
2. **The law looks forward and never commands the impossible** (Fuller 1964; *lex non cogit ad impossibilia*). An entry is judged by the law in force before it. Every rule is admitted with a witness that violates it and one that satisfies it: the first proves the rule can fail, the second that compliance is possible.
3. **Whatever is held must be produced** (habeas corpus; Habeas Corpus Act 1679). Every obligation is derived from present state and the clock, carries a deadline, and escalates when the deadline passes. No component waits for an event; each reconciles state.
4. **Decide by expected value; forbid only the irreversible** (Arrow & Fisher 1974; Blackwell 1951). Reversible acts are priced and scored, never blocked. Hard gates stand only before effects that cannot be undone, where waiting has positive option value. *Corollary:* every source of influence is scored, because an unscored source has unknown value; no party, the sovereign's delegates and counsel included, acts except through entries that carry its identity. Ostrom's commons found the same pair empirically: graduated sanctions, and monitors accountable to the monitored (Ostrom 1990).

## 3. The minimal law: three secondary rules (Hart 1961)

Only this section is law at genesis. Primary rules accrete as precedent (Blackstone), each from a witnessed case.

- **Recognition.** An entry is valid iff (a) its parent is the head of the log; (b) it is signed by a key that the law in force grants for its type; (c) every rule in force at its parent accepts it.
- **Change.** A rule enters or leaves only by a change entry signed by a key holding the change power (at genesis, Guy's alone). It binds from the next entry. It carries its two witnesses. Rules are data in a decidable language (proposed: stratified Datalog; Ceri, Gottlob & Tanca 1989), so the law can grow while the trusted interpreter stays fixed. *Lapse:* a rule all of whose violating witnesses the rest of the law already rejects is a lapse candidate (tested oldest first, one at a time, so two rules never lapse on each other's account). It lapses at the end of a notice period unless some proposer enters a counter-witness that it alone rejects, which then joins its witnesses. Witness-redundancy is not subsumption, which is undecidable for recursive Datalog; the notice is how a rule that still guards something unwritten is defended. Law should not outlive its necessity (Jefferson to Madison, 6 September 1789), and since the test and the defence are both entries, lapse costs Guy nothing.
- **Adjudication.** The checker is the only adjudicator of validity. Its digest is in the log; it runs from trunk, never from the proposal; a second implementation by a different author replays every entry, and any disagreement halts the clerk and raises a writ to Guy. Questions of merit (is this work good?) are not questions of validity: they are forecasts, scored when the world resolves them. Statutes are confined to decidable properties, because non-trivial semantic properties of programs are undecidable (Rice 1953).

## 4. Law as computation

| Law | Computation |
|---|---|
| the record | an append-only, hash-chained log |
| the law in force at entry *i* | the rules admitted by entries before *i*: a versioned interpreter, in which retroactivity cannot be expressed |
| the state | fold(law, log): state-machine replication (Lamport 1978; Schneider 1990) |
| rule of recognition | the validity predicate |
| a statute | a decidable predicate, admitted with a violating and a satisfying witness (mutant and twin) |
| a judgement on the merits | a forecast under a strictly proper score (Gneiting & Raftery 2007), resolved by the world |
| a writ | an obligation computed from state and clock, with deadline and escalation: a level-triggered reconciliation loop (Burns et al. 2016) |
| a seal | a capability: the only reference to an irreversible effect (Dennis & Van Horn 1966; Miller 2006) |
| precedent | a rule enters only from a witnessed case, and lapses when redundant and undefended |
| safety and liveness | every property is the intersection of a safety and a liveness property (Alpern & Schneider 1985): recognition and adjudication carry safety, writs carry liveness |
| trusting trust | a kernel small enough for a human to read (de Bruijn criterion; LCF, Gordon, Milner & Wadsworth 1979), replayed by a diverse second implementation (Thompson 1984; Wheeler 2005) |

Fuller's eight desiderata become checks:

| Fuller | Check |
|---|---|
| generality | rules quantify over entry types, never name a party |
| promulgation | rules, and the checker's digest, are entries |
| non-retroactivity | prefix interpretation, by construction |
| clarity | every rule decidable, with its witnesses |
| non-contradiction | the satisfying witnesses pass the whole law together |
| possibility of compliance | each satisfying witness passes the law in force plus its rule |
| constancy | change only by change entries; the rate is reported |
| congruence | the checker that runs is the one whose digest is recorded; two implementations agree |

## 5. Architecture

Three roles, separated by key, not by convention.

- **Checker (judiciary).** Pure, deterministic, small: log format, Datalog engine and validity predicate together within 1,000 lines, so Guy can read all of it. Two implementations, in different languages, by authors from different model families.
- **Clerk (executive).** Dumb and level-triggered. On a timer it reads state and clock, computes obligations, issues writs and invitations, and escalates overdue ones along a pre-stated ladder: re-invite; re-invite on another runner or model; writ to Guy. It decides nothing about validity and holds no change power.
- **Proposers (everyone else).** Every model, counsel, and Guy in his ordinary acts. Untrusted. Each output is an entry carrying its proposer and, where it predicts, a forecast. Which proposer is invited is an election by Hedge or Fixed Share on proper scores (Freund & Schapire 1997; Herbster & Warmuth 1998; EXP3 under bandit feedback, Auer et al. 2002): an entrant, not law.
- **Keys and capabilities.** Genesis lists the keys. Proposed default, Guy's to decide: an offline master key (change power; capability grants for money, releases and new keys) and an online herald key that may sign only `accept` and `wish` entries, so a compromised herald can do nothing else. Signatures are verified from the log itself (`ssh-keygen -Y verify`), never from a platform's event timeline.

Read as a control loop: the log is the measurement record; fold(law, log) is the model every good regulator must contain (Conant & Ashby 1970); the clerk is the controller; the checker is a safety filter no control action bypasses; the election is adaptation. The pool of proposers must carry at least the variety of the disturbances it absorbs (Ashby 1956), which is the case for several model families rather than one, and for not letting one vendor's limits stop the court.

## 6. Three tests, and promotion

- **Safety, by independent replay.** Both checkers accept and reject the same entries, for the same reasons, on the real log and on simulated adversarial logs. Every named attack is refused; every twin is admitted.
- **Liveness, by writ.** No writ outlives its deadline without escalation. The share of items completed with no repair by Guy beats a null rate *p₀*.
- **Value, against a baseline.** C1: the liveness rate itself. C2: aggregated forecasts beat the base-rate forecaster in log-loss. C3: the agent beats the incumbents under assize's sealed judge.

Liveness and value are tested by betting e-processes (Shafer & Vovk 2019; Ramdas et al. 2023), prequentially (Dawid 1984). For outcomes *Yᵢ* ∈ {0, 1} and H₀: E[*Yᵢ* | past] ≤ *p₀* for every *i*, the process *Eₜ* = ∏ᵢ≤ₜ (1 + *λᵢ*(*Yᵢ* − *p₀*)), with predictable *λᵢ* ∈ [0, 1/*p₀*], is a non-negative supermartingale under H₀, so P(supₜ *Eₜ* ≥ 1/α) ≤ α (Ville 1939). Log-loss differences are tested the same way after clipping probabilities, which bounds them. Stopping at any time costs nothing. Unbounded quantities (repairs per merge, minutes) are reported and never tested: no procedure can certify a small mean of an unbounded variable (Bahadur & Savage 1956).

**Promotion rule.** A layer is promoted (frozen, and the next begins) when, within its pre-stated window: safety holds with zero disagreements; liveness and value reach *Eₜ* ≥ 20 (α = 0.05; C0, which produces nothing yet, needs safety alone); and Guy has not vetoed. Windows, α, *p₀* and the attack list are committed before the window opens. A layer that fails its window is not patched in place: the failure is a precedent, the fix is a change entry, and the window starts again.

**Simulator first.** Before any model touches a layer, it runs against synthetic proposers drawn from the attack list: self-judging, retroactive, vacuous, impossible, forged, rewriting, forking, unattributed, stalling and flooding. Real models enter only when that run is clean.

## 7. Guy's acts

- **Decisions:** a wish; a signature on genesis, a change entry or a capability grant (money, releases, keys); a veto or promotion at a layer boundary; the budget.
- **Repairs:** every other act.

Every act of Guy's is an entry, typed by its entry type and the key that signs it, so the split is mechanical and fixed in advance, not judged afterwards. Targets: repairs tend to zero; decisions to a handful a week. A repair means a layer has found a defect, and the repair is recorded as a precedent case. Wishes are never scored: they are preferences, not predictions. What the court forecasts about his answers (the Vizier's role in assize) is an entrant like any other.

## 8. Build order

| Layer | Content | Exit (pre-stated) |
|---|---|---|
| C0 | log; two checkers; law as data; simulator; judge workflow | §9 |
| C1 | clerk and writs; Guy's acts as typed entries | clean simulator run, then *Eₜ* ≥ 20 against *p₀* within 14 days live |
| C2 | forecasts, proper scores, election (assize's `harness.ledger` scoring ported as an entrant) | aggregated forecasts beat base rates, *Eₜ* ≥ 20 |
| C3 | the seed agent (CLAUDE.md L3's content) | assize's sealed judge: beats random on held-out seeds in both Worlds, and the predictive floor |

C0 enables (a record that binds); C1 acts; C2 obliges the system to control itself (*Federalist* 51: "you must first enable the government to control the governed; and in the next place oblige it to control itself"). Each is a simple system that works before the next is added (Gall 1977). C3 needs assize's sealed image and waits for L2's verdict; C0–C2 contain no agent and can start now.

## 9. Brief C0: the record and the checker

**Precondition.** Guy has named the repository. §§2–3 of this charter are its genesis text. Nothing is imported from assize; code may be copied with attribution.

**Purpose.** A record that binds, judged by a checker no proposer can edit, small enough for Guy to read entire.

**Scope.**
1. Log: `log.jsonl`, one entry per line, `{seq, parent, ts, type, proposer, body, sig}`. `parent` is the SHA-256 of the previous line. `sig` is an SSH signature (`ssh-keygen -Y sign`, namespace `core-entry`) over the line without `sig`. Types at genesis: `genesis`, `key`, `rule`, `repeal`, `proposal`, `merge`.
2. Law: rules are stratified Datalog over facts extracted from the log prefix; a rule derives `violation(Seq, RuleId)`. Each `rule` entry carries its violating and satisfying witness entries.
3. Checker: `check(log) → ok | (seq, rule, reason)`. Entry *i* is checked against the rules admitted before *i*. A `rule` entry is valid only if its violating witness yields a violation, and its satisfying witness none, under the law in force plus the new rule. Lapse candidates (§3) are reported at each change entry; the notice and the lapse itself wait for C1's clerk.
4. Second checker: an independent implementation of 1–3, in another language, written from the spec text alone by an author from a different model family.
5. Simulator: seeded generators for every attack in §6 and for benign entries; property tests.
6. Judge workflow: for every proposal, trunk's two checkers run over the proposal's appended entries as data. Facts about the proposal (paths touched, signing key) are derived from git, never from the proposal's claims. The proposal's code is never executed by the judge; the workflow holds no secret and a read-only token.
7. `LAW.md`: §§2–3 in prose, each sentence citing the code that enforces it.

**Pre-stated criteria.**
1. Every pin below is KILLED and its twin passes, in CI, from trunk.
2. The two checkers agree, entry by entry and reason by reason, on the real log and on 10⁵ simulated logs, whose seed list is committed before the first run.
3. Kernel (log, Datalog engine, checker; not tests, simulator or second checker) within 1,000 lines; an excess is reported, never hidden.
4. Guy has read the kernel and signed `genesis`.

**Pins, each with its named mutant, KILLED with a passing twin.**
- `judge_from_proposal`: a merge judged by a checker the proposal supplied is refused.
- `final_law_for_all`: a checker applying the latest law to earlier entries is killed by a log in which a later rule would reject an earlier valid entry.
- `vacuous_rule_admitted`: a rule whose violating witness passes is refused.
- `impossible_rule_admitted`: a rule whose satisfying witness fails is refused.
- `unsigned_change`: a `rule` or `repeal` signed by a key without the change power is refused.
- `history_rewritten`: a log with an edited past line fails at that line.
- `fork_admitted`: a second entry on the same parent is refused.
- `redundancy_unreported`: a rule whose witnesses a later rule already rejects is not reported as a lapse candidate.
- `unattributed_entry`: an entry with no proposer, or an unknown key, is refused.
- `checker_drift`: a seeded divergence in the second checker turns CI red.

**Refusal list.** No LLM call, network access or clock read in either checker; time enters only as an entry field. No rule written as code. No dependency outside the language's standard library in the kernel. No agent code.

**Stop and report if** stratified Datalog cannot express a C0 rule; the two implementations disagree about what the spec means (an ambiguity is a finding, not a patch); or the kernel passes 1,500 lines.

**Deliverables.** The repository at C0's exit; a C0 report with transcripts; a draft brief for C1.

## 10. Assize until the freeze

1. **Stop adding procedure.** Once #113, #174 and #176 have merged, no further process instruction goes to assize unless it removes a stall the brief cannot route around. Process wishes go to this charter's backlog instead. Procedure's value in assize expires at the freeze; the same idea in the core compounds.
2. **Optionally, narrow L2a.** L1's obligations 44–55 (process, git, CI) are recorded as discharged where a later instruction's pin already covers them, and are otherwise carried here as design inputs rather than pinned in a repository about to freeze. Obligations 1–43 concern the judge, the interface, the harness and measurement, and stay.
3. **Measure weekly** with `guy_acts.py`. The series becomes *p₀* for C1.
4. **Afterwards**, assize's sealed image is C3's value test, and its ledger's scoring code is C2's first entrant.

## 11. Counsel's forecasts

| id | Claim | p | Resolves |
|---|---|---:|---|
| K1 | Guy's repairs on assize, 14–20 Oct HKT, are fewer than the 147 of 7–13 Oct, by `guy_acts.py` as of 13 Oct | 0.60 | 21 Oct |
| K2 | Repairs per merge on assize, 14–20 Oct, below 2.0 | 0.35 | 21 Oct |
| K3 | The root `REPORT.md` carries an L2 verdict line by 30 Nov 2026 | 0.20 | 30 Nov |
| K4 | As K3, conditional on §10.1 and §10.2 both adopted by 20 Oct (void otherwise) | 0.35 | 30 Nov |
| K5 | C0's kernel is within 1,000 lines at its exit | 0.75 | C0 exit |
| K6 | The two checkers disagree on at least one simulated log before C0's exit | 0.65 | C0 exit |
| K7 | C0 exits within 14 days of the founding session's start | 0.50 | +14 days |
| K8 | C1's first live window reaches *Eₜ* ≥ 20 against *p₀* | 0.40 | window end |

Scored by log-loss. They enter a ledger only if Guy files them (assize A1.11(b)).

## 12. What would show this charter wrong

- C0 cannot hold recognition, change and adjudication within 1,500 lines, or Datalog cannot express C0's rules: the minimal-law thesis fails; revisit §3.
- C1's window fails against assize's baseline: level-triggered writs do not buy liveness here, and the fault lies in the clerk, not the proposers.
- Repairs fall only because acts are re-typed as decisions (Goodhart 1975). Guarded by typing acts by entry type and key, fixed before any window.
- The core repeats assize's procedure growth. Count procedure entries per object entry; at more than assize's 5 : 1 (20 : 4) in any 14-day window, stop and report.

## 13. References

- Alpern, B. & Schneider, F. B. (1985). Defining liveness. *Information Processing Letters* 21(4), 181–185.
- Arrow, K. J. & Fisher, A. C. (1974). Environmental preservation, uncertainty, and irreversibility. *Quarterly Journal of Economics* 88(2), 312–319.
- Ashby, W. R. (1956). *An Introduction to Cybernetics.* Chapman & Hall.
- Auer, P., Cesa-Bianchi, N., Freund, Y. & Schapire, R. E. (2002). The nonstochastic multiarmed bandit problem. *SIAM Journal on Computing* 32(1), 48–77.
- Bahadur, R. R. & Savage, L. J. (1956). The nonexistence of certain statistical procedures in nonparametric problems. *Annals of Mathematical Statistics* 27(4), 1115–1122.
- Barendregt, H. & Wiedijk, F. (2005). The challenge of computer mathematics. *Philosophical Transactions of the Royal Society A* 363, 2351–2375. (The de Bruijn criterion.)
- Blackstone, W. (1765–69). *Commentaries on the Laws of England.* Clarendon Press.
- Blackwell, D. (1951). Comparison of experiments. *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability*, 93–102.
- Burns, B., Grant, B., Oppenheimer, D., Brewer, E. & Wilkes, J. (2016). Borg, Omega, and Kubernetes. *ACM Queue* 14(1).
- Ceri, S., Gottlob, G. & Tanca, L. (1989). What you always wanted to know about Datalog (and never dared to ask). *IEEE Transactions on Knowledge and Data Engineering* 1(1), 146–166.
- Coke, E. (1610). Dr Bonham's Case, 8 Co. Rep. 107a.
- Conant, R. C. & Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science* 1(2), 89–97.
- Dawid, A. P. (1984). Statistical theory: the prequential approach. *Journal of the Royal Statistical Society A* 147(2), 278–292.
- Dennis, J. B. & Van Horn, E. C. (1966). Programming semantics for multiprogrammed computations. *Communications of the ACM* 9(3), 143–155.
- Freund, Y. & Schapire, R. E. (1997). A decision-theoretic generalization of on-line learning and an application to boosting. *Journal of Computer and System Sciences* 55(1), 119–139.
- Fuller, L. L. (1964). *The Morality of Law.* Yale University Press.
- Gall, J. (1977). *Systemantics: How Systems Work and Especially How They Fail.* Quadrangle.
- Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association* 102(477), 359–378.
- Goodhart, C. A. E. (1975). Problems of monetary management: the U.K. experience. *Papers in Monetary Economics*, Reserve Bank of Australia.
- Gordon, M. J., Milner, R. & Wadsworth, C. P. (1979). *Edinburgh LCF.* LNCS 78, Springer.
- Habeas Corpus Act 1679 (31 Cha. 2 c. 2).
- Hart, H. L. A. (1961). *The Concept of Law.* Clarendon Press.
- Herbster, M. & Warmuth, M. K. (1998). Tracking the best expert. *Machine Learning* 32(2), 151–178.
- Jefferson, T. (1789). Letter to James Madison, 6 September.
- Lamport, L. (1978). Time, clocks, and the ordering of events in a distributed system. *Communications of the ACM* 21(7), 558–565.
- Madison, J. (1788). *The Federalist* No. 51.
- Miller, M. S. (2006). *Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control.* PhD thesis, Johns Hopkins University.
- Ostrom, E. (1990). *Governing the Commons.* Cambridge University Press.
- Ramdas, A., Grünwald, P., Vovk, V. & Shafer, G. (2023). Game-theoretic statistics and safe anytime-valid inference. *Statistical Science* 38(4), 576–601.
- Rice, H. G. (1953). Classes of recursively enumerable sets and their decision problems. *Transactions of the American Mathematical Society* 74(2), 358–366.
- Schneider, F. B. (1990). Implementing fault-tolerant services using the state machine approach: a tutorial. *ACM Computing Surveys* 22(4), 299–319.
- Shafer, G. & Vovk, V. (2019). *Game-Theoretic Foundations for Probability and Finance.* Wiley.
- Thompson, K. (1984). Reflections on trusting trust. *Communications of the ACM* 27(8), 761–763.
- Ville, J. (1939). *Étude critique de la notion de collectif.* Gauthier-Villars.
- Wheeler, D. A. (2005). Countering trusting trust through diverse double-compiling. *Proceedings of the 21st Annual Computer Security Applications Conference (ACSAC).*

## Amendment A1: C0 is the record (14 October 2026)

Guy's decision on counsel's review of PR #1 (head fe5c2f2). Appended; overrides earlier text where they conflict.

1. **C0 holds no language for primary rules.** Entry types at C0: `genesis`, `key`, `proposal`, `merge`. The three secondary rules are code:
   - *recognition*: a canonical line, its `seq`, its parent in the chain, and a signature by a declared key whose powers include the entry's type. Keys are `ssh-ed25519`, canonical and not of small order. The SSHSIG reserved field is empty.
   - *change*: `key` entries signed by a key holding the `key` power declare, re-declare or revoke keys.
   - *adjudication*: trunk's kernel, by digest. The judge refuses any proposal whose trusted-base digest differs from trunk's, or that changes `CHARTER.md` (`trusted_path`). The trusted base is `kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and `SPEC.md`.
2. **Signatures are verified in the kernel**, standard library only, by SPEC.md's strict rule. `ssh-keygen` is the signing tool and a test oracle, never part of the kernel.
3. **The law language moves to C1**: §3's rules as data, their witnesses and lapse, and §4's Fuller rows on rules. C1 builds the smallest language that expresses the first real case. When rules come:
   - they judge conduct entries only, and never bind entries of change (`genesis`, `key`, `rule`, `repeal`), so no rule can entrench itself or make the log unusable (Hart's distinction);
   - a repeal that leaves any rule without a passing satisfying witness is refused, exactly as an admission is;
   - negation does not depend on the order of literals.
4. **Genesis** is committed to `main` by Guy himself, and its charter hash is checked against `CHARTER.md`. Only then are `judge` and `tests` made required checks.
5. **§9's criteria stand for this scope**, with criterion 3's bound at 450 lines. The pins are:
   - those of §9 that concern the record and the judge;
   - `trusted_path_unguarded`, `trusted_rename_admitted`, `forged_signature_admitted`, `weak_key_declared` and `checker_drift`.
6. **Timestamps do not decrease along the log**: C1.
7. **Recorded lesson.** The first draft's defects lay in machinery C0 did not yet need. The builder's own mutants did not find them; cold probes by another party did. Every layer is reviewed by a party that did not write it.


## Amendment A2: the opening of C1 (18 October 2026)

Guy's rulings of 18 October 2026 on the cold reads of C1's brief (`transcripts/REVIEW-brief.md`,
`REVIEW-brief-2.md`) and on counsel's research of the same day (`transcripts/RESEARCH-trusted-core.md`).
Appended; overrides earlier text where they conflict. Recorded by `amend` A2 under SPEC §7, after a
`decision` of kind `transmute` naming it; in force from its `activate_at`.

1. **Primary rules and their language.** The law language of §3 and A1.3, with its witnesses and lapse,
   enters at the layer in which the first real case arises: the first entry Guy wants refused that
   recognition does not refuse. Until then no primary rule exists, and no layer is required to build the
   language in advance of it. Each layer's report states whether a case arose. If none has arisen by C2's
   exit, §12's thesis that three secondary rules suffice is on trial, and C2's report says so.
2. **Timestamps.** `ts` does not decrease along the log. This is part of recognition, in the kernel, and
   binds every entry (replacing A1.6's allocation of it to a rule). Reason `ts_decreased`; pin
   `clock_runs_backward`.
3. **The judge's grounds.** The judge refuses a proposal on any ground a layer's brief pre-states,
   provided the ground is decidable from git and the log alone, is stated over powers and paths and never
   over a party's name, and refusing costs the proposer nothing but resubmission. §2.4 governs effects; the
   adjudication of a proposal is not an effect. The grounds of SPEC §10.7–10, adopted on 16 October, are
   the first such grounds; until keys exist for every party, the `Proposer:` trailer stands in for the
   signing key, and that substitution ends when the party's key is declared.
4. **Briefs.** A layer's brief may pre-state criteria, bounds and review rules for that layer, as §9 did
   for C0. They bind that layer only, and may tighten the charter's bounds, never loosen them. The kernel's
   bound is 500 lines for C1.
5. **The last key.** A `key` entry that would leave no key holding the `key` power is refused (§2.4:
   losing it is irreversible). Reason `bad_key`, a third cause of a refused declaration (SPEC §7); pin
   `last_key_revocable`.
6. **The sovereign's acts are entries** (§7, made mechanical). A change to the trusted base is lawful only
   when a `push` entry names its digest; the judge and the self-check refuse a trunk whose trusted base
   is not the one in force (SPEC §10.11). Veto, promotion, budget, grant, transmutation and the fix of a
   failed window are `decision` entries signed by a key declared in genesis (§10.14). A layer boundary is
   therefore an entry, not a tag; `c0-exit` is the last tag.
7. **Amendment is two acts and a wait.** A `decision` of kind `transmute` names the amendment; the
   `amend` follows and is in force from its `activate_at`, never before, and never over earlier entries
   (§3: the law looks forward). Between the `amend` and its height no `push` is lawful (SPEC §10.12): the
   law changes, then the code. An amendment that cannot be followed by agreeing checkers lapses unused.
8. **Someone other than the owner checks the record.** The head hash of `log.jsonl` on `main` is
   published on every push; a monitor that the owner does not operate verifies that each head extends the
   last and that both checkers accept the log, and writs Guy on any failure (§3 adjudication, extended to
   the record's history; maxim 1 applied to the sovereign).
9. **Review ends by construction.** A review finding is a pin, a mutant with a passing twin, or a replay
   disagreement; a reviewer's key may propose only under `pins/` and `spec/vectors/`; a builder's key may
   not touch them; a round that adds no pin ends the review. A builder that finds the specification
   contradictory records a `spec_conflict` entry and stops; it does not make the tests pass.
10. **Recorded lesson.** C0's exit found that counsel's harness, written freely and reviewed open-endedly,
    grew without producing the evidence it claimed, and that a brief had twice tried to settle by drafting
    what only an amendment can settle. Code is written to a text Guy has read; questions of what the
    charter allows are put to Guy as rulings and recorded here. Whatever counsel and builders are forbidden
    is what the agent of C3 is forbidden, by the same judge, keys and amendment path; nothing is imposed on
    the agent that was not first imposed on us.

## Amendment A3: the ledger before the clerk (25 October 2026)

Guy's ruling of 25 October 2026 on counsel's options (`transcripts/RULING-20261025-ledger-first.md`),
recorded by `amend` A3 under SPEC §7 after a `decision` of kind `transmute` naming it, and in force
from its `activate_at`. Appended; overrides earlier text where they conflict.

1. **§8, build order.** C1 reads: *the ledger (`forecast` and `resolution` entries under a proper
   score), then the clerk and writs; Guy's acts as typed entries.* C2 reads: *the election of
   proposers by their record; the ledger's types extended only as witnessed cases require.* C0 and
   C3 are unchanged. The reason, in one line: the clerk is better built against a real obligation
   than an invented one, and an overdue forecast is the first such obligation the record can hold.
2. **Two windows in one layer.** C1 has two pre-stated windows, C1a (the ledger) and C1b (the
   clerk), each with its exit written in `BRIEF-C1.md` before it opens. C1a's window opens at this
   amendment's activation height and runs fourteen days from this entry's `ts`. The layer is
   promoted at C1b's exit. A window that fails is a precedent, fixed by a lawful change and
   followed by a new pre-stated window; it is never patched in place (§6).
3. **Maxim 1 in the kernel.** No party resolves its own forecast, judged by principal, not by key;
   reason code `self_judged`. With A2.2's `ts_decreased`, both implemented by C1a's installing
   push, the closed set of reason codes is fourteen.
4. **The price of this amendment is recorded.** A3 is the third amendment in eleven days. §12's
   guard on procedure growth applies: the C1a report counts object entries (forecasts and
   resolutions of world types) against procedure entries (every other entry) over the window, and
   a ratio above assize's 5 : 1 stops the layer and reports.
5. **Order of acts.** `decision transmute A3` first; the SPEC text and the code that implements the
   types and `ts_decreased` by one `push`; this `amend` immediately after that push, with the
   default `activate_at`. Between the `amend` and its height no `push` is lawful (SPEC §10.12).
   Nothing entered before the activation height counts toward C1a's window.
