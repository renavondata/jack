#!/usr/bin/env python3
"""W5: append-only counsel writs, read without signing or changing the record."""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check, log  # noqa: E402
from tools import status as st  # noqa: E402

PATH = "transcripts/COUNSEL-DUE.jsonl"
REDATES = {"c2b-report": "2026-12-02T12:00:00Z", "c2c-brief": "2026-11-16T00:00:00Z"}


def file_at(root, rev, path=PATH):
    if rev is not None:
        if not st.git_bytes(root, "ls-tree", rev, "--", path):
            return None
        return st.tree_bytes(root, rev, path)
    try:
        return st.tree_bytes(root, None, path)
    except FileNotFoundError:
        return None


def inventory_check(root, rev, data, inventory=None):
    """Check every earlier first-parent version, including a deletion later restored."""
    newer = data or b""
    for sha in st.git_bytes(root, "log", "--first-parent", "--format=%H", rev or "HEAD", "--", PATH).decode().splitlines():
        older = file_at(root, sha) or b""
        if not newer.startswith(older):
            raise ValueError("COUNSEL-DUE rows changed (append-only)")
        newer = older
    if inventory is not None:
        seed = file_at(root, inventory)
        if seed is None:
            raise ValueError("no COUNSEL-DUE inventory")
        present = {r["id"] for r in fold(data or b"")}
        for r in fold(seed):
            if r["id"] not in present:
                raise ValueError("missing " + r["id"])


def first_merge(root, prefix, path, line=None, cache=None):
    """Only merges on this signed prefix count; never inspect a later log entry."""
    cache = {} if cache is None else cache
    for e in sorted(prefix, key=lambda e: e["seq"]):
        if e["type"] != "merge":
            continue
        key = (e["body"]["commit"], path)
        if key not in cache:
            cache[key] = file_at(root, key[0], path)
        data = cache[key]
        if data is not None and (line is None or line in data.splitlines(keepends=True)):
            return e
    return None


def fold(data):
    """Keep each discharge's original bytes for Amendment 7's merge witness."""
    rows, redated = {}, set()
    def done_ok(d):
        return (isinstance(d, dict) and set(d) == {"seq", "what"} and
                type(d["seq"]) is int and d["seq"] >= 0 and isinstance(d["what"], str))
    try:
        for raw in data.splitlines(keepends=True):
            row = json.loads(raw)
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError()
            rid, keys = row["id"], set(row)
            if keys == {"id", "due", "what", "done"}:
                if rid in rows or row["done"] is not None or not isinstance(row["what"], str):
                    raise ValueError()
                if not isinstance(row["due"], str) or st.instant(row["due"]).strftime(st.FMT) != row["due"]:
                    raise ValueError()
                rows[rid] = dict(row, discharges=[])
            elif keys == {"id", "done"}:
                if rid not in rows or not done_ok(row["done"]):
                    raise ValueError()
                rows[rid]["discharges"].append((row["done"], raw))
            elif keys == {"id", "due", "seq", "why"}:
                if (rid not in rows or rid in redated or rows[rid]["discharges"] or
                        REDATES.get(rid) != row["due"] or type(row["seq"]) is not int or
                        row["seq"] != 1564 or not isinstance(row["why"], str)):
                    raise ValueError()
                rows[rid]["due"] = row["due"]
                redated.add(rid)
            else:
                raise ValueError()
    except (ValueError, TypeError, KeyError, UnicodeError):
        raise ValueError("malformed COUNSEL-DUE file") from None
    return list(rows.values())


def assess(root, rev, es, as_of, inventory=None):
    data = file_at(root, rev)
    inventory_check(root, rev, data, inventory)
    if data is None:
        return None
    prefix = sorted((e for e in es if st.instant(e["ts"]) <= st.instant(as_of)), key=lambda e: e["seq"])
    entries, cache, result = {e["seq"]: e for e in prefix}, {}, []
    for row in fold(data):
        effective = []
        for done, raw in row["discharges"]:
            cited = entries.get(done["seq"])
            if cited is None or row["id"] not in log.canonical(cited["body"]):
                continue
            merge = first_merge(root, prefix, PATH, raw, cache)
            if merge is not None:
                effective.append((max(cited["ts"], merge["ts"]), done["seq"]))
        when, seq = min(effective, default=(None, None))
        late = (st.instant(when or as_of) - st.instant(row["due"])).total_seconds() / 3600
        result.append({k: row[k] for k in ("id", "due", "what")} |
                      dict(done=seq, effective_at=when, escalated=late > 0, hours=max(0, late)))
    return result


def render(rows):
    if rows is None:
        return "W5: no COUNSEL-DUE file"
    result = []
    for r in rows:
        state = f"done seq {r['done']} " if r["done"] is not None else ""
        if r["escalated"]:
            state += f"ESCALATED {r['hours']:.2f}h " + ("late" if r["done"] is not None else "past due")
        else:
            state += "on time" if r["done"] is not None else "OPEN"
        result.append(f"W5 {r['id']} due {r['due']} {r['what']}: {state}")
    return "\n".join(result)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--rev", help="read committed file and log instead of working tree")
    ap.add_argument("--inventory", help="opening seed commit; every seeded id must remain")
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).strftime(st.FMT))
    a = ap.parse_args(argv)
    try:
        data = st.tree_bytes(a.root, a.rev, "log.jsonl")
        checked = check.read_lines(data)
        if not check.check(checked)["ok"]:
            raise ValueError("the log is refused by the kernel")
        print(render(assess(a.root, a.rev, [json.loads(line) for line in checked], a.as_of, a.inventory)))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"W5: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
