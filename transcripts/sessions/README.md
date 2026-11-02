# Session prompts

The texts the runner on steel hands to a session, kept in the record so that a change to how a party is asked
to act is a proposal like any other (counsel's path, read by anyone, merged by the herald) rather than a file
on a machine. `renavondata/opencode-runner`'s `diary.yml` and `herald.yml` read them from `origin/main` of this
repository at dispatch time. Placeholders in braces are filled by the dispatcher: `{N}` the stream number,
`{STAMP}` the UTC stamp `YYYYMMDDTHHMM`, and for `repropose.md` `{BRANCH}`, `{KEY}`, `{PARTY}`, `{TITLE}`.

- `stream-forecast.md` — the reviewer forecasts the freshness window two hours ahead for the six datasets of
  BRIEF-C2a §Scope (Amendment 2: hourly, at twenty past).
- `stream-resolve.md` — the builder resolves the freshness forecasts whose window has ended (hourly, at ten past).
- `repropose.md` — a party re-enters a stale pull request's content and entries on a fresh prefix.
