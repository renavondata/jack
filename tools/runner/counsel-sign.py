#!/usr/bin/env python3
"""Sign counsel's requested entries with counsel's key on steel (counsel-sign.yml). Written to
transcripts/runner/counsel-courier.md in renavondata/jack; that text governs, this file is its code."""
import hashlib, json, os, re, subprocess, sys, tempfile  # noqa: E401
FIELDS = {"forecast": {"claim": str, "p": int, "by": str}, "proposal": {"title": str}}
OPTIONAL = {"forecast": {"type": str, "args": dict}, "proposal": {}}
REGULAR = {"100644", "100755"}  # SPEC §10 item 9: the repository holds regular files only

class CommandFailed(Exception): """a git or gh command failed: the request's refusal, filed by the outer handler"""  # noqa: E701
class Refused(SystemExit): """a refusal whose issue is already filed"""  # noqa: E701

def sh(*args, cwd=None, env=None, ok=True):
    r = subprocess.run(list(args), cwd=cwd, env=env, capture_output=True, text=True)
    if ok and r.returncode:
        raise CommandFailed(f"{' '.join(args[:4])} failed (exit {r.returncode})\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return r

def added_files(repo, before, after, token):
    """Use Git's unbounded diff rather than GitHub's 300-file REST response."""
    with tempfile.TemporaryDirectory(prefix="counsel-trigger-") as tmp:
        sh("git", "init", "-q", tmp)
        sh("git", "remote", "add", "origin", repo, cwd=tmp)
        auth = f"http.extraHeader=Authorization: Bearer {token}"
        sh("git", "-c", auth, "fetch", "-q", "--no-tags", "origin", after, cwd=tmp)
        if set(before) == {"0"}:
            output = sh("git", "diff-tree", "--root", "--no-commit-id", "--name-status", "-z", after, cwd=tmp).stdout
        else:
            sh("git", "-c", auth, "fetch", "-q", "--no-tags", "origin", before, cwd=tmp)
            output = sh("git", "diff", "--name-status", "-z", before, after, cwd=tmp).stdout
    fields = output.split("\0")
    return [fields[i + 1] for i in range(0, len(fields) - 1, 2) if fields[i] == "A"]

def powered_key_declarations(entries, pub):
    declarations = [d for e in entries for d in (e["body"]["keys"] if e["type"] == "genesis" else [e["body"]] if e["type"] == "key" else [])]
    return [d for d in declarations if d["pubkey"] == pub and d["powers"]]

def changed_by(wt, sha):  # judge.judge.changed_by's command: both sides of a rename, a merge against each parent
    return set(sh("git", "diff-tree", "-r", "-m", "--root", "--no-commit-id", "--name-only", "--no-renames", sha, cwd=wt).stdout.split()) - {""}

def outside_scope(wt, scope):  # paths the branch changes that counsel's scope does not list, and changed paths that are not regular files
    changed = [c for c in sh("git", "diff", "--name-only", "--no-renames", "-z", "origin/main...HEAD", cwd=wt).stdout.split("\0") if c]
    out = [c for c in changed if not any(c == s or (s.endswith("/") and c.startswith(s)) for s in scope)]
    modes = dict(l.split("\t", 1)[::-1] for l in sh("git", "ls-tree", "-r", "-z", "HEAD", cwd=wt).stdout.split("\0") if l)
    irregular = [c for c in changed if c in modes and modes[c].split()[0] not in REGULAR]
    return out, irregular

def entries(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def kernel_ok(wt):  # the kernel's verdict on the branch's log, by the branch's kernel (counsel's scope excludes kernel/, so it is main's)
    r = sh(sys.executable, "-m", "kernel.check", "log.jsonl", cwd=wt, ok=False)
    try: ok = r.returncode == 0 and json.loads(r.stdout).get("ok") is True
    except ValueError: ok = False
    return ok, r.stdout.strip()[-300:] + r.stderr.strip()[-300:]

def canon(x): return json.dumps(x, sort_keys=True, separators=(",", ":"))  # noqa: E704

def shape(line):  # a forecast line as its entry's body would read: no member for an absent type or args (tools/entry.py)
    return canon(dict({"claim": line["claim"], "p": line["p"], "resolves_by": line["by"]},
                      **({k: line[k] for k in ("type", "args") if k in line})))

def stands(line, candidates, principal):
    if not candidates: return None
    b = candidates[0]["body"]
    if canon({k: b[k] for k in ("claim", "p", "resolves_by", "type", "args") if k in b}) == shape(line):
        return candidates.pop(0)["seq"]
    raise RuntimeError(f"entry seq {candidates[0]['seq']} on the branch is not the request's next forecast line")

def clean(x):  # no control character or unencodable text anywhere in a line's strings: a verb cannot be given one
    if isinstance(x, str):
        try: x.encode("utf-8")
        except UnicodeEncodeError: return False
        return not any(ord(c) < 32 or 0x7F <= ord(c) <= 0x9F for c in x) and x.strip() != "" and len(x) <= 4000 and not x.startswith("-")
    return all(clean(k) and clean(v) for k, v in x.items()) if isinstance(x, dict) else all(clean(v) for v in x) if isinstance(x, list) else True

def main():
    here, before_sha, after_sha = os.environ["GITHUB_REPOSITORY"], os.environ["BEFORE"], os.environ["AFTER"]
    home = os.path.expanduser("~")
    jack, wt_root = f"{home}/git/jack", f"{home}/git/worktrees/jack"
    key, run_id, read = f"{home}/.ssh/jack-counsel-3", os.environ.get("GITHUB_RUN_ID", "?"), os.environ["READ_TOKEN"]
    gh_read = lambda *a: sh("gh", "api", *a, env={**os.environ, "GH_TOKEN": read}).stdout  # noqa: E731
    repo = f"https://github.com/{here}.git"
    files = sorted(f for f in added_files(repo, before_sha, after_sha, read)
                   if f.startswith("requests/sign-") and f.endswith(".json"))
    print(f"{len(files)} sign request(s): {files}")
    if not files: return 0
    tok = os.environ.get("COUNSEL_GH_TOKEN") or (open(p).read().strip() if os.path.exists(p := f"{home}/.config/jack/gh-counsel") else "")
    tok or sys.exit("counsel's token is absent (COUNSEL_GH_TOKEN or ~/.config/jack/gh-counsel); nothing done")
    os.path.exists(key) or sys.exit(f"{key} is absent on this runner; nothing done")
    env = {**os.environ, "GH_TOKEN": tok, "JACK_KEY": key}
    print("identity:", json.loads(sh("gh", "api", "user", env=env).stdout)["login"])
    sh("git", "fetch", "-q", "origin", cwd=jack), sh("git", "worktree", "prune", cwd=jack)
    scope = json.loads(sh("git", "show", "origin/main:judge/scope.json", cwd=jack).stdout)["parties"]["counsel"]
    pub = " ".join(open(key + ".pub").read().split()[:2])
    main_entries = [json.loads(l) for l in sh("git", "show", "origin/main:log.jsonl", cwd=jack).stdout.splitlines() if l.strip()]
    mine = powered_key_declarations(main_entries, pub)
    len(mine) == 1 or sys.exit(f"{key}.pub is declared {len(mine)} times with powers on main; nothing done")
    principal, trailer = mine[0]["principal"], f"Proposer: {mine[0]['principal']} {mine[0]['key_id']}"

    def refuse(rid, why):
        safe = rid if re.fullmatch(r"[A-Za-z0-9._/-]+", str(rid)) else "invalid-id"
        body = f"counsel-sign run {run_id} refused {safe}: {why}\n\n<!-- counsel-sign-refusal: {safe} -->\n"
        sh("gh", "api", "-X", "POST", f"repos/{here}/issues", "-f", f"title=counsel-sign: {safe} refused", "-f", f"body={body}",
           env={**os.environ, "GH_TOKEN": tok}, ok=False)
        raise Refused(f"{safe}: refused: {why}")

    def handle(f):
        try: q = json.loads(gh_read("-H", "Accept: application/vnd.github.raw", f"repos/{here}/contents/{f}?ref={after_sha}"))
        except ValueError as x: refuse(f, f"the trigger is not JSON: {x}")
        isinstance(q, dict) or refuse(f, "the trigger is not a JSON object")
        rid, branch = q.get("id"), q.get("branch")
        (isinstance(rid, str) and re.fullmatch(r"[A-Za-z0-9._-]+", rid)) or refuse(f, "id must match [A-Za-z0-9._-]+")
        (set(q) == {"id", "act", "branch"} and isinstance(branch, str) and rid == os.path.basename(f).removesuffix(".json")) or refuse(rid, "bad trigger")
        name = branch[len("counsel/"):]
        if q.get("act") != "sign" or not branch.startswith("counsel/") or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name) or ".." in name:
            refuse(rid, f"not a sign request on a counsel/<name> branch: {branch!r}")
        sh("git", "rev-parse", "--verify", "-q", f"origin/{branch}", cwd=jack, ok=False).returncode and refuse(rid, f"origin/{branch} does not exist")
        wt, local = f"{wt_root}/{branch}", not sh("git", "rev-parse", "--verify", "-q", f"refs/heads/{branch}", cwd=jack, ok=False).returncode
        (os.path.lexists(wt) and not os.path.isdir(wt)) and refuse(rid, f"{wt} exists and is not a directory")
        if os.path.isdir(wt):
            sh("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=wt, ok=False).stdout.strip() == branch or refuse(rid, f"{wt} holds wrong branch")
            sh("git", "status", "--porcelain", cwd=wt).stdout.strip() and refuse(rid, f"{wt} is not clean; nothing reset")
        else:
            sh("git", "worktree", "add", "-q", *([wt, branch] if local else ["-b", branch, wt, f"origin/{branch}"]), cwd=jack)
        sh("git", "branch", "-q", f"--set-upstream-to=origin/{branch}", branch, cwd=wt)
        if sh("git", "merge-base", "--is-ancestor", "HEAD", f"origin/{branch}", cwd=wt, ok=False).returncode:
            sh("git", "merge-base", "--is-ancestor", f"origin/{branch}", "HEAD", cwd=wt, ok=False).returncode and refuse(rid, f"{branch} diverged")
            sh("git", "push", "-q", "origin", branch, cwd=wt, env=env, ok=False).returncode and refuse(rid, f"pushing {branch} was rejected")
            sh("git", "fetch", "-q", "origin", cwd=wt)
        sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt)
        req = f"{wt}/transcripts/requests/{name}.jsonl"
        (os.path.isfile(req) and not os.path.islink(req)) or refuse(rid, f"{branch} has no regular file transcripts/requests/{name}.jsonl")
        before = open(req, "rb").read()
        try:
            raw = before.decode("utf-8").removesuffix("\n").split("\n") if before else []
            if not raw or any(not l.strip() for l in raw): raise ValueError("empty or blank line")
            lines = [json.loads(l) for l in raw]
        except ValueError as x: refuse(rid, f"request does not parse: {x}")
        (lines and all(isinstance(l, dict) for l in lines)) or refuse(rid, "every request line must be a JSON object")
        bad = [i + 1 for i, l in enumerate(lines) if not isinstance(l.get("verb"), str) or l.get("verb") not in FIELDS or
               set(l) - {"verb", *FIELDS[l["verb"]], *OPTIONAL[l["verb"]]} or
               any(not isinstance(l.get(k), t) or isinstance(l.get(k), bool) for k, t in FIELDS[l["verb"]].items()) or
               any(k in l and (not isinstance(l[k], t) or isinstance(l[k], bool)) for k, t in OPTIONAL[l["verb"]].items()) or not clean(l)]
        verbs = [l.get("verb") for l in lines]
        (not bad and verbs[-1] == "proposal" and verbs.count("proposal") == 1) or refuse(rid, f"invalid request lines {bad}, verbs {verbs}")
        out, irregular = outside_scope(wt, scope)
        (out or irregular) and refuse(rid, f"{branch} changes paths outside counsel's scope {out} or non-regular files {irregular}")
        ok, verdict = kernel_ok(wt)
        ok or refuse(rid, f"{branch}'s log.jsonl does not pass the kernel: {verdict}")
        commits = sh("git", "rev-list", "--topo-order", "HEAD", "--not", "origin/main", cwd=wt).stdout.split()
        if not commits:
            holds = lambda c: (bool(c) and not sh("git", "merge-base", "--is-ancestor", c, f"origin/{branch}", cwd=wt, ok=False).returncode and  # noqa: E731
                               (r := sh("git", "show", f"{c}:transcripts/requests/{name}.jsonl", cwd=wt, ok=False)).returncode == 0 and r.stdout.encode() == before)
            named = next((e["body"]["commit"] for e in reversed(main_entries) if e["type"] == "proposal" and e["proposer"] == principal
                          and holds(e["body"].get("commit", ""))), None)
            named or refuse(rid, f"{branch} has no commit origin/main lacks and no matching proposal on main")
            print(f"{rid}: {branch}: {len(lines)} line(s) in run {run_id}; request sha256 {hashlib.sha256(before).hexdigest()}; "
                  f"proposal commit {named}; head {sh('git', 'rev-parse', 'HEAD', cwd=wt).stdout.strip()}; pull request (merged); "
                  f"already proposed, merged, nothing signed", flush=True)
            return
        content = next((c for c in commits if changed_by(wt, c) - {"log.jsonl"}), sh("git", "rev-parse", "HEAD", cwd=wt).stdout.strip())
        base = sh("git", "merge-base", "origin/main", "HEAD", cwd=wt).stdout.strip()
        branch_entries = entries(f"{wt}/log.jsonl")[len(sh("git", "show", f"{base}:log.jsonl", cwd=wt).stdout.splitlines()):]
        own_forecasts = [e for e in branch_entries if e["type"] == "forecast" and e["proposer"] == principal]
        any(e["type"] not in ("forecast", "proposal") or e["proposer"] != principal for e in branch_entries) and refuse(rid, "foreign entries on branch")
        if any(e["type"] == "proposal" and e["body"].get("commit") == content for e in branch_entries):
            expected = [("forecast", shape(l)) for l in lines[:-1]] + [("proposal", canon({"title": lines[-1]["title"], "commit": content}))]
            actual = [(e["type"], canon({k: e["body"][k] for k in ("claim", "p", "resolves_by", "type", "args") if k in e["body"]}) if e["type"] == "forecast"
                       else canon({"title": e["body"].get("title"), "commit": e["body"].get("commit")})) for e in branch_entries]
            actual == expected or refuse(rid, f"{branch} holds entries that do not match the request in order")
            n = sh("gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number", "--jq", ".[0].number", cwd=wt, env=env).stdout.strip()
            n or print(sh("gh", "pr", "create", "--base", "main", "--head", branch, "--title", lines[-1]["title"][:200], "--body", trailer, cwd=wt, env=env).stdout)
            print(f"{rid}: {branch}: {len(lines)} line(s) in run {run_id}; request sha256 {hashlib.sha256(before).hexdigest()}; "
                  f"proposal commit {content}; head {sh('git', 'rev-parse', 'HEAD', cwd=wt).stdout.strip()}; pull request {n or 'opened now'}; "
                  f"already proposed, nothing signed", flush=True)
            return
        any(e["type"] == "proposal" for e in branch_entries) and refuse(rid, f"{branch} already holds a proposal entry naming another commit")
        merged = bool(sh("git", "merge-base", "--is-ancestor", "origin/main", "HEAD", cwd=wt, ok=False).returncode)
        if merged:
            r = sh("git", "-c", "user.name=counsel", "-c", "user.email=counsel@steel", "merge", "origin/main",
                   "-m", f"Merge main into {branch}", "-m", trailer, cwd=wt, ok=False)
            if r.returncode:
                sh("git", "merge", "--abort", cwd=wt, ok=False)
                refuse(rid, f"merging origin/main into {branch} conflicts; nothing signed:\n{(r.stdout + r.stderr)[-800:]}")
            try:
                if not os.path.isfile(req) or os.path.islink(req) or open(req, "rb").read() != before:
                    raise SystemExit("the merge changed or removed the request file")
                if any(outside_scope(wt, scope)) or not kernel_ok(wt)[0]:
                    raise SystemExit(f"after the merge, {branch} fails scope or kernel check")
            except BaseException as x:
                sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                refuse(rid, f"{x}; the merge is undone, nothing signed")
        signed_any = False
        for i, l in enumerate(lines):
            if l["verb"] == "forecast":
                try: seq = stands(l, own_forecasts, principal)
                except RuntimeError as x:
                    merged and not signed_any and sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                    refuse(rid, f"{x}; nothing signed")
                if seq is not None:
                    print(f"{rid}: line {i + 1} forecast already stands as seq {seq}; not entered again")
                    continue
                cmd = ["tools/jack", "forecast", l["claim"], "--p", str(l["p"]), "--by", l["by"],
                       *(["--type", str(l["type"])] if "type" in l else []),
                       *(["--args", json.dumps(l["args"], separators=(",", ":"))] if "args" in l else [])]
            else:
                if own_forecasts:
                    merged and not signed_any and sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                    refuse(rid, f"{branch} holds {len(own_forecasts)} unrequested forecast(s); the proposal is not signed")
                cmd = ["tools/jack", "proposal", "--title", l["title"]]
            try: pre, before_entries = sh("git", "rev-parse", "HEAD", cwd=wt).stdout.strip(), entries(f"{wt}/log.jsonl")
            except BaseException as x:
                merged and not signed_any and sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                refuse(rid, f"line {i + 1} ({l['verb']}): branch unreadable before verb: {x}")
            try: r = subprocess.run(cmd, cwd=wt, env=env, capture_output=True, text=True)
            except OSError as x:
                head_now = sh("git", "rev-parse", "HEAD", cwd=wt, ok=False).stdout.strip()
                if merged and not signed_any and head_now == pre:
                    sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                refuse(rid, f"line {i + 1} ({l['verb']}) failed in the host: {x}")
            if r.returncode:
                head_now = sh("git", "rev-parse", "HEAD", cwd=wt, ok=False).stdout.strip()
                if merged and not signed_any and head_now == pre:
                    sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                refuse(rid, f"line {i + 1} ({l['verb']}) refused:\n{(r.stdout + r.stderr)[-1200:]}")
            now, n_before = entries(f"{wt}/log.jsonl"), len(before_entries)
            if [canon(e) for e in now[:n_before]] != [canon(e) for e in before_entries]:
                head_now = sh("git", "rev-parse", "HEAD", cwd=wt, ok=False).stdout.strip()
                if merged and not signed_any and head_now == pre:
                    sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                refuse(rid, f"line {i + 1}: prior entries changed")
            new = now[n_before:]
            got = (canon({k: new[-1]["body"][k] for k in ("claim", "p", "resolves_by", "type", "args") if k in new[-1]["body"]})
                   if new and new[-1]["type"] == "forecast" else None)
            if not (len(new) == 1 and new[0]["proposer"] == principal and new[0]["type"] == l["verb"]
                    and (got == shape(l) if l["verb"] == "forecast" else new[0]["body"].get("title") == l["title"])):
                head_now = sh("git", "rev-parse", "HEAD", cwd=wt, ok=False).stdout.strip()
                if merged and not signed_any and head_now == pre:
                    sh("git", "reset", "-q", "--hard", f"origin/{branch}", cwd=wt, ok=False)
                refuse(rid, f"line {i + 1} ({l['verb']}): verb exited 0 without writing the requested entry")
            signed_any = True
        head = sh("git", "rev-parse", "HEAD", cwd=wt).stdout.strip()
        named = next((e["body"]["commit"] for e in reversed(entries(f"{wt}/log.jsonl")) if e["type"] == "proposal"), "?")
        n = sh("gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number", "--jq", ".[0].number", cwd=wt, env=env, ok=False).stdout.strip()
        print(f"{rid}: {branch}: {len(lines)} line(s) in run {run_id}; request sha256 {hashlib.sha256(before).hexdigest()}; "
              f"proposal commit {named}; head {head}; pull request {n or '(none open)'}", flush=True)

    failed = 0
    for f in files:
        try: handle(f)
        except BaseException as x:
            failed += 1
            print(f"{f}: {type(x).__name__}: {x}", flush=True)
            if not isinstance(x, Refused):
                safe = f if re.fullmatch(r"[A-Za-z0-9._/-]+", f) else "invalid-file"
                sh("gh", "api", "-X", "POST", f"repos/{here}/issues", "-f", f"title=counsel-sign: {safe} failed",
                   "-f", f"body=counsel-sign run {run_id} failed on {safe}: {type(x).__name__}: {str(x)[:1500]}\n\n<!-- counsel-sign-refusal: {safe} -->\n",
                   env={**os.environ, "GH_TOKEN": tok}, ok=False)
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
