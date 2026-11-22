# The clerk acts: the lane under the law (counsel's research paper, draft v4, 22 November 2026)

Written by a counsel session (`claude-opus-5-5`, `session_01VpB3TmrXo8QB1Qa3EdgZSU`) to the Project brief `claude/session-briefs/06-the-clerk-acts.md` (revision 2). It was carried out on the sovereign's word "Sure" of 21 November to the brief's author, and his "Yes" of 22 November, in this session's chat, to go on drafting after finding S1.

**It binds nothing.** It is offered in the form of `transcripts/RESEARCH-meta-jack-20261107.md`, as an input to C2c-2's brief, but it has none of that note's acceptance by him. C2c-2's brief is not on `main`; a partial draft, v8, is on `counsel/c2c-2-spec-v4`. Where this paper and the record differ, the record governs.

**Draft v4.** Two fresh pre-reads of counsel's own family and one cold read of another family (runner #1194, sol, on v3) have read it. #1194 gave `VERDICT: FAIL` with three BLOCKs, all on B9. V4 states that B9 cannot be made decidable on any text that exists today (§4), and answers #1194's FIXes.
- **v1's read** found three BLOCKs: custody v2 had been read and failed (runner #1032), which v1 missed; the herald did not close #1112; and B8 and B9 were not decidable.
- **v2's read** found two: B9's first clause was circular, and C2c-1's brief §9 pre-states C2c-3's claim as B0–B7, which v2 did not disclose.

V3 withdrew B8 and B9 to their minimum and disclosed §9 (§5.3, §8).

**What was read, at which commits:**
- jack `main` at `226355d3`;
- `renavondata/opencode-runner` `main` at `dd5578d7`, every tracked file whole;
- `counsel/c2c-2-spec-v4` at `59b0b021`, for `transcripts/DRAFT-custody.md` v2 and `BRIEF-C2c-2-draft.md` v8;
- runner issues #188, #1011 and #1032 (the reports, each the issue's last comment);
- CHARTER, SPEC and RUNBOOK in the sections the brief lists, whole.

Other texts are cited by the line read. Three sources are off `main`:
- `CLERK.md`, on the orphan branch `adviser/notes`;
- the Project docs, cited by path (`claude/plan-20261111-to-bootstrap.md`, "the worklist"; `claude/jack-situation-and-impasse-20261119.md`, "the situation paper"; `claude/session-briefs/00-common.md`);
- his words in chat, quoted as given.

Every figure carries the command that gives it.

**Interest.** Counsel's own key (`~/.ssh/jack-counsel-3`) and token sit on steel with every other party's (`transcripts/runner/host.md` §6). B9 would bind counsel's custody. Counsel's forecasts on the windows gain from fewer lost windows. This session holds no forecast of its own.

## 0. In six lines

1. On this paper's reading, the lane is the charter's clerk, the part that acts. Of its six workflows, two (the courier's) have a text on `main`. The other four, the scripts and the timers have no job text in README's four parts; `host.md` §2–3 and RUNBOOK's `jack key` govern parts of them. The enforcement map records the lane as one row, `runner: hand: sessions`, with no deadline.
2. C2c-1's ratchet moves that one row to `code` on the courier alone, and its pin's twin 10 ignores a workflow with no shell. So at C2c-1's exit the map reads `code` for a lane four of whose six jobs are still hand. BRIEF-C2c-1's own sentence that they stay as dated hand rows then has no row to point at.
3. Every job can read every party key and act as `gfrmin` (#188, known). **S1:** every job can also read the file of the sovereign's master key, by his answer of 22 November. No text on `main` says so, though he had told counsel-5 on 18 November that it lies in "g's home on steel" (Project doc `claude/counsel-5-state-20261118.md`). Custody v2 moves every job off `g` and checks that the copies left there are unreadable to its users. It states and checks nothing of the master key's file.
4. Custody v2 answers #1011's deputy, and was itself read and failed (#1032). Its gravest finding is a second deputy: the re-proposer runs code from a branch a session can write under the party's key. That is true of the re-proposer today too.
5. The race with a moving `main` is the root of the re-proposer and the herald's stale-closes, and of the re-proposal branches on jack (411 branch heads have names ending in `-r`; the count is by name, not cause). The verbs' retry (C2c-1 Amendment 3) does not reach it: it binds main verbs and excludes branch verbs.
6. One predicate row can be written in the form of B0–B7, decidable given one list a brief would write: B8 (the clerk acts). B9 (the parties' keys are separated) cannot be made decidable on any text that exists today, and the paper says what a custody text must define first (§4). Adding them changes the roadmap, which is his to decide. It also meets a pre-statement in C2c-1's merged brief (§9: C2c-3's claim is "B0–B7"), which is disclosed in §5.3.

## 1. Inventory

Each job is given: trigger; identity; keys and tokens it can read by path; what it does, in order; the jack text it is written to; its enforcement-map row; incidents. "Every job can read" means every file in `g`'s home, as user `g` (row 1).

```sh
# run from the directory that holds both clones, jack/ and opencode-runner/
git -C opencode-runner rev-parse --short HEAD          # dd5578d
git -C opencode-runner ls-files | wc -l                # 15
wc -l opencode-runner/.github/workflows/*.yml opencode-runner/.github/scripts/*
# counsel-sign.yml 29, counsel.yml 27, diary.yml 113, herald.yml 92, repropose.yml 56, run.yml 98,
# counsel-act.py 168, counsel-sign.py 326, gh-as-app 21, repropose.py 135, test-worktree-cleanup.sh 87, worktree-cleanup.sh 72
```

The fifteen tracked files are these twelve, the two `host/` drop-ins, and `.gitignore` (`__pycache__/`). The brief's list omits `gh-as-app` and `test-worktree-cleanup.sh`.

### Row 1 — runner issue #188: the host (open since 2026-11-03T12:36:47Z)

- **Fact:** all three runners run as `g`. Its `gh` login is `gfrmin`, with scopes `admin:org`, `repo` and `workflow`. Its home holds "ssh keys, keyrings and so on", and "Any step of any job on these runners can read all of it" (#188's body).
- **Push to `main`:** `main`'s protection requires `judge` and `tests` and exempts administrators, so a job acting as `gfrmin` can push `main`. That route is named by #188 ("can push to every repo") and by `host.md` line 9 ("administrators exempt").
- **His acts:** he read `host.md` v14 on 8–9 November. It is not installed (worklist §4 row 15).
- **Map row:** none. The courier text says "no row names the host" (`counsel-courier.md` §Custody).

```sh
gh api repos/renavondata/opencode-runner/issues/188 --jq .state                        # open
gh api repos/renavondata/jack/branches/main/protection --jq '.enforce_admins.enabled'   # false
```

### Row 2 — S1: the sovereign's master key, readable by every job

- **Where he works:** his pastes run on steel ("the machine that holds the sovereign's key", `transcripts/PUSH-c2a-prime-opening.md` line 65), in `~/git/jack-guy`, beside the runner's `~/git/jack`, which is `/home/g`'s (`host.md` §2's default `--old-home`).
- **Which key signs:** no paste on `main` names a key, so the verbs use `$JACK_KEY` if his shell sets it, else `~/.ssh/id_ed25519` (`tools/jack` line 314; RUNBOOK §Common, "Key and party"). The texts do not say which; his answer settles that the key is reachable on steel, not its file name.
- **His answer:** by his answer to the adviser of 22 November (`CLERK.md` entry 7), the key is on steel where the jobs can reach it.
- **Limits:** it asks for a passphrase (RUNBOOK line 29). Whether an `ssh-agent` under `g` holds it unlocked was asked in `CLERK.md` entry 6. His paste of 22 November (entry 9) showed two agent sockets under `g`, `gcr/ssh` and `gnupg/S.gpg-agent.ssh`, each holding no key at that moment.
- **What the texts say:** none on `main` names S1. Off `main`, counsel-5's state note of 18 November records his answer "g's home on steel" and his "Password added...". `host.md` line 3 names "every party key". Its "the runner holds no key of his" (line 9) is of the state after the install.
- **What custody v2 does:** it moves every job to six new users. `finish` "checks that every copy left there is unreadable to the six users" (v2 §4). It makes no statement of the master key's file and no check of it, and it says it "does not bind the owner".
- **Map row:** none.
- **The stop:** this is the brief's stop condition, reported on 21 November before drafting (`CLERK.md` entry 5), with the cost under B5 of a hand fix: an act off GitHub, outside every instrument; as a `decision fix` naming no failed window, a repair and a late report. This paper recommends no fix.

```sh
git grep -n -E 'JACK_KEY|--key' origin/main -- 'transcripts/PUSH-*.md'   # no output
sed -n 314p tools/jack | grep -c 'id_ed25519'                             # 1
```

### Row 3 — `herald.yml` (92 lines)

**Trigger.** The workflow's `schedule: */10 * * * *` (line 10), and dispatches by the user unit `herald-tick` on steel.
- The unit's drop-in (`host/herald-tick.service.d/app.conf`) calls `~/.config/jack/gh-as-app-timer`, and falls back to `gh workflow run herald` under the owner's login.
- The record states a cadence: "the herald fetches and pulls every two minutes" (`PUSH-c2a-prime-opening.md` line 66), against the workflow's own `*/10` (line 10). The record does not reconcile the two. The runs show a dispatch every two minutes on 22 November (`gh api 'repos/renavondata/opencode-runner/actions/runs?per_page=15'`). His paste in `CLERK.md` entry 9 names the units: `herald-tick.timer` and `jack-diary.timer` (user units of `g`), and the three runner services as system units.
- The unit and timer files and the bytes of `gh-as-app-timer` are in neither repository.

**Identity.** The jack-court App when its files exist (lines 29–31), else "owner login". The wrapper `gh-as-app` is fetched from the runner's own repository at `$GITHUB_SHA`.

**Keys and tokens.** `~/.ssh/jack-herald` (`herald-2`, {merge}); the App's private key; row 1.

**What it does, in order.**
1. Exits if the key is absent (line 26).
2. Sweeps `/tmp` and pulls `~/git/jack` `main`.
3. For each open pull request, oldest first, reads the head's last log entry. It skips drafts (line 53).
4. If that entry is a `merge`: completes GitHub's merge on green, or calls `repropose()` if the head's log is no longer a byte-prefix extension of `main`'s.
5. If it is a `proposal` whose log is no longer such an extension: calls `repropose()`.
6. Otherwise, on `judge` and `tests` green: runs `JACK_KEY=~/.ssh/jack-herald tools/jack merge N`. On `CONFLICTING` it calls `repropose()`.

**`repropose()`** (lines 36–48) reads the party from the pull request's body (`sed -n 's/^Proposer: …/'`, line 38), and the branch and title from the pull request (lines 39–40).
- Only for `builder` or `reviewer` does it comment, close and dispatch `repropose.yml`.
- For any other party it prints and does nothing.

**Text and map row.** No four-part job text; `host.md` §3 governs its identity fallback. RUNBOOK's `jack key` and `jack merge` describe the key and the verb, not the job. Map row `W3` witnesses merges after the fact; the job is under `runner: hand: sessions`.

**Incidents.**
- C2a-prime died when the herald merged a branch cut before the opening (COUNSEL-OPEN row 69).
- It sat on #229 and #231 for hours (its own comment, lines 55–59).
- On 18 November a re-proposal it dispatched held counsel's sign job queued, and counsel then closed #1112 itself through the courier (row 74).

### Row 4 — `repropose.yml` (56) with `repropose.py` (135)

**Trigger.** A dispatch by the herald, with inputs `n`, `branch`, `party` and `title`, all from the stale pull request.

**Identity.** The App, else owner login (lines 38–41).

**Keys.** `JACK_KEY="$HOME/.ssh/jack-$PARTY"` (line 45), with `PARTY` limited to builder or reviewer (line 35); row 1.

**What it does, in order.**
1. Checks out the runner repository.
2. Runs `repropose.py` from that checkout.
3. The script applies the stale branch's non-log diff as a commit (lines 93–95), then runs `tools/jack` **from that patched worktree** (lines 96 and 105). Under the party's key it re-enters each forecast and resolution, then proposes (line 124).
4. On any non-zero exit (lines 48–50) it fills `transcripts/sessions/repropose.md` with `sed`, putting `$BRANCH` and `$TITLE` into the `sed` program's text (`s/{BRANCH}/$BRANCH/g` and `s|{TITLE}|$TITLE|g`, line 53), and files a model session under that party's key (line 55).

**Text and map row.** `transcripts/sessions/repropose.md` is the fallback's prompt; the job has no text. It is under `runner: hand: sessions`.

**Incidents.**
- The exposure of 18 November and his three `decision fix` entries, seq 5877, 5878 and 5936. Two of the three are acts on the lane; 5878 is a setting on jack (situation paper, Appendix A).
- Content-only proposals were dropped until 8 November (runner #410).
- Six resolutions were skipped as forecasts on 3 November (the workflow's comment).
- Counsel's reviewer-keyed re-proposals of 8 November (row 46).
- The fix brief that cannot land (`counsel/repropose-fix-brief`; situation paper §5.5).
- #1032 F5 (row 9).

### Row 5 — `diary.yml` (113, of which 46 lines are inline Python)

**Trigger.** Dispatch only, by the user unit `jack-diary` "at ten past every hour and twenty past every third hour" (line 1), through `gh-as-app-timer`, falling back to the owner's login (`host/jack-diary.service.d/app.conf`).

**Identity.** The App, else owner login.

**Keys.** It signs with none. It chooses each session's key through the template's `key: ~/.ssh/jack-{PARTY}` line (`due-resolve.md`) or the fixed `key: ~/.ssh/jack-reviewer` (`stream-forecast.md`). Row 1.

**What it does, in order.**
1. Takes the role from the run's `createdAt` minute (lines 42–43).
2. Before :15: computes the due list from `origin/main`'s log and the clock (lines 51–96), and files one `run` issue per party (lines 100–104).
3. Otherwise: files the reviewer's stream session (lines 106–112).

Two inputs come from issues, not from the log:
- the "handed" set, from the `due-seqs:` lines of issues titled `resolve the writs due` (lines 49 and 59–64);
- the stream number N, from issue titles (lines 106–108).

**Text and map row.** The two templates are prompts. The computation has no text; its rules are its comments. It is under `runner: hand: sessions`.

**Incidents.** Four forecasts expired on 3 November (lines 8–14). The owner's login died from 10:15Z to 13:06Z on 13 November and stopped the lane (the drop-ins' comment).

### Row 6 — `run.yml` (98): the session runner

**Trigger.** `issues: labeled` with `run` (lines 13–14, 23). The lane comes from the `build` label (line 28).

**Identity.** The job token (`issues: write`) for the issue steps; for the session, the App, else owner login. The job token is also written into the text of the session's own step, for fetching the wrapper (custody v2 §2, "The job's own token").

**Keys.** `JACK_KEY` comes from the body's `key:` line, read when the job starts (lines 39, 41 and 44, as custody v2 cites them). The model keys come from the runner's `.env`. Row 1.

**What it does, in order.**
1. Reads the body.
2. Takes `model:`, `key:` and `branch:` from its first four lines.
3. Posts `started:`.
4. Cuts a worktree from `origin/main`.
5. Runs `opencode run`.
6. Posts the transcript tail, relabels `done`, closes the issue, and sweeps `done` issues.
7. Removes the worktree with `worktree-cleanup.sh`, fetched from the runner at `$GITHUB_SHA`.

**Text and map row.** None for the job. It is under `runner: hand: sessions`.

**Incidents.**
- #188.
- #1011's deputy (row 9).
- `/tmp` out of inodes on 2 November.
- 449 worktrees and about 60G left behind "until 11 Nov" (its comment).
- The job token shadowing the owner's login (run 41060460243).

### Row 7 — the courier

The courier is `counsel.yml` (27) with `counsel-act.py` (168), and `counsel-sign.yml` (29) with `counsel-sign.py` (326).

**Trigger.** A push to `counsel-requests`.

**Identity.** `assize-reviewer`'s token (the grant of seq 2131); the job token for reads.

**Keys.** `~/.ssh/jack-counsel-3` (sign job); counsel's token; row 1.

**Order and text.** As `transcripts/runner/counsel-courier.md` states (C2c-1's).

**Map row.** `runner`, which moves to `code` in C2c-1 (R7).

**Where the scripts come from.** Both workflows fetch their scripts from the runner's own `main` (`counsel.yml` lines 25–26, `counsel-sign.yml` 27–28), not from jack's. That is C2c-1's change to make.

**A difference between text and script.** The courier text says that, from `host.md` §3, a body counsel wrote "may carry no `key:` line at all". `counsel-act.py` at `dd5578d` refuses only a line naming `jack-builder` (line 114). The text calls any such difference "a finding against the scripts".

**Incidents.** #335 and #369 installed by his merges (row 46, the courier lapse); #1112 (row 74).

### Row 8 — the helper scripts

`worktree-cleanup.sh` (72) and `gh-as-app` (21) are fetched by the workflows from the runner at `$GITHUB_SHA`. `gh-as-app` mints an installation token naming no permission or repository (line 18), so the token carries the App's whole grant. `test-worktree-cleanup.sh` (87) is fetched by nothing: it is the cleanup script's test. None of the three has a text; they fall under `runner`.

### Row 9 — the deputies

**#1011's.** Any identity that can file and label a runner issue can start a session under any key `run.yml` will read. That includes every session, through the App. The job token in the session's step cannot start one: an issue or label it makes "raises no `labeled` event" (`diary.yml` lines 16–17). It could edit the body of an issue already labelled, before that issue's job starts. Nothing on `main` answers either route.

**#1032 F5.** This one is against custody v2 and true of today's code too. A session pushes a branch that keeps a stale proposal's valid log and adds a content commit changing `tools/jack`, then opens a pull request. The herald dispatches a re-proposal for the log's party, and `repropose.py` runs the patched `tools/jack` under that party's key (row 4, step 3). #1032: "Additional identities, files or permissions held by the attacking session: none."

### Row 10 — substrate, named and not legislated

GitHub (Actions, the API, branch protection, the organisation and its plan); steel's operating system and root; the runner binary and its registration; systemd, the three runner service units and their drop-ins (the memory drop-in of 8 November on `steel-opencode-2`'s, `host.md` line 22) and the two user timers; the model providers.

Three things the texts name sit beside these:
- the runner's `.env` with the model keys, which every session reads;
- `actions/checkout@v4`, a third party's action at a mutable tag, run by `repropose.yml` (line 31) on a keyed runner;
- prospective machinery the texts name and that does not yet exist: the monitor's `publish.yml` (in jack) and `verify.yml` (to be installed in this repository on GitHub's runners, `monitor.md`); `host.md`'s `install.sh` and `check.sh`; custody v2's installer, `check.sh`, `witness.yml` and a third daily timer. B8.1 would ask for a shell for each workflow once it is on the runner's `main`.

What the record can see of it: GitHub's run objects (`path`, `head_sha`, `event`, `runner_name`) through the API, and of steel only what a job prints.

```sh
gh api repos/renavondata/opencode-runner/actions/workflows --jq '.workflows[] | .path+" "+.state'   # six, all active
```

**The stop condition.** It was applied before drafting. #188 is known and is not a stop. S1 fired the condition and was reported on 21 November; he answered on the fact (`CLERK.md` entry 7) and said "Yes" to drafting.

Nothing else the inventory found is in the condition's three kinds without being named:
- the pushes to `main` in row 1 and the herald's merge;
- commits on steel under his git name (custody v2 §4 cites jack #1116; `CLERK.md` entry 6 cites `7b03d75d`);
- the drop-ins' fallback to his login, named in the drop-ins themselves.

#1032 F5 lets a session sign as another party. It is not one of the three kinds, and under #188 any job can already read any key, so it is a finding of this paper and not a stop.

## 2. Dispositions

The three dispositions are the brief's. The precedent for "clerk code" is the courier: a shell in the runner, byte-equal to `tools/runner/workflows/<job>.yml`, fetches `tools/runner/<job>.py` from jack's `main`, and the job is written to a four-part text under `transcripts/runner/` (README). Its witness is a KILLED pin plus byte-equality. The dispositions below are the paper's reading.

| Job | Disposition | Precedent or change | The test that would witness it |
|---|---|---|---|
| herald, merge path | clerk code | the courier; RUNBOOK `jack merge`: "When the clerk holds `merge`, this verb is unchanged" | a pin that it merges only a head whose last entry is a `proposal` by a declared key, with green checks; byte-equality |
| herald, stale-close and dispatch | clerk code under route 6(a); gone under 6(b) | the charter's ladder, "re-invite" (§5) | a pin that the party is read from the head's log (custody v2 §2), not the pull request |
| re-proposer | clerk code under 6(a); gone under 6(b) | custody v2 §2–3; pin `repropose_party`; and, for #1032 F5, a rule that no keyed job runs code a session wrote (K6, §3.3) | `repropose_party` extended to F5's case, KILLED; byte-equality |
| re-proposer's model fallback | under 6(a), a writ in place of a keyed model session (§6) | the ladder: "re-invite on another runner or model; writ to Guy" | a pin that a refusal files a writ and no keyed session |
| diary | clerk code | the courier. The due list is already code (`diary.yml` lines 51–96); its rules are in comments, not in a text | a pin that the due list and the handed set are a function of `origin/main`'s log and the clock alone |
| session runner | clerk code | custody v2 §2's `admit` / `session` / `post` split; pins `admit_tests`, `workflow_rules` | those pins KILLED |
| courier | clerk code | C2c-1 (R7) | `courier_signs_only_the_request`; criterion 8 |
| `worktree-cleanup.sh`, `gh-as-app` | clerk code (scripts a shell fetches); the test moves into `tests/` | the courier's scripts | its test; byte-equality |
| the timers, their drop-ins, `gh-as-app-timer` | substrate; the drop-ins' bytes held as shells | custody v2 §3's last row | byte-equality of the drop-ins; when they fire is not visible to the record |
| the quiet-minute waits in his pastes | deleted, by a change already agreed | the verbs' retry (worklist row 27; BRIEF-C2c-1 Amendment 3) | Amendment 3's pin |

No job is deleted on today's law alone. Amendment 3: "A party's branch verbs are outside it."

## 3. The clerk's identity and the parties' keys

### 3.1 "Change power" (the paper's reading of four texts)

- **CHARTER §3:** "A rule enters or leaves only by a change entry signed by a key holding the change power (at genesis, Guy's alone)".
- **§5:** the master key holds "change power; capability grants for money, releases and new keys".
- **SPEC §10.1:** the trusted base changes "only by Guy's `jack push`".
- **RUNBOOK:** of `merge`, nothing it does "reaches `main` except through the judge" (§Common to every verb); and "When the clerk holds `merge`, this verb is unchanged" (§`jack merge`).

Read together, change power is the power over the law, the trusted base and the keys: `amend`, `push`, `key` and the sovereign's `decision`s. A merge applies what the judge admitted and changes no rule, so a clerk can hold `merge` and "no change power". No text says this in one sentence. C2c-2's brief would have to state it before giving the clerk a key.

### 3.2 The acting clerk's principal (the paper's reading)

**Precedent.** `herald-2` (principal `herald`, {merge}, seq 201). From the window that first runs rounds it signs invites: "Only `--invite` signs, with the key file it is given: the herald's" (RUNBOOK `jack elect`). That needs a power C2b withholds ("`herald-2` holds no `forecast` power").

**Reading.** The acting clerk is the `herald` principal. Its powers grow only by his `key` entries, which are capability grants (§7). It holds none of `amend`, `push`, `key` or `decision`. Custody v2 gives it the filer App, on users where no model session runs.

### 3.3 The keys: #1011, custody v2 and #1032

| Finding | Custody v2 (59b0b021) | #1032 on v2 |
|---|---|---|
| #1011 2(i): shared App credentials file a keyed session | separate Apps; no session identity files, labels or edits a runner issue; `admit.py`'s four tests | "Answered for that route" |
| #1011 1: re-proposer's placement; five parties against three groups; the diary | the party's user; three session parties; `jack-diary` | answered |
| #1011 2(iii): execution-time body | the body rule: the event's body, hashed | "Partly answered" |
| #1011 2(ii): pushed workflows | left, detected by W3/W4 (rung 4) | "Left with a reason" |
| #1011 3: the witness | W1–W5 with stated intervals | F8 BLOCK: "all five can record no breach while a session signs as another party" |
| #1011 4: "repairs, no entries" | `decision fix` for v2 §5's rows 4–6 | answered |
| — | — | **F5/F14 BLOCK: the re-proposer runs branch code under the party's key** (row 9) |
| — | v2 §6 lists leftover `g` processes and `/home/g` copies at rung 6 | F6 BLOCK: against v2's claim to close both routes "for every session" |
| — | its four pins | F11 BLOCK: several rules have no twin and no "Not tested" entry |

```sh
gh api repos/renavondata/opencode-runner/issues/1032 --jq .title                                # reader: cold read of the custody text, draft v2 …
gh api repos/renavondata/opencode-runner/issues/1032/comments --jq '.[-1].body' | grep 'VERDICT:' | tail -1   # VERDICT: FAIL
git grep -c 1032 origin/main -- transcripts/COUNSEL-OPEN.md                                       # no output, exit 1: not yet on the record
```

S1 is in none of the three reads.

**What the paper needs from a custody text.** These are requirements for B9, not the install:

- **K1:** every key with powers on the log that a lane job uses is named under exactly one user in `custody.json`.
- **K2:** no job's key, model, branch or party is read from text a session can write. The party comes from a filer's label or the signed log.
- **K3:** no identity a session holds can file, label or edit a runner issue, dispatch a workflow, or write a file on the runner.
- **K4:** `custody.json` names, as data, the paths of secrets outside its users' homes that the lane must not reach. The sovereign's master key file is one of them, and its path is his to state. W1 tests each path unreadable from every session user.
- **K5:** the interval observations (W3, W4) are contiguous from the later of T_c and the window's opening. The snapshot observations (W1, W2, W5) are made at least once a day.
- **K6:** no keyed job runs code that a principal other than its own could have written since `main`. For the re-proposer: `tools/jack` and the tests are run from `origin/main`, not from the stale branch's tree. #1032 F5 is the case.

### 3.4 The session runner and `counsel-act.py`'s refusal

**Today.** `run.yml` "exports whatever `key:` an issue body names" (`host.md` line 3). `counsel-act.py` refuses a body counsel wrote that names `jack-builder` (line 114). That closes counsel's raw-form request with the builder's key.

**It does not close:**
- a raw body naming any other key, which the courier text already forbids and the script lags (row 7);
- an issue filed by another identity (the App, the owner);
- an edit of an issue's body by the job token in a session's step, before that issue's job starts;
- an edit of the body before the job starts;
- reading any key by path (row 1).

`host.md` says the same: "the courier's refusal in §3 is a courtesy to the record, not a bound" (line 3).

## 4. Two predicate rows in B0–B7's form, at their minimum

Each row is a *test* decidable from `log.jsonl`, the tree and evidence files the record already defines, and a *residue*.

**Reads so far.** Draft v1 wrote both rows with clauses no evidence decides. Draft v2 wrote them over evidence it invented, and a pre-read found B9 circular. Draft v3 wrote them at their minimum, and the cold read #1194 found B9 still undecidable: custody v2's `party_key` is a file name, not a log `key_id` (F1, F12), and custody's witness is an observed operation, not a pin (F13). By 00-common rule 4 a clause that fails twice is withdrawn to its minimum and not patched again. B9 has failed three times, so it is withdrawn below to what can be said. B8's comparisons #1194 found decidable, conditional on its new list (F11).

### B8 The clerk acts

*Evidence:* the runner evidence as C2c-1's window file defines it (`transcripts/evidence/runner-<stamp>.json`, one `{workflow, sha256}` per file under `.github/workflows/` of the runner's `main`). The test also needs the bootstrap window's file to list `lane_rows`, the enforcement-map rows that are the lane's, by name. That is a list a brief writes, as C2c-1's `ratchet.witnesses` does.

*Test,* on the exit prefix:
1. Every workflow in the newest runner evidence within its grace has a shell of the same name under `tools/runner/workflows/` (C2c-1's directory), byte-equal by sha256. This is criterion 8's comparison with C2c-1's twin 10 inverted.
2. Every row in `lane_rows` reads `code`, and the witness the window file names for it is KILLED in the verified run.

*Residue:*
- The runner's `.github/scripts/` and `host/` are not compared. What a shell runs is shown by its own bytes, which say where it fetches from, and those are reviewed text, not a test.
- No text for each job is required here. A text under `transcripts/runner/` is read under ground 15 when it changes.
- A workflow pushed to another branch of the runner runs its own bytes (`host.md` §4; custody v2 §6, rung 4).
- The timers fire on steel, and the record sees only the dispatches they cause.

### B9 The parties' keys are separated: not decidable today

No text on `main` or in draft defines what B9 would compare, so no clause of it can be decided today:
- **Keys.** Custody v2's `custody.json` names each user's party key by its *file name* (v2 §4: "the file name of its `party_key`, or null"). The log names signers by `key_id` (`builder-2`, `reviewer-2`, `counsel-3`, `herald-2`). Nothing maps one to the other.
- **The witness.** C2c-2's draft R7 makes the `custody` row's witness "an operation observed in the window, not a file installed". Custody v2 replaces those observations with W1–W5, and #1032 F8 finds that all five "can record no breach while a session signs as another party".

**The minimum that can be said is what a custody text must define before B9 can be written as a test:**
1. **Signers.** For each user, the log `key_id`s whose private keys it holds, so that "every `key_id` that signed an entry inside the window is held by exactly one user" is a comparison of the log with the tree.
2. **The witness.** The `custody` row's witness, named in the window file as either a pin or an observation with a stated acceptance rule.

Until a custody text that has passed its reads defines both, B9 is a heading with a residue, not a row.

*Residue,* which stands whatever form B9 later takes:
- **Signing.** That no copy of any key exists elsewhere, and that no session signed as another party.
- **The deputies:** K2, K3, K6, and #1032 F5.
- **Old keys.** Five keys still hold powers: `builder-1`, `reviewer-1`, `counsel-1`, `reviewer-2`, `builder-2` (seqs 6, 7, 8, 32, 34). Revoking them is his `key` act.
- **The host.** Copies in `/home/g`, and processes left as `g` (#1032 F6).
- **The master key.** Where it lies (S1). CHARTER §5's proposed default is "an offline master key". Rotating it needs a change to the judge and the charter first (counsel-5's state note of 18 November; SPEC §10 ground 14).
- **The owner.**
- **The shared model keys.**

```sh
python3 -c "import json
k={}
for l in open('log.jsonl'):
  e=json.loads(l)
  for d in (e['body']['keys'] if e['type']=='genesis' else [e['body']] if e['type']=='key' else []): k[d['key_id']]=d['powers']
print(sorted(i for i,p in k.items() if p))"
# ['builder-1', 'builder-2', 'counsel-1', 'counsel-3', 'guy-master', 'herald-2', 'reviewer-1', 'reviewer-2']
```

**Decidability.** B8 compares names, bytes and a pin's verdict, given `lane_rows`. B9 is not decidable today, for the two reasons above.

## 5. Placement

### 5.1 What C2c-2 carries, and what waits (options for C2c-2's brief)

- **The C2c-2 row** (`RESEARCH-meta-jack-20261107.md` §3.2) carries items 3, 4 and 5: `wish`, ground 15, the `NaN` fix, the kernel's bound and the monitor. It names no key separation. Worklist §4 row 16 put it at C2c-2 with "none in B0–B7".
- **The brief draft v8** carries it as R7 and R6 row c, with target rung "1, in this window". Its R7 still describes "one runner group for each, restricted to the workflow files and commits", which custody v2 §6 says GitHub documents for Enterprise only and must be brought to v2 before the sovereign's read.

| | Item | Where |
|---|---|---|
| option | a custody text v3 that answers #1032 and adds K4–K6, its pins, the `custody` row | C2c-2 |
| option | shells under `tools/runner/workflows/` for all six workflows, so that B8.1 can hold | C2c-2, with custody's W5 |
| option | the herald taking the party from the log, and the re-proposer on the party's user running `main`'s code (K6) | C2c-2, with custody |
| waits | four-part texts for the herald, diary, session runner and re-proposer, and their logic moved from shell to `tools/runner/<job>.py`; the `lane_rows` B8.2 reads | after C2c-2, before C2c-3's claim |
| waits | route 6(a)'s writ in place of the model fallback, or route 6(b) | brief 7, if he asks |

**Carrying custody in C2c-2 changes C2c-1's texts in C2c-2.** Custody v2 changes the courier's acts rule (a body counsel wrote is filed as `party:reader`) and the courier shells' `runs-on`. So C2c-2's brief would amend `counsel-courier.md` and C2c-1's `tools/runner/workflows/counsel*.yml`, by its own proposals and reads.

### 5.2 Size against the cap

`judge/scope.json` counts Python under `sim/`, `harness/`, `tests/`, `pins/` and `tools/` against 8,400. `main` at `226355d3` counts 8,347. Shells (`.yml`) and shell scripts are not counted: only `.py` files and files whose first line is a `#!` naming `python` are (SPEC §10.10).

```sh
python3 -I -c "import json,subprocess as s;c=json.load(open('judge/scope.json'));n=0
for f in s.run(['git','ls-tree','-r','--name-only','HEAD'],capture_output=True,text=True).stdout.split():
  b=s.run(['git','show','HEAD:'+f],capture_output=True).stdout
  if any(f.startswith(p) for p in c['counted']) and (f.endswith('.py') or (b[:2]==b'#!' and b'python' in b.split(b'\n')[0])): n+=b.count(b'\n')+(1 if b and not b.endswith(b'\n') else 0)
print(n,c['cap'])"                                        # 8347 8400
```

| File at `dd5578d` | Lines | Counted if moved to `tools/runner/` |
|---|---|---|
| `herald.yml` | 92 | no (shell); its logic in Python would be |
| `repropose.yml` | 56 | no |
| `repropose.py` | 135 | yes |
| `diary.yml` | 113 | no; its 46 lines of Python, as a script, yes |
| `run.yml` | 98 | no |
| `worktree-cleanup.sh` | 72 | no |
| `counsel-act.py` (C2c-1's) | 168 | yes, inside C2c-1's 14,500 |
| `counsel-sign.py` (C2c-1's) | 326 | yes, inside C2c-1's 14,500 |

On today's `main`, any move into `tools/runner/` that adds more than 53 counted lines needs his push to raise the cap. Later, the moves count against the cap of whichever window carries them:
- C2c-1's file states 14,500 and its brief projects 14,123 at its opening;
- C2c-2's draft v8 proposes C2c-1's cap plus 2,000.

The scripts alone add 181 counted lines (135, and 46 by `sed -n '51,96p' opencode-runner/.github/workflows/diary.yml | wc -l`), before any rewrite of the herald or the session runner in Python and before their tests and pins, which are counted and are not estimated here. Whether they fit is the builder's count at the time. A raise is his: "a raise relaxes a control" (BRIEF-C2c-1 §7).

### 5.3 C2c-1

**What this paper changes:** none of C2c-1's merged texts. B8 is read at C2c-3's claim and leaves criterion 8 and twin 10 as they are.

**What follows if the options are taken up:**
- Carrying custody in C2c-2 changes, by that window's own proposals and reads, texts C2c-1 names or freezes: `counsel-courier.md` and the courier's shells (§5.1); every session template (a `party:` line, then the `key:` lines removed); `repropose.md`'s `{KEY}`; `transcripts/runner/README.md`; and `host.md`, including line 40's "repairs, no entries" (custody v2 §3, last paragraph, and §5).
- A "yes" to §8 meets BRIEF-C2c-1 §9, which pre-states C2c-3's promotion forecast as "B0–B7, as `transcripts/RESEARCH-meta-jack-20261107.md` §1 states them once on `main`, hold on the exit prefix".
  - Either that sentence changes by C2c-1's own procedure, or C2c-3's brief departs from it.
  - Or B8 and B9 are carried as a second claim of C2c-3's beside B0–B7, leaving §9's sentence, and ledger claims N7 and N8, as written.
  - Which of these is lawful is not settled here.

```sh
grep -o 'the promotion forecast "B0–B7[^"]*"' transcripts/BRIEF-C2c-1-draft.md   # §9's sentence, on line 134
```

**An inconsistency inside C2c-1's texts**, which this paper finds and does not cure. BRIEF-C2c-1 R7 says the herald, diary, session runner and re-proposer stay "as `hand: sessions` rows the map now dates". But C2c-1's window file names one lane row, `runner`, and moves it to `code`, so at the exit no row is left to date them.

```sh
python3 -c "import json;print(json.load(open('transcripts/windows/C2c-1.json'))['ratchet']['deadlines'])"   # {'runner': 'end', 'elections': 'opening+elections_deadline_days'}
```

## 6. The root cause, stated and not proposed

**SPEC §4:** an entry has "**exactly** the keys `seq, parent, ts, type, proposer, body, sig`". **SPEC §6:** "The signed message is the UTF-8 bytes of the canonical serialisation (§2) of the entry object **without** its `sig` member." So the position (`seq`, `parent`) is signed, and an entry `main` overtakes must be signed again by its party.

**`tools/jack` lines 48–49,** verbatim:

```
    if not on_main and fails("git", "merge-base", "--is-ancestor", "origin/main", "HEAD"):
        refuse(f"{branch} does not contain origin/main; run:\n  git merge origin/main -m \"Merge main into {branch}\" -m \"{t}\"")
```

So the commit moves too, and with it the `proposal` entry's `body.commit`.

**Jobs that exist because a proposal races a moving `main`:**
- the re-proposer, which also handles the herald's `CONFLICTING` refusals, a conflict of content and not only of position;
- the herald's stale-closes;
- `repropose.md`;
- `counsel-sign.py` step 7;
- the signing guard of 00-common rule 8.

Of jack's 1,341 branch heads, 411 have names ending in one or more `-r`/`-rN`, from 262 stems. The count is by name, so it also takes in a few hand re-files and revision names. The longest chain is seventeen deep. The verbs' retry removes none of these: "A party's branch verbs are outside it" (Amendment 3).

```sh
git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||' > heads
wc -l < heads; grep -c -E -- '-r[0-9]*$' heads; grep -E -- '-r[0-9]*$' heads | sed -E 's/(-r[0-9]*)+$//' | sort -u | wc -l   # 1341, 411, 262
grep -o -E -- '(-r[0-9]*)+$' heads | awk -F'-r' '{print NF-1}' | sort -n | tail -1                                    # 17
```

### Can every trigger be computed from the record?

No. The inputs the lane acts on fall into three kinds.

**Text a pull request or issue says of itself:**
- the herald's party, branch and title;
- the session runner's key, model, branch and lane (`build`);
- the diary's handed set and stream number. An issue carrying `due-seqs:` suppresses those writs for three hours, whoever filed it.

**GitHub's state (substrate):** the herald's open list, check results and draft flags.

**The clock:** the diary's role.

The herald's staleness is computed from the logs' bytes, and the diary's due list from the log and the clock. Custody v2 answers the party and the key. No text answers the diary's two.

### Which of his acts each job has needed, and how B5 types them today

- **Installs on the runner:** his merges of #335, #369 and the workflows. These are "repairs by §7's letter" (the ruling of 4 November), and "the classifier does not see a pull request he opens or a merge event" (BRIEF-C2c-1 R7), so they are listed in the report.
- **On steel:** the drop-ins, the memory drop-in of 8 November, the key files, the `gh auth login` of 13 November. These are acts on another host, outside every instrument (B5's residue).
- **The re-proposer disabled and re-enabled** (5877, 5936), and the collaborators-only limit on jack (5878): `decision fix`, so on-log repairs and late reports.
- **The App, counsel's token, deploy keys:** capability grants, so decisions (row 44; seq 2131).

A new typing would be needed for an act that carries out a text he has read and answers no defect (custody v2 §5, "What is not counsel's to settle"). This paper proposes none.

### Route (a): today's design, made safe

The clerk detects a stale proposal from the logs' bytes (the herald does already) and takes the party from the head's log (custody v2). It invites that party, whose re-proposal runs under its own isolated key on `main`'s code (K6). This is the charter's "re-invite".

*Can that re-proposal be a script?* It is one already: "Nothing in it needs judgement to re-make, so no model is asked to" (`repropose.py`). A model is asked only after a refusal. On the ladder a refusal is "re-invite on another runner or model; writ to Guy", so the fallback could be a writ in place of a keyed model session. That is an option, not a proposal.

| Line | Route (a) |
|---|---|
| Spends | a custody text v3 and its reads; custody's acts (v2 §5: two Apps, a staging directory, three root runs, one push, two grants, three `fix` entries); the re-proposer's code under the cap (§5.2) |
| Reversible | until `finish`: custody v2's two phases keep the old runners, and a revert of the paste restores today's lane. After `finish`, by a new install |
| Evidence | §1 rows 3–6 and 9; custody v2 §2–4; #1011; #1032 |
| If nothing is done | the deputies of row 9 stand, and every stale proposal is re-signed under a key every job can read |
| Trial form | custody's pins, and the first admitted runs before `finish` |
| Stop when | a W1–W5 line lists a breach, or a session needs a grant the table does not give |

### Route (b): a sequencing change

Proposers sign what they attest, and the clerk's entry fixes the position. Its price carries all three of:
1. the commit still moves when `main` does, so `body.commit` changes and the party signs again, unless the attestation is made independent of the commit too;
2. a merge queue that judges the merged tree before it lands;
3. a kernel rule refusing a content-signed entry placed twice (replay).

That is a kernel change in both checkers, a change to SPEC §4–§6, and an amendment.

| Line | Route (b) |
|---|---|
| Spends | both checkers, SPEC §4–§6, the judge's grounds 3 and 7, an amendment (A2.7), a merge queue (a GitHub feature whose availability on the organisation's plan the record does not hold), and new pins |
| Reversible | not cheaply. A kernel change binds every later entry; earlier entries stay under the law they were made under (CHARTER §2.2) |
| Evidence | SPEC §4–§6; `tools/jack` 48–49; the branch count above |
| If nothing is done | route (a)'s cost recurs at every moved `main` |
| Trial form | none on the record without the amendment |
| Stop when | the replay rule cannot be stated decidably, or no merge queue is available |

**The paper recommends neither.** Route (b) would be brief 7, if he asks for it.

## 7. The brief's questions

- **Is the lane under an obligation in force?**
  - The `runner` row's principle is "no party acts except through entries; second checker for text". Its enforcer is `hand: sessions`, with no deadline today (`tools/enforcement.json`).
  - From C2c-1's opening a hand row carries a deadline, printed ESCALATED once past (R7, pin `hand_row_deadline`).
  - The paper's reading: a deadline schedules the principle and does not meet it. Only a `code` row with a KILLED witness is enforcement, and C2c-1's witness for the row is the courier's pin alone.
- **"Change power."** §3.1.
- **Which jobs exist because of the race, and what removes them?** §6. The retry removes none of them; each needs 6(a) or 6(b).
- **Can every trigger be computed from the record?** No (§6).
- **His acts.** §6.
- **What do B8 and B9 change?** Ledger claims N7 and N8 (seq 2558, 2559) are written over "the eight rows B0–B7". A5.2 requires C2c-3's promotion claim before its opening. Adding rows changes the roadmap, which under worklist §8 is his to decide.

```sh
python3 -c "import json
for l in open('log.jsonl'):
  e=json.loads(l)
  if e['seq'] in (2558,2559): print(e['seq'], e['body']['claim'][:80])"
```

## 8. The question, with counsel's view

After the paper has passed its read, in 00-common rule 3's form: "Add two rows to the bootstrap predicate, B8 (the clerk acts) and B9 (the parties' keys are separated), so that C2c-3's claim becomes B0–B9?"

**Counsel's view: yes, knowing what it costs.**
- Without B9, B0–B7 can hold while any session on steel signs as any party, and while every job can read his master key's file (S1).
- Without B8, the map can read `code` for a lane most of whose jobs are hand (§5.3).
- B9 is not decidable today (§4). A yes therefore means C2c-3's claim cannot be made until a custody text that passes its reads defines B9's two fields.
- If he wants only rows that can be tested now, the answer is no, and B8 can be put to him alone later.

What a yes does:
- It changes the roadmap, and lengthens the road to the bootstrap claim.
- It meets BRIEF-C2c-1 §9's pre-statement (§5.3).
- It asks C2c-2's and C2c-3's briefs for the `lane_rows` list, six shells and a custody text that passes its reads.

**Interest**, beyond the top:
- The bootstrap claim is counsel's exit, and these rows delay it.
- The counsel principal holds N7 and N8, which are written over B0–B7.
- Counsel's own reviewer-keyed re-proposals of 8 November (row 46) are conduct B9 would bind.

Nothing stands on his silence.
