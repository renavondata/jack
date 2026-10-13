"""The judge: trunk's kernel over a proposal's appended entries, facts from git (§9.6)."""
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

from harness import build, gitfix
from harness.build import proposal
from harness.gitfix import commit_all, git, write
from judge import judge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


class Fixture(unittest.TestCase):
    """A temp repo: main has the real kernel, judge, a workflow, SPEC.md and a genesis log."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.w = build.World(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def repo(self, with_log=True):
        fx = gitfix.make_repo(self.w, with_log=with_log, tmpdir=self.tmp.name)
        self.lg, self.main = fx.log, fx.main
        return fx.repo

    def judge(self, repo, trunk=None, head=None):
        return judge.judge(repo, trunk or "main", head or "pr")


class Verdicts(Fixture):
    def test_valid_appended_entry_is_accepted(self):
        repo = self.repo()
        line = self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "append")
        r = self.judge(repo)
        self.assertTrue(r["ok"], r)
        self.assertEqual((r["reason"], r["touched"], r["appended"]), (None, ["log.jsonl"], 1))
        blob = base64.b64decode(json.loads(line)["sig"])
        n = int.from_bytes(blob[10:14], "big")
        fp = "SHA256:" + base64.b64encode(hashlib.sha256(blob[14:14 + n]).digest()).decode().rstrip("=")
        self.assertEqual(r["signers"], [fp])
        self.assertEqual(r["verdict"], {"ok": True, "entries": 2, "lapse": []})
        self.assertEqual(r["trusted_digest"], judge.digest(repo, self.main))
        self.assertEqual(r["kernel2"], "absent")

    def test_nothing_appended_is_accepted(self):
        repo = self.repo()
        write(repo, "README.md", "changed\n")
        commit_all(repo, "docs")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["appended"], r["touched"]), (True, 0, ["README.md"]))

    def test_no_logs_anywhere(self):
        repo = self.repo(with_log=False)
        write(repo, "README.md", "x\n")
        commit_all(repo, "docs")
        self.assertTrue(self.judge(repo)["ok"])

    def test_trusted_paths_refused(self):
        for path in ("kernel/check.py", "judge/judge.py", ".github/workflows/judge.yml", "SPEC.md", "CHARTER.md", "kernel/new.py"):
            repo = self.repo()
            write(repo, path, "import sys; print('{\"ok\": true, \"entries\": 0, \"lapse\": []}')\n")
            commit_all(repo, "edit")
            r = self.judge(repo)
            self.assertEqual((r["ok"], r["reason"]), (False, "trusted_path"), path)
            self.assertIn(path, r["touched"])

    def test_prefix_broken(self):
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        write(repo, "log.jsonl", self.lg.text().replace(self.lg.lines[0], self.lg.lines[0].replace("guy", "gux"), 1))
        commit_all(repo, "rewrite")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "prefix_broken"))
        repo = self.repo()
        write(repo, "log.jsonl", "")
        commit_all(repo, "truncate")
        self.assertEqual(self.judge(repo)["reason"], "prefix_broken")

    def test_genesis_by_proposal(self):
        repo = self.repo(with_log=False)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "genesis")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "genesis_by_proposal"))

    def test_kernel_refusal_propagates(self):
        repo = self.repo()
        self.lg.add("rule", "ann", build.rule_body("r1", build.forbid_title("r1", "x"),
                                                  [build.witness("proposal", "p", proposal("x"))],
                                                  [build.witness("proposal", "p", proposal("y"))]), self.w.ann)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "bad")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["verdict"]["seq"]), (False, "no_power", 1))

    def test_merge_checker_must_match_trunk_digest(self):
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        self.lg.add("merge", "guy", build.merge(1, "ab" * 32), self.w.guy)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "merge")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "judge_from_proposal"))
        self.lg.lines.pop()
        self.lg.add("merge", "guy", build.merge(1, judge.digest(repo, self.main)), self.w.guy)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "merge ok")
        self.assertTrue(self.judge(repo)["ok"])

    def test_diff_is_against_merge_base(self):
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "append")
        git(repo, "checkout", "-q", "main")
        write(repo, "README.md", "trunk moved on\n")
        commit_all(repo, "trunk change")
        git(repo, "checkout", "-q", "pr")
        r = self.judge(repo)
        self.assertEqual(r["touched"], ["log.jsonl"])

    def test_digest_covers_trusted_base_only(self):
        repo = self.repo()
        d0 = judge.digest(repo, self.main)
        files = {"kernel/check.py", "kernel/log.py", "judge/judge.py", ".github/workflows/judge.yml", "SPEC.md"}
        self.assertTrue(files <= set(judge.trusted_files(repo, self.main)))
        self.assertNotIn("README.md", judge.trusted_files(repo, self.main))
        write(repo, "README.md", "x\n"); sha = commit_all(repo, "readme")
        self.assertEqual(judge.digest(repo, sha), d0)
        write(repo, "SPEC.md", "y\n"); sha = commit_all(repo, "spec")
        self.assertNotEqual(judge.digest(repo, sha), d0)
        expected = hashlib.sha256()
        for path in sorted(judge.trusted_files(repo, self.main)):
            expected.update(path.encode() + b"\0" + judge.show(repo, self.main, path) + b"\0")
        self.assertEqual(d0, expected.hexdigest())


class TrunkKernelRuns(Fixture):
    def test_the_kernel_that_runs_is_trunks(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        stub = 'import json, sys\nprint(json.dumps({"ok": False, "seq": 0, "rule": None, "reason": "stub", "detail": ""}))\nsys.exit(1)\n'
        write(repo, "kernel/check.py", stub)
        trunk = commit_all(repo, "stub trunk")
        git(repo, "checkout", "-q", "pr")
        log_path = os.path.join(repo, "any.jsonl")
        write(repo, "any.jsonl", self.lg.text())
        self.assertEqual(judge.run_kernel(repo, trunk, log_path)["reason"], "stub")
        self.assertTrue(judge.run_kernel(repo, self.main, log_path)["ok"])


class Cli(Fixture):
    def test_cli_exit_codes_and_json(self):
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "append")
        r = subprocess.run([PY, os.path.join(ROOT, "judge", "judge.py"), "--repo", repo, "--trunk", "main", "--proposal", "pr"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(json.loads(r.stdout)["ok"])
        write(repo, "SPEC.md", "z\n")
        commit_all(repo, "spec")
        r = subprocess.run([PY, os.path.join(ROOT, "judge", "judge.py"), "--repo", repo, "--trunk", "main", "--proposal", "pr"],
                           capture_output=True, text=True)
        self.assertEqual((r.returncode, json.loads(r.stdout)["reason"]), (1, "trusted_path"))
        r = subprocess.run([PY, os.path.join(ROOT, "judge", "judge.py"), "--repo", repo, "--trunk", "nosuch", "--proposal", "pr"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
