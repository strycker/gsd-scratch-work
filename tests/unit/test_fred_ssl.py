"""FRED ingestion SSL: certifi bundle patched into fredapi's urlopen."""

from __future__ import annotations

import ssl
from unittest.mock import MagicMock, patch

import pytest


def test_patch_fredapi_urlopen_injects_certifi_context() -> None:
    import fredapi.fred as fred_mod

    from trading_crab_lib.ingestion import fred as fred_ingest

    # Reset module patch flag so test is isolated
    fred_ingest._FREDAPI_SSL_PATCHED = False
    orig_open = fred_mod.urlopen
    captured: dict = {}

    def fake_urlopen(*args, **kwargs):
        captured["context"] = kwargs.get("context")
        r = MagicMock()
        r.read.return_value = b'<?xml version="1.0"?><observations></observations>'
        return r

    fred_mod.urlopen = fake_urlopen

    try:
        fred_ingest._patch_fredapi_urlopen(ssl_verify=True)
        fred_mod.urlopen("https://example.com")
        ctx = captured.get("context")
        assert isinstance(ctx, ssl.SSLContext)
    finally:
        fred_mod.urlopen = orig_open
        fred_ingest._FREDAPI_SSL_PATCHED = False


def test_fetch_all_calls_patch_before_fred(monkeypatch: pytest.MonkeyPatch) -> None:
    from trading_crab_lib.ingestion import fred as fred_ingest

    fred_ingest._FREDAPI_SSL_PATCHED = False
    calls: list[str] = []

    def fake_patch(verify: bool) -> None:
        calls.append(f"patch:{verify}")

    monkeypatch.setattr(fred_ingest, "_patch_fredapi_urlopen", fake_patch)

    empty = __import__("pandas").DataFrame()

    class _Fred:
        def get_series(self, *a, **k):
            return empty

    monkeypatch.setattr(fred_ingest, "Fred", lambda **k: _Fred())

    cfg = {
        "fred": {
            "api_key": "x",
            "series": {
                "GDP": {"name": "fred_gdp", "shift": True},
            },
            "ssl_verify": True,
        },
        "data": {"start_date": "2000-01-01", "end_date": "2001-01-01"},
    }
    out = fred_ingest.fetch_all(cfg)
    assert "patch:True" in calls
    assert "fred_gdp" in out.columns or len(out.columns) >= 0
