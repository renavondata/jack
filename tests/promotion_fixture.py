"""Synthetic installing pushes for item 15 tests; no live log or sovereign key."""
import hashlib
import json
import functools
import os
from unittest.mock import patch

from harness import build, gitfix
from judge import judge
from kernel import check, log, sig

PREFIXES = {}
VERIFIED = functools.cache(sig.verify)


def prepare(repo, world):
    """Memoise verified signatures in disposable kernels, so 5564 padding entries cost once.

    This changes only fixture trees. Every cached tuple is first verified by the real
    kernel; all shape, parent, key, power and state checks still run on every call.
    """
    cache = os.path.join(os.path.dirname(world.guy.path), "verified-signatures.json")
    if not os.path.exists(cache):
        with open(cache, "w") as f:
            json.dump([], f)
    path = os.path.join(repo, "kernel/sig.py")
    with open(path) as f:
        source = f.read()
    if "_fixture_verified" not in source:
        with open(path, "a") as f:
            f.write("\nimport json as _json\n_fixture_verify = verify\n" +
                    f"_fixture_verified = set(_json.load(open({cache!r})))\n" +
                    "def verify(message, pubkey_blob, sig64):\n" +
                    "    return hashlib.sha256(message + pubkey_blob + sig64).hexdigest() in _fixture_verified or _fixture_verify(message, pubkey_blob, sig64)\n")
    return cache


def pad(lg, world, ts=build.TS):
    """A verified prefix long enough for the real installing-push boundary."""
    key = (tuple(lg.lines), ts)
    if key not in PREFIXES:
        while len(lg.lines) < 5564:
            lg.add("proposal", "guy", build.proposal("before installation"), world.guy, ts=ts)
        with patch.object(sig, "verify", VERIFIED):
            verdict = check.check(lg.lines)
        assert verdict["ok"], verdict
        PREFIXES[key] = tuple(lg.lines)
    lg.lines = list(PREFIXES[key])
    cache = os.path.join(os.path.dirname(world.guy.path), "verified-signatures.json")
    if os.path.exists(cache):
        with open(cache) as f:
            verified = set(json.load(f))
        for line in lg.lines:
            e = json.loads(line)
            blob, signature = sig.parse_sshsig(e["sig"])
            message = log.canonical({k: v for k, v in e.items() if k != "sig"}).encode()
            verified.add(hashlib.sha256(message + blob + signature).hexdigest())
        with open(cache, "w") as f:
            json.dump(sorted(verified), f)


def install(repo, lg, world, ts=build.TS):
    """Install the committed SPEC with a prior signed grant and a push after seq 5564."""
    pad(lg, world, ts)
    spec = judge.show(repo, "HEAD", "SPEC.md")
    lg.add("decision", "guy", {"kind": "grant", "subject": "promote_unmet: SPEC.md " + hashlib.sha256(spec).hexdigest()},
           world.guy, ts=ts)
    lg.add("push", "guy", {"digest": judge.digest(repo, "HEAD"), "review": "0" * 64}, world.guy, ts=ts)
    gitfix.write(repo, "log.jsonl", lg.text())
    return gitfix.commit_all(repo, "Install promotion judging")


def entries(repo, ref="HEAD"):
    return [json.loads(l) for l in judge.split_lines(judge.show(repo, ref, "log.jsonl"))]
