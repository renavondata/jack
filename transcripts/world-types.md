# World types and their resolvers

A forecast is world-typed iff its `type` begins `world.` **and** the type is named here before the
first forecast of that type is entered (BRIEF-C1.md). Each paragraph says what outcome 1 means, what
the evidence file is, and who may resolve. Counsel's text; amended by proposal, never retroactively
for forecasts already entered under a type.

## `world.screen`
A claim about one of the nine candidate screens of 25 October 2026 (registry entity resolution;
pipeline linkage; regulatory obligations; HKJC calibration; HKEX disclosure anomalies; FOI outcomes;
citation verification; security triage; operational alerting). Outcome 1 iff the screen's report,
written to the screen's own pre-registered protocol, states the forecast's condition met in so many
words (for example "the bare model's wrong answers were stated at confidence ≥ 0.9 in at least half
the cases"). Evidence: the report file. Resolver: any party with `resolution` power other than the
forecaster.

## `world.ximenes`
A claim about a measured result in `gfrmin/ximenes` (a brief's headline, a paired comparison, a
spend). Outcome 1 iff the cited `reports/` file in that repository, at a named commit, states it.
Evidence: that file at that commit, copied. Resolver: as above.

## `world.assize`
A claim about the state of `renavondata/assize` (a verdict line present, an issue closed, a label
applied, a price figure). Outcome 1 iff the GitHub REST response for the named object, fetched after
`resolves_by` and saved, shows it. Evidence: the saved response. Resolver: as above.

## `world.hkjc`
A claim about the outcome of racing run by the Hong Kong Jockey Club: a named runner's finishing
position, how many races at a meeting the market favourite wins, a dividend, or the settled return
of a published set of picks. Named in this file on 2026-10-28, in the commit before the first forecast of the type was entered
on the same branch, with the base rates it is forecast against in
`transcripts/HKJC-EPROCESS-20261028.md`. Terms: a *meeting* is one HKJC fixture, identified by its
date and racecourse; "the first (second) meeting after this entry" means the first (second) fixture
whose first race is scheduled after the forecast's `ts`, by the HKJC's published fixture list; the
*races at a meeting* are the races actually run there (an abandoned or voided race is not one); the
*favourite* in a race is the runner with the shortest final WIN odds as the HKJC's result shows them,
and a dead-heat for shortest odds counts if any of the tied runners wins; a runner's *final WIN odds*
are the HKJC's final WIN odds for it, which for the winner are its WIN dividend per ten dollars
divided by ten; *hkjc.guru's published picks for a meeting* are the rows its proofing ledger
(`https://hkjc.guru/proofing`) froze for that meeting's races before they were run, and their *settled
flat return* is the sum over those rows of (stake × WIN dividend per dollar if the runner won, else
zero) minus the sum of stakes, as the ledger settles it; a meeting for which the ledger published
nothing has a settled flat return of zero, which is not positive. Outcome 1 iff the HKJC's official
results for the meeting (the Local Results pages of `racing.hkjc.com`, one per race) — or, for a claim
about hkjc.guru's picks, the settled proofing ledger as `hkjc.guru/proofing` shows it — fetched
after the meeting and saved, show the forecast's condition met. Evidence: the saved pages. The
market's own forecast is the incumbent of this type (A4 clause 4): a forecast may carry the market's
implied probability of its claim in `args` as `market_p` (per mille) with its source and time, and the
base rate it was forecast against as `base_rate`. Resolver: as above.

**Reading of `world.hkjc`'s "settled flat return" (28 October 2026, after `transcripts/REVIEWER-HKJC-20261028.md`
findings 1 and 2; a reading of the text above, not a change to it, so it binds the forecasts already entered).**
The operative definition is the formula and the words "as the ledger settles it": the return is at the ledger's
own stakes (its 1, 2 and 3 unit tiers), with each row's settled payout as the ledger records it, so a scratched
runner settled as a refund contributes zero, not a loss. The word "flat" in the term's name is a misnomer and
means nothing further. The base rate counsel forecast against (0.273 over 615 meetings) was computed at one
unit per pick; at the ledger's tiers the same seven seasons give 0.250 (0.188 over the last two), and the two
signs disagree at one meeting in seventeen — the forecasts stand as entered, and the discrepancy is theirs to
bear. `/proofing` shows the fifty most recently settled picks, so a meeting's evidence is fetched and saved
within a few days of its settlement, not at `resolves_by`; the ledger's R2 mirror and `ledger.sqlite` on the
host hold the rows after the page has rolled on, and either serves as evidence when saved.
