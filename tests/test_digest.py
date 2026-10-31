"""tools/digest.py: parity with the judge and refusal of foreign objects."""
import os
import subprocess
import sys
import tempfile
import unittest

from judge import judge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def tool(name, *args):
    return subprocess.run([PY, os.path.join(ROOT, "tools", name), *args], capture_output=True, text=True, cwd=ROOT)


class Digest(unittest.TestCase):
    def test_matches_the_judge_on_the_working_tree(self):
        r = tool("digest.py")
        self.assertEqual(r.returncode, 0, r.stderr)
        head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
        clean = subprocess.run(["git", "status", "--porcelain", "--", "kernel", "kernel2", "judge", ".github/workflows", "SPEC.md"],
                               capture_output=True, text=True, cwd=ROOT).stdout.strip()
        if clean:
            self.skipTest("trusted base has uncommitted changes; cannot compare with the judge's git-derived digest")
        self.assertEqual(r.stdout.strip(), judge.digest(ROOT, head))


    def test_refuses_a_tree_holding_a_foreign_object(self):
        """SPEC §10.1: a symbolic link or submodule in the trusted base is named, exit 2, no digest printed."""
        from harness import gitfix
        for kind, rel, target in (("link", "SPEC.md", "README.md"), ("present", "kernel/vendor", None),
                                  ("absent", "kernel/vendor", None), ("file", "kernel/vendor", None)):
            with tempfile.TemporaryDirectory() as tmp:
                gitfix.git(tmp, "init", "-q")
                for rel_ in ("tools/digest.py", "judge/__init__.py", "judge/judge.py", "kernel/check.py", "SPEC.md"):
                    gitfix.write(tmp, rel_, open(os.path.join(ROOT, rel_), "rb").read())
                gitfix.write(tmp, "README.md", "readme\n")
                gitfix.git(tmp, "add", "-A")
                gitfix.place(tmp, kind, rel, target)
                gitfix.git(tmp, "add", "-A")
                r = subprocess.run([PY, os.path.join(tmp, "tools", "digest.py")], capture_output=True, text=True, cwd=tmp)
                if kind == "file":
                    self.assertEqual((r.returncode, len(r.stdout.strip())), (0, 64), r.stderr)
                    continue
                self.assertEqual(r.returncode, 2, (kind, r.stdout, r.stderr))
                self.assertIn(rel, r.stderr)
                self.assertEqual(r.stdout, "")


if __name__ == "__main__":
    unittest.main()
