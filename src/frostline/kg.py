"""Base tables of the evidence graph (plan 3.7): dated facts in two tables.

Every fact carries known_from, the first moment it was public, and its source.
Facts without a date are kept for description only and never pass the as-of filter.

    uv run python -m frostline.kg
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, time

import polars as pl

from frostline.config import INTERIM

REGISTRY = INTERIM / "registry"
LISTS = INTERIM / "lists"
OUT = INTERIM / "kg"
EDGE_SCHEMA = {
    "src": pl.String,
    "dst": pl.String,
    "relation": pl.String,
    "known_from": pl.Datetime("us", "UTC"),
    "source": pl.String,
}


def facts_as_of(edges: pl.DataFrame, node: str, t: datetime) -> pl.DataFrame:
    """The one as-of filter (plan 3.7): facts about a node that were public at time t."""
    return edges.filter(
        ((pl.col("src") == node) | (pl.col("dst") == node))
        & pl.col("known_from").is_not_null()
        & (pl.col("known_from") <= t)
    )


def build() -> dict:
    wallets = pl.read_parquet(REGISTRY / "wallets.parquet")
    events = pl.read_parquet(REGISTRY / "events.parquet")
    props = pl.read_parquet(REGISTRY / "proposals.parquet")
    entries = pl.read_parquet(LISTS / "list_entries.parquet")
    court = pl.read_parquet(LISTS / "court_labels.parquet")
    run = datetime.now(UTC).isoformat(timespec="seconds")

    edges: list[dict] = []
    for pid, submitted, tx, function, target in props.select(
        "proposal_id", "submitted_at", "submit_tx", "function", "target"
    ).iter_rows():
        if function == "addBlackList" and target:
            edges.append(
                {
                    "src": f"vote:{pid}",
                    "dst": f"wallet:{target}",
                    "relation": "vote_to_freeze",
                    "known_from": submitted,
                    "source": f"TronGrid Submission {tx}",
                }
            )
    relation = {"freeze": "froze", "release": "released", "destroy": "destroyed_funds"}
    for kind, wallet, ts, tx in events.select("kind", "wallet", "ts", "tx").iter_rows():
        edges.append(
            {
                "src": "issuer:tether",
                "dst": f"wallet:{wallet}",
                "relation": relation[kind],
                "known_from": ts,
                "source": f"TronGrid {kind} {tx}",
            }
        )
    for wallet, batch, first_vote in (
        wallets.filter(pl.col("batch_id").is_not_null())
        .select("wallet", "batch_id", "first_vote_at")
        .iter_rows()
    ):
        edges.append(
            {
                "src": f"wallet:{wallet}",
                "dst": f"batch:{batch}",
                "relation": "in_batch",
                "known_from": first_vote,
                "source": "registry batch rule (plan 2.2)",
            }
        )
    for wallet, source, listed_on in entries.select("wallet", "source", "listed_on").iter_rows():
        edges.append(
            {
                "src": f"wallet:{wallet}",
                "dst": f"list:{source}",
                "relation": "listed_on",
                "known_from": datetime.combine(listed_on, time(), UTC) if listed_on else None,
                "source": f"{source} list file in data/raw",
            }
        )
    for wallet, role in court.iter_rows():
        edges.append(
            {
                "src": f"wallet:{wallet}",
                "dst": f"court:{role}",
                "relation": "labelled_as",
                "known_from": None,
                "source": "Taiwan court labels (Mendeley 62dmsngtfb v3)",
            }
        )
    frame = pl.DataFrame(edges, schema=EDGE_SCHEMA).with_columns(pl.lit(run).alias("run_id"))
    nodes = (
        pl.concat(
            [frame.select(pl.col("src").alias("node")), frame.select(pl.col("dst").alias("node"))]
        )
        .unique()
        .with_columns(pl.col("node").str.split(":").list.first().alias("kind"))
        .sort("node")
    )
    OUT.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(OUT / "edges.parquet")
    nodes.write_parquet(OUT / "nodes.parquet")
    summary = {
        "run_id": run,
        "nodes": nodes.height,
        "edges": frame.height,
        "edges_by_relation": dict(frame.group_by("relation").len().sort("relation").iter_rows()),
        "undated_edges": frame.filter(pl.col("known_from").is_null()).height,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    return summary


def main() -> int:
    print(json.dumps(build(), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
