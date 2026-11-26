# FrostLine: Implementation Plan

Version 2.2, 26 November 2026. AI in Finance group project, crime domain. SP Jain School of Global Management, Dubai.
Group 2: Kartik Joshi, Prem Kukreja, Gagandeep Singh, Samuel Alex.
Status: **development started on 26 November 2026** (13.1, row 24). **Final presentation: Tuesday 15 December 2026.** The day-by-day schedule is in 9.2. This plan contains no code; the code lives in the repository (9.1).

**FrostLine** is the project's name (13.1, row 17): frost is the first sign of a freeze, and the line is our warning line. The explainer page `Before-the-Freeze.html`, used at the first presentation on 26 November 2026, still carries the old name, "Before the Freeze".

Approved direction: D1 (primary), D2 and D3 (secondary). D4 is supporting analysis only. D5 is folded into D1.

**How to read the evidence in this plan**

- **[chain]** means we measured it ourselves from public TRON data, **counting events to the end of 23 November 2026 (UTC)** unless another date is given. Section 5.5 lists each measurement and its limits.
- **[data]** means we measured it by inspecting the downloaded files. No model was trained.
- A link means we read the source, in full or in the part we cite.
- "Not verified" means exactly that. Appendix B lists everything we could not read or check.
- Tool versions, release dates and licences were read from PyPI, npm, GitHub and the tools' own pages on **26 November 2026**.
- All dates and times are UTC.

**Words used in this plan**

| Word | Meaning here |
|---|---|
| Wallet | A TRON address. Version 1 said "account" or "address" |
| Public vote, time **S** | The **earliest** multisig proposal to freeze the wallet, executed or not |
| Freeze, time **F** | The first `AddedBlackList` event for the wallet |
| Warning | The wallet is above the warning line at a scoring moment |
| Right warning | The public vote on that wallet starts within 30 days after the warning |
| Early warning | A right warning whose vote starts at least 7 days after the warning |
| Learn, Tune, Test | The three past periods. Version 1 said train, validation and test |
| Live lists | The sealed warning lists made once a day from the analysis lock (6.9) |

---

## 0. What changed in versions 2, 2.1 and 2.2

**Version 2.2 (26 November 2026, late evening)**

- **Who does what is not in this plan.** Version 2.1 named an owner for each work package and phase without being asked. All of those names are removed. You assign owners, and progress.md records them (9.3, 13.2).
- **Repository.** Public, at https://github.com/KartikJoshi23/FrostLine (your decision; 13.1, row 26). Version 2.1's "private until the lock" is withdrawn.
- **Master laptop.** Described as the laptop this repository was set up on. The plan does not say whose it is.

**Version 2.1 (26 November 2026, after the audit)**

- **Deadline.** The final presentation is on 15 December 2026, so the live trial no longer waits two months. From the analysis lock (target 4 December) a warning list is sealed every day, and a held-out check covers 1 November to the lock. On 15 December every list is shown with its open window marked as pending; final totals follow when the last 30-day window closes (6.9).
- **Errors fixed in the audit.**
  1. The trial screen's losses were to be measured on Test months before the lock, which would have touched Test data early. They are now designed on Tune months and reported on Test after the lock (6.9).
  2. The warning line was set for monthly scoring, but the live lists are daily. Past and live scoring now use the same daily rhythm, with a 30-day wait before a wallet can be listed again (RQ2, 6.7).
  3. Some life-cycle features used all history since 2024, which the live pipeline cannot read. Every feature now uses at most 180 days (3.1).
  4. Nothing stopped anyone from sealing several lists and later showing the best one. Now exactly one list a day is sealed, and its root is published within an hour (6.9).
  5. The held-out data could have been pulled before the lock. They are now pulled only after it (2.3, 6.6).
  6. "The four checks use early warnings" did not fit check 1, which uses AUROC. All four checks are now described as made at seven days before the vote (6.7).
  7. Section 9.1 placed the brief in `docs/`, but the brief stays in the root folder, where the collaborator prompt expects it.
- **Decisions settled** (13.1, rows 17 to 27): the name, the stack, the evidence graph, Merkle sealing, the grouping of the work into four packages, the trial timing and what happens if the checks fail.
- **Removed.** The unrequested proposal documents (the `proposal/` folder) and the copy of plan version 1, both moved to the Recycle Bin.
- **Added.** A day-by-day schedule (9.2) and a run sheet for 15 December (9.6).

**Version 2 (26 November 2026)**

- **Name.** FrostLine replaces "Before the Freeze" (13.1, row 17).
- **Decisions of 25 November 2026 added.** The ten named rules, the four rule details the group agreed, right and early warnings, the six additions and the live trial. They were on the explainer page but not yet in this plan.
- **New parts.** The evidence graph (3.7), the AI helpers (3.8), the live trial protocol (6.9), the live service (7.2), the dashboard design (7.3), a tool register with versions and licences (8.1 to 8.3), collaboration and `progress.md` (9.5), phases P10 to P13 (9.2) and a fifth work package, merged back into four in version 2.1 (9.3).
- **Stack changes.** Python 3.11 becomes 3.12, managed by uv with a lock file. The separate HDBSCAN package is dropped, because scikit-learn has HDBSCAN. SHAP becomes optional. marimo notebooks replace Jupyter except on Colab. pnpm with a release-age rule builds the dashboard. Dagster, MLflow, Ollama and LangGraph, already on the explainer page, are now in this plan.
- **Sealing.** Each list is sealed with a Merkle root instead of a plain file fingerprint (6.9). It is still one published fingerprint, but it lets us prove later that one frozen wallet was on the list without opening the rest.
- **Unchanged.** Every audited number, the leakage register, the comparison design, the four checks and the six verdicts.

---

## 1. The project, the research questions and the novelty

### 1.1 What we are building

Tether can freeze the USDT in any TRON wallet. We build an early-warning tool that looks at a wallet's public activity **before the public vote on its freeze** and reports how closely it resembles wallets that were later frozen. The tool also reports three things about itself:

1. **How early it works, and at what cost in wrong warnings** (D1).
2. **What kind of freeze it has learned to recognise** (D2).
3. **How easily a stranger could push an innocent wallet over the warning line** (D3).

From the analysis lock we seal one warning list a day and show which listed wallets Tether then freezes (6.9). The lists count as a live trial if the tool passes all four checks on past months (6.7); otherwise they are shown as a demonstration of the method. A live dashboard shows TRON as it happens, each new freeze as it happens, our results and the live lists (7.3), at the final presentation on 15 December 2026.

A freeze is the issuer's decision. The output is a resemblance score, not a finding of crime.

### 1.2 Research questions (from the brief, unchanged in meaning)

| RQ | Question |
|---|---|
| RQ1 | How different, before the freeze, is the observable activity of later-frozen wallets from that of comparable unfrozen wallets? |
| RQ2 | How early before a freeze, if at all, do those differences show up? |
| RQ3 | What groups or network structures do frozen wallets form, and do any match documented red flags? |
| RQ4 | How much of the "frozen" signal reflects sanctions-driven freezes rather than fraud or laundering, and what does that do to any conclusion? |
| RQ5 | What share of value reaches an apparent off-ramp before a freeze, and what can and cannot on-chain data say about the cross-border leg? |

### 1.3 The novel idea

Predicting Tether freezes on TRON is **not** new. Two groups already do it ([Zenodo 24031003](https://zenodo.org/records/24031003), the Early Detection dataset, and [FreezeCheck](https://freezecheck.org/en/methodology.html)), and a third says it tests something similar ([AMLBot](https://blog.amlbot.com/can-machine-learning-catch-criminals-before-the-blockchain-does-report/)). What we did not find in any tool or paper we read is a freeze early-warning tool that combines the design features below.

| # | Design feature | Zenodo 24031003 | FreezeCheck | [StableAML](https://arxiv.org/abs/2602.17842) (Ethereum) | AMLBot study | **Ours (planned)** |
|---|---|---|---|---|---|---|
| 1 | Information stops at the **public vote**, not at the freeze | No, cuts at freeze | No, one hour before the freeze | No pre-freeze cut found | Unknown | **Yes** |
| 2 | Comparison wallets chosen using only **what was known at that moment** | No | Not stated | No; also removes normals within 2–3 hops of illicit wallets | Unknown | **Yes** |
| 3 | **Wrong warnings at each lead time**, under a fixed warning budget | No, recall only | No. Recall at one hour, plus the flagged share of 287 other wallets at one date | No | Unknown | **Yes** |
| 4 | Results that respect **batch freezing** | No | Not stated | Not found | Unknown | **Yes** |
| 5 | Tests **what the label measures**, by freeze type and on independent court labels | Counts OFAC overlap; one run without released wallets | Coverage counts, no model test | Merges sanctioned with frozen | Unknown | **Yes** |
| 6 | Separates features a **stranger can write**, and measures the **cost to frame** an innocent wallet | No; 0.01 USDT dust filter | Partly, a dust rule | Not found | Unknown | **Yes** |
| 7 | Declines to score when history is too thin | No | Yes | Excludes low activity | Unknown | Yes (not novel) |
| 8 | Rules **locked first**, then **tested live** on days that had not happened yet | Not found | No. Its method page says its test is not a live forecast and was not registered in advance | Not found | Unknown | **Yes, if it passes the past tests** |

On the explainer page these features appear as **six additions**: before the vote (feature 1), honest (3), fair (2 and 4), clear (5), hard to trick (6) and tested live (8).

[MistTrack](https://misttrack.io/solutions/usdt-risk-screening.html) and [FreezeRadar](https://www.alchemy.com/dapps/freezeradar) are further comparators. MistTrack sells risk scores. FreezeRadar states that it does not predict freezes.

### 1.4 Why each gap matters

- **Feature 1.** TRON freezes run through a 2-of-3 multisig, so the target is public before the freeze. We matched 9,328 of 9,357 freezes to their votes; the other 29 date from 2020 and early 2021 [chain]. The median gap per freeze batch is 68 minutes: 103 minutes for 2024–25 batches and 23 minutes for 2026. (Per freeze, one 779-wallet batch distorts the figures: 64 minutes overall.) A model that cuts at the freeze has seen activity from after the target was public, and by a different amount in its learning and test years.
- **Features 2 and 3.** The Zenodo notebook picks normal wallets by activity on 11 fixed days up to September 2026, whatever their reference date. Its lead-time test reports recall only.
- **Feature 2, shown on the existing data.** In the Zenodo table's 2026 test rows, the average transfer size alone separates frozen from normal wallets with an AUC of 0.906, and the largest transfer alone with 0.909 [data]. In those rows the median average transfer is $26,040 for frozen wallets and $514 for normals. The two groups differ in size before any model is trained, so the reported 0.965 is measured against unlike wallets.
- **Feature 4.** 78% of frozen wallets sit in batches of five or more, with ten minutes or less between neighbours (73% if batches are formed by vote time), and one batch holds 779 [chain]. Treating wallets as independent makes results look more certain than they are.
- **Feature 5.** In one day, 447 wallets were released. 46 of 346 OFAC-listed TRON wallets (2024–26) were frozen more than a week before they were listed, 300 within two days, and none later [chain]. "Frozen" mixes several different events.
- **Feature 6.** On the genuine USDT contract, a stranger can write a zero-value "outgoing" transfer into anyone's history, including one that points at a frozen wallet [chain, read-only simulation].
- **Feature 8.** A test on past months can be tuned, knowingly or not, until it looks good. Locking the rules and then scoring days that had not happened yet removes that doubt for the days tested.

The closest method-level precedent is on Bitcoin. A re-test of [Elliptic++](https://arxiv.org/abs/2611.04000) found illicit F1 fell from 0.846 to 0.291 after removing future leakage. We found no equivalent for TRON freezes.

### 1.5 What is not novel, and we will not claim

Freeze labels, a time split, value weighting, GNN baselines, freeze-delay losses, sanctions coverage, escape-share figures, address-poisoning counts and declining thin wallets.

Also not new, and not claimed: sealing forecasts with OpenTimestamps and Bitcoin ([Gracia, 2026](https://arxiv.org/abs/2610.34245) already does it); the vote window as an event ([Wu et al., 2026](https://arxiv.org/abs/2603.27739) record it, and FreezeCheck publishes [proposal-window data](https://zenodo.org/records/24124768)); Merkle proofs ([RFC 6962](https://www.rfc-editor.org/rfc/rfc6962)); AI writing helpers; live dashboards.

### 1.6 How strong the novelty is

| Claim | Confidence that it is missing elsewhere | What would weaken it |
|---|---|---|
| Features 1, 3, 4 | Fairly high, within what we could read | A private vendor system, or the unpublished Zenodo paper, doing the same |
| Features 2, 5, 6 | Medium | Our search was wide but not exhaustive |
| Feature 8 | Medium | About ten days of live lists before 15 December is a short test, and few lists will be fully judged by then |
| Feature 1 changes results a lot | **Low; unknown** | Most wallets do not move money in the window. Correct practice either way |

Wording rule: "we found no published tool that does all of these", never "the first".

---

## 2. Data

### 2.1 Sources and licences

| Source | Used for | How obtained | Size | Licence or terms |
|---|---|---|---|---|
| [TronGrid API](https://www.trongrid.io/terms-of-service): USDT contract events | Freeze, release, destruction times | API, free key | about 11,700 events | Terms read (24 Sept 2026): no circumventing limits, no reselling, keys personal. Quotas vary |
| TronGrid API: multisig events | Vote times | API | about 23,900 events | Same |
| TronGrid API: live events and per-wallet USDT history | Live service (7.2); live-trial step 2 (6.9) | API, each member's own key | 200 events per page; see 7.2 and 6.9 for call counts | Same |
| [Zenodo 24031003](https://zenodo.org/records/24031003) | Benchmark to reproduce | Download | 2.8 MB | CC BY 4.0 |
| [BigQuery TRON tables](https://docs.cloud.google.com/blockchain-analytics/docs/schema) `bigquery-public-data.goog_blockchain_tron_mainnet_us.decoded_events` | All USDT transfers | Query | about 640 GB scanned per full pass (2.3) | Public dataset, Preview status, no service guarantee. 1 TiB a month free, then [$6.25 per TiB](https://cloud.google.com/bigquery/pricing). Google closed its older copy on 31 October 2026 and points users to this one |
| [OFAC mirror](https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses) and its daily history | Sanctions dates to about one day | GitHub | small | MIT for the tool; underlying list is published by OFAC |
| [UK Sanctions List](https://www.gov.uk/government/publications/the-uk-sanctions-list) | Sanctions wallets | Download | 50 MB | The page links Open Government Licence v3.0 |
| [EU consolidated list](https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions) | Sanctions wallets | Download | 25 MB | European Commission reuse notice |
| [OpenSanctions: Israel crypto wallets](https://www.opensanctions.org/datasets/il_mod_crypto/) | NBCTF order wallets with order dates | Download | 2.5 MB full file; we keep only wallets, order dates and status | [CC BY-NC 4.0](https://www.opensanctions.org/licensing/): non-commercial only |
| [Taiwan court labels](https://data.mendeley.com/datasets/62dmsngtfb/3) | Independent label test (D2) | Download | 130 KB | CC BY 4.0. Confirmed: 638 raw TRON wallets (478 fraud platform, 160 pseudo broker); victims' wallets are withheld by the authors |
| FreezeCheck data: [proposal window](https://zenodo.org/records/24124768), [groups](https://zenodo.org/records/24124771), releases and burns (DOI 10.5281/zenodo.24124777) | Cross-checks on our own registry | Download | about 1.4 MB | CC BY 4.0 |
| **F. Exchange wallet list (we build):** exchange proof-of-reserve pages and protocol documentation | Named hot wallets, bridges and swap contracts (RQ3, RQ5) | By hand, one public link per wallet | about 50 to 200 wallets | **To check per source** before use (P8) |

**Status on 24 November 2026:** every downloadable file above is in `data/raw` (about 81 MB). Checksums match the published values for the three Zenodo records we could compare. `data/raw/SOURCES.md` lists each source. Nothing has been queried in BigQuery.

Sources considered and rejected: [SQD public portal](https://docs.sqd.dev/en/portal/pricing.md), about 50 MB a month, too small; FreezeCheck's 71 million exchange labels, private.

### 2.2 The freeze registry

One row per wallet ever blacklisted. Fields:

| Field | Definition |
|---|---|
| Public vote **S** | Time of the **earliest** proposal to freeze the wallet, executed or not. This is the event time for the whole project. For 18 wallets an earlier, unexecuted proposal came first, by up to 34 days [chain] |
| Freeze time **F** | Time of the first `AddedBlackList` event |
| Gap | F minus S |
| Release time | First `RemovedBlackList`, if any |
| Destruction time | First `DestroyedBlackFunds`, if any |
| Batch | Votes joined when consecutive ones are 10 minutes apart or less |
| Origin flags | OFAC, UK, EU, NBCTF, with listing date where known |
| Voted only | Wallets in freeze proposals never executed. 134 proposals have no execution event; 95 of them are freeze proposals, and 44 of their targets were never frozen [chain] |

Rules: first freeze only (36 wallets were frozen more than once). Remove the USDT contract's own address, which is on the blacklist. Drop the 29 early events with no vote. Any wallet leaves the comparison pool at its first vote, executed or not.

**Acceptance checks.** The registry must reproduce: 8,017 events and 7,987 wallets to 12 August 2026 (Bitquery); 8,206 still frozen on 8 November (FreezeCheck); 4,221 events in FreezeCheck's window; 447 releases on 14 May 2026. All four were reproduced in the audit.

### 2.3 Wallet universe and the transfer pull

- **Contract filter:** only transfers of contract `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`. Counterfeits never enter.
- **Window:** 1 January 2024 to 31 October 2026. The held-out check (6.9) needs a second pull, from 1 November to the lock, made only after the lock.
- **Seed wallets, fixed before the pull:**
  1. every wallet in the freeze registry;
  2. every wallet on the sanctions and court lists, frozen or not;
  3. the 9,249 normal wallets of the Zenodo table, so the waterfall (6.1) can recompute them;
  4. a **hash sample** of all other wallets. A wallet is in or out by a fixed hash of its text, so selection cannot depend on activity or time.
- **What the pull returns:** all transfers of seed wallets, plus a monthly summary for each direct recipient of a frozen wallet's outflow (total in, total out, largest recipient and its share), needed for RQ3 and RQ5. **Output guard:** any wallet-month with more than 5,000 transfers comes back as a monthly summary only. Without this, one exchange hot wallet in the hash sample could return tens of millions of rows.
- **Very busy wallets (agreed 25 November 2026):** wallets that behave like services at time t are left out of both groups in the same way: over 1,000 distinct counterparties in 90 days, or over 5,000 transfers in 30 days. Repeated with half and double (6.5). We report how many frozen wallets this removes.

**Query size, stated in advance**

| Step | Expected scan | Share of one free month | Basis |
|---|---|---|---|
| Dry runs | 0 | 0% | [Google: dry runs are not charged](https://docs.cloud.google.com/bigquery/docs/running-queries) |
| Sizing query, one month | about 19 GB | about 2% | 631 GB over 34 months |
| Main pull | about 640 GB | about 58% of 1 TiB | The notebook printed 631 GB (213.9 GB for 2024, 230.9 GB for 2025, 186.1 GB for 2026), before October 2026 was complete |
| Held-out pull, 1 November to the lock, run after the lock (6.9) | about 21 GB | about 2% | About 0.6 GB per day of data |
| Live lists: one screen a day from the lock, plus two rehearsals (6.9) | about 55 GB | about 5% | About 4.3 GB per run (7 days of data); stated again before the first run |
| **Total planned** | **about 735 GB** | **about 67%** | If all of it fell in one month. If the main pull runs by 30 November, November uses about 660 GB and December about 76 GB |

⛔ **The main pull runs only after the dry-run figure is shown to the user and approved.** A per-query byte cap and a project daily quota are set first. A second full pass in one month would cost about $3 to $4.

**Sandbox limits.** The [sandbox](https://docs.cloud.google.com/bigquery/docs/sandbox) gives 10 GiB of storage **for life**, not refunded on deletion, and tables expire after 60 days. We expect 3 to 5 GB of output, so there are only two or three attempts. The hash rate defaults to 0.5% of wallets (1 in 200), about 23 million rows before the output guard, because the 1-in-25 line in 6.7 needs enough sampled wallets to be measured. The sizing query confirms the rate and tests the download route before the main pull.

**One account only.** [Google's terms](https://cloud.google.com/terms) forbid multiple accounts used to act as one to avoid fees or quotas. The BigQuery project lives on the master laptop (9.5).

**Fallback without BigQuery ("TronGrid mode").** Pull each frozen wallet's transfers by API. Build the comparison frame from wallets seen in randomly chosen past blocks, with weights. Rough size: 100,000 calls. It works but loses the clean hash sample.

### 2.4 Cleaning planted transfers

Applied to frozen and comparison wallets alike, before any feature is computed.

| Transfer type | Treatment | Why |
|---|---|---|
| Zero-value, any direction | Removed from features, edges and balances; counted separately | Anyone can write them [chain] |
| Inbound up to 10 USDT from a wallet that, **by time t**, has never sent more than 10 and has not been paid by the wallet | Removed from the "clean" version; kept in the "full" version | Current lures are typically 1 to 5 USDT ([FreezeCheck](https://freezecheck.org/research/poisoning-losses-en.html)); the 0.01 filter caught 413 of 1,880 small deposits in our two samples [chain] |
| Same, where the sender's first two characters after T and last four copy a real counterparty | Also flagged "lookalike" | Poisoning marker |
| Other tokens, including counterfeit USDT | Never loaded | Contract filter |

The 10 USDT line is a choice. Results are repeated at 1 and 100 USDT.

### 2.5 Comparison wallets

We use **risk-set sampling**: at the exact calendar moment of a frozen wallet's observation, we draw comparison wallets from those **active then and not yet voted on then**. A wallet voted on later may serve as a comparison earlier, because nobody could have known. Nothing after time t is used to choose anyone. Set A comes only from the hash sample, so list, court and Zenodo seeds cannot enter it unless the hash picks them; each sampled wallet stands for 200 real ones at a 0.5% rate.

| Set | Drawn from | Answers |
|---|---|---|
| **A: population** | Hash-sample wallets with a real transfer in the 30 days before t; about 20 per frozen wallet | Real-world wrong warnings; weights restore true prevalence |
| **B: look-alike** | Set A, matched on days since last transfer, number of transfers, size and first-seen month (coarse bands, all measured at t); about 5 per frozen wallet | RQ1's "comparable wallets". Differences in the matched variables are reported against Set A only |
| **C: neighbours** (stretch) | Direct counterparties of frozen wallets, not voted on by t. Needs a second pull | Hardest test |
| **Z: legacy** | The Zenodo normals, unchanged | Reproducing the benchmark only |

**Set aside, and counted openly (agreed 25 November 2026).** At each moment t, a wallet with fewer than 3 real payments so far, or with no real payment in the 30 days before t, gets "not enough history" and is not scored. This applies to later-frozen and comparison wallets alike. Later-frozen wallets set aside count as misses in the main results and are also reported apart (6.2).

### 2.6 Time handling and the leakage register

**Eight moments.** Each frozen wallet is observed at S minus 1 hour, and 1, 3, 7, 14, 30, 60 and 90 days before S. Comparison wallets are observed at the same calendar moments. Features use trailing windows of 7, 30, 90 and 180 days.

**Left edge.** Data start on 1 January 2024. Frozen wallets voted on before 1 July 2024 are used only for description, so the moment nearest the vote always has 180 days of history. Earlier moments of wallets voted on in the second half of 2024 may have less. There the 180-day window is cut to what exists, the same cut is applied to their comparison wallets, and a test without them is reported.

| # | Leak | Rule |
|---|---|---|
| L1 | Activity after the vote became public | Cut at S minus 1 hour at the latest |
| L2 | Deposits arriving after a freeze | Excluded by L1 |
| L3 | Comparison wallets chosen by later activity | Hash sample plus risk set |
| L4 | "Never frozen" judged today | Judged at t, from the first vote, executed or not |
| L5 | Neighbour labels from later freezes | A neighbour counts as frozen only if frozen before t |
| L6 | Release or destruction flags | Never a feature |
| L7 | Exchange, sanctions or scam tags added later | Dated tags used only after their date; undated tags for description only |
| L8 | Future graph edges | Graph rebuilt at each t, through the as-of filter (3.7) |
| L9 | Scaling, tuning or early stopping on test data | Fitted on Learn data; tuning on Tune data |
| L10 | Address format (`T…` against `0x…`) and helper columns | One format; helper columns dropped on load |
| L11 | Batch siblings in both Learn and Test | Batches never split |
| L12 | Voted-but-unexecuted wallets as normals | They leave the pool at their vote, not before |
| L13 | Balance at freeze as a shortcut | Reported with and without (3.2) |
| L14 | Choosing the analysis after seeing test results | Analysis lock (6.6) |

Batches may still share an operator, so confidence intervals are also repeated with network communities as the resampling unit. Each rule gets an automated check in the build, run as a blocking Dagster asset check. A single failure stops the run.

### 2.7 Splits, with real counts

All frozen wallets by vote date [chain]. Usable numbers will be lower: of 8,273 wallets frozen from January 2024 to 14 October 2026, where the Zenodo table ends, it lacks 1,061 (13%) [data], and FreezeCheck could not judge 27 of 150.

| Split | Vote dates | Wallets | Batches | Later released | Destroyed | OFAC-listed | Largest batch |
|---|---|---|---|---|---|---|---|
| Description only | before 1 Jul 2024 | 1,046 | 285 | 117 | 399 | 15 | 114 |
| **Learn** | 1 Jul 2024 – 30 Sep 2025 | 3,701 | 592 | 197 | 517 | 69 | 779 |
| **Tune** | 1 Oct – 31 Dec 2025 | 573 | 137 | 46 | 167 | 33 | 36 |
| **Test** | 1 Jan – 31 Oct 2026 | 3,794 | 758 | 643 | 163 | 229 | 173 |
| **Held out**, not touched | 1 Nov 2026 to the day before the analysis lock | 178 to 23 Nov | 58 | 0 | 0 | 6 | 17 |
| **Live lists** | Daily from the lock (target 4 December 2026) to 14 December, each judged for 30 days (6.9) | – | – | – | – | – | – |

- A recount in the 25 November audit gave 591, 137 and 759 batches for Learn, Tune and Test. The difference comes from batches near a split boundary. P1 fixes the rule (a batch belongs to the split of its first vote, so L11 holds) and updates this table.
- The 779-wallet batch of 12 July 2025 is 21% of Learn wallets by count, but 718 of them are absent from the Zenodo table, and all 45 we sampled (25, then 20 afresh) had **no USDT transfer** before the freeze; only 2 of the last 20 had ever been activated on TRON [chain]. They cannot be warned about from USDT activity, so they leave the model and stay in the coverage count. The next largest Learn batches have 144 and 95 wallets. A batch's total learning weight is capped at that of 25 wallets.
- **Coverage ceiling.** Frozen wallets with no earlier USDT activity are reported separately as "not warnable". Early-warning results are given twice: among warnable wallets, and among all freezes.
- 447 of the Test wallets were mass-released on 14 May 2026; 352 were voted on in Q1 and 95 in Q2. Test results are shown with and without them, and by quarter.
- Every Test moment, even at 90 days, falls after Learn ends on 30 September 2025. A comparison wallet is used in one split only. A wallet that was a comparison in Learn and was voted on later stays in Test, because removing it would use the future; we report how many there are.
- Some freeze types are small (69 OFAC-listed and 429 listed on any of the four lists in Learn), so D2 intervals will be wide.

### 2.8 Data quality checks

Reconstructed balances against Tether's published destroyed amounts (Bitquery reports over 99% match with this method); no transfer after t; row counts by month against the sizing query; duplicate transfer check; a 200-row spot check against TronGrid; and a check of the 1,061 wallets frozen since 2024 that the Zenodo table lacks. So far they look explained: 718 are the July 2025 batch (above); of 40 others sampled, 20 had no USDT transfer before the freeze and 20 had only pre-2024 transfers. We found no sign that the table misses transfers [chain]. Every check is a Pandera schema or a blocking Dagster asset check.

---

## 3. Features and methods

### 3.1 Features, all computed at time t

| Group | Examples | Red flag link | Who can write it |
|---|---|---|---|
| Size | Inflow, outflow, median and largest transfer | | Mixed |
| Tempo | Transfers per day, bursts, longest silence | FATF Annex A T2, T15 | Mixed |
| Dwell time | Hours between money arriving and leaving | T4, rapid in and out | Owner for outflow |
| Pass-through | Outflow over inflow in each window | T4 | Mixed |
| Counterparties | Number of senders and receivers, concentration, share that are new | T2, T3 | Senders: stranger. Receivers: owner |
| Life cycle | First-seen month, time dormant, sudden activation | T16, A2 (part) | Mixed |
| Round amounts | Share of transfers in round hundreds | | Mixed |
| Local network | Share of counterparties already frozen at t, reciprocity, shared funders | | Partly stranger |
| Planting exposure | Zero-value and lookalike counts | | Stranger. **Diagnostics for D3 only, not used for scoring** |

Local-network features read the evidence graph's as-of facts (3.7), so "already frozen at t" is enforced in one place.

**180 days at most.** Every feature uses only the 180 days before t; life-cycle features such as first-seen and time dormant are capped at 180 days. The live pipeline (6.9) reads exactly 180 days of history, so it computes the same features the model learned from.

**Writability classes (the core of D3)**

- **Owner-signed:** non-zero outflows. In our two samples 52 of 53 were signed by the wallet itself [chain]. Approvals and permission changes explain exceptions, so we test 300 more.
- **Paid-in:** inbound above the threshold. A stranger can write it, but must spend real money.
- **Free-to-write:** zero-value records and small inbound. Nearly free.

Three model versions: **Full**, **Clean** (free-to-write removed) and **Owner-only**.

### 3.2 Balance and pass-through

Frozen wallets often still hold money, and the issuer may choose them for that, so balance at freeze partly describes the issuer's choice. The Zenodo authors drop balance but keep inflow and outflow, which rebuild it. We report every headline result twice: with balance-type features, and without balance, net flow and full-history pass-through. Windowed pass-through at seven days or more before S is kept in both, because rapid in-and-out is a documented red flag.

### 3.3 Models and baselines

| Level | Model | Why |
|---|---|---|
| 0 | Random ranking; activity-only ranking | Floor |
| 1 | Red-flag checklist from FATF Annex A, testable items only | What a supervisor could use today |
| 2 | Logistic regression (scikit-learn) | Simple and explainable; FreezeCheck's choice |
| 3 | Decision trees, gradient boosted (LightGBM) | Main candidate |
| 4 | Neural network (small multilayer perceptron, PyTorch) | Course topic; compared on equal terms |
| 5 | GraphSAGE, time-respecting (PyTorch Geometric, on Colab) | **Kept only if it helps.** Rule: on Tune data, its AUPRC at seven days must beat LightGBM with the lower bound of the paired batch bootstrap above zero. If not, it is reported as tested and dropped. Trees beat GNNs in StableAML and in one [Elliptic re-test](https://arxiv.org/abs/2604.19514) |

**Which model is kept (agreed 25 November 2026).** The model with the most right warnings on the Tune months, at the line of 1,000 warnings a month, is kept. GraphSAGE must also pass its own rule above. The choice is made and written into the analysis lock before any Test score (6.6). Explanations for tree models use LightGBM's built-in feature contributions; the SHAP package is optional, for plots only.

Unlabelled wallets are not proven clean. We follow [this warning](https://arxiv.org/abs/2303.02462) and repeat key metrics assuming 0.1% and 1% of comparison wallets are hidden positives.

### 3.4 Network analysis (RQ3, RQ5, supporting)

- **Graph:** wallets as nodes, cleaned transfers as dated edges, frozen wallets plus one hop, built from the evidence graph (3.7) at each t.
- **Measures:** in and out degree, reciprocity, concentration, shared funders, distance between frozen wallets.
- **Communities:** Louvain from NetworkX. Leiden packages are GPL, so they stay optional. NetworKit (MIT) is used only if NetworkX is too slow on the full one-hop graph.
- **Campaign test:** do freeze batches match communities better than chance, against a shuffled baseline that keeps batch sizes?

### 3.5 Cluster analysis

Standardised features of later-frozen wallets, grouped with k-means and HDBSCAN (both in scikit-learn), reported with stability across resamples. Each cluster gets a plain behavioural description, never a crime label. Clusters are then compared with freeze type (D2). The dashboard's 2-D map of frozen wallets (7.3, scene 6) uses UMAP if it installs cleanly, otherwise t-SNE from scikit-learn; the map is a picture, never an input to a result.

### 3.6 Course topics

| Course topic | Where it is used |
|---|---|
| Prevention and analytics, the fraud cycle | 1.1 and 5.3: detection before the freeze; preventing false accusation by planting |
| Process model | 9.2: build phases follow problem, data, cleaning, analysis, evaluation, use |
| Data collection and sampling | 2.2 to 2.5: registry, hash sample, risk-set controls |
| Types of data, exploration | 2.8, 4 (RQ1): transfers, events, lists, graph |
| Descriptive statistics | RQ1 effect sizes; gap and batch tables |
| Descriptive analytics for fraud detection | RQ1, RQ4 composition; the dashboard's results scenes (7.3) |
| Cluster analysis | 3.5 |
| Neural network methods | 3.3, levels 4 and 5 |
| Social network analysis | 3.4 measures; 3.7 evidence graph |
| Network methods for fraud analytics | 3.4 communities and campaign test; GraphSAGE |

### 3.7 The evidence graph (a small knowledge graph)

We looked at whether a knowledge graph would help, and we use one only where it does real work. It is a set of **dated facts** about wallets, stored as two DuckDB tables. There is no graph database.

| Part | What it holds |
|---|---|
| Nodes | Wallet (internal ID), freeze batch, public vote, list entry (OFAC, UK, EU, NBCTF), court label, exchange or service label (list F), daily sealed list |
| Edges | paid (daily totals, cleaned), paid by a stranger (free-to-write records, kept apart), in the same batch, listed on, labelled as, looks like (lookalike sender), warned in (sealed list; master laptop only) |
| On every fact | `known_from` (the first moment the fact was public), source (file or link, with its SHA-256), run ID |

It has three uses, and only these:

1. **One rule for "known at time t".** Every query goes through one as-of filter (`known_from` ≤ t). The local-network features (3.1), the off-ramp work (RQ5) and leakage checks L5, L7 and L8 use it, so the rule lives in one place and gets one test.
2. **Facts for the AI helpers.** The fact finder (3.8) may read only `facts_as_of(wallet, t)`. Every sentence in a note points to a stored fact with its source, and the number check compares against these facts.
3. **The evidence view.** For wallets Tether has frozen, the dashboard shows the as-of graph around them with a date slider (7.3, scene 9). Never for other wallets.

**Options looked at and not used**

| Option | Why not |
|---|---|
| A graph database: Kuzu, its forks, Neo4j | Kuzu's repository was archived in October 2025; its last release, 0.11.3, came out on 10 October 2025. The forks are very new (`ladybug` 0.23.0 was released on 25 November 2026). Neo4j needs its own server. Our graph fits in DuckDB tables |
| [DuckPGQ](https://duckdb.org/community_extensions/extensions/duckpgq) (graph queries inside DuckDB) | A community extension; from DuckDB 2.0 its grammar must be switched on with a setting. Our one- and two-hop questions are plain SQL joins |
| RDF and SPARQL (rdflib 7.6, pyoxigraph 0.5) | Built for linked web data, not dated payments |
| An AI model that builds the graph from text ("GraphRAG") | Our facts are already structured. A model would only add errors |

Graph algorithms run in NetworkX on subgraphs exported from DuckDB.

### 3.8 AI helpers (short notes in plain words)

Numbers alone are hard to read, so three AI helpers turn the facts of one case into a short note. They run on the laptop with Ollama. No data leaves the laptop, and no paid service is used.

| Step | Who | Limits |
|---|---|---|
| Fact finder | AI helper | Reads only `facts_as_of` and the result store. No internet, no addresses (internal IDs only), cannot change a number |
| Doubter | AI helper | Argues against the score: planted junk, thin history, very busy, batch effect |
| Writer | AI helper | Writes 80 to 150 words with both sides, following the wording rules (10.2) |
| Number check | Normal code | Every number and date in the note must match a stored fact. A mismatch sends the note back. After two failed tries a fixed template is used |
| Person | One of us | Reads every note and says yes or no |

- **LangGraph** runs the steps: who speaks next, the two tries, and a stop that waits for the person.
- **Model.** Default: Qwen3 4B (2.5 GB in Ollama; [Apache-2.0](https://huggingface.co/Qwen/Qwen3-4B); Ollama lists tool calling and thinking for it). Candidates: Qwen3.5 4B (3.3 to 4.0 GB in Ollama; [Apache-2.0](https://huggingface.co/Qwen/Qwen3.5-4B)) and Gemma 4 E2B or E4B ([Apache-2.0](https://huggingface.co/google/gemma-4-E4B-it); the smallest Gemma 4 download listed by Ollama is about 4.6 GB). In P9 each candidate writes the same 20 notes. We keep the one with the fewest number-check failures that writes a note in under a minute on the master laptop. Each download needs your OK first.
- **Where notes appear.** (a) Frozen wallets shown on the dashboard, from public facts only. (b) Internal review of trial warnings, kept with the sealed list on the master laptop. A note never shows a score for a never-frozen wallet outside the team.
- The helpers explain results. They never produce one, and they are not a novelty claim.

---

## 4. How each research question is answered

### RQ1. How different?

- **Analysis:** later-frozen wallets against Set B (and Set A for context) at each moment. Matched-set logistic regression and effect sizes.
- **Metric:** standardised difference per feature with batch-level 95% intervals, and false-discovery control at 5% across features. Combined: AUROC and AUPRC of the Clean model against Set B.
- **Negative result:** most differences vanish against Set B. Reading: earlier contrasts came from comparing with unlike wallets.

### RQ2. How early?

- **Analysis:** lead-time curves at the eight moments, and a **calendar replay** that scores all active wallets every day of the Test months, without knowing who will be frozen, in the same rhythm as the live lists (6.9). A wallet goes on a day's list only if it was not on a list in the previous 30 days.
- **Right and early (agreed 25 November 2026).** Each warning on each scoring date is judged on its own: it is **right** if the public vote on that wallet starts within 30 days after the warning, and wrong otherwise. A vote counts as **caught** if the wallet was warned in the 30 days before the vote, and as **caught early** if it was warned at least 7 days before the vote; the lead time is measured from the earliest warning in those 30 days. The four checks (6.7) use early warnings. A vote that never leads to a freeze is listed separately. The same rules apply to past months and to the live trial (6.9). This replaces version 1's day-7-to-day-6 rule.
- **Metric:** recall at one right warning in 25 checks, recall at fixed false-alarm rates (0.01%, 0.1%, 1% of active wallets), precision at true prevalence, and USDT still in the wallet when first warned. Shown twice: all wallets visible at that lead time, and a **fixed cohort** visible at 90 days, so survivors do not flatter the curve.
- **Useful, by our pre-set test:** section 6.7. The headline number is the share of later-frozen wallets warned early while a reviewer checks no more than 25 warnings per right one, at the network's real mix, with the line at 1,000 warnings a month.
- **Negative result:** early recall is no better than the checklist. Reading: the signal is mostly the issuer acting on wallets already under way.

### RQ3. What networks, and which red flags?

- **Analysis:** section 3.4, plus red-flag prevalence in frozen wallets against Set B.
- **Coverage:** FATF Annex A lists 40 indicators (our count). Numbering them T (transaction), A (anonymity) and F (terrorist and proliferation financing) within Annex A, we can test five from transfers alone (T2, T3, T4, T15, T16) and up to five in part if service labels exist (A2, A3, A8, A9, A10). The rest need customer, device or cash data. Case Study E of the [UAE supervisory paper](https://www.centralbank.ae/media/z02hk1ct/jointp-3.pdf) is now read: its red flags are high-velocity USDT on TRON, rapid movement between wallets and an immediate off-ramp attempt. We can test the first two, and the third only where a service label exists. Its section 3.1 asks for velocity and chain-hop thresholds, which RQ3 can inform.
- **Metric:** odds ratios with batch-level intervals; batch-to-community agreement against the shuffled baseline.
- **Negative result:** communities do not match batches, or red flags are as common in Set B.

### RQ4. How much is sanctions?

- **Analysis:** section 5.2.
- **Metric:** share of freezes matched to dated public lists, given as a range; change in AUROC when a type is removed; learn-on-one-type, test-on-another grid.
- **Negative result:** the model works only on the sanctions-linked type, or fails on court-named wallets. Reading: it learns issuer action more than fraud-like behaviour. This is the most important honest finding the project could produce.

### RQ5. What reaches an off-ramp?

- **Analysis:** destinations of pre-vote outflow at one hop, and two hops through deposit-like wallets. A deposit-like wallet sends at least 90% of a month's inflow to one wallet in that month. Named services come from our exchange wallet list F (2.1), each entry with a public link.
- **Metric:** lower bound (named service), upper bound (named plus deposit-like unnamed), and unlabelled share; by wallet and by value, with the ten largest wallets shown separately because they dominate totals.
- **What the chain cannot say:** country, owner, payout, or whether a deposit was cashed out. No cross-border claim is made.
- **Negative result:** the range is too wide to be useful. That is reported as the answer.

---

## 5. Label noise, the sanctions confound, and fake or planted tokens

### 5.1 Label noise

- Main label: voted on and then frozen. Released wallets stay in the main test, because nobody knew at the time.
- Every headline result is repeated without released wallets, without the 14 May block, and only on wallets later destroyed (stronger but rarer).
- Released is **not** read as innocent, and destroyed is **not** read as guilty. Bitquery calls released wallets a false-positive population. That is their inference; 44% of all TRON releases happened in one evening [chain].

### 5.2 The sanctions confound (D2)

Each freeze gets one **origin** and one **outcome**, kept apart:

| | Value | Rule |
|---|---|---|
| Origin | OFAC | On OFAC, with listing date from the mirror's history: frozen more than a week before, within two days, or later |
| Origin | Other list | UK, EU or NBCTF, with order date where known. NBCTF orders get renewed, so the first order may be missing |
| Origin | On none of the four lists | Not the same as "no public reason": US forfeiture complaints, court papers and press releases are not covered |
| Outcome | Released | Any `RemovedBlackList`; mass block flagged |
| Outcome | Destroyed | Any `DestroyedBlackFunds` |
| Outcome | Still frozen | Neither |

Steps:
1. Composition by quarter, against known regime changes: OFAC auto-freezing from December 2023 ([BlockSec](https://blocksec.com/blog/1-26-billion-frozen-usdt-blacklisting-on-ethereum-and-tron-in-2025)); the 12 July 2025 batch; the March–April 2026 wave and its release; the [reported end of T3](https://cointelegraph.com/news/tron-tether-chainalysis-cybercrime-task-force-laundering) in August 2026.
2. A grid: learn on each origin, test on every other; the same for outcomes.
3. Leave-one-out results for each origin and outcome.
4. **Court-label test.** Score Taiwan court-named wallets against Set B-style wallets at the same moments. Of 638 raw wallets, 212 were active on or after 1 July 2024 and 129 were first seen after it; only 2 were ever frozen [data]. The data omit case dates, so we score each wallet on the first of every month in which it was active in the previous 30 days, with no hindsight about its first or last activity. If fewer than 150 survive cleaning, this becomes a description with no claim. The authors call their labels judicially documented, not infallible.

**What the lists cover now [data].** OFAC 352, UK 49, EU 3 and NBCTF 688 TRON wallets (590 under active orders); 1,038 distinct, of which 993 were ever frozen. All US, UK and EU wallets are frozen; 45 NBCTF wallets never were. The lists match 10.7% of ever-frozen, 11.9% of still-frozen wallets and 11.7% of the Zenodo frozen wallets. So about nine freezes in ten are on none of these four lists, and RQ4 gives a range. 2023 OFAC dates in the mirror are unreliable and excluded. None of the 9,249 Zenodo normals is on these lists, and none has been frozen since.

### 5.3 Fake and planted tokens (D3)

| Reading | Risk to us | Handling |
|---|---|---|
| **Counterfeit USDT** | Low. 16 transfers in 4 of 133 sampled wallets [chain] | Contract filter. Freeze events come from the same contract, so labels cannot be counterfeit |
| **Planted transfers** | Real. 70 of 133 sampled wallets had lookalike senders; 39 had zero-value outgoing records; all 37 we checked were signed by someone else [chain] | Cleaning (2.4), writability classes (3.1), cost-to-frame test |
| **Real tokens, fake meaning:** hijacked wallets, self-dealing, deceptive tags | Real but unmeasured. [Bitquery](https://bitquery.io/investigations/tron-permission-changes) found 3,776 funded wallets no longer answering to their original key | Stated limitation. "Owner-signed" means signed by the wallet's valid key, not by its owner |

**Cost-to-frame test.** Take comparison wallets below the warning line. In a copy of the data, add records that a stranger could write, and recompute the score. Families: zero-value records, including ones pointing at frozen wallets; small deposits; larger deposits. Budgets: fees only, 10, 100, 1,000 and 10,000 USDT. Report, for Full, Clean and Owner-only, the share pushed over the line and the median cost.

Rules: simulation only; nothing is ever sent on-chain; results in aggregate; no step-by-step method published; no test of how a frozen wallet could hide. Simulated records never enter learning.

**Success:** Clean or Owner-only cuts the share framed at 100 USDT by at least half, for a small loss in recall. **Negative result:** no version resists, which we report as a warning about this whole class of tool.

**Labels.** Planting would affect labels only if it led Tether to freeze someone. We found no confirmed case. We found reported harm at exchanges ([Kraken](https://www.unlock-bc.com/en/kraken-dust-attack-tests-crypto-sanctions-compliance), August 2026) and on Ethereum ([12 ETH tainted over 9 million ETH](https://arxiv.org/abs/2507.11721)).

### 5.4 What stays a limitation

Deliberate large payments look like ordinary ones. Planting before 2024 is invisible to us. Our 10 USDT line can be outspent. Hash sampling cannot find every coordinated wallet. The live lists before 15 December cover only about ten days.

### 5.5 Our own measurements and their limits

| Measurement | Limit |
|---|---|
| Freeze, release and destruction counts | Full census to the end of 23 November 2026, 11,673 acts. On 24 November our total to 02:43 UTC, 11,679, matched [StableScan](https://stablescan.achivx.com/tron/freezes) exactly |
| Multisig | Read on chain: 3 owners, 2 signatures required, and it owns the USDT contract |
| Vote gap | Reported per batch, because two large batches cause most gaps over a day. 52% of batches waited over an hour, 4% over a day |
| OFAC dating | The mirror updates nightly and had no gap we could find. Accurate to about two days, so we use a one-week margin. 2023 unreliable |
| Planted-transfer samples | Two independent samples, 75 and 59 wallets drawn, 133 with history; one per batch; last 200 transfers before S; strict lookalike rule; not representative |
| Contract simulations | Read-only; nothing broadcast; a handful of wallets |
| Live volume | About 1,700 USDT transfers a minute in three samples on 25 and 26 November 2026 (1,163, 2,260 and 1,617); one page of 200 covered 6 seconds on 26 November. Varies by hour |
| Block time | 3.0 seconds on average over 1,000 blocks read on 26 November 2026 |

Scripts used for these were temporary. All were recomputed with newly written scripts in the audit, and will be rebuilt in P1 of the build.

---

## 6. Evaluation

### 6.1 The AUC waterfall

Start from the Zenodo table, features and split, then change one thing at a time:

1. Reproduce the reported AUC (0.965 claimed; the summary file is typed by hand, so this is unconfirmed).
2. Remove features that rebuild the balance.
3. Cut at the public vote.
4. Clean planted transfers.
5. Replace normals with Set A, then Set B.
6. Cap batch weight.
7. Move to seven and thirty days before.

Steps 1 and 2 use only the 2.8 MB download. Because order matters, each change is also tested alone. Steps 3 to 7 need the main pull, including the Zenodo normals (2.3).

### 6.2 Measures

AUROC and AUPRC; recall at 1-in-25 yield and at 0.01%, 0.1% and 1% false-alarm rates; precision at true prevalence using sampling weights; precision in the top 100, 500 and 1,000; value reached, with the ten largest wallets shown separately; calibration curve and Brier score. Wallets set aside for thin or silent history (2.5) get "not enough history"; recall is reported with them left out and counted as misses. Results are shown at the main line of 1,000 warnings a month and also at 100 and 500.

### 6.3 Early, not just near the freeze

Every headline is shown at all eight moments and in the calendar replay. A result that holds only at S minus 1 hour is reported as "near-freeze only".

### 6.4 Uncertainty

Bootstrap over **batches**, 1,000 resamples, 95% intervals; paired bootstrap for model comparisons; results by wallet and by batch. Five seeds for neural models. Results by quarter, as regimes changed.

### 6.5 Robustness

Cleaning line at 1, 10 and 100 USDT; batch gap at 10 and 60 minutes; very-busy limits halved and doubled; with and without the 779 batch, the 14 May block and the 25 March to 2 April wave; three Learn start dates.

### 6.6 Analysis lock

Before any Test score is computed, the group writes a dated lock file listing the ten rules, features, models, the kept model, the warning line, the live-scoring screen (6.9), metrics, thresholds and success rules. The lock file is fingerprinted with SHA-256 and time-stamped with OpenTimestamps; the trained model file is fingerprinted too, stays with the team, and a reviewer can check it. Later changes are listed as exploratory. The lock comes before any Test work in P5 to P8; its target date is 4 December 2026. Data from 1 November 2026 onward stay untouched until the lock; they are then pulled and scored once, as the held-out check (6.9; 178 frozen wallets to 23 November).

### 6.7 The usefulness test: four checks

An earlier draft used "25% recall at a 0.1% false-alarm rate". That bar is easy to attack. About 370 wallets a month were frozen in 2026 [chain], against a reported [10 million or more monthly active stablecoin users on TRON](https://invezz.com/news/2026/02/10/the-state-of-tron-h2-2025-stablecoin-settlement-at-scale-amid-rising-competition/) (sponsored report; our sizing query will measure it). That is roughly 1 in 27,000. At a 0.1% false-alarm rate there would be about 10,000 wrong warnings a month, so even a model that caught every case would be right about 3.6% of the time. This is the [base-rate problem](https://www.cerias.purdue.edu/apps/reports_and_papers/view/2815).

**The warning line.** It is set on the Tune months so that, scoring every day and listing a wallet again only after 30 days, about 1,000 new warnings a month come out, network-wide: about 33 a day, or 45 a working day, which a small team can read. The network-wide count is estimated from the hash sample with its weights. Results at 100 and 500 a month are shown too.

All four checks are made at seven days before the vote (with early warnings wherever warnings are counted), and all are fixed before testing.

| Check | Question | Pass rule |
|---|---|---|
| **1. Real** | Is there any signal against comparable wallets? | AUROC against Set B beats the best single number (such as transfer size): lower 95% bound of the paired difference above zero, and p below 0.01 in a test that shuffles labels by batch |
| **2. Better** | Does it beat what a supervisor could do today? | At the same workload (1,000 warnings a month, network-wide), it catches more later-frozen wallets early than the checklist and the best single number; lower bound of the paired difference above zero |
| **3. Useful** | Would a reviewer accept it? | Positive [net benefit](https://pmc.ncbi.nlm.nih.gov/articles/PMC2577036) at a 4% threshold, at true prevalence, with the lower 95% bound above zero; shown across 1% to 10% |
| **4. Strong** | Does it survive the known traps? | Checks 1 and 2 also hold without released wallets, without listed wallets, without the largest batches, without balance features, on the Clean version, and in at least three of the four Test quarters |

**Why 4%, or 1 in 25.** Nineteen US banks reported about 16 million alerts and over 640,000 suspicious activity reports in 2017 ([Bank Policy Institute](https://bpi.com/getting-to-effectiveness-report-on-u-s-financial-institution-resources-devoted-to-bsa-aml-sanctions-compliance/)). That is 4% by our arithmetic. It is the yield banks already work with, so it is an outside reference, not our choice. It is a US bank figure from 2017, and several alerts can end in one report, so we show the whole 1% to 10% range.

**Why seven days.** [Bitquery](https://bitquery.io/investigations/tether-blacklist-audit) finds that on Ethereum a freeze within an address's first week kept 59 cents per dollar received, against 12 after 180 days; TRON loses more at every point. It says four in five freezes come more than a week after the address first received funds. Our own check of the Zenodo table, for TRON, gives 77.5% (81.2% in 2026), counting from the first transfer since 2024 [data].

**Six verdicts, fixed in advance** (the same sentences as on the explainer page)

| Result | Verdict we will report |
|---|---|
| Check 1 fails at every lead time | No early warning found. |
| Check 1 passes only under seven days | It only works in the last seven days before the vote. |
| Check 1 passes at seven days, check 2 fails | It is real, but no better than a checklist. |
| Checks 1 and 2 pass, check 3 fails | It is real and better, but not useful at this scale. |
| Checks 1 to 3 pass, check 4 fails | It is promising, and we name the check that failed. |
| All four checks pass | Useful early warning. |

Read the table from the top; the first row that fits is the verdict. Precision measured this way is a **lower bound**, because some unfrozen wallets may later be frozen or may be unknown cases.

### 6.8 Checklist against ten known pitfalls

[Arp et al. (USENIX Security 2022)](https://arxiv.org/abs/2010.09470) list ten pitfalls of machine learning in security. A challenger is likely to start here.

| Pitfall | How this project answers it |
|---|---|
| P1 Sampling bias | Hash sample and risk-set controls (2.3, 2.5); weights to true prevalence |
| P2 Label inaccuracy | Freeze types, released and destroyed variants, court test (5.1, 5.2) |
| P3 Data snooping | Leakage register L1 to L14; analysis lock (2.6, 6.6) |
| P4 Spurious correlations | Balance and size tests, batch effects, planting (3.2, 5.3, 6.7 check 1) |
| P5 Biased parameter selection | Tuning on Tune months only (L9) |
| P6 Inappropriate baselines | Checklist, single numbers, logistic regression (3.3) |
| P7 Inappropriate measures | Recall at fixed yield, AUPRC, calibration (6.2) |
| P8 Base-rate fallacy | True-prevalence replay and 1-in-25 line (6.7) |
| P9 Lab-only evaluation | Monthly calendar replay without knowing the freezes (RQ2); live trial (6.9) |
| P10 Inappropriate threat model | Cost-to-frame test (5.3) |

### 6.9 The live lists and the held-out check (fitted to 15 December 2026)

The trial approved on 25 November waited four weeks and then 30 days, about two months. The final presentation is on 15 December, so the same method now runs on a shorter clock, with nothing removed.

**Three parts**

| Part | Data | What it shows | Ready by 15 December |
|---|---|---|---|
| **Test results** | 1 January to 31 October 2026, scored once after the lock | The four checks and the verdict (6.7) | Complete |
| **Held-out check** | 1 November 2026 to the day before the lock; pulled and scored only after the lock, in the same daily rhythm | The same scores on days nobody had looked at | Scoring days of 1 to 14 November fully judged; later days partly |
| **Live lists** | Every day from the lock (target 4 December) to 14 December | Lists sealed before the outcome exists; hits revealed with proofs as Tether freezes | About ten lists, with their 30-day windows still open and marked as pending |

**When the lists count as a trial.** The lists start at the lock, before the verdict is known, so no live day is lost. If the verdict is "Useful early warning", they are the live trial. If not, they are shown as a **demonstration of the method, not a trial**, and the verdict is reported as it is.

**One run a day, on the master laptop** (Dagster schedule; data cut-off 00:00 UTC), with the locked rules, model and line:

| Step | What happens | Size |
|---|---|---|
| 1. Screen (BigQuery) | For every wallet active in the last 7 days, compute simple 7-day numbers in SQL and apply the locked screen. The screen is designed on the Tune months to keep at most 3,000 wallets a day while losing as few later-frozen wallets as possible (the network-wide count is estimated from the hash sample with its weights). Its losses on Test are reported after the lock. Only the kept wallets' IDs are downloaded | About 4.3 GB scanned per run, stated before the first run |
| 2. History (TronGrid) | For each kept wallet, read the 180 days of USDT history that end at the data cut-off | About 6,000 calls (our estimate, measured in the rehearsals), about two hours |
| 3. Score (laptop) | Set aside thin, silent and very busy wallets (2.3, 2.5); skip wallets that were on a list in the previous 30 days and wallets already voted on; compute the locked features; score; keep those above the line | About 33 a day (1,000 a month) |
| 4. Seal and publish | Build the sealed list, push its root to the public repository within an hour, and stamp it with OpenTimestamps | Minutes |

Two rehearsal runs, on the two days before the lock, test steps 1 to 4 for time, size and calls. They use a draft model, are marked as rehearsals, and are never judged.

**Sealing with a Merkle root (decided).** Each entry (wallet, list date, rank band) gets its own 32-byte random salt. The salted entries are the leaves of a Merkle tree hashed as in [RFC 6962](https://www.rfc-editor.org/rfc/rfc6962) (SHA-256, with different prefixes for leaves and inner nodes). The root is the list's fingerprint. We publish the root, the list size and the data cut-off in `trial/YYYY-MM-DD/`, and commit the `.ots` proof once Bitcoin confirms it. Because each entry has a secret salt, nobody can test whether a given wallet is on a list. Lists, salts and trees stay on the master laptop, with an encrypted backup kept by another member (you choose who), and never go into git.

- **One list a day.** Exactly one root a day, pushed within an hour of sealing and logged in progress.md. A day without a root is a day without a list; it is never filled in later. This stops anyone from sealing several lists and showing only the best one.
- **Seal time** is the time of the Bitcoin block that confirms the root. Only votes that start after the seal time count for that list.
- **Revealing a hit.** When a listed wallet is frozen, we reveal that one entry: wallet, list date, salt and the proof path to the root. Anyone can check it against the published root. Entries of wallets that have not been frozen are never revealed.

**Judging.** The rules of RQ2: each warning is right or wrong on its own, once its 30 days are over; a vote is caught if the wallet was on a list sealed in the 30 days before the vote, and caught early if that list was sealed at least 7 days before; a vote that never leads to a freeze is listed separately. Freezes whose wallets were on no list are misses; set-aside wallets are counted apart.

**On 15 December.** For each list: its date, root, Bitcoin block, size, days elapsed, hits so far and early hits so far. Totals are labelled "so far": a list sealed on 10 December has had only 5 of its 30 days, and early hits are possible only for lists at least 7 days old (those of 5 to 8 December). A warning becomes wrong only when its 30 days are over, so no wrong warnings can be counted live by 15 December. The held-out check gives the fuller picture, and the Test results give the main answer.

**After 15 December.** The last list's window closes on 13 January 2027. If the group keeps going, final totals are published then; if the course has ended, we publish what has come in and say so. A reviewer (the professor) can check the full lists privately on the master laptop.

**What is ours here, and what is not.** Sealed forecasts with OpenTimestamps already exist (Gracia, 2026). What we add is applying them to freeze warnings with a locked model, fixed counting rules and per-entry proofs.

---

## 7. Architecture

### 7.1 Layers

```
SOURCES                 PIPELINE (Dagster; checks L1-L14 stop the run)        MODELS             SERVING           DASHBOARD
TronGrid events ──┐
lists, court,     ├──►  1 Freeze registry ──┐
FreezeCheck  ─────┘                         ├──►  4 Comparison ──► 6 Learn, tune, ──► 8 Result ───► 9 API ─────► 11 Story mode
BigQuery transfers ──►  2 Transfer store ───┤        sets            test               store        (read-only,    Console mode
Zenodo ──────────────►  3 Cleaning ─────────┤          │               ▲                (versioned)   OpenAPI)
                        E Evidence graph ───┴──►  5 Features at t ─────┘   7 D2, D3, ──────┤
                          (dated facts) ────────►  AI helpers (Ollama) ──► notes ──────────┘
TronGrid live feed ──►  10 Live service (watch, store, record) ─────────────────────────────────► SSE ───────► live scenes
                        12 Live lists, daily: screen ► history ► score ► seal ► Merkle root ► OpenTimestamps ─► trial scenes
```

- **Data pipeline:** raw files are never edited; each step writes a versioned table with its own checks. Dagster runs the steps in order, and its blocking asset checks stop the line when a check fails.
- **Model layer:** reads feature tables only, never raw data. MLflow records every run: settings, code version, data fingerprints and results.
- **Serving layer:** precomputed results through a read-only FastAPI service, with a fixed OpenAPI file that the dashboard is built against. It cannot score a wallet that someone types in.
- **Live service and live lists:** 7.2 and 6.9.
- **Dashboard:** now specified (7.3), following the details given on 26 November 2026. Version 1 only reserved its place.

### 7.2 The live service

A small Python service reads TRON as it happens and sends it to the dashboard. It runs on the master laptop, or on any member's laptop with their own key.

| Feed | Source | How often | Calls |
|---|---|---|---|
| Votes | Tether multisig events (`Submission`, `Confirmation`, `Execution`), one call for all | Every 60 seconds; every 10 seconds while the dashboard is open | About 1,440 a day, plus about 360 an hour during demos |
| Freezes, releases, destructions | USDT `AddedBlackList`, `RemovedBlackList` and `DestroyedBlackFunds` events, one call per event name | Same as votes | About 4,320 a day, plus about 1,080 an hour during demos |
| USDT transfers (counts and amount bands only) | USDT `Transfer` events, 200 per page | Only while the dashboard is open: about 10 pages a minute at today's volume | About 600 an hour |
| New blocks | The block numbers inside the transfer events | No extra calls | 0 |

- **Quota guard.** At most 1 call a second on average and 20,000 a day per key, with backoff on any refusal. TronGrid does not publish one fixed free limit (Appendix B). The daily list run (about 6,000 calls) and the watchers (about 5,800) leave room for about four hours of dashboard time a day; the transfer feed runs only while the dashboard is open.
- **Storage and push.** Events go into a DuckDB table and out to the browser as Server-Sent Events (sse-starlette). The browser never calls TronGrid and never holds a key.
- **Recorder.** Every event sent is also written to a dated JSONL file. **Recorded mode** replays a file at normal or faster speed, with a "Recorded on [date, time]" badge, so a demo still works without a network. A recording is never shown as live.
- **Freeze check.** When a freeze executes, the service asks the trial store whether the wallet is on a sealed list (6.9) and, if it is, sends the proof to the dashboard.
- **What it never does.** Score a wallet; show the full address of a wallet that has not been frozen (a vote shows a short form such as `T…9xQ2` until the freeze executes); send anything on-chain.

### 7.3 The dashboard

**Purpose.** Presented live to the class and the professor, and used by the team to watch the trial. It must be polished, professional and clearly about this topic: money moving, the vote, the freeze, the warning line and the sealed proof.

#### 7.3.1 Two modes

- **Story mode** for the presentation: full-screen scenes in order, moved with arrow keys or the clicker, with camera moves between scenes.
- **Console mode** for daily use: a grid of the same panels, with filters and the system health panel. No long animations.

#### 7.3.2 Scenes

| # | Scene | What the viewer sees | Data | Signature effect |
|---|---|---|---|---|
| 1 | **TRON, right now** | A pulse for each new block; USDT transfers a minute; a river of light where each particle is a live transfer, sized by amount band. No addresses | Live service | WebGL particle river with bloom; block pulse ring |
| 2 | **Freeze watch** | Votes (violet), freezes (ice), releases (thaw) and destructions as they happen. For each freeze: "On our sealed list since [date], [n] days before the vote", with the proof, or "Not on our lists" | Live service, trial store | Frost grows across the card from its edges; nearby particles in the river slow down and turn to ice |
| 3 | **The vote window** | Why we stop before the vote: the gap from vote to freeze by year (median 103 minutes in 2024–25, 23 in 2026) | Result store | A timeline the camera travels along; the gap closes year by year |
| 4 | **How early: the frost line** | Lead-time curves at the eight moments; right, early and wrong warnings per 1,000. A replay of already-frozen wallets as they looked on past dates, beside anonymous comparison wallets | Result store | The warning line glows amber; later-frozen wallets rise past it as ice shards while the date scrubs back |
| 5 | **The honest count** | Per 1,000 warnings: right, early, wrong, with batch-bootstrap bands; the 100 and 500 views | Result store | Numbers roll like a counter; bands drawn as soft aurora ribbons |
| 6 | **Fair and clear** | Set A and Set B comparisons; the freeze-type grid (lists, scams, undone); a 2-D map of frozen wallets coloured by type | Result store | A star map of points that regroup when the type filter changes |
| 7 | **Can it be tricked?** | A simulated innocent wallet receiving planted payments; the score meter; the cost counter for Full, Clean and Owner-only. Aggregates only | Result store | Junk payments as sparks; with the Clean version they slide off a glass shield |
| 8 | **Sealed and live** | Every daily list since the lock: data cut-off, seal time, root, Bitcoin block, days elapsed of its 30, hits and early hits so far; the held-out check; the funnel of the latest run as counts only (active, screened, scored, above the line); a "demonstration" badge if the checks failed | Trial store, result store | A glass capsule closes and the root is etched on it; when a hit is revealed, its proof path lights up from the leaf to the root |
| 9 | **Evidence view** (frozen wallets only) | The as-of graph around one frozen wallet, with a date slider | Evidence graph | WebGL graph; frost spreads from node to node as the slider passes each freeze |
| 10 | **The verdict** | The four checks lighting one by one, and the fixed verdict sentence (6.7) | Result store | One slow reveal; nothing else moves |

Console mode adds **System health**: data checks, model and lock fingerprints, TronGrid calls used today, the last BigQuery run, live or recorded.

#### 7.3.3 Look and feel: "polar night"

- **Base.** Near-black blue backgrounds with a faint aurora drawn by a slow WebGL shader, film grain at low strength, and frosted-glass panels on top.
- **Colour roles.** Each colour means one thing everywhere, and no single colour covers more than about a quarter of the screen.

| Role | Colour | Used for |
|---|---|---|
| Night | `#05070D`, `#0A0F1C`, `#121A2E` | Backgrounds and raised panels |
| Snow | `#EEF3FF` | Main text |
| Mist | `#A9B4C9` | Secondary text |
| Slate | `#5C6A85` | Lines, grids, quiet labels |
| Ice | `#8BE9FF` | Freezes and frost |
| Aurora green | `#4BE3A6` | USDT moving |
| Amber | `#FFB648` | Our warnings and the warning line |
| Violet | `#B193FF` | Public votes |
| Coral | `#FF6B7D` | TRON blocks, used sparingly |

  These are starting values. In P11 they are checked for text contrast on the night backgrounds and for colour-blind separation with a palette validator, and changed if they fail. State is never shown by colour alone: each state also has an icon and a word.
- **Type.** Bricolage Grotesque for titles (as on the explainer page), Inter for text and JetBrains Mono for hashes, block numbers and amounts, with tabular figures. All three are under the SIL Open Font Licence and are bundled through Fontsource, so the demo works offline.
- **Glass.** Background blur of 16 to 24 px, a 1 px light edge, a 6% to 10% white fill and a soft inner glow. Never more than two glass layers on top of each other, for speed and for reading.
- **Hover.** Cards lift by 2 to 4 px, a soft light follows the cursor across the glass, and a line of detail appears. Every number shows its exact value and its source on hover.
- **Motion.** Panels "crystallise" when they appear (blur to sharp, 400 to 600 ms). Scene changes are camera moves. The warning line pulses once per block (3 seconds). In console mode no animation lasts over 1.2 seconds.
- **Cinematic moments.** The opening: a dark screen, one block pulse, the river fades in, and the name forms out of frost. A live freeze: the river slows and the frost spreads. The proof: the path from leaf to root lights up in the sealed tree.

#### 7.3.4 How it is built

| Need | Tool (version checked 26 Nov 2026) | Role |
|---|---|---|
| App and build | React 19.3.1, TypeScript 5.9.3, Vite 8.3.8 | The app, its types and the build |
| Motion | Motion 14.13.0 (the new name of Framer Motion) | Hover, panel entry, layout changes |
| Story timelines | GSAP 3.15.1 with ScrollTrigger, @gsap/react 2.1.2, Lenis 1.3.27 | Scene timelines, camera moves, smooth scrolling |
| WebGL | three 0.187.0, @react-three/fiber 9.8.2, drei 10.7.9, @react-three/postprocessing 3.2.2, postprocessing 6.39.6 | River, frost, aurora, capsule; bloom, depth of field, grain |
| Network view | sigma 4.0.6, @react-sigma/core 6.0.0, graphology 0.26.0 | WebGL graph for the evidence view |
| Charts | D3 7.9.2, visx 4.0.0 | Lead-time curves, bands, grids |
| Layout and parts | Tailwind CSS 4.3.5, Radix UI 1.8.1, lucide-react 1.72.0 | Tokens, accessible dialogs, tabs and tooltips, icons |
| Data | TanStack Query 5.107.1, TanStack Router 1.170.46, Zustand 5.1.0, Zod 4.6.7 | Server data, scenes in the address bar, view state, checks on live messages |
| API types | openapi-typescript 7.13.0, openapi-fetch 0.17.0 | Types made from the API's OpenAPI file, so both sides agree |
| Tests and style | Vitest 5.1.0, Playwright 1.65.0, Biome 2.6.7 | Unit tests, screen tests, formatting and lint |

**Live data flow.** FastAPI `/live/stream` (SSE) → each message checked with Zod → kept in the TanStack Query cache and a Zustand store → the scenes. Message types: block, transfer batch (counts and amount bands per second), vote, freeze, release, destroy, trial reveal, health.

**Running it.** During development, `pnpm dev` against the local API. For the presentation, a production build served by the FastAPI app on the master laptop. No cloud hosting is needed.

#### 7.3.5 Rules the dashboard must keep

- No score for a never-frozen wallet, anywhere, ever. No warning list is shown.
- Full addresses appear only for wallets Tether has frozen; a wallet under a public vote shows a short form.
- Every results scene carries the standard sentence (10.2), and the banned-words check also scans the dashboard's text.
- Recorded mode always shows its badge.

#### 7.3.6 Speed, access and tests

- **Speed.** Target 60 frames a second on the team laptops (2 GB GPU): quality presets (high, low, off), device pixel ratio capped at 1.5, at most 20,000 particles, and WebGL paused when the tab is hidden. Checked on the presentation laptop before the day.
- **Access.** With "reduce motion" on, scenes become still images with the same numbers. Full keyboard control. Text contrast at WCAG AA. Works offline except the live feed.
- **Tests.** Vitest for data transforms. Playwright opens every scene, compares screenshots and fails on console errors. A **never-frozen check** scans API answers and the page for any score next to an address that is not in the freeze registry.

---

## 8. Tools, compute, cost and setup

### 8.1 Tool register

Versions, release dates and licences as read on 26 November 2026. The exact versions are fixed at P0 by the rules in 8.3, so the installed version can be one step older than the newest shown here.

**Language and environment**

| Tool | Newest (release date) | Licence | Use | Decision |
|---|---|---|---|---|
| Python | 3.12, through uv | PSF | Language | **Changed from 3.11.** NumPy 2.5.5 and NetworkX 3.7 need 3.12 or newer; Dagster supports up to 3.14 and recommends 3.13. DuckDB 2.0.1 lists Windows wheels tagged 3.11 and 3.12, so 3.12 is the safe choice. 3.13 only if P0 shows every wheel installs |
| uv | 0.13.10 (24 Nov 2026) | MIT or Apache-2.0 | Python versions, environments, `uv.lock` | **New.** One lock file, so every laptop gets the same versions. The laptop has 0.11.28; update in P0 |
| pnpm | 10.30.3 (installed) | MIT | Dashboard packages, `pnpm-lock.yaml` | **New.** Its `minimumReleaseAge` setting enforces the 14-day rule (8.3) |
| Node.js | 22.21.1 (installed) | MIT | Runs the dashboard tools | Keep |

**Data and pipeline**

| Tool | Newest (release date) | Licence | Use | Decision |
|---|---|---|---|---|
| DuckDB | 2.0.1 (20 Nov 2026); 2.0.0 on 21 Oct 2026 | MIT | Store, ASOF joins, evidence graph tables | Keep. 2.0 is a new major version: P0 tests our queries on it; fall back to 1.5.6 (28 Sep 2026) if a test fails |
| Polars | 2.2.0 (24 Nov 2026); 2.0.0 on 6 Oct 2026 | MIT | Cleaning and features | Keep. Pandera 0.36 asks for Polars 1.20 or newer and does not say it supports 2.x: P0 tests them together; fall back to 1.44.2 |
| pandas | 3.1.1 (4 Nov 2026) | BSD-3-Clause | Only where a library needs it | Keep |
| PyArrow | 26.0.1 (3 Nov 2026) | Apache-2.0 | Parquet files | Keep. MLflow needs PyArrow below 27 |
| NumPy | 2.5.5 (15 Nov 2026) | BSD-3-Clause and bundled permissive licences | Numbers | Keep |
| Pandera | 0.36.0 (10 Nov 2026) | MIT | Table checks | Keep |
| Dagster, dagster-webserver, dagster-duckdb | 1.13.31 / 0.29.31 (19 Nov 2026) | Apache-2.0 | Runs every step in order; blocking asset checks stop the line | Keep. Its install guide gives Windows steps |
| google-cloud-bigquery, -bigquery-storage, db-dtypes | 3.47.0 / 2.43.0 / 1.9.0 | Apache-2.0 | The pull and the trial screen | Keep |
| httpx, tenacity | 0.29.0 (26 Nov 2026) / 9.2.1 | BSD-3-Clause / Apache-2.0 | TronGrid calls with retries and backoff | Keep. httpx 0.29.0 came out today, so 0.28.1 is used under 8.3 |
| base58 | 2.1.1 | MIT | Address format checks | Keep |

**Models and analysis**

| Tool | Newest (release date) | Licence | Use | Decision |
|---|---|---|---|---|
| scikit-learn | 1.9.1 (10 Sep 2026) | BSD-3-Clause | Logistic regression, k-means, HDBSCAN, t-SNE | Keep. **The separate `hdbscan` package is dropped** |
| LightGBM | 4.7.0 (18 Jul 2026) | MIT (from its GitHub licence; the PyPI field is empty) | Main candidate | Keep |
| PyTorch (CPU) | 2.15.0 (28 Oct 2026) | PyPI lists BSD-3-Clause plus the permissive licences of bundled parts (Apache-2.0, MIT, Zlib and others) | Neural network | Keep |
| PyTorch Geometric | 2.8.1 (12 Oct 2026) | MIT | GraphSAGE, on Colab | Keep, optional |
| statsmodels | 0.15.0 | BSD-3-Clause | Tests and intervals | Keep |
| NetworkX | 3.7 (21 Sep 2026) | BSD-3-Clause | Network measures, Louvain | Keep |
| NetworKit | 11.3 (6 Nov 2026) | MIT | Speed-up for large graphs | **New, optional.** Windows wheels for Python 3.10 to 3.15 |
| MLflow | 3.18.0 (3 Nov 2026) | Apache-2.0 | Run logbook, local store, no server | Keep |
| SHAP | 0.54.1 | MIT | Plots | **Now optional.** LightGBM gives tree contributions itself |
| umap-learn | 0.6.0 (10 Nov 2026) | BSD-3-Clause (from its GitHub licence) | The 2-D map in scene 6 | **New, optional.** Falls back to t-SNE |
| matplotlib | checked at P0 | PSF-based | Report figures | Keep |

**AI helpers**

| Tool | Newest (release date) | Licence | Use | Decision |
|---|---|---|---|---|
| Ollama | (app) | MIT | Runs the model on the laptop | Keep. Not installed yet |
| Qwen3 4B | 2.5 GB in Ollama | Apache-2.0 | Default helper model | Keep; tested against two candidates in P9 (3.8) |
| LangGraph, langchain-ollama, ollama (Python) | 1.2.24 / 1.2.0 / 0.6.3 | MIT | Runs the helper steps and the stop for the person | Keep |

**Serving, live and proof**

| Tool | Newest (release date) | Licence | Use | Decision |
|---|---|---|---|---|
| FastAPI, Uvicorn, Pydantic | 0.165.0 / 0.54.0 / 2.14.4 | MIT / BSD-3-Clause / MIT | Read-only API | Keep |
| sse-starlette | 3.7.1 (22 Nov 2026) | BSD-3-Clause | Live push to the dashboard | **New** |
| opentimestamps-client | 0.8.0 (27 Oct 2026), with python-bitcoinlib 0.12.2 | LGPL-3.0-or-later | Time stamps on the lock and the trial roots | Keep. **P0 finding (26 Nov):** the `ots` command fails on Windows, because python-bitcoinlib 0.12.2 looks for an old OpenSSL library that Windows lacks. The library's own calendar client (`opentimestamps.calendar`) works, so we stamp and upgrade through it; anyone can check a proof with the official client on Linux or macOS. Used unchanged, which the LGPL allows |
| SHA-256 and the Merkle tree | Python's standard `hashlib` | PSF | Fingerprints and sealed lists | Our own short code, following RFC 6962; no extra package |

**Development and teamwork**

| Tool | Newest (release date) | Licence | Use | Decision |
|---|---|---|---|---|
| pytest | 9.2.0 | MIT | Tests | Keep |
| Hypothesis | 6.170.17 | MPL-2.0 | Random tests of the leakage rules (for example: no feature ever uses a row after t) | **New**, development only; used unchanged |
| Ruff | 0.17.6 | MIT | Lint and format | Keep |
| pre-commit | 4.7.0 | MIT | Checks before each commit, including keys and data files | Keep |
| marimo | 0.26.0 (24 Nov 2026) | Apache-2.0 | Notebooks saved as plain `.py` files, so four people can merge them | **New.** Jupyter only on Colab |
| git, GitHub, GitHub Actions | git 2.51.2, gh 2.87.0 (installed) | GPL-2.0 (git, used as a tool); GitHub terms | Code, reviews, CI | Keep. CI runs tests on every pull request |

The dashboard's tools are listed with their versions in 7.3.4. Their licences: MIT for React, Vite, Motion, three, @react-three/*, Lenis, Tailwind CSS, Radix UI, TanStack, Zustand, Zod, sigma, graphology, visx, openapi-typescript, openapi-fetch and Vitest; Apache-2.0 for TypeScript and Playwright; ISC for D3 and lucide-react; Zlib for postprocessing; MIT or Apache-2.0 for Biome; SIL Open Font Licence for the fonts.

**GSAP's licence.** GSAP 3.15.1 uses Webflow's ["Standard 'No Charge' License"](https://gsap.com/community/standard-license/), read on 26 November 2026. It is free, including the former members-only plugins, for commercial and non-commercial sites, as long as end users are not charged to use the product. It forbids use in no-code visual animation builders that compete with Webflow, and Webflow may end the licence if its terms are broken. It is not an open-source licence. Our free dashboard is allowed. If the group wants open-source licences only, Motion alone can drive the scroll scenes.

### 8.2 Options checked and not chosen

| Option | Licence | Why not |
|---|---|---|
| Prefect 3.9.5, Kedro 1.8.0, Hamilton 1.90.0 | Apache-2.0 | Good tools. Dagster stays because its blocking asset checks match our "a failed check stops everything" rule, and its lineage view helps four people see what depends on what |
| Great Expectations 1.25.0 | Apache-2.0 | Heavier than we need |
| Patito 0.8.6 | MIT | Polars-only and younger than Pandera |
| XGBoost 3.4.1, CatBoost 1.2.10 | Apache-2.0 | No reason for a second tree library |
| igraph 1.0.0, leidenalg 0.12.0 | GPL | Copyleft; Louvain in NetworkX is enough |
| graspologic 3.4.4 | MIT | Needs Python below 3.13; not needed |
| rustworkx 0.18.1 | Apache-2.0 | NetworKit covers the speed-up |
| Kuzu, LadybugDB, Neo4j, rdflib, pyoxigraph, DuckPGQ | Various | See 3.7 |
| DVC 3.67.1 | Apache-2.0 | More setup than a checksum manifest for four people (9.5) |
| Pydantic AI 2.75.0 | MIT | Good typed outputs. LangGraph stays because the helper loop, with two tries and a stop for a person, is a small graph |
| ty 0.0.112 | MIT | Still in early versions. Pyright 1.1.414 (MIT) is an optional type checker |
| Qwen3.5 4B, Gemma 4 E2B or E4B | Apache-2.0 | Not rejected: candidates in the P9 test (3.8) |
| TypeScript 7.0.2 (8 Jul 2026) and 6.0.3 | Apache-2.0 | openapi-typescript 7.13.0 needs TypeScript 5, so 5.9.3 is used |
| Vite 8.4.0 | MIT | Released today; 8.3.8 is used under 8.3 |
| React 19.4 or newer | MIT | @react-three/fiber 9.8.2 supports React below 19.4 |
| three 0.188 or newer | MIT | postprocessing 6.39.6 supports three below 0.188 |
| ECharts 6.1.0, deck.gl 9.4.2 | Apache-2.0, MIT | Not needed: D3 and visx, three and sigma cover every view |
| @cosmograph/react 2.6.1 | CC BY-NC 4.0 | Non-commercial licence; avoided |
| ESLint 10 and Prettier | MIT | Biome does both in one tool |

### 8.3 Version rules

1. **Fourteen days.** Install only releases that are at least 14 days old on the day of setup. uv's `exclude-newer` setting (it accepts a date or a duration) and pnpm's `minimumReleaseAge` (in minutes; 20,160 for 14 days) enforce it.
2. **Lock files are committed.** `uv.lock` and `dashboard/pnpm-lock.yaml`. Everyone installs from them (`uv sync --locked`, `pnpm install --frozen-lockfile`).
3. **New major versions** (DuckDB 2, Polars 2) are tested with our own code in P0. If a test fails, use the last 1.x version and record it in progress.md.
4. **A new tool** is added only after its licence is checked and a row is added to 8.1.

### 8.4 Compute

The master laptop (8 threads, 16 GB RAM, 197 GB free on D:) is enough for everything except GraphSAGE. The 2 GB GPU and CPU-only PyTorch cannot train it. [Colab's](https://research.google.com/colaboratory/faq.html) free GPU can, but resources are not guaranteed. GraphSAGE is therefore tried last and kept only under the rule in 3.3. The AI helpers run on the CPU with 16 GB RAM; their speed is not measured yet (P9). The dashboard's frame rate on the 2 GB GPU is not measured yet (P11).

### 8.5 Cost

| Item | Expected | Worst case |
|---|---|---|
| BigQuery | $0 in the sandbox (about 735 GB in all, at most about 67% of one month's 1 TiB allowance; 2.3) | About $4 for one extra full pass, only with billing on and only if you approve |
| TronGrid | $0, free personal keys, within the quota guard (7.2) | $0; calls slow down if a limit is reached |
| Ollama and models, Colab, Zenodo, lists, OpenTimestamps, GitHub | $0 | $0 |
| Fonts and dashboard libraries | $0 | $0 |

### 8.6 Setup, in words (P0)

1. Make this project folder a git repository and push it to the public repository https://github.com/KartikJoshi23/FrostLine (13.1, row 26; warning in 10.1). Protect `main`: changes only through pull requests with passing CI.
2. Install Python 3.12 through uv (0.11.28 or newer) and create the environment from `uv.lock`. Install the pre-commit hooks.
3. Install the dashboard packages with pnpm from `pnpm-lock.yaml`. Check that the installed pnpm supports `minimumReleaseAge`.
4. Each member registers a free TronGrid key and puts it in their own `.env` file, which is never committed. `.env.example` shows the names.
5. On the master laptop only: create one Google Cloud project in the BigQuery sandbox, without billing; set a per-query byte cap. If billing is enabled later, set the daily quota first.
6. Download the files listed in 2.1, with checksums recorded. (Done on 24 November 2026.)
7. Test the BigQuery download route on the one-month sizing result, and measure how many hours the table runs behind the chain (needed for the trial).
8. Install Ollama and pull the default model (2.5 GB) only when P9 starts, after your OK.
9. Check: tests pass, Dagster's web view opens, the dashboard builds, and progress.md is updated.

BigQuery's free quota is monthly. If P1 is done by 29 November, the main pull uses November's allowance, which ends on 30 November, and December's covers the held-out pull and the daily lists. Otherwise all of it falls in December (about 67%, 2.3).

---

## 9. Repository, phases and work split

### 9.1 Repository structure

This project folder becomes the repository.

| Folder or file | Contents |
|---|---|
| `implementation-plan.md`, `progress.md`, `collaborator-prompt.md` | This plan, the handover file and the prompt for each new session |
| `docs/` | Analysis lock, wording rules, data dictionary. The brief stays in the root folder |
| `config/settings.toml` | Dates, thresholds and rule values from this plan, read by the code and checked by tests |
| `data/raw`, `data/interim`, `data/final`, `data/live` | Never committed; only `data/MANIFEST.csv` (file, SHA-256, rows, command, date) and README files are |
| `pipelines/` | Dagster definitions: assets, checks, schedules |
| `src/frostline/registry`, `pull`, `clean`, `controls`, `features` | Data pipeline |
| `src/frostline/models`, `evaluate` | D1 |
| `src/frostline/labels` | D2 |
| `src/frostline/planting` | D3 |
| `src/frostline/network`, `kg` | RQ3, RQ5, evidence graph |
| `src/frostline/helpers` | AI helpers |
| `src/frostline/live`, `trial` | Live service, live trial and sealing |
| `src/frostline/serving` | API and result store |
| `notebooks/` | marimo notebooks (`.py` files) |
| `dashboard/` | The React app |
| `tests/` | Leakage checks L1 to L14, registry checks, wording check, never-frozen check, seal and proof checks; small made-up test data |
| `trial/` | Public only: daily roots, list sizes, cut-offs and `.ots` proofs |
| `reports/` | Figures, tables, final write-up |
| `archive/` | The original brief (local only, git-ignored) |

### 9.2 Build phases and the schedule to 15 December

The dates assume that Claude Code writes most of the code while each member reviews it, runs it and checks the results. Version 2's estimate of about 49 person-days for people working alone does not fit into 19 days without that help.

| Phase | Work | Needs | Done when | Dates |
|---|---|---|---|---|
| **P0** Setup | Repository, uv and pnpm environments with lock files, CI, pre-commit, `.env` files, keys, BigQuery sandbox, sizing query, BigQuery delay check | The go-ahead (given) | Same environment on two laptops; CI green; download route tested | 26–27 Nov |
| **P1** Registry and lists | Registry, votes, sanctions dates, court list, seed list; evidence-graph base tables; the batch rule at split edges | P0 | All 2.2 checks pass; split counts settled | 27–28 Nov |
| **P2** Benchmark | Waterfall steps 1 and 2 on the Zenodo table | P0 | AUC reproduced or difference explained | 27–29 Nov |
| **P3** Main pull | Dry run, ⛔ your approval, pull, quality checks | P1 | 2.8 checks pass | 28–30 Nov |
| **P4** Features and controls | Cleaning, comparison sets, features, as-of facts, leakage checks | P3 | All L checks pass | 1–2 Dec |
| **P5** D1 | Models, line and screen on Learn and Tune; ⛔ analysis lock; Test scoring, checks, verdict and replay | P4 | Lock stamped; RQ1 and RQ2 tables final; verdict known | 3–4 Dec |
| **P6** D2 | Origin and outcome grid, court test | Model code from P5 | RQ4 range reported | 5–8 Dec |
| **P7** D3 | Writability versions, cost to frame | Model and line from P5 | Table for three versions | 5–8 Dec |
| **P8** Networks and list F | Communities, red flags, exchange list F, off-ramp range, clusters | P4 | RQ3 and RQ5 reported | 1–8 Dec |
| **P9** Serving and AI helpers | Result store and read-only API with a frozen OpenAPI file; AI helpers and their 20-note test | API shape fixed on sample data; results from P5 to P8 | Interface frozen; helper test done | 1–9 Dec |
| **P10** Live service | A recorded sample hour (27 Nov) for the dashboard; watchers, quota guard, SSE, recorder, recorded mode | P0, P1 | 24 hours without errors or quota warnings | 27 Nov–3 Dec |
| **P11** Dashboard | Design tokens and scenes on sample data and the recording, then live data and results; console mode; tests | P0; P9 and P10 to go live | Every scene passes its Playwright test; frame rate checked on the presentation laptop; never-frozen check passes | 27 Nov–12 Dec |
| **P12** Live lists | Two rehearsal runs (2 and 3 Dec), then one sealed list a day from the lock; reveals; totals so far | P5, P10 | One root a day, public within an hour; totals so far on the dashboard | 2–14 Dec |
| **P13** Quality and final pack | Held-out check, wording and never-frozen checks, rerun from raw, report tables and slide inputs | All | Clean rerun matches | 5–13 Dec |

Owners of the phases are assigned by you and recorded in progress.md.

**Key dates**

| Date | Milestone |
|---|---|
| Fri 27 Nov | Environments match; keys and sandbox ready; dashboard skeleton runs on a recording |
| Sat 28 Nov | Registry passes its checks; ⛔ main-pull size shown for approval |
| Mon 30 Nov | Main pull done inside November's free allowance |
| Wed 2 Dec | Features and leakage checks pass; first rehearsal run |
| Fri 4 Dec | ⛔ Analysis lock stamped; Test results and verdict; first live list (cut-off 5 Dec, 00:00) |
| Tue 8 Dec | D2, D3, networks and the held-out check done |
| Sat 12 Dec | Every scene on real data; no new features after this |
| Sun 13 Dec | Full rehearsal on the presentation laptop; recording for recorded mode |
| Mon 14 Dec | Fixes only; last list before the presentation |
| Tue 15 Dec | Final presentation |

**Critical path:** P0 → P1 → P3 → P4 → P5 (lock) → live lists. Each day the lock slips costs one live list. If the lock is not stamped by 6 December, the live lists still start on the day it is, and the held-out check carries more of the weight.

**Order of work if time runs short.** Nothing is dropped from the plan, but the work is done in this order, so the most important parts are safe first: (1) registry, pull, features and leakage checks; (2) models, lock, Test results and verdict; (3) live service, live lists and dashboard scenes 1, 2, 4, 5, 8 and 10; (4) D2, D3, networks and the held-out check, with scenes 3, 6 and 7; (5) the evidence view, the 2-D map, GraphSAGE, Set C, the court test, the second hop and AI notes beyond the 20-note test.

### 9.3 Work packages

The work falls into four groups, so that several people can build at the same time. **Who owns each package is decided by you**, not by this plan, and is recorded in progress.md.

| Package | Phases | Hands over |
|---|---|---|
| **A. Data, live feed and official runs** | P0, registry in P1, P3, cleaning in P4, P10, daily runs in P12, rerun from raw in P13; all official runs on the master laptop | Registry, transfer store, live service, daily roots |
| **B. Early warning** | P2, comparison sets and features in P4, P5, P7, scoring code in P12, held-out check | Feature tables, models, lock, Test results, verdict, cost to frame |
| **C. Labels, networks, evidence graph, AI helpers** | Lists and court data in P1, as-of facts in P4, P6, P8, AI helpers in P9 | Type grid, communities, list F, off-ramp range, evidence graph, notes |
| **D. Serving and dashboard** | Result store and API in P9, P11, wording and never-frozen checks in P13 | API, dashboard, checks |

Packages meet only through agreed tables with written column definitions and through the frozen OpenAPI file, so they can be built in parallel on small test files.

### 9.4 Stages

| Stage | Date | What is shown |
|---|---|---|
| **1. First presentation** | 26 November 2026, done | Problem, solution, data and novelty, using the explainer page |
| **2. Interim report** | No date given | If one is asked for: P0 to P4 and the first D1 results |
| **3. Final presentation** | Tuesday 15 December 2026 | Results, the live dashboard, the live lists so far, the report and the slides |

### 9.5 Collaboration

**The master laptop.** The laptop this repository was set up on is the master laptop; progress.md records it. It holds the official copy of `data/`, the MLflow store and the trial store, and it alone runs the official steps: the main BigQuery pull, the analysis lock, Test scoring, the weekly trial runs, sealing and time-stamping, and the final rerun from raw. Every member can run everything else on sample data on their own laptop.

**progress.md** is the handover file. It is read first and updated at the end of every session, even when nothing worked: the snapshot, the phase board, the quota table and a new log entry at the top (date, who, laptop, what was done, files, tests and results, decisions with who made them, blockers and the exact next step). The next step must be clear enough for someone else to start within five minutes. Old entries are never deleted.

**collaborator-prompt.md** is pasted at the start of every new Claude Code session, on any laptop. It makes the session read `progress.md` and this plan first, stop at the same gates as this plan, and update `progress.md` at the end.

**Git.** One branch per task, named after its phase (for example `p4/tempo-features`). Small pull requests into `main`, with CI passing and one review by another member. No force-pushes to `main`. If this plan and progress.md disagree, this plan wins unless progress.md records a later group decision; when in doubt, ask.

**Data.** Data never goes into git. `data/MANIFEST.csv` lists every data file with its SHA-256, row count and the command that made it. Files move between laptops through a private shared drive folder, and each laptop checks the hashes. Tests use small made-up data, never real never-frozen wallets.

**Secrets.** Each laptop has its own `.env` (git-ignored); `.env.example` lists the names. TronGrid keys are personal under TronGrid's terms. The trial salts, lists and trees stay on the master laptop with one encrypted backup kept by another member (you choose who), and the backup password is kept apart from it. A pre-commit check blocks `.env`, key files and anything under `data/` or the trial store.

### 9.6 Run sheet for 15 December

- **Machine.** The master laptop runs the dashboard, because the keys, the trial store and the data are there. A second laptop has the same build and the latest recording, as a standby.
- **Network.** Venue Wi-Fi, with a phone hotspot as backup. If both fail, recorded mode, with its badge.
- **The day before.** Build the dashboard; run the never-frozen and wording checks; check the frame rate at the projector's resolution; record the last 24 hours of live events; seal the day's list; charge both laptops.
- **On the day.** Story mode, scenes 1 to 10, then console mode for questions. If no freeze happens during the talk, scene 8 shows the hits revealed earlier, each with its proof.

---

## 10. Ethical and legal safeguards

### 10.1 Rules

1. A freeze is the issuer's decision, not a finding of crime.
2. No wallet is tied to a named person. Name columns in sanctions files are dropped on load.
3. No claim that any wallet is criminal, frozen or not, released or not.
4. **No address-level score is shown for a never-frozen wallet**, in any output or demo (decided). Public outputs use aggregates or hashed identifiers. The "time machine" replay shows already-frozen wallets as they looked at past dates, next to anonymous comparison wallets. Frozen wallets appear only with the public fact of the freeze.
5. Planting is simulated offline. Nothing is sent on-chain. No how-to is published.
6. Court material is described with its status; allegations stay allegations.
7. FATF Box 3 is described as FATF frames it: payments to **trafficked** workers.
8. The tool is not for blocking, reporting or accusing anyone.
9. Data licences are kept: attribution for CC BY sources, non-commercial use only for OpenSanctions.
10. Keys and raw data stay out of the repository.
11. **Public repository warning.** Anything pushed to a public repository can be copied, forked or indexed. Making it private later does not take those copies back, and other groups could see the idea. Only code, documents, aggregate results, trial roots and `.ots` proofs go in. The group keeps the repository public (13.1, rows 12 and 26). A public repository also lets anyone see the lock and every daily root when they are made.
12. **Live view.** It shows on-chain facts only: transfers as anonymous amounts, votes and freezes. A full address appears only after the freeze executes; a wallet under a public vote shows a short form.
13. **Live lists.** A warning list is never shown or published. Only entries for wallets Tether has since frozen are revealed, each with its proof. Exactly one root a day is published. Totals are labelled "so far" until each list's 30 days are over.
14. **AI notes** stay internal unless they are about a frozen wallet and use public facts only. Code checks every number, and a person approves every note.
15. **Recorded mode** is always labelled with its date and time. A recording is never presented as live.

This is coursework and not legal advice. The group confirmed that no school ethics approval is needed.

### 10.2 Wording rules for every output, including the dashboard and AI notes

| Say | Do not say |
|---|---|
| later-frozen wallet; wallet Tether froze on [date] | launderer, criminal, illicit wallet |
| resembles wallets that were later frozen | is suspicious, is laundering |
| resemblance score, percentile | probability of crime, guilt, risk of crime |
| comparison wallet; not frozen at that time | clean, innocent, legitimate ("innocent" is allowed only for the simulated wallet in D3, never for a real wallet) |
| released by the issuer | cleared, false positive, wrongly frozen |
| appears to reach a service labelled as an exchange | cashed out |
| on our sealed list since [date] | we knew, we predicted it would be frozen |
| a public vote to freeze started | accused, charged |
| we found no published tool that does all of these | first, only, best |
| not enough history to score | safe |

Every results page and results scene carries: *"A freeze is an issuer decision. This score measures resemblance to wallets frozen in the past. It is not evidence of wrongdoing."* An automated check searches outputs, dashboard text and AI notes for banned words.

The brief's title was corrected to match these rules; its figures in the PDF version still need the same change.

---

## 11. Risks and mitigations

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| 1 | Signal collapses under fair testing | Medium | It is a valid answer; P2 and the D2 and D3 results still stand |
| 2 | Comparison frame is biased | Medium | Two sets, sensitivity tests, risk-set rules |
| 3 | BigQuery output too large, or sandbox storage used up | Medium | Sizing query, low hash rate, two or three attempts only |
| 4 | BigQuery unavailable | Low | TronGrid mode (2.3) |
| 5 | Table gaps in `decoded_events` | Low to medium | Spot checks against TronGrid. None found so far |
| 6 | Batches dominate results | High | Weight cap, batch bootstrap, with and without |
| 7 | Regime change (T3, new task force) | High | Quarter-by-quarter results |
| 8 | Court labels too few or too old | Medium | Pre-set minimum of 150; otherwise descriptive |
| 9 | Service labels too thin for RQ5 | High | Range, not point; unlabelled share shown |
| 10 | Cost to frame misread as a how-to | Medium | Aggregates only; wording audit |
| 11 | Zenodo result cannot be reproduced | Medium | Report the difference; no accusation |
| 12 | Leakage slips in | Medium | L1 to L14 tests, Hypothesis tests of the as-of rule; another member reviews (you choose who) |
| 13 | Scope overload | High | Core and stretch lists; D4 stays supporting |
| 14 | Novelty claim challenged | Medium | Comparison table (1.3) with sources; careful wording |
| 15 | Source pages change or vanish | Medium | Save dated copies; the UAE paper has already moved once |
| 16 | Someone's wallet wrongly exposed | Low | Rules 4 and 12 in 10.1; the never-frozen check |
| 17 | Base rate makes any score impractical | High | Check 3 states it openly; the verdict table covers it |
| 18 | Public repository leaks data or the idea | Medium | `.gitignore`, pre-commit block, rule 11, or start private |
| 19 | Earliest public signal missed for some wallets | Low | Decode all unexecuted proposals, as the audit did |
| 20 | TronGrid limit or outage during a live demo | Medium | Quota guard; recorded mode; another member's laptop and key as standby (you choose whose) |
| 21 | WebGL too slow on a team laptop or the presentation PC | Medium | Quality presets; reduce-motion mode; test on the presentation machine before the day |
| 22 | GSAP's licence terms change | Low | Our use is allowed today; Motion can replace the scroll scenes |
| 23 | The 15 December deadline leaves little slack | High | Day-by-day schedule (9.2); critical path first; the order of work if time runs short; recorded mode as the demo fallback |
| 24 | The master laptop is lost or broken | Low | Code on GitHub; encrypted backup of data and the trial store with another member (you choose who) |
| 25 | New major versions break code (DuckDB 2, Polars 2) | Medium | The 14-day rule, lock files, P0 tests, fall back to the last 1.x |
| 26 | The small local model writes wrong text | High | Code checks every number; two tries, then a fixed template; a person approves |
| 27 | BigQuery runs too far behind the chain for the daily runs | Medium | Measure the delay in P0; use TronGrid for step 1 if needed |
| 28 | Two members edit the same files | Medium | One task per branch; packages meet through agreed tables; progress.md |
| 29 | A sealed list or salt leaks through git | Low | The trial store lives outside the repository; pre-commit block |
| 30 | The trial screen drops many later-frozen wallets | Medium | Designed on Tune months; its losses on Test are reported after the lock |
| 31 | A daily run is missed or fails | Medium | Dagster schedule plus a manual run the same day; a missed day is logged as "no list" and never filled in later |
| 32 | Someone says we sealed several lists and showed the best | Low | One root a day, public within an hour, logged in progress.md; the dashboard shows every root, including those with no hits |
| 33 | The lock slips past 6 December | Medium | The live lists start on the day of the lock; the held-out check carries more of the weight |

---

## 12. Traceability

### 12.1 Brief to plan

| Brief section | Requirement | Plan section | Phase |
|---|---|---|---|
| 1, 2, 9 | Can later-frozen wallets be told apart before the freeze, and how early? | 1, 4, 6 | P5 |
| 3, 4, 5 | Background and scale, with corrected counts | Appendix A, 2.2 | P1, P13 |
| 4 (Figure 1) | Study the public record before the freeze | 2.6 | P3, P4 |
| 5 | 8,206 corrected to a like-for-like count | 2.2, Appendix A | P1 |
| 6 | Freezes follow official action; noisy labels | 5.1, 5.2 | P6 |
| 6 (Figure 2) | Uneven coverage by list, including the sixth group | 5.2, 5.3 | P6 |
| 7 | Protect victims and unwitting counterparties | 5.3, 10 | P7 |
| 8 | Cross-border leg is context and RQ5 | 4 (RQ5) | P8 |
| 11 | Scope: USDT on TRON, freeze and release events, pre-freeze only | 2.2 to 2.6 | P1, P3 |
| 11 | Out of scope items respected | 10 | P13 |
| 12 | Zenodo benchmark and BigQuery; known gaps | 2.1, 2.8, 6.1 | P2, P3 |
| 13 | Limits of issuer freezes as a control | 4 (RQ2, RQ4) | P5, P6 |
| 14 | Ethical and legal limits | 10 | All |
| 15 | Terms used consistently | 10.2 | P13 |
| 16 | References checked | Appendices | P13 |

### 12.2 Research questions

| RQ | Section | Metric | Phase |
|---|---|---|---|
| RQ1 | 4, 2.5, 3.1 | Matched effect sizes; AUROC against Set B | P5 |
| RQ2 | 4, 6.3, 6.9 | Recall at fixed wrong-warning rates by lead time; replay; live trial | P5, P12 |
| RQ3 | 4, 3.4, 3.5, 3.7 | Odds ratios; batch-to-community agreement | P8 |
| RQ4 | 4, 5.2 | Range by list; type grid; court test | P6 |
| RQ5 | 4, 2.1 (list F) | Lower and upper off-ramp bound | P8 |

### 12.3 Your rules and course topics

| Requirement | Section |
|---|---|
| Not a copy; compared with what exists | 1.3 to 1.6 |
| Every claim sourced; unverified marked | Throughout, Appendix B |
| Licences checked | 2.1, 8.1, 8.2 |
| Query size stated before running | 2.3, 6.9 |
| Fake-token question | 5.3 |
| Sanctions confound and label noise | 5.1, 5.2 |
| No leakage | 2.6, 3.7 |
| Course topics | 3.6 |
| Work split | 9.3 |

### 12.4 The development request of 26 November 2026

| Request | Where |
|---|---|
| Audit the tech stack; use better options where they exist | 8.1 to 8.3, section 0 |
| Use a knowledge graph only if it is really needed | 3.7 |
| Show TRON live and live testing in the dashboard | 7.2; 6.9; 7.3 scenes 1, 2 and 8 |
| React, TypeScript, Motion, WebGL, GSAP, glass and hover effects | 7.3.3, 7.3.4 |
| Dark theme, many colours with none dominant, polished, creative, cinematic and on topic | 7.3.3 |
| Update the plan | This document |
| `progress.md` for collaboration, with this laptop as the master | 9.5 and `progress.md` |
| A prompt for collaborators, structured like the original brief | `collaborator-prompt.md` |
| A better project name | Title; 13.1, row 17 |
| Plan first; build only after the go-ahead | Status line; 13.1, row 24 |
| Remove what was never asked for | Section 0; the `proposal/` folder and the plan v1 copy removed |
| Show how it works by 15 December without cutting anything | 6.9, 9.2, 9.6 |
| Choose the best option for the open decisions | 13.1, rows 17 to 20, 22, 23 and 25 (method and planning only) |
| Leave every decision about individual members to you | Section 0, version 2.2; 9.3; 13.2 |
| Keep the repository public | 13.1, row 26; 8.6 |
| Audit the plan and fix what is wrong | Section 0, version 2.1 |
| Start development | 13.1, row 24; `progress.md` |

---

## 13. Decisions taken, and questions still open

### 13.1 Decisions

| # | Date | Question | Decision |
|---|---|---|---|
| 1 | 24 Nov 2026 | Stages | First presentation on 26 November, then an interim report if asked, then the final presentation (now 15 December, row 21) |
| 2 | 24 Nov 2026 | Members | Kartik Joshi, Prem Kukreja, Samuel Alex, Gagandeep Singh. Who does what is decided by you, not in this plan (9.3) |
| 3 | 24 Nov 2026 | BigQuery sandbox | Yes, one sandbox, on the master laptop |
| 4 | 24 Nov 2026 | Downloads | Approved and done |
| 5 | 24 Nov 2026 | Papers we cannot reach | The group will download them from links provided |
| 6 | 24 Nov 2026 | Usefulness rule | Four checks with the 1-in-25 line (6.7) |
| 7 | 24 Nov 2026 | Never-frozen wallets | No address-level score anywhere; the replay shows frozen wallets only |
| 8 | 24 Nov 2026 | GraphSAGE | Kept only if it beats LightGBM on Tune data (3.3) |
| 9 | 24 Nov 2026 | Brief | Corrected; original kept in `archive/` |
| 10 | 24 Nov 2026 | Deliverables | Report, NotebookLM slides, live dashboard in the last stage |
| 11 | 24 Nov 2026 | Ethics approval | Not needed |
| 12 | 24 Nov 2026 | Repository | Public now, private at the end. Changed by row 26 |
| 13 | 25 Nov 2026 | Live trial | Approved: weekly for four weeks, sealed list, 30-day wait, totals; only if all four checks pass. Changed by rows 22 and 23 to fit 15 December |
| 14 | 25 Nov 2026 | Rule details | Agreed: thin or silent wallets set aside and counted; very busy wallets left out; model kept by most right warnings on Tune months at 1,000 a month; right means a vote within 30 days |
| 15 | 25 Nov 2026 | Novelty wording | Six additions; "we found no published tool that does all of these" |
| 16 | 26 Nov 2026 | Master laptop | The laptop this repository was set up on (9.5) |
| 17 | 26 Nov 2026 | Project name | **FrostLine**, kept because it fits: frost is the first sign of a freeze, and the line is our warning line. Our searches found no crypto or stablecoin project with this name; on GitHub it is used by a plant-hardiness dataset and by game projects |
| 18 | 26 Nov 2026 | Development stack | Section 8 and 7.3.4 |
| 19 | 26 Nov 2026 | Knowledge graph | Only the small evidence graph in DuckDB (3.7) |
| 20 | 26 Nov 2026 | Sealing | A Merkle root over salted entries (6.9) |
| 21 | 26 Nov 2026 | Final presentation | Tuesday 15 December 2026 |
| 22 | 26 Nov 2026 | Trial timing | Daily lists from the lock, a held-out check, results "so far" on 15 December, final totals after the last window (6.9) |
| 23 | 26 Nov 2026 | If the four checks fail | The daily lists still run, labelled as a demonstration of the method, not a trial |
| 24 | 26 Nov 2026 | Development gate | Given: "audit the plan thoroughly, check for errors, bugs, mistakes, missing things and fix if anything is found, then start the development plan" |
| 25 | 26 Nov 2026 | Work packages | Four groups of work (9.3). Owners are decided by you |
| 26 | 26 Nov 2026 | Repository | Public, at https://github.com/KartikJoshi23/FrostLine (your decision). Row 12 still applies |
| 27 | 26 Nov 2026 | Unrequested documents | The `proposal/` folder and the copy of plan version 1 were moved to the Recycle Bin |

Rows 17 to 20, 22, 23 and 25 were chosen by Claude on 26 November 2026, as asked: "select the best possible option according to you for other decisions". They are method and planning choices only. Rows 16, 21, 24 and 26 come from you. Who does what is never decided in this plan.

### 13.2 Still open: steps only you can take

1. Register a free TronGrid key and put it in `.env` on the master laptop. Each member does the same on their own laptop.
2. Create the Google Cloud project with the BigQuery sandbox on the master laptop and sign in, so the sizing query and the dry run can run.
3. Who owns each work package and phase (9.3), and who keeps the encrypted backup of the trial store (6.9).
4. ⛔ Approval of the main pull once its dry-run size is shown (target 28 November).
5. The interim report date, if there is one.
6. The papers in Appendix B that only you can open.

---

## Appendix A. Corrections and updates to the brief

| Brief | Correction |
|---|---|
| §5: count "reached" 8,206 | 8,206 is still-frozen. Ever-frozen on 8 November is 9,191 |
| §12: record does not name features or explain normals | The record's notebook does both |
| §12: labels rebuilt from BigQuery | Labels came from TronGrid; transfers came from BigQuery |
| §12: two data sources | RQ3, RQ4 and RQ5 need more (2.1) |
| §15: exact freeze time | True, but the vote is public earlier |
| §2 and §6: five lists | Six groups; poisoning factories (0 of 17) were omitted |
| §4 and §6: FATF para 66 | Also names identification on a national sanctions list |
| §8: Box 3 | Payments to trafficked workers |
| §8: destinations | Cite the [November sentencing release](https://www.justice.gov/usao-edva/pr/venezuelan-national-sentenced-12-years-prison-laundering-over-billion-dollars-illicit), not the charging release |
| §2: "four things" | Five research questions |
| §13: "meets a FATF request" | FATF asks jurisdictions; we do not measure P2P volume |
| Not in brief | T3 reportedly ended in August 2026; a new Tron, Tether and Chainalysis task force started on 12 November 2026 |
| §13: UAE paper "tells firms to use" freezes | It says firms should monitor them and that analytics may include them |
| §7: P2P seller "was not an accused person" | Not confirmed by the law-firm summary we could read |
| Not in brief | `DestroyedBlackFunds` as a third event; release clustering |

## Appendix B. Not verified or not read

- UAE FIU report (403). Madras High Court order: not read, but a [law-firm summary](https://prismlawfirm.com/madras-high-court-on-freezing-of-bank-accounts-relief-to-crypto-trader/) confirms the defreeze and the Rs 3 lakh lien.
- The paper behind Zenodo 24031003, the article behind the Taiwan data, AMLBot's full report, Griffin et al. (2025).
- Whether BigQuery rows are complete and current, and how far behind the chain they run: needs an account (P0).
- BigQuery download route in the sandbox: to be tested in P0.
- TronGrid free quota: official pages say it varies; third parties say about 100,000 calls a day. Our quota guard stays well below that.
- Licences of exchange proof-of-reserve pages.
- Monthly active USDT wallets on TRON: only a sponsored report's figure; our sizing query will measure it.
- Bitquery says one key controls freezes and BlockSec says frozen wallets cannot receive. Both conflict with the chain and with other sources; we use the chain.
- Whether Pandera 0.36 works with Polars 2.x, and our queries with DuckDB 2.0: tested in P0.
- Whether DuckDB 2.0.1 installs on Python 3.13 on Windows: PyPI lists Windows wheels tagged 3.11 and 3.12.
- Speed of the AI helper models and the dashboard's frame rate on our laptops: measured in P9 and P11.
- Whether the installed pnpm (10.30.3) supports `minimumReleaseAge`: the current documentation describes it; checked in P0.
