"""BRIEF-C2b: five unchanged commands and a fail-closed parallel tests gate."""
import itertools
from pathlib import Path
import re
import subprocess
import unittest


class WorkflowTest(unittest.TestCase):
    def test_workflow_steps_preserved(self):
        text = (Path(__file__).resolve().parents[1] / ".github/workflows/tests.yml").read_text()
        # Parse the committed workflow's indentation-based job/step subset. Unknown
        # run forms fail the command inventory rather than silently escaping it.
        jobs = {}
        parts = re.split(r"^  ([\w-]+):\s*$", text.split("\njobs:\n", 1)[1], flags=re.M)
        self.assertFalse(parts[0].strip())
        for name, body in zip(parts[1::2], parts[2::2]):
            self.assertNotIn(name, jobs)
            jobs[name] = body
        expected = {
            "unit": ["python3 -m unittest discover -s tests -t . -v", "python3 tools/count_kernel.py"],
            "pins": ["python3 pins/run.py"],
            "sample": ["python3 judge/selfcheck.py", "python3 harness/diff.py --seeds 300 --b kernel2/check 'spec/vectors/logs/*.jsonl'"],
        }
        self.assertEqual(set(jobs), set(expected) | {"tests"})
        checkout = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
        runtime = "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97"
        for name, commands in expected.items():
            body = jobs[name]
            with self.subTest(job=name):
                self.assertNotRegex(body, r"(?m)^\s*(?:if|continue-on-error):")
                self.assertRegex(body, r"(?m)^    runs-on: ubuntu-latest\s*$")
                steps = re.split(r"^      - ", body.split("    steps:\n", 1)[1], flags=re.M)
                self.assertFalse(steps[0].strip())
                self.assertEqual(len(steps[1:]), 2 + len(commands))
                setup = [re.sub(r" #[^\n]*", "", step).strip() for step in steps[1:3]]
                self.assertEqual(setup, [f"uses: {checkout}", f'uses: {runtime}\n        with:\n          python-version: "3.12"'])
                actual = re.findall(r"^        run: (.+)$", body, flags=re.M)
                self.assertEqual(actual, commands)
                self.assertEqual(len(re.findall(r"(?m)^\s*run:", body)), len(commands))
        gate = jobs["tests"]
        self.assertEqual(re.findall(r"(?m)^    if: (.+)$", gate), ["always()"])
        self.assertEqual(re.findall(r"(?m)^    needs: (.+)$", gate), ["[unit, pins, sample]"])
        self.assertNotRegex(gate, r"(?m)^\s*continue-on-error:|^ {6,}if:")
        self.assertEqual(len(re.findall(r"(?m)^      - ", gate)), 1)
        self.assertEqual(len(re.findall(r"(?m)^\s*run:", gate)), 1)
        shell = gate.split("        run: |\n", 1)[1]
        self.assertTrue(all(not line.strip() or line.startswith("          ") for line in shell.splitlines()))
        # Evaluate the real gate command for every dependency result: a failed,
        # skipped or cancelled worker must make the single tests conclusion red.
        for results in itertools.product(("success", "failure", "cancelled", "skipped"), repeat=3):
            command = shell
            for name, result in zip(expected, results):
                command = command.replace("${{ needs." + name + ".result }}", result)
            with self.subTest(results=results):
                run = subprocess.run(["sh", "-c", command], capture_output=True)
                self.assertEqual(run.returncode == 0, all(r == "success" for r in results))
