"""Simulator: seeded attack and benign generators with an independent oracle; property checks."""
import json
import os
import random
import tempfile
import unittest

from kernel import check
from sim import gen, run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def strip(v):
    return {k: x for k, x in v.items() if k != "detail"}


class Generators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.pool = gen.KeyPool(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_attack_in_section_6_has_a_generator(self):
        for name in ("self_judging", "retroactive", "vacuous", "impossible", "forged", "rewriting", "forking",
                     "unattributed", "stalling", "flooding", "benign", "lapse", "unsigned_change", "orphaning"):
            self.assertIn(name, gen.KINDS, name)

    def test_oracle_agrees_with_kernel_for_every_kind(self):
        for kind in gen.KINDS:
            for seed in range(3):
                case = gen.generate_kind(kind, random.Random(seed), self.pool)
                self.assertEqual(case.kind, kind)
                self.assertEqual(strip(check.check(case.lines)), case.expected, f"{kind} seed {seed}: {case.lines[-1][:120]}")

    def test_generate_is_deterministic_in_the_seed(self):
        a, b = gen.generate("4178ee380b3a2c0a", self.pool), gen.generate("4178ee380b3a2c0a", self.pool)
        self.assertEqual((a.kind, a.expected), (b.kind, b.expected))
        self.assertEqual([json.loads(l)["body"] for l in a.lines], [json.loads(l)["body"] for l in b.lines])

    def test_seeds_cover_all_kinds(self):
        kinds = {gen.generate(f"{i:016x}", self.pool).kind for i in range(80)}
        self.assertEqual(kinds, set(gen.KINDS))

    def test_self_judging_is_a_judge_level_attack_but_valid_in_the_log(self):
        case = gen.generate_kind("self_judging", random.Random(1), self.pool)
        self.assertTrue(case.expected["ok"])
        self.assertTrue(any(json.loads(l)["type"] == "merge" for l in case.lines))


class Properties(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.pool = gen.KeyPool(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_properties_hold_on_generated_cases(self):
        for i in range(12):
            case = gen.generate(f"{i:016x}", self.pool)
            self.assertEqual(run.evaluate(case, self.pool), [], case.kind)

    def test_property_names(self):
        self.assertEqual(set(run.PROPERTIES), {"oracle", "prefix", "sticky_refusal", "deterministic"})

    def test_sticky_refusal_detects_a_bad_checker(self):
        case = gen.generate_kind("forking", random.Random(7), self.pool)
        flaky = lambda lines: {"ok": False, "seq": len(lines), "rule": None, "reason": "x"}  # noqa: E731
        failures = run.evaluate(case, self.pool, checker=flaky)
        self.assertIn("sticky_refusal", [f[0] for f in failures])


class Runner(unittest.TestCase):
    def test_run_writes_transcript_and_respects_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc = run.main(["--budget", "60", "--jobs", "2", "--limit", "10", "--out", tmp,
                          "--seeds", os.path.join(ROOT, "sim", "seeds.txt")])
            self.assertEqual(rc, 0)
            files = os.listdir(tmp)
            self.assertEqual(len(files), 1)
            with open(os.path.join(tmp, files[0])) as f:
                t = json.load(f)
            self.assertEqual((t["seeds_run"], t["failures"]), (10, []))
            self.assertEqual(sum(t["by_kind"].values()), 10)
            self.assertEqual(t["seeds"][0], "4178ee380b3a2c0a")
            self.assertIn("properties", t)


if __name__ == "__main__":
    unittest.main()


class Robustness(unittest.TestCase):
    def test_free_title_exists_when_every_vocabulary_title_is_forbidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            pool = gen.KeyPool(tmp)
            s = gen.Sim(random.Random(3), pool)
            s.step_rule(list(gen.TITLES))
            self.assertEqual(s.free_title(), gen.SPARE)
            self.assertNotIn(gen.SPARE, gen.TITLES)
            s.step_proposal()
            self.assertEqual(strip(check.check(s.lg.lines)), s.ok())

    def test_worker_reports_a_generator_error_instead_of_dying(self):
        run._init()
        seed, kind, failures = run._one("not-hex")
        self.assertEqual((seed, kind), ("not-hex", "error"))
        self.assertEqual(failures[0][0], "generator")
