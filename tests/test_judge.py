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
from harness.gitfix import git, write
from judge import judge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def commit_all(repo, msg, proposer="builder test-model test-session"):
    return gitfix.commit_all(repo, msg + (f"\n\nProposer: {proposer}" if proposer else ""))


class Fixture(unittest.TestCase):
    """A temp repo: main has the real kernel, judge, a workflow, SPEC.md, CHARTER.md and a genesis log."""

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

    def append(self, repo, msg="append"):
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, msg)


class Verdicts(Fixture):
    def test_valid_appended_entry_is_accepted(self):
        repo = self.repo()
        line = self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        self.append(repo)
        r = self.judge(repo)
        self.assertTrue(r["ok"], r)
        self.assertEqual((r["reason"], r["touched"], r["appended"]), (None, ["log.jsonl"], 1))
        blob = base64.b64decode(json.loads(line)["sig"])
        n = int.from_bytes(blob[10:14], "big")
        fp = "SHA256:" + base64.b64encode(hashlib.sha256(blob[14:14 + n]).digest()).decode().rstrip("=")
        self.assertEqual(r["signers"], [fp])
        self.assertEqual(r["verdict"], {"ok": True, "entries": 2})
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
        self.append(repo, "genesis")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "genesis_by_proposal"))

    def test_kernel_refusal_propagates(self):
        repo = self.repo()
        self.lg.add("key", "ann", build.decl("x", "ann", self.w.stranger, ["proposal"]), self.w.ann)
        self.append(repo, "unsigned change")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["verdict"]["seq"]), (False, "no_power", 1))

    def test_merge_checker_must_match_trunk_digest(self):
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        self.lg.add("merge", "guy", build.merge(1, "ab" * 32), self.w.guy)
        self.append(repo, "merge")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "judge_from_proposal"))
        self.lg.lines.pop()
        self.lg.add("merge", "guy", build.merge(1, judge.digest(repo, self.main)), self.w.guy)
        self.append(repo, "merge ok")
        self.assertTrue(self.judge(repo)["ok"])

    def test_diff_is_against_merge_base(self):
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        self.append(repo)
        git(repo, "checkout", "-q", "main")
        write(repo, "README.md", "trunk moved on\n")
        commit_all(repo, "trunk change")
        git(repo, "checkout", "-q", "pr")
        r = self.judge(repo)
        self.assertEqual(r["touched"], ["log.jsonl"])
        self.assertTrue(r["ok"], r)


class TrustedBase(Fixture):
    def test_trusted_paths_refused(self):
        for path in ("kernel/check.py", "kernel/new.py", "kernel2/check", "judge/judge.py",
                     ".github/workflows/judge.yml", ".github/workflows/new.yml", "SPEC.md", "CHARTER.md"):
            repo = self.repo()
            write(repo, path, "import sys; print('{\"ok\": true, \"entries\": 0}')\n")
            commit_all(repo, "edit")
            r = self.judge(repo)
            self.assertEqual((r["ok"], r["reason"]), (False, "trusted_path"), path)
            self.assertIn(path, r["detail"])

    def test_renames_are_refused_although_the_diff_hides_them(self):
        for old, new in (("SPEC.md", "docs/SPEC.md"), ("CHARTER.md", "CHARTER.old.md"), ("kernel/check.py", "kernel/x.py")):
            repo = self.repo()
            gitfix.move(repo, old, new)
            commit_all(repo, "rename")
            r = self.judge(repo)
            self.assertNotIn(old, r["touched"], "git reports the rename under its new name only; the guard must not rely on paths")
            self.assertEqual((r["ok"], r["reason"]), (False, "trusted_path"), (old, new))
            self.assertIn(old, r["detail"])
        repo = self.repo()
        gitfix.move(repo, "README.md", "transcripts/README.md")
        commit_all(repo, "rename docs")
        self.assertTrue(self.judge(repo)["ok"])

    def test_deletion_is_refused(self):
        repo = self.repo()
        git(repo, "rm", "-q", "SPEC.md")
        commit_all(repo, "delete")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "trusted_path"))

    def test_trunk_moving_its_trusted_base_requires_a_rebase(self):
        repo = self.repo()
        write(repo, "README.md", "proposal\n")
        commit_all(repo, "docs")
        git(repo, "checkout", "-q", "main")
        write(repo, "kernel/check.py", "# Guy's own change\n")
        commit_all(repo, "trunk kernel change")
        git(repo, "checkout", "-q", "pr")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["touched"]), (False, "trusted_path", ["README.md"]))
        self.assertIn("kernel/check.py", r["detail"])

    def test_digest_covers_trusted_base_only(self):
        repo = self.repo()
        d0 = judge.digest(repo, self.main)
        files = {"kernel/check.py", "kernel/log.py", "judge/judge.py", ".github/workflows/judge.yml", "SPEC.md"}
        self.assertTrue(files <= set(judge.trusted_files(repo, self.main)))
        self.assertNotIn("README.md", judge.trusted_files(repo, self.main))
        self.assertNotIn("CHARTER.md", judge.trusted_files(repo, self.main))
        write(repo, "README.md", "x\n"); sha = commit_all(repo, "readme")
        self.assertEqual(judge.digest(repo, sha), d0)
        write(repo, "kernel2/check", "#!/bin/sh\n"); sha = commit_all(repo, "kernel2")
        self.assertNotEqual(judge.digest(repo, sha), d0)
        self.assertIn("kernel2/check", judge.trusted_files(repo, sha))
        write(repo, "SPEC.md", "y\n"); sha = commit_all(repo, "spec")
        self.assertNotEqual(judge.digest(repo, sha), d0)
        expected = hashlib.sha256()
        for path in sorted(judge.trusted_files(repo, self.main)):
            expected.update(path.encode() + b"\0" + judge.show(repo, self.main, path) + b"\0")
        self.assertEqual(d0, expected.hexdigest())
        self.assertEqual(judge.TRUSTED, ("kernel/", "kernel2/", "judge/", ".github/workflows/", "SPEC.md"))


class Charter(Fixture):
    def test_genesis_charter_hash_must_match_trunks_charter(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "CHARTER.md", gitfix.CHARTER_TEXT + "\namended by Guy\n")
        commit_all(repo, "Guy edits the charter after genesis")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        self.append(repo)
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["touched"]), (False, "charter_mismatch", ["log.jsonl"]))

    def test_no_genesis_no_charter_check(self):
        repo = self.repo(with_log=False)
        git(repo, "checkout", "-q", "main")
        write(repo, "CHARTER.md", "a different charter\n")
        commit_all(repo, "charter before genesis")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        write(repo, "README.md", "x\n")
        commit_all(repo, "docs")
        self.assertTrue(self.judge(repo)["ok"])

    def test_charter_check_precedes_the_kernel(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "CHARTER.md", "changed\n")
        commit_all(repo, "charter")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        self.lg.add("proposal", "guy", proposal("a"), self.w.stranger)
        self.append(repo)
        self.assertEqual(self.judge(repo)["reason"], "charter_mismatch")


class TrunkKernelRuns(Fixture):
    def test_the_kernel_that_runs_is_trunks(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        stub = 'import json, sys\nprint(json.dumps({"ok": False, "seq": 0, "reason": "stub", "detail": ""}))\nsys.exit(1)\n'
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
        self.append(repo)
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


class Scope(Fixture):
    """SPEC §10 items 7-10: attribution, counsel does not build, scope, size cap."""

    def proposal_touching(self, path, proposer="builder m s", data="x\n"):
        repo = self.repo()
        write(repo, path, data)
        commit_all(repo, "change", proposer)
        return self.judge(repo)

    def test_scope_json_is_the_specs(self):
        with open(os.path.join(ROOT, "judge", "scope.json")) as f:
            scope = json.load(f)
        self.assertEqual(scope, {"layer": "C0", "cap": 3000,
            "paths": ["sim/", "harness/", "tests/", "pins/", "tools/", "transcripts/",
                      "REPORT.md", "BRIEF-C1.md", "LAW.md", "README.md", "RUNBOOK.md", "log.jsonl"],
            "documents": ["REPORT.md", "BRIEF-C1.md", "LAW.md", "README.md", "RUNBOOK.md", "transcripts/", "sim/runs/"],
            "counted": ["sim/", "harness/", "tests/", "pins/", "tools/"]})

    def test_unattributed_proposal(self):
        for proposer in (None, "martian x", " ", "Builder x"):
            r = self.proposal_touching("README.md", proposer)
            self.assertEqual((r["ok"], r["reason"]), (False, "unattributed_proposal"), proposer)
        for p in judge.PARTIES:
            r = self.proposal_touching("REPORT.md", f"{p} model session")
            self.assertEqual((r["ok"], r["proposer"]), (True, p), r)

    def test_trailer_is_read_from_the_commit_never_from_files(self):
        r = self.proposal_touching("README.md", None, "Proposer: builder m s\n")
        self.assertEqual(r["reason"], "unattributed_proposal")
        repo = self.repo()
        commit_all(repo, "Proposer: builder m s mentioned in the subject only", None)
        self.assertEqual(self.judge(repo)["reason"], "unattributed_proposal")

    def test_self_check_skips_items_7_to_10(self):
        repo = self.repo()
        write(repo, "README.md", "proposal\n")
        commit_all(repo, "docs")
        git(repo, "checkout", "-q", "main")
        write(repo, "REPORT.md", "trunk moved on\n")
        before = commit_all(repo, "trunk change")
        git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "--no-ff", "pr", "-m", "Merge pull request #1")
        self.assertEqual(len(git(repo, "rev-list", "--parents", "-1", "main").split()), 3)
        r = self.judge(repo, "main", "main")
        self.assertEqual((r["ok"], r["reason"], r["proposer"]), (True, None, None), r)
        r = self.judge(repo, before, "main")
        self.assertEqual((r["ok"], r["reason"], r["proposer"]), (False, "unattributed_proposal", None))
        git(repo, "checkout", "-q", "-b", "pr2", "main")
        write(repo, "README.md", "again\n")
        commit_all(repo, "no trailer", None)
        self.assertEqual(self.judge(repo, "main", "pr2")["reason"], "unattributed_proposal")

    def test_attribution_follows_the_kernel(self):
        repo = self.repo()
        self.lg.add("proposal", "guy", proposal("a"), self.w.stranger)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "bad entry", None)
        self.assertEqual(self.judge(repo)["reason"], "unknown_key")

    def test_counsel_builds(self):
        for path in ("sim/gen.py", "tests/test_x.py", "sim/runsx.txt"):
            r = self.proposal_touching(path, "counsel m s")
            self.assertEqual((r["ok"], r["reason"]), (False, "counsel_builds"), path)
        repo = self.repo()
        self.lg.add("proposal", "ann", proposal("a"), self.w.ann)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "a valid entry, by counsel", "counsel m s")
        self.assertEqual(self.judge(repo)["reason"], "counsel_builds")
        for path in ("REPORT.md", "transcripts/t.txt", "sim/runs/r.txt", "LAW.md"):
            self.assertTrue(self.proposal_touching(path, "counsel m s")["ok"], path)
        self.assertTrue(self.proposal_touching("sim/gen.py", "builder m s")["ok"])

    def test_out_of_scope(self):
        for path in ("docs/x.md", "REPORT.md.bak", "sim", "x.py", "spec/vectors/v.json"):
            r = self.proposal_touching(path)
            self.assertEqual((r["ok"], r["reason"]), (False, "out_of_scope"), path)
            self.assertIn(path, r["detail"])
        for path in ("sim/x.py", "harness/x.py", "RUNBOOK.md", "transcripts/a/b.txt"):
            self.assertTrue(self.proposal_touching(path)["ok"], path)

    def test_rename_out_of_scope_touches_both_paths(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "notes.txt", "trunk's\n")
        commit_all(repo, "trunk note")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        gitfix.move(repo, "notes.txt", "transcripts/notes.txt")
        commit_all(repo, "move")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["touched"]), (False, "out_of_scope", ["transcripts/notes.txt"]))
        self.assertIn("notes.txt", r["detail"])

    def test_code_cap(self):
        r = self.proposal_touching("sim/big.py", data="x = 1\n" * 3001)
        self.assertEqual((r["ok"], r["reason"]), (False, "code_cap"))
        self.assertTrue(self.proposal_touching("sim/big.py", data="x = 1\n" * 3000)["ok"])
        self.assertTrue(self.proposal_touching("sim/big.py", data="x = 1\n" * 2999 + "y = 2")["ok"])
        self.assertTrue(self.proposal_touching("sim/runs/big.txt", data="x\n" * 4000)["ok"])

    def test_code_cap_counts_the_whole_head_not_the_diff(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "tools/a.py", "a = 1\n" * 2000)
        commit_all(repo, "trunk code")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        write(repo, "pins/b.py", "b = 1\n" * 1001)
        commit_all(repo, "more code")
        self.assertEqual(self.judge(repo)["reason"], "code_cap")


if __name__ == "__main__":
    unittest.main()
