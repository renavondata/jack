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
            edited = [i for i, l in enumerate(case.lines) if json.loads(l)["ts"] == "2025-06-15T12:34:56Z"]
            self.assertEqual(len(edited), 1, s)
            e = json.loads(case.lines[edited[0]])
            self.assertEqual((e["type"], sorted(e["body"])), ("key", ["key_id", "powers", "principal", "pubkey"]), s)
            self.assertIn((case.expected["seq"] - edited[0], case.expected["reason"]),
                          [(0, "bad_signature"), (1, "parent_mismatch")], s)

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


EDITS = {
    "wrong_seq": 'v["seq"] = v.get("seq", 0) + 1',
    "wrong_reason": 'v["reason"] = "schema" if v.get("reason") != "schema" else "bad_seq"',
    "unknown_reason": 'v["reason"] = "nope"',
    "no_detail": 'v.pop("detail", None)',
    "detail_number": 'v["detail"] = 123',
    "nan_detail": 'v["detail"] = float("nan")',
    "surrogate_detail": 'v["detail"] = "\\ud800"',
    "bom": 'raw = b"\\xef\\xbb\\xbf" + raw',
    "utf16": 'raw = raw.decode().encode("utf-16")',
    "not_object": 'raw = b"[]"',
}
EDIT_PY = """import json, sys
name = sys.argv[1]
raw = sys.stdin.buffer.read()
edits = %r
if name in ("bom", "utf16", "not_object"):
    exec(edits[name])
else:
    v = json.loads(raw)
    exec(edits[name])
    raw = json.dumps(v).encode()
sys.stdout.buffer.write(raw)
"""


class Second(unittest.TestCase):
    """--second: the kernel as its own twin never disagrees; a second checker that accepts everything is caught."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.pool = gen.KeyPool(cls.tmp.name)
        cls.twin = [sys.executable, "-E", "-s", "-m", "kernel.check"]  # as harness/diff.py; run from the repo root
        kernel = " ".join(cls.twin) + ' "$1"'
        edit_py = os.path.join(cls.tmp.name, "edit.py")
        with open(edit_py, "w") as f:
            f.write(EDIT_PY % EDITS)
        cls.mutants = {}
        for name, script in {
            "accept_all": "echo '{\"ok\": true, \"entries\": 0}'",
            # right on every log of two or more lines, wrong on the one-line prefix (the review's counterexample)
            "prefix_divergent": 'if [ "$(wc -l < "$1")" -eq 1 ]; then echo \'{"ok": false, "seq": 0, "reason": "bad_signature", "detail": "x"}\'; exit 1; fi; exec '
                                + kernel,
            # the kernel's own verdict, edited on the way out: well-formed but wrong, or outside the contract
            **{name: 'out=$(' + kernel + '); rc=$?; printf %s "$out" | ' + sys.executable + ' ' + edit_py + ' ' + name + '; exit $rc'
              for name in EDITS},
            "ok_as_integer": kernel + " | sed 's/true/1/'",
            "wrong_exit": kernel + "; exit 1",
            "duplicate_member": kernel + " | sed 's/{/{\"ok\": true, /'",
            "sleeper": "sleep 5; " + kernel,
        }.items():
            path = os.path.join(cls.tmp.name, name)
            with open(path, "w") as f:
                f.write("#!/bin/sh\n" + script + "\n")
            os.chmod(path, 0o755)
            cls.mutants[name] = [path]
        cls.mutant = cls.mutants["accept_all"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_twin_agrees_on_every_kind(self):
        for kind in gen.KINDS:
            case = gen.generate_kind(kind, random.Random(3), self.pool)
            self.assertEqual(run.evaluate(case, self.pool, second=self.twin), [], kind)

    def test_mutant_second_checker_is_caught(self):
        case = gen.generate_kind("forking", random.Random(7), self.pool)
        self.assertFalse(case.expected["ok"])
        failures = run.evaluate(case, self.pool, second=self.mutant)
        self.assertIn("agree", [f[0] for f in failures])

    def test_second_checker_wrong_only_on_a_prefix_is_caught(self):
        case = gen.generate_kind("benign", random.Random(5), self.pool)
        self.assertTrue(case.expected["ok"] and len(case.lines) >= 2)
        failures = run.evaluate(case, self.pool, second=self.mutants["prefix_divergent"])
        self.assertEqual([f[0] for f in failures], ["agree"])
        self.assertIn("prefix of length 1", failures[0][1])

    def test_malformed_verdicts_never_agree(self):
        accepted = gen.generate_kind("benign", random.Random(5), self.pool)
        refused = gen.generate_kind("forking", random.Random(7), self.pool)
        for name in ("ok_as_integer", "wrong_exit", "duplicate_member", "bom", "utf16", "not_object"):
            failures = run.evaluate(accepted, self.pool, second=self.mutants[name])
            self.assertEqual([f[0] for f in failures], ["agree"], name)
            self.assertIn("malformed", failures[0][1], name)
        for name in ("unknown_reason", "no_detail", "detail_number", "nan_detail", "surrogate_detail"):
            failures = run.evaluate(refused, self.pool, second=self.mutants[name])
            self.assertEqual([f[0] for f in failures], ["agree"], name)
            self.assertIn("malformed", failures[0][1], name)

    def test_well_formed_wrong_refusals_are_disagreements(self):
        refused = gen.generate_kind("forking", random.Random(7), self.pool)
        for name in ("wrong_seq", "wrong_reason"):
            failures = run.evaluate(refused, self.pool, second=self.mutants[name])
            self.assertEqual([f[0] for f in failures], ["agree"], name)
            self.assertNotIn("malformed", failures[0][1], name)

    def test_prefix_divergence_is_caught_on_refused_and_long_logs(self):
        refused = gen.generate_kind("forking", random.Random(7), self.pool)
        self.assertFalse(refused.expected["ok"])
        self.assertGreaterEqual(refused.expected["seq"], 1)
        long = gen.generate_kind("flooding", random.Random(5), self.pool)
        self.assertTrue(long.expected["ok"] and len(long.lines) > 10)
        for case in (refused, long):
            failures = run.evaluate(case, self.pool, second=self.mutants["prefix_divergent"])
            self.assertEqual([f[0] for f in failures], ["agree"], case.kind)
            self.assertIn("prefix of length 1", failures[0][1], case.kind)

    def test_prefixes_of_a_refused_log_are_checked_in_the_kernel_too(self):
        """A checker wrong on the valid part of a refused log, or not sticky past the refusal, fails without --second."""
        refused = gen.generate_kind("forking", random.Random(7), self.pool)
        s = refused.expected["seq"]
        def wrong_prefix(lines):  # refuses the one-entry log, otherwise the kernel
            return {"ok": False, "seq": 0, "reason": "bad_signature", "detail": ""} if len(lines) == 1 else check.check(lines)
        def not_sticky(lines):  # a longer prefix past the refusal gives a different refusal
            v = check.check(lines)
            return dict(v, reason="schema") if not v["ok"] and s < len(lines) < len(refused.lines) else v
        self.assertIn("prefix", [f[0] for f in run.evaluate(refused, self.pool, checker=wrong_prefix)])
        if s + 1 < len(refused.lines):
            self.assertIn("sticky_refusal", [f[0] for f in run.evaluate(refused, self.pool, checker=not_sticky)])

    def test_timeout_is_malformed_not_agreement(self):
        case = gen.generate_kind("benign", random.Random(5), self.pool)
        with self.assertRaises(SystemExit):
            run.main(["--limit", "1", "--second", " ".join(self.twin), "--second-timeout", "0"])
        with self.assertRaises(SystemExit):
            run.main(["--limit", "0"])
        v = run.second_verdict(self.mutants["sleeper"], case.lines, timeout=1)
        self.assertIn("timeout", v.get("malformed", ""))
        self.assertNotEqual(v, run.strip(check.check(case.lines)))

    def test_complete_refuses_short_empty_or_duplicated_seed_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, text in (("short", "4178ee380b3a2c0a\na6c1a31696521e5b\n"), ("empty", "\n"),
                               ("dup", "4178ee380b3a2c0a\n4178ee380b3a2c0a\n"),
                               ("case", "\n".join(f"{i:016x}" for i in range(9)) + "\n4178EE380B3A2C0A\n")):
                path = os.path.join(tmp, name)
                with open(path, "w") as f:
                    f.write(text)
                rc = run.main(["--jobs", "1", "--limit", "10", "--budget", "60", "--complete", "--out", tmp, "--seeds", path])
                self.assertEqual(rc, 2, name)

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
            self.assertEqual((len(t["seeds_sha256"]), t["seeds_selected"], t["complete"]), (64, 6, True))
            self.assertEqual((len(t["second_sha256"]), t["limit"], t["complete_required"]), (64, 6, False))


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

    def test_complete_fails_a_run_the_budget_cut_short(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ["--jobs", "2", "--limit", "10", "--out", tmp, "--complete"]
            self.assertEqual(run.main(args + ["--budget", "0"]), 1)
            self.assertEqual(run.main(args + ["--budget", "60"]), 0)

    def test_worker_reports_a_generator_error_instead_of_dying(self):
        run._init()
        seed, kind, failures = run._one("not-hex")
        self.assertEqual((seed, kind), ("not-hex", "error"))
        self.assertEqual(failures[0][0], "generator")


if __name__ == "__main__":
    unittest.main()
