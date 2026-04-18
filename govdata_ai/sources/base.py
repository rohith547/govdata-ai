from __future__ import annotations
import abc
from typing import Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from govdata_ai.models import SearchResult
from govdata_ai.matching import NameMatcher


class BaseGovSource(abc.ABC):
    name: str = ""
    state: Optional[str] = None
    base_url: str = ""

    def __init__(self):
        self.matcher = NameMatcher()

    @abc.abstractmethod
    async def search(self, name: str) -> list[SearchResult]:
        ...

    def _make_result(self, name: str, query: str, source_url: str, claim_url: str,
                     amount: Optional[float] = None, property_type: Optional[str] = None,
                     reported_date: Optional[str] = None) -> SearchResult:
        confidence = self.matcher.match(query, name)
        return SearchResult(name=name, amount=amount, source=self.name,
                            source_url=source_url, confidence=confidence,
                            claim_url=claim_url, property_type=property_type,
                            reported_date=reported_date, state=self.state)


class SocrataSource(BaseGovSource):
    """
    Base for any government database published via Socrata open data platform.
    Dozens of cities/counties/states publish unclaimed property data here.
    No CAPTCHA, clean JSON API, fully public.
    """
    dataset_id: str = ""
    domain: str = ""
    name_field: str = ""         # field containing owner name
    amount_field: str = ""       # field containing dollar amount
    date_field: str = ""         # field containing report date
    claim_page: str = ""         # URL where user goes to claim

    def _api_url(self) -> str:
        return f"https://{self.domain}/resource/{self.dataset_id}.json"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def _fetch_json(self, params: dict) -> list[dict]:
        # Build query string manually — httpx encodes '$' as '%24' but Socrata
        # requires literal '$where', '$limit', etc. in the query string.
        import urllib.parse
        qs_parts = []
        for k, v in params.items():
            qs_parts.append(f"{k}={urllib.parse.quote(str(v))}")
        url = f"{self._api_url()}?{'&'.join(qs_parts)}"
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()

    async def search(self, name: str) -> list[SearchResult]:
        parts = name.strip().upper().split()
        if not parts:
            return []

        # Socrata SoQL: case-insensitive name search
        where = f"upper({self.name_field}) like upper('%{parts[-1]}%')"

        try:
            rows = await self._fetch_json({"$where": where, "$limit": 100})
        except Exception:
            return []

        results = []
        for row in rows:
            candidate_name = row.get(self.name_field, "")
            if not candidate_name:
                continue

            amount_raw = row.get(self.amount_field)
            try:
                amount = float(str(amount_raw).replace(",", "").replace("$", "")) if amount_raw else None
            except ValueError:
                amount = None

            result = self._make_result(
                name=candidate_name,
                query=name,
                source_url=f"https://{self.domain}/d/{self.dataset_id}",
                claim_url=self.claim_page,
                amount=amount,
                reported_date=row.get(self.date_field),
            )
            if result.confidence >= 0.6:
                results.append(result)

        return sorted(results, key=lambda r: r.confidence, reverse=True)
