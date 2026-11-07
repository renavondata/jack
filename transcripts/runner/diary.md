# The diary — definition (counsel's text, C2c-1; today `.github/workflows/diary.yml`)

## What it holds
`~/git/jack` (the court's checkout on steel); the owner's `gh` login or the App's identity; no signing key.

## When it runs
Dispatched by steel's timer at ten past every hour and at twenty past every third hour (never by GitHub's schedule: it fired once unbidden on 1 Nov). The minute of the dispatch decides the role, not the minute the job gets a runner.

## What it does, in order
1. Fetch `origin/main`; read `log.jsonl` and `transcripts/sessions/due-resolve.md` from it; read the runner's own issues of the last three hours titled `resolve the writs due` (what was already handed).
2. **At :10, the due list.** For every unresolved forecast on `main` whose evidence should now exist — a freshness window that has ended; a race whose off time passed half an hour ago; a proposal whose first tests run has had an hour; any other claim within two hours of its deadline — and that was not handed to a session in the last three hours, one line (seq, proposer, type, what it is about, deadline, `PAST DUE` if past, claim). A line past due stays on the list, tick after tick, until it is resolved (on 3 November a six-hour cutoff dropped four of counsel's forecasts from every list while `status.py` printed ESCALATED; the diary writes no evidence and decides nothing — the escalations evidence is derived from the issues this step files, by the evidence session, C2c-1 R6). The lines are routed by proposer: the builder's to the reviewer, everyone else's to the builder (the kernel refuses self-resolution). Per party with lines: one issue, the template filled (`{PARTY} {MODEL} {STAMP} {NOW} {COUNT} {LIST}` and a trailing `due-seqs:` line), labelled `run`; `gpt-5.4-mini` when every line is freshness, `gpt-6-astra` otherwise (a wrong resolution is permanent).
3. **At :20, the forecast.** One reviewer issue from `transcripts/sessions/stream-forecast.md` with the next stream number (one more than the largest in this repository's issue titles), labelled `run`; at the cadence the window file names (`stream_cadence_hours`), skipping the ticks between.
4. **At the first :10 tick of each UTC day, the evidence session.** One builder issue from `transcripts/sessions/evidence.md` for the window now open (the latest `transcripts/windows/<w>.json` on `main` whose opening is on the log), labelled `run`, so the escalations, acts and runner evidence reach `main` by proposal at least daily; the sovereign files one by hand before a promotion if the newest is older than the grace.
5. Print what it filed.

## What it never does
Decide a resolution; write a file into the tree or sign anything; read `log.jsonl` into a model; drop a past-due forecast from the list before it is resolved; hand a seq twice within three hours; file with the workflow's token (an issue the token creates raises no `labeled` event and the session never starts).
