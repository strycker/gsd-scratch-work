"""
Real venv + wheel smoke: build a wheel, install into a clean venv, set
TRADING_CRAB_ROOT to a minimal project tree, verify ``load()`` resolves config.

**Not run by default** (slow, ~minutes, network). Opt in with environment
variable ``RUN_WHEEL_SMOKE=1``.

Examples::

    RUN_WHEEL_SMOKE=1 pytest -v tests/integration/test_wheel_smoke.py
    RUN_WHEEL_SMOKE=1 pytest -v -m wheel_smoke
    bash scripts/smoke_wheel_paths.sh

Requires network for ``pip install`` of the wheel (dependency resolution).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

MINIMAL_SETTINGS_YAML = """\
data: {}
fred: {}
"""


def _venv_python(venv: Path) -> Path:
    if sys.platform == "win32":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


@pytest.mark.smoke
@pytest.mark.network
@pytest.mark.wheel_smoke
@pytest.mark.skipif(sys.version_info < (3, 10), reason="project requires Python 3.10+")
@pytest.mark.skipif(
    os.environ.get("RUN_WHEEL_SMOKE") != "1",
    reason="slow venv+wheel smoke; set RUN_WHEEL_SMOKE=1 (see module docstring)",
)
def test_wheel_install_loads_config_with_trading_crab_root(tmp_path: Path) -> None:
    wheel_dir = tmp_path / "wheelhouse"
    wheel_dir.mkdir()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            str(REPO_ROOT),
            "-w",
            str(wheel_dir),
        ],
        check=True,
        cwd=REPO_ROOT,
    )
    main_wheels = sorted(wheel_dir.glob("trading_crab_lib-*.whl"))
    assert len(main_wheels) == 1, f"expected one trading_crab_lib wheel, got {list(wheel_dir.glob('*.whl'))}"

    venv = tmp_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    py = _venv_python(venv)
    subprocess.run(
        [str(py), "-m", "pip", "install", "--upgrade", "pip", str(main_wheels[0])],
        check=True,
    )

    project = tmp_path / "project"
    cfg_dir = project / "config"
    cfg_dir.mkdir(parents=True)
    (cfg_dir / "settings.yaml").write_text(MINIMAL_SETTINGS_YAML, encoding="utf-8")

    env = os.environ.copy()
    env["TRADING_CRAB_ROOT"] = str(project.resolve())
    env.pop("PYTHONPATH", None)

    proc = subprocess.run(
        [
            str(py),
            "-c",
            "import trading_crab_lib as t; "
            "assert t.CONFIG_DIR.name == 'config'; "
            "cfg = t.load(); "
            "assert isinstance(cfg, dict); "
            "assert 'fred' in cfg",
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        pytest.fail(f"subprocess failed:\nstdout={proc.stdout}\nstderr={proc.stderr}")
