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


class DueTest(unittest.TestCase):
    def repository(self, old, new, entries=()):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        def git(*args):
            return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                                   "-c", "commit.gpgsign=false", *args], cwd=root, capture_output=True,
                                  env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1"),
                                  text=True, check=True).stdout.strip()
        git("init", "-q"); (root / "transcripts").mkdir()
        for state in (old, new):
            path = root / due.FILE
            if state is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text("".join(json.dumps(r) + "\n" for r in state))
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
        entries = [dict(seq=7, ts=T)]
        for done in (7, dict(seq=8, what="filed"), dict(seq=9, what="future")):
            # A bare integer also violates the only permitted row transition.
            root = self.repository([ROW] if isinstance(done, dict) else [], [dict(ROW, done=done)],
                                   entries + [dict(seq=9, ts="2026-11-04T00:00:00Z")])
            code, text = self.run_due(root)
            self.assertEqual(code, 2); self.assertIn("ESCALATED", text); self.assertIn("not an entry)", text)
            self.assertIn("malformed", text)
        root = self.repository([ROW], [dict(ROW, done=dict(seq=7, what="filed"))], entries)
        self.assertEqual(self.run_due(root), (0, f"W5 report due {T} file report: done seq 7 on time\n"))

    def test_w5_rows_append_only(self):
        completed = dict(ROW, done=dict(seq=7, what="filed"))
        for old, new in (([ROW], []), ([ROW], None), ([ROW], [dict(ROW, what="edited")]), ([ROW], [dict(ROW, due=LATE)]),
                         ([ROW], [dict(ROW, id="other")]), ([completed], [ROW]),
                         ([completed], [dict(ROW, done=dict(seq=8, what="changed"))])):
            self.assertEqual(self.run_due(self.repository(old, new)), (2, "W5: rows changed: report\n"))
        root = self.repository([ROW], [ROW, dict(ROW, id="next")])
        self.assertEqual(self.run_due(root)[0], 0)

    def test_w5_inventory(self):
        root = self.repository([ROW], [])
        self.assertEqual(self.run_due(root, "--inventory", "HEAD~1"), (2, "W5: missing report\n"))
        self.assertEqual(self.run_due(root, "--rev", "HEAD~1", "--inventory", "HEAD~1")[0], 0)
        root = self.repository([ROW], [ROW, dict(ROW, id="next")])
        self.assertEqual(self.run_due(root, "--inventory", "HEAD~1")[0], 0)

    def test_w5_escalation_history(self):
        for ts, expected in ((LATE, "ESCALATED 2h late"), (T, "on time")):
            root = self.repository([ROW], [dict(ROW, done=dict(seq=7, what="filed"))], [dict(seq=7, ts=ts)])
            for now in (LATE, "2026-11-05T00:00:00Z"):
                self.assertEqual(self.run_due(root, now=now), (0, f"W5 report due {T} file report: done seq 7 {expected}\n"))

    def test_status_prints_w5_after_clerk_and_forwards_inventory(self):
        es = [dict(seq=0, type="genesis", ts=T, body={"keys": [{"principal": "guy"}]})]
        s = dict(subject="C2a", end=LATE, checks=[(False, "short")], overdue=[])
        for new, expected in (([ROW], 0), ([], 2)):
            root = self.repository([ROW], new)
            context = dict(root=root, rev="HEAD", es=es, runs=[])
            with patch.object(status, "inputs", return_value=context), patch.object(status, "report", return_value=s), \
                    patch.object(status, "render", return_value="status"), contextlib.redirect_stdout(io.StringIO()) as out:
                code = status.main(["--root", root, "--as-of", LATE, "--inventory", "HEAD~1"])
            text = out.getvalue()
            self.assertEqual(code, expected)
            self.assertLess(text.index("W4 short"), text.index("W5"))
            self.assertTrue(text.endswith("W5: missing report\n") if expected else "ESCALATED 2h past due" in text)
