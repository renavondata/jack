model: openai/gpt-5.4-mini
key: ~/.ssh/jack-builder
branch: ops-resolve-{STAMP}

# builder: resolve the freshness forecasts now due (renavondata/jack)

You are the **builder** (`JACK_KEY=~/.ssh/jack-builder`, party `builder`), in the worktree `~/git/worktrees/jack/ops-resolve-{STAMP}` on branch `ops-resolve-{STAMP}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read`/`Glob` a path outside it. Your paths: `transcripts/`, `log.jsonl`. No code; edit no existing file. Read RUNBOOK `## jack resolve` only. Run the `tools/jack` verbs one at a time, each after the previous has printed its result — two run together take the same sequence number and the branch is unusable. Do not read `log.jsonl` whole — `python3 tools/clerk.py` lists every open writ with its forecast seq; one entry is `grep -n '"seq":<n>,' log.jsonl` (canonical JSON has no spaces).

**Resolve what is due, nothing else — and all of it.** List what is due with this command — not from `status.py`, whose W1 lines show only writs already past their deadline (on 2 November the 16:10 session read those, found only the builder's own expired 442–447, and resolved nothing while the 15:00 window sat due):
```
python3 - <<'EOF'
import json,datetime
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
E=[json.loads(l) for l in open('log.jsonl')]
done={e['body']['forecast'] for e in E if e['type']=='resolution'}
for e in E:
    b=e['body']
    if e['type']=='forecast' and b.get('type')=='world.renavon' and b.get('args',{}).get('stream')=='freshness' and e['seq'] not in done and b['args']['window_utc'][1]<=now and e['proposer']!='builder':
        print(e['seq'], e['proposer'], b['args']['dataset'], b['args']['window_utc'], 'due', b['resolves_by'])
EOF
```
Every line it prints is a forecast you resolve now: its window has ended, it is unresolved, and it is not the builder's own (the kernel refuses `self_judged`; never try one). If it prints nothing, nothing is due. If more than one window is due — an earlier tick was delayed — resolve every due forecast of every window, and name every window in the title. For each, fetch its `args.url` now with `curl -sL`, save the raw page under `transcripts/evidence/renavon-freshness/{STAMP}/<dataset>.html`, and record in `transcripts/evidence/renavon-freshness-{STAMP}-resolve.json` a list of rows `{"forecast": seq, "dataset", "url", "sha256", "fetched_at", "last_updated": "<as printed>", "last_updated_utc", "window_utc", "outcome": 1|0}` — outcome 1 iff the parsed last-updated instant is at or after `window_utc[0]`. If a page no longer prints a last-updated instant, or cannot be fetched, do not resolve that forecast; report it. Then for each row: `tools/jack resolve <seq> --outcome <o> --evidence "<dataset> last updated <as printed> (<utc>) against window <window_utc>; <saved path> sha256:<hash>"` — `<saved path>` is the path **relative to the repository root** (`transcripts/evidence/renavon-freshness/{STAMP}/<dataset>.html`), never an absolute path: an absolute path names a worktree that will not exist, and the 14:10Z session on 2 November exited with nothing proposed after following one into a directory it may not read. **Do not open earlier ticks' evidence files or directories at all**; every page you need you fetch yourself, now. If nothing is due, stop and report that; propose nothing.

**Order:** the `tools/jack resolve` commands first (each commits `log.jsonl` itself), then one commit for the evidence files, then — last of all, never before a resolution is entered — `tools/jack proposal --title "freshness: <k> resolved (<m> advanced) for window <window_utc[0]>"` (several windows: list them) — it runs the test suite and can take ten minutes, so call it with the bash tool's `timeout` set to `900000`. If the push is refused, run the two commands the verb prints and report their output. Report the PR number and each resolution (seq, dataset, outcome, your resolution's UTC time against the forecast's `resolves_by`).
