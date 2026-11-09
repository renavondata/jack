#!/usr/bin/env python3
"""Record sha256 per workflow file under .github/workflows/ of renavondata/opencode-runner at its main
(transcripts/sessions/evidence.md step 3; transcripts/runner/README.md; C2c-1.json evidence.runner)."""
import hashlib, json, os, subprocess, sys  # noqa: E401
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acts import api, current_stamp, now_iso, root_dir, stamp_to_iso, t  # noqa: E402

RUNNER = "renavondata/opencode-runner"


def gh_raw_bytes(path):
    r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", path], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"refused: gh api {path}: {r.stderr.decode('utf-8', errors='replace').strip()}")
    return r.stdout


def collect_runner_workflows():
    items = api(f"repos/{RUNNER}/contents/.github/workflows?ref=main")
    if not isinstance(items, list):
        raise SystemExit("refused: .github/workflows listing is not a JSON list")
    out = []
    for it in sorted(items, key=lambda x: x.get("name", "")):
        if it.get("type") != "file":
            continue
        raw = gh_raw_bytes(f"repos/{RUNNER}/contents/{it['path']}?ref=main")
        out.append({"workflow": it["name"], "sha256": hashlib.sha256(raw).hexdigest()})
    return out


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if len(args) > 1:
        raise SystemExit("usage: runner.py [stamp]")
    root = root_dir()
    stamp = current_stamp(root, args[0] if args else None)
    stamp_iso = stamp_to_iso(stamp)
    if t(stamp_iso) > t(now_iso()):
        raise SystemExit(f"refused: stamp {stamp_iso} is after collection instant {now_iso()}")
    workflows = collect_runner_workflows()
    out_path = os.path.join(root, "transcripts", "evidence", f"runner-{stamp}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(workflows, f, indent=2)
        f.write("\n")
    print(f"transcripts/evidence/runner-{stamp}.json ({len(workflows)} workflows, stamp {stamp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
