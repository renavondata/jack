model: {MODEL}
key: ~/.ssh/jack-builder
branch: {BRANCH}

# builder: build to the texts {TEXTS} on branch {BRANCH} (renavondata/jack)

You are the **builder** (`JACK_KEY=~/.ssh/jack-builder`, party `builder`), in the worktree `~/git/worktrees/jack/{BRANCH}` on branch `{BRANCH}`, cut from `origin/main` now. Do not read or write anything outside this worktree. Your paths: `sim/`, `harness/`, `tests/`, `tools/`, `transcripts/`, `log.jsonl` (`judge/scope.json`). Run the `tools/jack` verbs one at a time. Now is the UTC instant `date -u +%Y-%m-%dT%H:%M:%SZ` prints.

**The texts.** `{TEXTS}` is a comma-separated list of paths on `origin/main` — a brief's rules, a window file, a runner definition under `transcripts/runner/`, a session template. Read each whole. They are what you build to (SPEC §10.8: counsel writes texts, you write code), and the sovereign has read them (A2.10). Where a text names a rule, implement it once; where it names twins and mutants, your tests make the twins pass; where it names a pin, the reviewer writes the pin, not you. Where a text is undecidable or contradicts another in force, build nothing for that rule and say so in your report with the sentence that stops you: a `spec_conflict` entry is the lawful objection (`tools/jack spec_conflict --section S --text T`), never a guess.

**Build.** Commit as you go, each commit with the trailer `Proposer: builder <your model id> <this issue's number>` and, from C2c-2, `Model: <your model id>`. Run the tests, the pins and the count (`python3 -m unittest discover -s tests -t .`; `python3 pins/run.py`; `python3 tools/count_kernel.py`) before proposing; `main` is never red by design. Then `tools/jack proposal --title "<what you built, in one line>"` with the bash tool's `timeout` set to `900000`; if the push is refused, run the two commands the verb prints.

Report, as the issue's last comment: what you built, to which text and section; what you did not build and why, quoting the sentence; the PR number.
