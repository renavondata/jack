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

    def test_only_ten_types(self):
        lg = self.w.log()
        for type_ in ("rule", "repeal", "wish"):
            lg2 = self.w.log(); lg2.add(type_, "guy", {"rule_id": "r1"}, self.w.guy)
            self.refused(lg2.lines, 1, "schema")
        self.assertEqual(log.TYPES, ("genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict",
                                     "forecast", "resolution"))
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

    def test_last_key_power_cannot_be_lost(self):
        without_key = [t for t in build.ALL if t != "key"]
        lg = self.w.log()
        lg.add("key", "guy", build.decl("guy-master", "guy", self.w.guy, without_key), self.w.guy)
        self.refused(lg.lines, 1, "bad_key")
        lg = self.w.log()
        lg.add("key", "guy", build.decl("guy-master", "guy", self.w.guy, build.ALL), self.w.guy)
        self.ok(lg)
        # Another holder first: then the original holder may drop it, and the last one may not.
        lg = self.w.log()
        lg.add("key", "guy", build.decl("ann-1", "ann", self.w.ann, ["proposal", "key"]), self.w.guy)
        lg.add("key", "guy", build.decl("guy-master", "guy", self.w.guy, without_key), self.w.guy)
        self.ok(lg)
        lg.add("key", "ann", build.decl("ann-1", "ann", self.w.ann, []), self.w.ann)
        self.refused(lg.lines, 3, "bad_key")
        # Genesis is untouched: it may found a log in which no key holds `key`.
        lg = build.Log(); lg.add("genesis", "guy", build.genesis_body([build.decl("guy-master", "guy", self.w.guy, without_key)]), self.w.guy)
        self.ok(lg)

    def test_last_key_rule_after_weakness_and_ownership(self):
        name, pub32 = keys.weak_keys()[0]
        lg = self.w.log()
        lg.add("key", "guy", build.decl("guy-master", "guy", keys.fake_key(pub32), []), self.w.guy)
        self.assertIn("non-canonical or small-order", self.refused(lg.lines, 1, "bad_key")["detail"])
        lg = self.w.log()
        lg.add("key", "guy", build.decl("guy-master", "guy", self.w.ann, []), self.w.guy)
        self.assertIn("belongs to ann-1", self.refused(lg.lines, 1, "bad_key")["detail"])

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


T0, T1, T2, EARLY = "2026-10-25T00:00:00Z", "2026-10-25T00:00:01Z", "2026-11-01T00:00:00Z", "2026-10-24T23:59:59Z"


class Ledger(Base):
    """C1a (SPEC §7, §8 steps 2a, 7, 8a, 9): timestamps do not decrease; forecasts and their resolutions, by principal."""
    fold = OpeningState.fold

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        w = cls.w
        cls.key = {"guy": w.guy, "ann": w.ann, "ann2": keys.make_key(cls.tmp.name, "ann2"), "builder": w.parties["builder"],
                   "stranger": w.stranger}
        cls.decls = [build.decl("guy-master", "guy", w.guy, build.ALL), build.decl("ann-1", "ann", w.ann, ["proposal", "forecast", "resolution"]),
                     build.decl("ann-2", "ann", cls.key["ann2"], ["resolution"]),  # a second key of the same party
                     build.decl("builder-1", "builder", cls.key["builder"], ["forecast", "resolution"])]

    def lg(self, *steps):
        """Genesis, then each step: ("f", signer, overrides) a forecast at T0, or ("r", forecast seq, signer, overrides) at T1;
        the signer "ann2" signs as ann, "as:X" overrides the proposer."""
        lg = self.w.log(decls=self.decls)
        for step in steps:
            kind, *rest = step
            seq = rest.pop(0) if kind == "r" else None
            signer, over = rest[0], dict(rest[1]) if len(rest) > 1 else {}
            who, ts = over.pop("as", signer.rstrip("2")), over.pop("ts", T0 if kind == "f" else T1)
            body = {"claim": "it rains", "p": 700, "resolves_by": T2} if kind == "f" else {"forecast": seq, "outcome": 1, "evidence": "run 4"}
            lg.add("forecast" if kind == "f" else "resolution", who, dict(body, **over), self.key[signer], ts=ts)
        return lg

    def test_timestamps_equal_or_later_are_admitted_earlier_is_ts_decreased(self):
        lg = self.w.log(decls=self.decls)  # genesis at build.TS, 2026-10-13
        for ts in (build.TS, T0, T0):
            lg.add("proposal", "ann", proposal(), self.w.ann, ts=ts)
        self.ok(lg)
        for earlier in (EARLY, "2025-12-31T23:59:59Z", "0001-01-01T00:00:00Z"):
            bad = build.Log(lg.lines); bad.add("proposal", "ann", proposal(), self.w.ann, ts=earlier)
            self.refused(bad.lines, 4, "ts_decreased")
        g = build.Log(); g.add("genesis", "guy", build.genesis_body(self.decls), self.w.guy, ts="9999-12-31T23:59:59Z")
        self.ok(g)  # genesis has no parent and is exempt
        g.add("proposal", "ann", proposal(), self.w.ann, ts=T0)
        self.refused(g.lines, 1, "ts_decreased")

    def test_ts_decreased_is_step_2a_after_shape_before_seq(self):
        lg = self.lg(("f", "ann", {"ts": T1}))
        for line in (build.make_entry(9, lg.head, "proposal", "", {"no": "body"}, self.w.stranger, ts=T0),  # bad seq, proposer, body, key
                     build.make_entry(2, "00" * 32, "genesis", "ann", proposal(), self.w.ann, ts=T0)):  # parent, genesis misplaced
            self.refused(lg.lines + [line], 2, "ts_decreased")
        e = log.parse_line(build.make_entry(2, lg.head, "proposal", "ann", proposal(), self.w.ann, ts=T0)); e["extra"] = 1
        self.refused(lg.lines + [log.canonical(e)], 2, "schema")  # shape is step 2

    def test_admitted_ledger_and_its_state(self):
        lg = self.lg(("f", "ann", {"type": "world.screen", "args": {"n": [1]}}), ("f", "guy", {"p": 1, "resolves_by": T0}),
                     ("f", "builder", {"p": 999}), ("r", 1, "builder", {"outcome": 0, "note": "x"}), ("r", 2, "ann"), ("r", 3, "ann2"))
        self.ok(lg)  # resolves_by equal to ts; ann's second key resolves builder's forecast; extra members
        state = self.fold(lg)
        self.assertEqual((state.forecasts, state.resolved, state.ts), ({1: "ann", 2: "guy", 3: "builder"}, {1, 2, 3}, T1))
        self.assertEqual((check.EMPTY.forecasts, check.EMPTY.resolved, check.EMPTY.ts), ({}, frozenset(), None))
        old = self.w.log(); old.add("proposal", "ann", proposal(), self.w.ann); old.add("merge", "guy", build.merge(1), self.w.guy)
        self.ok(old)  # earlier logs replay unchanged

    def test_refusals_each_at_its_step(self):
        cases = [  # (steps, (seq, reason)); each is one refusal, its twin admitted in test_admitted_ledger_and_its_state
            ((("f", "ann", {"resolves_by": EARLY}),), (1, "schema")),  # resolves_by before ts, step 7
            ((("f", "stranger", {"as": "ann", "resolves_by": EARLY}),), (1, "schema")),  # ... before the signature
            ((("f", "ann", {"p": 0}),), (1, "schema")), ((("f", "ann", {"p": 1000}),), (1, "schema")),
            ((("f", "ann", {"p": True}),), (1, "schema")), ((("f", "ann", {"p": False}),), (1, "schema")),
            ((("f", "ann"), ("r", 1, "builder", {"outcome": False})), (2, "schema")),
            ((("f", "ann"), ("r", 1, "builder", {"outcome": True})), (2, "schema")),
            ((("f", "ann2"),), (1, "no_power")),  # ann-2 holds resolution, not forecast
            ((("f", "ann"), ("r", 0, "builder")), (2, "schema")), ((("f", "ann"), ("r", 2, "builder")), (2, "schema")),  # genesis; itself
            ((("f", "ann"), ("r", 9, "builder")), (2, "schema")),  # the future
            ((("f", "ann"), ("r", 0, "stranger", {"as": "builder"})), (2, "schema")),  # dangling outranks unknown_key
            ((("f", "ann"), ("r", 1, "stranger", {"as": "builder"})), (2, "unknown_key")),
            ((("f", "ann"), ("r", 1, "builder"), ("r", 1, "guy", {"outcome": 0})), (3, "schema")),  # double
            ((("f", "ann"), ("r", 1, "builder"), ("r", 1, "ann")), (3, "schema")),  # a self-resolution of a resolved forecast
            ((("f", "ann"), ("r", 1, "ann")), (2, "self_judged")), ((("f", "ann"), ("r", 1, "ann2")), (2, "self_judged")),  # by principal
            ((("f", "guy"), ("r", 1, "guy")), (2, "self_judged")),
            ((("f", "ann"), ("r", 1, "builder", {"as": "ann"})), (2, "proposer_mismatch")),
        ]
        for steps, verdict in cases:
            self.refused(self.lg(*steps).lines, *verdict)
        lg = self.lg(("f", "ann"), ("r", 1, "ann"))
        e = log.parse_line(lg.lines[-1]); e["body"]["evidence"] = "tampered"
        self.refused(lg.lines[:-1] + [log.canonical(e)], 2, "bad_signature")  # not self_judged: the party is not yet a fact
        self.ok(self.lg(("f", "ann"), ("r", 1, "builder")))  # the twin of every refusal above
        nopower = self.w.log(); nopower.add("forecast", "ann", {"claim": "c", "p": 5, "resolves_by": T2}, self.w.ann, ts=T0)
        self.refused(nopower.lines, 1, "no_power")


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
