"""Simulator: seeded attack and benign generators with an independent oracle; property checks."""
import json
import os
import random
import sys
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

    def test_every_record_attack_in_section_6_has_a_generator(self):
        for name in ("self_judging", "retroactive", "forged", "rewriting", "forking", "unattributed", "stalling",
                     "flooding", "benign", "unsigned_change", "revoked", "weak_key", "duplicate_key", "schema", "structure"):
            self.assertIn(name, gen.KINDS, name)
        for name in ("vacuous", "impossible", "lapse", "orphaning", "breach"):
            self.assertNotIn(name, gen.KINDS, "rule attacks return with the law language in C1")

    def test_oracle_agrees_with_kernel_for_every_kind(self):
        for kind in gen.KINDS:
            for seed in range(3):
                case = gen.generate_kind(kind, random.Random(seed), self.pool)
                self.assertEqual(case.kind, kind)
                self.assertEqual(strip(check.check(case.lines)), case.expected, f"{kind} seed {seed}: {case.lines[-1][:120]}")

    def test_rewriting_a_key_entry_is_not_a_schema_refusal(self):
        """Seeds on which `rewriting` hits a key entry; the oracle said schema-valid tampering, the entry was not."""
        for s in ("abe4598310936905", "807cfd4db6b58b69", "cb54abe4a7a01c36", "5f09da6ff7544a65",
                  "dcf96225d14ce404", "7f5d392118fff56c", "38cc2874cb07b5a8", "27d1519a7b5c64af"):
            case = gen.generate(s, self.pool)
            self.assertEqual(case.kind, "rewriting")
            self.assertEqual(strip(check.check(case.lines)), case.expected, s)

    def test_generate_is_deterministic_in_the_seed(self):
        a, b = gen.generate("4178ee380b3a2c0a", self.pool), gen.generate("4178ee380b3a2c0a", self.pool)
        self.assertEqual((a.kind, a.expected), (b.kind, b.expected))
        self.assertEqual([json.loads(l)["body"] for l in a.lines], [json.loads(l)["body"] for l in b.lines])

    def test_seeds_cover_all_kinds(self):
        kinds = {gen.generate(f"{i:016x}", self.pool).kind for i in range(200)}
        self.assertEqual(kinds, set(gen.KINDS))

    def test_self_judging_is_a_judge_level_attack_but_valid_in_the_log(self):
        case = gen.generate_kind("self_judging", random.Random(1), self.pool)
        self.assertTrue(case.expected["ok"])
        self.assertTrue(any(json.loads(l)["type"] == "merge" for l in case.lines))

    def test_retroactive_log_keeps_the_revoked_keys_earlier_entry(self):
        case = gen.generate_kind("retroactive", random.Random(2), self.pool)
        self.assertTrue(case.expected["ok"])
        types = [json.loads(l)["type"] for l in case.lines]
        proposers = [json.loads(l)["proposer"] for l in case.lines]
        i = proposers.index("bob")
        self.assertIn("key", types[i + 1:], "bob's key is revoked after bob's proposal")


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
        flaky = lambda lines: {"ok": False, "seq": len(lines), "reason": "x"}  # noqa: E731
        failures = run.evaluate(case, self.pool, checker=flaky)
        self.assertIn("sticky_refusal", [f[0] for f in failures])


class Second(unittest.TestCase):
    """--second: the kernel as its own twin never disagrees; a second checker that accepts everything is caught."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.pool = gen.KeyPool(cls.tmp.name)
        cls.twin = [sys.executable, "-E", "-s", "-m", "kernel.check"]  # as harness/diff.py; run from the repo root
        cls.mutant = os.path.join(cls.tmp.name, "accept_all")
        with open(cls.mutant, "w") as f:
            f.write("#!/bin/sh\necho '{\"ok\": true, \"entries\": 0}'\n")
        os.chmod(cls.mutant, 0o755)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_twin_agrees_on_every_kind(self):
        for kind in gen.KINDS:
            case = gen.generate_kind(kind, random.Random(3), self.pool)
            self.assertNotIn("agree", [f[0] for f in run.evaluate(case, self.pool, second=self.twin)], kind)

    def test_mutant_second_checker_is_caught(self):
        case = gen.generate_kind("forking", random.Random(7), self.pool)
        self.assertFalse(case.expected["ok"])
        failures = run.evaluate(case, self.pool, second=[self.mutant])
        self.assertIn("agree", [f[0] for f in failures])

    def test_transcript_names_the_second_checker(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc = run.main(["--budget", "60", "--jobs", "2", "--limit", "6", "--out", tmp,
                           "--second", " ".join(self.twin)])
            self.assertEqual(rc, 0)
            with open(os.path.join(tmp, os.listdir(tmp)[0])) as f:
                t = json.load(f)
            self.assertEqual((t["seeds_run"], t["failures"], t["second"]), (6, [], " ".join(self.twin)))
            self.assertIn("agree", t["properties"])
            self.assertEqual(len(t["commit"]), 40)


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

    def test_worker_reports_a_generator_error_instead_of_dying(self):
        run._init()
        seed, kind, failures = run._one("not-hex")
        self.assertEqual((seed, kind), ("not-hex", "error"))
        self.assertEqual(failures[0][0], "generator")


if __name__ == "__main__":
    unittest.main()
