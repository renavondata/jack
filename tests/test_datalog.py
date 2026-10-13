"""Stratified Datalog over tagged atoms: compile, stratify, evaluate."""
import unittest

from kernel import datalog
from kernel.log import Refuse, atom, untag


def F(*vals):
    return tuple(atom(v) for v in vals)


def facts(**preds):
    return {p: set(rows) for p, rows in preds.items()}


def rule(rule_id, *clauses):
    return datalog.compile_rule(rule_id, [{"head": h, "body": list(b)} for h, b in clauses])


def rows(result, pred):
    return {tuple(untag(a) for a in row) for row in result.get(pred, ())}


class Compile(unittest.TestCase):
    def malformed(self, rule_id, clauses):
        with self.assertRaises(Refuse) as cm:
            datalog.compile_rule(rule_id, clauses)
        self.assertEqual(cm.exception.reason, "rule_malformed")
        return cm.exception.detail

    def test_good_rule_compiles(self):
        c = rule("r1", (["violation", "?S", "r1"], [["entry", "?S", "proposal", "?_"], ["field", "?S", "title", "x"]]),
                 (["r1.helper", "?S"], [["entry", "?S", "merge", "?P"], ["not", ["field", "?S", "ok", True]]]))
        self.assertEqual(len(c), 2)

    def test_head_constraints(self):
        self.malformed("r1", [{"head": ["violation", "?S", "r2"], "body": [["candidate", "?S"]]}])
        self.malformed("r1", [{"head": ["violation", "?S"], "body": [["candidate", "?S"]]}])
        self.malformed("r1", [{"head": ["helper", "?S"], "body": [["candidate", "?S"]]}])
        self.malformed("r1", [{"head": ["r2.helper", "?S"], "body": [["candidate", "?S"]]}])
        self.malformed("r1", [{"head": ["r1.Helper", "?S"], "body": [["candidate", "?S"]]}])
        self.malformed("r1", [{"head": ["entry", "?S", "x", "y"], "body": [["candidate", "?S"]]}])

    def test_body_predicates_and_arity(self):
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["nosuch", "?S"]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["entry", "?S", "x"]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["violation", "?S"]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["not", ["not", ["candidate", "?S"]]]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["candidate", ["?S"]]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [[1, "?S"]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["candidate", "?S"], "oops"]}])
        rule("r1", (["violation", "?S", "r1"], [["candidate", "?S"], ["r2.other", "?S"], ["violation", "?S", "r2"]]))

    def test_shape(self):
        self.malformed("r1", [])
        self.malformed("r1", "x")
        self.malformed("r1", [{"head": ["violation", "?S", "r1"]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [], "extra": 1}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["candidate", "?"]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["candidate", "?1"]]}])

    def test_range_restriction(self):
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["candidate", "?T"]]}])
        self.malformed("r1", [{"head": ["violation", "?S", "r1"], "body": [["candidate", "?S"], ["not", ["field", "?S", "k", "?V"]]]}])
        self.malformed("r1", [{"head": ["violation", "?_", "r1"], "body": [["candidate", "?S"]]}])
        rule("r1", (["violation", "?S", "r1"], [["candidate", "?S"], ["not", ["field", "?S", "k", "?_"]]]))
        rule("r1", (["r1.fact", "k"], []))


class Stratify(unittest.TestCase):
    def test_negation_orders_strata(self):
        c = rule("r1", (["r1.a", "?S"], [["candidate", "?S"]]),
                 (["violation", "?S", "r1"], [["candidate", "?S"], ["not", ["r1.a", "?S"]]]))
        strata = datalog.stratify(c)
        self.assertEqual([len(s) for s in strata], [1, 1])
        self.assertEqual(strata[0][0][0][0], "r1.a")

    def test_positive_recursion_is_one_stratum(self):
        c = rule("r1", (["r1.reach", "?A", "?B"], [["field", "?A", "next", "?B"]]),
                 (["r1.reach", "?A", "?C"], [["r1.reach", "?A", "?B"], ["field", "?B", "next", "?C"]]))
        self.assertEqual(len(datalog.stratify(c)), 1)

    def test_negative_cycle_is_unstratifiable(self):
        c = rule("r1", (["r1.a", "?S"], [["candidate", "?S"], ["not", ["r1.b", "?S"]]]),
                 (["r1.b", "?S"], [["candidate", "?S"], ["not", ["r1.a", "?S"]]]))
        with self.assertRaises(Refuse) as cm:
            datalog.stratify(c)
        self.assertEqual(cm.exception.reason, "unstratifiable")

    def test_not_violation_is_unstratifiable(self):
        c = rule("r1", (["violation", "?S", "r1"], [["candidate", "?S"], ["not", ["violation", "?S", "r2"]]]))
        with self.assertRaises(Refuse):
            datalog.stratify(c)

    def test_cross_rule_cycle_detected_when_closed(self):
        r1 = rule("r1", (["r1.a", "?S"], [["candidate", "?S"], ["not", ["r2.b", "?S"]]]))
        datalog.stratify(r1)  # dangling r2.b is fine
        r2 = rule("r2", (["r2.b", "?S"], [["candidate", "?S"], ["not", ["r1.a", "?S"]]]))
        with self.assertRaises(Refuse):
            datalog.stratify(r1 + r2)


class Evaluate(unittest.TestCase):
    base = facts(entry={F(1, "proposal", "ann"), F(2, "proposal", "bob"), F(3, "merge", "ann")},
                 field={F(1, "title", "x"), F(2, "title", "y"), F(3, "proposal", 1), F(1, "n", 1), F(2, "n", True)},
                 candidate={F(3)})

    def test_join_and_constant(self):
        c = rule("r1", (["violation", "?S", "r1"], [["entry", "?S", "proposal", "?_"], ["field", "?S", "title", "x"]]))
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), {(1, "r1")})

    def test_base_facts_are_preserved(self):
        c = rule("r1", (["violation", "?S", "r1"], [["candidate", "?S"]]))
        out = datalog.evaluate(c, self.base)
        self.assertEqual(rows(out, "entry"), rows(self.base, "entry"))
        self.assertEqual(rows(out, "violation"), {(3, "r1")})

    def test_negation(self):
        c = rule("r1", (["violation", "?S", "r1"], [["entry", "?S", "proposal", "?_"], ["not", ["field", "?S", "title", "x"]]]))
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), {(2, "r1")})

    def test_wildcard_negation(self):
        c = rule("r1", (["violation", "?S", "r1"], [["entry", "?S", "?_", "?_"], ["not", ["field", "?S", "title", "?_"]]]))
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), {(3, "r1")})

    def test_type_aware_constants(self):
        c = rule("r1", (["violation", "?S", "r1"], [["field", "?S", "n", True]]),)
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), {(2, "r1")})
        c = rule("r1", (["violation", "?S", "r1"], [["field", "?S", "n", 1]]),)
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), {(1, "r1")})

    def test_recursion_and_cross_entry_reference(self):
        c = rule("r1", (["violation", "?S", "r1"], [["entry", "?S", "merge", "?_"], ["field", "?S", "proposal", "?P"],
                                                  ["not", ["entry", "?P", "proposal", "?_"]]]))
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), set())
        g = facts(field={F(1, "next", 2), F(2, "next", 3)})
        c = rule("r1", (["r1.reach", "?A", "?B"], [["field", "?A", "next", "?B"]]),
                 (["r1.reach", "?A", "?C"], [["r1.reach", "?A", "?B"], ["field", "?B", "next", "?C"]]))
        self.assertEqual(rows(datalog.evaluate(c, g), "r1.reach"), {(1, 2), (2, 3), (1, 3)})

    def test_ground_fact_clause(self):
        c = rule("r1", (["r1.flag", "on"], []), (["violation", "?S", "r1"], [["candidate", "?S"], ["r1.flag", "on"]]))
        self.assertEqual(rows(datalog.evaluate(c, self.base), "violation"), {(3, "r1")})

    def test_repeated_variable_in_literal(self):
        c = rule("r1", (["violation", "?S", "r1"], [["field", "?S", "proposal", "?S"]]))
        self.assertEqual(rows(datalog.evaluate(c, facts(field={F(1, "proposal", 1), F(2, "proposal", 1)})), "violation"), {(1, "r1")})


if __name__ == "__main__":
    unittest.main()
