# Capital Markets Intelligence Platform

A unified data-driven intelligence system tracking IPOs, M&A, and sovereign capital markets activity across 12 months. Built to demonstrate financial services research, strategic analysis, and risk modeling capabilities.

## Project Structure

```
├── data/
│   ├── raw/                         # Raw datasets
│   │   ├── ipo_data_raw.csv         # 25 IPOs across 7 countries
│   │   ├── mna_data_raw.csv         # 20 M&A deals ($483.5B total)
│   │   └── sovereign_issuance_raw.csv  # 31 issuances across 18 countries
│   └── processed/
│       ├── stress_test_results.csv  # 60 sovereign stress scenarios
│       └── case_studies.csv         # 20 M&A case study analyses
├── scripts/
│   ├── 01_fetch_ipo_data.py         # IPO data pipeline
│   ├── 02_fetch_mna_data.py         # M&A deal database builder
│   ├── 03_stress_test_model.py      # Sovereign stress testing (5 scenarios)
│   ├── 04_case_study_builder.py     # M&A case study analysis
│   ├── 05_fetch_sovereign_data.py   # Sovereign bond issuance tracker
│   ├── 06_generate_visualizations.py # 10 professional charts
│   └── 07_generate_memos.py         # 4 application-ready memos
├── analysis/                         # Jupyter notebooks
│   ├── market_sentiment.ipynb       # GS-GIR style market analysis
│   ├── country_risk_model.ipynb     # JPM Country Risk stress model
│   └── deal_case_studies.ipynb      # PwC/DB deal analysis
├── output/
│   ├── memos/                       # Application-ready research memos
│   │   ├── gs_gir_weekly_snapshot.txt
│   │   ├── de_shaw_ipo_dashboard.txt
│   │   ├── jpm_sovereign_risk_model.txt
│   │   └── pwc_db_mna_case_studies.txt
│   ├── ipo_first_day_returns.png    # IPO performance charts
│   ├── ipo_total_returns.png
│   ├── ipo_by_sector.png
│   ├── mna_by_sector.png            # M&A analysis charts
│   ├── mna_deal_status.png
│   ├── risk_heatmap.png             # Sovereign risk charts
│   ├── yield_impact.png
│   ├── vulnerability_ranking.png
│   ├── deal_size_distribution.png   # Case study charts
│   └── research_relevance.png
└── docs/                            # Planning & specs
```

## What This Delivers

### Layer 1: Data Foundation
- **IPO Tracker**: 25 IPOs with pricing, first-day/total returns, underwriter, sector (7 countries)
- **M&A Database**: 20 deals totaling $483.5B with strategic rationale, status, risk factors
- **Sovereign Issuance**: 31 bond issuances across 18 countries ($325.8B total volume)
- **Stress Test Model**: 12 sovereigns x 5 macro scenarios = 60 risk assessments

### Layer 2: Multi-Dimensional Analysis
- **Market Sentiment Lens** (GS-GIR) — Weekly capital market trends, IPO pipeline, M&A flow
- **Risk Stress Lens** (JPM Country Risk) — Sovereign yield shocks, vulnerability rankings
- **Value Creation Lens** (PwC/DB Strategy) — M&A post-close analysis, value drivers
- **10 Professional Charts** — Publication-quality visualizations (matplotlib/seaborn)

### Layer 3: Application-Ready Memos
1. **GS-GIR**: "Weekly Capital Markets Snapshot" — Executive overview of IPO, M&A, and sovereign markets
2. **D.E. Shaw**: "IPO Performance Dashboard" — Quantitative analysis with statistical summary, return distributions, underwriter league table
3. **JPM Country Risk**: "Sovereign Risk & Capital Issuance Model" — Stress test results, vulnerability rankings, policy implications
4. **PwC/DB Strategy**: "M&A Strategic Rationale Case Studies" — Deep dives on top deals, thematic analysis, regulatory landscape

## Quick Start

```bash
# Clone the repository
git clone https://github.com/DogInfantry/capital-markets-intelligence.git
cd capital-markets-intelligence

# Set up Python environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Run the full pipeline
python scripts/01_fetch_ipo_data.py           # Fetch IPO data (25 IPOs)
python scripts/02_fetch_mna_data.py           # Fetch M&A data (20 deals)
python scripts/03_stress_test_model.py        # Run stress tests (5 scenarios)
python scripts/04_case_study_builder.py       # Generate case studies
python scripts/05_fetch_sovereign_data.py     # Fetch sovereign issuance data
python scripts/06_generate_visualizations.py  # Generate 10 charts
python scripts/07_generate_memos.py           # Generate 4 research memos
```

## Sample Output

### Charts
| Chart | Description |
|-------|-------------|
| `ipo_first_day_returns.png` | First-day returns by company (green/red bars) |
| `ipo_total_returns.png` | Total returns to date with median line |
| `risk_heatmap.png` | Sovereign risk scores by scenario (color-coded heatmap) |
| `vulnerability_ranking.png` | Country vulnerability ranking across stress scenarios |
| `deal_size_distribution.png` | M&A deal sizes by tier (mega/large/mid/core) |

### Research Memos
| Memo | Target | Pages |
|------|--------|-------|
| GS-GIR Weekly Snapshot | Goldman Sachs GIR / Executive Office | ~5 |
| D.E. Shaw IPO Dashboard | D.E. Shaw Capital Markets Research | ~4 |
| JPM Sovereign Risk Model | JPMorgan Country Risk Advisory | ~6 |
| PwC/DB M&A Case Studies | PwC Deals Strategy / Deutsche Bank | ~8 |

## Data Sources

- **IPOs**: SEC EDGAR, Renaissance Capital, Company filings
- **M&A**: Bloomberg, Refinitiv, SEC EDGAR (8-K, S-4 filings)
- **Sovereign Data**: IMF, World Bank, Central Bank bulletins, Bloomberg
- **Market Data**: Yahoo Finance, FRED, Trading Economics

## Technology Stack

- **Python 3.13**: pandas, numpy, requests, beautifulsoup4
- **Analysis**: Jupyter, matplotlib, seaborn, scipy
- **Data**: CSV
- **Visualization**: matplotlib (Agg backend), seaborn
- **Version Control**: Git + GitHub

## Applications

This project is positioned for:
- **Goldman Sachs** (GIR, Executive Office)
- **D.E. Shaw** (Capital Markets Research)
- **JPMorganChase** (Country Risk)
- **Deutsche Bank** (PB Strategy, Ratings Advisory)
- **PwC** (Deals Strategy)

## License

MIT License — see [LICENSE](LICENSE)

---

**Created**: March 2026
**Status**: Complete
