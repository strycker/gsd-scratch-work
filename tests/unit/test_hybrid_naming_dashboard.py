import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import importlib.util


def _load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"Could not load module {module_name} from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_dashboard_hybrid_naming_merges_overrides_onto_suggestions(tmp_path, monkeypatch):
    """
    Behavioral contract for REGIME-03 hybrid pinning:
    - start from auto-suggested names
    - overlay pinned overrides
    - unpinned IDs must still have names (from suggestions)
    """
    repo_root = Path(__file__).resolve().parents[2]
    dash_path = repo_root / "pipelines" / "07_dashboard.py"
    dash = _load_module_from_path("dashboard_mod_hybrid", dash_path)

    data_dir = tmp_path / "data"
    cfg_dir = tmp_path / "config"
    regimes_dir = data_dir / "regimes"
    regimes_dir.mkdir(parents=True, exist_ok=True)
    cfg_dir.mkdir(parents=True, exist_ok=True)

    suggested = {0: "Auto0", 1: "Auto1", 2: "Auto2", 3: "Auto3", 4: "Auto4"}
    overrides = {1: "Pinned1", 3: "Pinned3"}  # leave others unpinned

    (regimes_dir / "regime_names_suggested.yaml").write_text(
        yaml.safe_dump(suggested),
        encoding="utf-8",
    )
    (cfg_dir / "regime_labels.yaml").write_text(
        yaml.safe_dump(overrides),
        encoding="utf-8",
    )

    monkeypatch.setattr(dash, "DATA_DIR", data_dir)
    monkeypatch.setattr(dash, "CONFIG_DIR", cfg_dir)

    names = dash.load_regime_names()

    assert names[1] == "Pinned1"
    assert names[3] == "Pinned3"
    # Unpinned IDs still have names from suggestions.
    assert names[0] == "Auto0"
    assert names[2] == "Auto2"
    assert names[4] == "Auto4"
