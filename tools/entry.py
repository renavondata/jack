#!/usr/bin/env python3
"""Prepare an entry on a log's current head, then assemble its SSH signature into a line the kernel admits.
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
from harness.keys import dearmour  # noqa: E402
from kernel import check, log  # noqa: E402

LOG = os.path.join(ROOT, "log.jsonl")


class Usage(Exception):
    """Exit 2: nothing written."""


def read_log(path):
    with open(path, "rb") as f:
        return check.read_lines(f.read())


def unsigned(a):
    """The canonical message (§2) on the head of a.log, or Usage."""
    lines = read_log(a.log)
    if not lines:
        raise Usage(f"{a.log} is empty: genesis is tools/genesis.py's job")
    if not log.instant(a.ts):
        raise Usage("--ts must be an instant like 2026-10-14T09:00:00Z (SPEC §4)")
    try:
        body = json.loads(a.body_json)
    except ValueError as x:
        raise Usage(f"--body-json is not JSON: {x}") from None
    if not isinstance(body, dict):
        raise Usage("--body-json must be a JSON object")
    entry = dict(seq=len(lines), parent=log.line_hash(lines[-1]), ts=a.ts, type=a.type, proposer=a.proposer, body=body)
    try:
        message = log.canonical(entry)
        log.check_shape(dict(log.parse_line(message), sig="AAAA"))
        log.check_body(a.type, body)
    except log.Refuse as x:
        raise Usage(f"the entry is refused before signing: {x.reason} {x.detail}") from None
    return message


def prepare(a):
    message = unsigned(a)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(message)
    sign = shlex.join(["ssh-keygen", "-Y", "sign", "-f", re.sub(r"\.pub$", "", a.pubkey), "-n", "core-entry", a.out])
    log_args = [] if a.log == LOG else ["--log", a.log]
    assemble = shlex.join(["python3", "tools/entry.py", "assemble", a.out, a.out + ".sig", *log_args])
    print(f"Unsigned entry written to {a.out} ({len(message)} bytes, canonical).\n"
          f"Sign it with exactly:\n\n    {sign}\n\n"
          f"then assemble:\n\n    {assemble} >> {shlex.quote(a.log)}\n")
    return 0


def assemble(a):
    """Print the signed line only if the kernel admits the log with it appended."""
    with open(a.unsigned, encoding="utf-8") as f:
        entry = json.loads(f.read())
    with open(a.sig) as f:
        entry["sig"] = dearmour(f.read())
    line = log.canonical(entry)
    verdict = check.check(read_log(a.log) + [line])
    if not verdict["ok"]:
        print(json.dumps(verdict, sort_keys=True), file=sys.stderr)
        return 1
    sys.stdout.write(line + "\n")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--type", required=True)
    p.add_argument("--proposer", required=True)
    p.add_argument("--ts", required=True)
    p.add_argument("--body-json", required=True, help="JSON object for the entry body")
    p.add_argument("--pubkey", required=True, help="the signer's public key file")
    p.add_argument("--out", required=True)
    p.add_argument("--log", default=LOG)
    p.set_defaults(fn=prepare)
    s = sub.add_parser("assemble")
    s.add_argument("unsigned")
    s.add_argument("sig")
    s.add_argument("--log", default=LOG)
    s.set_defaults(fn=assemble)
    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except (Usage, OSError, ValueError, log.Refuse) as x:
        print(str(x), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
