"""Wallets on the official lists, and the court labels (plan 2.1, 5.2).

Names are never loaded (plan 10.1, rule 2): only address, date and status columns
are read. One list entry used Cyrillic letters that look Latin; they are mapped first.

    uv run python -m frostline.lists
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

import polars as pl

from frostline.config import INTERIM, RAW
from frostline.tron import is_address

OUT = INTERIM / "lists"
CYRILLIC = str.maketrans("АВСЕНКМОРТХасеорхуӏ", "ABCEHKMOPTXaceopxyl")
CANDIDATE = re.compile(r"(?=(T[1-9A-HJ-NP-Za-km-z]{33}))")
COURT_CSV = (
    RAW
    / "mendeley_62dmsngtfb_v3"
    / "unzipped"
    / "Judicially Grounded Virtual Asset Address Labels a"
    / "public_release_second_revision2"
    / "judicial_ground_truth_address_labels_public_v2.csv"
)
COURT_ROLES = ("fraud platform", "pseudo broker")


def find_addresses(text: str | None) -> set[str]:
    """Every valid TRON address in a piece of text, after mapping Cyrillic look-alikes."""
    if not text:
        return set()
    fixed = text.translate(CYRILLIC)
    return {m for m in CANDIDATE.findall(fixed) if is_address(m)}


def parse_date(value: str | None) -> date | None:
    v = (value or "").strip()[:10]
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def _read_columns(path: Path, columns: list[str], sep: str = ",") -> pl.DataFrame:
    """Read only the named columns; the header may follow a title line."""
    with path.open(encoding="utf-8-sig", errors="replace") as f:
        lines = [f.readline() for _ in range(5)]
    skip = next(i for i, line in enumerate(lines) if columns[0] in line)
    return pl.read_csv(
        path,
        separator=sep,
        skip_rows=skip,
        columns=columns,
        infer_schema=False,
        encoding="utf8-lossy",
        truncate_ragged_lines=True,
    )


def _earliest(rows: list[dict]) -> list[dict]:
    """One row per (wallet, source), keeping the earliest known date."""
    best: dict[tuple[str, str], dict] = {}
    for r in rows:
        k = (r["wallet"], r["source"])
        old = best.get(k)
        if old is None or (
            r["listed_on"] and (not old["listed_on"] or r["listed_on"] < old["listed_on"])
        ):
            best[k] = r
    return sorted(best.values(), key=lambda r: (r["source"], r["wallet"]))


def ofac_entries(raw: Path = RAW) -> list[dict]:
    """OFAC wallets, dated by the mirror's history where it can (frostline.ofac_history)."""
    from frostline.ofac_history import first_seen

    dates, _ = first_seen()
    rows = []
    for name in ("sanctioned_addresses_TRX.txt", "sanctioned_addresses_USDT.txt"):
        text = (raw / "ofac_mirror" / name).read_text(encoding="utf-8", errors="replace")
        for a in find_addresses(text):
            d = dates.get(a)
            listed = parse_date(d) if d else None
            rows.append({"wallet": a, "source": "OFAC", "listed_on": listed, "active": True})
    return _earliest(rows)


def uk_entries(raw: Path = RAW) -> list[dict]:
    df = _read_columns(
        raw / "uk_sanctions" / "UK-Sanctions-List.csv", ["Other Information", "Date Designated"]
    )
    rows = []
    for info, designated in df.iter_rows():
        for a in find_addresses(info):
            rows.append(
                {"wallet": a, "source": "UK", "listed_on": parse_date(designated), "active": True}
            )
    return _earliest(rows)


def eu_entries(raw: Path = RAW) -> list[dict]:
    cols = [
        "Entity_DesignationDate",
        "Entity_Regulation_PublicationDate",
        "NameAlias_Remark",
        "Address_ContactInfo",
        "Address_Remark",
    ]
    df = _read_columns(raw / "eu_sanctions" / "csvFullSanctionsList_1_1.csv", cols, sep=";")
    rows = []
    for designated, published, *texts in df.iter_rows():
        when = parse_date(designated) or parse_date(published)
        for a in set().union(*(find_addresses(t) for t in texts)):
            rows.append({"wallet": a, "source": "EU", "listed_on": when, "active": True})
    return _earliest(rows)


def nbctf_entries(raw: Path = RAW) -> list[dict]:
    df = pl.read_csv(
        raw / "opensanctions_il_mod_crypto" / "nbctf_tron_addresses.csv", infer_schema=False
    )
    rows = []
    for address, order_date, active in df.select(
        "address", "order_date", "active_target"
    ).iter_rows():
        for a in find_addresses(address):
            rows.append(
                {
                    "wallet": a,
                    "source": "NBCTF",
                    "listed_on": parse_date(order_date),
                    "active": active == "True",
                }
            )
    return _earliest(rows)


def court_labels(path: Path = COURT_CSV) -> list[dict]:
    df = pl.read_csv(path, columns=["address", "ground_truth_role_label"], infer_schema=False)
    best: dict[str, str] = {}
    for address, role in df.iter_rows():
        if role in COURT_ROLES:
            for a in find_addresses(address):
                best.setdefault(a, role)
    return [{"wallet": w, "role": r} for w, r in sorted(best.items())]


def build(raw: Path = RAW, out_dir: Path = OUT) -> dict:
    entries = ofac_entries(raw) + uk_entries(raw) + eu_entries(raw) + nbctf_entries(raw)
    court = court_labels(raw / COURT_CSV.relative_to(RAW))
    out_dir.mkdir(parents=True, exist_ok=True)
    schema = {"wallet": pl.String, "source": pl.String, "listed_on": pl.Date, "active": pl.Boolean}
    pl.DataFrame(entries, schema=schema).write_parquet(out_dir / "list_entries.parquet")
    pl.DataFrame(court, schema={"wallet": pl.String, "role": pl.String}).write_parquet(
        out_dir / "court_labels.parquet"
    )
    by_source: dict[str, int] = {}
    for e in entries:
        by_source[e["source"]] = by_source.get(e["source"], 0) + 1
    summary = {
        "by_source": by_source,
        "nbctf_active": sum(1 for e in entries if e["source"] == "NBCTF" and e["active"]),
        "distinct_list_wallets": len({e["wallet"] for e in entries}),
        "dated": {
            s: sum(1 for e in entries if e["source"] == s and e["listed_on"]) for s in by_source
        },
        "court_wallets": len(court),
        "court_by_role": {r: sum(1 for c in court if c["role"] == r) for r in COURT_ROLES},
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    return summary


def main() -> int:
    print(json.dumps(build(), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
