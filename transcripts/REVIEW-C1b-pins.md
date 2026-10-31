# C1b pins registered and measured

Reviewer: `reviewer-2`, party `reviewer`, model `openai/gpt-6-astra`.
Branch: `review-c1b-pins`. Builder base: `14e274b` (PR #60).
Measured registration commit: `fdb30dc`.

## Result

All 24 pins named in BRIEF-C1b v7 are registered in `pins/pins.py`.
Their 30 mutants are KILLED, each with its passing twin. No pin was omitted
or weakened. The complete registry is 70 pins and 94 mutants KILLED;
SURVIVED, STALE, TWIN FAILED and PENDING are all zero.
The complete run is recorded in `transcripts/C1b-pins-results.txt`.

The fixtures run selected builder unittest methods in subprocesses rooted
in the disposable tree. They cover both attack and control inputs. The
evidence-component mutant actually combines connected evidence components;
it is not a substitute mutation of the item count. Named and oldest-only
repair attribution are separate mutants; the historical replay retains its
semantic twin, without rewriting the signed production log.

## Verification and submission blocker

`python3 pins/run.py --transcript transcripts/C1b-pins-results.txt` exits 0:
94 KILLED, zero other outcomes. All C1b failures are assertion failures,
not syntax errors or missing imports.

`python3 -m unittest discover -s tests -q` runs 264 tests, with one failure
and one skip. The failure is `Registry.test_pins_are_well_formed` at
`tests/test_pins.py:40`: `self.assertEqual(len(names), 46)` now sees 70.
The other tests pass. The builder must update this obsolete count; the
reviewer's permitted paths do not include `tests/`. This also blocks the
local `tools/jack proposal` check, before signing or pushing a proposal.

The requested verb was attempted with title
`C1b pins registered: 24 pins, 30 mutants KILLED; tree at 6874 counted lines`.
It refused with `the check fails: -m unittest discover -s tests -t .` and
the same `70 != 46` failure (264 tests, one failure, one skip). No reviewer
proposal entry was signed, and no push-recovery commands were printed.
The measured branch is published separately as a draft PR carrying this
blocker; it is not a successfully recorded proposal.

Forecast seq 199 was entered through `tools/jack forecast` under reviewer-2:
"the counted lines of this branch's proposal head exceed 6,200 by at most 674",
type `proposal.count`, p = 990/1000, resolves_by `2026-11-03T00:00:00Z`.

## Counted lines

The requested committed-tree measurement:

```sh
python3 -c "from judge.judge import counted_lines; import json; s=json.load(open('judge/scope.json')); print(counted_lines('.', 'HEAD', s['counted']))"
```

Output: **6874**. The consolidated builder base is **6744**.
`pins/pins.py`: **820 before, 950 after, +130**.
The measured tree exceeds the 6200 cap by **674** lines.
Transcripts and log entries do not add counted lines.

Per-file counts use the judge's regular-file, Python suffix/shebang and
newline rules, over its configured counted roots:

| File | Counted lines |
|---|---:|
| `harness/__init__.py` | 0 |
| `harness/build.py` | 68 |
| `harness/diff.py` | 62 |
| `harness/gitfix.py` | 87 |
| `harness/keys.py` | 91 |
| `harness/runner.py` | 30 |
| `pins/__init__.py` | 0 |
| `pins/fixtures.py` | 162 |
| `pins/pins.py` | 950 |
| `pins/run.py` | 107 |
| `sim/__init__.py` | 0 |
| `sim/gen.py` | 318 |
| `sim/run.py` | 125 |
| `tests/__init__.py` | 0 |
| `tests/clerk_fixture.py` | 65 |
| `tests/test_check.py` | 437 |
| `tests/test_clerk.py` | 179 |
| `tests/test_diff.py` | 84 |
| `tests/test_digest.py` | 53 |
| `tests/test_entry.py` | 160 |
| `tests/test_jack.py` | 729 |
| `tests/test_judge.py` | 720 |
| `tests/test_law.py` | 30 |
| `tests/test_log.py` | 231 |
| `tests/test_pins.py` | 117 |
| `tests/test_promotion.py` | 235 |
| `tests/test_score.py` | 109 |
| `tests/test_sig.py` | 207 |
| `tests/test_sim.py` | 154 |
| `tests/test_status.py` | 77 |
| `tests/test_tools.py` | 63 |
| `tests/test_vectors.py` | 67 |
| `tools/clerk.py` | 88 |
| `tools/count_kernel.py` | 46 |
| `tools/digest.py` | 49 |
| `tools/entry.py` | 187 |
| `tools/jack` | 282 |
| `tools/status.py` | 372 |
| `tools/vectors.py` | 133 |
| **Total** | **6874** |
