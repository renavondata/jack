#!/usr/bin/env python3
"""Make counsel's requested acts under counsel's own account (counsel.yml), within the grant of seq 2131 and nothing
else: on renavondata/jack, opening counsel's proposals and closing its own stale proposals with a comment; on
renavondata/opencode-runner, filing and closing issues. Written to transcripts/runner/counsel-courier.md."""
import datetime, json, os, re, subprocess, sys  # noqa: E401
JACK, RUNNER, SEG = "renavondata/jack", "renavondata/opencode-runner", r"[A-Za-z0-9_-][A-Za-z0-9._-]*"

def gh(token, *args, payload=None):
    r = subprocess.run(["gh", "api", *args] + (["--input", "-"] if payload is not None else []),
                       input=json.dumps(payload) if payload is not None else None, capture_output=True, text=True,
                       env={**os.environ, "GH_TOKEN": token})
    r.returncode and sys.exit(f"refused: gh api {' '.join(args[:3])}: {r.stdout}{r.stderr}")
    return json.loads(r.stdout) if r.stdout.strip() else None

def gh_raw(token, path):
    r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", path],
                       capture_output=True, text=True, env={**os.environ, "GH_TOKEN": token})
    r.returncode and sys.exit(f"refused: gh api {path}: {r.stdout}{r.stderr}")
    return r.stdout

def jack_text(dir_, name, ext): return f"repos/{JACK}/contents/transcripts/{dir_}/{name}.{ext}?ref=main"  # noqa: E704

def issues(tok, repo):
    out, page = [], 1
    while len(batch := gh(tok, f"repos/{repo}/issues?state=all&per_page=100&page={page}")) == 100:
        out, page = out + batch, page + 1
    return out + batch

def valid_counsel_branch(ref):
    name = ref[len("counsel/"):] if isinstance(ref, str) and ref.startswith("counsel/") else ""
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name)) and ".." not in name

def main():
    here, before_sha, after_sha, read = os.environ["GITHUB_REPOSITORY"], os.environ["BEFORE"], os.environ["AFTER"], os.environ["READ_TOKEN"]
    ep = f"repos/{here}/commits/{after_sha}" if set(before_sha) == {"0"} else f"repos/{here}/compare/{before_sha}...{after_sha}"
    files = sorted(f["filename"] for f in gh(read, ep)["files"]
                   if f["status"] == "added" and f["filename"].startswith("requests/") and f["filename"].endswith(".json")
                   and not f["filename"].startswith("requests/sign-"))
    print(f"{len(files)} request(s) for this job: {files}")
    if not files: return 0
    tok = os.environ.get("COUNSEL_GH_TOKEN") or (open(p).read().strip() if os.path.exists(p := os.path.expanduser("~/.config/jack/gh-counsel")) else "")
    tok or sys.exit("counsel's token is absent (COUNSEL_GH_TOKEN or ~/.config/jack/gh-counsel); nothing done")
    me = gh(tok, "user")["login"]
    print("identity:", me)

    def handle(f):
        q = json.loads(gh_raw(read, f"repos/{here}/contents/{f}?ref={after_sha}"))
        isinstance(q, dict) or sys.exit(f"{f}: refused: the request is not a JSON object")
        act, rid = q.get("act"), q.get("id")
        (isinstance(rid, str) and re.fullmatch(r"[A-Za-z0-9._-]+", rid)) or sys.exit("refused: id must match [A-Za-z0-9._-]+")
        if act == "pr":
            if set(q) != {"id", "act", "head", "title", "body"} or not all(isinstance(q[k], str) for k in ("head", "title", "body")) or not q["title"].strip():
                sys.exit(f"{rid}: refused: pr requires string head, non-empty title, and body")
            valid_counsel_branch(q["head"]) or sys.exit(f"{rid}: refused: head {q['head']!r} is not a counsel/<name> branch")
            d = gh(tok, "-X", "POST", f"repos/{JACK}/pulls", payload={"title": q["title"], "head": q["head"], "base": "main", "body": q["body"]})
            print(f"{rid}: pr -> {d['html_url']}")
        elif act == "issue":
            if "template" in q:
                set(q) - {"id", "act", "template", "window", "model", "branch", "texts", "labels", "then_labels"} and sys.exit(f"{rid}: refused: unexpected fields")
                (isinstance(q["template"], str) and re.fullmatch(r"[a-z0-9-]+", q["template"])) or sys.exit(f"{rid}: refused: bad template")
                ("texts" in q and "window" not in q) and sys.exit(f"{rid}: refused: texts given without window")
                ("window" in q and "model" in q) or sys.exit(f"{rid}: refused: template issue requires window and model")
                vals = {k: q[k] for k in ("window", "model", "branch", "texts") if k in q}
                all(isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9._/,-]+", v) for v in vals.values()) or sys.exit(f"{rid}: refused: bad placeholder value")
                re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", vals["window"]) or sys.exit(f"{rid}: refused: bad window {vals['window']!r}")
                for k, parts in (("branch", [vals["branch"]] if "branch" in vals else []), ("texts", vals["texts"].split(",") if "texts" in vals else [])):
                    all(re.fullmatch(rf"(?:{SEG}/)*{SEG}", t) for t in parts) or sys.exit(f"{rid}: refused: invalid path in {k}")
                tpl = gh_raw(tok, jack_text("sessions", q["template"], "md"))
                if "texts" in vals:
                    frozen = json.loads(gh_raw(tok, jack_text("windows", vals["window"], "json"))).get("frozen", {}).get("paths", [])
                    loose = [t for t in vals["texts"].split(",") if not any(t.startswith(p) for p in frozen)]
                    loose and sys.exit(f"{rid}: refused: texts not under a frozen prefix of {vals['window']}: {loose}")
                now = datetime.datetime.now(datetime.timezone.utc)
                body = tpl.replace("{STAMP}", now.strftime("%Y%m%dT%H%M")).replace("{NOW}", now.strftime("%Y-%m-%dT%H:%M:%SZ"))
                for k, v in vals.items(): body = body.replace("{" + k.upper() + "}", v)
                re.findall(r"\{[A-Z]+\}", body) and sys.exit(f"{rid}: refused: placeholders unfilled")
                first_h1 = next((l[2:].strip() for l in body.splitlines() if l.startswith("# ")), "")
                first_h1 or sys.exit(f"{rid}: refused: template has no # title line")
                q = {**q, "title": first_h1[:250], "body": body, "labels": q.get("labels", ["run"])}
            else:
                if set(q) - {"id", "act", "title", "body", "labels", "then_labels"} or not isinstance(q.get("title"), str) or not q["title"].strip() or not isinstance(q.get("body"), str):
                    sys.exit(f"{rid}: refused: issue requires non-empty string title and string body")
                re.search(r"^\s*key\s*:", q["body"], re.M | re.I) and sys.exit(f"{rid}: refused: key: line in direct issue body")
            labels, then_labels = q.get("labels", []), q.get("then_labels", [])
            if not (isinstance(labels, list) and all(isinstance(x, str) for x in labels) and isinstance(then_labels, list) and all(isinstance(x, str) for x in then_labels)):
                sys.exit(f"{rid}: refused: invalid labels")
            mark = f"<!-- counsel-request: {rid} -->"
            seen = [i for i in issues(tok, RUNNER) if mark in (i.get("body") or "") and i["user"]["login"] == me and "pull_request" not in i]
            if seen:
                missing = [l for l in then_labels if l not in {x["name"] for x in seen[0].get("labels", [])}]
                missing and gh(tok, "-X", "POST", f"repos/{RUNNER}/issues/{seen[0]['number']}/labels", payload={"labels": missing})
                return print(f"{rid}: issue already filed ({seen[0]['html_url']}); labels added: {missing}")
            d = gh(tok, "-X", "POST", f"repos/{RUNNER}/issues", payload={"title": q["title"], "body": q["body"] + f"\n\n{mark}\n", "labels": labels})
            then_labels and gh(tok, "-X", "POST", f"repos/{RUNNER}/issues/{d['number']}/labels", payload={"labels": then_labels})
            print(f"{rid}: issue -> {d['html_url']}")
        elif act == "close":
            if set(q) != {"id", "act", "repo", "number", "stale"} or not isinstance(q.get("number"), int) or isinstance(q.get("number"), bool) or not isinstance(q.get("stale"), str):
                sys.exit(f"{rid}: refused: close requires repo, integer number, and string stale")
            repo, n, why = q["repo"], q["number"], q["stale"].strip()
            (repo in (JACK, RUNNER) and why) or sys.exit(f"{rid}: refused: invalid repo or empty stale reason")
            it = gh(tok, f"repos/{repo}/issues/{n}")
            it["user"]["login"] == me or sys.exit(f"{rid}: refused: {repo}#{n} was opened by {it['user']['login']}, not {me}")
            if it["state"] != "open": return print(f"{rid}: {repo}#{n} is already closed; skipped")
            if repo == JACK:
                "pull_request" in it or sys.exit(f"{rid}: refused: {repo}#{n} is not a pull request")
                pr = gh(tok, f"repos/{repo}/pulls/{n}")
                valid_counsel_branch(str(pr["head"]["ref"])) or sys.exit(f"{rid}: refused: not a counsel/<name> branch")
                gh(tok, "-X", "POST", f"repos/{repo}/issues/{n}/comments", payload={"body": f"stale: {why}"})
            else:
                "pull_request" not in it or sys.exit(f"{rid}: refused: {repo}#{n} is a pull request, not an issue")
            gh(tok, "-X", "PATCH", f"repos/{repo}/issues/{n}", payload={"state": "closed"})
            print(f"{rid}: closed {repo}#{n} (stale: {why[:80]})")
        else:
            sys.exit(f"{rid}: refused: unknown act {act!r}")

    failed = 0
    for f in files:
        try: handle(f)
        except BaseException as x:
            failed += 1
            safe, why = (f if re.fullmatch(r"[A-Za-z0-9._/-]+", f) else "invalid-file"), str(x)[:1500]
            print(f"{safe}: refused: {why}", flush=True)
            try:
                gh(tok, "-X", "POST", f"repos/{RUNNER}/issues",
                   payload={"title": f"counsel-act: {safe} refused", "body": f"counsel-act run {os.environ.get('GITHUB_RUN_ID', '?')} refused {safe}: {why}\n\n<!-- counsel-act-refusal: {safe} -->\n"})
            except BaseException: pass
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
