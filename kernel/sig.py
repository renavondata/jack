"""SSHSIG parsing and strict Ed25519 verification, standard library only.

CHARTER §9.1 (`ssh-keygen -Y sign`, namespace core-entry). Verification follows
RFC 8032 §5.1.7 with the strict choices fixed in SPEC.md: S < L, canonical
encodings of A and R, cofactorless equation [S]B == R + [k]A with k = SHA-512
(R ‖ A ‖ M) reduced modulo L, as every deployed verifier and the published
edge-case vectors assume. Only ssh-ed25519 keys and sha512 SSHSIG payloads with
an empty reserved field (so one signature has one encoding). A public key of
small order or in a non-canonical encoding is weak and may not be declared.
"""
import base64
import hashlib
import struct

NAMESPACE = b"core-entry"
P = 2**255 - 19
L = 2**252 + 27742317777372353535851937790883648493
D = (-121665 * pow(121666, -1, P)) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)
BASE = (15112221349535400772501151409588531511454012693041857206046113283949847762202,
        46316835694926478169428394003475163141307993866256225615783033603165251855960)
IDENTITY = (1).to_bytes(32, "little")


def sshstr(buf, off):
    """Read one SSH wire string (uint32 length, bytes) at `off`."""
    if off + 4 > len(buf):
        raise ValueError("truncated length")
    (n,) = struct.unpack(">I", buf[off:off + 4])
    if off + 4 + n > len(buf):
        raise ValueError("truncated string")
    return buf[off + 4:off + 4 + n], off + 4 + n


def _pack(b):
    return struct.pack(">I", len(b)) + b


def parse_sshsig(b64):
    """Base64 SSHSIG payload → (public key blob, 64-byte signature); ValueError if not exact."""
    try:
        raw = base64.b64decode(b64, validate=True)
    except (ValueError, TypeError):
        raise ValueError("base64") from None
    if raw[:10] != b"SSHSIG\x00\x00\x00\x01":
        raise ValueError("magic or version")
    pub, off = sshstr(raw, 10)
    namespace, off = sshstr(raw, off)
    reserved, off = sshstr(raw, off)
    hash_alg, off = sshstr(raw, off)
    inner, off = sshstr(raw, off)
    if off != len(raw) or namespace != NAMESPACE or hash_alg != b"sha512" or reserved != b"":
        raise ValueError("trailing bytes, namespace, hash algorithm or reserved field")
    sig_type, ioff = sshstr(inner, 0)
    sig64, ioff = sshstr(inner, ioff)
    if ioff != len(inner) or sig_type != b"ssh-ed25519" or len(sig64) != 64:
        raise ValueError("inner signature")
    key_type, poff = sshstr(pub, 0)
    pub32, poff = sshstr(pub, poff)
    if poff != len(pub) or key_type != b"ssh-ed25519" or len(pub32) != 32:
        raise ValueError("public key blob")
    return pub, sig64


def signed_data(message):
    """The bytes an SSHSIG signature actually signs (PROTOCOL.sshsig)."""
    return (b"SSHSIG" + _pack(NAMESPACE) + _pack(b"") + _pack(b"sha512")
            + _pack(hashlib.sha512(message).digest()))


def verify(message, pubkey_blob, sig64):
    return ed25519_verify(pubkey_blob[-32:], sig64, signed_data(message))


def decode_point(b):
    """Canonical decoding (RFC 8032 §5.1.3): affine (x, y) or None."""
    n = int.from_bytes(b, "little")
    sign, y = n >> 255, n & ((1 << 255) - 1)
    if y >= P:
        return None
    u, v = (y * y - 1) % P, (D * y * y + 1) % P
    x = pow(u * pow(v, 3, P) * pow(u * pow(v, 7, P), (P - 5) // 8, P), 1, P)
    if (v * x * x - u) % P == 0:
        pass
    elif (v * x * x + u) % P == 0:
        x = x * SQRT_M1 % P
    else:
        return None
    if x == 0 and sign:
        return None
    return (P - x if (x & 1) != sign else x, y)


def _add(p, q):
    """Extended coordinates (X, Y, Z, T), unified addition for a = -1 (also doubles)."""
    x1, y1, z1, t1 = p
    x2, y2, z2, t2 = q
    a, b = (y1 - x1) * (y2 - x2) % P, (y1 + x1) * (y2 + x2) % P
    c, d = 2 * t1 * t2 * D % P, 2 * z1 * z2 % P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def _mul(k, p):
    r = (0, 1, 1, 0)
    while k:
        if k & 1:
            r = _add(r, p)
        p, k = _add(p, p), k >> 1
    return r


def _ext(affine):
    x, y = affine
    return (x, y, 1, x * y % P)


def _encode(p):
    x, y, z, _ = p
    zi = pow(z, P - 2, P)
    x, y = x * zi % P, y * zi % P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def weak_key(pub32):
    """A public key no entry may be attributed to: non-canonical encoding, or a point of small order."""
    a = decode_point(pub32)
    return a is None or _encode(_mul(8, _ext(a))) == IDENTITY


def ed25519_verify(pub32, sig64, msg):
    """Strict cofactorless Ed25519: [S]B == R + [k]A, S < L, canonical A and R."""
    if len(pub32) != 32 or len(sig64) != 64:
        return False
    a, r = decode_point(pub32), decode_point(sig64[:32])
    s = int.from_bytes(sig64[32:], "little")
    if a is None or r is None or s >= L:
        return False
    k = int.from_bytes(hashlib.sha512(sig64[:32] + pub32 + msg).digest(), "little") % L
    return _encode(_mul(s, _ext(BASE))) == _encode(_add(_ext(r), _mul(k, _ext(a))))
