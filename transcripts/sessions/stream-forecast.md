model: openai/gpt-5.4-mini
key: ~/.ssh/jack-reviewer
branch: ops-stream-{N}

# reviewer: freshness stream {N} — six forecasts for the window two hours ahead (renavondata/jack)

You are the **reviewer** (`JACK_KEY=~/.ssh/jack-reviewer`, party `reviewer`), in the worktree `~/git/worktrees/jack/ops-stream-{N}` on branch `ops-stream-{N}`, cut from `origin/main` now. Do not read `~/git/jack` or anything outside this worktree; never `Read`/`Glob` a path outside it. Your paths: `transcripts/`, `log.jsonl`. No code; edit no existing file. Read RUNBOOK `## jack forecast` only. Do not read `log.jsonl` whole — one entry is `grep -n '"seq":<n>,' log.jsonl` (canonical JSON has no spaces); `python3 tools/clerk.py` lists the open forecasts.

**The window.** H = the top of the current hour, UTC: `H=$(date -u +%Y-%m-%dT%H:00:00Z)`. Forecast the window `[H+2h, H+3h)`: `W0=$(date -u -d "$H + 2 hour" +%Y-%m-%dT%H:%M:%SZ)`, `W1=$(date -u -d "$H + 3 hour" +%Y-%m-%dT%H:%M:%SZ)`, `BY=$(date -u -d "$H + 5 hour" +%Y-%m-%dT%H:%M:%SZ)`; use the printed values verbatim. A forecast of a window that has already begun is not a forecast.

**The six datasets** (BRIEF-C2a §Scope; urls in `transcripts/evidence/renavon-freshness-20261031-base.json`): `hk_property_poi`, `hkex_disclosures`, `hkex_disclosure_interests`, `crhk_companies`, `sfc_licences`, `hk_property_transactions`.

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

**Six forecasts, one per dataset**, in the form of the stream's earlier ones (read one: `grep -n '"seq":404,' log.jsonl`): the claim text with this window's instants and the dataset's url; `--type world.renavon`; `--by $BY`; `--args` a JSON object with the same keys as that entry — `stream`, `dataset`, `url`, `window_utc` (`[W0, W1]`), `hour_hkt`, `evidence`, `resolution_evidence`, `base_rate_permille`, `base_rate_population` — plus `"model": "openai/gpt-5.4-mini"`. Your p is yours, and the record above is your evidence: a dataset that has advanced in every window gets a high p; one that has never advanced a low one; one that has advanced in *some* windows is not daily — give it a p near its Laplace rate, higher in the hours it has advanced before, and **never below 50‰ or above 950‰ for a dataset that has surprised the record at least once** (one confident wrong call costs more than ten right ones earn). Write one line of reasoning per dataset, citing the counts, in `transcripts/REVIEWER-FRESHNESS-{STAMP}.md` before the entries.

**Check before proposing:** `grep -c "\"window_utc\":\[\"$W0\"" log.jsonl` must print 6. If it prints less, enter the missing datasets' forecasts; do not propose five.

Then one commit for the note and `tools/jack proposal --title "freshness stream {N}: six forecasts for window $W0"`. If the push is refused, run the two commands the verb prints and report their output. Report the PR number and the six (dataset, p) rows.
