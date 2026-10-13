"""The validity predicate: recognition (a)(b)(c), per-type admissibility, CLI."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from harness import build, keys
from harness.build import forbid_title, proposal, rule_body, witness
from kernel import check, log

PY = sys.executable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def refusal(v):
    return (v["seq"], v["rule"], v["reason"]) if not v["ok"] else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.w = build.World(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def ok(self, lg, lapse=()):
        v = check.check(lg.lines)
        self.assertEqual(v, {"ok": True, "entries": len(lg.lines), "lapse": [list(x) for x in lapse]}, v)

    def refused(self, lines, seq, reason, rule=None):
        v = check.check(lines)
        self.assertEqual(refusal(v), (seq, rule, reason), v)
        return v


class Structure(Base):
    def test_empty_log_is_ok(self):
        self.assertEqual(check.check([]), {"ok": True, "entries": 0, "lapse": []})

    def test_genesis_alone(self):
        self.ok(self.w.log())

    def test_malformed_and_noncanonical(self):
        lg = self.w.log()
        self.refused(lg.lines + ["{"], 1, "malformed_json")
        self.refused([lg.lines[0].replace(',"ts"', ', "ts"')], 0, "not_canonical")

    def test_shape(self):
        lg = self.w.log()
        e = log.parse_line(lg.lines[0]); e["extra"] = 1
        self.refused([log.canonical(e)], 0, "schema")

    def test_bad_seq(self):
        lg = self.w.log()
        lg.lines.append(build.make_entry(2, lg.head, "proposal", "ann", proposal(), self.w.ann))
        self.refused(lg.lines, 1, "bad_seq")

    def test_parent_mismatch(self):
        lg = self.w.log()
        lg.lines.append(build.make_entry(1, "ab" * 32, "proposal", "ann", proposal(), self.w.ann))
        self.refused(lg.lines, 1, "parent_mismatch")
        bad = build.Log([build.make_entry(0, "ab" * 32, "genesis", "guy", build.genesis_body(self.w.decls), self.w.guy)])
        self.refused(bad.lines, 0, "parent_mismatch")

    def test_genesis_misplaced(self):
        lg = self.w.log()
        lg.add("genesis", "guy", build.genesis_body(self.w.decls), self.w.guy)
        self.refused(lg.lines, 1, "genesis_misplaced")
        lg = build.Log(); lg.add("proposal", "ann", proposal(), self.w.ann)
        self.refused(lg.lines, 0, "genesis_misplaced")

    def test_no_proposer(self):
        lg = self.w.log(); lg.add("proposal", "", proposal(), self.w.ann)
        self.refused(lg.lines, 1, "no_proposer")

    def test_body_schema(self):
        lg = self.w.log(); lg.add("proposal", "ann", {"title": "t"}, self.w.ann)
        self.refused(lg.lines, 1, "schema")

    def test_fork_is_parent_mismatch(self):
        lg = self.w.log(); lg.add("proposal", "ann", proposal("a"), self.w.ann)
        h1 = lg.head
        lg.add("proposal", "ann", proposal("b"), self.w.ann)
        lg.lines.append(build.make_entry(3, h1, "proposal", "ann", proposal("c"), self.w.ann))
        self.refused(lg.lines, 3, "parent_mismatch")


class Signatures(Base):
    def test_unknown_key(self):
        lg = self.w.log(); lg.add("proposal", "guy", proposal(), self.w.stranger)
        self.refused(lg.lines, 1, "unknown_key")

    def test_proposer_mismatch(self):
        lg = self.w.log(); lg.add("proposal", "guy", proposal(), self.w.ann)
        self.refused(lg.lines, 1, "proposer_mismatch")

    def test_no_power(self):
        lg = self.w.log()
        lg.add("rule", "ann", rule_body("r1", forbid_title("r1", "x"), [witness("proposal", "p", proposal("x"))],
                                        [witness("proposal", "p", proposal("y"))]), self.w.ann)
        self.refused(lg.lines, 1, "no_power")
        lg = self.w.log(); lg.add("repeal", "ann", {"rule_id": "r1"}, self.w.ann)
        self.refused(lg.lines, 1, "no_power")

    def test_bad_signature(self):
        lg = self.w.log(); lg.add("proposal", "ann", proposal("a"), self.w.ann)
        e = log.parse_line(lg.lines[1]); e["body"]["title"] = "b"
        self.refused([lg.lines[0], log.canonical(e)], 1, "bad_signature")
        e = log.parse_line(lg.lines[1]); e["sig"] = "AAAA"
        self.refused([lg.lines[0], log.canonical(e)], 1, "bad_signature")

    def test_history_rewritten(self):
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("a"), self.w.ann)
        lg.add("proposal", "ann", proposal("b"), self.w.ann)
        e = log.parse_line(lg.lines[1]); e["body"]["title"] = "evil"
        edited = log.canonical(e)
        self.refused([lg.lines[0], edited, lg.lines[2]], 1, "bad_signature")
        del e["sig"]
        resigned = build.make_entry(1, lg.lines and log.line_hash(lg.lines[0]), "proposal", "ann", e["body"], self.w.ann)
        self.refused([lg.lines[0], resigned, lg.lines[2]], 2, "parent_mismatch")

    def test_genesis_must_be_signed_by_its_own_key_with_genesis_power(self):
        decls = [build.decl("ann-1", "ann", self.w.ann, ["proposal"])]
        lg = build.Log(); lg.add("genesis", "ann", build.genesis_body(decls), self.w.ann)
        self.refused(lg.lines, 0, "no_power")
        lg = build.Log(); lg.add("genesis", "guy", build.genesis_body(decls), self.w.guy)
        self.refused(lg.lines, 0, "unknown_key")


class Keys(Base):
    def test_key_entry_grants_and_revokes(self):
        lg = self.w.log()
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, ["proposal"]), self.w.guy)
        lg.add("proposal", "stranger", proposal(), self.w.stranger)
        self.ok(lg)
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, []), self.w.guy)
        lg.add("proposal", "stranger", proposal(), self.w.stranger)
        self.refused(lg.lines, 4, "no_power")

    def test_key_entry_cannot_govern_itself(self):
        lg = self.w.log()
        lg.add("key", "stranger", build.decl("stranger-1", "stranger", self.w.stranger, ["key"]), self.w.stranger)
        self.refused(lg.lines, 1, "unknown_key")

    def test_key_power_required(self):
        lg = self.w.log()
        lg.add("key", "ann", build.decl("x", "ann", self.w.stranger, ["proposal"]), self.w.ann)
        self.refused(lg.lines, 1, "no_power")

    def test_duplicate_pubkey(self):
        lg = self.w.log()
        lg.add("key", "guy", build.decl("ann-2", "ann", self.w.ann, ["proposal"]), self.w.guy)
        self.refused(lg.lines, 1, "schema")


class Rules(Base):
    def r1(self):
        return rule_body("r1", forbid_title("r1", "x"), [witness("proposal", "p", proposal("x"))],
                         [witness("proposal", "p", proposal("y"))])

    def test_rule_binds_from_the_next_entry(self):
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("x"), self.w.ann)
        lg.add("rule", "guy", self.r1(), self.w.guy)
        lg.add("proposal", "ann", proposal("y"), self.w.ann)
        self.ok(lg)
        lg.add("proposal", "ann", proposal("x"), self.w.ann)
        self.refused(lg.lines, 4, "violation", "r1")

    def test_rule_entry_is_judged_by_law_before_it(self):
        lg = self.w.log()
        body = rule_body("r1", [{"head": ["violation", "?S", "r1"], "body": [["entry", "?S", "rule", "?_"]]}],
                         [witness("rule", "p", self.r1())], [witness("proposal", "p", proposal("y"))])
        lg.add("rule", "guy", body, self.w.guy)
        self.ok(lg)
        lg.add("rule", "guy", self.r1(), self.w.guy)
        self.refused(lg.lines, 2, "violation", "r1")

    def test_earliest_rule_reported(self):
        lg = self.w.log()
        lg.add("rule", "guy", rule_body("b", forbid_title("b", "x"), [witness("proposal", "p", proposal("x"))],
                                        [witness("proposal", "p", proposal("y"))]), self.w.guy)
        lg.add("rule", "guy", rule_body("a", forbid_title("a", "x"), [witness("proposal", "p", proposal("x"))],
                                        [witness("proposal", "p", proposal("y"))]), self.w.guy)
        lg.add("proposal", "ann", proposal("x"), self.w.ann)
        self.refused(lg.lines, 3, "violation", "b")

    def test_repeal_lifts_the_rule(self):
        lg = self.w.log()
        lg.add("rule", "guy", self.r1(), self.w.guy)
        lg.add("repeal", "guy", {"rule_id": "r1"}, self.w.guy)
        lg.add("proposal", "ann", proposal("x"), self.w.ann)
        self.ok(lg)
        lg.add("repeal", "guy", {"rule_id": "r1"}, self.w.guy)
        self.refused(lg.lines, 4, "unknown_rule")

    def test_duplicate_rule_id_even_after_repeal(self):
        lg = self.w.log()
        lg.add("rule", "guy", self.r1(), self.w.guy)
        lg.add("repeal", "guy", {"rule_id": "r1"}, self.w.guy)
        lg.add("rule", "guy", self.r1(), self.w.guy)
        self.refused(lg.lines, 3, "duplicate_rule")

    def test_rule_malformed(self):
        lg = self.w.log()
        lg.add("rule", "guy", rule_body("r1", [{"head": ["violation", "?S", "zz"], "body": []}],
                                        [witness("proposal", "p", proposal("x"))], [witness("proposal", "p", proposal("y"))]), self.w.guy)
        self.refused(lg.lines, 1, "rule_malformed")
        lg = self.w.log()
        lg.add("rule", "guy", rule_body("r1", forbid_title("r1", "x"), [], [witness("proposal", "p", proposal("y"))]), self.w.guy)
        self.refused(lg.lines, 1, "rule_malformed")
        lg = self.w.log()
        lg.add("rule", "guy", rule_body("r1", forbid_title("r1", "x"), [witness("proposal", "p", {"title": "x"})],
                                        [witness("proposal", "p", proposal("y"))]), self.w.guy)
        self.refused(lg.lines, 1, "rule_malformed")
        lg = self.w.log()
        lg.add("rule", "guy", rule_body("r1", forbid_title("r1", "x"), [witness("wish", "p", proposal("x"))],
                                        [witness("proposal", "p", proposal("y"))]), self.w.guy)
        self.refused(lg.lines, 1, "rule_malformed")

    def test_unstratifiable(self):
        lg = self.w.log()
        c = [{"head": ["r1.a", "?S"], "body": [["candidate", "?S"], ["not", ["r1.b", "?S"]]]},
             {"head": ["r1.b", "?S"], "body": [["candidate", "?S"], ["not", ["r1.a", "?S"]]]},
             {"head": ["violation", "?S", "r1"], "body": [["r1.a", "?S"]]}]
        lg.add("rule", "guy", rule_body("r1", c, [witness("proposal", "p", proposal("x"))],
                                        [witness("proposal", "p", proposal("y"))]), self.w.guy)
        self.refused(lg.lines, 1, "unstratifiable")

    def test_merge_shape_only(self):
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("a"), self.w.ann)
        lg.add("merge", "guy", build.merge(1, "ff" * 32), self.w.guy)
        self.ok(lg)

    def test_prefix_property(self):
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("x"), self.w.ann)
        lg.add("rule", "guy", self.r1(), self.w.guy)
        lg.add("proposal", "ann", proposal("y"), self.w.ann)
        for n in range(len(lg.lines) + 1):
            self.assertTrue(check.check(lg.lines[:n])["ok"], n)


class Cli(Base):
    def run_cli(self, text):
        path = os.path.join(self.tmp.name, "log.jsonl")
        with open(path, "w") as f:
            f.write(text)
        r = subprocess.run([PY, "-m", "kernel.check", path], capture_output=True, text=True, cwd=ROOT)
        return r.returncode, json.loads(r.stdout) if r.stdout else r.stderr

    def test_ok_and_refused_and_usage(self):
        lg = self.w.log(); lg.add("proposal", "ann", proposal(), self.w.ann)
        self.assertEqual(self.run_cli(lg.text()), (0, {"ok": True, "entries": 2, "lapse": []}))
        self.assertEqual(self.run_cli(lg.text().rstrip("\n")), (0, {"ok": True, "entries": 2, "lapse": []}))
        rc, v = self.run_cli(lg.text() + "{bad\n")
        self.assertEqual((rc, v["ok"], v["seq"], v["reason"]), (1, False, 2, "malformed_json"))
        rc, v = self.run_cli("")
        self.assertEqual((rc, v), (0, {"ok": True, "entries": 0, "lapse": []}))
        r = subprocess.run([PY, "-m", "kernel.check"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 2)
        r = subprocess.run([PY, "-m", "kernel.check", "/nonexistent/log.jsonl"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 2)

    def test_undecodable_bytes(self):
        path = os.path.join(self.tmp.name, "bytes.jsonl")
        with open(path, "wb") as f:
            f.write(b'{"a":1}\xff\n')
        r = subprocess.run([PY, "-m", "kernel.check", path], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual((r.returncode, json.loads(r.stdout)["reason"]), (1, "malformed_json"))


if __name__ == "__main__":
    unittest.main()
