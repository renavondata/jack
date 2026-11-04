VERDICT: BLOCK
Reviewed tree: 82828514933b17ac6ab007d42882ebdef4a17873
Reader: reviewer reviewer-2; model openai/gpt-6-astra; 2026-11-04

F1: The delayed installation expressly permits changing already-finalised liveness outcomes and subsequent stakes; the exemption needs a narrower order or the sovereign's answer before opening — severity: BLOCK (BRIEF-C1b §Liveness: "An item once finalised is never regrouped: no later entry, evidence string or merge changes an earlier item or any bet already placed (A4.3)." CHARTER A4.1: "A window that fails and is followed by a new one continues the same wealth process on the same statistic under the same null; *E* is never set back to 1 and no α is split.") — witness: transcripts/BRIEF-C2a-prime-draft.md:153–171; transcripts/BRIEF-C1b-draft.md:91–142; tools/status.py:65–114.

The conflicting sentence is explicit: "items finalised in the interval are recomputed by every run after the merge"; it then says: "This touches BRIEF-C1b's 'no later entry, evidence string or merge changes an earlier item' for that interval alone, and correction 3 accepts it." The interval is not hypothetical: the prescribed order enters the fix, opens the window, and only then proposes and merges the changed item process. The streams continue throughout. The exemption's list at lines 162–165 does not include C1b's finalisation rule.

The strongest defence is substantial. A2.6 already calls the fix of a failed window a decision; the corrected ruling is read before the fix; changing an erroneous implementation need not change the law applicable to an entry. Correction 3 also forbids reliance on the old typing for a promotion, writ disposition or report. On the prefix that exists today the change really is inert: seven decisions, no fix. That defeats a claim that v6 revises *today's* scored items, and it would support an implementation that uses the correct, pre-stated typing from the first affected item.

It does not establish what v6 actually needs for the intervening items. The old `item_process` finalises on log entries, not on the first occasion someone relies on its output. A qualifying fix taints every then-open writ; timely resolutions and their merges can finalise before the implementation lands. The next implementation changes their Y values and the prefix from which later stakes are calculated. Not promoting during that interval does not prevent this. Nor does keeping p₀ and the formula fixed prove the same statistic: Y's repair term is part of the statistic. Printing both results in the report records the change, rather than making the results identical.

A read-only synthetic probe of the committed `item_process`, with signer lookup mocked, demonstrates the difference. It has one timely batch, another writ open at a sovereign fix, its timely batch, and a third timely batch. Replacing only that fix's kind with `grant` exercises the existing non-repair-decision branch while preserving the sovereign batch boundary; it is a stand-in for the proposed exclusion, not a claim to have implemented the new predicate:

```
old Ys/stakes/E/late:    [1, 0, 1] ['0', '22/45', '0']     11/15  [5]
exempt Ys/stakes/E/late: [1, 1, 1] ['0', '22/45', '33/40'] 121/72  []
```

The entry at synthetic seq 5 is assumed to satisfy the new boundary predicate; the probe isolates the consequence for items and bets. No signed log was edited. A passing twin would apply the lawful boundary classification before the affected finalisations and preserve every finalised `(seq, forecasts, Y, stake, E)` across the later code merge. The specified real-log test stops *before* the first fix (line 151), precisely before the distinguishing witness.

My answer to §The exemption is therefore split: a new brief can pre-state a new cap and acts interval, and can implement A2.6's boundary classification; it cannot justify the quoted interval exception merely by calling the null and stake formula unchanged. A2.4 says briefs "may tighten the charter's bounds, never loosen them"; A3.2 provides a new window, not permission to revise a continuing process's earlier outcomes. Correction 3's timing order is the source of the collision, not an amendment resolving it. Correction 4 expressly withdraws the ruling's claimed amendment-free precedence. Put this precise conflict to the sovereign under A2.10, as v6 line 173 itself requires, or revise the order so no affected outcome or stake changes. This is the blocking conflict; the remaining findings are obligations, not additional charter amendments invented by this reader.

F2: Order 2's re-typing objection is bounded by the four conditions but not defeated by them — severity: OBLIGATION — witness: transcripts/RULING-20261104-window-fix.md:49–59,86–93,157–195; transcripts/BRIEF-C2a-prime-draft.md:119–142,232–263; CHARTER.md:106–111,185–190.

Construct the adverse case after a genuinely failed window, with a genuine committed repair row, no promotion, and before the next opening. The sovereign does a fresh operational repair while writs are open, then enters his first `decision fix` with subject `C2a: repaired the runner; acts-20261103T2144`. All four proposed conditions hold. The new act is not the act which failed the old window, but the predicate exempts it just the same. No condition tests that the entry records *only* the boundary judgement, and the existing twins do not distinguish this case. An old qualifying file supplies the failure witness indefinitely until the next push. The veto alternative supplies an additional route without a file.

The important limits are real: only one first fix per failed window, only after the later end, only before the next push, no erasure of the old repair row, and every other fix remains a repair. A2.6 supports the actual boundary recording in the prescribed paste. Typed law cannot establish the truth of an arbitrary prose account of an act, and merely inventing a semantic classifier would make matters worse. Nevertheless the ruling's assertion that narrowness *closes* the route is too strong. An ordinary repair can be represented as that one boundary decision, just as a false `grant` could misdescribe a repair. Record this residual route in the Order 2 answer and the C2c distinct-kind work; do not report the pin as establishing that the sovereign's hands did no work. The prescribed paste itself describes the failed-window recording and is not a witness that this laundering has occurred.

The file-name rule is also deliberately weaker than an identifier: `acts-X` is a substring of `acts-X-raw` and of longer names. The raw-only twin at lines 253–255 has an empty attributed file, so it does not kill a matcher that accepts a raw-name subject when the attributed file *also* has a qualifying row. Require that distinguishing test or explicitly retain substring matching as the rule, including its consequence. Presence of a raw twin and the classifier's hash proves neither that the attributed table was generated by that classifier nor that its rows came from the raw table.

F3: Criterion 7 needs a boundary-row pin and a narrower claim about what the instrument measures — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-prime-draft.md:66–73,175–186,210,225–227,272–278; transcripts/evidence/guy_acts3.py:52–54,61–70,156–163,172–206; tools/status.py:215–221.

The new interval does not, by itself, make the existing implementation count every row the specified collection command obtains. The classifier filters actual instants against its requested interval, then discards seconds in the CSV. `off_log_repairs` compares the resulting minute's *start* against the opening. This read-only command against the committed function is a distinguishing witness:

```
PYTHONDONTWRITEBYTECODE=1 python3 -c 'from tools.status import off_log_repairs; r={"repo":"renavondata/jack","class":"repair","time_hkt":"2026-11-18 08:00"}; print(off_log_repairs([r],"2026-11-18T00:00:30Z","2026-11-18T00:05:00Z")); print(off_log_repairs([r],"2026-11-18T00:00:00Z","2026-11-18T00:05:00Z"))'
0
1
```

A real repair at `00:00:31Z` belongs to the window opened at `00:00:30Z`; the classifier includes it, writes that row, and the present assessment loses it. Change 1 must specify how to handle that lossy boundary and pin it. The proposed `offlog_from_second_opening` mutant only distinguishes old from new opening; it does not kill this omission. Correction 2's whole-minute containment is a *sufficient witness of failure*, where refusing ambiguous evidence is conservative. It must not be reused as a *proof of zero repairs*, where the same omission is permissive.

On the question of normal-operation false positives: under the stated operating restrictions, I found no unavoidable repair row produced by the two `decision` commands, the opening `push`, or `decision promote`. They push commits; first-attempt push workflows are not re-runs or dispatches. The App's login is excluded by the classifier's actor tests. A properly declared counsel close within the two-minute rule becomes a party-act. Those are genuine improvements over the nine-row precedent.

They do not make the table a complete §7 instrument. The classifier does not read log signatures; ordinary sovereign comments are not counted as acts, issue creation is typed an instruction/decision without a signed wish, and the declaration rule can attribute a nearby act of the sovereign's to counsel. It also cannot measure the runner acts outside this repository. Conversely a counsel close with a late or missing declaration still becomes a sovereign repair row; a court re-run under the owner's credential still does too. The brief's restrictions reduce these risks prospectively; the tree alone cannot verify the external App rollout or identify the hand behind every row. State these limitations, preserve raw evidence, and distinguish measured zero from proof that §7's entire requirement is met. No new unavoidable false-positive act was established by this read.

F4: The acts evidence's freshness and provenance contract is not yet executable as stated — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-prime-draft.md:175–184,198–210; tools/jack:51–60,84–95,121–127,147–163,247–272; tools/status.py:215–221,388–410; transcripts/evidence/guy_acts3.py:202–206.

Line 182 requires the table's generation instant to be at or after the last entry before promotion, while line 180 requires counsel to commit it before promotion. The ordinary counsel path generates the file, commits it, appends a proposal, and receives a herald merge: those last two entries are later than generation. The CSV carries neither its requested start/end nor a generation instant; `decision --acts` passes a pathname to status but stores only `{kind, subject}` in the decision body. The current verb does not require that pathname to be a committed file under `transcripts/evidence/`, or require its raw twin or hash file. A matching classifier hash alone is not an attestation of an execution.

This needs a concrete protocol, not an assumed chronology. For example, a post-merge re-collection that is byte-identical to the committed table can avoid a further evidence commit, but the specified command and current CSV alone do not record its coverage or that equality check. A new row requires a new evidence cycle. The final gap from collection to the signed decision also remains: rerunning in the report detects it after promotion, while A5.1 requires the criteria at the decision's prefix. State what proves that gap clean before signing. Pin stale, uncommitted and incomplete evidence, with a committed complete twin. The example classifier command writes the attributed file only; the raw twin needs its own specified collection step. None of these provenance/freshness checks is in the proposed pin list.

F5: Most new predicates are decidable, but the pin list and unchanged-code guard do not cover every promised rule — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-prime-draft.md:35–47,108–151,214–278; tools/jack:177–220; tools/status.py:224–249; judge/scope.json:4–9.

The computable core is well specified: late opening plus pre-opening V5; cap and tree history; per-window veto attribution; fixed-file failure evidence at the fix's carrying commit; first fix and next-push ordering; and a merge anchor for the permitted process change. The proposed pins name useful mutants for each. These are requirements for the forthcoming build, not pins already killed on this tree. `VALUE_PINS` currently contains only C2a's eighteen names.

There are additional missing witnesses:

- The gate currently accepts the first valid non-counsel accepting review; it does not require **two** reviews, different model families, or evidence that the sovereign read the corrections. These remain preconditions checked outside the gate. Model-family independence is not established by a free-text `Reader:` line alone.
- The process guard covers functions, their local transitive function dependencies, and direct callers, but not arbitrary top-level data they read. Changing a global table of window ends or an exemption set can alter classification without changing those function ASTs. Require a global-data mutation witness as well as the caller mutation witness; the tuple of function names must not be a way to remove protected code from the comparison.
- The window-code anchor is selected by title and commit ancestry. It does not itself prove that the named proposal supplied the specified implementation. Pin an unrelated title-matching proposal and the intended builder-code twin before treating its merge as a trusted baseline.
- The two-read requirement, first-code-proposal order, App identity, no counsel labels/edits/closing keywords, no row re-attribution, evidence freshness, and the instruction to stop before any further act are not mechanically enforced by these pins. Some are decidable historical checks if represented in the log/tree; actual platform custody and the hand behind an act need external evidence. Describe these as obligations rather than claiming every rule has an enforcing mutant.

The 8,400 cap is a pre-stated resource budget, not a hand-picked statistic or significance threshold; I find no conflict in its kind. The cited 8,022-line external draft is not independently verified in this worktree. The actual current count is 7,784/7,800, leaving 616 lines at 8,400 for the implementation and its tests and pins. Stopping on a shortfall is the prescribed outcome, not permission for another push.

F6: The principal boundary sequence is mechanically coherent, but the report's supposed no-window gap chooses the early reading — severity: OBLIGATION — witness: transcripts/BRIEF-C2a-prime-draft.md:28–47,78–97,153–159,186–200,283–287,316–320; transcripts/BRIEF-C2b-draft.md:278–292; tools/jack:31–49,177–244,247–272; tools/value.py:40–41; tools/clerk.py:53–56.

Walk of the prescribed acts against the current code and the specified changes:

1. Merge the unchanged brief and both signed reads; enter V5–V7. The review filenames, first line, reviewed commit and non-counsel proposal provenance are the forms `push_read_gate` actually reads. A BLOCK prevents this read from satisfying that gate.
2. Wait strictly past `2026-11-17T12:00:00Z`, checking that the old opening is still the last push and that no old promotion occurred. The normal `decision grant` and `decision fix` verbs check identity, branch, clean state and recognition; they do **not** enforce the new four-condition boundary test. That is why the exact paste and preconditions matter.
3. Update the cap branch to contain both new decisions. Otherwise `v_push` refuses the stale ancestry. `--opens C2a-prime` is accepted as a name and looks for the named brief and review pattern; `′` is not accepted. The scope and SPEC edits give a changed trusted digest; there is no checker-source change requiring a new run of record. The cap-only push still runs its ordinary checks.
4. Before the window code lands, status continues to select the first opening, ends its assessed prefix at the early end, and sees the changed scope. It cannot promote the new window. Its item process does not see the later fix in that old assessment. This is correctly described by lines 153–157, but is not a proof that the underlying continuing item process has no affected finalisations (F1).
5. The forthcoming status changes must select the new diagnostic window while leaving `value.opening_push` at seq 367 and liveness anchored at C1b. Resetting the value roster, weights, prior differences or liveness prefix is not a permissible implementation of the new window. The new pending-merge guard must refuse until the anchor exists; then the exact-HEAD green tests run is still required.
6. `jack decision promote C2a` remains an admitted subject, fetches current and historical runs, obtains the assessment instant once, and signs only the exact lawful line. New status must interpret its subject by v6's stated mapping. C2b then finds that same promotion, grants the herald powers, and opens after it; it must not enter a second promotion. The old C2b step 1/read/forecast prerequisites still need to hold before starting its step 3. This read does not adopt or review C2b's unread Amendment 2.

The conservative boundary acts do not require adjudicating C2a's end. But line 186 says: "The off-log acts between 2026-11-15T15:04:14Z and C2a-prime's opening fall inside no window's interval." That is false on the late reading: acts through `2026-11-17T12:00:00Z` are inside C2a. Report the overlap under both readings, as the brief otherwise promises. It cannot be called an unconditional no-window interval. Likewise "The window has failed" on the first new repair row should mean promotion has become impossible, not that a new legal end or immediate restart was created; the next fix still waits for the stated end.

C2a's historical `status.py` view continues to use the early end. A V2 resolution that differs between the two exit prefixes still needs the ruling's referral; there is no code change here that resolves that question. The instruction to wait for the later instant avoids an early act but does not make the two historical reports identical.

F7: The main factual grounds are reproducible; they support a new window, not rescue of the failed one — severity: OBLIGATION — witness: CHARTER.md:94–111,313–317,342–360,376–384; transcripts/COUNSEL-OPEN.md:42–44; log.jsonl:362,1077; transcripts/evidence/acts-20261103T2144.csv:79,137–155; commands below.

The requested bare status command was run, unchanged:

```
python3 tools/status.py 2>&1 | grep -E '^promote|^value|^liveness continued|criterion' | cut -c1-200
```

It reports the current cap as `7784/7800`, kernel `450/500`, value `1.000000` over zero scored events, liveness 1 over zero counted items, and off-log repairs `unknown (no acts file)`; the promotion is refused. Those last numbers are missing-input projections, not measured deterioration of the live processes. The historical C1b lines also lack run evidence on that invocation.

With the committed evidence:

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/status.py --subject C2a --as-of 2026-11-03T21:26:25Z --acts transcripts/evidence/acts-20261103T2144.csv --runs transcripts/evidence/runs-tests-20261103T2144.json 2>&1 | grep -E '^promote|^value|^liveness continued|criterion' | cut -c1-200
```

The relevant outputs are:

```
criterion 3: counted 7784/7800; kernel 450/500; scope equals SPEC and unchanged: True met
criterion 4: attack green on main before first scored cutoff: 2026-11-01T15:59:44Z met
criterion 5: value E 386.009170 >= 20 met
criterion 7: off-log repairs: 9 SHORT
value: E 386.009170 over 210 events; window events 210
```

Continued liveness is the exact fraction
`3349298034955599095318942248963066521029422565733678974841423611/136566436648336993276433405036982023734532505600000000000000000`
over 62 items, approximately 24.53 and above 20. Criteria 1 and 2 are SHORT for the assessed current tree at that historical instant; this does not establish a failure on those criteria. The nine-row sufficient witness is independently present. `sha256sum transcripts/evidence/guy_acts3.py` returns the brief's stated `ed0d37ba919412c32ab774ae5217a56e8cbf3c9c5ebe3632c687b18c96a1725b`. Targeted searches of the decisions in both `41f0d6c` and the reviewed tree confirm the four transmutes, budget and two promotions, with no fix.

The strongest rescue accusation is that counsel caused one repair, tried the withdrawn in-place amendment, then designed a short second window that carries already-earned wealth, clears the off-log count and exempts the otherwise disqualifying fix. V5 and V7 benefit from all three. Unlike the withdrawn proposal, v6 keeps the nine rows, waits past both possible ends, does not reset either wealth, preserves V0–V3's wording and discloses the liveness expiry risk. The forecast entry V0 says "C2a promoted, not failed"; a later second-window promotion must not retrospectively make that claim succeed on the failed first window. Those protections defeat the accusation of rescuing V0 by resetting criterion 7 *inside its window*. No minimum duration is required by A5; an early crossing in a genuinely new window is not itself an evasion. The unresolved objection is F1's interval, not the existence of a second window or the resource budget.

The future opening obligation is to rerun these checks on the then-current prefix. Today's seven-decision fact does not certify that no nonqualifying fix, intervening push, veto, stale review or expired V5 will exist on the opening day. I found no additional blocking conflict beyond F1. The obligations above must not be described as pins already killed or external facts independently verified by this read.

forecast: p = 0.45 that C2a-prime promotes before its stated end, 2026-11-30T00:00:00Z. Success means a sovereign `decision promote C2a` naming the second window under its pre-stated mapping, with ts strictly before that end; no such entry, including no opening, is outcome 0. This forecast resolves by 2026-12-15T00:00:00Z. It anticipates possible revisions after this BLOCK; it does not treat v6 as presently admissible.
