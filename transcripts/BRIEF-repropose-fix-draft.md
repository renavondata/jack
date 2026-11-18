# BRIEF: the re-proposer runs nothing a signature does not cover (counsel's draft 1, 18 November 2026)

**Status.** A draft of counsel's, unread. It is a brief for code on `renavondata/opencode-runner`, which lands "only by his opening and merging it" (COUNSEL-OPEN row 44). No builder session begins before a cold read has passed this text and the sovereign has read it.

**Why now.** On 18 November the sovereign disabled the `repropose` workflow by hand (log seq 5877) on counsel's finding (COUNSEL-OPEN row 75). While it is disabled a stale proposal of the builder's or the reviewer's is closed and not re-made. This brief is the fix after which it is enabled again.

## 1. What the code does today

Read by counsel on 18 November at the runner's `main` `dd5578d7` and jack's `main` `315bf158`; a builder checks each line before relying on it.

- `herald.yml` loops over every open pull request to `main` (line 49) and calls its function `repropose` at lines 61, 78 and 90. The function (36 to 48) reads the party from a `Proposer:` line of the pull request's body (38), the head's branch name (39) and the title (40), and dispatches `repropose.yml` with all three (44).
- `repropose.yml` takes four inputs (11 to 15) and runs `repropose.py` beside the key `~/.ssh/jack-<party>` (45). When the script exits non-zero it fills a session template with `sed`, writing the title and the branch name into the text of the `sed` program (52 to 53), appends the last fifteen lines of the script's output to the prompt (54), and files the session under a title that holds the branch name (55).
- `repropose.py` fetches the branch by name (43), finds the common prefix of the two logs by lines (47 to 49), plans to re-make every forecast and resolution after it (51 to 70) without reading an entry's proposer or verifying a signature, takes as content the whole difference from the merge base to the stale head outside `log.jsonl` (71 to 72), applies it in a new worktree, and runs that tree's `tools/jack` there (96, 105, 124).
- `tools/jack` imports `kernel`, `judge` and `tools` from the checkout its own file lies in (line 5), and the proposal verb runs that tree's tests and pins before it signs (97 to 99, 123). It signs `{title, commit}`, the commit being the branch's last commit that changes a path other than `log.jsonl` (121 to 127).

So a branch on `origin` that carries a party's valid stale log and one more commit has that commit's code run beside the party's key, and a pull request's title reaches a program's text.

## 2. The rules

R1 to R9 bind `repropose.py` and `repropose.yml`; H1 to H4 bind `herald.yml`. A refusal named `R-…` is a **provenance refusal**: the job comments on the pull request with the code and one sentence, files no session, signs nothing, and exits 0.

- **R1, the log first.** Before any file of the stale branch is executed or imported, the job makes a clean detached worktree of `origin/main`, writes the stale head's `log.jsonl` bytes to a file outside every tree, and runs `main`'s `python3 -m kernel.check <file>` in that worktree. Not ok: `R-log`.
- **R2, the party.** The party is the proposer of the last entry of type `proposal` after the fork point (R3). It must equal the principal that `main`'s log declares for the key in this job's home. Otherwise `R-party`. The workflow's `party` input only chooses the runner.
- **R3, the fork point and what may follow it.** The fork point is the longest common prefix of `main`'s log and the stale log, by lines. After it, every entry's proposer is the party, except entries of type `merge` by the herald's principal that come after the party's last proposal. Any other entry: `R-foreign`.
- **R4, the content.** C is the `commit` that last proposal entry names. C is an ancestor of the stale head, and every commit after C up to the head changes `log.jsonl` alone. Otherwise `R-unsigned`. The patch is the difference outside `log.jsonl` from the merge base of C and `origin/main` to C.
- **R5, the title.** The new proposal's title is that entry's `title` with one suffix naming the stale pull request's number in digits. It is passed as one argument. A title that begins with `-`, holds a control character, or is longer than 4,000 characters: `R-title`. No string of the pull request (title, body, branch name) is written into the text of a program, a command line a shell parses, or a prompt.
- **R6, what is re-made.** Today's three skips stay (a forecast whose window has begun; a forecast past its `resolves_by`; a resolution of a forecast `main` already resolves). Added: a forecast whose proposer and body `main`'s log already holds is not made again. An entry after the fork point of any type but `forecast`, `resolution`, `proposal` and `merge` takes the fallback of R8.
- **R7, the age.** The last proposal entry's `ts` is no older than `repropose_max_age_hours`, a number in the runner's configuration that the sovereign sets (counsel's evidence for it: among jack's pull requests #922 to #1121, 56 mechanical re-proposals opened between 7.4 and 167.8 minutes after their stale original). Older: `R-old`.
- **R8, the fallback.** Any failure that is not a provenance refusal (the patch does not apply; a verb refuses; the check fails) files the party's own session from the template with two values and no others: the pull request's number, matched against `[0-9]+`, and C, matched against forty hexadecimal digits. The template is filled by plain replacement of each placeholder in a script, not by `sed`. The template tells the session to work from C and to take the title from the signed entry. The session's body holds, beside the template, the name of the step that failed from a closed list the script defines, and none of the script's output; the issue's title holds the party and the number and no branch name.
- **R9, the head.** The job reads the pull request by its number through the API. Its head repository is `renavondata/jack` and its head commit is the tip of its head branch on `origin` at the job's fetch. Otherwise `R-head`. The branch name is passed to `git` as an argument; one that begins with `-` is `R-head`.
- **R10.** `REPROPOSE_MAIN` (line 25 today) is removed; the tests pass their `main` as an argument.
- **H1.** A pull request whose head repository is not `renavondata/jack` is skipped at the top of the loop with a printed line: not merged, not re-proposed, not commented on.
- **H2.** The party the herald passes is the proposer of the last `proposal` entry in the head's log, which it already reads; never the body.
- **H3.** The herald dispatches with `n` and `party` and nothing else; `repropose.yml` has those two inputs. Its comment on the stale pull request names the number and the party, not the branch.
- **H4.** The three call sites call as they do today.

**The claim these make**, and no wider: after R1 to R4, the code that runs beside a party's key in a re-proposal is `main`'s plus the tree of a commit that a signed proposal entry of that same party names.

## 3. The pin, `repropose_provenance`

Fixtures are built by the pin in a temporary repository with throwaway keys, as `harness/build.py` builds its worlds. **F0**, the base: `main` M0 with keys for `builder` and `reviewer` and the herald; a branch `b` cut from M0 on which the builder has entered one forecast f (window not begun, `resolves_by` ahead), committed content commit C1 (one file under `transcripts/`), and entered a proposal naming C1 with title T; then `main` gains one entry by the reviewer (M1), so `b` is stale. Run on F0 as the builder: a new branch holds a forecast with f's body, a commit whose tree is M1's plus C1's file, and a proposal entry signed by the builder whose title is T plus the suffix. Each twin is F0 with the one change named.

| Twin | Change | Expected |
|---|---|---|
| P1 | none | re-proposed as above (the positive case) |
| P2 | the stale log's last line has one byte of its signature changed | `R-log`; nothing signed |
| P3 | the job runs with the reviewer's key | `R-party` |
| P4 | after f, an entry by the reviewer, validly signed, is on `b`'s log | `R-foreign` |
| P5 | a commit C2 changing `tools/jack` is added to `b` after the proposal entry | `R-unsigned`; a marker file that C2's `tools/jack` would write is absent |
| P6 | the proposal's title T begins with `-` | `R-title` |
| P7 | the pull request's title (not the entry's) is `X` | the new proposal's title is T plus the suffix, not `X` |
| P8 | `main` M1 already holds a forecast by the builder with f's body | no second such forecast is made; the proposal is made |
| P9 | the proposal entry's `ts` is `repropose_max_age_hours` plus one second before the run | `R-old` |
| P10 | the same, exactly `repropose_max_age_hours` before | re-proposed |
| P11 | C1's patch does not apply on M1, and the pull request's title, body and branch name each hold the marker `ZZMARK` | the fallback: one session filed whose title and body hold the number and C1's hash and nowhere `ZZMARK` |
| P12 | the pull request's head repository is another | `R-head`; and in the herald's script, skipped (H1) |
| P13 | after the proposal, a `merge` entry by the herald is on `b`'s log | re-proposed; the merge entry is not re-made |
| P14 | the herald's `party` input names the reviewer | `R-party` |

Mutants, each with the twins that must fail under it while P1 passes: one that skips R1 (P2); one that takes the party from the input (P3, P14); one that omits R3's test (P4); one that diffs to the stale head, as today (P5); one that takes the title from the pull request (P7); one that puts the pull request's title, its branch name or the script's output into the session (P11); one that compares the age with "older than or equal" (P10).

**Not tested by this pin:** that GitHub reports a pull request's head repository truly; that the runner on which the job runs holds only the party's key (the custody text's); the herald's three call sites' conditions (unchanged).

## 4. What this leaves

- A stale head of a party's, already re-proposed and not yet merged, can be re-proposed a second time by whoever re-opens it: one wasted run and its tests, no signature misused.
- Inside `repropose_max_age_hours`, a proposal a party abandoned can be re-proposed as the party signed it by whoever re-opens it.
- The keys still lie in one user's home on steel until the custody text is built; this brief does not change who can read them.
- An identity with Actions write on the runner can dispatch `repropose.yml` with any `n` and `party`; under R2 and R9 a false one ends in a refusal.

## 5. Deliverables and order

`repropose.py`, `repropose.yml`, `herald.yml` and the template `transcripts/sessions/repropose.md` as changed; the pin; their copies under `tools/runner/workflows/` on jack by a builder's proposal first, then the sovereign's pull request on the runner carrying the same bytes, then `repropose` enabled by his hand and entered as `jack decision fix`. A line cap, if the pin needs one raised, is his number.
