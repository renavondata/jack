# C0 report — the record and the checker

> §8, counsel's exit report of 17 October 2026, supersedes §2 (verdict) and §7 (what C0 still
> needs). §§1–6 are the founding session's report, unchanged.

Founding session, 13–14 October 2026. Proposer: founder `claude-fable-5-1`,
session `743dd139-c951-42b5-8e20-14cce485acab`. Branch `c0-founding`, pull
request [#1](https://github.com/renavondata/jack/pull/1) against `main`.
CHARTER.md is unchanged; every change proposed to it is in §5 below.

## 1. Scope change: C0 is the record only

**Guy's decision, 14 October 2026, on counsel's review.** The first build of
C0 carried the law language the charter's §9.2–9.3 describe: stratified Datalog
rules as data, `rule` and `repeal` entries, witnesses, replacements, the weak
non-contradiction check and lapse candidates (658 kernel lines). Counsel's
review found that language premature: no precedent yet needs a rule, and the
charter's own §3 says primary rules accrete from witnessed cases. Guy removed it
from C0 and moved it to C1, where the first real case will fix the smallest
language that expresses it.

What was done, in order:

1. Branch `c1-law-draft` was created at the last rule-bearing commit
   (`fe5c2f2`) and pushed before anything was removed. It is design input for
   C1 and is never merged. Its REPORT.md, transcripts and two simulator runs
   (37,146 and 36,352 seeds, zero kernel disagreements) stay there.
2. Removed from `c0-founding`: `kernel/datalog.py`; the `rule` and `repeal`
   types; witnesses, replacements, orphan and lapse logic; their tests
   (`test_datalog`, `test_witness_lapse`), five pins, six simulator kinds and
   SPEC.md §§7–12 of the old numbering. C0 types: `genesis`, `key`,
   `proposal`, `merge`.
3. The secondary rules stay in code: recognition = canonical line, `seq`,
   parent chain, signature by a declared key whose powers include the entry's
   type; change = `key` entries signed by a key with the `key` power
   (declare, re-declare, revoke); adjudication = trunk's kernel, by digest.
4. Counsel's fixes that still apply, kept: (1) the judge refuses any proposal
   whose trusted-base digest differs from trunk's or whose CHARTER.md differs,
   by content, so renames and deletions are caught (`trusted_path`; pin
   `trusted_rename_admitted`); (2) `kernel2/` in the trusted base; (5) weak
   public keys refused at declaration and an empty SSHSIG reserved field
   required, each with a pin; (6) trunk's genesis charter hash checked against
   trunk's CHARTER.md (`charter_mismatch`).
5. BRIEF-C1.md takes the law language, starting from the smallest language that
   expresses the first real case, with non-decreasing timestamps as the first
   candidate rule.

The decision moves probability mass from "C0 fails on an expressiveness stop
condition" (now impossible: there is nothing to express) to "C1 opens later
than planned". It also shrinks what Guy must read before signing by two fifths.

## 2. Verdict against §9's pre-stated criteria

| # | criterion | state | evidence |
|---|---|---|---|
| 1 | every pin KILLED and its twin passes, in CI, from trunk | **OPEN** | 13 mutants across 10 pins KILLED with passing twins (`transcripts/pins-20261014T012918Z.txt`), and in the pull request's `tests` run. `checker_drift` is **PENDING**, named, never passed: there is no second checker to drift. The pin list differs from §9's (see §5): four rule pins left with the law language, and four pins from counsel's review were added. "From trunk" waits for the merge; `tests.yml` runs on `push: main`. |
| 2 | both checkers agree, entry by entry and reason by reason, on the real log and 10⁵ simulated logs from a pre-committed seed list | **OPEN** | No second checker exists (by design; `kernel2/README.md`). The real log is empty until genesis is signed. Against the simulator's independent oracle: one full ten-minute run, 52,194 seeds on 12 workers, all 15 kinds, 0 disagreements between the kernel and the oracle, and the prefix, sticky-refusal and determinism properties held on every case (`sim/runs/20261014T012421Z-52194.json`). The seed list (`sim/seeds.txt`, 10⁵) was committed before any run and is unchanged. |
| 3 | kernel within 1,000 lines; an excess reported, never hidden | **MET** | 392 physical lines: `log.py` 144, `sig.py` 140, `check.py` 108, `__init__.py` 0 (`transcripts/count-20261014T012918Z.txt`); within Guy's target of 450. `judge/judge.py` (196 lines) is outside the kernel and the count. |
| 4 | Guy has read the kernel and signed genesis | **OPEN** | Guy's act. `README.md` gives the procedure; `genesis.template.json` and `tools/genesis.py` carry no key of his. |

C0 is not at exit. The posterior that it reaches exit without touching the
kernel is higher than before the scope change: criterion 3 is met with wide
margin, the surface a second author must reproduce is 282 lines of SPEC.md with
twelve reason codes and no evaluation engine, and criteria 1–2 turn on one
deliverable, the second checker, plus Guy's reading. None of §9's stop
conditions fired.

Counsel's forecasts (CHARTER §11): K5 (kernel within 1,000 lines at exit) is
now very likely. K6 (the checkers disagree on at least one simulated log before
exit) has moved down: the Datalog engine was the component most likely to
produce a disagreement, and it is gone; the strict Ed25519 rule and canonical
JSON remain the likeliest sources (SPEC.md §12).

## 3. Counts

| what | count |
|---|---|
| commits on `c0-founding`, each with `Proposer: founder claude-fable-5-1 <session>` (this one included) | 26 |
| kernel physical lines (criterion 3) | 392 (target ≤ 450; limit 1,000) |
| tests | 115 (local run under Python 3.12.8 / OpenSSH 10.5p1: 114 pass, 1 skipped by design: `test_named_difference_s_plus_L`, since this OpenSSH build also rejects S ≥ L; on GitHub's ubuntu-latest image it passes). The second named difference, `reserved_nonempty`, is present on both builds and its test passes. |
| pins / mutants | 11 pins; 13 mutants KILLED, 0 SURVIVED, 0 STALE, 0 twin failures; 1 PENDING |
| simulator, one full budget | 52,194 seeds in 600 s on 12 workers (about 87 seeds/s; 10⁵ in roughly 19 minutes); 0 property failures; kinds 3,399–3,525 each |
| reason codes | 12 in the checker, each covered by a spec vector; 6 judge-level |
| spec vectors | 24 signed logs with required verdicts; 6 canonical-JSON vectors; 5 RFC 8032, 12 speccheck and 12 weak-key vectors |

## 4. Decisions and ambiguities

Readings the brief forced; each is recorded in SPEC.md §12 and is Guy's to
overturn. Those Guy decided in session are marked ★.

1. ★ **C0 is the record only** (§1). Consequences: the verdict is
   `{"ok":true,"entries":N}` or `{"ok":false,"seq","reason","detail"}`, with
   no `rule` and no `lapse` member (§9.3's `(seq, rule, reason)` becomes
   `(seq, reason)` until rules exist); body keys may contain `.` again (the
   prohibition served fact flattening only); recognition (c) holds vacuously.
2. ★ **Signatures are verified in the kernel**, standard library only, by a
   strict rule (S < L, canonical A and R, cofactorless, k mod L, sha512 and
   ssh-ed25519 only). §9's refusal list and §5's "pure, deterministic" were read
   as outranking §5's parenthetical `ssh-keygen -Y verify`, which remains the
   signing tool and a test oracle. `ssh-keygen` accepts two things the kernel
   refuses, each a named, tested difference: S + L (absent on this OpenSSH
   build) and a non-empty reserved field. A hardware key would stop the genesis
   procedure.
3. ★ **Empty SSHSIG reserved field** (counsel's fix 5): OpenSSH signs over an
   empty reserved field whatever the blob carries, so without this rule one
   signature has many valid encodings and a line could be re-encoded while
   staying valid.
4. ★ **Weak public keys refused at declaration** (counsel's fix 5), reason
   `bad_key`: non-canonical encodings and the eight points of small order. A
   small-order key is an identity anyone can sign for (with [k]A taking at most
   eight values, a forger finds a valid (R, S) in a handful of tries). The
   duplicate-pubkey refusal joined `bad_key` (it was `schema`): one key, one
   identity. Weakness is tested before duplication; `no_power` on the signer
   comes before either for a `key` entry.
5. ★ **Trusted base, by content** (counsel's fixes 1 and 2): `kernel/`,
   `kernel2/`, `judge/`, `.github/workflows/`, `SPEC.md`, plus CHARTER.md
   byte for byte. The old path-based guard was unsound: git reports a rename
   under its new name only, so `SPEC.md → docs/SPEC.md` passed it; the pin
   `trusted_rename_admitted` kills that guard. Consequence, tested and
   accepted: a proposal must rebase after Guy changes the trusted base on
   trunk. Until C1's `merge.installs`, these paths change only by a commit Guy
   makes himself, `kernel2/` included; the founding pull request is the stated
   exception (`main` had no judge), and the judge run locally against it
   refuses with `trusted_path` (`transcripts/judge-founding-20261014T012918Z.json`).
6. ★ **`charter_mismatch`** (counsel's fix 6): once trunk has a genesis, every
   proposal is refused while trunk's CHARTER.md does not hash to the recorded
   value. Checked after `trusted_path` (so head's charter equals trunk's by
   then) and before the kernel runs. A test, not a pin; Guy may ask for one.
7. **"Over the line without `sig`"** = canonical re-serialisation of the entry
   minus `sig`; lines must be canonical (sorted keys, ASCII escapes, integers
   only); genesis parent is 64 zeros; `seq` is the line index.
8. **The judge enforces what the log cannot:** trunk's kernel runs, never the
   proposal's; a merge must name trunk's digest (`judge_from_proposal`);
   genesis never arrives by proposal (`genesis_by_proposal`); trunk's log must
   be a byte prefix of the proposal's. No kernel-level `self_judged` check.
9. **`history_rewritten`, "fails at that line"**: an edited line fails at that
   line by its own signature; an edited and re-signed line fails at the next
   line (`parent_mismatch`), which is also how a fork fails.
10. **`final_law_for_all` has no pin at C0.** Non-retroactivity is structural
    (a fold over the prefix; a `key` at *i* governs entries after *i* only),
    and with no rules there is no single site a mutant could edit to make the
    latest law reach back. The property is asserted by
    `test_revocation_does_not_reach_back` and by the simulator's
    `retroactive` kind; the pin returns with rules in C1.
11. **"Signing key derived from git, never from the proposal's claims"** is read
    as: from the SSHSIG blob in the log object at the proposal's commit, which
    the judge reports as a fingerprint; `proposer` is a claim checked against
    it. Commits need not be SSH-signed; the `Proposer:` trailer is a convention.
12. **F1 remains in the `pull_request` job**: the brief asked for it; it is the
    accused's own run. Only the `push: main` run should count for criterion 1.
13. **Stalling and flooding** have no refusal in C0 (liveness; C1). The
    simulator generates them as benign logs the checker must accept, and says so.
14. **Timestamps are recorded, not ordered**, at C0; non-decreasing `ts` is
    C1's first candidate rule (BRIEF-C1.md).
15. **Lone surrogates outrank number defects** in the parse order, so two
    checkers cannot disagree on a line with both.
16. **Not built, reported:** refusing a `key` entry that leaves no key with
    `key` power; comparing `genesis.checker` with trunk's current digest
    (which would freeze the trusted base until C1).

Nothing was imported or copied from `renavondata/assize`; its pins harness was
surveyed and its text-edit discipline (find string occurring exactly once,
disposable copy, causal twin) adopted in spirit. Copied with attribution:
RFC 8032 §7.1 vectors; ed25519-speccheck cases and the eight small-order points
(Apache-2.0; Chalkias, Garillot & Nikolaenko 2020).

## 5. Proposed changes to CHARTER.md

For Guy to sign or decline; nothing here edits the charter.

- §9.1: types at genesis are `genesis`, `key`, `proposal`, `merge`; define
  "the line without `sig`" as canonical form; note that only plain
  `ssh-ed25519` keys sign at C0 and that the SSHSIG reserved field is empty.
- §9.2–9.3: move the law language (Datalog, witnesses, lapse reporting) to C1's
  brief; §9.3's checker signature reads `check(log) → ok | (seq, reason)` at C0.
- §3 Change: state that at C0 the change entries are `key` entries, and that
  a rule entry carries its two witnesses when rules arrive.
- §5 / §9 refusal list: state that signatures are verified in-kernel by SPEC.md
  §6's rule; name `ssh-keygen` as the signing tool only; add that weak public
  keys are refused at declaration.
- §9.6: add the trusted base (`kernel/`, `kernel2/`, `judge/`,
  `.github/workflows/`, `SPEC.md`), compared by content; `charter_mismatch`;
  genesis by Guy's own commit; the byte-prefix rule; promote `merge.installs`
  to C1 so the recorded digest can rotate.
- §9 pins: at C0 the list is `judge_from_proposal`, `unsigned_change` (over
  `key` entries), `history_rewritten` ("fails at that line or, if re-signed,
  at the next"), `fork_admitted`, `unattributed_entry`, `checker_drift`,
  `forged_signature_admitted`, `trusted_path_unguarded`,
  `trusted_rename_admitted`, `weak_key_admitted`, `reserved_bytes_admitted`;
  `final_law_for_all`, `vacuous_rule_admitted`, `impossible_rule_admitted`
  and `redundancy_unreported` return with the rules in C1.
- §9 criterion 3: record Guy's target of 450 lines beside the 1,000 limit.
- §12: the stop condition "Datalog cannot express a C0 rule" is void at C0.

## 6. Transcripts

- `transcripts/tests-20261014T012918Z.txt` — 115 tests under Python 3.12.8, OpenSSH 10.5p1.
- `transcripts/pins-20261014T012918Z.txt` — every mutant with the wrong verdict it produced.
- `transcripts/count-20261014T012918Z.txt` — kernel line count.
- `transcripts/judge-founding-20261014T012918Z.json` — the judge on `c0-founding` against `main`.
- `sim/runs/20261014T012421Z-52194.json` — the full simulator budget.
- Pull request CI: `tests` passed on ubuntu-latest on the documents commit `c9b67b1`, the final code state ([run 38496000482](https://github.com/renavondata/jack/actions/runs/38496000482)); the three intermediate heads failed as the tree was brought into line commit by commit; the run on this head is on the pull request; `judge` did not run, as expected (no workflow on `main` yet).
- The rule-era transcripts and simulator runs are on branch `c1-law-draft`.

## 7. What C0 still needs

1. The second checker, from `SPEC.md` alone, by another model family
   (`kernel2/README.md`); it enters `main` by Guy's own commit, since
   `kernel2/` is trusted; then `checker_drift` KILLED, 10⁵ seeds through both.
2. Guy's reading of the 392 lines and his signature on genesis, committed to
   `main` by him; then `judge` and `tests` as required checks.

## 8. Exit report (counsel, 17 October 2026)

Proposer: counsel `claude-fable-5-1`, session `session_01GMQpCypjVueCfEEkLaPiSm`. State of `main` at
`46543de`. Everything cited is on `main` or under `transcripts/`.

### 8.1 Verdict against §9's criteria, as amended by A1.5

| # | criterion | state | evidence |
|---|---|---|---|
| 1 | every pin KILLED and its twin passes, in CI, from trunk | **MET** | `tests` on `push: main` is green on every push since genesis; latest on `46543de`. 34 mutants across 22 pins KILLED, 0 SURVIVED, 0 STALE, 0 twin failures, 0 PENDING. Every pin A1.5 names is present (`weak_key_declared` is the pin `weak_key_admitted`); `checker_drift` KILLED against kernel2; four pins for the differential (SPEC §9a.7) and four for the judge's new grounds (§10.7–10). |
| 2 | both checkers agree, entry by entry and reason by reason, on the real log and 10⁵ simulated logs from a pre-committed seed list | **MET** | Real log: the CI self-check runs both checkers over `log.jsonl` (one entry, genesis) on every push; they agree. Simulated: `harness/diff.py`, built to SPEC §9a, compared **every proper prefix and the whole log** of all 10⁵ seeds of `sim/seeds.txt` (committed at `3a53b5a` on 13 Oct, before any run; SHA-256 `011b2ee0…`, recorded in each report), in both checkers, verdicts parsed strictly: **100,000 logs, 658,885 prefixes, 0 disagreements, 0 uncompared**, in twelve ranges covering 0–100000 without gap, all on commit `46543de` (`transcripts/diff-100000-20261017T1001Z-part00.json` … `part11.json`). The 32 spec vectors and their 81 prefixes: 0 disagreements. |
| 3 | kernel within 450 lines (A1.5) | **MET** | 411 physical lines: `log.py` 164, `sig.py` 140, `check.py` 107. CI counts it on every push. |
| 4 | Guy has read the kernel and signed genesis | **MET, with a note** | Genesis `95679e7`, committed by Guy, ts `2026-10-14T05:41:39Z`; one key, `guy-master`, all four powers; charter hash `383867d0…` equals `CHARTER.md` with A1. The kernel was 392 lines at genesis and is 411 now, the difference being SPEC round 2 (`0fecdf5`, `2d7e9a9`); whether Guy has read those nineteen lines is his to say. Branch protection on `main`: required checks `judge` and `tests`, strict; no force-push, no deletion; `enforce_admins` off (A1.4); ruleset "append-only branches" active. |

No stop condition of §9 fired. **Counsel recommends promotion.** Promotion is Guy's act (§7); C0 has no
entry type for it, so it is recorded outside the log, as a signed tag on the merge commit of this report
(8.5). That gap is C1's (BRIEF-C1.md).

### 8.2 What happened between the founding report and exit

| commit | what | found by |
|---|---|---|
| `da2a744` | Amendment A1: C0 is the record | counsel's review of PR #1 |
| `95679e7` | genesis, by Guy | — |
| `738b20a` | pin `checker_drift` | counsel |
| `0610a74`, `a6f36b4` | kernel2 from SPEC.md alone (Codex); Gemini's cold review | — |
| `0fecdf5`, `2d7e9a9` | SPEC round 2: timestamps as real instants in ASCII digits; nesting depth; long integers; key declarations with exactly four members; one pubkey, one key_id; every log has one verdict | Gemini's review, Codex's questions, counsel's byte probes |
| `12fc4ee` | kernel2 revised to round 2 (fresh OpenCode session) | — |
| `08e7335` | the judge honours git's executable bit; pin `kernel2_unrunnable` | counsel: without it every PR after kernel2 would have failed with a judge error |
| `bd0a003` | CI judge self-check on the production path; pin `selfcheck_blind` | counsel |
| PR #2 | `sim/run.py --second` (whole-log); the stale `rewriting` oracle fixed | counsel's first run with `--second` |
| PR #3 | a progress line | Guy's session |
| `6ce3ab8` | a CI simulator sample | counsel |
| reviews 1–3 | counsel's harness found short of criterion 2 three times (8.3) | Codex, Gemini, GPT, cold |
| `04ad395` | SPEC §9a (the differential as text) and §10.7–10 (attribution, counsel does not build, scope, size cap) | counsel's text, Guy's push |
| `judge-rules` | the judge's new grounds, four pins (Claude Code builder; counsel's cold read; Guy's push) | — |
| `947e192`, `62aabe6` | the CI sample moved to the differential | Guy |
| PR #5 | `sim/run.py` back to the founder's runner plus the progress line; counsel's harness and its transcript removed | Guy |
| PR #6 | `harness/diff.py` built to §9a, 60 lines, four pins (Claude Code builder; Gemini's cold read: "implements §9a") | — |
| PR #7 | `--seeds A:B` so the run of record splits across processes; bound 65 | Guy's amendment to §9a |

### 8.3 Disclosures

1. **Counsel's harness was wrong three times, and the reviews said so.** Counsel wrote a differential
   into `sim/run.py` (PR #2) and twice more on an unmerged branch. Cold reviews by three families
   (`transcripts/REVIEW-sim.md`, `-2.md`, `-3.md`) found: whole-log comparison where the criterion says
   entry by entry; loose verdict parsing (`{"ok":1}` equal to `{"ok":true}`, a wrong exit status
   ignored); a sampling regression counsel introduced while fixing the first. The branch was discarded.
   The differential was then specified as text (SPEC §9a), built by a builder session, read cold by
   another family, and is what criterion 2 rests on. The earlier 10⁵ runs under `--second` are
   superseded and their transcript removed (PR #5); the run of record is 8.1's.
2. **The record has one entry.** No proposal appended a `proposal` entry and no `merge` entry exists;
   the four entry types are built and tested but, bar genesis, unused. Appending entries is the clerk's
   work and the clerk is C1. Criterion 2's real-log leg is therefore met on one line.
3. **The generator changed after the seed list was committed**, once, in PR #2: SPEC round 2 made a
   key declaration exactly four members, and the `rewriting` attack still added one, so its expected
   verdict was stale. The seed list is unchanged; the fix is a regression test; every run cited is after
   it. The CI sample (300 seeds and the vectors on every push) exists so that this is caught next time.
4. **No window was stated for C0**, and the layer was patched in place throughout. §6 asks for both. C1
   states its window before it opens, and a trusted-base defect inside the window restarts it.
5. **Two commits carry placeholder attribution**: `0fecdf5` and `2d7e9a9` have
   `Proposer: reviewer <gemini model id> <session id>` unfilled. Recorded, not rewritten. Since
   `judge-rules`, a proposal with no party is refused (`unattributed_proposal`); the party is still a
   claim until keys exist (C1).
6. **The trusted base changed after genesis.** Genesis records digest `d3ac5ef5…`; trunk's is now
   `13ea4b40…` (kernel2, the judge's fixes and grounds, the CI). A1 does not compare them; `merge.installs`
   (C1) makes such changes entries. `judge/scope.json` caps counted code at 3,000 lines and C0 exits at
   2,936; C1 sets its own number.
7. **Not provable by the differential:** that kernel2 is an independent implementation. That rests on
   the trusted-base rule, its provenance (`kernel2/NOTES.md`, `REVIEW-gemini.md`) and Guy's reading.

### 8.4 Counsel's forecasts (§11)

| id | p | resolution | note |
|---|---:|---|---|
| K5 | 0.75 | true | 411 ≤ 1,000 |
| K6 | 0.65 | **Guy's ruling** | "disagree on at least one *simulated* log". For true: three disagreements were found and fixed during C0 (timestamp digits, deep nesting, a long integer). For false: all three came from reviews and byte probes, none from a simulated log; on simulated logs no run, before or after the fixes, found one. Counsel does not resolve its own forecast (§2.1). |
| K7 | 0.50 | true iff promoted by 27 Oct | founding began 13 Oct |
| K1, K2 | 0.60, 0.35 | 21 Oct | the weekly measurement |
| K3, K4, K8 | 0.20, 0.35, 0.40 | later | |

Counsel's in-session forecasts on its own harness (p = 0.3, 0.75, 0.7 that reviews would come back clean)
all missed; the record of that is in the reviews.

### 8.5 After promotion

Promotion: a tag `c0-exit` signed by Guy on the merge commit of this report, its message carrying the
decision and the K6 ruling. C0 is then frozen: the trusted base changes only for a defect, by Guy's push,
each recorded as a precedent, until C1's `merge.installs`. No `key` entries until C1 guards the master key
against revoking its own `key` power. A CHARTER.md edit makes the judge refuse every proposal
(`charter_mismatch`) until C1's charter-amendment entry.
