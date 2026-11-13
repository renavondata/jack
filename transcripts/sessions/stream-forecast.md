model: openai/gpt-5.4-mini
key: ~/.ssh/jack-reviewer
branch: ops-stream-{N}

# reviewer: freshness stream {N} — six forecasts for the window two hours ahead (renavondata/jack)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/ops-stream-{N}` on branch `ops-stream-{N}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read`/`Glob` a path outside it. Your paths: `transcripts/`, `log.jsonl`. No code; edit no existing file. Read RUNBOOK `## jack forecast` only. Run the `tools/jack` verbs one at a time, each after the previous has printed its result — two run together take the same sequence number and the branch is unusable. Do not read `log.jsonl` whole — one entry is `grep -n '"seq":<n>,' log.jsonl` (canonical JSON has no spaces); `python3 tools/clerk.py` lists the open forecasts.

**The windows (BRIEF-C2a Amendment 3).** H = the top of the current hour, UTC: `H=$(date -u +%Y-%m-%dT%H:00:00Z)`. This session covers **three** hourly windows: `[H+2h, H+3h)`, `[H+3h, H+4h)` and `[H+4h, H+5h)` — compute `A=$(date -u -d "$H + 2 hour" +%Y-%m-%dT%H:%M:%SZ)`, `B=$(date -u -d "$H + 3 hour" +%Y-%m-%dT%H:%M:%SZ)`, `C=$(date -u -d "$H + 4 hour" +%Y-%m-%dT%H:%M:%SZ)`. If you were started late, also compute `P=$(date -u -d "$H + 1 hour" +%Y-%m-%dT%H:%M:%SZ)`. For each candidate start in P, A, B, C: skip it if it is less than twenty minutes ahead of now, or if `grep -c "\"window_utc\":\[\"<start>\"" log.jsonl` prints 6 or more (already forecast on `main`); otherwise it is one of your windows. For each of your windows, W0 = its start, `W1=$(date -u -d "$W0 + 1 hour" +%Y-%m-%dT%H:%M:%SZ)`, `BY=$(date -u -d "$W1 + 4 hour" +%Y-%m-%dT%H:%M:%SZ)` (the deadline is the window's end plus four hours); use the printed values verbatim. A forecast of a window that has already begun is not a forecast; a window forecast twice gains nothing (the second is a revision).

**The six datasets** (BRIEF-C2a §Scope; urls in `transcripts/evidence/renavon-freshness-20261031-base.json`): `hk_property_poi`, `hkex_disclosures`, `hkex_disclosure_interests`, `crhk_companies`, `sfc_licences`, `hk_property_transactions`. Print their urls and copy each from that output, never from memory:
```
python3 -c 'import json; u={r["dataset"]: r["url"] for r in json.load(open("transcripts/evidence/renavon-freshness-20261031-base.json"))["datasets"]}; [print(d, u[d]) for d in ("hk_property_poi","hkex_disclosures","hkex_disclosure_interests","crhk_companies","sfc_licences","hk_property_transactions")]'
```

**Two things before anything else.** Print neither `log.jsonl` nor the output of `python3 tools/clerk.py` whole: each is hundreds of lines, and a session that printed one ended with nothing entered (stream 94). And enter the eighteen forecasts before you write the note: a session that wrote its note and ran `tools/jack proposal` without running `tools/jack forecast` once entered nothing, and three windows went unforecast (stream 99). The check under **Check before proposing** prints 6 for each of your windows before the note is written and before the proposal is run.

**The record first.** Print each dataset's resolved windows so far — how many advanced, and in which hours (UTC) it advanced:
```
python3 - <<'EOF'
import json
from collections import defaultdict
E=[json.loads(l) for l in open('log.jsonl')]
F={e['seq']:e for e in E if e['type']=='forecast' and e['body'].get('type')=='world.renavon' and e['body'].get('args',{}).get('stream')=='freshness'}
c=defaultdict(lambda:[0,0,[]])
for e in E:
    if e['type']=='resolution' and e['body']['forecast'] in F:
        a=F[e['body']['forecast']]['body']['args']; d=a['dataset']; c[d][0]+=1; c[d][1]+=e['body']['outcome']
        if e['body']['outcome']: c[d][2].append(a['window_utc'][0][11:13]+'Z')
for d,(n,s,hrs) in sorted(c.items()): print(f"{d}: {s}/{n} windows advanced; Laplace {(s+1)/(n+2):.3f}; advanced at hours {sorted(set(hrs))}")
EOF
```

**Six forecasts per window, one per dataset** (eighteen for three windows), in the form of the stream's earlier ones (read one: `grep -n '"seq":404,' log.jsonl`): the claim text with this window's instants and the dataset's url; `--type world.renavon`; `--by $BY`; `--args` a JSON object with the same keys as that entry — `stream`, `dataset`, `url`, `window_utc` (`[W0, W1]`), `hour_hkt`, `evidence`, `resolution_evidence`, `base_rate_permille`, `base_rate_population` — plus `"model": "openai/gpt-5.4-mini"`. Your p is yours, and the record above is your evidence: a dataset that has advanced in every window gets a high p; one that has never advanced a low one; one that has advanced in *some* windows is not daily — give it a p near its Laplace rate, higher in the hours it has advanced before, and **never below 50‰ or above 950‰ for a dataset that has surprised the record at least once** (one confident wrong call costs more than ten right ones earn: on 2 November `crhk_companies` was forecast at 25‰ and then 20‰ in two windows where its record stood near 3 in 4, it advanced both times, and each cost the value process about thirty per cent — the fourteen correct 980‰ calls around them earned two per cent each). A mixed record means a middling p, near the Laplace rate, moved by the hour pattern and never past those bounds. Write one line of reasoning per dataset, citing the counts, in `transcripts/REVIEWER-FRESHNESS-{STAMP}.md` before the entries.

**Check before proposing:** for each of your windows, `grep -c "\"window_utc\":\[\"<W0>\"" log.jsonl` must print 6. If one prints less, enter the missing datasets' forecasts for it; do not propose a window short.

**And every url must be the base file's.** This must print nothing:
```
python3 - <<'EOF'
import json, subprocess
u={r["dataset"]: r["url"] for r in json.load(open("transcripts/evidence/renavon-freshness-20261031-base.json"))["datasets"]}
base=subprocess.run(["git","merge-base","HEAD","origin/main"],capture_output=True,text=True).stdout.strip()
n=len(subprocess.run(["git","show",base+":log.jsonl"],capture_output=True,text=True).stdout.splitlines())
for l in open("log.jsonl").read().splitlines()[n:]:
    e=json.loads(l); a=e["body"].get("args") if e["type"]=="forecast" else None
    if isinstance(a,dict) and a.get("url")!=u.get(a.get("dataset")): print("WRONG URL", e["seq"], a.get("dataset"), a.get("url"))
EOF
```
If it prints a line, do not write the note and do not propose: report the lines and stop. A forecast on a page that is not the dataset's cannot be resolved and expires: stream 108 (12 November) entered twelve on four such pages, and five expired.

Then one commit for the note and `tools/jack proposal --title "freshness stream {N}: forecasts for windows <your W0s, comma-separated>"` — it runs the test suite and can take ten minutes, so call it with the bash tool's `timeout` set to `900000`. If the push is refused, run the two commands the verb prints and report their output. Report the PR number and the six (dataset, p) rows.
