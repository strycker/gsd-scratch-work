"""Ingestion subpackage: multpl, FRED, ETF prices, optional Grok labels, macro repair.

Import concrete modules explicitly, e.g. ``from trading_crab_lib.ingestion import fred``
or ``from trading_crab_lib.ingestion.fred import fetch_all``. The parent package
also exposes ``trading_crab_lib.ingestion`` via lazy loading.
"""

# Data sources span: official macro API (FRED), scraped HTML (multpl), market prices (yfinance), optional labels (grok).
