"""Rhode Island — Providence unclaimed property (Socrata open data)"""
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register


@register("RI")
class ProvidenceRISource(SocrataSource):
    """
    Providence, RI — Unclaimed stale-dated checks.
    Live dataset: https://data.providenceri.gov/d/4hhd-fzq6
    Updated regularly. No CAPTCHA. Fully public API.
    1,779+ records. Fields: payee_name, payment_amount, city, state, zip_code.
    """
    name = "City of Providence, RI — Unclaimed Checks"
    state = "RI"
    domain = "data.providenceri.gov"
    dataset_id = "4hhd-fzq6"
    name_field = "payee_name"
    amount_field = "payment_amount"
    date_field = "check_date"
    claim_page = "https://www.providenceri.gov/finance/unclaimed-property/"
