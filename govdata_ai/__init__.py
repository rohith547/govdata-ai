"""
govdata-ai — Open source AI layer for US government databases.

Search $210 billion in unclaimed money across all 50 states.
Zero hallucinations: every result links to an official .gov source.
"""

from govdata_ai.api import UnclaimedMoneySearch
from govdata_ai.matching import NameMatcher
from govdata_ai.models import SearchResult

__version__ = "0.1.0"
__all__ = ["UnclaimedMoneySearch", "NameMatcher", "SearchResult"]
