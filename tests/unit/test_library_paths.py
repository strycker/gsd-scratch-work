"""Tests for trading_crab_lib.paths (PKG-10 workspace resolution)."""

from __future__ import annotations

import pytest

from trading_crab_lib.paths import LibraryPaths, resolve_library_paths


@pytest.fixture(autouse=True)
def clear_trading_crab_env(monkeypatch):
    for key in (
        "TRADING_CRAB_ROOT",
        "TRADING_CRAB_CONFIG",
        "TRADING_CRAB_DATA",
        "TRADING_CRAB_OUTPUT",
    ):
        monkeypatch.delenv(key, raising=False)


def test_trading_crab_root_sets_all_dirs(tmp_path, monkeypatch):
    monkeypatch.setenv("TRADING_CRAB_ROOT", str(tmp_path))
    pkg_file = tmp_path / "any" / "trading_crab_lib" / "paths.py"
    paths = resolve_library_paths(package_file=pkg_file)
    assert paths.root == tmp_path.resolve()
    assert paths.config_dir == tmp_path / "config"
    assert paths.data_dir == tmp_path / "data"
    assert paths.output_dir == tmp_path / "outputs"
    assert isinstance(paths, LibraryPaths)


def test_walk_finds_repo_layout(tmp_path, monkeypatch):
    project = tmp_path / "project"
    (project / "config").mkdir(parents=True)
    (project / "config" / "settings.yaml").write_text("data: {}\n", encoding="utf-8")
    pkg_file = project / "vendor" / "trading_crab_lib" / "paths.py"
    paths = resolve_library_paths(package_file=pkg_file)
    assert paths.root == project.resolve()
    assert paths.config_dir == project / "config"
    assert paths.data_dir == project / "data"
    assert paths.output_dir == project / "outputs"


def test_site_packages_raises_with_message(tmp_path, monkeypatch):
    pkg_file = tmp_path / "lib" / "site-packages" / "trading_crab_lib" / "paths.py"
    pkg_file.parent.mkdir(parents=True)
    with pytest.raises(RuntimeError, match="TRADING_CRAB_ROOT"):
        resolve_library_paths(package_file=pkg_file)


def test_partial_granular_env_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("TRADING_CRAB_CONFIG", str(tmp_path / "c"))
    monkeypatch.setenv("TRADING_CRAB_DATA", str(tmp_path / "d"))
    pkg_file = tmp_path / "x" / "trading_crab_lib" / "paths.py"
    with pytest.raises(RuntimeError, match="TRADING_CRAB_ROOT"):
        resolve_library_paths(package_file=pkg_file)


def test_all_granular_dirs_without_root(tmp_path, monkeypatch):
    cfg = tmp_path / "cfg"
    ddir = tmp_path / "dat"
    odir = tmp_path / "out"
    cfg.mkdir()
    (cfg / "settings.yaml").write_text("x: 1\n", encoding="utf-8")
    ddir.mkdir()
    odir.mkdir()
    monkeypatch.setenv("TRADING_CRAB_CONFIG", str(cfg))
    monkeypatch.setenv("TRADING_CRAB_DATA", str(ddir))
    monkeypatch.setenv("TRADING_CRAB_OUTPUT", str(odir))
    pkg_file = tmp_path / "venv" / "trading_crab_lib" / "paths.py"
    paths = resolve_library_paths(package_file=pkg_file)
    assert paths.config_dir == cfg.resolve()
    assert paths.data_dir == ddir.resolve()
    assert paths.output_dir == odir.resolve()
    assert paths.root == tmp_path.resolve()
