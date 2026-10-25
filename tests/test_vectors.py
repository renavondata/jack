"""spec/vectors must match the kernel exactly; harness/diff.py must find a checker equal to itself."""
import glob
import json
import os
import sys
import tempfile
import unittest

from harness import build, diff
from kernel import check, log
from kernel.log import Refuse
from tools import vectors

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
        """Data-driven: every log verdicts.json names, and only those, gives its verdict; every reason is one of the kernel's."""
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
        self.assertLessEqual(reasons - {None}, set(log.REASONS))
        self.assertEqual(log.REASONS, tuple(diff.REASONS))  # SPEC §9 and §9a.3, enumerated together
        self.assertTrue(any(v["ok"] for v in verdicts.values()))

    def test_generator_produces_every_log(self):
        """tools/vectors.py yields logs that are committed, each with its recorded verdict, from fresh keys; others' logs may follow."""
        with open(os.path.join(VEC, "verdicts.json")) as f:
            verdicts = json.load(f)["verdicts"]
        with tempfile.TemporaryDirectory() as tmp:
            generated = vectors.logs(build.World(tmp))
        self.assertLessEqual({name + ".jsonl" for name in generated}, set(verdicts))
        for name, lines in generated.items():
            v = check.check(lines)
            self.assertEqual({k: x for k, x in v.items() if k != "detail"}, verdicts[name + ".jsonl"], name)

    def test_differential_harness_against_itself(self):
        cmd = [sys.executable, "-E", "-s", "-m", "kernel.check"]
        paths = sorted(glob.glob(os.path.join(VEC, "logs", "*.jsonl")))[:4]
        self.assertEqual(diff.compare(cmd, cmd, paths), [])
        self.assertEqual({d[0] for d in diff.compare(cmd, ["/bin/false"], paths)}, set(paths))


if __name__ == "__main__":
    unittest.main()
