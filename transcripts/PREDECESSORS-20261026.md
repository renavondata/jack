# The seven predecessors, read cold (26 October 2026)

Counsel's evidence for Amendment A4. A cold read, by a session of the same family as counsel, of
the public repositories that preceded jack: `gfrmin/proplang`, `gfrmin/wald-charter`, `gfrmin/wald`,
`gfrmin/wald-arena`, `gfrmin/life-agent`, `gfrmin/tannen`, `gfrmin/credence`,
`gfrmin/credence-governor`, with assize read from this charter's §1. Shallow clones; in-repo text
and `git log -1` only; nothing executed. Paths are relative to each repository. Quotations are
verbatim; where a repository lacks a thing the entry says "none found". The question put to the
reader was: what did each state as its exit criterion, was it met, why was it superseded, and what
did the owner's time cost. The reader's cross-repo synthesis is reproduced unedited at the end.

## proplang (2026-07-04 → 2026-09-20, ~11 weeks)
- Design: a minimal Haskell language in which "the alphabet IS the prior, deliberation is a
  sentence, and the world — never the language — supplies every constant" (`KERNEL.md`); frozen
  oracles under `test*/` and `audit/`, hashed in `MANIFEST.sha256` and signed before
  implementation (`CLAUDE.md`, "Two-phase build").
- Exit: brief §12's four acceptance tests and six deliverables; "definition of done — all of
  them, no partial credit" (`CLAUDE.md`). Declared met at `writeup-freeze`, 2026-07-07 ("The
  roadmap terminates here", `WRITEUP.md` §5, §9); re-opened 07-12 and 07-25; a second terminus
  "AFTER 5 THE ROADMAP TERMINATES" (`EXACT_PLAN.md` §13.0); a third sitting ~09-05; then "Three
  things have arrived against that terminus" (`chooseeu-sitting/CONFERRAL.md` I.1). At HEAD
  `PAPER.md` reads "DRAFT — builder-authored, not frozen".
- Lessons, as protocol amendments: "the protocol the project ends with is the one its own failures
  wrote" (`WRITEUP.md` §8). `OBLIGATIONS.md`: "the composite read as 'mostly done' and the
  parenthetical evaporated". `CONFERRAL.md` F4: five open issues "all disposed at ONE sitting …
  One of the author's own posted comments is now false and is actively misinstructing a consumer."
- Governance: signed manifest; two SSH keys with recorded delegations; seven gates; mutant pools
  M56–M98 with kill matrices; 986 mentions of "sitting"; 35 distinct `R-` ruling ids.
- Measured: synthetic worlds and one stdin transcript; the one field reading "NOT MEASURED on 95k
  live events … no engine passes the registered loss bar" (`EXACT_PLAN.md` §13.0). No money.
  52,982 lines of .md against 10,899 of .hs (3,105 in `src/`).
- Owner's time: "ALL open issues must be closed when dealt with" (`DOCKET.md`, 2026-09-19); "the
  overloaded docket that manufactures the defect the next round convicts" (OB-26).

## wald-charter (2026-09-20 → 2026-10-02)
- Design: the law as signed pages with reference checkers in exact `Fraction`s and a kit that
  judges any implementation; "a signed law, an external kit that judges any implementation, and a
  builder that cannot touch either. Protect that above everything." (`HANDOFF.md` §1).
- Exit: none terminal by design — "Amendment. Only by a new signed version, carrying the
  measurement that forced it." (`CHARTER.md` §8); signing stop rule "sign when a session finds
  nothing reproducible in the page's substantive categories" (`HANDOFF.md` §4.4); "Each stage must
  be useful alone and forced by a measurement" (§1).
- On its predecessor: credence's "builder held the pen on the reasoner, CI never ran the engine's
  tests, arithmetic was Float64, and its router learned a reliability with no ground truth"
  (`HANDOFF.md` §1); "One had no verdict; the other had a verdict that carried no information."
  (`CHARTER-v0.2.md` §0). "Attackers find the author's errors far more often than the kernel's"
  (§7); two pages took "fifteen and eight drafts … to finding problems a machine could have found".
- Measured against money and hosts: arena $38.40 plus ~$26 of droplet; Renavon World 20,736
  states; the owner's full World "24.9 M states … out of reach" (`HANDOFF.md` §5). 1,005 lines of
  signed law, 8,507 of reference and kit, zero object code.

## wald (briefs 001–014, ~2026-09-20 → 2026-10-02)
- "A brief is done when the `cage` check is green on your pull request" (`CLAUDE.md`); CI on an
  unseen seed; met for fourteen briefs, releases v0.1.0–v0.2.3. `QUESTIONS.md` (18 entries): "The
  author amends; I do not guess." Builder barred from `cage/`, `.github/`, `CODEOWNERS`.
  "a performance problem is a stop, not an approximation" (`HANDOFF.md` §4.8).

## wald-arena (2026-09-14 → 2026-10-01)
- Exit: "Done when the scoreboard prints … the four pre-registered claims (QUESTIONS.md, 2.13)
  are each marked held or missed. Nothing reaches a frozen model until the pre-registration is
  ruled" (`briefs/002-omniscience.md`). **Met as written**: 250 unseen questions, Δ ± 2 SE; two
  claims held, two part-missed, one "stated in advance as underpowered"; the owner hand-audited
  the grader 56/60. "a baseline that wins is reported as winning": the better single model +56.7
  against wald +36.0. $38.40 of logged spend. 5,193 lines of Python against 3,355 of .md.

## life-agent (2026-05-23 → 2026-10-01; reset 2026-09-19; prune 2026-09-30)
- Exit: "MVP = reusable by a stranger"; J4: "the exit test, which counts calendar days carrying
  live traffic, has not started counting. The decision log of record holds no live row after
  2026-09-20" (`ROADMAP.md`).
- Lessons: the "unification arc" archived (93 reports, 19 conferrals, "60+ audit instruments");
  "158 ruling references across ~30 documents with no index, so asking the owner cost less than
  searching" (`archive/docs/unification/RULINGS.md`); M-20 "Fourth instance in four checkpoints of
  building on an unverified premise"; "MODEL.md promised that a document marked SEALED could never
  reach a disclosing rung; nothing in the code marked or checked it"; the unified ledger deleted
  because "nothing read the ledger but its own reconciliation" (`rulings.md`, `CHANGELOG.md`).
- Measured: owner set 41/0/37, U/q +0.504 at $0.0114 a question; live stream 1,882 rows, last
  2026-08-31. src 22,411 / tests 32,206 / .md 42,532; `archive/` 67,602 lines in 246 files.
- "Engines are upstream … Each enters when it beats the host on the board or catches a defect a
  test here cannot" (`CLAUDE.md`).

## tannen (2026-08-24 → 2026-09-29, v0.5.1)
- Design: a content-addressed pipeline kernel; "Most of this repository is not the kernel. It is
  the machinery that decides what may enter the kernel" (`README.md`).
- Exit: "implementation ends when the frozen suite is green"; M5 = "one Renavon vertical,
  byte-identical vs production on frozen inputs … (production bugs found = wins)" (`BRIEF.md` §8).
  M5 closed 2026-09-19; D0270: "M5 attests that tannen reproduces production's code; it cannot
  surface a production defect, and 'production bugs found' is out of its reach by construction."
  The red team showed a pipeline that "computes nothing" passes all 128 laws
  (`docs/redteam/2026-09-19-m5-boundary.md`).
- Owner's time, measured: D0267 "it's rigorous but too slow"; "18 minutes of hooks per commit (19
  for a one-file docs commit), make verify 46 minutes, CI 41 … the M4 sitting driver 19 steps and
  3h03m; 265 records in 23 days at 79 lines each". `budget.yaml`: every ceiling 0; no spend ever
  authorised. src 6,619 / tests 22,545 / governance and records 59,572 (~9 : 1).
- "The owner's involvement is a weekly batch, not a stream"; "being asked something answerable
  from policy.yaml is a bug" (`BRIEF.md` §9); D0273 "the first real use as the demand signal for
  what comes next".

## credence (≥2026-04-20 → 2026-08-30) and credence-governor (~2026-06-25 → 2026-08-22)
- credence: postures closed by date (P3 04-22, P4 04-27, P5 04-30), a pivot "to governance sidecar
  following routing-collapse benchmark" (`docs/master-plan.md`). Stage A (2026-08-09): "Every
  evidence channel the engine was ever fed runs at 0.99 or above … discards 69,850 of 141,717
  outcome records — 49.3% … The channel is degenerate because of our label."; "Phase 1 should not
  start"; "it is the user's call". No in-repo statement of abandonment; the verdict lives in
  wald-charter. src 9,059 / apps 63,533 / tests 70,975 / docs 27,633.
- credence-governor: a pre-stated exit with constants — "exit-from-shadow declared: bar_waste
  0.05%, n_min 1,000, rolling 30 days … incumbent FAILS the waste bar (6.50% vs 0.05%)"; ~30k real
  decisions in shadow, "demoted from enforcement because it blocked too often"; shadow retired
  2026-07-22 (`docs/governance-roadmap.md`, `docs/membrane-shadow.md` §6.3). Code 22,318 against
  docs 1,811.

## Cross-repo synthesis (the reader's, unedited)

Lifetimes shorten and the governance share rises until the wald split: credence ~4–5 months,
life-agent ~4.5, proplang 11 weeks, tannen 5 weeks, wald/wald-charter/wald-arena ~2 weeks each;
prose-to-kernel ratios run ~5:1 (proplang), ~9:1 (tannen), 3:1 with a 67k-line archive
(life-agent), ~1:1 (wald family), inverted in credence-governor. No repo carries its own reason
for stopping: proplang ends on unposted drafts, credence on a merge, tannen on a version sitting;
each reason appears in the successor's founding text (`wald-charter/HANDOFF.md` §1,
`CHARTER-v0.2.md` §0; tannen `BRIEF.md` §1 adopting proplang's disciplines; life-agent
`ROADMAP.md` swapping credence→proplang→wald). Pre-stated completion criteria existed in four
repos and were met in letter but not in effect: proplang declared its roadmap terminated three
times (07-07, ~08-08, ~09-05) and continued under "demand-gated residue"; tannen's M5 passed with
"production bugs found … out of its reach by construction"; life-agent's live-traffic exit test
"has not started counting"; credence-governor's shadow failed its own bar and was retired. Only
wald-arena's brief 002 was met as written, against money ($38.40) and an external board, with
held/missed printed. The recurring defect across all of them is frozen or of-record prose
falsified by the code (proplang FL inventories, life-agent SEALED, tannen "documentary" bindings,
wald-charter ERRATA), each answered by a new instrument. The owner's cost was measured explicitly
only in tannen D0267 and life-agent's RULINGS ("asking the owner cost less than searching");
proplang and wald-charter encode it as rules (close every issue; recommend with the alternative in
one line). The only rule in the corpus about when to stop building and start using is
demand-gating: proplang's "two-sided gate with a measurement", wald-charter's "forced by a
measurement or not added at all", life-agent's "enters when it beats the host on the board",
tannen's "wait until use asks for them".

## assize (6 → 25 October 2026), from this charter's §1 and the weekly acts series
Twenty of twenty-four merges in 10–13 October changed the court's own procedure; 147 repairs by
the owner in the week of 7–13 October, 40 in the week after; ended at the seal by the owner's
wish #341, its remaining content carried here. The reason for jack is written in jack's charter,
not in assize's: the pattern above, once more.
