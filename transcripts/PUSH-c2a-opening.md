# The opening push of C2a (counsel's note for the sovereign's `jack push`)

Three edits, pre-stated in BRIEF-C2a v1 §Scope ("the cap") and nothing else: `judge/scope.json` `cap` 6900 → 7300
and the identical block in SPEC §10 with one clause added to the cap's history; `.github/workflows/tests.yml`
skipping the simulator-sample step (about three of a run's seven minutes) on a head whose diff against its first
parent is `log.jsonl` alone — a forecast, a resolution, a merge entry — and running every other step as before.
The checkout fetches two commits so that the diff can be taken; no kernel source changes; no run of record is due.

Why 7,300 before the build rather than a measured push after it: C1b's cap moved mid-window (6,200 → 6,900, seq
197) and that was the window's one sovereign act besides the promote; the C1b report names it as the thing C2a
is written to avoid. The number is a budget the builder reports against; if `tools/value.py`, its tests and
the fourteen pins do not fit, the builder stops with the shortfall and the window fails on criterion 3
(BRIEF-C2a §Stop and report). C2a's window opens at this entry's `ts`.

What the skip changes and what it does not: the simulator sample compares kernel and kernel2 on committed
vectors and reads nothing a log-only head changes; unit tests, pins, the judge self-check and the kernel count
still run on every head, so W3 ("the herald merges only on green CI") verifies on a log-only head everything it
verified before except a comparison whose inputs that head cannot have moved.
