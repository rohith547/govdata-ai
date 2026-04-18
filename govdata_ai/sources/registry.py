"""Registry mapping state codes to their source implementations."""
from __future__ import annotations
from typing import Optional
from govdata_ai.sources.base import BaseGovSource

# Registry populated as state modules are added
_STATE_REGISTRY: dict[str, type[BaseGovSource]] = {}


def register(state: str):
    """Decorator to register a source class for a state."""
    def decorator(cls: type[BaseGovSource]):
        _STATE_REGISTRY[state.upper()] = cls
        return cls
    return decorator


def get_source_for_state(state: str) -> Optional[BaseGovSource]:
    """Get an instantiated source for a given state code."""
    # Import all state modules to trigger registration
    from govdata_ai.sources import states  # noqa: F401
    cls = _STATE_REGISTRY.get(state.upper())
    return cls() if cls else None


def list_supported_states() -> list[str]:
    """Return all states with a registered source."""
    from govdata_ai.sources import states  # noqa: F401
    return sorted(_STATE_REGISTRY.keys())
