"""TRON addresses in one format (plan 2.6, L10).

Wallets are stored as base58check text ("T..."). TronGrid events give 20-byte hex,
so every address is converted on load.
"""

from __future__ import annotations

import hashlib
import re

import base58

PREFIX = 0x41
_HEX = re.compile(r"^(0x|41)?[0-9a-fA-F]{40}$")


def hex_to_base58(value: str) -> str:
    """'0x' + 40 hex, '41' + 40 hex, or 40 hex -> 'T...'."""
    h = value.strip()
    if not _HEX.match(h):
        raise ValueError(f"not a 20-byte hex address: {value!r}")
    h = h[-40:].lower()
    return base58.b58encode_check(bytes([PREFIX]) + bytes.fromhex(h)).decode()


def base58_to_hex(address: str) -> str:
    """'T...' -> 40 lowercase hex characters, without a prefix."""
    raw = base58.b58decode_check(address)
    if len(raw) != 21 or raw[0] != PREFIX:
        raise ValueError(f"not a TRON address: {address!r}")
    return raw[1:].hex()


def is_address(value: str) -> bool:
    try:
        base58_to_hex(value)
    except ValueError:
        return False
    return value.startswith("T") and len(value) == 34


def normalize(value: str) -> str | None:
    """Any accepted form ('T...', '0x' + 40 hex, '41' + 40 hex) -> 'T...', or None.

    The Early Detection table writes frozen wallets as 'T...' and normal ones as '0x...'.
    The format alone would give the label away (plan 2.6, L10), so everything is
    converted on load.
    """
    v = (value or "").strip()
    if is_address(v):
        return v
    try:
        return hex_to_base58(v)
    except ValueError:
        return None


def hash_bucket(address: str, buckets: int = 200) -> int:
    """A fixed hash of the address text (plan 2.3): SHA-256, first 4 bytes, modulo buckets.

    In BigQuery: MOD(CAST(CONCAT('0x', TO_HEX(SUBSTR(SHA256(address), 1, 4))) AS INT64), 200).
    """
    digest = hashlib.sha256(address.encode("ascii")).digest()
    return int.from_bytes(digest[:4], "big") % buckets


def in_hash_sample(address: str, rate: float = 0.005) -> bool:
    return hash_bucket(address, round(1 / rate)) == 0
