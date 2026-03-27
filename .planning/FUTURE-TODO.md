# Future planning — deferred work

Cross-cutting items moved here so early phases (04–05, 07, 09–11) can close as **Complete** in GSD while product backlog stays visible.

**Next milestone planning:** See **[`v1.5-CLEANUP-BACKLOG.md`](v1.5-CLEANUP-BACKLOG.md)** for template-hardening, doc drift, and GSD **v1.5** kickoff items (2026-03-26 pass).

---

## From phase retrospectives

- **09 — Tactics & diagnostics:** Additional diagnostic overlays (e.g. cross-asset stress panels) beyond current tactics parquet + weekly section.
- **10 — Tactics install:** CI matrix expansion across more Python/OS combinations; optional install path hardening.
- **11 — Core cleanup:** Deeper repo-wide lint/import policy automation (beyond current conventions).

---

## Product / library backlog (see also `CLAUDE.md`, `ROADMAP.md`)

- **Empirical forward-window table:** Shipped as **`build_forward_window_probabilities()`** in **`src/trading_crab_lib/regime.py`**; step 4 writes **`data/regimes/forward_window_probabilities.parquet`**. Legacy **`compute_forward_probabilities()`** in **`legacy/regime_analysis.py`** is the historical name only.
- **Confusion matrix visualization** — ✓ shipped: **`plot_regime_confusion_matrix()`** in **`plotting.py`**, PNG **`outputs/plots/05_confusion_matrix.png`** (**TMPL-03** / Phase **39**).
- **Additional FRED series**, yield-curve tuning (beyond current **`yc_*`** in **`transforms.py`** where config lists them), **macrotrends** scraper, **LightGBM**, weekly AI narrative report — as prioritized in project **`ROADMAP.md`**.

---

## Template / fork hygiene (v1.5 candidates)

- Optional bulk update of **archived** `.planning/phases/*` files still mentioning `market_regime` (historical; low priority).
- Document **single source of truth** for dependencies (`pyproject.toml` vs `requirements.txt`) for downstream forks.
