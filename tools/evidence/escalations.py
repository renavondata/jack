#!/usr/bin/env python3
"""Rebuild transcripts/evidence/escalations.json wholly from the diary's 'resolve the writs due' issues
on renavondata/opencode-runner since 12 hours before the window's opening (evidence.md step 2; C2c-1.json)."""
import datetime as dt, json, os, re, sys  # noqa: E401
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acts import FMT, api, load_entries, now_iso, opening_instant, pages, root_dir, t  # noqa: E402

RUNNER = "renavondata/opencode-runner"
DIARY_LOGIN = "renavondata-jack-court[bot]"
TITLE = "resolve the writs due"


def due_seqs(body):
    lines = re.findall(r"^due-seqs:\s*(.+)$", body or "", re.M)
    return [int(x) for line in lines for x in re.findall(r"\d+", line)]


def build_escalations(window_name, root=None, through=None):
    root = root or root_dir()
    es = load_entries(root)
    open_iso = opening_instant(window_name, es=es, root=root)
    through = through or now_iso()
    since_dt, through_dt = t(open_iso) - dt.timedelta(hours=12), t(through)
    since_iso = since_dt.strftime(FMT)
    deadlines = {e["seq"]: e["body"]["resolves_by"] for e in es if e["type"] == "forecast"}
    rows, ignored = [], []
    for it in pages(f"repos/{RUNNER}/issues?state=all&since={since_iso}&sort=created&direction=asc"):
        if "pull_request" in it or it.get("title") != TITLE:
            continue
        filed_at = it.get("created_at") or it.get("createdAt") or ""
        if not filed_at or not (since_dt <= t(filed_at) <= through_dt):
            continue
        user = (it.get("user") or {}).get("login") or ""
        if user != DIARY_LOGIN:
            ignored.append((it["number"], user, it.get("title") or ""))
            continue
        for seq in due_seqs(it.get("body") or ""):
            if seq not in deadlines:
                continue
            kind = "escalated" if t(deadlines[seq]) < t(filed_at) else "handed"
            rows.append({"forecast": seq, "issue": it["number"], "filed_at": filed_at, "kind": kind, "user": user})
    rows.sort(key=lambda r: (r["filed_at"], r["issue"], r["forecast"]))
    return {"through": through, "rows": rows}, ignored


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if len(args) != 1:
        raise SystemExit("usage: escalations.py <window>")
    root = root_dir()
    data, ignored = build_escalations(args[0], root=root)
    for num, user, title in ignored:
        print(f"ignored issue #{num} by {user}: {title}")
    out_path = os.path.join(root, "transcripts", "evidence", "escalations.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"transcripts/evidence/escalations.json (through {data['through']}, {len(data['rows'])} rows, {len(ignored)} ignored)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
