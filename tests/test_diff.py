"""harness/diff.py (SPEC §9a): shell scripts stand in for wrong checkers, one test per pin of §9a.7."""
import contextlib
import io
import json
import os
import tempfile
import unittest

from harness import diff
from pins.pins import toy

OK = 'echo "{\\"ok\\":true,\\"entries\\":$n}"'


class Differential(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = self.write("log", "x\ny\nz\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        with open(os.path.join(self.tmp.name, name), "w") as f:
            f.write(text)
        os.chmod(f.name, 0o755)
        return f.name

    def checker(self, body=OK, wrong_at=-1):
        return [self.write(f"c{len(os.listdir(self.tmp.name))}", "#!/bin/sh\n" + toy(body, wrong_at))]

    def lengths(self, b, a=None, **kw):
        return [k for _, k, _, _ in diff.compare(a or self.checker(), b, [self.log], **kw)]

    def test_whole_log_only(self):
        self.assertEqual(self.lengths(self.checker(wrong_at=1)), [1])

    def test_prefix_skipped(self):
        stats = {"logs": 0, "prefixes": 0, "uncompared": []}
        self.assertEqual(diff.compare(self.checker(), self.checker(), [self.log, self.log + ".absent"], stats=stats), [])
        self.assertEqual((stats["logs"], stats["prefixes"], len(stats["uncompared"])), (1, 3, 1))
        for k in (0, 2, 3):
            self.assertEqual(self.lengths(self.checker(wrong_at=k)), [k])

    def test_loose_parse(self):
        no = ['{"ok":1,"entries":3}', '{"ok":true,"entries":true}', '{"ok":true,"entries":3,"entries":3}',
              '{"ok":true,"entries":3,"x":0}', '{"ok":true,"entries":NaN}', '{"ok":true,"entries":-1}',
              '{"ok":true,"entries":3}{"ok":true,"entries":3}', '\\357\\273\\277{"ok":true,"entries":3}', '\\377',
              '{"ok":false,"seq":0,"reason":"crash","detail":""}', '{"ok":false,"seq":0,"reason":"schema","detail":1}',
              '{"ok":false,"seq":0,"reason":"schema"}', '[{"ok":true,"entries":3}]']
        for out in no:
            self.assertNotIn("ok", diff.run(self.checker(f"printf '{out}'"), self.log), out)
            self.assertNotIn("ok", diff.run(self.checker(f"printf '{out}'; exit 1"), self.log), out)
        self.assertNotIn("ok", diff.run(self.checker(OK + "; exit 1"), self.log))
        refusal = '{"detail":"x","ok":false,"reason":"schema","seq":0}'
        self.assertEqual(diff.run(self.checker(f"printf '{refusal}'; exit 1"), self.log), {"ok": False, "seq": 0, "reason": "schema"})
        self.assertEqual(self.lengths(self.checker('echo " {\\"entries\\": $n, \\"ok\\": true}"')), [])

    def test_crash_as_agreement(self):
        missing = [os.path.join(self.tmp.name, "missing")]
        for a in (self.checker("exit 3"), self.checker("exec sleep 30"), missing):
            self.assertEqual(self.lengths(a, a, timeout=0.3), [0, 1, 2, 3])
        self.assertEqual(self.lengths(self.checker()), [])

    def test_seed_range(self):
        with open(os.path.join(diff.ROOT, "sim", "seeds.txt")) as f:
            seeds = f.read().splitlines()
        with contextlib.redirect_stdout(out := io.StringIO()):
            rc = diff.main(["--a", *self.checker(), "--b", *self.checker(wrong_at=0), "--seeds", "3:5"])
        r = json.loads(out.getvalue())
        self.assertEqual((rc, r["seeds"], r["requested"], r["logs"]), (1, [3, 5], 2, 2))
        self.assertEqual([d["log"] for d in r["disagreements"]], [seeds[3], seeds[4]])


if __name__ == "__main__":
    unittest.main()
