"""C2b reviewer fixtures, run inside each disposable mutant tree."""
import json
import os
import unittest
from fractions import Fraction
from unittest.mock import patch

from tests.clerk_fixture import SignedFixture, commit, tree
from tests.test_c2b import C2b
from tests.test_due import DueTest, discharge, lines, row
from tests.test_elect import Election, ElectionMathTest
from tests.test_push_gate import REVIEW, PushGate
from tests.test_value import CUT, END, OPEN, Value, calc, e, forecast, resolve, seed
from tests.test_workflow import WorkflowTest
from tests import test_status
from kernel import check
from sim import election as el, gen, run as sim_run
from tools import due, elect, status as st, value as val

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


class ElectionCases(Election):
    def test_gain_in_unit_interval(self):
        ElectionMathTest("test_gain_endpoints_representation_and_bad_round_kept").test_gain_endpoints_representation_and_bad_round_kept()
        self.assertEqual(el.gain([1] * 6), Fraction(0))
        self.assertEqual(el.gain([999] * 6), Fraction(1))

    def test_round_loss_is_mean(self):
        self.assertEqual(el.gain([999] * 6), Fraction(1))
        self.assertAlmostEqual(float(el.gain([999] * 5 + [1])), 5 / 6)

    def test_bad_round_kept(self):
        self.test_bad_round_waits_then_keeps_five_sixths_and_freezes_at_deadline()
        self.setUp()
        inv = self.invite()
        self.events(inv)
        es = list(map(json.loads, self.chain.lines))
        row = elect.audit(es, "2026-11-18T03:00:00Z", lambda _: True)["rows"][0]
        self.assertEqual((row["gain"], row["success"]), (Fraction(1), 1))

    def test_exp3_importance(self):
        ElectionMathTest("test_importance_weight_uses_saved_grid_mass_and_exact_identity").test_importance_weight_uses_saved_grid_mass_and_exact_identity()
        inv = self.invite()
        self.events(inv)
        es = list(map(json.loads, self.chain.lines))
        audit = elect.audit(es, "2026-11-18T03:00:00Z", lambda _: True)
        arm = audit["rows"][0]["arm"]
        saved = Fraction(inv["body"]["args"]["propensity"])
        self.assertEqual(audit["gains"][0][arm], Fraction(1) / saved)

    def test_exp3_constants(self):
        ElectionMathTest("test_theorem_constants_and_grid_boundaries").test_theorem_constants_and_grid_boundaries()
        inv = self.invite()
        self.assertEqual((inv["body"]["args"]["gamma"], inv["body"]["args"]["eta"]), (repr(el.GAMMA), repr(el.ETA)))
        self.assertEqual((round(el.GAMMA, 5), round(el.ETA, 5)), (0.15111, 0.05037))

    def test_instance_feedback_complete(self):
        ElectionMathTest("test_round_zero_strictly_after_opening_and_skips_keep_the_index").test_round_zero_strictly_after_opening_and_skips_keep_the_index()
        self.test_bad_round_waits_then_keeps_five_sixths_and_freezes_at_deadline()
        self.setUp()
        inv = self.invite()
        self.events(inv)
        second = self.invite(w0="2026-11-18T05:00:00Z", ts="2026-11-18T03:00:00Z")
        self.assertEqual((second["body"]["args"]["round"], second["body"]["args"]["instance"]), (4, 0))

    def test_draw_replays_from_prefix(self):
        import base64
        self.test_signed_prefix_replay_and_four_independent_instances()
        self.setUp()
        def forge_gains(b):
            forged = (Fraction(5), Fraction(0), Fraction(0))
            d = el.draw(forged, base64.b64decode(b["args"]["sigma"]))
            arm = d["arm"]
            principal, model = el.ROSTER[arm]
            b["args"].update(gains=["5/1", "0/1", "0/1"], cuts=[str(c) for c in d["cuts"]],
                             propensity=f"{d['cuts'][arm + 1] - d['cuts'][arm]}/{el.GRID}",
                             principal=principal, model=model)
            b["claim"] = (f"stream freshness, window 2026-11-18T01:00:00Z: the invited entrant <{principal}, {model}> "
                          "achieves a mean clipped log-loss on the window's six events below the base rate's")
        bad = self.invite(edit=forge_gains)
        es = list(map(json.loads, self.chain.lines))
        with self.assertRaisesRegex(ValueError, "rigged_election"):
            elect.replay(es, bad["seq"], lambda _: True)

    def test_sigma_verifies(self):
        self.test_sigma_namespace_raw_bytes_determinism_and_key_power()
        inv = self.invite()
        es = list(map(json.loads, self.chain.lines))
        self.assertEqual(elect.replay(es, inv["seq"], lambda _: True)["seq"], inv["seq"])
        other_sig = elect.sign_sigma(self.signers["herald"].path, elect.clerk(es), "freshness", "2026-11-18T02:00:00Z")
        self.setUp()
        bad = self.invite(edit=lambda b: b["args"].update(sigma=other_sig))
        es_bad = list(map(json.loads, self.chain.lines))
        with self.assertRaisesRegex(ValueError, "rigged_election"):
            elect.replay(es_bad, bad["seq"], lambda _: True)

    def test_draw_on_the_grid(self):
        boundaries = el.cuts((Fraction(0),) * 3)
        try:
            arm, mass = el.select(boundaries, el.GRID - 1)
        except StopIteration:
            self.fail("maximal hash unassigned on the grid")
        self.assertEqual((arm, mass), (2, Fraction(boundaries[3] - boundaries[2], el.GRID)))

    def test_roster_fixed(self):
        inv = self.invite()
        es = list(map(json.loads, self.chain.lines))
        self.assertEqual(elect.replay(es, inv["seq"], lambda _: True)["seq"], inv["seq"])
        self.setUp()
        bad = self.invite(edit=lambda b: b["args"].update(roster=[list(p) for p in el.ROSTER] + [["counsel", "openai/gpt-5.4-mini"]]))
        with self.assertRaisesRegex(ValueError, "rigged_election"):
            elect.replay(list(map(json.loads, self.chain.lines)), bad["seq"], lambda _: True)
        # Value roster is also fixed at the opening push: a post-opening key declaration is excluded.
        ves = seed() + [e(1, "key", ts="2026-10-31T12:00:00Z", key_id="herald-2", principal="herald", powers=["forecast"]),
                        forecast(2, who="herald"), forecast(3, who="counsel"), resolve(4, 2), resolve(5, 3)]
        vr = calc(ves)
        self.assertEqual(vr["excluded_forecasts"], [(2, "not in opening roster")])
        self.assertEqual(set(vr["rows"][0]["forecasts"]), {"counsel"})

    def test_invite_before_session(self):
        self.test_missing_page_wrong_session_and_self_resolution_are_imputed()
        self.setUp()
        inv = self.invite()
        self.events(inv)
        es = list(map(json.loads, self.chain.lines))
        row = elect.audit(es, "2026-11-18T06:00:00Z", lambda _: True)["rows"][0]
        self.assertEqual((row["gain"], row["success"]), (Fraction(1), 1))

    def test_invite_cutoff_W0(self):
        self.test_late_invite_revision_and_known_outcome_are_refused()
        self.setUp()
        inv = self.invite(w0="2026-11-18T01:00:00Z", ts="2026-11-18T00:15:00Z")
        es = list(map(json.loads, self.chain.lines))
        self.assertEqual(elect.audit(es, "2026-11-18T00:15:00Z", lambda _: True)["refused"], [])

    def test_invite_p_is_success_rate(self):
        ElectionMathTest("test_invite_p_is_half_up_laplace_success_rate_not_propensity").test_invite_p_is_half_up_laplace_success_rate_not_propensity()
        self.test_invite_success_strict_exact_comparison_and_half_up_rate()
        self.setUp()
        inv = self.invite()
        self.assertEqual(inv["body"]["p"], 500)

    def test_invite_resolution_strict(self):
        self.test_invite_success_strict_exact_comparison_and_half_up_rate()

    def test_resolver_not_forecaster(self):
        self.test_missing_page_wrong_session_and_self_resolution_are_imputed()
        self.setUp()
        inv = self.invite()
        self.events(inv)
        es = list(map(json.loads, self.chain.lines))
        plan = elect.resolve_plan(es, inv["seq"], "2026-11-18T03:00:00Z", lambda _: True)
        self.assertEqual(plan["resolver"], "builder" if inv["body"]["args"]["principal"] == "reviewer" else "reviewer")
        self.assertEqual(plan["outcome"], 1)

    def check_sim_election_kind(self, kind, reason):
        import random
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            pool = gen.KeyPool(tmp)
            for s in range(6):
                attack = gen.generate_election(kind, random.Random(s), pool)
                self.assertTrue(check.check(attack.lines)["ok"])
                es = list(map(json.loads, attack.lines))
                res = elect.audit(es, es[-1]["ts"], lambda _: True)
                self.assertEqual([w[:len(reason)] for _, w in res["refused"]], [reason])
                self.assertEqual(sim_run.evaluate(attack, pool), [])
                twin = gen.generate_election(kind, random.Random(s), pool, attack=False)
                self.assertTrue(check.check(twin.lines)["ok"])
                es_twin = list(map(json.loads, twin.lines))
                res_twin = elect.audit(es_twin, es_twin[-1]["ts"], lambda _: True)
                self.assertEqual((res_twin["refused"], len(res_twin["history"])), ([], 1))

    def test_self_invite_pin(self):
        self.test_self_invite()
        self.check_sim_election_kind("self_invite", "unkeyed")
        self.setUp()
        self.test_sigma_namespace_raw_bytes_determinism_and_key_power()

    def test_rigged_election_pin(self):
        self.test_rigged_election()
        self.check_sim_election_kind("rigged_election", "rigged_election")
        # Draw from a later prefix: round 4 drawn using round 0's future resolution, but entered before round 0 resolves.
        self.setUp()
        first = self.invite()
        self.events(first)
        later_es = list(map(json.loads, self.chain.lines))
        later_audit = elect.audit(later_es, "2026-11-18T03:00:00Z", lambda _: True)
        w0 = "2026-11-18T05:00:00Z"
        sigma = elect.sign_sigma(self.signers["herald"].path, elect.clerk(later_es), "freshness", w0)
        later_body = elect.invite_body(later_es, later_audit["history"], "2026-11-18T03:00:00Z", "freshness", w0, sigma, lambda _: True)
        # Twin: entered on the later prefix after round 0's resolutions -> replays cleanly.
        twin_inv = self.add("forecast", "herald", "2026-11-18T03:00:00Z", later_body)
        self.assertEqual(elect.replay(list(map(json.loads, self.chain.lines)), twin_inv["seq"], lambda _: True)["seq"], twin_inv["seq"])
        # Attack: the same body entered at 00:16:00Z before round 0's forecasts/resolutions, followed by round 0's events.
        self.setUp()
        first = self.invite()
        early_inv = self.add("forecast", "herald", "2026-11-18T00:16:00Z", later_body)
        self.events(first)
        attack_es = list(map(json.loads, self.chain.lines))
        self.assertTrue(any(seq == early_inv["seq"] and why.startswith("rigged_election")
                            for seq, why in elect.audit(attack_es, "2026-11-18T03:00:00Z", lambda _: True)["refused"]))


class ValueStatusCases(C2b):
    def test_mixture_untouched_and_continued(self):
        Value("test_worked_table").test_worked_table()
        second = "2026-11-01T02:00:00Z"
        es = seed() + [
            e(338, "push", ts=OPEN),
            forecast(339, 900, "counsel"), resolve(340, 339, 1),
            forecast(341, 900, "counsel", race=2, cutoff=second), resolve(342, 341, 1),
            e(343, "push", ts=second),
            e(344, "forecast", "counsel", ts=second, p=500, claim="inv", type="election.invite", resolves_by=END),
            forecast(345, 900, "counsel", race=3, cutoff="2026-11-01T03:00:00Z"), resolve(346, 345, 1),
        ]
        full = val.value(es, no_attack_gate=True)
        continued = val.value(es, no_attack_gate=True, window_opening=second)
        self.assertEqual(continued["rows"], full["rows"])
        self.assertEqual(continued["E_value"], full["E_value"])
        self.assertEqual(continued["terminal_weights"], full["terminal_weights"])
        self.assertEqual(continued["own_likelihood_ratio_vs_base"], full["own_likelihood_ratio_vs_base"])
        self.assertNotEqual(continued["rows"][2]["weights_before"],
                            dict.fromkeys(continued["rows"][2]["weights_before"], Fraction(1, 5)))
        self.assertGreater(continued["rows"][2]["lambda"], 0)

    def test_procedure_types_out(self):
        es = seed() + [forecast(1, 800, "counsel"), resolve(2, 1, 1)]
        for i, typ in enumerate(("counsel.programme", "proposal.ci", "proposal.count", "review.forecast", "election.invite")):
            fseq = 10 + 2 * i
            es += [forecast(fseq, 900, "counsel", type=typ, args={"id": f"P{i}"}), resolve(fseq + 1, fseq, 1)]
        r = calc(es)
        self.assertEqual(r["events"], 1)
        self.assertEqual(r["unkeyed"], [10, 12, 14, 16, 18])

    def test_window_from_the_push_c2b(self):
        test_status.C2aPrimeTest.c2a_stream(self)
        self.s.forecast(ts="2026-11-17T00:00:00Z", args={"id": "X0"}, resolves_by="2026-11-18T12:00:00Z")
        self.s.forecast(ts="2026-11-17T00:00:01Z", args={"id": "X7"}, resolves_by="2026-12-01T12:00:00Z")
        self.s.add("decision", "guy", ts="2026-11-18T00:00:00Z", kind="promote", subject="C2a")
        self.s.merge(ts="2026-11-18T00:00:01Z")
        op = self.s.add("push", "guy", ts="2026-11-18T00:00:02Z", digest="a" * 64, review="0" * 64)
        self.assertEqual(st.c2b_window(self.s.es), (op, "2026-11-18T00:00:02Z", "2026-12-01T12:00:00Z"))
        s = st.status(self.s.es, "A3", 14, "2026-11-18T02:00:00Z", subject="C2b")
        self.assertEqual((s["start"], s["end"], s["entries_in_window"]), ("2026-11-18T00:00:02Z", "2026-12-01T12:00:00Z", 0))
        for change in (lambda e: e["body"]["args"].update(id="X1"),
                       lambda e: e["body"].update(resolves_by="2026-11-18T00:00:02Z"),
                       lambda e: e.update(seq=op + 1)):
            es = json.loads(json.dumps(self.s.es))
            change(next(e for e in es if e["body"].get("args", {}).get("id") == "X7"))
            self.assertEqual(st.promotion_line(st.assess(es, "C2b", "2026-11-18T02:00:00Z", None, None)),
                             "promote C2b: refused: C2b has no promotion forecast before its opening")

    def test_promote_refused_c2b(self):
        self.test_criteria_continue_ledgers_require_verified_attacks_and_ignore_invites()
        self.setUp()
        self.test_decision_dispatch_signs_only_the_single_lawful_c2b_verdict()
