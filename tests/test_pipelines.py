def test_dagster_definitions_load():
    from pipelines.definitions import defs

    names = {a.key.to_user_string() for a in defs.assets}
    assert {
        "trongrid_events",
        "freeze_registry",
        "official_lists",
        "seed_wallets",
        "evidence_graph",
    } <= names
