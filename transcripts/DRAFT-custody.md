# Custody — each party's key in its own place, and who may start a job there (counsel's text, draft v2, 18 November 2026; follows `transcripts/runner/host.md`, which leaves this to "C2c-2's, with a text of its own"; it replaces draft v1, which a cold read failed, runner #1011)

**What this text closes, and what it leaves open.** Today one user on steel runs every job, and a session can sign as any party in two ways. The first is by reading: every party's key lies in that one user's home. The second is by asking: `run.yml` exports as the signing key whatever path an issue's body names (lines 41 and 44, at the runner's `main` `dd5578d7`, as every line cited here), it reads the body when the job starts and not when the issue was filed (line 39), and every job's `gh` acts as the jack-court App with a token that carries all the App was granted (`gh-as-app` line 18 asks for a token and names no limit), minted from a private key in the job user's own home (lines 7 and 14). So a session can file an issue that names another party's key and have the runner start a session under it. Draft v1 closed the first way and left the second, and its reader found it.

This text is written to close both for every session on the host, by three things. Each party's key lies in the home of a user of its own. The key a job signs with is the one in that job's own home, and nothing a session can write chooses it. And no session holds an identity that can file, label or edit an issue on the runner, start a workflow there, or write a file to it. It does not bind the owner: he is root on steel, he owns the organisation, and counsel's drafting session pushes under his login. Against him the aim is that a change shows (`transcripts/QUESTION-20261111-constitution.md`: "the reachable aim is tamper-evidence, not prevention"), and §6 says how far that reaches. It uses nothing of GitHub's that the lane does not use today (an App, runners registered to the repository, a workflow's `permissions`), and so asks for no other plan; §2 says what two features of other plans would add. It binds nothing until the acts of §5 are made and the checks of §4 have run.

## 1. The users

Six system users, each with no password, login shell `/usr/sbin/nologin`, no sudo and a home of mode 700. Each runs its own runners, registered to `renavondata/opencode-runner`, and every runner of a user bears that user's party label and no other user's. A user that runs sessions has two runners, one for each of today's two lanes, which keep long work off the runner that the diary's sessions need inside the hour (`run.yml` lines 24 to 28): each bears the party label and one of two lane labels of new names, `lane-long` and `lane-hour`, so that no workflow of today's reaches a new runner and no workflow of this text reaches an old one (a job runs on any runner that matches every value of its `runs-on`, F3). `jack-counsel` has two likewise, since a signing is allowed 45 minutes (`counsel-sign.yml` line 18) and a request to file should not wait behind one; and `jack-diary` has two under its one label, since every session's start and end now pass through it (§2). A runner registered to a repository serves that repository alone (F2), so no workflow of jack's or of any other repository reaches one of these. What each user holds is all it holds for signing or for GitHub:

| User | Party label | Party key in `~/.ssh/` | GitHub identity in `~/.config/jack/` | What runs as it |
|---|---|---|---|---|
| `jack-builder` | `party-builder` | `jack-builder` | the session App; the reader App | the builder's sessions; the re-proposal of the builder's own stale proposals |
| `jack-reviewer` | `party-reviewer` | `jack-reviewer` | the session App; the reader App | the reviewer's sessions; the re-proposal of the reviewer's own |
| `jack-reader` | `party-reader` | none | none | every session that only reads, counsel's raw-form requests among them |
| `jack-herald` | `party-herald` | `jack-herald` | the filer App | `herald.yml`, and no model session |
| `jack-diary` | `party-diary` | none | the filer App; the session App's and the reader App's files, for the witness alone (§4) | `diary.yml`, the re-proposer's fallback filing, every job that writes to an issue of the runner (§2), the witness's reads of GitHub (§4), and no model session |
| `jack-counsel` | `party-counsel` | `jack-counsel-3` | counsel's token | `counsel.yml` and `counsel-sign.yml`, and no model session |

The first three run model sessions; the last three run only the workflows named and never `opencode`. `jack-builder`, `jack-reviewer`, `jack-herald` and `jack-counsel` also hold jack's deploy key, with which the verbs push branches (`host.md` line 9). `jack-reader` holds no key and no GitHub identity: `renavondata/jack` is public and is fetched without one. The three session users each hold the runner's `.env` with the model keys, which are shared. Each user has its own clone of jack and its own worktrees. The one user `host.md` §1 describes is not made: its installer was never built (`tools/runner/` is absent from jack's `main`), and §4's installer starts from today's one user.

## 2. The identities, and who may start a job

**Three Apps in place of one.** GitHub bounds an installation token by its App's own grant: a request for a token may name fewer permissions and fewer repositories than the App holds, and the token "cannot be granted permissions that the app was not granted" (F1; the sources are listed at the end). An App's permissions are chosen once, for the App; the repositories it reaches are chosen when it is installed (F10). So a session that reads an App's private key can do what that App was granted, on the repositories it was installed on, and no more, whatever it does with the key; and an App installed on two repositories holds its whole set on both. Each App a session can reach is therefore installed on one repository only:

| Identity | Installed on | Its permissions | Its files lie in the homes of |
|---|---|---|---|
| the session App | `renavondata/jack` only | pull requests: write; contents: read | `jack-builder`, `jack-reviewer`; and `jack-diary`, for the witness alone |
| the reader App | `renavondata/opencode-runner` only | issues: read; actions: read | `jack-builder`, `jack-reviewer`; and `jack-diary`, for the witness alone |
| the filer App | both | issues: write; actions: write; pull requests: write; contents: write | `jack-herald`, `jack-diary` |
| counsel's token (the `assize-reviewer` account) | as it is today | as it is today | `jack-counsel` |

Each grant is there for calls read in the code. The session App's: the verbs list, retitle and open a proposal's pull request (`tools/jack` lines 89 to 91 on jack's `main`); jack is public, and its reads need no grant. The reader App's: the session templates have a session read the readers' reports in the runner's issues (`transcripts/sessions/build.md` line 11) and list its workflow runs (`transcripts/sessions/evidence.md` line 14), and the runner is private. The filer App's: the diary creates issues (`diary.yml` lines 101 and 110); the herald comments on, closes and merges pull requests on jack and starts the re-proposer (`herald.yml` lines 42 to 44 and 66). It is installed on both repositories and so holds on each what it needs on the other; no session runs beside it, and §6 names that breadth. The wrapper that makes a job's `gh` act as an App (`gh-as-app`) picks the App by the repository a call names. Counsel's token is the courier's and this text changes nothing in it. Which of the three is today's jack-court App with its grant changed is the sovereign's to choose when he makes them (§5); `custody.json` (§4) names each by its id. These grants are counsel's reading of the code and are untested until the first sessions run under them; a call that then fails for want of a permission comes back to counsel as a finding and is not met by widening a grant on the spot. That is why the old runners stand until those sessions have run (§4).

**The job's own token.** Each job also receives a token from GitHub, and today `run.yml` gives it `issues: write` on the runner (lines 15 to 17) and writes it into the text of the very step that runs the session (line 53; `opencode run` is line 68 of the same step, which runs from line 47 to line 69). A workflow or a job may set what that token can do, and of the permissions it leaves out "all of those that are not specified are set to none" (F8). The rule of this text: **a job on a runner whose user ever runs a model session declares `permissions: contents: read` and nothing more, and that user's home holds no GitHub identity but the session App's and the reader App's, or none.** This text does not assume that what a session started has ended when its job ends, so the rule covers every job on those three users' runners and not only the jobs that run `opencode`. Whatever is written to an issue of the runner (the `started:` line, the transcript, a `refused:` line, the `done` label, the close) is written by a job on a runner of `jack-diary`, where no session runs.

**Who decides that a job runs as a party.** The job's place decides its key (§1); a label on the issue decides the place; so what matters is who can put the label there, and that the decision is made where no session runs. `run.yml` becomes three jobs (§3 gives the lines):

1. **`admit`**, on a runner of `jack-diary`, keeps today's job-level `if` (line 23), so that a label other than `run` starts no job, and runs a script (`admit.py`) on the event, which holds the issue (F7). It admits the event only when all four hold: the label just added is `run` (the test line 23 makes today); the issue bears exactly one label that begins `party:`; that label is `party:builder`, `party:reviewer` or `party:reader` (the three users that run sessions; an issue labelled for `herald`, `diary` or `counsel` is refused, so no session is started beside the filer App or counsel's token); and both the issue's author (the event's `issue.user.login`) and the identity that added the label (its `sender.login`) are on the filer list of `custody.json`, which the script reads from jack's `origin/main`. On admitting, it posts `started:` with the party, the lane, the author, the sender and the SHA-256 of the body, and gives the party and the lane as its outputs. On refusing, it posts `refused:` with the clause that failed, and the job fails.
2. **`session`**, which `needs` `admit`, has `runs-on: [self-hosted, party-<party>, <lane>]` from `admit`'s outputs (a job's `runs-on` may read the `needs` context, F11); the lane is chosen as line 28 chooses it today (`lane-long` when the issue bears `build`, `lane-hour` otherwise). When `admit` fails or is skipped, a job that needs it is skipped (F9). The prompt is the issue's body as the same event carries it, not a second fetch when the job starts (today's line 39). No line of the body sets the key: `JACK_KEY` is the one party key in the job user's `~/.ssh`, or unset where there is none. Unset, the verbs fall back to `~/.ssh/id_ed25519` (`tools/jack` line 314), so no home of the six holds a file at that path, and a verb that signs fails on `jack-reader`'s runners.
3. **`post`**, on a runner of `jack-diary`, which runs whatever became of `session`, posts the transcript and closes the issue.

A label only selects a runner: a job runs on any runner that matches every value of its `runs-on` (F3). So the label is no authority in itself, and the authority here is the script's four tests, made on a runner of `jack-diary`. The script is on jack's `main` beside the workflows (§4), and a pin of §4 runs it on events written in the shape F7 gives. Three things the pin cannot show, because they are facts about what GitHub delivers: that `issue.user.login` is the issue's author, that `sender.login` is who added the label, and that the event for `run` carries the party label already on the issue. Counsel has read none of the three in GitHub's pages. The first admitted run shows them, in its `started:` line, and until that run exists they are untested.

The filer list in this draft holds the filer App's bot login and `assize-reviewer`. Whether the sovereign's own login is on it is his to say when he grants `custody.json`; this text takes no position on it.

**The two filers, and how each chooses the party.** Neither takes it from anything a session wrote.

- The diary files one resolver session for each party its own script lists (`diary.yml` lines 96 to 103) and the stream's session for the reviewer (lines 110 to 112), from the log and the templates of jack's `origin/main` (lines 47, 48 and 109). It gives each issue the party its own code already names in the title.
- The courier files what a request file on the runner's `counsel-requests` branch says (`counsel-act.py`). Today it refuses a body of counsel's own that names the builder's key: "a builder-keyed session is filed from a template, never from a body counsel wrote" (line 115). With no `key:` line left to read, that rule is restated on the label and made to cover the reviewer as well: a request that carries a body counsel wrote is filed as `party:reader` and nothing else; a request that names a template is filed with the party that the template's own `party:` line names on jack's `origin/main`, and is refused when that line holds a placeholder (the templates the diary and the re-proposer fill, whose party their own code supplies), so that the party of a session the courier files is always a word on `main` and never a value in a request.

Both create the issue with its `party:` label and add `run` afterwards, which is what the courier's `then_labels` is for today (`counsel-act.py` line 16: they are "added after the issue exists, so run.yml sees `build` when the `labeled run` event fires"), so that the event for `run` finds the party label there. Between the two calls no identity a session holds can edit the issue (the first two rows of the table below).

**What refuses each route by which a session might start a job as another party.** Counsel has looked for routes and lists those it found; this is a report of a search, not a proof that there are no others.

| The session tries to | With | What refuses it | Rung (BRIEF-C2c-2 R6) |
|---|---|---|---|
| create an issue, or label or edit one, on the runner | the session App's key, or the reader App's | the first is not installed on the runner; the second holds `issues: read` (F1, F10) | 1 |
| the same | its job's own token | the token holds `contents: read` only (F8) | 1 |
| start `herald.yml`, `diary.yml` or `repropose.yml` | either App's key, or its job's token | the call needs the Actions permission at write on the runner (F4), which none of the three holds | 1 |
| push anything to the runner: a workflow file, or a request file for the courier | any of the three | none can write contents there | 1 |
| have a filer file for it, by words in its report or its proposal | nothing of its own | the diary reads the log and its templates from jack's `origin/main`, where a session's entry arrives only by a merged proposal, and takes the party from its own code; the courier reads request files that no session can push (previous row); the herald names the re-proposer's party from the signed log (below) | 3, by the gate on `main`; for the re-proposer 2, by its check |
| name another party's key in an issue's body | a body it cannot write, and a line the runner no longer reads | the `session` job above | 1 |

The first four rows rest on GitHub refusing the call. For the two Apps the witness makes each of those calls and records the refusal (§4, W2). For the job's own token nothing makes the calls: a pin reads the `permissions` each job declares (§4, `workflow_rules`). The fifth rests on what the filers' code does, which is on `main` and changes only by a merged proposal.

**The re-proposer.** Three things in today's files bear on it. `repropose.yml` runs on the shared lane and signs with whichever party's key its `party` input names (line 23; line 45: `JACK_KEY="$HOME/.ssh/jack-$PARTY"`). The herald takes that party from the stale pull request's body (`herald.yml` line 38). The proposal verb writes that body from the principal of the key that signed (`tools/jack` lines 40, 41 and 91); but it is a field of a pull request, and a session's identity can write pull requests on jack, as it must to open them. And when the mechanical re-proposal refuses, the workflow files a model session for the party so named, putting the stale proposal's title into the text of a `sed` program on the way (`repropose.yml` lines 52 to 55). So today the party whose key re-signs a branch, and the party whose session is started on a refusal, are both read from a field that a session can write. In this text:

- the herald takes the party from the stale head's log: the `proposer` of the last `proposal` entry there, and from nothing in the pull request's title or body;
- `repropose.yml` runs on `[self-hosted, party-<party>, lane-hour]`, under a job-level `if` that admits only `builder` and `reviewer` (today's line 35 makes that test in a step, after a runner is taken), and signs with the one key in that user's home;
- before any verb it refuses unless the stale head's log passes the kernel's check and every entry it would make again names that same party as its `proposer` (the test `counsel-sign.py` makes for counsel at line 206). A branch whose log names another party over a signature that is not that party's fails the first (`kernel/check.py` lines 35 and 36 refuse an entry whose `proposer` is not the principal of the key that signed it); a dispatch that names one party and another party's branch fails the second;
- when it refuses on either of those two grounds, nothing is filed. On any other refusal the fallback (today's `repropose.yml` line 55) is filed by a second job on a runner of `jack-diary`, for the party of the dispatch. The title and branch that reach that session's prompt were written by a session of the same party.

It is started by the herald, with the filer App (`herald.yml` line 44); who may dispatch it at all is the filer App and the owner.

**What two features of a paid plan would add.** GitHub documents Actions policies that list who may trigger workflows and by which events (F5), and, for Enterprise, runner groups restricted to named workflow files (F6). Under the first, a run started by an actor or an event off the list fails; the second would keep a workflow file that is not on its list off a keyed runner, which is a route this text only detects (§6). Counsel has not found on GitHub's pages which plans carry the first, and the organisation's plan is a fact only the sovereign can read (asked with this text, §5). Nothing above depends on either.

## 3. The workflow changes, by file and line

Lines are those of the runner's `main` at `dd5578d7`. Five rules hold across the files, and a pin of §4 tests them on the files themselves.

- **The token rule (§2).** Every job declares its own `permissions`, and they are `contents: read` and nothing more unless its `runs-on` is written out, with no expression in it, as a runner of `jack-herald`, `jack-diary` or `jack-counsel`. So a job whose runner is chosen by an expression (`session`; the re-proposer's first job) is always under the rule.
- **The trigger rule.** The events that start a job are today's three kinds and no other: a label added to an issue (`run.yml` line 14); a dispatch (`herald.yml`, `diary.yml`, `repropose.yml`, and the witness's workflow of §4); a push to `counsel-requests` (`counsel.yml` line 10, `counsel-sign.yml` line 12).
- **The data rule.** No job on a runner of `jack-herald`, `jack-diary` or `jack-counsel` puts a string that a session wrote (a pull request's title, body or branch name; a transcript; an issue's body) into the text of a program or of a command line that a shell parses. Such a string travels as an argument, an environment variable or a file, and a template is filled as `counsel-act.py` fills one today (line 108, a plain replacement of each placeholder). Today's `repropose.yml` line 53, which this text moves to a runner of `jack-diary`, is the one place counsel found that would break it; a report of a search, not a proof.
- **The key rule.** No workflow reads the name or path of a key from an issue, a pull request or an input. A job signs with the party key in its own user's `~/.ssh`, or with none.
- **The body rule.** `session` takes its prompt from the event of its own run, the one `admit` hashed, and no step of it reads the issue again.

| File | Lines today | What they do today | In this text |
|---|---|---|---|
| `run.yml` | 15 to 17 | one `permissions` block for the whole workflow: `issues: write`, `contents: read` | `admit` and `post`: `issues: write`, `contents: read`. `session`: `contents: read` |
| | 23 | `if: github.event.label.name == 'run'`, on the one job | kept, on `admit`; made again as the first of `admit.py`'s four tests; `session` runs only when `admit` succeeded |
| | 28 | `runs-on` by lane alone | `admit` and `post`: `[self-hosted, party-diary]`. `session`: `[self-hosted, party-<party>, <lane>]` from `admit`'s outputs |
| | 36 to 46 | with the job's token: fetch the body (39); take `model:`, `key:` and `branch:` from its first four lines (40 to 42); export `JACK_KEY` from the `key:` line (44); post `started:` (46) | the body is the event's; `model:` and `branch:` as today; no `key:` line is read; `JACK_KEY` by the key rule; `started:` is posted by `admit`, with the party, the lane, the author, the sender and the body's SHA-256 |
| | 52 to 55 | every `gh` call of the job acts as the App whose files are in the home (the wrapper is fetched with the job's token, 53) | the wrapper picks the App by the repository a call names: the session App for jack, the reader App for the runner; `jack-reader`'s home has neither |
| | 68 | `opencode run`, the session | unchanged, in `session` |
| | 70 to 84 | with the job's token: post the transcript's last 60,000 bytes (76, 77); relabel `done` (78); close (82); sweep earlier `done` issues (83, 84) | all of it in `post`. How the transcript passes from `session` to `post` is the builder's to choose among means that give `session` no further permission; `post` handles it by the data rule |
| | 85 to 98 | remove the session's worktree; reads one script with the job's token (95) | unchanged, in `session`; `contents: read` suffices for line 95 |
| `herald.yml` | 19 | `runs-on: [self-hosted, herald]` | `[self-hosted, party-herald]` |
| | 29 to 31 | the App wrapper | unchanged in form: the files in `jack-herald`'s home are the filer App's |
| | 38 | the party to re-propose for, from the pull request's body | from the stale head's log: the `proposer` of its last `proposal` entry |
| | 39, 40, 44 | branch and title read from the pull request and passed as inputs to `repropose.yml` | unchanged; both are handled by the data rule from here on |
| `repropose.yml` | 23 | `runs-on: [self-hosted, opencode]` | `[self-hosted, party-<party>, lane-hour]`, with the job-level `if` of §2 |
| | 35 | the test that the party is `builder` or `reviewer`, in a step | in the job-level `if` |
| | 45 | `JACK_KEY="$HOME/.ssh/jack-$PARTY"` | by the key rule; and `repropose.py` gains the two refusals of §2 before any verb |
| | 52 to 55 | on a refusal, fill the template with `sed` and file a session for `$PARTY` | a second job on a runner of `jack-diary`: nothing on either of the two refusals of §2; otherwise the template filled by the data rule and the issue filed with `party:<party>`, the party taken from the dispatch's input and never from the first job's output |
| `diary.yml` | 28 | `runs-on: [self-hosted, opencode]` | `[self-hosted, party-diary]` |
| | 37, 38 | the App wrapper | unchanged in form: the filer App's files |
| | 101 to 103, 110 to 112 | `gh issue create … --label run` | created with `party:$PARTY` (101) or `party:reviewer` (110), then `run` added |
| `run.yml`, `herald.yml`, `repropose.yml`, `diary.yml` | 55; 32; 41; 39 | when the App's files are absent the job goes on under whatever login its user has ("identity: owner login") | removed. No user of the six has a login of the owner's, and a job whose identity is missing stops; `jack-reader` is the one place where none is expected |
| `counsel.yml` | 15 | `runs-on: [self-hosted, opencode]` | `[self-hosted, party-counsel, lane-hour]` |
| `counsel-sign.yml` | 17 | `runs-on: [self-hosted, build]` | `[self-hosted, party-counsel, lane-long]` |
| `counsel-act.py` | 113 to 115, 125 to 127 | labels as the request gives them; a body of counsel's naming the builder's key refused | the rule of §2: a body counsel wrote is filed as `party:reader`; a template is filed with the party its own `party:` line names on jack's `origin/main`, and refused when that line holds a placeholder; `run` is added after |
| `host/herald-tick.service.d/app.conf`, `host/jack-diary.service.d/app.conf` | 6 in each | a user unit of today's one user starts `herald` and `diary` as the App and, when that fails, under the owner's login | units of `jack-diary`, which start both with the filer App and have no second login to fall back to |

The whole run of `run.yml` is still started by the `labeled` event of an issue (line 14), by whoever caused it; `admit` runs for every such event whose label is `run`, and treats the event as data.

Three things follow for jack's own files, each by a proposal on `main`: every session template gains a line `party: <name>` among its first four, which the courier reads (§2), and keeps its `key:` line until `finish` has run, so that a revert of the paste restores today's lane; a later proposal removes the `key:` lines (the five counsel read, `due-resolve`, `stream-forecast`, `build`, `repropose` and `review-brief`, each carry `key: ~/.ssh/jack-…` as their second line, two of them with a placeholder for the party); `transcripts/sessions/repropose.md` no longer carries a `{KEY}` placeholder (`repropose.yml` line 53 fills one today); and `transcripts/runner/host.md` is corrected, as its own proposal after its own read (§5), with the two other texts the first draft's reader named as still describing one user (`transcripts/runner/README.md` and `counsel-courier.md`; counsel has not re-read them for this draft).

## 4. `custody.json`, the installer, its check, the witness and the pins

**Where things live.** The names are BRIEF-C2c-2's. `tools/runner/custody.json` on jack's `main` is the one statement of the intended state. The runner's workflows and scripts as this text changes them are held on jack under `tools/runner/workflows/`, with `admit.py` and the changed `repropose.py` beside them; they enter jack by a builder's proposal like any code, the sovereign's paste copies their bytes to the runner's `main` (§5), and the witness compares the two (W5). The installer and its check are `tools/runner/host/install.sh` and `check.sh`.

**`custody.json`** holds no secret. Its fields:

- `users`: for each of the six, its `party`; whether it runs `sessions`; its `runners`, each a name and a list of labels; the file name of its `party_key`, or null; its `identities` (of `session`, `reader`, `filer`, `counsel`); whether it holds the deploy key and the model keys. A party key is named under one user only, and the installer refuses a file that names one under two;
- `apps`: for each of the three, its `app_id`, its bot `login`, the repositories it is `installed_on` and its `permissions`;
- `filers`: the logins `admit.py` admits;
- `secrets`: every file that only its owner may read, as a user and a path: each party key, each App's private key and cached token, counsel's token, each copy of the deploy key, each file of model keys;
- `refused_calls`: the closed list of calls the witness makes under W2.

**The installer** is run by the sovereign as root on steel. `transcripts/runner/host.md` describes one for a single user; it was never built (`tools/runner/` is absent from jack's `main`), and this one takes its place.

- *Inputs.* `custody.json`, and a staging directory he fills, laid out as the homes it feeds (`DIR/<user>/.ssh/…`, `DIR/<user>/.config/jack/…`). A file there that `custody.json` does not name stops the run, and so does a named file that is missing, in both cases before anything is placed.
- *Starting states.* Today's, where one user (`g`, home `/home/g`, by `host.md` line 22) runs every runner and holds every key; or the state a run of its own left when it stopped part-way. Each step checks its end state first and skips when it holds, so a second run after a complete one changes nothing and a run after an interrupted one finishes it.
- *Two phases, so that the lane does not stop.* **Place**: create the six users and their homes (mode 700); place each user's files (mode 600, owned by that user); clone jack for each; install and register each user's runners under the labels `custody.json` gives. The new runners' labels match no workflow of today's (§1), so the old runners go on serving the lane. Then the sovereign pastes the workflows to the runner's `main`; from that push on, each new job names a party label and reaches only a new runner, and a job already running finishes where it is. **Finish**, run only after the first resolver's and the first stream's sessions have completed under the new workflows: refuse while any job runs on an old runner; remove the old runners; make the two timers units of `jack-diary` (§3's last row), and the witness's timer a third. Until `finish`, the old runners stand and the templates still carry their `key:` lines (§3), so a revert of the paste restores today's lane. It deletes nothing from `/home/g`: it checks that every copy left there is unreadable to the six users, lists them, and leaves their removal to him.
- *The pin's mode.* `--root DIR` places under `DIR/home/<user>/`, creates no user, registers no runner, touches no unit, and prints each command it would have run for those.

**The check**, `check.sh`, run by him as root, prints `ok` or `FAIL` for each line and exits 1 on any `FAIL`: every file of `secrets` exists, is owned by its user and has mode 600, in a home of mode 700; no home of the six holds a file of `secrets` that `custody.json` does not give it; no home of the six holds a file at `~/.ssh/id_ed25519`; every runner unit runs as the user `custody.json` gives its labels to, and none runs as `g`; the three timers' units run as `jack-diary`.

**The witness.** Five observations, each made by a workflow and not by a model's report, each recorded with the instant it was made, T_w, and the interval it speaks for. The workflow is `witness.yml`, held with the others under `tools/runner/workflows/`; a third timer of `jack-diary` starts it by dispatch once a day with the filer App, and a dispatch needs a permission that no identity a session holds has (§2). Its jobs write to nothing but their own logs, which a session of the window's evidence reads with the reader App. Two instants bound them and are not the same: T_c, the instant of the push that first pasted the workflows to the runner's `main`, and T_w. Before T_c the runner is as today, and the witness says nothing of it. After T_w nothing is observed until the next witness.

- **W1**, on a runner of each of the three session users, at T_w, printed with `id -un`: each other user's home exists, is owned by that user and has mode 700; for every file of `secrets` that belongs to another user, `test -r` is false; and, as the control that the test was made and the paths formed rightly, `test -r` is true for each of its own. W1 cannot tell a file that is missing inside a closed home from one that is there and closed; the check above, run by him as root, sees inside. W1 is evidence from a place a session of that user can write to, and the check is the other observation of the same thing.
- **W2**, on a runner of `jack-diary`, at T_w: with a token of the session App, and again with one of the reader App, each call of `refused_calls` on the runner returns 403 or 404: create an issue; add a label to one; edit one's body; dispatch a workflow; write a file. A call that succeeds is itself a breach, reported as one and not undone by the witness. W2 shows what those two Apps were refused at T_w, and nothing about an earlier instant.
- **W3**, on a runner of `jack-diary`, for the interval from T_c to T_w: every job in that interval on a runner of any of the six users (GitHub gives each job its runner's name and each run its workflow's path, commit, branch and event; `custody.json` gives each runner's user) is a job of a workflow whose file, at the run's own commit, has the bytes that file has had on jack's `main`, started by an event that file allows (the courier's two workflows run at the commit of each push to `counsel-requests`, so the test is on the file's bytes there and not on the branch); and for every `session` job, `admit` succeeded in the same run, the issue's author and the actor of its `run` label, as GitHub's own record of the issue gives them at T_w, are on the filer list, the issue bears exactly one party label, that party is the runner's user's, and the SHA-256 in the `started:` line equals that of the issue's body read at T_w. A job that fails any of these is listed as a breach.
- **W4**, on a runner of `jack-diary`, for the interval from T_c to T_w: every push to the runner repository, with its pusher and its branch. A push that changes only files under `requests/` on `counsel-requests` is the courier's traffic and is listed. A push that changes any other path is matched to an entry of the sovereign's on jack's log or listed as a breach. Counsel has not read the page of GitHub's API that lists a repository's pushes; if what it gives does not cover the interval, W4 is made from the branches' commits and says what that cannot see, a branch pushed and deleted inside the interval.
- **W5**, on a runner of `jack-diary`, at T_w: the bytes of each workflow and script on the runner's `main` equal those under `tools/runner/workflows/` on jack's `main`; and each App's permissions and repositories, as its own installation reports them, equal `custody.json`'s.

Each observation prints its rows and then one last line with its name, T_w, its interval, the number of rows and its breaches, and those lines are what the window's evidence copies (BRIEF-C2c-2 R7: "observed inside the window and copied into the runner evidence"). The custody row of the ratchet is `unmet` when any of the five is absent, or lists a breach, or is stale by the brief's rule. The five show nothing about the owner.

**The pins.** Four, each on files or scripts that live on jack. Every twin names its fixture and changes one thing in it; every mutant names the twins that kill it.

*`party_key_unreadable`, on the installer in `--root` mode.* Fixture H: a `custody.json` with the six users of §1; a staging directory complete by it; an old home laid out as `host.md` line 22 describes today's.

| Twin | The one change from H | Expected |
|---|---|---|
| A1 | none | exit 0; every file of `secrets` is under its user's home with mode 600; each home has mode 700; no other file lies under any home's `.ssh` or `.config/jack`; the printed commands create each of the six users once |
| A2 | one file added to the staging directory that `custody.json` does not name | exit non-zero; the file is named; nothing is placed |
| A3 | one named file removed from the staging directory | exit non-zero; the file is named; nothing is placed |
| A4 | run on H2, which is H with the reviewer's key also named under `jack-builder` and also staged there | exit non-zero; both holders are named; nothing is placed |
| A5 | the run made twice | the second exits 0, and names, bytes and modes under `DIR` are as after the first |
| A6 | run on H3, the tree a run leaves when it stops after the first user | names, bytes and modes under `DIR` equal A1's |
| A7 | `finish` run after A1 | names, bytes and modes under the old home are unchanged; the printed commands remove each old runner and make three units for `jack-diary`, the two timers' and the witness's |
| A8 | `check.sh --root` run on A1's tree | every line it can make without users is `ok`; exit 0 |
| A9 | as A8, with one placed file's mode set to 644 | `FAIL` on that file's line; exit 1 |
| A10 | as A8, with the reviewer's key copied into `jack-builder`'s `.ssh` | `FAIL`, naming the file; exit 1 |

Mutants: one that places every secret in every home (A1); one that places with mode 644 (A1); one that ignores a file the staging directory should not hold (A2); one that places the rest when a file is missing (A3); one that accepts a party key under two users (A4: on H2 it places both, and the rule refuses); one that appends to a placed file on each run (A5); one that skips every remaining user once any home exists (A6); one whose `finish` deletes from the old home (A7); one whose `finish` makes the timers' units for `g` (A7); a check that prints `ok` for every line (A9, A10); a check that reads modes and not names (A10). Not tested: that the six users cannot read one another's files, since `--root` mode makes no users (the check and W1 observe that on steel); the check's lines on owners and on units, for the same reason; `finish`'s refusal while a job runs; the registration of runners; anything GitHub does.

*`admit_tests`, on `admit.py`.* Fixture E: an event of action `labeled` whose label is `run`; the issue bears `party:builder` and `run`; its author and the sender are the filer App's bot login; a body of three lines; a `custody.json` whose `filers` are that login and `assize-reviewer`.

| Twin | The one change from E | Expected |
|---|---|---|
| B1 | none | admitted; outputs party `builder`, lane `lane-hour`; the `started:` text holds both, the author, the sender and the body's SHA-256 |
| B2 | the label just added is `done` | refused, first test; exit non-zero; no outputs |
| B3 | the issue bears no `party:` label | refused, second test |
| B4 | the issue bears `party:reviewer` as well | refused, second test |
| B5, B6 | the party label is `party:reviewer`; `party:reader` | admitted, with that party |
| B7 to B10 | the party label is `party:herald`; `party:diary`; `party:counsel`; `party:other` | refused, third test, each |
| B11 | the author is a login off the list | refused, fourth test |
| B12 | the sender is a login off the list | refused, fourth test |
| B13, B13b | the author is `assize-reviewer`; the sender is | admitted, each |
| B14 | `custody.json`'s `filers` holds the bot login alone, and the author is `assize-reviewer` (fixture E2: E with that list; the change is the author) | refused, fourth test |
| B15 | the issue bears `build` as well | admitted; lane `lane-long` |
| B16 | one byte of the body differs | admitted; the SHA-256 differs from B1's |
| B17 | the body's first line is `party: reviewer` | admitted; party `builder` |
| B18 | run on E3, which is E with an empty `filers` | refused, fourth test |

Every refused twin exits non-zero, gives no outputs, and names in its `refused:` text the first test that failed, in the order given; each twin fails one test only, and an event that fails two is not pinned.

Mutants: one without the first test (B2); one that takes the first party label of several, or `builder` when there is none (B4, B3); one that admits any party name (B7 to B10); one without the author's test (B11); one without the sender's (B12); one with the filer list written into the script (B14); one whose lane is always `lane-hour` (B15); one that hashes the title (B16); one that reads the party from the body (B17); one that admits when the list is empty (B18). Not tested: the three facts about what GitHub delivers that §2 names; that a failed `admit` keeps `session` off a runner (the first refused event shows it); the posting itself.

*`workflow_rules`, on the files under `tools/runner/workflows/`.* Fixture W: those files as proposed.

| Twin | The one change from W | Expected |
|---|---|---|
| C1 | none | pass |
| C2 | `session` gains `issues: write` | fail, the token rule |
| C3 | `session` loses its `permissions` block and the workflow's own block grants `issues: write` | fail, the token rule |
| C3b | `session` loses its `permissions` block and the workflow has none | fail, the token rule: a job declares its own |
| C4 | the re-proposer's first job gains `actions: write` | fail, the token rule |
| C5 | a step of `session` sets `JACK_KEY` from a line of the prompt | fail, the key rule |
| C6 | `repropose.yml` sets `JACK_KEY` from its `party` input | fail, the key rule |
| C6b | a step of `session` reads the issue's body through `gh` | fail, the body rule |
| C7 | `run.yml` gains the trigger `issue_comment` | fail, the trigger rule. The checker compares each file's `on:` with the allowed three, so one name stands for every other |
| C8 | the fallback's template is filled for the title `a|b&c` | the filed body holds those five characters where `{TITLE}` stood |

Mutants: a checker that reads only the workflow's own block (C2); one that takes a missing block for no permissions (C3, C3b); one that reads only `run.yml` (C4, C6); one that accepts any assignment to `JACK_KEY` (C5, C6); one without the body rule (C6b); one that does not read `on:` (C7); a filler that passes the title through a `sed` program (C8). Not tested: the data rule beyond the one place C8 covers, which is read by the reviewer and not pinned; any event GitHub might add.

*`repropose_party`, on `repropose.py` and the script by which the herald names the party.* Fixture R: a repository whose `main` has moved on and a stale branch whose own entries, a forecast and a proposal, are signed by a builder's fixture key; the dispatch names `builder`; the job's home holds that key.

| Twin | The one change from R | Expected |
|---|---|---|
| D1 | none | the entries are made again on `main`'s log and signed by that key |
| D2 | the dispatch names `reviewer`, and the home holds a reviewer's fixture key (fixture R2: R with that home; the change is the input) | refused for the party; nothing signed; the fallback is not to be filed |
| D3 | run on R3, which is R2 with every one of the stale branch's own entries reading `proposer: reviewer` over the builder's signature; the dispatch names `reviewer` | refused for the log; nothing signed; the fallback is not to be filed |
| D4 | the stale branch cannot be re-made on `main` for a reason other than those two (the builder takes one from `repropose.py` as it stands, which counsel has not read) | refused; the fallback is to be filed, for `builder` |
| D5 | the pull request's body reads `Proposer: reviewer` | the herald's script still names `builder`, from the log |

Mutants: one without the party's test (D2: it signs the builder's entries with the reviewer's key); one without the kernel's check (D3: every entry names `reviewer`, so the party's test passes and it signs); one that files the fallback on every refusal (D2, D3); one that reads the party from the pull request's body (D5). Not tested: `herald.yml`'s shell around the script.

## 5. The sovereign's acts

What this text asks of his hand, in order, and what the record already says of acts of each kind. Counsel types nothing anew here; each typing is quoted.

| | His act | What the record says of acts of its kind |
|---|---|---|
| 1 | His read of this text, before any builder's session for it | BRIEF-C2c-2 §2: "His read comes before any build", citing A2.10. This text is one of the six that the brief's single `grant` names "by path and by the SHA-256 of its bytes on `main`" |
| 2 | Make two Apps; set the permissions of the three as §2's table lists them; install each on its repositories; give counsel the three Apps' ids and bot logins, which are no secrets, for `custody.json` | the ruling of 4 November: "the App is a capability grant (a decision)" |
| 3 | Fill the staging directory with today's key files and the Apps' private keys | row 44 typed "the token's update and placing" as that ruling types the App, "a capability grant (a decision)"; that typing is counsel's, recorded there at p 0.8 |
| 4 | Run `install.sh place` as root | the ruling of 4 November typed his merges on the runner and his labelling of a runner as "his hand doing the court's machinery work — repairs by §7's letter" |
| 5 | Paste the workflows and scripts to the runner's `main`: one push, at an instant when no session is running | the same |
| 6 | After the first sessions under the new workflows have completed (§4): run `install.sh finish`, then `check.sh`, as root | the same |

Between rows 2 and 3 the builder's work reaches jack's `main` by proposal: `custody.json`, the installer and its check, the workflows and scripts under `tools/runner/workflows/`, the templates' `party:` lines, and the four pins.

**How each is entered.** CHARTER §7: "Every act of Guy's is an entry, typed by its entry type and the key that signs it". Row 2 is one `decision` of kind `grant`, entered when the Apps are made, that names the three by id and says each holds the permissions of §2's table. Row 3 is one more, entered when the directory is filled, that names `custody.json` by its SHA-256 and says the credentials are staged as it lists. The words of both are counsel's drafts, read cold before he sees them, and the entries are his. For rows 4 to 6 the RUNBOOK's line is: "repairs are entered as `jack decision fix \"<what>\"` when made (§7)". `transcripts/runner/host.md` line 40 says of an install and a paste "repairs, no entries"; this text does not follow it, since it contradicts §7's sentence, and host.md's correction is its own proposal.

**What is not counsel's to settle.** §7 says "Repairs: every other act", and also "A repair means a layer has found a defect". Rows 4 to 6 answer no defect found: they carry out a text he will have read. By §7's letter, as the ruling of 4 November read it, they are repairs all the same, and they are entered so. To count them otherwise §7 itself would have to change (row 44: "or §7 must change (A2.10)"), which is an amendment by the charter's own process and not something a text or a brief may do (A2.4: a brief "may tighten the charter's bounds, never loosen them"). Counsel proposes none here and holds an interest in how repairs are counted (row 44 lists its forecasts), so it urges nothing (row 35). What a repair costs in C2c-2's window is that window's brief's to state, and the brief is in draft.

**What it costs him**, said plainly: two Apps to make in GitHub's settings; one directory to fill; three runs as root; one push; two grants and three `fix` entries beyond the brief's own, each a paste counsel gives him. And two facts only he can read, asked here because they bear on §6 and on no step above: which plan the organisation `renavondata` is on, and whether the runner repository's Actions settings offer policies of the kind F5 describes. Neither changes this text.

## 6. What is left, with its rung

The rungs are BRIEF-C2c-2 R6's: "(1) impossible by construction; (2) refused at admission; (3) gated before an irreversible step; (4) detected afterwards at a pre-stated price; (5) attested by a party other than the one bound; (6) narrated by hand".

| What is left | Rung | What shows it |
|---|---|---|
| The owner. He is root on steel and owns the organisation: he can read every key, change every App and every workflow, and file or label any issue. Nothing here binds him | none | a change of an App or of a workflow's bytes shows in W5; a push in W4 |
| A workflow pushed to any branch of the runner under the owner's login, under which counsel's drafting session also pushes. It can name any runner's labels (F3) and declare any permissions, and so run beside any key | 4 | W3 lists the job, since its file's bytes are not jack's; W4 lists the push |
| The courier's two workflows run as the pushed commit has them (each push to `counsel-requests` starts both, at that commit), and fetch their scripts from the runner's `main` when they run (`counsel.yml` lines 25 to 27). So a push there supplies the text of a job beside counsel's key and token | 4 | the same two |
| A request file pushed there has the courier file a session: for the builder or the reviewer from a template whose words and party are `main`'s, or for the reader with a body counsel wrote | 3 for the template's words, by the gate on `main`; 4 for the act | every request is a commit W4 lists, and every issue so filed has `assize-reviewer` as its author in W3 |
| An issue edited after it is filed and before `run` is added, by an identity that can edit it (a filer; the owner). The session runs the edited body. The SHA-256 in `started:` is of the body as admitted, so W3 shows an edit made after that and not one made before | none | nothing; no session holds such an identity (§2) |
| The filer App holds its whole set on both repositories (F10), contents: write on the runner among it. It lies only where no session runs. What stands between it and a string a session wrote is the data rule, pinned in one place (C8) and otherwise read by the reviewer | 3 | the reviewer's read of each change under `tools/runner/workflows/` |
| With the session App a session can retitle, edit or close any pull request on jack, another party's included. The App holds no `contents: write`, which the herald's merge uses, and the party of a stale proposal is now read from the log | none | the pull request's own history on GitHub |
| The model keys are one set, held by all three session users | none | nothing |
| What a party's session does with what is in its own user's home: its key, its Apps, its runners' own files | none | the log, for what it signs |
| Anything a session left running as `g` before `finish`, and the copies of every key that stay in `/home/g` until he removes them | 6 | `finish` lists the copies; ending such processes (a restart of steel does it) and removing the copies are his |
| The installer and the check beyond their pin: owners, units, the registration of runners, `finish`'s refusal while a job runs | 6 | his reading of `check.sh`'s output on steel |
| Before T_c, and after the last T_w, nothing is observed | none | each observation states its interval |

**What the brief must change with this text.** BRIEF-C2c-2 R7 as drafted has "one runner group for each, restricted to the workflow files and commits `tools/runner/custody.json` lists", and a witness whose second and third observations are a pushed workflow "that names the reviewer's group and never starts" and "each group's workflow list, read through the API". GitHub documents such groups for Enterprise only (F6), and this text rests on none. R7, row c of R6 and the brief's list of deliverables are to be brought to this text, and read, before either goes to the sovereign's read. Row c's target cell reads "1, in this window: one user for each party (the custody text)"; this text aims at rung 1 against every session on the host, for reading a key and for starting a job as another party; counsel's search found no route below that rung, which is a report of a search; and the rest stands at the rungs of the table above.

## Sources

GitHub's documentation, read on 18 November 2026. Each fact is in counsel's words; two phrases are quoted in §2, one from F1's page and one from F8's, and no other.

- **F1** A token for an installation may be asked for with fewer permissions and fewer repositories; asked for with neither, it has all the App's permissions on every repository of the installation; it lasts about an hour; and it is bounded by the App's own grant, in the words quoted in §2. https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app
- **F2** A runner added to a repository serves that repository alone. https://docs.github.com/en/actions/concepts/runners/self-hosted-runners
- **F3** A job runs on any runner that matches every value of its `runs-on`. https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
- **F4** Starting a workflow by dispatch needs the Actions permission at write (https://docs.github.com/en/rest/actions/workflows). An event raised with a job's own token starts no workflow run, a dispatch excepted (https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
- **F5** Actions policies can list which actors may trigger workflows and which events may run them; the page does not say which plans have them. https://docs.github.com/en/actions/concepts/about-actions-policies
- **F6** The page on runner groups for the Free and Team plans speaks of which repositories may use a group and has no section on which workflows may; its Enterprise versions add that a group can be limited to a list of workflows. https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access
- **F7** The payload of an `issues` event holds the issue, and a label added arrives as the action `labeled`; payloads carry a `sender`. https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads
- **F8** A workflow or a job may set the permissions of its token, and those it leaves out are none, in the words quoted in §2. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- **F9** A job-level `if` keeps a job from running unless its condition is met (https://docs.github.com/actions/using-jobs/using-conditions-to-control-job-execution); when a job fails or is skipped, the jobs that need it are skipped unless their own condition says otherwise (https://docs.github.com/actions/using-jobs/using-jobs-in-a-workflow).
- **F10** An App's permissions are chosen for the App when it is registered; installing it grants those permissions, and the installer chooses the repositories it reaches (https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app; https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps). A permission added later must be approved where the App is installed (https://docs.github.com/en/apps/maintaining-github-apps/modifying-a-github-app-registration).
- **F11** A job's `runs-on` may read the contexts `github`, `needs`, `strategy`, `matrix`, `vars` and `inputs`; a job's `if` may read `github`, `needs`, `vars` and `inputs`. https://docs.github.com/en/actions/learn-github-actions/contexts

Observed on the live API on 18 November, not taken from a page: a workflow run carries its file's `path`, its `head_branch`, `head_sha`, `event` and `triggering_actor`; a job carries its `runner_name` and `labels`.
