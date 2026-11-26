"""The seed list for the main pull (plan 2.3), and the split table (plan 2.7).

The seed list is fixed and fingerprinted before the pull. The 1-in-200 hash sample is
applied inside the BigQuery query with the same rule as frostline.tron.hash_bucket.

    uv run python -m frostline.seeds
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from frostline.config import FINAL, INTERIM, RAW, settings
from frostline.registry.build import SPLITS, split_of, to_dt
from frostline.registry.expected import AUDIT_CUT
from frostline.tron import in_hash_sample, is_address, normalize

REGISTRY = INTERIM / "registry"
LISTS = INTERIM / "lists"


def split_table(wallets: pl.DataFrame, ofac: set[str], cut: datetime | None = None) -> dict:
    """Plan 2.7 columns per split, with each batch in the split of its first vote."""
    w = wallets.filter(pl.col("split").is_in(SPLITS))
    if cut is not None:
        w = w.filter(pl.col("first_vote_at") < cut)
    out = {}
    for name in SPLITS:
        s = w.filter(pl.col("split") == name)
        rel = s.filter(pl.col("first_release_at").is_not_null())
        des = s.filter(pl.col("first_destroy_at").is_not_null())
        if cut is not None:
            rel = rel.filter(pl.col("first_release_at") < cut)
            des = des.filter(pl.col("first_destroy_at") < cut)
        sizes = s.group_by("batch_id").len()
        out[name] = {
            "wallets": s.height,
            "batches": sizes.height,
            "released": rel.height,
            "destroyed": des.height,
            "ofac": s.filter(pl.col("wallet").is_in(sorted(ofac))).height,
            "largest_batch": int(sizes["len"].max()) if sizes.height else 0,
        }
    return out


def crossing_batches(wallets: pl.DataFrame) -> int:
    """Batches whose wallets' own vote dates span two splits (the rule keeps them whole)."""
    seen: dict[int, set[str]] = {}
    for batch, first_vote in (
        wallets.filter(pl.col("batch_id").is_not_null())
        .select("batch_id", "first_vote_at")
        .iter_rows()
    ):
        seen.setdefault(batch, set()).add(split_of(int(first_vote.timestamp() * 1000)))
    return sum(1 for s in seen.values() if len(s) > 1)


def build(raw: Path = RAW, out_dir: Path = FINAL) -> dict:
    wallets = pl.read_parquet(REGISTRY / "wallets.parquet")
    entries = pl.read_parquet(LISTS / "list_entries.parquet")
    court = pl.read_parquet(LISTS / "court_labels.parquet")
    zen = pl.read_parquet(
        raw / "zenodo_24031003" / "model_data.parquet", columns=["address", "label"]
    )

    registry = set(wallets["wallet"])
    listed = set(entries["wallet"])
    roles = dict(court.iter_rows())
    normals_raw = set(zen.filter(pl.col("label") == 0)["address"])
    normals = {n for n in (normalize(a) for a in normals_raw) if n}
    zen_formats = {
        "base58": sum(is_address(a) for a in zen["address"]),
        "hex": sum(a.startswith("0x") for a in zen["address"]),
    }
    seeds = sorted(registry | listed | set(roles) | normals)
    rate = settings()["rules"]["hash_rate"]
    frame = pl.DataFrame(
        {
            "wallet": seeds,
            "in_registry": [w in registry for w in seeds],
            "on_list": [w in listed for w in seeds],
            "court_role": [roles.get(w) for w in seeds],
            "zenodo_normal": [w in normals for w in seeds],
            "in_hash_sample": [in_hash_sample(w, rate) for w in seeds],
        }
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(out_dir / "seed_wallets.parquet")
    csv_path = out_dir / "seed_wallets.csv"
    csv_path.write_text("wallet\n" + "\n".join(seeds) + "\n", encoding="ascii", newline="\n")
    fingerprint = hashlib.sha256(csv_path.read_bytes()).hexdigest()

    cut = to_dt(AUDIT_CUT)
    frozen_by_cut = set(wallets.filter(pl.col("first_freeze_at") < cut)["wallet"])
    ofac = set(entries.filter(pl.col("source") == "OFAC")["wallet"])
    summary = {
        "built_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "seed_wallets": len(seeds),
        "seed_csv_sha256": fingerprint,
        "from_registry": len(registry),
        "from_lists": len(listed),
        "from_court": len(roles),
        "zenodo_normals": len(normals_raw),
        "zenodo_normals_valid": len(normals),
        "zenodo_address_formats": zen_formats,
        "zenodo_normals_in_registry": len(normals & registry),
        "seeds_in_hash_sample": int(frame["in_hash_sample"].sum()),
        "list_wallets_ever_frozen_at_audit_cut": len(listed & frozen_by_cut),
        "court_wallets_ever_frozen_now": len(
            set(roles) & set(wallets.filter(pl.col("first_freeze_at").is_not_null())["wallet"])
        ),
        "splits_at_audit_cut": split_table(wallets, ofac, cut),
        "splits_now": split_table(wallets, ofac),
        "batches_crossing_a_split_edge": crossing_batches(wallets),
    }
    (out_dir / "seed_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    return summary


def main() -> int:
    print(json.dumps(build(), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
