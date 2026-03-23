# Trading-Crab — Operational runbook

This document is the **canonical place** for repeatable pipeline runs, **`market_code`** discipline, checkpoint hygiene, and **steps 8–9** vs the core **1–7** flow. It aligns with the header of [`run_pipeline.py`](run_pipeline.py); for full CLI tables and project conventions see [`CLAUDE.md`](CLAUDE.md).

**Feature invariant (do not violate):** Step 2 writes **centered** features for clustering (steps 3–4) and **causal** `features_supervised` for supervised learning (step 5 onward). Mixing files or reusing stale checkpoints after editing `clustering_features` causes silent wrong results — see [`ARCHITECTURE.md`](ARCHITECTURE.md) §1 and §10.

---

## Prerequisites

- **Python:** 3.10+ recommended (see `pyproject.toml`).
- **Install:** `pip install -e ".[dev]"` from repo root.
- **FRED:** `cp .env.example .env` and set `FRED_API_KEY` (free key from [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)).
- **Optional:** `pip install k-means-constrained` for balanced cluster sizes; use `python run_pipeline.py --no-constrained` if absent.
- **Dirs:** `data/` and `outputs/` are created by the pipeline; both are gitignored.

---

## Golden path

These copy-paste flows mirror **COMMON WORKFLOWS** in [`run_pipeline.py`](run_pipeline.py).

### First machine / full refresh (Grok seed + save labels)

```bash
python run_pipeline.py --refresh --recompute --plots \
    --market-code grok --save-market-code
```

### First machine / fully data-driven clusters

```bash
python run_pipeline.py --refresh --recompute --plots --save-market-code
```

### Fast rerun (cached raw + features; re-cluster through dashboard)

```bash
python run_pipeline.py --steps 3,4,5,6,7 --plots
```

When using **`market_code`** overlays for steps 4–7, pass **one** consistent strategy (see [market_code and save-market-code](#market_code-and-save-market-code)). If you omit `--market-code`, behavior matches the “no overlay” path described in `run_pipeline.py`.

---

## Partial reruns and when to use them

| Situation | Command (from `run_pipeline.py`) |
|-----------|----------------------------------|
| Re-cluster only; save for downstream | `python run_pipeline.py --steps 3 --save-market-code --plots` |
| Recompute features from cached raw, then downstream | `python run_pipeline.py --recompute --steps 2,3,4,5,6,7 --plots` |
| Downstream using **saved** balanced labels | `python run_pipeline.py --steps 4,5,6,7 --market-code clustered --plots` |

**Single strategy per coherent run**

- After a full **1–5** pass, **`predicted`** labels are auto-saved as checkpoint **`market_code_predicted`** — good for reporting that matches the latest classifiers.
- After **`--save-market-code`**, use **`clustered`** for a stable overlay tied to the last clustering run.
- **`grok`** is a fixed external baseline for comparison — not updated by your pipeline.

**Do not** train or score on one label story and then swap `--market-code` for 6–7 without re-running **4–7** unless you explicitly want a diagnostic mismatch.

---

## market_code and save-market-code

`market_code` is a per-quarter integer regime label **overlay** attached for analysis and some training modes. Sources (paraphrased from **MARKET CODE EXPLAINED** in `run_pipeline.py`):

| Source | Meaning |
|--------|---------|
| `grok` | External LLM-assisted labels; checkpoint `market_code_grok` after first load |
| `clustered` | Last **`balanced_cluster`** saved via `--save-market-code` → `market_code_clustered` |
| `predicted` | Last step **5** output → **`market_code_predicted`** (auto-saved each run) |
| *(omit flag)* | No overlay — fully data-driven clustering |

**Worked examples**

Downstream with new cluster labels:

```bash
python run_pipeline.py --steps 4,5,6,7 --market-code clustered --plots
```

Downstream with Grok overlay:

```bash
python run_pipeline.py --steps 4,5,6,7 --market-code grok --plots
```

Downstream with last predicted labels:

```bash
python run_pipeline.py --steps 4,5,6,7 --market-code predicted --plots
```

**List `market_code_*` checkpoints**

```bash
python -c "
from trading_crab_lib.io.checkpoints import CheckpointManager
cm = CheckpointManager()
mc = [e for e in cm.list() if e['name'].startswith('market_code_')]
for e in mc:
    print(e['name'], '—', e.get('rows', '?'), 'rows')
"
```

---

## Checkpoint hygiene and staleness

| Flag | Effect |
|------|--------|
| `--refresh` | Re-scrape multpl + FRED (slow); step 1–2 use fresh raw where applicable |
| `--recompute` | Rebuild features from **cached** raw — use after editing `config/settings.yaml` feature lists or transforms without re-scraping |
| `--refresh-assets` | Re-fetch ETF prices (step **6**) only |

Checkpoints and manifests live under **`data/checkpoints/`**. The `CheckpointManager` tracks freshness; stale parquets can still be **semantically** wrong if you changed:

- **`clustering_features`** or **`initial_features`** — changes cluster geometry → re-run **2–7** (or at least **3–7**).
- **FRED / macro expansion** — Adding or rewiring **`fred.series`** entries or **`features.*`** lists (including new **`fred_*`** / **`yc_*`** columns) changes the feature matrix the same way as editing **`clustering_features`**: use **`--recompute`** (and **`--refresh`** if you need fresh FRED pulls), then **3–7**, and refresh **`config/regime_labels.yaml`** when cluster IDs shift.
- **`config/regime_labels.yaml`** after clusters move — align pinned IDs with `balanced_k` and re-run **4–7**.

Changing `market_code` source **without** re-running dependent steps produces **semantic desync** between classifiers (MODEL-*) and return tables (PORT-*).

### Step 5 — model artifacts (`outputs/models/` + reports)

After supervised training (**step 5**), expect at least:

| File | Role |
|------|------|
| `current_regime.pkl` | **RandomForest** — primary regime probabilities / production path |
| `decision_tree.pkl` | Shallow **DecisionTree** (interpretability) |
| `current_regime_gb.pkl` | **GradientBoostingClassifier** when `prediction.use_boosted: true` (hyperparameters from `boosted_*` in `settings.yaml`) |
| `forward_classifiers.pkl` | Per-horizon DT/RF/(GB) models |
| `behavior_models.pkl` | Per-asset behavior classifiers |

Text interpretability exports under **`outputs/reports/`**:

- `current_regime_tree.txt` — shallow tree on top‑K features from **RF** importances  
- `current_regime_tree_gb.txt` — same pattern from **GB** when `interpret_tree_on_boosted: true`  

Structured CV metrics: **`outputs/reports/model_metrics/`** (includes `gb` rows when boosted training runs).

---

## After re-clustering (regime_labels checklist)

1. Run step **3** (and **`--save-market-code`** if you need `market_code clustered`).
2. Confirm **`clustering.balanced_k`** in `config/settings.yaml` matches expected regime count (e.g. **5** → IDs **0–4**).
3. Update **`config/regime_labels.yaml`** so every active cluster ID is pinned (see `REGIME-03` / Phase 15).
4. Re-run **4 → 7** (and **8–9** if you rely on those artifacts).

---

## Extended pipeline: steps 8 and 9

Core **end-to-end “weekly product”** path is usually steps **1–7** (ingest → dashboard). **Steps 8 and 9** add artifacts some report sections and diagnostics consume:

| Step | Name | Main outputs |
|------|------|----------------|
| **8** | diagnostics | `outputs/reports/diagnostics/ratios_current.parquet`, `rrg_current.parquet` (config in `diagnostics.*`); optional PNGs `outputs/plots/08_diagnostics_*.png` with **`--plots`** |
| **9** | tactics | `outputs/reports/tactics_signals.parquet` — per-asset `tactics_label`, vol/trend/corr metrics, **`as_of`**, **`quarter_end`**, **`last_price`**, **`entry_bias_score`**, **`soft_stop_z`** (Phase 20); **`tactics.classification_version`** (`v1` \| `v1_2`), **`vol_aggregate`**, **`weekly_report_enrich`** in `settings.yaml` |

**Step 8 prerequisite:** ETF **prices** must exist (`data/raw/asset_prices.parquet` from step **6** or a prior run). Ratio **trigger** rules and `rrg_lookback` live under **`config/settings.yaml` → `diagnostics`**.

The weekly markdown report **may** include a **Tactics** block when `tactics_signals.parquet` exists, and a **Diagnostics** block when `diagnostics.weekly_report_include` is true and the diagnostics parquets exist (typically after step **8**). Re-run step **7** after step **8** if you need `weekly_report.md` to pick up the new section.

For a full extended run:

```bash
python run_pipeline.py --steps 1,2,3,4,5,6,7,8,9 --plots
```

If **1–7** are already fresh but you need prices + diagnostics:

```bash
python run_pipeline.py --steps 6,8,7 --plots
```

If **1–7** are already fresh:

```bash
python run_pipeline.py --steps 8,9 --plots
```

---

## Environment-only: email and setup (REPORT-03 / INSTALL-10)

- **File-based outputs** (`outputs/reports/*.csv`, `*.md`, parquets) do **not** require SMTP or secrets.
- **Email delivery** (REPORT-03) needs local credentials — do not commit them; use `.env` / installer docs.
- See **[`scripts/README.md`](scripts/README.md)** for setup scripts, env checks, and smoke workflows referenced by INSTALL-10.

---

## v1.0 milestone audit — integration index

Maps **`.planning/v1.0-MILESTONE-AUDIT.md`** integration / ops bullets to this file (for `$gsd-audit-milestone` traceability).

| Audit source | RUNBOOK section |
|--------------|-----------------|
| `gaps.integration`: regime label semantic drift (`--market-code`, partial reruns, stale checkpoints vs classifiers / returns) | [market_code and save-market-code](#market_code-and-save-market-code); [Partial reruns and when to use them](#partial-reruns-and-when-to-use-them); [Checkpoint hygiene and staleness](#checkpoint-hygiene-and-staleness) |
| `gaps.integration`: missing single golden-path + post–re-cluster YAML checklist | [Golden path](#golden-path); [After re-clustering (regime_labels checklist)](#after-re-clustering-regime_labels-checklist) |
| `gaps.integration`: core docs 1–7 vs DIAG/TACTICS / report dependence on steps **8–9** | [Extended pipeline: steps 8 and 9](#extended-pipeline-steps-8-and-9) |
| `tech_debt.operational`: config/checkpoint freshness when feature lists or `regime_labels.yaml` change | [Checkpoint hygiene and staleness](#checkpoint-hygiene-and-staleness); [After re-clustering (regime_labels checklist)](#after-re-clustering-regime_labels-checklist) |
| `tech_debt.operational`: REPORT-03 / INSTALL-10 environment-dependent (SMTP, secrets) | [Environment-only: email and setup (REPORT-03 / INSTALL-10)](#environment-only-email-and-setup-report-03--install-10) |

---

*Last updated with Phase 20 (TACTICS-10 — multi-horizon tactics v1_2, entry bias, soft-stop proxy, weekly report enrich).*

**Quick test (tactics only):** `PYTHONPATH=src python -m pytest tests/test_tactics.py -q`
