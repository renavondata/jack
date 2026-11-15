"""C2b's amended criteria: committed trees, continuing ledgers and W5 history."""
import json
import os
from fractions import Fraction
from unittest.mock import patch

from tests.clerk_fixture import SignedFixture, tree, commit
from tests import test_status
from tools import due, status as st

END = "2026-11-18T02:00:00Z"
GREEN = dict(path=st.WORKFLOW, event="push", head_branch="main", conclusion="success", updated_at=END)


class C2b(SignedFixture):
    def opening(self):
        first = test_status.C2aPrimeTest.c2a_stream(self)
        self.s.forecast(ts="2026-11-17T00:00:00Z", args={"id": "X7"}, resolves_by="2026-12-01T12:00:00Z")
        self.s.add("decision", "guy", ts="2026-11-18T00:00:00Z", kind="promote", subject="C2a")
        op = self.s.add("push", "guy", ts="2026-11-18T00:00:01Z", digest="a" * 64, review="0" * 64)
        return first, op

    def files(self):
        sc = dict(counted=["tests/"], cap=10400)
        files = {"judge/scope.json": json.dumps(sc), "SPEC.md": "## 10. Outside\nat C1 it is:\n```\n" + json.dumps(sc) + "\n```\n",
                 "log.jsonl": self.s.log.text(), st.WORKFLOW: "workflow\n", due.PATH: b"",
                 "pins/pins.py": "\n".join(f'Pin("{n}", t, m)' for n in st.VALUE_PINS + list(st.C2B_PINS) + st.C2B_BOUND_PINS)}
        for p in ("tools/status.py", "tools/clerk.py", "tools/elect.py", "sim/election.py", "tests/test_elect.py",
                  "tests/test_sim.py", "tests/test_value.py", "tests/test_clerk.py"):
            with open(os.path.join(st.ROOT, p)) as f:
                files[p] = f.read()
        return files

    def test_window_is_push_to_x7_and_missing_or_late_x7_refuses(self):
        _, op = self.opening()
        self.assertEqual(st.c2b_window(self.s.es), (op, "2026-11-18T00:00:01Z", "2026-12-01T12:00:00Z"))
        s = st.status(self.s.es, "A3", 14, END, subject="C2b")
        self.assertEqual((s["entries_in_window"], s["procedure"], s["object"]), (0, 0, 0))
        self.assertEqual(s["end"], "2026-12-01T12:00:00Z")
        for change in (lambda e: e["body"]["args"].update(id="X0"),
                       lambda e: e["body"].update(resolves_by="2026-11-18T00:00:01Z"),
                       lambda e: e.update(seq=op + 1)):
            es = json.loads(json.dumps(self.s.es))
            change(next(e for e in es if e["body"].get("args", {}).get("id") == "X7"))
            self.assertEqual(st.promotion_line(st.assess(es, "C2b", END, None, None)),
                             "promote C2b: refused: C2b has no promotion forecast before its opening")

    def test_opening_is_the_trusted_and_process_baseline_including_intermediate_trees(self):
        first, _ = self.opening()
        files = self.files()
        files["log.jsonl"] = "\n".join(self.s.log.lines[:first + 1]) + "\n"
        with tree(files) as (root, _):
            start = commit(root, {"log.jsonl": self.s.log.text()})
            s = st.status(self.s.es, "A3", 14, END, subject="C2b")
            self.assertEqual(st.c2b_tree_evidence(root, start, s)[:2], (True, True))
            source = files["tools/status.py"]
            changed = commit(root, {"tools/status.py": source.replace("P0 = Fraction(6, 11)", "P0 = Fraction(1, 2)")})
            self.assertFalse(st.c2b_tree_evidence(root, changed, s)[1])
            restored = commit(root, {"tools/status.py": source})
            self.assertTrue(st.c2b_tree_evidence(root, restored, s)[1])
            commit(root, {st.WORKFLOW: "changed\n"})
            restored = commit(root, {st.WORKFLOW: files[st.WORKFLOW]})
            self.assertFalse(st.c2b_tree_evidence(root, restored, s)[0])

    def test_criteria_continue_ledgers_require_verified_attacks_and_ignore_invites(self):
        first, _ = self.opening()
        with patch.object(st, "C2B_PINS", ["fixture"]):
            files = self.files()
            files["log.jsonl"] = "\n".join(self.s.log.lines[:first + 1]) + "\n"
            with tree(files) as (root, _):
                start = commit(root, {"log.jsonl": self.s.log.text()})
                f = self.s.forecast(ts="2026-11-18T00:10:00Z", type="world.hkjc", args=dict(meeting="m", race=1,
                                    off_utc="2026-11-18T01:00:00Z"), resolves_by=END)
                self.s.resolve(f, ts="2026-11-18T01:00:00Z")
                self.s.forecast(ts="2026-11-18T01:01:00Z", type="election.invite", args={}, resolves_by=END)
                head = commit(root, {"log.jsonl": self.s.log.text()})
                run = dict(GREEN, head_sha=head)
                runs = [dict(GREEN, head_sha=start, updated_at="2026-11-18T00:00:02Z"), run]
                context = dict(es=self.s.es, subject="C2b", as_of=END, root=root, rev=head, run=run, runs=runs, acts=[])
                s = st.assess(**context)
                self.assertEqual([text[:11] for ok, text in s["checks"] if not ok], ["criterion 5", "criterion 6"])
                expected = st.val.value(s["prefix"], as_of=END, attack_green=st.attack_start(root, runs, END, "tests/test_value.py"),
                                        window_opening=s["start"])
                self.assertEqual(s["value"], expected)
                self.assertIn("election: no rounds (BRIEF-C2b Amendment 10)", st.render(s))
                self.assertIn("unverified (the brief specifies no act-to-forecast matching rule)", st.render(s))
                self.assertNotIn("V6", st.render(s))
                wealthy = dict(expected, E_value=20)
                with patch.object(st.val, "value", return_value=wealthy), patch.object(st, "score_items", return_value=dict(E=Fraction(20), items=[])):
                    self.assertEqual(st.promotion_line(st.assess(**context)), "promote C2b: lawful")
                    bad = st.assess(**dict(context, run=dict(run, event="pull_request")))
                    self.assertEqual([int(text.split(":")[0].split()[-1]) for ok, text in bad["checks"] if not ok], [1, 2, 4, 7, 8])
                    row = dict(repo="renavondata/jack", time_hkt="2026-11-18 08:00", **{"class": "repair"})
                    self.assertTrue(any(not ok and text.startswith("criterion 9:") for ok, text in st.assess(**dict(context, acts=[row]))["checks"]))

    def test_history_uses_first_merge_and_only_contemporaneously_committed_tick_files(self):
        for deadline, landing, tick, discharged, expected in (
                ("2026-11-18T00:00:00Z", True, False, True, True),
                ("2026-11-18T00:30:00Z", True, False, True, True),
                ("2026-11-18T01:00:00Z", True, False, True, False),
                ("2026-11-18T01:00:00Z", True, True, True, True),
                ("2026-11-18T01:00:00Z", False, False, True, True),
                ("2026-11-18T00:00:00Z", True, False, False, False)):
            self.setUp()
            self.opening()
            row = (json.dumps(dict(id="task", due=deadline, what="writ", done=None)) + "\n").encode()
            with self.subTest(deadline=deadline, landing=landing, tick=tick, discharged=discharged), tree({due.PATH: row,
                    "log.jsonl": self.s.log.text()}) as (root, seed):
                cited = self.s.add("proposal", "counsel", ts="2026-11-18T00:10:00Z", title="task", commit="a" * 40)
                payload = commit(root, {"log.jsonl": self.s.log.text(), **({"tools/due.py": "# W5\n"} if landing else {})})
                self.s.add("merge", ts="2026-11-18T00:30:00Z", proposal=cited, commit=payload, checker="a" * 64)
                first = self.s.add("proposal", ts="2026-11-18T01:00:01Z", title="tick", commit="b" * 40)
                witness = f"W5 task due {deadline} writ: ESCALATED 0.00h past due\n"
                commit(root, {"log.jsonl": self.s.log.text(), **({"transcripts/evidence/w5/tick.txt": witness} if tick else {})})
                discharge = (json.dumps(dict(id="task", done=dict(seq=cited, what="delivered"))) + "\n").encode()
                payload = commit(root, {due.PATH: row + discharge if discharged else row})
                self.s.add("merge", ts="2026-11-18T01:20:00Z", proposal=cited, commit=payload, checker="a" * 64)
                head = commit(root, {"log.jsonl": self.s.log.text()})
                s = st.status(self.s.es, "A3", 14, END, subject="C2b")
                result, lines = st.counsel_bound(s, root, head, seed)
                self.assertEqual(result, expected, lines)
                if landing and deadline == "2026-11-18T01:00:00Z" and not tick:
                    # A retrospective file with the right text cannot repair the first prefix.
                    late = commit(root, {"transcripts/evidence/w5/late.txt": witness})
                    self.assertFalse(st.counsel_bound(s, root, late, seed)[0])

    def test_decision_dispatch_signs_only_the_single_lawful_c2b_verdict(self):
        from types import SimpleNamespace
        from tests import test_promotion
        jack = test_promotion.jack
        args = SimpleNamespace(kind="promote", subject="C2b", acts=None)
        sha, verdict = "a" * 40, "promote C2b: lawful"
        def command(*cmd):
            if cmd[0] == "gh":
                return SimpleNamespace(stdout=json.dumps([{"workflow_runs": [dict(GREEN, head_sha=sha)]}]))
            self.assertEqual(cmd[cmd.index("--subject") + 1], "C2b")
            self.assertEqual(cmd[cmd.index("--as-of") + 1], END)
            return SimpleNamespace(stdout=verdict)
        with patch.object(jack, "begin"), patch.object(jack, "git", return_value=sha), patch.object(jack, "run", side_effect=command), \
                patch.object(jack.entry, "now", return_value=END), patch.object(jack, "main_ending") as ending, \
                patch.object(jack, "append") as append:
            jack.v_decision(args)
            self.assertEqual(ending.call_args.args[2](), dict(kind="promote", subject="C2b"))
            ending.reset_mock()
            for verdict in [f"promote C2b: refused: criterion {n}" for n in range(1, 10)] + [
                    "promote C2a: lawful", "promote C2b: lawful\npromote C2b: refused: criterion 8", ""]:
                with self.subTest(verdict=verdict), self.assertRaises(jack.Refused):
                    jack.v_decision(args)
                ending.assert_not_called()
                append.assert_not_called()

    def test_pin_inventory_requires_every_named_pin_including_both_amendments(self):
        self.assertEqual((len(st.C2B_PINS), len(set(st.C2B_PINS)), len(st.C2B_BOUND_PINS)), (33, 33, 10))
        self.assertTrue({"w5_redate", "c2b_history_from_w5"} <= set(st.C2B_BOUND_PINS) <= set(st.C2B_PINS))
        text = "\n".join(f'Pin("{name}", t, m)' for name in st.C2B_PINS)
        with tree({"pins/pins.py": text}) as (root, full):
            self.assertTrue(st.pins_registered(root, full, st.C2B_PINS))
            for name in st.C2B_PINS:
                missing = commit(root, {"pins/pins.py": text.replace(f'Pin("{name}", t, m)', "")})
                self.assertFalse(st.pins_registered(root, missing, st.C2B_PINS), name)
                self.assertEqual(st.pins_registered(root, missing, st.C2B_BOUND_PINS), name not in st.C2B_BOUND_PINS)
