"""The pin runner: text-edit mutants on disposable copies, KILLED only with a passing twin."""
import os
import tempfile
import unittest

from pins import pins, run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def toy_pin(name, find, replace, path="kernel/log.py", fails_on_mutant=True):
    def test(root):
        with open(os.path.join(root, path)) as f:
            text = f.read()
        if fails_on_mutant:
            assert "# mutated" not in text, "mutated"
    return pins.Pin(name, test, [pins.Mutant("m", path, find, replace)])


class Registry(unittest.TestCase):
    def test_pins_are_well_formed(self):
        names = [p.name for p in pins.PINS]
        self.assertEqual(len(names), len(set(names)))
        for required in ("judge_from_proposal", "unsigned_change", "history_rewritten", "fork_admitted",
                         "unattributed_entry", "checker_drift", "forged_signature_admitted", "trusted_path_unguarded",
                         "trusted_rename_admitted", "weak_key_admitted", "reserved_bytes_admitted"):
            self.assertIn(required, names)
        for gone in ("final_law_for_all", "vacuous_rule_admitted", "impossible_rule_admitted", "redundancy_unreported",
                     "orphaned_rule_admitted"):
            self.assertNotIn(gone, names, "rule pins return with the law language in C1")
        self.assertEqual(len(names), 16)
        for p in pins.PINS:
            self.assertTrue(p.mutants, p.name)
            for m in p.mutants:
                path = os.path.join(ROOT, m.path)
                if not os.path.exists(path):
                    self.assertEqual(p.name, "checker_drift", f"{p.name}: missing target {m.path}")
                    continue
                with open(path) as f:
                    self.assertEqual(f.read().count(m.find), 1, f"{p.name}/{m.name}: find string must occur exactly once")
                self.assertNotEqual(m.find, m.replace)


class Runner(unittest.TestCase):
    def test_killed_survived_stale_pending(self):
        killed = toy_pin("k", "def canonical(obj):", "def canonical(obj):  # mutated")
        survived = toy_pin("s", "def canonical(obj):", "def canonical(obj):  # mutated", fails_on_mutant=False)
        stale = toy_pin("st", "no such text anywhere", "x")
        pending = toy_pin("p", "x", "y", path="kernel2/no-such-file")
        results = run.run_pins([killed, survived, stale, pending], ROOT)
        by = {(r.pin, r.mutant): r.status for r in results}
        self.assertEqual(by[("k", "m")], "KILLED")
        self.assertEqual(by[("s", "m")], "SURVIVED")
        self.assertEqual(by[("st", "m")], "STALE")
        self.assertEqual(by[("p", "m")], "PENDING")
        self.assertEqual(run.exit_code(results), 1)
        self.assertEqual(run.exit_code([r for r in results if r.pin in ("k", "p")]), 0)

    def test_twin_failure_is_a_defect(self):
        def bad_test(root):
            raise AssertionError("twin fails")
        pin = pins.Pin("t", bad_test, [pins.Mutant("m", "kernel/log.py", "def canonical(obj):", "def canonical(obj):  #")])
        results = run.run_pins([pin], ROOT)
        self.assertEqual([r.status for r in results], ["TWIN FAILED"])
        self.assertEqual(run.exit_code(results), 1)

    def test_copy_excludes_git_and_caches(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = run.disposable_copy(ROOT, tmp)
            self.assertTrue(os.path.exists(os.path.join(copy, "kernel", "check.py")))
            self.assertFalse(os.path.exists(os.path.join(copy, ".git")))
            for dirpath, dirnames, _ in os.walk(copy):
                self.assertNotIn("__pycache__", dirnames, dirpath)


if __name__ == "__main__":
    unittest.main()
