# Audit log, 24 November 2026

Scope: the problem statement, the implementation plan, the proposal pack, the figures, the downloaded data and the support files. Every chain number was recomputed from a fresh pull of the freeze, release, destruction and multisig events, with newly written scripts. All counts now use one fixed cut-off: **events to the end of 23 November 2026 (UTC)**.

## A. Wrong or fragile facts, corrected

| # | Was | Now | Cause |
|---|---|---|---|
| 1 | 98 of 346 OFAC-listed addresses frozen before listing | 46 frozen more than a week before; 300 within two days; none later | 52 of the 98 were only one to two days early, which is inside the dating error |
| 2 | Lists match 938 addresses, 10.1% | 993, 10.7% | Incomplete Israeli file used (590 of 688 TRON addresses); one entry had Cyrillic lookalike letters |
| 3 | "Nine in ten freezes have no public reason" | "On none of the four lists we checked" | Court seizures and press releases are public reasons too |
| 4 | Benchmark lacks 1,095 accounts and misses some transfers | Lacks 1,061; no sign of missing transfers | The table ends on 14 October; 34 later freezes were counted by mistake, and the sample was drawn from the wrong set |
| 5 | 44 of 74 wallets had lookalike senders | 70 of 133 | Rule was too loose (last four characters only; strict rule gives 40 of 74). A second independent sample was added |
| 6 | Gap quoted as 64, 145 and 8 minutes in text, but 23 in Figure 2 | One measure, per batch: 68 overall, 103 for 2024–25, 23 for 2026 | Event-level and batch-level medians were mixed |
| 7 | Frozen and normal transfer sizes $31,458 and $510 beside a 2026 AUC | $26,040 and $514, same 2026 rows as the AUC | Medians and AUC used different rows |
| 8 | Comparison tables said "Ours: Yes" | "Ours (planned)" | Nothing is built yet |
| 9 | FreezeCheck: "hits only" | Adds its flagged share of 287 other wallets | Unfair to the source |
| 10 | Every freeze "matched to its public proposal" | 9,328 of 9,357; 29 early ones cannot be matched | Overstated |
| 11 | A real case described as "innocent people" | "Ordinary holders" | The court case is still under investigation |
| 12 | "25 files downloaded and inspected", then "eight sources" | "About 81 MB from seven sources, with checksums" | Not every file was inspected; FreezeCheck's three records are one source |
| 13 | Batch figure credited to FreezeCheck in the brief | Credited to our own count | Wrong attribution |
| 14 | Every TRON freeze is proposed first | Freezes since early 2021 | Earlier ones were not |

## B. Design bugs in the plan, fixed

| # | Bug | Fix |
|---|---|---|
| 1 | Cut-off used the executed proposal | Uses the **earliest** proposal. 18 addresses had an earlier, unexecuted one, up to 34 days before |
| 2 | Gate 2 used recall at 1-in-25, so it failed whenever gate 3 failed | Gate 2 now compares at a fixed workload of 1,000 alerts a month |
| 3 | Verdict table did not cover every outcome | Six ordered verdicts |
| 4 | The planting test (P7) ran before the model it needs existed | P7 depends on P5; P6 needs P5's model code |
| 5 | Analysis lock covered only P5 | Comes before all test work in P5 to P8 |
| 6 | Zenodo normals were not in the data pull, so waterfall steps 3 to 6 were impossible | Added to the pull |
| 7 | One exchange wallet in the sample could return tens of millions of rows | Account-months over 5,000 transfers come back as summaries |
| 8 | Deposit-like rule needed 24-hour data, but only monthly summaries were pulled | Rule rewritten for monthly data |
| 9 | Held-out November data was outside the pull window | Later small pull planned |
| 10 | Calendar replay did not define a hit | Day 7 after scoring to day 6 after the next scoring |
| 11 | Court addresses were scored at their last activity, which uses hindsight | Scored monthly while active |
| 12 | Freeze types mixed origin and outcome | Separated |
| 13 | Proposed-only addresses were removed using later knowledge | They leave the pool at their proposal |
| 14 | Set B tested variables it was matched on | Matched variables reported against Set A only |
| 15 | "Never sent more than 10 USDT" looked into the future | Judged by time t |
| 16 | Confidence intervals treated batches of one operator as independent | Repeated with network communities |

## C. Support files, fixed

- `data/raw/checksums.md5` could not be verified (Windows line endings). Rewritten; all 27 files now verify.
- `.gitignore` hid the source list, the checksums and our proposal PDF. Rewritten and tested in a scratch repository: third-party data, PDFs, keys and archives stay out.
- NotebookLM prompt banned company names that the slides need. Reworded.
- Stale lines in the plan (old sizes, old counts, "brief's own title") and reference order in the brief.

## D. Checked and confirmed

- Bitquery's 8,017 events and 7,987 addresses, FreezeCheck's 8,206 and its 4,221-event window, and 447 releases in 26 minutes were all reproduced.
- The multisig was read on chain: three owners, two signatures required, and it owns the USDT contract.
- All split counts and batches were reproduced. No batch crosses a split boundary.
- Benchmark AUCs (0.906 and 0.909) were reproduced with a second library, with the direction fixed on training rows.
- "Four in five freezes come after a week" holds for TRON in our own check: 77.5%, or 81.2% in 2026.
- Planted records: 37 of 37 zero-value outflows signed by someone else; 52 of 53 normal outflows signed by the wallet.
- The OFAC mirror updated in most months with no gap we could find.
- The July 2025 batch: none of 45 sampled addresses had any USDT transfer before the freeze.

## E. Still open

- Not read: Madras High Court order, UAE FIU report, AMLBot's full report, Griffin et al. (2025), and the papers behind the Zenodo and Taiwan data.
- Whether the Madras seller "was not an accused person" is not confirmed by the summary we read.
- The number of monthly stablecoin users on TRON comes from a sponsored report.
- Israeli orders get renewed, so their dates may not be the first order.
- BigQuery access, completeness and the download route are untested.
- Figures 1 and 2 in the brief's own PDF still need the corrections made in the text.
