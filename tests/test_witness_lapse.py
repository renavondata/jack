"""Rule admission: witnesses, the weak non-contradiction check, lapse candidates."""
import tempfile
import unittest

from harness import build
from harness.build import forbid_title, proposal, rule_body, witness
from kernel import check

W = lambda title: witness("proposal", "p", proposal(title))  # noqa: E731


def R(rule_id, forbid, viol, sat, **kw):
    return rule_body(rule_id, forbid_title(rule_id, *forbid), [W(t) for t in viol], [W(t) for t in sat], **kw)


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.w = build.World(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def admit(self, *bodies):
        lg = self.w.log()
        for b in bodies:
            lg.add("rule", "guy", b, self.w.guy)
        return lg, check.check(lg.lines)

    def refused(self, v, seq, reason):
        self.assertEqual((v["ok"], v["seq"], v["reason"]), (False, seq, reason), v)


class Witnesses(Base):
    def test_vacuous_when_own_rule_does_not_fire(self):
        _, v = self.admit(R("r1", ["x"], ["z"], ["y"]))
        self.refused(v, 1, "vacuous_rule")

    def test_vacuous_when_only_an_older_rule_fires(self):
        _, v = self.admit(R("r0", ["z"], ["z"], ["y"]), R("r1", ["x"], ["z"], ["y"]))
        self.refused(v, 2, "vacuous_rule")

    def test_impossible_when_own_rule_rejects_satisfying(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["x"]))
        self.refused(v, 1, "impossible_rule")

    def test_impossible_when_older_rule_rejects_satisfying(self):
        _, v = self.admit(R("r0", ["y"], ["y"], ["w"]), R("r1", ["x"], ["x"], ["y"]))
        self.refused(v, 2, "impossible_rule")

    def test_all_witnesses_count(self):
        _, v = self.admit(R("r1", ["x", "z"], ["x", "z"], ["y", "w"]))
        self.assertTrue(v["ok"], v)
        _, v = self.admit(R("r1", ["x", "z"], ["x", "q"], ["y", "w"]))
        self.refused(v, 1, "vacuous_rule")
        _, v = self.admit(R("r1", ["x", "z"], ["x", "z"], ["y", "x"]))
        self.refused(v, 1, "impossible_rule")

    def test_witness_sees_prefix_and_candidate(self):
        clauses = [{"head": ["violation", "?S", "r1"],
                    "body": [["candidate", "?S"], ["entry", "?S", "merge", "?_"], ["field", "?S", "proposal", "?P"],
                             ["not", ["entry", "?P", "proposal", "?_"]]]}]
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("a"), self.w.ann)
        lg.add("rule", "guy", rule_body("r1", clauses, [witness("merge", "guy", build.merge(99))],
                                        [witness("merge", "guy", build.merge(1))]), self.w.guy)
        self.assertTrue(check.check(lg.lines)["ok"])
        lg.add("merge", "guy", build.merge(7), self.w.guy)
        self.refused(check.check(lg.lines), 3, "violation")

    def test_witness_ts_fact(self):
        clauses = [{"head": ["violation", "?S", "r1"], "body": [["entry", "?S", "proposal", "?_"], ["ts", "?S", "2000-01-01T00:00:00Z"]]}]
        _, v = self.admit(rule_body("r1", clauses, [witness("proposal", "p", proposal(), ts="2000-01-01T00:00:00Z")],
                                    [witness("proposal", "p", proposal(), ts="2026-01-01T00:00:00Z")]))
        self.assertTrue(v["ok"], v)

    def test_rule_over_signed_by_is_inadmissible(self):
        clauses = [{"head": ["violation", "?S", "r1"], "body": [["entry", "?S", "proposal", "?_"], ["not", ["signed_by", "?S", "guy-master"]]]}]
        _, v = self.admit(rule_body("r1", clauses, [W("x")], [W("y")]))
        self.refused(v, 1, "impossible_rule")


class Orphans(Base):
    def test_new_rule_orphaning_an_older_rule_is_refused(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r2", ["y"], ["y"], ["z"]))
        self.refused(v, 2, "orphans_rule")

    def test_replacement_witness_rescues(self):
        lg, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r2", ["y"], ["y"], ["z"], replacements={"r1": [W("z")]}))
        self.assertTrue(v["ok"], v)
        lg.add("rule", "guy", R("r3", ["z"], ["z"], ["w"]), self.w.guy)
        self.refused(check.check(lg.lines), 3, "orphans_rule")
        lg.lines.pop()
        lg.add("rule", "guy", R("r3", ["z"], ["z"], ["w"], replacements={"r1": [W("w")], "r2": [W("w")]}), self.w.guy)
        self.assertTrue(check.check(lg.lines)["ok"])

    def test_one_surviving_witness_suffices(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["y", "q"]), R("r2", ["y"], ["y"], ["z"]))
        self.assertTrue(v["ok"], v)

    def test_replacement_for_unknown_rule(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["y"], replacements={"nope": [W("z")]}))
        self.refused(v, 1, "rule_malformed")

    def test_replacement_must_pass_the_whole_law(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r2", ["y"], ["y"], ["z"], replacements={"r1": [W("y")]}))
        self.refused(v, 2, "impossible_rule")

    def test_replacement_shape(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["y"], replacements={"r1": "y"}))
        self.refused(v, 1, "rule_malformed")

    def test_repeal_does_not_orphan(self):
        lg, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r2", ["z"], ["z"], ["y"]))
        lg.add("repeal", "guy", {"rule_id": "r2"}, self.w.guy)
        self.assertTrue(check.check(lg.lines)["ok"])


class Lapse(Base):
    def test_broader_later_rule_makes_older_a_candidate(self):
        lg, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r2", ["x", "z"], ["z"], ["y"]))
        self.assertEqual(v, {"ok": True, "entries": 3, "lapse": [[2, "r1"]]})
        lg.add("proposal", "ann", proposal("y"), self.w.ann)
        self.assertEqual(check.check(lg.lines)["lapse"], [[2, "r1"]])

    def test_disjoint_rules_no_candidates(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r3", ["w"], ["w"], ["y"]))
        self.assertEqual(v["lapse"], [])

    def test_mutual_redundancy_lapses_one_at_a_time(self):
        _, v = self.admit(R("r1", ["x", "y"], ["x"], ["w"]), R("r2", ["x", "y"], ["y"], ["w"]))
        self.assertEqual(v["lapse"], [[2, "r1"]])

    def test_candidates_at_each_change_entry(self):
        _, v = self.admit(R("r1", ["x"], ["x"], ["w"]), R("r2", ["y"], ["y"], ["w"]), R("r3", ["x", "y"], ["x"], ["w"]))
        self.assertEqual(v["lapse"], [[3, "r1"], [3, "r2"]])

    def test_repeal_recomputes(self):
        lg, v = self.admit(R("r1", ["x"], ["x"], ["y"]), R("r2", ["x", "z"], ["z"], ["y"]))
        lg.add("repeal", "guy", {"rule_id": "r2"}, self.w.guy)
        self.assertEqual(check.check(lg.lines)["lapse"], [[2, "r1"]])
        lg.add("rule", "guy", R("r4", ["x", "q"], ["q"], ["y"]), self.w.guy)
        self.assertEqual(check.check(lg.lines)["lapse"], [[2, "r1"], [4, "r1"]])


if __name__ == "__main__":
    unittest.main()
