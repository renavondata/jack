#!/usr/bin/env python3
"""Enforcement map ledger check and deadline resolution (BRIEF-C2c-1 R7)."""
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import log  # noqa: E402

FIELDS = {"principle", "enforcer", "witness", "deadline"}
FMT = "%Y-%m-%dT%H:%M:%SZ"


def valid_deadline(dl, numbers=None):
    if not isinstance(dl, str) or not dl:
        return False
    if log.instant(dl) or dl == "end":
        return True
    if dl.startswith("opening+"):
        key = dl.split("+", 1)[1]
        return bool(key) and (numbers is None or (key in numbers and type(numbers[key]) is int))
    return False


def check_map(mapping, numbers=None):
    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("enforcement map must be a non-empty JSON object")
    for name, row in mapping.items():
        if not isinstance(row, dict) or set(row) != FIELDS or not all(isinstance(v, str) for v in row.values()):
            raise ValueError(f"row {name!r} must have string fields {sorted(FIELDS)}")
        if not row["principle"].strip():
            raise ValueError(f"row {name!r} has empty principle")
        enf = row["enforcer"]
        if not enf.startswith(("code:", "hand:")) or not enf.split(":", 1)[1].strip():
            raise ValueError(f"row {name!r} has invalid enforcer {enf!r}")
        if enf.startswith("hand:") and not valid_deadline(row["deadline"], numbers):
            raise ValueError(f"hand row {name!r} has missing or invalid deadline {row['deadline']!r}")
        if enf.startswith("code:") and row["deadline"] and not valid_deadline(row["deadline"], numbers):
            raise ValueError(f"code row {name!r} has invalid deadline {row['deadline']!r}")
    return mapping


def resolve_deadline(dl, start_ts, end_ts, numbers=None):
    if log.instant(dl):
        return dl
    if dl == "end" and end_ts:
        return end_ts
    if dl.startswith("opening+") and start_ts and numbers:
        key = dl.split("+", 1)[1]
        if key in numbers and type(numbers[key]) is int:
            t0 = dt.datetime.strptime(start_ts, FMT).replace(tzinfo=dt.timezone.utc)
            return (t0 + dt.timedelta(days=numbers[key])).strftime(FMT)
    raise ValueError(f"cannot resolve deadline {dl!r}")


def main(argv=None):
    path = argv[0] if argv else os.path.join(ROOT, "tools", "enforcement.json")
    try:
        with open(path) as f:
            check_map(json.load(f))
    except (OSError, ValueError) as exc:
        print(f"enforcement map refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
