"""jack score's witness (BRIEF-C1.md criterion 5): tests/vectors/score.jsonl, built by witness() below, and the brief's table.
`python3 -m tests.test_score` rebuilds the vector with fresh throwaway keys."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from harness import build, keys
from kernel import check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR = os.path.join(ROOT, "tests", "vectors", "score.jsonl")
FORECASTS = [("counsel", "world.screen", 600), ("builder", "pins_green", 800), ("counsel", "world.screen", 300),
             ("reviewer", "pins_green", 700), ("builder", "world.delivery", 900), ("counsel", "pins_green", 500),
             ("builder", "pins_green", 650), ("counsel", "world.screen", 400), ("guy", "world.race", 200),
             ("reviewer", "world.screen", 550)]  # F1..F10, seqs 1..10
RESOLUTIONS = [(2, 1, "reviewer"), (1, 1, "builder"), (4, 0, "counsel"), (3, 0, "reviewer"), (6, 1, "builder"), (5, 0, "counsel")]
TABLE = """| proposer | type | resolved | mean p | rate | loss | base-rate loss |
|---|---|---:|---:|---:|---:|---:|
| builder | pins_green | 1 | 0.8000 | 1.0000 | 0.2231 | 0.6931 |
| builder | world.delivery | 1 | 0.9000 | 0.0000 | 2.3026 | 0.6931 |
| counsel | pins_green | 1 | 0.5000 | 1.0000 | 0.6931 | 0.6931 |
| counsel | world.screen | 2 | 0.4500 | 0.5000 | 0.4338 | 0.8959 |
| reviewer | pins_green | 1 | 0.7000 | 0.0000 | 1.2040 | 1.0986 |"""  # BRIEF-C1.md, verbatim


def witness(tmpdir):
    """Ten forecasts then six resolutions, each by a party other than the forecaster, under throwaway keys."""
    k = {p: keys.make_key(tmpdir, p) for p in ("guy", "builder", "reviewer", "counsel")}
    lg = build.Log()
    lg.add("genesis", "guy", build.genesis_body([build.decl("guy-master", "guy", k["guy"], build.ALL)] + [
        build.decl(f"{p}-1", p, k[p], ["forecast", "resolution"]) for p in ("builder", "reviewer", "counsel")]), k["guy"])
    for i, (who, type_, p) in enumerate(FORECASTS, 1):
        lg.add("forecast", who, {"claim": f"F{i}", "p": p, "resolves_by": "2026-11-08T00:00:00Z", "type": type_}, k[who],
               ts=f"2026-10-26T00:{i:02}:00Z")
    for j, (f, outcome, who) in enumerate(RESOLUTIONS):
        lg.add("resolution", who, {"forecast": f, "outcome": outcome, "evidence": f"run {f}"}, k[who], ts=f"2026-10-27T00:{j:02}:00Z")
    return lg


def score(log_text, *args):
    """`tools/jack score` run in a copy of the tools holding only this log.jsonl: no key, no git, no remote."""
    with tempfile.TemporaryDirectory() as tmp:
        for d in ("tools", "kernel", "judge", "harness"):
            shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d), ignore=shutil.ignore_patterns("__pycache__"))
        with open(os.path.join(tmp, "log.jsonl"), "w") as f:
            f.write(log_text)
        return subprocess.run([sys.executable, os.path.join(tmp, "tools", "jack"), "score", *args], capture_output=True, text=True, cwd=tmp)


class Witness(unittest.TestCase):
    def test_the_vector_is_the_brief_s_log(self):
        with open(VECTOR) as f:
            lines = f.read().splitlines()
        self.assertEqual(check.check(lines), {"ok": True, "entries": 17})
        es = [json.loads(line) for line in lines]
        self.assertEqual([(e["proposer"], e["body"]["type"], e["body"]["p"]) for e in es[1:11]], FORECASTS)
        self.assertEqual([(e["body"]["forecast"], e["body"]["outcome"], e["proposer"]) for e in es[11:]], RESOLUTIONS)
        self.assertTrue(all(es[e["body"]["forecast"]]["proposer"] != e["proposer"] for e in es[11:]))
        with tempfile.TemporaryDirectory() as tmp:  # witness() rebuilds it but for keys and signatures
            fresh = [json.loads(line) for line in witness(tmp).lines]
        strip = lambda e: {k: v for k, v in e.items() if k not in ("sig", "parent")}  # noqa: E731
        self.assertEqual([strip(e) for e in es[1:]], [strip(e) for e in fresh[1:]])

    def test_jack_score_prints_the_brief_s_table_exactly(self):
        with open(VECTOR) as f:
            r = score(f.read())
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.split("\n\n")[0], TABLE)
        self.assertEqual(r.stdout, TABLE + """

| proposer | forecasts | resolved | mean p | rate | loss | base-rate loss |
|---|---:|---:|---:|---:|---:|---:|
| builder | 3 | 2 | 0.8500 | 0.5000 | 1.2629 | 0.6931 |
| counsel | 4 | 3 | 0.4667 | 0.6667 | 0.5202 | 0.8283 |
| reviewer | 2 | 1 | 0.7000 | 0.0000 | 1.2040 | 1.0986 |

| type | forecasts | resolved | mean p | rate | loss | base-rate loss |
|---|---:|---:|---:|---:|---:|---:|
| pins_green | 4 | 3 | 0.6667 | 0.6667 | 0.7068 | 0.8283 |
| world.delivery | 1 | 1 | 0.9000 | 0.0000 | 2.3026 | 0.6931 |
| world.screen | 4 | 2 | 0.4500 | 0.5000 | 0.4338 | 0.8959 |
""")

    def test_overdue_with_as_of_and_refusals(self):
        with open(VECTOR) as f:
            text = f.read()
        r = score(text, "--as-of", "2026-11-08T00:00:01Z")
        self.assertTrue(r.stdout.endswith("""overdue at 2026-11-08T00:00:01Z:
| seq | proposer | type | p | resolves_by |
|---:|---|---|---:|---|
| 7 | builder | pins_green | 650 | 2026-11-08T00:00:00Z |
| 8 | counsel | world.screen | 400 | 2026-11-08T00:00:00Z |
| 9 | guy | world.race | 200 | 2026-11-08T00:00:00Z |
| 10 | reviewer | world.screen | 550 | 2026-11-08T00:00:00Z |
"""), r.stdout)
        self.assertNotIn("| 7 |", score(text, "--as-of", "2026-11-08T00:00:00Z").stdout)  # before as-of, strictly
        for args, log_text in ((["--as-of", "tomorrow"], text), ([], text + "{}\n")):
            r = score(log_text, *args)
            self.assertEqual((r.returncode, r.stdout), (1, ""), r.stderr)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        with open(VECTOR, "w") as f:
            f.write(witness(tmp).text())
