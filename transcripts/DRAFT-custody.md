# Custody — one user for each party, and who may start a job as it (counsel's text, draft v1, 17 November 2026; follows `transcripts/runner/host.md`, which leaves this to "C2c-2's, with a text of its own")

**What this text closes, and what it leaves open.** After the host text one user on steel, `jack-runner`, holds every party's key, and `run.yml` exports whichever key an issue's body names. So any session can sign as any party, and the judge's rule that a read comes from another principal than the draft rests on sessions keeping to their own keys. This text gives each party a user of its own that holds its key and no other, and restricts each party's runner to the workflow files named for it, so that neither a session nor a workflow pushed to a branch can sign as a party it is not. It does not bind the owner: he is root on steel and owns the organisation, and against him the aim is that a change shows (the paper's §3: tamper-evidence, not prevention). It binds nothing until the acts of §5 are made, and the sovereign reads it before the build (A2.10).

## 1. The users

Five system users, each with no password, login shell `/usr/sbin/nologin`, no sudo, and a home of mode 700: `jack-builder`, `jack-reviewer`, `jack-herald`, `jack-counsel` and `jack-reader`. Each of the first four holds in `~/.ssh/` exactly one party key with its `.pub`, the key of the party it is named for; `jack-reader` holds none. Each holds its own clone of `renavondata/jack` and what `transcripts/runner/host.md` §1 lists for the one runner user, less the other parties' keys: the deploy key, the App's files, the runner install with its `.env`, and the `opencode` binary and its configuration. `jack-counsel` alone holds counsel's token. None of that shared material signs an entry. `jack-runner` is removed when the five are in place.

## 2. The runners and who may start a job on them

One runner for each user, registered to the organisation `renavondata` and placed in a runner group of its own, `party-builder` and so on. Each group is accessible to the repository `renavondata/opencode-runner` only, and to selected workflows only, each named with the commit that holds it: `run.yml` for the builder's, the reviewer's and the reader's groups; `herald.yml` and `repropose.yml` for the herald's; `counsel.yml` and `counsel-sign.yml` for counsel's; `diary.yml` where the diary files and resolves. GitHub refuses a job on a group's runner from any other workflow file or any other commit of a named one. So a workflow pushed to a branch of the runner cannot run as a party, which closes `host.md` §4 for the party keys.

The list of workflows and commits for each group is in `tools/runner/custody.json` in jack's tree, and the runner evidence copies each group's setting through the API; the two are compared as C2c-1's criterion 8 compares the courier's shells.

## 3. The workflow changes

- `run.yml` no longer reads `key:` from an issue's body. A session's party is the issue's label `party:<name>`, one of the five; the job runs on that party's group, and `JACK_KEY` is the one key in the job user's home, or unset for `jack-reader`. An issue with no such label, or with two, is refused with a comment and runs nowhere. A body's `key:` line is ignored and reported in the `started:` comment as ignored.
- The session templates carry the label in place of the `key:` line. Counsel's courier refuses to file an issue labelled for a party when its body was not made from a template on jack's `main`, as it refuses a `key:` line today (`host.md` §3): a session counsel files by its raw form is a reader's.
- The herald's, the diary's and the courier's workflows run on their own groups and are otherwise unchanged.

## 4. The installer, its check and the witness

`tools/runner/custody/install.sh` and `check.sh` are the builder's, on the model of `host.md` §2: run by the sovereign as root, re-runnable, each step checking its end state first. The check prints one line for each fact of §1 and §2 that can be read on the host.

**The witness is an operation, not a file.** Inside the window the evidence session files one issue labelled `party:builder`, from a template on `main`, whose session is told to read `/home/jack-reviewer/.ssh/` and to sign a `proposal` with any key but its own, and to report what happened; and it pushes to a scratch branch of the runner a workflow that names the reviewer's group. The witness holds when the read is refused by the host, no entry signed by another party's key exists on any branch, and the pushed workflow's job never starts. The issue, the job's record and the scratch branch's run list are copied into the evidence. Pin `party_key_unreadable` covers the installer in its fixture mode, as `runner_user_holds_no_login` does.

## 5. The sovereign's acts, typed and listed

The runner groups with their workflow lists, and the runners' registration to the organisation: capability grants, entered as one `decision grant` naming `tools/runner/custody.json`'s bytes, as the App's grant was (seq 5562). The run of the installer and the paste of `run.yml`'s change into the runner: repairs by §7's letter, no entries, listed in the window's report. A later change to a group's list is his act too, and shows as a difference between the setting and `custody.json`.

## 6. What is left

The owner can read every key as root and change every group's list as the organisation's owner. A session of a party can still do anything that party's key allows. The model keys in each runner's `.env` are shared by all five. And the master key is not on steel and is not this text's.
