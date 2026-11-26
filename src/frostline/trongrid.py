"""A small TronGrid client with the quota guard of plan 7.2.

At most one call a second on average, retries with backoff on refusals and
network errors, and the member's own key from .env when there is one.
"""

from __future__ import annotations

import os
import time
from collections.abc import Iterator
from typing import Any

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

BASE_URL = "https://api.trongrid.io"


def _retryable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.TransportError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code == 429 or exc.response.status_code >= 500
    return False


class TronGrid:
    def __init__(self, api_key: str | None = None, min_interval: float = 1.05, timeout: float = 40):
        key = api_key if api_key is not None else os.environ.get("TRONGRID_API_KEY", "")
        headers = {"Accept": "application/json", "User-Agent": "frostline/0.1"}
        if key:
            headers["TRON-PRO-API-KEY"] = key
        self.has_key = bool(key)
        self.min_interval = min_interval
        self.calls = 0
        self._last = 0.0
        self._http = httpx.Client(base_url=BASE_URL, headers=headers, timeout=timeout)

    def _pace(self) -> None:
        wait = self.min_interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    @retry(
        retry=retry_if_exception(_retryable),
        wait=wait_exponential(multiplier=2, min=2, max=60),
        stop=stop_after_attempt(7),
        reraise=True,
    )
    def _request(self, method: str, url: str, **kwargs: Any) -> Any:
        self._pace()
        self.calls += 1
        response = self._http.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def events(
        self, contract: str, event_name: str, min_ts: int = 0, max_ts: int | None = None
    ) -> Iterator[dict]:
        """All confirmed events of one kind, oldest first, following TronGrid's pages."""
        params: dict[str, Any] | None = {
            "event_name": event_name,
            "limit": 200,
            "order_by": "block_timestamp,asc",
            "only_confirmed": "true",
            "min_block_timestamp": min_ts,
        }
        if max_ts is not None:
            params["max_block_timestamp"] = max_ts
        url: str | None = f"/v1/contracts/{contract}/events"
        while url:
            page = self._request("GET", url, params=params)
            yield from page.get("data", [])
            url = ((page.get("meta") or {}).get("links") or {}).get("next")
            params = None

    def transaction(self, txid: str) -> dict:
        return self._request(
            "POST", "/wallet/gettransactionbyid", json={"value": txid, "visible": True}
        )
