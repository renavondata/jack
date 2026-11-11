"""C2a-prime reviewer fixtures, run against each disposable mutant tree."""
import os
import subprocess
import sys


def cases(root, *methods):
    names = [f"tests.test_status.C2aPrimeTest.{method}" for method in methods]
    result = subprocess.run([sys.executable, "-E", "-s", "-m", "unittest", "-q", *names],
                            cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def second_window_from_the_end(root):
    cases(root, "test_change_1_window")


def second_window_end_is_v5(root):
    cases(root, "test_change_1_window")


def second_window_cap(root):
    path = os.path.join(root, "tests", "test_status.py")
    with open(path) as f:
        text = f.read()
    old = 'self.assertFalse(st.c2a_tree_evidence(root, bad_cap, self.s.es, op2)[0])'
    extra = '''self.assertFalse(st.c2a_tree_evidence(root, bad_cap, self.s.es, op2)[0])
            same_cap_changed = commit(root, {"judge/scope.json": json.dumps(dict(s84, counted=["tools/"])),
                                             "SPEC.md": spec_of(dict(s84, counted=["tools/"]))})
            self.assertFalse(st.c2a_tree_evidence(root, same_cap_changed, self.s.es, op2)[0])'''
    assert text.count(old) == 1
    with open(path, "w") as f:
        f.write(text.replace(old, extra))
    cases(root, "test_change_1_window")


def offlog_from_second_opening(root):
    cases(root, "test_change_1_window")


def promote_refused_before_end(root):
    cases(root, "test_change_1_window")


def window_fix_is_decision(root):
    cases(root, "test_change_2_window_fix")


def window_fix_not_retroactive(root):
    cases(root, "test_change_2_window_fix")


def process_unchanged_from_opening(root):
    cases(root, "test_change_3_process_unchanged")
