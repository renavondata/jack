#!/usr/bin/env python3
"""Antecedent: may this head reuse an earlier `tests` run as its evidence? (BRIEF-C2b, the opening push's
third change; REVIEW-C2a-v1 F8's contract.)

The answer is yes only when a completed, successful `tests` run exists for a commit whose tree is identical
to this head's in every file but `log.jsonl` — the complete input of the unit tests, the pins, the self-check
build and the simulator sample, none of which reads the log — and that run was made by this same workflow
file (the workflow is part of the tree, so equality covers it). The log itself is replayed through both
checkers on every head by the `judge` workflow, which never skips. A run that was itself a reuse counts,
because tree equality is transitive and every link names its antecedent in its own log.

Prints `skip=true` and the antecedent (`sha`, `run`) for the job's outputs, or `skip=false` with the reason.
Exits 0 either way; any failure to decide is `skip=false`. No secret: the token is GitHub's read-only one.
"""
import hashlib, json, os, subprocess, sys, urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "renavondata/jack")
WORKFLOW = ".github/workflows/tests.yml"
LOG = "log.jsonl"


def tree_without_log(sha):
    """SHA-256 over `git ls-tree -r` of the commit with the log's line removed: the test inputs' identity."""
    out = subprocess.check_output(["git", "ls-tree", "-r", sha], text=True)
    lines = [l for l in out.splitlines() if not l.endswith("\t" + LOG)]
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={
        "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def decide(head):
    want = tree_without_log(head)
    runs = api(f"/repos/{REPO}/actions/workflows/tests.yml/runs?status=success&per_page=100")["workflow_runs"]
    for run in runs:  # newest first
        if run.get("path") != WORKFLOW or run.get("conclusion") != "success" or run["head_sha"] == head:
            continue
        try:
            subprocess.run(["git", "cat-file", "-e", run["head_sha"] + "^{commit}"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            subprocess.run(["git", "fetch", "-q", "--depth=1", "origin", run["head_sha"]], capture_output=True)
            if subprocess.run(["git", "cat-file", "-e", run["head_sha"] + "^{commit}"], capture_output=True).returncode:
                continue
        if tree_without_log(run["head_sha"]) == want:
            return True, run["head_sha"], run["id"], "tree identical but for log.jsonl"
    return False, "", "", "no successful tests run with an identical tree"


def main():
    head = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    try:
        skip, sha, run, why = decide(head)
    except Exception as e:  # any failure to decide runs the tests
        skip, sha, run, why = False, "", "", f"undecided: {e!r}"
    print(f"antecedent for {head}: skip={'true' if skip else 'false'} sha={sha} run={run} ({why})")
    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as f:
            f.write(f"skip={'true' if skip else 'false'}\nsha={sha}\nrun={run}\n")


if __name__ == "__main__":
    main()
