# Notebooks (exploration)

These notebooks **read artifacts** produced by the pipeline (`data/`, `outputs/`) and call helpers in `trading_crab_lib.plotting`. They do not replace `run_pipeline.py` or `pipelines/*.py`.

## Before you run

1. Install the package so imports resolve:

   ```bash
   pip install -e ".[dev]"
   ```

2. Run the relevant pipeline steps first (each notebook’s title markdown lists prerequisites). Example:

   ```bash
   python run_pipeline.py --steps 1,2,3 --plots
   ```

## Imports

Use the installable package name **`trading_crab_lib`** (not legacy aliases). Example:

```python
import trading_crab_lib as crab
from trading_crab_lib.config import load, setup_logging
from trading_crab_lib.runtime import RunConfig
```

If you fork this repo and rename the package, update these imports consistently.
