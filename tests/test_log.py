"""Log format: canonical JSON, hashing, parsing, schemas, fact extraction."""
import hashlib
import unittest

from kernel import log
from kernel.log import Refuse

PUB = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIRevXM6fDuOfjLwMr+gzX8x8aToFjGndWTh0Fk5N6BH"
HEX64 = "ab" * 32
HEX40 = "cd" * 20
KEY = {"key_id": "guy-master", "principal": "guy", "pubkey": PUB,
       "powers": ["genesis", "key", "rule", "repeal", "proposal", "merge"]}


def entry(**over):
    e = {"seq": 1, "parent": HEX64, "ts": "2026-10-13T00:00:00Z", "type": "proposal",
         "proposer": "guy", "body": {"title": "t", "commit": HEX40}, "sig": "AAAA"}
    e.update(over)
    return e


class Canonical(unittest.TestCase):
    def test_sorted_keys_no_whitespace(self):
        self.assertEqual(log.canonical({"b": 1, "a": "x"}), '{"a":"x","b":1}')

    def test_ascii_escapes(self):
        self.assertEqual(log.canonical("é\n\x01/"), '"\\u00e9\\n\\u0001/"')
        self.assertEqual(log.canonical("\U0001F600"), '"\\ud83d\\ude00"')

    def test_nested(self):
        self.assertEqual(log.canonical({"z": [1, {"y": None, "x": True}]}),
                         '{"z":[1,{"x":true,"y":null}]}')


class LineHash(unittest.TestCase):
    def test_sha256_of_utf8_bytes(self):
        self.assertEqual(log.line_hash("abc"), hashlib.sha256(b"abc").hexdigest())


class ParseLine(unittest.TestCase):
    def refused(self, line):
        with self.assertRaises(Refuse) as cm:
            log.parse_line(line)
        return cm.exception.reason

    def test_canonical_object_parses(self):
        self.assertEqual(log.parse_line('{"a":1}'), {"a": 1})

    def test_not_json(self):
        self.assertEqual(self.refused("nope"), "malformed_json")

    def test_not_object(self):
        self.assertEqual(self.refused("[1]"), "malformed_json")

    def test_whitespace_is_not_canonical(self):
        self.assertEqual(self.refused('{"a": 1}'), "not_canonical")

    def test_unsorted_keys(self):
        self.assertEqual(self.refused('{"b":1,"a":2}'), "not_canonical")

    def test_float(self):
        self.assertEqual(self.refused('{"a":1.0}'), "not_canonical")

    def test_negative_zero_and_exponent(self):
        self.assertEqual(self.refused('{"a":-0}'), "not_canonical")
        self.assertEqual(self.refused('{"a":1e2}'), "not_canonical")

    def test_integer_bound(self):
        self.assertEqual(log.parse_line('{"a":9007199254740991}'), {"a": 2**53 - 1})
        self.assertEqual(self.refused('{"a":9007199254740992}'), "not_canonical")
        self.assertEqual(self.refused('{"a":-9007199254740992}'), "not_canonical")

    def test_duplicate_keys(self):
        self.assertEqual(self.refused('{"a":1,"a":2}'), "not_canonical")

    def test_lone_surrogate(self):
        self.assertEqual(self.refused('{"a":"\\ud800"}'), "malformed_json")

    def test_raw_non_ascii(self):
        self.assertEqual(self.refused('{"a":"é"}'), "not_canonical")


class Shape(unittest.TestCase):
    def refused(self, e):
        with self.assertRaises(Refuse) as cm:
            log.check_shape(e)
        return cm.exception.reason

    def test_good_entry(self):
        self.assertIsNone(log.check_shape(entry()))

    def test_missing_and_extra_keys(self):
        e = entry(); del e["ts"]
        self.assertEqual(self.refused(e), "schema")
        self.assertEqual(self.refused(entry(extra=1)), "schema")

    def test_field_types(self):
        self.assertEqual(self.refused(entry(seq=True)), "schema")
        self.assertEqual(self.refused(entry(seq=-1)), "schema")
        self.assertEqual(self.refused(entry(parent="ab")), "schema")
        self.assertEqual(self.refused(entry(parent=HEX64.upper())), "schema")
        self.assertEqual(self.refused(entry(ts="2026-10-13 00:00:00")), "schema")
        self.assertEqual(self.refused(entry(type="wish")), "schema")
        self.assertEqual(self.refused(entry(proposer=1)), "schema")
        self.assertEqual(self.refused(entry(body=[])), "schema")
        self.assertEqual(self.refused(entry(sig=1)), "schema")
        self.assertEqual(self.refused(entry(sig="not base64!")), "schema")

    def test_empty_proposer_is_shape_valid(self):
        self.assertIsNone(log.check_shape(entry(proposer="")))


class Body(unittest.TestCase):
    def refused(self, t, body):
        with self.assertRaises(Refuse) as cm:
            log.check_body(t, body)
        return cm.exception.reason

    def test_genesis(self):
        self.assertIsNone(log.check_body("genesis", {"charter": HEX64, "checker": HEX64, "keys": [KEY]}))
        self.assertEqual(self.refused("genesis", {"charter": HEX64, "checker": HEX64}), "schema")
        self.assertEqual(self.refused("genesis", {"charter": HEX64, "checker": HEX64, "keys": "x"}), "schema")
        bad = dict(KEY, powers=["wish"])
        self.assertEqual(self.refused("genesis", {"charter": HEX64, "checker": HEX64, "keys": [bad]}), "schema")

    def test_key_declaration(self):
        self.assertIsNone(log.check_body("key", KEY))
        self.assertIsNone(log.check_body("key", dict(KEY, powers=[])))
        self.assertEqual(self.refused("key", dict(KEY, key_id="Guy Master")), "schema")
        self.assertEqual(self.refused("key", dict(KEY, principal="")), "schema")
        self.assertEqual(self.refused("key", dict(KEY, pubkey="ssh-rsa AAAAB3NzaC1yc2E=")), "schema")
        self.assertEqual(self.refused("key", dict(KEY, pubkey=PUB + " comment")), "schema")
        self.assertEqual(self.refused("key", dict(KEY, pubkey="ssh-ed25519 AAAA")), "schema")
        self.assertEqual(self.refused("key", dict(KEY, powers="rule")), "schema")

    def test_rule_repeal_proposal_merge(self):
        rule = {"rule_id": "r1", "clauses": [], "witnesses": {"violating": [], "satisfying": []}}
        self.assertIsNone(log.check_body("rule", rule))
        self.assertIsNone(log.check_body("rule", dict(rule, replacements={})))
        self.assertEqual(self.refused("rule", dict(rule, rule_id="R.1")), "schema")
        self.assertEqual(self.refused("rule", dict(rule, witnesses={"violating": []})), "schema")
        self.assertEqual(self.refused("rule", dict(rule, replacements=[])), "schema")
        self.assertIsNone(log.check_body("repeal", {"rule_id": "r1"}))
        self.assertEqual(self.refused("repeal", {}), "schema")
        self.assertIsNone(log.check_body("proposal", {"title": "t", "commit": HEX40, "extra": [1]}))
        self.assertEqual(self.refused("proposal", {"title": "t"}), "schema")
        self.assertIsNone(log.check_body("merge", {"proposal": 3, "commit": HEX40, "checker": HEX64}))
        self.assertEqual(self.refused("merge", {"proposal": True, "commit": HEX40, "checker": HEX64}), "schema")

    def test_dotted_keys_forbidden_anywhere(self):
        self.assertEqual(self.refused("proposal", {"title": "t", "commit": HEX40, "a.b": 1}), "schema")
        self.assertEqual(self.refused("proposal", {"title": "t", "commit": HEX40, "a": {"b.c": 1}}), "schema")


class Facts(unittest.TestCase):
    def test_flatten(self):
        body = {"a": 1, "b": {"c": "x"}, "d": [1, 2], "e": [{"f": True}], "g": {}, "h": None, "i": []}
        self.assertEqual(log.flatten(body), [("a", 1), ("b.c", "x"), ("d", 1), ("d", 2), ("e.0.f", True), ("h", None)])

    def test_atoms_are_type_aware(self):
        self.assertNotEqual(log.atom(1), log.atom(True))
        self.assertNotEqual(log.atom("1"), log.atom(1))
        self.assertNotEqual(log.atom(0), log.atom(None))
        self.assertEqual(log.atom(1), log.atom(1))
        self.assertEqual(log.untag(log.atom("x")), "x")


if __name__ == "__main__":
    unittest.main()
