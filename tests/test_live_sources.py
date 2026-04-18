"""
Integration tests that hit real government APIs.
These make actual network  run with: pytest tests/test_live_sources.py -vcalls 
Skipped in CI unless GOVDATA_LIVE_TESTS=1 is set.
"""
import os
import pytest
import asyncio

pytestmark = pytest.mark.skipif(
    os.getenv("GOVDATA_LIVE_TESTS") != "1",
    reason="Live API tests: set GOVDATA_LIVE_TESTS=1 to run"
)

from govdata_ai.sources.states import ri, ca_sonoma, mn_ramsey, tx_austin
from govdata_ai.sources.registry import get_source_for_state


@pytest.mark.asyncio
async def test_ri_search_returns_results():
    src = get_source_for_state("RI")
    results = await src.search("Smith")
    assert len(results) > 0
    for r in results:
        assert "SMITH" in r.name.upper()
        assert r.confidence >= 0.6
        assert ".gov" in r.source_url or ".us" in r.source_url or ".gov" in r.claim_url


@pytest.mark.asyncio
async def test_mn_search_returns_results():
    src = get_source_for_state("MN_RAMSEY")
    results = await src.search("Jones")
    assert len(results) > 0
    for r in results:
        assert r.amount is not None
        assert r.confidence >= 0.5


@pytest.mark.asyncio
async def test_tx_search_returns_results():
    src = get_source_for_state("TX_AUSTIN")
    results = await src.search("Martinez")
    assert len(results) > 0
    for r in results:
        assert r.confidence >= 0.6


@pytest.mark.asyncio
async def test_results_no_duplicates():
    """Ensure MN source deduplicates results."""
    src = get_source_for_state("MN_RAMSEY")
    results = await src.search("Jones")
    keys = [(r.name, r.amount) for r in results]
    assert len(keys) == len(set(keys)), "Duplicate results found"


@pytest.mark.asyncio
async def test_ri_confidence_ordering():
    """Results should be sorted highest confidence first."""
    src = get_source_for_state("RI")
    results = await src.search("Smith")
    confs = [r.confidence for r in results]
    assert confs == sorted(confs, reverse=True)
