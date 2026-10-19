#!/usr/bin/env python3
"""The judge: trunk's checker over a proposal's appended log entries, as data.

CHARTER §9.6. Facts about the proposal (paths touched, signing keys) come from
git objects, never from the proposal's claims; the proposal's code is never
executed; the trusted base (kernel/, kernel2/, judge/, .github/workflows/,
SPEC.md) and CHARTER.md must be byte-identical between trunk and the proposal
(maxim 1): compared by content, so a rename or deletion is caught as surely as
an edit. Trunk's promulgated charter must record the SHA-256 of CHARTER.md.
Standard library only; the only side effects are git reads and a temporary
directory.
"""
import argparse
import base64
import hashlib
import itertools
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
PARTIES = ("guy", "founder", "builder", "counsel", "reviewer")  # the trailer's parties, for tools/jack; the judge reads keys, not trailers


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


def commits_of(repo, trunk, head):
    """The proposal's commits, those reachable from head and not from trunk, newest first (children before parents)."""
    return git(repo, "rev-list", "--topo-order", head, "--not", trunk).splitlines()


def changed_by(repo, sha):
    """Paths one commit changes, both sides of a rename, a merge against each of its parents."""
    return set(git(repo, "diff-tree", "-r", "-m", "--root", "--no-commit-id", "--name-only", "--no-renames", sha).splitlines()) - {""}


def signer_blob(e):
    """Base64 of the pubkey blob embedded in the entry's SSHSIG container."""
    blob = base64.b64decode(e["sig"])
    n = int.from_bytes(blob[10:14], "big")
    return base64.b64encode(blob[14:14 + n]).decode()


def principal_at(entries, i, blob):
    """Principal of the key whose pubkey blob is `blob` under the law in force at entry i (SPEC §7):
    genesis's declarations, then every key entry before i, a later declaration of a key_id replacing the earlier."""
    decls = entries[0]["body"]["keys"] + [e["body"] for e in entries[1:i] if e["type"] == "key"]
    keys = dict((d["key_id"], d) for d in decls)
    return next((d["principal"] for d in keys.values() if d["pubkey"].split(" ")[1] == blob), None)


def is_python(path, data):
    """A .py file, or one whose first line is a #! line naming python (SPEC §10.10; tools/count_kernel.py alike)."""
    first = data.split(b"\n", 1)[0]
    return path.endswith(".py") or (first.startswith(b"#!") and b"python" in first)


def counted_lines(repo, sha, prefixes):
    """Physical lines of every python file under `prefixes` at `sha`, as tools/count_kernel.py counts them."""
    texts = ((p, show(repo, sha, p)) for p in files(repo, sha) if is_under(p, prefixes))
    return sum(len(split_lines(data)) for p, data in texts if is_python(p, data))


def differing(repo, trunk, head):
    """Trusted-base files and CHARTER.md whose bytes differ between two commits: edits, renames, deletions, additions."""
    paths = set(trusted_files(repo, trunk)) | set(trusted_files(repo, head)) | {CHARTER}
    return sorted(p for p in paths if show(repo, trunk, p) != show(repo, head, p))


def genesis_charter(line):
    """The charter claim in a genesis (or amendment) line, if present."""
    try:
        return json.loads(line)["body"]["charter"]
    except (ValueError, KeyError, TypeError):
        return None


def promulgated_charter(repo, trunk, data):
    """Latest valid charter claim, including amendments not yet in force."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, LOG)
        with open(path, "wb") as f:
            f.write(data)
        verdict = run_kernel(repo, trunk, path)
    lines = split_lines(data)
    valid = lines if verdict["ok"] else lines[:verdict["seq"]]
    return next((genesis_charter(l) for l in reversed(valid)
                 if json.loads(l)["type"] in ("genesis", "amend")), None)


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
    if old and promulgated_charter(repo, trunk, trunk_log) != hashlib.sha256(show(repo, trunk, CHARTER) or b"").hexdigest():
        return refuse("charter_mismatch", "trunk's promulgated charter does not record the SHA-256 of trunk's CHARTER.md")
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
    entries = [json.loads(line) for line in new]
    if head != trunk:
        failure = proposal_checks(repo, trunk, head, report, entries, len(old))
        if failure:
            return refuse(*failure)
    trusted = next((e["body"]["digest"] for e in reversed([json.loads(l) for l in old]) if e["type"] == "push"),
                   entries[0]["body"]["checker"] if entries else None)
    if old and trusted != report["trusted_digest"]:
        return refuse("trusted_base_unrecorded", "trunk's digest is not the trusted base in force")
    amendments = [e for e in entries if e["type"] == "amend"]
    if any(a["seq"] < e["seq"] < a["body"]["activate_at"] for e in entries if e["type"] == "push" for a in amendments):
        return refuse("push_during_amendment", "push strictly between amendment and activation")
    transmuted = set()
    for e in entries:
        if e["type"] == "amend" and e["body"]["id"] not in transmuted:
            return refuse("amend_untransmuted", f"amendment at seq {e['seq']} has not been transmuted")
        if e["type"] == "decision" and e["body"]["kind"] == "transmute":
            transmuted.add(e["body"]["subject"])
    founders = {d["pubkey"].split(" ")[1] for d in entries[0]["body"]["keys"]} if entries else set()
    for e in entries:
        blob = base64.b64decode(e["sig"])
        n = int.from_bytes(blob[10:14], "big")
        if e["type"] == "decision" and base64.b64encode(blob[14:14 + n]).decode() not in founders:
            return refuse("decision_by_other", f"decision at seq {e['seq']} is not signed by a genesis key")
    return dict(report, ok=True)


def proposal_checks(repo, trunk, head, report, entries, first):
    """Items 7-10 apply only when head differs from trunk. `first` is the seq of the first appended entry."""
    scope, commits = json.loads(show(repo, trunk, SCOPE) or b""), commits_of(repo, trunk, head)
    named = [(i, e) for i, e in enumerate(entries) if i >= first and e["type"] == "proposal" and e["body"]["commit"] in commits]
    if not named:
        return "unattributed_proposal", "no appended proposal entry names a commit of the proposal"
    seq, last = named[-1]
    # commits_of lists newest first, so the commits before the named one are those after it
    later = set().union(*(changed_by(repo, c) for c in itertools.takewhile(lambda c: c != last["body"]["commit"], commits)))
    if later - {LOG}:
        return "unattributed_proposal", f"commits after {last['body']['commit']} (seq {seq}) change {', '.join(sorted(later - {LOG}))}"
    report["proposer"] = principal_at(entries, seq, signer_blob(last))
    changed = touched(repo, trunk, head, "--no-renames")  # a rename touches both its paths
    allowed = scope["parties"].get(report["proposer"])  # a party absent from `parties` is bounded by item 9 alone
    if allowed is not None and any(not is_under(p, allowed) for p in changed):
        return "party_scope", f"outside {report['proposer']}'s paths: {', '.join(p for p in changed if not is_under(p, allowed))}"
    if any(not is_under(p, scope["paths"]) for p in changed):
        return "out_of_scope", f"outside {scope['layer']}'s paths: {', '.join(p for p in changed if not is_under(p, scope['paths']))}"
    if counted_lines(repo, head, scope["counted"]) > scope["cap"]:
        return "code_cap", f"{counted_lines(repo, head, scope['counted'])} counted lines exceed the cap of {scope['cap']}"


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
