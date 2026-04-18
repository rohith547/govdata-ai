"""Texas — Austin unclaimed property (Socrata open data)"""
from __future__ import annotations
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register
from govdata_ai.models import SearchResult


@register("TX_AUSTIN")
class AustinTXSource(SocrataSource):
    """
    City of Austin, TX — Unclaimed property.
    Live Socrata dataset. No CAPTCHA. Fully public API.
    Fields: last (surname), first (given name). No amount — city uses $100 max cutoff.
    """
    name = "City of Austin, TX — Unclaimed Property"
    state = "TX"
    domain = "datahub.austintexas.gov"
    dataset_id = "h3i4-5e5v"
    name_field = "last"
    amount_field = ""
    date_field = ""
    claim_page = "https://www.austintexas.gov/finance/unclaimed-property"

    async def search(self, name: str) -> list[SearchResult]:
        """Austin stores last + first separately; combine them for matching."""
        parts = name.strip().upper().split()
        if not parts:
            return []

        last = parts[-1]
        where = f"upper(last) like upper('%{last}%')"
        try:
            rows = await self._fetch_json({"$where": where, "$limit": 100})
        except Exception:
            return []

        results = []
        for row in rows:
            last_name = row.get("last", "").strip()
            first_name = row.get("first", "").strip()
            full_name = f"{first_name} {last_name}".strip() if first_name else last_name
            if not full_name:
                continue

            result = self._make_result(
                name=full_name,
                query=name,
                source_url=f"https://{self.domain}/d/{self.dataset_id}",
                claim_url=self.claim_page,
                amount=None,
            )
            if result.confidence >= 0.6:
                results.append(result)

        return sorted(results, key=lambda r: r.confidence, reverse=True)
