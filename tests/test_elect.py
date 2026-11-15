"""BRIEF-C2b's election: exact downstream arithmetic and signed-prefix replay."""
from fractions import Fraction
import base64
import copy
import contextlib
import io
import json
import math
import os
import tempfile
import unittest
from unittest.mock import patch

from harness import build, keys
from kernel import check, log, sig
from sim import election as el
from tools import elect


class ElectionMathTest(unittest.TestCase):
    def test_round_zero_strictly_after_opening_and_skips_keep_the_index(self):
        for opening in ("2026-11-18T00:00:00Z", "2026-11-18T00:59:59Z"):
            op = {"ts": opening}
            end = "2026-12-01T12:00:00Z"
            self.assertEqual(elect.slot(op, end, "freshness", "2026-11-18T01:00:00Z"),
                             (0, 0, "2026-11-18T02:00:00Z", "2026-11-18T06:00:00Z"))
            self.assertEqual(elect.slot(op, end, "freshness", "2026-11-18T08:00:00Z")[:2], (7, 3))
            for stream, w0 in (("freshness", "2026-11-18T00:00:00Z"), ("hkjc", "2026-11-18T01:00:00Z"),
                               ("freshness", "2026-11-18T01:01:00Z"), ("freshness", "2026-12-02T01:00:00Z")):
                with self.subTest(stream=stream, w0=w0), self.assertRaises(ValueError):
                    elect.slot(op, end, stream, w0)

    def test_draw_hashes_raw_signature_bytes_as_a_big_endian_integer(self):
        draw = el.draw((Fraction(0),) * 3, bytes(64))
        self.assertEqual(draw["u"], int("f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b", 16))
        self.assertEqual(draw["arm"], 2)
        self.assertEqual(draw["propensity"], Fraction(draw["cuts"][3] - draw["cuts"][2], 2 ** 256))
        for sigma in (b"a" * 63, b"a" * 65, "a" * 64):
            with self.subTest(sigma=sigma), self.assertRaises(ValueError):
                el.draw((Fraction(0),) * 3, sigma)

    def test_invite_p_is_half_up_laplace_success_rate_not_propensity(self):
        self.assertEqual(el.success_rate([]), 500)
        self.assertEqual(el.success_rate([1]), 667)
        self.assertEqual(el.success_rate([0]), 333)
        self.assertEqual(el.success_rate([0] * 14), 63)  # 62.5 rounds up
        self.assertEqual(el.success_rate([0] * 2000), 1)
        self.assertEqual(el.success_rate([1] * 2000), 999)
        with self.assertRaises(ValueError):
            el.success_rate([True])

    def test_importance_weight_uses_saved_grid_mass_and_exact_identity(self):
        gains = (Fraction(0),) * 3
        old = el.draw(gains, b"a" * 64)
        g = el.gain([2] * 6)
        after = el.update(gains, old["arm"], g, old["propensity"])
        self.assertEqual(after[old["arm"]], g / old["propensity"])
        self.assertEqual(el.draw(after, b"a" * 64), el.draw(after, b"a" * 64))
        self.assertNotEqual(el.cuts(after), old["cuts"])
        updated = el.update(after, old["arm"], g, old["propensity"])
        self.assertEqual(updated[old["arm"]], 2 * g / old["propensity"])
        # Integrate over the three grid intervals, not an approximate float pi.
        for k in range(3):
            boundaries = el.cuts(after)
            identity = sum(Fraction(boundaries[a + 1] - boundaries[a], el.GRID) *
                           (g / Fraction(boundaries[a + 1] - boundaries[a], el.GRID) if a == k else 0) for a in range(3))
            self.assertEqual(identity, g)

    def test_theorem_constants_and_grid_boundaries(self):
        self.assertEqual((el.K, el.HORIZON, el.D), (3, 84, 3))
        self.assertEqual(el.GAMMA, math.sqrt(3 * math.log(3) / ((math.e - 1) * 84)))
        self.assertEqual(el.ETA, el.GAMMA / 3)
        boundaries = el.cuts((Fraction(0),) * 3)
        self.assertEqual(boundaries, (0, math.floor((1 / 3) * 2 ** 256), math.floor((2 / 3) * 2 ** 256), 2 ** 256))
        for k in range(3):
            mass = Fraction(boundaries[k + 1] - boundaries[k], 2 ** 256)
            self.assertEqual(el.select(boundaries, boundaries[k]), (k, mass))
            self.assertEqual(el.select(boundaries, boundaries[k + 1] - 1), (k, mass))
        self.assertEqual(el.select(boundaries, 2 ** 256 - 1)[0], 2)

    def test_gain_endpoints_representation_and_bad_round_kept(self):
        self.assertEqual(el.gain([1] * 6), 0)
        self.assertEqual(el.gain([999] * 6), 1)
        self.assertEqual(el.gain([2] * 6), Fraction(math.fsum(math.log(2) for _ in range(6)) / 6 / math.log(999)))
        self.assertAlmostEqual(float(el.gain([999] * 5 + [1])), 5 / 6)
        for ns in ([999] * 5, [999] * 7, [0] * 6, [1000] * 6, [True] * 6):
            with self.subTest(ns=ns), self.assertRaises(ValueError):
                el.gain(ns)


class Election(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(dir=os.path.dirname(__file__))
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.signers = {w: keys.make_key(cls.tmp.name, w) for w in ("guy", "herald", "reviewer", "builder", "counsel")}

    def setUp(self):
        self.chain = build.Log()
        declarations = [build.decl("herald-2" if w == "herald" else w, w, key, build.ALL)
                        for w, key in self.signers.items()]
        self.add("genesis", "guy", "2026-11-17T22:00:00Z", build.genesis_body(declarations))
        self.add("forecast", "counsel", "2026-11-17T22:00:01Z", dict(claim="X7", p=550,
                 resolves_by="2026-12-01T12:00:00Z", args=dict(id="X7")))
        self.add("decision", "guy", "2026-11-17T23:00:00Z", dict(kind="promote", subject="C2a"))
        self.add("push", "guy", "2026-11-18T00:00:00Z", dict(digest=build.HEX64, review=build.HEX64))

    def add(self, typ, who, ts, body):
        return json.loads(self.chain.add(typ, who, body, self.signers[who], ts=ts))

    def invite(self, w0="2026-11-18T01:00:00Z", ts="2026-11-18T00:15:00Z", edit=None, who="herald"):
        es = list(map(json.loads, self.chain.lines))
        audit = elect.audit(es, ts, lambda ev: ev == "page")
        sigma = elect.sign_sigma(self.signers["herald"].path, elect.clerk(es), "freshness", w0)
        body = elect.invite_body(es, audit["history"], ts, "freshness", w0, sigma, lambda ev: ev == "page")
        if edit:
            edit(body)
        return self.add("forecast", who, ts, body)

    def events(self, invite, p=999, missing=(), evidence="page", resolved="2026-11-18T02:10:00Z", model=None):
        a, fs = invite["body"]["args"], []
        for dataset in elect.DATASETS:
            if dataset not in missing:
                args = dict(stream="freshness", window_utc=a["window_utc"], dataset=dataset,
                            invite=invite["seq"], model=model or a["model"])
                fs.append(self.add("forecast", a["principal"], "2026-11-18T00:20:00Z",
                          dict(claim=dataset, p=p, type="world.renavon", args=args,
                               resolves_by=invite["body"]["resolves_by"])))
        resolver = "builder" if a["principal"] == "reviewer" else "reviewer"
        for f in fs:
            self.add("resolution", resolver, resolved, dict(forecast=f["seq"], outcome=1, evidence=evidence))
        return fs

    def test_signed_prefix_replay_and_four_independent_instances(self):
        invite = self.invite()
        self.events(invite)
        es = list(map(json.loads, self.chain.lines))
        self.assertTrue(check.check(self.chain.lines)["ok"])
        audit = elect.audit(es, "2026-11-18T03:00:00Z", lambda ev: ev == "page")
        self.assertEqual(audit["refused"], [])
        arm = audit["rows"][0]["arm"]
        propensity = Fraction(invite["body"]["args"]["propensity"])
        self.assertEqual(audit["gains"][0][arm], 1 / propensity)
        self.assertEqual(audit["gains"][1:], [(Fraction(0),) * 3] * 3)
        before = es[:invite["seq"]]
        a = invite["body"]["args"]
        body = elect.invite_body(before, [], invite["ts"], "freshness", a["window_utc"][0], a["sigma"], lambda _: False)
        self.assertEqual(body, invite["body"])
        # Resolution entries at the same ts as a later draw are available only by seq.
        for w0, expected in (("2026-11-18T04:00:00Z", (3, 3)), ("2026-11-18T05:00:00Z", (4, 0))):
            sigma = elect.sign_sigma(self.signers["herald"].path, elect.clerk(es), "freshness", w0)
            body = elect.invite_body(es, audit["history"], "2026-11-18T02:10:00Z", "freshness", w0, sigma, lambda _: True)
            self.assertEqual((body["args"]["round"], body["args"]["instance"]), expected)
            self.assertEqual(body["args"]["gains"][arm], "0/1" if expected[1] == 3 else
                             f"{(1 / propensity).numerator}/{(1 / propensity).denominator}")
        self.assertEqual(elect.audit(list(reversed(es)), "2026-11-18T03:00:00Z", lambda _: True), audit)

    def test_bad_round_waits_then_keeps_five_sixths_and_freezes_at_deadline(self):
        invite = self.invite()
        self.events(invite, missing=(elect.DATASETS[-1],))
        es = list(map(json.loads, self.chain.lines))
        sigma = elect.sign_sigma(self.signers["herald"].path, elect.clerk(es), "freshness", "2026-11-18T05:00:00Z")
        with self.assertRaisesRegex(ValueError, "wait: instance 0 round 0 unresolved"):
            elect.invite_body(es, [invite], "2026-11-18T04:00:00Z", "freshness", "2026-11-18T05:00:00Z", sigma, lambda _: True)
        with self.assertRaisesRegex(ValueError, "skipped: W0"):
            elect.invite_body(es, [invite], "2026-11-18T05:00:00Z", "freshness", "2026-11-18T05:00:00Z", sigma, lambda _: True)
        result = elect.audit(es, "2026-11-18T06:00:00Z", lambda _: True)
        row = result["rows"][0]
        self.assertEqual(row["success"], 0)
        self.assertAlmostEqual(float(row["gain"]), 5 / 6)
        self.assertEqual(result["gains"][0][row["arm"]], row["gain"] / row["propensity"])
        # A complete round's resolution arriving after its deadline is still missing.
        a = invite["body"]["args"]
        late = [dict(seq=100, type="forecast", proposer=a["principal"], ts="2026-11-18T00:21:00Z",
                     body=dict(p=999, type="world.renavon", resolves_by=invite["body"]["resolves_by"],
                               args=dict(a, invite=invite["seq"], dataset=elect.DATASETS[-1]))),
                dict(seq=101, type="resolution", proposer="counsel", ts="2026-11-18T06:00:01Z",
                     body=dict(forecast=100, outcome=1, evidence="page"))]
        self.assertEqual(elect.audit(es + late, "2026-11-18T07:00:00Z", lambda _: True)["gains"], result["gains"])

    def test_missing_page_wrong_session_and_self_resolution_are_imputed(self):
        invite = self.invite()
        self.events(invite)
        es = list(map(json.loads, self.chain.lines))
        for change in (lambda e: e["body"]["args"].update(model="other"),
                       lambda e: e.update(ts=invite["ts"]),
                       lambda e: e["body"]["args"].update(invite=invite["seq"] + 1),
                       lambda e: e["body"].update(resolves_by="2026-11-18T07:00:00Z")):
            twin = copy.deepcopy(es)
            for e in twin:
                if e["type"] == "forecast" and e["body"].get("type") == "world.renavon":
                    change(e)
            row = elect.audit(twin, "2026-11-18T06:00:00Z", lambda _: True)["rows"][0]
            self.assertEqual((row["gain"], row["success"]), (0, 0))
        row = elect.audit(es, "2026-11-18T06:00:00Z", lambda _: False)["rows"][0]
        self.assertEqual((row["gain"], row["success"]), (0, 0))
        twin = copy.deepcopy(es)
        for e in twin:
            if e["type"] == "resolution":
                e["proposer"] = invite["body"]["args"]["principal"]
        row = elect.audit(twin, "2026-11-18T06:00:00Z", lambda _: True)["rows"][0]
        self.assertEqual((row["gain"], row["success"]), (0, 0))

    def test_self_invite(self):
        invite = self.invite(who="builder")
        self.assertTrue(check.check(self.chain.lines)["ok"])
        es = list(map(json.loads, self.chain.lines))
        result = elect.audit(es, invite["ts"], lambda _: True)
        self.assertEqual(result["history"], [])
        self.assertIn("unkeyed", result["refused"][0][1])
        with self.assertRaisesRegex(ValueError, "unkeyed"):
            elect.replay(es, invite["seq"], lambda _: True)

    def test_rigged_election(self):
        original = self.chain.lines.copy()
        edits = (lambda b: b["args"].update(gains=["1/1", "0/1", "0/1"]),
                 lambda b: b["args"].update(cuts=["0", "1", "2", str(el.GRID)]),
                 lambda b: b["args"].update(propensity="1/3"),
                 lambda b: b["args"].update(sigma=base64.b64encode(bytes(64)).decode()),
                 lambda b: b["args"].update(instance=1), lambda b: b["args"].update(round=1),
                 lambda b: b["args"].update(principal="guy"), lambda b: b["args"].update(roster=[]),
                 lambda b: b["args"].update(gamma="0.1"), lambda b: b.update(p=333))
        for edit in edits:
            self.chain.lines = original.copy()
            invite = self.invite(edit=edit)
            self.assertTrue(check.check(self.chain.lines)["ok"])
            es = list(map(json.loads, self.chain.lines))
            with self.subTest(body=invite["body"]), self.assertRaisesRegex(ValueError, "rigged_election"):
                elect.replay(es, invite["seq"], lambda _: True)
    def test_invite_success_strict_exact_comparison_and_half_up_rate(self):
        invite = self.invite()
        self.events(invite, p=500)
        es = list(map(json.loads, self.chain.lines))
        fs = {e["seq"]: e for e in es if e["type"] == "forecast"}
        # Independent equal base probabilities isolate the strict comparison,
        # including an exact tie which rounded log losses must not turn into 1.
        rates = [(r, fs[r["body"]["forecast"]], Fraction(1, 2), (0, 0)) for r in es if r["type"] == "resolution"]
        with patch.object(elect.entry, "resolution_rates", return_value=rates):
            tied = elect.feedback(invite, es, "2026-11-18T03:00:00Z", lambda _: True)
            self.assertEqual(tied["success"], 0)
            for f in fs.values():
                if f["body"].get("type") == "world.renavon":
                    f["body"]["p"] = 501
            won = elect.feedback(invite, es, "2026-11-18T03:00:00Z", lambda _: True)
            self.assertEqual(won["success"], 1)
            w0 = "2026-11-18T05:00:00Z"
            sigma = elect.sign_sigma(self.signers["herald"].path, elect.clerk(es), "freshness", w0)
            body = elect.invite_body(es, [invite], "2026-11-18T03:00:00Z", "freshness", w0, sigma, lambda _: True)
            drawn = el.ROSTER.index((body["args"]["principal"], body["args"]["model"]))
            old = el.ROSTER.index((invite["body"]["args"]["principal"], invite["body"]["args"]["model"]))
            self.assertEqual(body["p"], 667 if drawn == old else 500)

    def test_cli_replay_resolver_table_revision_and_wait_are_read_only(self):
        invite = self.invite()
        path = os.path.join(self.tmp.name, "election-log.jsonl")
        with open(path, "w") as f:
            f.write(self.chain.text())
        before = self.chain.text()
        cases = [(["--replay", str(invite["seq"])], 0, "replay verified"),
                 (["--resolve-plan", str(invite["seq"])], 0, '"outcome": null'),
                 (["--table"], 0, "no detection guarantee"),
                 (["--invite", "freshness", "2026-11-18T01:00:00Z"], 1, "revision"),
                 (["--invite", "freshness", "2026-11-18T05:00:00Z"], 3, "wait: instance 0"),
                 (["--invite", "hkjc", "2026-11-18T03:00:00Z"], 1, "outside the freshness window")]
        for args, expected, text in cases:
            out, err = io.StringIO(), io.StringIO()
            with self.subTest(args=args), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(elect.main(["--log", path, "--as-of", "2026-11-18T00:30:00Z", *args]), expected)
            self.assertIn(text, out.getvalue() + err.getvalue())
            if "--resolve-plan" in args:
                self.assertNotEqual(json.loads(out.getvalue())["resolver"], invite["body"]["args"]["principal"])
        with open(path) as f:
            self.assertEqual(f.read(), before)
        os.remove(path)

    def test_table_reports_all_grid_propensities_and_skipped_hours(self):
        first = self.invite()
        self.events(first)
        second = self.invite(w0="2026-11-18T05:00:00Z", ts="2026-11-18T03:00:00Z")
        es = list(map(json.loads, self.chain.lines))
        result = elect.table(es, "2026-11-18T05:00:00Z", lambda _: True)
        self.assertEqual([r["round"] for r in result["skipped"]], [1, 2, 3])
        self.assertEqual(sum(a["invited"] for a in result["arms"]), 2)
        self.assertEqual(sum(a["settled"] for a in result["arms"]), 1)
        for k, a in enumerate(result["arms"]):
            expected = sum((Fraction(int(f["body"]["args"]["cuts"][k + 1]) -
                                     int(f["body"]["args"]["cuts"][k]), el.GRID) for f in (first, second)), Fraction(0)) / 2
            self.assertEqual(Fraction(a["mean_propensity"]), expected)
        self.assertEqual(sum(Fraction(a["mean_propensity"]) for a in result["arms"]), 1)
        plan = elect.resolve_plan(es, first["seq"], "2026-11-18T05:00:00Z", lambda _: True)
        self.assertEqual(plan["outcome"], 1)
        self.assertNotEqual(plan["resolver"], first["body"]["args"]["principal"])

    def test_first_physical_event_resolution_supplies_the_base_and_outcome(self):
        invite = self.invite()
        fs = self.events(invite)
        es = list(map(json.loads, self.chain.lines))
        # A prior resolution of another forecast of the same physical event is
        # still that event's first resolution, as in tools/value.py's ledger.
        extra = copy.deepcopy(fs[0])
        at = invite["seq"] + 7
        extra["seq"], extra["proposer"] = at, "counsel"
        extra["body"]["args"].pop("invite")
        resolution = dict(seq=at + 1, type="resolution", proposer="herald", ts="2026-11-18T02:00:00Z",
                          body=dict(forecast=at, outcome=0, evidence="page"))
        # Place the new forecast and resolution before the existing resolutions.
        combined = es[:at] + [extra, resolution] + [dict(e, seq=e["seq"] + 2) for e in es[at:]]
        result = elect.feedback(invite, combined, "2026-11-18T03:00:00Z", lambda _: True)
        self.assertEqual(result["ns"], [1] + [999] * 5)
        self.assertAlmostEqual(float(result["gain"]), 5 / 6)

    def test_cli_invite_prints_body_without_an_entry_and_current_power_is_required(self):
        path = os.path.join(self.tmp.name, "election-log.jsonl")
        with open(path, "w") as f:
            f.write(self.chain.text())
        args = ["--log", path, "--as-of", "2026-11-18T00:15:00Z", "--invite", "freshness", "2026-11-18T01:00:00Z"]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(elect.main([*args, "--key", self.signers["herald"].path]), 0)
        body = json.loads(out.getvalue())
        self.assertEqual(body["type"], "election.invite")
        self.assertEqual((body["args"]["round"], body["args"]["instance"], body["p"]), (0, 0, 500))
        self.assertNotIn("seq", body)
        self.assertEqual(len(base64.b64decode(body["args"]["sigma"])), 64)
        # A C2b-style key has merge alone: even a supplied sigma gives no power.
        self.add("key", "guy", "2026-11-18T00:01:00Z",
                 build.decl("herald-2", "herald", self.signers["herald"], ["merge"]))
        with open(path, "w") as f:
            f.write(self.chain.text())
        err = io.StringIO()
        with contextlib.redirect_stderr(err), patch.object(elect, "sign_sigma", side_effect=AssertionError("must not sign")):
            self.assertEqual(elect.main([*args, "--sigma", body["args"]["sigma"]]), 1)
        self.assertIn("unkeyed", err.getvalue())
        with open(path) as f:
            self.assertEqual(f.read(), self.chain.text())
        os.remove(path)

    def test_late_invite_revision_and_known_outcome_are_refused(self):
        invite = self.invite()
        duplicate = self.add("forecast", "herald", "2026-11-18T00:16:00Z", invite["body"])
        es = list(map(json.loads, self.chain.lines))
        result = elect.audit(es, duplicate["ts"], lambda _: True)
        self.assertEqual(result["refused"], [(duplicate["seq"], "revision")])
        late = copy.deepcopy(invite)
        late["ts"] = "2026-11-18T01:00:00Z"
        late["sig"] = keys.sign(self.signers["herald"], log.canonical({k: v for k, v in late.items() if k != "sig"}).encode())
        with self.assertRaisesRegex(ValueError, "rigged_election: skipped: W0"):
            elect.replay(es[:invite["seq"]] + [late], invite["seq"], lambda _: True)
        a = invite["body"]["args"]
        old = dict(seq=20, type="forecast", proposer="counsel", ts="2026-11-18T00:01:00Z",
                   body=dict(type="world.renavon", p=500, args=dict(stream="freshness", dataset=elect.DATASETS[0],
                             window_utc=a["window_utc"])))
        resolution = dict(seq=21, type="resolution", proposer="builder", ts="2026-11-18T00:02:00Z",
                          body=dict(forecast=20, outcome=1))
        with self.assertRaisesRegex(ValueError, "already known"):
            elect.invite_body(es[:invite["seq"]] + [old, resolution], [], invite["ts"], "freshness",
                              a["window_utc"][0], a["sigma"], lambda _: True)

    def test_sigma_namespace_raw_bytes_determinism_and_key_power(self):
        pub = log.pubkey_blob(self.signers["herald"].pubkey)
        w0 = "2026-11-18T01:00:00Z"
        sigma = elect.sign_sigma(self.signers["herald"].path, pub, "freshness", w0)
        self.assertEqual(sigma, elect.sign_sigma(self.signers["herald"].path, pub, "freshness", w0))
        self.assertEqual(len(elect.verify_sigma(pub, "freshness", w0, sigma)), 64)
        for blob, stream, start, encoded in ((pub, "other", w0, sigma),
                (pub, "freshness", "2026-11-18T02:00:00Z", sigma),
                (log.pubkey_blob(self.signers["builder"].pubkey), "freshness", w0, sigma),
                (pub, "freshness", w0, base64.b64encode(bytes(64)).decode()),
                (pub, "freshness", w0, keys.sign(self.signers["herald"], elect.round_message("freshness", w0)))):
            with self.subTest(stream=stream, start=start), self.assertRaises(ValueError):
                elect.verify_sigma(blob, stream, start, encoded)
        declaration = build.decl("herald-2", "herald", self.signers["herald"], ["merge"])
        es = [dict(seq=0, type="genesis", body=dict(keys=[declaration]))]
        with self.assertRaisesRegex(ValueError, "unkeyed"):
            elect.clerk(es)
        es.append(dict(seq=1, type="key", body=dict(declaration, powers=["merge", "forecast"])))
        self.assertEqual(elect.clerk(es), pub)
        es.append(dict(seq=2, type="key", body=dict(declaration, powers=[])))
        with self.assertRaisesRegex(ValueError, "unkeyed"):
            elect.clerk(es)
