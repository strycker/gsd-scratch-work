"""
trading_crab_lib — market regime classification and prediction.

The package resolves workspace paths (``ROOT``, ``CONFIG_DIR``, ``DATA_DIR``,
``OUTPUT_DIR``), loads YAML config via :func:`load`, and exposes
:class:`~trading_crab_lib.runtime.RunConfig` plus :class:`~trading_crab_lib.checkpoints.CheckpointManager`
for pipeline checkpoints. Submodules (``transforms``, ``clustering``, ``ingestion``,
…) are available through normal imports or lazy attributes on the package object
(see :func:`__getattr__`).
"""

# ---------------------------------------------------------------------------
# Replication note (economist + engineer)
# This package is the single import surface for a quarterly macro→regime→assets
# pipeline. Paths resolve to config/, data/, outputs/ so checkpoints and YAML
# stay on disk like a small "data lake" — no hidden globals. Re-implementing
# elsewhere: keep the same three directories and checkpoint naming, or set
# TRADING_CRAB_* env vars per paths.py.
# ---------------------------------------------------------------------------

from .paths import LibraryPaths, resolve_library_paths  # noqa: E402

_paths = resolve_library_paths()
# Four anchors mirror a typical quant research layout: YAML in config/, parquet in data/, artifacts in outputs/.
ROOT = _paths.root
CONFIG_DIR = _paths.config_dir
DATA_DIR = _paths.data_dir
OUTPUT_DIR = _paths.output_dir

# Convenience re-exports so callers can use:
#   import trading_crab_lib as crab
#   crab.load(), crab.setup_logging(), crab.RunConfig(), ...
from .checkpoints import CheckpointManager  # noqa: E402
from .config import load, load_portfolio, setup_logging  # noqa: E402
from .runtime import RunConfig  # noqa: E402

__all__ = [
    "ROOT",
    "CONFIG_DIR",
    "DATA_DIR",
    "OUTPUT_DIR",
    "LibraryPaths",
    "resolve_library_paths",
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
    # Lazy imports keep `import trading_crab_lib` fast; heavy deps (sklearn, scipy) load only on use.
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
