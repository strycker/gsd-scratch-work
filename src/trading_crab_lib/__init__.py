"""
trading_crab_lib — Market Regime Classification & Prediction Pipeline
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent.parent   # repo root
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

# Convenience re-exports so callers can use:
#   import trading_crab_lib as crab
#   crab.load(), crab.setup_logging(), crab.RunConfig(), ...
from .config import load, load_portfolio, setup_logging  # noqa: E402
from .runtime import RunConfig  # noqa: E402
from .checkpoints import CheckpointManager  # noqa: E402

__all__ = [
    "ROOT",
    "CONFIG_DIR",
    "DATA_DIR",
    "OUTPUT_DIR",
    "load",
    "load_portfolio",
    "setup_logging",
    "RunConfig",
    "CheckpointManager",
]


def __getattr__(name: str):
    """
    Lazy access to submodules so callers can do:
      import trading_crab_lib as crab
      crab.transforms.engineer_all(...)
    """
    import importlib

    submodules = {
        "asset_returns",
        "cluster_comparison",
        "clustering",
        "checkpoints",
        "config",
        "density",
        "diagnostics",
        "email",
        "gmm",
        "ingestion",
        "plotting",
        "prediction",
        "regime",
        "reporting",
        "spectral",
        "tactics",
        "transforms",
        "runtime",
    }
    if name in submodules:
        return importlib.import_module(f"{__name__}.{name}")
    raise AttributeError(name)
