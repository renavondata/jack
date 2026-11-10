"""W5 rejecting witnesses and twins in isolated repositories with merge evidence."""
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
EARLY, CITED, MERGED = (f"2026-11-03T{h}:00:00Z" for h in ("02", "04", "05"))
ROW = dict(id="report", due=T, what="file report", done=None)
DONE = dict(id="report", done=dict(seq=7, what="filed"))
ENTRY = dict(seq=7, ts=T, body=dict(title="file report"))


class DueTest(unittest.TestCase):
    def repository(self, old, new, entries=(), inventory=None, merges=None):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        def git(*args):
            return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                                   "-c", "commit.gpgsign=false", *args], cwd=root, capture_output=True,
                                  env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1"),
                                  text=True, check=True).stdout.strip()
        git("init", "-q"); (root / "transcripts").mkdir()
        commits = []
        for state in (old, new) + (() if inventory is None else (inventory,)):
            path = root / due.FILE
            if state is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(state if isinstance(state, bytes) else "".join(json.dumps(r) + "\n" for r in state).encode())
            (root / "log.jsonl").write_text("".join(json.dumps(e) + "\n" for e in entries))
            git("add", "."); git("commit", "--allow-empty", "-qm", "fixture")
            commits.append(git("rev-parse", "HEAD"))
        if entries or merges is not None:
            if merges is None:
                merges = [(max(e["seq"] for e in entries) + 1, max(e["ts"] for e in entries), 1)]
            entries = sorted(list(entries) + [dict(seq=seq, ts=ts, type="merge", body=dict(
                commit=commits[ref] if type(ref) is int else ref)) for seq, ts, ref in merges], key=lambda e: e["seq"])
            (root / "log.jsonl").write_text("".join(json.dumps(e) + "\n" for e in entries))
            git("add", "."); git("commit", "--allow-empty", "-qm", "merge witnesses")
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

    def test_w5_redate(self):
        originals = [dict(ROW, id=key, due="2026-11-18T00:00:00Z") for key in ("c2b-report", "c2c-brief")]
        redates = [dict(id=row["id"], due=when, seq=1564, why="sovereign direction") for row, when in
                   zip(originals, ("2026-12-02T12:00:00Z", "2026-11-16T00:00:00Z"))]
        discharge = dict(DONE, id="c2b-report")
        entries = [dict(ENTRY, body=dict(title="c2b-report c2c-brief"))]
        for initial, appended in ((originals, redates), ([originals[0]], [redates[0]]),
                                  ([originals[1]], [redates[1]]), (originals, redates + [discharge])):
            code, text = self.run_due(self.repository(initial, initial + appended, entries))
            self.assertEqual(code, 0)
            for row in appended:
                if "due" in row:
                    self.assertIn(f"W5 {row['id']} due {row['due']} ", text)
                else:
                    self.assertIn("done seq 7 on time", text)
        bad = [originals + [dict(ROW, id="runbook-c2b"), dict(redates[0], id="runbook-c2b")],
               originals + [dict(redates[0], due="2026-12-01T00:00:00Z")],
               originals + redates + [redates[0]], originals + [dict(redates[0], seq=1565)],
               [redates[0]] + originals, originals + [discharge, redates[0]]]
        bad += [originals + [dict(redates[0], **change)] for change in
                ({"why": None}, {"why": 1}, {"seq": "1564"}, {"seq": 1564.0}, {"seq": True},
                 {"due": None}, {"extra": "key"})]
        bad += [originals + [{k: v for k, v in redates[0].items() if k != missing}] for missing in redates[0]]
        for records in bad:
            with self.subTest(records=records):
                self.assertEqual(self.run_due(self.repository([], records, entries)),
                                 (2, "W5: malformed COUNSEL-DUE file\n"))

    def test_w5_escalation_history(self):
        cases = [(CITED, [(8, MERGED, 1)], "done seq 7 on time"),
                 (CITED, [(8, LATE, 1)], "done seq 7 ESCALATED 2h late"),
                 (LATE, [(6, MERGED, 1)], None),
                 (CITED, [(8, MERGED, 1), (9, LATE, 1)], "done seq 7 on time"),
                 (CITED, [], None), (CITED, [(8, T, 1)], "done seq 7 on time"),
                 (T, [(6, MERGED, 1)], None)]
        for ts, merges, expected in cases:
            root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, ts=ts)], merges=[(0, EARLY, 0)] + merges)
            for now in (LATE, "2026-11-05T00:00:00Z"):
                state = (expected if any(seq > 7 and merged_at < now for seq, merged_at, _ in merges) else
                         f"ESCALATED {(due.instant(now) - due.instant(T)).total_seconds() / 3600:g}h past due")
                self.assertEqual(self.run_due(root, now=now), (0, f"W5 report due {T} file report: {state}\n"), (ts, merges, now))
        root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, ts=CITED)], merges=[(0, EARLY, 0), (8, MERGED, 1)])
        self.assertEqual(self.run_due(root, now="2026-11-03T04:30:00Z"), (0, f"W5 report due {T} file report: OPEN\n"))
        # Equal timestamps do not put a later sequence's merge on an earlier prefix (F8).
        root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, ts=CITED), dict(seq=8, ts=MERGED)],
                               merges=[(0, EARLY, 0), (9, MERGED, 1)])
        text, entries = due.blob(root, "HEAD", due.FILE), due.rows(due.blob(root, "HEAD", "log.jsonl"))
        self.assertEqual(due.project(root, text, entries[:-1], MERGED), ([f"W5 report due {T} file report: OPEN"], False))
        self.assertEqual(due.project(root, text, entries, MERGED), ([f"W5 report due {T} file report: OPEN"], False))
        # Same parsed discharge, different bytes: whitespace, key order, escapes, line ending.
        raw = (json.dumps(ROW) + "\n").encode()
        for line in (" " + json.dumps(DONE) + "\n", json.dumps(DONE, sort_keys=True) + "\n",
                     json.dumps(DONE).replace("report", r"\u0072eport") + "\n", json.dumps(DONE) + "\r\n"):
            root = self.repository([ROW], raw + line.encode(), [dict(ENTRY, ts=CITED)], inventory=[ROW, DONE],
                                   merges=[(0, EARLY, 0), (8, MERGED, 1)])
            self.assertEqual(due.project(root, due.blob(root, "HEAD", due.FILE),
                                        due.rows(due.blob(root, "HEAD", "log.jsonl")), LATE),
                             ([f"W5 report due {T} file report: ESCALATED 2h past due"], False))

    def test_unreadable_merge_is_unverified(self):
        for merges in ([(8, MERGED, "0" * 40)], [(8, MERGED, "0" * 40), (9, T, 1)]):
            root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, ts=CITED)], merges=merges)
            code, text = self.run_due(root)
            self.assertEqual(code, 2); self.assertIn("unverified merge", text); self.assertNotIn("done seq", text)
        root = self.repository([ROW], [ROW, DONE], [dict(ENTRY, ts=CITED)],
                               inventory=[ROW, DONE, dict(ROW, id="next")], merges=[(8, MERGED, 1)])
        commit = due.rows(due.blob(root, "HEAD", "log.jsonl"))[-1]["body"]["commit"]
        oid = subprocess.run(["git", "-C", root, "rev-parse", f"{commit}:{due.FILE}"],
                             capture_output=True, text=True, check=True).stdout.strip()
        (Path(root) / ".git" / "objects" / oid[:2] / oid[2:]).unlink()
        code, text = self.run_due(root)
        self.assertEqual(code, 2); self.assertIn("unverified merge", text)
        root = self.repository(None, [ROW, DONE], [dict(ENTRY, ts=CITED)], merges=[(0, EARLY, 0)])
        self.assertEqual(self.run_due(root), (0, f"W5 report due {T} file report: ESCALATED 2h past due\n"))

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
