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
                self.add("forecast", "counsel", when, args=dict(id="X7"), resolves_by=self.END, p=500)
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

    def test_criterion9_counts_a_repair_minute_overlapping_the_opening(self):
        row = dict(repo="renavondata/jack", time_hkt="2026-11-02 08:29", **{"class": "repair"})
        self.assertEqual(st.off_log_repairs([row], "2026-11-02T00:29:30Z", self.END, minute_overlap=True), 1)
        self.assertEqual(st.off_log_repairs([row], "2026-11-02T00:29:30Z", self.END), 0)

    def test_window_x7_outlasts_x0(self):
        x0 = e(3, self.es[0]["ts"], "forecast", "counsel", args=dict(id="X0"),
               resolves_by="2026-11-02T01:30:00Z", p=500)
        self.assertEqual(st.elect.window(self.es + [x0])[2], self.END)
        self.assertEqual(self.assessment(self.es + [x0])["end"], self.END)

    def test_window_x7_outlasts_fourteen_days(self):
        x7 = next(entry for entry in self.es if entry["body"].get("args", {}).get("id") == "X7")
        x7["body"]["resolves_by"] = "2026-12-01T12:00:00Z"
        self.assertLess(st.elect.later(self.START, 14 * 24), x7["body"]["resolves_by"])
        self.assertEqual(st.elect.window(self.es)[2], x7["body"]["resolves_by"])
        self.assertEqual(self.assessment()["end"], x7["body"]["resolves_by"])

    def test_window_requires_counsels_x7_before_opening(self):
        opening = st.elect.window(self.es)[0]
        x7 = next(entry for entry in self.es if entry["body"].get("args", {}).get("id") == "X7")
        without = [entry for entry in self.es if entry is not x7]
        # Keep the timestamp unchanged: sequence, not time or input order, decides.
        for ignored in ([], [dict(x7, seq=self.es[-1]["seq"] + 1)],
                        [dict(x7, seq=opening)], [dict(x7, proposer="builder")]):
            with self.subTest(ignored=ignored):
                entries = ignored + without
                with self.assertRaises(StopIteration): st.elect.window(entries)
                s = self.assessment(entries)
                self.assertEqual(st.render(s).splitlines()[-1],
                                 "promote C2b: refused: C2b has no promotion forecast before its opening")
                with patch.object(st, "inputs", return_value=dict(es=[self.es[0]], runs=[], rev="head")), \
                        patch.object(st, "report", return_value=s), patch.object(st, "tree_bytes", return_value=b""), \
                        patch("tools.due.main", return_value=0), patch("builtins.print") as output:
                    self.assertEqual(st.main(["--subject", "C2b", "--as-of", self.END]), 0)
                output.assert_any_call("promote C2b: refused: C2b has no promotion forecast before its opening")
                self.decision(s)

    def test_window_revised_x0_changes_nothing(self):
        expected = st.elect.window(self.es)
        x0 = e(3, self.es[0]["ts"], "forecast", "counsel", args=dict(id="X0"), resolves_by=self.END, p=500)
        for end in ("2026-11-02T01:30:00Z", "2026-12-31T00:00:00Z"):
            revised = e(4, x0["ts"], "forecast", "counsel", args=dict(id="X0", revises=x0["seq"]), resolves_by=end, p=500)
            self.assertEqual(st.elect.window(self.es + [x0, revised]), expected)
            self.assertEqual(self.assessment(self.es + [x0, revised])["value"]["events"], 80)

    def test_window_x7_exit_prefix(self):
        x7 = next(entry for entry in self.es if entry["body"].get("args", {}).get("id") == "X7")
        x7["body"]["resolves_by"] = "2026-11-02T01:30:00Z"
        short = self.assessment()
        self.assertEqual(short["value"]["events"], 70)  # post-end resolutions excluded
        self.assertTrue(all(entry["ts"] <= short["end"] for entry in short["prefix"]))
        self.assertLess(short["prefix_last_seq"], self.es[-1]["seq"])

    def test_unopened_names_all_nine_without_crashing(self):
        opening = st.elect.window(self.es)[0]
        for entries in ([x for x in self.es if x["seq"] < opening], self.es[:4]):
            s = self.assessment(entries)
            text = st.promotion_line(s)
            self.assertIn("C2b has not opened", text)
            for i in range(1, 10): self.assertIn(f"criterion {i}:", text)
            self.decision(s)


class C2bCounselTest(unittest.TestCase):
    OPEN = "2026-11-02T00:00:00Z"
    DUE, TICK, END = "2026-11-02T01:00:00Z", "2026-11-02T02:00:00Z", "2026-11-03T00:00:00Z"

    def setUp(self):
        from tools import due
        self.row = dict(id="report", due=self.DUE, what="file report", done=None)
        self.done = dict(id="report", done=dict(seq=3, what="filed"))
        self.path = due.FILE
        self.tick = "transcripts/evidence/w5/first.txt"
        self.line = f"W5 report due {self.DUE} file report: ESCALATED 1h past due"
        self.entries = [e(1, self.OPEN, "push", "guy")]
        self.s = dict(prefix=self.entries, opening=1, start=self.OPEN, as_of=self.END, end=self.END)
        self.root, self.start = self.enterContext(tree({self.path: self.records([self.row]),
                                                       "log.jsonl": self.records(self.entries)}))
        landing = commit(self.root, {"tools/due.py": "# W5 marker\n"})
        self.entries += [e(2, self.OPEN, "merge", "herald", commit=landing),
                         e(3, self.TICK, "proposal", "counsel", title="report")]

    def records(self, rows):
        return "".join(json.dumps(row) + "\n" for row in rows)

    def assess(self, rows=None, ticks=None, pins=None, verified=True, merges=None):
        files = {self.path: self.records(rows if rows is not None else [self.row, self.done]),
                 "pins/pins.py": "\n".join(f'Pin("{name}")' for name in (st.COUNSEL_PINS if pins is None else pins))}
        files.update({self.tick: f"as-of: {self.TICK}; prefix to seq 3\n{self.line}\n"} if ticks is None else ticks)
        files["log.jsonl"] = self.records(self.entries)
        rev = commit(self.root, files)
        prefix = self.entries + ([e(4, self.TICK, "merge", "herald", commit=rev)] if merges is None else merges)
        rev = commit(self.root, {"log.jsonl": self.records(prefix)})
        return st.counsel_bound(dict(self.s, prefix=prefix), verified, self.root, rev)

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

    def test_discharge_requires_verified_merge_evidence(self):
        ok, text = self.assess(merges=[])
        self.assertFalse(ok); self.assertIn("overdue undone ['report']", text); self.assertIn("malformed False", text)
        ok, text = self.assess(merges=[e(4, self.TICK, "merge", "herald", commit="0" * 40)])
        self.assertFalse(ok); self.assertIn("unverified merge", text)
        self.assertTrue(self.assess()[0])
        ok, text = self.assess(rows=[self.row, self.done, dict(id="other", extra="not allowed")])
        self.assertFalse(ok); self.assertIn("malformed COUNSEL-DUE file", text)

    def test_first_tick_not_reconstructed_or_replaced_by_later_success(self):
        later = "transcripts/evidence/w5/later.txt"
        good = f"window C2b: start .. end (as of {self.TICK}; prefix to seq 3)\n{self.line}\n"
        header = f"as-of: {self.TICK}; prefix to seq 3\n"
        for first in ("", f"as-of: {self.DUE}; prefix to seq 3\n{self.line}\n", f"{header}W5 report: OPEN\n",
                      f"{header}W5 report-other due {self.DUE} file report: ESCALATED\n"):
            bad = {self.tick: first, later: f"as-of: {self.END}; prefix to seq 4\n{self.line}\n"}
            self.assertFalse(self.assess(ticks=bad)[0])
            self.assertTrue(self.assess(ticks={self.tick: good})[0])
        self.assertFalse(self.assess(ticks={self.tick: f"as-of: 2026-11-04T00:00:00Z\n{self.line}\n",
                                          later: f"as-of: 2026-11-04T01:00:00Z\n{self.line}\n"})[0])

    def test_c2b_history_from_w5(self):
        from tools import due
        before, after, late = (f"2026-11-02T{h}:00Z" for h in ("00:30", "01:30", "03:00"))
        cases = [  # Amendment 8's seven twins, then the retained first-prefix contract (F7).
            ("1 pre-landing", after, late, None, True),
            ("2 missing history", before, late, None, False),
            ("3 first-prefix print", before, late, "first", True),
            ("4 undone", after, None, None, False),
            ("5 two landings", before, late, None, False),
            ("6 equality", self.DUE, late, None, True),
            ("7 no landing", None, late, None, True),
            ("on time", before, before, None, True),
            ("exactly due", before, self.DUE, None, True),
            ("skipped prefix", before, late, "skipped", False),
            ("equal-ts skipped prefix", before, late, "skipped", False),
            ("equal-ts first prefix", before, late, "first", True),
            ("backdated clock", before, late, "backdated", False),
            ("late clock", before, late, "late-clock", False),
            ("late-authored tick", before, late, "late-authored", False),
            ("unavailable tick tree", before, late, "unavailable", False),
            ("replaced tick bytes", before, late, "replaced", False),
            ("wrong sequence", before, late, "wrong-seq", False),
            ("equal-ts excluded landing", None, late, None, True),
            ("equal-ts excluded unreadable", None, late, None, True),
            ("non-merge marker", None, late, None, True),
            ("unreadable tree", None, late, None, False),
            ("unreadable landing subtree", before, late, "first", False),
        ]
        for name, landing, done_at, tick, expected in cases:
            with self.subTest(case=name):
                entries = [e(1, self.OPEN, "push", "guy")]
                inventory = self.records([self.row])
                root, start = self.enterContext(tree({self.path: inventory, "log.jsonl": self.records(entries),
                    "pins/pins.py": "\n".join(f'Pin("{p}")' for p in st.COUNSEL_PINS)}))
                entries += [e(2, self.OPEN, "merge", "herald", commit=start),
                            e(3, self.OPEN, "proposal", "counsel", title="file report")]
                rev = commit(root, {"log.jsonl": self.records(entries)})
                next_at = self.TICK if name.startswith("equal-ts") and name.endswith("prefix") else late
                actions = [(self.TICK, "tick"), (next_at, "next")]
                if landing: actions.append((landing, "landing"))
                if name.startswith("5 "): actions.append((after, "landing"))
                if done_at: actions.append((done_at, "done"))
                if name == "non-merge marker": actions.append((before, "proposal"))
                if name == "unreadable tree": actions.append((before, "unreadable"))
                printed = None
                for when, action in sorted(actions, key=lambda a: (a[0], a[1] == "next")):
                    files, body = {}, {}
                    typ = "proposal"
                    if action in ("landing", "proposal"):
                        marker = commit(root, {"tools/due.py": "# W5 marker\n"})
                        typ, body = ("merge" if action == "landing" else "proposal"), dict(commit=marker)
                    elif action in ("done", "unreadable"):
                        if action == "done":
                            inventory += self.records([self.done])
                            rev = commit(root, {self.path: inventory})
                        typ, body = "merge", dict(commit=rev if action == "done" else "0" * 40)
                    entries.append(e(entries[-1]["seq"] + 1, when, typ, "herald", **body))
                    if action == "tick":
                        stamp = self.DUE if tick == "backdated" else late if tick == "late-clock" else when
                        seq = entries[-1]["seq"] + (1 if tick == "wrong-seq" else 0)
                        printed = f"as-of: {stamp}; prefix to seq {seq}\n{self.line}\n"
                        if tick and tick not in ("skipped", "late-authored"): files[self.tick] = printed
                        if tick == "unavailable":
                            # Keep the print, but never commit this exact log prefix.
                            write(root, self.tick, printed)
                            continue
                        if tick == "replaced": files[self.tick] = printed.replace(self.line, "W5 report: OPEN")
                    if action == "next" and tick in ("skipped", "late-authored", "replaced"):
                        files[self.tick] = (f"as-of: {when}; prefix to seq {entries[-1]['seq']}\n{self.line}\n"
                                            if tick == "skipped" else printed)
                    rev = commit(root, dict(files, **{"log.jsonl": self.records(entries)}))
                prefix = entries[:]
                if name.startswith("equal-ts excluded"):
                    marker = commit(root, {"tools/due.py": "# W5 marker\n"})
                    entries.append(e(entries[-1]["seq"] + 1, late, "merge", "herald",
                                     commit="0" * 40 if name.endswith("unreadable") else marker))
                    rev = commit(root, {"log.jsonl": self.records(entries)})
                if name == "unreadable landing subtree":
                    # Discharge reads traverse transcripts; only the landing read needs tools.
                    oid = st.git_bytes(root, "rev-parse", f"{marker}:tools").decode().strip()
                    (Path(root) / ".git" / "objects" / oid[:2] / oid[2:]).unlink()
                with patch.object(st, "git_bytes", wraps=st.git_bytes) as reads:
                    ok, text = st.counsel_bound(dict(self.s, prefix=list(reversed(prefix))), True, root, rev)
                self.assertEqual(ok, expected, text)
                if name.startswith("equal-ts excluded"):
                    self.assertFalse(any(call.args[1:] == ("ls-tree", marker, "--", "tools/due.py")
                                         for call in reads.call_args_list))
                if name.startswith("unreadable"): self.assertIn("unverified", text)
                elif not expected:
                    self.assertIn("overdue undone ['report']" if done_at is None else
                                  "first-tick escalation missing ['report']", text)
                if name == "unreadable landing subtree":
                    self.assertIn(unittest.mock.call(root, "ls-tree", marker, "--", "tools/due.py"), reads.call_args_list)
                if done_at and done_at > self.DUE and name != "unreadable tree":
                    lines, malformed = due.project(root, inventory.encode(), prefix, self.END)
                    self.assertFalse(malformed); self.assertIn("done seq 3 ESCALATED", lines[0])

    def test_append_only_history_and_opening_inventory(self):
        self.assertTrue(self.assess()[0])
        commit(self.root, {self.path: self.records([dict(self.row, what="rewritten"), self.done])})
        self.assertFalse(self.assess()[0])  # restoring at exit cannot erase the rewrite

    def test_liveness_ast_identity(self):
        source = (Path(st.ROOT) / "tools/status.py").read_text()
        root, start = self.enterContext(tree({"tools/status.py": source}))
        with patch.object(st, "prefix_tree", return_value=start), patch.object(st.val, "opening_push", return_value=dict(seq=1)):
            harmless = commit(root, {"tools/status.py": source + "\n# harmless comment\n"})
            self.assertTrue(st.liveness_unchanged(root, harmless, self.entries, 1))
            for before, after in (("P0 = Fraction(6, 11)", "P0 = Fraction(1, 2)"),
                                  ('return {d["pubkey"].split()[1]', 'return {d["pubkey"].split()[0]'),
                                  ("successes += item[\"Y\"]", "successes += 1"),
                                  ("repairs.append(seq)", "repairs.append(0)")):
                rev = commit(root, {"tools/status.py": source.replace(before, after)})
                self.assertFalse(st.liveness_unchanged(root, rev, self.entries, 1))


if __name__ == "__main__":
    unittest.main()
