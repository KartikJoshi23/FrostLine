"""Acceptance checks on the built P1 tables (plan 2.2). Skipped where the data are not present,
for example in CI, which has no data."""

import json

import pytest

from frostline.config import FINAL, INTERIM

REG = INTERIM / "registry" / "summary.json"
LISTS = INTERIM / "lists" / "summary.json"
SEEDS = FINAL / "seed_summary.json"


@pytest.mark.skipif(not REG.is_file(), reason="registry not built on this laptop")
def test_registry_reproduces_every_audited_number():
    s = json.loads(REG.read_text(encoding="utf-8"))
    assert s["audit_differences"] == []


@pytest.mark.skipif(not LISTS.is_file(), reason="lists not built on this laptop")
def test_list_counts():
    s = json.loads(LISTS.read_text(encoding="utf-8"))
    assert s["by_source"] == {"OFAC": 352, "UK": 49, "EU": 3, "NBCTF": 688}
    assert s["nbctf_active"] == 590
    assert s["distinct_list_wallets"] == 1038
    assert s["court_by_role"] == {"fraud platform": 480, "pseudo broker": 160}


@pytest.mark.skipif(not SEEDS.is_file(), reason="seed list not built on this laptop")
def test_seed_list_and_overlap():
    s = json.loads(SEEDS.read_text(encoding="utf-8"))
    assert s["list_wallets_ever_frozen_at_audit_cut"] == 993
    assert s["zenodo_normals"] == 9249
    assert len(s["seed_csv_sha256"]) == 64
