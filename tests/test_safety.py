import pytest

from frostline.config import ROOT
from frostline.safety import is_forbidden, main


@pytest.mark.parametrize(
    "name",
    [
        ".env",
        "config/.env",
        ".env.local",
        "data/raw/ofac_mirror/sanctioned.json",
        "data\\final\\scores.parquet",
        "trial_store/2026-12-05/salts.json",
        "keys/tron.key",
        "out/scores.parquet",
        "store.duckdb",
    ],
)
def test_blocked(name):
    assert is_forbidden(name)


@pytest.mark.parametrize(
    "name",
    [
        ".env.example",
        "data/raw/SOURCES.md",
        "data/raw/checksums.md5",
        "data/MANIFEST.csv",
        "trial/2026-12-05/root.txt",
        "src/frostline/safety.py",
        "dashboard/src/data/scenes.ts",
    ],
)
def test_allowed(name):
    assert not is_forbidden(name)


def test_exit_code():
    assert main(["src/x.py"]) == 0
    assert main(["src/x.py", ".env"]) == 1


def test_gitignore_keeps_secrets_and_data_out():
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    for rule in [".env", "data/**", "trial_store/", "*.parquet", "*.pdf", ".venv/", "archive/"]:
        assert rule in lines
