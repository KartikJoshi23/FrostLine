"""Dagster runs the P1 steps in order; a failed blocking check stops the line (plan 7.1).

uv run dagster dev -m pipelines.definitions
"""

from __future__ import annotations

import json

import dagster as dg

from frostline import kg, lists, seeds
from frostline.config import load_env
from frostline.registry import build as registry_build
from frostline.registry import pull as registry_pull
from frostline.trongrid import TronGrid

EXPECTED_LISTS = {"OFAC": 352, "UK": 49, "EU": 3, "NBCTF": 688}


@dg.asset(group_name="registry", description="Freeze and vote events from TronGrid, append-only.")
def trongrid_events() -> dg.MaterializeResult:
    load_env()
    client = TronGrid()
    added = registry_pull.pull_events(client)
    added["proposal_transactions"] = registry_pull.pull_unexecuted_proposals(client)
    return dg.MaterializeResult(metadata={"calls": client.calls, **added})


@dg.asset(
    deps=[trongrid_events], group_name="registry", description="One row per wallet (plan 2.2)."
)
def freeze_registry() -> dg.MaterializeResult:
    s = registry_build.build()
    return dg.MaterializeResult(metadata={"wallets": s["wallets"], "events": s["events"]})


@dg.asset_check(
    asset=freeze_registry, blocking=True, description="Every audited number reproduced."
)
def registry_matches_audit() -> dg.AssetCheckResult:
    s = json.loads((registry_build.OUT / "summary.json").read_text(encoding="utf-8"))
    diff = s["audit_differences"]
    return dg.AssetCheckResult(passed=not diff, metadata={"differences": ", ".join(diff) or "none"})


@dg.asset(group_name="lists", description="Official-list wallets and court labels; no names.")
def official_lists() -> dg.MaterializeResult:
    s = lists.build()
    return dg.MaterializeResult(metadata={"distinct": s["distinct_list_wallets"], **s["by_source"]})


@dg.asset_check(asset=official_lists, blocking=True, description="List counts as audited.")
def lists_match_audit() -> dg.AssetCheckResult:
    s = json.loads((lists.OUT / "summary.json").read_text(encoding="utf-8"))
    ok = s["by_source"] == EXPECTED_LISTS and s["distinct_list_wallets"] == 1038
    return dg.AssetCheckResult(passed=ok, metadata={"by_source": json.dumps(s["by_source"])})


@dg.asset(
    deps=[freeze_registry, official_lists], group_name="seeds", description="Fixed before the pull."
)
def seed_wallets() -> dg.MaterializeResult:
    s = seeds.build()
    return dg.MaterializeResult(
        metadata={"seed_wallets": s["seed_wallets"], "sha256": s["seed_csv_sha256"]}
    )


@dg.asset(
    deps=[freeze_registry, official_lists], group_name="evidence_graph", description="Plan 3.7."
)
def evidence_graph() -> dg.MaterializeResult:
    s = kg.build()
    return dg.MaterializeResult(metadata={"nodes": s["nodes"], "edges": s["edges"]})


defs = dg.Definitions(
    assets=[trongrid_events, freeze_registry, official_lists, seed_wallets, evidence_graph],
    asset_checks=[registry_matches_audit, lists_match_audit],
)
