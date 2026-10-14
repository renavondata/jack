# kernel2 — the second checker (not yet written)

CHARTER §3 Adjudication and §9.4: *an independent implementation of the log and
the validity predicate, in another language, written from the spec text alone
by an author from a different model family.* Until it exists, the pin
`checker_drift` is reported **PENDING** and §9 criteria 1 and 2 cannot be met.

## Rules for its author

- **Read only `SPEC.md`** (and the vector files it names under `tests/vectors/`
  and `spec/vectors/`). Do not read `kernel/`, `tests/`, `pins/` or `sim/gen.py`.
  If `SPEC.md` is ambiguous or silent, **stop and record the question** in
  `kernel2/QUESTIONS.md`; an ambiguity is a finding, never a guess (CHARTER §9,
  "stop and report").
- Not Python. Any language whose standard library (or vendored, attributed code)
  gives you SHA-256, SHA-512, big integers and base64. No network, no clock, no
  LLM call at run time. Nothing imported from `renavondata/assize`.
- The author must be a model from a family other than Anthropic's (the kernel's
  author was `claude-fable-5-1`). Record model and session in every commit's
  `Proposer:` trailer, as the founding commits do.
- Deliver into this directory only. `kernel2/` is part of the trusted base, so
  the judge refuses any proposal that touches it (`trusted_path`); like every
  trusted-base change until C1, it enters `main` by a commit Guy makes himself
  (he fetches the author's branch and pushes it), after reading it.

## Interface (the CLI contract, SPEC.md §9)

- `kernel2/check <path-to-log.jsonl>` — an executable file (a script with a
  shebang, or a tiny launcher that runs your binary). Build steps, if any, go
  in `kernel2/build.sh`; the judge and the harness run `kernel2/check` directly
  on ubuntu-latest, so prefer something that needs no build.
- stdout: exactly one JSON object, `{"ok":true,"entries":N}` or
  `{"ok":false,"seq":n,"reason":"code","detail":"..."}`.
- exit 0 if ok, 1 if refused, 2 on usage or I/O error.

## How it will be exercised

- **Differential harness:** `python3 harness/diff.py --b kernel2/check 'spec/vectors/logs/*.jsonl'`
  compares both checkers verdict by verdict (minus `detail`). `sim/run.py` will
  gain a `--second kernel2/check` flag to run the 10^5 seeded logs through both.
- **Pins:** every pin in `pins/pins.py` runs its fixtures through the CLI, so
  the same fixtures run against `kernel2/check` unchanged. `checker_drift`
  applies a text edit to `kernel2/check` that flips a reason code and expects
  the harness to turn red; its mutant is defined already (`pins/pins.py`), so the
  pin leaves PENDING the moment `kernel2/check` exists — and fails if your file
  does not contain the literal string `bad_signature`.
- **Judge:** `judge/judge.py` runs `kernel2/check` from trunk when present and
  refuses with `checker_drift` on any disagreement.

## What done looks like

Both checkers agree on `spec/vectors/logs/*`, on the real log, and on the
committed seed list (`sim/seeds.txt`, 10^5 seeds); `checker_drift` is KILLED;
and `kernel2/QUESTIONS.md` is either empty or has been answered by a change to
`SPEC.md` recorded in REPORT.md.
