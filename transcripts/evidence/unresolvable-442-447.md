# Late disposition of forecasts 442–447

Reviewer: `reviewer reviewer-2`, model `openai/gpt-6-astra`.
Reviewed 2026-11-05 on `resolve-442-447`, from `origin/main`
`7b8dda5`.
Related issue: <https://github.com/renavondata/jack/issues/350>.

All six forecasts are the builder's `world.renavon` / `freshness` claims for
`[2026-11-02T02:00:00Z, 2026-11-02T03:00:00Z)`, due
`2026-11-02T05:00:00Z`. Each entry was read individually from `log.jsonl`.
These are late dispositions; they do not undo the already-recorded expiries.

## Evidence and rule

The named `renavon-freshness-20261031-base.json` is a pre-forecast catalogue
snapshot, not evidence of the November 2 outcome. The contemporaneous outcome
pages are already committed on main under
`transcripts/evidence/renavon-freshness/20261102T0305/`, with fetch metadata in
`transcripts/evidence/renavon-freshness-20261102T0305-resolve.json`. That manifest
was written for forecasts 434–439: its dataset URLs and windows match 442–447
exactly, so the underlying public observations also bear on these forecasts.

The raw pages were committed by
`2a58faffacb3e2a8becf9787c706e0cc0d003f63` at 2026-11-02T03:08:22Z.
The manifest's forecast selection was corrected by
`52ea0a3b1d510dc353868514c4032725a4485504` at 03:10:01Z; the six raw pages were
not changed. Thus the observations were recorded after the window and before
the resolution deadline, rather than reconstructed from today's pages.

Verification on 2026-11-05 recomputed each raw page's SHA-256, extracted its
literal `dateModified`, compared it with the manifest, checked each URL and
window against its individual forecast, and checked that each fetch was after
03:00Z and before 05:00Z. All checks passed. The observable is the public
Dataset `dateModified`, as explained in
`transcripts/REVIEWER-FRESHNESS-20261031.md`, not a sample row or rounded age.

`transcripts/sessions/due-resolve.md` specifies threshold comparison against
the window start and forbids a resolution where the evidence does not decide
the claim exactly. This task explicitly permits contemporaneous committed
evidence. `transcripts/world-types.md` was also read: it contains **no
`world.renavon` contract** (its history has no such addition). No missing
contract has been invented or added retroactively. The five resolutions below
use the claims' stated observable and contemporaneous evidence of their named
hour. Seq 445 has a material timing ambiguity, detailed separately.

## Per-sequence disposition

All times below are UTC. The threshold is 2026-11-02T02:00:00Z.

| Seq | Dataset | Fetch time on November 2 | Recorded last updated | Disposition |
| --- | --- | --- | --- | --- |
| 442 | `hk_property_poi` | 03:06:46Z | 2026-11-02T02:48:18Z | Resolve **1**: timestamp is inside the named hour. |
| 443 | `hkex_disclosures` | 03:06:58Z | 2026-11-02T02:40:40Z | Resolve **1**: timestamp is inside the named hour. |
| 444 | `hkex_disclosure_interests` | 03:06:59Z | 2026-11-02T02:40:40Z | Resolve **1**: timestamp is inside the named hour. |
| 445 | `crhk_companies` | 03:06:58Z | 2026-11-02T01:28:28Z | **Unresolvable without a timing interpretation**; no resolution entered. See below. |
| 446 | `sfc_licences` | 03:06:59Z | 2026-10-31T04:32:32Z | Resolve **0**: contemporaneous post-window timestamp precedes the threshold. |
| 447 | `hk_property_transactions` | 03:06:59Z | 2026-11-02T02:40:26Z | Resolve **1**: timestamp is inside the named hour. |

Hashes of the `20261102T0305/<dataset>.html` pages:

| Seq | SHA-256 |
| --- | --- |
| 442 | `38757c73baad1194bed673254e7a0bd3dadb5180783d844aaca4a9fab3c07a10` |
| 443 | `823832a6f9a68dfaa3bd64f5dcb24d9bcd3668027d49055c2d7975587403d426` |
| 444 | `90256053d8409e332c891e9f0301a5b098955a5ef7dbdc108d1c14f121acc887` |
| 445 | `dd47f0507b64f68ad1db5348c9f49ea73cbb94ce3dfb863e6e915650d96095ce` |
| 446 | `4f4aba3d09439ef0184f38d17f73389dfe3d56959754e2c66e66ef5a1f388d18` |
| 447 | `e7f8de79197e03a74611992f95908a587ffbadfaa0a5686c21f03d5e53d3b936` |

## 445 — why no binary resolution is entered

The claim says the page, "fetched after 2026-11-02T03:00:00Z", shows a timestamp
at or after 02:00Z, and parenthetically identifies this with delivery by the
10 HKT hourly window. It does not specify an exact fetch instant, a first-fetch
rule, or an upper bound on the displayed timestamp. The original freshness
note (lines 94–102) explicitly recognized this distinction between the literal
threshold and attribution to an hourly run.

Two committed historical observations give different threshold results:

1. The main-branch 03:06:58Z page above prints
   `2026-11-02T01:28:28+00:00`: **0** under the post-window observation procedure.
2. Commit `ba7db3a8b909dfc15b371b09d169701b7f33ed89` on
   `ops-resolve-20261102T0510` contains
   `transcripts/evidence/renavon-freshness-20261102T0510-resolve.json` and
   `transcripts/evidence/renavon-freshness/20261102T0510/crhk_companies.html`.
   Its recorded fetch is **2026-11-02T05:21:32Z**, and its literal `dateModified`
   is **2026-11-02T03:27:53+00:00**: **1** under the unbounded literal threshold,
   but that update is outside the named 02:00–03:00Z hour. The raw page's hash,
   independently recomputed from that Git object, matches its manifest:
   `06abf291cf5f280ef595330bceb75519564f895f7166b2dcd8f9a210a3c832ae`.
   This is a historical committed record, not a new network fetch or a claim
   that the branch's attempted resolutions reached main.

The later positive observation cannot establish that the named hour delivered
rows; the earlier negative observation cannot negate the unrestricted
"fetched after" wording for every later fetch. There is no registered type
contract selecting between these interpretations. Therefore no unique outcome
at the claim's intended instant can be assigned without adding a timing rule.
An authoritative interpretation fixing the observation instant (or choosing
the literal unbounded threshold over the named-hour reading) would decide which
of these already-preserved observations controls. No guess is entered here.

For comparison, the same later manifest still prints
`2026-10-31T04:32:32+00:00` for `sfc_licences`; it does not contradict seq 446's
contemporaneous negative observation. The four positive resolutions already
have timestamps inside the named hour itself.
