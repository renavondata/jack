# Second cold read of Amendment A4 (v2) — PR #30

26 October 2026. Reader: Google `google/gemini-4-argon`, a different model family
from counsel. Reviewed branch `counsel-a4-text` at `eedf0b4` (`log.jsonl` seqs 0–62).
Attribution for Guy's commit: `Proposer: reviewer reviewer-2`.

Read in the requested order: `CHARTER.md` (including A1–A3), `transcripts/REVIEW-A4.md`
and `transcripts/REPLY-REVIEW-A4.md`, `SPEC.md` §§7–10 (and §§4–5 schemas),
`BRIEF-C1.md`, `transcripts/AMEND-A4.md` (v2), `transcripts/PREDECESSORS-20261026.md`,
`transcripts/LITERATURE-20261026.md`, `transcripts/COUNSEL-OPEN.md`, and `log.jsonl`.
No key was used and no other file was touched.

## Disposition of the first read's findings (`transcripts/REVIEW-A4.md`)

1. **Clause 1 — universal "measured rate" undefined; safety replay is not a production-log rate:** ANSWERED — Clause 1 restricts incumbents to classes with a pre-stated statistic in a brief in force (population, window, score) and makes safety a gate, never a comparison score.
2. **Clause 2 — exponentiated log-score difference $\exp(\sum D_i)$ is not a test supermartingale under the equal-expected-score null:** ANSWERED — Clause 2 replaces $\exp(\sum D_i)$ with the bounded-difference betting process $E_t = \prod (1 + \lambda_i D_i / B)$ ($B = \ln 999$, predictable $\lambda_i \in [0, 1)$), which is a valid non-negative supermartingale under $\mathbb{E}[D_i \mid \mathcal{F}_{i-1}] \le 0$.
3. **Clause 2 — confidence sequence at $\alpha$ plus test at $\alpha$ yields $\alpha + \delta$, not $\alpha$:** ANSWERED — Clause 2 runs both at $\alpha$ and explicitly records the combined guarantee as $2\alpha$ in the forecast.
4. **Clause 2 — blocking reversible replacements until $E_t \ge 1/\alpha$ conflicts with §2.4 ("priced and scored, never blocked"):** ANSWERED — Clause 3 replaces reversible incumbents immediately for the window and reverts them at window end only if the challenger did not win.
5. **Clause 3 — "founding text" lacked a decidable path/power predicate (A2.3) and claimed reach over external repositories:** ANSWERED — Clause 3 names the exact paths (`CHARTER.md`, `SPEC.md`, `LAW.md`, `judge/scope.json`, layer-opening `BRIEF-*.md`) and states that a repository founded outside `jack` is reached by record only as a §7 repair.
6. **Clause 3 — requiring an "unresolved" forecast admitted losing challengers and blocked a challenger already resolved 1:** NOT ANSWERED — Requiring a `challenger` forecast "that has resolved 1" fixes the resolved-winner case for forecasters and shadow clerks, but creates the converse deadlock for gated files (`CHARTER.md`, `SPEC.md`, `LAW.md`, `judge/scope.json`, `BRIEF-*.md`) that have no non-safety statistic in `BRIEF-C1.md` and cannot be scored in force before reaching `main`.
7. **Clause 4 — `PREDECESSORS-20261026.md` did not establish the six-repository owner-decision replacement claim (`credence-governor` adverse):** ANSWERED — Clause 4 drops the six-repository replacement-decision claim, notes `credence-governor`'s retired shadow as an exception, and narrows the claim to the absence of in-repo termination decisions.
8. **Clause 4 — universal founding gate unforced by a measurement:** ANSWERED — Clause 4 retracts the claim that predecessor measurements proved the gate works and prices the rule explicitly as a bet (`seq 53`, $p = 0.6$).
9. **Clause 5 — bootstrap not decidable from log entries alone, named `counsel` against §4 generality, added unforced categorical gates, and left C3 ambiguous:** NOT ANSWERED — Clause 5 removes the party name `counsel`, leaves C3's test untouched, and anchors promotion in `decision promote bootstrap`, but still requires recomputing "from the log alone" conditions that depend on prose in briefs, `transcripts/world-types.md`, and unlogged election draws.
10. **Clause 6 (v1) — lapse by firing-rate e-process had the wrong tail, no trial denominator, and conflated deterrence with uselessness:** ANSWERED — v2 deletes the firing-rate lapse rule (Clause 7 now states A4 is removed like any other amendment by `transmute` and `amend`).
11. **Clause 7 (v1, now Clause 6) — $\lambda_i$ plug-in not unique, "truncated strictly inside" undefined, and potential $\varepsilon$ constant:** ANSWERED — Clause 6 gives closed-form parameter-free formulas $\lambda_i = \max(0, (\hat{q}_i - p_0)/(p_0(1-p_0)))$ and $\lambda_i = \max(0, 2\hat{q}_i - 1)$ with Laplace $\hat{q}_i = (s_i + 1)/(n_i + 2) < 1$ strictly, eliminating any $\varepsilon$ constant (leaving only tie-breaking for $D_i = 0$ and the $p_0 = 1$ boundary from Clause 2's unpaired branch).
12. **Clause 8 — order of acts:** ANSWERED — Held in v1 and updated in v2 to include the second cold read.
13. **Question (iii) — an incumbent with rate 1 cannot lose:** NOT ANSWERED — Excluding safety as a score removes the safety-replay instance, but both branches of Clause 2 still admit unbeatable incumbents (an incumbent with zero failures in its reference sample has confidence-sequence upper bound $U_n = 1 \implies p_0 = 1$ in the unpaired branch; and a calibrated challenger on a skewed event with $\mathbb{E}[D_i] > 0$ but $\Pr(D_i > 0) \le 1/2$ has $\lambda_i = 0$ in the paired branch).

## Clause findings (v2)

### 1. Incumbents are what a brief has measured — HOLDS

Defining an incumbent by a brief-stated statistic (population of entries, window, and §6 liveness or value score), barring challenges to classes that have none, and treating safety replay as a gate rather than a comparison score are consistent with CHARTER §0, §2.2, and §6.

**Layer:** **text-only until C1b's installing push**, then **judge** (`safety_used_as_score`) and **clerk** (statistic computation).

### 2. Challengers — UNENFORCEABLE

The paired betting e-process $E_t = \prod_{i \le t} (1 + \lambda_i D_i / B)$ with $B = \ln 999$ and predictable $\lambda_i \in [0, 1)$ is a valid non-negative supermartingale under $H_0: \mathbb{E}[D_i \mid \mathcal{F}_{i-1}] \le 0$. However, the clause still cannot be deterministically and soundly enforced from its text:

1. **Unpaired confidence sequence unspecified and degenerates at zero failures:** Clause 2 sets $p_0$ to "the upper end of a confidence sequence for the incumbent's rate at the layer's $\alpha$" without naming the confidence sequence construction (Hoeffding, empirical Bernstein, inverted betting CS, etc. yield different upper bounds $U_n$). Worse, as shown in (iii) below, any valid $(1-\alpha)$ confidence sequence on $[0, 1]$ must return $U_n = 1$ whenever the incumbent has zero failures in its sample ($S_n = n$), which sets $p_0 = 1$, makes Clause 6's $\lambda_i$ divide by $p_0(1-p_0) = 0$, and makes $E_t \le 1 < 1/\alpha$ for every challenger.
2. **Paired sign-bet entrenches incumbents on skewed events:** Combined with Clause 6's $\lambda_i = \max(0, 2\hat{q}_i - 1)$ where $\hat{q}_i$ tracks the **sign** of $D_i$, any challenger that strictly beats the incumbent in expected log score ($\mathbb{E}[D_i] > 0$) while having $\Pr(D_i > 0) \le 1/2$ gets $\hat{q}_i \le 1/2 \implies \lambda_i = 0$ and can never move $E_t$ above $1$ (shown with a concrete witness and mutant in (iii) below).
3. **Score vs loss sign convention:** `BRIEF-C1.md` (§C1a Scoring) defines `jack score`'s figure as positive log-**loss** (`−[o·ln(p/1000) + (1−o)·ln(1−p/1000)]`, lower is better). Clause 2 defines $D_i$ as "the challenger's score minus the incumbent's on item *i*" with $\lambda_i \ge 0$ and null "the challenger's expected score is no better." Unless "score" is explicitly defined as negated log-loss ($\text{loss}_{\text{inc}} - \text{loss}_{\text{chal}}$), subtracting `jack score`'s figures inverts the test.

**Layer:** intended for the **clerk** (and **kernel** for `forecast`/`resolution` recognition), with no pin named for the statistical test itself and no pricing rule when the confidence sequence or sign-bet degenerates.

### 3. Reversible replacements are priced; irreversible ones are gated — CONTRADICTS

Immediate replacement of reversible incumbents for the window with reversion unless the challenger wins aligns with §2.4, and external repositories are now properly scoped as record-only §7 repairs. However, the mechanical gate on the trusted base and founding files conflicts with existing `SPEC.md`, `CHARTER.md`, and `BRIEF-C1.md` rules:

1. **Conflict with `SPEC.md` §10.1–10.2 on who may change `CHARTER.md`, `SPEC.md`, and `judge/scope.json`:**
   > A4.3: "a `push` that changes the trusted-base digest, or a proposal that changes `CHARTER.md`, `SPEC.md`, `LAW.md` or `judge/scope.json` or adds a `BRIEF-*.md` that opens a layer, is refused by the judge from C1b's installing push unless its body names a `challenger` forecast by the same party that has resolved 1 and whose `args` name the digest or file being entered"

   > `SPEC.md` §10.1: "**trusted_path** — the trusted-base digest of the proposal's head differs from trunk's, or `CHARTER.md` differs byte for byte. The digest is SHA-256 over `path ‖ 0x00 ‖ content ‖ 0x00` for every file under `kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and the file `SPEC.md` ... These files change only by Guy's `jack push`, recorded by a `push` entry (item 11)."

   > `SPEC.md` §10.2: "An amendment therefore lands as one push by Guy: the text appended to `CHARTER.md` and the `amend` entry appended to `log.jsonl`, together."

   Under `SPEC.md` §10.1, a `proposal` that touches `CHARTER.md`, `SPEC.md`, or `judge/scope.json` is unconditionally refused as `trusted_path`; those files never enter by `proposal`. Conversely, `CHARTER.md` changes on `main` via an `amend` entry, which is neither a `push` entry nor a `proposal` entry and therefore falls outside "a `push` ... or a proposal" (or, if treated as a proposal, is forbidden by §10.1).
2. **Conflict with `CHARTER.md` §2.2 (*lex non cogit ad impossibilia*), §6, and `BRIEF-C1.md` (failed-window fix and layer-opening briefs):**
   > A4.1–3: "a class with none [a pre-stated statistic in a brief in force] cannot be challenged or replaced until it has one. Safety (§6's replay) is a gate ... never the score" (A4.1); "entered before any text or code of the replacement reaches `main` ... A challenger wins when $E_t \ge 1/\alpha$ within its window" (A4.2); refused "unless its body names a `challenger` forecast by the same party that has resolved 1 and whose `args` name the digest or file being entered" (A4.3).

   > `CHARTER.md` §2.2: "The law looks forward and never commands the impossible". `CHARTER.md` §6 / `BRIEF-C1.md`: "A window fails if any criterion is unmet at its end, or if a trusted-base defect is found inside it ... the fix enters by a lawful change (`push`, or `transmute` and `amend`); a new window is pre-stated in this file before it opens".

   Neither `CHARTER.md` nor `BRIEF-C1.md` defines a non-safety §6 liveness or value statistic for `CHARTER.md`, `SPEC.md`, `LAW.md`, `judge/scope.json`, `BRIEF-*.md`, or the trusted base at its digest; and none of those files can accumulate $E_t \ge 1/\alpha$ on a live liveness or value statistic *before* its text or code reaches `main`. Requiring a `challenger` forecast already resolved 1 before any `push` or layer-opening `BRIEF-*.md` is admitted makes a trusted-base bug fix, a `LAW.md` update, or opening `BRIEF-C2.md` impossible once enforced.
3. **Timing conflict with Clause 5:**
   > A4.3: "is refused by the judge from C1b's installing push ... Until that push the rule binds by this text alone"

   > A4.5: "the bootstrap is complete at a `decision` of kind `promote` with subject `bootstrap` [at C2's exit] ... From that decision the foundation changes only by clauses 2 and 3."

   Clause 3 applies the gate immediately (by text now, and by the judge from C1b's installing push), whereas Clause 5 states that the foundation changes only by Clauses 2 and 3 *from* `decision promote bootstrap` after C2's exit.

**Layer:** **text-only until C1b's installing push**, then **judge** (`unwon_push_admitted`, `unwon_founding_admitted`, `safety_used_as_score`) and **clerk**.

### 4. The sovereign is bound, as a bet — HOLDS

Subjecting Guy's `push` and founding acts to the same self-check / judge rules as other parties follows CHARTER §2.4 (corollary), §7, and A2.6 (`SPEC.md` §10.11–14). Clause 4 retracts v1's unsupported causal history, states its narrower observation about `PREDECESSORS-20261026.md` (qualified in (i) below), and prices the rule explicitly as forecast seq 53 ($p = 0.6$).

**Layer:** **text-only until C1b's installing push**, then **judge** (via the self-check and proposal checks of Clause 3); external repositories by record only as a §7 repair.

### 5. The bootstrap, decidable — UNENFORCEABLE

Anchoring the bootstrap exit in a `decision` entry of kind `promote` with subject `bootstrap` gives the event a log entry (`SPEC.md` §5 allows `kind: "promote"` and `subject: "bootstrap"`), drops the party-specific exclusion of `counsel` (§4), and leaves C3's test intact. However, the requirement "whose body carries, and whose checks recompute from the log alone" cannot be satisfied for three of its five conditions (detailed in (ii) below):
- whether a world type is one "whose brief declares its outcomes resolved by a mechanism outside the repository" is a semantic property of brief prose outside `log.jsonl`;
- whether an entry is an "object" entry for §12's bound depends in `BRIEF-C1.md` on membership in `transcripts/world-types.md`, a file outside `log.jsonl`;
- whether "every `invite` entry of the last window names the proposer the election drew" cannot be recomputed from `log.jsonl` alone when the election rule lives in code outside the log and draws at random from weights (`LITERATURE-20261026.md` row 4) without a logged seed and weight vector.

As noted under Clause 3, its final sentence ("From that decision the foundation changes only by clauses 2 and 3") also contradicts Clause 3's activation of those same gates at C1b's installing push (and by text immediately).

**Layer:** intended for **judge** / **clerk** at `decision promote bootstrap`, with no named pin and no pricing fallback for the non-log-decidable conjuncts.

### 6. The wealth is never reset, and the bet is mechanical — HOLDS

Continuing $E_t$ across failed windows on the same statistic under the same null and fixing $\lambda_i = \max(0, (\hat{q}_i - p_0)/(p_0(1 - p_0)))$ for binary outcomes and $\lambda_i = \max(0, 2\hat{q}_i - 1)$ for bounded differences with Laplace $\hat{q}_i = (s_i + 1)/(n_i + 2)$ over the prefix $1..i-1$ is a valid, parameter-free test supermartingale construction under $H_0$ for interior $p_0 \in (0, 1)$ (proved in (iv) below). Reading "the sign of $D_i$" as the binary indicator $\mathbf{1}\{D_j > 0\}$ over the $i-1$ prior items makes the formula deterministic; the power failure it induces when $\Pr(D_i > 0) \le 1/2$ is a defect of Clause 2's challenger test (shown in (iii)), not of supermartingale validity under $H_0$.

**Layer:** **clerk** / scoring tools (outside the kernel per `BRIEF-C1.md`'s refusal list; text-only until C1b).

### 7. The price of this amendment is recorded — HOLDS

Recording A4 as the fourth amendment in thirteen days under §12's 5 : 1 procedure-to-object guard, citing forecasts seq 53 ($p = 0.6$) and seq 60 ($p = 0.5$), and removing A4 only by `transmute` and `amend` (with no custom firing-rate lapse rule) matches CHARTER §3, §12, A2.1, A2.7, and A3.4.

**Layer:** **kernel** and **judge** for `transmute` and `amend` (`SPEC.md` §§7, 10.2, 10.12–13); **clerk** / layer report for §12's ratio and `jack score` for seqs 53 and 60.

### 8. Order of acts — HOLDS

Requiring the second cold read by another model family, `decision transmute A4`, `amend A4` with default `activate_at`, no `push` between `amend` and `activate_at`, and deferring Clause 3's three pins (`unwon_push_admitted`, `unwon_founding_admitted`, `safety_used_as_score`) to C1b's installing push is consistent with A1.7, A2.4, A2.7, and `SPEC.md` §§7, 10.12–13. (Note: "are listed in `BRIEF-C1.md`'s C1b section" holds prospectively when C1b's brief text is written at C1a's exit per `BRIEF-C1.md` line 272; `BRIEF-C1.md` at `eedf0b4` does not yet list those three pin names.)

**Layer:** **kernel** (`amend` schema and `activate_at`), **judge** (`amend_untransmuted`, `push_during_amendment`, `charter_mismatch`), and **text-only until C1b's installing push** for the three named pins.

## The four specific questions

### (i) Does the evidence file support clause 4's factual claim?

1. **Against the first version's claim (that each predecessor was replaced by the owner's decision with the reason written only in the successor): No.** `transcripts/PREDECESSORS-20261026.md` does not show that conjunction for any of the repositories in the file:
   - `proplang`, `wald-charter`, `wald`, `wald-arena`, `life-agent`, `tannen`, `credence`: the file contains no record of an owner's decision replacing the repository.
   - `credence-governor`: the file shows an explicit in-repo stopping reason (`incumbent FAILS the waste bar (6.50% vs 0.05%)`, `demoted from enforcement because it blocked too often`, shadow retired in `docs/governance-roadmap.md` and `docs/membrane-shadow.md` §6.3), contradicting "written only in the successor."
   - `wald-arena`: was not replaced for failure; its pre-registered brief 002 exit was "Met as written."
   - `assize`: records the owner's decision (`wish #341`, an issue in `renavondata/assize`), while the evidence file does not prove that the reason is absent from `assize`.
2. **Against v2's narrowed claim ("of the eight predecessors read, none records in its own repository the decision that ended it (credence-governor's retired shadow the honest exception), and the reason for this repository is written in this repository and not in assize"):** v2 corrects the `credence-governor` exception and drops the claim that an owner replacement decision is shown for the others, but the file still does not show the narrowed claim for **`wald-arena`** (one of the eight repositories in `PREDECESSORS-20261026.md`, whose exit is recorded in-repo as "Met as written" rather than ended by an unrecorded decision) or for **`assize`** (which records the ending decision in-repo as owner's `wish #341`, even though the fuller analysis is in `jack`'s `CHARTER.md` §1).

### (ii) Is clause 5's bootstrap condition decidable from log entries alone, and does any part of it smuggle in a constant not on the charter's admitted list (α, windows, p₀, attack list, budget)?

1. **Not decidable from log entries alone.** While v2 records the bootstrap at a `decision` entry (`kind: "promote"`, `subject: "bootstrap"`) whose body carries the summary figures, a check that must "recompute from the log alone" cannot verify three conjuncts from `log.jsonl`:
   - *"at least one world of a type whose brief declares its outcomes resolved by a mechanism outside the repository (C2's statistic, defined in C2's brief)"*: briefs (`BRIEF-*.md`) and `transcripts/world-types.md` are repository files outside `log.jsonl`, and whether a brief's prose declares an external resolution mechanism is not a decidable predicate on log entries;
   - *"procedure to object in the last window is within §12's bound"*: under `BRIEF-C1.md` (§C1a World types and Pre-stated criteria), a `forecast` or `resolution` counts as an object entry only if its `type` is present in `transcripts/world-types.md`, which is outside `log.jsonl`;
   - *"every `invite` entry of the last window names the proposer the election drew"*: the election is an entrant in code (`CHARTER.md` §5), and under randomized/bandit drawing (`LITERATURE-20261026.md` row 4) the log alone does not determine which proposer "the election drew" unless the weight calculation and random seed/draw are themselves entries in `log.jsonl`.
   (In addition, $\alpha$, $p_0$, and the window boundaries must be read from `decision` entries on the log rather than only from `BRIEF-*.md` for $E_t \ge 1/\alpha$ to be recomputed from `log.jsonl` alone.)
2. **Admitted constants:** v2 removes the party-specific `counsel` ban. The `5 : 1` procedure-to-object bound is already in CHARTER §12 and A3.4. The remaining quantities in Clause 5 ("at least one world", "every `invite` entry", "no `challenger` forecast is unresolved") are existential/universal quantifiers ($1, \forall, 0$), not new numerical tuning constants outside $(\alpha, \text{windows}, p_0, \text{attack list}, \text{budget})$—though requiring zero unresolved `challenger` forecasts allows any party with `forecast` power to block `bootstrap` promotion by entering a new `challenger` forecast just before the check.

### (iii) Is there a reading of clause 2 under which the incumbent can never lose (a green that cannot fail)? If so, state the mutant that would show it.

**Yes, in both the paired and unpaired branches of Clause 2:**

1. **Paired branch (combined with Clause 6's sign-based $\lambda_i$):**
   Clause 2 tests paired score differences by $E_t = \prod_{i \le t} (1 + \lambda_i D_i / B)$ ($B = \ln 999$), and Clause 6 defines $\lambda_i = \max(0, 2\hat{q}_i - 1)$ where $\hat{q}_i = (s_i + 1)/(n_i + 2)$ is the Laplace estimate on **the sign of $D_i$**.
   Under a strictly proper scoring rule like log-loss, a calibrated challenger regularly beats an overconfident incumbent in expected score ($\mathbb{E}[D_i] > 0$) while having $D_i > 0$ on **fewer than half** of the items ($\Pr(D_i > 0) < 1/2$). Specifically, let outcomes $Y_i \stackrel{\text{i.i.d.}}{\sim} \text{Bernoulli}(0.2)$, let the incumbent predict $p_{\text{inc}} = 50$ ($0.05$), and let the challenger predict the true probability $p_{\text{chal}} = 200$ ($0.20$), with $D_i = \text{loss}_{\text{inc}}(Y_i) - \text{loss}_{\text{chal}}(Y_i)$:
   - When $Y_i = 1$ (probability $0.20$): $D_i = \ln(0.20) - \ln(0.05) = +1.3863 > 0$.
   - When $Y_i = 0$ (probability $0.80$): $D_i = \ln(0.80) - \ln(0.95) = -0.1719 < 0$.
   - Expected score gain per item: $\mathbb{E}[D_i] = 0.20(1.3863) + 0.80(-0.1719) = +0.1398 > 0$ (the challenger is the true distribution).
   - Yet $\Pr(D_i > 0) = 0.20 < 1/2$. At $i = 1$, $\hat{q}_1 = (0+1)/(0+2) = 1/2 \implies \lambda_1 = \max(0, 2(1/2) - 1) = 0$. Whenever the prefix has $s_i \le n_i / 2$ (which holds with probability $0.80$ at $i = 2$ and almost surely for large $i$), $\hat{q}_i \le 1/2 \implies \lambda_i = 0$, so $E_t = 1 < 20$ forever.
   - **Mutant (`paired_challenger_sign_minority_entrenched`):** in the paired challenger evaluator, replace the wealth update with $E_t = 1$ (or return `keep_incumbent`) whenever $s_i \le n_i / 2$. On any deterministic or seeded fixture where $Y_i \in \{0, 1\}$ has $20\%$ ones, $p_{\text{inc}} = 50$, and $p_{\text{chal}} = 200$ with $s_i \le n_i / 2$ along the prefix, both the unmutated Clause 2/6 rule and the mutant produce $E_t = 1$ and never promote the true forecaster.
2. **Unpaired branch (incumbent with zero failures in its reference sample):**
   Clause 2 sets $p_0$ to "the upper end of a confidence sequence for the incumbent's rate at the layer's $\alpha$." For **any** valid $(1-\alpha)$ confidence sequence $[L_n, U_n]$ for a Bernoulli mean $p \in [0, 1]$, when the incumbent's observed sample has zero failures ($S_n = n$, e.g. $20/20$ obligations completed without Guy's repair), coverage at $p = 1$ ($\Pr_{p=1}(\forall n,\, S_n = n) = 1$) forces $U_n(1, \dots, 1) = 1$. Setting $p_0 = U_n = 1$ makes every factor in §6's e-process satisfy $1 + \lambda_i(Y_i - 1) \le 1$ (so $E_t \le 1 < 1/\alpha$ for every challenger outcome sequence) and makes Clause 6's $\lambda_i = \max(0, (\hat{q}_i - p_0)/(p_0(1-p_0)))$ divide by $p_0(1 - p_0) = 0$.
   - **Mutant (`unpaired_zero_failure_incumbent_entrenched`):** in the unpaired challenger evaluator, return `keep_incumbent` whenever the incumbent's failure count in its window is $0$, without reading the challenger's outcomes. No challenger trace can kill this mutant because $p_0 = 1$ forces $E_t \le 1$.

### (iv) Clause 6: is the continued-wealth rule and the truncated prequential plug-in for λ a valid test supermartingale construction under H0, and is anything in it a constant not on the admitted list?

1. **Valid test supermartingale under $H_0$: Yes, for interior $p_0 \in (0, 1)$ and bounded differences $D_i \in [-B, B]$.**
   - **Binary statistic ($0 < p_0 < 1$):** With $s_i, n_i$ counting successes and trials in the prefix $1..i-1$, $\hat{q}_i = (s_i + 1)/(n_i + 2)$ is $\mathcal{F}_{i-1}$-measurable and satisfies $0 < \hat{q}_i < 1$ strictly for every finite $n_i \ge 0$. Therefore:
     $$\lambda_i = \max\!\left(0, \frac{\hat{q}_i - p_0}{p_0(1 - p_0)}\right) = \frac{1}{p_0}\max\!\left(0, 1 - \frac{1 - \hat{q}_i}{1 - p_0}\right) \in \left[0, \frac{1}{p_0}\right)$$
     strictly. Each factor $1 + \lambda_i(Y_i - p_0)$ is strictly positive (when $\hat{q}_i > p_0$, it equals the prequential plug-in likelihood ratio $\hat{q}_i/p_0$ for $Y_i = 1$ and $(1-\hat{q}_i)/(1-p_0)$ for $Y_i = 0$), and under $H_0: \mathbb{E}[Y_i \mid \mathcal{F}_{i-1}] \le p_0$,
     $$\mathbb{E}[E_i \mid \mathcal{F}_{i-1}] = E_{i-1}\bigl(1 + \lambda_i(\mathbb{E}[Y_i \mid \mathcal{F}_{i-1}] - p_0)\bigr) \le E_{i-1}.$$
   - **Bounded difference ($D_i \in [-B, B]$):** Because $\hat{q}_i \in (0, 1)$ is predictable, $\lambda_i = \max(0, 2\hat{q}_i - 1) \in [0, 1)$ strictly. Thus $1 + \lambda_i D_i / B \ge 1 - \lambda_i > 0$, and under $H_0: \mathbb{E}[D_i \mid \mathcal{F}_{i-1}] \le 0$, $\mathbb{E}[E_i \mid \mathcal{F}_{i-1}] = E_{i-1}(1 + (\lambda_i / B)\mathbb{E}[D_i \mid \mathcal{F}_{i-1}]) \le E_{i-1}$.
   - **Continued wealth across windows:** Carrying $E_t$ forward across window boundaries on the same statistic under the same $H_0$ maintains a single non-negative supermartingale with $E_0 = 1$, so Ville's inequality $\Pr_{H_0}(\sup_{t \ge 1} E_t \ge 1/\alpha) \le \alpha$ holds at any stopping time without splitting $\alpha$.
   - **Boundary and tie caveats:** (a) if $p_0 = 1$ enters from Clause 2's confidence sequence, $p_0(1 - p_0) = 0$; (b) when $D_i = 0$, "the sign of $D_i$" must be fixed as $\mathbf{1}\{D_j > 0\}$ (or ties excluded) so two implementations do not diverge; (c) validity under $H_0$ does not imply power under $H_1$ when $\mathbb{E}[D_i] > 0$ and $\Pr(D_i > 0) \le 1/2$, as shown in (iii).
2. **Constants not on the admitted list: None.** Because $\hat{q}_i = (s_i + 1)/(n_i + 2) < 1$ holds algebraically for all finite $n_i$, the strict upper bounds $\lambda_i < 1/p_0$ and $\lambda_i < 1$ hold without introducing an $\varepsilon$ truncation constant. The Laplace $(+1, +2)$ pseudocounts are already in `BRIEF-C1.md` for base-rate scoring, and $B = \ln 999$ is fixed by `SPEC.md` §5's per-mille domain $1..999$.

VERDICT: BLOCK — P(cited or refuses something within 90 days | amended as written) = 0.85
