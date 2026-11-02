#!/usr/bin/env python3
"""Antecedent: may this run reuse an earlier `tests` run as its evidence? (BRIEF-C2b, the opening push's
third change; REVIEW-C2a-v1 F8's contract.)

Every run of this workflow computes the identity of the tree it tests — SHA-256 over `git ls-tree -r HEAD`
with `log.jsonl`'s line removed: the complete input of the unit tests, the pins, the self-check build and the
simulator sample, none of which reads the log — and publishes it as an artifact named `tree-<identity>`, so
the record of what each run tested is the run's own statement, not a reconstruction. A later run on the same
identity may reuse a completed, successful run that published that name: each worker then prints the
antecedent's run id and head and exits green. The log itself is replayed through both checkers on every head
by the `judge` workflow, which never reuses anything. A run that was itself a reuse counts, because tree
identity is transitive and every link names its antecedent in its own log.

`identity` prints the identity; `decide <identity> <this run id>` prints `skip=…`, `sha=…`, `run=…` for the
job's outputs. Exits 0 either way; any failure to decide is `skip=false`. No secret: GitHub's read-only token.
"""
import hashlib, json, os, subprocess, sys, urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "renavondata/jack")
WORKFLOW = ".github/workflows/tests.yml"
LOG = "log.jsonl"


def identity(rev="HEAD"):
    out = subprocess.check_output(["git", "ls-tree", "-r", rev], text=True)
    return hashlib.sha256("\n".join(l for l in out.splitlines() if not l.endswith("\t" + LOG)).encode()).hexdigest()


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={
        "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def decide(ident, this_run):
    arts = api(f"/repos/{REPO}/actions/artifacts?name=tree-{ident}&per_page=100")["artifacts"]
    for a in arts:  # newest first
        run_id = a.get("workflow_run", {}).get("id")
        if not run_id or str(run_id) == str(this_run) or a.get("expired"):
            continue
        run = api(f"/repos/{REPO}/actions/runs/{run_id}")
        if run.get("path") == WORKFLOW and run.get("status") == "completed" and run.get("conclusion") == "success":
            return True, run["head_sha"], run_id, "a successful run published this tree identity"
    return False, "", "", "no successful run published this tree identity"


def main():
    if sys.argv[1:2] == ["identity"]:
        print(identity()); return
    ident, this_run = sys.argv[2], sys.argv[3]
    try:
        skip, sha, run, why = decide(ident, this_run)
    except Exception as e:  # any failure to decide runs the tests
        skip, sha, run, why = False, "", "", f"undecided: {e!r}"
    print(f"antecedent for tree {ident[:16]}: skip={'true' if skip else 'false'} sha={sha} run={run} ({why})")
    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as f:
            f.write(f"skip={'true' if skip else 'false'}\nsha={sha}\nrun={run}\n")


if __name__ == "__main__":
    main()
