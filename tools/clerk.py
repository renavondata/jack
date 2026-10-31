#!/usr/bin/env python3
"""Level-triggered C1b forecast writs. The W3/W4 integration is not yet installed."""
import argparse
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check  # noqa: E402
from tools.status import FMT, c1b_window  # noqa: E402


def forecast_writs(entries, runs, now):
    """Pure W1 projection; `runs` is reserved for the other writs' supplied REST view."""
    es = [e for e in entries if e["ts"] <= now]
    opening, _, _ = c1b_window(es)
    keys = {d["key_id"]: d for d in es[0]["body"]["keys"]}
    for e in es:
        if e["type"] == "key":
            keys[e["body"]["key_id"]] = e["body"]
    resolved = {e["body"]["forecast"] for e in es if e["type"] == "resolution"}
    sovereign = ",".join(sorted({d["principal"] for d in es[0]["body"]["keys"]}))
    writs = []
    for e in es:
        if e["type"] == "forecast" and e["seq"] > opening and e["seq"] not in resolved:
            holders = tuple(sorted(k for k, d in keys.items() if "resolution" in d["powers"] and
                                   d["principal"] != e["proposer"]))
            deadline = e["body"]["resolves_by"]
            writs.append({"class": "W1", "seq": e["seq"], "holders": holders, "deadline": deadline,
                          "escalated": deadline < now, "sovereign": sovereign})
    return writs


def render(writs):
    return "\n".join(f"{w['class']} forecast {w['seq']}: holders {','.join(w['holders']) or '(none)'}; "
                     f"deadline {w['deadline']}" + (f" ESCALATED to {w['sovereign']}" if w["escalated"] else "")
                     for w in writs)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", default=os.path.join(ROOT, "log.jsonl"))
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).strftime(FMT))
    a = ap.parse_args(argv)
    with open(a.log, "rb") as f:
        lines = check.read_lines(f.read())
    if not check.check(lines)["ok"]:
        raise SystemExit("the log is refused by the kernel")
    print(render(forecast_writs([json.loads(line) for line in lines], [], a.as_of)))


if __name__ == "__main__":
    main()
