"""California State Controller — Unclaimed Property Division"""
from __future__ import annotations
import re
from typing import Optional
from govdata_ai.models import SearchResult
from govdata_ai.sources.base import BaseGovSource
from govdata_ai.sources.registry import register


@register("CA")
class CaliforniaSource(BaseGovSource):
    """
    California State Controller's Office — Unclaimed Property.
    Largest unclaimed property database in the US ($15 billion+).
    Official: https://ucpweb.sco.ca.gov
    """

    name = "California State Controller's Office"
    state = "CA"
    base_url = "https://ucpweb.sco.ca.gov"
    search_url = "https://ucpweb.sco.ca.gov/ucpsearch/results"

    async def search(self, name: str) -> list[SearchResult]:
        """Search California unclaimed property database."""
        parts = name.strip().split()
        if len(parts) < 2:
            return []

        first_name = parts[0]
        last_name = parts[-1]

        try:
            response = await self._fetch(
                self.search_url,
                params={
                    "firstName": first_name,
                    "lastName": last_name,
                    "propertyType": "ALL",
                },
            )
            return self._parse(response.text, name)
        except Exception:
            return []

    def _parse(self, html: str, query: str) -> list[SearchResult]:
        """Parse CA SCO search results HTML."""
        results = []
        # Real parsing will use BeautifulSoup against CA SCO's response format
        # Placeholder until we inspect the live response structure
        return results
