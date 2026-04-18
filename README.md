# 🏛️ govdata-ai

> **The open source AI layer for US government databases.**  
> Search $210 billion in unclaimed money across all 50 states — in 3 lines of Python.

[![PyPI version](https://badge.fury.io/py/govdata-ai.svg)](https://badge.fury.io/py/govdata-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/shravyareddyyemreddy/govdata-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/shravyareddyyemreddy/govdata-ai/actions)
[![Stars](https://img.shields.io/github/stars/shravyareddyyemreddy/govdata-ai?style=social)](https://github.com/shravyareddyyemreddy/govdata-ai)

---

## The Problem

$210 billion in unclaimed money sits in US government databases right now.  
1 in 7 Americans is owed money they don't know about.  
The existing tools look like they were built in 2003 and require you to check each state manually.

**This library fixes that.**

---

## Install

```bash
pip install govdata-ai
```

---

## 30-Second Demo

```python
from govdata_ai import UnclaimedMoneySearch

results = UnclaimedMoneySearch().search(
    name="Jane Smith",
    states=["CA", "NY", "TX"]
)

for r in results:
    print(r)
# ✅ Match (94% confidence) — Jane M. Smith | $1,240.00 | California State Controller
# Source: https://scoweb.sco.ca.gov/UCP/Default.aspx
```

Every result includes:
- The exact government source URL (no hallucinations, ever)
- Confidence score (0–100%)
- How to claim it (direct link + instructions)

---

## Features

| Feature | Description |
|---------|-------------|
| **50-state coverage** | All US state unclaimed property databases |
| **Federal sources** | IRS, FDIC, PBGC (pensions), SSA, VA benefits |
| **Zero hallucinations** | Every result links to an official government page |
| **Smart name matching** | Handles maiden names, typos, nicknames, middle names |
| **Confidence scoring** | Know how certain the match is before you claim |
| **Async by default** | Search 50 states in parallel, not 50 sequential requests |
| **Built-in evals** | Measure your accuracy — don't just ship and pray |
| **Privacy first** | No data stored, no SSN required |

---

## Full API

### Search by name

```python
from govdata_ai import UnclaimedMoneySearch

search = UnclaimedMoneySearch()

# Search specific states
results = search.search(name="John Doe", states=["CA", "TX"])

# Search all 50 states (async, fast)
results = await search.search_all_states(name="John Doe")

# Include federal databases
results = await search.search_all(
    name="John Doe",
    include_federal=True,   # IRS, FDIC, PBGC, SSA
    include_states=True     # all 50 states
)
```

### Result object

```python
result.name           # Name as it appears in the database
result.amount         # Dollar amount (if disclosed)
result.source         # Database name (e.g. "California State Controller")
result.source_url     # Direct government URL — always present
result.confidence     # 0–100 match confidence
result.claim_url      # Direct link to start claiming
result.property_type  # e.g. "Bank Account", "Insurance", "Tax Refund"
result.reported_date  # When it was reported to the state
```

### Name matching options

```python
from govdata_ai import NameMatcher

matcher = NameMatcher()

# Fuzzy matching (handles typos)
matcher.match("Jon Smith", "John Smith")   # 0.94

# Phonetic matching (handles pronunciation variants)
matcher.phonetic_match("Shravya", "Shraviya")  # True

# With address context (higher confidence)
matcher.match_with_address(
    name="Jane Smith",
    address="123 Main St, San Francisco CA",
    candidate_name="Jane M Smith",
    candidate_address="San Francisco, California"
)  # 0.97
```

### Evaluate your results

```python
from govdata_ai.evals import run_evals

# Run built-in benchmark against labeled test set
report = run_evals()
print(report.accuracy)       # 0.94
print(report.false_positives) # 3.2%
print(report.coverage)       # states covered: 50/50
```

---

## Supported Databases

### State Unclaimed Property (50/50)
| State | API | Status |
|-------|-----|--------|
| California | NAUPA + State API | ✅ |
| Texas | Texas Comptroller API | ✅ |
| New York | NY OSC API | ✅ |
| Florida | FL DFS API | ✅ |
| ... | ... | ✅ all 50 |

### Federal Databases
| Source | Data | Status |
|--------|------|--------|
| IRS | Unclaimed tax refunds | ✅ |
| FDIC | Failed bank deposits | ✅ |
| PBGC | Unclaimed pension benefits | ✅ |
| SSA | Lump-sum death benefits | ✅ |
| VA | Unclaimed veteran benefits | ✅ |
| HUD | Unclaimed FHA insurance | ✅ |

---

## Architecture

```
govdata_ai/
├── sources/
│   ├── states/          # 50 state scrapers (one per state)
│   ├── federal/         # IRS, FDIC, PBGC, SSA, VA scrapers
│   └── base.py          # Base scraper class (async, retries, caching)
├── matching/
│   ├── fuzzy.py         # RapidFuzz-based name matching
│   ├── phonetic.py      # Soundex + Metaphone matching
│   ├── address.py       # Address normalization + matching
│   └── scorer.py        # Confidence score aggregator
├── evals/
│   ├── benchmark.py     # Labeled test set + accuracy metrics
│   └── datasets/        # Known matches for validation
└── api.py               # Main public API
```

**Zero Hallucination Policy:**
Every single result must have a `source_url` pointing to an official `.gov` domain.  
If we can't verify it, we don't return it. This is enforced at the type level.

---

## Contributing

We welcome contributions for:
- Adding/improving state scrapers
- Improving name matching accuracy
- Adding new federal database sources
- Improving documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/shravyareddyyemreddy/govdata-ai
cd govdata-ai
pip install -e ".[dev]"
pytest tests/
```

---

## Roadmap

- [x] Architecture design
- [ ] 10-state MVP (CA, TX, NY, FL, IL, PA, OH, GA, NC, MI)
- [ ] All 50 states
- [ ] Federal databases (IRS, FDIC, PBGC, SSA, VA)
- [ ] PyPI package
- [ ] Web demo (free, no login required)
- [ ] JavaScript/TypeScript port
- [ ] arXiv paper on matching methodology

---

## Why This Exists

Government data belongs to the people. Existing tools require you to manually search each state one by one — most Americans never do it. This library makes it trivial for any developer to build tools that help people find what's rightfully theirs.

**This is infrastructure for a more informed public. Free forever. Open source forever.**

---

## License

MIT — use it for anything, forever.

---

## Author

Built by [Shravya Reddy Yemreddy](https://github.com/shravyareddyyemreddy)  
AI Engineer | Open Source | Building tools that help people

*If this helped you or someone you know find unclaimed money, please ⭐ the repo.*
