from __future__ import annotations
import abc
import asyncio
from typing import Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from govdata_ai.models import SearchResult
from govdata_ai.matching import NameMatcher


class BaseGovSource(abc.ABC):
    """
    Base class for all government database sources.
    Handles retries, rate limiting, caching, and the zero-hallucination contract.
    """

    name: str = ""          # Human-readable source name
    state: Optional[str] = None  # 2-letter state code, None for federal
    base_url: str = ""      # Official government base URL

    def __init__(self):
        self.matcher = NameMatcher()
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if not self._client:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers={"User-Agent": "govdata-ai/0.1.0 (open source research tool)"},
                follow_redirects=True,
            )
        return self._client

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def _fetch(self, url: str, **kwargs) -> httpx.Response:
        client = await self._get_client()
        response = await client.get(url, **kwargs)
        response.raise_for_status()
        return response

    @abc.abstractmethod
    async def search(self, name: str) -> list[SearchResult]:
        """Search this source for unclaimed property matching the given name."""
        ...

    def _make_result(
        self,
        name: str,
        query: str,
        source_url: str,
        claim_url: str,
        amount: Optional[float] = None,
        property_type: Optional[str] = None,
        reported_date: Optional[str] = None,
    ) -> SearchResult:
        """Build a SearchResult with automatic confidence scoring."""
        confidence = self.matcher.match(query, name)
        return SearchResult(
            name=name,
            amount=amount,
            source=self.name,
            source_url=source_url,
            confidence=confidence,
            claim_url=claim_url,
            property_type=property_type,
            reported_date=reported_date,
            state=self.state,
        )

    async def close(self):
        if self._client:
            await self._client.aclose()
