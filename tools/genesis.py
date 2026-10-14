#!/usr/bin/env python3
"""Guy's genesis procedure (README.md): prepare the unsigned canonical message, print the exact
ssh-keygen command, then assemble the signed line. Generates no key. Not kernel."""
import argparse
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from harness.keys import dearmour  # noqa: E402
from kernel import log  # noqa: E402
from tools.digest import digest  # noqa: E402

STOP = ("STOP: the public key is not a plain ssh-ed25519 key. A hardware key (sk-ssh-ed25519@openssh.com) "
        "signs a different message; C0 verifies ssh-ed25519 only. Report this; the format is added later by a change entry.")


def prepare(a):
    with open(a.pubkey) as f:
        fields = f.read().split()
    if len(fields) < 2 or fields[0] != "ssh-ed25519":
        print(STOP, file=sys.stderr)
        return 3
    pubkey = " ".join(fields[:2])
    if log.pubkey_blob(pubkey) is None:
        print("the public key does not decode as ssh-ed25519", file=sys.stderr)
        return 2
    if not log.instant(a.ts):
        print("--ts must look like 2026-10-14T09:00:00Z (UTC)", file=sys.stderr)
        return 2
    with open(os.path.join(ROOT, "genesis.template.json")) as f:
        template = {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    with open(os.path.join(ROOT, "CHARTER.md"), "rb") as f:
        charter = hashlib.sha256(f.read()).hexdigest()
    text = json.dumps(template).replace("<<TS>>", a.ts).replace("<<CHARTER_SHA256>>", charter)
    text = text.replace("<<KERNEL_DIGEST>>", digest()).replace("<<GUY_SSH_PUBLIC_KEY>>", pubkey)
    entry = json.loads(text)
    log.check_shape(dict(entry, sig="AAAA"))
    log.check_body("genesis", entry["body"])
    message = log.canonical(entry)
    with open(a.out, "w") as f:
        f.write(message)
    key_path = re.sub(r"\.pub$", "", a.pubkey)
    print(f"Unsigned genesis written to {a.out} ({len(message)} bytes, canonical).\n"
          f"Sign it with exactly:\n\n    ssh-keygen -Y sign -f {key_path} -n core-entry {a.out}\n\n"
          f"then assemble:\n\n    python3 tools/genesis.py assemble {a.out} {a.out}.sig > log.jsonl\n")
    return 0


def assemble(a):
    with open(a.unsigned) as f:
        entry = json.loads(f.read())
    with open(a.sig) as f:
        entry["sig"] = dearmour(f.read())
    line = log.canonical(entry)
    sys.stdout.write(line + "\n")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--pubkey", required=True, help="Guy's ssh-ed25519 public key file")
    p.add_argument("--ts", required=True, help="UTC timestamp of signing, e.g. 2026-10-14T09:00:00Z")
    p.add_argument("--out", default="genesis.unsigned")
    p.set_defaults(fn=prepare)
    s = sub.add_parser("assemble")
    s.add_argument("unsigned")
    s.add_argument("sig")
    s.set_defaults(fn=assemble)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
