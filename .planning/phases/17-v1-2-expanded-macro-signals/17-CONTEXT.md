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

## Resolved decisions (Phase 17 execution)

### Feature wiring table

| Column | `log_columns` | `initial_features` | `clustering_features` | Notes |
|--------|---------------|--------------------|------------------------|-------|
| `fred_vix` | yes → `log_fred_vix` | `log_fred_vix` | `log_fred_vix_d1`, `d2` | VIX level |
| `fred_unrate` | yes → `log_fred_unrate` | `log_fred_unrate` | `log_fred_unrate_d1`, `d2` | UNRATE |
| `fred_m2sl` | yes → `log_fred_m2sl` | `log_fred_m2sl` | `log_fred_m2sl_d1`, `d2` | M2 |
| `fred_m2ns` | yes → `log_fred_m2ns` | `log_fred_m2ns` | `log_fred_m2ns_d1`, `d2` | M2 NSA |
| `fred_gs2` | no (rate %) | `fred_gs2` | `fred_gs2_d1`, `d2` | Same pattern as `fred_gs10` |
| `fred_houst` | yes → `log_fred_houst` | `log_fred_houst` | `log_fred_houst_d1`, `d2` | Housing starts |
| `fred_umcsent` | yes → `log_fred_umcsent` | `log_fred_umcsent` | `log_fred_umcsent_d1`, `d2` | Sentiment |
| `yc_10y_2y` | no (spread, can be ≤0) | `yc_10y_2y` | `yc_10y_2y_d1`, `d2` | `fred_gs10` − `fred_gs2` |
| `yc_10y_3m` | no | `yc_10y_3m` | `yc_10y_3m_d1`, `d2` | `fred_gs10` − `fred_tb3ms` |
| `yc_2y_3m` | no | `yc_2y_3m` | `yc_2y_3m_d1`, `d2` | `fred_gs2` − `fred_tb3ms` |
| `fred_t10y2y` | — | — | — | **Not** in `features.*`; remains ingested under `fred.series` for QA/exports |
| `fred_t10y3m` | — | — | — | **Not** in `features.*`; use `yc_10y_3m` for clustering to avoid double-counting FRED spreads |

**Redundancy rule:** **`yc_*`** derived spreads are the single clustering signal for the 10Y−2Y and 10Y−3M ideas; **FRED `T10Y2Y` / `T10Y3M`** are not duplicated in `initial_features` / `clustering_features`.

### Scope

- **Clustering:** all of the above (except omitted FRED spread duplicates) are in **`clustering_features`** as **d1/d2** (and raw levels only where the series is already a rate, matching existing conventions).
- **Causal vs non-causal:** same columns flow through **`engineer_all(..., causal=False)`** and **`causal=True`**; step 2 still writes both parquet outputs per existing step-2 contract.
