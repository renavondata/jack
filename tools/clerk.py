#!/usr/bin/env python3
"""Read-only, level-triggered C1b clerk: W1 forecasts, W3 unwitnessed merges, W4 unmet
window lines and historical sovereign REPAIRs. No signing, network or persisted state.
W1 holders are current resolution keys of other principals; resolution discharges it.
W3/W4 holder is counsel; deadline is the window end. A COUNSEL-OPEN table row containing
literal 'W3 merge <seq>' discharges W3. W4 clears when its line is met; a historical
REPAIR remains. Strictly past a deadline, ESCALATED names the sovereign. Supply saved
Actions/acts evidence explicitly; missing evidence is unverified, never green."""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from tools import status  # noqa: E402
from tools.status import c1b_window  # noqa: E402


def forecast_writs(entries, runs, now):
    """Pure W1 projection; runs do not discharge a forecast."""
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


def writ(es, kind, obligation, deadline, now, seq=None):
    return {"class": kind, "seq": seq, "obligation": obligation, "holders": ("counsel",),
            "deadline": deadline, "escalated": deadline < now,
            "sovereign": ",".join(sorted({d["principal"] for d in es[0]["body"]["keys"]}))}


def merge_writs(es, runs, now, deadline, counsel_open):
    rows = [line for line in counsel_open.splitlines() if line.lstrip().startswith("|")]
    return [writ(es, "W3", f"merge {e['seq']}: unwitnessed {e['body']['commit']}", deadline, now, e["seq"])
            for e in es if e["type"] == "merge" and e["ts"] <= now and
            not any(r.get("path") == status.WORKFLOW and r.get("head_sha") == e["body"]["commit"] and
                    r.get("conclusion") == "success" and status.completed_by(r, e["ts"]) for r in runs) and
            not any(re.search(rf"\bW3 merge {e['seq']}\b", row) for row in rows)]


def window_writs(es, s, now):
    lines = [text for ok, text in s["checks"] if not ok] + s.get("repairs", [])
    lines += [f"overdue forecast {seq} ({who}) due {by}" for by, seq, who, _ in s["overdue"]]
    return [writ(es, "W4", text, s["end"], now) for text in lines]


def render(writs):
    return "\n".join(f"{w['class']} {w.get('obligation', 'forecast ' + str(w['seq']))}: holders {','.join(w['holders']) or '(none)'}; "
                     f"deadline {w['deadline']}" + (f" ESCALATED to {w['sovereign']}" if w["escalated"] else "")
                     for w in writs)


def main(argv=None):
    ap = status.parser(__doc__)
    ap.add_argument("--counsel-open", metavar="FILE", help="W3 precedent table (default transcripts/COUNSEL-OPEN.md at HEAD)")
    a = ap.parse_args(argv)
    try:
        es, head, subject, run, runs, acts, mapping = status.inputs(a)
        s = status.report(es, head, subject, a.as_of, a.root, run, runs, acts, mapping)
        try:
            if a.counsel_open:
                with open(a.counsel_open) as f:
                    precedents = f.read()
            else:
                precedents = status.tree_bytes(a.root, head, "transcripts/COUNSEL-OPEN.md").decode()
        except (FileNotFoundError, subprocess.CalledProcessError):
            precedents = ""
        forecasts = forecast_writs(es, runs, a.as_of) if subject == "C1b" else []
        print(render(forecasts + merge_writs(es, runs, a.as_of, s["end"], precedents) + window_writs(es, s, a.as_of)))
    except (StopIteration, OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"clerk unverified: {exc or 'window opening or L0 missing'}")


if __name__ == "__main__":
    main()
