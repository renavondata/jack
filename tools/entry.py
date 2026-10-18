#!/usr/bin/env python3
"""Prepare an entry on log.jsonl's current head, then assemble its SSH signature.
Generates no key. Not kernel.
"""
import argparse
import json
import os
import re
import shlex
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check, log  # noqa: E402
from tools.genesis import assemble, STOP  # noqa: E402


def prepare(a):
    with open(a.pubkey) as f:
        fields = f.read().split()
    if len(fields) < 2 or fields[0] != "ssh-ed25519":
        print(STOP, file=sys.stderr)
        return 3
    if log.pubkey_blob(" ".join(fields[:2])) is None:
        raise ValueError("the public key does not decode as ssh-ed25519")
    with open(a.log, "rb") as f:
        lines = check.read_lines(f.read())
    state = check.EMPTY
    for i, line in enumerate(lines):
        state = check.check_entry(state, i, line)
    body = log.parse_line(log.canonical(json.loads(a.body_json)))
    entry = dict(seq=len(lines), parent=state.head, ts=a.ts, type=a.type, proposer=a.proposer, body=body)
    log.check_shape(dict(entry, sig="AAAA"))
    log.check_body(a.type, body)
    message = log.canonical(entry)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(message)
    command = shlex.join(["ssh-keygen", "-Y", "sign", "-f", re.sub(r"\.pub$", "", a.pubkey),
                          "-n", "core-entry", a.out])
    assemble_command = shlex.join(["python3", "tools/entry.py", "assemble", a.out, a.out + ".sig"])
    print(f"Unsigned entry written to {a.out} ({len(message)} bytes, canonical).\n"
          f"Sign it with exactly:\n\n    {command}\n\nthen assemble:\n\n    {assemble_command}\n")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--pubkey", required=True)
    p.add_argument("--proposer", required=True)
    p.add_argument("--type", required=True, choices=log.TYPES)
    p.add_argument("--body-json", required=True, help="JSON object for the entry body")
    p.add_argument("--ts", required=True)
    p.add_argument("--log", default="log.jsonl")
    p.add_argument("--out", default="entry.unsigned")
    p.set_defaults(fn=prepare)
    s = sub.add_parser("assemble")
    s.add_argument("unsigned")
    s.add_argument("sig")
    s.set_defaults(fn=assemble)
    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except (OSError, ValueError, log.Refuse) as x:
        print(str(x), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
