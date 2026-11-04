#!/usr/bin/env python3
"""W5: counsel's dated writs, projected from a committed tree and an explicit clock."""
import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

FILE = "transcripts/COUNSEL-DUE.jsonl"
ROOT = Path(__file__).resolve().parents[1]


def instant(text):
    value = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.utcoffset() != dt.timedelta(0):
        raise ValueError("timestamp must be UTC")
    return value


def rows(text):
    return [json.loads(line) for line in text.splitlines()]


def unchanged(previous, current):
    current = current.splitlines(keepends=True)
    for i, old in enumerate(previous.splitlines(keepends=True)):
        if i >= len(current) or old != current[i]:
            raise ValueError(f"rows changed: {json.loads(old)['id']}")


def fold(records):
    result = {}
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError("malformed COUNSEL-DUE file")
        key = row["id"]
        if set(row) == {"id", "due", "what", "done"} and key not in result and row["done"] is None and all(
                isinstance(row[k], str) for k in ("due", "what")):
            result[key] = dict(row)
        elif set(row) == {"id", "done"} and key in result and result[key]["done"] is None and row["done"] is not None:
            result[key] = dict(result[key], done=row["done"])
        else:
            raise ValueError("malformed COUNSEL-DUE file")
    return list(result.values())


def project(current, entries, as_of):
    """Return rendered rows and whether any completion is malformed; overdue is not an error."""
    now, lines, malformed = instant(as_of), [], False
    prefix = {e["seq"]: e for e in entries if instant(e["ts"]) <= now}
    for row in current:
        due, done = instant(row["due"]), row["done"]
        state = f"ESCALATED {(now - due).total_seconds() / 3600:g}h past due" if due < now else "OPEN"
        if done is not None:
            seq = done.get("seq") if isinstance(done, dict) else done
            valid = (isinstance(done, dict) and set(done) == {"seq", "what"} and
                     type(seq) is int and isinstance(done["what"], str) and seq in prefix and
                     row["id"] in json.dumps(prefix[seq].get("body", {}), sort_keys=True, separators=(",", ":"), ensure_ascii=True))
            if valid:
                late = (instant(prefix[seq]["ts"]) - due).total_seconds() / 3600
                state = f"done seq {seq} " + (f"ESCALATED {late:g}h late" if late > 0 else "on time")
            else:
                malformed = True
                state += f" (done names seq {seq}, not an entry)"
        lines.append(f"W5 {row['id']} due {row['due']} {row['what']}: {state}")
    return lines, malformed


def blob(root, rev, path, optional=False):
    result = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], capture_output=True)
    if result.returncode and not optional:
        raise ValueError(f"cannot read {rev}:{path}")
    return None if result.returncode else result.stdout


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).isoformat())
    ap.add_argument("--inventory", metavar="COMMIT")
    a = ap.parse_args(argv)
    try:
        rev = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", f"{a.rev}^{{commit}}"],
                             capture_output=True, text=True, check=True).stdout.strip()
        text = blob(a.root, rev, FILE, optional=True)
        unchanged(blob(a.root, rev + "~1", FILE, optional=True) or b"", text or b"")
        current = fold(rows(text or b""))
        if a.inventory:
            for row in fold(rows(blob(a.root, a.inventory, FILE))):
                if row["id"] not in {r["id"] for r in current}:
                    raise ValueError(f"missing {row['id']}")
        if text is None:
            print("W5: no COUNSEL-DUE file")
            return 0
        lines, malformed = project(current, rows(blob(a.root, rev, "log.jsonl")), a.as_of)
        if malformed:
            lines.append("W5: malformed COUNSEL-DUE file")
        print("\n".join(lines))
        return 2 if malformed else 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"W5: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
