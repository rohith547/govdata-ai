"""
govdata-ai — Basic tests

Run: pytest tests/ -v
"""
import pytest
from govdata_ai.matching import NameMatcher
from govdata_ai.models import SearchResult


class TestNameMatcher:
    def setup_method(self):
        self.matcher = NameMatcher()

    def test_exact_match_returns_1(self):
        assert self.matcher.match("JOHN SMITH", "JOHN SMITH") == 1.0

    def test_typo_still_high_confidence(self):
        score = self.matcher.match("Jon Smith", "John Smith")
        assert score >= 0.80, f"Expected >= 0.80, got {score}"

    def test_word_order_doesnt_matter(self):
        score = self.matcher.match("Smith John", "John Smith")
        assert score >= 0.85

    def test_maiden_name_partial(self):
        score = self.matcher.match("Jane Smith", "Jane Smith-Johnson")
        assert score >= 0.75

    def test_completely_different_names(self):
        score = self.matcher.match("John Smith", "Maria Garcia")
        assert score < 0.50

    def test_phonetic_match_soundalikes(self):
        # "Jon" and "John" sound the same
        result = self.matcher.phonetic_match("Jon", "John")
        assert result is True

    def test_phonetic_no_match(self):
        result = self.matcher.phonetic_match("Smith", "Garcia")
        assert result is False


class TestSearchResult:
    def test_valid_gov_url_accepted(self):
        result = SearchResult(
            name="John Smith",
            amount=1240.00,
            source="California State Controller",
            source_url="https://ucpweb.sco.ca.gov/results",
            confidence=0.94,
            claim_url="https://ucpweb.sco.ca.gov/claim/12345",
            state="CA",
        )
        assert result.confidence == 0.94

    def test_non_gov_url_rejected(self):
        with pytest.raises(Exception):
            SearchResult(
                name="John Smith",
                amount=100.00,
                source="Fake Source",
                source_url="https://fakemoney.com/results",  # not .gov!
                confidence=0.9,
                claim_url="https://fakemoney.com/claim",
                state="CA",
            )

    def test_str_representation(self):
        result = SearchResult(
            name="Jane Smith",
            amount=847.50,
            source="California State Controller",
            source_url="https://ucpweb.sco.ca.gov/results",
            confidence=0.94,
            claim_url="https://ucpweb.sco.ca.gov/claim",
        )
        output = str(result)
        assert "94%" in output
        assert "847.50" in output
        assert "✅" in output
