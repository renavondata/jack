"""Throwaway SSH keys and signatures for tests, pins and the simulator.

Not part of the kernel. Shells out to ssh-keygen; the kernel never does.
"""
import base64
import json
import os
import struct
import subprocess
import tempfile
from collections import namedtuple

Key = namedtuple("Key", "path pubkey")  # path to private key; pubkey = "ssh-ed25519 <b64>"

NAMESPACE = "core-entry"
WEAK_KEYS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "vectors", "weak_keys.json")


def make_key(directory, name, type_="ed25519"):
    path = os.path.join(directory, name)
    subprocess.run(["ssh-keygen", "-q", "-t", type_, "-N", "", "-C", "", "-f", path], check=True)
    with open(path + ".pub") as f:
        pub = " ".join(f.read().split()[:2])
    return Key(path, pub)


def fake_key(pub32):
    """A Key with no private half: a public key text for 32 raw bytes (weak keys, tests only)."""
    blob = sshstr(b"ssh-ed25519") + sshstr(pub32)
    return Key(None, "ssh-ed25519 " + base64.b64encode(blob).decode())


def weak_keys():
    """[(name, 32 bytes)] every public key the checker must refuse at declaration."""
    with open(WEAK_KEYS) as f:
        v = json.load(f)
    return [(w["name"], bytes.fromhex(w["pub_key"])) for group in ("small_order", "non_canonical") for w in v[group]]


def dearmour(text):
    lines = [l for l in text.strip().splitlines() if not l.startswith("-----")]
    return "".join(lines)


def armour(b64):
    body = "\n".join(b64[i:i + 70] for i in range(0, len(b64), 70))
    return f"-----BEGIN SSH SIGNATURE-----\n{body}\n-----END SSH SIGNATURE-----\n"


def sign(key, message, namespace=NAMESPACE, extra=()):
    """ssh-keygen -Y sign over `message` (bytes); returns the base64 payload."""
    out = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", key.path, "-n", namespace, *extra, "-"],
                         input=message, capture_output=True, check=True)
    return dearmour(out.stdout.decode())


def ssh_keygen_verify(pubkey, principal, message, sig_b64, namespace=NAMESPACE):
    """Independent oracle: does ssh-keygen -Y verify accept this signature?"""
    with tempfile.TemporaryDirectory() as d:
        allowed = os.path.join(d, "allowed_signers")
        sigfile = os.path.join(d, "msg.sig")
        with open(allowed, "w") as f:
            f.write(f'{principal} namespaces="{namespace}" {pubkey}\n')
        with open(sigfile, "w") as f:
            f.write(armour(sig_b64))
        r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", allowed, "-I", principal,
                            "-n", namespace, "-s", sigfile], input=message, capture_output=True)
        return r.returncode == 0


def sshstr(b):
    return struct.pack(">I", len(b)) + b


def rewrap(sig_b64, sig64=None, namespace=None, hash_alg=None, version=None, trailing=b"", pubkey_blob=None, reserved=None):
    """Re-encode an SSHSIG payload with fields replaced (for crafting bad signatures)."""
    raw = base64.b64decode(sig_b64)
    off = 10
    fields = []
    for _ in range(5):
        n = struct.unpack(">I", raw[off:off + 4])[0]
        fields.append(raw[off + 4:off + 4 + n])
        off += 4 + n
    pub, ns, res, halg, inner = fields
    if sig64 is not None:
        inner = sshstr(b"ssh-ed25519") + sshstr(sig64)
    blob = (b"SSHSIG" + struct.pack(">I", 1 if version is None else version)
            + sshstr(pubkey_blob or pub) + sshstr(ns if namespace is None else namespace.encode())
            + sshstr(res if reserved is None else reserved) + sshstr(halg if hash_alg is None else hash_alg.encode())
            + sshstr(inner) + trailing)
    return base64.b64encode(blob).decode()
