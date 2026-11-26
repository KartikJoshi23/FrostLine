"""Read the project settings from config/settings.toml, and local keys from .env.

The values come from implementation-plan.md. Change them only after a group
decision that is recorded in progress.md.
"""

from __future__ import annotations

import os
import tomllib
from functools import cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SETTINGS_FILE = ROOT / "config" / "settings.toml"
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
FINAL = DATA / "final"


@cache
def settings() -> dict[str, Any]:
    """Return all settings as nested dictionaries. The file is read once."""
    with SETTINGS_FILE.open("rb") as f:
        return tomllib.load(f)


def load_env(path: Path | None = None) -> None:
    """Load KEY=VALUE lines from .env into the environment, without overriding anything set."""
    env_file = path or ROOT / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
