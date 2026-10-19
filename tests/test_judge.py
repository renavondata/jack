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
from pins.fixtures import make_repo, propose

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
        fx = make_repo(self.w, with_log=with_log, tmpdir=self.tmp.name)
        self.lg, self.main = fx.log, fx.main
        return fx.repo

    def judge(self, repo, trunk=None, head=None):
        return judge.judge(repo, trunk or "main", head or "pr")

    def append(self, repo, msg="append"):
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, msg)

    def propose(self, repo, msg="change", party="builder", key=None):
        """The working tree as the proposal's work, attributed by a signed proposal entry (SPEC §10.7)."""
        write(repo, "log.jsonl", self.lg.text())
        return propose(repo, self.lg, self.w, party, msg, key)


class Verdicts(Fixture):
    def test_valid_appended_entry_is_accepted(self):
        repo = self.repo()
        self.propose(repo, party="ann", key=self.w.ann)
        line = self.lg.lines[-1]
        r = self.judge(repo)
        self.assertTrue(r["ok"], r)
        self.assertEqual((r["reason"], r["touched"], r["appended"], r["proposer"]), (None, ["log.jsonl"], 1, "ann"))
        blob = base64.b64decode(json.loads(line)["sig"])
        n = int.from_bytes(blob[10:14], "big")
        fp = "SHA256:" + base64.b64encode(hashlib.sha256(blob[14:14 + n]).digest()).decode().rstrip("=")
        self.assertEqual(r["signers"], [fp])
        self.assertEqual(r["verdict"], {"ok": True, "entries": 2})
        self.assertEqual(r["trusted_digest"], judge.digest(repo, self.main))
        self.assertEqual(r["kernel2"], "absent")

    def test_nothing_appended_is_unattributed(self):
        repo = self.repo()
        write(repo, "README.md", "changed\n")
        commit_all(repo, "docs")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["appended"], r["touched"], r["reason"]), (False, 0, ["README.md"], "unattributed_proposal"))

    def test_no_logs_anywhere(self):
        repo = self.repo(with_log=False)
        write(repo, "README.md", "x\n")
        commit_all(repo, "docs")
        self.assertEqual(self.judge(repo)["reason"], "unattributed_proposal")  # no log, so no entry to attribute by

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
        self.propose(repo)
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
        self.propose(repo)
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
        self.propose(repo, "rename docs", "counsel")
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
        self.assertEqual(self.judge(repo)["reason"], "unattributed_proposal")  # past the charter check; no log to attribute by

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


class OpeningGrounds(Fixture):
    def publish(self, repo):
        git(repo, "checkout", "-q", "main")
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "Guy records acts")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")

    def amend(self, id_="A2", height=20, charter=gitfix.CHARTER_SHA256):
        self.lg.add("amend", "guy", {"id": id_, "charter": charter, "activate_at": height}, self.w.guy)

    def decision(self, subject="A2", kind="transmute", key=None, proposer="guy"):
        self.lg.add("decision", proposer, {"kind": kind, "subject": subject}, key or self.w.guy)

    def test_promulgated_charter_even_before_activation(self):
        repo = self.repo()
        text = gitfix.CHARTER_TEXT + "\nA2\n"
        self.decision()
        self.amend(charter=hashlib.sha256(text.encode()).hexdigest())
        git(repo, "checkout", "-q", "main")
        write(repo, "CHARTER.md", text)
        self.publish(repo)
        self.assertTrue(self.judge(repo, "main", "main")["ok"])
        write(repo, "README.md", "docs\n")
        self.propose(repo, "docs", "counsel")
        self.assertTrue(self.judge(repo)["ok"])

    def test_stale_or_invalid_amendment_does_not_bind_charter(self):
        for invalid in (False, True):
            repo = self.repo()
            self.decision()
            self.amend(charter="ff" * 32, height=2 if invalid else 20)
            self.publish(repo)
            r = self.judge(repo, "main", "main")
            self.assertEqual(r["reason"], "schema" if invalid else "charter_mismatch", r)

    def test_trusted_base_recording(self):
        for selfcheck in (False, True):
            repo = self.repo()
            git(repo, "checkout", "-q", "main")
            write(repo, "SPEC.md", "new trusted text\n")
            commit_all(repo, "Guy changes trusted base")
            git(repo, "checkout", "-q", "pr")
            git(repo, "reset", "-q", "--hard", "main")
            write(repo, "README.md", "proposal\n")
            self.propose(repo, "docs", "counsel")
            head = "main" if selfcheck else "pr"
            self.assertEqual(self.judge(repo, "main", head)["reason"], "trusted_base_unrecorded")
            self.lg.add("push", "guy", {"digest": judge.digest(repo, "main"), "review": "0" * 64}, self.w.guy)
            self.publish(repo)
            self.assertTrue(self.judge(repo, "main", "main")["ok"])

    def test_proposal_push_does_not_repair_unrecorded_trunk(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "SPEC.md", "new trusted text\n")
        commit_all(repo, "trusted base changes")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        self.lg.add("push", "guy", {"digest": judge.digest(repo, "main"), "review": "0" * 64}, self.w.guy)
        self.propose(repo)
        self.assertEqual(self.judge(repo)["reason"], "trusted_base_unrecorded")

    def test_freeze_is_strict_and_checks_all_amendments(self):
        for selfcheck in (False, True):
            for height in (3, 4):
                repo = self.repo()
                self.decision()
                self.amend(height=height)
                self.lg.add("push", "guy", {"digest": judge.digest(repo, "main"), "review": "0" * 64}, self.w.guy)
                if selfcheck:
                    self.publish(repo)
                else:
                    self.propose(repo)
                r = self.judge(repo, "main", "main" if selfcheck else "pr")
                self.assertEqual((r["ok"], r["reason"]), (height == 3, None if height == 3 else "push_during_amendment"))
        repo = self.repo()
        self.decision()
        self.amend(height=10)
        self.decision("A3")
        self.amend("A3", height=5)
        self.lg.add("push", "guy", {"digest": judge.digest(repo, "main"), "review": "0" * 64}, self.w.guy)
        self.propose(repo)
        self.assertEqual(self.judge(repo)["reason"], "push_during_amendment")

    def test_transmutation_is_prior_and_names_the_amendment(self):
        for selfcheck in (False, True):
            for earlier in ("none", "wrong_subject", "wrong_kind", "after", "correct"):
                repo = self.repo()
                if earlier == "wrong_subject":
                    self.decision("A3")
                if earlier == "wrong_kind":
                    self.decision(kind="fix")
                if earlier == "correct":
                    self.decision()
                self.amend()
                if earlier == "after":
                    self.decision()
                if selfcheck:
                    self.publish(repo)
                else:
                    self.propose(repo)
                r = self.judge(repo, "main", "main" if selfcheck else "pr")
                self.assertEqual((r["ok"], r["reason"]), (earlier == "correct", None if earlier == "correct" else "amend_untransmuted"), r)

    def test_decision_requires_original_genesis_blob_not_principal_or_id(self):
        for selfcheck in (False, True):
            for kind in ("veto", "promote", "budget", "grant", "transmute", "fix"):
                repo = self.repo()
                self.lg.add("key", "guy", build.decl("guy-master", "guy", self.w.stranger, build.ALL), self.w.guy)
                self.decision(kind=kind, key=self.w.stranger)
                if selfcheck:
                    self.publish(repo)
                else:
                    self.propose(repo)
                r = self.judge(repo, "main", "main" if selfcheck else "pr")
                self.assertEqual(r["reason"], "decision_by_other", r)
        repo = self.repo()
        self.lg.add("key", "guy", build.decl("ann-1", "renamed", self.w.ann, ["decision"]), self.w.guy)
        self.decision(key=self.w.ann, proposer="renamed")
        self.propose(repo)
        self.assertTrue(self.judge(repo)["ok"])  # any genesis-declared key, even after a new principal


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
        self.propose(repo)
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
    """SPEC §10 items 7-10: attribution by the signed proposal entry, the party's paths, the layer's paths, the size cap."""

    def proposal_touching(self, path, party="builder", data="x\n", key=None):
        repo = self.repo()
        write(repo, path, data)
        self.propose(repo, party=party, key=key)
        return self.judge(repo)

    def scope(self):
        with open(os.path.join(ROOT, "judge", "scope.json")) as f:
            return json.load(f)

    def test_scope_json_is_the_specs(self):
        with open(os.path.join(ROOT, "SPEC.md")) as f:
            spec = f.read()
        block = spec.split("at C1 it is:", 1)[1].split("```", 2)[1]
        self.assertEqual(self.scope(), json.loads(block))

    def test_party_is_the_principal_of_the_signing_key(self):
        for party in ("builder", "reviewer", "counsel"):
            r = self.proposal_touching("transcripts/t.txt", party)
            self.assertEqual((r["ok"], r["proposer"]), (True, party), r)
        r = self.proposal_touching("README.md", "ann", key=self.w.ann)
        self.assertEqual((r["ok"], r["proposer"]), (True, "ann"), r)

    def test_a_trailer_alone_does_not_attribute(self):
        repo = self.repo()
        write(repo, "README.md", "x\n")
        commit_all(repo, "change", "builder m s")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["proposer"]), (False, "unattributed_proposal", None))

    def test_entry_must_name_a_commit_of_the_proposal(self):
        for named in ("hex40", "trunk"):
            repo = self.repo()
            write(repo, "README.md", "x\n")
            commit_all(repo, "work")
            self.lg.add("proposal", "builder", proposal("a", commit=build.HEX40 if named == "hex40" else self.main),
                        self.w.parties["builder"])
            self.append(repo, "entry")
            r = self.judge(repo)
            self.assertEqual((r["ok"], r["reason"]), (False, "unattributed_proposal"), named)

    def test_entry_must_be_appended_not_trunks(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "-b", "side", "main")
        write(repo, "README.md", "x\n")
        work = commit_all(repo, "work")
        git(repo, "checkout", "-q", "main")
        self.lg.add("proposal", "builder", proposal("a", commit=work), self.w.parties["builder"])
        self.append(repo, "trunk records an entry naming the side branch's commit")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "side", "-m", "take the work")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["appended"]), (False, "unattributed_proposal", 0))

    def test_later_commits_change_only_the_log(self):
        repo = self.repo()
        write(repo, "sim/x.py", "x\n")
        self.propose(repo)
        write(repo, "sim/y.py", "y\n")
        commit_all(repo, "after the entry")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "unattributed_proposal"))
        self.assertIn("sim/y.py", r["detail"])
        repo = self.repo()
        write(repo, "sim/x.py", "x\n")
        self.propose(repo)
        write(repo, "sim/y.py", "y\n")
        commit_all(repo, "after the entry")
        git(repo, "rm", "-q", "sim/y.py")
        commit_all(repo, "and back")
        self.assertEqual(self.judge(repo)["reason"], "unattributed_proposal", "each commit is judged, not the net diff")
        repo = self.repo()
        write(repo, "sim/x.py", "x\n")
        self.propose(repo)
        self.lg.add("proposal", "ann", proposal("b"), self.w.ann)
        self.append(repo, "a log-only commit after the entry")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["proposer"]), (True, "builder"), r)

    def test_a_merge_after_the_entry_counts_against_its_first_parent(self):
        repo = self.repo()
        write(repo, "sim/x.py", "x\n")
        self.propose(repo)
        git(repo, "checkout", "-q", "main")
        write(repo, "README.md", "trunk moved on\n")
        commit_all(repo, "trunk change")
        git(repo, "checkout", "-q", "pr")
        git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "main", "-m", "merge trunk")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "unattributed_proposal"))
        self.assertIn("README.md", r["detail"])

    def test_the_last_entry_attributes(self):
        for order, reason, party in ((("reviewer", "builder"), "party_scope", "builder"), (("builder", "reviewer"), None, "reviewer")):
            repo = self.repo()
            write(repo, "pins/p.py", "x\n")
            work = commit_all(repo, "work")
            for p in order:
                self.lg.add("proposal", p, proposal(p, commit=work), self.w.parties[p])
            self.append(repo, "entries")
            r = self.judge(repo)
            self.assertEqual((r["reason"], r["proposer"]), (reason, party), order)

    def test_party_under_the_law_in_force_at_the_entry(self):
        repo = self.repo()
        write(repo, "sim/x.py", "x\n")
        self.propose(repo)
        self.lg.add("key", "guy", build.decl("builder-1", "reviewer", self.w.parties["builder"], ["proposal"]), self.w.guy)
        self.append(repo, "the key is re-declared after the entry")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["proposer"]), (True, "builder"), r)
        repo = self.repo()
        write(repo, "sim/x.py", "x\n")
        self.lg.add("key", "guy", build.decl("stranger-1", "counsel", self.w.stranger, ["proposal"]), self.w.guy)
        self.propose(repo, party="counsel", key=self.w.stranger)
        r = self.judge(repo)
        self.assertEqual((r["reason"], r["proposer"]), ("party_scope", "counsel"), r)

    def test_attribution_follows_the_kernel(self):
        repo = self.repo()
        self.lg.add("proposal", "guy", proposal("a"), self.w.stranger)
        write(repo, "log.jsonl", self.lg.text())
        commit_all(repo, "bad entry", None)
        self.assertEqual(self.judge(repo)["reason"], "unknown_key")

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

    def test_party_scope(self):
        cases = {"builder": (("pins/p.py", "spec/vectors/v.json", "REPORT.md", "LAW.md", "docs/x.md"),
                             ("sim/x.py", "tests/t.py", "tools/t", "harness/h.py", "transcripts/t.txt", "sim/runs/r.json")),
                 "reviewer": (("sim/x.py", "tests/t.py", "tools/t", "README.md", "pinsx.py"),
                              ("pins/p.py", "spec/vectors/v.json", "transcripts/t.txt")),
                 "counsel": (("sim/gen.py", "tests/test_x.py", "sim/runsx.txt", "pins/p.py", "spec/vectors/v.json"),
                             ("REPORT.md", "transcripts/t.txt", "sim/runs/r.txt", "LAW.md", "RUNBOOK.md", "BRIEF-C1.md"))}
        for party, (refused, admitted) in cases.items():
            for path in refused:
                r = self.proposal_touching(path, party)
                self.assertEqual((r["ok"], r["reason"], r["proposer"]), (False, "party_scope", party), (party, path))
                self.assertIn(path, r["detail"])
            for path in admitted:
                self.assertTrue(self.proposal_touching(path, party)["ok"], (party, path))

    def test_a_party_absent_from_parties_is_bounded_by_paths_only(self):
        for path in ("pins/p.py", "sim/x.py", "REPORT.md", "spec/vectors/v.json"):
            self.assertTrue(self.proposal_touching(path, "ann", key=self.w.ann)["ok"], path)
        self.assertEqual(self.proposal_touching("docs/x.md", "ann", key=self.w.ann)["reason"], "out_of_scope")

    def test_rename_touches_both_paths_for_the_party_too(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "sim/a.py", "a = 1\n")
        commit_all(repo, "trunk code")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        gitfix.move(repo, "sim/a.py", "pins/a.py")
        self.propose(repo, "move", "reviewer")
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"]), (False, "party_scope"))
        self.assertIn("sim/a.py", r["detail"])

    def test_out_of_scope(self):
        for path in ("docs/x.md", "REPORT.md.bak", "sim", "x.py", "spec/x.json"):
            r = self.proposal_touching(path, "ann", key=self.w.ann)
            self.assertEqual((r["ok"], r["reason"]), (False, "out_of_scope"), path)
            self.assertIn(path, r["detail"])
        for path in ("sim/x.py", "harness/x.py", "RUNBOOK.md", "transcripts/a/b.txt", "spec/vectors/v.json"):
            self.assertTrue(self.proposal_touching(path, "ann", key=self.w.ann)["ok"], path)

    def test_rename_out_of_scope_touches_both_paths(self):
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "notes.txt", "trunk's\n")
        commit_all(repo, "trunk note")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        gitfix.move(repo, "notes.txt", "transcripts/notes.txt")
        self.propose(repo, "move", "ann", self.w.ann)
        r = self.judge(repo)
        self.assertEqual((r["ok"], r["reason"], r["touched"]), (False, "out_of_scope", ["log.jsonl", "transcripts/notes.txt"]))
        self.assertIn("notes.txt", r["detail"])

    def test_code_cap(self):
        cap = self.scope()["cap"]
        r = self.proposal_touching("sim/big.py", data="x = 1\n" * (cap + 1))
        self.assertEqual((r["ok"], r["reason"]), (False, "code_cap"))
        self.assertTrue(self.proposal_touching("sim/big.py", data="x = 1\n" * cap)["ok"])
        self.assertTrue(self.proposal_touching("sim/big.py", data="x = 1\n" * (cap - 1) + "y = 2")["ok"])
        self.assertTrue(self.proposal_touching("sim/runs/big.txt", data="x\n" * (cap + 1))["ok"])

    def test_code_cap_counts_python_shebang_files(self):
        cap = self.scope()["cap"]
        for shebang in ("#!/usr/bin/env python3", "#!/usr/bin/python", "#! /usr/bin/env python"):
            r = self.proposal_touching("tools/big", data=shebang + "\n" + "x = 1\n" * cap)
            self.assertEqual((r["ok"], r["reason"]), (False, "code_cap"), shebang)
            self.assertTrue(self.proposal_touching("tools/big", data=shebang + "\n" + "x = 1\n" * (cap - 1))["ok"], shebang)
        for data in ("#!/bin/sh\n" + "python x\n" * cap, "\n#!/usr/bin/python\n" + "x\n" * cap, "# python\n" + "x\n" * cap):
            self.assertTrue(self.proposal_touching("tools/big", data=data)["ok"], data[:20])

    def test_code_cap_refuses_a_symlink_under_counted(self):
        """SPEC §10.10: a symbolic link under a counted prefix is refused whatever it points to, and named."""
        cap = self.scope()["cap"]
        for target, data in (("../transcripts/long", "#!/usr/bin/env python3\n" + "x = 1\n" * cap),
                             ("../transcripts/short", "x\n"), ("../sim/", None), ("../nowhere", None)):
            repo = self.repo()
            if data is not None:
                write(repo, target[3:], data)
            gitfix.link(repo, "tools/script", target)
            self.propose(repo)
            r = self.judge(repo)
            self.assertEqual((r["ok"], r["reason"]), (False, "code_cap"), target)
            self.assertIn("tools/script", r["detail"])
        repo = self.repo()
        write(repo, "transcripts/short", "x\n")
        gitfix.link(repo, "transcripts/link", "short")
        self.propose(repo)
        self.assertTrue(self.judge(repo)["ok"])

    def test_code_cap_counts_the_whole_head_not_the_diff(self):
        cap = self.scope()["cap"]
        repo = self.repo()
        git(repo, "checkout", "-q", "main")
        write(repo, "tools/a.py", "a = 1\n" * (cap // 2))
        commit_all(repo, "trunk code")
        git(repo, "checkout", "-q", "pr")
        git(repo, "reset", "-q", "--hard", "main")
        write(repo, "tests/b.py", "b = 1\n" * (cap - cap // 2 + 1))
        self.propose(repo, "more code")
        self.assertEqual(self.judge(repo)["reason"], "code_cap")


if __name__ == "__main__":
    unittest.main()
