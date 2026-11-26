"""OFAC listing dates from the public mirror's history (plan 2.1, 5.2).

The OFAC list file has no dates. The mirror (github.com/0xB10C/ofac-sanctioned-digital-
currency-addresses) commits each change, so the first commit that contains an address
dates its listing to about a day. Addresses already present in the first commit we can
read are left undated, because they were listed before the history starts.

    uv run python -m frostline.ofac_history
"""

from __future__ import annotations

import time

import httpx

from frostline.config import RAW
from frostline.jsonl import append_jsonl, read_jsonl
from frostline.lists import find_addresses

REPO = "0xB10C/ofac-sanctioned-digital-currency-addresses"
FILES = ("sanctioned_addresses_TRX.txt", "sanctioned_addresses_USDT.txt")
HISTORY = RAW / "ofac_mirror" / "history.jsonl"


def list_commits(http: httpx.Client, path: str) -> list[dict]:
    commits, page = [], 1
    while True:
        r = http.get(
            f"https://api.github.com/repos/{REPO}/commits",
            params={"sha": "lists", "path": path, "per_page": 100, "page": page},
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            return commits
        commits += [{"sha": c["sha"], "date": c["commit"]["committer"]["date"]} for c in batch]
        page += 1
        time.sleep(1)


def pull() -> int:
    have = {(h["file"], h["sha"]) for h in read_jsonl(HISTORY)}
    rows = []
    with httpx.Client(timeout=40, headers={"User-Agent": "frostline/0.1"}) as http:
        for path in FILES:
            for c in sorted(list_commits(http, path), key=lambda c: c["date"]):
                if (path, c["sha"]) in have:
                    continue
                raw = http.get(f"https://raw.githubusercontent.com/{REPO}/{c['sha']}/{path}")
                raw.raise_for_status()
                rows.append({"file": path, **c, "addresses": sorted(find_addresses(raw.text))})
                time.sleep(0.3)
    return append_jsonl(HISTORY, rows)


def first_seen() -> tuple[dict[str, str | None], dict[str, str]]:
    """Address -> first commit date (ISO), or None if it was already there when a file's
    history starts (listed on or before that start). Also returns each file's start."""
    earliest: dict[str, tuple[str, bool]] = {}
    starts: dict[str, str] = {}
    for path in FILES:
        snaps = sorted(
            (h for h in read_jsonl(HISTORY) if h["file"] == path), key=lambda h: h["date"]
        )
        if not snaps:
            continue
        starts[path] = snaps[0]["date"]
        records = [(snaps[0]["date"], a, True) for a in snaps[0]["addresses"]]
        prev = set(snaps[0]["addresses"])
        for snap in snaps[1:]:
            now = set(snap["addresses"])
            records += [(snap["date"], a, False) for a in now - prev]
            prev = now
        for date, a, at_start in records:
            if a not in earliest or date < earliest[a][0]:
                earliest[a] = (date, at_start)
    return {a: (None if at_start else d) for a, (d, at_start) in earliest.items()}, starts


def main() -> int:
    added = pull()
    first, starts = first_seen()
    dated = sum(1 for d in first.values() if d)
    print(
        f"snapshots added: {added}; starts: {starts}; dated: {dated}; undated: {len(first) - dated}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
