"""tools/genesis.py and tools/digest.py: Guy's signing procedure, end to end with a throwaway key."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

from harness import keys
from judge import judge
from kernel import check, log

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def tool(name, *args):
    return subprocess.run([PY, os.path.join(ROOT, "tools", name), *args], capture_output=True, text=True, cwd=ROOT)


class Digest(unittest.TestCase):
    def test_matches_the_judge_on_the_working_tree(self):
        r = tool("digest.py")
        self.assertEqual(r.returncode, 0, r.stderr)
        head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
        clean = subprocess.run(["git", "status", "--porcelain", "--", "kernel", "kernel2", "judge", ".github/workflows", "SPEC.md"],
                               capture_output=True, text=True, cwd=ROOT).stdout.strip()
        if clean:
            self.skipTest("trusted base has uncommitted changes; cannot compare with the judge's git-derived digest")
        self.assertEqual(r.stdout.strip(), judge.digest(ROOT, head))


    def test_refuses_a_tree_holding_a_foreign_object(self):
        """SPEC §10.1: a symbolic link or submodule in the trusted base is named, exit 2, no digest printed."""
        from harness import gitfix
        for kind, rel, target in (("link", "SPEC.md", "README.md"), ("present", "kernel/vendor", None),
                                  ("absent", "kernel/vendor", None), ("file", "kernel/vendor", None)):
            with tempfile.TemporaryDirectory() as tmp:
                gitfix.git(tmp, "init", "-q")
                for rel_ in ("tools/digest.py", "judge/__init__.py", "judge/judge.py", "kernel/check.py", "SPEC.md"):
                    gitfix.write(tmp, rel_, open(os.path.join(ROOT, rel_), "rb").read())
                gitfix.write(tmp, "README.md", "readme\n")
                gitfix.git(tmp, "add", "-A")
                gitfix.place(tmp, kind, rel, target)
                gitfix.git(tmp, "add", "-A")
                r = subprocess.run([PY, os.path.join(tmp, "tools", "digest.py")], capture_output=True, text=True, cwd=tmp)
                if kind == "file":
                    self.assertEqual((r.returncode, len(r.stdout.strip())), (0, 64), r.stderr)
                    continue
                self.assertEqual(r.returncode, 2, (kind, r.stdout, r.stderr))
                self.assertIn(rel, r.stderr)
                self.assertEqual(r.stdout, "")


class Genesis(unittest.TestCase):
    def test_prepare_sign_assemble_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = keys.make_key(tmp, "guy")
            unsigned = os.path.join(tmp, "genesis.unsigned")
            r = tool("genesis.py", "prepare", "--pubkey", key.path + ".pub", "--ts", "2026-10-14T09:00:00Z", "--out", unsigned)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("ssh-keygen -Y sign -f", r.stdout)
            self.assertIn("-n core-entry", r.stdout)
            with open(unsigned) as f:
                message = f.read()
            e = json.loads(message)
            self.assertEqual(log.canonical(e), message)
            self.assertEqual((e["seq"], e["parent"], e["type"], e["proposer"]), (0, "0" * 64, "genesis", "guy"))
            with open(os.path.join(ROOT, "CHARTER.md"), "rb") as f:
                self.assertEqual(e["body"]["charter"], hashlib.sha256(f.read()).hexdigest())
            self.assertEqual(e["body"]["checker"], tool("digest.py").stdout.strip())
            self.assertEqual(e["body"]["keys"][0]["pubkey"], key.pubkey)
            sig = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", key.path, "-n", "core-entry", unsigned],
                                 capture_output=True, text=True)
            self.assertEqual(sig.returncode, 0, sig.stderr)
            r = tool("genesis.py", "assemble", unsigned, unsigned + ".sig")
            self.assertEqual(r.returncode, 0, r.stderr)
            line = r.stdout.rstrip("\n")
            self.assertEqual(check.check([line]), {"ok": True, "entries": 1})
            self.assertEqual(e["body"]["keys"][0]["powers"], ["genesis", "key", "proposal", "merge"])

    def test_hardware_key_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            pub = os.path.join(tmp, "sk.pub")
            with open(pub, "w") as f:
                f.write("sk-ssh-ed25519@openssh.com AAAAGnNrLXNzaC1lZDI1NTE5QG9wZW5zc2guY29tAAAAIAAA guy@laptop\n")
            r = tool("genesis.py", "prepare", "--pubkey", pub, "--ts", "2026-10-14T09:00:00Z", "--out", os.path.join(tmp, "g"))
            self.assertEqual(r.returncode, 3)
            self.assertIn("stop", r.stderr.lower())

    def test_template_has_placeholders(self):
        with open(os.path.join(ROOT, "genesis.template.json")) as f:
            t = f.read()
        for ph in ("<<GUY_SSH_PUBLIC_KEY>>", "<<CHARTER_SHA256>>", "<<KERNEL_DIGEST>>", "<<TS>>"):
            self.assertIn(ph, t)
        self.assertIn("ssh-keygen -Y sign", t)


if __name__ == "__main__":
    unittest.main()
