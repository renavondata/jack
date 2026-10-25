# BUILD-C1a — the ledger (builder, `builder-1`)

Branch `c1a-ledger`, cut from `main` at `3059176` (`decision: transmute A3`, seq 28). Built to `SPEC.md` as
patched by counsel's text (commit `2ac8532`, read by Guy before any code), `BRIEF-C1.md` (C1a), `RUNBOOK.md`,
`transcripts/AMEND-A3.md`, `transcripts/world-types.md`, `transcripts/REVIEW-brief-3.md` §5 and `kernel2/README.md`.
Nothing under `kernel2/` beyond its README was read; `harness/diff.py` was not run against kernel2.

## 0. Stop: the code cap (BRIEF-C1.md, "Stop and report if … `judge/scope.json` would need to change")

The judge's `code_cap` (SPEC §10.10) counts every Python file under `sim/ harness/ tests/ pins/ tools/`
against `judge/scope.json`'s cap of **5500**. `main` stands at **5101**; this branch, complete, at **5625**,
**125 over**. That is before the reviewer's ten C1a pins, which are under `pins/` and counted too.

| file | added | removed |
|---|---:|---:|
| `sim/gen.py` | 107 | 14 |
| `tests/test_score.py` (new) | 117 | 0 |
| `tests/test_check.py` | 93 | 2 |
| `tests/test_jack.py` | 86 | 11 |
| `tools/entry.py` | 84 | 2 |
| `tests/test_sim.py` | 32 | 5 |
| `tools/jack` | 31 | 31 |
| `tests/test_log.py` | 29 | 0 |
| `tests/test_diff.py` | 8 | 0 |
| `sim/run.py` | 6 | 4 |
| `harness/diff.py` | 1 | 1 |

After the installing push `main` itself would be over the cap, so the judge would refuse every later
proposal with `code_cap`, including the forecast and evidence proposals the window depends on.
I compacted the kernel tests and the simulator once (commit `21f83db`) without dropping a case. I have
not cut further, because the remaining lines are coverage of the new behaviour, and cutting them to fit
would be weakening tests to get green under another name. The choice is Guy's: raise the cap (a
`judge/scope.json` change, by his push, recorded as a finding against the pre-statement, as on
19 October), or rule which coverage goes. The branch is committed locally and **not pushed**, pending that ruling.

## 1. What was built, file by file

**Kernel** (`kernel/log.py`, `kernel/check.py`; `sig.py` unchanged):
- `TYPES` gains `forecast`, `resolution` (ten). `BODY`: `forecast` {`claim` non-empty, `p` integer 1–999,
  `resolves_by` an instant}; `resolution` {`forecast` integer ≥ 0, `outcome` integer 0 or 1, `evidence`
  non-empty}. Booleans fail both integer tests (`_is_int`). `type`/`args` are never read.
- Step 2a: `ts` earlier than the previous entry's `ts` (string comparison) → `ts_decreased`. The previous
  `ts` is state, `None` before genesis, so entry 0 is exempt.
- Step 7: `resolves_by < ts` → `schema`; a `resolution` naming a seq not in the recorded forecasts, or
  already resolved → `schema`; both before the signature.
- Step 8a, after `signer()`: the resolution's `proposer` equals the forecast's recorded proposer →
  `self_judged`. The proposer is the verified principal by then, so two keys of one party are caught.
- Step 9: `forecasts` (seq → proposer), `resolved` (frozenset), `ts`. `State` gains exactly these three fields.
- **`harness/diff.py`**: `REASONS` is the fourteen (SPEC §9, §9a.3); still 62 of its 65 lines.

**Simulator** (`sim/gen.py`, generator revision **`21f83db`**; `sim/run.py`):
- Timestamps never decrease: whole-hour steps, a zero step about one time in ten (so equal timestamps
  are exercised). Hand-built lines (`forking`, `structure`) now take the clock too. `rewriting` tampers a
  key entry's `powers` (one power repeated) instead of its `ts`, since an earlier `ts` is now `ts_decreased`.
- Benign steps now include forecasts (guy or ann, `p` often at 1 or 999, `resolves_by` equal to or after
  `ts`, `type`/`args` sometimes) and resolutions by the other party. ann's genesis key holds
  `proposal, forecast, resolution`.
- The ten kinds of the brief. Every refusing kind yields its refusal or, half the time, its **twin** (the
  nearest entry the law admits), under the same kind name:
  - `ts_decreasing` → `ts_decreased`. The earlier `ts` is 1 s, 1 h or a year back, or 0001-01-01. A bad
    seq, an empty proposer or a stranger's key doesn't mask it. Twin: `ts` equal to the last.
  - `resolution_self` → `self_judged` (same key, or a second key of the forecaster's party declared by
    guy), `bad_signature` (a tampered self-resolution) or `schema` (a self-resolution of an
    already-resolved forecast). Twin: the other party resolves.
  - `resolution_dangling` → `schema`. The target is a non-forecast seq, the resolution's own seq, a later
    seq or 2^53−1, sometimes under a stranger's key. Twin: an open forecast.
  - `resolution_double` → `schema`. Twin: a second, open forecast resolved.
  - `forecast_past` → `schema`. `resolves_by` is 1 s or 400 days before `ts`, sometimes under a stranger's
    key. Twin: `resolves_by` equal to `ts`.
  - `forecast_permille_0` → `schema` (twin `p` 1). `forecast_permille_1000` → `schema` (twin `p` 999).
  - `forecast_boolean` → `schema` (`p` true or false, `outcome` true or false). Twin: 1, or 1 and 0.
  - `forecast_valid`, `resolution_valid`: admitted.
- `sim/run.py` records `by_kind_verdict`: the intended verdicts per kind, so refusals and twins are
  counted separately.

**Verbs** (`tools/jack`, 250 lines; `tools/entry.py`):
- `jack forecast "CLAIM" --p N --by TS [--type T --args JSON]`. Refuses before signing: N outside 1–999;
  TS not an instant or earlier than the clock; an empty claim; `--args` not a JSON object. For guy's key
  it is a main verb (the main ending: commit, self-check, push). For every other party it is a branch
  verb: the entry is appended and committed as `forecast: <claim, whitespace collapsed, 60 chars>`,
  touching `log.jsonl` only, nothing pushed.
- `jack resolve SEQ --outcome 0|1 --evidence E`: branch or main verb as forecast; commit `resolution: SEQ OUTCOME`.
  Refuses before signing, with the kernel's reason in the message: `schema` (SEQ not an unresolved
  forecast, or an outcome not 0 or 1), `self_judged` (the caller's principal is the forecaster's). A
  `sha256:<hex64>` evidence must name `transcripts/evidence/<hex64>` whose SHA-256 is `<hex64>`.
- `jack score [--as-of TS]`: reads the working copy's `log.jsonl`. It makes no entry, signs nothing,
  fetches nothing and requires no clean tree. The logic is `entry.score`: natural log; Laplace base rate
  pooled by type in resolution-seq order; Fractions for p and rate, so four-decimal half-to-even rounding
  is exact. It prints the witness table verbatim, then forecast counts per (`proposer`, `type`), then the
  per-proposer and per-type tables. With `--as-of` it adds the overdue list, by `resolves_by` then seq.
- `jack proposal`: `commit` is the newest commit not on `origin/main` that changes a path other than
  `log.jsonl`, judged by the judge's own `commits_of` and `changed_by`; if there is none, HEAD (a
  forecast-only branch).
- `jack merge`: precondition is SPEC §10.7's own rule, by the judge's functions: the last proposal in the
  head's valid log naming a commit of the PR, followed only by commits that change `log.jsonl`. The
  RUNBOOK's trailer alternative is kept.
- `jack key`: powers are any of `TYPES` ("outside the ten").
- **`--remove` is cut**, third in RUNBOOK's cut order, to keep `tools/jack` at 250. `jack push` now
  prints `git worktree remove ~/git/worktrees/jack/<BRANCH>`. `valid_run` moved, unchanged but for its
  seed-count argument, to `tools/entry.py`, with the clock (`entry.now`).

**Tests**:
- `tests/test_check.py` `Ledger`: twenty refusal cases, each at its step, and their twins; the step-2a order;
  genesis exempt; the state; earlier logs replay unchanged.
- `tests/test_log.py`: the two body schemas, booleans, bounds and ignored members.
- `tests/test_diff.py`: exactly the fourteen codes are verdicts.
- `tests/test_sim.py`: the kinds exist; each refusing kind yields its reason and its twin; timestamps
  repeat but never decrease; the `rewriting` seeds re-found (see §4).
- `tests/test_jack.py`: the forecast branch and main verbs, the refusals, resolve with evidence, the
  merge precondition (a log-only commit after the proposal is merged, a work commit is refused), and
  the `--remove` cut.
- `tests/test_score.py` and the witness `tests/vectors/score.jsonl`: the brief's ten forecasts and six
  resolutions, signed with throwaway keys from `harness/keys.py`, each resolution by a party other than
  the forecaster (`python3 -m tests.test_score` rebuilds it). `jack score` is run as a subprocess in a copy
  of the tools; its first table must equal the brief's table byte for byte, and the whole output is pinned.
  Every figure of the other tables was checked against an independent computation.

## 2. `tools/count_kernel.py --limit 500`

```
kernel/__init__.py            0
kernel/check.py             138
kernel/log.py               170
kernel/sig.py               140
total                       448
```

## 3. Unit tests, pins

`python3 -m unittest discover -s tests -t .` → `Ran 229 tests … OK (skipped=1)`. The skip is
`test_sig.test_named_difference_s_plus_L` ("this OpenSSH build also rejects S >= L"), an environment skip
that predates this branch. `python3 pins/run.py` → `KILLED 50, SURVIVED 0, STALE 0, TWIN FAILED 0, PENDING 0`.
A mutation check of the new kernel lines, on a scratch copy against `tests/test_check.py` and
`tests/test_log.py`, killed nine of nine. The mutants: no step 2a; no `resolves_by` test; dangling
admitted; double admitted; no step 8a; `self_judged` coded `schema`; `p` 0 admitted; `p` 1000 admitted;
`p: true` admitted.

## 4. Simulator run of record

`python3 sim/run.py --budget 600` at generator revision `21f83db` →
`sim/runs/20261025T113336Z-49242.json`: **49,242 seeds** (the first 49,242 of `sim/seeds.txt`, `4178ee380b3a2c0a` …
`8668282caa09ebc5`) in 600.3 s, **0 property failures** (oracle, prefix, sticky_refusal, deterministic). An
earlier run, on the superseded revision `be60b82`, was also clean (48,612 seeds) and was discarded.
`sim/seeds.txt` is unedited. Intended verdicts per new kind, each the kernel's verdict:

| kind | refused (reason: n) | twin / admitted |
|---|---|---:|
| `ts_decreasing` | ts_decreased 990 | 1016 |
| `forecast_valid` | — | 1956 |
| `resolution_valid` | — | 2046 |
| `resolution_self` | self_judged 471, bad_signature 240, schema 249 | 1002 |
| `resolution_dangling` | schema 966 | 958 |
| `resolution_double` | schema 927 | 1007 |
| `forecast_past` | schema 951 | 998 |
| `forecast_permille_0` | schema 987 | 989 |
| `forecast_permille_1000` | schema 1013 | 1005 |
| `forecast_boolean` | schema 1007 | 994 |

The C0 kinds: benign 1976, duplicate_key 1961, flooding 1930, forged 1893, forking 1989, retroactive 1984,
revoked 1983, rewriting 1952, schema 1969, self_judging 2003, stalling 1949, structure 1920, unattributed 1931,
unsigned_change 2036, weak_key 1994.

## 5. Readings where the text was silent, each with my probability that it stands on cold read

1. SPEC patch placement: the §5 note sits directly after the table; step 9's clauses join its semicolon
   list; `2a.`/`8a.` are lines between the numbered steps. **0.9**
2. "The master key" is a key whose principal is `guy`: forecast and resolve are main verbs for it, branch
   verbs for every other party. **0.75**
3. **Score layout (nearest to a conflict).** BRIEF and RUNBOOK say each group prints "forecasts (all)", yet
   the witness table, which must print exactly, has no forecasts column. I print the table verbatim and
   give the forecast counts in their own (`proposer`, `type`) table and as a column of the per-proposer and
   per-type tables. A reader who wants the column inside the first table finds criterion 5 unsatisfiable,
   which is why I did not take that reading. Counsel should settle the layout in the text. **0.5**
4. The per-proposer and per-type groups are, like the pairs, those with at least one resolved forecast;
   "forecasts" counts all of the group's forecasts, resolved or not. **0.7**
5. A forecast whose `type` is absent or not a string has type `free`. **0.5**
6. `jack score` refuses (exit 1, nothing on stdout) a log the kernel refuses, and an `--as-of` that is not
   an instant. **0.7**
7. Overdue means `resolves_by` strictly before `--as-of`, printed under `overdue at TS:` as a table. **0.8**
8. Evidence: only the `sha256:` form is checked (form, file, hash); a run id or commit is any non-empty
   string. "Already in the tree" is the file's presence under the clean-tree precondition, so a gitignored
   file at that path would pass. **0.6**
9. `jack resolve` also refuses an outcome other than 0 or 1 before signing, as `schema`. **0.85**
10. `jack forecast` refuses `--args` that is not a JSON object (BRIEF: "args (any object)"). **0.7**
11. Commit subjects: `forecast: <claim>` with whitespace collapsed, cut at 60 characters; `resolution: <SEQ>
    <OUTCOME>`, since RUNBOOK names no form for it. **0.7**
12. A branch forecast or resolution pushes nothing and opens no PR: `jack proposal` does. **0.85**
13. `jack proposal`'s commit is judged commit by commit with the judge's functions (merges against each
    parent); a branch with only log commits proposes HEAD. **0.7**
14. `jack merge` uses the last proposal in the head's log that names a commit of the PR (the judge's
    rule), and keeps the RUNBOOK's trailer alternative. **0.8**
15. `--remove` is cut; the printed command uses the RUNBOOK's worktree convention. **0.7**
16. A refusing kind and its twin share one kind name, 50/50 by seed. **0.8**
17. `test_rewriting_a_key_entry_is_not_a_schema_refusal`: adding kinds changes which kind every seed
    draws, so its eight seeds were re-found. Its intent is unchanged and it is stronger: it now asserts
    that a key entry was the one tampered. **0.9**
18. The fixture of `tests/test_jack.py` now copies `tests/vectors/weak_keys.json`: two of its twelve seeds
    now draw `weak_key`, which reads that file. **0.95**

## 6. Found, not mine to fix

- **Vectors 40–49 will break `tests/test_vectors.py` and need `tools/vectors.py`.** The test asserts that
  `tools/vectors.py` generates exactly the 40 committed logs and that their reasons are exactly the twelve.
  Both are builder paths the reviewer may not touch. When the reviewer's vectors land, a builder change
  must come with them: either the reviewer's proposal fails `tests`, or the builder extends
  `tools/vectors.py` to the new logs first.
- SPEC §11 (patched) names `40`–`49` (eleven logs); BRIEF-C1.md's deliverables say "`40`–`47`".
- The SPEC sentences the patch left (reported at Step 1): §4's "does not order timestamps at C0"; §8
  step 9's "no effect on the state beyond the head hash" (every entry now records its `ts`); the "(C0)" title.
- `tests/test_score.py`'s witness and the reviewer's independent `spec/vectors/` rebuild should agree
  field for field but for keys and signatures. Any other difference is a finding against one of us.

## 7. Not implemented as written

Nothing. Every text was implementable; the cap (§0) is a bound, not a text.
