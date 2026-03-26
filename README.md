# Capital Markets Intelligence Platform

A comprehensive data-driven intelligence system tracking IPOs, M&A, and sovereign capital markets activity. Pulls live data from Yahoo Finance and World Bank APIs, runs proprietary analytical models (yield curve decomposition, sovereign risk scoring, cross-asset regime detection), and produces professional outputs across three independent formats: interactive Plotly HTML dashboards, formatted Excel workbooks, and PDF research reports.

Built to demonstrate financial services research, strategic analysis, and risk modeling capabilities relevant to Goldman Sachs, D.E. Shaw, JPMorganChase, Deutsche Bank, and PwC.

## Project Structure

```
├── data/
│   ├── raw/                                  # Live API + curated datasets
│   │   ├── ipo_data_raw.csv                  # 25 IPOs across 7 countries
│   │   ├── mna_data_raw.csv                  # 20 M&A deals ($483.5B total)
│   │   ├── sovereign_issuance_raw.csv        # 31 issuances, 18 countries
│   │   ├── yield_curve_history.csv           # Treasury yields (3M/5Y/10Y/30Y, 501 days)
│   │   ├── market_rates.csv                  # S&P500, VIX, Gold, WTI Oil
│   │   ├── fx_rates.csv                      # 9 EM/DM FX pairs + 30d rolling vol
│   │   ├── worldbank_indicators.csv          # 15 indicators, 20 countries
│   │   └── country_macro_panel.csv           # Country-year panel dataset
│   ├── processed/                            # Analytical model outputs
│   │   ├── yield_curve_analysis.csv          # Level/slope/curvature decomposition
│   │   ├── sovereign_risk_index.csv          # Proprietary risk scores (0-100)
│   │   ├── regime_indicators.csv             # Risk-on/off regime signals
│   │   ├── deal_screening_model.csv          # M&A completion predictors
│   │   ├── deal_feature_importance.csv       # Point-biserial correlations
│   │   ├── ipo_event_study.csv               # Abnormal returns & money left on table
│   │   ├── stress_test_results.csv           # 60 sovereign stress scenarios
│   │   └── case_studies.csv                  # 20 M&A case study analyses
│   └── cache/                                # Offline fallback cache
├── scripts/
│   ├── 01_fetch_ipo_data.py                  # IPO data pipeline
│   ├── 02_fetch_mna_data.py                  # M&A deal database builder
│   ├── 03_stress_test_model.py               # Sovereign stress testing (5 scenarios)
│   ├── 04_case_study_builder.py              # M&A case study analysis
│   ├── 05_fetch_sovereign_data.py            # Sovereign bond issuance tracker
│   ├── 06_generate_visualizations.py         # 10 static PNG charts
│   ├── 07_generate_memos.py                  # 4 text research memos
│   ├── 08_fetch_fred_data.py                 # Live Yahoo Finance market data
│   ├── 09_fetch_worldbank_data.py            # World Bank API macro indicators
│   ├── 10_advanced_analysis.py               # 5 proprietary analytical models
│   ├── 11_generate_plotly_dashboards.py      # 5 interactive HTML dashboards
│   ├── 12_generate_excel_reports.py          # 4 formatted Excel workbooks
│   └── 13_generate_pdf_reports.py            # 4 professional PDF reports
├── analysis/                                  # Jupyter notebooks
│   ├── market_sentiment.ipynb                # GS-GIR style market analysis
│   ├── country_risk_model.ipynb              # JPM Country Risk stress model
│   └── deal_case_studies.ipynb               # PwC/DB deal analysis
├── output/
│   ├── dashboards/                            # Interactive Plotly HTML
│   │   ├── yield_curve_dashboard.html
│   │   ├── sovereign_risk_dashboard.html
│   │   ├── market_regime_dashboard.html
│   │   ├── ipo_analysis_dashboard.html
│   │   └── mna_screening_dashboard.html
│   ├── excel/                                 # Formatted Excel workbooks
│   │   ├── ipo_analysis_workbook.xlsx
│   │   ├── sovereign_risk_workbook.xlsx
│   │   ├── mna_analysis_workbook.xlsx
│   │   └── capital_markets_master.xlsx
│   ├── pdf/                                   # Professional PDF reports
│   │   ├── gs_gir_capital_markets_snapshot.pdf
│   │   ├── jpm_sovereign_risk_report.pdf
│   │   ├── de_shaw_ipo_dashboard.pdf
│   │   └── pwc_db_mna_case_studies.pdf
│   └── memos/                                 # Text research memos
│       ├── gs_gir_weekly_snapshot.txt
│       ├── de_shaw_ipo_dashboard.txt
│       ├── jpm_sovereign_risk_model.txt
│       └── pwc_db_mna_case_studies.txt
└── docs/                                      # Planning & specs
```

## What This Delivers

### Layer 1: Live Data Foundation
- **Yahoo Finance API**: Treasury yields (3M/5Y/10Y/30Y, 501 trading days), S&P500, VIX, Gold, WTI Oil, 9 EM/DM FX pairs with 30-day rolling volatility
- **World Bank Open Data API**: 15 macro indicators across 20 countries (GDP, inflation, debt/GDP, current account, reserves, FDI, unemployment, exchange rates, real interest rates, external debt)
- **IPO Tracker**: 25 IPOs with pricing, first-day/total returns, underwriter, sector (7 countries)
- **M&A Database**: 20 deals totaling $483.5B with strategic rationale, status, risk factors
- **Sovereign Issuance**: 31 bond issuances across 18 countries ($325.8B total volume)

### Layer 2: Proprietary Analytical Models
1. **Yield Curve Decomposition** — Level, slope, curvature extraction from Treasury term structure; rolling z-scores; regime classification (Inverted/Flat/Normal/Steep); slope momentum signals
2. **Sovereign Risk Index** — Composite score (0-100) from 11 z-score-normalized World Bank indicators across fiscal health, external vulnerability, growth stability, and reserves adequacy; risk tier classification
3. **Cross-Asset Regime Detection** — 6-signal framework (VIX level, S&P trend, S&P momentum, gold safe-haven, yield curve, FX volatility) producing Risk-On/Neutral/Risk-Off regime calls
4. **M&A Deal Screening** — Point-biserial correlation analysis of 9 deal features against completion outcome; predictive feature importance ranking
5. **IPO Event Study** — Abnormal returns vs S&P500 benchmark; money left on table quantification; pricing assessment classification (Underpriced/Fairly Priced/Overpriced)
6. **Sovereign Stress Testing** — 12 sovereigns x 5 macro scenarios (Base, Fed Hawkish, Global Recession, EM Currency Crisis, Oil Shock)

### Layer 3: Three Independent Output Formats

**Interactive HTML Dashboards (Plotly)**
- Yield curve term structure with regime timeline
- Sovereign risk heatmap with macro indicators
- Market regime dashboard with signal decomposition
- IPO performance scatter with event study metrics
- M&A screening matrix with feature importance

**Formatted Excel Workbooks (openpyxl)**
- IPO workbook: database, event study, summary stats, underwriter league table
- Sovereign workbook: risk index with color scales, macro panel, stress tests, issuance
- M&A workbook: deal database with status coloring, case studies, screening model
- Master summary: executive overview across all verticals

**Professional PDF Reports (fpdf)**
- GS-GIR: Weekly Capital Markets Snapshot
- JPM: Sovereign Risk & Capital Issuance Model
- D.E. Shaw: IPO Performance Dashboard (quantitative)
- PwC/DB: M&A Strategic Rationale Case Studies

### Layer 4: Static Analysis & Memos
- **10 PNG Charts** — Publication-quality matplotlib/seaborn visualizations
- **4 Research Memos** — Firm-specific text reports with executive summaries

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

# Run the full pipeline (in order)

# Phase 1: Data collection
python scripts/01_fetch_ipo_data.py           # IPO data (25 IPOs)
python scripts/02_fetch_mna_data.py           # M&A data (20 deals)
python scripts/03_stress_test_model.py        # Stress tests (5 scenarios)
python scripts/04_case_study_builder.py       # Case studies
python scripts/05_fetch_sovereign_data.py     # Sovereign issuance data

# Phase 2: Live API data
python scripts/08_fetch_fred_data.py          # Yahoo Finance market data
python scripts/09_fetch_worldbank_data.py     # World Bank macro indicators

# Phase 3: Advanced analysis
python scripts/10_advanced_analysis.py        # 5 proprietary models

# Phase 4: Visualizations & outputs
python scripts/06_generate_visualizations.py  # 10 static charts
python scripts/07_generate_memos.py           # 4 text memos
python scripts/11_generate_plotly_dashboards.py  # 5 interactive dashboards
python scripts/12_generate_excel_reports.py   # 4 Excel workbooks
python scripts/13_generate_pdf_reports.py     # 4 PDF reports
```

## Data Sources

| Source | API Key Required | Data |
|--------|-----------------|------|
| Yahoo Finance (yfinance) | No | Treasury yields, S&P500, VIX, Gold, Oil, FX rates |
| World Bank Open Data API | No | 15 macro indicators across 20 countries |
| SEC EDGAR | No | IPO filings (with fallback to curated dataset) |
| Curated databases | N/A | M&A deals, sovereign issuance (sourced from public filings) |

## Technology Stack

- **Python 3.13**: pandas, numpy, requests, scipy
- **Live Data**: yfinance, World Bank API (requests)
- **Analysis**: Jupyter, scipy (stats), numpy (linear algebra)
- **Interactive Dashboards**: Plotly (graph_objects, make_subplots)
- **Excel Reports**: openpyxl (conditional formatting, styled workbooks)
- **PDF Reports**: fpdf (professional formatted reports)
- **Static Visualization**: matplotlib (Agg backend), seaborn
- **Version Control**: Git + GitHub

## Applications

This project is positioned for:
- **Goldman Sachs** (GIR, Executive Office) — Capital markets snapshot, cross-asset regime analysis
- **D.E. Shaw** (Capital Markets Research) — Quantitative IPO event study, statistical analysis
- **JPMorganChase** (Country Risk) — Proprietary sovereign risk index, stress testing
- **Deutsche Bank** (Ratings Advisory) — Sovereign issuance analysis, macro indicators
- **PwC** (Deals Strategy) — M&A case studies, deal screening model

## License

MIT License — see [LICENSE](LICENSE)

---

**Created**: March 2026
**Status**: Complete
