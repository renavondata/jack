"""W5 rejecting witnesses and twins in isolated two-commit repositories."""
import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import due, status

T = "2026-11-03T06:00:00Z"
LATE = "2026-11-03T08:00:00Z"
ROW = dict(id="report", due=T, what="file report", done=None)
DONE = dict(id="report", done=dict(seq=7, what="filed"))
ENTRY = dict(seq=7, ts=T, body=dict(title="file report"))


class DueTest(unittest.TestCase):
    def repository(self, old, new, entries=(), inventory=None):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        def git(*args):
            return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                                   "-c", "commit.gpgsign=false", *args], cwd=root, capture_output=True,
                                  env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1"),
                                  text=True, check=True).stdout.strip()
        git("init", "-q"); (root / "transcripts").mkdir()
        for state in (old, new) + (() if inventory is None else (inventory,)):
            path = root / due.FILE
            if state is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(state if isinstance(state, bytes) else "".join(json.dumps(r) + "\n" for r in state).encode())
            (root / "log.jsonl").write_text("".join(json.dumps(e) + "\n" for e in entries))
            git("add", "."); git("commit", "--allow-empty", "-qm", "fixture")
        return str(root)

    def run_due(self, root, *args, now=LATE):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = due.main(["--root", root, "--as-of", now, *args])
        return code, out.getvalue()

    def test_w5_overdue_escalates(self):
        root = self.repository([ROW], [ROW])
        self.assertEqual(self.run_due(root), (0, f"W5 report due {T} file report: ESCALATED 2h past due\n"))
        self.assertTrue(self.run_due(root, now=T)[1].endswith(": OPEN\n"))
        (Path(root) / due.FILE).write_text("")
        self.assertIn("ESCALATED 2h past due", self.run_due(root)[1])
        self.assertEqual(self.run_due(self.repository(None, None)), (0, "W5: no COUNSEL-DUE file\n"))

    def test_w5_done_is_an_entry(self):
        entries = [ENTRY, dict(ENTRY, seq=8, body=dict(args=dict(id="other"))),
                   dict(ENTRY, seq=9, ts="2026-11-04T00:00:00Z"), dict(seq=10, ts=T)]
        for done in (7, dict(seq=8, what="report"), dict(seq=9, what="future"), dict(seq=10, what="no body"),
                     dict(seq=11, what="absent"), dict(seq=True, what="boolean")):
            root = self.repository([ROW], [ROW, dict(DONE, done=done)], entries)
            code, text = self.run_due(root)
            self.assertEqual(code, 2); self.assertIn("ESCALATED", text); self.assertIn("not an entry)", text)
            self.assertIn("malformed", text)
        for body in (ENTRY["body"], dict(args=dict(id="report"))):
            root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, body=body)])
            self.assertEqual(self.run_due(root), (0, f"W5 report due {T} file report: done seq 7 on time\n"))

    def test_w5_rows_append_only(self):
        completed = [ROW, DONE]
        raw = (json.dumps(ROW) + "\n").encode()
        for old, new in (([ROW], []), ([ROW], None), ([ROW], [dict(ROW, what="edited")]), ([ROW], [dict(ROW, due=LATE)]),
                         ([ROW], [dict(ROW, id="other")]), ([ROW], [dict(ROW, done=DONE["done"])]), (completed, [ROW]),
                         (completed, [ROW, dict(DONE, done=dict(seq=8, what="changed"))]),
                         (raw, b" " + raw), (raw, raw.replace(b"\n", b"\r\n")), (raw, raw.rstrip(b"\n"))):
            self.assertEqual(self.run_due(self.repository(old, new)), (2, "W5: rows changed: report\n"))
        root = self.repository([ROW], [ROW, dict(ROW, id="next")])
        self.assertEqual(self.run_due(root)[0], 0)
        self.assertIn("done seq 7 on time", self.run_due(self.repository([ROW], completed, [ENTRY]))[1])

    def test_malformed_discharge_lines(self):
        for new in ([DONE], [DONE, ROW], [ROW, DONE, DONE], [ROW, ROW], [dict(ROW, done=DONE["done"])],
                    [ROW, dict(DONE, done=None)], [ROW, dict(DONE, id="unknown")]):
            self.assertEqual(self.run_due(self.repository([], new, [ENTRY])), (2, "W5: malformed COUNSEL-DUE file\n"))

    def test_w5_inventory(self):
        root = self.repository([], [], inventory=[ROW])
        self.assertEqual(self.run_due(root, "--rev", "HEAD~1", "--inventory", "HEAD"), (2, "W5: missing report\n"))
        self.assertEqual(self.run_due(root, "--inventory", "HEAD")[0], 0)
        root = self.repository([ROW], [ROW, dict(ROW, id="next")])
        self.assertEqual(self.run_due(root, "--inventory", "HEAD~1")[0], 0)

    def test_w5_escalation_history(self):
        for ts, expected in ((LATE, "ESCALATED 2h late"), (T, "on time")):
            root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, ts=ts)])
            for now in (LATE, "2026-11-05T00:00:00Z"):
                self.assertEqual(self.run_due(root, now=now), (0, f"W5 report due {T} file report: done seq 7 {expected}\n"))

    def test_status_prints_w5_after_clerk_and_forwards_inventory(self):
        es = [dict(seq=0, type="genesis", ts=T, body={"keys": [{"principal": "guy"}]})]
        s = dict(subject="C2a", end=LATE, checks=[(False, "short")], overdue=[])
        root = self.repository([], [ROW])
        for rev, expected in (("HEAD", 0), ("HEAD~1", 2)):
            context = dict(root=root, rev=rev, es=es, runs=[])
            with patch.object(status, "inputs", return_value=context), patch.object(status, "report", return_value=s), \
                    patch.object(status, "render", return_value="status"), contextlib.redirect_stdout(io.StringIO()) as out:
                code = status.main(["--root", root, "--as-of", LATE, "--inventory", "HEAD"])
            text = out.getvalue()
            self.assertEqual(code, expected)
            self.assertLess(text.index("W4 short"), text.index("W5"))
            self.assertTrue(text.endswith("W5: missing report\n") if expected else "ESCALATED 2h past due" in text)
