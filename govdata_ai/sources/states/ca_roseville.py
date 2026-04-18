"""California - Roseville city stale dated checks (Socrata open data)"""
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register


@register("CA_ROSEVILLE")
class RosevilleCASource(SocrataSource):
    """
    City of Roseville, CA - Stale dated checks (unclaimed).
    Live Socrata dataset. No CAPTCHA. Fully public API.
    Fields: name, amount, date.
    """
    name = "City of Roseville, CA - Stale Dated Checks"
    state = "CA"
    domain = "data.roseville.ca.us"
    dataset_id = "vtyn-52t8"
    name_field = "name"
    amount_field = "amount"
    date_field = "date"
    claim_page = "https://www.roseville.ca.us/cms/one.aspx?portalId=7922140&pageId=16650448"
