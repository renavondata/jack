"""tools/status.py: the window's figures from synthetic entries (hermetic; no log on disk, no clock)."""
import hashlib
import json
import os
import unittest
from unittest.mock import patch

from tools import status as st
from harness.gitfix import write
from tests.clerk_fixture import SignedFixture, commit, tree


def e(seq, ts, type_, proposer, **body):
    return {"seq": seq, "ts": ts, "type": type_, "proposer": proposer, "body": body}


class StatusTest(unittest.TestCase):
    def setUp(self):
        blob = b"a saved page\n"
        self.h = hashlib.sha256(blob).hexdigest()
        self.root, _ = self.enterContext(tree({"transcripts/evidence/" + self.h: blob}))
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
        write(self.root, "transcripts/evidence/" + "0" * 64, b"present, but not the claimed bytes")
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
        with patch.object(st, "tree_facts", return_value=dict(counted=6900, kernel=500, scope=True)):
            text = st.render(st.assess(self.es, "C1a", "2026-10-26T04:00:00Z", self.root, None))
        self.assertIn("forecasts 3/20; proposers 3/3", text)
        self.assertIn("world-typed with evidence 1/5 SHORT", text)
        self.assertIn("maximum 5:1) met", text)


class C2aPrimeTest(SignedFixture):
    def c2a_stream(self):
        while len(self.s.es) < 337:
            self.s.add("proposal", title="pad", commit="a" * 40)
        self.s.add("decision", "guy", kind="promote", subject="C1b")
        self.s.forecast(args={"id": "V0"}, resolves_by="2026-11-17T12:00:00Z")
        op1 = self.s.add("push", "guy", ts="2026-11-01T15:04:14Z", digest="a" * 64, review="0" * 64)
        return op1

    def test_change_1_window(self):
        self.c2a_stream()
        self.s.add("push", "guy", ts="2026-11-16T00:00:00Z", digest="a" * 64, review="0" * 64)
        self.assertIsNone(st.c2a_prime_window(self.s.es))
        op_no_v5 = self.s.add("push", "guy", ts="2026-11-18T00:00:30Z", digest="a" * 64, review="0" * 64)
        self.s.forecast(ts="2026-11-18T01:00:00Z", args={"id": "V5"}, resolves_by="2026-11-30T00:00:00Z")
        s0 = st.assess(self.s.es, "C2a", "2026-11-18T02:00:00Z", None, None)
        self.assertEqual(st.promotion_line(s0), "promote C2a: refused: C2a-prime has no promotion forecast before its opening")
        self.assertIn(f"window: C2a-prime (second window of C2a, opened seq {op_no_v5})", st.render(s0))

        self.setUp()
        self.c2a_stream()
        self.s.add("decision", "guy", ts="2026-11-10T00:00:00Z", kind="veto", subject="C2a")
        self.s.add("decision", "guy", ts="2026-11-10T00:01:00Z", kind="veto", subject="C2a-prime")
        self.s.forecast(ts="2026-11-16T00:00:00Z", args={"id": "V5"}, resolves_by="2026-11-30T00:00:00Z")
        op2 = self.s.add("push", "guy", ts="2026-11-18T00:00:30Z", digest="a" * 64, review="0" * 64)
        scope78 = {"counted": ["tests/"], "cap": 7800}
        scope84 = {"counted": ["tests/"], "cap": 8400}
        files = {"judge/scope.json": json.dumps(scope78), "SPEC.md": "at C1 it is:\n```\n" + json.dumps(scope78) + "\n```\n",
                 "log.jsonl": "\n".join(self.s.log.lines[:-1]) + "\n", "tests/test_clerk.py": "# a\n", "tests/test_value.py": "# a\n",
                 "pins/pins.py": "\n".join(f'Pin("{name}", t, m)' for name in st.VALUE_PINS)}
        for path in ("tools/status.py", "tools/clerk.py"):
            with open(os.path.join(st.ROOT, path)) as f:
                files[path] = f.read()
        with tree(files) as (root, pre_sha):
            before = st.assess(self.s.es[:-1], "C2a", "2026-11-17T00:00:00Z", root, pre_sha,
                               acts=[dict(repo="renavondata/jack", time_hkt="2026-11-02 22:11", **{"class": "repair"}, kind="fix", ref="", note="")])
            self.assertNotIn("window: C2a-prime", st.render(before))
            self.assertIn("criterion 7: off-log repairs: 1 SHORT", st.render(before))
            open_sha = commit(root, {"judge/scope.json": json.dumps(scope84),
                                     "SPEC.md": "at C1 it is:\n```\n" + json.dumps(scope84) + "\n```\n",
                                     "log.jsonl": self.s.log.text()})
            row = lambda hkt: dict(repo="renavondata/jack", time_hkt=hkt, **{"class": "repair"}, kind="fix", ref="", note="")
            s = st.assess(self.s.es, "C2a", "2026-11-25T00:00:00Z", root, open_sha,
                          acts=[row("2026-11-02 22:11"), row("2026-11-18 08:00")])
            self.assertEqual((s["start"], s["end"], s["veto"]), ("2026-11-18T00:00:30Z", "2026-11-30T00:00:00Z", False))
            self.assertIn("counted 2/8400; kernel 0/500; scope equals SPEC and unchanged: True met", st.render(s))
            self.assertIn("criterion 7: off-log repairs: 1 SHORT", st.render(s))
            self.assertEqual(st.render(s).splitlines()[-2], f"window: C2a-prime (second window of C2a, opened seq {op2})")
            s_clean = st.assess(self.s.es, "C2a", "2026-11-25T00:00:00Z", root, open_sha,
                                acts=[row("2026-11-02 22:11"), row("2026-11-18 07:59"), row("2026-11-30 08:01")])
            self.assertIn("criterion 7: off-log repairs: 0 met", st.render(s_clean))
            self.s.add("decision", "guy", ts="2026-11-19T00:00:00Z", kind="veto", subject="C2a-prime")
            vetoed = commit(root, {"log.jsonl": self.s.log.text()})
            self.assertTrue(st.assess(self.s.es, "C2a", "2026-11-25T00:00:00Z", root, vetoed, acts=[])["veto"])
            bad_cap = commit(root, {"judge/scope.json": json.dumps(dict(scope84, cap=8401)),
                                    "SPEC.md": "at C1 it is:\n```\n" + json.dumps(dict(scope84, cap=8401)) + "\n```\n"})
            self.assertFalse(st.c2a_tree_evidence(root, bad_cap, self.s.es, op2)[0])


if __name__ == "__main__":
    unittest.main()
