"""tools/entry.py: prepare on the log's head, sign with ssh-keygen, assemble only what the kernel admits."""
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest

from harness import build
from kernel import check, log

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "entry.py")
PUSH = {"digest": "bb" * 32, "review": "0" * 64}


def tool(*args, cwd=ROOT):
    return subprocess.run([sys.executable, TOOL, *args], capture_output=True, text=True, cwd=cwd)


def prepare(key, out, type_="push", body=PUSH, ts=build.TS, proposer="guy", log_path=None):
    args = ["prepare", "--type", type_, "--proposer", proposer, "--ts", ts,
            "--body-json", body if isinstance(body, str) else json.dumps(body), "--pubkey", key.path + ".pub", "--out", out]
    return tool(*args, *(["--log", log_path] if log_path else []))


def printed(stdout, prefix):
    """The one printed command line starting with prefix, as argv."""
    return shlex.split(next(l.strip() for l in stdout.splitlines() if l.strip().startswith(prefix)))


def sign(stdout):
    r = subprocess.run(printed(stdout, "ssh-keygen "), capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


class Entry(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="entry space ")
        self.w = build.World(self.tmp.name)
        self.lg = self.w.log()
        self.path = os.path.join(self.tmp.name, "log.jsonl")
        self.write(self.lg.text())
        self.out = os.path.join(self.tmp.name, "entry unsigned")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        with open(self.path, "w") as f:
            f.write(text)

    def assemble(self, *extra):
        return tool("assemble", self.out, self.out + ".sig", "--log", self.path, *extra)

    def test_prepare_sign_assemble_current_head(self):
        for type_, body in (
            ("decision", {"kind": "transmute", "subject": "A2"}),
            ("amend", {"id": "A2", "charter": "aa" * 32, "activate_at": 3}),
            ("push", PUSH),
            ("spec_conflict", {"section": "5", "text": "disagreement", "extra.key": "é"}),
        ):
            with self.subTest(type=type_):
                # Both permitted file endings produce the same next parent.
                self.write(self.lg.text().rstrip("\n") if type_ == "push" else self.lg.text())
                r = prepare(self.w.guy, self.out, type_, body, log_path=self.path)
                self.assertEqual(r.returncode, 0, r.stderr)
                with open(self.out) as f:
                    message = f.read()
                entry = json.loads(message)
                self.assertEqual(message, log.canonical(entry))
                self.assertEqual(entry, dict(seq=len(self.lg.lines), parent=self.lg.head, type=type_, body=body, ts=build.TS, proposer="guy"))
                self.assertEqual(printed(r.stdout, "ssh-keygen "),
                                 ["ssh-keygen", "-Y", "sign", "-f", self.w.guy.path, "-n", "core-entry", self.out])
                self.assertEqual(printed(r.stdout, "python3 tools/entry.py assemble"),
                                 ["python3", "tools/entry.py", "assemble", self.out, self.out + ".sig", "--log", self.path, ">>", self.path])
                sign(r.stdout)
                a = self.assemble()
                self.assertEqual((a.returncode, a.stderr), (0, ""))
                line = a.stdout.rstrip("\n")
                self.assertEqual(a.stdout, line + "\n")
                self.assertEqual(log.canonical(json.loads(line)), line)
                self.lg.lines.append(line)
                self.assertEqual(check.check(self.lg.lines), {"ok": True, "entries": len(self.lg.lines)})
                os.remove(self.out + ".sig")

    def test_log_defaults_to_the_repository_root(self):
        with open(os.path.join(ROOT, "log.jsonl"), "rb") as f:
            lines = check.read_lines(f.read())
        if not lines:
            self.skipTest("the repository's log.jsonl is empty")
        r = prepare(self.w.guy, self.out)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.out) as f:
            entry = json.loads(f.read())
        self.assertEqual((entry["seq"], entry["parent"]), (len(lines), log.line_hash(lines[-1])))
        self.assertEqual(printed(r.stdout, "python3 tools/entry.py assemble"),
                         ["python3", "tools/entry.py", "assemble", self.out, self.out + ".sig", ">>", os.path.join(ROOT, "log.jsonl")])
        a = tool("assemble", self.out, os.path.join(self.tmp.name, "absent.sig"))
        self.assertEqual((a.returncode, a.stdout), (2, ""))

    def test_prepare_refusals_exit_2_and_write_nothing(self):
        cases = {
            "empty log": dict(log_path=os.path.join(self.tmp.name, "empty.jsonl")),
            "missing log": dict(log_path=os.path.join(self.tmp.name, "absent.jsonl")),
            "impossible date": dict(ts="2026-02-29T00:00:00Z"),
            "not a timestamp": dict(ts="2026-10-14 09:00:00"),
            "not JSON": dict(body="{digest"),
            "not an object": dict(body="[]"),
            "unknown type": dict(type_="wish"),
            "non-integer number": dict(body={"digest": "bb" * 32, "review": "0" * 64, "x": 1.5}),
            "body schema": dict(body={"digest": "bad", "review": "0" * 64}),
        }
        with open(cases["empty log"]["log_path"], "w"):
            pass
        for name, kw in cases.items():
            with self.subTest(name):
                r = prepare(self.w.guy, self.out, **dict(dict(log_path=self.path), **kw))
                self.assertEqual((r.returncode, r.stdout), (2, ""), r.stderr)
                self.assertTrue(r.stderr.strip())
                self.assertFalse(os.path.exists(self.out))

    def test_assemble_refused_by_the_kernel_exits_1_and_prints_nothing(self):
        # ann holds no `push` power: signed, but no_power.
        r = prepare(self.w.ann, self.out, proposer="ann", log_path=self.path)
        self.assertEqual(r.returncode, 0, r.stderr)
        sign(r.stdout)
        a = self.assemble()
        self.assertEqual((a.returncode, a.stdout), (1, ""))
        self.assertEqual({k: v for k, v in json.loads(a.stderr).items() if k != "detail"}, {"ok": False, "seq": 1, "reason": "no_power"})
        # The last key holding `key` drops it: bad_key.
        os.remove(self.out + ".sig")
        drop = build.decl("guy-master", "guy", self.w.guy, [t for t in build.ALL if t != "key"])
        r = prepare(self.w.guy, self.out, "key", drop, log_path=self.path)
        self.assertEqual(r.returncode, 0, r.stderr)
        sign(r.stdout)
        a = self.assemble()
        self.assertEqual((a.returncode, a.stdout, json.loads(a.stderr)["reason"]), (1, "", "bad_key"))
        # The log moved on after prepare: the prepared entry's parent is stale.
        os.remove(self.out + ".sig")
        r = prepare(self.w.guy, self.out, log_path=self.path)
        sign(r.stdout)
        self.lg.add("proposal", "ann", build.proposal(), self.w.ann)
        self.write(self.lg.text())
        a = self.assemble()
        self.assertEqual((a.returncode, a.stdout, json.loads(a.stderr)["seq"]), (1, "", 2))

    def test_assemble_without_its_files_exits_2(self):
        r = prepare(self.w.guy, self.out, log_path=self.path)
        self.assertEqual(r.returncode, 0, r.stderr)
        a = self.assemble()  # not signed yet
        self.assertEqual((a.returncode, a.stdout), (2, ""))
        sign(r.stdout)
        a = tool("assemble", self.out, self.out + ".sig", "--log", os.path.join(self.tmp.name, "absent.jsonl"))
        self.assertEqual((a.returncode, a.stdout), (2, ""))


if __name__ == "__main__":
    unittest.main()
