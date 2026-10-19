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

    def test_counts_nested_kernel_files_and_follows_no_link(self):
        """CHARTER §9 criterion 3: every python file under kernel/, nested ones too, by the arithmetic of SPEC §10.10;
        a symbolic link is neither followed nor counted, and is no error (the cap of §10.10 is the judge's alone)."""
        with tempfile.TemporaryDirectory() as tmp:
            for d in ("tools", "kernel/nested", "sub"):
                os.makedirs(os.path.join(tmp, d))
            shutil.copy2(os.path.join(ROOT, "tools", "count_kernel.py"), os.path.join(tmp, "tools"))
            long = "#!/usr/bin/env python3\n" + "x = 1\n" * 2000
            for rel, data in (("kernel/check.py", "x = 1\n"), ("kernel/nested/a.py", "a\nb\nc"),
                              ("kernel/nested/tool", "#!/usr/bin/python\n"), ("kernel/notes.txt", "x\n" * 2000),
                              ("long", long), ("sub/x.py", long)):
                with open(os.path.join(tmp, rel), "w") as f:
                    f.write(data)
            for rel, target in (("kernel/script", "../long"), ("kernel/sub", "../sub"), ("kernel/dangling.py", "../nowhere")):
                os.symlink(target, os.path.join(tmp, rel))
            r = subprocess.run([sys.executable, "tools/count_kernel.py"], capture_output=True, text=True, cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            listed = {l.split()[0]: int(l.split()[1]) for l in r.stdout.strip().splitlines()}
            self.assertEqual(listed, {"kernel/check.py": 1, "kernel/nested/a.py": 3, "kernel/nested/tool": 1, "total": 5})

if __name__ == "__main__":
    unittest.main()
