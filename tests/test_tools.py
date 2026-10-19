"""Repository tools: kernel line count."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from judge import judge
from tools import count_kernel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CountKernel(unittest.TestCase):
    def test_reports_per_file_and_total_and_limit(self):
        r = subprocess.run([sys.executable, "tools/count_kernel.py"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.strip().splitlines()
        self.assertTrue(any(l.startswith("kernel/check.py") for l in lines))
        total = int(lines[-1].split()[-1])
        self.assertTrue(lines[-1].startswith("total"))
        self.assertLessEqual(total, 1000)
        r = subprocess.run([sys.executable, "tools/count_kernel.py", "--limit", "10"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 1)
        self.assertIn("EXCESS", r.stdout)

    def test_counts_the_files_and_lines_the_judge_counts(self):
        """SPEC §10.10: .py files and files whose first line is a #! line naming python, counted alike."""
        samples = {"a.py": b"x\ny", "tool": b"#!/usr/bin/env python3\nx\n", "py": b"#!/usr/bin/python", "spaced": b"#! /usr/bin/env python\n\n",
                   "sh": b"#!/bin/sh\npython x\n", "late": b"\n#!/usr/bin/python\n", "comment": b"# python\n", "empty": b"", "e.py": b""}
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in samples.items():
                with open(os.path.join(tmp, name), "wb") as f:
                    f.write(data)
            counted = {n for n in samples if count_kernel.is_python(os.path.join(tmp, n))}
            self.assertEqual(counted, {"a.py", "tool", "py", "spaced", "e.py"})
            self.assertEqual(counted, {n for n, d in samples.items() if judge.is_python(n, d)})
            for name, data in samples.items():
                self.assertEqual(count_kernel.lines(os.path.join(tmp, name)), len(judge.split_lines(data)), name)

    def test_refuses_to_follow_a_symlink(self):
        """SPEC §10.10: a symbolic link is named and the tool exits 2, never following it, whatever it points to."""
        with tempfile.TemporaryDirectory() as tmp:
            for d in ("tools", "kernel", "sub"):
                os.makedirs(os.path.join(tmp, d))
            shutil.copy2(os.path.join(ROOT, "tools", "count_kernel.py"), os.path.join(tmp, "tools"))
            for rel, data in (("kernel/check.py", "x = 1\n"), ("long", "#!/usr/bin/env python3\n" + "x = 1\n" * 2000)):
                with open(os.path.join(tmp, rel), "w") as f:
                    f.write(data)
            links = {"kernel/script": "../long", "kernel/sub": "../sub", "kernel/dangling.py": "../nowhere"}
            for rel, target in links.items():
                os.symlink(target, os.path.join(tmp, rel))
            r = subprocess.run([sys.executable, "tools/count_kernel.py"], capture_output=True, text=True, cwd=tmp)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            for rel in links:
                self.assertIn(rel, r.stdout + r.stderr)
            self.assertNotIn("total", r.stdout)
            for f in (count_kernel.is_python, count_kernel.lines):
                self.assertRaises(OSError, f, os.path.join(tmp, "kernel", "script"))


if __name__ == "__main__":
    unittest.main()
