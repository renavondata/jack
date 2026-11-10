"""C2b pin witnesses: signed scratch logs, rejecting cases and passing twins."""
import base64
import copy
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from fractions import Fraction as F
from unittest.mock import patch

from harness import build, runner
from kernel import check, log
from sim import election as fx, gen
from tools import elect as e, status as st, value as v


class Election(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="elect-test-", dir=e.ROOT)
        cls.pool = gen.KeyPool(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.lg = fx.setup(self.pool)
        self.f = fx.add_invite(self.lg, self.pool)

    def entries(self):
        return fx.entries(self.lg)

    def result(self, at="2026-01-01T06:00:00Z"):
        return e.round_result(self.entries(), self.f, at)

    def rewrite(self, f, body=None, ts=None, who="herald"):
        """Replace only the terminal forecast, signing its changed body honestly."""
        self.lg.lines = self.lg.lines[:f["seq"]]
        self.f = fx.add_invite(self.lg, self.pool, body or f["body"], ts or f["ts"], who)

    def audit(self):
        return e.audit(self.entries(), e.verify_sigma)

    def cli(self, *args):
        path = os.path.join(self.tmp.name, "log.jsonl")
        with open(path, "w") as out:
            out.write(self.lg.text())
        text = io.StringIO()
        with redirect_stdout(text):
            code = e.main(["--log", path, *map(str, args)])
        return code, text.getvalue()

    def test_gain_in_unit_interval(self):
        self.assertEqual(e.gain([1] * 6), 0)
        self.assertEqual(e.gain([999] * 6), 1)
        self.assertLess(math.fsum([math.log(999)] * 6) / 6 / math.log(1000), 1)
        for n in range(1, 1000):
            self.assertTrue(0 <= e.gain([n] * 6) <= 1)
        for ns in ([1] * 5, [1] * 7, [0] * 6, [1000] * 6, [True] * 6):
            with self.assertRaises(ValueError):
                e.gain(ns)

    def test_round_loss_is_mean(self):
        ns = [999, 500, 2, 1, 200, 800]
        expected = F(math.fsum(math.log(n) for n in ns) / 6 / math.log(999))
        self.assertEqual(e.gain(ns), expected)
        self.assertNotEqual(e.gain(ns), F(math.fsum(math.log(n) for n in ns) / math.log(999)))

    def test_represented_gain_identity(self):
        represented = F(math.fsum([math.log(999)] * 5 + [0.0]) / 6 / math.log(999))
        self.assertEqual(F(e.gain([999] * 5 + [1])), represented)
        self.assertNotEqual(represented, F(5, 6))
        cs = e.cuts([F(0)] * 3)
        for k in range(3):
            pi = e.propensity(k, cs)
            self.assertEqual(pi * (represented / pi), represented)
            self.assertNotEqual(pi * (F(5, 6) / pi), represented)

    def test_bad_round_kept(self):
        fx.feedback(self.lg, self.pool, self.f, count=5)
        self.assertFalse(self.result("2026-01-01T05:59:59Z")["settled"])
        r = self.result()
        represented = F(math.fsum([math.log(999)] * 5 + [0.0]) / 6 / math.log(999))
        self.assertEqual((r["gain"], r["success"], r["settled"]), (represented, 0, True))
        a = self.f["body"]["args"]
        k = e.ROSTER.index((a["principal"], a["model"]))
        G = e.state(self.entries(), [self.f], 0, "2026-01-01T06:00:00Z")
        self.assertEqual(G[k], represented / F(a["propensity"]))
        self.assertNotEqual(G[k], 0)  # dropped round
        self.assertNotEqual(G[k], 1 / F(a["propensity"]))  # dropped sixth event
        who = e.resolver(self.f)
        key = self.pool.stranger if who == "builder" else self.pool.ann
        self.lg.add("resolution", who, dict(forecast=self.f["seq"] + 6, outcome=1, evidence="late page"),
                    key, ts="2026-01-01T06:00:01Z")
        self.assertEqual(self.result("2026-01-01T07:00:00Z"), r)
        self.setUp()
        fx.feedback(self.lg, self.pool, self.f)
        self.assertEqual((self.result()["gain"], self.result()["success"]), (1, 1))

    def test_exp3_importance(self):
        fx.feedback(self.lg, self.pool, self.f)
        a = self.f["body"]["args"]
        k = e.ROSTER.index((a["principal"], a["model"]))
        G = e.state(self.entries(), [self.f], 0, "2026-01-01T04:15:00Z")
        self.assertEqual(G[k], 1 / F(a["propensity"]))
        self.assertNotEqual(G[k], 1 / e.propensity(k, e.cuts(G)))
        self.assertEqual(e.state(self.entries(), [self.f], 1, "2026-01-01T04:15:00Z"), [0] * 3)
        self.assertTrue(all(type(g) is F for g in G))

    def test_exp3_constants(self):
        gamma = min(1, math.sqrt(3 * math.log(3) / ((math.e - 1) * 84)))
        self.assertEqual((e.GAMMA, e.ETA, e.D), (gamma, gamma / 3, 3))
        self.assertNotEqual(e.GAMMA, 0.1)
        self.assertEqual(self.f["body"]["args"]["gamma"], repr(gamma))
        self.assertEqual(self.f["body"]["args"]["eta"], repr(gamma / 3))
        json.dumps(self.f["body"], allow_nan=False)
        self.assertFalse(any(isinstance(x, float) for x in self.f["body"]["args"].values()))

    def test_instance_feedback_complete(self):
        W = e.later(fx.W0, 4)
        with self.assertRaisesRegex(ValueError, "wait: instance 0 round 0 unresolved"):
            e.ready(self.entries(), [self.f], "freshness", W, "2026-01-01T04:15:00Z")
        code, output = self.cli("--invite", "freshness", W, "--as-of", "2026-01-01T04:15:00Z")
        self.assertEqual(code, 3)
        self.assertIn("wait: instance 0 round 0 unresolved", output)
        code, output = self.cli("--invite", "freshness", W, "--as-of", W)
        self.assertEqual(code, 1)
        self.assertIn("skipped", output)
        fx.feedback(self.lg, self.pool, self.f)
        self.assertEqual(e.ready(self.entries(), [self.f], "freshness", W, "2026-01-01T04:15:00Z"), 4)
        # Missing round 4 does not renumber round 8, nor hide still-outstanding feedback.
        self.assertEqual(e.slot(e.later(fx.W0, 8), fx.OPEN), 8)
        s = e.summary(self.entries(), [self.f], W)
        self.assertIn(W, s["skipped"])
        self.assertEqual(s["instances"][0], dict(instance=0, last_round=0, resolved=True))

    def test_draw_replays_from_prefix(self):
        self.assertEqual(self.audit()[1], {})
        fx.feedback(self.lg, self.pool, self.f)
        second = fx.add_invite(self.lg, self.pool, fx.body(self.lg, self.pool, e.later(fx.W0, 4), "2026-01-01T04:15:00Z"),
                               when="2026-01-01T04:15:00Z")
        self.assertEqual(e.audit(list(reversed(self.entries())), e.verify_sigma)[1], {})
        # Same timestamp, different seq: a later resolution cannot enter the draw's prefix.
        old = self.entries()[:self.f["seq"]]
        self.assertIsNone(e.replay_fields(old, [], self.f, e.verify_sigma))
        forged = copy.deepcopy(second["body"])
        forged["args"]["gains"] = ["0", "0", "0"]
        self.rewrite(second, forged)
        self.assertIn("args.gains", self.audit()[1][second["seq"]])
        self.assertEqual(self.cli("--replay", self.f["seq"])[0], 1)
        self.assertEqual(self.cli("--replay", old[-1]["seq"] + 1)[0], 0)

    def test_sigma_verifies(self):
        a = self.f["body"]["args"]
        msg = e.round_string("freshness", fx.W0)
        self.assertTrue(e.verify_sigma(self.pool.bob.pubkey, msg, a["sigma"]))
        self.assertEqual(a["sigma"], e.sign_sigma(self.pool.bob.path, msg))
        for key, message in ((self.pool.stranger, msg), (self.pool.bob, msg + "\n")):
            self.assertFalse(e.verify_sigma(key.pubkey, message, a["sigma"]))
        b = copy.deepcopy(self.f["body"])
        b["args"]["sigma"] = e.sign_sigma(self.pool.stranger.path, msg)
        self.rewrite(self.f, b)
        self.assertEqual(self.audit()[1][self.f["seq"]], "rigged_election: sigma")
        # A later key declaration cannot retroactively change the verification key.
        self.setUp()
        self.lg.add("key", "guy", build.decl("herald-2", "herald", self.pool.bob, []), self.pool.guy, ts=fx.DRAW)
        self.assertEqual(self.audit()[1], {})
        with self.assertRaises(ValueError):
            e.raw_sigma(base64.b64encode(b"x" * 63).decode())

    def test_draw_on_the_grid(self):
        cs = e.cuts([F(0)] * 3)
        self.assertEqual(e.arm(e.GRID - 1, cs), 2)
        self.assertEqual((e.GRID - 1) / e.GRID, 1.0)  # float-u mutant leaves this unassigned
        self.assertEqual(e.arm(0, cs), 0)
        for k in range(3):
            self.assertEqual(e.arm(cs[k], cs), k)
            self.assertEqual(e.arm(cs[k + 1] - 1, cs), k)
        self.assertEqual(sum(e.propensity(k, cs) for k in range(3)), 1)
        a = self.f["body"]["args"]
        U = int.from_bytes(hashlib.sha256(base64.b64decode(a["sigma"])).digest(), "big")
        self.assertEqual(e.ROSTER[e.arm(U, cs)], (a["principal"], a["model"]))
        self.assertTrue(a["propensity"].endswith("/" + str(e.GRID)))
        self.assertEqual(cs[1:3], tuple(math.floor(sum([1 / 3] * k) * 2**256) for k in (1, 2)))

    def test_roster_fixed(self):
        self.assertEqual(self.audit()[1], {})
        for field, val in (("principal", "counsel"), ("model", "other/model"), ("roster", [["builder", "other/model"]])):
            b = copy.deepcopy(self.f["body"])
            b["args"][field] = val
            self.rewrite(self.f, b)
            self.assertIn("rigged_election", self.audit()[1][self.f["seq"]])
            self.setUp()

    def test_invite_before_session(self):
        fx.feedback(self.lg, self.pool, self.f)
        self.assertEqual(self.result()["gain"], 1)
        good = self.entries()
        for mutation in ("late", "same_ts", "wrong_model", "wrong_key", "wrong_invite", "wrong_deadline"):
            es = copy.deepcopy(good)
            for f in es:
                if f["type"] != "forecast" or f["body"].get("type") != "world.renavon":
                    continue
                if mutation == "late":
                    f["seq"] = self.f["seq"] - 1
                elif mutation == "same_ts":
                    f["ts"] = self.f["ts"]
                elif mutation == "wrong_model":
                    f["body"]["args"]["model"] = "other"
                elif mutation == "wrong_key":
                    f["proposer"] = e.resolver(self.f)
                elif mutation == "wrong_invite":
                    f["body"]["args"]["invite"] += 1
                else:
                    f["body"]["resolves_by"] = fx.W0
            # seq-changing attack has dangling resolutions: test only its forecasts at deadline.
            if mutation == "late":
                es = [f for f in es if f["type"] != "resolution"]
            self.assertEqual(e.round_result(es, self.f, "2026-01-01T06:00:00Z")["gain"], 0, mutation)

    def test_invite_cutoff_W0(self):
        self.assertEqual(self.audit()[1], {})
        self.rewrite(self.f, ts=fx.W0)
        self.assertEqual(self.cli("--replay", self.f["seq"]), (1, "rigged_election: rigged: ts >= W0\n"))

    def test_invite_p_is_success_rate(self):
        self.assertEqual(self.f["body"]["p"], 500)
        a = self.f["body"]["args"]
        self.assertNotEqual(500, round(1000 * F(a["propensity"])))
        k = e.ROSTER.index((a["principal"], a["model"]))
        self.assertEqual(e.success_rate(self.entries(), [self.f], k, fx.DRAW), 500)
        fx.feedback(self.lg, self.pool, self.f)
        self.assertEqual(e.success_rate(self.entries(), [self.f], k, "2026-01-01T04:00:00Z"), 667)
        self.setUp()
        self.assertEqual(e.success_rate(self.entries(), [self.f], k, "2026-01-01T06:00:00Z"), 333)
        b = copy.deepcopy(self.f["body"])
        b["p"] = 333
        self.rewrite(self.f, b)
        self.assertIn("p differs", self.audit()[1][self.f["seq"]])

    def test_invite_resolution_strict(self):
        fx.feedback(self.lg, self.pool, self.f, p=500)
        # Controlled exact tie, using the same loader seam as value; then a strict win.
        rates = list(e.resolution_rates(self.entries()))
        tied = [(r, f, F(1, 2), counts) for r, f, _, counts in rates]
        with patch.object(e, "resolution_rates", return_value=iter(tied)):
            self.assertEqual(self.result()["success"], 0)
        better = [(r, f, F(499, 1000), counts) for r, f, _, counts in rates]
        with patch.object(e, "resolution_rates", return_value=iter(better)):
            self.assertEqual(self.result()["success"], 1)
        missing = copy.deepcopy(self.entries())
        missing[-1]["body"]["evidence"] = ""
        self.assertEqual(e.round_result(missing, self.f, "2026-01-01T06:00:00Z")["success"], 0)

    def test_resolver_not_forecaster(self):
        for principal in ("reviewer", "builder"):
            f = copy.deepcopy(self.f)
            f["body"]["args"]["principal"] = principal
            self.assertNotEqual(e.resolver(f), principal)
        code, out = self.cli("--resolve-plan", self.f["seq"])
        self.assertEqual((code, out.strip()), (0, e.resolver(self.f)))
        fx.feedback(self.lg, self.pool, self.f)
        self.assertEqual(self.result()["gain"], 1)
        bad = self.entries()
        for r in bad:
            if r["type"] == "resolution":
                r["proposer"] = self.f["body"]["args"]["principal"]
        self.assertEqual(e.round_result(bad, self.f, "2026-01-01T06:00:00Z")["gain"], 0)

    def attack_pair(self, kind, variant="gains"):
        for twin in (False, True):
            self.lg, seq = fx.attack(self.pool, kind, variant, twin)
            self.assertTrue(check.check(self.lg.lines)["ok"])
            self.assertEqual(runner.check_with(e.ROOT, self.lg.lines, cmd=["kernel2/check"]),
                             {"ok": True, "entries": len(self.lg.lines)})
            code, text = self.cli("--replay", seq)
            self.assertEqual(code, 0 if twin else 1, text)
            self.assertIn("replay verified" if twin else kind, text)

    def test_self_invite(self):
        self.attack_pair("self_invite")

    def test_rigged_election(self):
        for variant in ("gains", "sigma", "later_prefix"):
            self.attack_pair("rigged_election", variant)

    def test_mixture_untouched_and_continued(self):
        from tests.test_value import worked_entries, calc
        es = worked_entries()
        all_ = calc(es)
        carried = calc(es, window_opening="2026-11-01T03:00:00Z")
        for name in ("rows", "terminal_weights", "E_value", "mixture_likelihood_ratio_vs_base"):
            self.assertEqual(carried[name], all_[name])
        self.assertNotEqual(carried["terminal_weights"], carried["window_weights"])
        # Literal digest fixes the original fixture; the test never writes it.
        fixture = os.path.join(e.ROOT, "transcripts/evidence/value-fixture-20261101.json")
        with open(fixture, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(digest, FIXTURE_SHA256)
        self.assertNotEqual(all_["rows"][-1]["weights_before"], all_["rows"][0]["weights_before"])
        self.assertEqual(set(all_["terminal_weights"]), {"counsel", "reviewer", "builder", "guy", "base"})

    def test_procedure_types_out(self):
        from tests.test_value import seed, forecast, resolve, calc
        for typ in ("counsel.programme", "proposal.ci", "proposal.count", "review.forecast", "election.invite"):
            f = forecast(1, type=typ)
            self.assertIsNone(v.event(f))
            self.assertEqual(calc(seed() + [f, resolve(2, 1)])["events"], 0)
        self.assertEqual(calc(seed() + [forecast(1), resolve(2, 1)])["events"], 1)

    def test_invite_cli_and_revision(self):
        f = self.f
        self.lg.lines.pop()
        sigma = f["body"]["args"]["sigma"]
        args = ("--invite", "freshness", fx.W0, "--as-of", fx.DRAW, "--sigma", sigma)
        code, out = self.cli(*args)
        self.assertEqual(code, 0, out)
        self.assertIn(e.round_string("freshness", fx.W0) + "\n", out)
        self.assertEqual(json.loads(out.splitlines()[-1]), f["body"])
        real_run = subprocess.run
        def red(cmd, **kw):
            return subprocess.CompletedProcess(cmd, 1) if "unittest" in cmd else real_run(cmd, **kw)
        with patch.object(e.subprocess, "run", side_effect=red):
            code, out = self.cli(*args)
            self.assertEqual(code, 1)
            self.assertIn("attack tests not green", out)
        fx.add_invite(self.lg, self.pool, f["body"])
        self.assertIn("revision", self.cli(*args)[1])
        self.assertEqual(self.cli("--table", "--as-of", "2026-01-01T06:00:00Z")[0], 0)
        out = self.cli("--table", "--as-of", "2026-01-01T06:00:00Z")[1]
        self.assertIn("diagnostic, no detection guarantee", out)
        self.assertIn('"skipped"', out)

    def test_promotion_election_is_built_not_run(self):
        opening, start, end = e.window(self.entries())
        s = dict(prefix=self.entries(), prefix_last_seq=self.entries()[-1]["seq"], opening=opening,
                 start=start, end=end, as_of=end, subject="C2b", procedure=0, object=1, veto=False,
                 j7_unresolved_past_due=0, j7_denominator=0, overdue=[])
        facts = dict(counted=9800, kernel=450, scope=True)
        with patch.object(st, "tree_bytes", return_value=b'{"cap":9800}'), \
                patch.object(st, "election_tree_evidence", return_value=(True, True)):
            checks = st.assess_election(s, facts, True, e.ROOT, "head", [])
            self.assertTrue(all(ok for ok, text in checks if text.startswith(tuple(f"criterion {i}:" for i in (1, 2, 3, 4, 7)))))
            self.assertIn("election built and not run", checks[4][1])
            s["checks"] = checks
            self.assertIn("election: no rounds (BRIEF-C2b Amendment 10)", st.render(s))
            self.assertFalse(st.assess_election(s, dict(facts, counted=9801), True, e.ROOT, "head", [])[2][0])
            self.assertFalse(st.assess_election(s, facts, False, e.ROOT, "head", [])[0][0])
        def missing(root, rev, path):
            if path == "sim/election.py":
                raise OSError("missing")
            return b'{"cap":9800}'
        with patch.object(st, "tree_bytes", side_effect=missing), \
                patch.object(st, "election_tree_evidence", return_value=(False, True)):
            checks = st.assess_election(s, facts, True, e.ROOT, "head", [])
            self.assertFalse(checks[2][0])
            self.assertFalse(checks[4][0])

    def test_decision_c2b_dispatch_refuses(self):
        from tests.test_promotion import jack
        from types import SimpleNamespace
        a = SimpleNamespace(kind="promote", subject="C2b", acts=None)
        def command(*cmd):
            if cmd[0] == "gh":
                return SimpleNamespace(stdout='[{"workflow_runs":[]}]')
            self.assertEqual(cmd[cmd.index("--subject") + 1], "C2b")
            return SimpleNamespace(stdout="promote C2b: refused: criterion 7\n")
        with patch.object(jack, "begin"), patch.object(jack, "git", return_value="head"), \
                patch.object(jack, "run", side_effect=command), patch.object(jack, "main_ending") as signing:
            with self.assertRaises(jack.Refused):
                jack.v_decision(a)
            signing.assert_not_called()


FIXTURE_SHA256 = "0b3fd0937bd727ac3f4c7fb5d78bc6ef37657436f098c7c3e31d3a69634e736f"
