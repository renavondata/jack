# jack

Bayesian self-improving agent under a small core of law; judged by assize.

This repository is the core: an append-only, hash-chained, SSH-signed record
(`log.jsonl`), the law as data (stratified Datalog rules with witnesses), a
checker small enough to read entire, and a judge that runs trunk's checker over
every proposal. `CHARTER.md` is the founding text; `LAW.md` reads its §§2–3
against the code; `SPEC.md` is the contract a second checker is written from;
`REPORT.md` is the C0 verdict.

## Layout

| path | what |
|---|---|
| `kernel/` | the checker: `log.py` (format, schemas, facts), `sig.py` (SSHSIG + Ed25519), `datalog.py` (rules as data), `check.py` (the validity predicate, CLI). Standard library only; no clock, network or LLM. |
| `judge/judge.py` | trunk's kernel over a proposal's appended entries, every fact from git; guards the trusted base |
| `.github/workflows/` | `judge.yml` (pull_request_target, read-only, no secrets), `tests.yml` (tests, pins, line count) |
| `pins/` | the pins as data and their runner (text-edit mutants on disposable copies) |
| `sim/` | seeded simulator, committed seed list, run transcripts |
| `harness/` | throwaway keys, log builders, git fixtures, the differential harness |
| `kernel2/` | the second checker's interface (to be written by another model family from `SPEC.md`) |
| `spec/vectors/` | canonical-JSON vectors and signed logs with required verdicts |
| `tools/` | `count_kernel.py`, `digest.py`, `genesis.py`, `vectors.py` |
| `transcripts/` | pin and test run outputs cited by `REPORT.md` |

## Run it

```
python3 -m kernel.check log.jsonl          # → {"ok":true,"entries":N,"lapse":[...]} or a refusal; exit 0/1
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
   admissible.

5. **Only then** make `judge` and `tests` required status checks on `main`.
   Until genesis is on `main`, `log.jsonl` is absent and both workflows pass
   trivially on an empty record.

## The trusted base

`kernel/`, `judge/`, `.github/workflows/` and `SPEC.md` are the trusted base;
their digest is what genesis records as `checker`, and the judge refuses any
proposal whose diff touches them or `CHARTER.md` (`trusted_path`). Until C1
brings a lawful change path (`merge.installs`, see `BRIEF-C1.md`), they change
only by a commit Guy makes himself. The founding pull request is the stated
exception: `main` had no judge yet.
