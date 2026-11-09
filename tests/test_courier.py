"""The counsel courier (transcripts/runner/counsel-courier.md, transcripts/runner/README.md):
tools/runner/counsel-sign.py, tools/runner/counsel-act.py, and tools/runner/workflows/*.yml."""
import importlib.util, json, os, shutil, subprocess, sys, tempfile, unittest  # noqa: E401
from harness import build, gitfix
from judge.judge import digest as commit_digest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGN_SCRIPT, ACT_SCRIPT = (os.path.join(ROOT, "tools", "runner", n) for n in ("counsel-sign.py", "counsel-act.py"))
SIGN_WF, ACT_WF = (os.path.join(ROOT, "tools", "runner", "workflows", n) for n in ("counsel-sign.yml", "counsel.yml"))

GH_STUB = """#!%s
import json, os, sys
state_path, args, tok = os.environ["STUB_GH_STATE"], sys.argv[1:], os.environ.get("GH_TOKEN", "")
state = json.load(open(state_path))
state["calls"].append({"args": args, "token": tok})
if args[0] == "pr":
    head = args[args.index("--head") + 1]
    if args[1] == "list":
        prs = [str(p["number"]) for p in state["prs"] if p["head"] == head and p["state"] == "open"]
        out = (prs[0] + "\\n") if prs else ""
    else:
        n = len(state["prs"]) + 1
        state["prs"].append({"number": n, "head": head, "title": args[args.index("--title") + 1],
                             "body": args[args.index("--body") + 1], "state": "open", "user": state["login"]})
        out = f"https://x/pull/{n}\\n"
    json.dump(state, open(state_path, "w")); sys.stdout.write(out); sys.exit(0)
method, fields, raw, use_input, rest, i = "GET", {}, False, False, [], 1
while i < len(args):
    if args[i] == "-X": method, i = args[i + 1], i + 2
    elif args[i] == "-f": k, v = args[i + 1].split("=", 1); fields[k], i = v, i + 2
    elif args[i] == "-H": raw, i = "raw" in args[i + 1], i + 2
    elif args[i] == "--input": use_input, i = True, i + 2
    else: rest.append(args[i]); i += 1
if use_input: fields = json.loads(sys.stdin.read())
ep, out = rest[0], None
if ep == "user": out = {"login": state["login"]}
elif "/commits/" in ep or "/compare/" in ep: out = {"files": state["added_files"]}
elif "/contents/" in ep:
    path = ep.split("/contents/", 1)[1].split("?", 1)[0]
    path in state["contents"] or (json.dump(state, open(state_path, "w")), sys.exit(1))
    val = state["contents"][path]
    if raw: json.dump(state, open(state_path, "w")); sys.stdout.write(val if isinstance(val, str) else json.dumps(val)); sys.exit(0)
    out = val
elif ep.endswith("/pulls") and method == "POST":
    n = len(state["prs"]) + 1
    state["prs"].append({"number": n, "head": fields["head"], "title": fields["title"], "body": fields["body"], "state": "open", "user": state["login"]})
    out = {"number": n, "html_url": f"https://x/pull/{n}"}
elif "/pulls/" in ep:
    pr = next(p for p in state["prs"] if p["number"] == int(ep.rsplit("/", 1)[1]))
    out = {"number": pr["number"], "head": {"ref": pr["head"]}, "state": pr["state"], "user": {"login": pr["user"]}}
elif "/issues?" in ep:
    repo, page = ep.split("/issues?", 1)[0].split("repos/", 1)[1], int(ep.rsplit("page=", 1)[1])
    out = state["issues"].get(repo, [])[(page - 1) * 100:page * 100]
elif ep.endswith("/issues") and method == "POST":
    repo = ep.split("/issues", 1)[0].split("repos/", 1)[1]
    items = state["issues"].setdefault(repo, [])
    n = len(items) + 1
    out = {"number": n, "title": fields["title"], "body": fields["body"], "labels": [{"name": l} for l in fields.get("labels", [])],
           "state": "open", "user": {"login": state["login"]}, "html_url": f"https://x/{repo}/issues/{n}"}
    items.append(out)
elif ep.endswith("/labels") and method == "POST":
    p = ep.split("/")
    item = next(x for x in state["issues"][f"{p[1]}/{p[2]}"] if x["number"] == int(p[4]))
    have = {x["name"] for x in item["labels"]}
    item["labels"] += [{"name": l} for l in fields.get("labels", []) if l not in have]
    out = item["labels"]
elif ep.endswith("/comments") and method == "POST":
    p = ep.split("/")
    state["comments"].append({"repo": f"{p[1]}/{p[2]}", "number": int(p[4]), "body": fields["body"]})
    out = {"id": len(state["comments"])}
elif "/issues/" in ep:
    p = ep.split("/")
    out = next(x for x in state["issues"].get(f"{p[1]}/{p[2]}", []) if x["number"] == int(p[4]))
    method == "PATCH" and out.update(fields)
json.dump(state, open(state_path, "w"))
out is not None and sys.stdout.write(json.dumps(out))
""" % sys.executable


def write_file(path, text, mode=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    if mode is not None:
        os.chmod(path, mode)


def load_script(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def template(tmp):
    w = build.World(tmp)
    w.decls = [build.decl("guy-master", "guy", w.guy, build.ALL),
               build.decl("builder-2", "builder", w.parties["builder"], ["proposal", "spec_conflict", "forecast", "resolution"]),
               build.decl("reviewer-2", "reviewer", w.parties["reviewer"], ["proposal", "forecast", "resolution"]),
               build.decl("counsel-3", "counsel", w.parties["counsel"], ["proposal", "forecast"])]
    repo = gitfix.make_repo(w, with_log=False, tmpdir=tmp).repo
    gitfix.git(repo, "checkout", "-q", "main"), gitfix.git(repo, "branch", "-D", "pr")
    for rel in ("tools/jack", "tools/entry.py", "tools/digest.py", "tools/count_kernel.py",
                "sim/__init__.py", "sim/gen.py", "sim/seeds.txt", "tests/vectors/weak_keys.json"):
        os.makedirs(os.path.dirname(dst := os.path.join(repo, rel)), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, rel), dst)
    os.chmod(os.path.join(repo, "tools/jack"), 0o755)
    shutil.copytree(os.path.join(ROOT, "harness"), os.path.join(repo, "harness"), ignore=shutil.ignore_patterns("__pycache__"))
    write_file(os.path.join(repo, "tests/__init__.py"), "")
    write_file(os.path.join(repo, "tests/test_ok.py"), "import unittest\nclass T(unittest.TestCase):\n def test_ok(self): pass\n")
    write_file(os.path.join(repo, "pins/run.py"), "import sys; sys.exit(0)\n")
    write_file(os.path.join(repo, "kernel2/build.sh"), "#!/bin/sh\ntrue\n", 0o755)
    write_file(os.path.join(repo, "kernel2/check"),
               f"#!/bin/sh\nexec {sys.executable} -E -s -c \"import sys; sys.path.insert(0, '{ROOT}'); "
               "from kernel.check import main; sys.exit(main(sys.argv))\" \"$@\"\n", 0o755)
    write_file(os.path.join(repo, ".gitignore"), "__pycache__/\n*.pyc\n")
    gitfix.commit_all(repo, "the tree")
    write_file(os.path.join(repo, "log.jsonl"), w.log(charter=gitfix.CHARTER_SHA256, checker=commit_digest(repo, "HEAD")).text())
    gitfix.commit_all(repo, "genesis")
    subprocess.run(["git", "clone", "-q", "--bare", repo, origin := os.path.join(tmp, "origin.git")], check=True)
    return w, origin


class CourierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory(prefix="courier-shared-")
        cls.w, cls.origin_template = template(cls.shared.name)

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="courier-test-")
        t = self.tmp.name
        self.home = os.path.join(t, "home")
        self.origin, self.trigger_origin, self.jack, self.trigger, self.wt, self.stubs, self.gh_state = (os.path.join(t, n) for n in ("origin.git", "runner.git", "home/git/jack", "runner", "home/git/worktrees/jack", "stubs", "gh_state.json"))
        shutil.copytree(self.origin_template, self.origin)
        write_file(os.path.join(self.stubs, "gh"), GH_STUB, 0o755)
        subprocess.run(["git", "clone", "-q", "--bare", self.origin, self.trigger_origin], check=True)
        write_file(os.path.join(t, "gitconfig"), f"[user]\n\tname = t\n\temail = t@t\n[url \"{self.trigger_origin}\"]\n\tinsteadOf = https://github.com/renavondata/opencode-runner.git\n")
        self.env = dict(os.environ, HOME=self.home, PATH=self.stubs + os.pathsep + os.environ["PATH"], STUB_GH_STATE=self.gh_state,
                        GITHUB_REPOSITORY="renavondata/opencode-runner", BEFORE="0" * 40, AFTER="a" * 40,
                        READ_TOKEN="read-tok", COUNSEL_GH_TOKEN="counsel-tok", GITHUB_RUN_ID="99",
                        GIT_CONFIG_GLOBAL=os.path.join(t, "gitconfig"), GIT_CONFIG_NOSYSTEM="1")
        self.set_gh()
        subprocess.run(["git", "clone", "-q", self.origin, self.jack], check=True, env=self.env)
        subprocess.run(["git", "clone", "-q", self.trigger_origin, self.trigger], check=True, env=self.env)
        key = os.path.join(self.home, ".ssh", "jack-counsel-3")
        os.makedirs(os.path.dirname(key), exist_ok=True)
        shutil.copy2(self.w.parties["counsel"].path, key)
        shutil.copy2(self.w.parties["counsel"].path + ".pub", key + ".pub")

    def tearDown(self):
        self.tmp.cleanup()

    def set_gh(self, added=(), contents=None, prs=None, issues=None, login="assize-reviewer"):
        write_file(self.gh_state, json.dumps({"login": login, "added_files": [{"filename": f, "status": "added"} for f in added],
                                               "contents": contents or {}, "prs": prs or [], "issues": issues or {}, "comments": [], "calls": []}))
        if added and os.path.isdir(self.trigger):
            before = self.git("rev-parse", "HEAD", cwd=self.trigger)
            for path in added:
                write_file(os.path.join(self.trigger, path), "{}\n")
            self.git("add", *added, cwd=self.trigger)
            self.git("commit", "-q", "-m", "trigger files", cwd=self.trigger)
            after = self.git("rev-parse", "HEAD", cwd=self.trigger)
            self.git("push", "-q", "origin", "main", cwd=self.trigger)
            self.env.update(BEFORE=before, AFTER=after)

    def get_gh(self):
        with open(self.gh_state, encoding="utf-8") as f:
            return json.load(f)

    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd or self.jack, env=self.env, capture_output=True, text=True, check=True).stdout.strip()

    def make_counsel_branch(self, name, req_lines, extra_files=None, symlinks=None, base="origin/main"):
        work = os.path.join(self.tmp.name, f"draft-{name}")
        subprocess.run(["git", "clone", "-q", "-b", "main", self.origin, work], check=True, env=self.env)
        self.git("checkout", "-q", "-b", f"counsel/{name}", base, cwd=work)
        if req_lines is not None:
            write_file(os.path.join(work, "transcripts", "requests", f"{name}.jsonl"),
                       "\n".join(l if isinstance(l, str) else json.dumps(l) for l in req_lines) + "\n")
        for rel, content in (extra_files or {}).items():
            write_file(os.path.join(work, rel), content)
        for rel, target in (symlinks or {}).items():
            os.makedirs(os.path.dirname(dst := os.path.join(work, rel)), exist_ok=True)
            os.path.lexists(dst) and os.remove(dst)
            os.symlink(target, dst)
        self.git("add", "-A", cwd=work)
        self.git("commit", "-q", "-m", f"draft {name}", "-m", "Proposer: counsel test-model s1", cwd=work)
        self.git("push", "-q", "origin", f"counsel/{name}", cwd=work)
        return self.git("rev-parse", "HEAD", cwd=work)

    def trigger_sign(self, rid, branch, extra=None):
        path = f"requests/{rid}.json"
        self.set_gh(added=[path], contents={path: dict({"id": rid, "act": "sign", "branch": branch}, **(extra or {}))})
        return subprocess.run([sys.executable, SIGN_SCRIPT], env=self.env, capture_output=True, text=True)

    def remote_entries(self, ref="main"):
        return [json.loads(l) for l in self.git("--git-dir", self.origin, "show", f"{ref}:log.jsonl").splitlines() if l.strip()]

    def test_workflows_shells_match_readme_and_courier_spec(self):
        for path, name, lane, timeout, script in (
            (SIGN_WF, "name: counsel-sign", "runs-on: [self-hosted, build]", "timeout-minutes: 45", "tools/runner/counsel-sign.py"),
            (ACT_WF, "name: counsel", "runs-on: [self-hosted, opencode]", "timeout-minutes: 10", "tools/runner/counsel-act.py"),
        ):
            with open(path, encoding="utf-8") as f:
                text = f.read()
            for expected in (name, "branches: [counsel-requests]", lane, timeout, f"repos/renavondata/jack/contents/{script}?ref=main"):
                self.assertIn(expected, text)
            self.assertNotIn("concurrency:", text)

    def test_trigger_files_are_not_limited_by_githubs_rest_file_cap(self):
        before = self.git("rev-parse", "main")
        work = os.path.join(self.tmp.name, "trigger-files")
        subprocess.run(["git", "clone", "-q", self.origin, work], check=True, env=self.env)
        for number in range(301):
            write_file(os.path.join(work, "requests", f"{number:03}.json"), "{}\n")
        self.git("add", "requests", cwd=work)
        self.git("commit", "-q", "-m", "many trigger files", cwd=work)
        after = self.git("rev-parse", "HEAD", cwd=work)
        self.git("push", "-q", "origin", "HEAD:main", cwd=work)
        sign, act = load_script(SIGN_SCRIPT, "courier_sign"), load_script(ACT_SCRIPT, "courier_act")
        expected = [f"requests/{number:03}.json" for number in range(301)]
        self.assertEqual(sign.added_files(self.origin, before, after, "read"), expected)
        self.assertEqual(act.added_files(self.origin, before, after, "read"), expected)

    def test_powered_key_declarations_are_not_collapsed_by_key_id(self):
        sign = load_script(SIGN_SCRIPT, "courier_sign_keys")
        entries = [{"type": "key", "body": {"key_id": "same", "pubkey": "pub", "powers": ["proposal"]}},
                   {"type": "key", "body": {"key_id": "same", "pubkey": "pub", "powers": ["forecast"]}}]
        self.assertEqual(len(sign.powered_key_declarations(entries, "pub")), 2)

    def test_sign_custody_paths_are_not_environment_selectable(self):
        with open(SIGN_SCRIPT, encoding="utf-8") as f:
            text = f.read()
        for name in ("COUNSEL_JACK", "COUNSEL_WT", "COUNSEL_KEY", "COUNSEL_TRIGGER_REPO"):
            self.assertNotIn(name, text)

    def test_courier_signs_only_the_request(self):
        """Pin courier_signs_only_the_request: exact request lines in order, once; branch tools/ or symlink refused; merge edit refused."""
        base_len = len(self.remote_entries("main"))
        f1 = {"verb": "forecast", "claim": "first claim", "p": 600, "by": "2099-01-01T00:00:00Z",
              "type": "counsel.undertaking", "args": {"id": "u1", "window": "C2c-1"}}
        f2 = {"verb": "forecast", "claim": "second claim", "p": 700, "by": "2099-01-02T00:00:00Z"}
        prop = {"verb": "proposal", "title": "counsel proposal title"}
        work_sha = self.make_counsel_branch("ok", [f1, f2, prop], extra_files={"transcripts/note.md": "hello\n"})
        r = self.trigger_sign("sign-1", "counsel/ok")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        own = self.remote_entries("counsel/ok")[base_len:]
        self.assertEqual([(e["type"], e["proposer"]) for e in own], [("forecast", "counsel"), ("forecast", "counsel"), ("proposal", "counsel")])
        self.assertEqual(own[0]["body"], {"claim": "first claim", "p": 600, "resolves_by": "2099-01-01T00:00:00Z",
                                          "type": "counsel.undertaking", "args": {"id": "u1", "window": "C2c-1"}})
        self.assertEqual(own[1]["body"], {"claim": "second claim", "p": 700, "resolves_by": "2099-01-02T00:00:00Z"})
        self.assertEqual(own[2]["body"], {"title": "counsel proposal title", "commit": work_sha})
        self.assertIn(f"proposal commit {work_sha}", r.stdout)

        r2 = self.trigger_sign("sign-1b", "counsel/ok")
        self.assertEqual((r2.returncode, self.remote_entries("counsel/ok")[base_len:]), (0, own))
        self.assertIn("already proposed, nothing signed", r2.stdout)

        self.make_counsel_branch("partial", [f1, f2, prop], extra_files={"transcripts/p.md": "p\n"})
        wt_partial = os.path.join(self.wt, "counsel", "partial")
        self.git("fetch", "-q", "origin")
        self.git("worktree", "add", "-q", "-b", "counsel/partial", wt_partial, "origin/counsel/partial")
        subprocess.run([os.path.join(wt_partial, "tools", "jack"), "--key", self.w.parties["counsel"].path,
                        "forecast", f1["claim"], "--p", str(f1["p"]), "--by", f1["by"], "--type", f1["type"], "--args", json.dumps(f1["args"])],
                       cwd=wt_partial, env=self.env, check=True, capture_output=True)
        r_part = self.trigger_sign("sign-part", "counsel/partial")
        self.assertEqual((r_part.returncode, [e["type"] for e in self.remote_entries("counsel/partial")[base_len:]]),
                         (0, ["forecast", "forecast", "proposal"]))

        marker = os.path.join(self.tmp.name, "ran_branch_tools")
        with open(os.path.join(ROOT, "tools", "jack"), encoding="utf-8") as f:
            bad_jack = f.read().replace("import argparse", f"open({marker!r}, 'w').write('boom')\nimport argparse", 1)
        self.make_counsel_branch("bad-tools", [prop], extra_files={"tools/jack": bad_jack})
        self.assertEqual(self.trigger_sign("sign-tools", "counsel/bad-tools").returncode, 1)
        self.assertFalse(os.path.exists(marker))
        self.assertEqual(self.remote_entries("counsel/bad-tools")[base_len:], [])

        self.make_counsel_branch("bad-link", [prop], symlinks={"transcripts/link.md": "README.md"})
        self.assertEqual(self.trigger_sign("sign-link", "counsel/bad-link").returncode, 1)
        self.assertEqual(self.remote_entries("counsel/bad-link")[base_len:], [])

        main_work = os.path.join(self.tmp.name, "main-edit")
        subprocess.run(["git", "clone", "-q", "-b", "main", self.origin, main_work], check=True, env=self.env)
        write_file(os.path.join(main_work, "transcripts", "requests", "merge-chg.jsonl"), json.dumps(prop) + "\n")
        self.git("add", "-A", cwd=main_work)
        self.git("commit", "-q", "-m", "seed request", "-m", "Proposer: guy guy-master", cwd=main_work)
        self.git("push", "-q", "origin", "main", cwd=main_work)
        branch_sha = self.make_counsel_branch("merge-chg", None, extra_files={"transcripts/m.md": "1\n"})
        write_file(os.path.join(main_work, "transcripts", "requests", "merge-chg.jsonl"),
                   json.dumps({"verb": "proposal", "title": "tampered by main"}) + "\n")
        self.git("add", "-A", cwd=main_work)
        self.git("commit", "-q", "-m", "main edits request", "-m", "Proposer: guy guy-master", cwd=main_work)
        self.git("push", "-q", "origin", "main", cwd=main_work)
        self.assertEqual(self.trigger_sign("sign-mchg", "counsel/merge-chg").returncode, 1)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=os.path.join(self.wt, "counsel", "merge-chg")), branch_sha)
        self.assertEqual(self.remote_entries("counsel/merge-chg")[base_len:], [])

        branch_sha = self.make_counsel_branch("merge-fail", [prop], extra_files={"transcripts/f.md": "1\n"})
        with open(os.path.join(ROOT, "tools", "jack"), encoding="utf-8") as f:
            failing_jack = f.read().replace("#!/usr/bin/env python3", "#!/usr/bin/env python3\nraise SystemExit(1)", 1)
        write_file(os.path.join(main_work, "tools", "jack"), failing_jack, 0o755)
        self.git("add", "tools/jack", cwd=main_work)
        self.git("commit", "-q", "-m", "main makes the verb fail", cwd=main_work)
        self.git("push", "-q", "origin", "main", cwd=main_work)
        self.assertEqual(self.trigger_sign("sign-mfail", "counsel/merge-fail").returncode, 1)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=os.path.join(self.wt, "counsel", "merge-fail")), branch_sha)

    def test_sign_empty_push_and_refusals(self):
        self.set_gh(added=["requests/act-only.json"])
        self.assertEqual(subprocess.run([sys.executable, SIGN_SCRIPT],
                                        env=dict(self.env, COUNSEL_GH_TOKEN="", COUNSEL_KEY="/no/key"), capture_output=True, text=True).returncode, 0)
        prop = {"verb": "proposal", "title": "t"}
        self.make_counsel_branch("wrong-identity", [prop])
        self.set_gh(added=["requests/sign-wrong-identity.json"],
                    contents={"requests/sign-wrong-identity.json": {"id": "sign-wrong-identity", "act": "sign", "branch": "counsel/wrong-identity"}},
                    login="not-counsel")
        self.assertEqual(subprocess.run([sys.executable, SIGN_SCRIPT], env=self.env, capture_output=True, text=True).returncode, 1)
        for idx, bad_lines in enumerate([
            [{"verb": "forecast", "claim": "c", "p": True, "by": "2099-01-01T00:00:00Z"}, {"verb": "proposal", "title": "t"}],
            [{"verb": "forecast", "claim": "c", "p": 500, "by": "2099-01-01T00:00:00Z", "type": 123}, {"verb": "proposal", "title": "t"}],
            [{"verb": "proposal", "title": "--help"}],
            [{"verb": "proposal", "title": "bad\x07title"}],
            [{"verb": "forecast", "claim": "c", "p": 500, "by": "2099-01-01T00:00:00Z"}],
        ]):
            self.make_counsel_branch(f"bad-{idx}", bad_lines)
            self.assertEqual(self.trigger_sign(f"sign-bad-{idx}", f"counsel/bad-{idx}").returncode, 1, idx)
            self.assertEqual(len(self.get_gh()["issues"].get("renavondata/opencode-runner", [])), 1, idx)
        f1, prop = {"verb": "forecast", "claim": "asked", "p": 600, "by": "2099-01-01T00:00:00Z"}, {"verb": "proposal", "title": "t"}
        self.make_counsel_branch("unasked", [prop], extra_files={"transcripts/u.md": "u\n"})
        wt_u = os.path.join(self.wt, "counsel", "unasked")
        self.git("fetch", "-q", "origin")
        self.git("worktree", "add", "-q", "-b", "counsel/unasked", wt_u, "origin/counsel/unasked")
        subprocess.run([os.path.join(wt_u, "tools", "jack"), "--key", self.w.parties["counsel"].path,
                        "forecast", f1["claim"], "--p", "600", "--by", f1["by"]], cwd=wt_u, env=self.env, check=True, capture_output=True)
        self.assertEqual(self.trigger_sign("sign-unasked", "counsel/unasked").returncode, 1)
        self.assertEqual([e["type"] for e in self.remote_entries("counsel/unasked")[-1:]], ["forecast"])

    def test_courier_refuses_a_token_not_owned_by_assize_reviewer(self):
        self.make_counsel_branch("wrong-identity", [{"verb": "proposal", "title": "t"}])
        self.set_gh(added=["requests/sign-wrong-identity.json"],
                    contents={"requests/sign-wrong-identity.json": {"id": "sign-wrong-identity", "act": "sign", "branch": "counsel/wrong-identity"}},
                    login="not-counsel")
        self.assertEqual(subprocess.run([sys.executable, SIGN_SCRIPT], env=self.env, capture_output=True, text=True).returncode, 1)
        self.set_gh(added=["requests/act-wrong-identity.json"],
                    contents={"requests/act-wrong-identity.json": {"id": "act-wrong-identity", "act": "issue", "title": "x", "body": "x"}},
                    login="not-counsel")
        self.assertEqual(subprocess.run([sys.executable, ACT_SCRIPT], env=self.env, capture_output=True, text=True).returncode, 1)

    def test_acts_job_pr_issue_template_and_close(self):
        self.set_gh(added=["requests/sign-1.json"])
        empty = subprocess.run([sys.executable, ACT_SCRIPT], env=dict(self.env, COUNSEL_GH_TOKEN=""), capture_output=True, text=True)
        self.assertEqual(empty.returncode, 0, empty.stdout + empty.stderr)
        self.set_gh(added=["requests/identity.json"], contents={"requests/identity.json": {"id": "identity", "act": "issue", "title": "T", "body": "B"}},
                    login="not-counsel")
        self.assertEqual(subprocess.run([sys.executable, ACT_SCRIPT], env=self.env, capture_output=True, text=True).returncode, 1)
        with open(ACT_SCRIPT, encoding="utf-8") as f:
            self.assertNotIn("COUNSEL_TRIGGER_REPO", f.read())
        tpl = "model: {MODEL}\nkey: ~/.ssh/jack-builder\nbranch: {BRANCH}\n\n# builder: build {TEXTS} on {BRANCH} at {NOW} ({STAMP}) for {WINDOW}\nBody.\n"
        win = {"window": "C2c-1", "frozen": {"paths": ["transcripts/runner/", "transcripts/windows/"]}}
        reqs = {
            "requests/01-pr-ok.json": {"id": "01-pr-ok", "act": "pr", "head": "counsel/foo", "title": "T", "body": "B"},
            "requests/02-pr-bad.json": {"id": "02-pr-bad", "act": "pr", "head": "builder-x", "title": "T", "body": "B"},
            "requests/03-issue-direct.json": {"id": "03-issue-direct", "act": "issue", "title": "Reader",
                                               "body": "hello", "labels": ["read"], "then_labels": ["run"]},
            "requests/04-issue-bkey.json": {"id": "04-issue-bkey", "act": "issue", "title": "Sneak", "body": "key: ~/.ssh/jack-builder\ndo this"},
            "requests/04-issue-rkey.json": {"id": "04-issue-rkey", "act": "issue", "title": "Sneak", "body": "key: ~/.ssh/jack-reviewer\ndo this"},
            "requests/05-tpl-ok.json": {"id": "05-tpl-ok", "act": "issue", "template": "build", "window": "C2c-1",
                                        "model": "google/gemini-4-argon", "branch": "builder-c2c-1-courier",
                                        "texts": "transcripts/runner/counsel-courier.md,transcripts/windows/C2c-1.json",
                                        "labels": ["build"], "then_labels": ["run"]},
            "requests/06-tpl-loose.json": {"id": "06-tpl-loose", "act": "issue", "template": "build", "window": "C2c-1",
                                           "model": "google/gemini-4-argon", "branch": "builder-x", "texts": "transcripts/UNFROZEN.md"},
            "requests/07-close-jack.json": {"id": "07-close-jack", "act": "close", "repo": "renavondata/jack", "number": 1, "stale": "superseded"},
            "requests/08-close-runner.json": {"id": "08-close-runner", "act": "close", "repo": "renavondata/opencode-runner", "number": 2, "stale": "done"},
            "requests/09-issue-dedup.json": {"id": "03-issue-direct", "act": "issue", "title": "Reader",
                                              "body": "hello", "labels": ["read"], "then_labels": ["run", "extra"]},
        }
        prs = [{"number": 1, "head": "counsel/old", "title": "Old", "body": "", "state": "open", "user": "assize-reviewer"}]
        issues = {"renavondata/jack": [{"number": 1, "state": "open", "user": {"login": "assize-reviewer"}, "pull_request": {}}]}
        self.set_gh(added=sorted(reqs), contents={**reqs, "transcripts/sessions/build.md": tpl, "transcripts/windows/C2c-1.json": win},
                    prs=prs, issues=issues)
        self.assertEqual(subprocess.run([sys.executable, ACT_SCRIPT], env=self.env, capture_output=True, text=True).returncode, 1)
        st = self.get_gh()
        self.assertEqual([p["head"] for p in st["prs"]], ["counsel/old", "counsel/foo"])
        self.assertEqual((st["issues"]["renavondata/jack"][0]["state"], st["comments"]),
                         ("closed", [{"repo": "renavondata/jack", "number": 1, "body": "stale: superseded"}]))
        runner_issues = st["issues"]["renavondata/opencode-runner"]
        direct_issue = next(i for i in runner_issues if i["title"] == "Reader")
        self.assertEqual((direct_issue["state"], {l["name"] for l in direct_issue["labels"]}), ("closed", {"read", "run", "extra"}))
        tpl_issue = next(i for i in runner_issues if "<!-- counsel-request: 05-tpl-ok -->" in i["body"])
        self.assertTrue(tpl_issue["title"].startswith("builder: build transcripts/runner/counsel-courier.md"))
        self.assertEqual({l["name"] for l in tpl_issue["labels"]}, {"build", "run"})
        self.assertEqual(len([i for i in runner_issues if i["title"].startswith("counsel-act:")]), 4)
    def test_host_installer_check_and_workflows(self):
        install_sh = os.path.join(ROOT, "tools", "runner", "host", "install.sh")
        check_sh = os.path.join(ROOT, "tools", "runner", "host", "check.sh")
        staged = (".ssh/jack-builder", ".ssh/jack-builder.pub", ".ssh/jack-reviewer", ".ssh/jack-reviewer.pub",
                  ".ssh/jack-herald", ".ssh/jack-herald.pub", ".ssh/jack-counsel-3", ".ssh/jack-counsel-3.pub",
                  ".ssh/deploy-jack", ".ssh/deploy-jack.pub", ".config/jack/app-id", ".config/jack/app.pem", ".config/jack/gh-counsel")
        write_file(os.path.join(self.stubs, "curl"), '#!/bin/sh\necho \'{"ssh_keys":["ssh-ed25519 AAAATESTKEY"]}\'\n', 0o755)

        def make_fixture(name):
            base = os.path.join(self.tmp.name, f"host-{name}")
            stg, old, root = (os.path.join(base, d) for d in ("staging", "old", "root"))
            for rel in staged:
                write_file(os.path.join(stg, rel), f"content:{rel}\n")
            subprocess.run(["git", "clone", "-q", self.origin, os.path.join(old, "git", "jack")], check=True, env=self.env)
            return stg, old, root

        def tree_files(d):
            return sorted(os.path.relpath(os.path.join(dp, fn), d) for dp, _, fns in os.walk(d) for fn in fns) if os.path.exists(d) else []

        # Twin 1: exact 13 staged files, checkout at origin -> 12 placed + .gitconfig + .ssh/config + .ssh/known_hosts
        stg1, old1, root1 = make_fixture("twin1")
        r1 = subprocess.run([install_sh, "--root", root1, "--staging", stg1, "--old-home", old1], env=self.env, capture_output=True, text=True)
        self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
        self.assertIn("MemoryMax=12G", r1.stdout)
        home1 = os.path.join(root1, "home", "jack-runner")
        want_placed = sorted([p for p in staged if p != ".ssh/deploy-jack.pub"] + [".gitconfig", ".ssh/config", ".ssh/known_hosts"])
        self.assertEqual(tree_files(home1), want_placed)
        self.assertEqual(tree_files(root1), [f"home/jack-runner/{p}" for p in want_placed])
        for rel in staged:
            if rel != ".ssh/deploy-jack.pub":
                self.assertEqual(os.stat(os.path.join(home1, rel)).st_mode & 0o777, 0o600)
        for cfg in (".ssh/config", ".ssh/known_hosts"):
            self.assertEqual(os.stat(os.path.join(home1, cfg)).st_mode & 0o777, 0o644)
        self.assertEqual(subprocess.run([install_sh, "--root", root1, "--staging", stg1, "--old-home", old1], env=self.env, capture_output=True, text=True).returncode, 0)

        # A completed root-mode install retains the known-host bytes on rerun.
        with open(os.path.join(home1, ".ssh", "known_hosts"), encoding="utf-8") as f:
            known_hosts = f.read()
        write_file(os.path.join(self.stubs, "curl"), '#!/bin/sh\necho \'{"ssh_keys":["ssh-ed25519 CHANGED"]}\'\n', 0o755)
        self.assertEqual(subprocess.run([install_sh, "--root", root1, "--staging", stg1, "--old-home", old1], env=self.env, capture_output=True, text=True).returncode, 0)
        with open(os.path.join(home1, ".ssh", "known_hosts"), encoding="utf-8") as f:
            self.assertEqual(f.read(), known_hosts)

        # The host keys must come from GitHub Meta; no embedded fallback is accepted.
        stg_meta, old_meta, root_meta = make_fixture("meta-failure")
        write_file(os.path.join(self.stubs, "curl"), "#!/bin/sh\nexit 1\n", 0o755)
        meta = subprocess.run([install_sh, "--root", root_meta, "--staging", stg_meta, "--old-home", old_meta], env=self.env, capture_output=True, text=True)
        self.assertNotEqual(meta.returncode, 0)
        self.assertIn("GitHub Meta", meta.stdout + meta.stderr)
        write_file(os.path.join(self.stubs, "curl"), '#!/bin/sh\necho \'{"ssh_keys":["ssh-ed25519 AAAATESTKEY"]}\'\n', 0o755)

        # Twin 2: hosts.yml added to staging -> stops with that name and writes nothing
        stg2, old2, root2 = make_fixture("twin2")
        write_file(os.path.join(stg2, "hosts.yml"), "oauth_token: secret\n")
        r2 = subprocess.run([install_sh, "--root", root2, "--staging", stg2, "--old-home", old2], env=self.env, capture_output=True, text=True)
        self.assertNotEqual(r2.returncode, 0)
        self.assertIn("hosts.yml", r2.stdout + r2.stderr)
        self.assertEqual(tree_files(root2), [])

        # Staged secrets are files, never symlinks to bytes outside the staging tree.
        stg_link, old_link, root_link = make_fixture("symlink")
        os.remove(os.path.join(stg_link, ".ssh", "jack-builder"))
        os.symlink(os.path.join(old_link, "git", "jack", "README.md"), os.path.join(stg_link, ".ssh", "jack-builder"))
        r_link = subprocess.run([install_sh, "--root", root_link, "--staging", stg_link, "--old-home", old_link], env=self.env, capture_output=True, text=True)
        self.assertNotEqual(r_link.returncode, 0)
        self.assertIn("symlink", r_link.stdout + r_link.stderr)
        self.assertEqual(tree_files(root_link), [])

        # Twin 3: jack-reviewer absent -> stops before any placement
        stg3, old3, root3 = make_fixture("twin3")
        os.remove(os.path.join(stg3, ".ssh/jack-reviewer"))
        r3 = subprocess.run([install_sh, "--root", root3, "--staging", stg3, "--old-home", old3], env=self.env, capture_output=True, text=True)
        self.assertNotEqual(r3.returncode, 0)
        self.assertEqual(tree_files(root3), [])

        # Twin 4: old checkout one commit ahead of origin -> stops
        stg4, old4, root4 = make_fixture("twin4")
        write_file(os.path.join(old4, "git", "jack", "README.md"), "ahead\n")
        self.git("add", "-A", cwd=os.path.join(old4, "git", "jack"))
        self.git("commit", "-q", "-m", "ahead", cwd=os.path.join(old4, "git", "jack"))
        r4 = subprocess.run([install_sh, "--root", root4, "--staging", stg4, "--old-home", old4], env=self.env, capture_output=True, text=True)
        self.assertNotEqual(r4.returncode, 0)
        self.assertEqual(tree_files(root4), [])

        # Runner.Worker running under old home -> stops
        stg5, old5, root5 = make_fixture("worker")
        worker_bin = os.path.join(old5, ".local", "share", "actions-runner-1", "bin", "Runner.Worker")
        write_file(worker_bin, "#!/bin/sh\nsleep 30\n", 0o755)
        proc = subprocess.Popen([worker_bin])
        try:
            r5 = subprocess.run([install_sh, "--root", root5, "--staging", stg5, "--old-home", old5], env=self.env, capture_output=True, text=True)
            self.assertNotEqual(r5.returncode, 0)
            self.assertEqual(tree_files(root5), [])
            # Mutant (d): Runner.Worker test deleted -> proceeds
            m_d = os.path.join(self.tmp.name, "install-md.sh")
            with open(install_sh, encoding="utf-8") as f:
                src = f.read()
            line_d = '! pgrep -f "$OLD/.local/share/actions-runner-[^/]*/bin/Runner.Worker" >/dev/null 2>&1 || { echo "refused: Runner.Worker is running under $OLD" >&2; exit 1; }\n'
            self.assertEqual(src.count(line_d), 1)
            write_file(m_d, src.replace(line_d, ""), 0o755)
            self.assertEqual(subprocess.run([m_d, "--root", root5, "--staging", stg5, "--old-home", old5], env=self.env, capture_output=True, text=True).returncode, 0)
        finally:
            proc.terminate()
            proc.wait()

        # Mutants (a), (b), (c): each a single line of install.sh deleted
        for idx, (find_line, stg_m, old_m, root_m, expected_file) in enumerate([
            ('for rel in $(find "$STAGING" -mindepth 1 -type f -printf \'%P\\n\' | sort); do case " $STAGED_FILES " in *" $rel "*) ;; *) echo "refused: unexpected staged file: $rel" >&2; exit 1 ;; esac; done\n',
             stg2, old2, root2, "home/jack-runner/hosts.yml"),
            ('for rel in $STAGED_FILES; do [ -f "$STAGING/$rel" ] && [ ! -L "$STAGING/$rel" ] || { echo "refused: missing staged file: $rel" >&2; exit 1; }; done\n',
             stg3, old3, root3, "home/jack-runner/.ssh/jack-builder"),
            ('ahead=$(git -C "$OLD/git/jack" for-each-ref --format=\'%(refname:short)\' refs/heads/ | while read -r b; do if [ -n "$(git -C "$OLD/git/jack" rev-list "origin/$b..$b" 2>/dev/null || git -C "$OLD/git/jack" rev-list "$b" --not --remotes=origin)" ]; then echo "$b"; fi; done); [ -z "$ahead" ] || { echo "refused: local branch ahead of origin: $ahead" >&2; exit 1; }\n',
             stg4, old4, root4, "home/jack-runner/.ssh/jack-builder"),
        ]):
            self.assertEqual(src.count(find_line), 1, idx)
            m_sh = os.path.join(self.tmp.name, f"install-m{idx}.sh")
            write_file(m_sh, src.replace(find_line, ""), 0o755)
            rm = subprocess.run([m_sh, "--root", root_m, "--staging", stg_m, "--old-home", old_m], env=self.env, capture_output=True, text=True)
            self.assertEqual(rm.returncode, 0, rm.stdout + rm.stderr)
            self.assertIn(expected_file, tree_files(root_m))

        # Check check.sh against passing and failing fixtures
        units = os.path.join(self.tmp.name, "units")
        write_file(os.path.join(units, "actions.runner.renavondata-opencode-runner.steel-1.service"), f"[Service]\nUser={os.environ.get('USER', 'g')}\n")
        subprocess.run(["git", "clone", "-q", self.origin, os.path.join(home1, "git", "jack")], check=True, env=self.env)
        write_file(os.path.join(old1, ".config", "gh", "hosts.yml"), "secret\n", 0o000)
        write_file(os.path.join(self.stubs, "gh"), "#!/bin/sh\nexit 1\n", 0o755)
        chk_env = dict(self.env, JACK_RUNNER_HOME=home1, JACK_OLD_HOME=old1, JACK_RUNNER_USER=os.environ.get("USER", "g"), JACK_UNITS_DIR=units)
        try:
            rc_ok = subprocess.run([check_sh], env=chk_env, capture_output=True, text=True)
            self.assertEqual(rc_ok.returncode, 0, rc_ok.stdout + rc_ok.stderr)
            self.assertNotIn("FAIL:", rc_ok.stdout)
            os.chmod(os.path.join(old1, ".config", "gh", "hosts.yml"), 0o644)
            rc_fail = subprocess.run([check_sh], env=chk_env, capture_output=True, text=True)
            self.assertEqual(rc_fail.returncode, 1)
            self.assertIn("FAIL:", rc_fail.stdout)
        finally:
            os.chmod(os.path.join(old1, ".config", "gh", "hosts.yml"), 0o600)

        # Workflow changes under tools/runner/host/workflows/
        for wf in ("run.yml", "diary.yml", "herald.yml", "repropose.yml"):
            with open(os.path.join(ROOT, "tools", "runner", "host", "workflows", wf), encoding="utf-8") as f:
                text = f.read()
            self.assertNotIn("identity: owner login", text)
            self.assertIn('echo "no identity: the App\'s files are absent"', text)
            if wf == "run.yml":
                self.assertLess(text.index('refused: no identity (the App\'s files are absent)'), text.index('started: run $GITHUB_RUN_ID'))


if __name__ == "__main__":
    unittest.main()
