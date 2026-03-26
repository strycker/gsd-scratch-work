"""Per-asset tactical metrics and labels (volatility, trend, correlation, entry bias).

Computes rolling volatility, log-price slopes, correlation to SPY, soft-stop z-scores,
and classifies each asset into ``buy_hold`` / ``swing`` / ``stand_aside`` using
``config/settings.yaml`` ``tactics`` thresholds. Used by the dashboard / reporting
layer, not by regime clustering.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _realized_vol(returns: pd.Series, window: int) -> float:
    """Realised volatility over a rolling window (std of returns)."""
    r = returns.dropna()
    if r.empty:
        return float("nan")
    if len(r) < window:
        return float(r.std(ddof=0))
    return float(r.rolling(window).std(ddof=0).iloc[-1])


def _trend_slope(prices: pd.Series, window: int) -> float:
    """Simple linear regression slope on log-prices over the last `window` points."""
    p = prices.dropna()
    if p.empty:
        return 0.0
    if len(p) < window:
        window = len(p)
    if window < 2:
        return 0.0
    y = np.log(p.iloc[-window:])
    x = np.arange(len(y), dtype=float)
    x = x - x.mean()
    y = y - y.mean()
    denom = (x**2).sum()
    if denom == 0:
        return 0.0
    return float((x * y).sum() / denom)


def _rolling_corr(a: pd.Series, b: pd.Series, window: int) -> float:
    """Rolling correlation over the last `window` points."""
    df = pd.concat([a, b], axis=1).dropna()
    if df.empty:
        return float("nan")
    if len(df) < window:
        return float(df.iloc[:, 0].corr(df.iloc[:, 1]))
    return float(df.iloc[-window:, 0].corr(df.iloc[-window:, 1]))


def _soft_stop_z_score(series: pd.Series, window: int) -> float:
    """Z-score of last close vs rolling mean over trailing `window` bars (VWAP proxy)."""
    s = series.dropna()
    if s.empty:
        return float("nan")
    w = min(int(window), len(s))
    if w < 2:
        return float("nan")
    tail = s.iloc[-w:]
    last = float(tail.iloc[-1])
    mu = float(tail.mean())
    std = float(tail.std(ddof=0))
    if std == 0.0 or np.isnan(std):
        return 0.0
    return (last - mu) / std


def _aggregate_vol(vol_values: list[float], how: str) -> float:
    arr = np.array(vol_values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        return float("nan")
    if how == "max":
        return float(np.max(arr))
    if how == "median":
        return float(np.median(arr))
    if how == "mean":
        return float(np.mean(arr))
    return float(np.max(arr))


def _shortest_slope_column(slope_cols: list[str]) -> str | None:
    """Pick slope_* with smallest numeric suffix (for v1_2 primary trend)."""
    best: str | None = None
    best_w: int | None = None
    for c in slope_cols:
        if not c.startswith("slope_"):
            continue
        try:
            w = int(c.split("_", 1)[1])
        except (IndexError, ValueError):
            continue
        if best_w is None or w < best_w:
            best_w = w
            best = c
    return best


def compute_tactics_metrics(
    prices: pd.DataFrame,
    regimes: pd.Series,
    cfg: dict,
) -> pd.DataFrame:
    """
    Compute per-asset volatility, trend, correlation, and current regime metrics.
    Adds as_of, quarter_end, last_price, soft_stop_z, entry_bias_score (Phase 20).
    """
    tac_cfg = cfg.get("tactics", {})
    vol_windows = tac_cfg.get("vol_windows", [5, 20, 60])
    trend_windows = tac_cfg.get("trend_windows", [5, 20, 60])
    corr_lookback = int(tac_cfg.get("corr_lookback", 60))
    eb = tac_cfg.get("entry_bias") or {}
    short_w = int(eb.get("short_slope_window", 5))
    long_w = int(eb.get("long_slope_window", 20))
    ss = tac_cfg.get("soft_stop_proxy") or {}
    ss_enabled = bool(ss.get("enabled", True))
    ss_window = int(ss.get("window", 20))

    as_of = pd.Timestamp(prices.index.max())
    quarter_end = pd.Timestamp(as_of.to_period("Q").end_time)

    # Latest regime label (balanced_cluster)
    current_regime = int(regimes.dropna().iloc[-1])

    records: list[dict] = []
    for col in prices.columns:
        s = prices[col]
        ret = s.pct_change()
        row: dict = {
            "asset": col,
            "current_regime": current_regime,
            "as_of": as_of,
            "quarter_end": quarter_end,
        }

        for w in vol_windows:
            row[f"vol_{w}"] = _realized_vol(ret, w)

        for w in trend_windows:
            row[f"slope_{w}"] = _trend_slope(s, w)

        spy = prices["SPY"] if "SPY" in prices.columns else s
        row["corr_spy"] = _rolling_corr(s, spy, corr_lookback)

        lp = s.dropna()
        row["last_price"] = float(lp.iloc[-1]) if not lp.empty else float("nan")

        if ss_enabled:
            row["soft_stop_z"] = _soft_stop_z_score(s, ss_window)
        else:
            row["soft_stop_z"] = float("nan")

        s_short = f"slope_{short_w}"
        s_long = f"slope_{long_w}"
        if s_short in row and s_long in row:
            sh = row[s_short]
            lo = row[s_long]
            if np.isnan(sh) or np.isnan(lo):
                row["entry_bias_score"] = float("nan")
            else:
                row["entry_bias_score"] = float(np.tanh(float(sh) - float(lo)))
        else:
            row["entry_bias_score"] = float("nan")

        records.append(row)

    return pd.DataFrame.from_records(records).set_index("asset")


def classify_tactics(metrics: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """
    Classify each asset as buy_hold / swing / stand_aside based on metrics.

    ``classification_version``:
      - ``v1`` — legacy: middle ``vol_*`` column + lexicographically first ``slope_*`` (matches pre–Phase 20).
      - ``v1_2`` — multi-horizon: aggregate ``vol_*`` via ``vol_aggregate`` + shortest-window ``slope_*``.
    """
    tac_cfg = cfg.get("tactics", {})
    version = str(tac_cfg.get("classification_version", "v1")).lower()
    vol_bands = tac_cfg.get("vol_bands", {"low": 0.05, "high": 0.25})
    low = float(vol_bands.get("low", 0.05))
    high = float(vol_bands.get("high", 0.25))
    trend_min = float(tac_cfg.get("trend_min_slope", 0.0))
    vol_how = str(tac_cfg.get("vol_aggregate", "max")).lower()
    min_corr = tac_cfg.get("min_corr_spy")

    df = metrics.copy()
    vol_cols = sorted([c for c in df.columns if c.startswith("vol_")])
    slope_cols = sorted([c for c in df.columns if c.startswith("slope_")])
    if not vol_cols or not slope_cols:
        df["tactics_label"] = "stand_aside"
        return df

    if version == "v1_2":
        slope_col = _shortest_slope_column(slope_cols) or slope_cols[0]
    else:
        mid_idx = len(vol_cols) // 2
        vol_col = vol_cols[mid_idx]
        slope_col = slope_cols[0]

    labels: list[str] = []
    for _, row in df.iterrows():
        if version == "v1_2":
            vol_vals = [float(row[c]) for c in vol_cols]
            vol = _aggregate_vol(vol_vals, vol_how)
        else:
            vol = float(row[vol_col])

        slope = float(row[slope_col])

        if min_corr is not None:
            cs = row.get("corr_spy")
            if cs is not None and not pd.isna(cs) and float(cs) < float(min_corr):
                labels.append("stand_aside")
                continue

        if np.isnan(vol) or np.isnan(slope):
            labels.append("stand_aside")
        elif vol <= low and slope >= trend_min:
            labels.append("buy_hold")
        elif low < vol < high and slope >= trend_min:
            labels.append("swing")
        else:
            labels.append("stand_aside")

    df["tactics_label"] = labels
    return df
