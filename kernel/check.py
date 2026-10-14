"""The validity predicate: check(log) → ok | (seq, reason). CHARTER §3, §9.3.

Entry i is judged by the keys declared by entries 0..i-1 (genesis certifies
itself). C0 is the record only: recognition (c) holds vacuously because no
rule can be admitted, and the change rule governs `key` entries. Pure: no I/O
except in main().
"""
import json
import sys
from collections import namedtuple

from . import log, sig
from .log import Refuse

Key = namedtuple("Key", "principal blob powers")
State = namedtuple("State", "head keys owners")  # owners: pubkey blob -> the one key_id it may ever belong to
EMPTY = State(log.GENESIS_PARENT, {}, {})


def signer(e, keys):
    """Recognition (b): which declared key signed e, with power for its type."""
    try:
        blob, sig64 = sig.parse_sshsig(e["sig"])
    except ValueError as x:
        raise Refuse("bad_signature", f"sshsig: {x}") from None
    key_id = next((k for k, d in keys.items() if d.blob == blob), None)
    if key_id is None:
        raise Refuse("unknown_key")
    if keys[key_id].principal != e["proposer"]:
        raise Refuse("proposer_mismatch", f"key {key_id} belongs to {keys[key_id].principal}")
    if e["type"] not in keys[key_id].powers:
        raise Refuse("no_power", f"key {key_id} may not sign {e['type']}")
    message = log.canonical({k: v for k, v in e.items() if k != "sig"}).encode("utf-8")
    if not sig.verify(message, blob, sig64):
        raise Refuse("bad_signature")
    return key_id


def declare(keys, owners, d):
    """Change: a declaration enters the law; the latest for a key_id wins, empty powers revoke."""
    blob = log.pubkey_blob(d["pubkey"])
    if sig.weak_key(blob[-32:]):
        raise Refuse("bad_key", f"{d['key_id']}: non-canonical or small-order public key")
    if owners.get(blob, d["key_id"]) != d["key_id"]:
        raise Refuse("bad_key", f"pubkey belongs to {owners[blob]} for the life of the log")
    return {**keys, d["key_id"]: Key(d["principal"], blob, frozenset(d["powers"]))}, {**owners, blob: d["key_id"]}


def check_entry(state, i, line):
    """Recognition (a)(b) under the law before i, then the entry's effect: the next state."""
    e = log.parse_line(line)
    log.check_shape(e)
    if e["seq"] != i:
        raise Refuse("bad_seq", f"expected {i}")
    if e["parent"] != state.head:
        raise Refuse("parent_mismatch")
    if (e["type"] == "genesis") != (i == 0):
        raise Refuse("genesis_misplaced")
    if e["proposer"] == "":
        raise Refuse("no_proposer")
    log.check_body(e["type"], e["body"])
    keys, owners = state.keys, state.owners
    if e["type"] == "genesis":
        for d in e["body"]["keys"]:
            keys, owners = declare(keys, owners, d)
    signer(e, keys)
    if e["type"] == "key":
        keys, owners = declare(keys, owners, e["body"])
    return State(log.line_hash(line), keys, owners)


def check(lines):
    """check(log) → {"ok": true, "entries": N} | {"ok": false, "seq", "reason", "detail"}."""
    state = EMPTY
    for i, line in enumerate(lines):
        try:
            state = check_entry(state, i, line)
        except Refuse as x:
            return {"ok": False, "seq": i, "reason": x.reason, "detail": x.detail}
    return {"ok": True, "entries": len(lines)}


def read_lines(data):
    """Split log bytes into lines; undecodable bytes become lone surrogates and fail parsing."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return [l.decode("utf-8", "surrogateescape") for l in lines]


def main(argv):
    if len(argv) != 2:
        print("usage: python3 -m kernel.check <log.jsonl>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], "rb") as f:
            data = f.read()
    except OSError as x:
        print(f"cannot read {argv[1]}: {x}", file=sys.stderr)
        return 2
    verdict = check(read_lines(data))
    print(json.dumps(verdict, sort_keys=True))
    return 0 if verdict["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
