"""spec/vectors must match the kernel exactly; harness/diff.py must find a checker equal to itself."""
import glob
import json
import os
import sys
import unittest

from harness import diff
from kernel import check, log
from kernel.log import Refuse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VEC = os.path.join(ROOT, "spec", "vectors")


class SpecVectors(unittest.TestCase):
    def test_canonical_vectors(self):
        with open(os.path.join(VEC, "canonical.json")) as f:
            v = json.load(f)
        for c in v["canonical"]:
            self.assertEqual(log.canonical(c["value"]), c["canonical"])
            self.assertEqual(log.line_hash(c["canonical"]), c["sha256"])
            self.assertEqual(log.parse_line(c["canonical"]), c["value"])
        for r in v["refused_lines"]:
            with self.assertRaises(Refuse) as cm:
                log.parse_line(r["line"])
            self.assertEqual(cm.exception.reason, r["reason"], r["line"])
        self.assertEqual(v["genesis_parent"], "0" * 64)

    def test_log_vectors(self):
        with open(os.path.join(VEC, "verdicts.json")) as f:
            verdicts = json.load(f)["verdicts"]
        paths = sorted(glob.glob(os.path.join(VEC, "logs", "*.jsonl")))
        self.assertEqual({os.path.basename(p) for p in paths}, set(verdicts))
        reasons = set()
        for p in paths:
            with open(p, "rb") as f:
                v = check.check(check.read_lines(f.read()))
            self.assertEqual({k: x for k, x in v.items() if k != "detail"}, verdicts[os.path.basename(p)], p)
            reasons.add(v.get("reason"))
        self.assertEqual(reasons - {None}, {"malformed_json", "not_canonical", "schema", "bad_seq", "parent_mismatch",
                                            "genesis_misplaced", "no_proposer", "bad_key", "unknown_key",
                                            "proposer_mismatch", "no_power", "bad_signature"})
        self.assertTrue(any(v["ok"] for v in verdicts.values()))

    def test_differential_harness_against_itself(self):
        cmd = [sys.executable, "-E", "-s", "-m", "kernel.check"]
        paths = sorted(glob.glob(os.path.join(VEC, "logs", "*.jsonl")))[:4]
        self.assertEqual(diff.compare(cmd, cmd, paths), [])
        self.assertEqual({d[0] for d in diff.compare(cmd, ["/bin/false"], paths)}, set(paths))


if __name__ == "__main__":
    unittest.main()
