"""The validity predicate: recognition (a)(b), the change rule over keys, CLI."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from harness import build, keys
from harness.build import proposal
from kernel import check, log

PY = sys.executable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def refusal(v):
    return (v["seq"], v["reason"]) if not v["ok"] else None


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.w = build.World(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def ok(self, lg):
        v = check.check(lg.lines)
        self.assertEqual(v, {"ok": True, "entries": len(lg.lines)}, v)

    def refused(self, lines, seq, reason):
        v = check.check(lines)
        self.assertEqual(refusal(v), (seq, reason), v)
        self.assertEqual(set(v), {"ok", "seq", "reason", "detail"})
        return v


class Structure(Base):
    def test_empty_log_is_ok(self):
        self.assertEqual(check.check([]), {"ok": True, "entries": 0})

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

    def test_only_eight_types(self):
        lg = self.w.log()
        for type_ in ("rule", "repeal", "wish"):
            lg2 = self.w.log(); lg2.add(type_, "guy", {"rule_id": "r1"}, self.w.guy)
            self.refused(lg2.lines, 1, "schema")
        self.assertEqual(log.TYPES, ("genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict"))
        self.assertEqual(len(lg.lines), 1)

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

    def test_merge_shape_only(self):
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("a"), self.w.ann)
        lg.add("merge", "guy", build.merge(1, "ff" * 32), self.w.guy)
        self.ok(lg)

    def test_prefix_property(self):
        lg = self.w.log()
        lg.add("proposal", "ann", proposal("x"), self.w.ann)
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, ["proposal"]), self.w.guy)
        lg.add("proposal", "stranger", proposal("y"), self.w.stranger)
        lg.add("merge", "guy", build.merge(1), self.w.guy)
        for n in range(len(lg.lines) + 1):
            self.assertTrue(check.check(lg.lines[:n])["ok"], n)


class Signatures(Base):
    def test_unknown_key(self):
        lg = self.w.log(); lg.add("proposal", "guy", proposal(), self.w.stranger)
        self.refused(lg.lines, 1, "unknown_key")

    def test_proposer_mismatch(self):
        lg = self.w.log(); lg.add("proposal", "guy", proposal(), self.w.ann)
        self.refused(lg.lines, 1, "proposer_mismatch")

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
        self.refused([lg.lines[0], log.canonical(e), lg.lines[2]], 1, "bad_signature")
        resigned = build.make_entry(1, log.line_hash(lg.lines[0]), "proposal", "ann", e["body"], self.w.ann)
        self.refused([lg.lines[0], resigned, lg.lines[2]], 2, "parent_mismatch")

    def test_reserved_bytes_are_bad_signature(self):
        lg = self.w.log(); lg.add("proposal", "ann", proposal("a"), self.w.ann)
        e = log.parse_line(lg.lines[1]); e["sig"] = keys.rewrap(e["sig"], reserved=b"\x00")
        self.refused([lg.lines[0], log.canonical(e)], 1, "bad_signature")

    def test_genesis_must_be_signed_by_its_own_key_with_genesis_power(self):
        decls = [build.decl("ann-1", "ann", self.w.ann, ["proposal"])]
        lg = build.Log(); lg.add("genesis", "ann", build.genesis_body(decls), self.w.ann)
        self.refused(lg.lines, 0, "no_power")
        lg = build.Log(); lg.add("genesis", "guy", build.genesis_body(decls), self.w.guy)
        self.refused(lg.lines, 0, "unknown_key")


class Change(Base):
    """§3 Change at C0: `key` entries, signed by a key holding the `key` power."""

    def test_key_entry_grants_and_revokes(self):
        lg = self.w.log()
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, ["proposal"]), self.w.guy)
        lg.add("proposal", "stranger", proposal(), self.w.stranger)
        self.ok(lg)
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, []), self.w.guy)
        lg.add("proposal", "stranger", proposal(), self.w.stranger)
        self.refused(lg.lines, 4, "no_power")

    def test_revocation_does_not_reach_back(self):
        lg = self.w.log()
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, ["proposal"]), self.w.guy)
        lg.add("proposal", "stranger", proposal("before"), self.w.stranger)
        lg.add("key", "guy", build.decl("stranger-1", "stranger", self.w.stranger, []), self.w.guy)
        lg.add("proposal", "ann", proposal("after"), self.w.ann)
        self.ok(lg)

    def test_key_entry_cannot_govern_itself(self):
        lg = self.w.log()
        lg.add("key", "stranger", build.decl("stranger-1", "stranger", self.w.stranger, ["key"]), self.w.stranger)
        self.refused(lg.lines, 1, "unknown_key")

    def test_unsigned_change_is_no_power(self):
        lg = self.w.log()
        lg.add("key", "ann", build.decl("x", "ann", self.w.stranger, ["proposal"]), self.w.ann)
        self.refused(lg.lines, 1, "no_power")

    def test_redeclaration_changes_principal_and_powers(self):
        lg = self.w.log()
        lg.add("key", "guy", build.decl("ann-1", "ann", self.w.ann, ["proposal", "merge"]), self.w.guy)
        lg.add("merge", "ann", build.merge(0), self.w.ann)
        self.ok(lg)

    def test_weak_key_is_bad_key_at_declaration(self):
        for name, pub32 in keys.weak_keys():
            lg = self.w.log()
            lg.add("key", "guy", build.decl("eve-1", "eve", keys.fake_key(pub32), ["proposal"]), self.w.guy)
            v = self.refused(lg.lines, 1, "bad_key")
            self.assertIn("eve-1", v["detail"], name)
            decls = self.w.decls + [build.decl("eve-1", "eve", keys.fake_key(pub32), [])]
            lg = build.Log(); lg.add("genesis", "guy", build.genesis_body(decls), self.w.guy)
            self.refused(lg.lines, 0, "bad_key")

    def test_weak_key_without_power_is_no_power_first(self):
        name, pub32 = keys.weak_keys()[0]
        lg = self.w.log()
        lg.add("key", "ann", build.decl("eve-1", "eve", keys.fake_key(pub32), []), self.w.ann)
        self.refused(lg.lines, 1, "no_power")

    def test_duplicate_pubkey_is_bad_key(self):
        lg = self.w.log()
        lg.add("key", "guy", build.decl("ann-2", "ann", self.w.ann, ["proposal"]), self.w.guy)
        self.refused(lg.lines, 1, "bad_key")
        decls = self.w.decls + [build.decl("guy-2", "guy", self.w.guy, ["merge"])]
        lg = build.Log(); lg.add("genesis", "guy", build.genesis_body(decls), self.w.guy)
        self.refused(lg.lines, 0, "bad_key")


class OpeningState(Base):
    def fold(self, lg):
        state = check.EMPTY
        for i, line in enumerate(lg.lines):
            state = check.check_entry(state, i, line)
        return state

    def test_genesis_state_and_forward_amendments(self):
        lg = self.w.log()
        founding = self.fold(lg)
        self.assertEqual((founding.charter, founding.charter_at(0), founding.trusted_base, founding.transmuted),
                         (build.HEX64, build.HEX64, build.HEX64, frozenset()))
        lg.add("amend", "guy", {"id": "A2", "charter": "aa" * 32, "activate_at": 5}, self.w.guy)
        first = self.fold(lg)
        self.assertEqual(first.charter, "aa" * 32)
        self.assertEqual([first.charter_at(i) for i in (0, 1, 4, 5, 6)], [build.HEX64] * 3 + ["aa" * 32] * 2)
        lg.add("amend", "guy", {"id": "A3", "charter": "bb" * 32, "activate_at": 4}, self.w.guy)
        second = self.fold(lg)
        self.assertEqual([second.charter_at(i) for i in (3, 4, 5, 6)], [build.HEX64] + ["bb" * 32] * 3)
        self.assertEqual(second.charter, "bb" * 32)
        self.assertEqual(founding.charter, build.HEX64)
        self.assertEqual(first.charter_at(5), "aa" * 32)
        self.ok(lg)  # transmutation is enforced by the judge, not the kernel

    def test_activation_and_unique_id_are_schema_before_signature(self):
        for height in (-1, 0, 1, True, "2"):
            lg = self.w.log()
            lg.add("amend", "ann", {"id": "A2", "charter": build.HEX64, "activate_at": height}, self.w.ann)
            self.refused(lg.lines, 1, "schema")
        lg = self.w.log()
        lg.add("amend", "guy", {"id": "A2", "charter": build.HEX64, "activate_at": 2}, self.w.guy)
        lg.add("amend", "ann", {"id": "A2", "charter": build.HEX64, "activate_at": 9}, self.w.ann)
        self.refused(lg.lines, 2, "schema")

    def test_new_types_require_power_and_allow_later_grants(self):
        bodies = {
            "amend": {"id": "A2", "charter": build.HEX64, "activate_at": 10},
            "push": {"digest": "aa" * 32, "review": "0" * 64},
            "decision": {"kind": "transmute", "subject": "A2"},
            "spec_conflict": {"section": "5", "text": "conflict"},
        }
        for type_, body in bodies.items():
            lg = self.w.log(); lg.add(type_, "ann", body, self.w.ann)
            self.refused(lg.lines, 1, "no_power")
            lg = self.w.log()
            lg.add("key", "guy", build.decl("ann-1", "ann", self.w.ann, [type_]), self.w.guy)
            lg.add(type_, "ann", body, self.w.ann)
            self.ok(lg)

    def test_push_transmute_and_no_effect_types(self):
        lg = self.w.log()
        lg.add("push", "guy", {"digest": "ab" * 32, "review": "0" * 64}, self.w.guy)
        state = self.fold(lg)
        self.assertEqual(state.trusted_base, "ab" * 32)
        lg.add("push", "guy", {"digest": "cd" * 32, "review": "ef" * 32}, self.w.guy)
        lg.add("decision", "guy", {"kind": "transmute", "subject": "A2"}, self.w.guy)
        lg.add("decision", "guy", {"kind": "transmute", "subject": "A2"}, self.w.guy)
        lg.add("decision", "guy", {"kind": "transmute", "subject": "A3"}, self.w.guy)
        state = self.fold(lg)
        self.assertEqual(state.transmuted, {"A2", "A3"})
        self.assertEqual(state.trusted_base, "cd" * 32)
        for kind in ("veto", "promote", "budget", "grant", "fix"):
            lg.add("decision", "guy", {"kind": kind, "subject": "A4"}, self.w.guy)
        lg.add("spec_conflict", "guy", {"section": "8", "text": "conflict"}, self.w.guy)
        lg.add("proposal", "guy", proposal(), self.w.guy)
        lg.add("merge", "guy", build.merge(1), self.w.guy)
        after = self.fold(lg)
        self.assertEqual(after._replace(head=state.head), state)
        self.assertEqual(after.head, lg.head)
        self.assertEqual(check.EMPTY.transmuted, frozenset())


class Cli(Base):
    def run_cli(self, text):
        path = os.path.join(self.tmp.name, "log.jsonl")
        with open(path, "w") as f:
            f.write(text)
        r = subprocess.run([PY, "-m", "kernel.check", path], capture_output=True, text=True, cwd=ROOT)
        return r.returncode, json.loads(r.stdout) if r.stdout else r.stderr

    def test_ok_and_refused_and_usage(self):
        lg = self.w.log(); lg.add("proposal", "ann", proposal(), self.w.ann)
        self.assertEqual(self.run_cli(lg.text()), (0, {"ok": True, "entries": 2}))
        self.assertEqual(self.run_cli(lg.text().rstrip("\n")), (0, {"ok": True, "entries": 2}))
        rc, v = self.run_cli(lg.text() + "{bad\n")
        self.assertEqual((rc, v["ok"], v["seq"], v["reason"]), (1, False, 2, "malformed_json"))
        rc, v = self.run_cli("")
        self.assertEqual((rc, v), (0, {"ok": True, "entries": 0}))
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
