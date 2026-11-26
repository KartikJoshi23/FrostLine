from datetime import UTC, date, datetime

import polars as pl

from frostline.kg import EDGE_SCHEMA, facts_as_of
from frostline.lists import find_addresses, parse_date

W = "T9yb6vP8o8PQJLNmcCkC9wfk73ULTCy2MB"


def test_cyrillic_look_alikes_are_mapped_before_checking():
    cyr = W.replace("T", "Т", 1)  # Cyrillic capital Te
    assert find_addresses(f"wallet: {cyr};") == {W}
    assert find_addresses(f"{W[:-1]}X") == set()
    assert find_addresses(None) == set()


def test_dates_in_list_formats():
    assert parse_date("07/03/2022") == date(2022, 3, 7)
    assert parse_date("2025-09-01") == date(2025, 9, 1)
    assert parse_date("") is None


def test_as_of_filter_hides_future_and_undated_facts():
    t = datetime(2026, 1, 10, tzinfo=UTC)
    edges = pl.DataFrame(
        [
            {
                "src": "vote:1",
                "dst": "wallet:W",
                "relation": "vote_to_freeze",
                "known_from": datetime(2026, 1, 9, tzinfo=UTC),
                "source": "s",
            },
            {
                "src": "issuer:tether",
                "dst": "wallet:W",
                "relation": "froze",
                "known_from": datetime(2026, 1, 11, tzinfo=UTC),
                "source": "s",
            },
            {
                "src": "wallet:W",
                "dst": "court:fraud platform",
                "relation": "labelled_as",
                "known_from": None,
                "source": "s",
            },
            {
                "src": "wallet:V",
                "dst": "list:OFAC",
                "relation": "listed_on",
                "known_from": datetime(2025, 1, 1, tzinfo=UTC),
                "source": "s",
            },
        ],
        schema=EDGE_SCHEMA,
    )
    facts = facts_as_of(edges, "wallet:W", t)
    assert facts["relation"].to_list() == ["vote_to_freeze"]
