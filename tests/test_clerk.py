"""C1b's own signed fixtures, independent of the simulator's stalling/flooding seeds."""
import copy
import json
import os
import unittest
from fractions import Fraction

from harness import build
from kernel import check
from tests.clerk_fixture import DUE, LATE, NOW, SignedFixture, Stream
from tools import clerk, status


class ClerkTest(SignedFixture):
    def rows(self):
        return [(i["seq"], i["kind"], i["forecasts"], i["Y"]) for i in self.s.process()["items"]]

    def test_w1_from_entry_strict_deadline_holders_and_discharge(self):
        f = self.s.forecast()
        self.assertTrue(check.check(self.s.log.lines)["ok"])
        for now, escalated in ((NOW, False), (DUE, False), (LATE, True)):
            writs = clerk.forecast_writs(self.s.es, [], now)
            self.assertEqual([(w["seq"], w["holders"], w["deadline"], w["escalated"]) for w in writs],
                             [(f, ("guy", "herald"), DUE, escalated)])
            self.assertEqual("ESCALATED to guy" in clerk.render(writs), escalated)
        self.s.resolve(f)
        self.assertEqual(clerk.forecast_writs(self.s.es, [], LATE), [])

    def test_flood_and_byte_identical_projection(self):
        forecasts = [self.s.forecast() for _ in range(6)]
        before = copy.deepcopy(self.s.es)
        first = clerk.forecast_writs(self.s.es, [], NOW)
        second = clerk.forecast_writs(self.s.es, [], NOW)
        self.assertEqual([w["seq"] for w in first], forecasts)
        self.assertEqual(clerk.render(first).encode(), clerk.render(second).encode())
        self.assertEqual(before, self.s.es)

    def test_holders_follow_key_revocation(self):
        self.s.forecast()
        self.s.add("key", "guy", **build.decl("herald", "herald", self.signers["herald"], []))
        self.assertEqual(clerk.forecast_writs(self.s.es, [], NOW)[0]["holders"], ("guy",))

    def test_window_and_same_timestamp_opening(self):
        old = self.s.opening - 1
        self.s.add("decision", "guy", kind="budget", subject="later")
        fresh = self.s.forecast(resolves_by=LATE, args={"id": "L1"})
        self.assertEqual(status.c1b_window(self.s.es), (self.s.opening, NOW, DUE))
        self.s.resolve(old)
        self.s.resolve(fresh)
        m = self.s.merge()
        self.assertEqual(self.rows(), [(m, "batch", (fresh,), 1)])

    def test_expiry_precedes_own_resolution_and_expired_only_merge(self):
        f = self.s.forecast()
        r = self.s.resolve(f, ts=LATE)
        self.s.merge(ts=LATE)
        self.assertEqual(self.rows(), [(r, "expiry", (f,), 0)])

    def test_mixed_batch_keeps_only_fresh_writs(self):
        expired = self.s.forecast()
        fresh = self.s.forecast(resolves_by=LATE)
        r = self.s.resolve(expired, ts=LATE)
        self.s.resolve(fresh, ts=LATE)
        m = self.s.merge(ts=LATE)
        self.assertEqual(self.rows(), [(r, "expiry", (expired,), 0), (m, "batch", (fresh,), 1)])

    def test_expiry_ties_in_forecast_order(self):
        fs = [self.s.forecast() for _ in range(2)]
        boundary = self.s.add("proposal", ts=LATE, **build.proposal())
        self.assertEqual(self.rows(), [(boundary, "expiry", (f,), 0) for f in fs])

    def test_sovereign_resolution_and_merge_are_zero(self):
        for when in (NOW, LATE):
            self.s = Stream(self.signers)
            f = self.s.forecast()
            r = self.s.resolve(f, who="guy", ts=when)
            self.s.merge(ts=when)
            self.assertEqual(self.rows(), [(r, "expiry" if when == LATE else "sovereign resolution", (f,), 0)])
        self.s = Stream(self.signers)
        f = self.s.forecast()
        self.s.resolve(f)
        m = self.s.merge("guy")
        self.s.merge("guy")
        self.assertEqual(self.rows(), [(m, "batch", (f,), 0)])

    def test_sovereign_boundary_clears_pending_without_future_expiry(self):
        f = self.s.forecast()
        self.s.resolve(f)
        self.s.add("decision", "guy", kind="fix", subject="runner")
        self.s.merge(ts=LATE)
        self.assertEqual(self.rows(), [])

    def test_repair_subject_never_narrows_taint(self):
        for subject in ("A", "B", "neither", "", None):
            self.s = Stream(self.signers)
            a, b = self.s.forecast(claim="A"), self.s.forecast(claim="B")
            if subject is not None:
                self.s.add("decision", "guy", kind="fix", subject=subject)
            self.s.resolve(b)
            mb = self.s.merge()
            self.s.resolve(a)
            ma = self.s.merge()
            y = int(subject is None)
            self.assertEqual(self.rows(), [(mb, "batch", (b,), y), (ma, "batch", (a,), y)], subject)

    def test_repair_without_open_writ_has_no_future_taint(self):
        self.s.add("decision", "guy", kind="fix", subject="runner")
        self.s.complete(1)
        self.assertEqual(self.rows(), [(8, "batch", (6,), 1)])

    def test_late_report_never_changes_prior_items_stakes_or_wealth(self):
        self.s.complete(9)
        before = self.s.process()
        self.assertGreater(before["items"][-1]["stake"], 0)
        f = self.s.forecast()
        r = self.s.add("decision", "guy", kind="fix", subject=str(before["items"][0]["forecasts"][0]))
        self.s.resolve(f)
        m = self.s.merge()
        after = self.s.process()
        self.assertEqual(after["items"][:-1], before["items"])
        self.assertEqual(after["late_reports"], [r])
        self.assertEqual(self.rows()[-1], (m, "batch", (f,), 0))

    def test_batch_is_not_a_count_of_resolutions(self):
        fs = [self.s.forecast() for _ in range(6)]
        for f in fs:
            self.s.resolve(f)
        m = self.s.merge()
        self.assertEqual(self.rows(), [(m, "batch", tuple(fs), 1)])
        self.s = Stream(self.signers)
        self.s.complete(6)
        self.assertEqual(len(self.rows()), 6)
        self.assertTrue(all(len(row[2]) == row[3] == 1 for row in self.rows()))

    def test_evidence_reuse_cannot_regroup_scored_items(self):
        for n in range(6):
            self.s.resolve(self.s.forecast(), evidence=f"run{n}")
            self.s.merge()
        before = self.s.process()["items"]
        for evidence, n in (("run", 7), ("fresh", 8)):
            fs = [self.s.forecast() for _ in range(2)]
            for k, f in enumerate(fs):
                self.s.resolve(f, evidence=f"{evidence}{k}")
            m = self.s.merge()
            after = self.s.process()["items"]
            self.assertEqual(after[:-1], before)
            self.assertEqual(self.rows()[-1], (m, "batch", tuple(fs), 1))
            self.assertEqual((len(after), after[-1]["E"]), (n, status.score_items([{"Y": 1}] * n)["E"]))
            before = after

    def test_exact_prequential_wealth(self):
        eight = status.score_items([{"Y": 1}] * 8)["items"]
        nine = status.score_items([{"Y": 1}] * 9)["items"]
        self.assertEqual(status.P0, Fraction(6, 11))
        self.assertEqual(nine[:-1], eight)
        self.assertIsInstance(nine[-1]["E"], Fraction)
        self.assertLess(eight[-1]["E"], 20)
        self.assertGreaterEqual(nine[-1]["E"], 20)
        self.assertEqual(nine[0]["stake"], 0)

    def test_real_prefix_and_semantic_twin(self):
        with open(os.path.join(status.ROOT, "log.jsonl")) as f:
            es = [json.loads(line) for line in f if json.loads(line)["seq"] <= 163]
        items = status.item_process(es)["items"]
        expected = [(50, (45,), 0), (68, (46,), 0), (68, (47,), 0),
                    (102, (73, 74, 75, 83, 84, 85), 1), (103, (56,), 0), (106, (76, 86), 1),
                    (110, (38,), 0), (140, (121,), 1), (151, (114, 115, 118, 123, 127), 1)]
        self.assertEqual([(i["seq"], i["forecasts"], i["Y"]) for i in items], expected)
        self.assertEqual(sum(i["Y"] for i in items), 4)
        self.assertEqual([i["repairs"] for i in items], [(46, 47), (47,), (), (), (), (), (44, 45, 46, 47), (), ()])
        twin = status.item_process([e for e in es if e["seq"] not in (44, 45, 46, 47)])["items"]
        self.assertEqual(next(i["Y"] for i in twin if i["seq"] == 110), 1)
        for n in range(1, len(es) + 1):
            prefix = status.item_process(es[:n])["items"]
            self.assertEqual(prefix, items[:len(prefix)])


if __name__ == "__main__":
    unittest.main()
