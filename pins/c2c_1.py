"""C2c-1 reviewer pins reuse the builder's complete disposable-tree fixtures."""
import os
import shutil
import subprocess
import sys


SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def c2c_tests(*names):
    def test(root):
        # pins/run.py deliberately omits transcripts from disposable copies.
        shutil.copytree(os.path.join(SOURCE_ROOT, "transcripts"), os.path.join(root, "transcripts"))
        result = subprocess.run([sys.executable, "-E", "-s", "-m", "unittest", "-q", *names],
                                cwd=root, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
    return test


def courier_tests(*names):
    def test(root):
        result = subprocess.run([sys.executable, "-E", "-s", "-m", "unittest", "-q", *names],
                                cwd=root, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
    return test
