# The opening push of C2a-prime (counsel's note for the sovereign's paste)

BRIEF-C2a-prime §The window and §Order of acts step 2, as amended (Amendments 5, 7 and 9). Written again on
13 November 2026 by counsel-5, for the branch that holds the rebuild; the note of 5 November was for the
first build, which does not enter (the sovereign's entry at seq 3545). SPEC §10's cap history, in the push's
first commit, names this file. Part 1 lists what the push carries, recorded because `jack push` checks none
of it; part 2 is the paste; part 3 is what follows it. **The commands are final only when counsel says so in the
sitting message.**

## 1. What the push carries, at the branch head

Branch `opening-c2a-prime-3`, head `ced344f9363ce9149e97044027107317b14a4c69`.

- **Counted lines: 8,347 of 8,400**, by `judge.judge.counted_lines` over `sim/ harness/ tests/ pins/ tools/`.
- **The read: `VERDICT: ACCEPT`**, the first line of `transcripts/REVIEW-C2a-prime-code.md` on the branch
  (`Reviewed tree: 5f2a94b9`; reviewer key, `openai/gpt-5.6-terra`, runner issue #770). The pins on that tree:
  `KILLED 147, SURVIVED 0, STALE 0, TWIN FAILED 0` (#769).
- **The gate's two reviews of the brief** are on `main` at its present bytes (SHA-256 `02b4411f…9675`):
  `transcripts/REVIEW-C2a-prime-20261113T0629-openai.md` (`openai/gpt-6-astra`) and
  `transcripts/REVIEW-C2a-prime-20261113T0629-google.md` (`google/gemini-4-argon`), each `VERDICT: ACCEPT`,
  `Reviewed tree: ac104c5b`. `push_read_gate` from `tools/jack` passes on `main` (counsel, 13 November
  07:50Z, in a scratch clone). A third file, `REVIEW-C2a-prime-20261113T0330.md`, holds argon's review
  written over astra's and counts for nothing (COUNSEL-OPEN row 64). The brief is not amended again before
  the push: an amendment would stale both reviews.
- **Each commit's party, against SPEC §10.8's scopes**, the trusted-base commit apart:

  | commit | author / committer, as git prints them | `Proposer:` | paths | |
  |---|---|---|---|---|
  | `43df79af` | counsel / Guy Freeman | counsel | `SPEC.md`, `judge/scope.json` | the trusted-base change: counsel's patch, applied by the sovereign's own hand (seqs 4016, 4017) |
  | `269cc512`, `4c1f9c97`, `0d9c5e8b`, `25274da0`, `a30a6a3b`, `74b0b074` | Guy Freeman / Guy Freeman | builder (#697) | `tools/status.py`, `tests/test_status.py` | builder's scope; changes 1 to 3 |
  | `1db53f43`, `4966d9ff` | Guy Freeman / Guy Freeman | builder (#733) | `tools/jack`, `tools/status.py`, `tests/` | builder's scope; change 4 in Amendment 6's form |
  | `c788e8aa` | Guy Freeman / Guy Freeman | builder (#758) | `tools/jack`, `tests/test_jack.py` | builder's scope; change 4 in Amendment 7's form, the form of the tree |
  | `33ee227a` | Guy Freeman / Guy Freeman | reviewer (#769) | none | the merge of the builder's branch into the reviewer's |
  | `64f7d294`, `5f2a94b9` | Guy Freeman / Guy Freeman | reviewer (#703, #769) | `pins/c2a_prime.py`, `pins/pins.py` | reviewer's scope; the eight pins and the ninth |
  | `ced344f9` | Guy Freeman / Guy Freeman | reviewer (#770) | `transcripts/REVIEW-C2a-prime-code.md` | reviewer's scope |

  Sessions on the runner commit under the runner's git identity, which is the sovereign's name; the party of
  such a commit is in its trailer. Only the first commit is of his own hand (seq 4017). In the second, third
  and sixth rows the paths are those of the row's commits together.

  The nine builder commits are the re-creation, by one `git cherry-pick`, of the nine built on
  `builder-c2a-prime-rebuild` (`git range-diff` pairs each with its original by `=`; #766). The thirteen
  after the first were committed after the entry at seq 4017, and the first sixteen seconds before that
  entry, which reports it. Commit `32df5f10` is no ancestor of the head.
- **The trusted base changes in three places:** `judge/scope.json`'s `cap`, 7,800 → 8,400; SPEC §10's block, to
  match; and one clause of SPEC §10's cap history, which begins "raised to 8400 at the opening of C2a-prime"
  and names this note. The brief quotes that clause in short ("8,400 at C2a-prime's opening, for the window
  code"); the commit's words are the ones the sovereign read (seq 4016). No kernel source changes, so no run
  of record is due.

To print these again:

```
git fetch origin main opening-c2a-prime-3
git log --reverse --format='%h | %an | %cn | %cI | %(trailers:key=Proposer,valueonly,separator=%x20) | %s' origin/main..origin/opening-c2a-prime-3
git merge-base --is-ancestor 32df5f10 origin/opening-c2a-prime-3; echo $?
python3 -c 'from judge.judge import counted_lines; print(counted_lines(".", "ced344f9363ce9149e97044027107317b14a4c69", ["sim/", "harness/", "tests/", "pins/", "tools/"]))'
git show origin/opening-c2a-prime-3:transcripts/REVIEW-C2a-prime-code.md | head -3
```

The window opens at this push's `ts` and ends at V5's `resolves_by`, `2026-11-30T00:00:00Z`.

## 2. The paste

One paste, on the machine that holds the sovereign's key. It stops at the first line that fails and says so.
It checks for itself that:
- it is after `2026-11-17T12:00:00Z`;
- no proposal is open on `renavondata/jack` (the three standing pull requests #125, #316 and #562 apart: none
  of them is a proposal that can merge), and the minute is 40 or later, so that the next batch cannot merge
  before the push has landed. It prints `waiting` every thirty seconds until both hold, which can take up to
  an hour; it may be left running;
- the log holds seven `push` entries, the last at seq 367, and no `decision promote C2a`;
- the branch head is the commit named above. It makes the push's worktree and checks this before it enters
  anything;
- the verb's own read gate passes: it runs `push_read_gate` from `tools/jack`, which reads and writes nothing
  else, so that a review gone stale or overwritten stops the paste before the `grant` and not after the `fix`.

Counsel's V5–V7 have been on `main` since 5 November (seqs 1580 to 1582).

```
cd ~/git/jack && git switch main && [ "$(date -u +%s)" -gt 1794916800 ] && until [ "$(gh api 'repos/renavondata/jack/pulls?state=open&per_page=100' --jq 'map(select(.number!=125 and .number!=316 and .number!=562))|length')" = 0 ] && [ "$(date -u +%M)" -ge 40 ]; do echo "waiting: a proposal is open, or the minute is before 40"; sleep 30; done && git pull --ff-only && [ "$(grep -c '"type":"push"' log.jsonl)" = 7 ] && ! grep -q '"kind":"promote","subject":"C2a"' log.jsonl && git fetch origin && git worktree add -b opening-c2a-prime-3-push ~/git/worktrees/jack/opening-c2a-prime-3-push origin/opening-c2a-prime-3 && [ "$(git -C ~/git/worktrees/jack/opening-c2a-prime-3-push rev-parse HEAD)" = ced344f9363ce9149e97044027107317b14a4c69 ] && python3 -c 'import runpy; runpy.run_path("tools/jack")["push_read_gate"]("opening-c2a-prime-3-push", "C2a-prime")' && tools/jack decision grant "GitHub App renavondata-jack-court[bot]: the court's platform acts on renavondata/jack (opencode-runner #227), in force since 2026-11-04T05:40Z" && tools/jack decision fix "C2a: criterion 7 unmet at the stated end — nine off-log repair rows (acts-20261103T2144); the court's platform acts moved to a GitHub App (opencode-runner #227)" && git fetch origin && git -C ~/git/worktrees/jack/opening-c2a-prime-3-push merge --no-ff --no-edit origin/main -m "merge: main into the opening branch of C2a-prime, after the grant and the fix" -m "Proposer: guy guy-master" && tools/jack push opening-c2a-prime-3-push --opens C2a-prime --review ~/git/worktrees/jack/opening-c2a-prime-3-push/transcripts/REVIEW-C2a-prime-code.md || echo "Stopped. Send counsel everything printed above before pasting anything again."
```

**Notes on the paste.**
- The `grant` and the `fix` are the brief's, word for word; the `fix` is the ruling's Order 3 paste.
- The merge commit carries the sovereign's `Proposer:` trailer, because `jack push` refuses a commit without
  one.
- The local branch is named `opening-c2a-prime-3-push` so that it does not collide with a branch the runner
  has checked out.
- If it stops before the `grant`, nothing has been entered. If it stops between the `grant` and the `fix`, the
  `grant` stands alone: it records the App and moves nothing else. If it stops after the `fix`, the two
  `decision` entries stand and the push has not been made: by the brief's §Stop and report if, counsel is told
  before any other act. After the `fix` the push can still be refused at the merge, at the verb's own checks
  or because `main` moved under it.
- The paste makes a local branch and worktree, `opening-c2a-prime-3-push`, before it enters anything. If it
  stops at any later step they remain, and a second paste would stop at that step; counsel sends the line
  that removes them with whatever follows.

## 3. After the push

Counsel reads `python3 tools/status.py --subject C2a` on the new `main`. A rehearsal of 13 November on a copy
of the log (COUNSEL-OPEN row 62; simulated entries, so it tested the status tool and not the verbs) printed
what the brief predicts, and showed what follows.

- **The window line** reads from the push's `ts` to `2026-11-30T00:00:00Z`. Criteria 1 and 2 are met once the
  `tests` run at the push's commit is green.
- **The promotion cannot be immediate.** A3.4 reads `procedure 0 : object 0` and `STOP` until the stream's
  entries fall inside the new window. In the rehearsal, twenty hours of batches gave 80 : 240.
- **Expiries.** Five of counsel's forecasts expire at the opening, as Amendment 2 says (V0, V2, V3, RM-3, and
  V1 unless a resolver other than counsel has entered it). Four more expire at `2026-11-18T00:00:00Z` (X0, X2,
  X3 and X6, on C2b's exit, which will not exist by then), and N5 is due at 12:00Z that day. Each expiry
  multiplies continued liveness by about 0.77, and each clean batch by about 1.2; criterion 6 needs 20.
- **The acts evidence.** Counsel commits the raw and attributed tables of the window by a proposal (§The acts
  evidence), re-runs the attributed command once it has merged, and sends the promotion paste, which names
  the table:

  ```
  tools/jack decision promote C2a --acts transcripts/evidence/acts-c2a2-<end>.csv
  ```

  The verb refuses unless the status line reads `lawful` and the file is the one committed at `HEAD`
  (Amendment 7). Between the opening and that paste the sovereign does nothing on GitHub under his own
  login: any such act is a `repair` row, and one row ends the window (§Stop and report if).
- **What the table does not see.** The classifier lists the workflow runs created inside the interval it is
  given, so a re-run inside the window of a run created before the opening is not collected (found on 13
  November by a reader's trial; COUNSEL-OPEN row 65). The classifier may not change before the exit
  (§Refusal list). Before the promotion paste counsel also runs it from `2026-11-01T15:04:14Z` and reads the
  rows that fall inside the window; a `repair` row there goes to the sovereign before any promotion, and the
  C2a report prints both tables.
