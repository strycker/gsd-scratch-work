"""FRED API ingestion for macro series.

Fetches each series defined in ``cfg["fred"]["series"]``, resamples to quarterly
frequency (period-end), and returns a single wide DataFrame. Series are fetched
in parallel (:class:`~concurrent.futures.ThreadPoolExecutor`) to cut wall-clock
time from ~N×latency to roughly one round-trip latency.

**Publication-lag shift:** GDP and GNP are released after quarter close. Series
marked ``shift: true`` are shifted forward one quarter so values align with when
they would have been known — avoiding look-ahead bias in supervised models.
"""

from __future__ import annotations

import logging
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import certifi
import pandas as pd
from fredapi import Fred

log = logging.getLogger(__name__)

# fredapi.fred binds urllib.request.urlopen at import time without an SSL context.
# macOS Python.org builds often lack system CA certs → CERTIFICATE_VERIFY_FAILED.
# We patch once to inject certifi's CA bundle (or an unverified context if disabled).
_FREDAPI_SSL_PATCHED = False


def _patch_fredapi_urlopen(ssl_verify: bool) -> None:
    global _FREDAPI_SSL_PATCHED
    if _FREDAPI_SSL_PATCHED:
        return
    import fredapi.fred as fred_mod

    _orig = fred_mod.urlopen

    def _urlopen(*args, **kwargs):  # type: ignore[no-untyped-def]
        if kwargs.get("context") is None:
            if ssl_verify:
                kwargs["context"] = ssl.create_default_context(cafile=certifi.where())
            else:
                log.warning(
                    "FRED ssl_verify is false — TLS certificate verification disabled (insecure)"
                )
                kwargs["context"] = ssl._create_unverified_context()
        return _orig(*args, **kwargs)

    fred_mod.urlopen = _urlopen
    _FREDAPI_SSL_PATCHED = True


# FRED is generally tolerant of small parallel bursts; keep a modest cap so
# we don't get rate-limited or trigger any undocumented throttle.
_MAX_WORKERS = 8


def _fetch_one(fred: Fred, series_id: str, start: str, end: str, shift: bool) -> pd.Series:
    """Pull one FRED series, resample to QE, optionally apply publication lag."""
    raw = fred.get_series(series_id, observation_start=start, observation_end=end)
    quarterly = raw.resample("QE").last()
    if shift:
        quarterly = quarterly.shift(1)  # lag one quarter — data known next quarter
    return quarterly


def fetch_all(cfg: dict) -> pd.DataFrame:
    """
    Fetch every series in cfg["fred"]["series"] and join into one DataFrame.

    All series are fetched concurrently (up to _MAX_WORKERS threads) so the
    wall-clock time is roughly one network round-trip instead of N×latency.

    Config shape expected:
        fred:
          series:
            GDP:
              name:  "fred_gdp"
              shift: true
            BAA:
              name:  "fred_baa"
              shift: false

    Returns:
        DataFrame indexed by quarter-end dates, columns = friendly names.
    """
    api_key = cfg["fred"].get("api_key")
    if not api_key:
        raise OSError("FRED_API_KEY is not set")

    ssl_verify = bool(cfg.get("fred", {}).get("ssl_verify", True))
    _patch_fredapi_urlopen(ssl_verify)

    fred = Fred(api_key=api_key)

    start = cfg["data"]["start_date"]
    end = cfg["data"]["end_date"] or str(date.today())

    series_cfg: dict = cfg["fred"]["series"]

    def _fetch_task(series_id: str, meta: dict) -> tuple[str, pd.Series | None]:
        friendly_name = meta["name"]
        shift = meta.get("shift", False)
        lag_note = " (shifted +1Q)" if shift else ""
        log.info("Fetching FRED %-10s → %s%s", series_id, friendly_name, lag_note)
        try:
            s = _fetch_one(fred, series_id, start, end, shift)
            s.name = friendly_name
            return friendly_name, s
        except Exception as exc:
            log.warning("Failed to fetch %s (%s): %s", friendly_name, series_id, exc)
            return friendly_name, None

    frames: dict[str, pd.Series] = {}
    with ThreadPoolExecutor(max_workers=min(_MAX_WORKERS, len(series_cfg))) as pool:
        futures = {pool.submit(_fetch_task, sid, meta): sid for sid, meta in series_cfg.items()}
        for future in as_completed(futures):
            friendly_name, series = future.result()
            if series is not None:
                frames[friendly_name] = series

    df = pd.DataFrame(frames)
    df.index.name = "date"
    log.info("FRED fetch complete: %d quarters, %d series", len(df), len(df.columns))
    return df
