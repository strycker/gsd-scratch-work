from __future__ import annotations

import importlib.util
import os
import types
from pathlib import Path

import pandas as pd
import pytest

from trading_crab_lib.checkpoints import CheckpointManager
from trading_crab_lib.config import load


def _load_step_module(script_name: str) -> types.ModuleType:
    """
    Load a step script from the top-level `pipelines/` directory as a module.

    This avoids relying on non-standard module names like `pipelines01_ingest`
    while still giving tests a handle to call `main()`.
    """
    root = Path(__file__).parent.parent
    script_path = root / "pipelines" / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load step module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


step01 = _load_step_module("01_ingest.py")
step02 = _load_step_module("02_features.py")


@pytest.fixture
def isolated_pipeline_data(monkeypatch, tmp_path: Path) -> Path:
    """
    Point pipeline + checkpoints at tmp_path so pytest never writes real data/*.

    Without this, pipeline smoke tests overwrite repo ``macro_raw`` / checkpoints
    with tiny synthetic frames and break subsequent ``run_pipeline.py`` runs.
    """
    data_root = tmp_path / "data"
    for sub in ("raw", "processed", "regimes", "checkpoints"):
        (data_root / sub).mkdir(parents=True, exist_ok=True)
    ckpt_dir = data_root / "checkpoints"

    import run_pipeline as rp
    import trading_crab_lib as crab
    import trading_crab_lib.checkpoints as ckpt_mod

    monkeypatch.setattr(crab, "DATA_DIR", data_root)
    monkeypatch.setattr(rp, "DATA_DIR", data_root)
    monkeypatch.setattr(ckpt_mod, "CHECKPOINT_DIR", ckpt_dir)
    return data_root


def _make_synthetic_macro() -> pd.DataFrame:
    dates = pd.date_range("2000-03-31", periods=4, freq="QE")
    return pd.DataFrame(
        {
            "fred_gdp": [1000.0, 1010.0, 1020.0, 1030.0],
            "fred_cpi": [200.0, 201.0, 202.0, 203.0],
        },
        index=dates,
    )


@pytest.fixture
def cfg():
    return load()


@pytest.mark.pipeline_ingest_smoke
@pytest.mark.skipif(
    os.environ.get("RUN_PIPELINE_INGEST_SMOKE") != "1",
    reason=(
        "slow (loads pipelines/01_ingest.py); opt in: "
        "RUN_PIPELINE_INGEST_SMOKE=1 or pytest --pipeline-ingest-smoke"
    ),
)
def test_step01_ingest_writes_macro_raw_without_network(
    monkeypatch, isolated_pipeline_data: Path, cfg
) -> None:
    """
    Smoke test for pipelines/01_ingest.py.

    Network-dependent fetches are patched to return a tiny synthetic DataFrame.
    The step should write macro_raw.parquet under the isolated DATA_DIR/raw.

    **Not run by default** — same pattern as ``RUN_WHEEL_SMOKE``::

        RUN_PIPELINE_INGEST_SMOKE=1 pytest tests/test_pipelines_ingest_features.py::test_step01_ingest_writes_macro_raw_without_network -q
        pytest --pipeline-ingest-smoke tests/test_pipelines_ingest_features.py::test_step01_ingest_writes_macro_raw_without_network -q
        bash scripts/smoke_pipeline_ingest.sh
    """

    from trading_crab_lib.ingestion import fred as fred_module
    from trading_crab_lib.ingestion import multpl as multpl_module

    synthetic = _make_synthetic_macro()

    monkeypatch.setattr(fred_module, "fetch_all", lambda _cfg: synthetic)
    monkeypatch.setattr(
        multpl_module, "fetch_all", lambda _cfg: pd.DataFrame(index=synthetic.index)
    )

    raw_dir = isolated_pipeline_data / "raw"
    out_path = raw_dir / "macro_raw.parquet"
    if out_path.exists():
        out_path.unlink()
    CheckpointManager().clear("macro_raw")

    # Pass an empty argv list so argparse inside pipelines/01_ingest.py does not
    # see pytest's own CLI arguments (which would otherwise cause parsing errors).
    step01.main([])

    assert out_path.exists(), "01_ingest.main() did not write macro_raw.parquet"
    loaded = pd.read_parquet(out_path)
    pd.testing.assert_index_equal(loaded.index, synthetic.index)

    cm = CheckpointManager()
    cm.save(loaded, "macro_raw")


def test_step02_features_writes_feature_artifacts_without_network(
    monkeypatch, isolated_pipeline_data: Path, cfg
) -> None:
    """
    Smoke test for pipelines/02_features.py.

    Reads macro_raw from isolated DATA_DIR/raw and writes processed feature artifacts.
    We patch engineer_all to avoid heavy computation and external dependencies.
    """

    from trading_crab_lib import transforms as transforms_module

    raw_dir = isolated_pipeline_data / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    macro_path = raw_dir / "macro_raw.parquet"
    if not macro_path.exists():
        _make_synthetic_macro().to_parquet(macro_path)

    dummy_features = pd.DataFrame(
        {"feature1": [1.0, 2.0, 3.0, 4.0]},
        index=pd.date_range("2000-03-31", periods=4, freq="QE"),
    )

    def fake_engineer_all(raw, _cfg, causal: bool):
        return dummy_features

    monkeypatch.setattr(transforms_module, "engineer_all", fake_engineer_all)

    processed_dir = isolated_pipeline_data / "processed"
    features_path = processed_dir / "features.parquet"
    features_sup_path = processed_dir / "features_supervised.parquet"
    for p in (features_path, features_sup_path):
        if p.exists():
            p.unlink()

    step02.main()

    assert features_path.exists(), "02_features.main() did not write features.parquet"
    assert features_sup_path.exists(), (
        "02_features.main() did not write features_supervised.parquet"
    )

    features = pd.read_parquet(features_path)
    features_sup = pd.read_parquet(features_sup_path)

    assert not features.empty
    assert not features_sup.empty

    cm = CheckpointManager()
    cm.save(features, "features_noncausal")
    cm.save(features_sup, "features_causal")
