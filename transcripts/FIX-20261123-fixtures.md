# FIX-20261123-fixtures: build the padded promotion fixture once, not for every test

Counsel's text, 23 November 2026, for the sovereign's read (CHARTER A2.10). The builder makes it under `transcripts/sessions/fix.md`, on branch `FIX-20261123-fixtures`, and proposes it. It changes test fixtures only. No judge, kernel, tool, pin or production path changes, and no existing test asserts anything new. It is one of three texts for the slow `tests` job, with FIX-20261123-check and FIX-20261123-pins-parallel. None needs another.

**Why.**
- **Every fixture now carries the padded prefix.** Since the push that moved the promotion evaluator under `judge/` (log seq 7281), every fixture repository that `harness/gitfix.make_repo` builds with a log carries an installed promotion prefix. `tests/promotion_fixture.install` pads the log past seq 5564, the boundary of SPEC §10 item 15 (`judge/judge.py` line 221), and adds a grant and a push.
- **The suite has grown about two and a half times slower.** The `tests` job on `main` took 10 minutes at 2026-11-22T18:01Z, with unit tests in 163 s and pins in 187 s. Since the move it takes 23 to 28 minutes: unit tests 421 to 511 s, pins 690 to 802 s (ADVISER.md entry 140).
- **Every proposal pays this three times:**
  - `tools/jack proposal`'s own check;
  - the `tests` job on the proposal's head;
  - the `tests` job on the head that carries its merge entry.

  Court proposals now take 50 to 70 minutes from opening to merge, against a median of 22 before the move. The court cannot carry its hourly work, and new forecast streams are paused until this is fixed (the sovereign's "Yes", ADVISER.md entry 143).
- **Where the time goes.** A profile of `tests.test_judge` on `main` (`d7fc0493`) took 367 s for 49 tests:
  - `make_repo`: 149 s over 178 repositories, of which `install` is 115 s and its `pad` 83 s;
  - `commit_all`: 93 s over 886 commits, most of them of a log of about 5566 lines;
  - the judge's kernel subprocesses: 91 s over 301 calls.

  `pad` re-hashes all 5564 padding lines into `verified-signatures.json`, and rewrites that file, on every call (ADVISER.md entry 141).
- **What this does, and what it does not.** The rest of the time is the judge itself. Each call of `judge/judge.py` on a padded fixture takes about a second: it runs the kernel over the 5566-entry log twice and parses the log several times more. That is trusted code, and the tests exist to run it. A prototype of points 1 and 2 below, counsel's own and not proposed, was measured on one machine with two cores, `main` first:
  - the unit tests went from 638 s to 552 s, about a seventh less;
  - the pins went from 926 s to 885 s, about a twentieth less. Nearly all of the pins' time is the judge's, `judge/status.py`'s and the pins' own (ADVISER.md entry 150).

  So this text takes about a minute off each `tests` job and off each session's check. It does not restore the 10-minute job, and it does not end the pause by itself.

**The change.**
1. **The padded, installed base is built once and copied.** Within one test process, a fixture repository that needs the installed prefix is made by copying a repository already built with the same inputs: the trusted-base files copied from the same root, the same world and keys, the same timestamps. It is not rebuilt by re-padding, re-hashing and re-committing the log. The copy may be a `git clone --local` or a copy of the directory. Either way, its branches, every commit's tree and its `log.jsonl` must equal those of a repository `make_repo` builds today from the same inputs. Commit hashes may differ only as two such builds' differ today, by commit time. The cache is keyed by the world and by the bytes it copies from the root: every file under `kernel/` and `judge/`, with its path and mode. It is never keyed by the root's path. So `pins/run.py`'s unmutated copies of the tree, each at a new path, share one base, and a mutant, whose bytes differ, gets its own. Every fixture gets its own copy, and no test ever touches the cached base itself.
2. **The verified-signature set is computed once per padded prefix.** `promotion_fixture.pad` adds a prefix's hashes to `verified-signatures.json` once, not on every call. Every signature it caches is still verified with OpenSSL first, as today.
3. **Nothing else.**
   - No test, twin or mutant asserts anything different.
   - No test is added or removed, but the one test that Acceptance (iii) asks for.
   - No memo of a kernel check is added: the fixture's kernel copy checks every entry of every log as today, signatures excepted as today.

**Paths.**
- **May change:** `harness/gitfix.py`, `tests/promotion_fixture.py`, `tests/fixture_signatures.py`, a new test file under `tests/` for (iii)'s test, and a new helper file under `tests/` or `harness/` if the cache needs one.
- **May not change:** anything under `judge/`, `kernel/`, `kernel2/`, `pins/`, `spec/`, `sim/` or `tools/`, and no other file.

**Acceptance.**
- **(i) The same results.** On `origin/main` and at the head, on the same machine:
  - `python3 -m unittest discover -s tests -t .` passes, with `Ran N tests` on `origin/main` and `Ran N+1 tests` at the head, the one being (iii)'s test;
  - `python3 pins/run.py` ends with the same line on both, today `KILLED 158, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`.
- **(ii) Not slower, and the unit tests faster.** Run `python3 -m unittest discover -s tests -t .` three times on the same machine, one after the other: on `origin/main`, at the head, and on `origin/main` again. The head's time must be under the faster `origin/main` time. Run the pins once on each tree. The head's time must be at most 1.05 times `origin/main`'s. Report all five times. A machine that other sessions share can slow any one run, and the second `origin/main` run is there to show it. If either bound is missed, push the branch, do not propose, and report the times.
- **(iii) A test of the cache itself.** Show that two fixtures built from the same inputs, one built and one copied, have equal branches, equal trees for every commit, and byte-equal `log.jsonl`. Show also that a fixture built from a root whose `kernel/` or `judge/` bytes differ is not served from the cache, and that one built from a byte-identical root at another path is. Put this under `tests/`, as one new test, and name it in the report.
- **(iv) Report the time of the `tests` job on the proposal's head**, from its run on GitHub, with the time of each step.
