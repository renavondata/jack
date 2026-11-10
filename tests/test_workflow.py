"""The serial commands at 9fcf8e7, preserved by C2b's three workers and fail-closed gate."""
import copy
import itertools
import json
import re
import subprocess
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ["python3 -m unittest discover -s tests -t . -v", "python3 pins/run.py",
            "python3 judge/selfcheck.py", "python3 harness/diff.py --seeds 300 --b kernel2/check 'spec/vectors/logs/*.jsonl'",
            "python3 tools/count_kernel.py"]
SETUP = [{"uses": "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"},
         {"uses": "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", "with": {"python-version": "3.12"}}]


def preserved(workflow):
    jobs = workflow["jobs"]
    gate = jobs["tests"]
    workers = set(jobs) - {"tests"}
    assert len(workers) == 3 and set(gate["needs"]) == workers and len(gate["needs"]) == 3
    assert gate["if"].strip() in ("always()", "${{ always() }}") and "continue-on-error" not in gate
    commands = []
    for name in workers:
        job = jobs[name]
        assert not {"if", "continue-on-error", "needs", "strategy"} & job.keys()
        assert job["runs-on"] == "ubuntu-latest" and job["steps"][:2] == SETUP
        for step in job["steps"]:
            assert not {"if", "continue-on-error"} & step.keys()
        commands += [step["run"] for step in job["steps"] if "run" in step]
    assert sorted(commands) == sorted(COMMANDS)
    assert len(gate["steps"]) == 1
    step = gate["steps"][0]
    assert not {"if", "continue-on-error"} & step.keys()
    script = step["run"].strip()
    # Accept only the three shell tests: no side effects or hidden success path in this executable witness.
    pattern = r'test "\$\{\{ needs\.([\w-]+)\.result \}\}" = success'
    tests = script.split(" && ")
    matches = [re.fullmatch(pattern, test) for test in tests]
    assert len(tests) == 3 and all(matches) and {m[1] for m in matches} == workers
    for results in itertools.product(("success", "failure", "cancelled", "skipped"), repeat=3):
        values = dict(zip(sorted(workers), results))
        rendered = re.sub(r"\$\{\{ needs\.([\w-]+)\.result \}\}", lambda m: values[m[1]], script)
        assert (subprocess.run(["sh", "-c", rendered]).returncode == 0) == all(v == "success" for v in results)


class WorkflowTest(unittest.TestCase):
    def test_workflow_steps_preserved(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/tests.yml").read_text())
        # Before the opening, the actual file is still serial. Exercise the exact planned split now;
        # once the cap opens, the real workflow itself must pass, including if someone reverts it.
        if json.loads((ROOT / "judge/scope.json").read_text())["cap"] <= 7800:
            self.assertEqual(set(workflow["jobs"]), {"tests"})
            serial = workflow["jobs"]["tests"]
            self.assertEqual(serial["steps"][:2], SETUP)
            self.assertEqual([s["run"] for s in serial["steps"] if "run" in s], COMMANDS)
            workflow["jobs"] = {name: dict(serial, steps=copy.deepcopy(SETUP) + [{"run": COMMANDS[i]} for i in indices])
                                for name, indices in (("unit", (0, 4)), ("pins", (1,)), ("sample", (2, 3)))}
            workflow["jobs"]["tests"] = {"needs": ["unit", "pins", "sample"], "if": "always()", "steps": [{"run":
                ' && '.join('test "${{ needs.' + name + '.result }}" = success' for name in ("unit", "pins", "sample"))}]}
        preserved(workflow)
        sample = next(name for name, job in workflow["jobs"].items() if any(s.get("run") == COMMANDS[3] for s in job["steps"]))
        broken = copy.deepcopy(workflow)
        broken["jobs"][sample]["steps"] = [s for s in broken["jobs"][sample]["steps"] if s.get("run") != COMMANDS[3]]
        with self.assertRaises(AssertionError): preserved(broken)
        broken = copy.deepcopy(workflow); broken["jobs"]["tests"].pop("if")
        with self.assertRaises((AssertionError, KeyError)): preserved(broken)
