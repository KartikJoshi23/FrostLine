from datetime import UTC, datetime

from frostline.registry.build import (
    Event,
    Proposal,
    build_wallets,
    decode_submit,
    make_batches,
    ms,
    split_of,
)
from frostline.tron import base58_to_hex

W1 = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # any valid address works for the logic
W2 = "TBPxhVAsuzoFnKyXtc1o2UySEydPHgATto"
W3 = "T9yb6vP8o8PQJLNmcCkC9wfk73ULTCy2MB"


def submit_data(selector: str, target: str) -> str:
    """Call data of submitTransaction(destination, 0, selector + address)."""
    inner = selector + base58_to_hex(target).rjust(64, "0")
    words = ["00" * 32, "00" * 32, f"{96:064x}", f"{len(inner) // 2:064x}"]
    return "c6427474" + "".join(words) + inner.ljust(128, "0")


def test_decode_submit_reads_function_and_target():
    assert decode_submit(submit_data("0ecb93c0", W3)) == ("addBlackList", W3)
    assert decode_submit(submit_data("e4997dc5", W3)) == ("removeBlackList", W3)
    assert decode_submit(submit_data("a9059cbb", W3)) == ("a9059cbb", None)
    assert decode_submit("deadbeef") == (None, None)


def test_batches_join_votes_ten_minutes_apart_or_less():
    t0 = ms(2025, 1, 1)
    items = [(t0, "a"), (t0 + 600_000, "b"), (t0 + 1_200_001, "c"), (t0 + 1_300_000, "d")]
    assert [[w for _, w in b] for b in make_batches(items, 600_000)] == [["a", "b"], ["c", "d"]]


def test_split_edges_follow_the_settings():
    assert split_of(ms(2024, 6, 30)) == "description"
    assert split_of(ms(2024, 7, 1)) == "learn"
    assert split_of(ms(2025, 9, 30) + 86_399_999) == "learn"
    assert split_of(ms(2025, 10, 1)) == "tune"
    assert split_of(ms(2026, 1, 1)) == "test"
    assert split_of(ms(2026, 11, 1)) == "held_out"


def test_public_vote_is_the_earliest_vote_executed_or_not():
    t0 = ms(2025, 3, 1)
    day = 86_400_000
    events = [
        Event("freeze", W3, t0 + 10 * day, "tx-freeze", 1, 100, None),
        Event("release", W3, t0 + 20 * day, "tx-release", 1, 200, None),
    ]
    props = {
        7: Proposal(7, t0 + 9 * day, "tx-sub-7", executed=t0 + 10 * day, exec_tx="tx-freeze"),
        3: Proposal(3, t0, "tx-sub-3", function="addBlackList", target=W3),
    }
    rows, batches = build_wallets(events, props, {"tx-freeze": [7]})
    (row,) = rows
    assert row["first_vote_at"] == datetime.fromtimestamp(t0 / 1000, UTC)
    assert row["first_vote_executed"] is False
    assert round(row["earlier_vote_days"]) == 9
    assert row["gap_minutes"] == 10 * 24 * 60
    assert row["first_release_at"] is not None
    assert row["split"] == "learn" and len(batches) == 1


def test_voted_only_wallets_are_kept_but_not_batched():
    t0 = ms(2026, 2, 1)
    props = {5: Proposal(5, t0, "tx-sub-5", function="addBlackList", target=W2)}
    rows, batches = build_wallets([], props, {})
    assert rows[0]["voted_only"] is True
    assert rows[0]["split"] == "voted_only"
    assert batches == []


def test_the_usdt_contract_itself_is_not_a_wallet():
    t0 = ms(2025, 5, 1)
    events = [Event("freeze", W1, t0, "tx", 1, 1, None)]
    rows, _ = build_wallets(events, {}, {})
    assert rows == []
