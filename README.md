# jack

Bayesian self-improving agent under a small core of law; judged by assize.

This repository is the core: an append-only, hash-chained, SSH-signed record
(`log.jsonl`), a checker small enough to read entire, and a judge that runs
trunk's checker over every proposal. **C0 is the record only** (Guy's decision
on counsel's review, 14 October 2026): four entry types, `genesis`, `key`,
`proposal`, `merge`; the law is CHARTER §3's three secondary rules in code;
rules as data, witnesses and lapse arrive in C1 when a first precedent needs
them (`BRIEF-C1.md`; the earlier draft is on branch `c1-law-draft`). `CHARTER.md`
is the founding text; `LAW.md` reads its §§2–3 against the code; `SPEC.md` is
the contract a second checker is written from; `REPORT.md` is the C0 verdict.

## Layout

| path | what |
|---|---|
| `kernel/` | the checker: `log.py` (format, schemas), `sig.py` (SSHSIG + strict Ed25519, weak keys), `check.py` (the validity predicate, CLI). Standard library only; no clock, network or LLM. |
| `judge/judge.py` | trunk's kernel over a proposal's appended entries, every fact from git; guards the trusted base and the charter hash |
| `.github/workflows/` | `judge.yml` (pull_request_target, read-only, no secrets), `tests.yml` (tests, pins, line count) |
| `pins/` | the pins as data and their runner (text-edit mutants on disposable copies) |
| `sim/` | seeded simulator, committed seed list, run transcripts |
| `harness/` | throwaway keys, log builders, git fixtures, the differential harness |
| `kernel2/` | the second checker's interface (to be written by another model family from `SPEC.md`) |
| `spec/vectors/` | canonical-JSON vectors and signed logs with required verdicts |
| `tools/` | `count_kernel.py`, `digest.py`, `genesis.py`, `vectors.py` |
| `transcripts/` | pin, test, count and judge run outputs cited by `REPORT.md` |

## Run it

```
python3 -m kernel.check log.jsonl          # → {"ok":true,"entries":N} or a refusal; exit 0/1
python3 -m unittest discover -s tests -t . # unit tests (needs ssh-keygen and git on PATH)
python3 pins/run.py                        # every mutant KILLED with a passing twin; checker_drift PENDING
python3 tools/count_kernel.py              # kernel physical lines against the 1,000 limit
python3 sim/run.py --budget 600            # seeded simulator within a time budget → sim/runs/
python3 judge/judge.py --trunk main --proposal <branch-or-sha>
```

Python 3.12. The kernel verifies signatures itself; `ssh-keygen` is needed only
to *make* them (tests, fixtures, Guy's genesis).

## Genesis — Guy's procedure, in this order

Nothing binds until entry 0 exists. No key is generated here; Guy signs with his
own **plain `ssh-ed25519`** key. If his master key is a hardware key
(`sk-ssh-ed25519@openssh.com`), `prepare` stops with exit 3: that format signs
a different message and is added later by a change entry. Report it.

1. Prepare the canonical unsigned message (the trusted-base digest is computed
   from the working tree, so do this on a clean checkout of `main`):

       python3 tools/genesis.py prepare --pubkey ~/.ssh/id_ed25519.pub --ts 2026-10-14T09:00:00Z

2. Sign it — exactly this command, which `prepare` also prints:

       ssh-keygen -Y sign -f ~/.ssh/id_ed25519 -n core-entry genesis.unsigned

3. Assemble entry 0 and check it:

       python3 tools/genesis.py assemble genesis.unsigned genesis.unsigned.sig > log.jsonl
       python3 -m kernel.check log.jsonl

4. **Commit `log.jsonl` to `main` yourself.** Genesis never arrives by pull
   request: the judge refuses any proposal that introduces entry 0
   (`genesis_by_proposal`), because before genesis anyone's genesis would be
   admissible. From then on the judge refuses every proposal while `CHARTER.md`
   on `main` does not hash to the value genesis records (`charter_mismatch`).

5. **Only then** make `judge` and `tests` required status checks on `main`.
   Until genesis is on `main`, `log.jsonl` is absent and both workflows pass
   trivially on an empty record.

## The trusted base

`kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and `SPEC.md` are the
trusted base; their digest is what genesis records as `checker`. The judge
refuses any proposal whose trusted-base digest, or whose `CHARTER.md`, differs
from trunk's (`trusted_path`): compared by content, so an edit, a rename, a
deletion or an addition under those paths is refused alike, and a proposal must
rebase after trunk's trusted base moves. Until C1 brings a lawful change path,
these files change only by a commit Guy makes himself. The founding pull
request is the stated exception: `main` had no judge yet.
