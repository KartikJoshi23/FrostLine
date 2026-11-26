"""Build and check data/MANIFEST.csv (plan 9.5).

Data never go into git. The manifest lists every data file with its size and
SHA-256, so each laptop can check that its copy matches the master laptop's.

    uv run python -m frostline.manifest build    # write data/MANIFEST.csv
    uv run python -m frostline.manifest verify   # compare files with the manifest
"""

from __future__ import annotations

import csv
import hashlib
import sys
from datetime import UTC, datetime
from pathlib import Path

from frostline.config import ROOT

DATA = ROOT / "data"
MANIFEST = DATA / "MANIFEST.csv"
FIELDS = ["path", "bytes", "sha256", "rows", "made_by", "modified_utc"]
SKIP = {"MANIFEST.csv"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def count_rows(path: Path) -> str:
    """Rows for tabular files; empty for anything else."""
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        import pyarrow.parquet as pq

        return str(pq.ParquetFile(path).metadata.num_rows)
    if suffix == ".csv":
        with path.open("rb") as f:
            lines = sum(1 for _ in f)
        return str(max(lines - 1, 0))
    return ""


def made_by(rel: str) -> str:
    if rel.startswith("raw/"):
        return "download, see data/raw/SOURCES.md"
    return "pipeline"


def scan(data_dir: Path = DATA) -> list[dict[str, str]]:
    rows = []
    for path in sorted(p for p in data_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(data_dir).as_posix()
        if path.name in SKIP:
            continue
        stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
        rows.append(
            {
                "path": rel,
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
                "rows": count_rows(path),
                "made_by": made_by(rel),
                "modified_utc": stamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )
    return rows


def write(rows: list[dict[str, str]], manifest: Path = MANIFEST) -> None:
    with manifest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def read(manifest: Path = MANIFEST) -> list[dict[str, str]]:
    with manifest.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify(data_dir: Path = DATA, manifest: Path = MANIFEST) -> list[str]:
    """Return a list of problems; an empty list means every file matches."""
    expected = {r["path"]: r for r in read(manifest)}
    problems = []
    for rel, row in expected.items():
        path = data_dir / rel
        if not path.is_file():
            problems.append(f"missing: {rel}")
        elif sha256(path) != row["sha256"]:
            problems.append(f"changed: {rel}")
    present = {r["path"] for r in scan(data_dir)}
    problems += [f"not in manifest: {rel}" for rel in sorted(present - set(expected))]
    return problems


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args == ["build"]:
        rows = scan()
        write(rows)
        print(f"wrote {MANIFEST.relative_to(ROOT).as_posix()}: {len(rows)} files")
        return 0
    if args == ["verify"]:
        problems = verify()
        for p in problems:
            print(p)
        print("manifest OK" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0
    print("usage: python -m frostline.manifest build|verify")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
