"""SSHSIG parsing and strict Ed25519 verification (SPEC.md §signatures)."""
import base64
import hashlib
import json
import os
import random
import tempfile
import unittest

from harness import keys
from kernel import log, sig

HERE = os.path.dirname(__file__)
L = 2**252 + 27742317777372353535851937790883648493


def load(name):
    with open(os.path.join(HERE, "vectors", name)) as f:
        return json.load(f)["vectors"]


def with_s(sig64, s):
    return sig64[:32] + s.to_bytes(32, "little")


class Wire(unittest.TestCase):
    def test_sshstr(self):
        self.assertEqual(sig.sshstr(b"\x00\x00\x00\x03abcZ", 0), (b"abc", 7))
        with self.assertRaises(ValueError):
            sig.sshstr(b"\x00\x00\x00\x09abc", 0)
        with self.assertRaises(ValueError):
            sig.sshstr(b"\x00\x00", 0)


class SshSig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.key = keys.make_key(cls.tmp.name, "k")
        cls.msg = b'{"a":1}'
        cls.b64 = keys.sign(cls.key, cls.msg)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_parse_real_signature(self):
        blob, s64 = sig.parse_sshsig(self.b64)
        self.assertEqual(blob, log.pubkey_blob(self.key.pubkey))
        self.assertEqual(len(s64), 64)

    def test_exact_parse_rejects_deviations(self):
        bad = [keys.rewrap(self.b64, version=2), keys.rewrap(self.b64, namespace="file"),
               keys.rewrap(self.b64, hash_alg="sha256"), keys.rewrap(self.b64, trailing=b"\x00"),
               self.b64[:-8], "!!notbase64", base64.b64encode(b"SSHSIH" + base64.b64decode(self.b64)[6:]).decode(),
               keys.sign(self.key, self.msg, namespace="file"),
               keys.sign(self.key, self.msg, extra=("-O", "hashalg=sha256"))]
        for b in bad:
            with self.assertRaises(ValueError, msg=b[:40]):
                sig.parse_sshsig(b)

    def test_rsa_signature_rejected(self):
        rsa = keys.make_key(self.tmp.name, "rsa", "rsa")
        with self.assertRaises(ValueError):
            sig.parse_sshsig(keys.sign(rsa, self.msg))

    def test_signed_data_layout(self):
        d = sig.signed_data(self.msg)
        self.assertTrue(d.startswith(b"SSHSIG\x00\x00\x00\x0acore-entry\x00\x00\x00\x00\x00\x00\x00\x06sha512\x00\x00\x00\x40"))
        self.assertTrue(d.endswith(hashlib.sha512(self.msg).digest()))

    def test_verify_wrapped(self):
        blob, s64 = sig.parse_sshsig(self.b64)
        self.assertTrue(sig.verify(self.msg, blob, s64))
        self.assertFalse(sig.verify(b'{"a":2}', blob, s64))
        other = keys.make_key(self.tmp.name, "k2")
        self.assertFalse(sig.verify(self.msg, log.pubkey_blob(other.pubkey), s64))

    def test_oracle_agrees_on_legit_and_tampered(self):
        self.assertTrue(keys.ssh_keygen_verify(self.key.pubkey, "p", self.msg, self.b64))
        self.assertFalse(keys.ssh_keygen_verify(self.key.pubkey, "p", b"x", self.b64))


class Ed25519(unittest.TestCase):
    def test_rfc8032_vectors_verify(self):
        for v in load("rfc8032.json"):
            ok = sig.ed25519_verify(bytes.fromhex(v["public_key"]), bytes.fromhex(v["signature"]),
                                    bytes.fromhex(v["message"]))
            self.assertTrue(ok, v["name"])

    def test_rfc8032_vectors_reject_tampering(self):
        v = load("rfc8032.json")[1]
        pub, s64, msg = (bytes.fromhex(v[k]) for k in ("public_key", "signature", "message"))
        self.assertFalse(sig.ed25519_verify(pub, s64, msg + b"x"))
        self.assertFalse(sig.ed25519_verify(pub, bytes([s64[0] ^ 1]) + s64[1:], msg))
        self.assertFalse(sig.ed25519_verify(pub, s64[:63], msg))
        self.assertFalse(sig.ed25519_verify(pub[:31], s64, msg))

    def test_speccheck_edge_cases(self):
        for v in load("speccheck.json"):
            got = sig.ed25519_verify(bytes.fromhex(v["pub_key"]), bytes.fromhex(v["signature"]),
                                     bytes.fromhex(v["message"]))
            self.assertEqual(got, v["expected"], f'case {v["index"]}: {v["comment"]}')

    def test_s_bounds(self):
        v = load("rfc8032.json")[0]
        pub, s64, msg = (bytes.fromhex(v[k]) for k in ("public_key", "signature", "message"))
        s = int.from_bytes(s64[32:], "little")
        self.assertTrue(sig.ed25519_verify(pub, with_s(s64, s), msg))
        self.assertFalse(sig.ed25519_verify(pub, with_s(s64, s + L), msg), "S+L malleation")
        self.assertFalse(sig.ed25519_verify(pub, with_s(s64, L), msg))
        self.assertFalse(sig.ed25519_verify(pub, with_s(s64, 2**253 + s), msg))

    def test_noncanonical_point_encodings(self):
        v = load("rfc8032.json")[0]
        pub, s64, msg = (bytes.fromhex(v[k]) for k in ("public_key", "signature", "message"))
        p = 2**255 - 19
        y = int.from_bytes(pub, "little") & ((1 << 255) - 1)
        self.assertGreater(y, 18, "vector key has a y that cannot be made non-canonical; pick another")
        self.assertIsNone(sig.decode_point((p + 1).to_bytes(32, "little")), "y >= p")
        self.assertIsNone(sig.decode_point(((1 << 255) | 1).to_bytes(32, "little")), "x = 0 with sign bit")
        self.assertIsNotNone(sig.decode_point((1).to_bytes(32, "little")), "y = 1, x = 0, sign 0 is canonical")


class Differential(unittest.TestCase):
    """Kernel vs ssh-keygen on random and mutated signatures; disagreements must be named."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.key = keys.make_key(cls.tmp.name, "k")
        with open(os.path.join(HERE, "vectors", "ssh_keygen_differences.json")) as f:
            cls.allowed = {d["name"] for d in json.load(f)["differences"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def kernel(self, msg, b64):
        try:
            blob, s64 = sig.parse_sshsig(b64)
        except ValueError:
            return False
        return sig.verify(msg, blob, s64)

    def test_random_and_mutated(self):
        rng = random.Random(2026)
        for i in range(12):
            msg = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 64)))
            b64 = keys.sign(self.key, msg)
            self.assertTrue(self.kernel(msg, b64))
            self.assertTrue(keys.ssh_keygen_verify(self.key.pubkey, "p", msg, b64))
            blob, s64 = sig.parse_sshsig(b64)
            mutated = bytearray(s64)
            mutated[rng.randrange(64)] ^= 1 << rng.randrange(8)
            mb64 = keys.rewrap(b64, sig64=bytes(mutated))
            k, o = self.kernel(msg, mb64), keys.ssh_keygen_verify(self.key.pubkey, "p", msg, mb64)
            self.assertEqual(k, o, f"unnamed disagreement on mutation {i}")
            self.assertFalse(k)

    def test_named_difference_s_plus_L(self):
        self.assertIn("s_plus_L", self.allowed)
        msg = b"malleable"
        b64 = keys.sign(self.key, msg)
        blob, s64 = sig.parse_sshsig(b64)
        s = int.from_bytes(s64[32:], "little")
        mb64 = keys.rewrap(b64, sig64=with_s(s64, s + L))
        self.assertFalse(self.kernel(msg, mb64), "kernel must refuse S+L")
        if not keys.ssh_keygen_verify(self.key.pubkey, "p", msg, mb64):
            self.skipTest("this OpenSSH build also rejects S >= L; the named difference is absent here")


if __name__ == "__main__":
    unittest.main()
