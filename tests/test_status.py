"""tools/status.py: the window's figures from synthetic entries (hermetic; no log on disk, no clock)."""
import hashlib
import os
import tempfile
import unittest
from unittest.mock import patch

from tools import status as st


def e(seq, ts, type_, proposer, **body):
    return {"seq": seq, "ts": ts, "type": type_, "proposer": proposer, "body": body}


class StatusTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "transcripts", "evidence"))
        blob = b"a saved page\n"
        self.h = hashlib.sha256(blob).hexdigest()
        with open(os.path.join(self.root, "transcripts", "evidence", self.h), "wb") as f:
            f.write(blob)
        self.es = [
            e(0, "2026-10-25T16:44:10Z", "amend", "guy", id="A3", activate_at=1),
            e(1, "2026-10-26T00:00:00Z", "forecast", "counsel", claim="w", p=500, resolves_by="2026-10-27T00:00:00Z", type="world.x"),
            e(2, "2026-10-26T00:00:01Z", "forecast", "guy", claim="free", p=500, resolves_by="2026-11-20T00:00:00Z"),
            e(3, "2026-10-26T00:00:02Z", "proposal", "counsel", commit="c", title="t"),
            e(4, "2026-10-26T01:00:00Z", "resolution", "herald", forecast=1, outcome=1, evidence="sha256:" + self.h),
            e(5, "2026-10-26T02:00:00Z", "forecast", "reviewer", claim="w2", p=300, resolves_by="2026-10-26T03:00:00Z", type="world.x",
              args={"evidence": "https://example/page"}),
            e(6, "2026-11-09T00:00:00Z", "forecast", "counsel", claim="after the window", p=500, resolves_by="2026-12-01T00:00:00Z"),
        ]

    def test_counts_ratio_and_evidence(self):
        s = st.status(self.es, "A3", 14, "2026-10-26T04:00:00Z", root=self.root)
        self.assertEqual((s["start"], s["end"]), ("2026-10-25T16:44:10Z", "2026-11-08T16:44:10Z"))
        self.assertEqual((s["forecasts"], s["resolutions"], s["world_resolutions"], s["world_resolutions_with_evidence"]), (3, 1, 1, 1))
        self.assertEqual(s["proposers"], ["counsel", "guy", "reviewer"])
        self.assertEqual((s["procedure"], s["object"]), (3, 3))  # amend, free forecast, proposal : two world forecasts, one world resolution
        self.assertFalse(s["veto"])

    def test_overdue_and_j7_follow_the_clock(self):
        early = st.status(self.es, "A3", 14, "2026-10-26T02:30:00Z", root=self.root)
        late = st.status(self.es, "A3", 14, "2026-10-26T04:00:00Z", root=self.root)
        self.assertEqual(early["overdue"], [])
        self.assertEqual([(seq, who, ev) for _, seq, who, ev in late["overdue"]], [(5, "reviewer", "https://example/page")])
        self.assertEqual((late["j7_unresolved_past_due"], late["j7_denominator"]), (1, 3))

    def test_exit_prefix_stops_at_the_window_end(self):
        s = st.status(self.es, "A3", 14, "2026-12-31T00:00:00Z", root=self.root)
        self.assertEqual(s["prefix_last_seq"], 5)  # seq 6 is after the end instant and never counts
        self.assertEqual(s["forecasts"], 3)

    def test_evidence_must_hash(self):
        with open(os.path.join(self.root, "transcripts", "evidence", "0" * 64), "wb") as f:
            f.write(b"present, but not the claimed bytes")
        bad = dict(self.es[4]); bad["body"] = dict(bad["body"], evidence="sha256:" + "0" * 64)
        s = st.status(self.es[:4] + [bad] + self.es[5:], "A3", 14, "2026-10-26T04:00:00Z", root=self.root)
        self.assertEqual((s["world_resolutions"], s["world_resolutions_with_evidence"]), (1, 0))

    def test_resolution_ratio_follows_its_forecasts_type(self):
        world = st.status(self.es, "A3", 14, "2026-10-26T04:00:00Z", root=self.root)
        procedure = st.status(self.es + [e(6, "2026-10-26T04:00:00Z", "resolution", "herald", forecast=2, outcome=1, evidence="run")],
                              "A3", 14, "2026-10-26T04:00:00Z", root=self.root)
        self.assertEqual((procedure["procedure"], procedure["object"]), (world["procedure"] + 1, world["object"]))

    def test_veto_on_the_subject(self):
        es = self.es + [e(7, "2026-10-27T00:00:00Z", "decision", "guy", kind="veto", subject="C1a")]
        self.assertTrue(st.status(es, "A3", 14, "2026-10-28T00:00:00Z", root=self.root)["veto"])
        self.assertFalse(st.status(es, "A3", 14, "2026-10-28T00:00:00Z", root=self.root, subject="other")["veto"])

    def test_render_marks_short_lines(self):
        with patch.object(st, "tree_facts", return_value=dict(counted=6200, kernel=500, scope=True)):
            text = st.render(st.assess(self.es, "C1a", "2026-10-26T04:00:00Z", self.root, None))
        self.assertIn("forecasts 3/20; proposers 3/3", text)
        self.assertIn("world-typed with evidence 1/5 SHORT", text)
        self.assertIn("maximum 5:1) met", text)


if __name__ == "__main__":
    unittest.main()
