# The opening push of C2a-prime (counsel's note for the sovereign's paste)

BRIEF-C2a-prime v7 §The window and §Order of acts step 2. Written on 5 November 2026, before the day, as the
brief requires. Part 1 lists what the push carries, recorded because `jack push` checks none of it; part 2 is
the paste.

## 1. What the push carries, at the branch head

Branch `opening-c2a-prime`, head `a17864cc6be14a9eb90810293b57a02dd38f66e6`.

- **Counted lines: 8,362 of 8,400**, by `judge.judge.counted_lines` over `sim/ harness/ tests/ pins/ tools/`
  (opencode-runner #280).
- **The read: `VERDICT: ACCEPT`**, the first line of `transcripts/REVIEW-C2a-prime-code.md` (gpt-6-astra,
  reviewer key). It records 145 mutants KILLED, 0 SURVIVED, STALE, TWIN FAILED or PENDING, and all 99 twins
  passing. `pytest`: 337 passed, 1 skipped.
- **Each commit's party, against SPEC §10.8's scopes:**

  | commit | `Proposer:` | paths | |
  |---|---|---|---|
  | `05dfcee` | builder builder-2 | `tests/test_c2a_prime.py`, `tools/status.py` | builder's scope |
  | `1c1b27f` | counsel counsel-2 | `SPEC.md`, `judge/scope.json` | the cap, by the precedent of C2a's opening (`cd9d8eb`) |
  | `bfd685e` | reviewer reviewer-2 | `pins/c2aprime.py`, `pins/pins.py` | reviewer's scope |
  | `a17864c` | reviewer reviewer-2 | `transcripts/REVIEW-C2a-prime-code.md` | reviewer's scope |

- **The trusted base changes in three places:** `judge/scope.json`'s `cap`, 7,800 → 8,400; SPEC §10's block,
  to match; and SPEC §10's cap history, which gains "raised to 8400 at the opening of C2a-prime, the budget
  BRIEF-C2a-prime v7 pre-stated and measured before the build (…), by the opening push that carries the window
  code, its tests and the reviewer's pins (transcripts/PUSH-c2a-prime-opening.md)". That clause names this
  note. No kernel source changes, so no run of record is due.

The window opens at this push's `ts` and ends at V5's `resolves_by`, `2026-11-30T00:00:00Z`.

## 2. The paste

**Conditions.** Paste only when all of these hold.
- It is after `2026-11-17T12:00:00Z`.
- Counsel's V5–V7 are on `main`.
- No `push` and no `decision promote C2a` has been entered since seq 367.
- No pull request is open on `renavondata/jack`.

The first three lines below print what you need to check: the clock, the open pull requests (none should be
listed) and the last `push` entry's seq (it should be 367). If any check fails, stop and tell counsel.

```
cd ~/git/jack && git switch main && git pull --ff-only
date -u +%FT%TZ
gh pr list -R renavondata/jack --state open
python3 -c "import json; print([json.loads(l)['seq'] for l in open('log.jsonl') if json.loads(l)['type']=='push'][-1])"
tools/jack decision grant "GitHub App renavondata-jack-court[bot]: the court's platform acts on renavondata/jack (opencode-runner #227), in force since 2026-11-04T05:40Z"
tools/jack decision fix "C2a: criterion 7 unmet at the stated end — nine off-log repair rows (acts-20261103T2144); the court's platform acts moved to a GitHub App (opencode-runner #227)"
git fetch origin
git worktree add -b opening-c2a-prime-push ~/git/worktrees/jack/opening-c2a-prime-push origin/opening-c2a-prime
git -C ~/git/worktrees/jack/opening-c2a-prime-push merge --no-ff --no-edit origin/main -m "merge: main into C2a-prime's opening branch, after the grant and the fix" -m "Proposer: guy guy-master"
tools/jack push opening-c2a-prime-push --opens C2a-prime --review ~/git/worktrees/jack/opening-c2a-prime-push/transcripts/REVIEW-C2a-prime-code.md
```

**Notes on the paste.**
- The `fix` line is the ruling's Order 3 paste, word for word.
- The merge commit carries your `Proposer:` trailer, because `jack push` refuses a commit without one.
- The local branch is named `opening-c2a-prime-push` so that it does not collide with a branch the runner
  has checked out.
- If `jack push` refuses, nothing has moved except the two `decision` entries, which stand. Send counsel the
  refusal.

**Afterwards**, counsel reads `python3 tools/status.py --subject C2a` on the new `main`. The window line must
read from this push's `ts` to `2026-11-30T00:00:00Z`.
