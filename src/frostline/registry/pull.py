"""Pull the freeze and vote events from TronGrid (plan 2.1, 2.2).

Raw files are append-only JSON lines in data/raw/trongrid/, one event per line,
exactly as TronGrid returned it. Running again adds only new events.

    uv run python -m frostline.registry.pull
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from frostline.config import RAW, load_env, settings
from frostline.jsonl import append_jsonl, read_jsonl
from frostline.trongrid import TronGrid

TRONGRID_RAW = RAW / "trongrid"
EVENTS = {
    "AddedBlackList": "usdt",
    "RemovedBlackList": "usdt",
    "DestroyedBlackFunds": "usdt",
    "Submission": "tether_multisig",
    "Execution": "tether_multisig",
}
PROPOSAL_TXS = "proposal-transactions.jsonl"


def pull_events(client: TronGrid, raw_dir: Path = TRONGRID_RAW) -> dict[str, int]:
    """Append every event not seen before. Returns the number added per event."""
    contracts = settings()["contracts"]
    added = {}
    for event, contract_key in EVENTS.items():
        path = raw_dir / f"{event}.jsonl"
        old = read_jsonl(path)
        seen = {(e["transaction_id"], e["event_index"]) for e in old}
        start = max((e["block_timestamp"] for e in old), default=0)
        new = []
        for e in client.events(contracts[contract_key], event, min_ts=start):
            key = (e["transaction_id"], e["event_index"])
            if key not in seen:
                seen.add(key)
                new.append(e)
        added[event] = append_jsonl(path, new)
        print(f"{event}: {len(old)} before, {added[event]} added", flush=True)
    return added


def unexecuted_submission_txs(raw_dir: Path = TRONGRID_RAW) -> list[str]:
    executed = {e["result"]["transactionId"] for e in read_jsonl(raw_dir / "Execution.jsonl")}
    subs = read_jsonl(raw_dir / "Submission.jsonl")
    return sorted(
        {e["transaction_id"] for e in subs if e["result"]["transactionId"] not in executed}
    )


def pull_unexecuted_proposals(client: TronGrid, raw_dir: Path = TRONGRID_RAW) -> int:
    """Fetch the submitting transaction of each never-executed vote, to read its target."""
    path = raw_dir / PROPOSAL_TXS
    have = {t.get("txID") for t in read_jsonl(path)}
    todo = [tx for tx in unexecuted_submission_txs(raw_dir) if tx not in have]
    rows = []
    for i, tx in enumerate(todo, 1):
        rows.append(client.transaction(tx))
        if i % 25 == 0:
            print(f"  proposal transactions: {i}/{len(todo)}", flush=True)
    n = append_jsonl(path, rows)
    print(f"proposal transactions: {len(have)} before, {n} added", flush=True)
    return n


def main() -> int:
    load_env()
    client = TronGrid()
    started = datetime.now(UTC)
    added = pull_events(client)
    added["proposal_transactions"] = pull_unexecuted_proposals(client)
    append_jsonl(
        TRONGRID_RAW / "pulls.jsonl",
        [
            {
                "started_utc": started.isoformat(timespec="seconds"),
                "finished_utc": datetime.now(UTC).isoformat(timespec="seconds"),
                "calls": client.calls,
                "with_key": client.has_key,
                "added": added,
            }
        ],
    )
    print(f"done: {client.calls} calls, key used: {client.has_key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
