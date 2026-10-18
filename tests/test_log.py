"""Log format: canonical JSON, hashing, parsing, schemas."""
import hashlib
import unittest

from kernel import log
from kernel.log import Refuse

PUB = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIRevXM6fDuOfjLwMr+gzX8x8aToFjGndWTh0Fk5N6BH"
HEX64 = "ab" * 32
HEX40 = "cd" * 20
KEY = {"key_id": "guy-master", "principal": "guy", "pubkey": PUB,
       "powers": ["genesis", "key", "proposal", "merge"]}


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

    def test_proposal_and_merge(self):
        self.assertIsNone(log.check_body("proposal", {"title": "t", "commit": HEX40, "extra": [1]}))
        self.assertEqual(self.refused("proposal", {"title": "t"}), "schema")
        self.assertEqual(self.refused("proposal", {"title": 1, "commit": HEX40}), "schema")
        self.assertIsNone(log.check_body("merge", {"proposal": 3, "commit": HEX40, "checker": HEX64}))
        self.assertEqual(self.refused("merge", {"proposal": True, "commit": HEX40, "checker": HEX64}), "schema")
        self.assertEqual(self.refused("merge", {"proposal": -1, "commit": HEX40, "checker": HEX64}), "schema")

    def test_no_rule_or_repeal_bodies(self):
        for type_ in ("rule", "repeal"):
            self.assertNotIn(type_, log.BODY)
            self.assertNotIn(type_, log.TYPES)

    def test_new_body_schemas(self):
        bodies = {
            "amend": {"id": "A2", "charter": HEX64, "activate_at": 2},
            "push": {"digest": HEX64, "review": "0" * 64},
            "decision": {"kind": "transmute", "subject": "A2"},
            "spec_conflict": {"section": "5", "text": "conflict"},
        }
        for type_, body in bodies.items():
            with self.subTest(type=type_):
                self.assertIsNone(log.check_body(type_, dict(body, **{"extra.key": {"a.b": []}})))
                for field in body:
                    missing = {k: v for k, v in body.items() if k != field}
                    self.assertEqual(self.refused(type_, missing), "schema")
                    for bad in (None, True, [], {}):
                        self.assertEqual(self.refused(type_, dict(body, **{field: bad})), "schema")
        for id_ in ("A2", "Z0", "A000", "B999"):
            self.assertIsNone(log.check_body("amend", dict(bodies["amend"], id=id_)))
        for id_ in ("a2", "A", "A1234", "AA2", "A٢", "A2\n"):
            self.assertEqual(self.refused("amend", dict(bodies["amend"], id=id_)), "schema")
        for kind in ("veto", "promote", "budget", "grant", "transmute", "fix"):
            self.assertIsNone(log.check_body("decision", {"kind": kind, "subject": "\n"}))
        for kind in ("", "Transmute", "transmute\n", "other"):
            self.assertEqual(self.refused("decision", dict(bodies["decision"], kind=kind)), "schema")
        for type_, field in (("decision", "subject"), ("spec_conflict", "section"), ("spec_conflict", "text")):
            self.assertEqual(self.refused(type_, dict(bodies[type_], **{field: ""})), "schema")
        for type_, field in (("amend", "charter"), ("push", "digest"), ("push", "review")):
            for bad in ("F" * 64, "0" * 63, "0" * 65):
                self.assertEqual(self.refused(type_, dict(bodies[type_], **{field: bad})), "schema")
        for bad in ("2", 2.0):
            self.assertEqual(self.refused("amend", dict(bodies["amend"], activate_at=bad)), "schema")

    def test_eight_names_in_key_declarations(self):
        for powers in (list(log.TYPES), [], ["push", "push"]):
            declaration = dict(KEY, powers=powers)
            self.assertIsNone(log.check_body("key", declaration))
            self.assertIsNone(log.check_body("genesis", {"charter": HEX64, "checker": HEX64, "keys": [declaration]}))

    def test_extra_members_allowed_including_dotted_keys(self):
        self.assertIsNone(log.check_body("proposal", {"title": "t", "commit": HEX40, "a.b": 1, "n": {"c.d": []}}))
        self.assertEqual(self.refused("key", dict(KEY, powers=["rule"])), "schema")


if __name__ == "__main__":
    unittest.main()


class ParseOrder(unittest.TestCase):
    """malformed_json (lone surrogate) outranks not_canonical (numbers) whatever the field order."""

    def test_surrogate_wins_over_float(self):
        for line in ('{"a":1.5,"b":"\\ud800"}', '{"a":"\\ud800","b":1.5}', '{"a":99999999999999999,"b":"\\udfff"}'):
            with self.assertRaises(Refuse) as cm:
                log.parse_line(line)
            self.assertEqual(cm.exception.reason, "malformed_json", line)
