"""The non-kernel entry signing procedure, including the exact printed command."""
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


class Entry(unittest.TestCase):
    def test_prepare_sign_assemble_current_head(self):
        with tempfile.TemporaryDirectory(prefix="entry space ") as tmp:
            w = build.World(tmp)
            lg = w.log()
            path = os.path.join(tmp, "log.jsonl")
            unsigned = os.path.join(tmp, "entry unsigned")
            for type_, body in (
                ("decision", {"kind": "transmute", "subject": "A2"}),
                ("amend", {"id": "A2", "charter": "aa" * 32, "activate_at": 3}),
                ("push", {"digest": "bb" * 32, "review": "0" * 64}),
                ("spec_conflict", {"section": "5", "text": "disagreement", "extra.key": "é"}),
            ):
                with self.subTest(type=type_):
                    # Both permitted file endings produce the same next parent.
                    with open(path, "w") as f:
                        f.write(lg.text().rstrip("\n") if type_ == "push" else lg.text())
                    r = subprocess.run([sys.executable, TOOL, "prepare", "--type", type_, "--body-json", json.dumps(body),
                                        "--pubkey", w.guy.path + ".pub", "--proposer", "guy", "--ts", build.TS,
                                        "--out", unsigned], cwd=tmp, capture_output=True, text=True)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    with open(unsigned) as f:
                        message = f.read()
                    entry = json.loads(message)
                    self.assertEqual(message, log.canonical(entry))
                    self.assertEqual(entry, dict(seq=len(lg.lines), parent=lg.head, type=type_, body=body, ts=build.TS, proposer="guy"))
                    command = next(line.strip() for line in r.stdout.splitlines() if line.strip().startswith("ssh-keygen "))
                    self.assertEqual(shlex.split(command), ["ssh-keygen", "-Y", "sign", "-f", w.guy.path, "-n", "core-entry", unsigned])
                    signed = subprocess.run(shlex.split(command), capture_output=True, text=True)
                    self.assertEqual(signed.returncode, 0, signed.stderr)
                    assembled = subprocess.run([sys.executable, TOOL, "assemble", unsigned, unsigned + ".sig"], capture_output=True, text=True)
                    self.assertEqual(assembled.returncode, 0, assembled.stderr)
                    line = assembled.stdout.rstrip("\n")
                    self.assertEqual(log.canonical(json.loads(line)), line)
                    lg.lines.append(line)
                    self.assertEqual(check.check(lg.lines), {"ok": True, "entries": len(lg.lines)})
                    os.remove(unsigned + ".sig")

    def test_bad_body_or_timestamp_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = build.World(tmp)
            path = os.path.join(tmp, "log.jsonl")
            with open(path, "w") as f:
                f.write(w.log().text())
            out = os.path.join(tmp, "unsigned")
            for body, ts in (("[]", build.TS), ('{"digest":"bad"}', build.TS),
                             ('{"digest":"' + "0" * 64 + '","review":"' + "0" * 64 + '"}', "2026-02-29T00:00:00Z")):
                r = subprocess.run([sys.executable, TOOL, "prepare", "--type", "push", "--body-json", body,
                                    "--pubkey", w.guy.path + ".pub", "--proposer", "guy", "--ts", ts, "--log", path,
                                    "--out", out], capture_output=True, text=True)
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertFalse(os.path.exists(out))
