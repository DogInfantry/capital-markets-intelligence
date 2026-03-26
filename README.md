# Capital Markets Intelligence Platform

A unified data-driven intelligence system tracking IPOs, M&A, and sovereign capital markets activity across 12 months. Built to demonstrate financial services research, strategic analysis, and risk modeling capabilities.

## Project Structure

```
├── data/
│   ├── raw/              # Raw data from APIs and public sources
│   └── processed/        # Cleaned, normalized datasets
├── scripts/              # Data acquisition and processing
│   ├── 01_fetch_ipo_data.py
│   ├── 02_fetch_mna_data.py
│   ├── 03_stress_test_model.py
│   └── 04_case_study_builder.py
├── analysis/             # Jupyter notebooks for exploratory analysis
│   ├── market_sentiment.ipynb
│   ├── country_risk_model.ipynb
│   └── deal_case_studies.ipynb
└── output/               # Deliverable datasets and charts
```

## What This Delivers

### Layer 1: Data Foundation
- **IPO Tracker**: Recent IPOs with pricing, performance, underwriter, sector
- **M&A Database**: Announced and completed deals with strategic rationale
- **Sovereign Issuance**: Government bond activity, rating changes, FX impact

### Layer 2: Multi-Dimensional Analysis
- **Market Sentiment Lens** (Tier 1: GS-GIR) — Weekly commentary on capital market trends
- **Risk Stress Lens** (Tier 2: JPM Country Risk) — Sovereign rating impact scenarios
- **Value Creation Lens** (Tier 2: PwC Deals, DB Strategy) — M&A post-close performance

### Layer 3: Application-Ready Memos
1. **GS-GIR**: "Weekly Capital Markets Snapshot" (research brief)
2. **D.E. Shaw**: "IPO Performance Dashboard" (IPO-centric analysis)
3. **JPM Country Risk**: "Sovereign Risk & Capital Issuance Model" (stress framework)
4. **PwC/DB Strategy**: "M&A Strategic Rationale Case Studies" (deal analysis)

## Quick Start

### Week 1: Data Pipeline
```bash
python scripts/01_fetch_ipo_data.py
python scripts/02_fetch_mna_data.py
```

### Week 2: Analysis
```bash
jupyter notebook analysis/market_sentiment.ipynb
jupyter notebook analysis/country_risk_model.ipynb
```

### Week 3: Stress Testing & Case Studies
```bash
python scripts/03_stress_test_model.py
python scripts/04_case_study_builder.py
```

### Week 4: Export & Polish
Output CSV/Parquet files → Opus for memo writing

## Data Sources

- **IPOs**: SEC EDGAR, Renaissance Capital, Company filings
- **M&A**: Bloomberg, Refinitiv, SEC EDGAR (8-K, S-4 filings)
- **Sovereign Data**: IMF, World Bank, Central Bank bulletins, Bloomberg
- **Market Data**: Yahoo Finance, FRED, Trading Economics

## Technology Stack

- **Python**: pandas, numpy, requests, beautifulsoup4
- **Analysis**: Jupyter, matplotlib, seaborn, scipy
- **Data**: CSV, Parquet
- **Version Control**: Git
- **Export**: CSV → Excel/PDF (via Opus + Word)

## Git Workflow

Each week = new branch:
```bash
git checkout -b week-1-data-pipeline
git add scripts/01_fetch_ipo_data.py
git commit -m "Add IPO data scraper (SEC EDGAR + Renaissance)"
git push origin week-1-data-pipeline
```

## Timeline

- **Week 1**: Data gathering & cleaning (5–10 scripts)
- **Week 2**: Exploratory analysis & visualization
- **Week 3**: Stress testing, case study logic, modeling
- **Week 4**: Export → Opus for polished memos
- **Week 5**: Package for applications (GitHub + PDFs)

## Applications

This project is positioned for:
- Goldman Sachs (GIR, Executive Office)
- D.E. Shaw (Capital Markets Research)
- JPMorganChase (Country Risk)
- Deutsche Bank (PB Strategy, Ratings Advisory)
- PwC (Deals Strategy)

---

**Created**: March 2026  
**Status**: In progress (Week 1)
