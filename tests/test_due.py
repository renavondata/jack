"""W5's fold and effective discharges in real committed histories."""
import contextlib
import io
import json
import unittest

from harness.gitfix import git
from tests.clerk_fixture import SignedFixture, commit, tree
from tools import due


def lines(*rows):
    return b"".join((json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode() for row in rows)


def row(rid="task", by="2026-11-03T12:00:00Z"):
    return dict(id=rid, due=by, what="deliver it", done=None)


def discharge(rid="task", seq=1):
    return dict(id=rid, done=dict(seq=seq, what="delivered"))


class DueTest(unittest.TestCase):
    def test_render_boundary_and_late_history_never_clears(self):
        data = lines(row(), discharge())
        with tree({due.PATH: data}) as (root, sha):
            early, by, late = "2026-11-03T11:00:00Z", "2026-11-03T12:00:00Z", "2026-11-03T13:00:00Z"
            cite = dict(seq=1, ts=early, type="proposal", body=dict(title="task"))
            merge = dict(seq=2, ts=late, type="merge", body=dict(commit=sha))
            text = lambda es, at: due.render(due.assess(root, sha, es, at))
            self.assertTrue(text([], by).endswith(": OPEN"))
            self.assertTrue(text([], late).endswith(": ESCALATED 1.00h past due"))
            self.assertTrue(text([cite, merge], late).endswith(": done seq 1 ESCALATED 1.00h late"))
            self.assertEqual(text([cite, merge], late), text([cite, merge], "2026-12-01T00:00:00Z"))
            self.assertTrue(text([cite, dict(merge, ts=by)], late).endswith(": done seq 1 on time"))
            self.assertEqual(due.render(None), "W5: no COUNSEL-DUE file")

    def test_append_only_checks_deleted_and_restored_history_and_seed_inventory(self):
        data = lines(row())
        with tree({due.PATH: data}) as (root, seed):
            sha = commit(root, {due.PATH: data + lines(row("another"))})
            due.inventory_check(root, sha, due.file_at(root, sha), seed)
            for bad in (b"", lines(dict(row(), what="rewritten")), lines(row("another"))):
                with self.subTest(data=bad), self.assertRaisesRegex(ValueError, "append-only|missing"):
                    due.inventory_check(root, sha, bad, seed)
            # An inventory from another tree is still a binding list, not hardcoded eleven ids.
            inventory = commit(root, {due.PATH: data + lines(row("seeded-later"))})
            with self.assertRaisesRegex(ValueError, "missing seeded-later"):
                due.inventory_check(root, seed, data, inventory)
            deleted = commit(root, {due.PATH: b""})
            restored = commit(root, {due.PATH: due.file_at(root, inventory)})
            for rev in (deleted, restored):
                with self.subTest(rev=rev), self.assertRaisesRegex(ValueError, "append-only"):
                    due.inventory_check(root, rev, due.file_at(root, rev))
            git(root, "rm", due.PATH)
            with self.assertRaisesRegex(ValueError, "append-only"):
                due.inventory_check(root, seed, due.file_at(root, None))

    def test_done_requires_an_entry_on_prefix_naming_the_id_in_its_body(self):
        early, late = "2026-11-03T11:00:00Z", "2026-11-03T13:00:00Z"
        with tree({due.PATH: lines(row(), discharge())}) as (root, sha):
            merge = dict(seq=2, ts=early, type="merge", body=dict(commit=sha))
            for body, ts, done in [(dict(title="unrelated"), early, None),
                                   (dict(title="task delivered"), early, 1),
                                   (dict(args=dict(id="task")), early, 1),
                                   (dict(args=dict(id="task")), late, None)]:
                es = [dict(seq=1, ts=ts, type="proposal", body=body, proposer="task"), merge]
                with self.subTest(body=body, ts=ts):
                    self.assertEqual(due.assess(root, sha, es, early)[0]["done"], done)
            self.assertIsNone(due.assess(root, sha, [merge], late)[0]["done"])

    def test_discharge_uses_later_of_citation_and_first_byte_exact_merge(self):
        early, due_at, late = "2026-11-03T11:00:00Z", "2026-11-03T12:00:00Z", "2026-11-03T13:00:00Z"
        data = lines(row(), discharge())
        with tree({due.PATH: lines(row())}) as (root, original):
            held = commit(root, {due.PATH: data})
            another = commit(root, {"note": "another merge"})
            cite = dict(seq=1, ts=early, type="proposal", body=dict(title="delivered task"))
            merges = [dict(seq=2, ts=early, type="merge", body=dict(commit=original)),
                      dict(seq=3, ts=early, type="merge", body=dict(commit=held)),
                      dict(seq=4, ts=late, type="merge", body=dict(commit=another))]
            cases = [(early, early, late, True, False), (early, late, late, True, True),
                     (late, early, late, True, True), (early, early, due_at, True, False),
                     (early, None, late, False, True), (early, due_at, early, False, False)]
            for cited_at, merged_at, as_of, done, escalated in cases:
                es = [dict(cite, ts=cited_at), merges[0]]
                if merged_at:
                    es += [dict(merges[1], ts=merged_at), merges[2]]
                with self.subTest(case=(cited_at, merged_at, as_of)):
                    got = due.assess(root, held, es, as_of)[0]
                    self.assertEqual((got["done"] is not None, got["escalated"]), (done, escalated))
            # Same JSON, different bytes: neither the row's own merge nor this line witnesses it.
            reformatted = commit(root, {due.PATH: lines(row()) + (json.dumps(discharge(), indent=None) + "\n").encode()})
            es = [cite, dict(merges[1], body=dict(commit=reformatted))]
            self.assertIsNone(due.assess(root, held, es, late)[0]["done"])

    def test_malformed_rows_do_not_discharge_or_replace_obligations(self):
        for data in (b"not json", b"[]\n", b"\n", lines(row(), row()), lines(discharge()),
                     lines(dict(row(), done=1)), lines(dict(row(), done=discharge()["done"])),
                     lines(dict(row(), due="2026-11-32T00:00:00Z")), lines(dict(row(), extra=1)),
                     lines(row(), dict(id="task", done=1)), lines(row(), discharge(seq=True)),
                     lines(row(), dict(id="task", done=dict(seq=1, what=5)))):
            with self.subTest(data=data), self.assertRaisesRegex(ValueError, "malformed COUNSEL-DUE file"):
                due.fold(data)

    def test_fold_and_only_the_two_authorised_redates(self):
        dates = [dict(id=rid, due=by, seq=1564, why="direction") for rid, by in due.REDATES.items()]
        seeds = [row(d["id"], "2026-11-18T00:00:00Z") for d in dates]
        folded = due.fold(lines(*seeds, *dates, discharge("c2c-brief")))
        self.assertEqual([r["due"] for r in folded], list(due.REDATES.values()))
        self.assertEqual(folded[1]["discharges"][0][1], lines(discharge("c2c-brief")))
        bads = [lines(*seeds, dict(dates[0], id="runbook-c2b")),
                lines(*seeds, dict(dates[0], due="2026-12-01T00:00:00Z")),
                lines(*seeds, dates[0], dates[0]), lines(*seeds, dict(dates[0], seq=1565)),
                lines(dates[0], *seeds), lines(*seeds, discharge("c2b-report"), dates[0]),
                lines(*seeds, dict(dates[0], seq=True)), lines(*seeds, dict(dates[0], why=0))]
        for data in bads:
            with self.subTest(data=data), self.assertRaisesRegex(ValueError, "malformed COUNSEL-DUE file"):
                due.fold(data)


class DueCLITest(SignedFixture):
    def test_cli_reads_requested_tree_and_refuses_malformed_files_and_logs(self):
        with tree({due.PATH: lines(row()), "log.jsonl": self.s.log.text()}) as (root, sha):
            out, err = io.StringIO(), io.StringIO()
            args = ["--root", root, "--as-of", "2026-11-03T13:00:00Z"]
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(due.main(args + ["--rev", sha, "--inventory", sha]), 0)
                self.assertIn("ESCALATED 1.00h past due", out.getvalue())
                bad = commit(root, {due.PATH: lines(row()) + b"not-json\n"})
                self.assertEqual(due.main(args + ["--rev", bad]), 2)
                self.assertIn("W5: malformed COUNSEL-DUE file", err.getvalue())
                # A committed read is independent of today's replacement file and log.
                commit(root, {due.PATH: b"", "log.jsonl": "not-json\n"})
                self.assertEqual(due.main(args + ["--rev", sha]), 0)
                self.assertEqual(due.main(args), 2)
