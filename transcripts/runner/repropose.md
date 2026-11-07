# Repropose — definition (counsel's text, C2c-1; today `.github/workflows/repropose.yml` and `.github/scripts/repropose.py`)

## What it holds
The party keys; `~/git/jack`; the App's identity.

## When it runs
Dispatched by the herald when it closes a builder's or reviewer's pull request as stale, with the PR's number, head branch, party and title.

## What it does, in order
1. On a fresh branch from `origin/main` (`<branch>-r`, the first free), re-apply the stale PR's evidence files.
2. Re-enter its forecasts and resolutions with the jack verbs under the same party's key, skipping by rule only: a forecast of a window already begun or past its deadline; a resolution `main` already holds.
3. `tools/jack proposal` with the PR's title.
4. On anything unexpected (exit 2), file the model session `transcripts/sessions/repropose.md` describes, so nothing is lost by trying the machine first.

## What it never does
Change what the stale PR said; skip a resolution as if it were a forecast (3 Nov); act under a key other than the stale PR's party's.
