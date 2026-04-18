"""
State-specific unclaimed property data sources.

Each module registers its source with @register("STATE_CODE").
Import all here so they get auto-registered when the package loads.
"""
from govdata_ai.sources.states import ri, ca_sonoma, mn_ramsey, tx_austin, ca_roseville, ca_marin  # noqa: F401

# Legacy
from govdata_ai.sources.states import ca  # noqa: F401
