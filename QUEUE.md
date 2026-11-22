# QUEUE.md: the queue to the bootstrap (a proto-procedure; it binds nothing until he adopts it)

- Built by the adviser session on 22 November 2026, at his word (see Words). It is not law. It grants nothing, relaxes no rule on `main` and touches no file on `main`. Where the law requires a read, a grant or a wait, the law stands.
- Everything below is computed by `queue_check.py`, beside this file, from `main`'s log and from git. Run it in any clone of `renavondata/jack`:
  ```sh
  git fetch -q origin adviser/notes && git show FETCH_HEAD:queue_check.py > /tmp/queue_check.py && python3 -I /tmp/queue_check.py
  ```

## The rules

1. **One step.** The queue is the record's own order (CHARTER §8; `transcripts/RESEARCH-meta-jack-20261107.md` §3.2), as listed below. The head is the first step whose check fails. Sessions work on the head and on nothing else. Any number of short sessions may serve the head, and a fresh session may replace a long one. Anything else a session notices gets one line under Later, and no draft.
2. **Frozen.** Three texts are frozen: the predicate, which is the eight rows B0 to B7 of that paper (predicate sha256 `5dab9b060e12a0eeb035bcb32704b6c74f7ab3d9149e19716e5466b1821967b8`); the checker (checker sha256 `76d7030e0ce4a78255c203c108aaaac2d57622e36b15ea44d9b79d0a2ed85f4c`); and this page above "## Words". They change only at a review or by his override. Either is his words, recorded verbatim under Words with the page's new hash. The checker counts his overrides and prints the count on every run.
3. **Budget.** Budget: drafts 4, cold reads 2, days 7. Everything is charged to the head.
   - A draft is a commit, since the head began, on a `counsel/` or `agent/` branch, that changes a `transcripts/*.md` file other than a review.
   - A cold read is a runner issue, since the head began, whose title begins `reader:`.
   - Days run from the entry that passed the step before, or from the first instant the law allows the step, if that is later. A step that ends in a promotion has no day budget: its window's stated end governs.
   - When a number is spent, the session at work stops and puts one choice to him: ship with the known defects listed, or cut the step down.
   - A step is done when its check passes. A read can inform that, and never decides it.
4. **Review.** Weekly, on Sundays; the first is on 29 November 2026. He reads the checker's output. Later is cut down to what he keeps. Any change to the frozen texts is made then.
5. **End.** This page lapses when the last step passes; or on 31 January 2027; or after 6 December 2026, if steps Q1 to Q4 have not all passed by then. On a lapse the checker says so, and what follows is his to decide.

## The queue

| Step | Passes when `main`'s log holds |
|---|---|
| Q1 | A6 in force: an `amend` with id `A6` |
| Q2 | C2a-prime ended: a `decision veto` naming it, at or above A6's `activate_at` |
| Q3 | the promotion evaluator moved: a `push` after that veto, with `judge/status.py` on `main` |
| Q4 | C2a-3 open: his `decision fix` of C2a-prime and then a `push`, both after 2026-11-30T00:00:00Z |
| Q5 | C2a promoted: `decision promote C2a` after that push |
| Q6, Q7 | C2b open (the next `push`), then promoted |
| Q8, Q9 | C2c-1 open, then promoted |
| Q10, Q11 | C2c-2 open, then promoted |
| Q12, Q13 | C2c-3 open, then promoted: bootstrapped, B0 to B7 hold |

Beside the queue, and not on it: the court's scheduled streams; and the runner's move off steel, which ends when the lane runs on the droplet.

## Words

Append only. His words, verbatim, one line each. The checker reads lines of the form `ADOPTED|REVIEW|OVERRIDE <instant> sha256 <this page's hash above "## Words"> — "his words"`; an override that changes no frozen text leaves the hash out.

BUILT 2026-11-22T09:00:00Z — to the adviser's "Shall I build it now, under those bounds?": "But if you think it's best you implement this, and ensure you keep it minimal etc, so be it"
ADOPTED 2026-11-22T09:06:41Z sha256 7ab37fc9f86eaddd0f96f724b61b86372d7f3d3469239fbae72c4153df1047fe — to the adviser's "Do you adopt QUEUE.md as it stands?": "Yes"
OVERRIDE 2026-11-22T09:20:47Z — to the adviser's "Shall I run that audit now?" (a fresh session of its own family, then one read by another family; off the head, so against rule 1): "Maybe one cold read too?"

## Later

Append only between reviews. One line each, and no draft.

- B8 and B9: his word of 22 November, "Add B8 and B9" (`CLERK.md` entry 20). They have no text on `main` yet.
- The signing of the brief-6 paper: `counsel/clerk` at `28f19a8a`; its cold read, runner #1197, passed.
- The seed lane (the research report's S5): for the first review.
- Hooks that hold sessions to the head: only if a review finds this page ignored.
- A defect in rule 1, found by the adviser on 22 November on rereading the source: `transcripts/PLAN-20261030.md` §3 has "The next layer's *pre-stated* deliverables are built during the current layer's window". Rule 1 forbids that. It first bites at Q5, after 2026-11-30T00:00:00Z. For the first review.
- An independent audit of this page and its checker: his question of 22 November, "The kernel underwent a lot of auditing before it was put into effect. Why not QUEUE.md, which you already changed once?"
