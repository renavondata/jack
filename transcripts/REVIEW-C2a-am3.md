VERDICT: ACCEPT WITH OBLIGATIONS

Reviewed tree: 1204d566ea3845bcbb7fa06dc0a422db18d4b8d3 (origin/main).
Reviewer: reviewer reviewer-2; model: openai/gpt-6-astra; 2 November 2026.

Amendment 3 is lawful mid-window on the law as written. The obligations below
are applications of existing rules, not additional exit criteria. There is
no charter or brief conflict on which I would BLOCK this amendment.

F1: Three future windows per session preserve the event contract and A4.4's conditional null; the delayed-session rule is sound, not merely harmless because of scorer exclusion — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:38–91,118–141,229–235,304–310; CHARTER.md:354–360.

For H on the specified three-hour grid, the three starts H+2, H+3 and H+4
tile the same hourly schedule Amendment 2 adopted. Each carries all six
datasets. Eighteen signatures replace three six-signature sessions; no
dataset, hour, cutoff or predicate is selected by its outcome. A late session
does not acquire permission to backfill a missed hour after seeing its result.

The exact on-time lead times at :20 are 1 h 40 min, 2 h 40 min and 3 h 40 min.
Signing roughly four rather than two hours ahead changes the information
available to the forecaster and may change performance. It does not change
the null E[D_i | past] <= 0, the bounded log-loss difference, or its prefix
bet. The base remains the clipped, type-pooled, per-resolution Laplace rate
from the prefix before the event's first resolution, not a calibrated truth
at the signature time or a horizon-specific model. The aggregate still uses
resolution-prefix weights and pre-cutoff entrant probabilities. Its meaning
and the comparator's meaning therefore survive the earlier signatures.

"has not yet begun" means the signature timestamp is strictly before W0;
equality is excluded. Together with "is not yet forecast on `main`, and
nothing else", this is a substantive prospective selection rule. It does
not admit a signature at or after cutoff. **Obligation:** apply it at each
signature, including a re-signature in a delayed re-proposal, not just when
a session starts. A session straddling W0 must skip the now-begun window.
Checking `main` cannot prevent every concurrent duplicate; the unchanged
first-forecast/revision rules remain applicable. Neither a duplicate nor a
late signature acquires validity from the new batching rule. The scorer's
`rigged` exclusion is defense against a breach, not what makes this rule sound.

F2: Four-hour deadlines for unissued writs are lawful; neither the statistic nor the conditional liveness null is replaced — severity: OBLIGATION — witness: CHARTER.md:97–102,342–353; transcripts/BRIEF-C1b-draft.md:91–142; transcripts/BRIEF-C2a-draft.md:176–180,313–315; log.jsonl:480–485,551–556.

Section 6's frozen list is, verbatim: "Windows, α, *p₀* and the attack list
are committed before the window opens." The promotion window and its end
are not individual writ deadlines. This sentence does not freeze a numerical
deadline offset for every future writ. Amendment 2's "Nothing else moves"
preserved the then-current two-hour rule; Amendment 3 expressly supersedes
that operational term prospectively. It does not supersede the item rule.

C1b defines success relative to each signed field: "**Yᵢ = 1** iff every
resolution in the item was entered not after its forecast's `resolves_by`";
the following no-sovereign-repair condition remains essential. Before an
entry is processed, a writ strictly past its own deadline becomes a zero;
later resolution cannot reverse it. The unchanged statistic is timely,
unrepaired completion against the issued contract, not completion within
two hours for all time. Extending an unissued contract may improve its
success probability, but H0 remains E[Y_i | past] <= 6/11 for the actual
item sequence, with the same item/batch, repair, expiry and prefix-bet rules.
The baseline constant is not re-estimated. This does not establish a claim
about success under the old two-hour service target.

A4.1 says: "A window that fails and is followed by a new one continues the
same wealth process on the same statistic under the same null; *E* is never
set back to 1 and no α is split." The amendment changes neither prior factors
nor that process. Changing future inputs to the signed-deadline statistic
is not replacing it with a different statistic. C2a's "The clerk and its
writs are unchanged" remains true of the clerk's rule and issued writs;
the new forecast field values require no retrospective writ alteration.

The unlawful construction is to observe that an issued writ missed 12:00,
move its deadline to 14:00 after seeing its 12:15 resolution, and replay its
failure as success (or defer its already-required expiry). That violates
C1b's verbatim rule: "**An item once finalised is never regrouped**: no later
entry, evidence string or merge changes an earlier item or any bet already
placed (A4.3)." Re-signing an equivalent forecast cannot erase the original
writ or its loss either. Amendment 3 excludes this construction explicitly:
"Deadlines already entered do not move" and the new offset applies only
to forecasts entered after the read.

The requested concrete case is decisive: forecasts 479–484 were signed at
07:36:58–07:37:14Z for [09:00,10:00), with `resolves_by` 12:00Z. Resolutions
550–555 were signed at 12:15:08–12:15:27Z. They remain six liveness expiry
zeros even though five world outcomes are 1. **Obligation:** retain those
zeros, every other issued deadline, all prior wealth and prefix history;
apply +4 h uniformly only to the specified future forecasts. The longer
deadline also does not extend the separate ten-minute evidence-fetch rule.

F3: Responding to poor past scores is permissible prefix adaptation, not outcome-selected inclusion; being below one supplies neither a prohibition nor an exemption — severity: OBLIGATION — witness: CHARTER.md:100,348–360; transcripts/REVIEW-C2a-am2.md:10–59; transcripts/BRIEF-C2a-draft.md:295–325; command evidence below.

The earlier read accepted hourly continuation after E = 1.68 because the
next trial was chosen prospectively under a conditional null, not because
1.68 was a favorable score. The same reasoning applies at E_value = 0.950914
and E_live about 0.268974. The amendment's choice plainly responds to observed
performance and congestion. That is not the prohibited choice of an event
after observing that event's outcome.

Let F_(i-1) include prior outcomes and the schedule decision. For value,

    E[E_i | F_(i-1)] = E_(i-1) (1 + lambda_i E[D_i | F_(i-1)] / B)
                      <= E_(i-1)

under A4.4's null. Waiting leaves wealth unchanged. Ville therefore covers
prefix-dependent continuation and stopping with the same threshold 20. For
liveness, replace D_i/B by Y_i - 6/11; the analogous inequality holds under
the same conditional null for items generated by prospective contracts.
No independence or equal spacing is required. A null merely about the old
cadence's marginal outcomes, or the old two-hour completion probability,
would not suffice; those are not the law's stated conditional nulls.

A breaking construction: among candidate events with b = 1/2, q = 3/4 and
fair binary outcomes, unscreened expected D is (ln(3/2) + ln(1/2))/2 < 0.
Inspect outcomes and keep only Y = 1: every retained D is ln(3/2) > 0,
eventually producing a crossing despite no unscreened advantage. Equivalent
breaches include suppressing failed scheduled evidence, selecting resolution
order by observed score, rescuing late issued writs retrospectively, or
restarting wealth at 1 after losses. Ville does not license those acts.
Amendment 3 authorizes none: it forecasts all three still-future windows,
retains missed-window exclusions and past losses, and leaves the statistic
and issued deadlines intact. **Obligation:** preserve the scheduled evidence
and observation timing, including failures; do not use batching or stale
re-proposals as an outcome filter. In particular the four-hour resolution
allowance is no permission to substitute a later, more favorable page.

The stated operational reason is coherent: two incoming proposals per hour
against nominal capacity three is not reliable spare capacity when every
merge makes competing proposals stale. Grouping forecasts reduces scheduled
proposal arrivals from 48/day to 32/day while retaining 144 freshness events
and hourly resolution sessions. It can reduce retries; it does not prove
that deadlines or the remaining promotion gates will be met. The brief's
57 opened / 24 merged / 29 stale and twenty-minute-run measurements are
its operational account, not independently recounted PR statistics here.

Command and log evidence (on the reviewed tree):

- `python3 tools/value.py --table --attack-green 2026-11-01T15:59:44Z | head -30`
  printed `events: 48`; as expected when `head` closes a longer JSON stream,
  Python also reported a broken pipe. A subsequent complete JSON parse of
  the same value command returned `E_value: 0.950914`, `window_events: 48`.
- Its `excluded_forecasts` includes 487–492, 526–531 and 534–539, all
  `rigged: ts >= cutoff` (also the older 288–290). The requested 08:00 and
  11:00 windows are present, but **10:00 is also flagged**: seq 526 is signed
  at 10:43:27Z for [10:00,11:00). Seqs 487 and 534 start the other groups,
  signed at 08:01:44Z and 11:06:21Z respectively
  (`log.jsonl:488,527,535`). Thus "two windows" is not an exhaustive count
  of the current table's late-forecast windows. This qualification does not
  change the lawfulness of the future rule.
- `python3 tools/status.py | grep -E 'liveness|J7'` printed
  `liveness continued: E 1 over 0 items (including projected expiries)`
  and `attack unverified`, plus `J7: 6 of 92 window forecasts unresolved
  past resolves_by`. Bare status lacks historical Actions evidence; its
  unverified empty process is not evidence that wealth reset to 1.
- Reproducing the decision-time liveness snapshot with existing evidence:

      python3 tools/status.py --as-of 2026-11-02T13:30:00Z --runs transcripts/evidence/runs-tests-20261101b.json --acts transcripts/evidence/acts-20261101.csv | grep -E 'liveness|J7'

  returns `liveness continued: E
  144209936106499234037676064081/536147960394992400000000000000
  over 29 items (including projected expiries)` (about 0.269), with
  liveness attack time `2026-10-31T13:32:21Z`. These saved runs do not
  verify the later C2a attack gate; this invocation is evidence for liveness,
  not a promotion certificate. J7 counts still-unresolved overdue writs,
  not all historical expiry zeros, so it need not equal twelve.

F4: Amendment 3 contains no substantive fourth change and no blocking conflict — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-draft.md:304–325,189–203,229–235.

It changes forecast-session grouping/timing and prospective deadline values,
and restates hourly resolutions. The delayed-session restriction and the
builder W1 assignment are execution details of those items, not a new roster,
self-resolution permission or event-selection license. Its reasons and
statistical explanation introduce no additional scoring term. There is no
new dataset, predicate, cutoff, base, mixture, null, threshold, attack, wealth
reset, end-date extension, trusted-base change or exit criterion. Nothing
else would make me block. **Obligation:** assess every existing criterion
on the exit prefix; neither lawful adaptation nor a past threshold crossing
substitutes for both processes being at least 20 there.

forecast: p = 0.55 that C2a's current window ends in promotion rather than
failure: every pre-stated criterion holds on the exit prefix by the window's
end, 2026-11-15T15:04:14Z. A purported promotion missing a criterion, or this
window's failure followed by promotion in a later window, resolves 0.
Ledger type: review.forecast; resolves_by: 2026-12-15T00:00:00Z;
args: {"model":"openai/gpt-6-astra"}.

This is lower than my family's Amendment 2 forecast of 0.70. There is time
for substantial new evidence and the queue change plausibly helps, but the
observed liveness losses, late forecasts and value wealth below one make
recovery of all exit gates materially less certain. Lawfulness is not a
prediction of promotion.
