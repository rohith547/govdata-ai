"""California — Sonoma County stale dated checks (Socrata open data)"""
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register


@register("CA_SONOMA")
class SonomaCountyCASource(SocrataSource):
    """
    Sonoma County, CA — Stale dated checks (unclaimed).
    Live Socrata dataset. No CAPTCHA. Fully public API.
    Fields: payeename, issueamount, issuedate, checknumber.
    """
    name = "Sonoma County, CA — Stale Dated Checks"
    state = "CA"
    domain = "data.sonomacounty.ca.gov"
    dataset_id = "7zt2-w5w6"
    name_field = "payeename"
    amount_field = "issueamount"
    date_field = "issuedate"
    claim_page = "https://sonomacounty.ca.gov/administrative-support-and-fiscal-services/auditor-controller-treasurer-tax-collector/divisions/treasury-and-taxation"
