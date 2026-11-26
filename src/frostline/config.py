"""Read the project settings from config/settings.toml.

The values come from implementation-plan.md. Change them only after a group
decision that is recorded in progress.md.
"""

from __future__ import annotations

import tomllib
from functools import cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SETTINGS_FILE = ROOT / "config" / "settings.toml"


@cache
def settings() -> dict[str, Any]:
    """Return all settings as nested dictionaries. The file is read once."""
    with SETTINGS_FILE.open("rb") as f:
        return tomllib.load(f)
