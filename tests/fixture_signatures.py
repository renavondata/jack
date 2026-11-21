"""Fast signing/verification of generated fixture keys, with stdlib/OpenSSL only.

Production kernels and their signature tests always use kernel.sig. These helpers
only build the thousands of valid padding entries needed to reach seq 5564.
"""
import base64
import ctypes as c
import ctypes.util
import functools

from harness import keys
from kernel import sig


@functools.cache
def crypto():
    lib = c.CDLL(ctypes.util.find_library("crypto"))
    specs = {
        "EVP_PKEY_new_raw_private_key_ex": ([c.c_void_p, c.c_char_p, c.c_char_p, c.c_char_p, c.c_size_t], c.c_void_p),
        "EVP_PKEY_new_raw_public_key_ex": ([c.c_void_p, c.c_char_p, c.c_char_p, c.c_char_p, c.c_size_t], c.c_void_p),
        "EVP_MD_CTX_new": ([], c.c_void_p),
        "EVP_DigestSignInit": ([c.c_void_p, c.c_void_p, c.c_void_p, c.c_void_p, c.c_void_p], c.c_int),
        "EVP_DigestVerifyInit": ([c.c_void_p, c.c_void_p, c.c_void_p, c.c_void_p, c.c_void_p], c.c_int),
        "EVP_DigestSign": ([c.c_void_p, c.c_void_p, c.POINTER(c.c_size_t), c.c_char_p, c.c_size_t], c.c_int),
        "EVP_DigestVerify": ([c.c_void_p, c.c_char_p, c.c_size_t, c.c_char_p, c.c_size_t], c.c_int),
        "EVP_MD_CTX_free": ([c.c_void_p], None), "EVP_PKEY_free": ([c.c_void_p], None),
    }
    for name, (args, result) in specs.items():
        fn = getattr(lib, name)
        fn.argtypes, fn.restype = args, result
    return lib


@functools.cache
def signing_key(key):
    with open(key.path) as f:
        data = base64.b64decode("".join(f.read().splitlines()[1:-1]))
    def string(offset):
        size = int.from_bytes(data[offset:offset + 4], "big")
        return data[offset + 4:offset + 4 + size], offset + 4 + size
    assert data.startswith(b"openssh-key-v1\0")
    cipher, offset = string(15)
    kdf, offset = string(offset)
    _, offset = string(offset)
    assert cipher == kdf == b"none" and int.from_bytes(data[offset:offset + 4], "big") == 1
    _, offset = string(offset + 4)
    data, _ = string(offset)
    typ, offset = string(8)
    _, offset = string(offset)
    private, _ = string(offset)
    assert typ == b"ssh-ed25519" and len(private) == 64
    return private[:32], keys.sign(key, b"fixture envelope")


def sign(key, message):
    seed, envelope = signing_key(key)
    lib = crypto()
    pkey = lib.EVP_PKEY_new_raw_private_key_ex(None, b"ED25519", None, seed, len(seed))
    ctx = lib.EVP_MD_CTX_new()
    try:
        assert pkey and ctx and lib.EVP_DigestSignInit(ctx, None, None, None, pkey) == 1
        signature, size = c.create_string_buffer(64), c.c_size_t(64)
        data = sig.signed_data(message)
        assert lib.EVP_DigestSign(ctx, signature, c.byref(size), data, len(data)) == 1 and size.value == 64
        return keys.rewrap(envelope, sig64=signature.raw)
    finally:
        lib.EVP_MD_CTX_free(ctx)
        lib.EVP_PKEY_free(pkey)


def verify(message, blob, signature):
    lib = crypto()
    pkey = lib.EVP_PKEY_new_raw_public_key_ex(None, b"ED25519", None, blob[-32:], 32)
    ctx = lib.EVP_MD_CTX_new()
    try:
        assert pkey and ctx and lib.EVP_DigestVerifyInit(ctx, None, None, None, pkey) == 1
        data = sig.signed_data(message)
        return lib.EVP_DigestVerify(ctx, signature, len(signature), data, len(data)) == 1
    finally:
        lib.EVP_MD_CTX_free(ctx)
        lib.EVP_PKEY_free(pkey)
