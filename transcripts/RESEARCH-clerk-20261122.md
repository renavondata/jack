# The clerk acts: the lane under the law (counsel's research paper, draft v1, 22 November 2026)

Written by a counsel session (`claude-opus-5-5`, `session_01VpB3TmrXo8QB1Qa3EdgZSU`) to the Project brief "06 — the clerk acts" (revision 2), on the sovereign's word "Sure" of 21 November to have it written and carried out, and his "Yes" of 22 November to go on drafting after finding S1. **It binds nothing.** It has the standing of `transcripts/RESEARCH-meta-jack-20261107.md`: an input to C2c-2's brief, which is not on `main` (a partial draft, v8, is on `counsel/c2c-2-spec-v4`). Where this paper and the record differ, the record governs.

**What was read, at which commits.** jack `main` at `226355d3`; `renavondata/opencode-runner` `main` at `dd5578d7`, every file of it whole; `counsel/c2c-2-spec-v4` at `59b0b021` for `transcripts/DRAFT-custody.md` v2 and `BRIEF-C2c-2-draft.md` v8; runner issues #188 and #1011 (its last comment, the report). The sections of CHARTER, SPEC and RUNBOOK the brief lists were read whole; other texts are cited by the line read. Every figure below carries the command that gives it.

**Interest.** Counsel's own key (`~/.ssh/jack-counsel-3`) and token sit on steel with every other party's (`transcripts/runner/host.md` §6), and B9 would bind counsel's custody. Counsel's forecasts on the windows gain from fewer lost windows. This session holds no forecast of its own.

## 0. In six lines

1. The lane is the charter's clerk, the part that acts. Of its six workflows, two (the courier's) have a text on `main`. The other four, and every script and timer, have none. The enforcement map records all of them as one row, `runner: hand: sessions`, with no deadline.
2. C2c-1's ratchet moves that one row to `code` on the courier alone. Its own pin's twin 10 ignores every workflow that has no shell. So from C2c-1's exit the map would read `code` for a lane of which four jobs of six are still hand.
3. Every job can read every party key and act as `gfrmin` (#188, known). **S1:** every job can also read the file of the sovereign's master key, by his answer of 22 November. No text on `main` says so, and custody v2 does not reach it.
4. The deputy of #1011 is answered in design by custody v2, which is unread. Three triggers the lane acts on are still taken from text that a pull request or an issue says of itself.
5. The race with a moving `main` is the root of the re-proposer, the herald's stale-closes, and 411 of jack's 1,339 branch heads. The verbs' retry (C2c-1 Amendment 3) does not reach it, because it binds main verbs and excludes branch verbs.
6. Two predicate rows are decidable in the form of B0–B7: B8 (the clerk acts) and B9 (the parties' keys are separated). Each has a residue the record cannot show. Adding them changes the roadmap, and that is his to decide.

## 1. Inventory

Each job is given: trigger; identity; keys and tokens it can read by path; what it does, in order; the jack text it is written to; its enforcement-map row; incidents. "Every job can read" means: as user `g`, every file in `g`'s home (row 1).

The figures re-verified against the brief's baseline:

```sh
git -C opencode-runner rev-parse --short HEAD                     # dd5578d
wc -l opencode-runner/.github/workflows/*.yml opencode-runner/.github/scripts/*
# counsel-sign.yml 29, counsel.yml 27, diary.yml 113, herald.yml 92, repropose.yml 56, run.yml 98,
# counsel-act.py 168, counsel-sign.py 326, gh-as-app 21, repropose.py 135, test-worktree-cleanup.sh 87, worktree-cleanup.sh 72
git -C opencode-runner ls-files host                              # host/herald-tick.service.d/app.conf, host/jack-diary.service.d/app.conf
```

The brief's list omits `gh-as-app` (21 lines) and `test-worktree-cleanup.sh` (87). Both are listed below.

### Row 1 — runner issue #188: the host (open since 2026-11-03T12:36:47Z)

- **Fact:** all three runners (`steel-opencode`, `steel-opencode-2`, `steel-herald`) run as `g`. `g`'s `gh` login is `gfrmin`, with scopes `admin:org`, `repo` and `workflow`. Its home holds "ssh keys, keyrings and so on", and "Any step of any job on these runners can read all of it" (#188's body).
- **Push to `main`:** `main`'s protection requires `judge` and `tests` and exempts administrators (`enforce_admins` false), so a job acting as `gfrmin` can push `main` directly. This route is named by #188 ("can push to every repo") and by `host.md` line 9 ("administrators exempt").
- **His acts:** he read `host.md` v14 on 8–9 November. It has not been installed (worklist §4 row 15).
- **Map row:** none. The courier text says so: "no row names the host" (`counsel-courier.md` §Custody).

```sh
gh api repos/renavondata/opencode-runner/issues/188 --jq .state                        # open
gh api repos/renavondata/jack/branches/main/protection --jq '.enforce_admins.enabled'   # false
```

### Row 2 — S1: the sovereign's master key, readable by every job

- **Fact:** his pastes run on steel ("the machine that holds the sovereign's key", `transcripts/PUSH-c2a-prime-opening.md` line 65), in `~/git/jack-guy`, beside the runner's `~/git/jack` in `/home/g` (`host.md` §2's default `--old-home`).
- **Which key signs:** no paste on `main` names a key, so the verbs default to `~/.ssh/id_ed25519` (`tools/jack` line 314; RUNBOOK §Common "Key and party").
- **His answer:** by his answer to the adviser of 22 November (`CLERK.md` entry 7), the key is on steel where the jobs can reach it.
- **Limits:** the key asks for a passphrase (RUNBOOK line 29), so a job that reads the file holds a ciphertext, not a signature. Whether an `ssh-agent` under `g` holds it unlocked is open (`CLERK.md` entry 6, OPINION).
- **What the texts say:** none names S1. `host.md` line 3 names "every party key". Its "the runner holds no key of his" (line 9) describes the state after the install. Custody v2 says it "does not bind the owner" and deletes nothing from `/home/g` (§4, finish).
- **Map row:** none.
- **Typing:** this is the brief's stop condition, reported on 21 November before drafting (`CLERK.md` entry 5). The cost under B5 of a hand fix was stated there: off GitHub, outside every instrument; as a `decision fix` naming no failed window, a repair and a late report. This paper recommends no fix.

```sh
git grep -n -E 'JACK_KEY|--key' origin/main -- 'transcripts/PUSH-*.md'   # no output
sed -n 314p tools/jack | grep -c 'id_ed25519'                             # 1
```

### Row 3 — `herald.yml` (92 lines)

- **Trigger:** two. The workflow's own `schedule: */10 * * * *` (line 10), and a dispatch by the user unit `herald-tick` on steel. The unit's drop-in (`host/herald-tick.service.d/app.conf`) calls `~/.config/jack/gh-as-app-timer`, "or" falls back to `gh workflow run herald` under the owner's login. The unit's timer interval and the bytes of `gh-as-app-timer` are in neither repository.
- **Identity:** the jack-court App when `~/.config/jack/app-id` and `app.pem` exist (lines 29–31), else "owner login". The wrapper `gh-as-app` is fetched from the runner's own repository at `$GITHUB_SHA`, not from jack.
- **Keys and tokens:** `~/.ssh/jack-herald` (key_id `herald-2`, {merge}); the App's private key; and everything in row 1.
- **What it does, in order:**
  1. Sweeps `/tmp`.
  2. Pulls `~/git/jack` `main`.
  3. For each open pull request, oldest first, reads the head's last log entry.
  4. If that entry is a `merge`: completes GitHub's merge on green checks, or re-proposes if the head's log is no longer prefixed by `main`'s.
  5. If it is a `proposal` and the log is no longer a byte-prefix, closes the pull request "as stale" with a comment and dispatches `repropose.yml`.
  6. Otherwise, on `judge` and `tests` both green, runs `JACK_KEY=~/.ssh/jack-herald tools/jack merge N`. On `CONFLICTING` it re-proposes.
  - In steps 4 and 5 the party to re-propose for is read from the pull request's **body**: `sed -n 's/^Proposer: …/'` (line 38). The branch and title come from the pull request too (lines 39–40).
- **Text:** none on `main`. RUNBOOK `jack key` and `jack merge` describe the verb and the herald's key, not the job.
- **Map row:** `W3` ("the herald merges only on green CI", `code: tools/clerk.py merge_writs`) witnesses the merge after the fact. The job itself is under `runner: hand: sessions`.
- **Incidents:** C2a-prime died when the herald merged a branch cut before the opening (COUNSEL-OPEN row 69). It sat on #229 and #231 for hours after a `--watch` returned non-zero (its own comment, lines 55–59). It closed counsel's #1112 as stale (row 74).

### Row 4 — `repropose.yml` (56) with `repropose.py` (135)

- **Trigger:** `workflow_dispatch` by the herald, with inputs `n`, `branch`, `party` and `title`, all taken from the stale pull request.
- **Identity:** the App, else owner login (lines 38–41).
- **Keys:** `JACK_KEY="$HOME/.ssh/jack-$PARTY"` (line 45), `PARTY` limited to builder or reviewer (line 35); and row 1.
- **What it does, in order:**
  1. Checks out the runner repository.
  2. Runs `repropose.py` from that checkout.
  3. The script re-applies the stale branch's non-log diff, re-enters each forecast and resolution with the verbs under the party's key on a new `<branch>-r…` branch from `origin/main`, and proposes. It skips by rule only (`repropose.py` docstring).
  4. On exit 2 it fills `transcripts/sessions/repropose.md` with `sed`, putting `$TITLE` into the `sed` program's text (`s|{TITLE}|$TITLE|g`, line 53), and files a model session under that party's key (line 55).
- **Text:** `transcripts/sessions/repropose.md` is the fallback session's prompt. The job itself has no text.
- **Map row:** `runner: hand: sessions`.
- **Incidents:**
  - The exposure of 18 November, and his three late reports, seq 5877, 5878 and 5936. Two of those three are acts on the lane (situation paper, Appendix A).
  - Content-only proposals dropped until 8 November (runner #410; jack #616 lost by ninety seconds).
  - Six resolutions skipped as forecasts on 3 November (the workflow's comment).
  - Counsel's reviewer-keyed re-proposals of 8 November (row 46).
  - The `fix` brief that cannot land (`counsel/repropose-fix-brief`, situation §5.5).

### Row 5 — `diary.yml` (113, of which 46 are inline Python)

- **Trigger:** `workflow_dispatch` only (a schedule "fired once unbidden on 1 Nov", line 2). It is dispatched by the user unit `jack-diary` through `gh-as-app-timer`, falling back to the owner's login (`host/jack-diary.service.d/app.conf`).
- **Identity:** the App, else owner login.
- **Keys:** none used. It reads everything in row 1.
- **What it does, in order:**
  - The role is fixed by the dispatch's minute, read from the run's `createdAt` (lines 42–43).
  - Before :15, it computes from `origin/main`'s log every forecast now due (lines 51–96). It then files one `run` issue per party, carrying the list and `due-seqs:`, from `transcripts/sessions/due-resolve.md` (lines 100–104).
  - Otherwise, it files the reviewer's stream session from `stream-forecast.md` (lines 106–112).
  - The set "already handed" is read from the `due-seqs:` lines of issues whose title matches `resolve the writs due` (lines 49 and 59–64). The stream number N is the largest in any issue title, plus one (lines 106–108).
- **Text:** `due-resolve.md` and `stream-forecast.md` are the sessions' prompts. The job's computation has no text; its rules are its comments.
- **Map row:** `runner: hand: sessions`.
- **Incidents:** four forecasts expired on 3 November while nothing was filed; the six-hour cutoff was changed to two days (lines 8–14). The owner's login died from 10:15Z to 13:06Z on 13 November and stopped the lane (the drop-ins' comment).

### Row 6 — `run.yml` (98): the session runner

- **Trigger:** `issues: labeled` with label `run` (lines 13–14, 23), from whoever adds the label.
- **Identity:** the job token (`issues: write`) for the issue's steps. For the session, the App, else owner login.
- **Keys:** `JACK_KEY` is set from the body's `key:` line, read when the job starts (custody v2 §0 cites lines 39, 41 and 44). The model keys come from the runner's `.env`. And row 1.
- **What it does, in order:**
  1. Reads the body.
  2. Takes `model:`, `key:` and `branch:` from its first four lines.
  3. Posts `started:`.
  4. Makes a worktree from `origin/main`.
  5. Runs `opencode run` with the body as prompt.
  6. Posts the transcript tail, relabels `done`, closes the issue and sweeps older `done` issues.
  7. Removes the worktree with `worktree-cleanup.sh`, fetched from the runner at `$GITHUB_SHA`.
- **Text:** none for the job. The templates under `transcripts/sessions/` are prompts that it runs.
- **Map row:** `runner: hand: sessions`.
- **Incidents:**
  - #188.
  - #1011's deputy (row 9 below).
  - `/tmp` out of inodes on 2 November.
  - 449 worktrees and about 60G by 9 November.
  - The job token shadowing the owner's login (run 41060460243).

### Row 7 — `counsel.yml` (27) with `counsel-act.py` (168), and `counsel-sign.yml` (29) with `counsel-sign.py` (326): the courier

- **Trigger:** a push to `counsel-requests`.
- **Identity:** `assize-reviewer`'s token (the grant of seq 2131), and the job token for reads.
- **Keys:** `~/.ssh/jack-counsel-3` (the sign job), counsel's token, and row 1.
- **Order:** as `transcripts/runner/counsel-courier.md` states.
- **Text:** `counsel-courier.md` (C2c-1's).
- **Map row:** `runner`, moving to `code` in C2c-1 (R7).
- **Where the scripts come from:** both workflows fetch their script from the runner's `main` (`counsel.yml` lines 25–26; `counsel-sign.yml` 27–28), not from jack's. That is C2c-1's change.
- **One difference between text and script.** The courier text says that, from `host.md` §3, a body counsel wrote "may carry no `key:` line at all". `counsel-act.py` at `dd5578d` refuses only a line naming `jack-builder` (line 114). The text itself says that any difference "is a finding against the scripts".
- **Incidents:** #335 and #369 installed by his merges (row 46, "the courier lapse"); #1112 staled (row 74).

### Row 8 — `worktree-cleanup.sh` (72), `test-worktree-cleanup.sh` (87), `gh-as-app` (21)

- **Fetching:** each is fetched by the workflows from the runner's own repository at `$GITHUB_SHA`. `gh-as-app` mints an installation token for the App with no permission or repository named (line 18), so the token carries the App's whole grant (custody v2 §0).
- **Text, map row:** none for any of the three; they fall under `runner`.

### Row 9 — the deputy (#1011)

Any identity that can file and label an issue on the runner, which today includes every session through the App, can start a session under any key `run.yml` will read.

- **#1011 found:** the route needs no key stolen (§2(i) of its report). Its witness "can appear satisfied while custody is false" (§3).
- **What still answers it on `main`:** nothing.
- **Custody v2's answer:** three Apps; session users with no identity that files, labels or edits a runner issue; `admit.py`'s four tests on the event; the party taken from a label set by a filer, never from a body.

### Row 10 — substrate, named and not legislated

GitHub (Actions, the API, branch protection, the organisation and its plan); steel's operating system and root; the runner binary and its registration (`.runner`, `.credentials`); systemd and the two user timers; the model providers.

- **What the record can see:** GitHub's run objects (`path`, `head_sha`, `event`, `runner_name`) through the API, and nothing of steel itself except what a job prints.

```sh
gh api repos/renavondata/opencode-runner/actions/workflows --jq '.workflows[] | .path+" "+.state'   # six, all active
```

**The stop condition.** It was applied before drafting. #188 is known and is not a stop. S1 fired the condition and was reported on 21 November (`CLERK.md` entry 5); he answered on the fact (entry 7) and said "Yes" to drafting on 22 November. Nothing else the inventory found is unnamed:

- a push to `main` by the herald's merge, through the judge;
- a push by the `gfrmin` login, named in row 1;
- commits on steel under his git name: custody v2 §4 cites the herald's merge on jack #1116, and `CLERK.md` entry 6 cites builder commit `7b03d75d`;
- the drop-ins' fallback to the owner's login, named in the drop-ins themselves and in custody v2 §3's last row.

## 2. Dispositions

The three dispositions are the brief's. The precedent for "clerk code" is the courier: a shell in the runner, byte-equal to `tools/runner/workflows/<job>.yml`, fetches `tools/runner/<job>.py` from jack's `main`. The job is written to a four-part text under `transcripts/runner/` (README). Its witness is a KILLED pin plus criterion 8's byte-equality.

| Job | Disposition | Precedent or change | The test that would witness it |
|---|---|---|---|
| herald (merge path) | clerk code | the courier; RUNBOOK `jack merge`: "When the clerk holds `merge`, this verb is unchanged" | a pin that it merges only a head whose last entry is a `proposal` by a declared key with green checks, and closes nothing whose staleness the bytes do not show; byte-equality |
| herald (stale-close and dispatch) | clerk code, or delete under 6(b) | the charter's ladder, "re-invite" (§5) | the same pin, with the party read from the head's log (custody v2 §2) |
| re-proposer | clerk code under 6(a); delete under 6(b) | custody v2 §2–3 (the party user, the log's `proposer`, refusals before any verb); pin `repropose_party` (D1–D5) | `repropose_party` killed; byte-equality |
| re-proposer's model fallback | clerk code (a writ in place of a model) under 6(a); see §6 | the ladder's "re-invite on another runner or model; writ to Guy" | a pin that a refusal files a writ and no keyed session |
| diary | clerk code | the courier; `transcripts/sessions/due-resolve.md` already moves "what is due" into code (the diary's own comment, lines 2–10) | a pin that the due list and the handed set are a function of `origin/main`'s log and the clock alone (§3.4 below) |
| session runner | clerk code | custody v2 §2's `admit` / `session` / `post` split; pins `admit_tests`, `workflow_rules` | those pins killed; custody's W3 |
| courier | clerk code | C2c-1 (R7) | `courier_signs_only_the_request`, criterion 8 |
| worktree cleanup, `gh-as-app` | clerk code (scripts the shells fetch) | the courier's scripts | its existing test file moved into `tests/`; byte-equality |
| the two timers and `gh-as-app-timer` | substrate, with their unit files as shells | custody v2 §3's last row (units of `jack-diary`) | byte-equality of the unit drop-ins under `tools/runner/host/`; what the timer does when it fires is not visible to the record |
| quiet-minute waits in his pastes | delete | the verbs' retry (worklist row 27; BRIEF-C2c-1 Amendment 3) | Amendment 3's pin |

**No job is marked delete on today's law alone.** The verbs' retry removes only his waits. Amendment 3: "A party's branch verbs are outside it."

## 3. The clerk's identity and the parties' keys

### 3.1 What "change power" covers

- **CHARTER §3:** "A rule enters or leaves only by a change entry signed by a key holding the change power (at genesis, Guy's alone)."
- **§5:** the offline master key holds "change power; capability grants for money, releases and new keys". The online herald key "may sign only `accept` and `wish` entries".
- **SPEC §10.1:** the trusted base changes "only by Guy's `jack push`".
- **RUNBOOK `jack merge`:** nothing the merge does "reaches `main` except through the judge", and "When the clerk holds `merge`, this verb is unchanged".

So, on the texts, change power is the power over the law and the trusted base: `amend`, `push`, `key`, and the `decision` kinds §7 lists. A merge applies a proposal the judge has admitted and changes no rule, so the charter's clerk may hold `merge` and still hold "no change power". The texts never say this in one sentence; the paper reads it from the four above and names it for C2c-2's brief to state.

### 3.2 Under which principal the acting clerk signs

**Precedent:** `herald-2` (principal `herald`, {merge}, seq 201). From the window that first runs rounds it signs invites: "Only `--invite` signs, with the key file it is given: the herald's" (RUNBOOK `jack elect`). That needs a `forecast` power `herald-2` does not hold in C2b ("`herald-2` holds no `forecast` power").

**The paper's reading.** The acting clerk is the `herald` principal. Its powers grow only by his `key` entries, which are capability grants and so decisions (§7). It never holds `amend`, `push`, `key` or `decision`.

**Its GitHub identity.** Custody v2 gives it the filer App, on a user (`jack-herald`, `jack-diary`) where no model session runs.

### 3.3 The keys: custody v2 against #1011

| #1011 finding | v2 | Left |
|---|---|---|
| BLOCK 2(i) the deputy | answered in design. No session identity can file, label or edit a runner issue (§2's table, rows 1–4). `admit.py` admits an event only for one of three session parties, with author and sender on the filer list. The courier files a body counsel wrote only as `party:reader` | three facts of what GitHub delivers (author, sender, label present at the event) are untested until the first admitted run (v2 §2) |
| BLOCK 2(iii) execution-time body | answered. The body rule: the prompt is the event's, hashed in `started:` | an edit by a filer or the owner before `run` is added (v2 §6: rung "none") |
| BLOCK 1 re-proposer on the wrong user; five parties against three groups; diary unplaced | answered. The re-proposer runs on the party's user; sessions only for builder, reviewer and reader; a `jack-diary` user | — |
| BLOCK 2(ii) pushed workflows and commit pinning | not prevented. It relies on no Enterprise feature; detection is by W3 and W4 (rung 4) | a workflow pushed to any branch of the runner under the owner's login |
| BLOCK 3 the witness | redesigned as five observations with intervals (W1–W5) | W1 is evidence from a place a session of that user can write to (v2's own words) |
| BLOCK 4 "repairs, no entries" | answered. Rows 4–6 of v2 §5 are entered as `decision fix` | each is a repair under §7; inside a window each fails B5 |
| BLOCK 5 missing inputs | `custody.json`'s fields; the installer's two phases | v2 §6's table |

**Not in #1011 and not in v2: S1.** V2 makes no statement about the master key's file, and `check.sh` looks only at the six new homes ("no home of the six holds a file at `~/.ssh/id_ed25519`"). **And v2 is unread:** no runner issue from #1051 to #1193 reads it.

```sh
gh api 'repos/renavondata/opencode-runner/issues?state=all&per_page=100' --jq '[.[0].number,.[-1].number], [.[]|select((.title+" "+(.body//""))|test("custody";"i"))|.number]'
# [1193,1094] then []   (and [1150,1051] then [] in CLERK.md entry 2)
```

**What the paper needs from the custody text** (requirements, not the install):

- **K1** Every key with powers on the log that a lane job uses is named under exactly one user in `custody.json`, and no job runs as a user that holds another principal's key.
- **K2** No job's key, model, branch or party is read from text a session can write. The party comes from a filer's label or the signed log.
- **K3** No identity a session holds can file, label or edit an issue, dispatch a workflow, or write a file on the runner.
- **K4** No user of `custody.json` can read any file of a home outside it, the sovereign's included. This is W1 extended from "each other user's home" to every home on steel that holds a secret. That is the part of S1 a job's observation can decide.
- **K5** Each observation states its interval, and the intervals are contiguous from the window's opening.

### 3.4 The session runner, and what `counsel-act.py`'s refusal closes

**Today.** `run.yml` "exports whatever `key:` an issue body names" (`host.md` line 3). `counsel-act.py` refuses a body counsel wrote that names `jack-builder` (line 114). That refusal closes one route: counsel's raw-form request carrying the builder's key.

**What it does not close:**

- a raw body naming the reviewer's, herald's or counsel's key. The courier text already forbids any `key:` line, and the script lags it (row 7);
- any issue filed by another identity: the App, which every session holds, or the owner;
- an edit of the body after filing, since `run.yml` reads the body when the job starts;
- reading any key by path (row 1).

`host.md` says the same: "the courier's refusal in §3 is a courtesy to the record, not a bound" (line 3).

## 4. Two predicate rows in B0–B7's form

### B8 The clerk acts

*Test*, on the exit prefix, from the tree, the log and the runner evidence (`transcripts/evidence/runner-<stamp>.json`, extended from `.github/workflows/` to every file of the runner's `main`), all four:

1. Every file of the runner's `main` is byte-equal (sha256) to a file of the same name under `tools/runner/workflows/`, `tools/runner/` or `tools/runner/host/`. Names and paths are as `tools/runner/custody.json` maps them.
2. Every shell fetches its script from `renavondata/jack`'s `main` and from nowhere else. Bytes equal to a reviewed shell decide this; no separate test is needed.
3. Every job of part 2 marked clerk code has a text under `transcripts/runner/` in README's four parts.
4. Every row of `tools/enforcement.json` whose principle is the lane's reads `code`, with a witness that is KILLED in the verified run.

This extends C2c-1's criterion 8 from the courier to the whole lane. It is the mutant C2c-1's pin `ratchet_row_moves` names for its twin 10 ("every workflow required to have a shell"), made the rule at the bootstrap and not in C2c-1, whose texts it leaves as they are.

*Residue:*

- A workflow pushed to any other branch of the runner runs its own bytes (`host.md` §4; custody v2 §6, rung 4). B8 reads `main` only; custody's W3 and W4 detect such a run, and B8 says so.
- The timers fire on steel, and the record sees only the dispatches they cause.
- That a shell's script is the one GitHub ran is shown by the run's `head_sha` and nothing stronger.

### B9 The parties' keys are separated

*Test*, on the exit prefix:

1. `tools/runner/custody.json` on the tree meets K1 for every key with powers on the log at the prefix that a lane job uses.
2. The newest custody evidence (custody v2 §4's W1–W5, copied by the evidence session as B7 copies the monitor's) is within twenty-four hours of the assessed instant. Each of its five lines lists zero breaches. Its intervals, with every earlier copy in the tree, cover the window from its opening without a gap (K5).
3. W1, as K4 extends it, finds no other home's secret readable, and no file of the sovereign's home readable, from any session user.
4. The map's `custody` row reads `code`, with `party_key_unreadable`, `admit_tests`, `workflow_rules` and `repropose_party` KILLED in the verified run.

Like B7's, the evidence pattern is a file the evidence session copies. Like `host.md`'s `check.sh`, the witness prints one `ok` or `FAIL` line per test.

*Residue*, in B6's form:

- that no copy of any key exists elsewhere, the record cannot show;
- copies left in `/home/g` until he removes them (custody v2 §6, rung 6);
- where the master key lives, which is his (S1);
- the owner, who is root and owns the organisation;
- the shared model keys;
- what a party's session does with its own key;
- anything outside the witnesses' intervals.

W1 is an observation from inside the place it observes, and his `check.sh` is the other observation of the same thing.

**Decidability.** Both rows are decidable from the log, the tree and named evidence files. Neither decides that the property holds between observations, or against the owner. That is the minimum each can claim, and their residues say so. If the sovereign rules that an observation from a session user's own runner cannot count for B9.3, the minimum left is B9.1 with B9.4, and B9.3 moves to the residue.

## 5. Placement

### 5.1 What C2c-2 carries and what waits

- **The C2c-2 row** (`RESEARCH-meta-jack-20261107.md` §3.2) carries `wish`, ground 15 and the monitor. It names no key separation; worklist row 16 placed it at C2c-2 with "none in B0–B7".
- **The C2c-2 brief draft** (v8) does carry it, as R7 and R6 row c (target rung 1, "in this window"), with criterion 8's `custody` row. But its R7 still names Enterprise runner groups and a file `transcripts/runner/custody.md`. Custody v2 §6 says R7 must be brought to v2 "before either goes to the sovereign's read".

The paper's placement, for C2c-2's brief to adopt or refuse:

| | Item | Window |
|---|---|---|
| carry | custody v2, after its reads, with K4 added: B9's test; its four pins; the `custody` ratchet row | C2c-2 |
| carry | W5's byte-equality of every workflow and script on the runner's `main`: the evidence for B8.1 | C2c-2, with custody |
| carry | the herald reading the party from the log, and `repropose.yml` on the party's user (custody v2 §2) | C2c-2, with custody |
| wait | a four-part text for each of the herald, the diary, the session runner and the re-proposer, and moving their logic out of shell into `tools/runner/<job>.py`: B8.3 and B8.4 | after C2c-2, before C2c-3's claim |
| wait | route 6(a)'s script in place of the model fallback, or route 6(b) | brief 7, if he asks for it |

### 5.2 Size against the cap

`judge/scope.json` counts Python under `sim/`, `harness/`, `tests/`, `pins/` and `tools/` against a cap of 8,400. `main` at `226355d3` counts 8,347, which leaves 53. Shells (`.yml`) and shell scripts (`.sh`) are not counted: only `.py` files and files whose first line is a `#!` naming `python` are (SPEC §10.10).

```sh
python3 -I -c "import json,subprocess as s;c=json.load(open('judge/scope.json'));n=0
for f in s.run(['git','ls-tree','-r','--name-only','HEAD'],capture_output=True,text=True).stdout.split():
  b=s.run(['git','show','HEAD:'+f],capture_output=True).stdout
  if any(f.startswith(p) for p in c['counted']) and (f.endswith('.py') or (b[:2]==b'#!' and b'python' in b.split(b'\n')[0])): n+=b.count(b'\n')+(1 if b and not b.endswith(b'\n') else 0)
print(n,c['cap'])"                                        # 8347 8400
```

| File at `dd5578d` | Lines | Counted if moved to `tools/runner/` |
|---|---|---|
| `herald.yml` | 92 | no (shell); its logic, rewritten in Python, would be |
| `repropose.yml` | 56 | no |
| `repropose.py` | 135 | yes |
| `diary.yml` | 113 | no; its 46 lines of inline Python, made a script, yes |
| `run.yml` | 98 | no |
| `worktree-cleanup.sh` | 72 | no |
| `counsel-act.py` (C2c-1's) | 168 | yes, inside C2c-1's 14,500 |
| `counsel-sign.py` (C2c-1's) | 326 | yes, inside C2c-1's 14,500 |

Beyond C2c-1, the scripts alone are 181 counted lines (`repropose.py` 135 and the diary's 46) before any rewrite of the herald or the runner in Python, and before their tests and pins, which are counted too and are not estimated here. Any job moved into `tools/runner/` therefore needs his push to raise the cap. That is the sovereign's own push (SPEC §10), and "a raise relaxes a control" (BRIEF-C2c-1 §7).

### 5.3 C2c-1 untouched

Nothing here changes C2c-1's merged texts. B8 is a row of the bootstrap predicate, read at C2c-3's claim, and does not alter criterion 8 or the pin's twin 10. The `runner` row's move in C2c-1 stands as its brief states it.

**One consequence C2c-2's brief should record.** From C2c-1's exit the map reads `runner: code:tools/runner` while four jobs stay hand (§0, line 2). BRIEF-C2c-1 R7 says the other jobs "stay as they are … as `hand: sessions` rows the map now dates". But the window file names only one ratchet row for the lane, `runner` (`ratchet.deadlines`: `runner`, `elections`).

```sh
python3 -c "import json;print(json.load(open('transcripts/windows/C2c-1.json'))['ratchet'])"
```

## 6. The root cause, stated and not proposed

**SPEC §4–§6.**

- An entry has "**exactly** the keys `seq, parent, ts, type, proposer, body, sig`" (§4).
- "The signed message is the UTF-8 bytes of the canonical serialisation (§2) of the entry object **without** its `sig` member" (§6).
- So `seq` and `parent`, the position, are inside what is signed. An entry overtaken by `main` cannot be moved; it must be signed again by its party.

**`tools/jack` lines 48–49** (the branch verbs):

```
    if not on_main and fails("git", "merge-base", "--is-ancestor", "origin/main", "HEAD"):
        refuse(f"{branch} does not contain origin/main; run:\n  git merge origin/main …")
```

So the commit moves too, and with it the `proposal` entry's `body.commit`.

**The jobs that exist only because a proposal races a moving `main`:**

- the re-proposer, whole;
- the herald's stale-close and dispatch (lines 36–48, 60–62, 77–79, 88–90);
- the template `repropose.md`;
- `counsel-sign.py` step 7, which merges `main` into the branch;
- the signing guard of 00-common rule 8, a counsel practice.

On jack, 411 of 1,339 branch heads are re-proposal branches, from 262 stems; one chain is seventeen deep. The verbs' retry removes none of these: it binds the six main verbs, and "A party's branch verbs are outside it" (Amendment 3).

```sh
git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||' > heads
wc -l < heads; grep -c -E -- '-r[0-9]*$' heads; grep -E -- '-r[0-9]*$' heads | sed -E 's/(-r[0-9]*)+$//' | sort -u | wc -l   # 1339, 411, 262
```

**Can every trigger be computed from the record?** No. Three cannot today:

1. the herald's party for a re-proposal, read from the pull request's body (row 3);
2. the session runner's key, model and branch, read from the issue's body (row 6);
3. the diary's handed set and stream number, read from issues' bodies and titles (row 5). An issue carrying a `due-seqs:` line suppresses those seqs' writs for three hours, whoever filed it.

Custody v2 answers the first two. The third is in no text. The herald's staleness itself is computed from bytes of the logs, and the diary's due list from the log and the clock. The courier's requests are counsel's acts by design, and B6 ties them to receipts.

**Which of his acts each job has needed, and how B5 types them today:**

- **The installs on the runner:** his merges of #335 and #369, and of the workflows generally. These are acts on the runner repository, "repairs by §7's letter" (the ruling of 4 November). BRIEF-C2c-1 R7: "the classifier does not see a pull request he opens or a merge event", so they are listed in the report.
- **On steel:** the drop-ins, the memory drop-in of 8 November, the key files, and the `gh auth login` of 13 November. These are acts on another host, outside every instrument (B5's residue).
- **Disabling and re-enabling the re-proposer** (5877, 5936), and the collaborators-only limit on jack (5878): entered as `decision fix`, so on-log repairs, and late reports.
- **The App, counsel's token and deploy keys:** capability grants, so decisions (row 44; seq 2131).

A new typing would be needed where an act carries out a text he has read and answers no defect (custody v2 §5's "What is not counsel's to settle"). The paper proposes none.

**Route (a), today's design made safe.** The clerk detects a stale proposal from the log and the tree alone. The herald already compares bytes; custody v2 has it take the party from the head's log. It invites the party, whose re-proposal runs under its own isolated key. This is the charter's "re-invite".

*Can the re-proposal be a script rather than a model?* `repropose.py` is one already: "Nothing in it needs judgement to re-make, so no model is asked to". The model session is only the fallback on exit 2: an unexpected entry type, a patch that will not apply, a verb refusing. On the ladder, a refusal is "re-invite on another runner or model; writ to Guy". So the fallback can be a writ instead of a keyed model session. The paper states that as an option.

| Line | Route (a) |
|---|---|
| Spends | custody v2's acts (two Apps, a staging directory, three root runs, one push, two grants, three `fix` entries; its §5); the re-proposer's code under the cap (§5.2); a stream re-proposal stays one keyed run per stale proposal |
| Reversible | yes: custody v2's two phases keep the old runners until `finish`, and a revert of the paste restores today's lane |
| Evidence | §1 rows 3–6, 9; custody v2 §2–4; #1011 |
| If nothing is done | the deputy stands (row 9), and every stale proposal keeps re-signing under a key every job can read |
| Trial form | custody v2's pins, and the first admitted runs before `finish` |
| Stop when | a W1–W5 line lists a breach, or a session needs a grant the table does not give (v2: "comes back to counsel as a finding") |

**Route (b), a sequencing change.** Proposers sign what they attest, and the clerk's entry fixes the position. Its price carries all three of:

1. the commit still moves when `main` does, so `body.commit` changes and the party signs again, unless the attestation is also made independent of the commit;
2. a merge queue that judges the merged tree before it lands;
3. a kernel rule refusing a content-signed entry placed twice (replay).

That is a kernel change in both checkers, a SPEC change to §4–§6, and an amendment.

| Line | Route (b) |
|---|---|
| Spends | both checkers, SPEC §4–§6, the judge's grounds 3 and 7, an amendment by A2.7, a merge queue (a GitHub feature whose plan the record does not hold), and a new pin set; every window since C0 would be replayed under the old law |
| Reversible | not cheaply: a kernel change binds every later entry, and the old entries stay under the old law (CHARTER §2.2) |
| Evidence | SPEC §4–§6; `tools/jack` 48–49; the 411 branches |
| If nothing is done | route (a)'s cost recurs at every moved `main` |
| Trial form | none without the amendment; a simulation on a fork could price it |
| Stop when | the replay rule cannot be stated decidably, or the merge queue is unavailable on the plan |

**The paper recommends neither.** Route (b) would be brief 7, if he asks for it.

## 7. The brief's questions, answered

- **Is the lane already under an obligation in force?**
  - The `runner` row's principle is "no party acts except through entries". Its enforcer is `hand: sessions`, with no deadline today (`tools/enforcement.json`).
  - From C2c-1's opening a hand row carries a deadline, and the clerk prints it ESCALATED once past (R7, pin `hand_row_deadline`).
  - A deadline schedules the principle and does not meet it. Only a `code` row with a KILLED witness meets it. And C2c-1's witness for the row is the courier's pin alone.
- **What does "change power" mean?** §3.1: the law and the trusted base, not merges.
- **Which jobs exist only because of the race?** §6. The retry removes none of them. Each needs 6(a) or 6(b).
- **Can every trigger be computed from the record?** No: three named in §6.
- **Which of his acts has each job needed?** §6.
- **What do B8 and B9 change?**
  - Ledger claims N7 and N8 (seq 2558, 2559) name "B0–B7".
  - A5.2 requires C2c-3's promotion claim before its opening.
  - Adding rows changes the roadmap, and under the worklist's §8 that is his to decide.

```sh
python3 -c "import json
for l in open('log.jsonl'):
  e=json.loads(l)
  if e['seq'] in (2558,2559): print(e['seq'], e['body']['claim'][:120])"
```

## 8. The question

In 00-common rule 3's form, after the paper has passed its read: "Add two rows to the bootstrap predicate, B8 (the clerk acts) and B9 (the parties' keys are separated), so that C2c-3's claim becomes B0–B9?" Counsel's view and interest go with it to him. Nothing stands on his silence.
