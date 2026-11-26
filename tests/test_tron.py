import pytest

from frostline.tron import base58_to_hex, hash_bucket, hex_to_base58, in_hash_sample, is_address

USDT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
USDT_HEX = "a614f803b6fd780986a42c78ec9c7f77e6ded13c"


@pytest.mark.parametrize(
    "form", [USDT_HEX, "0x" + USDT_HEX, "41" + USDT_HEX, "0x" + USDT_HEX.upper()]
)
def test_hex_forms_convert_to_one_address(form):
    assert hex_to_base58(form) == USDT


def test_round_trip():
    assert base58_to_hex(USDT) == USDT_HEX
    assert hex_to_base58(base58_to_hex(USDT)) == USDT


@pytest.mark.parametrize("bad", ["", "0x1234", "T" + "1" * 33, USDT[:-1] + "u", "zz" * 20])
def test_bad_addresses_are_rejected(bad):
    assert not is_address(bad)


def test_hash_sample_is_fixed_and_about_one_in_two_hundred():
    assert hash_bucket(USDT) == hash_bucket(USDT)
    assert 0 <= hash_bucket(USDT) < 200
    sample = [hex_to_base58(f"{i:040x}") for i in range(20000)]
    share = sum(in_hash_sample(a) for a in sample) / len(sample)
    assert 0.003 < share < 0.007
