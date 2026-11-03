model: {MODEL}
key: ~/.ssh/jack-{PRINCIPAL}
branch: ops-election-{INVITE}

# {PRINCIPAL}: six freshness forecasts for election invite {INVITE}

The diary substitutes `{MODEL}`, `{PRINCIPAL}` and `{INVITE}` from the replayed invite, never by hand. You are that principal, under `JACK_KEY=~/.ssh/jack-{PRINCIPAL}`, in `~/git/worktrees/jack/ops-election-{INVITE}`, cut from `origin/main` now. Work only inside this worktree, in `transcripts/` and `log.jsonl`; no code and no edits to existing files. Read RUNBOOK's forecast section. Run `tools/jack` verbs one at a time. Do not read the whole log; one entry is `grep -n '"seq":{INVITE},' log.jsonl` (canonical JSON has no spaces).

First run `python3 tools/elect.py --replay {INVITE}`. Stop on any refusal. Read that invite: your principal and model must exactly equal `args.principal` and `args.model`. The invite owns `W0`, `W1` (`args.window_utc`) and `BY` (`resolves_by`, W1 + 4 h). Use those strings verbatim. If now is at or after W0, stop and report the missed session; do not substitute a later window. The uncovered-hour fallback in `stream-forecast.md` applies only to a session filed **without** an invite. From the first election invite, the diary files one session per invite, not a three-window session.

The six datasets are `hk_property_poi`, `hkex_disclosures`, `hkex_disclosure_interests`, `crhk_companies`, `sfc_licences`, `hk_property_transactions`; URLs are in `transcripts/evidence/renavon-freshness-20261031-base.json`. Use the record-counting command and forecasting method in `stream-forecast.md` (including its mixed-history probability bounds), restricted to the public record before the invite; inspect the public pages at forecast time. Apply the same forecasting method regardless of which arm was drawn. Do not let the selected arm or sigma change your method or the outcomes. Record one line of reasoning per dataset, with counts and page evidence, in `transcripts/ELECTION-{INVITE}-FORECAST.md` before entering forecasts.

Enter exactly six `world.renavon` forecasts, one per dataset, before W0. Each has `--by <BY>` and the stream forecast's args (`stream`, `dataset`, `url`, `window_utc`, `hour_hkt`, `evidence`, `resolution_evidence`, `base_rate_permille`, `base_rate_population`), plus `"model":"{MODEL}"` and `"invite":{INVITE}` (an integer). The claim is the existing freshness claim for that dataset and this window. Do not revise a forecast already entered; report it. Check that the six entries name six distinct datasets and all carry this invite, model, window and deadline.

Commit the note, then `tools/jack proposal --title "election invite {INVITE}: six freshness forecasts for <W0>"` with timeout 900000. Report the PR, six forecast seqs and (dataset, p) rows. The resolver is the other principal, as `python3 tools/elect.py --resolve-plan {INVITE}` prints. Missing forecasts/pages or feedback after BY remain in the round as n=1, and the invitation fails; a later arrival cannot repair its gain.
