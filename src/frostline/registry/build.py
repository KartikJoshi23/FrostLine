"""Build the freeze registry from the raw TronGrid events (plan 2.2, 2.7).

A freeze and the multisig execution that caused it share one transaction, so each
freeze is linked to its vote through that transaction. Votes that were never
executed are read from their submitting transaction. S, the public vote, is the
earliest vote to freeze the wallet, executed or not.

    uv run python -m frostline.registry.build
"""

from __future__ import annotations

import json
import statistics as st
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import polars as pl

from frostline.config import INTERIM, settings
from frostline.jsonl import read_jsonl
from frostline.registry.expected import AUDIT_CUT, AUDIT_NUMBERS, AUDIT_SPLITS
from frostline.registry.pull import PROPOSAL_TXS, TRONGRID_RAW
from frostline.tron import hex_to_base58

OUT = INTERIM / "registry"
KIND = {"AddedBlackList": "freeze", "RemovedBlackList": "release", "DestroyedBlackFunds": "destroy"}
SUBMIT_SELECTOR = "c6427474"  # submitTransaction(address,uint256,bytes)
FUNCTIONS = {
    "0ecb93c0": "addBlackList",
    "e4997dc5": "removeBlackList",
    "f3bdc228": "destroyBlackFunds",
}
SPLITS = ("description", "learn", "tune", "test", "held_out")


def ms(y: int, m: int, d: int) -> int:
    return int(datetime(y, m, d, tzinfo=UTC).timestamp() * 1000)


def to_dt(t: int | None) -> datetime | None:
    return None if t is None else datetime.fromtimestamp(t / 1000, UTC)


@dataclass(frozen=True)
class Event:
    kind: str
    wallet: str
    ts: int
    tx: str
    index: int
    block: int
    amount: int | None  # micro-USDT, destroy events only


@dataclass
class Proposal:
    id: int
    submitted: int
    submit_tx: str
    executed: int | None = None
    exec_tx: str | None = None
    function: str | None = None
    target: str | None = None


def load_events(raw_dir: Path = TRONGRID_RAW) -> list[Event]:
    out = []
    for name, kind in KIND.items():
        for e in read_jsonl(raw_dir / f"{name}.jsonl"):
            r = e["result"]
            out.append(
                Event(
                    kind=kind,
                    wallet=hex_to_base58(r.get("_user") or r["_blackListedUser"]),
                    ts=e["block_timestamp"],
                    tx=e["transaction_id"],
                    index=e["event_index"],
                    block=e["block_number"],
                    amount=int(r["_balance"]) if "_balance" in r else None,
                )
            )
    return sorted(out, key=lambda e: (e.ts, e.tx, e.index))


def decode_submit(data: str) -> tuple[str | None, str | None]:
    """Function and target address inside submitTransaction(destination, value, data)."""
    if not data.startswith(SUBMIT_SELECTOR):
        return None, None
    body = data[8:]
    words = [body[i : i + 64] for i in range(0, len(body), 64)]
    if len(words) < 5:
        return None, None
    inner = "".join(words[4:])[: 2 * int(words[3], 16)]
    selector = inner[:8]
    if not selector:
        return None, None
    arg = inner[8:72]
    target = hex_to_base58(arg[-40:]) if selector in FUNCTIONS and len(arg) == 64 else None
    return FUNCTIONS.get(selector, selector), target


def load_proposals(
    raw_dir: Path = TRONGRID_RAW,
) -> tuple[dict[int, Proposal], dict[str, list[int]]]:
    props: dict[int, Proposal] = {}
    for e in read_jsonl(raw_dir / "Submission.jsonl"):
        pid = int(e["result"]["transactionId"])
        if pid not in props or e["block_timestamp"] < props[pid].submitted:
            props[pid] = Proposal(pid, e["block_timestamp"], e["transaction_id"])
    exec_by_tx: dict[str, list[int]] = defaultdict(list)
    for e in read_jsonl(raw_dir / "Execution.jsonl"):
        pid = int(e["result"]["transactionId"])
        exec_by_tx[e["transaction_id"]].append(pid)
        p = props.get(pid)
        if p is not None and (p.executed is None or e["block_timestamp"] < p.executed):
            p.executed, p.exec_tx = e["block_timestamp"], e["transaction_id"]
    calls = {t.get("txID"): t for t in read_jsonl(raw_dir / PROPOSAL_TXS)}
    for p in props.values():
        t = calls.get(p.submit_tx)
        if t:
            data = t["raw_data"]["contract"][0]["parameter"]["value"].get("data", "")
            p.function, p.target = decode_submit(data)
    return props, dict(exec_by_tx)


def make_batches(items: list[tuple[int, str]], gap_ms: int) -> list[list[tuple[int, str]]]:
    """Group (time, wallet) pairs: a new batch starts when the gap is over gap_ms."""
    items = sorted(items)
    batches: list[list[tuple[int, str]]] = []
    for item in items:
        if batches and item[0] - batches[-1][-1][0] <= gap_ms:
            batches[-1].append(item)
        else:
            batches.append([item])
    return batches


def split_of(t: int) -> str:
    s = settings()["splits"]

    def start(d: date) -> int:
        return ms(d.year, d.month, d.day)

    def end(d: date) -> int:
        return start(d + timedelta(days=1))

    if t < start(s["learn"][0]):
        return "description"
    if t < end(s["learn"][1]):
        return "learn"
    if t < end(s["tune"][1]):
        return "tune"
    if t < end(s["test"][1]):
        return "test"
    return "held_out"


def build_wallets(
    events: list[Event], props: dict[int, Proposal], exec_by_tx: dict[str, list[int]]
) -> tuple[list[dict], list[dict]]:
    contract = settings()["contracts"]["usdt"]
    gap_ms = settings()["rules"]["batch_gap_minutes"] * 60_000
    by_kind: dict[str, dict[str, list[Event]]] = defaultdict(lambda: defaultdict(list))
    for e in events:
        if e.wallet != contract:
            by_kind[e.kind][e.wallet].append(e)

    executed_votes: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for e in events:
        if e.kind != "freeze" or e.wallet == contract:
            continue
        ids = exec_by_tx.get(e.tx, [])
        if len(ids) == 1 and ids[0] in props:
            p = props[ids[0]]
            p.function, p.target = p.function or "addBlackList", p.target or e.wallet
            executed_votes[e.wallet].append((p.submitted, p.id))
    open_votes: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for p in props.values():
        if p.executed is None and p.function == "addBlackList" and p.target:
            open_votes[p.target].append((p.submitted, p.id))

    rows = []
    for w in sorted(set(by_kind["freeze"]) | set(open_votes)):
        freezes = by_kind["freeze"].get(w, [])
        releases = by_kind["release"].get(w, [])
        destroys = by_kind["destroy"].get(w, [])
        votes = sorted(executed_votes.get(w, []) + open_votes.get(w, []))
        first_exec = min(executed_votes[w]) if executed_votes.get(w) else None
        s_ms = votes[0][0] if votes else None
        f_ms = min(e.ts for e in freezes) if freezes else None
        earlier = (
            (first_exec[0] - s_ms) / 86_400_000 if first_exec and s_ms < first_exec[0] else None
        )
        rows.append(
            {
                "wallet": w,
                "first_vote_at": to_dt(s_ms),
                "first_vote_id": votes[0][1] if votes else None,
                "first_vote_executed": bool(votes) and props[votes[0][1]].executed is not None,
                "first_executed_vote_at": to_dt(first_exec[0]) if first_exec else None,
                "earlier_vote_days": earlier,
                "first_freeze_at": to_dt(f_ms),
                "freeze_count": len(freezes),
                "gap_minutes": (f_ms - s_ms) / 60_000
                if f_ms is not None and s_ms is not None
                else None,
                "first_release_at": to_dt(min(e.ts for e in releases)) if releases else None,
                "release_count": len(releases),
                "first_destroy_at": to_dt(min(e.ts for e in destroys)) if destroys else None,
                "destroyed_usdt": sum(e.amount or 0 for e in destroys) / 1e6 if destroys else None,
                "voted_only": not freezes,
                "_s": s_ms,
            }
        )

    positives = [
        (r["_s"], r["wallet"]) for r in rows if r["_s"] is not None and not r["voted_only"]
    ]
    batch_rows, info = [], {}
    for i, b in enumerate(make_batches(positives, gap_ms), 1):
        split = split_of(b[0][0])
        batch_rows.append(
            {
                "batch_id": i,
                "first_vote_at": to_dt(b[0][0]),
                "last_vote_at": to_dt(b[-1][0]),
                "size": len(b),
                "split": split,
            }
        )
        for _, w in b:
            info[w] = (i, b[0][0], len(b), split)
    for r in rows:
        s_ms = r.pop("_s")
        if r["wallet"] in info:
            r["batch_id"], first, r["batch_size"], r["split"] = info[r["wallet"]]
            r["batch_first_vote_at"] = to_dt(first)
        else:
            r["batch_id"], r["batch_size"], r["batch_first_vote_at"] = None, None, None
            r["split"] = "voted_only" if r["voted_only"] else ("no_vote" if s_ms is None else None)
    return rows, batch_rows


def audit_numbers(
    events: list[Event],
    props: dict[int, Proposal],
    exec_by_tx: dict[str, list[int]],
    cut: int,
    ofac: set[str] | None = None,
) -> dict:
    """The audited chain numbers of 24 November 2026, recomputed the same way."""
    contract = settings()["contracts"]["usdt"]
    gap_ms = settings()["rules"]["batch_gap_minutes"] * 60_000
    a = [e for e in events if e.kind == "freeze" and e.ts < cut]
    r = [e for e in events if e.kind == "release" and e.ts < cut]
    d = [e for e in events if e.kind == "destroy" and e.ts < cut]
    a2 = [e for e in a if e.wallet != contract]
    year = lambda t: datetime.fromtimestamp(t / 1000, UTC).year  # noqa: E731
    n: dict = {}

    def frozen_at(t: int) -> tuple[int, int]:
        last_f: dict[str, int] = {}
        last_r: dict[str, int] = {}
        for e in a2:
            if e.ts < t:
                last_f[e.wallet] = max(last_f.get(e.wallet, 0), e.ts)
        for e in r:
            if e.ts < t:
                last_r[e.wallet] = max(last_r.get(e.wallet, 0), e.ts)
        return sum(1 for w, t_ in last_f.items() if last_r.get(w, 0) < t_), len(last_f)

    n["freeze_release_destroy_events"] = [len(a), len(r), len(d)]
    n["ever_frozen"] = len({e.wallet for e in a2})
    n["still_frozen_at_cut"] = frozen_at(cut)[0]
    aug = ms(2026, 8, 13)
    n["to_12_aug_2026_events_and_wallets_incl_contract"] = [
        sum(e.ts < aug for e in a),
        len({e.wallet for e in a if e.ts < aug}),
    ]
    n["on_8_nov_2026_still_and_ever"] = list(frozen_at(ms(2026, 11, 9)))
    n["ever_released_wallets"] = len({e.wallet for e in r})
    n["destroyed_wallets"] = len({e.wallet for e in d})
    n["frozen_more_than_once"] = sum(1 for c in Counter(e.wallet for e in a2).values() if c > 1)
    first: dict[str, Event] = {}
    for e in a2:
        first.setdefault(e.wallet, e)
    n["first_freezes_by_year"] = dict(sorted(Counter(year(e.ts) for e in first.values()).items()))
    n["released_14_may_2026"] = sum(ms(2026, 5, 14) <= e.ts < ms(2026, 5, 15) for e in r)

    subs = {p.id: p.submitted for p in props.values() if p.submitted < cut}
    matched, unmatched_years = [], Counter()
    for e in a:
        ids = [i for i in exec_by_tx.get(e.tx, []) if props.get(i) and props[i].executed < cut]
        if len(ids) == 1 and ids[0] in subs:
            matched.append((e.ts, (e.ts - subs[ids[0]]) / 60_000, e.wallet, subs[ids[0]]))
        else:
            unmatched_years[year(e.ts)] += 1
    n["freezes_matched_to_votes"] = len(matched)
    n["unmatched_by_year"] = dict(sorted(unmatched_years.items()))
    n["negative_gaps"] = sum(1 for g in matched if g[1] < 0)

    fb = make_batches([(g[0], str(i)) for i, g in enumerate(matched)], gap_ms)
    gap_of = {str(i): g[1] for i, g in enumerate(matched)}
    meds = [(b[0][0], st.median(gap_of[k] for _, k in b)) for b in fb]
    n["freeze_time_batches"] = len(fb)
    n["batch_median_gap_minutes"] = round(st.median(m for _, m in meds), 1)
    n["batch_median_gap_2024_25"] = round(
        st.median(m for t, m in meds if 2024 <= year(t) <= 2025), 1
    )
    n["batch_median_gap_2026"] = round(st.median(m for t, m in meds if year(t) == 2026), 1)
    n["share_batches_over_1h"] = round(100 * sum(m > 60 for _, m in meds) / len(meds), 1)
    first_batches = make_batches([(e.ts, w) for w, e in first.items()], gap_ms)
    n["wallets_in_freeze_batches_5plus_pct"] = round(
        100 * sum(len(b) for b in first_batches if len(b) >= 5) / len(first), 1
    )
    big = max(first_batches, key=len)
    n["largest_freeze_batch"] = [len(big), to_dt(big[0][0]).date().isoformat()]
    n["freezecheck_window_events"] = sum(ms(2025, 11, 4) <= g[0] < ms(2026, 11, 8) for g in matched)

    fp: dict[str, int] = {}
    for g in sorted(matched, key=lambda g: g[3]):
        if g[2] != contract:
            fp.setdefault(g[2], g[3])
    n["wallets_with_executed_vote"] = len(fp)
    pb = make_batches([(t, w) for w, t in fp.items()], gap_ms)
    n["wallets_in_vote_batches_5plus_pct"] = round(
        100 * sum(len(b) for b in pb if len(b) >= 5) / len(fp), 1
    )
    bid = {w: i for i, b in enumerate(pb) for _, w in b}
    released = {e.wallet for e in r}
    destroyed = {e.wallet for e in d}
    splits = {}
    for name in SPLITS:
        ws = [w for w, t in fp.items() if split_of(t) == name and t < cut]
        sizes = Counter(bid[w] for w in ws)
        splits[name] = {
            "wallets": len(ws),
            "batches": len(sizes),
            "released": sum(w in released for w in ws),
            "destroyed": sum(w in destroyed for w in ws),
            "largest_batch": max(sizes.values()) if sizes else 0,
        }
        if ofac is not None:
            splits[name]["ofac"] = sum(w in ofac for w in ws)
    n["splits_audit_definition"] = splits

    open_ids = [
        p for p in props.values() if p.submitted < cut and (p.executed is None or p.executed >= cut)
    ]
    n["unexecuted_submissions"] = len(open_ids)
    freeze_votes = [p for p in open_ids if p.function == "addBlackList"]
    n["unexecuted_freeze_votes"] = len(freeze_votes)
    ever = {e.wallet for e in a2}
    targets = {p.target for p in freeze_votes}
    n["their_targets_never_frozen"] = len(targets - ever)
    leads = []
    for w, t in fp.items():
        early = [p.submitted for p in freeze_votes if p.target == w and p.submitted < t]
        if early:
            leads.append((t - min(early)) / 86_400_000)
    n["wallets_with_earlier_unexecuted_vote"] = len(leads)
    n["max_earlier_vote_days"] = round(max(leads)) if leads else 0
    return n


def compare(found: dict, expected: dict) -> list[str]:
    """Return the keys whose values differ (dict keys compared as strings)."""
    norm = lambda v: json.loads(json.dumps(v))  # noqa: E731
    return [k for k, v in expected.items() if norm(found.get(k)) != norm(v)]


def build(raw_dir: Path = TRONGRID_RAW, out_dir: Path = OUT) -> dict:
    events = load_events(raw_dir)
    props, exec_by_tx = load_proposals(raw_dir)
    wallets, batches = build_wallets(events, props, exec_by_tx)
    out_dir.mkdir(parents=True, exist_ok=True)
    pl.DataFrame(
        [
            {
                "kind": e.kind,
                "wallet": e.wallet,
                "ts": to_dt(e.ts),
                "tx": e.tx,
                "event_index": e.index,
                "block": e.block,
                "amount_micro": e.amount,
            }
            for e in events
        ],
        infer_schema_length=None,
    ).write_parquet(out_dir / "events.parquet")
    pl.DataFrame(
        [
            {
                "proposal_id": p.id,
                "submitted_at": to_dt(p.submitted),
                "submit_tx": p.submit_tx,
                "executed_at": to_dt(p.executed),
                "exec_tx": p.exec_tx,
                "function": p.function,
                "target": p.target,
            }
            for p in sorted(props.values(), key=lambda p: p.id)
        ],
        infer_schema_length=None,
    ).write_parquet(out_dir / "proposals.parquet")
    pl.DataFrame(wallets, infer_schema_length=None).write_parquet(out_dir / "wallets.parquet")
    pl.DataFrame(batches, infer_schema_length=None).write_parquet(out_dir / "batches.parquet")
    found = audit_numbers(events, props, exec_by_tx, AUDIT_CUT)
    diff = compare(found, AUDIT_NUMBERS)
    if compare(found["splits_audit_definition"], AUDIT_SPLITS):
        diff.append("splits_audit_definition")
    last = max(e.ts for e in events)
    summary = {
        "built_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "events": len(events),
        "last_event_utc": to_dt(last).isoformat(),
        "wallets": len(wallets),
        "audit_cut_utc": to_dt(AUDIT_CUT).isoformat(),
        "audit_numbers": found,
        "audit_differences": diff,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=1, default=str), encoding="utf-8"
    )
    return summary


def main() -> int:
    s = build()
    print(f"events {s['events']}, wallets {s['wallets']}, last event {s['last_event_utc']}")
    if s["audit_differences"]:
        expected = {**AUDIT_NUMBERS, "splits_audit_definition": AUDIT_SPLITS}
        for k in s["audit_differences"]:
            print(f"DIFFERS {k}: found {s['audit_numbers'].get(k)} expected {expected[k]}")
        return 1
    print("all audited numbers reproduced at the 24 November cut-off")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
