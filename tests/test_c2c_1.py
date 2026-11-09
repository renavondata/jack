"""C2c-1 window layer tests: R1-R11 twins, RUNBOOK push/decision gates, world-types.json."""
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from harness import build, gitfix, keys
from tools import clerk, enforcement, status as st, window as win

ROOT = st.ROOT
with open(os.path.join(ROOT, "transcripts/windows/C2c-1.json"), "rb") as _f:
    WFILE_BYTES = _f.read()
    WFILE = json.loads(WFILE_BYTES)
    WFILE_SHA = hashlib.sha256(WFILE_BYTES).hexdigest()
with open(os.path.join(ROOT, "transcripts/world-types.json"), "rb") as _f:
    WTYPES_BYTES = _f.read()
with open(os.path.join(ROOT, "tools/enforcement.json")) as _f:
    ENF_MAP = json.load(_f)

loader = importlib.machinery.SourceFileLoader("jack_c2c1", os.path.join(ROOT, "tools/jack"))
spec = importlib.util.spec_from_loader(loader.name, loader)
jack = importlib.util.module_from_spec(spec)
loader.exec_module(jack)

T_EARLY = "2026-11-08T00:00:00Z"
T_OPEN = "2026-11-08T10:00:00Z"
T_NOW = "2026-11-08T12:00:00Z"
T_END = "2026-11-15T10:00:00Z"
STAMP = "20261108T1145"
ACTS_HEADER = "repo,time_hkt,class,kind,ref,note\n"


class C2c1Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.signers = {who: keys.make_key(cls.tmp.name, who)
                       for who in ("guy", "counsel", "builder", "reviewer", "herald")}

    def make_env(self, wfile_override=None, due_rows=None, keep_due=False,
                 budget_hash=True, fc_hash=True, fc_after=False, fc_type="window.promotion",
                 extra_files=None):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        repo = td.name
        gitfix.git(repo, "init", "-q")
        wf_bytes = json.dumps(wfile_override).encode() if wfile_override is not None else WFILE_BYTES
        wf_sha = hashlib.sha256(wf_bytes).hexdigest()

        lg = build.Log()
        es = []

        def add(typ, who="counsel", ts=T_EARLY, **body):
            line = lg.add(typ, who, body, self.signers[who], ts=ts)
            es.append(json.loads(line))
            return es[-1]["seq"]

        decls = [build.decl("guy", "guy", self.signers["guy"], build.ALL)]
        add("genesis", "guy", **build.genesis_body(decls))
        for who in ("counsel", "builder", "reviewer", "herald"):
            add("key", "guy", **build.decl(who, who, self.signers[who], build.ALL))
        add("forecast", "counsel", claim="L0", p=500, resolves_by=T_END, args={"id": "L0"})
        add("decision", "guy", kind="promote", subject="C1a")
        add("push", "guy", ts="2026-11-08T00:05:00Z", digest="0" * 64, review="0" * 64, record="0" * 64)
        fcs = [add("forecast", "reviewer", ts="2026-11-08T00:30:00Z", claim=f"w{i}", p=950, resolves_by=T_END,
                   type="world.hkjc", args={"meeting": "M", "race": i + 1, "off_utc": f"2026-11-08T01:{i:02d}:00Z"})
               for i in range(9)]
        for f in fcs:
            add("resolution", "builder", ts="2026-11-08T02:00:00Z", forecast=f, outcome=1, evidence="run")
            add("merge", "herald", ts="2026-11-08T02:00:00Z", **build.merge(1))
        add("decision", "guy", ts="2026-11-08T03:00:00Z", kind="promote", subject="C2b")

        b_subj = f"C2c-1: window file sha256:{wf_sha}; cap 10900" if budget_hash else "C2c-1: no hash"
        add("decision", "guy", ts="2026-11-08T09:50:00Z", kind="budget", subject=b_subj)
        if not fc_after:
            fc_args = {"id": "C2c-1-V0", "window": "C2c-1"}
            if fc_hash:
                fc_args["window_sha256"] = wf_sha
            add("forecast", "counsel", ts="2026-11-08T09:55:00Z", claim="promo", p=600,
                resolves_by=T_END, type=fc_type, args=fc_args)
        add("push", "guy", ts=T_OPEN, digest="a" * 64, review="0" * 64, record="0" * 64)
        if fc_after:
            add("forecast", "counsel", ts="2026-11-08T10:05:00Z", claim="promo", p=600,
                resolves_by=T_END, type=fc_type, args={"id": "C2c-1-V0", "window": "C2c-1", "window_sha256": wf_sha})

        scope = {"counted": ["tests/"], "cap": 10900}
        all_pins = WFILE["criteria"][3]["args"]["pins"]
        pins_py = "\n".join(f'Pin("{p}", test, mutants)' for p in all_pins) + "\n"
        files = {
            "judge/scope.json": json.dumps(scope),
            "SPEC.md": f"at C1 it is:\n```\n{json.dumps(scope)}\n```\n",
            "tools/enforcement.json": json.dumps(ENF_MAP),
            "transcripts/windows/C2c-1.json": wf_bytes,
            "transcripts/world-types.json": WTYPES_BYTES,
            "pins/pins.py": pins_py,
            "tests/test_clerk.py": "# attack\n",
            "tests/test_value.py": "# attack\n",
            "tools/runner/workflows/counsel-sign.yml": "name: sign\n",
            "tools/runner/workflows/counsel.yml": "name: act\n",
            "log.jsonl": lg.text(),
        }
        for p in ("tools/status.py", "tools/clerk.py", "tools/window.py"):
            with open(os.path.join(ROOT, p), "rb") as f:
                files[p] = f.read()
        if due_rows is not None:
            files["transcripts/COUNSEL-DUE.jsonl"] = "\n".join(json.dumps(r) for r in due_rows) + "\n"
        if extra_files:
            files.update(extra_files)
        for path, data in files.items():
            gitfix.write(repo, path, data)
        open_sha = gitfix.commit_all(repo, "opening push\n\nProposer: guy guy-master")
        head = open_sha
        if due_rows is not None and not keep_due:
            head = self.propose_merge(repo, lg, es, "counsel", {}, delete=("transcripts/COUNSEL-DUE.jsonl",))
        return repo, lg, es, open_sha, head, add

    def propose_merge(self, repo, lg, es, party, files, delete=(), ts=None, extra_log_commit=False, merge_files=None):
        ts = ts or max("2026-11-08T11:00:00Z", es[-1]["ts"])
        gitfix.write(repo, "log.jsonl", lg.text())
        if gitfix.git(repo, "status", "--porcelain"):
            gitfix.commit_all(repo, "sync log\n\nProposer: guy guy-master")
        main_sha = gitfix.git(repo, "rev-parse", "HEAD")
        gitfix.git(repo, "checkout", "-q", "-B", "work", main_sha)
        for p in delete:
            full = os.path.join(repo, p)
            if os.path.exists(full):
                os.remove(full)
        for p, data in files.items():
            gitfix.write(repo, p, data)
        work_sha = gitfix.commit_all(repo, f"work\n\nProposer: {party} {party}")
        es.append(json.loads(lg.add("proposal", party, {"title": "w", "commit": work_sha}, self.signers[party], ts=ts)))
        gitfix.write(repo, "log.jsonl", lg.text())
        gitfix.commit_all(repo, f"proposal: w\n\nProposer: {party} {party}")
        if extra_log_commit:
            es.append(json.loads(lg.add("forecast", party, {"claim": "c", "p": 500, "resolves_by": T_END, "type": "world.hkjc"},
                                        self.signers[party], ts=ts)))
            gitfix.write(repo, "log.jsonl", lg.text())
            gitfix.commit_all(repo, f"forecast: c\n\nProposer: {party} {party}")
        p_head = gitfix.git(repo, "rev-parse", "HEAD")
        es.append(json.loads(lg.add("merge", "herald", {"proposal": 1, "commit": p_head, "checker": "0" * 64},
                                    self.signers["herald"], ts=ts)))
        gitfix.write(repo, "log.jsonl", lg.text())
        branch_tip = gitfix.commit_all(repo, "merge: #1\n\nProposer: herald herald")
        gitfix.git(repo, "checkout", "-q", "-B", "main", main_sha)
        if merge_files:
            gitfix.git(repo, "merge", "--no-ff", "-q", "--no-commit", branch_tip)
            for path, data in merge_files.items():
                gitfix.write(repo, path, data)
            gitfix.commit_all(repo, "Merge pull request #1")
        else:
            gitfix.git(repo, "merge", "--no-ff", "-q", "-m", "Merge pull request #1", branch_tip)
        return gitfix.git(repo, "rev-parse", "HEAD")


class R1NumeralsAndR9Binding(C2c1Fixture):
    def test_r1_numerals_housed_twins_and_mutants(self):
        with open(os.path.join(ROOT, "tools/window.py")) as f:
            self.assertEqual(win.scan_source_numerals(f.read(), WFILE), [])
        with open(os.path.join(ROOT, "tools/value.py")) as f:
            self.assertEqual(win.scan_source_numerals(f.read(), WFILE), [])
        self.assertTrue(win.check_window_file_numbers(WFILE))
        self.assertEqual(win.scan_tools_window_paths(), [])
        for bad_src in ('P0 = Fraction(6, 11)\n', 'x = 6900\n', 'x = int("6900")\n',
                        't = "2026-11-17T12:00:00Z"\n', 'x = 20.0\n', 'x = math.log(999)\n', 'x = 337\n'):
            self.assertTrue(win.scan_source_numerals(bad_src, WFILE), bad_src)
        bad_wf = copy.deepcopy(WFILE)
        bad_wf["criteria"][2]["args"]["counted"] = "missing_key"
        with self.assertRaises(ValueError):
            win.check_window_file_numbers(bad_wf)
        bad_wf2 = copy.deepcopy(WFILE)
        bad_wf2["processes"]["liveness"]["null"] = "missing_null"
        with self.assertRaises(ValueError):
            win.check_window_file_numbers(bad_wf2)

    def test_r9_window_file_fixed_twins(self):
        repo, lg, es, _, head, _ = self.make_env()
        s = st.assess(es, "C2c-1", T_NOW, repo, head)
        self.assertEqual(len(s["criterion_lines"]), 12)
        gitfix.write(repo, "transcripts/windows/C2c-1.json", WFILE_BYTES + b"\n")
        head2 = gitfix.commit_all(repo, "edit window file")
        out2 = st.render(st.assess(es, "C2c-1", T_NOW, repo, head2))
        self.assertEqual(out2, "promote C2c-1: refused: window file changed")
        for b_ok, f_ok in ((False, True), (True, False)):
            r3, _, es3, _, h3, _ = self.make_env(budget_hash=b_ok, fc_hash=f_ok)
            self.assertEqual(st.render(st.assess(es3, "C2c-1", T_NOW, r3, h3)),
                             "promote C2c-1: refused: window file not bound")
        empty_wf = copy.deepcopy(WFILE)
        empty_wf["criteria"] = []
        gitfix.write(repo, "transcripts/windows/C2c-1.json", json.dumps(empty_wf).encode())
        head5 = gitfix.commit_all(repo, "drop all criteria")
        self.assertEqual(st.render(st.assess(es, "C2c-1", T_NOW, repo, head5)),
                         "promote C2c-1: refused: window file changed")

    def test_r3_one_stated_end_twins(self):
        repo, lg, es, _, head, _ = self.make_env(fc_after=True)
        self.assertEqual(st.render(st.assess(es, "C2c-1", T_NOW, repo, head)),
                         "promote C2c-1: refused: C2c-1 has no promotion forecast before its opening")
        repo2, _, es2, _, head2, _ = self.make_env(fc_type="counsel.programme")
        self.assertEqual(st.render(st.assess(es2, "C2c-1", T_NOW, repo2, head2)),
                         "promote C2c-1: refused: C2c-1 has no promotion forecast before its opening")


class R2R4R8CriteriaAndWrits(C2c1Fixture):
    def test_r2_window_from_file_twins(self):
        repo, _, es, _, head, _ = self.make_env()
        out = st.render(st.assess(es, "C2c-1", T_NOW, repo, head))
        c_lines = [l for l in out.splitlines() if l.startswith("criterion ")]
        self.assertEqual(len(c_lines), 12)
        wf11 = copy.deepcopy(WFILE)
        wf11["criteria"] = [c for c in wf11["criteria"] if c["id"] != 8]
        r2, _, es2, _, h2, _ = self.make_env(wfile_override=wf11)
        self.assertEqual(len(st.assess(es2, "C2c-1", T_NOW, r2, h2)["criterion_lines"]), 11)
        wf_txt = copy.deepcopy(WFILE)
        wf_txt["criteria"][8]["text"] = "custom criterion nine text"
        r3, _, es3, _, h3, _ = self.make_env(wfile_override=wf_txt)
        self.assertIn("criterion 9: custom criterion nine text", st.render(st.assess(es3, "C2c-1", T_NOW, r3, h3)))
        wf_bad = copy.deepcopy(WFILE)
        wf_bad["criteria"][0]["kind"] = "x"
        r4, _, es4, _, h4, _ = self.make_env(wfile_override=wf_bad)
        self.assertIn("promote C2c-1: refused:", st.render(st.assess(es4, "C2c-1", T_NOW, r4, h4)))
        s_c2b = st.assess(es, "C2b", T_NOW, repo, head)
        self.assertNotIn("from_window_file", s_c2b)

    def test_r2_criteria_three_valued_twins(self):
        repo, lg, es, _, head, _ = self.make_env()
        s0 = st.assess(es, "C2c-1", T_NOW, repo, head)
        by_id = dict(enumerate(s0["criterion_lines"], 1))
        self.assertTrue(by_id[9].endswith("unknown (no acts)"))
        self.assertTrue(by_id[4].endswith("unknown (no run)"))
        gitfix.write(repo, "pins/pins.py", "PINS = []\n")
        h_miss_pin = gitfix.commit_all(repo, "remove pin")
        s_pin = st.assess(es, "C2c-1", T_NOW, repo, h_miss_pin, run=None)
        self.assertTrue(s_pin["criterion_lines"][3].endswith("unmet"))
        repo, lg, es, _, head, _ = self.make_env()
        h_acts = self.propose_merge(repo, lg, es, "builder", {
            f"transcripts/evidence/acts-C2c-1-jack-{STAMP}.csv": ACTS_HEADER,
            f"transcripts/evidence/acts-C2c-1-opencode-runner-{STAMP}.csv": ACTS_HEADER,
        })
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_acts)["criterion_lines"][8].endswith("met"))
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-08T15:00:00Z", repo, h_acts)["criterion_lines"][8].endswith("unknown (stale acts)"))
        repair_row = ACTS_HEADER + "renavondata/jack,2026-11-08 18:30,repair,fix,1,n\n"
        h_rep = self.propose_merge(repo, lg, es, "builder", {
            "transcripts/evidence/acts-C2c-1-jack-20261108T1150.csv": repair_row,
            "transcripts/evidence/acts-C2c-1-opencode-runner-20261108T1150.csv": ACTS_HEADER,
        })
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_rep)["criterion_lines"][8].endswith("unmet"))

    def test_r4_one_writ_function_and_r8_object_declared(self):
        repo, lg, es, _, head, add = self.make_env()
        u_seq = add("forecast", "counsel", ts="2026-11-08T10:30:00Z", claim="u", p=700,
                    resolves_by="2026-11-09T00:00:00Z", type="counsel.undertaking", args={"id": "u1", "window": "C2c-1"})
        writs = clerk.forecast_writs(es, [], T_NOW)
        seqs = [w["seq"] for w in writs]
        self.assertIn(5, seqs)  # L0 before C1b opening
        self.assertIn(u_seq, seqs)  # counsel.undertaking listed like any other
        rendered_status = st.render(st.assess(es, "C2c-1", T_NOW, repo, head))
        self.assertIn("W1 forecast 5:", rendered_status)
        self.assertIn(f"W1 forecast {u_seq}:", rendered_status)
        # R8 object_declared twins
        add("forecast", "reviewer", ts="2026-11-08T10:31:00Z", claim="r", p=500,
            resolves_by=T_END, type="world.renavon")
        add("forecast", "counsel", ts="2026-11-08T10:32:00Z", claim="p", p=500,
            resolves_by=T_END, type="counsel.programme")
        s_r8 = st.assess(es, "C2c-1", T_NOW, repo, head)
        self.assertNotEqual(s_r8["ratio_lines"][0], s_r8["ratio_lines"][1])
        self.assertNotIn("undeclared", s_r8["ratio_lines"][1])
        add("forecast", "reviewer", ts="2026-11-08T10:33:00Z", claim="u", p=500,
            resolves_by=T_END, type="world. mystery")
        s_undec = st.assess(es, "C2c-1", T_NOW, repo, head)
        self.assertIn("undeclared: world. mystery", s_undec["ratio_lines"][1])
        gitfix.write(repo, "transcripts/world-types.json", b'{"world.hkjc": {"reads_record": "no"}}\n')
        h_bad_wt = gitfix.commit_all(repo, "corrupt world-types")
        s_bad_wt = st.assess(es, "C2c-1", T_NOW, repo, h_bad_wt)
        self.assertIn("undeclared: transcripts/world-types.json", s_bad_wt["ratio_lines"][1])
        self.assertIn("undeclared: world.hkjc", s_bad_wt["ratio_lines"][1])


class R5R6R7R10R11Criteria(C2c1Fixture):
    def test_r5_undertakings_are_forecasts_twins(self):
        due_rows = [
            {"id": "exp-1", "due": "2026-11-05T00:00:00Z", "done": None},
            {"id": "due-1", "due": "2026-11-10T00:00:00Z", "done": None},
        ]
        repo, lg, es, _, head, add = self.make_env(due_rows=due_rows)
        # Missing forecast for due-1 -> unmet (twin 9)
        s_miss = st.assess(es, "C2c-1", T_NOW, repo, head)
        self.assertTrue(s_miss["criterion_lines"][9].endswith("unmet"))
        self.assertEqual(s_miss["expired_lines"], ["expired undertaking exp-1"])
        # Wrong window C2b -> unmet (twin 10)
        u_bad = add("forecast", "counsel", ts="2026-11-08T10:10:00Z", claim="u", p=800,
                    resolves_by="2026-11-09T00:00:00Z", type="counsel.undertaking",
                    args={"id": "due-1", "window": "C2b"})
        add("resolution", "reviewer", ts="2026-11-08T10:20:00Z", forecast=u_bad, outcome=1, evidence="run")
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, head)["criterion_lines"][9].endswith("unmet"))
        # Correct forecast for due-1, unresolved before resolves_by -> met (twin 4 & 12)
        u_ok = add("forecast", "counsel", ts="2026-11-08T10:25:00Z", claim="u", p=800,
                   resolves_by="2026-11-09T00:00:00Z", type="counsel.undertaking",
                   args={"id": "due-1", "window": "C2c-1"})
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, head)["criterion_lines"][9].endswith("met"))
        # Unresolved past resolves_by -> unmet (twin 3)
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-09T01:00:00Z", repo, head)["criterion_lines"][9].endswith("unmet"))
        # Resolved 1 at or before resolves_by, plus builder undertaking resolved 0 (twin 1 & 6) -> met
        b_fc = add("forecast", "builder", ts="2026-11-08T10:30:00Z", claim="bu", p=800,
                   resolves_by="2026-11-09T00:00:00Z", type="counsel.undertaking", args={"id": "b1", "window": "C2c-1"})
        add("resolution", "reviewer", ts="2026-11-08T10:35:00Z", forecast=b_fc, outcome=0, evidence="run")
        add("resolution", "reviewer", ts="2026-11-08T10:40:00Z", forecast=u_ok, outcome=1, evidence="run")
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-09T01:00:00Z", repo, head)["criterion_lines"][9].endswith("met"))
        # Due file present at assessed prefix -> unmet (twin 8)
        r_keep, _, es_keep, _, h_keep, _ = self.make_env(due_rows=[due_rows[0]], keep_due=True)
        self.assertTrue(st.assess(es_keep, "C2c-1", T_NOW, r_keep, h_keep)["criterion_lines"][9].endswith("unmet"))
        # Deletion outside a proposal is not retirement (R5's migration rule).
        r_hand, _, es_hand, _, h_hand, _ = self.make_env(due_rows=[due_rows[0]], keep_due=True)
        os.remove(os.path.join(r_hand, "transcripts/COUNSEL-DUE.jsonl"))
        h_hand = gitfix.commit_all(r_hand, "hand delete")
        self.assertTrue(st.assess(es_hand, "C2c-1", T_NOW, r_hand, h_hand)["criterion_lines"][9].endswith("unmet"))

    def test_r6_escalation_recorded_and_red_line_twins(self):
        repo, lg, es, _, head, add = self.make_env()
        # No evidence -> unknown (no escalations) (twin 3)
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-08T16:00:00Z", repo, head)["criterion_lines"][6].endswith("unknown (no escalations)"))
        f1 = add("forecast", "counsel", ts="2026-11-08T10:10:00Z", claim="c1", p=500, resolves_by="2026-11-08T13:00:00Z")
        # Twin 12 & 13: RED line 60 min before deadline
        esc_early = {"through": "2026-11-08T11:50:00Z", "rows": []}
        h_e1 = self.propose_merge(repo, lg, es, "builder", {"transcripts/evidence/escalations.json": json.dumps(esc_early)})
        self.assertEqual(st.assess(es, "C2c-1", "2026-11-08T11:50:00Z", repo, h_e1)["red_lines"], [])
        esc_red = {"through": "2026-11-08T12:15:00Z", "rows": []}
        h_e2 = self.propose_merge(repo, lg, es, "builder", {"transcripts/evidence/escalations.json": json.dumps(esc_red)})
        s_red = st.assess(es, "C2c-1", "2026-11-08T12:15:00Z", repo, h_e2)
        self.assertEqual(s_red["red_lines"], [f"RED: forecast {f1} due 2026-11-08T13:00:00Z, no session filed"])
        # Twin 4: past due by less than grace -> met
        self.assertTrue(s_red["criterion_lines"][6].endswith("met"))
        # Past due + grace (15:00Z) with no row -> unmet (twin 2)
        esc_miss = {"through": "2026-11-08T15:30:00Z", "rows": []}
        h_e3 = self.propose_merge(repo, lg, es, "builder", {"transcripts/evidence/escalations.json": json.dumps(esc_miss)})
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-08T15:30:00Z", repo, h_e3)["criterion_lines"][6].endswith("unmet"))
        # Row within [resolves_by - lead, resolves_by + grace] -> met (twin 1, 7b)
        esc_ok = {"through": "2026-11-08T15:30:00Z",
                  "rows": [{"forecast": f1, "issue": 10, "filed_at": "2026-11-08T11:30:00Z", "kind": "handed"}]}
        h_e4 = self.propose_merge(repo, lg, es, "builder", {"transcripts/evidence/escalations.json": json.dumps(esc_ok)})
        s_ok = st.assess(es, "C2c-1", "2026-11-08T15:30:00Z", repo, h_e4)
        self.assertTrue(s_ok["criterion_lines"][6].endswith("met"))
        self.assertEqual(s_ok["red_lines"], [])
        # Stale escalations (twin 11)
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-08T18:00:00Z", repo, h_e4)["criterion_lines"][6].endswith("unknown (stale escalations)"))
        # A stale file is unknown even if its recorded interval has an uncovered forecast.
        self.assertTrue(st.assess(es, "C2c-1", "2026-11-08T18:00:00Z", repo, h_e3)["criterion_lines"][6].endswith("unknown (stale escalations)"))

    def test_r7_ratchet_and_hand_row_deadline_twins(self):
        repo, lg, es, open_sha, head, _ = self.make_env()
        # Hand row deadline writs in clerk
        s = st.assess(es, "C2c-1", T_NOW, repo, head)
        w4 = clerk.window_writs(es, s, T_NOW)
        rendered = clerk.render(w4)
        self.assertIn(f"W4 hand-row runner deadline {T_END}: holders counsel; deadline {T_END}", rendered)
        self.assertNotIn("ESCALATED", clerk.render([w for w in w4 if "hand-row runner" in w["obligation"]]))
        w4_late = clerk.window_writs(es, s, "2026-11-16T00:00:00Z")
        self.assertIn("ESCALATED to guy", clerk.render([w for w in w4_late if "hand-row runner" in w["obligation"]]))
        bad_map = copy.deepcopy(ENF_MAP)
        bad_map["runner"]["deadline"] = ""
        with self.assertRaises(ValueError):
            enforcement.check_map(bad_map)
        # Ratchet row not moved -> unmet (twin 2)
        self.assertTrue(s["criterion_lines"][7].endswith("unmet"))
        # Move runner row to code + witness + runner evidence
        moved_map = copy.deepcopy(ENF_MAP)
        moved_map["runner"] = {"principle": moved_map["runner"]["principle"], "enforcer": "code: tools/runner",
                               "witness": "courier_signs_only_the_request", "deadline": ""}
        s1_sha = hashlib.sha256(b"name: sign\n").hexdigest()
        s2_sha = hashlib.sha256(b"name: act\n").hexdigest()
        runner_ev = [
            {"workflow": "counsel-sign.yml", "sha256": s1_sha},
            {"workflow": "counsel.yml", "sha256": s2_sha},
            {"workflow": "diary.yml", "sha256": "0" * 64},
        ]
        h_moved = self.propose_merge(repo, lg, es, "builder", {
            "tools/enforcement.json": json.dumps(moved_map),
            f"transcripts/evidence/runner-{STAMP}.json": json.dumps(runner_ev),
        })
        # Twin 6 of criteria_three_valued: runner evidence present, no run -> unknown (no run)
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_moved, run=None)["criterion_lines"][7].endswith("unknown (no run)"))
        run_ok = {"path": st.WORKFLOW, "event": "push", "head_branch": "main", "head_sha": h_moved,
                  "conclusion": "success", "updated_at": T_NOW}
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_moved, run=run_ok)["criterion_lines"][7].endswith("met"))
        # Twin 3: witness not KILLED in run -> unmet
        run_surv = dict(run_ok, pins={"courier_signs_only_the_request": "SURVIVED"})
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_moved, run=run_surv)["criterion_lines"][7].endswith("unmet"))

    def test_r11_tree_bounds_and_evidence_provenance_twins(self):
        repo, lg, es, open_sha, head, _ = self.make_env()
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, head)["criterion_lines"][2].endswith("met"))
        # Allowed builder change (tools/runner/ and acts pair) + extra log commit (provenance twin 1, tree_bounds twin 3, 12)
        h_ok = self.propose_merge(repo, lg, es, "builder", {
            "tools/runner/diary.py": "# allowed\n",
            f"transcripts/evidence/acts-C2c-1-jack-{STAMP}.csv": ACTS_HEADER,
            f"transcripts/evidence/acts-C2c-1-opencode-runner-{STAMP}.csv": ACTS_HEADER,
        }, extra_log_commit=True)
        s_ok = st.assess(es, "C2c-1", T_NOW, repo, h_ok)
        self.assertTrue(s_ok["criterion_lines"][2].endswith("met"))
        self.assertTrue(s_ok["criterion_lines"][8].endswith("met"))
        # Reviewer changing pins/pins.py -> met (twin 5)
        h_rev = self.propose_merge(repo, lg, es, "reviewer", {
            "pins/pins.py": gitfix.git(repo, "show", f"{h_ok}:pins/pins.py") + "\n# rev\n"
        })
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_rev)["criterion_lines"][2].endswith("met"))
        # Counsel synchronisation merge importing builder's acts pair without changing it (provenance twin 2, tree_bounds twin 14)
        gitfix.git(repo, "checkout", "-q", "-B", "c-sync", open_sha)
        gitfix.write(repo, "REPORT.md", "report\n")
        c_work = gitfix.commit_all(repo, "report\n\nProposer: counsel counsel")
        gitfix.git(repo, "merge", "--no-ff", "-q", "-m", "Sync main\n\nProposer: counsel counsel", h_rev)
        sync_head = gitfix.git(repo, "rev-parse", "HEAD")
        es.append(json.loads(lg.add("proposal", "counsel", {"title": "rep", "commit": sync_head},
                                    self.signers["counsel"], ts="2026-11-08T11:10:00Z")))
        gitfix.write(repo, "log.jsonl", lg.text())
        p_head = gitfix.commit_all(repo, "proposal: rep\n\nProposer: counsel counsel")
        es.append(json.loads(lg.add("merge", "herald", {"proposal": 2, "commit": p_head, "checker": "0" * 64},
                                    self.signers["herald"], ts="2026-11-08T11:10:00Z")))
        gitfix.write(repo, "log.jsonl", lg.text())
        b_tip = gitfix.commit_all(repo, "merge: #2\n\nProposer: herald herald")
        gitfix.git(repo, "checkout", "-q", "-B", "main", h_rev)
        gitfix.git(repo, "merge", "--no-ff", "-q", "-m", "Merge pull request #2", b_tip)
        h_sync = gitfix.git(repo, "rev-parse", "HEAD")
        s_sync = st.assess(es, "C2c-1", T_NOW, repo, h_sync)
        self.assertTrue(s_sync["criterion_lines"][2].endswith("met"))
        self.assertTrue(s_sync["criterion_lines"][8].endswith("met"))  # acts pair still counts as builder's!
        # Builder touching tools/status.py -> unmet (twin 2), even if restored later (twin 11)
        h_bad = self.propose_merge(repo, lg, es, "builder", {"tools/status.py": "# changed\n"})
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_bad)["criterion_lines"][2].endswith("unmet"))
        with open(os.path.join(ROOT, "tools/status.py"), "rb") as f:
            orig_st = f.read()
        h_rest = self.propose_merge(repo, lg, es, "builder", {"tools/status.py": orig_st})
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_rest)["criterion_lines"][2].endswith("unmet"))
        # A frozen path changed by the GitHub merge itself is charged to the proposal.
        r_merge, lg_merge, es_merge, _, _, _ = self.make_env()
        h_merge = self.propose_merge(r_merge, lg_merge, es_merge, "builder", {"REPORT.md": "report\n"},
                                     merge_files={"tools/status.py": "# merge conflict edit\n"})
        self.assertTrue(st.assess(es_merge, "C2c-1", T_NOW, r_merge, h_merge)["criterion_lines"][2].endswith("unmet"))

    def test_r11_remaining_tree_bounds_and_provenance_twins(self):
        repo, lg, es, open_sha, head, add = self.make_env()
        # Twin 15: sovereign decision budget inside the window -> met
        add("decision", "guy", ts="2026-11-08T10:30:00Z", kind="budget", subject="note")
        gitfix.write(repo, "log.jsonl", lg.text())
        h_sov = gitfix.commit_all(repo, "decision: budget\n\nProposer: guy guy-master")
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, h_sov)["criterion_lines"][2].endswith("met"))
        # Twin 4: reviewer changing tools/runner/diary.py -> unmet
        r4, lg4, es4, _, _, _ = self.make_env()
        h4 = self.propose_merge(r4, lg4, es4, "reviewer", {"tools/runner/diary.py": "x\n"})
        self.assertTrue(st.assess(es4, "C2c-1", T_NOW, r4, h4)["criterion_lines"][2].endswith("unmet"))
        # Twin 6: push inside window -> unmet
        r6, _, es6, _, h6, add6 = self.make_env()
        add6("push", "guy", ts="2026-11-08T10:30:00Z", digest="b" * 64, review="0" * 64, record="0" * 64)
        self.assertTrue(st.assess(es6, "C2c-1", T_NOW, r6, h6)["criterion_lines"][2].endswith("unmet"))
        # Twin 10: transcripts/windows/C2a.json added -> unmet, and C2a stays history
        r10, lg10, es10, _, _, _ = self.make_env()
        h10 = self.propose_merge(r10, lg10, es10, "counsel", {"transcripts/windows/C2a.json": WFILE_BYTES})
        self.assertTrue(st.assess(es10, "C2c-1", T_NOW, r10, h10)["criterion_lines"][2].endswith("unmet"))
        self.assertFalse(win.has_file(r10, h10, "C2a"))
        # Twin 13 & Provenance Twin 5: hand commit on main editing escalations.json -> unmet & escalations ignored
        r13, lg13, es13, _, _, _ = self.make_env()
        esc_data = json.dumps({"through": T_NOW, "rows": []})
        h13_ok = self.propose_merge(r13, lg13, es13, "builder", {"transcripts/evidence/escalations.json": esc_data})
        self.assertIsNotNone(win.load_escalations(r13, h13_ok, win.provenance_changers(r13, h13_ok)))
        gitfix.write(r13, "transcripts/evidence/escalations.json", esc_data + "\n")
        h13_hand = gitfix.commit_all(r13, "hand edit")
        self.assertIsNone(win.load_escalations(r13, h13_hand, win.provenance_changers(r13, h13_hand)))
        self.assertTrue(st.assess(es13, "C2c-1", T_NOW, r13, h13_hand)["criterion_lines"][2].endswith("unmet"))
        # Provenance Twins 3 & 4: older builder acts pair used when newer pair has one file edited/deleted by counsel
        rp, lgp, esp, _, _, _ = self.make_env()
        self.propose_merge(rp, lgp, esp, "builder", {
            "transcripts/evidence/acts-C2c-1-jack-20261108T1135.csv": ACTS_HEADER,
            "transcripts/evidence/acts-C2c-1-opencode-runner-20261108T1135.csv": ACTS_HEADER,
        }, ts="2026-11-08T11:35:00Z")
        hp2 = self.propose_merge(rp, lgp, esp, "builder", {
            f"transcripts/evidence/acts-C2c-1-jack-{STAMP}.csv": ACTS_HEADER,
            f"transcripts/evidence/acts-C2c-1-opencode-runner-{STAMP}.csv": ACTS_HEADER,
        }, ts="2026-11-08T11:45:00Z")
        self.assertEqual(win.newest_acts_pair(rp, hp2, "C2c-1")["stamp"], STAMP)
        hp3 = self.propose_merge(rp, lgp, esp, "counsel", {
            f"transcripts/evidence/acts-C2c-1-jack-{STAMP}.csv": ACTS_HEADER + "\n",
        }, ts="2026-11-08T11:50:00Z")
        self.assertEqual(win.newest_acts_pair(rp, hp3, "C2c-1")["stamp"], "20261108T1135")
        # Twin 18, 19, 20: unattributable merges (sibling, octopus, both-parents-on-main)
        gitfix.git(repo, "checkout", "-q", "-B", "sib", open_sha)
        gitfix.write(repo, "REPORT.md", "sib\n")
        sib_sha = gitfix.commit_all(repo, "sib")
        gitfix.git(repo, "checkout", "-q", "-B", "oct", h_sov)
        gitfix.write(repo, "LAW.md", "oct\n")
        gitfix.commit_all(repo, "oct")
        gitfix.git(repo, "merge", "--no-ff", "-q", "-m", "octopus", open_sha, sib_sha)
        oct_sha = gitfix.git(repo, "rev-parse", "HEAD")
        self.assertEqual(win.attribute_commit(repo, oct_sha, h_sov)[0], "unattributable")

    def test_r10_eprocess_continued_twins(self):
        repo, lg, es, open_sha, head, add = self.make_env()
        run_ok = {"path": st.WORKFLOW, "event": "push", "head_branch": "main", "head_sha": head,
                  "conclusion": "success", "updated_at": T_NOW}
        runs = [{"path": st.WORKFLOW, "event": "push", "head_branch": "main", "head_sha": open_sha,
                 "conclusion": "success", "updated_at": "2026-11-08T00:10:00Z"}, run_ok]
        # Twin 4: no run -> unknown (no run)
        s_norun = st.assess(es, "C2c-1", T_NOW, repo, head, run=None, runs=runs)
        self.assertTrue(s_norun["criterion_lines"][4].endswith("unknown (no run)"))
        self.assertTrue(s_norun["criterion_lines"][5].endswith("unknown (no run)"))
        # Twin 1: E >= 20 and gates held -> met for liveness
        s_met = st.assess(es, "C2c-1", T_NOW, repo, head, run=run_ok, runs=runs)
        self.assertTrue(s_met["criterion_lines"][5].endswith("met"))
        # Twin 2: late-reported repair -> unmet
        add("decision", "guy", ts="2026-11-08T10:30:00Z", kind="fix", subject="late")
        self.assertTrue(st.assess(es, "C2c-1", T_NOW, repo, head, run=run_ok, runs=runs)["criterion_lines"][5].endswith("unmet"))
        # Twin 3: process changed from opening -> unmet
        r3, _, es3, o3, _, _ = self.make_env()
        gitfix.write(r3, "tools/clerk.py", b"# modified\n")
        h3 = gitfix.commit_all(r3, "modify clerk")
        r3_ok = dict(run_ok, head_sha=h3)
        self.assertTrue(st.assess(es3, "C2c-1", T_NOW, r3, h3, run=r3_ok, runs=[dict(runs[0], head_sha=o3), r3_ok])["criterion_lines"][5].endswith("unmet"))


class RunbookGates(C2c1Fixture):
    def test_v_decision_requires_window_file_and_fresh_acts_pair(self):
        repo, lg, es, _, head, _ = self.make_env()
        # Closed window C1b has no window file -> refused
        with self.assertRaisesRegex(ValueError, "promotion criteria unknown for C1b"):
            win.check_promote_gate(repo, head, "C1b", T_NOW)
        # C2c-1 with no acts pair -> refused
        with self.assertRaisesRegex(ValueError, "no counting acts pair"):
            win.check_promote_gate(repo, head, "C2c-1", T_NOW)
        # C2c-1 with fresh acts pair (11:45Z is within 30 min before 12:00Z) -> admitted
        h_acts = self.propose_merge(repo, lg, es, "builder", {
            f"transcripts/evidence/acts-C2c-1-jack-{STAMP}.csv": ACTS_HEADER,
            f"transcripts/evidence/acts-C2c-1-opencode-runner-{STAMP}.csv": ACTS_HEADER,
        })
        self.assertTrue(win.check_promote_gate(repo, h_acts, "C2c-1", T_NOW))
        # Stale acts pair (11:45Z is 45 min before 12:30Z > 30 min) -> refused
        with self.assertRaisesRegex(ValueError, "not within 30 minutes"):
            win.check_promote_gate(repo, h_acts, "C2c-1", "2026-11-08T12:30:00Z")


if __name__ == "__main__":
    unittest.main()
