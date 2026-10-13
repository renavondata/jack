# C0 report — the record and the checker

Founding session, 13 October 2026. Proposer: founder `claude-fable-5-1`, session
`743dd139-c951-42b5-8e20-14cce485acab`. Branch `c0-founding`, pull request
[#1](https://github.com/renavondata/jack/pull/1) against `main`. CHARTER.md is unchanged; every change proposed to it is
in §4 below.

## 1. Verdict against §9's pre-stated criteria

| # | criterion | state | evidence |
|---|---|---|---|
| 1 | every pin KILLED and its twin passes, in CI, from trunk | **OPEN** | 15 mutants across 12 pins KILLED with passing twins, locally and in the pull request's `tests` run ([run 38442174913](https://github.com/renavondata/jack/actions/runs/38442174913): 147 tests OK, 15 KILLED / 1 PENDING, 658 lines). `checker_drift` is **PENDING**, named, never passed: there is no second checker to drift. "From trunk" waits for the merge; `tests.yml` runs on `push: main`. |
| 2 | both checkers agree, entry by entry and reason by reason, on the real log and 10⁵ simulated logs from a pre-committed seed list | **OPEN** | No second checker exists (by design; `kernel2/README.md`). The real log is empty until genesis is signed. Against the simulator's independent oracle: two full runs within the session's ten-minute budget each, 37,146 and 36,352 seeds (73,498 cases in all, the second run from the same first seed after a generator fix), 0 disagreements between the kernel and the oracle, and the prefix, sticky-refusal and determinism properties held on every case. The seed list (`sim/seeds.txt`, 10⁵) was committed before any run. |
| 3 | kernel within 1,000 lines; an excess reported, never hidden | **MET** | 658 physical lines: `check.py` 221, `log.py` 186, `sig.py` 131, `datalog.py` 120, `__init__.py` 0 (`transcripts/count-*.txt`). `judge/judge.py` (177 lines) is outside the kernel and the count. |
| 4 | Guy has read the kernel and signed genesis | **OPEN** | Guy's act. `README.md` gives the procedure; `genesis.template.json` and `tools/genesis.py` carry no key of his. |

C0 is not at exit. The posterior that it reaches exit without touching the
kernel is high: criterion 3 is met with margin, and criteria 1–2 now turn on one
deliverable, the second checker, plus Guy's reading. None of §9's stop
conditions fired: stratified Datalog expressed every rule the pins and the
simulator needed; the kernel is 658 lines, not 1,500; the charter's ambiguities
were resolvable by readings recorded in §3, two of them by Guy in session.

Counsel's forecasts (CHARTER §11): K5 (kernel within 1,000 lines at exit) looks
likely; the kernel would need to grow by half. K6 (the checkers disagree on at
least one simulated log before exit) is unresolved; the 1 : 1 odds counsel gave
it remain the best estimate, and SPEC.md §16 lists the choices most likely to
produce that disagreement.

## 2. Counts

| what | count |
|---|---|
| commits on `c0-founding`, each with `Proposer: founder claude-fable-5-1 <session>` | 16 |
| kernel physical lines (criterion 3) | 658 |
| tests | 147 (local run under Python 3.12.8 / OpenSSH 10.5: 146 pass, 1 skipped by design (`test_named_difference_s_plus_L`: this OpenSSH build also rejects S ≥ L, so the tolerated difference is absent here; on GitHub's ubuntu-latest image the test *passes*: that build's `ssh-keygen` accepts S+L, so the named difference is real there) |
| pins / mutants | 13 pins; 15 mutants KILLED, 0 SURVIVED, 0 STALE, 0 twin failures; 1 PENDING |
| simulator, first full run | 37,146 seeds in 574 s on 12 workers; 1 failure, a generator error on seed `c35942cde0736065` (fixed in the next commit; not a kernel defect); 0 kernel disagreements with the oracle |
| simulator, second full run | 36,352 seeds in 571 s on 12 workers; 0 failures across all 21 kinds (`sim/runs/20261013T175038Z-36352.json`) |
| projected cost of 10⁵ seeds | about 64 seeds/s on 12 cores → roughly 26 minutes; the exit criterion is reachable in one sitting once kernel2 exists |
| reason codes | 19 in the checker, each covered by a spec vector; 5 judge-level |
| spec vectors | 26 signed logs with required verdicts; 6 canonical-JSON vectors; 5 RFC 8032 and 12 speccheck Ed25519 vectors |

## 3. Decisions and ambiguities

Readings the brief forced; each is recorded in SPEC.md §16 and is Guy's to
overturn. Two were put to Guy in session and decided by him (marked ★).

1. ★ **Signatures are verified in the kernel**, standard library only, by a
   strict rule (S < L, canonical A and R, cofactorless, k mod L, sha512 and
   ssh-ed25519 only). §9's refusal list ("no dependency outside the standard
   library") and §5's "pure, deterministic" were read as outranking §5's
   parenthetical `ssh-keygen -Y verify`, which remains the signing tool and a
   test oracle. Consequence: `ssh-keygen` may accept what the kernel refuses;
   the one such case (S+L) is a named, tested difference, absent on this
   OpenSSH build. A hardware key would stop the genesis procedure.
2. ★ **§4's non-contradiction row** ("the satisfying witnesses pass the whole
   law together") is built in a weak form: on admitting a rule, every rule in
   force must keep at least one satisfying witness that passes the whole law;
   the new rule may carry `replacements` that join older rules' witnesses;
   otherwise `orphans_rule`. Strict joint compliance would have refused new
   rules that merely narrow an older rule's example of compliance.
3. **Trusted base** (Guy's amendment to the plan): the digest covers `kernel/`,
   `judge/`, `.github/workflows/` and `SPEC.md`; the judge refuses any
   proposal touching them or `CHARTER.md` (`trusted_path`). Until C1's
   `merge.installs`, they change only by a commit Guy makes himself. The
   founding pull request is the stated exception: `main` had no judge, and the
   judge run locally against it refuses with `trusted_path`
   (`transcripts/judge-founding-*.json`), as it should.
4. **"Over the line without `sig`"** = canonical re-serialisation of the entry
   minus `sig`; lines must be canonical (sorted keys, ASCII escapes, integers
   only); genesis parent is 64 zeros; `seq` is the line index.
5. **The judge enforces what the log cannot:** trunk's kernel runs, never the
   proposal's; a merge must name trunk's digest (`judge_from_proposal`);
   genesis never arrives by proposal (`genesis_by_proposal`, since before
   genesis anyone's genesis would be admissible); trunk's log must be a byte
   prefix of the proposal's. No kernel-level `self_judged` check: with no
   rotation mechanism among the six types it would freeze the digest forever.
6. **`history_rewritten`, "fails at that line"**: an edited line fails at that
   line by its own signature; an edited and re-signed line fails at the next
   line (`parent_mismatch`), which is also how a fork fails.
7. **`final_law_for_all`**: non-retroactivity is structural (a prefix fold), so
   the only mutant that can reach back is removing the candidate filter; the
   plan's second mutant ("rules admitted at or before i") has no site in the
   code and was dropped. The fixture still asserts that a rule entry is judged
   by the law before it.
8. **Witnesses** are judged by recognition (c) only; a `repeal` carries no
   witnesses; `key` is not a change entry; the violating witness must be
   violated by the new rule's own id; lapse is tested against the current
   prefix, oldest first, one at a time.
9. **"Signing key derived from git, never from the proposal's claims"** is read
   as: from the SSHSIG blob in the log object at the proposal's commit, which
   the judge reports as a fingerprint; `proposer` is a claim checked against it.
   Commits need not be SSH-signed; the `Proposer:` trailer is a convention.
10. **F1 remains in the `pull_request` job**: the brief asked for it; it is the
    accused's own run. Only the `push: main` run should count for criterion 1.
11. **Stalling and flooding** have no refusal in C0 (liveness; C1). The
    simulator generates them as benign logs the checker must accept, and says so.
12. **No comparison built-ins**: a uniqueness rule is inexpressible at C0; a
    rule over `signed_by` can have no satisfying witness and is inadmissible.
13. **Deferred §4 checks**, reported not built: generality (no party constants
    in rules), constancy (change-rate reporting). Also not built: refusing a
    `key` entry that leaves no key with `key` power.
14. **Lone surrogates outrank number defects** in the parse order, so two
    checkers cannot disagree on a line with both.

Nothing was imported or copied from `renavondata/assize`; its pins harness was
surveyed and its text-edit discipline (find string occurring exactly once,
disposable copy, causal twin) adopted in spirit. Copied with attribution:
RFC 8032 §7.1 vectors; ed25519-speccheck cases (Apache-2.0).

## 4. Proposed changes to CHARTER.md

For Guy to sign or decline; nothing here edits the charter.

- §5 / §9 refusal list: state that signatures are verified in-kernel by SPEC.md
  §6's rule; name `ssh-keygen` as the signing tool only.
- §4, non-contradiction row: adopt the weak form (decision 2) or restore the
  strict one knowingly.
- §9.1: define "the line without `sig`" as canonical form; add `replacements`
  to the rule entry; note that only plain `ssh-ed25519` keys sign at C0.
- §9.6: add the trusted base, `trusted_path`, genesis by Guy's own commit, and
  the byte-prefix rule; promote `merge.installs` (or a `checker` entry type)
  to C1 so the recorded digest can rotate.
- §9 pins: word `history_rewritten` as "fails at that line or, if re-signed, at
  the next"; add the three pins Guy introduced in session.
- §3 Change: "A rule entry carries its two witnesses" (a repeal carries none).

## 5. Transcripts

- `transcripts/tests-20261013T180044Z.txt` — 147 tests under Python 3.12.8, OpenSSH 10.5p1.
- `transcripts/pins-20261013T174618Z.txt` — every mutant with the wrong verdict it produced.
- `transcripts/count-20261013T174618Z.txt` — kernel line count.
- `transcripts/judge-founding-20261013T174618Z.json` — the judge on `c0-founding` against `main`.
- `sim/runs/20261013T173944Z-37146.json` — first full simulator run.
- `sim/runs/20261013T175038Z-36352.json` — second full simulator run, after the generator fix.
- Pull request CI: `tests` passed on ubuntu-latest in 21 s ([run 38442174913](https://github.com/renavondata/jack/actions/runs/38442174913)); `judge` did not run, as expected (no workflow on `main` yet).

## 6. What C0 still needs

1. The second checker, from `SPEC.md` alone, by another model family
   (`kernel2/README.md`); then `checker_drift` KILLED, 10⁵ seeds through both.
2. Guy's reading of the 658 lines and his signature on genesis, committed to
   `main` by him; then `judge` and `tests` as required checks.
3. A decision on `kernel2/`'s place in the trusted base.
