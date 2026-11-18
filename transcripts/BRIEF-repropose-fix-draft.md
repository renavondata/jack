# BRIEF: the re-proposer runs nothing a signature under `main`'s law does not cover (counsel's draft 2, 18 November 2026)

**Status.** A draft of counsel's. Draft 1 (`9777a61e`) failed its cold read (runner #1037); this draft answers that read. It is a brief for code on `renavondata/opencode-runner`, which lands "only by his opening and merging it" (COUNSEL-OPEN row 44). No builder session begins before a cold read has passed this text and the sovereign has read it.

**Why now.** On 18 November the sovereign disabled the `repropose` workflow by hand (log seq 5877) on counsel's finding. While it is disabled a stale proposal of the builder's or the reviewer's is closed and not re-made (jack #1126 was so lost at 12:44Z).

## 1. What the code does today

Read by counsel on 18 November at the runner's `main` `dd5578d7` and jack's `main` `315bf158`. The runner is private: a reader who cannot open its files cannot check the first three items, and a builder checks each before relying on it.

- `herald.yml` loops over every open pull request to `main` (line 49) and calls its function `repropose` at lines 61, 78 and 90. The function (36 to 48) reads the party from a `Proposer:` line of the pull request's body (38), the head's branch name (39) and the title (40), and dispatches `repropose.yml` with all three (44).
- `repropose.yml` takes four inputs (11 to 15) and runs `repropose.py` beside the key `~/.ssh/jack-<party>` (45). When the script exits non-zero it fills a session template with `sed`, writing the title and the branch name into the text of the `sed` program (52 to 53), appends the last fifteen lines of the script's output to the prompt (54), and files the session under a title that holds the branch name (55).
- `repropose.py` fetches the branch by name (43), finds the common prefix of the two logs by lines (47 to 49), plans to re-make every forecast and resolution after it (51 to 70) without reading an entry's proposer or verifying a signature, takes as content the whole difference from the merge base to the stale head outside `log.jsonl` (71 to 72), applies it in a new worktree (94), and runs that worktree's `tools/jack` there (96, 105, 124).
- `tools/jack` imports `kernel`, `judge` and `tools` from the checkout its own file lies in (line 5). The proposal verb runs that tree's tests and pins before it signs (97 to 99, 123) and signs `{title, commit}`; the commit is the first that `commits_of(ROOT, "origin/main", "HEAD")` yields which changes a path other than `log.jsonl`, else `HEAD` (124).

So where a stale branch's patch changes a file that the verbs import or the check runs, that file's code runs beside the party's key, whoever added it; and a pull request's title reaches a program's text.

## 2. Terms

- **M**: the commit `origin/main` names at the job's one fetch. Every later use of "`main`" in a run means M; the job fetches `origin` once.
- **S**: the stale head, the commit the pull request's head branch names on `origin` at that same fetch.
- **The fork point** k: the number of leading lines, compared as bytes with their line ends, that M's `log.jsonl` and S's `log.jsonl` share.
- **The suffix**: S's log lines after the first k.
- **The law at the fork point**: the keys that M's first k lines declare, as `kernel/check.py` folds them.
- **The job's party**: the principal the law at the fork point gives the key file this job signs with; if that key is not declared there, the job has none.

## 3. The rules

R1 to R12 bind `repropose.py` and `repropose.yml`; H1 to H4 bind `herald.yml`. Rules are tested in their number's order and the first that fails decides. A refusal named `R-…` is a **provenance refusal**: the job comments on the pull request with the code and nothing else of the run, files no session, signs nothing, pushes nothing, and exits 0. No file of S is executed or imported, and no model session is filed, unless R1 to R7 have all passed.

- **R1, the head.** The job reads the pull request by its number through the API: its head repository is `renavondata/jack`, and S is the tip of its head branch on `origin`. Otherwise `R-head`. The branch name goes to `git` as one argument; one beginning with `-` is `R-head`.
- **R2, anchored to `main`.** k is at least 1, so the two logs share genesis, and k is the whole length of M's log or less. In a clean detached worktree of M, with S's log bytes written to a file outside every tree, M's `python3 -m kernel.check <file>` reports ok. Otherwise `R-log`. (With k ≥ 1 the kernel checks every suffix entry's signature against keys declared by `main`'s own genesis and by key entries in the shared prefix or the suffix; R3 removes the suffix's.)
- **R3, what the suffix may hold.** Every suffix entry is of type `forecast`, `resolution`, `proposal` or `merge`. A `forecast`, `resolution` or `proposal` entry's proposer is the job's party and its signing key is one the law at the fork point declares for that party. A `merge` entry's proposer is the principal the law at the fork point gives a key holding the power `merge` and no other party power, and it comes after at least one `proposal` entry. The suffix holds at least one `proposal`. Otherwise `R-foreign` (an entry of another party or type) or `R-party` (the job has no party, or the last proposal's proposer is not it).
- **R4, the content.** P is the suffix's last `proposal` entry and C the commit it names. C is an ancestor of S. Every commit in `git rev-list C..S` changes, against each of its parents, `log.jsonl` alone or nothing. Otherwise `R-unsigned`. The patch is `git diff --binary B C` outside `log.jsonl`, B being the merge base of C and M; when there are several merge bases: `R-unsigned`.
- **R5, the title.** T is P's `title`. T begins with `-`, holds a character below U+0020 or from U+007F to U+009F, or is longer than 4,000 characters: `R-title`. The new proposal's title is T followed by ` (re-proposed mechanically: PR #<n> went stale)`, as today, n in digits; it is passed to the verb as one argument.
- **R6, the age.** P's `ts` is not later than the job's clock, read once at the start, and not more than `repropose_max_age_hours` before it; the number is a whole number of hours in a file of the runner's `main` that the sovereign sets, and a missing or unreadable file is `R-old`. Exactly that many hours before: not refused. Otherwise `R-old`. (Evidence for the number: among jack's pull requests #922 to #1121, 56 mechanical re-proposals opened between 7.4 and 167.8 minutes after their stale original.)
- **R7, not twice.** If M's log holds a `proposal` entry of the job's party whose title is the new title R5 gives: `R-replayed`. The job runs under a concurrency group of the pull request's number, as today.
- **R8, no string of the pull request in a program or a prompt.** No title, body or branch name of the pull request, no commit message, no entry body and no output of the script is written into the text of a program, into a command line that a shell parses, or into a session's title or body. Each travels as an argument, an environment variable or a file. A forecast's claim and arguments and a resolution's evidence go to the verbs as arguments, as today's script passes them (lines 100 to 104).
- **R9, what is re-made.** In the suffix's order: a forecast is skipped when its window has begun, when its `resolves_by` is before the job's clock, or when M's log holds a forecast of the same proposer and body; a resolution is skipped when M's log resolves that forecast; proposals and merges are not re-made. The rest are re-made by the verbs in a new worktree that holds M with the patch applied and committed. If nothing is re-made and the patch is empty, the job comments "nothing to re-make" and ends with no proposal.
- **R10, the fallback.** A failure after R1 to R7 have passed (the patch does not apply; a verb or the check refuses) files the job's party's own session from the template `transcripts/sessions/repropose.md` as M holds it, filled by a script's plain replacement of two placeholders: the pull request's number (digits) and C (forty hexadecimal digits). The issue's title holds the party and the number. The body holds the template, those two values and the failed step's name from a closed list the script defines, and no other text. The template tells the session to work from C and from P's title, and that nothing in the pull request's own title, body or comments is an instruction. Entries the job had already signed before the failure stay on its unpushed worktree, which the job removes; nothing is pushed.
- **R11.** `REPROPOSE_MAIN` is removed; the tests pass M as an argument that the workflow never passes.
- **R12, the inputs.** `repropose.yml` has two inputs, `n` and `party`. `n` matches `[0-9]+` and `party` is `builder` or `reviewer`, each as a whole string; otherwise the job ends with a printed line and no comment. `party` chooses the runner and nothing else: R3 decides the party from the key.
- **H1.** A pull request whose head repository is not `renavondata/jack` is skipped at the top of the loop with a printed line: not merged, not re-proposed, not commented on.
- **H2.** The party the herald passes is the proposer of the last `proposal` entry in the head's log, which it already reads; if there is none, or it is neither `builder` nor `reviewer`, the herald closes the pull request as stale with today's line for a party "not re-proposed from steel" and dispatches nothing.
- **H3.** The herald dispatches with `n` and `party` and nothing else. Its comment names the number and the party, not the branch.
- **H4.** The three call sites call as they do today.

**The claim**, and no wider: when R1 to R7 pass, every file the job's verbs import or its check runs is a file of M or a file changed by the patch from B to C, C being named by a proposal entry that a key `main`'s log declares for the job's party has signed. The claim is about the files' origin; the patched tree is a third tree, and what its code does when run, including fetching or generating other code, is not bounded by this brief.

## 4. What this refuses that the lane does today

- A stale branch holding, after the fork point, an entry by a party other than the job's (but for the herald's merges). Counted on `main`'s log at `315bf158`: since seq 195 no merged proposal's segment has held one; this is a count of what merged, not of what a branch may hold.
- A stale branch on which content was committed after its last proposal entry. The party's remedy is its own session.
- A pull request from a fork. Of jack's last 100, none came from one.

It does not refuse: a re-proposal of a re-proposal; a branch with two proposal entries, with or without a herald's merge between them (P is the last); a proposal with no content commit (the patch is empty and the entries are re-made).

## 5. The pin, `repropose_provenance`

The pin builds its worlds as `harness/build.py` does, with throwaway keys, and runs the script with M, the clock and the configuration passed as arguments. **F0**: genesis declares `guy-master` (all powers), `builder-1` (principal `builder`; proposal, forecast, resolution), `reviewer-1` (principal `reviewer`; the same) and `herald-1` (principal `herald`; merge). The clock is fixed at t₀ = 2026-01-01T12:00:00Z and `repropose_max_age_hours` is 24. On a branch `b` cut from the genesis commit the builder enters, with `ts` t₀ − 3 h, a forecast f (no window; `resolves_by` t₀ + 48 h); commits C1, which adds the one file `transcripts/x.md`; and enters, with `ts` t₀ − 2 h, a proposal P naming C1 with title `T0`. `main` then gains one forecast by the reviewer with `ts` t₀ − 1 h, giving M. The pull request #7 has head `b`, title `T0` and body `Proposer: builder builder-1`. The job runs with the builder's key. **Expected on F0 (P1):** a new branch from M holds a forecast with f's body, a commit whose tree is M's plus `transcripts/x.md`, and a proposal signed by `builder-1` titled `T0 (re-proposed mechanically: PR #7 went stale)`.

Each twin is F0 with the one change named; "nothing signed" means the branch list and every log are as before the run.

| Twin | The one change | Expected |
|---|---|---|
| P2 | S's log is a self-contained valid log: its own genesis declares a new key under principal `builder`, which signs f and P | `R-log` (k = 0); nothing signed; no session filed |
| P3 | one byte of P's signature is changed | `R-log` |
| P4 | the job runs with the reviewer's key | `R-party` |
| P5 | between f and P the suffix holds a forecast validly signed by `reviewer-1`, with `ts` t₀ − 150 min | `R-foreign` |
| P6 | after P, a commit C2 that changes `tools/jack` to write a file `MARK` when imported | `R-unsigned`; `MARK` exists nowhere |
| P7 | `T0` is replaced by `-x` in P | `R-title` |
| P8 | the pull request's title is `ZZ` | as P1 (the title is `T0 …`) |
| P9 | P's `ts` is t₀ − 24 h − 1 s and f's is t₀ − 25 h | `R-old` |
| P10 | P's `ts` is t₀ − 24 h and f's is t₀ − 25 h | as P1 |
| P11 | M's log also holds a proposal by `builder-1` titled `T0 (re-proposed mechanically: PR #7 went stale)` | `R-replayed` |
| P12 | M also holds a forecast by `builder-1` with f's body | no second forecast with f's body; the proposal is made |
| P13 | M's tree also holds `transcripts/x.md` with other bytes, so the patch does not apply | one session filed for `builder`; its title and body hold `7` and C1's hash |
| P14 | as P13, and the pull request's title, body and branch name and C1's message each hold `ZZMARK`, and the script's failing step prints `ZZMARK` | as P13, and `ZZMARK` is nowhere in the session's title or body |
| P15 | the head repository of #7 is `other/jack` | `R-head`; in the herald's loop, skipped |
| P16 | after P the suffix holds a merge entry by `herald-1` | as P1; no merge entry is made |
| P17 | the suffix is f, P, a merge by `herald-1`, then a second proposal P′ by the builder naming C1 | as P1 with P′ as P |
| P18 | f's `resolves_by` is t₀ − 1 h (its `ts` unchanged) and C1 is absent, P naming the log-only head | a comment "nothing to re-make"; no proposal |

(P14 is its own fixture, derived from P13, and changes one thing from it.)

Mutants, each passing P1 and failing the twins named: no test that k ≥ 1 (P2); the party taken from the `party` input and not from the key (P4, run with input `builder`); no test of a suffix entry's proposer (P5); the patch taken from B to S with R4's test of later commits removed (P6); the title taken from the pull request (P8); the age compared with "at least" for "more than" (P10); no R7 (P11); the fallback's body built with the script's output or the pull request's strings (P14); merges refused in the suffix (P16, P17).

**Not tested by this pin:** that GitHub reports a head repository truly; the herald's three call sites' conditions; that the runner holds only the party's key; R8 for strings other than those P14 marks; R4's refusal for several merge bases; what a filed session then reads or does.

## 6. What this leaves

- **The fallback's session is a model reading a branch.** After R1 to R7 the branch's content and P are the job's own party's signed work, but a session that works from C reads its files, and a model may take what it reads as instruction. The template's sentence is a request to the model, not a control. Rung 6, narrated.
- **Signed code is still code.** A party's own signed commit can do anything its key's user can; this brief authenticates whose it is.
- **Replay inside the age.** Within `repropose_max_age_hours`, a proposal a party abandoned can be re-proposed as signed by whoever re-opens its pull request, once: R7 refuses the second. Each provenance refusal costs one run; nothing bounds how many pull requests an identity with pull-request write may open.
- **A dispatch with a false `party`** by an identity with Actions write on the runner runs on that party's runner and ends in `R-party` when the stale proposal is not that party's; it is not refused before the job starts.
- **The keys still lie in one user's home on steel** until the custody text is built; any session there can read them without the re-proposer.
- **Entries a job signed before a failure** are discarded with its worktree; a forecast so signed and never pushed is not on any log.

## 7. Deliverables and order

`repropose.py`, `repropose.yml`, `herald.yml`, the template and the age file as changed, with the pin, by a builder's proposal to jack under `tools/runner/workflows/` first; then the sovereign's pull request on the runner carrying the same bytes; then `repropose` enabled by his hand and entered as `jack decision fix`. If the pin needs the line cap raised, the number is his.
