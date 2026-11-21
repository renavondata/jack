"""The live evaluator has only trusted imports; historical source paths stay historical."""
import ast
import os
import unittest

from harness.gitfix import git
from judge import entries, status, value
from tests.clerk_fixture import commit, tree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Move(unittest.TestCase):
    def test_live_modules_and_shared_functions_are_under_judge(self):
        for module in (entries, status, value):
            self.assertTrue(module.__file__.startswith(os.path.join(ROOT, "judge") + os.sep))
            with open(module.__file__) as f:
                source = ast.parse(f.read())
            for node in ast.walk(source):
                if isinstance(node, ast.ImportFrom):
                    self.assertNotIn(node.module.split(".")[0], ("tools", "harness", "tests", "sim"))
        from tools import entry
        for name in ("now", "read_log", "resolution_rates"):
            self.assertIs(getattr(entry, name), getattr(entries, name))
        for old in ("tools/status.py", "tools/value.py"):
            self.assertFalse(os.path.exists(os.path.join(ROOT, old)))

    def test_scope_walk_ignores_a_side_parents_scope(self):
        # Reuse the evaluator's synthetic opening fixture, with a real merge whose
        # side parent has another scope. Only the mainline's scopes bind criterion 3.
        import json
        from tests.test_status import C2aPrimeTest
        case = C2aPrimeTest("test_change_3_process_unchanged")
        case.setUpClass()
        try:
            case.setUp()
            case.c2a_stream()
            case.s.forecast(ts="2026-11-16T00:00:00Z", args={"id": "V5"}, resolves_by="2026-11-30T00:00:00Z")
            op = case.s.add("push", "guy", ts="2026-11-18T00:00:00Z", digest="a" * 64, review="0" * 64)
            scope = {"counted": ["tests/"], "cap": 8400}
            with open(status.__file__) as f:
                source = f.read()
            with open(os.path.join(ROOT, "tools/clerk.py")) as f:
                clerk = f.read()
            files = {"log.jsonl": case.s.log.text(), "judge/scope.json": json.dumps(scope),
                     "SPEC.md": "at C1 it is:\n```\n" + json.dumps(scope) + "\n```\n",
                     "tools/status.py": source, "tools/clerk.py": clerk,
                     "pins/pins.py": "\n".join(f'Pin("{n}", t, m)' for n in status.VALUE_PINS)}
            with tree(files) as (root, start):
                git(root, "checkout", "-q", "-b", "side")
                side = commit(root, {"judge/scope.json": json.dumps(dict(scope, cap=1))})
                git(root, "checkout", "-q", "--detach", start)
                commit(root, {"README.md": "first parent\n"})
                git(root, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "--no-ff", "-s", "ours", side, "-m", "Keep first-parent scope")
                head = git(root, "rev-parse", "HEAD")
                self.assertEqual(status.c2a_tree_evidence(root, head, case.s.es, op), (True, True, True))
        finally:
            case.doClassCleanups()


if __name__ == "__main__":
    unittest.main()
