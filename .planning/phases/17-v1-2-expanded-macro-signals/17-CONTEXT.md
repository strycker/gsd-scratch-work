# Phase 17 — Context (v1.2 expanded macro & yield data)

## Requirement

**DATA-10** — Additional FRED series & yield spreads; causal / non-causal feature parity (`features.parquet` vs `features_supervised.parquet` / `features_causal` per existing step-2 behavior).

## Baseline (already in repo)

- **`config/settings.yaml`** — `fred.series` lists GDP…UMCSENT including **VIXCLS, UNRATE, M2SL/M2NS, GS2, T10Y2Y, T10Y3M, HOUST, UMCSENT** with column names `fred_*`.
- **`transforms.add_yield_curve_features`** — builds **`yc_10y_2y`**, **`yc_10y_3m`**, **`yc_2y_3m`** when **fred_gs10**, **fred_gs2**, **fred_tb3ms** exist.
- **`engineer_all`** — runs cross-ratios → **yield features** → log → … → derivatives → clustering selection.

## Gap

New FRED columns and derived spreads are **not** yet in **`features.initial_features`** / **`features.clustering_features`** (and related **`log_columns`**), so they do not influence PCA/clustering or supervised models.

## Constraints (from `CLAUDE.md` / project rules)

- **`n_pca_components: 5`** and **regime label stability**: expanding **`clustering_features`** changes cluster geometry → users must **re-run steps 3–7** and refresh **`config/regime_labels.yaml`** per **`RUNBOOK.md`**.
- **Publication-lag `shift`**: only add `shift: true` where economically justified (GDP/GNP pattern); document each new shift in YAML comments.
- **Do not** silently duplicate highly correlated series (e.g. **fred_t10y2y** vs **yc_10y_2y**) in **`clustering_features`** without an explicit decision in this phase.

## Open decisions (resolve during execution)

1. Which **VIX / UNRATE / M2 / housing / sentiment** columns enter **clustering** vs diagnostics-only?
2. Log-transform rules for bounded or %-style series (mirror existing **fred_gs10** handling patterns).
3. Whether **Phase 17** updates **`clustering_features`** in this PR or lands **ingest + `initial_features` + supervised-only** first — default: **include in `clustering_features`** with RUNBOOK note (DATA-10 asks for regime-relevant macro expansion).
