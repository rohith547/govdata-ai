"""California - Marin County unclaimed checks (Socrata open data)"""
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register


@register("CA_MARIN")
class MarinCountyCASource(SocrataSource):
    """
    Marin County, CA - Unclaimed checks (vendor payments).
    Live Socrata dataset. No CAPTCHA. Fully public API.
    Updated 2025. Fields: vendor_name, amount, check_date.
    """
    name = "Marin County, CA - Unclaimed Checks"
    state = "CA"
    domain = "data.marincounty.gov"
    dataset_id = "er4x-svwp"
    name_field = "vendor_name"
    amount_field = "amount"
    date_field = "check_date"
    claim_page = "https://www.marincounty.gov/depts/au/divisions/payroll-and-vendor-services"
