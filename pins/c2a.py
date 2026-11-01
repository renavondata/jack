"""Reviewer fixtures run inside the disposable tree, against its scorer imports."""
import copy
import unittest
from fractions import Fraction as F
from tests.test_value import seed, forecast, resolve, calc, worked_entries, e, OPEN, CUT, END
from tools import value as v, status as st


class Cases(unittest.TestCase):
    def test_rigged_record(self):
        es = worked_entries()
        r = calc(es)
        self.assertEqual(r["excluded_forecasts"], [(seq, "rigged: ts >= cutoff") for seq in (288, 289, 290)])
        twin = copy.deepcopy(es)
        for f in twin:
            if f["seq"] in (288, 289, 290):
                f["body"]["args"] = dict(f["body"]["args"], window_utc=["2026-11-01T05:00:00Z", "2026-11-01T06:00:00Z"])
        admitted = calc(twin)
        self.assertEqual(admitted["excluded_forecasts"], [])
        self.assertEqual((r["events"], admitted["events"]), (25, 28))
        self.assertTrue({288, 289, 290} <= {seq for row in admitted["rows"] for seq, p in row["forecasts"].values()})

    def test_per_dataset(self):
        def fresh(seq, dataset):
            return forecast(seq, type="world.renavon", args=dict(stream="freshness", dataset=dataset,
                            window_utc=[CUT, "2026-11-01T02:00:00Z"]))
        es = seed() + [fresh(1, "hk_property_poi"), resolve(2, 1), fresh(3, "crhk_companies"), resolve(4, 3, 0)]
        rows = calc(es)["rows"]
        self.assertEqual([row["base"] for row in rows], [F(1, 2), F(2, 3)])
        self.assertEqual([row["base_counts"] for row in rows], [(0, 0), (1, 1)])
        es[3]["body"]["args"]["dataset"] = "hk_property_poi"
        es[3]["body"]["args"]["window_utc"] = ["2026-11-01T02:00:00Z", "2026-11-01T03:00:00Z"]
        self.assertEqual([row["base"] for row in calc(es)["rows"]], [F(1, 2), F(2, 3)])

    def test_factor_tree(self):
        # True probability b. Equality and opposite endpoints have exact x=0,+/-1;
        # no floating logarithm is treated as an exact general-purpose oracle.
        nodes, adaptive_equalities = [], []
        def walk(path, prior, b):
            q = b if path and path[-1] else 1 - b
            lam = v.stake(prior)
            exact_lam = F(lam)
            xs = (0, 0) if q == b else (-1, 1) if q > b else (1, -1)
            factors = [v.factor(lam, v.difference(q, b, y)) for y in (0, 1)]
            for y in (0, 1):
                self.assertEqual(v.difference(q, b, y), xs[y])
                self.assertEqual(factors[y], float(1 + exact_lam * xs[y]))
                self.assertGreater(factors[y], 0)
            expectation = (1-b)*F(factors[0]) + b*F(factors[1])
            self.assertLessEqual(expectation, 1)  # exact comparison of actual binary64 outputs
            self.assertLessEqual((1-b)*(1+exact_lam*xs[0]) + b*(1+exact_lam*xs[1]), 1)
            if q == b:
                self.assertEqual(expectation, 1)
                self.assertEqual(expectation + F(1, 50), F(51, 50))
                adaptive_equalities.append(lam > 0)
            nodes.append(path)
            if len(path) < 2:
                for y in (0, 1):
                    walk(path + (y,), prior + [float(xs[y])], b)
        for b in (F(1, 2), F(1, 1000), F(999, 1000)):
            walk((), [], b)
        self.assertEqual(len(nodes), 21)
        self.assertTrue(any(adaptive_equalities))
        abstain = calc(seed()+[forecast(1, ts=CUT), resolve(2, 1)])["rows"][0]
        self.assertEqual((abstain["q"], abstain["base"], abstain["D_over_B"]), (F(1, 2), F(1, 2), 0.0))

    def test_opening_merge(self):
        gate, after = "2026-11-01T02:00:00Z", "2026-11-01T03:00:00Z"
        es = seed() + [e(337, "decision", kind="promote", subject="C1b"), e(350, "merge"),
                      e(366, "forecast", args={"id": "V0"}, resolves_by="2026-12-01T00:00:00Z"),
                      e(367, "push", ts=CUT)]
        self.assertEqual(v.opening_push(es)["seq"], 367)
        self.assertEqual(st.c2a_window(es), (367, CUT, "2026-11-15T01:00:00Z"))
        for cutoff, attack, expected in ((OPEN, OPEN, 0), (CUT, OPEN, 0), (gate, gate, 0), (after, gate, 1), (after, None, 0)):
            trial = es + [forecast(368, cutoff=cutoff), resolve(369, 368)]
            r = v.value(trial, attack_green=attack)
            self.assertEqual(r["events"], expected, (cutoff, attack))
            self.assertEqual(len(r["excluded_events"]), 1-expected)

    def test_second_window(self):
        second = "2026-11-01T02:00:00Z"
        es = seed() + [e(338, "push", ts=OPEN), forecast(339), resolve(340, 339),
                      forecast(341, race=2, cutoff=second), resolve(342, 341),
                      e(343, "push", ts=second), forecast(344, race=3, cutoff="2026-11-01T03:00:00Z"), resolve(345, 344)]
        first = v.value(es, no_attack_gate=True)
        retry = v.value(es, no_attack_gate=True, window_opening=second)
        self.assertGreater(first["rows"][1]["E_after"], 1)
        self.assertGreater(first["rows"][2]["lambda"], 0)
        self.assertEqual(retry["E_value"], first["E_value"])
        self.assertEqual(retry["rows"], first["rows"])
        self.assertEqual(retry["terminal_weights"], first["terminal_weights"])
        self.assertEqual(retry["window_events"], 1)
        self.assertNotEqual(retry["window_weights"], retry["terminal_weights"])
