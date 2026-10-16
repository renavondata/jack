#!/usr/bin/env python3
"""The judge: trunk's checker over a proposal's appended log entries, as data.

CHARTER §9.6. Facts about the proposal (paths touched, signing keys) come from
git objects, never from the proposal's claims; the proposal's code is never
executed; the trusted base (kernel/, kernel2/, judge/, .github/workflows/,
SPEC.md) and CHARTER.md must be byte-identical between trunk and the proposal
(maxim 1): compared by content, so a rename or deletion is caught as surely as
an edit. Trunk's genesis must record the SHA-256 of trunk's CHARTER.md.
Standard library only; the only side effects are git reads and a temporary
directory.
"""
import argparse
import base64
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile

TRUSTED = ("kernel/", "kernel2/", "judge/", ".github/workflows/", "SPEC.md")
CHARTER = "CHARTER.md"
LOG = "log.jsonl"
SCOPE = "judge/scope.json"
PARTIES = ("guy", "founder", "builder", "counsel", "reviewer")


class JudgeError(Exception):
    pass


def git(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        raise JudgeError(f"git {' '.join(args)}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout if binary else r.stdout.decode().strip()


def rev(repo, ref):
    return git(repo, "rev-parse", "--verify", ref + "^{commit}")


def files(repo, sha):
    return git(repo, "ls-tree", "-r", "--name-only", sha).splitlines()


def show(repo, sha, path):
    """Bytes of `path` in commit `sha`, or None if absent."""
    r = subprocess.run(["git", "-C", repo, "show", f"{sha}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def is_under(path, roots):
    return any(path == r or (r.endswith("/") and path.startswith(r)) for r in roots)


def trusted_files(repo, sha):
    return sorted(p for p in files(repo, sha) if is_under(p, TRUSTED))


def digest(repo, sha):
    """sha256 over path\\0content\\0 for every trusted-base file, sorted by path."""
    h = hashlib.sha256()
    for path in trusted_files(repo, sha):
        h.update(path.encode() + b"\0" + show(repo, sha, path) + b"\0")
    return h.hexdigest()


def touched(repo, trunk, head, *flags):
    """Paths git reports as changed since the merge base (by default renames appear under the new name only)."""
    base = git(repo, "merge-base", trunk, head)
    return sorted(p for p in git(repo, "diff", "--name-only", *flags, base, head).splitlines() if p)


def party(repo, sha):
    """First word of the head commit's first `Proposer:` trailer, parsed by git from the message, or None."""
    values = git(repo, "log", "-1", "--format=%(trailers:key=Proposer,valueonly)", sha).split("\n")
    return (values[0].split() or [None])[0]


def counted_lines(repo, sha, prefixes):
    """Physical lines of every .py file under `prefixes` at `sha`, as tools/count_kernel.py counts them."""
    return sum(len(split_lines(show(repo, sha, p))) for p in files(repo, sha) if p.endswith(".py") and is_under(p, prefixes))


def differing(repo, trunk, head):
    """Trusted-base files and CHARTER.md whose bytes differ between two commits: edits, renames, deletions, additions."""
    paths = set(trusted_files(repo, trunk)) | set(trusted_files(repo, head)) | {CHARTER}
    return sorted(p for p in paths if show(repo, trunk, p) != show(repo, head, p))


def genesis_charter(line):
    """The charter hash entry 0 records, or None if the line does not carry one."""
    try:
        return json.loads(line)["body"]["charter"]
    except (ValueError, KeyError, TypeError):
        return None


def split_lines(data):
    lines = data.split(b"\n")
    return lines[:-1] if lines and lines[-1] == b"" else lines


def extract(repo, sha, prefix, into):
    """Write the files under `prefix` at `sha` into `into`, honouring git's executable bit (mode 100755)."""
    for line in git(repo, "ls-tree", "-r", sha).splitlines():
        meta, path = line.split("\t", 1)
        if path.startswith(prefix):
            dest = os.path.join(into, path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(show(repo, sha, path))
            if meta.split()[0] == "100755":
                os.chmod(dest, 0o755)


def run_json(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True)
    try:
        if r.returncode in (0, 1):
            return json.loads(r.stdout)
    except ValueError:
        pass
    raise JudgeError(f"{cmd[0]} failed ({r.returncode}): {r.stderr.decode(errors='replace')[-500:]}")


def run_kernel(repo, trunk, log_path):
    """Run trunk's kernel (extracted from git, never from a checkout) over a log file."""
    with tempfile.TemporaryDirectory() as tmp:
        extract(repo, trunk, "kernel/", tmp)
        return run_json([sys.executable, "-E", "-s", "-m", "kernel.check", log_path], tmp)


def run_kernel2(repo, trunk, log_path):
    if "kernel2/check" not in files(repo, trunk):
        return "absent"
    with tempfile.TemporaryDirectory() as tmp:
        extract(repo, trunk, "kernel2/", tmp)
        exe = os.path.join(tmp, "kernel2", "check")
        os.chmod(exe, os.stat(exe).st_mode | stat.S_IXUSR)
        return run_json([exe, log_path], tmp)


def fingerprint(line):
    """SHA256 fingerprint of the key embedded in the entry's SSHSIG blob."""
    blob = base64.b64decode(json.loads(line)["sig"])
    n = int.from_bytes(blob[10:14], "big")
    return "SHA256:" + base64.b64encode(hashlib.sha256(blob[14:14 + n]).digest()).decode().rstrip("=")


def strip(v):
    return {k: x for k, x in v.items() if k != "detail"} if isinstance(v, dict) else v


def judge(repo, trunk_ref, proposal_ref):
    trunk, head = rev(repo, trunk_ref), rev(repo, proposal_ref)
    report = {"trunk": trunk, "proposal": head, "touched": touched(repo, trunk, head),
              "trusted_digest": digest(repo, trunk), "appended": 0, "signers": [], "verdict": None,
              "kernel2": "absent", "proposer": None, "ok": False, "reason": None, "detail": ""}

    def refuse(reason, detail=""):
        return dict(report, reason=reason, detail=detail)

    if digest(repo, head) != report["trusted_digest"] or show(repo, head, CHARTER) != show(repo, trunk, CHARTER):
        return refuse("trusted_path", f"differs from trunk: {', '.join(differing(repo, trunk, head))}")
    trunk_log, head_log = show(repo, trunk, LOG) or b"", show(repo, head, LOG) or b""
    old, new = split_lines(trunk_log), split_lines(head_log)
    if old and genesis_charter(old[0]) != hashlib.sha256(show(repo, trunk, CHARTER) or b"").hexdigest():
        return refuse("charter_mismatch", "trunk's genesis does not record the SHA-256 of trunk's CHARTER.md")
    if not head_log.startswith(trunk_log):
        return refuse("prefix_broken", "trunk's log is not a byte prefix of the proposal's")
    appended = new[len(old):]
    report["appended"] = len(appended)
    if appended and not old:
        return refuse("genesis_by_proposal", "genesis is Guy's own commit to trunk, never a proposal")
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, LOG)
        with open(log_path, "wb") as f:
            f.write(head_log)
        report["verdict"] = run_kernel(repo, trunk, log_path)
        report["kernel2"] = run_kernel2(repo, trunk, log_path)
    if report["kernel2"] != "absent" and strip(report["kernel2"]) != strip(report["verdict"]):
        return refuse("checker_drift", "the two checkers disagree")
    if not report["verdict"]["ok"]:
        return refuse(report["verdict"]["reason"], report["verdict"].get("detail", ""))
    report["signers"] = [fingerprint(l.decode()) for l in appended]
    for line in appended:
        e = json.loads(line)
        if e["type"] == "merge" and e["body"]["checker"] != report["trusted_digest"]:
            return refuse("judge_from_proposal", f"merge at seq {e['seq']} claims a checker trunk does not have")
    if head == trunk:  # the self-check: items 7-10 concern proposals, and trunk against itself is none
        return dict(report, ok=True)
    scope, report["proposer"] = json.loads(show(repo, trunk, SCOPE) or b""), party(repo, head)
    if report["proposer"] not in PARTIES:
        return refuse("unattributed_proposal", f"head commit's Proposer trailer names no party of {', '.join(PARTIES)}")
    changed = touched(repo, trunk, head, "--no-renames")  # a rename touches both its paths
    if report["proposer"] == "counsel" and any(not is_under(p, scope["documents"]) for p in changed):
        return refuse("counsel_builds", f"counsel touches code: {', '.join(p for p in changed if not is_under(p, scope['documents']))}")
    if any(not is_under(p, scope["paths"]) for p in changed):
        return refuse("out_of_scope", f"outside {scope['layer']}'s paths: {', '.join(p for p in changed if not is_under(p, scope['paths']))}")
    if counted_lines(repo, head, scope["counted"]) > scope["cap"]:
        return refuse("code_cap", f"{counted_lines(repo, head, scope['counted'])} counted lines exceed the cap of {scope['cap']}")
    return dict(report, ok=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".")
    ap.add_argument("--trunk", required=True)
    ap.add_argument("--proposal", required=True)
    a = ap.parse_args(argv)
    try:
        report = judge(a.repo, a.trunk, a.proposal)
    except (JudgeError, OSError, ValueError, KeyError) as x:
        print(f"judge error: {x}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=1))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
