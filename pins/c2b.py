"""C2b reviewer fixtures, run inside each disposable mutant tree."""
import base64, json, os, random, tempfile
from fractions import Fraction
from kernel import check
from sim import election as el, gen, run as sim_run
from tests import test_status
from tests.clerk_fixture import commit, tree
from tests.test_c2b import C2b, END as C2B_END, GREEN
from tests.test_due import DueTest, discharge, lines, row
from tests.test_elect import Election, ElectionMathTest
from tests.test_push_gate import REVIEW, PushGate
from tests.test_value import END, OPEN, Value, calc, e, forecast, resolve, seed
from tests.test_workflow import WorkflowTest
from tools import due, elect, status as st, value as val

SEED_IDS = ("c2a-acts", "c2a-report", "hkjc-hv-20261104", "D-1", "runbook-c2b", "V0", "V1", "V2", "V3", "c2b-report", "c2c-brief")


class GateCases(PushGate):
    def test_read_not_counsels_twins(self):
        self.test_read_not_counsels()
        self.publish(f"VERDICT: BLOCK\nReviewed tree: `{self.base}`\n", "reviewer")
        self.write(REVIEW, self.accepted()); self.git("add", ".")
        self.git("commit", "-qm", "counsel edits headers\n\nProposer: counsel counsel-1"); self.main()
        self.rejected("REVIEW-C2b-v1.md:.*identical review blob")
        self.publish(self.accepted(), "reviewer"); self.gate()


class W5Cases(C2b):
    def test_w5_overdue_escalates(self):
        DueTest("test_render_boundary_and_late_history_never_clears").test_render_boundary_and_late_history_never_clears()
        first, _ = self.opening()
        files = dict(self.files(), **{"log.jsonl": "\n".join(self.s.log.lines[:first + 1]) + "\n",
                                      due.PATH: lines(row("task", "2026-11-18T01:00:00Z"))})
        with tree(files) as (root, _):
            head = commit(root, {"log.jsonl": self.s.log.text()})
            self.assertIn("W5 task due 2026-11-18T01:00:00Z deliver it: OPEN",
                          st.render(st.assess(self.s.es, "C2b", "2026-11-18T01:00:00Z", root, head)))
            self.assertIn("W5 task due 2026-11-18T01:00:00Z deliver it: ESCALATED 1.00h past due",
                          st.render(st.assess(self.s.es, "C2b", "2026-11-18T02:00:00Z", root, head)))

    def test_w5_escalation_history(self):
        t1, t2, d0, t3, t4, as_of = (f"2026-11-03T{h:02}:00:00Z" for h in (10, 11, 12, 13, 14, 15))
        with tree({due.PATH: lines(row("task", d0))}) as (root, seed_sha):
            discharged = commit(root, {due.PATH: lines(row("task", d0), discharge("task", 2))})
            again = commit(root, {"note": "second merge holding discharge"})
            row_merge = dict(seq=1, ts=t1, type="merge", body=dict(commit=seed_sha))
            cite_early, cite_late = (dict(seq=2, ts=t, type="proposal", body=dict(title="task")) for t in (t1, t3))
            merge_early, merge_late = (dict(seq=3, ts=t, type="merge", body=dict(commit=discharged)) for t in (t2, t3))
            merge_second = dict(seq=4, ts=t4, type="merge", body=dict(commit=again))
            show = lambda es, at=as_of: due.render(due.assess(root, discharged, es, at, seed_sha))
            self.assertTrue(show([row_merge, cite_early, merge_early]).endswith(": done seq 2 on time"))
            self.assertTrue(show([row_merge, cite_early, merge_late]).endswith(": done seq 2 ESCALATED 1.00h late"))
            self.assertTrue(show([row_merge, cite_late, merge_early]).endswith(": done seq 2 ESCALATED 1.00h late"))
            self.assertTrue(show([row_merge, cite_early, merge_early, merge_second]).endswith(": done seq 2 on time"))
            self.assertTrue(show([row_merge, cite_early]).endswith(": ESCALATED 3.00h past due"))
            self.assertTrue(show([row_merge, cite_early, merge_early], "2026-11-03T10:30:00Z").endswith(": OPEN"))

    def test_w5_done_is_an_entry(self):
        DueTest("test_done_requires_an_entry_on_prefix_naming_the_id_in_its_body").test_done_requires_an_entry_on_prefix_naming_the_id_in_its_body()
        DueTest("test_malformed_rows_do_not_discharge_or_replace_obligations").test_malformed_rows_do_not_discharge_or_replace_obligations()

    def test_w5_rows_append_only(self):
        d0 = "2026-11-03T12:00:00Z"
        with tree({due.PATH: lines(row("task", d0))}) as (root, seed_sha):
            discharged = commit(root, {due.PATH: lines(row("task", d0), row("task2", d0), discharge("task", 1))})
            es = [dict(seq=1, ts="2026-11-03T10:00:00Z", type="proposal", body=dict(title="task")),
                  dict(seq=2, ts="2026-11-03T11:00:00Z", type="merge", body=dict(commit=discharged))]
            self.assertEqual([r["done"] for r in due.assess(root, discharged, es, "2026-11-03T13:00:00Z", seed_sha)], [1, None])
        DueTest("test_append_only_checks_deleted_and_restored_history_and_seed_inventory").test_append_only_checks_deleted_and_restored_history_and_seed_inventory()

    def test_w5_inventory(self):
        with open(os.path.join(st.ROOT, due.PATH), "rb") as f:
            self.assertEqual([r["id"] for r in due.fold(f.read())], list(SEED_IDS))
        d0 = "2026-11-03T12:00:00Z"
        with tree({due.PATH: lines(row("task", d0), row("keep", d0))}) as (root, seed_sha):
            discharged = commit(root, {due.PATH: lines(row("task", d0), row("keep", d0), discharge("task", 1))})
            es = [dict(seq=1, ts="2026-11-03T10:00:00Z", type="proposal", body=dict(title="task")),
                  dict(seq=2, ts="2026-11-03T11:00:00Z", type="merge", body=dict(commit=discharged))]
            self.assertEqual(due.assess(root, discharged, es, "2026-11-03T11:30:00Z", seed_sha)[0]["done"], 1)
            extra = commit(root, {due.PATH: lines(row("task", d0), row("keep", d0), row("third", d0))})
            with self.assertRaisesRegex(ValueError, "missing third"):
                due.assess(root, discharged, es, "2026-11-03T11:30:00Z", extra)

    def test_w5_redate(self):
        d0 = "2026-11-18T00:00:00Z"
        r_rep, r_br, r_rb = row("c2b-report", d0), row("c2c-brief", d0), row("runbook-c2b", d0)
        d_rep = dict(id="c2b-report", due="2026-12-02T12:00:00Z", seq=1564, why="direction")
        d_br = dict(id="c2c-brief", due="2026-11-16T00:00:00Z", seq=1564, why="direction")
        with tree({due.PATH: lines(r_rep, r_br, d_rep, d_br)}) as (root, sha):
            rendered = due.render(due.assess(root, sha, [], "2026-11-15T00:00:00Z", sha))
            self.assertIn("W5 c2b-report due 2026-12-02T12:00:00Z", rendered)
            self.assertIn("W5 c2c-brief due 2026-11-16T00:00:00Z", rendered)
        for idx, bad in enumerate((
            lines(r_rep, r_br, r_rb, d_rep, d_br, dict(id="runbook-c2b", due="2026-12-02T12:00:00Z", seq=1564, why="x")),
            lines(r_rep, r_br, dict(d_rep, due="2026-12-01T00:00:00Z"), d_br),
            lines(r_rep, r_br, d_rep, d_rep, d_br),
            lines(r_rep, r_br, dict(d_rep, seq=1565), d_br),
            lines(d_rep, r_rep, r_br, d_br),
        ), 2):
            with self.subTest(twin=idx), self.assertRaisesRegex(ValueError, "malformed COUNSEL-DUE file"):
                due.fold(bad)

    def test_c2b_history_from_w5(self):
        cases = (
            (1, "2026-11-18T00:20:00Z", ["2026-11-18T00:30:00Z"], False, True, True),
            (2, "2026-11-18T01:00:00Z", ["2026-11-18T00:30:00Z"], False, True, False),
            (3, "2026-11-18T01:00:00Z", ["2026-11-18T00:30:00Z"], True, True, True),
            (4, "2026-11-18T00:20:00Z", ["2026-11-18T00:30:00Z"], False, False, False),
            (5, "2026-11-18T00:40:00Z", ["2026-11-18T00:30:00Z", "2026-11-18T00:50:00Z"], False, True, False),
            (6, "2026-11-18T00:30:00Z", ["2026-11-18T00:30:00Z"], False, True, True),
            (7, "2026-11-18T01:00:00Z", [], False, True, True),
        )
        for twin, deadline, landings, tick, discharged, expected in cases:
            self.setUp()
            first, _ = self.opening()
            r0 = lines(row("task", deadline))
            files = dict(self.files(), **{"log.jsonl": "\n".join(self.s.log.lines[:first + 1]) + "\n", due.PATH: r0})
            with self.subTest(twin=twin), tree(files) as (root, _):
                start = commit(root, {"log.jsonl": self.s.log.text()})
                cited = self.s.add("proposal", "counsel", ts="2026-11-18T00:10:00Z", title="task", commit="a" * 40)
                for i, lts in enumerate(landings):
                    w5_c = commit(root, {"log.jsonl": self.s.log.text(), "tools/due.py": f"# W5 {i}\n"})
                    self.s.add("merge", ts=lts, proposal=cited, commit=w5_c, checker="a" * 64)
                self.s.add("proposal", ts="2026-11-18T01:00:01Z", title="tick", commit="b" * 40)
                witness = f"W5 task due {deadline} deliver it: ESCALATED 0.00h past due\n"
                commit(root, {"log.jsonl": self.s.log.text(), **({"transcripts/evidence/w5/tick.txt": witness} if tick else {})})
                if discharged:
                    d_c = commit(root, {due.PATH: r0 + lines(discharge("task", cited))})
                    self.s.add("merge", ts="2026-11-18T01:20:00Z", proposal=cited, commit=d_c, checker="a" * 64)
                head = commit(root, {"log.jsonl": self.s.log.text()})
                run = dict(GREEN, head_sha=head)
                runs = [dict(GREEN, head_sha=start, updated_at="2026-11-18T00:00:02Z"), run]
                s = st.assess(self.s.es, "C2b", C2B_END, root, head, run=run, runs=runs, acts=[])
                self.assertEqual(next(ok for ok, text in s["checks"] if text.startswith("criterion 8:")), expected)


class WorkflowCases(WorkflowTest):
    pass


class ElectionCases(Election):
    def test_gain_in_unit_interval(self):
        ElectionMathTest("test_gain_endpoints_representation_and_bad_round_kept").test_gain_endpoints_representation_and_bad_round_kept()
        self.assertEqual((el.gain([1] * 6), el.gain([999] * 6)), (Fraction(0), Fraction(1)))

    def test_round_loss_is_mean(self):
        self.assertEqual(el.gain([999] * 6), Fraction(1))
        self.assertAlmostEqual(float(el.gain([999] * 5 + [1])), 5 / 6)

    def test_bad_round_kept(self):
        self.test_bad_round_waits_then_keeps_five_sixths_and_freezes_at_deadline()
        self.setUp(); inv = self.invite(); self.events(inv)
        row = elect.audit(list(map(json.loads, self.chain.lines)), "2026-11-18T03:00:00Z", lambda _: True)["rows"][0]
        self.assertEqual((row["gain"], row["success"]), (Fraction(1), 1))

    def test_exp3_importance(self):
        ElectionMathTest("test_importance_weight_uses_saved_grid_mass_and_exact_identity").test_importance_weight_uses_saved_grid_mass_and_exact_identity()
        inv = self.invite(); self.events(inv)
        audit = elect.audit(list(map(json.loads, self.chain.lines)), "2026-11-18T03:00:00Z", lambda _: True)
        self.assertEqual(audit["gains"][0][audit["rows"][0]["arm"]], Fraction(1) / Fraction(inv["body"]["args"]["propensity"]))

    def test_exp3_constants(self):
        ElectionMathTest("test_theorem_constants_and_grid_boundaries").test_theorem_constants_and_grid_boundaries()
        inv = self.invite()
        self.assertEqual((inv["body"]["args"]["gamma"], inv["body"]["args"]["eta"]), (repr(el.GAMMA), repr(el.ETA)))
        self.assertEqual((round(el.GAMMA, 5), round(el.ETA, 5)), (0.15111, 0.05037))

    def test_instance_feedback_complete(self):
        ElectionMathTest("test_round_zero_strictly_after_opening_and_skips_keep_the_index").test_round_zero_strictly_after_opening_and_skips_keep_the_index()
        self.test_bad_round_waits_then_keeps_five_sixths_and_freezes_at_deadline()
        self.setUp(); inv = self.invite(); self.events(inv)
        second = self.invite(w0="2026-11-18T05:00:00Z", ts="2026-11-18T03:00:00Z")
        self.assertEqual((second["body"]["args"]["round"], second["body"]["args"]["instance"]), (4, 0))

    def test_draw_replays_from_prefix(self):
        self.test_signed_prefix_replay_and_four_independent_instances()
        self.setUp()
        def forge_gains(b):
            d = el.draw((Fraction(5), Fraction(0), Fraction(0)), base64.b64decode(b["args"]["sigma"]))
            arm, (principal, model) = d["arm"], el.ROSTER[d["arm"]]
            b["args"].update(gains=["5/1", "0/1", "0/1"], cuts=[str(c) for c in d["cuts"]],
                             propensity=f"{d['cuts'][arm + 1] - d['cuts'][arm]}/{el.GRID}", principal=principal, model=model)
            b["claim"] = (f"stream freshness, window 2026-11-18T01:00:00Z: the invited entrant <{principal}, {model}> "
                          "achieves a mean clipped log-loss on the window's six events below the base rate's")
        bad = self.invite(edit=forge_gains)
        with self.assertRaisesRegex(ValueError, "rigged_election"):
            elect.replay(list(map(json.loads, self.chain.lines)), bad["seq"], lambda _: True)

    def test_sigma_verifies(self):
        self.test_sigma_namespace_raw_bytes_determinism_and_key_power()
        inv = self.invite(); es = list(map(json.loads, self.chain.lines))
        self.assertEqual(elect.replay(es, inv["seq"], lambda _: True)["seq"], inv["seq"])
        other_sig = elect.sign_sigma(self.signers["herald"].path, elect.clerk(es), "freshness", "2026-11-18T02:00:00Z")
        self.setUp(); bad = self.invite(edit=lambda b: b["args"].update(sigma=other_sig))
        with self.assertRaisesRegex(ValueError, "rigged_election"):
            elect.replay(list(map(json.loads, self.chain.lines)), bad["seq"], lambda _: True)

    def test_draw_on_the_grid(self):
        boundaries = el.cuts((Fraction(0),) * 3)
        try:
            arm, mass = el.select(boundaries, el.GRID - 1)
        except StopIteration:
            self.fail("maximal hash unassigned on the grid")
        self.assertEqual((arm, mass), (2, Fraction(boundaries[3] - boundaries[2], el.GRID)))

    def test_roster_fixed(self):
        inv = self.invite(); es = list(map(json.loads, self.chain.lines))
        self.assertEqual(elect.replay(es, inv["seq"], lambda _: True)["seq"], inv["seq"])
        self.setUp()
        bad = self.invite(edit=lambda b: b["args"].update(roster=[list(p) for p in el.ROSTER] + [["counsel", "openai/gpt-5.4-mini"]]))
        with self.assertRaisesRegex(ValueError, "rigged_election"):
            elect.replay(list(map(json.loads, self.chain.lines)), bad["seq"], lambda _: True)
        ves = seed() + [e(1, "key", ts="2026-10-31T12:00:00Z", key_id="herald-2", principal="herald", powers=["forecast"]),
                        forecast(2, who="herald"), forecast(3, who="counsel"), resolve(4, 2), resolve(5, 3)]
        vr = calc(ves)
        self.assertEqual((vr["excluded_forecasts"], set(vr["rows"][0]["forecasts"])), ([(2, "not in opening roster")], {"counsel"}))

    def test_invite_before_session(self):
        self.test_missing_page_wrong_session_and_self_resolution_are_imputed()
        self.setUp(); inv = self.invite(); self.events(inv)
        row = elect.audit(list(map(json.loads, self.chain.lines)), "2026-11-18T06:00:00Z", lambda _: True)["rows"][0]
        self.assertEqual((row["gain"], row["success"]), (Fraction(1), 1))

    def test_invite_cutoff_W0(self):
        self.test_late_invite_revision_and_known_outcome_are_refused()
        self.setUp(); self.invite(w0="2026-11-18T01:00:00Z", ts="2026-11-18T00:15:00Z")
        self.assertEqual(elect.audit(list(map(json.loads, self.chain.lines)), "2026-11-18T00:15:00Z", lambda _: True)["refused"], [])

    def test_invite_p_is_success_rate(self):
        ElectionMathTest("test_invite_p_is_half_up_laplace_success_rate_not_propensity").test_invite_p_is_half_up_laplace_success_rate_not_propensity()
        self.test_invite_success_strict_exact_comparison_and_half_up_rate()
        self.setUp(); self.assertEqual(self.invite()["body"]["p"], 500)

    def test_invite_resolution_strict(self):
        self.test_invite_success_strict_exact_comparison_and_half_up_rate()

    def test_resolver_not_forecaster(self):
        self.test_missing_page_wrong_session_and_self_resolution_are_imputed()
        self.setUp(); inv = self.invite(); self.events(inv)
        plan = elect.resolve_plan(list(map(json.loads, self.chain.lines)), inv["seq"], "2026-11-18T03:00:00Z", lambda _: True)
        self.assertEqual((plan["resolver"], plan["outcome"]),
                         ("builder" if inv["body"]["args"]["principal"] == "reviewer" else "reviewer", 1))

    def check_sim_election_kind(self, kind, reason):
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
        self.test_self_invite(); self.check_sim_election_kind("self_invite", "unkeyed")
        self.setUp(); self.test_sigma_namespace_raw_bytes_determinism_and_key_power()

    def test_rigged_election_pin(self):
        self.test_rigged_election(); self.check_sim_election_kind("rigged_election", "rigged_election")
        self.setUp(); first = self.invite(); self.events(first)
        later_es = list(map(json.loads, self.chain.lines))
        later_audit = elect.audit(later_es, "2026-11-18T03:00:00Z", lambda _: True)
        w0 = "2026-11-18T05:00:00Z"
        sigma = elect.sign_sigma(self.signers["herald"].path, elect.clerk(later_es), "freshness", w0)
        later_body = elect.invite_body(later_es, later_audit["history"], "2026-11-18T03:00:00Z", "freshness", w0, sigma, lambda _: True)
        twin_inv = self.add("forecast", "herald", "2026-11-18T03:00:00Z", later_body)
        self.assertEqual(elect.replay(list(map(json.loads, self.chain.lines)), twin_inv["seq"], lambda _: True)["seq"], twin_inv["seq"])
        self.setUp(); first = self.invite()
        early_inv = self.add("forecast", "herald", "2026-11-18T00:16:00Z", later_body)
        self.events(first)
        attack_es = list(map(json.loads, self.chain.lines))
        self.assertTrue(any(seq == early_inv["seq"] and why.startswith("rigged_election")
                            for seq, why in elect.audit(attack_es, "2026-11-18T03:00:00Z", lambda _: True)["refused"]))


class ValueStatusCases(C2b):
    def test_mixture_untouched_and_continued(self):
        Value("test_worked_table").test_worked_table()
        second = "2026-11-01T02:00:00Z"
        es = seed() + [e(338, "push", ts=OPEN), forecast(339, 900, "counsel"), resolve(340, 339, 1),
                       forecast(341, 900, "counsel", race=2, cutoff=second), resolve(342, 341, 1), e(343, "push", ts=second),
                       e(344, "forecast", "counsel", ts=second, p=500, claim="inv", type="election.invite", resolves_by=END),
                       forecast(345, 900, "counsel", race=3, cutoff="2026-11-01T03:00:00Z"), resolve(346, 345, 1)]
        full, continued = val.value(es, no_attack_gate=True), val.value(es, no_attack_gate=True, window_opening=second)
        for k in ("rows", "E_value", "terminal_weights", "own_likelihood_ratio_vs_base"):
            self.assertEqual(continued[k], full[k])
        self.assertNotEqual(continued["rows"][2]["weights_before"], dict.fromkeys(continued["rows"][2]["weights_before"], Fraction(1, 5)))
        self.assertGreater(continued["rows"][2]["lambda"], 0)

    def test_procedure_types_out(self):
        es = seed() + [forecast(1, 800, "counsel"), resolve(2, 1, 1)]
        for i, typ in enumerate(("counsel.programme", "proposal.ci", "proposal.count", "review.forecast", "election.invite")):
            es += [forecast(10 + 2 * i, 900, "counsel", type=typ, args={"id": f"P{i}"}), resolve(11 + 2 * i, 10 + 2 * i, 1)]
        r = calc(es)
        self.assertEqual((r["events"], r["unkeyed"]), (1, [10, 12, 14, 16, 18]))

    def test_window_from_the_push_c2b(self):
        test_status.C2aPrimeTest.c2a_stream(self)
        self.s.forecast(ts="2026-11-17T00:00:00Z", args={"id": "X0"}, resolves_by="2026-11-18T12:00:00Z")
        self.s.forecast(ts="2026-11-17T00:00:01Z", args={"id": "X7"}, resolves_by="2026-12-01T12:00:00Z")
        self.s.add("decision", "guy", ts="2026-11-18T00:00:00Z", kind="promote", subject="C2a")
        self.s.merge(ts="2026-11-18T00:00:01Z")
        op = self.s.add("push", "guy", ts="2026-11-18T00:00:02Z", digest="a" * 64, review="0" * 64)
        self.assertEqual(st.c2b_window(self.s.es), (op, "2026-11-18T00:00:02Z", "2026-12-01T12:00:00Z"))
        s = st.status(self.s.es, "A3", 14, C2B_END, subject="C2b")
        self.assertEqual((s["start"], s["end"], s["entries_in_window"]), ("2026-11-18T00:00:02Z", "2026-12-01T12:00:00Z", 0))
        for change in (lambda e: e["body"]["args"].update(id="X1"),
                       lambda e: e["body"].update(resolves_by="2026-11-18T00:00:02Z"),
                       lambda e: e.update(seq=op + 1)):
            es = json.loads(json.dumps(self.s.es))
            change(next(e for e in es if e["body"].get("args", {}).get("id") == "X7"))
            self.assertEqual(st.promotion_line(st.assess(es, "C2b", C2B_END, None, None)),
                             "promote C2b: refused: C2b has no promotion forecast before its opening")

    def test_promote_refused_c2b(self):
        self.test_criteria_continue_ledgers_require_verified_attacks_and_ignore_invites()
        self.setUp(); self.test_decision_dispatch_signs_only_the_single_lawful_c2b_verdict()
