# FrostLine: Progress

This is the handover file. Read it first. Update it at the end of every session, even if nothing worked. The newest log entry goes at the top of section 10.

- **Repository:** https://github.com/KartikJoshi23/FrostLine (public).
- **Master laptop:** the laptop this repository was set up on. It holds the official data copy and alone runs the official steps (main BigQuery pull, analysis lock, Test scoring, daily live lists, sealing). See plan 9.5.
- **Plan:** `implementation-plan.md`, version 2.3 (26 November 2026). The plan wins over this file, unless this file records a later group decision.
- **Brief:** `Before-the-freeze-Problem-Statement.md`. **Audit:** `audit-log.md`. **Data sources:** `data/raw/SOURCES.md`.
- **Prompt for every new Claude Code session:** `collaborator-prompt.md`.
- **Final presentation: Tuesday 15 December 2026.** Day-by-day schedule: plan 9.2.
- **Who does what** is decided by the team and written here. Claude never assigns it.

---

## 1. Snapshot

| Item | Now |
|---|---|
| Stage | Development, started 26 November 2026 |
| Development gate | **Given** on 26 November 2026 (section 2) |
| Current phase | **P1 done** on branch `p1/registry` (not merged yet): registry, votes, list dates, court labels, seed list, evidence-graph base tables, batch rule; every audited number reproduced. **P0** still waits for the TronGrid key, the BigQuery sandbox, the sizing query and the BigQuery delay check |
| Next step | (1) Review and merge P1. (2) BigQuery sandbox on the master laptop, then the sizing query and the main pull's dry run, so the size can be approved by 28 November. (3) TronGrid key for P10. P2, P10 and P11 can start in parallel from 27 November |
| Owners | To be assigned by the team (section 4) |
| Blockers | TronGrid key and BigQuery sandbox (plan 13.2) |
| Last updated | 26 November 2026, master laptop, Claude Code session |

## 2. Gates and approvals

| Date | Gate or decision | Where | Record |
|---|---|---|---|
| 24 Nov 2026 | Research direction D1 + D2 + D3 | Master laptop session | "Approve D1 + D2 + D3" |
| 24 Nov 2026 | Twelve planning decisions | Master laptop session | Plan 13.1, rows 1 to 12 |
| 25 Nov 2026 | Four-week live trial (since changed to fit 15 December) | Master laptop session | Plan 13.1, row 13 |
| 25 Nov 2026 | Four rule details | Master laptop session | "We agree on all four, keep them" |
| 26 Nov 2026 | First presentation done; this laptop is the master laptop | Master laptop session | "this will be the master laptop" |
| 26 Nov 2026 | Unrequested proposal documents removed | Master laptop session | "No proposal was told to made, so clean up all such useless things which were not told to build" |
| 26 Nov 2026 | Final presentation on 15 December 2026 | Master laptop session | "final presentation is on 15th December" |
| 26 Nov 2026 | Open method decisions left to Claude | Master laptop session | "select the best possible option according to you for other decisions" (plan 13.1, rows 17 to 20, 22, 23 and 25) |
| 26 Nov 2026 | Name FrostLine kept | Master laptop session | "if FrostLine makes really sense and is relevant than continue" |
| 26 Nov 2026 | **Development go-ahead** | Master laptop session | "audit the plan thoroughly, check for errors, bugs, mistakes, missing things and fix if anything is found, then start the development plan" |
| 26 Nov 2026 | Decisions about team members belong to the team only | Master laptop session | "you are not allowed to do any such thing, leave that to me, I will tell such information, do not assume anything like that" |
| 26 Nov 2026 | Public GitHub repository | Master laptop session | "https://github.com/KartikJoshi23/FrostLine - github repo, will keep it public as of now" |
| 26 Nov 2026 | P1 started | Master laptop session | "Start P1" |
| – | Main BigQuery pull (about 640 GB, after a dry run) | – | Not given; target 28 November |
| – | Ollama model download (about 2.5 GB) | – | Not given; needed in P9 |
| – | Analysis lock | – | Target 4 December, latest 6 December |
| – | Live lists count as a trial | – | Only if the verdict is "Useful early warning" |

## 3. Phase board

| Phase | Work | Owner | Dates | Status | Notes |
|---|---|---|---|---|---|
| P0 | Setup | To be assigned | 26–27 Nov | In progress | Waiting: TronGrid key, BigQuery sandbox, sizing query, BigQuery delay check |
| P1 | Registry and lists | To be assigned | 26 Nov | Done | Branch `p1/registry`, not merged. All 2.2 checks pass; split counts settled |
| P2 | Benchmark | To be assigned | 27–29 Nov | Not started | |
| P3 | Main pull | To be assigned | 28–30 Nov | Not started | ⛔ needs approval after the dry run |
| P4 | Features and controls | To be assigned | 1–2 Dec | Not started | |
| P5 | D1 models, lock, Test results | To be assigned | 3–4 Dec | Not started | ⛔ analysis lock |
| P6 | D2 freeze types | To be assigned | 5–8 Dec | Not started | |
| P7 | D3 cost to frame | To be assigned | 5–8 Dec | Not started | |
| P8 | Networks and list F | To be assigned | 1–8 Dec | Not started | |
| P9 | Serving and AI helpers | To be assigned | 1–9 Dec | Not started | |
| P10 | Live service | To be assigned | 27 Nov–3 Dec | Not started | Sample recording on 27 Nov for the dashboard |
| P11 | Dashboard | To be assigned | 27 Nov–12 Dec | Not started | Skeleton from P0 builds and passes its tests |
| P12 | Live lists | To be assigned | 2–14 Dec | Not started | Rehearsals 2 and 3 Dec; first list 5 Dec |
| P13 | Quality and final pack | To be assigned | 5–13 Dec | Not started | |

Status words: Not started, In progress, Blocked, In review, Done.

## 4. Work packages

The groups of work are in plan 9.3. Owners are written here by the team.

| Package | Owner |
|---|---|
| A. Data, live feed and official runs | To be assigned |
| B. Early warning | To be assigned |
| C. Labels, networks, evidence graph, AI helpers | To be assigned |
| D. Serving and dashboard | To be assigned |
| Encrypted backup of the trial store | To be assigned |

## 5. Environment on the master laptop (26 November 2026)

| Item | State |
|---|---|
| Python | 3.12.13 installed through uv 0.11.28 (uv printed a harmless warning about a version shortcut link). `.venv` holds all 241 locked packages, including every optional group |
| Install rule | `uv.lock` resolved with `exclude-newer = 2026-11-12`; `dashboard/pnpm-workspace.yaml` sets `minimumReleaseAge: 20160` (14 days) |
| Key versions | DuckDB 2.0.0, Polars 2.1.0, pandas 3.1.1, PyArrow 26.0.1, Pandera 0.36.0, Dagster 1.13.29, MLflow 3.18.0, scikit-learn 1.9.1, LightGBM 4.7.0, NetworkX 3.7, PyTorch 2.15.0 (CPU), PyTorch Geometric 2.8.1, NetworKit 11.3, LangGraph 1.2.20, FastAPI 0.162.5, httpx 0.28.1, Ruff 0.17.4 |
| Dashboard | Node 22.21.1, pnpm 10.30.3; React 19.3.1, TypeScript 5.9.3, Vite 8.3.8, Motion 14.13.0, GSAP 3.15.1, three 0.187.0 and the rest of plan 7.3.4 |
| git | `main` (first commit, CI passed) and `p1/registry` (P1 work); remote https://github.com/KartikJoshi23/FrostLine; pre-commit hooks installed |
| Ollama | Not installed (P9, after the download is approved) |
| Hardware | 8 threads, 16 GB RAM, 2 GB GPU, about 197 GB free on D: |

**P0 findings**
1. DuckDB 2.0.0, Polars 2.1.0 with Pandera 0.36.0, Dagster's blocking checks and LightGBM's contributions all work for our needs (`tests/test_stack.py`).
2. The OpenTimestamps `ots` command fails on Windows, because python-bitcoinlib 0.12.2 looks for an old OpenSSL library. The `opentimestamps` library's calendar client works, so P12 stamps through it (plan 8.1).
3. Every optional group installs and imports on Windows.
4. Plain `uv sync` removes the optional groups. Use `uv sync --all-extras` to keep them.

**Rerun P1 on the master laptop:** `uv run python -m frostline.registry.pull`, then `frostline.registry.build`, `frostline.ofac_history`, `frostline.lists`, `frostline.seeds` and `frostline.kg` (each with `uv run python -m`). Or run them all in order, with the blocking checks, from Dagster: `uv run dagster dev -m pipelines.definitions`.

**Set up another laptop:** clone the repository; `uv sync --all-extras`; `uv run pre-commit install`; in `dashboard/`, `pnpm install --frozen-lockfile`; copy `.env.example` to `.env` and add your own TronGrid key; `uv run pytest` and `pnpm test` must pass.

## 6. Data state

| Item | State |
|---|---|
| `data/raw` | Downloaded on 24 November 2026; `data/MANIFEST.csv` lists 29 files with SHA-256 and verifies (`uv run python -m frostline.manifest verify`). Other laptops get the files through a private shared folder, then run the same check |
| BigQuery | Nothing queried. Main pull about 640 GB, best run by 30 November in November's allowance (plan 2.3) |
| TronGrid | Event census to the end of 23 November 2026 from the audit (temporary scripts; rebuilt in P1) |
| Registry (P1) | `data/interim/registry/`: 11,728 freeze, release and destroy events to 26 Nov 2026 15:16 UTC; 12,052 votes, 11,918 executions; 9,416 wallets (frozen or voted on). Every audited number reproduced at the 24 November cut-off (`summary.json`) |
| Lists (P1) | `data/interim/lists/`: OFAC 352 (348 dated from the mirror's history), UK 49, EU 3, NBCTF 688 (590 active); 1,038 distinct; 993 of them frozen by the cut-off. Court labels: 640 TRON wallets (480 fraud platform, 160 pseudo broker) |
| Seed list (P1) | `data/final/seed_wallets.csv`: 19,348 wallets (registry, lists, court labels, 9,249 Early Detection normals). Fingerprint in section 8 |
| Evidence graph (P1) | `data/interim/kg/`: 21,427 nodes, 32,285 dated facts (644 undated: court labels and 4 OFAC entries) |
| Transfer store, features, models | None yet |
| `archive/` | Local only (git-ignored): the original brief |
| Third-party PDFs in the root folder | Local only (git-ignored) |

## 7. Quotas used

| Month | BigQuery scanned (of 1 TiB free) | TronGrid calls, peak day | Notes |
|---|---|---|---|
| November 2026 | 0 | 26 Nov: 316 TronGrid calls without a key (P1 pull), plus a few test calls; GitHub: about 10 API calls and 38 files (OFAC history) | The free BigQuery month ends on 30 November |

## 8. Locks, seals and live lists

| Item | Target date | SHA-256 or Merkle root | Bitcoin block | Notes |
|---|---|---|---|---|
| Seed list, fixed before the pull (plan 2.3) | 26 Nov 2026 | SHA-256 `546809ec7d1a54b994a4901b33bac4ceb32d15a688e1c0b2e8c00220ddb57f7c` | – | 19,348 wallets in `data/final/seed_wallets.csv` |
| Ten rules and analysis lock | 4 Dec 2026 (latest 6 Dec) | – | – | Before any Test score (plan 6.6) |
| Rehearsal runs | 2 and 3 Dec 2026 | – | – | Never judged |
| Daily live lists | 5 to 14 Dec 2026 | – | – | One row per list, added when sealed: date, root, block, size, hits so far |

## 9. Decisions waiting

| Decision | Who decides |
|---|---|
| Owners of the work packages and phases (sections 3 and 4) | The team |
| Who keeps the encrypted backup of the trial store | The team |
| Interim report date, if there is one | The team |

## 10. Session log (newest first)

### 26 November 2026, night · master laptop · Claude Code session · P1

- **Done (P1, branch `p1/registry`):** TronGrid client with the quota guard; pull of every freeze, release, destroy, vote and execution event (316 calls, no key); registry linking each freeze to its vote through the shared transaction, with never-executed votes decoded from their call data; S as the earliest vote; batches and splits; OFAC listing dates from the mirror's history; UK, EU and NBCTF lists and court labels, reading no names; seed list with its fingerprint; evidence-graph base tables; Dagster assets with blocking checks.
- **Checks run:** every audited number reproduced at the 24 November cut-off (9,357 freezes, 9,317 wallets ever frozen, 9,328 freezes matched to votes, 1,508 batches, largest 779 on 12 Jul 2025, 18 wallets with an earlier unexecuted vote, the split counts, and the rest in `src/frostline/registry/expected.py`). `uv run pytest`: 56 passed. `ruff check` and `ruff format --check`: clean. Manifest: 51 files, verified. CI on `main`: passed.
- **Findings:** (1) the plan's split table is exact; the audit's 591/759 came from counting with executed votes only; (2) court labels are 640 wallets, not 638; (3) the Early Detection table writes frozen wallets as `T…` and normal ones as `0x…`, which alone gives the label away, so every address is converted on load. Plan version 2.3 records all three.
- **Files:** `src/frostline/` (`tron.py`, `trongrid.py`, `jsonl.py`, `registry/`, `lists.py`, `ofac_history.py`, `seeds.py`, `kg.py`), `pipelines/definitions.py`, 6 new test files, `implementation-plan.md`, `progress.md`, `data/MANIFEST.csv`.
- **Next step:** review and merge `p1/registry`; then the BigQuery sandbox and P3's dry run.

### 26 November 2026, late evening · master laptop · Claude Code session

- **Correction:** version 2.1 of the plan, this file and the memory notes had named owners for work packages and phases, and had said whose laptop the master laptop is. Nobody had asked for that. All of it was removed: owners now say "to be assigned", and the master laptop is described only as the laptop this repository was set up on. A rule against it was added to `collaborator-prompt.md`.
- **Repository:** recorded as public at https://github.com/KartikJoshi23/FrostLine (plan 13.1, row 26); version 2.1's "private until the lock" is withdrawn. This entry is part of the first commit pushed to it. Commits from the master laptop use the account's GitHub noreply email (set for this repository only), so no personal email address is published.
- **Files:** `implementation-plan.md` (version 2.2), `progress.md`, `collaborator-prompt.md`.
- **Next step:** the team writes the owners into sections 3 and 4; the master laptop gets a TronGrid key and the BigQuery sandbox.

### 26 November 2026, evening · master laptop · Claude Code session

- **Done:** moved the unrequested `proposal/` folder (10 files) and the plan v1 copy to the Recycle Bin; audited the plan and fixed seven errors (plan section 0); fitted the trial to 15 December (daily sealed lists from the lock, a held-out check, results "so far"); settled the open method decisions; wrote a day-by-day schedule and a run sheet for the day; started P0.
- **P0 files:** `pyproject.toml`, `uv.lock`, `.python-version`, `config/settings.toml`, `src/frostline/` (`config.py`, `manifest.py`, `safety.py`), `tests/` (4 files), `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `.gitignore`, `.gitattributes`, `.env.example`, `data/MANIFEST.csv`, `dashboard/` (Vite, React and TypeScript skeleton with its lock file).
- **Checks run:** `uv run pytest`: 32 passed. `uv run ruff check` and `ruff format --check`: clean. Dashboard: `pnpm test` 4 passed, `pnpm build` and `pnpm lint` clean. pre-commit on the staged files: all hooks passed. Manifest: verified.

### 26 November 2026, afternoon · master laptop · Claude Code planning session

- **Done:** tool audit (versions, licences, Windows support); the evidence-graph decision; the live service, live trial and dashboard design; the name FrostLine; plan version 2; `progress.md` and `collaborator-prompt.md`.
- **Checks run:** PyPI and npm metadata; TronGrid gives 200 events per page; TRON averaged 3.0 seconds per block over 1,000 blocks.

### 24 and 25 November 2026 · master laptop · earlier sessions

Phase 1 checks, Phase 2 direction, plan version 1, two audits and the explainer page. Details are in `audit-log.md` and in the plan's section 13 and appendices.

## 11. How to update this file

- Update it at the end of every session, before the last commit.
- Change the snapshot (1), the phase board (3), the quotas (7) and, when they change, the gates (2), the owners (4), the locks and lists (8) and the open decisions (9).
- Add one log entry at the top of section 10: date, laptop, what was done, files, checks or tests and their results, decisions with where they were made, blockers, and the exact next step.
- Owners and roles are written only as the team gives them.
- Never delete old entries. Correct a mistake with a new line that says what was wrong.
- Facts only, in short lines. Never write keys, salts, sealed-list contents or scores of never-frozen wallets here.
