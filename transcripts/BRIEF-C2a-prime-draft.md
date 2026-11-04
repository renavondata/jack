# BRIEF-C2a-prime — the second window of C2a (draft v2, 4 November 2026, counsel)

This file is `transcripts/BRIEF-C2a-prime-draft.md`; the window is named `C2a-prime` wherever a tool reads a name (`′` is not admitted by `jack push --opens`). v2 answers counsel's cold read of v1 (F1–F8) and implements `transcripts/RULING-20261104-window-fix.md`.

C2a's first window will fail at its stated end. This brief pre-states the window that follows it, as A3.2
requires ("a window that fails is a precedent, fixed by a lawful change and followed by a new pre-stated
window; it is never patched in place") and A4.1 permits ("a window that fails and is followed by a new one
continues the same wealth process on the same statistic under the same null"). It changes criterion 3's number and
criterion 7's interval and nothing else of C2a's criteria; no statistic and no stream. It names the lawful
change that fixes the precedent, the entry that records it, the instant the new window opens, and the code
that lets `status.py` read it.

## Precondition
C2a's first window has reached its stated end, 2026-11-15T15:04:14Z (BRIEF-C2a Amendment 1), with
criterion 7 unmet — `off-log repairs` non-zero on the acts evidence of the window — and no `decision
promote C2a` on the log (A5.1: "a window that reaches its stated end with a criterion unmet has failed").
This brief and its two reads on `main`, each a `transcripts/REVIEW-C2a-prime-*.md` in the form `jack push
--opens` reads (first line `VERDICT: ACCEPT` or `VERDICT: ACCEPT WITH OBLIGATIONS`, a `Reviewed tree:` at which
this text's bytes equal `main`'s, carried to `main` by a proposal signed by a non-counsel key), one by a reader
of a model family other than the other's; `transcripts/RULING-20261104-window-fix.md` on `main`; counsel's V5
(§Forecasts) entered before the opening; the lawful change of §The precedent in force; the sovereign's
`decision fix` naming C2a (§Order of acts) entered.

## The precedent, and the lawful change
At seq 1076 (2026-11-03T21:26:25Z) value *E* was 386.0 over 210 events and continued liveness *E* 24.5 over
62 items, both at or above 20 for the first time, and `status.py` with the acts table of 21:44Z (branch
`counsel-c2a-exit-2`, `transcripts/evidence/acts-20261103T2144.csv`) read `promote C2a: refused` on criterion
7: nine `repair` rows under the sovereign's login inside the window. One was the sovereign's own hand at
counsel's request (the draft conversion of #236, 3 Nov 14:31Z); the others were the herald's re-run loop, a
closing keyword in a counsel pull request, labels set when issues were filed, and closes whose hand is not
established — acts of the court's machinery under the owner's login, which the acts classifier can only type
as the sovereign's. The failure is recorded as C2a's precedent in the C2a report; no row is re-attributed.

The lawful change (A3.2: "fixed by a lawful change") is to the machinery, not the law: from
2026-11-04T05:40Z every act of the court on jack's platform is made by a GitHub App
(`renavondata-jack-court[bot]`: opencode-runner #225, #227; the first merge under it PR #285 at 06:35:17Z),
the herald re-runs nothing (opencode-runner #220), and counsel writes no closing keyword and asks the
sovereign for no platform act. An act under the sovereign's login is now his or counsel's, and counsel's
carry their declaration (BRIEF-C1b Amendment 2). The record of C2a-prime's window is the first in which the
criterion measures what §7 means.

The entry that records the fix is the sovereign's `decision fix` whose `subject` begins `C2a:` (A2.6: "the
fix of a failed window" is a `decision`). Under the ruling of 4 November 2026 it is a decision and not a
repair when it names a window that failed, is entered after that window's stated end and before the next
opening push, and is the first `fix` naming it; the window code below implements that rule.

## Scope
**The window.** C2a-prime opens at the first `push` entry whose `ts` is after C2a's stated end; the window is
(opening `ts`, min(V5's `resolves_by`, opening `ts` + 14 d)] (A5.1, A5.2), where V5 is counsel's forecast with
`args.id` `V5` and a `seq` below the opening's. The push is made by `jack push <branch> --opens C2a-prime
--review <file>`. It changes `judge/scope.json`'s `cap` from 7,800 to **8,000**, SPEC §10's block to match, and
one clause of SPEC §10's cap history ("8,000 at C2a-prime's opening, for the window code"), and nothing else.
8,000 is a resource constant of the 7,800 kind (BRIEF-C2a §The cap): it enters no score, and it is fixed
here, not at the push. No second push inside the window.

**The subject.** The promotion is `decision promote C2a` — the same subject, because BRIEF-C2b keys its
opening on "the first `push` entry after `decision promote C2a`" and its read is on the record — with an
extra body member `"window": "C2a-prime"` (SPEC §5 admits extra members). A5.1's "whose `subject` names the
window" is read as the window open for that subject at the entry's instant: `status.py` assesses a `promote
C2a` against C2a-prime exactly when no `promote C2a` has `ts` at or before 2026-11-15T15:04:14Z and the
entry's `ts` is after C2a-prime's opening; against C2a's first window otherwise. It prints `window: C2a-prime
(second window of C2a, opened seq <n>)` beside the promotion line.

**What continues.** Value *E* and continued liveness *E* as they stand (A4.1; `wealth_continues`): the same
events, the same base rate, the same mixture, the same item process from C1b's wealth, the same attack gates.
The streams run as BRIEF-C2a Amendments 2 and 3 state; the HKJC stream ended with the meeting of 4 November
(COUNSEL-OPEN row 30). Nothing in `tools/value.py`, `tools/clerk.py`, `item_process`, `score_items`,
`sovereign_keys` or `P0` changes.

**The code** (the builder's, one branch pre-built before 15 November and proposed as the first proposal after
the opening push): in `tools/status.py`, (i) the C2a assessment reads the window above when C2a's first window
has ended without a promotion — opening by the rule above, V5 by `args.id` with `seq` below the opening,
criterion 3 against 8,000 and "unchanged since the opening" against that push, criterion 7's acts interval
from the opening — and prints the window line; (ii) the ruling's rule in `item_process`: a sovereign `decision
fix` meeting the ruling's four conditions is not a repair; (iii) criterion 6's "unchanged" comparison
(`c2a_tree_evidence`) for C2a-prime starts from the tree at the merge of this proposal, named by the first
`merge` entry after the opening whose proposal's title begins `C2a-prime window code`, because (ii) changes
`item_process` and lands after the opening. The new pins join `VALUE_PINS` so criterion 1 requires them. Tests
for each. Counted lines after it: at most 8,000.

**The acts evidence.** Criterion 7 reads one attributed table produced by the committed classifier
(`transcripts/evidence/guy_acts3.py`, PR #232, SHA-256
`ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b`) over exactly the window:
`python3 transcripts/evidence/guy_acts3.py renavondata/jack . <opening ts> <exit ts> transcripts/evidence/acts-c2a2-<exit>.csv`,
with its raw twin, committed by counsel before the promotion and named in the `decision`'s `--acts`. The table ends at its
generation instant, which is at or after the last entry before the `decision`; the C2a report re-runs the
command to the `decision`'s `ts`, commits the result beside it, and prints any row between the two. The
command reads GitHub's current record (comment bodies, labels, deletions); counsel therefore commits the raw
table with the attributed one, so the evidence the promotion read is on `main` whatever GitHub later shows.

## Order of acts, and the clock
1. This brief merged with two reads on the record (a reader of another model family among them) that return no
   BLOCK; counsel enters V5 with `args.id` `V5`; V5's `resolves_by` is the window's end and is never moved.
2. C2a's first window ends at 2026-11-15T15:04:14Z without a promotion. The sovereign, one paste: `decision fix
   "C2a: criterion 7 unmet at the stated end — nine off-log repair rows (acts-20261103T2144); the court's platform
   acts moved to a GitHub App (opencode-runner #227)"`, then the opening `push` (cap 8,000), the first `push`
   after that instant.
3. The builder proposes the window code (title beginning `C2a-prime window code`); the herald merges; the
   `tests` run on `main` verifies it.
4. `status.py` prints the window line, the value line, the liveness line and `promote C2a: lawful | refused: …`;
   counsel commits the acts evidence; the sovereign's `decision promote C2a --acts <file>` when it reads
   `lawful` (A5: at the crossing).
5. BRIEF-C2b's order of acts then begins at its step 3.

## Pre-stated criteria for C2a-prime, evaluated on the exit prefix
C2a's seven, read on C2a-prime's window:
1. Every pin of BRIEF-C2a's list, and §Pins below, KILLED with a passing twin in the `tests` run on `main` at
   the exit prefix.
2. Both checkers agree on the exit prefix and the committed seeds.
3. Counted lines within 8,000; the kernel within 500; `judge/scope.json` and SPEC §10's block unchanged since
   C2a-prime's opening push.
4. The attack tests green on `main` before the first scored event's cutoff (unchanged: 2026-11-01T15:59:44Z).
5. **Value**: *E*ᵥ ≥ 20 on the one ledger, by `tools/value.py`, wealth continued.
6. **Liveness continued**: C1b's process at or above 20 on the exit prefix, wealth continued.
7. No `decision` of kind `veto` with subject `C2a`; **off-log repairs 0 on the acts evidence of C2a-prime's window**;
   A3.4 at or under 5 : 1.

This brief states no minimum length for the window: A5 makes a window a maximum, and a minimum would be a
constant chosen by hand (the refusal list of BRIEF-C2a; the cold read of 4 November on the withdrawn
Amendment 4, finding F4). If every criterion holds an hour after the opening, the window closes in an hour,
and the record says so.

## Pins (the reviewer's), each with its named mutant and passing twin
`second_window_from_the_end` (the opening is the first push after C2a's stated end; mutant: the first push
after seq 337, which is C2a's own) · `second_window_end_is_v5` (the end is min(V5's `resolves_by`, opening +
14 d); mutants: V0's; a V5 with `seq` above the opening accepted) · `second_window_cap` (criterion 3 reads the cap the opening push set and refuses a later
change; mutant: 7,800 hard-coded, which refuses every prefix) · `offlog_from_second_opening` (criterion 7
counts rows from C2a-prime's opening; mutant: from C2a's, which counts the nine) · `promote_refused_before_end` (a
`promote C2a` at a prefix before C2a's stated end is assessed against the first window, where criterion 7
refuses; mutant: the second window read early) · `window_fix_is_decision` (a `decision fix` meeting the ruling's four conditions taints no writ and is no
late report; mutant: typed a repair; twin: a `fix` with a free-text subject, or naming a window that did not
fail, or entered after the next opening, still taints every open writ) · `process_unchanged_from_window_code`
(criterion 6's comparison starts at the window code's merge; mutant: at the opening push, which refuses every
prefix) · `wealth_continues` (C2a's; unchanged).

## Refusal list
C2a's, entire, plus: no change to any criterion's statistic or threshold; no re-attribution of any row of
C2a's acts evidence; no minimum window length; no second push inside the window; no code but §The code; **counsel's platform acts
on `renavondata/jack` in the window are `jack` verbs and declared closes of its own stale proposals, nothing
else** — no labels, no edits, no closing keywords, no reviews, no re-runs.

## Stop and report if
the window code does not fit under 8,000 (the shortfall); the two checkers disagree; a `repair` row appears in
C2a-prime's acts evidence (the window has failed; the report names the row and its hand, and the next window is
pre-stated by the same procedure); V5's `resolves_by` passes with a criterion unmet; **a `push` after C2a's stated end that precedes V5, or the
`decision fix`, or that does not set the cap to 8,000, opens a window with no end, no recorded fix or no room —
stop; the next window is pre-stated afresh by the same procedure**; the sovereign pushes before 15:04:14Z by
mistake (a second push in C2a's window: V3 resolves 0; stop and report before any other act).

## Deliverables
This brief and its reads; V5; the window code and its tests; the pins; the acts evidence of the window;
the C2a report's section on the first window's failure (the nine rows as precedent, the lawful change, the
date, and the sovereign's acts outside jack on 4 November — three runner merges and a runner label as off-log
repairs the instrument cannot see, the App as a capability grant), and on C2a-prime's exit with its length and
its acts count; `acts-20261103T2144` raw and attributed and `runs-tests-20261103T2144.json` committed to `main`
with that report; C2a-prime's line in LAW.md's departure notes retired if the identity change retires it.

## Counsel's forecasts on this window (entered after the reads, before the opening push)
| id | claim | p |
|---|---|---|
| V5 | the promotion forecast: every criterion of C2a-prime holds on the exit prefix by this forecast's `resolves_by`, 2026-11-30T00:00:00Z | 0.7 |
| V6 | the acts evidence of C2a-prime's window holds zero rows of class `repair` | 0.75 |
| V7 | `decision promote C2a` is entered within 48 hours of C2a-prime's opening push | 0.55 |

V0–V3 are not edited and resolve on their own words: V0 is 0 at C2a's stated end (criterion 7 failed); V1 is 1
(value first at or above 20 at seq 789, 3 Nov 03:12Z, inside seven days of the opening); V2 is decided by the
weights at C2a's stated end; V3 is 1 if no second push lands before 2026-11-15T15:04:14Z. Counsel's X0 on C2b likewise (BRIEF-C2b Amendment 2).
