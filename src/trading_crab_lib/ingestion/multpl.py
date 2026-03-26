"""multpl.com HTML scraper for valuation and macro series.

Fetches all series in ``cfg["multpl"]["datasets"]``, resamples to quarterly
frequency, and returns one wide DataFrame. Each dataset entry is
``[short_name, description, url, value_type]``; ``value_type`` controls parsing
(``num``, ``percent``, ``million``, ``trillion``).

Uses **lxml** CSS selectors (``#datatable``) to match the legacy scraper. A
fixed rate limit applies between requests (see ``RATE_LIMIT_SECONDS``).
"""

from __future__ import annotations

import logging
import time

import numpy as np
import pandas as pd
import requests
from lxml import html as HTMLParser

log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    )
}
RATE_LIMIT_SECONDS = 2.0  # be polite to the server

_SUFFIX_MAP = {
    "percent": "%",
    "million": " million",
    "trillion": " trillion",
}


def _scrape_raw_rows(url: str) -> list[list[str]]:
    """Return raw [date_str, value_str] rows from a multpl.com #datatable."""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    parsed = HTMLParser.fromstring(resp.content.decode("utf-8"))
    rows = parsed.cssselect("#datatable tr")
    return [[td.text.strip() for td in row.cssselect("td")] for row in rows[1:]]


def _parse_series(raw_rows: list, short_name: str, value_type: str) -> pd.Series:
    """
    Convert raw [date_str, value_str] rows into a clean, quarterly pd.Series.

    Handles all value_type suffixes. Percents are divided by 100 so every
    series stored is in natural units (0.05 = 5%, not 5.0).
    """
    df = pd.DataFrame(raw_rows, columns=["date", short_name])
    df["date"] = pd.to_datetime(df["date"], format="%b %d, %Y")

    suffix = _SUFFIX_MAP.get(value_type)
    if suffix:
        df[short_name] = df[short_name].str.replace(suffix, "", regex=False)

    df[short_name] = (
        df[short_name].replace("", np.nan).str.replace(",", "", regex=False).astype(float)
    )

    if value_type == "percent":
        df[short_name] /= 100.0

    return df.dropna().set_index("date")[short_name].resample("QE").last()


def fetch_all(cfg: dict, *, columns: set[str] | None = None) -> pd.DataFrame:
    """
    Scrape datasets from cfg["multpl"]["datasets"].

    Parameters
    ----------
    cfg
        Loaded settings (``multpl.datasets`` list of ``[short_name, …]``).
    columns
        If set, only scrape rows whose **short_name** is in this set (partial
        ingest for ``macro_partial.merge_missing_macro_columns``). If ``None``,
        scrape all configured series (default).

    Returns:
        DataFrame indexed by quarter-end dates, columns = short_names scraped.
    """
    datasets: list = cfg.get("multpl", {}).get("datasets", [])
    if not datasets:
        log.warning("No multpl datasets configured — skipping")
        return pd.DataFrame()

    if columns is not None:
        want = frozenset(columns)
        datasets = [e for e in datasets if e[0] in want]
        if not datasets:
            log.warning(
                "multpl: no datasets match requested columns %s — skipping scrape",
                sorted(want),
            )
            return pd.DataFrame()
        log.info(
            "multpl subset: scraping %d dataset(s) (of %d configured) for %s",
            len(datasets),
            len(cfg.get("multpl", {}).get("datasets", [])),
            sorted(want),
        )

    series_list: list[pd.Series] = []

    for entry in datasets:
        short_name, _desc, url, value_type = entry
        log.info("Scraping %-24s  %s", short_name, url)
        try:
            raw = _scrape_raw_rows(url)
            s = _parse_series(raw, short_name, value_type)
            s.name = short_name
            series_list.append(s)
        except Exception as exc:
            log.warning("Failed to scrape %s: %s", short_name, exc)
        time.sleep(RATE_LIMIT_SECONDS)

    if not series_list:
        return pd.DataFrame()

    df = pd.concat(series_list, axis=1)
    df.index.name = "date"
    log.info("multpl fetch complete: %d quarters, %d series", len(df), len(df.columns))
    return df
