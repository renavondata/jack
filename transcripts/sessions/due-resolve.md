model: {MODEL}
key: ~/.ssh/jack-{PARTY}
branch: due-{PARTY}-{STAMP}

# {PARTY}: resolve the writs due — {COUNT} listed, computed by the diary at {NOW} (renavondata/jack)

You are the **{PARTY}** (`JACK_KEY=~/.ssh/jack-{PARTY}`, party `{PARTY}`), acting only as a resolver, in the worktree `~/git/worktrees/jack/due-{PARTY}-{STAMP}` on branch `due-{PARTY}-{STAMP}`, cut from `origin/main` now. Do not read or write anything outside this worktree; never `Read`/`Glob` a path outside it, and never write under `/tmp` (the session may not). Your paths: `transcripts/`, `log.jsonl`. No code; edit no existing file. Read RUNBOOK `## jack resolve` only. Run the `tools/jack` verbs one at a time, each after the previous has printed its result — two run together take the same sequence number and the branch is unusable. Do not read `log.jsonl` whole: one entry is `grep -n '"seq":<n>,' log.jsonl` (canonical JSON has no spaces). Now is the UTC instant `date -u +%Y-%m-%dT%H:%M:%SZ` prints; every instant in this issue and in the log is UTC (a `Z` suffix), never Hong Kong or Israel time.

**The list.** The diary computed it from `origin/main` at {NOW}: every unresolved forecast whose evidence should now exist (a window or race that has ended, a proposal whose first tests run has finished, a claim whose deadline is within two hours) and that is **not your own principal's** (the kernel refuses `self_judged`; never try one). One line per writ — seq, proposer, type, what it is about, its deadline, its claim:

{LIST}

Every line is a forecast you resolve now **if its procedure below decides it from evidence you produce now**. A wrong resolution is permanent: when the evidence does not decide a claim exactly as worded, enter nothing for it and report it under *left undecided* with the reason. A line marked `PAST DUE` has already expired for liveness; resolve it only if its procedure still decides it (a page that still witnesses the window, a results page that still exists), otherwise leave it. Read each claim in full from its own entry before deciding it; the list's claim column is truncated.

**Procedures, by type.**

*`world.renavon`, stream `freshness`* — for each, fetch its `args.url` now with `curl -sL`, save the raw page under `transcripts/evidence/renavon-freshness/{STAMP}/<dataset>.html`, and record in `transcripts/evidence/renavon-freshness-{STAMP}-resolve.json` a list of rows `{"forecast": seq, "dataset", "url", "sha256", "fetched_at", "last_updated": "<as printed>", "last_updated_utc", "window_utc", "outcome": 1|0}` — outcome 1 iff the parsed last-updated instant is at or after `window_utc[0]`. A page that no longer prints a last-updated instant, or cannot be fetched, leaves that forecast undecided. Evidence string: `"<dataset> last updated <as printed> (<utc>) against window <window_utc>; transcripts/evidence/renavon-freshness/{STAMP}/<dataset>.html sha256:<hash>"` — the path **relative to the repository root**, never absolute. Do not open earlier ticks' evidence files or directories; every page you need you fetch yourself, now.

*`world.hkjc`* — the entry's `args` name the meeting, the race and `off_utc`; its `args.resolution_evidence` names the page. Fetch the HKJC results and dividends page for that race with `curl -sL`, save the raw bytes under `transcripts/evidence/hkjc-<meeting date>/results-race-<r>.html`, and record `{"race", "winner", "winner_no", "shortest_final_win_odds": {"runner", "no", "odds"}, "favourite_won", "dead_heat", "void", "sources": [{"url", "sha256", "fetched_at"}]}` in `transcripts/evidence/hkjc-<meeting date>-results-{STAMP}.json`. The favourite is the runner with the shortest **final** WIN odds over every runner, not the winner's dividend alone. A race not yet run, or a page without final results, leaves the forecast undecided — never resolve from a live page. Outcome as the claim words it (a dead-heat involving the favourite is 1; a void race is 0). Evidence string: `"race <r>: winner <name> (<no>); shortest final WIN odds <runner> (<no>) at <odds>; <saved path> sha256:<hash>"`.

*`proposal.ci`, `proposal.count`* — the forecast belongs to the proposal entered just after it by the same proposer; find it and its head with
```
python3 - <<'EOF'
import json; E=[json.loads(l) for l in open('log.jsonl')]; S=<seq>
f=next(e for e in E if e['seq']==S); p=next(e for e in E if e['seq']>S and e['type']=='proposal' and e['proposer']==f['proposer'])
print(p['seq'], p['body'].get('commit'), p['body'].get('title'))
EOF
```
`body.commit` is the branch's last content commit (SPEC §10.7); the **proposal head** is the commit after it that carries the proposal entry, and the first tests run on it is the run the pull request's opening triggered. Find the pull request and that run:
```
gh api "repos/renavondata/jack/commits/<commit>/pulls" --jq '.[] | "\(.number) \(.head.ref) \(.state)"'
gh api "repos/renavondata/jack/actions/runs?branch=<head.ref>&event=pull_request&per_page=50" --jq '[.workflow_runs[] | select(.name=="tests")] | sort_by(.created_at) | .[0] | "\(.id) attempt \(.run_attempt) head \(.head_sha) created \(.created_at) \(.conclusion)"'
```
(take the pull request whose branch holds `body.commit` first — a later `-r` branch is a re-proposal, not this proposal). For `proposal.ci` ("the tests workflow is green on the first run of this branch's proposal head"): outcome 1 iff that earliest run's conclusion at attempt 1 is `success`; a run still in progress leaves it undecided. Evidence: `"tests run <id> (pull_request, attempt <n>, created <instant>), the first on PR #<N>'s proposal head <head_sha> (proposal seq <p>, commit <commit>): <conclusion>"`. A claim about pins ("every pin of this branch is KILLED with a passing twin in the first tests run") is decided from that run's log — `gh run view <id> -R renavondata/jack --log 2>/dev/null | grep -iE 'KILLED|SURVIVED|twin' | tail -20` — only if the log states each pin's verdict; otherwise leave it undecided. For `proposal.count` ("the counted lines of this branch's proposal head are at most N"): `git fetch -q origin <commit>` then `python3 -c 'from judge.judge import counted_lines; print(counted_lines(".", "<commit>", ["sim/", "harness/", "tests/", "pins/", "tools/"]))'`; outcome 1 iff the number is at most the N the claim states. Evidence: `"counted_lines at proposal seq <p> head <commit> = <n>, claim at most <N>"`.

*Crossing claims* (`counsel.programme` whose claim says C2a's value *E* and continued liveness *E* are **both** at least 20 on `main` at some prefix with `ts` before an instant *I*) — the two processes are evaluated together at every entry instant from the opening push (seq 367) to *I*; value *E* changes only when an entry arrives and continued liveness can only fall between entries, so the entry instants are the suprema. First save the runs file the gates need (the one on `main` may predate them):
```
mkdir -p transcripts/evidence && python3 - <<'EOF'
import json, subprocess
runs=[]
for page in range(1,15):
    r=subprocess.run(["gh","api",f"repos/renavondata/jack/actions/workflows/tests.yml/runs?per_page=100&page={page}"],capture_output=True,text=True)
    w=json.loads(r.stdout).get("workflow_runs",[]); runs+=w
    if len(w)<100: break
keep=["id","name","path","event","status","conclusion","head_branch","head_sha","created_at","updated_at","run_number","html_url"]
json.dump([{k:x.get(k) for k in keep} for x in runs], open("transcripts/evidence/runs-tests-{STAMP}.json","w"), indent=0); print("runs saved:", len(runs))
EOF
```
then the table, with `END` set to *I* exactly as the claim states it (the heredoc is a computation, not repository code; it calls the four functions `assess_value` in `tools/status.py` calls — confirm that by reading `assess_value` first):
```
python3 - <<'EOF' > transcripts/evidence/crossing-{STAMP}-<I without punctuation>.txt
import json, os, sys
from fractions import Fraction
ROOT, RUNS = os.getcwd(), "transcripts/evidence/runs-tests-{STAMP}.json"
START, END = "2026-11-01T15:04:14Z", "<I>"
sys.path.insert(0, ROOT)
from kernel import check
from tools import status as st
from tools import value as val
with open(os.path.join(ROOT, "log.jsonl"), "rb") as f:
    lines = check.read_lines(f.read())
assert check.check(lines)["ok"]
es = [json.loads(l) for l in lines]
runs = json.load(open(RUNS))
gate_v = st.attack_start(ROOT, runs, END, "tests/test_value.py")
gate_l = st.attack_start(ROOT, runs, END)
opening_c1b = st.c1b_window(es)[0]
print(f"# value attack-green {gate_v}; liveness attack-green {gate_l}; c1b opening seq {opening_c1b}")
print("ts | last_seq | value_E | liveness_E_fraction | liveness_E")
instants = sorted({e["ts"] for e in es if START <= e["ts"] <= END} | {START, END})
best = (Fraction(0), None)
for T in instants:
    prefix = [e for e in es if e["ts"] <= T]
    v = val.value(prefix, as_of=T, attack_green=gate_v)
    process = st.item_process(prefix, opening_c1b, T)
    live = st.score_items(i for i in process["items"] if gate_l is not None and gate_l < i["ts"])
    both = min(Fraction(v["E_value"]), live["E"])
    if both > best[0]:
        best = (both, T)
    print(f"{T} | {prefix[-1]['seq']} | {v['E_value']:.6f} | {live['E']} | {float(live['E']):.6f}", flush=True)
print(f"# max over instants of min(value E, liveness E): {float(best[0]):.6f} at {best[1]}")
EOF
```
The header line must name both gates (neither `None`; otherwise the runs file is incomplete — leave the claim undecided). Spot-check one row against `python3 tools/value.py --as-of <ts> --attack-green <value gate>` and `python3 tools/status.py --as-of <ts> --runs transcripts/evidence/runs-tests-{STAMP}.json | grep '^liveness continued'`. If the last line's maximum is below 20, the claim is **0**; if 20 or more, it is **1** only if that row's `ts` is before *I* (it is, by construction) — and then stop and report before resolving, because a crossing is the sovereign's business too. Evidence string: `"joint table <file>: max over every prefix before <I> of min(value E, continued liveness E) = <value> at <ts>"`. Several crossing claims with the same *I* share one table; a claim with a later *I* needs its own run. The instant *I* must have passed; a claim whose *I* is still ahead is left undecided (it is not yet false).

*Anything else* (`counsel.programme`, `review.forecast`, untyped) — read the whole entry: the claim, `args.evidence`, `args.id`. Decide it only if the claim's own terms are settled by evidence you can produce in this session with the tools on this tree (`git log`/`git show` on `origin/main`, `tools/status.py`, `tools/value.py`, `tools/jack score`, the GitHub API) and the claim's instant has passed or the claim is already true. Save what you ran and what it printed under `transcripts/evidence/due-{STAMP}-<seq>.txt` and name that file in the evidence string. If the claim needs a procedure you cannot complete here (a joint statistic over many prefixes, a table counsel keeps, a judgement about text), leave it undecided and say exactly what would decide it.

**Order:** the `tools/jack resolve <seq> --outcome <o> --evidence "<…>"` commands first (each commits `log.jsonl` itself; the writs with the earliest `resolves_by` first), then one commit for the evidence files (`git add transcripts/evidence/...` by name; never `git add -A`), then — last of all, never before a resolution is entered — `tools/jack proposal --title "due {STAMP}: <k> resolved (<types>)"` — it runs the test suite and can take ten minutes, so call it with the bash tool's `timeout` set to `900000`. If the push is refused, run the two commands the verb prints and report their output. If nothing on the list is decided, propose nothing. Report: the PR number; each resolution as (seq, outcome, your resolution's UTC time against the forecast's `resolves_by`); and *left undecided*: each seq with the reason.
