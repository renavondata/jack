# jack

Bayesian self-improving agent under a small core of law; judged by assize.

This repository is the core: an append-only, hash-chained, SSH-signed record
(`log.jsonl`), a checker small enough to read entire, and a judge that runs
trunk's checker over every proposal. The record carries ten entry types
(`kernel/log.py` `TYPES`): `genesis`, `key`, `proposal`, `merge`, `amend`,
`push`, `decision`, `spec_conflict`, `forecast` and `resolution`.

**Where it stands** (5 November 2026). The layers are pre-stated windows, each
with criteria written before it opens (`CHARTER.md` §8–§9, A3–A5; `REPORT.md`
holds each exit report).
- **C0**, the record and the checker: exit report `REPORT.md` §8 (17 October).
- **C1a**, the record says things about the world (`forecast`, `resolution`):
  promoted by the sovereign's `decision promote C1a`, seq 188.
- **C1b**, the clerk and its writs, and the liveness statistic: promoted at
  seq 337.
- **C2a**, the value statistic and the streams: opened by the push at seq 367
  on 1 November. Its first window cannot promote: criterion 7 read nine off-log
  repairs on its acts evidence. Its stated end is read two ways and unruled
  (`transcripts/CASES.md`).
- **C2a-prime**, the window that follows it (`transcripts/BRIEF-C2a-prime-draft.md`),
  and **C2b**, the election of proposers (`transcripts/BRIEF-C2b-draft.md`), are
  pre-stated and not yet open.

`CHARTER.md` is the founding text, with its amendments A1–A5 appended. `LAW.md`
reads its §§2–3 against the code and binds nothing. `SPEC.md` is the contract
a second checker is written from. `RUNBOOK.md` documents the verbs of
`tools/jack`. `transcripts/CASES.md` indexes the sovereign's rulings and says
where each part of the law is written; it binds nothing.

## Layout

| path | what |
|---|---|
| `kernel/` | the checker: `log.py` (format, schemas), `sig.py` (SSHSIG + strict Ed25519, weak keys), `check.py` (the validity predicate, CLI). Standard library only; no clock, network or LLM. |
| `kernel2/` | the second checker, in Go, written from `SPEC.md` by another model family |
| `judge/` | `judge.py`: trunk's kernel over a proposal's appended entries, every fact from git; guards the trusted base, the charter hash and each party's paths (`scope.json`) |
| `.github/workflows/` | `judge.yml` (pull_request_target, read-only, no secrets), `tests.yml` (tests, pins, line counts, the judge's self-check, the simulator sample) |
| `pins/` | the pins as data and their runner (text-edit mutants on disposable copies) |
| `sim/` | seeded simulator, committed seed list, run transcripts |
| `harness/` | throwaway keys, log builders, git fixtures, the differential harness |
| `spec/vectors/` | canonical-JSON vectors and signed logs with required verdicts |
| `tools/` | `jack` (the verbs; `RUNBOOK.md`), `entry.py` (prepare, assemble and score entries), `clerk.py` (the writs), `status.py` (each window's criteria and statistics), `value.py` (the value statistic), `count_kernel.py`, `digest.py`, `vectors.py`, `enforcement.json` (the enforcement map) |
| `transcripts/` | briefs, reviews, rulings, evidence and run outputs cited by the reports |

## Run it

```
python3 -m kernel.check log.jsonl            # → {"ok":true,"entries":N} or a refusal; exit 0/1
python3 -m unittest discover -s tests -t .   # unit tests (needs ssh-keygen and git on PATH)
python3 pins/run.py                          # every mutant KILLED with a passing twin
python3 tools/count_kernel.py --limit 500    # kernel physical lines; 500 is the bound status.py reads (criterion 3), 1,000 the tool's default
python3 tools/status.py                      # each window's criteria and statistics on the current tree
python3 tools/clerk.py                       # every open writ, with its holders and deadline
python3 sim/run.py --budget 600              # seeded simulator within a time budget → sim/runs/
python3 judge/judge.py --trunk main --proposal <branch-or-sha>
```

Python 3.12. The kernel verifies signatures itself; `ssh-keygen` is needed only
to *make* them. Entries are made by the verbs of `tools/jack`, each documented
in `RUNBOOK.md`.

## Genesis

Entry 0 was signed by Guy with his own `ssh-ed25519` key, `guy-master`, holding
all four powers, and committed to `main` by him at `95679e7` (ts
`2026-10-14T05:41:39Z`; `REPORT.md` §8.1, criterion 4). It was prepared and
assembled by `tools/genesis.py`, which was removed from the tree at `879caf9`
once genesis was done; its text is in git's history, and `tools/entry.py`
`prepare` and `assemble` now make every entry.

Genesis never arrives by pull request: the judge refuses any proposal that
introduces entry 0 (`genesis_by_proposal`), because before genesis anyone's
genesis would be admissible. The judge refuses every proposal while trunk's
`CHARTER.md` does not hash to the charter in force: genesis's `body.charter`
until A2, then the latest `amend`'s (`charter_mismatch`). `judge` and `tests`
are required status checks on `main`.

## The trusted base

`kernel/`, `kernel2/`, `judge/`, `.github/workflows/` and `SPEC.md` are the
trusted base; genesis recorded their digest as `checker`, and the trusted base
in force is the `digest` of the latest valid `push` entry (SPEC §7). The judge
refuses any proposal whose trusted-base digest, or whose `CHARTER.md`, differs
from trunk's (`trusted_path`): compared by content, so an edit, a rename, a
deletion or an addition under those paths is refused alike, and a proposal must
rebase after trunk's trusted base moves. These files change only by Guy's
`jack push`, recorded by a `push` entry (SPEC §10, items 1 and 11; `RUNBOOK.md`). The
founding pull request is the stated exception: `main` had no judge yet.
