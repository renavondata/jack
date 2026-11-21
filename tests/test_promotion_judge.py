"""Item 15 over git histories with an installing grant/push and real signed logs."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from harness import build, gitfix
from judge import judge
from tests.promotion_fixture import entries, install, prepare

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSESS = '''
def assess(es, subject, as_of, root, rev, run=None, runs=(), acts=None, mapping=None, decision=None):
    assert decision is None
    assert es == [json.loads(l) for l in tree_bytes(root, rev, "log.jsonl").splitlines()]
    assert as_of == "2026-10-13T00:00:00Z"
    assert run["head_sha"] == rev
    assert run in runs and isinstance(acts, list)
    return {"subject": subject, "checks": [(run.get("lawful", True), "fixture criterion")]}
'''


class Promotions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.w = build.World(cls.shared.name)
        fx = gitfix.make_repo(cls.w, with_log=False, tmpdir=cls.shared.name)
        cls.base = fx.repo
        gitfix.git(cls.base, "checkout", "-q", "main")
        prepare(cls.base, cls.w)
        with open(os.path.join(ROOT, "judge/status.py")) as f:
            gitfix.write(cls.base, "judge/status.py", f.read() + ASSESS)
        gitfix.commit_all(cls.base, "Synthetic trusted evaluator")
        cls.lg = cls.w.log(cls.w.decls + cls.w.party_decls, charter=gitfix.CHARTER_SHA256,
                           checker=judge.digest(cls.base, "HEAD"))
        cls.installed = install(cls.base, cls.lg, cls.w)

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = os.path.join(self.tmp.name, "repo")
        shutil.copytree(self.base, self.repo)
        self.log = build.Log(self.lg.lines)

    def tearDown(self):
        self.tmp.cleanup()

    def promote(self, lawful=True, subject="C1a", evidence_change=None, extra=None):
        assessed = gitfix.git(self.repo, "rev-parse", "HEAD")
        run = {"head_sha": assessed, "lawful": lawful}
        data = {"run": json.dumps(run), "runs": "[]", "acts": "repo,time_hkt,class,kind,ref,note\n"}
        evidence = {}
        for name, text in data.items():
            path = f"transcripts/evidence/promotion-{name}"
            gitfix.write(self.repo, path, text)
            evidence[name] = {"path": path, "sha256": hashlib.sha256(text.encode()).hexdigest()}
        if evidence_change:
            evidence_change(evidence)
        self.log.add("decision", "guy", {"kind": "promote", "subject": subject, "evidence": evidence}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        for path, text in (extra or {}).items():
            gitfix.write(self.repo, path, text)
        return gitfix.commit_all(self.repo, "Promotion [skip ci]")

    def check(self, expected=None, whole_judge=False):
        if whole_judge:
            report = judge.judge(self.repo, "HEAD", "HEAD")
        else:
            attested = []
            failure = judge.promotion_checks(self.repo, "HEAD", "HEAD", entries(self.repo), entries(self.repo), attested)
            report = {"reason": failure[0] if failure else None, "detail": failure, "ok": failure is None, "attested": attested}
        self.assertEqual(report["reason"], expected, report)
        self.assertEqual(report["ok"], expected is None, report)
        return report

    def test_lawful_and_attested_on_selfcheck(self):
        self.promote()
        report = self.check(whole_judge=True)
        self.assertEqual({x["name"] for x in report["attested"]}, {"run", "runs", "acts"})
        result = subprocess.run([sys.executable, os.path.join(ROOT, "judge/selfcheck.py"), "--repo", self.repo], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unmet_criteria_and_skipped_ci_are_refused_on_later_runs(self):
        self.promote(lawful=False)
        self.check("promote_unmet")
        result = subprocess.run([sys.executable, os.path.join(ROOT, "judge/selfcheck.py"), "--repo", self.repo], capture_output=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(b"promote_unmet", result.stdout)
        gitfix.write(self.repo, "README.md", "a later run\n")
        gitfix.commit_all(self.repo, "Later unrelated commit")
        self.check("promote_unmet")

    def test_evidence_shape_hash_presence_and_regular_files(self):
        changes = [lambda ev: ev.pop("acts"), lambda ev: ev.update(extra={}),
                   lambda ev: ev["run"].update(sha256="0" * 64),
                   lambda ev: ev["run"].update(path="transcripts/evidence/missing"),
                   lambda ev: ev["run"].update(extra=1),
                   lambda ev: ev["run"].update(path="transcripts/evidence/../outside")]
        for change in changes:
            with self.subTest(change=change):
                gitfix.git(self.repo, "reset", "-q", "--hard", self.installed)
                self.log = build.Log(self.lg.lines)
                self.promote(evidence_change=change)
                self.check("promote_unmet")
        gitfix.git(self.repo, "reset", "-q", "--hard", self.installed)
        self.log = build.Log(self.lg.lines)
        self.promote()
        path = os.path.join(self.repo, "transcripts/evidence/promotion-run")
        os.remove(path)
        os.symlink("promotion-runs", path)
        gitfix.commit_all(self.repo, "Replace evidence after entry")
        # Evidence is judged at the entry commit, not at the later replacement.
        self.check()
        gitfix.git(self.repo, "reset", "-q", "--soft", "HEAD~2")
        gitfix.commit_all(self.repo, "Entry with symlink")
        self.check("promote_unmet")

    def test_entry_must_append_alone_add_evidence_and_change_nothing_else(self):
        self.promote(extra={"README.md": "unassessed change\n"})
        self.check("promote_unmet")
        gitfix.git(self.repo, "reset", "-q", "--hard", self.installed)
        self.log = build.Log(self.lg.lines)
        self.log.add("decision", "guy", {"kind": "grant", "subject": "extra entry"}, self.w.guy)
        self.promote()
        self.check("promote_unmet")

    def test_appending_the_entry_does_not_authorise_a_log_mode_change(self):
        self.promote()
        os.chmod(os.path.join(self.repo, "log.jsonl"), 0o755)
        # Fold the mode change into the entry commit, leaving its bytes lawful.
        gitfix.git(self.repo, "reset", "-q", "--soft", self.installed)
        gitfix.commit_all(self.repo, "Entry and unrelated mode change")
        self.check("promote_unmet")

    def test_every_entry_commit_including_a_bad_side_branch_is_judged(self):
        good = self.promote()
        gitfix.git(self.repo, "checkout", "-q", "-b", "side", self.installed)
        # The very same signed promotion line is introduced on another history.
        gitfix.git(self.repo, "checkout", good, "--", "log.jsonl", "transcripts/evidence/")
        gitfix.write(self.repo, "README.md", "bad side entry commit\n")
        bad = gitfix.commit_all(self.repo, "Second entry commit")
        gitfix.git(self.repo, "checkout", "-q", "main")
        gitfix.git(self.repo, "merge", "-q", "--no-ff", bad, "-m", "Join histories")
        self.check("promote_unmet")

    def test_entry_commit_with_two_parents_is_refused(self):
        good = self.promote()
        tree = gitfix.git(self.repo, "rev-parse", good + "^{tree}")
        gitfix.git(self.repo, "reset", "-q", "--hard", self.installed)
        gitfix.write(self.repo, "README.md", "side\n")
        side = gitfix.commit_all(self.repo, "Side parent without entry")
        merge = gitfix.git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit-tree", tree,
                           "-p", self.installed, "-p", side, "-m", "Merge introduces entry")
        gitfix.git(self.repo, "reset", "-q", "--hard", merge)
        self.check("promote_unmet")

    def test_entry_line_anywhere_in_an_ancestors_log_counts_as_an_entry_commit(self):
        good = self.promote()
        gitfix.git(self.repo, "checkout", "-q", "-b", "side", self.installed)
        gitfix.git(self.repo, "checkout", good, "--", "log.jsonl", "transcripts/evidence/")
        gitfix.write(self.repo, "log.jsonl", "\n" + self.log.text())
        bad = gitfix.commit_all(self.repo, "Same line at the wrong offset on a side history")
        gitfix.git(self.repo, "checkout", "-q", "main")
        gitfix.git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "--no-ff", "-s", "ours", bad,
                   "-m", "Keep valid head but retain the side entry commit")
        self.check("promote_unmet")

    def test_assessed_digest_must_be_in_force(self):
        gitfix.write(self.repo, "judge/new.py", "# unrecorded evaluator\n")
        gitfix.commit_all(self.repo, "Unrecorded trusted change")
        self.promote()
        # A later push restores item 11, but cannot legalise the assessed tree.
        self.log.add("push", "guy", {"digest": judge.digest(self.repo, "HEAD"), "review": "0" * 64}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        gitfix.commit_all(self.repo, "Later recorded push")
        self.check("promote_unmet")

    def test_unknown_subject_and_evaluator_error_refuse(self):
        self.promote(subject="unknown")
        self.check("promote_unmet")
        gitfix.git(self.repo, "reset", "-q", "--hard", self.installed)
        self.log = build.Log(self.lg.lines)
        gitfix.write(self.repo, "judge/status.py", "raise RuntimeError('cannot decide')\n")
        gitfix.commit_all(self.repo, "Broken trusted evaluator")
        self.log.add("push", "guy", {"digest": judge.digest(self.repo, "HEAD"), "review": "0" * 64}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        gitfix.commit_all(self.repo, "Record evaluator push")
        self.promote()
        self.check("promote_unmet")

    def test_later_evaluator_does_not_rejudge_earlier_promotion(self):
        self.promote()
        gitfix.write(self.repo, "judge/status.py", "raise RuntimeError('later evaluator')\n")
        gitfix.commit_all(self.repo, "Later trusted evaluator")
        self.log.add("push", "guy", {"digest": judge.digest(self.repo, "HEAD"), "review": "0" * 64}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        gitfix.commit_all(self.repo, "Record later evaluator")
        self.check()

    def test_no_installing_push_refuses_even_without_promotions(self):
        gitfix.git(self.repo, "reset", "-q", "--hard", self.installed + "^")
        self.check("promote_unmet", whole_judge=True)
        # A kernel-valid genesis bound to the current tree still has no installation.
        lg = self.w.log(self.w.decls + self.w.party_decls, charter=gitfix.CHARTER_SHA256,
                        checker=judge.digest(self.repo, "HEAD"))
        gitfix.write(self.repo, "log.jsonl", lg.text())
        gitfix.commit_all(self.repo, "Pre-installation genesis")
        self.check("promote_unmet")

    def test_installation_requires_prior_grant_matching_spec_and_push_commit_digest(self):
        es = entries(self.repo)
        self.assertEqual(judge.installing_push(self.repo, "HEAD", es), 5565)
        for index, field, value in ((5564, "subject", "promote_unmet: SPEC.md " + "0" * 64),
                                    (5565, "digest", "0" * 64)):
            altered = json.loads(json.dumps(es))
            altered[index]["body"][field] = value
            self.assertIsNone(judge.installing_push(self.repo, "HEAD", altered))
        self.assertIsNone(judge.installing_push(self.repo, "HEAD", es[:5564] + es[5565:] + es[5564:5565]))

    def test_installation_uses_oldest_first_parent_push_commit_not_later_repair(self):
        good_tree = gitfix.git(self.repo, "rev-parse", "HEAD^{tree}")
        gitfix.write(self.repo, "SPEC.md", "not the granted SPEC\n")
        gitfix.git(self.repo, "add", "SPEC.md")
        bad_tree = gitfix.git(self.repo, "write-tree")
        args = ("-c", "user.name=t", "-c", "user.email=t@t", "commit-tree")
        bad = gitfix.git(self.repo, *args, bad_tree, "-p", self.installed + "^", "-m", "Wrong push commit")
        later = gitfix.git(self.repo, *args, good_tree, "-p", bad, "-m", "Later repaired tree")
        gitfix.git(self.repo, "reset", "-q", "--hard", later)
        self.check("promote_unmet")

    def test_subject_acceptance_comes_from_main_not_a_separate_choices_list(self):
        with open(os.path.join(self.repo, "judge/status.py")) as f:
            source = f.read()
        source += '''
def main(argv=None):
    ap = parser(__doc__)
    ap._option_string_actions["--subject"].choices = ("C1b",)
    ap.parse_args(argv)
    raise AssertionError("report must not run")
'''
        gitfix.write(self.repo, "judge/status.py", source)
        gitfix.commit_all(self.repo, "Main has narrower subject parser")
        self.log.add("push", "guy", {"digest": judge.digest(self.repo, "HEAD"), "review": "0" * 64}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        gitfix.commit_all(self.repo, "Record evaluator")
        self.promote(subject="C1a")
        self.check("promote_unmet")


if __name__ == "__main__":
    unittest.main()
