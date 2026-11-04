"""tools/status.py: the window's figures from synthetic entries (hermetic; no log on disk, no clock)."""
import hashlib
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import status as st
from harness.gitfix import write
from tests.clerk_fixture import tree
from tests.clerk_fixture import commit


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


class C2bExitTest(unittest.TestCase):
    START, END = "2026-11-02T00:00:00Z", "2026-11-03T00:00:00Z"

    def setUp(self):
        old = "2026-10-31T00:00:00Z"
        self.es = [e(0, old, "genesis", "guy", keys=[dict(key_id=k, principal=k, powers=["forecast"],
                    pubkey="ssh-ed25519 royal") for k in ("guy", "counsel", "reviewer", "builder")]),
                   e(1, old, "forecast", "counsel", args=dict(id="L0"), resolves_by=self.END, p=500),
                   e(2, old, "decision", "guy", kind="promote", subject="C1a"),
                   e(338, old, "push", "guy")]
        for i in range(80):
            when = "2026-11-01T00:00:00Z" if i < 70 else self.START
            cutoff = "2026-11-01T01:00:00Z" if i < 70 else "2026-11-02T01:00:00Z"
            resolved = "2026-11-01T02:00:00Z" if i < 70 else "2026-11-02T02:00:00Z"
            if i == 70:
                self.add("forecast", "counsel", when, args=dict(id="X0"), resolves_by=self.END, p=500)
                self.add("decision", "guy", when, kind="promote", subject="C2a")
                self.add("push", "guy", when)
            f = self.add("forecast", "counsel", when, p=999 if i % 2 else 1, type="world.hkjc",
                         args=dict(meeting="M", race=i, off_utc=cutoff), resolves_by=self.END)
            self.add("resolution", "builder", resolved, forecast=f, outcome=i % 2, evidence="fixture")
            self.add("merge", "herald", resolved)
        self.gate = "2026-10-30T23:59:59Z"
        self.enterContext(patch.object(st, "signer_blob", side_effect=lambda entry: "royal" if entry["proposer"] == "guy" else "other"))
        self.enterContext(patch.object(st, "attack_start", return_value=self.gate))
        self.same = self.enterContext(patch.object(st, "liveness_unchanged", return_value=True))
        self.bound = self.enterContext(patch.object(st, "counsel_bound", return_value=(True, "criterion 8: counsel bound")))

    def add(self, typ, who, ts, **body):
        seq = self.es[-1]["seq"] + 1
        self.es.append(e(seq, ts, typ, who, **body))
        return seq

    def assessment(self, es=None, acts=(), as_of=None):
        self.enterContext(patch.object(st, "tree_facts", return_value=dict(counted=9600, kernel=450, scope=True)))
        # Criteria 1–4 and 7 have their independent signed-round tests in test_elect.
        with patch.object(st, "assess_election", return_value=[(True, f"criterion {i}: witnessed") for i in (1, 2, 3, 4, 7)]):
            return st.assess(self.es if es is None else es, "C2b", as_of or self.END, ".", "head", acts=acts)

    def decision(self, s):
        from tests.test_promotion import jack
        a = SimpleNamespace(kind="promote", subject="C2b", acts="acts.csv")
        def command(*cmd):
            if cmd[0] == "gh":
                return SimpleNamespace(stdout='[{"workflow_runs":[]}]')
            self.assertEqual(cmd[cmd.index("--subject") + 1], "C2b")
            self.assertEqual(cmd[cmd.index("--acts") + 1], "acts.csv")
            self.assertEqual(cmd[cmd.index("--as-of") + 1], a.decision_ts)
            return SimpleNamespace(stdout=st.render(s))
        with patch.object(jack, "begin"), patch.object(jack, "git", return_value="head"), \
                patch.object(jack, "run", side_effect=command), patch.object(jack, "main_ending") as ending, \
                patch.object(jack, "append") as append:
            if st.unmet(s):
                with self.assertRaises(jack.Refused): jack.v_decision(a)
                ending.assert_not_called()
            else:
                jack.v_decision(a)
                ending.assert_called_once()
                self.assertEqual(ending.call_args.args[2](), dict(kind="promote", subject="C2b"))
            append.assert_not_called()

    def test_value_continues_and_refuses_short_exit(self):
        good = self.assessment()
        self.assertEqual(st.promotion_line(good), "promote C2b: lawful")
        self.assertEqual(len(good["checks"]), 9)
        self.decision(good)
        v = good["value"]
        self.assertEqual(v["events"], 80)
        self.assertEqual(v["window_events"], 10)
        self.assertEqual(v["E_value"], st.val.value(self.es, as_of=self.END, attack_green=self.gate)["E_value"])
        self.assertLess(st.val.value(self.es, opening=self.START, as_of=self.END, attack_green=self.gate)["E_value"], 20)
        bad = copy.deepcopy(self.es)
        for entry in bad:
            if entry["type"] == "forecast": entry["body"]["p"] = 500
        short = self.assessment(bad)
        self.assertEqual([t.split(":")[0] for t in st.unmet(short)], ["criterion 5"])
        self.decision(short)

    def test_liveness_continues_and_refuses_short_exit(self):
        good = self.assessment()
        self.assertEqual(len(good["continued_liveness"]["items"]), 80)
        self.assertGreaterEqual(good["continued_liveness"]["E"], 20)
        # One merge batches every resolution: value unchanged, only one liveness item.
        bad = [entry for entry in self.es if entry["type"] != "merge"] + [self.es[-1]]
        short = self.assessment(bad)
        self.assertEqual([t.split(":")[0] for t in st.unmet(short)], ["criterion 6"])
        self.assertEqual(short["value"]["E_value"], good["value"]["E_value"])
        self.decision(short)
        self.same.return_value = False
        self.assertIn("criterion 6", st.promotion_line(self.assessment()))

    def test_each_criterion_blocks_value_only_promotion(self):
        good = self.assessment()
        for i in range(9):
            bad = copy.deepcopy(good)
            bad["checks"][i] = (False, bad["checks"][i][1])
            self.decision(bad)
        self.bound.return_value = (False, "criterion 8: first-tick escalation missing")
        self.decision(self.assessment())

    def test_criterion9_veto_repairs_ratio_and_twins(self):
        row = dict(repo="renavondata/jack", time_hkt="2026-11-02 08:00", **{"class": "repair"})
        for acts in (None, [row]):
            bad = self.assessment(acts=acts)
            self.assertEqual([t.split(":")[0] for t in st.unmet(bad)], ["criterion 9"])
            self.decision(bad)
        outside = [dict(row, time_hkt="2026-11-02 07:59"), dict(row, time_hkt="2026-11-03 08:01")]
        self.assertFalse(st.unmet(self.assessment(acts=outside)))
        self.add("decision", "guy", self.END, kind="veto", subject="other")
        self.assertFalse(st.unmet(self.assessment()))
        self.add("decision", "guy", self.END, kind="veto", subject="C2b")
        self.decision(self.assessment())
        self.es.pop()
        good = self.assessment()
        for _ in range(5 * good["object"] - good["procedure"] - 1):
            self.add("proposal", "counsel", self.END, title="procedure")
        self.assertFalse(st.unmet(self.assessment()))  # includes prospective promote, exactly 5:1
        self.add("proposal", "counsel", self.END, title="one too many")
        bad = self.assessment()
        self.assertEqual([t.split(":")[0] for t in st.unmet(bad)], ["criterion 9"])
        self.decision(bad)

    def test_window_revised_x0_before_opening_and_exit_prefix(self):
        opening, start, end = st.elect.window(self.es)
        x0 = next(entry for entry in self.es if entry["body"].get("args", {}).get("id") == "X0")
        revised = copy.deepcopy(x0)
        revised["seq"] += 1
        revised["body"].update(args=dict(id="X0", revises=x0["seq"]), resolves_by="2026-11-02T01:30:00Z")
        shifted = [dict(entry, seq=entry["seq"] + 3) if entry["seq"] > x0["seq"] else entry for entry in self.es]
        later = copy.deepcopy(revised); later["seq"] += 1
        later["body"]["resolves_by"] = "2026-11-02T01:45:00Z"
        entries = sorted(shifted + [revised, later], key=lambda entry: entry["seq"])
        self.assertEqual(st.elect.window(entries)[2], later["body"]["resolves_by"])
        late = copy.deepcopy(later); late["seq"] = entries[-1]["seq"] + 1
        late["ts"] = self.END
        late["body"]["resolves_by"] = "2026-12-31T00:00:00Z"
        entries.append(late)
        self.assertEqual(st.elect.window(entries)[2], later["body"]["resolves_by"])
        short = self.assessment(entries)
        self.assertEqual(short["value"]["events"], 70)  # post-end resolutions excluded
        self.assertTrue(all(entry["ts"] <= short["end"] for entry in short["prefix"]))
        self.assertLess(short["prefix_last_seq"], entries[-2]["seq"])
        for who, args in (("builder", dict(id="X0", revises=x0["seq"])), ("counsel", dict(id="X0"))):
            ignored = dict(revised, proposer=who, body=dict(revised["body"], args=args))
            self.assertEqual(st.elect.window(shifted + [ignored])[2], end)
        revised["body"]["resolves_by"] = "2026-12-31T00:00:00Z"
        self.assertEqual(st.elect.window(shifted + [revised])[2], "2026-11-16T00:00:00Z")

    def test_unopened_names_all_nine_without_crashing(self):
        opening = st.elect.window(self.es)[0]
        for entries in ([x for x in self.es if x["seq"] < opening], self.es[:4]):
            s = self.assessment(entries)
            text = st.promotion_line(s)
            self.assertIn("C2b has not opened", text)
            for i in range(1, 10): self.assertIn(f"criterion {i}:", text)
            self.decision(s)


class C2bCounselTest(unittest.TestCase):
    DUE, TICK, END = "2026-11-02T01:00:00Z", "2026-11-02T02:00:00Z", "2026-11-03T00:00:00Z"

    def setUp(self):
        from tools import due
        self.row = dict(id="report", due=self.DUE, what="file report", done=None)
        self.done = dict(id="report", done=dict(seq=3, what="filed"))
        self.path = due.FILE
        self.tick = "transcripts/evidence/w5/first.txt"
        self.line = f"W5 report due {self.DUE} file report: ESCALATED 1h past due"
        self.entries = [e(1, self.DUE, "push", "guy"), e(3, self.TICK, "proposal", "counsel", title="report")]
        self.s = dict(prefix=self.entries, opening=1, start=self.DUE, as_of=self.END, end=self.END)
        self.root, self.start = self.enterContext(tree({self.path: self.records([self.row])}))
        self.enterContext(patch.object(st, "prefix_tree", return_value=self.start))

    def records(self, rows):
        return "".join(json.dumps(row) + "\n" for row in rows)

    def assess(self, rows=None, ticks=None, pins=None, verified=True):
        files = {self.path: self.records(rows if rows is not None else [self.row, self.done]),
                 "pins/pins.py": "\n".join(f'Pin("{name}")' for name in (st.COUNSEL_PINS if pins is None else pins))}
        files.update({self.tick: f"as-of: {self.TICK}\n{self.line}\n"} if ticks is None else ticks)
        rev = commit(self.root, files)
        return st.counsel_bound(self.s, verified, self.root, rev)

    def test_counsel_bound_passing_and_pin_run_twins(self):
        self.assertTrue(self.assess()[0])
        self.assertFalse(self.assess(verified=False)[0])
        for name in st.COUNSEL_PINS:
            self.assertFalse(self.assess(pins=[p for p in st.COUNSEL_PINS if p != name])[0])
        self.assertTrue(self.assess()[0])

    def test_overdue_undone_unrelated_and_late_discharge(self):
        self.assertFalse(self.assess(rows=[self.row])[0])
        self.assertTrue(self.assess()[0])
        self.entries[-1]["body"]["title"] = "unrelated"
        self.assertFalse(self.assess()[0])
        self.entries[-1]["body"]["title"] = "report"
        self.assertTrue(self.assess()[0])
        self.s["as_of"] = self.TICK
        self.entries[-1]["ts"] = self.END
        self.assertFalse(self.assess()[0])  # future entry cannot discharge

    def test_first_tick_not_reconstructed_or_replaced_by_later_success(self):
        later = "transcripts/evidence/w5/later.txt"
        good = f"window C2b: start .. end (as of {self.TICK}; prefix to seq 3)\n{self.line}\n"
        for first in ("", f"as-of: {self.DUE}\n{self.line}\n", f"as-of: {self.TICK}\nW5 report: OPEN\n",
                      f"as-of: {self.TICK}\nW5 report-other due {self.DUE} file report: ESCALATED\n"):
            bad = {self.tick: first, later: f"as-of: {self.END}\n{self.line}\n"}
            # A tick at exactly due is not after due; without a later failure it is a passing boundary twin.
            if first.startswith(f"as-of: {self.DUE}"):
                self.assertTrue(self.assess(ticks=bad)[0])
            else:
                self.assertFalse(self.assess(ticks=bad)[0])
            self.assertTrue(self.assess(ticks={self.tick: good})[0])
        self.assertFalse(self.assess(ticks={self.tick: f"as-of: 2026-11-04T00:00:00Z\n{self.line}\n",
                                          later: f"as-of: 2026-11-04T01:00:00Z\n{self.line}\n"})[0])

    def test_append_only_history_and_opening_inventory(self):
        self.assertTrue(self.assess()[0])
        commit(self.root, {self.path: self.records([dict(self.row, what="rewritten"), self.done])})
        self.assertFalse(self.assess()[0])  # restoring at exit cannot erase the rewrite

    def test_liveness_ast_identity(self):
        source = (Path(st.ROOT) / "tools/status.py").read_text()
        root, start = self.enterContext(tree({"tools/status.py": source}))
        with patch.object(st, "prefix_tree", return_value=start), patch.object(st.val, "opening_push", return_value=dict(seq=1)):
            harmless = commit(root, {"tools/status.py": source + "\n# harmless comment\n"})
            self.assertTrue(st.liveness_unchanged(root, harmless, self.entries))
            for before, after in (("P0 = Fraction(6, 11)", "P0 = Fraction(1, 2)"),
                                  ('return {d["pubkey"].split()[1]', 'return {d["pubkey"].split()[0]'),
                                  ("successes += item[\"Y\"]", "successes += 1"),
                                  ("repairs.append(seq)", "repairs.append(0)")):
                rev = commit(root, {"tools/status.py": source.replace(before, after)})
                self.assertFalse(st.liveness_unchanged(root, rev, self.entries))


if __name__ == "__main__":
    unittest.main()
