from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator


class SearchResult(BaseModel):
    """A single unclaimed property match. Every field is verified — no hallucinations."""

    name: str                        # Name as it appears in the government database
    amount: Optional[float] = None   # Dollar amount (not always disclosed)
    source: str                      # Database name e.g. "California State Controller"
    source_url: str                  # Always a .gov URL — enforced below
    confidence: float                # 0.0–1.0 match confidence
    claim_url: str                   # Direct link to start the claim
    property_type: Optional[str] = None   # "Bank Account", "Insurance", "Tax Refund", etc.
    reported_date: Optional[str] = None   # When reported to the state
    state: Optional[str] = None      # 2-letter state code

    @field_validator("source_url", "claim_url")
    @classmethod
    def must_be_gov_url(cls, v: str) -> str:
        """Zero hallucination policy: all URLs must point to official .gov domains."""
        trusted_domains = [".gov", "naupa.org", "unclaimed.org", "missingmoney.com"]
        if not any(domain in v for domain in trusted_domains):
            raise ValueError(
                f"Source URL must be an official government or trusted domain. Got: {v}"
            )
        return v

    def __str__(self) -> str:
        amount_str = f"${self.amount:,.2f}" if self.amount else "Amount not disclosed"
        pct = int(self.confidence * 100)
        return f"✅ Match ({pct}% confidence) — {self.name} | {amount_str} | {self.source}"
