"""Federal government database sources."""
from __future__ import annotations
from govdata_ai.sources.base import BaseGovSource


def get_federal_sources() -> list[BaseGovSource]:
    """Return all registered federal sources."""
    # Sources added as implemented
    return []
