#!/usr/bin/env python3
"""jack status: the current window's pre-stated criteria, the procedure:object ratio and the overdue forecasts, computed
from log.jsonl and the tree, so that no criterion is counted by hand (PLAN-20261030 §4; BRIEF-C1 criterion 4, A3.4, J7).
No entry, no signing, no fetch. The clock enters only as --as-of (default now); the kernel never reads it."""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kernel import check  # noqa: E402

FMT = "%Y-%m-%dT%H:%M:%SZ"


def instant(s):
    return dt.datetime.strptime(s, FMT).replace(tzinfo=dt.timezone.utc)


def evidence_ok(root, ev):
    """True iff `ev` is sha256:<hex64> naming transcripts/evidence/<hex64> whose SHA-256 is that value."""
    if not (isinstance(ev, str) and ev.startswith("sha256:") and len(ev) == 71):
        return False
    path = os.path.join(root, "transcripts", "evidence", ev[7:])
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest() == ev[7:]
    except OSError:
        return False


def status(es, window, days, as_of, root=ROOT, subject="C1a"):
    """The figures BRIEF-C1 evaluates on the exit prefix, on the prefix as of `as_of` (an instant string)."""
    opened = [e for e in es if e["type"] == "amend" and e["body"].get("id") == window]
    if not opened:
        raise SystemExit(f"no amend entry with id {window!r}")
    start = instant(opened[-1]["ts"])
    end = start + dt.timedelta(days=days)
    now = instant(as_of)
    prefix = [e for e in es if instant(e["ts"]) <= min(end, now)]
    inw = [e for e in prefix if instant(e["ts"]) >= start]
    world = {e["seq"] for e in es if e["type"] == "forecast" and str(e["body"].get("type", "")).startswith("world.")}
    resolved = {e["body"]["forecast"]: e for e in prefix if e["type"] == "resolution"}
    fc = [e for e in inw if e["type"] == "forecast"]
    rs = [e for e in inw if e["type"] == "resolution"]
    wrs = [e for e in rs if e["body"]["forecast"] in world]
    objects = sum(1 for e in inw if (e["type"] == "forecast" and e["seq"] in world) or (e["type"] == "resolution" and e["body"]["forecast"] in world))
    late = [e for e in fc if e["seq"] not in resolved and instant(e["body"]["resolves_by"]) < now]
    overdue = sorted((e["body"]["resolves_by"], e["seq"], e["proposer"], (e["body"].get("args") or {}).get("evidence", ""))
                     for e in es if e["type"] == "forecast" and e["seq"] not in resolved and instant(e["body"]["resolves_by"]) < now)
    return {
        "window": window, "start": start.strftime(FMT), "end": end.strftime(FMT), "as_of": as_of,
        "prefix_last_seq": prefix[-1]["seq"] if prefix else None, "entries_in_window": len(inw),
        "forecasts": len(fc), "proposers": sorted({e["proposer"] for e in fc}),
        "resolutions": len(rs), "world_resolutions": len(wrs),
        "world_resolutions_with_evidence": sum(1 for e in wrs if evidence_ok(root, e["body"]["evidence"])),
        "procedure": len(inw) - objects, "object": objects,
        "veto": any(e["type"] == "decision" and e["body"].get("kind") == "veto" and e["body"].get("subject") == subject for e in prefix),
        "j7_unresolved_past_due": len(late), "j7_denominator": len(fc),
        "overdue": overdue,
    }


def render(s):
    c4 = (s["forecasts"] >= 20, len(s["proposers"]) >= 3, s["resolutions"] >= 10, s["world_resolutions_with_evidence"] >= 5)
    ratio = (s["procedure"] / s["object"]) if s["object"] else float("inf")
    mark = lambda ok: "met" if ok else "SHORT"  # noqa: E731
    out = [f"window {s['window']}: {s['start']} .. {s['end']} (as of {s['as_of']}; prefix to seq {s['prefix_last_seq']}; {s['entries_in_window']} entries)",
           f"criterion 4: forecasts {s['forecasts']}/20 {mark(c4[0])}; proposers {len(s['proposers'])}/3 {mark(c4[1])} {s['proposers']}; "
           f"resolutions {s['resolutions']}/10 {mark(c4[2])}; world-typed with evidence in tree {s['world_resolutions_with_evidence']}/5 {mark(c4[3])} "
           f"(world-typed {s['world_resolutions']})",
           f"criterion 6: veto on the subject: {'YES' if s['veto'] else 'none'}",
           f"A3.4 ratio: procedure {s['procedure']} : object {s['object']} = {ratio:.2f} : 1 {'STOP' if ratio > 5 else 'within 5:1'}",
           f"J7: {s['j7_unresolved_past_due']} of {s['j7_denominator']} window forecasts unresolved past resolves_by",
           "criteria 1, 2, 3, 5 are the tests run on main (pins, checker agreement, kernel count, score vectors): see that run",
           f"overdue forecasts at {s['as_of']}: {len(s['overdue'])}"]
    out += [f"  seq {seq} ({who}) due {by} evidence: {ev or '-'}" for by, seq, who, ev in s["overdue"]]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", default=os.path.join(ROOT, "log.jsonl"))
    ap.add_argument("--window", default="A3", help="the amend entry whose ts opens the window")
    ap.add_argument("--days", type=int, default=14, help="the window's length as the brief states it (a maximum under A5)")
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).strftime(FMT))
    ap.add_argument("--subject", default="C1a")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.log, "rb") as f:
        lines = check.read_lines(f.read())
    if not check.check(lines)["ok"]:
        raise SystemExit("the log is refused by the kernel")
    es = [json.loads(line) for line in lines]
    s = status(es, a.window, a.days, a.as_of, root=os.path.dirname(os.path.abspath(a.log)), subject=a.subject)
    print(json.dumps(s, indent=1) if a.json else render(s))


if __name__ == "__main__":
    main()
