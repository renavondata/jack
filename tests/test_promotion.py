"""C1b promotion/W3/W4 witnesses and twins; supplied Actions data, no network."""
import copy
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from harness.gitfix import write
from tests.clerk_fixture import DUE, LATE, NOW, SignedFixture, Stream, commit, tree
from tools import clerk, status

EARLY = "2026-10-31T11:59:59Z"
SHA = "a" * 40
GREEN = dict(path=status.WORKFLOW, event="push", head_branch="main", head_sha=SHA, conclusion="success", updated_at=EARLY)
FACTS = dict(counted=6900, kernel=500, scope=True)
with open(os.path.join(status.ROOT, status.MAP)) as f:
    MAP = json.load(f)
loader = importlib.machinery.SourceFileLoader("jack_promotion", os.path.join(status.ROOT, "tools/jack"))
spec = importlib.util.spec_from_loader(loader.name, loader)
jack = importlib.util.module_from_spec(spec)
loader.exec_module(jack)


class Promotion(SignedFixture):
    def setUp(self):
        super().setUp()
        self.s.complete(9, type="world.fixture")

    def tree(self):
        scope = {"counted": ["tests/"], "cap": 6900}
        return tree({"judge/scope.json": json.dumps(scope), "SPEC.md": "at C1 it is:\n```\n" + json.dumps(scope) + "\n```\n",
                     "tests/test_clerk.py": "# synthetic attack witness\n", status.MAP: json.dumps(MAP),
                     "log.jsonl": self.s.log.text(), "transcripts/evidence/acts.csv": "repo,time_hkt,class,kind,ref,note\n"})

    def assess(self, **kw):
        args = dict(es=self.s.es, subject="C1b", as_of=NOW, root=self.tmp.name, rev=SHA,
                    run=GREEN, runs=[GREEN], acts=[], mapping=MAP)
        facts = kw.pop("facts", FACTS)
        with patch.object(status, "tree_facts", return_value=facts), patch.object(status, "tree_bytes", return_value=b"attack test"):
            return status.assess(**dict(args, **kw))

    def verdict(self, **kw):
        return status.promotion_line(self.assess(**kw))

    def refused(self, text, **kw):
        s = self.assess(**kw)
        self.assertEqual(len(status.unmet(s)), 1)
        self.assertIn(text, status.render(s))
        self.decision(status.render(s))
        return s

    def decision(self, text, run=GREEN):
        """Exercise the real gate and API arguments; only the irreversible ending is stubbed."""
        a = SimpleNamespace(kind="promote", subject="C1b", acts=None)
        calls = []
        def command(*cmd):
            calls.append(cmd)
            if cmd[0] == "gh":
                return SimpleNamespace(stdout=json.dumps([{"workflow_runs": [run] if run else []}]))
            self.assertEqual(cmd[cmd.index("--as-of") + 1], a.decision_ts)
            with open(cmd[cmd.index("--run") + 1]) as f:
                self.assertEqual(json.load(f), run if status.run_verified(run, SHA) else None)
            return SimpleNamespace(stdout=text)
        with patch.object(jack, "begin"), patch.object(jack, "git", return_value=SHA), patch.object(jack, "run", side_effect=command), \
                patch.object(jack, "main_ending") as ending, patch.object(jack, "append") as append:
            if text.splitlines()[-1] == "promote C1b: lawful":
                jack.v_decision(a)
                ending.assert_called_once()
                self.assertEqual(ending.call_args.args[2](), {"kind": "promote", "subject": "C1b"})
            else:
                with self.assertRaises(jack.Refused):
                    jack.v_decision(a)
                ending.assert_not_called()
            append.assert_not_called()
        self.assertEqual(calls[0], ("gh", "api", f"repos/{{owner}}/{{repo}}/actions/workflows/tests.yml/runs?head_sha={SHA}&event=push&branch=main",
                                    "--paginate", "--slurp"))
        self.assertIn(("gh", "api", "repos/{owner}/{repo}/actions/workflows/tests.yml/runs?event=push&branch=main", "--paginate", "--slurp"), calls)

    def test_all_met_lawful_and_the_verb_signs(self):
        s = self.assess()
        self.assertEqual(status.promotion_line(s), "promote C1b: lawful")
        self.assertGreaterEqual(s["E"], 20)
        self.assertEqual(clerk.window_writs(self.s.es, s, NOW), [])
        self.decision(status.render(s))

    def test_run_verified_each_field_and_no_signing(self):
        invalid = [None, {}, dict(GREEN, conclusion=None), dict(GREEN, conclusion="failure"),
                   dict(GREEN, path=".github/workflows/judge.yml", name="tests"), dict(GREEN, head_sha="b" * 40),
                   dict(GREEN, event="pull_request"), dict(GREEN, head_branch="work"), dict(GREEN, updated_at=LATE)]
        for run in invalid:
            with self.subTest(run=run):
                s = self.assess(run=run)
                self.assertFalse(s["checks"][0][0])
                self.assertFalse(s["checks"][1][0])
                self.assertIn("promote C1b: refused:", status.render(s))
                self.decision(status.render(s), run)

    def test_live_e_not_replaced_by_green_regression_run(self):
        self.s = Stream(self.signers)
        self.s.complete(1, type="world.fixture")
        s = self.refused("criterion 5: live E 1 >= 20; items 1; at promote E 1")
        self.assertEqual([(i["forecasts"], i["Y"]) for i in s["items"]], [((5,), 1)])

    def test_veto_subject_is_exact(self):
        self.s.add("decision", "guy", kind="veto", subject="other")
        self.assertEqual(self.verdict(), "promote C1b: lawful")
        self.s.add("decision", "guy", kind="veto", subject="C1b")
        self.refused("criterion 6: veto on C1b: YES")

    def test_map_printed_and_each_required_hand_row_refuses(self):
        for row in ("W1", "W3", "W4", "A5"):
            mapping = copy.deepcopy(MAP)
            mapping[row]["enforcer"] = "hand: counsel"
            s = self.refused("criterion 7: C1b enforcement map rows code", mapping=mapping)
            self.assertIn(f"map {row}: {mapping[row]['principle']} | hand: counsel", status.render(s))
        self.assertEqual(self.verdict(mapping=MAP), "promote C1b: lawful")  # runner/elections stay hand
        self.assertIn("criterion 7", self.verdict(mapping={}))

    def test_stop_ratio_alone_prevents_signing(self):
        s = self.assess()
        for _ in range(5 * s["object"] - s["procedure"]):
            self.s.add("proposal", title="procedure", commit=SHA)
        s = self.refused(" STOP")  # the prospective promote itself must fit
        self.assertEqual(s["procedure"], 5 * s["object"])
        self.s.add("proposal", title="procedure", commit=SHA)
        self.refused(" STOP")

    def test_short_tree_criterion_alone_prevents_signing(self):
        for facts in (dict(FACTS, counted=FACTS["counted"] + 1), dict(FACTS, kernel=501), dict(FACTS, scope=False)):
            self.refused("criterion 3", facts=facts)

    def test_promotion_accounts_for_expiry_since_last_entry_without_revising_live_items(self):
        self.s.forecast(resolves_by=NOW)
        before = self.assess()
        self.assertEqual(status.promotion_line(before), "promote C1b: lawful")
        after = self.assess(as_of="2026-10-31T12:00:01Z")
        self.assertEqual(after["items"], before["items"])
        self.assertEqual(after["E"], before["E"])
        self.assertLess(after["promotion_E"], 20)
        self.decision(status.render(after))

    def test_late_report_line_refuses_without_revising_any_bet(self):
        before = self.assess()
        self.s.add("decision", "guy", kind="fix", subject=str(before["items"][0]["forecasts"][0]))
        after = self.refused("late-reported repairs: 1 SHORT")
        self.assertEqual(after["items"], before["items"])
        self.assertEqual(after["E"], before["E"])

    def test_attack_run_must_precede_first_item_and_include_attack_file(self):
        for run in (dict(GREEN, updated_at=NOW), dict(GREEN, updated_at=LATE), dict(GREEN, event="pull_request")):
            s = self.assess(runs=[run])
            self.assertFalse(next(ok for ok, t in s["checks"] if t.startswith("criterion 4:")))
            self.assertEqual((s["items"], s["E"]), ([], 1))
        with patch.object(status, "tree_bytes", side_effect=subprocess.CalledProcessError(1, "git show")):
            self.assertIsNone(status.attack_start(self.tmp.name, [GREEN], NOW))
        self.assertEqual(self.verdict(), "promote C1b: lawful")

    def test_off_log_repairs_and_unknown_are_w4(self):
        row = dict(repo="renavondata/jack", time_hkt="2026-10-31 20:00", **{"class": "repair"}, kind="fix", ref="", note="")
        ignored = [dict(row, repo="other"), dict(row, **{"class": "decision"}), dict(row, time_hkt="2026-10-31 19:59"),
                   dict(row, time_hkt="2026-11-03 08:01")]
        self.assertEqual(status.off_log_repairs([row, dict(row, time_hkt="2026-11-03 08:00")] + ignored, NOW, DUE), 2)
        self.assertEqual(self.verdict(acts=ignored), "promote C1b: lawful")
        for acts, text in ((None, "off-log repairs: unknown (no acts file)"), ([row], "off-log repairs: 1")):
            s = self.refused(text, acts=acts)
            ws = clerk.window_writs(self.s.es, s, LATE)
            self.assertEqual([(w["class"], w["obligation"], w["holders"], w["deadline"], w["escalated"]) for w in ws],
                             [("W4", text, ("counsel",), DUE, True)])
            self.assertIn("ESCALATED to guy", clerk.render(ws))

    def test_w3_only_earlier_green_exact_workflow_and_commit_discharge(self):
        merge = self.s.es[-1]
        good = dict(GREEN, head_sha=merge["body"]["commit"])
        es = self.s.es[:self.s.opening + 1] + [merge]
        for runs in ([], [dict(good, conclusion="failure"), dict(good, updated_at=LATE)],
                     [dict(good, path=".github/workflows/judge.yml")], [dict(good, head_sha=SHA)]):
            ws = clerk.merge_writs(es, runs, NOW, DUE, "")
            self.assertEqual([(w["seq"], w["deadline"], w["holders"], w["escalated"]) for w in ws],
                             [(merge["seq"], DUE, ("counsel",), False)])
        for when in (EARLY, NOW):
            self.assertEqual(clerk.merge_writs(es, [dict(good, updated_at=when)], NOW, DUE, ""), [])
        marker = f"W3 merge {merge['seq']}"
        self.assertTrue(clerk.merge_writs(es, [], NOW, DUE, marker))  # prose is not a table row
        self.assertTrue(clerk.merge_writs(es, [], NOW, DUE, f"| {marker}0 |"))
        self.assertEqual(clerk.merge_writs(es, [], NOW, DUE, f"| precedent | {marker} |"), [])

    def test_historical_bad_promote_stays_repair_after_later_success(self):
        with self.tree() as (root, sha):
            promote = self.s.add("decision", "guy", kind="promote", subject="C1b")
            later = dict(GREEN, head_sha=commit(root, {"log.jsonl": self.s.log.text()}), updated_at=LATE)
            good, bad_run = dict(GREEN, head_sha=sha), dict(GREEN, head_sha=sha, conclusion="failure")
            def repairs(runs):
                s = status.report(es=self.s.es, subject="C1b", as_of=LATE, root=root, rev=later["head_sha"], runs=runs, acts=[])
                return [r for r in s["repairs"]
                        if f"promote C1b seq {promote}:" in r]
            bad = repairs([bad_run])
            self.assertEqual(len(bad), 1)
            self.assertIn("criterion 1", bad[0])
            self.assertEqual(repairs([bad_run, later]), bad)
            self.assertEqual(repairs([good, later]), [])
        s = self.assess()
        s["repairs"] = bad
        self.assertIn("sovereign REPAIR", clerk.render(clerk.window_writs(self.s.es, s, LATE)))

    def test_cli_saved_inputs_and_deterministic_clerk(self):
        with self.tree() as (root, sha):
            self.assertEqual(status.tree_facts(root, sha), dict(counted=1, kernel=0, scope=True))
            write(root, "run.json", json.dumps(dict(GREEN, head_sha=sha)))
            write(root, "runs.json", json.dumps([dict(GREEN, head_sha=sha)]))
            args = ["--root", root, "--log", os.path.join(root, "log.jsonl"), "--as-of", NOW,
                    "--run", os.path.join(root, "run.json"), "--runs", os.path.join(root, "runs.json"),
                    "--acts", os.path.join(root, "transcripts/evidence/acts.csv")]
            def cli(verb):
                r = subprocess.run([sys.executable, os.path.join(status.ROOT, "tools/jack"), verb, *args], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                return r.stdout
            self.assertEqual(cli("status").splitlines()[-1], "promote C1b: lawful")
            first = cli("clerk")
            self.assertIn("W3 merge", first)
            self.assertEqual(first, cli("clerk"))
            write(root, "run.json", json.dumps(dict(GREEN, head_sha=sha, event="pull_request")))
            self.assertIn("promote C1b: refused: criterion 1", cli("status"))
            write(root, "transcripts/evidence/acts.csv", "wrong,header\n")
            r = subprocess.run([sys.executable, os.path.join(status.ROOT, "tools/clerk.py"), *args], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("--acts header", r.stderr)


if __name__ == "__main__":
    unittest.main()
