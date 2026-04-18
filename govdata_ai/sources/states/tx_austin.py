"""Texas — Austin unclaimed property (Socrata open data)"""
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register


@register("TX_AUSTIN")
class AustinTXSource(SocrataSource):
    """
    City of Austin, TX — Unclaimed property.
    Live Socrata dataset. No CAPTCHA. Fully public API.
    """
    name = "City of Austin, TX — Unclaimed Property"
    state = "TX"
    domain = "datahub.austintexas.gov"
    dataset_id = "h3i4-5e5v"
    name_field = "last"
    amount_field = ""
    date_field = ""
    claim_page = "https://www.austintexas.gov/finance/unclaimed-property"
