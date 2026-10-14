"""Repository tools: kernel line count."""
import os
import subprocess
import sys
import unittest

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


if __name__ == "__main__":
    unittest.main()
