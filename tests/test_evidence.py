"""Tests for tools/evidence/{acts,escalations,runner,courier}.py (transcripts/sessions/evidence.md; C2c-1.json)."""
import csv, hashlib, io, json, os, subprocess, sys, tempfile, unittest, zipfile  # noqa: E401
from unittest import mock

from harness import build, keys
from tools.evidence import acts, courier, escalations, runner

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T_PROMOTE = "2026-11-08T00:00:00Z"
T_OPEN = "2026-11-08T01:00:00Z"
T_NOW = "2026-11-08T04:00:00Z"
STAMP = "20261108T0400"


class EvidenceScriptsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key_tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.key_tmp.cleanup)
        cls.signers = {who: keys.make_key(cls.key_tmp.name, who) for who in ("guy", "counsel", "builder", "herald")}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        lg = build.Log()
        lg.add("genesis", "guy", build.genesis_body([build.decl("guy", "guy", self.signers["guy"], build.ALL)]),
               self.signers["guy"], ts="2026-11-07T00:00:00Z")
        for who in ("counsel", "builder", "herald"):
            lg.add("key", "guy", build.decl(who, who, self.signers[who], build.ALL),
                   self.signers["guy"], ts="2026-11-07T00:01:00Z")
        self.fc_handed = json.loads(lg.add(
            "forecast", "counsel",
            {"claim": "handed claim", "p": 500, "resolves_by": "2026-11-08T02:00:00Z"},
            self.signers["counsel"], ts="2026-11-07T12:00:00Z"))["seq"]
        self.fc_escalated = json.loads(lg.add(
            "forecast", "counsel",
            {"claim": "escalated claim", "p": 500, "resolves_by": "2026-11-08T01:30:00Z"},
            self.signers["counsel"], ts="2026-11-07T12:05:00Z"))["seq"]
        lg.add("decision", "guy", {"kind": "promote", "subject": "C2b"}, self.signers["guy"], ts=T_PROMOTE)
        lg.add("push", "guy", {"digest": "0" * 64, "review": "0" * 64, "record": "0" * 64},
               self.signers["guy"], ts=T_OPEN)
        with open(os.path.join(self.root, "log.jsonl"), "w", encoding="utf-8") as f:
            f.write(lg.text())
        self.env_patch = mock.patch.dict(os.environ, {"JACK_ROOT": self.root, "JACK_NOW": T_NOW, "STAMP": STAMP})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

    def test_opening_instant_and_no_windows_path_literal(self):
        self.assertEqual(acts.opening_instant("C2c-1", root=self.root), T_OPEN)
        with self.assertRaises(SystemExit):
            acts.opening_instant("C2c-2", root=self.root)
        with self.assertRaises(SystemExit):
            acts.main(["C2c-1", "renavondata/jack", "20261108T0030"])
        for fn in ("acts.py", "escalations.py", "runner.py", "courier.py"):
            with open(os.path.join(ROOT, "tools", "evidence", fn), encoding="utf-8") as f:
                self.assertNotIn("transcripts/windows", f.read())

    def test_acts_writes_attributed_raw_and_classifier_hash_for_both_repos(self):
        def fake_api(path):
            if "/issues?state=all" in path:
                if "&page=1" not in path:
                    return []
                return [{"number": 91, "user": {"login": "counsel-bot"}, "pull_request": {}, "labels": []}]
            if "/issues/events" in path:
                if "&page=1" not in path:
                    return []
                return [
                    {"id": 1, "event": "closed", "actor": {"login": "gfrmin"}, "created_at": "2026-11-08T02:00:00Z",
                     "issue": {"number": 91, "user": {"login": "counsel-bot"}, "pull_request": {}, "labels": []}},
                    {"id": 2, "event": "labeled", "actor": {"login": "gfrmin"}, "created_at": "2026-11-08T02:10:00Z",
                     "label": {"name": "manual"}, "issue": {"number": 92, "user": {"login": "other"}, "labels": []}},
                ]
            if "/pulls/" in path and "/reviews" in path:
                return []
            if "/actions/runs" in path:
                return {"workflow_runs": []}
            if "/rulesets" in path:
                return []
            if "/issues/comments" in path:
                if "&page=1" not in path:
                    return []
                return [{"user": {"login": "gfrmin"}, "created_at": "2026-11-08T02:00:30Z",
                         "issue_url": "https://api.github.com/repos/x/y/issues/91",
                         "body": "stale: superseded\n\nProposer: counsel counsel-3"}]
            return []

        with mock.patch.object(acts, "api", side_effect=fake_api):
            self.assertEqual(acts.main(["C2c-1", "renavondata/jack", STAMP]), 0)
            self.assertEqual(acts.main(["C2c-1", "renavondata/opencode-runner", STAMP]), 0)

        ev_dir = os.path.join(self.root, "transcripts", "evidence")
        with open(os.path.join(ROOT, "tools", "evidence", "acts.py"), "rb") as f:
            expected_sha = hashlib.sha256(f.read()).hexdigest()

        for short, full_repo in (("jack", "renavondata/jack"), ("opencode-runner", "renavondata/opencode-runner")):
            attr_p = os.path.join(ev_dir, f"acts-C2c-1-{short}-{STAMP}.csv")
            raw_p = os.path.join(ev_dir, f"acts-C2c-1-{short}-{STAMP}-raw.csv")
            sha_p = os.path.join(ev_dir, f"acts-C2c-1-{short}-{STAMP}-classifier.sha256")
            with open(sha_p, encoding="utf-8") as f:
                self.assertEqual(f.read().strip(), expected_sha)
            with open(attr_p, newline="", encoding="utf-8") as f:
                attr_rows = list(csv.DictReader(f))
            with open(raw_p, newline="", encoding="utf-8") as f:
                raw_rows = list(csv.DictReader(f))
            self.assertEqual([r["class"] for r in raw_rows], ["repair", "comment", "repair"])
            self.assertEqual([r["class"] for r in attr_rows], ["party-act", "party-comment", "repair"])
            self.assertTrue(all(r["repo"] == full_repo for r in attr_rows))

    def test_acts_counts_an_overlapping_printed_minute_and_refuses_api_failure(self):
        with mock.patch.object(acts, "pages", return_value=iter(())), \
             mock.patch.object(acts, "api", side_effect=SystemExit("rulesets unavailable")):
            with self.assertRaisesRegex(SystemExit, "rulesets unavailable"):
                acts.collect_acts("renavondata/jack", T_OPEN, T_NOW)

        def fake_api(path):
            if "/actions/runs" in path:
                return {"workflow_runs": []}
            if "/issues?state=all" in path or "/issues/events" in path or "/issues/comments" in path:
                return []
            if path.endswith("/rulesets"):
                return [{"id": 1, "name": "r"}]
            return {"created_at": "2026-11-08T01:00:01Z", "name": "r"}

        with mock.patch.object(acts, "api", side_effect=fake_api):
            _, rows = acts.collect_acts("renavondata/jack", "2026-11-08T01:00:30Z", "2026-11-08T01:01:30Z")
        self.assertEqual(len(rows), 1)

        with self.assertRaisesRegex(SystemExit, "after collection instant"):
            acts.main(["C2c-1", "renavondata/jack", "20261108T0401"])

    def test_acts_keeps_an_event_in_the_opening_minute(self):
        event = {"id": 1, "event": "closed", "actor": {"login": "gfrmin"},
                 "created_at": "2026-11-08T01:00:01Z",
                 "issue": {"number": 91, "user": {"login": "other"}, "labels": []}}
        def fake_pages(path, **_):
            return iter([event] if "/issues/events" in path else [])
        with mock.patch.object(acts, "pages", side_effect=fake_pages), \
             mock.patch.object(acts, "api", return_value=[]):
            _, rows = acts.collect_acts("renavondata/jack", "2026-11-08T01:00:30Z", T_NOW)
        self.assertEqual([row[3] for row in rows], ["#91"])

    def test_pages_refuses_an_unbounded_result(self):
        with mock.patch.object(acts, "api", return_value=[{}] * 100):
            with self.assertRaisesRegex(SystemExit, "exceeded"):
                list(acts.pages("repos/x/y"))

    def test_escalations_rebuilds_from_diary_issues_and_ignores_other_logins(self):
        ev_dir = os.path.join(self.root, "transcripts", "evidence")
        os.makedirs(ev_dir, exist_ok=True)
        esc_path = os.path.join(ev_dir, "escalations.json")
        with open(esc_path, "w", encoding="utf-8") as f:
            json.dump({"through": "2026-11-01T00:00:00Z", "rows": [{"forecast": 999, "issue": 1}]}, f)

        issues_data = [
            {"number": 450, "title": "resolve the writs due",
             "created_at": "2026-11-07T14:00:00Z", "user": {"login": "renavondata-jack-court[bot]"},
             "body": f"list\n\ndue-seqs: {self.fc_handed}\n"},
            {"number": 451, "title": "resolve the writs due",
             "created_at": "2026-11-08T01:40:00Z", "user": {"login": "assize-reviewer"},
             "body": f"due-seqs: {self.fc_escalated}\n"},
            {"number": 452, "title": "resolve the writs due",
             "created_at": "2026-11-08T02:00:00Z", "user": {"login": "renavondata-jack-court[bot]"},
             "body": f"due-seqs: {self.fc_escalated}\n"},
            {"number": 449, "title": "resolve the writs due",
             "created_at": "2026-11-07T12:59:59Z", "user": {"login": "renavondata-jack-court[bot]"},
             "body": f"due-seqs: {self.fc_handed}\n"},
        ]
        with mock.patch.object(escalations, "pages", return_value=iter(issues_data)):
            buf = io.StringIO()
            with mock.patch("sys.stdout", buf):
                self.assertEqual(escalations.main(["C2c-1"]), 0)
            self.assertIn("ignored issue #451 by assize-reviewer", buf.getvalue())

        with open(esc_path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["through"], T_NOW)
        self.assertEqual(data["rows"], [
            {"forecast": self.fc_handed, "issue": 450, "filed_at": "2026-11-07T14:00:00Z",
             "kind": "handed", "user": "renavondata-jack-court[bot]"},
            {"forecast": self.fc_escalated, "issue": 452, "filed_at": "2026-11-08T02:00:00Z",
             "kind": "escalated", "user": "renavondata-jack-court[bot]"},
        ])

    def test_escalations_requires_the_exact_diary_title(self):
        issue = {"number": 453, "title": "builder: resolve the writs due", "created_at": T_NOW,
                 "user": {"login": "renavondata-jack-court[bot]"}, "body": f"due-seqs: {self.fc_handed}"}
        with mock.patch.object(escalations, "pages", return_value=iter([issue])):
            data, ignored = escalations.build_escalations("C2c-1", root=self.root, through=T_NOW)
        self.assertEqual(data["rows"], [])
        self.assertEqual(ignored, [])

    def test_runner_and_courier_evidence(self):
        wf_bytes = {"counsel-sign.yml": b"name: counsel-sign\n", "counsel.yml": b"name: counsel\n"}
        listing = [{"name": k, "path": f".github/workflows/{k}", "type": "file"} for k in wf_bytes]
        with mock.patch.object(runner, "api", return_value=listing), \
             mock.patch.object(runner, "gh_raw_bytes", side_effect=lambda p: wf_bytes[p.rsplit("/", 1)[-1].split("?")[0]]):
            self.assertEqual(runner.main([]), 0)

        runner_path = os.path.join(self.root, "transcripts", "evidence", f"runner-{STAMP}.json")
        with open(runner_path, encoding="utf-8") as f:
            r_items = json.load(f)
        self.assertEqual(r_items, [
            {"workflow": "counsel-sign.yml", "sha256": hashlib.sha256(wf_bytes["counsel-sign.yml"]).hexdigest()},
            {"workflow": "counsel.yml", "sha256": hashlib.sha256(wf_bytes["counsel.yml"]).hexdigest()},
        ])

        trig_json = '{"id": "sign-row-47", "act": "sign", "branch": "counsel/row-47"}'
        req_sha = "5cbcdb6ecdf142ece12b3023772bcfb89d00a5ce3f8815c4b8052ea5b3db5b72"
        receipt_line = (f"sign-row-47: counsel/row-47: 2 line(s) in run 101; request sha256 {req_sha}; "
                        "proposal commit abcdef; head 123456; pull request 620")
        zbuf = io.BytesIO()
        with zipfile.ZipFile(zbuf, "w") as z:
            z.writestr("0_sign.txt", f"2026-11-08T02:01:00.1234567Z {receipt_line}\n2026-11-08T02:01:01Z {receipt_line}\n")
            z.writestr("sign/1_step.txt", f"2026-11-08T02:01:00.1234567Z {receipt_line}\n")

        runs_page = [
            {"id": 101, "created_at": "2026-11-08T02:00:00Z", "run_started_at": "2026-11-08T02:00:05Z",
             "updated_at": "2026-11-08T02:05:00Z", "conclusion": "success", "head_sha": "deadbeef"},
            {"id": 99, "created_at": "2026-11-08T00:30:00Z", "run_started_at": "2026-11-08T00:30:00Z",
             "updated_at": "2026-11-08T00:31:00Z", "conclusion": "success", "head_sha": "oldsha"},
        ]
        commit_obj = {"files": [
            {"filename": "requests/sign-row-47.json", "status": "added"},
            {"filename": "requests/other.json", "status": "added"},
        ]}
        with mock.patch.object(courier, "pages", return_value=iter(runs_page)), \
             mock.patch.object(courier, "api", return_value=commit_obj), \
             mock.patch.object(courier, "gh_raw_bytes", return_value=trig_json.encode("utf-8")), \
            mock.patch.object(subprocess, "run", side_effect=lambda *args, **kwargs: (
                kwargs["stdout"].write(zbuf.getvalue()), subprocess.CompletedProcess([], 0, stderr=b""))[1]):
            self.assertEqual(courier.main(["C2c-1"]), 0)

        courier_path = os.path.join(self.root, "transcripts", "evidence", f"courier-{STAMP}.json")
        with open(courier_path, encoding="utf-8") as f:
            c_data = json.load(f)
        self.assertEqual(c_data["through"], T_NOW)
        self.assertEqual(len(c_data["runs"]), 1)
        self.assertEqual(c_data["runs"][0], {
            "run": 101,
            "created_at": "2026-11-08T02:00:00Z",
            "run_started_at": "2026-11-08T02:00:05Z",
            "updated_at": "2026-11-08T02:05:00Z",
            "conclusion": "success",
            "triggers": [{
                "path": "requests/sign-row-47.json",
                "id": "sign-row-47",
                "branch": "counsel/row-47",
                "contents": trig_json,
            }],
            "receipts": [receipt_line, receipt_line, receipt_line],
        })

    def test_courier_refuses_incomplete_logs_and_excessive_members(self):
        with mock.patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1, stderr=b"not ready")):
            with self.assertRaisesRegex(SystemExit, "not ready"):
                list(courier.run_log_lines(101, None))

        zbuf = io.BytesIO()
        with zipfile.ZipFile(zbuf, "w") as z:
            for n in range(courier.MAX_LOG_MEMBERS + 1):
                z.writestr(f"{n}.txt", "")
        with mock.patch.object(subprocess, "run", side_effect=lambda *args, **kwargs: (
                kwargs["stdout"].write(zbuf.getvalue()), subprocess.CompletedProcess([], 0, stderr=b""))[1]):
            with self.assertRaisesRegex(SystemExit, "more than"):
                list(courier.run_log_lines(101, "success"))

    def test_courier_refuses_receipts_too_large(self):
        line = "request: request sha256 " + "0" * 64
        with mock.patch.object(courier, "MAX_RECEIPT_BYTES", len(line.encode("utf-8"))):
            with self.assertRaisesRegex(SystemExit, "receipts exceed"):
                courier.extract_receipts([line, line])

    def test_runner_refuses_a_future_stamp(self):
        with self.assertRaisesRegex(SystemExit, "after collection instant"):
            runner.main(["20261108T0401"])

    def test_courier_fetches_every_commit_files_page(self):
        first = [{"filename": f"other/{n}", "status": "added"} for n in range(100)]
        second = [{"filename": "requests/sign-row-48.json", "status": "added"}]
        def fake_api(path):
            return {"files": first if path.endswith("page=1") else second}
        with mock.patch.object(courier, "api", side_effect=fake_api):
            self.assertEqual(courier.commit_files("deadbeef"), first + second)


if __name__ == "__main__":
    unittest.main()
