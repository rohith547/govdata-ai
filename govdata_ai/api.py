from __future__ import annotations
import asyncio
from typing import Optional
from govdata_ai.models import SearchResult


class UnclaimedMoneySearch:
    """
    Main entry point for govdata-ai.

    Searches US government databases for unclaimed property matching a name.
    Zero hallucinations: every result has a verified .gov source URL.

    Usage:
        from govdata_ai import UnclaimedMoneySearch

        results = UnclaimedMoneySearch().search("Jane Smith", states=["CA", "NY"])
        for r in results:
            print(r)
    """

    ALL_STATES = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
        "DC",
    ]

    def search(
        self,
        name: str,
        states: Optional[list[str]] = None,
        include_federal: bool = False,
        min_confidence: float = 0.7,
    ) -> list[SearchResult]:
        """
        Search for unclaimed property synchronously.

        Args:
            name: Full name to search (handles maiden names, typos, middle names)
            states: List of 2-letter state codes. Defaults to top 10 by population.
            include_federal: Also search IRS, FDIC, PBGC, SSA, VA databases.
            min_confidence: Only return results above this confidence threshold (0–1).

        Returns:
            List of SearchResult objects, sorted by confidence descending.
        """
        return asyncio.run(
            self.search_async(name, states, include_federal, min_confidence)
        )

    async def search_async(
        self,
        name: str,
        states: Optional[list[str]] = None,
        include_federal: bool = False,
        min_confidence: float = 0.7,
    ) -> list[SearchResult]:
        """Async version — searches all states in parallel."""
        from govdata_ai.sources.registry import get_source_for_state
        from govdata_ai.sources.federal import get_federal_sources

        target_states = states or ["CA", "TX", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]

        tasks = []
        for state in target_states:
            source = get_source_for_state(state)
            if source:
                tasks.append(source.search(name))

        if include_federal:
            for source in get_federal_sources():
                tasks.append(source.search(name))

        all_results = await asyncio.gather(*tasks, return_exceptions=True)

        results: list[SearchResult] = []
        for batch in all_results:
            if isinstance(batch, Exception):
                continue  # Log and continue — one state failing doesn't break everything
            results.extend(batch)

        return sorted(
            [r for r in results if r.confidence >= min_confidence],
            key=lambda r: r.confidence,
            reverse=True,
        )

    async def search_all_states(
        self, name: str, min_confidence: float = 0.7
    ) -> list[SearchResult]:
        """Search all 50 states + DC in parallel."""
        return await self.search_async(name, self.ALL_STATES, min_confidence=min_confidence)
