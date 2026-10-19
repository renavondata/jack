"""tools/jack: each verb's admitted case, one refusal per precondition RUNBOOK.md names, and the always-refused list.

Fixture repositories come from harness/gitfix.py with a local bare `origin`; `gh` and `ssh-keygen` are stub scripts
first on PATH that record their arguments (ssh-keygen then signs for real with throwaway keys). No network."""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from harness import build, gitfix, keys
from judge.judge import digest as commit_digest
from kernel import log

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KERNEL2_CHECK = ("#!/bin/sh\nexec %s -E -s -c \"import sys; sys.path.insert(0, '%s'); from kernel.check import main; "
                 "sys.exit(main(sys.argv))\" \"$@\"\n" % (sys.executable, ROOT))
GH = """#!%s
import json, os, sys
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps(["gh"] + sys.argv[1:]) + "\\n")
for prefix, rc, out in json.load(open(os.environ["STUB_GH"])):
    if sys.argv[1:1 + len(prefix)] == prefix:
        sys.stdout.write(out)
        sys.exit(rc)
""" % sys.executable
SSH_KEYGEN = """#!%s
import json, os, sys
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps(["ssh-keygen"] + sys.argv[1:]) + "\\n")
os.execv(%r, [%r] + sys.argv[1:])
""" % (sys.executable, shutil.which("ssh-keygen"), shutil.which("ssh-keygen"))
TRAILER = "Proposer: builder claude test"


def read(path):
    with open(path, "rb") as f:
        return f.read()


def write(path, text, mode=0o644):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    os.chmod(path, mode)


def template(tmp):
    """A bare origin whose main holds kernel/, judge/, kernel2/ (a wrapper of the kernel), the tools, a trivial check
    and a genesis declaring guy (all powers), builder-1 {proposal, spec_conflict} and odd-1, whose principal has a <."""
    w = build.World(tmp)
    w.odd, w.nobody = keys.make_key(tmp, "odd"), keys.make_key(tmp, "nobody")
    w.decls = [build.decl("guy-master", "guy", w.guy, build.ALL), build.decl("builder-1", "builder", w.ann, ["proposal", "spec_conflict"]),
               build.decl("odd-1", "x<y", w.odd, ["decision"])]
    repo = gitfix.make_repo(w, with_log=False, tmpdir=tmp).repo
    gitfix.git(repo, "checkout", "-q", "main")
    gitfix.git(repo, "branch", "-D", "pr")
    for rel in ("tools/jack", "tools/entry.py", "tools/digest.py", "tools/count_kernel.py", "sim/__init__.py", "sim/gen.py", "sim/seeds.txt"):
        os.makedirs(os.path.dirname(os.path.join(repo, rel)), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, rel), os.path.join(repo, rel))
    shutil.copytree(os.path.join(ROOT, "harness"), os.path.join(repo, "harness"), ignore=shutil.ignore_patterns("__pycache__"))
    write(os.path.join(repo, "tests/__init__.py"), "")
    write(os.path.join(repo, "tests/test_ok.py"), "import unittest\n\n\nclass Ok(unittest.TestCase):\n    def test_ok(self):\n        pass\n")
    write(os.path.join(repo, "pins/run.py"), "import os, sys\nsys.exit(os.path.exists(os.path.join(os.path.dirname(__file__), 'FAIL')))\n")
    write(os.path.join(repo, "kernel2/build.sh"), "#!/bin/sh\ntrue\n", 0o755)
    write(os.path.join(repo, "kernel2/check"), KERNEL2_CHECK, 0o755)
    write(os.path.join(repo, ".gitignore"), "__pycache__/\n*.pyc\nkernel2/.cache/\n")
    gitfix.commit_all(repo, "the tree")
    write(os.path.join(repo, "log.jsonl"), w.log(charter=gitfix.CHARTER_SHA256, checker=commit_digest(repo, "HEAD")).text())
    gitfix.commit_all(repo, "genesis")
    write(os.path.join(repo, "README.md"), "readme, revised\n")
    gitfix.commit_all(repo, "a commit after genesis, so that origin/main~1 has a log")
    subprocess.run(["git", "clone", "-q", "--bare", repo, os.path.join(tmp, "origin.git")], check=True)
    return w, os.path.join(tmp, "origin.git")


class Jack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory(prefix="jack ")
        cls.w, cls.origin_template = template(cls.shared.name)

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="jack-test ")
        t = self.tmp.name
        self.origin, self.repo, self.log_file, stubs = (os.path.join(t, n) for n in ("origin.git", "repo", "calls", "stubs"))
        shutil.copytree(self.origin_template, self.origin)
        write(os.path.join(stubs, "gh"), GH, 0o755)
        write(os.path.join(stubs, "ssh-keygen"), SSH_KEYGEN, 0o755)
        write(os.path.join(t, "gitconfig"), "[user]\n\tname = t\n\temail = t@t\n")
        self.env = dict(os.environ, PATH=stubs + os.pathsep + os.environ["PATH"], STUB_LOG=self.log_file, JACK_SEEDS="12",
                        STUB_GH=os.path.join(t, "gh.json"), GIT_CONFIG_GLOBAL=os.path.join(t, "gitconfig"), GIT_CONFIG_NOSYSTEM="1")
        self.gh()
        subprocess.run(["git", "clone", "-q", self.origin, self.repo], check=True, env=self.env)

    def tearDown(self):
        self.tmp.cleanup()

    def gh(self, *first, pr=None):
        """Stub responses: `first` (prefix, rc, stdout) win over the defaults."""
        pr = dict({"state": "OPEN", "baseRefName": "main", "mergeable": "MERGEABLE", "headRefName": "work"}, **(pr or {}))
        rules = [*first, (["pr", "view"], 0, json.dumps(pr)), (["pr", "list"], 0, ""), (["pr", "create"], 0, "https://x/pull/7\n"),
                 (["run", "list"], 0, "4242\n"), (["run", "watch"], 0, ""), (["pr", "checks"], 0, ""), (["pr", "merge"], 0, "")]
        write(self.env["STUB_GH"], json.dumps([list(r) for r in rules]))

    def jack(self, *args, key=None, cwd=None):
        open(self.log_file, "w").close()
        key = (key or self.w.guy).path
        return subprocess.run([sys.executable, os.path.join(cwd or self.repo, "tools", "jack"), "--key", key, *args],
                              cwd=cwd or self.repo, env=self.env, capture_output=True, text=True)

    def calls(self, *prefix):
        with open(self.log_file) as f:
            return [c for c in map(json.loads, f) if c[:len(prefix)] == list(prefix)]

    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd or self.repo, env=self.env, capture_output=True, text=True, check=True).stdout.strip()

    def commit(self, rel, text, msg="work", trailer=True, cwd=None):
        write(os.path.join(cwd or self.repo, rel), text)
        self.git("add", "-A", cwd=cwd)
        self.git("commit", "-q", "-m", msg, *(["-m", TRAILER] if trailer else []), cwd=cwd)
        return self.git("rev-parse", "HEAD", cwd=cwd)

    def entries(self, rev="HEAD"):
        return [json.loads(l) for l in self.git("show", f"{rev}:log.jsonl").splitlines()]

    def remote(self, ref="main"):
        return subprocess.run(["git", "--git-dir", self.origin, "rev-parse", ref], capture_output=True, text=True).stdout.strip()

    def admitted(self, r):
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def refused(self, r, words, signed=False):
        """Refused with exit 1 and its reason; nothing pushed to main; signed only when the kernel was asked."""
        self.assertEqual((r.returncode, r.stdout.count("refused")), (1, 0), r.stderr)
        self.assertIn(words, r.stderr)
        keys = {k.path for k in (self.w.guy, self.w.ann, self.w.odd, self.w.nobody)}
        self.assertEqual(any(c[4] in keys for c in self.calls("ssh-keygen", "-Y", "sign", "-f")), signed)  # the simulator signs too

    def branch(self, name="work", **kw):
        self.git("checkout", "-q", "-b", name)
        return self.commit(**dict(dict(rel="README.md", text="work\n"), **kw))

    # The common rules and the always-refused list.

    def test_always_refused_arguments_admin_and_force(self):
        for args in (["decision", "veto", "x", "--admin"], ["proposal", "--title", "--force"], ["decision", "fix", "x--force-with-lease"]):
            with self.subTest(args):
                self.refused(self.jack(*args), "--admin and --force are refused")
                self.assertEqual(self.calls(), [])

    def test_trailer_with_less_than_is_refused_before_signing(self):
        self.refused(self.jack("decision", "veto", "x", key=self.w.odd), "a trailer containing < is refused")

    def test_undeclared_key_is_refused_before_signing(self):
        self.refused(self.jack("decision", "veto", "x", key=self.w.nobody), "not a key the log declares")

    def test_dirty_tree_detached_head_and_wrong_branch(self):
        write(os.path.join(self.repo, "stray.txt"), "x")
        self.refused(self.jack("decision", "veto", "x"), "the tree is not clean")
        os.remove(os.path.join(self.repo, "stray.txt"))
        self.git("checkout", "-q", "--detach")
        self.refused(self.jack("decision", "veto", "x"), "detached HEAD")
        self.refused(self.jack("proposal", key=self.w.ann), "detached HEAD")
        self.git("checkout", "-q", "main")
        self.refused(self.jack("proposal", key=self.w.ann), "wrong branch main")
        self.refused(self.jack("spec_conflict", "--section", "5", "--text", "t", key=self.w.ann), "wrong branch main")
        self.branch()
        for args in (["decision", "veto", "x"], ["merge", "7"], ["push", "main", "--review", "none"], ["amend", "A3", "f"],
                     ["key", "k", "--principal", "p", "--powers", "", "--pubkey", self.w.nobody.path + ".pub"]):
            self.refused(self.jack(*args), "wrong branch work")

    def test_main_verbs_require_main_equal_to_origin_main(self):
        self.commit("README.md", "ahead\n")
        self.refused(self.jack("decision", "veto", "x"), "not up to date")
        self.git("reset", "-q", "--hard", "origin/main")
        other = os.path.join(self.tmp.name, "other")
        self.git("clone", "-q", self.origin, other)
        self.commit("README.md", "moved\n", cwd=other)
        self.git("push", "-q", "origin", "main", cwd=other)
        self.refused(self.jack("decision", "veto", "x"), "not up to date")  # the verb fetched first

    def test_kernel_refusal_appends_nothing_and_resets(self):
        before = self.git("rev-parse", "HEAD")
        r = self.jack("decision", "veto", "x", key=self.w.ann)  # builder-1 holds no `decision`: no_power
        self.refused(r, "the kernel refuses the decision entry", signed=True)
        self.assertIn("no_power", r.stderr)
        self.assertEqual((self.git("rev-parse", "HEAD"), self.git("status", "--porcelain"), self.remote()), (before, "", before))

    def test_failed_selfcheck_undoes_with_reset_hard_origin_main_and_pushes_nothing(self):
        moved = self.commit("SPEC.md", "unrecorded change to the trusted base\n")
        self.git("push", "-q", "origin", "main")
        r = self.jack("decision", "veto", "x")
        self.refused(r, "judge/selfcheck.py fails after the commit", signed=True)
        self.assertIn("git reset --hard origin/main", r.stderr)
        self.assertEqual((self.git("rev-parse", "HEAD"), self.remote(), self.git("status", "--porcelain")), (moved, moved, ""))
        self.assertEqual(self.calls("gh"), [])

    # jack decision

    def test_decision_admitted_with_the_main_verb_ending(self):
        r = self.jack("decision", "grant", "judge image sha256:ab")
        self.admitted(r)
        head = self.git("rev-parse", "HEAD")
        self.assertEqual(self.remote(), head)
        e = self.entries()[-1]
        self.assertEqual((e["type"], e["proposer"], e["body"]), ("decision", "guy", {"kind": "grant", "subject": "judge image sha256:ab"}))
        self.assertTrue(log.instant(e["ts"]) and e["ts"] > build.TS)  # the clock, UTC
        self.assertEqual(self.git("log", "-1", "--format=%B"), "decision: grant judge image sha256:ab\n\nProposer: guy guy-master")
        sign = self.calls("ssh-keygen")[0]
        self.assertEqual(sign[:7], ["ssh-keygen", "-Y", "sign", "-f", self.w.guy.path, "-n", "core-entry"])
        self.assertEqual(self.calls("gh"), [["gh", "run", "list", "--branch", "main", "--commit", head, "--json", "databaseId", "--jq",
                                            ".[0].databaseId"], ["gh", "run", "watch", "4242", "--exit-status"]])
        self.assertIn("run 4242 of main", r.stdout)

    def test_decision_refusals(self):
        self.refused(self.jack("decision", "wish", "x"), "KIND must be one of")
        self.refused(self.jack("decision", "veto", ""), "SUBJECT must be a non-empty string")

    # jack key

    def test_key_admitted_and_revocation(self):
        self.admitted(self.jack("key", "reviewer-1", "--principal", "reviewer", "--powers", "proposal", "--pubkey", self.w.nobody.path + ".pub"))
        self.assertEqual(self.entries()[-1]["body"], build.decl("reviewer-1", "reviewer", self.w.nobody, ["proposal"]))
        self.assertEqual(self.git("log", "-1", "--format=%s"), "key: reviewer-1")
        self.admitted(self.jack("key", "reviewer-1", "--principal", "reviewer", "--powers", "", "--pubkey", self.w.nobody.path + ".pub"))
        self.assertEqual(self.entries()[-1]["body"]["powers"], [])
        self.assertEqual(self.remote(), self.git("rev-parse", "HEAD"))

    def test_key_refusals(self):
        three = os.path.join(self.tmp.name, "three.pub")
        write(three, self.w.nobody.pubkey + " comment\n")
        args = ["--principal", "reviewer", "--pubkey", self.w.nobody.path + ".pub"]
        self.refused(self.jack("key", "r-1", "--principal", "r", "--powers", "proposal", "--pubkey", three), "not a two-field ssh-ed25519")
        self.refused(self.jack("key", "r-1", "--powers", "proposal,wish", *args), "powers outside the eight: wish")
        self.refused(self.jack("key", "guy-master", "--powers", "proposal", *args), "the signer's own key")

    # jack proposal and jack spec_conflict

    def test_proposal_admitted(self):
        work = self.branch(msg="the work")
        r = self.jack("proposal", key=self.w.ann)
        self.admitted(r)
        self.assertIn("PR #7", r.stdout)
        e = self.entries()[-1]
        self.assertEqual((e["type"], e["proposer"], e["body"]), ("proposal", "builder", {"title": "the work", "commit": work}))
        self.assertEqual(self.git("rev-parse", "HEAD^"), work)
        self.assertEqual(self.git("log", "-1", "--format=%B"), "proposal: the work\n\nProposer: builder builder-1")
        self.assertEqual(self.remote("work"), self.git("rev-parse", "HEAD"))
        self.assertEqual(self.remote(), self.git("rev-parse", "origin/main"))  # main untouched
        self.assertEqual(self.calls("gh", "pr", "create"), [["gh", "pr", "create", "--base", "main", "--head", "work", "--title", "the work",
                                                             "--body", "Proposer: builder builder-1"]])

    def test_proposal_with_an_open_pr_does_nothing_more(self):
        self.branch()
        self.gh((["pr", "list"], 0, "5\n"))
        r = self.jack("proposal", "--title", "T", key=self.w.ann)
        self.admitted(r)
        self.assertIn("PR #5", r.stdout)
        self.assertEqual((self.calls("gh", "pr", "create"), self.entries()[-1]["body"]["title"]), ([], "T"))

    def test_proposal_refusals(self):
        self.git("checkout", "-q", "-b", "work", "origin/main~1")  # a branch that does not contain origin/main
        self.commit("tests/notes.txt", "old base\n")
        r = self.jack("proposal", key=self.w.ann)
        self.refused(r, 'git merge origin/main -m "Merge main into work" -m "Proposer: builder builder-1"')
        self.git("merge", "-q", "origin/main", "-m", "Merge main into work", "-m", TRAILER)
        write(os.path.join(self.repo, "tests/notes.txt"), "uncommitted\n")
        self.refused(self.jack("proposal", key=self.w.ann), "the tree is not clean")
        self.commit("pins/FAIL", "")
        self.refused(self.jack("proposal", key=self.w.ann), "the check fails: pins/run.py")

    def test_branch_verb_push_rejected_prints_the_finishing_commands_and_undoes_nothing(self):
        self.branch()
        self.git("push", "-q", "origin", "work")
        other = os.path.join(self.tmp.name, "other")
        self.git("clone", "-q", "-b", "work", self.origin, other)
        self.commit("README.md", "moved\n", cwd=other)
        self.git("push", "-q", "origin", "work", cwd=other)
        r = self.jack("proposal", key=self.w.ann)
        self.refused(r, "the commit stands; finish the act with:\n  git push -u origin work\n  gh pr create --base main", signed=True)
        self.assertEqual((self.entries()[-1]["type"], self.calls("gh")), ("proposal", []))

    def test_spec_conflict_admitted_and_refused_off_origin_main(self):
        self.branch()
        self.commit("pins/FAIL", "")  # spec_conflict runs no check: it is filed exactly when the tests cannot pass
        r = self.jack("spec_conflict", "--section", "RUNBOOK merge", "--text", "cannot", key=self.w.ann)
        self.admitted(r)
        self.assertIn("stopped: the specification cannot be implemented as written; see PR #7", r.stdout)
        self.assertEqual(self.entries()[-1]["body"], {"section": "RUNBOOK merge", "text": "cannot"})
        self.assertEqual(self.git("log", "-1", "--format=%s"), "spec_conflict: RUNBOOK merge")
        self.assertEqual(self.calls("gh", "pr", "create")[0][7:9], ["--title", "spec_conflict: RUNBOOK merge"])
        self.git("checkout", "-q", "-b", "old", "origin/main~1")
        self.refused(self.jack("spec_conflict", "--section", "s", "--text", "t", key=self.w.ann), "does not contain origin/main")

    # jack merge

    def proposed(self):
        self.branch()
        self.admitted(self.jack("proposal", key=self.w.ann))
        head = self.git("rev-parse", "HEAD")
        self.git("checkout", "-q", "main")
        self.gh(pr={"headRefOid": head})
        return head

    def test_merge_admitted_entry_on_the_proposal_branch_then_github_merges(self):
        head = self.proposed()
        r = self.jack("merge", "7")
        self.admitted(r)
        tip = self.remote("work")
        self.assertEqual(self.git("rev-parse", f"{tip}^", cwd=self.origin), head)
        e = self.entries(tip)[-1]
        self.assertEqual((e["type"], e["body"]), ("merge", {"proposal": 7, "commit": head, "checker": commit_digest(self.repo, "main")}))
        self.assertEqual(self.git("log", "-1", "--format=%B", tip, cwd=self.origin), "merge: #7\n\nProposer: guy guy-master")
        gh = [c[1:4] for c in self.calls("gh")]
        self.assertEqual(gh, [["pr", "view", "7"], ["pr", "checks", "7"], ["pr", "checks", "7"], ["pr", "merge", "7"],
                              ["run", "list", "--branch"], ["run", "watch", "4242"]])
        self.assertEqual(self.calls("gh", "pr", "checks", "7")[1][4:], ["--watch"])
        self.assertEqual(self.remote(), self.git("rev-parse", "origin/main"))  # nothing of jack's reaches main
        self.assertEqual(self.git("worktree", "list").count("\n"), 0)  # the temporary worktree is gone

    def test_merge_refusals(self):
        head = self.proposed()
        for pr, words in (({"state": "CLOSED"}, "state is CLOSED"), ({"baseRefName": "dev"}, "baseRefName is dev"),
                          ({"mergeable": "CONFLICTING"}, "mergeable is CONFLICTING")):
            self.gh(pr=dict(pr, headRefOid=head))
            self.refused(self.jack("merge", "7"), words)
        self.gh((["pr", "checks", "7", "--required"], 1, ""), pr={"headRefOid": head})
        self.refused(self.jack("merge", "7"), "required checks are not green")
        self.git("checkout", "-q", "-b", "bare", "origin/main")
        self.commit("README.md", "no trailer\n", trailer=False)
        self.git("push", "-q", "origin", "bare")
        self.git("checkout", "-q", "main")
        self.gh(pr={"headRefOid": self.git("rev-parse", "bare"), "headRefName": "bare"})
        self.refused(self.jack("merge", "7"), "not one commit past a valid proposal and carries no filled Proposer")

    def test_merge_refused_when_the_proposal_moved_or_was_not_admitted(self):
        head = self.proposed()
        self.gh(pr={"headRefOid": self.git("rev-parse", f"{head}^")})  # GitHub's view is stale: the push is no fast-forward
        self.refused(self.jack("merge", "7"), "the branch moved, run again", signed=True)
        self.assertEqual((self.remote("work"), self.calls("gh", "pr", "merge")), (head, []))
        self.gh((["pr", "checks", "7", "--watch"], 1, ""), pr={"headRefOid": head})
        self.refused(self.jack("merge", "7"), "was not admitted by the judge and the tests; not merged", signed=True)
        self.assertEqual(self.calls("gh", "pr", "merge"), [])

    # jack push

    def test_push_admitted_without_a_run(self):
        built = self.branch("tb", rel="SPEC.md", text="spec, revised\n")
        self.git("checkout", "-q", "main")
        r = self.jack("push", "tb", "--review", "none")
        self.admitted(r)
        self.assertIn("WARNING: --review none: this push was not read", r.stderr)
        self.assertEqual((self.git("rev-parse", "HEAD^"), self.git("rev-parse", "tb"), self.remote()), (built, built, self.git("rev-parse", "HEAD")))
        e = self.entries()[-1]
        self.assertEqual((e["type"], e["body"]), ("push", {"digest": commit_digest(self.repo, "tb"), "review": "0" * 64, "record": "0" * 64}))
        self.assertEqual(self.git("log", "-1", "--format=%B"), "push: tb\n\nProposer: guy guy-master")

    def test_push_admitted_with_the_run_of_record_and_a_review(self):
        self.branch("tb", rel="kernel/__init__.py", text="# revised\n")
        self.git("checkout", "-q", "main")
        review = os.path.join(self.tmp.name, "REVIEW-tb.md")
        write(review, "read cold\n")
        self.admitted(self.jack("push", "tb", "--review", review))
        parts = sorted(glob.glob(os.path.join(self.repo, "transcripts", "diff-12-*-part*.json")))
        self.assertEqual([p[-11:] for p in parts], [f"part{k:02}.json" for k in range(12)])
        reps = [json.loads(read(p)) for p in parts]
        self.assertEqual((sum(r["logs"] for r in reps), [r["seeds"] for r in reps]), (12, [[k, k + 1] for k in range(12)]))
        record = hashlib.sha256(b"".join(map(read, parts))).hexdigest()
        body = self.entries()[-1]["body"]
        self.assertEqual(body, {"digest": commit_digest(self.repo, "tb"), "review": hashlib.sha256(b"read cold\n").hexdigest(), "record": record})
        self.assertEqual(self.git("show", "HEAD:transcripts/REVIEW-tb.md"), "read cold")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_push_counts_a_complete_run_already_on_the_branch(self):
        work = self.branch("tb", rel="kernel/__init__.py", text="# revised\n")
        names = [f"transcripts/diff-12-20261019T0000Z-part{k:02}.json" for k in range(12)]
        for k, n in enumerate(names):
            write(os.path.join(self.repo, n), json.dumps({"logs": 1, "seeds": [k, k + 1], "commit": work, "disagreements": [],
                                                          "uncompared": []}))
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "the run", "-m", TRAILER)
        self.git("checkout", "-q", "main")
        self.admitted(self.jack("push", "tb", "--review", "none"))
        record = hashlib.sha256(b"".join(read(os.path.join(self.repo, n)) for n in names)).hexdigest()
        self.assertEqual(self.entries()[-1]["body"]["record"], record)
        self.assertEqual(len(glob.glob(os.path.join(self.repo, "transcripts", "diff-*"))), 12)  # no second run was made

    def test_push_refusals(self):
        self.refused(self.jack("push", "nope", "--review", "none"), "nope is not a local branch")
        self.refused(self.jack("push", "+main", "--review", "none"), "+main is not a local branch")
        self.git("branch", "old", "HEAD~1")
        self.refused(self.jack("push", "old", "--review", "none"), "old does not contain origin/main")
        self.branch("docs")
        self.git("checkout", "-q", "main")
        self.refused(self.jack("push", "docs", "--review", "none"), "nothing to push: propose and merge")
        self.branch("bare", rel="SPEC.md", text="x\n", trailer=False)
        self.git("checkout", "-q", "main")
        self.refused(self.jack("push", "bare", "--review", "none"), "without a filled Proposer: trailer")
        self.branch("red", rel="SPEC.md", text="x\n")
        self.commit("pins/FAIL", "")
        self.git("checkout", "-q", "main")
        self.refused(self.jack("push", "red", "--review", "none"), "the check fails: pins/run.py")
        self.branch("drift", rel="kernel/__init__.py", text="# revised\n")
        self.commit("kernel2/check", "#!/bin/sh\nexit 3\n")
        self.git("checkout", "-q", "main")
        self.refused(self.jack("push", "drift", "--review", "none"), "the run of record is not twelve parts")
        self.assertEqual((self.git("rev-parse", "HEAD"), self.remote(), self.git("worktree", "list").count("\n")),
                         (self.git("rev-parse", "origin/main"), self.git("rev-parse", "origin/main"), 0))

    def test_push_refused_by_the_kernel_after_the_fast_forward_leaves_main_as_origin_main(self):
        self.branch("tb", rel="kernel/__init__.py", text="# revised\n")
        self.git("checkout", "-q", "main")
        review = os.path.join(self.tmp.name, "REVIEW.md")
        write(review, "read\n")
        r = self.jack("push", "tb", "--review", review, key=self.w.ann)  # builder-1 holds no `push`: no_power
        self.refused(r, "the kernel refuses the push entry", signed=True)
        self.assertEqual((self.git("rev-parse", "HEAD"), self.remote(), self.git("status", "--porcelain", "--ignored", "transcripts")),
                         (self.git("rev-parse", "origin/main"), self.git("rev-parse", "origin/main"), ""))

    def test_push_remove_removes_the_branch_worktree(self):
        wt = os.path.join(self.tmp.name, "wt")
        self.git("worktree", "add", "-q", wt, "-b", "tb")
        self.commit("SPEC.md", "spec, revised\n", cwd=wt)
        self.admitted(self.jack("push", "tb", "--review", "none", "--remove"))
        self.assertFalse(os.path.exists(wt))
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.git("rev-parse", "tb"))

    # jack amend

    def test_amend_admitted_after_transmute_and_its_refusals(self):
        text = os.path.join(self.tmp.name, "A3.md")
        write(text, "## Amendment A3: a test (19 October 2026)\n\nText.\n")
        self.refused(self.jack("amend", "A3", text), "transmute first")
        self.admitted(self.jack("decision", "transmute", "A3"))
        wrong = os.path.join(self.tmp.name, "wrong.md")
        write(wrong, "## Amendment A4: wrong id\n")
        self.refused(self.jack("amend", "A3", wrong), "first line is not '## Amendment A3:'")
        self.admitted(self.jack("amend", "A3", text))
        charter = read(os.path.join(self.repo, "CHARTER.md"))
        self.assertEqual(charter, gitfix.CHARTER_TEXT.encode() + b"\n## Amendment A3: a test (19 October 2026)\n\nText.\n")
        e = self.entries()[-1]
        self.assertEqual(e["body"], {"id": "A3", "charter": hashlib.sha256(charter).hexdigest(), "activate_at": e["seq"] + 1})
        self.assertEqual((self.git("log", "-1", "--format=%s"), self.remote()), ("amend: A3", self.git("rev-parse", "HEAD")))
        self.refused(self.jack("amend", "A3", text), "A3 is already an amendment")


if __name__ == "__main__":
    unittest.main()
