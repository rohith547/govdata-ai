"""Massachusetts - Framingham unclaimed payroll and vendor checks (Socrata open data)"""
from __future__ import annotations
from govdata_ai.sources.base import SocrataSource
from govdata_ai.sources.registry import register


@register("MA_FRAMINGHAM_PAYROLL")
class FraminghamMAPayrollSource(SocrataSource):
    """City of Framingham, MA - Unclaimed payroll checks. Fields: name, amount, date_of_check."""
    name = "City of Framingham, MA - Unclaimed Payroll Checks"
    state = "MA"
    domain = "data.framinghamma.gov"
    dataset_id = "9d75-5t5b"
    name_field = "name"
    amount_field = "amount"
    date_field = "date_of_check"
    claim_page = "https://www.framinghamma.gov/749/Finance"


@register("MA_FRAMINGHAM_VENDOR")
class FraminghamMAVendorSource(SocrataSource):
    """City of Framingham, MA - Unclaimed resident/vendor checks. Includes last known address."""
    name = "City of Framingham, MA - Unclaimed Resident & Vendor Checks"
    state = "MA"
    domain = "data.framinghamma.gov"
    dataset_id = "acuy-64k3"
    name_field = "name"
    amount_field = "amount"
    date_field = "date_of_check"
    claim_page = "https://www.framinghamma.gov/749/Finance"
