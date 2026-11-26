from datetime import date

import base58
import pytest

from frostline.config import settings


def test_splits_follow_each_other_without_overlap():
    s = settings()["splits"]
    learn, tune, test = s["learn"], s["tune"], s["test"]
    assert s["data_start"] < learn[0] <= learn[1] < tune[0] <= tune[1] < test[0] <= test[1]
    assert test[1] < s["held_out_from"]


def test_moment_nearest_the_vote_has_full_history():
    s = settings()
    gap = (s["splits"]["learn"][0] - s["splits"]["data_start"]).days
    assert gap >= max(s["moments"]["windows_days"])


def test_moments_and_windows():
    m = settings()["moments"]
    assert m["days"] == sorted(m["days"])
    assert 7 in m["days"]
    assert max(m["windows_days"]) == 180


def test_warning_rules_are_consistent():
    w = settings()["warnings"]
    assert 0 < w["early_days"] < w["right_days"]
    assert w["relist_after_days"] == w["right_days"]
    assert w["yield_line"] == pytest.approx(1 / 25)


def test_trial_dates_fit_the_final_presentation():
    t = settings()["trial"]
    assert t["cadence"] == "daily"
    assert t["lock_target"] <= t["lock_latest"] < t["final_presentation"] == date(2026, 12, 15)
    per_day = settings()["warnings"]["per_month"] / 30.4
    assert t["screen_max_per_day"] > 50 * per_day


@pytest.mark.parametrize("name", ["usdt", "tether_multisig"])
def test_contract_addresses_are_valid_tron_addresses(name):
    raw = base58.b58decode_check(settings()["contracts"][name])
    assert len(raw) == 21
    assert raw[0] == 0x41
