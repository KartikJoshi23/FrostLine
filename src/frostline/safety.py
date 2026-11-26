"""Pre-commit check: block data, keys and sealed lists from git (plan 9.5).

pre-commit passes the staged file names. Any forbidden path fails the commit,
even if someone forced it past .gitignore.
"""

from __future__ import annotations

import sys
from fnmatch import fnmatch
from pathlib import PurePosixPath

ALLOWED = {"data/raw/SOURCES.md", "data/raw/checksums.md5", "data/MANIFEST.csv", ".env.example"}
FORBIDDEN = [
    "data/*",
    "trial_store/*",
    ".env",
    ".env.*",
    "*.key",
    "*.pem",
    "*.parquet",
    "*.duckdb",
    "*.duckdb.wal",
]


def is_forbidden(name: str) -> bool:
    path = PurePosixPath(name.replace("\\", "/")).as_posix()
    if path in ALLOWED:
        return False
    base = PurePosixPath(path).name
    return any(fnmatch(path, pat) or fnmatch(base, pat) for pat in FORBIDDEN)


def main(argv: list[str] | None = None) -> int:
    names = sys.argv[1:] if argv is None else argv
    bad = [n for n in names if is_forbidden(n)]
    for n in bad:
        print(f"blocked: {n} (data, keys and sealed lists never go into git; plan 9.5)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
