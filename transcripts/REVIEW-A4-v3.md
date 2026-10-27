# Third cold read of Amendment A4 (v3) — PR #30

27 October 2026. Reader: Google `google/gemini-4-argon`, a different model family from counsel. Reviewed branch `counsel-a4-text` at `adc3809` (`log.jsonl` seqs 0–63). Attribution for Guy's commit: `Proposer: reviewer reviewer-2`.

Read in the requested order: `CHARTER.md` (including A1–A3; §6 closely), `transcripts/REVIEW-A4-v2.md` §(iv) and question (iii), `transcripts/REPLY-REVIEW-A4-v2.md`, `transcripts/AMEND-A4.md` (v3), and `transcripts/LITERATURE-20261026.md` item 2, checked against `SPEC.md` §§7–10 and `BRIEF-C1.md`.

## Clause findings

1. **The wealth is never reset — HOLDS.** Continuing $E_t$ across failed windows on the same statistic under the same null preserves a single non-negative supermartingale with $E_0 = 1$. Ville's inequality therefore controls the supremum over the whole sequence at the layer's $\alpha$ without error-splitting (`LITERATURE-20261026.md` item 2).
2. **$p_0$ is committed, never estimated from the window it judges — HOLDS.** Fixing $p_0$ as a pre-committed constant from the prior series matches CHARTER §6 and §10.3 and removes both the unmodelled baseline uncertainty and the zero-failure $U_n = 1$ degeneracy convicted in v2.
3. **The bet is a function of the prefix — HOLDS.** With $0 < p_0 < 1$ and Laplace $\hat{q}_i = (s_i + 1)/(n_i + 2)$ over the prefix since the layer's first window, $\hat{q}_i \in (0, 1)$ strictly and $\lambda_i = \max(0, (\hat{q}_i - p_0)/(p_0(1 - p_0))) \in [0, 1/p_0)$ is predictable with no truncation constant.
4. **Comparisons of two forecasters are bets on a bounded difference — HOLDS.** Defining $D_i$ as the incumbent's log loss minus the challenger's matches `BRIEF-C1.md`'s positive log-loss convention, and setting $\lambda_i = \min(\max(0, m_{1i}/m_{2i}), 1 - 1/(n_i + 2))$ with two pseudo-items at $+B$ and $-B$ ($B = \ln 999$) keeps $\lambda_i \in [0, 1)$ predictable while restoring power when $\mathbb{E}[D_i] > 0$ and $\Pr(D_i > 0) \le 1/2$.
5. **Price and order — HOLDS.** Recording A4 under §12's 5 : 1 guard, citing forecast seq 60, and following `decision transmute A4` then `amend A4` with no intervening `push` comply with A2.7, A3.4, and `SPEC.md` §§7, 10.12–13. (On `log.jsonl`, seq 60's immutable claim text still names "A4 clause 3 … founding text or trusted-base push" from v1.)

## Questions (a)–(d)

**(a) Test-supermartingale validity of §§1, 3 and 4.** Each of §§1, 3 and 4 is a valid test-supermartingale statement under its stated null, as written; no sentence fails:
- **§1:** Multiplying new non-negative factors of conditional expectation at most $1$ onto the existing $\mathcal{F}_{i-1}$-measurable wealth across window boundaries keeps $(E_t)_{t \ge 0}$ a single non-negative supermartingale with $E_0 = 1$, so $\Pr_{H_0}(\sup_{t \ge 1} E_t \ge 1/\alpha) \le \alpha$.
- **§3:** Because $0 < \hat{q}_i \le (n_i + 1)/(n_i + 2) < 1$, $\lambda_i \in [0, 1/p_0)$ is $\mathcal{F}_{i-1}$-measurable, $1 + \lambda_i(Y_i - p_0) \ge 1 - \lambda_i p_0 > 0$, and under $\mathbb{E}[Y_i \mid \text{past}] \le p_0$, $\mathbb{E}[1 + \lambda_i(Y_i - p_0) \mid \text{past}] \le 1$.
- **§4:** Under `SPEC.md` §5's per-mille range $1..999$, $|D_i| \le \ln 999 = B$. The two pseudo-items at $\pm B$ ensure $m_{2i} = (2 + \sum_{j < i}(D_j/B)^2)/(n_i + 2) \ge 2/(n_i + 2) > 0$, so $\lambda_i \in [0, 1 - 1/(n_i + 2)] \subset [0, 1)$ is well-defined and predictable, $1 + \lambda_i D_i / B \ge 1/(n_i + 2) > 0$, and under $\mathbb{E}[D_i \mid \text{past}] \le 0$, $\mathbb{E}[1 + \lambda_i D_i / B \mid \text{past}] \le 1$.

**(b) Extra constants or undecidable rules.** None. $B = \ln 999$ is fixed by `SPEC.md` §5, the Laplace $(+1, +2)$ pseudocounts are in `BRIEF-C1.md`, and the two symmetric pseudo-items at $\pm B$ with cap $1 - 1/(n_i + 2)$ avoid any tuning constant $\varepsilon$. §§1–4 are closed-form arithmetic on recorded prefix outcomes for the clerk/scoring tools outside the kernel; §5 uses existing kernel and judge checks.

**(c) Conflicts with CHARTER.md, SPEC §§7–10 or BRIEF-C1.md.** None. A4 explicitly overrides §6's window-restart wording, aligns $D_i$'s sign with `BRIEF-C1.md`'s log-loss definition, keeps scoring outside the kernel per `BRIEF-C1.md`'s refusal list, and leaves `SPEC.md` §§7–10 intact.

**(d) Anything unexamined by the two earlier reads requiring a further read.** Only §4's replacement of v2's sign-based $\lambda_i$ with $\min(\max(0, m_{1i}/m_{2i}), 1 - 1/(n_i + 2))$ under $\pm B$ pseudo-items is new relative to v1–v2; it is verified in (a)–(b) above and requires no further read.

VERDICT: ACCEPT — p(this text, amended as written, is cited by or refuses at least one act within 90 days) = 0.75
