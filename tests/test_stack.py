"""P0 checks that the pinned tools still do what the plan relies on (plan 8.3).

New major versions (DuckDB 2, Polars 2) are tested here with our own needs.
"""

import hashlib

import duckdb
import numpy as np
import polars as pl
import pytest


def test_duckdb_asof_join_uses_only_what_was_known_at_t():
    con = duckdb.connect()
    con.execute("create table facts(wallet varchar, known_from timestamp, balance double)")
    con.execute(
        "insert into facts values ('w', '2026-01-01', 1), ('w', '2026-01-05', 5), "
        "('w', '2026-01-09', 9)"
    )
    con.execute("create table moments(wallet varchar, t timestamp)")
    con.execute(
        "insert into moments values ('w', '2025-12-31'), ('w', '2026-01-01'), ('w', '2026-01-06')"
    )
    rows = con.execute(
        "select m.t::date::varchar, f.balance from moments m asof left join facts f "
        "on m.wallet = f.wallet and f.known_from <= m.t order by m.t"
    ).fetchall()
    assert rows == [("2025-12-31", None), ("2026-01-01", 1.0), ("2026-01-06", 5.0)]


def test_pandera_checks_polars_frames():
    import pandera.polars as pa
    from pandera.errors import SchemaError

    schema = pa.DataFrameSchema(
        {"wallet": pa.Column(str), "amount": pa.Column(float, pa.Check.ge(0))}
    )
    schema.validate(pl.DataFrame({"wallet": ["T1"], "amount": [1.5]}))
    with pytest.raises(SchemaError):
        schema.validate(pl.DataFrame({"wallet": ["T1"], "amount": [-1.0]}))


def test_lightgbm_gives_feature_contributions():
    import lightgbm as lgb

    x = np.random.default_rng(0).normal(size=(300, 3))
    y = (x[:, 0] > 0).astype(int)
    model = lgb.LGBMClassifier(n_estimators=20, verbose=-1).fit(x, y)
    assert model.predict_proba(x).shape == (300, 2)
    assert model.predict(x, pred_contrib=True).shape == (300, 4)


def test_dagster_blocking_check_stops_the_line():
    import dagster as dg

    @dg.asset
    def raw() -> int:
        return -1

    @dg.asset_check(asset=raw, blocking=True)
    def raw_is_positive(raw: int) -> dg.AssetCheckResult:
        return dg.AssetCheckResult(passed=raw > 0)

    @dg.asset
    def features(raw: int) -> int:
        return raw * 2

    result = dg.materialize([raw, raw_is_positive, features], raise_on_error=False)
    assert not result.success
    assert result.asset_materializations_for_node("features") == []


def test_opentimestamps_library_works_here():
    """The `ots` command fails on Windows: python-bitcoinlib 0.12.2 looks for an old OpenSSL
    library. The library's own calendar client works, so we stamp through it (plan 8.1)."""
    from opentimestamps.calendar import RemoteCalendar
    from opentimestamps.core.timestamp import Timestamp

    digest = hashlib.sha256(b"frostline").digest()
    assert Timestamp(digest).msg == digest
    assert callable(RemoteCalendar("https://a.pool.opentimestamps.org").submit)
