# The session runner — definition (counsel's text, C2c-1; today `.github/workflows/run.yml`)

## What it holds
`~/git/jack`; the party keys at `~/.ssh/jack-<party>` (every key readable by every job on steel, #188); the App's identity; the model API keys from the runner's own `.env`, never from GitHub.

## When it runs
When an issue in `renavondata/opencode-runner` is labelled `run`. An issue also labelled `build` runs only on a runner labelled `build` (long work); otherwise on any `opencode` runner (the diary's sessions, whose deadlines are inside the hour).

## What it does, in order
1. Take the issue body as the prompt; from its first four lines take `model:` (default `openai/gpt-6-astra`), `key:` (exported as `JACK_KEY`; **from C2c-1 only a path under `~/.ssh/jack-` that matches the party the issue's title names**, else refused) and `branch:` (default `issue-<n>`). Comment `started: run <id> on <host>, model, key, branch`.
2. In `~/git/jack`, fetch; create or reuse the worktree `~/git/worktrees/jack/<branch>` from `origin/main`; run the model there with a fifteen-minute command timeout and the prompt, teeing the transcript.
3. Post the transcript's last 60,000 bytes as a comment; relabel `run` → `done`; close the issue; close any earlier `done` issue still open.

## What it never does
Read or write outside the worktree; set the job's token where the session's `gh` would shadow the App's identity; give a session a key its party does not hold (the refusal of step 1 is C2c-1's; today any `key:` is exported).
