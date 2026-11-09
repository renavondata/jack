#!/usr/bin/env python3
"""Record counsel-sign workflow runs, their push triggers, and receipt lines since the window's opening
(transcripts/sessions/evidence.md step 4; C2c-1.json evidence.courier; RESEARCH-meta-jack-20261107.md B6)."""
import json, os, re, subprocess, sys, tempfile, zipfile  # noqa: E401
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acts import api, current_stamp, now_iso, opening_instant, pages, root_dir, t  # noqa: E402
from runner import RUNNER, gh_raw_bytes  # noqa: E402

TS_PREFIX = re.compile(r"^\ufeff?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s+")
RECEIPT_RE = re.compile(r"^([A-Za-z0-9._-]+):\s+.*\brequest sha256 [0-9a-fA-F]{64}\b")
MAX_LOG_MEMBERS = 1000
MAX_COMMIT_FILE_PAGES = 100
MAX_RECEIPT_BYTES = 64 * 1024 * 1024


def run_log_lines(run_id, conclusion):
    with tempfile.TemporaryFile() as log:
        r = subprocess.run(["gh", "api", f"repos/{RUNNER}/actions/runs/{run_id}/logs"],
                           stdout=log, stderr=subprocess.PIPE)
        if r.returncode != 0:
            raise SystemExit(f"refused: gh api repos/{RUNNER}/actions/runs/{run_id}/logs: {r.stderr.decode('utf-8', errors='replace').strip()}")
        log.seek(0)
        if zipfile.is_zipfile(log):
            with zipfile.ZipFile(log) as z:
                members = z.infolist()
                if len(members) > MAX_LOG_MEMBERS:
                    raise SystemExit(f"refused: run {run_id} log has more than {MAX_LOG_MEMBERS} members")
                for member_info in sorted(members, key=lambda member: member.filename):
                    with z.open(member_info) as member:
                        for line in member:
                            yield line.decode("utf-8", errors="replace").rstrip("\r\n")
            return
        for line in log:
            yield line.decode("utf-8", errors="replace").rstrip("\r\n")


def extract_receipts(lines):
    out, size = [], 0
    for raw in lines:
        cleaned = TS_PREFIX.sub("", raw.strip())
        m = RECEIPT_RE.match(cleaned)
        if m:
            size += len(cleaned.encode("utf-8"))
            if size > MAX_RECEIPT_BYTES:
                raise SystemExit(f"refused: courier receipts exceed {MAX_RECEIPT_BYTES} bytes")
            out.append(cleaned)
    return out


def commit_files(sha):
    files = []
    for page in range(1, MAX_COMMIT_FILE_PAGES + 1):
        suffix = "?per_page=100&page=" + str(page)
        response = api(f"repos/{RUNNER}/commits/{sha}{suffix}")
        page_files = response.get("files")
        if not isinstance(page_files, list):
            raise SystemExit(f"refused: commit {sha} files are not a JSON list")
        files.extend(page_files)
        if len(page_files) < 100:
            return files
    raise SystemExit(f"refused: commit {sha} files exceeded {MAX_COMMIT_FILE_PAGES} pages")


def collect_courier(window_name, root=None, through=None):
    root = root or root_dir()
    open_iso = opening_instant(window_name, root=root)
    through = through or now_iso()
    open_dt, through_dt = t(open_iso), t(through)
    raw_runs = [r for r in pages(f"repos/{RUNNER}/actions/workflows/counsel-sign.yml/runs",
                                 key="workflow_runs", stop=lambda r: t(r["created_at"]) < open_dt)
                if open_dt <= t(r["created_at"]) <= through_dt]
    raw_runs.sort(key=lambda r: (r["created_at"], r["id"]))
    runs = []
    for r in raw_runs:
        sha = r.get("head_sha") or ""
        files = commit_files(sha) if sha else []
        added = sorted(f["filename"] for f in files if f.get("status") == "added" and
                       f.get("filename", "").startswith("requests/sign-") and f.get("filename", "").endswith(".json"))
        triggers = []
        for path in added:
            raw_text = gh_raw_bytes(f"repos/{RUNNER}/contents/{path}?ref={sha}").decode("utf-8", errors="replace")
            try:
                obj = json.loads(raw_text)
                if not isinstance(obj, dict): obj = {}
            except ValueError:
                obj = {}
            rid = obj.get("id")
            triggers.append({"path": path, "id": rid, "branch": obj.get("branch"), "contents": raw_text})
        log_lines = run_log_lines(r["id"], r.get("conclusion"))
        receipts = extract_receipts(log_lines)
        runs.append({
            "run": r["id"],
            "created_at": r.get("created_at"),
            "run_started_at": r.get("run_started_at") or r.get("created_at"),
            "updated_at": r.get("updated_at"),
            "conclusion": r.get("conclusion"),
            "triggers": triggers,
            "receipts": receipts,
        })
    return {"through": through, "runs": runs}


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not (1 <= len(args) <= 2):
        raise SystemExit("usage: courier.py <window> [stamp]")
    root = root_dir()
    stamp = current_stamp(root, args[1] if len(args) == 2 else None)
    data = collect_courier(args[0], root=root)
    out_path = os.path.join(root, "transcripts", "evidence", f"courier-{stamp}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"transcripts/evidence/courier-{stamp}.json (through {data['through']}, {len(data['runs'])} runs, stamp {stamp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
