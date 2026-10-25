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

    def test_every_record_attack_in_section_6_has_a_generator(self):
        for name in ("self_judging", "retroactive", "forged", "rewriting", "forking", "unattributed", "stalling",
                     "flooding", "benign", "unsigned_change", "revoked", "weak_key", "duplicate_key", "schema", "structure"):
            self.assertIn(name, gen.KINDS, name)
        for name in ("ts_decreasing", "forecast_valid", "resolution_valid", "resolution_self", "resolution_dangling",
                     "resolution_double", "forecast_past", "forecast_permille_0", "forecast_permille_1000", "forecast_boolean"):
            self.assertIn(name, gen.KINDS, name)  # BRIEF-C1.md, C1a's simulator kinds
        for name in ("vacuous", "impossible", "lapse", "orphaning", "breach"):
            self.assertNotIn(name, gen.KINDS, "rule attacks return with the law language in C1")

    def test_oracle_agrees_with_kernel_for_every_kind(self):
        for kind in gen.KINDS:
            for seed in range(3):
                case = gen.generate_kind(kind, random.Random(seed), self.pool)
                self.assertEqual(case.kind, kind)
                self.assertEqual(strip(check.check(case.lines)), case.expected, f"{kind} seed {seed}: {case.lines[-1][:120]}")

    def test_rewriting_a_key_entry_is_not_a_schema_refusal(self):
        """Seeds on which `rewriting` hits a key entry: since round 2 a key declaration has exactly four members,
        so the generator tampers a valid field, not the body's shape (counsel's review, 14 Oct 2026). From C1a the field is
        `powers`, a power repeated, not `ts`: an earlier ts is ts_decreased. Seeds re-found for the C1a kinds."""
        for s in ("b40a8140306b53ae", "bcbd8a8f356f322e", "c2b71f90bf0ef9b8", "1161a16aed6daf91",
                  "8077e437c56c5c02", "0ce62cf5c485ee63", "4f332879346f2a0e", "e9c603ed305d7d56"):
            case = gen.generate(s, self.pool)
            self.assertEqual(case.kind, "rewriting")
            self.assertIn(case.expected["reason"], ("bad_signature", "parent_mismatch"), s)
            self.assertTrue(any(e["type"] == "key" and len(e["body"]["powers"]) > len(set(e["body"]["powers"]))
                                for e in map(json.loads, case.lines)), s)
            self.assertEqual(strip(check.check(case.lines)), case.expected, s)

    def test_generate_is_deterministic_in_the_seed(self):
        a, b = gen.generate("4178ee380b3a2c0a", self.pool), gen.generate("4178ee380b3a2c0a", self.pool)
        self.assertEqual((a.kind, a.expected), (b.kind, b.expected))
        self.assertEqual([json.loads(l)["body"] for l in a.lines], [json.loads(l)["body"] for l in b.lines])

    def test_every_refusing_ledger_kind_has_its_reason_and_a_passing_twin(self):
        """BRIEF-C1.md criterion 2: each new kind's refusing case is refused with its named reason and its twin admitted."""
        named = {"ts_decreasing": {"ts_decreased"}, "resolution_self": {"self_judged", "bad_signature", "schema"},
                 "resolution_dangling": {"schema"}, "resolution_double": {"schema"}, "forecast_past": {"schema"},
                 "forecast_permille_0": {"schema"}, "forecast_permille_1000": {"schema"}, "forecast_boolean": {"schema"},
                 "forecast_valid": set(), "resolution_valid": set()}
        for kind, reasons in named.items():
            seen = set()
            for seed in range(40):
                case = gen.generate_kind(kind, random.Random(seed), self.pool)
                v = strip(check.check(case.lines))
                self.assertEqual(v, case.expected, f"{kind} seed {seed}")
                seen.add(v.get("reason", "ok"))
            self.assertEqual(seen, reasons | {"ok"}, kind)

    def test_simulated_timestamps_never_decrease_but_repeat(self):
        ts = [json.loads(l)["ts"] for k in range(30) for l in gen.generate_kind("flooding", random.Random(k), self.pool).lines]
        self.assertTrue(any(a == b for a, b in zip(ts, ts[1:])))

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
            self.assertEqual({k: sum(v.values()) for k, v in t["by_kind_verdict"].items()}, t["by_kind"])
            self.assertEqual(t["seeds"][0], "4178ee380b3a2c0a")
            self.assertIn("properties", t)

    def test_worker_reports_a_generator_error_instead_of_dying(self):
        run._init()
        seed, kind, verdict, failures = run._one("not-hex")
        self.assertEqual((seed, kind, verdict), ("not-hex", "error", "error"))
        self.assertEqual(failures[0][0], "generator")


if __name__ == "__main__":
    unittest.main()
