## Amendment A4: §6 corrected (26 October 2026)

Counsel's text, third version, cut to what two cold reads of two families left standing
(`transcripts/REVIEW-A4.md`, `transcripts/REVIEW-A4-v2.md`; replies in `transcripts/REPLY-REVIEW-A4.md`
and `transcripts/REPLY-REVIEW-A4-v2.md`). Recorded by `amend` A4 under SPEC §7 after a `decision`
of kind `transmute` naming it, in force from its `activate_at`. Appended; overrides §6 where they
conflict. Forced by `transcripts/LITERATURE-20261026.md` item 2: §6 as written restarts the
e-process at each new window, which is *k* draws at one bound. The rules the earlier versions
tried to add — incumbents and challengers, a gate on retirements, a bootstrap predicate — go to
C1b's brief as rules of that layer, with pins, and return to this charter by amendment only
after one of them has refused or decided an act.

1. **The wealth is never reset.** A window that fails and is followed by a new one continues the
   same wealth process on the same statistic under the same null; *E* is never set back to 1 and
   no α is split. Ville's inequality then holds for the whole sequence at the layer's α.
2. **p₀ is committed, never estimated from the window it judges.** It is a constant on the
   admitted list, committed before the window opens (§6), taken from the incumbent's series as
   the briefs already provide, and never the incumbent's own rate in the window under test.
3. **The bet is a function of the prefix.** For a binary statistic with 0 < p₀ < 1,
   λᵢ = max(0, (q̂ᵢ − p₀) / (p₀(1 − p₀))), q̂ᵢ = (sᵢ + 1)/(nᵢ + 2) the Laplace estimate over the
   statistic's outcomes since the layer's first window. q̂ᵢ < 1 strictly, so λᵢ < 1/p₀ with no
   further constant; λᵢ is determined by the prefix, and no λ is entered after its outcome. Each
   factor 1 + λᵢ(Yᵢ − p₀) is positive and, under E[Yᵢ | past] ≤ p₀, has conditional expectation
   at most 1 (REVIEW-A4-v2 (iv)).
4. **Comparisons of two forecasters are bets on a bounded difference.** Dᵢ = (the incumbent's log
   loss − the challenger's log loss) on item *i*, positive when the challenger did better, bounded
   by B = ln 999 under per-mille clipping; *E_t* = ∏(1 + λᵢ Dᵢ / B) with
   λᵢ = min(max(0, m₁ᵢ / m₂ᵢ), 1 − 1/(nᵢ + 2)), m₁ᵢ and m₂ᵢ the mean of Dⱼ/B and of (Dⱼ/B)² over the
   prior items together with two pseudo-items at +B and −B. λᵢ ∈ [0, 1) and predictable; under
   E[Dᵢ | past] ≤ 0 the process is a test supermartingale. An exponentiated sum of score
   differences is not one under that null and is not used.
5. **Price and order.** A4 is the fourth amendment in thirteen days; §12's guard applies. Its
   forecast is seq 60 (p 0.5 that it is cited or refuses an act by 26 January 2027). Order:
   `decision transmute A4`; this `amend` with the default `activate_at`; no `push` between the
   `amend` and its height (SPEC §10.12). Two cold reads are on the record; a third is Guy's to
   require or waive.
