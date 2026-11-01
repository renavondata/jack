"""C2a witnesses: own entries, exact oracles, signed attacks and disposable git evidence."""
import copy
import itertools
import json
import math
import os
import random
import tempfile
import unittest
from fractions import Fraction as F
from types import SimpleNamespace
from unittest.mock import patch

from sim import gen
from kernel import check
from tests.clerk_fixture import SignedFixture, NOW, commit, tree
from tests.test_promotion import jack, GREEN, EARLY
from tools import value as v, status as st

OPEN = "2026-10-31T10:42:10Z"
CUT = "2026-11-01T01:00:00Z"
END = "2026-11-01T13:10:16Z"


def e(seq, typ, who="counsel", ts=OPEN, **body):
    return dict(seq=seq, type=typ, proposer=who, ts=ts, body=body)


def seed():
    return [e(0, "genesis", keys=[dict(key_id=k, principal=k, powers=["forecast"])
                                 for k in ("counsel", "reviewer", "builder", "guy")])]


def forecast(seq, p=900, who="counsel", race=1, cutoff=CUT, ts=OPEN, **body):
    return e(seq, "forecast", who, ts, **dict(dict(p=p, claim="same text", type="world.hkjc",
             args=dict(meeting="M", race=race, off_utc=cutoff), resolves_by=END), **body))


def resolve(seq, f, y=1):
    return e(seq, "resolution", ts=END, forecast=f, outcome=y)


def calc(es, **kw):
    return v.value(es, **dict(dict(opening=OPEN, no_attack_gate=True), **kw))


def worked_entries():
    """Independent reconstruction: five freshness blocks, ten races, eight old outcomes."""
    es = seed()
    for i, (r, y) in enumerate(zip((96, 97, 98, 99, 100, 101, 104, 105), (1, 0, 1, 1, 0, 1, 0, 0))):
        es += [forecast(70 + i, args={}), resolve(r, 70 + i, y)]
    datasets = ("hk_property_poi", "hkex_disclosures", "hkex_disclosure_interests")
    for h, (f0, r0, who, p) in enumerate(((251, 261, "reviewer", 200), (256, 269, "reviewer", 200),
                                        (264, 277, "builder", 360), (272, 285, "builder", 940), (280, 293, "reviewer", 970))):
        for j, dataset in enumerate(datasets):
            args = dict(stream="freshness", dataset=dataset, window_utc=[f"2026-11-01T{h:02}:00:00Z", f"2026-11-01T{h+1:02}:00:00Z"])
            es += [forecast(f0+j, p, who, type="world.renavon", args=args), resolve(r0+j, f0+j)]
            if h == 4:
                es += [forecast(288+j, 970, who, ts="2026-11-01T04:54:00Z", type="world.renavon", args=args), resolve(296+j, 288+j)]
    times = ("04:45", "05:15", "05:45", "06:15", "07:10", "07:40", "08:10", "08:40", "09:15", "09:50")
    for i, (r, y, time) in enumerate(zip((299, 301, 303, 307, 309, 311, 315, 317, 321, 323), (1, 0, 1, 0, 0, 1, 1, 0, 0, 0), times)):
        args = dict(meeting="M2", race=i+1, off_utc=f"2026-11-01T{time}:00Z")
        es += [forecast(227+i, 235 if i == 6 else 220, "reviewer", args=args), forecast(239+i, 250, args=args),
               resolve(r, 227+i, y), resolve(r+1, 239+i, y)]
    return sorted(es, key=lambda x: x["seq"])


class Value(unittest.TestCase):
    def test_worked_table(self):
        result = calc(worked_entries(), as_of=END)
        with open(os.path.join(st.ROOT, "transcripts/evidence/value-fixture-20261101.json")) as f:
            fixture = json.load(f)
        shown = v.table(result)
        for key in fixture:
            self.assertEqual(shown[key], fixture[key], key)
        by_seq = {r["resolution_seq"]: r for r in result["rows"]}
        for seq, q in ((261, F(11, 25)), (301, F(1777827743896729, 3428747920370700)),
                       (323, F(465556277223067128664965551, 1149033951561021100421363300))):
            self.assertEqual(by_seq[seq]["q"], q)

    def test_forecast_before_cutoff(self):
        es = seed() + [forecast(1, ts=CUT), forecast(2, 700), forecast(3, 200), resolve(4, 1)]
        r = calc(es)
        self.assertEqual(r["rows"][0]["forecasts"], {"counsel": (2, F(7, 10))})
        self.assertEqual(r["excluded_forecasts"], [(1, "rigged: ts >= cutoff"), (3, "revision")])

    def test_rigged(self):
        for ts in (CUT, END):
            r = calc(seed() + [forecast(1, ts=ts), resolve(2, 1)])
            self.assertEqual(r["rows"][0]["forecasts"], {})
            self.assertEqual(r["rows"][0]["q"], F(1, 2))
            self.assertIn("rigged", r["excluded_forecasts"][0][1])
        r = calc(seed() + [forecast(1, ts=END, cutoff="2026-11-02T00:00:00Z"), resolve(2, 1), forecast(3, ts=END, cutoff="2026-11-02T00:00:00Z")])
        self.assertEqual(r["excluded_forecasts"], [(3, "rigged: after resolution")])
        self.assertEqual(calc(seed()+[forecast(1), resolve(2, 1)])["excluded_forecasts"], [])

    def test_revision(self):
        r = calc(seed() + [forecast(1, 800), forecast(2, 100), resolve(3, 2), resolve(4, 1, 0)])
        self.assertEqual((r["events"], r["rows"][0]["Y"]), (1, 1))
        self.assertEqual(r["rows"][0]["forecasts"], {"counsel": (1, F(4, 5))})
        self.assertEqual(r["excluded_forecasts"], [(2, "revision")])

    def test_weights_from_resolved_prefix(self):
        es = seed() + [forecast(1), forecast(2, race=2), resolve(3, 2), resolve(4, 1, 0)]
        a, b = calc(es)["rows"]
        self.assertEqual([a["key"][2], b["key"][2]], [2, 1])
        self.assertEqual(b["weights_before"]["counsel"], F(9, 29))
        self.assertEqual(a["weights_before"]["counsel"], F(1, 5))
        self.assertEqual(b["q"], F(643, 870))

    def test_abstention_is_base(self):
        r = calc(seed() + [forecast(1, args={}), resolve(2, 1), forecast(3, 800), resolve(4, 3)])
        row = r["rows"][0]
        self.assertEqual((row["base"], row["q"]), (F(2, 3), F(52, 75)))
        self.assertEqual(r["own_likelihood_ratio_vs_base"]["builder"], 1)
        self.assertEqual(r["terminal_weights"]["builder"], F(5, 26))

    def test_one_event_one_key(self):
        es = seed()+[forecast(1), forecast(2, who="builder", claim="different text"), forecast(3, args={}),
                    resolve(4, 1), resolve(5, 2, 0), resolve(6, 3)]
        r = calc(es)
        self.assertEqual((r["events"], r["unkeyed"], r["rows"][0]["Y"]), (1, [3], 1))
        self.assertEqual(set(r["rows"][0]["forecasts"]), {"counsel", "builder"})
        twin = copy.deepcopy(es)
        twin[2]["body"]["args"]["race"] = 2  # genuinely different race, same claim is immaterial
        self.assertEqual([row["key"][2] for row in calc(twin)["rows"]], [1, 2])

    def test_grouping_by_principal(self):
        es = seed() + [e(1, "key", key_id="counsel-2", principal="counsel", powers=["forecast"]),
                       forecast(2), forecast(3, 100), resolve(4, 3)]
        r = calc(es)
        self.assertEqual(len(r["terminal_weights"]), 5)
        self.assertEqual(r["excluded_forecasts"], [(3, "revision")])
        self.assertEqual(r["rows"][0]["q"], F(29, 50))

    def test_uniform_prior(self):
        r = calc(seed()+[forecast(1), resolve(2, 1)])
        self.assertEqual(r["rows"][0]["weights_before"], dict.fromkeys(("counsel", "reviewer", "builder", "guy", "base"), F(1, 5)))

    def test_no_learning_rate(self):
        r = calc(seed()+[forecast(1), resolve(2, 1), forecast(3, 200, race=2), resolve(4, 3, 0)])
        self.assertEqual(r["terminal_weights"]["counsel"], F(27, 52))
        self.assertEqual(r["mixture_likelihood_ratio_vs_base"], sum(r["own_likelihood_ratio_vs_base"].values()) / 5)

    def test_exact_probabilities(self):
        r = calc(seed()+[forecast(1, 333), resolve(2, 1), forecast(3, 667, race=2), resolve(4, 3)])
        for row in r["rows"]:
            for p in [row["base"], row["q"], *row["weights_before"].values()]:
                self.assertIsInstance(p, F)
            self.assertEqual(sum(row["weights_before"].values()), 1)
        self.assertTrue(all(isinstance(w, F) for w in r["terminal_weights"].values()))

    def test_per_type_base(self):
        es = seed()+[forecast(1, args={}), resolve(2, 1), forecast(3, args={}, type="world.renavon"),
                    resolve(4, 3, 0), forecast(5, race=9), resolve(6, 5)]
        self.assertEqual(calc(es)["rows"][0]["base_counts"], (1, 1))
        self.assertEqual(calc(es)["rows"][0]["base"], F(2, 3))

    def test_bounded_difference(self):
        es = seed()
        for i in range(999):
            es += [forecast(2*i+1, args={}), resolve(2*i+2, 2*i+1, 0)]
        es += [forecast(1999, 999), resolve(2000, 1999)]
        row = calc(es)["rows"][0]
        self.assertEqual((row["base_counts"], row["base"]), ((0, 999), F(1, 1000)))
        self.assertEqual(v.clip(F(1000, 1001)), F(999, 1000))
        self.assertEqual(v.clip(F(0)), F(1, 1000))
        self.assertLessEqual(abs(row["D_over_B"]), 1)

    def test_lambda_predictable(self):
        es = seed()+[forecast(1), resolve(2, 1), forecast(3, race=2), resolve(4, 3)]
        rows = calc(es)["rows"]
        x = math.log(F(29, 25))/math.log(999)
        self.assertEqual(rows[0]["lambda"], 0)
        self.assertEqual(rows[1]["lambda"], x/(2+x*x))
        self.assertEqual(v.stake([0.5]*16), 1-1/18)
        es[-1]["body"]["outcome"] = 0
        self.assertEqual(calc(es)["rows"][1]["lambda"], rows[1]["lambda"])

    def test_factor_algebra(self):
        # Every node of a depth-three binary tree. Adaptive abstention gives equality;
        # opposite clipped endpoints give +/-1 exactly, so the oracle needs no log tolerance.
        for depth in range(3):
            for path in itertools.product((0, 1), repeat=depth):
                prior = [1.0 if y else -1.0 for y in path]
                lam = v.stake(prior)
                for b, q in ((F(1, 2), F(1, 2)), (F(1, 1000), F(999, 1000)), (F(999, 1000), F(1, 1000))):
                    xs = [v.difference(q, b, y) for y in (0, 1)]
                    self.assertEqual(xs, [0.0, 0.0] if q == b else [-1.0, 1.0] if q > b else [1.0, -1.0])
                    fs = [v.factor(lam, x) for x in xs]
                    expectation = (1-b)*F(fs[0]) + b*F(fs[1])
                    self.assertLessEqual(expectation, 1)
                    self.assertTrue(all(f > 0 for f in fs))
                    if q == b:
                        self.assertEqual(expectation, 1)
                        self.assertEqual(expectation + F(1, 50), F(51, 50))
        abstain = calc(seed()+[forecast(1, ts=CUT), resolve(2, 1)])["rows"][0]
        self.assertEqual((abstain["q"], abstain["base"], abstain["D_over_B"]), (F(1, 2), F(1, 2), 0.0))

    def test_window_from_the_push(self):
        es = seed()+[e(337, "push", ts=OPEN), e(367, "push", ts=CUT), forecast(368), resolve(369, 368)]
        self.assertEqual(v.value(es, no_attack_gate=True)["events"], 0)
        es[3]["body"]["args"]["off_utc"] = "2026-11-01T02:00:00Z"
        for gate, n in ((None, 0), ("2026-11-01T02:00:00Z", 0), (CUT, 1)):
            self.assertEqual(v.value(es, attack_green=gate)["events"], n)
        es += [e(366, "forecast", args={"id": "V0"}, resolves_by="2026-12-01T00:00:00Z")]
        self.assertEqual(st.c2a_window(sorted(es, key=lambda e: e["seq"])), (367, CUT, "2026-11-15T01:00:00Z"))

    def test_wealth_continues(self):
        es = seed()+[forecast(1), resolve(2, 1), forecast(3, race=2, cutoff="2026-11-01T02:00:00Z"), resolve(4, 3)]
        all_ = calc(es)
        retry = calc(es, window_opening=CUT)
        self.assertGreater(retry["E_value"], 1)
        self.assertEqual(retry["rows"], all_["rows"])
        self.assertEqual(retry["terminal_weights"], all_["terminal_weights"])
        self.assertEqual(retry["window_events"], 1)
        self.assertNotEqual(retry["window_weights"], retry["terminal_weights"])


class Attacks(SignedFixture):
    def test_three_refused(self):
        pool = gen.KeyPool(self.enterContext(tempfile.TemporaryDirectory()))
        for kind in ("rigged", "colluding"):
            case = gen.generate_kind(kind, random.Random(42), pool)
            self.assertTrue(check.check(case.lines)["ok"])
            es = list(map(json.loads, case.lines))
            r = v.value(es, opening=es[0]["ts"], no_attack_gate=True)
            self.assertEqual(r["events"], 1)
            self.assertEqual(set(r["terminal_weights"]), {"guy", "ann", "base"})
            row = r["rows"][0]
            self.assertEqual(row["forecasts"]["ann"][1], F(9, 10))
            self.assertEqual(row["q"], F(19, 30))
            self.assertEqual(len(r["excluded_forecasts"]), 2 if kind == "rigged" else 1)
            self.assertTrue(all(why.startswith("rigged" if kind == "rigged" else "revision") for _, why in r["excluded_forecasts"]))

    def test_promote_refused_value(self):
        self.s.complete(9, type="world.fixture")
        while len(self.s.es) < 337:
            self.s.add("proposal", title="padding to boundary", commit="a"*40)
        self.s.add("decision", "guy", kind="promote", subject="C1b")
        self.s.forecast(args={"id": "V0"}, resolves_by="2026-11-20T00:00:00Z")
        self.s.add("push", "guy", ts="2026-11-01T00:00:00Z", digest="a"*64, review="0"*64, record="0"*64)
        scope = {"counted": ["tests/"], "cap": 7800}
        files = {"judge/scope.json": json.dumps(scope), "SPEC.md": "at C1 it is:\n```\n"+json.dumps(scope)+"\n```\n",
                 "log.jsonl": self.s.log.text(), "tests/test_clerk.py": "# attacks\n", "tests/test_value.py": "# attacks\n",
                 "pins/pins.py": "\n".join(f'Pin("{name}", test, mutants)' for name in st.VALUE_PINS)}
        for path in ("tools/status.py", "tools/clerk.py"):
            with open(os.path.join(st.ROOT, path)) as f:
                files[path] = f.read()
        with tree(files) as (root, start):
            f = self.s.add("forecast", "counsel", ts="2026-11-01T00:30:00Z", **forecast(1, 500)["body"])
            self.s.resolve(f, ts=END)
            self.s.merge(ts=END)
            head = commit(root, {"log.jsonl": self.s.log.text()})
            run = dict(GREEN, head_sha=head, updated_at=END)
            runs = [dict(GREEN, head_sha=start, updated_at=EARLY), run]
            s = st.assess(self.s.es, "C2a", END, root, head, run=run, runs=runs, acts=[])
            self.assertEqual(st.unmet(s), ["criterion 5: value E 1.000000 >= 20"])
            self.assertEqual(len(s["continued_liveness"]["items"]), 10)
            self.assertEqual(s["end"], "2026-11-15T00:00:00Z")
            for evidence in (None, dict(run, event="pull_request"), dict(run, head_branch="builder-value"), dict(run, conclusion="failure")):
                bad = st.assess(self.s.es, "C2a", END, root, head, run=evidence, runs=[], acts=None)
                self.assertTrue(all(not ok for ok, text in bad["checks"] if text.startswith(("criterion 1:", "criterion 2:", "criterion 4:", "criterion 7: off"))))
            changed = commit(root, {"judge/scope.json": json.dumps(dict(scope, cap=7801))})
            restored = commit(root, {"judge/scope.json": json.dumps(scope)})
            self.assertFalse(st.c2a_tree_evidence(root, changed, self.s.es, 339)[0])
            self.assertFalse(st.c2a_tree_evidence(root, restored, self.s.es, 339)[0])
            self.assertEqual(st.c2a_tree_evidence(root, head, self.s.es, 339), (True, True, True))
            a = SimpleNamespace(kind="promote", subject="C2a", acts=None)
            def command(*cmd):
                if cmd[0] == "gh":
                    return SimpleNamespace(stdout=json.dumps([{"workflow_runs": runs}]))
                self.assertEqual(cmd[cmd.index("--subject")+1], "C2a")
                return SimpleNamespace(stdout=st.render(s))
            with patch.object(jack, "begin"), patch.object(jack, "git", return_value=head), patch.object(jack, "run", side_effect=command), \
                    patch.object(jack, "main_ending") as ending, patch.object(jack, "append") as append:
                with self.assertRaises(jack.Refused):
                    jack.v_decision(a)
                ending.assert_not_called()
                append.assert_not_called()
            self.s.add("forecast", "counsel", ts=END, **dict(forecast(1, args={})["body"], resolves_by=END))
            late = st.assess(self.s.es, "C2a", "2026-11-01T13:10:17Z", root, head, run=run, runs=runs, acts=[])
            self.assertLess(late["continued_liveness"]["E"], 20)
            self.assertEqual(late["continued_liveness"]["items"][-1]["kind"], "expiry")
            self.assertEqual(late["continued_liveness"]["items"][:-1], s["continued_liveness"]["items"])
