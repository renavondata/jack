"""C2b reviewer fixtures, run inside each disposable mutant tree."""
import json
import os
import unittest
from fractions import Fraction
from unittest.mock import patch

from tests.clerk_fixture import SignedFixture, commit, tree
from tests.test_due import DueTest, discharge, lines, row
from tests.test_push_gate import REVIEW, PushGate
from tests.test_workflow import WorkflowTest
from tests import test_status
from tools import due, status as st

SEED_IDS = ("c2a-acts", "c2a-report", "hkjc-hv-20261104", "D-1", "runbook-c2b",
            "V0", "V1", "V2", "V3", "c2b-report", "c2c-brief")


class GateCases(PushGate):
    def test_read_not_counsels_twins(self):
        self.test_read_not_counsels()
        self.publish(f"VERDICT: BLOCK\nReviewed tree: `{self.base}`\n", "reviewer")
        self.write(REVIEW, self.accepted())
        self.git("add", ".")
        self.git("commit", "-qm", "counsel edits headers\n\nProposer: counsel counsel-1")
        self.main()
        self.rejected("REVIEW-C2b-v1.md:.*identical review blob")
        self.publish(self.accepted(), "reviewer")
        self.gate()


class W5Cases(SignedFixture):
    def test_w5_overdue_escalates(self):
        DueTest("test_render_boundary_and_late_history_never_clears").test_render_boundary_and_late_history_never_clears()
        first = test_status.C2aPrimeTest.c2a_stream(self)
        self.s.forecast(ts="2026-11-17T00:00:00Z", args={"id": "X7"}, resolves_by="2026-12-01T12:00:00Z")
        self.s.add("decision", "guy", ts="2026-11-18T00:00:00Z", kind="promote", subject="C2a")
        self.s.add("push", "guy", ts="2026-11-18T00:00:01Z", digest="a" * 64, review="0" * 64)
        sc = dict(counted=["tests/"], cap=10400)
        files = {"judge/scope.json": json.dumps(sc), "SPEC.md": "## 10. Outside\nat C1 it is:\n```\n" + json.dumps(sc) + "\n```\n",
                 "log.jsonl": "\n".join(self.s.log.lines[:first + 1]) + "\n", st.WORKFLOW: "workflow\n",
                 due.PATH: lines(row("task", "2026-11-18T01:00:00Z"))}
        with tree(files) as (root, _):
            head = commit(root, {"log.jsonl": self.s.log.text()})
            at_due = st.render(st.assess(self.s.es, "C2b", "2026-11-18T01:00:00Z", root, head))
            past_due = st.render(st.assess(self.s.es, "C2b", "2026-11-18T02:00:00Z", root, head))
            self.assertIn("W5 task due 2026-11-18T01:00:00Z deliver it: OPEN", at_due)
            self.assertIn("W5 task due 2026-11-18T01:00:00Z deliver it: ESCALATED 1.00h past due", past_due)

    def test_w5_escalation_history(self):
        t1, t2, d0, t3, t4, as_of = ("2026-11-03T10:00:00Z", "2026-11-03T11:00:00Z", "2026-11-03T12:00:00Z",
                                     "2026-11-03T13:00:00Z", "2026-11-03T14:00:00Z", "2026-11-03T15:00:00Z")
        with tree({due.PATH: lines(row("task", d0))}) as (root, seed):
            discharged = commit(root, {due.PATH: lines(row("task", d0), discharge("task", 2))})
            again = commit(root, {"note": "second merge holding discharge"})
            row_merge = dict(seq=1, ts=t1, type="merge", body=dict(commit=seed))
            cite_early = dict(seq=2, ts=t1, type="proposal", body=dict(title="task"))
            cite_late = dict(seq=2, ts=t3, type="proposal", body=dict(title="task"))
            merge_early = dict(seq=3, ts=t2, type="merge", body=dict(commit=discharged))
            merge_late = dict(seq=3, ts=t3, type="merge", body=dict(commit=discharged))
            merge_second = dict(seq=4, ts=t4, type="merge", body=dict(commit=again))
            show = lambda es, at=as_of: due.render(due.assess(root, discharged, es, at, seed))
            # Twin 1: cited before D0, discharge first merged before D0 -> done on time
            self.assertTrue(show([row_merge, cite_early, merge_early]).endswith(": done seq 2 on time"))
            # Twin 2: cited before D0, discharge first merged after D0 -> ESCALATED late
            self.assertTrue(show([row_merge, cite_early, merge_late]).endswith(": done seq 2 ESCALATED 1.00h late"))
            # Twin 3: discharge first merged before D0, cited after D0 -> ESCALATED late
            self.assertTrue(show([row_merge, cite_late, merge_early]).endswith(": done seq 2 ESCALATED 1.00h late"))
            # Twin 4: cited before D0, discharge merged once before D0 and again after -> done on time
            self.assertTrue(show([row_merge, cite_early, merge_early, merge_second]).endswith(": done seq 2 on time"))
            # Twin 5: cited before D0, no merge holding discharge -> undone, ESCALATED past D0
            self.assertTrue(show([row_merge, cite_early]).endswith(": ESCALATED 3.00h past due"))
            # Twin 6: Twin 1 read at as-of after cited entry and before merge, both before D0 -> undone, OPEN
            self.assertTrue(show([row_merge, cite_early, merge_early], "2026-11-03T10:30:00Z").endswith(": OPEN"))

    def test_w5_done_is_an_entry(self):
        DueTest("test_done_requires_an_entry_on_prefix_naming_the_id_in_its_body").test_done_requires_an_entry_on_prefix_naming_the_id_in_its_body()
        DueTest("test_malformed_rows_do_not_discharge_or_replace_obligations").test_malformed_rows_do_not_discharge_or_replace_obligations()

    def test_w5_rows_append_only(self):
        d0 = "2026-11-03T12:00:00Z"
        with tree({due.PATH: lines(row("task", d0))}) as (root, seed):
            discharged = commit(root, {due.PATH: lines(row("task", d0), row("task2", d0), discharge("task", 1))})
            es = [dict(seq=1, ts="2026-11-03T10:00:00Z", type="proposal", body=dict(title="task")),
                  dict(seq=2, ts="2026-11-03T11:00:00Z", type="merge", body=dict(commit=discharged))]
            rows = due.assess(root, discharged, es, "2026-11-03T13:00:00Z", seed)
            self.assertEqual([r["done"] for r in rows], [1, None])
        DueTest("test_append_only_checks_deleted_and_restored_history_and_seed_inventory").test_append_only_checks_deleted_and_restored_history_and_seed_inventory()

    def test_w5_inventory(self):
        with open(os.path.join(st.ROOT, due.PATH), "rb") as f:
            seeded = due.fold(f.read())
        self.assertEqual([r["id"] for r in seeded], list(SEED_IDS))
        d0 = "2026-11-03T12:00:00Z"
        with tree({due.PATH: lines(row("task", d0), row("keep", d0))}) as (root, seed):
            discharged = commit(root, {due.PATH: lines(row("task", d0), row("keep", d0), discharge("task", 1))})
            es = [dict(seq=1, ts="2026-11-03T10:00:00Z", type="proposal", body=dict(title="task")),
                  dict(seq=2, ts="2026-11-03T11:00:00Z", type="merge", body=dict(commit=discharged))]
            self.assertEqual(due.assess(root, discharged, es, "2026-11-03T11:30:00Z", seed)[0]["done"], 1)
            extra = commit(root, {due.PATH: lines(row("task", d0), row("keep", d0), row("third", d0))})
            with self.assertRaisesRegex(ValueError, "missing third"):
                due.assess(root, discharged, es, "2026-11-03T11:30:00Z", extra)

    def test_w5_redate(self):
        d0 = "2026-11-18T00:00:00Z"
        r_rep, r_br, r_rb = row("c2b-report", d0), row("c2c-brief", d0), row("runbook-c2b", d0)
        d_rep = dict(id="c2b-report", due="2026-12-02T12:00:00Z", seq=1564, why="direction")
        d_br = dict(id="c2c-brief", due="2026-11-16T00:00:00Z", seq=1564, why="direction")
        # Twin 1: the two lines of the table, after their rows; the rows print their new dues.
        with tree({due.PATH: lines(r_rep, r_br, d_rep, d_br)}) as (root, sha):
            rendered = due.render(due.assess(root, sha, [], "2026-11-15T00:00:00Z", sha))
            self.assertIn("W5 c2b-report due 2026-12-02T12:00:00Z", rendered)
            self.assertIn("W5 c2c-brief due 2026-11-16T00:00:00Z", rendered)
        # Twins 2..6: each makes the file malformed.
        malformed = [
            lines(r_rep, r_br, r_rb, d_rep, d_br, dict(id="runbook-c2b", due="2026-12-02T12:00:00Z", seq=1564, why="x")),
            lines(r_rep, r_br, dict(d_rep, due="2026-12-01T00:00:00Z"), d_br),
            lines(r_rep, r_br, d_rep, d_rep, d_br),
            lines(r_rep, r_br, dict(d_rep, seq=1565), d_br),
            lines(d_rep, r_rep, r_br, d_br),
        ]
        for idx, bad in enumerate(malformed, 2):
            with self.subTest(twin=idx), self.assertRaisesRegex(ValueError, "malformed COUNSEL-DUE file"):
                due.fold(bad)

    def test_c2b_history_from_w5(self):
        end = "2026-11-18T02:00:00Z"
        green = dict(path=st.WORKFLOW, event="push", head_branch="main", conclusion="success", updated_at=end)
        # Twins 1..7 from Amendment 8:
        cases = [
            (1, "2026-11-18T00:20:00Z", ["2026-11-18T00:30:00Z"], False, True, True),
            (2, "2026-11-18T01:00:00Z", ["2026-11-18T00:30:00Z"], False, True, False),
            (3, "2026-11-18T01:00:00Z", ["2026-11-18T00:30:00Z"], True, True, True),
            (4, "2026-11-18T00:20:00Z", ["2026-11-18T00:30:00Z"], False, False, False),
            (5, "2026-11-18T00:40:00Z", ["2026-11-18T00:30:00Z", "2026-11-18T00:50:00Z"], False, True, False),
            (6, "2026-11-18T00:30:00Z", ["2026-11-18T00:30:00Z"], False, True, True),
            (7, "2026-11-18T01:00:00Z", [], False, True, True),
        ]
        for twin, deadline, landings, tick, discharged, expected in cases:
            self.setUp()
            first = test_status.C2aPrimeTest.c2a_stream(self)
            self.s.forecast(ts="2026-11-17T00:00:00Z", args={"id": "X7"}, resolves_by="2026-12-01T12:00:00Z")
            self.s.add("decision", "guy", ts="2026-11-18T00:00:00Z", kind="promote", subject="C2a")
            self.s.add("push", "guy", ts="2026-11-18T00:00:01Z", digest="a" * 64, review="0" * 64)
            r0 = lines(row("task", deadline))
            sc = dict(counted=["tests/"], cap=10400)
            files = {"judge/scope.json": json.dumps(sc), "SPEC.md": "## 10. Outside\nat C1 it is:\n```\n" + json.dumps(sc) + "\n```\n",
                     "log.jsonl": "\n".join(self.s.log.lines[:first + 1]) + "\n", st.WORKFLOW: "workflow\n", due.PATH: r0,
                     "pins/pins.py": "\n".join(f'Pin("{n}", t, m)' for n in st.VALUE_PINS + list(st.C2B_PINS) + st.C2B_BOUND_PINS)}
            for p in ("tools/status.py", "tools/clerk.py", "tools/elect.py", "sim/election.py", "tests/test_elect.py",
                      "tests/test_sim.py", "tests/test_value.py", "tests/test_clerk.py"):
                with open(os.path.join(st.ROOT, p)) as f:
                    files[p] = f.read()
            with self.subTest(twin=twin), tree(files) as (root, _):
                start = commit(root, {"log.jsonl": self.s.log.text()})
                cited = self.s.add("proposal", "counsel", ts="2026-11-18T00:10:00Z", title="task", commit="a" * 40)
                for i, lts in enumerate(landings):
                    w5_commit = commit(root, {"log.jsonl": self.s.log.text(), "tools/due.py": f"# W5 {i}\n"})
                    self.s.add("merge", ts=lts, proposal=cited, commit=w5_commit, checker="a" * 64)
                self.s.add("proposal", ts="2026-11-18T01:00:01Z", title="tick", commit="b" * 40)
                witness = f"W5 task due {deadline} deliver it: ESCALATED 0.00h past due\n"
                commit(root, {"log.jsonl": self.s.log.text(), **({"transcripts/evidence/w5/tick.txt": witness} if tick else {})})
                if discharged:
                    d_commit = commit(root, {due.PATH: r0 + lines(discharge("task", cited))})
                    self.s.add("merge", ts="2026-11-18T01:20:00Z", proposal=cited, commit=d_commit, checker="a" * 64)
                head = commit(root, {"log.jsonl": self.s.log.text()})
                run = dict(green, head_sha=head)
                runs = [dict(green, head_sha=start, updated_at="2026-11-18T00:00:02Z"), run]
                s = st.assess(self.s.es, "C2b", end, root, head, run=run, runs=runs, acts=[])
                c8 = next(ok for ok, text in s["checks"] if text.startswith("criterion 8:"))
                self.assertEqual(c8, expected)


class WorkflowCases(WorkflowTest):
    pass
