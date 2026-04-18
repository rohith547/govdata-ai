"""Minnesota — Ramsey County missing heirs / unclaimed estates (Socrata open data)"""
from __future__ import annotations
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register
from govdata_ai.models import SearchResult


@register("MN_RAMSEY")
class RamseyCountyMNSource(SocrataSource):
    """
    Ramsey County, MN — Missing heirs and unclaimed estate funds.
    Amounts up to $17,000+. Write-off dates listed.
    Live Socrata dataset. No CAPTCHA. Fully public API.
    Fields: heir, dollar_amount, estate_of, date_received, write_off.
    """
    name = "Ramsey County, MN — Missing Heirs & Unclaimed Estates"
    state = "MN"
    domain = "data.ramseycountymn.gov"
    dataset_id = "t2fe-qrnd"
    name_field = "heir"
    amount_field = "dollar_amount"
    date_field = "date_received"
    claim_page = "https://www.ramseycounty.us/your-government/leadership/court-administration/probate-division"

    async def search(self, name: str) -> list[SearchResult]:  # type: ignore[override]
        """Also search by estate_of field (deceased person's name)."""
        results = await super().search(name)
        seen_keys = {(r.name, r.amount) for r in results}

        # Also search estate_of field
        parts = name.strip().upper().split()
        if not parts:
            return results

        try:
            where = f"upper(estate_of) like upper('%{parts[-1]}%')"
            rows = await self._fetch_json({"$where": where, "$limit": 50})
            for row in rows:
                candidate = row.get("heir", "") or row.get("estate_of", "")
                if not candidate:
                    continue
                amount_raw = row.get("dollar_amount")
                try:
                    amount = float(str(amount_raw).replace(",", "")) if amount_raw else None
                except ValueError:
                    amount = None

                key = (candidate, amount)
                if key in seen_keys:
                    continue
                seen_keys.add(key)

                result = self._make_result(
                    name=candidate,
                    query=name,
                    source_url=f"https://{self.domain}/d/{self.dataset_id}",
                    claim_url=self.claim_page,
                    amount=amount,
                    reported_date=row.get("date_received"),
                    property_type="Estate/Probate",
                )
                if result.confidence >= 0.5:
                    results.append(result)
        except Exception:
            pass

        return sorted(results, key=lambda r: r.confidence, reverse=True)
