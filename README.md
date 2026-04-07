<div align="center">

# 📊 Capital Markets Intelligence Platform

**A production-grade financial intelligence system for IPO, M&A, and Sovereign Capital Markets research.**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)]()
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-f97316?style=for-the-badge)](CONTRIBUTING.md)
[![Data](https://img.shields.io/badge/Live_Data-Yahoo_Finance_%7C_World_Bank-0077B5?style=for-the-badge)]()

<br/>

> Built to mirror the analytical depth and output standards of **Goldman Sachs GIR**, **J.P. Morgan Country Risk**, **D.E. Shaw Capital Markets Research**, **Deutsche Bank Ratings Advisory**, and **PwC Deals Strategy**.

<br/>

[🚀 Quick Start](#-quick-start) · [📐 Architecture](#-architecture) · [🔬 Models](#-proprietary-analytical-models) · [📦 Outputs](#-output-formats) · [🗂️ Data Sources](#%EF%B8%8F-data-sources) · [🤝 Contributing](#-contributing) · [🗺️ Roadmap](#%EF%B8%8F-roadmap)

</div>

---

## ✦ What This Platform Does

This system ingests live market data, runs six proprietary quantitative models, and produces three independent professional output formats — all in a single automated Python pipeline.

```
Live APIs ──▶ Raw Data ──▶ Analytical Models ──▶ Dashboards │ Excel │ PDFs
```

| Vertical | Coverage | Key Output |
|----------|----------|------------|
| 🏛️ **IPO Markets** | 25 IPOs across 7 countries | Event study, abnormal returns, money-left-on-table |
| 🤝 **M&A** | 20 deals · $483.5B total value | Deal screening model, 20 case studies |
| 🌍 **Sovereign Bonds** | 31 issuances · 18 countries · $325.8B | Risk index (0–100), 60 stress test scenarios |
| 📈 **Macro / Cross-Asset** | 501 trading days · 9 FX pairs · VIX, Gold, WTI | Regime detection, yield curve decomposition |

---

## 📐 Architecture

```
capital-markets-intelligence/
│
├── 📁 data/
│   ├── raw/                      # Live API + curated datasets
│   │   ├── ipo_data_raw.csv              # 25 IPOs, 7 countries
│   │   ├── mna_data_raw.csv              # 20 M&A deals ($483.5B)
│   │   ├── sovereign_issuance_raw.csv    # 31 issuances, 18 countries
│   │   ├── yield_curve_history.csv       # Treasury yields 3M/5Y/10Y/30Y (501 days)
│   │   ├── market_rates.csv              # S&P500, VIX, Gold, WTI Oil
│   │   ├── fx_rates.csv                  # 9 EM/DM FX pairs + 30d rolling vol
│   │   ├── worldbank_indicators.csv      # 15 indicators, 20 countries
│   │   └── country_macro_panel.csv       # Country-year panel dataset
│   └── processed/                # Model output CSVs
│       ├── yield_curve_analysis.csv
│       ├── sovereign_risk_index.csv
│       ├── regime_indicators.csv
│       ├── deal_screening_model.csv
│       ├── ipo_event_study.csv
│       ├── stress_test_results.csv
│       └── case_studies.csv
│
├── 📁 scripts/                   # 13-script numbered pipeline
│   ├── 01_fetch_ipo_data.py
│   ├── 02_fetch_mna_data.py
│   ├── 03_stress_test_model.py
│   ├── 04_case_study_builder.py
│   ├── 05_fetch_sovereign_data.py
│   ├── 06_generate_visualizations.py
│   ├── 07_generate_memos.py
│   ├── 08_fetch_fred_data.py
│   ├── 09_fetch_worldbank_data.py
│   ├── 10_advanced_analysis.py
│   ├── 11_generate_plotly_dashboards.py
│   ├── 12_generate_excel_reports.py
│   └── 13_generate_pdf_reports.py
│
├── 📁 analysis/                  # Jupyter Notebooks
│   ├── market_sentiment.ipynb        # GS-GIR style cross-asset analysis
│   ├── country_risk_model.ipynb      # JPM country risk stress model
│   └── deal_case_studies.ipynb       # PwC/DB M&A deal analysis
│
├── 📁 docs/                      # Guides and cookbooks
├── 📄 CONTRIBUTING.md            # How to contribute
├── 📄 ROADMAP.md                 # What we're building next
└── 📁 output/
    ├── dashboards/               # 5 interactive Plotly HTML dashboards
    ├── excel/                    # 4 formatted Excel workbooks
    ├── pdf/                      # 4 professional PDF research reports
    └── memos/                    # 4 firm-style text research memos
```

---

## 🔬 Proprietary Analytical Models

### 1 · Yield Curve Decomposition
Extracts **level, slope, and curvature** components from the US Treasury term structure (3M–30Y). Computes rolling z-scores, classifies the curve regime (Inverted / Flat / Normal / Steep), and generates slope momentum signals.

### 2 · Sovereign Risk Index *(0–100 composite score)*
Aggregates **11 World Bank indicators** across four dimensions — fiscal health, external vulnerability, growth stability, and reserves adequacy — into a z-score normalized composite. Risk tier classifications: **Low / Moderate / Elevated / High / Critical**.

### 3 · Cross-Asset Regime Detection
A **6-signal framework** reading VIX level, S&P 500 trend & momentum, gold safe-haven flow, yield curve slope, and EM FX volatility to produce daily **Risk-On / Neutral / Risk-Off** regime calls with signal decomposition.

### 4 · M&A Deal Screening Model
Point-biserial correlation analysis of **9 deal features** (size, cross-border flag, sector, premium, deal type, etc.) against completion outcome. Produces a ranked feature importance table and completion probability signals.

### 5 · IPO Event Study
Measures **abnormal returns** relative to the S&P 500 benchmark across pre-IPO, listing day, +5d, +30d, and +90d windows. Quantifies money-left-on-table and classifies pricing as Underpriced / Fairly Priced / Overpriced.

### 6 · Sovereign Stress Testing
Runs **12 sovereigns × 5 macro scenarios** for 60 total stress paths: Base Case, Fed Hawkish Surprise, Global Recession, EM Currency Crisis, and Oil Price Shock. Outputs risk score deltas and tier migration analysis.

---

## 📦 Output Formats

### 🖥️ Interactive Plotly Dashboards *(HTML)*
| Dashboard | Description |
|-----------|-------------|
| `yield_curve_dashboard.html` | Term structure animation + regime timeline |
| `sovereign_risk_dashboard.html` | Risk heatmap + macro indicator drill-down |
| `market_regime_dashboard.html` | Signal decomposition + regime history |
| `ipo_analysis_dashboard.html` | Performance scatter + event study metrics |
| `mna_screening_dashboard.html` | Screening matrix + feature importance waterfall |

### 📊 Excel Workbooks *(openpyxl, conditional formatting)*
| Workbook | Sheets |
|----------|--------|
| `ipo_analysis_workbook.xlsx` | Database, Event Study, Summary Stats, Underwriter League Table |
| `sovereign_risk_workbook.xlsx` | Risk Index, Macro Panel, Stress Tests, Issuance Tracker |
| `mna_analysis_workbook.xlsx` | Deal Database, Case Studies, Screening Model |
| `capital_markets_master.xlsx` | Executive overview across all verticals |

### 📄 PDF Research Reports *(fpdf, firm-styled)*
| Report | Style |
|--------|-------|
| `gs_gir_capital_markets_snapshot.pdf` | Goldman Sachs GIR — Weekly capital markets brief |
| `jpm_sovereign_risk_report.pdf` | J.P. Morgan — Sovereign risk & issuance model |
| `de_shaw_ipo_dashboard.pdf` | D.E. Shaw — Quantitative IPO performance dashboard |
| `pwc_db_mna_case_studies.pdf` | PwC / Deutsche Bank — M&A strategic case studies |

### 📝 Research Memos *(text)*
Firm-voice narrative research memos with executive summaries and key risk flags for GS, D.E. Shaw, JPM, and PwC/DB.

---

## 🗂️ Data Sources

| Source | API Key | What It Provides |
|--------|---------|-----------------|
| [Yahoo Finance (yfinance)](https://pypi.org/project/yfinance/) | ❌ Not required | Treasury yields, S&P 500, VIX, Gold, WTI Oil, 9 FX pairs |
| [World Bank Open Data](https://data.worldbank.org/) | ❌ Not required | 15 macro indicators across 20 countries |
| [SEC EDGAR](https://www.sec.gov/edgar/) | ❌ Not required | IPO filings (with curated dataset fallback) |
| Curated Databases | N/A | M&A deals, sovereign issuance (sourced from public filings) |

> **Zero API keys required.** Clone, install, and run.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/DogInfantry/capital-markets-intelligence.git
cd capital-markets-intelligence

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt

# 3. Phase 1 — Data Collection
python scripts/01_fetch_ipo_data.py
python scripts/02_fetch_mna_data.py
python scripts/03_stress_test_model.py
python scripts/04_case_study_builder.py
python scripts/05_fetch_sovereign_data.py

# 4. Phase 2 — Live API Data
python scripts/08_fetch_fred_data.py
python scripts/09_fetch_worldbank_data.py

# 5. Phase 3 — Advanced Analysis
python scripts/10_advanced_analysis.py

# 6. Phase 4 — Generate All Outputs
python scripts/06_generate_visualizations.py
python scripts/07_generate_memos.py
python scripts/11_generate_plotly_dashboards.py
python scripts/12_generate_excel_reports.py
python scripts/13_generate_pdf_reports.py
```

---

## 🛠️ Technology Stack

```
Data          │ pandas · numpy · requests · yfinance · World Bank API
Analysis      │ scipy (stats) · numpy (linear algebra) · Jupyter
Dashboards    │ Plotly (graph_objects · make_subplots)
Excel Reports │ openpyxl (conditional formatting · styled workbooks)
PDF Reports   │ fpdf (professional formatted output)
Visualization │ matplotlib (Agg backend) · seaborn
Runtime       │ Python 3.13
```

---

## 🎯 Target Applications

This platform is architected to demonstrate capabilities directly relevant to:

| Firm | Division | Relevant Module |
|------|----------|-----------------|
| **Goldman Sachs** | GIR, Executive Office | Cross-asset regime detection, weekly capital markets snapshot |
| **D.E. Shaw** | Capital Markets Research | Quantitative IPO event study, statistical feature analysis |
| **J.P. Morgan** | Country Risk | Sovereign risk index (0–100), stress testing model |
| **Deutsche Bank** | Ratings Advisory | Sovereign issuance analytics, macro indicator panel |
| **PwC** | Deals Strategy | M&A case studies, deal screening model |

---

## 🤝 Contributing

**Contributions are welcome!** This platform is actively evolving — we're looking for collaborators with backgrounds in quant finance, Python engineering, data visualization, and financial research.

### Good places to start

- Browse issues labeled [`good first issue`](../../issues?q=is%3Aopen+label%3A%22good+first+issue%22) — well-scoped tasks with clear acceptance criteria
- Browse issues labeled [`help wanted`](../../issues?q=is%3Aopen+label%3A%22help+wanted%22) — higher-impact work the maintainer wants community help on
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for dev setup, coding style, and PR process
- See [ROADMAP.md](ROADMAP.md) for the full v1.1 → v1.2 → v1.3 plan

### We're especially looking for help with

- 📐 **Quant finance:** regime-switching models, advanced event-study statistics, factor models
- 🐍 **Python engineering:** packaging, CLI, CI/CD, type safety, testing
- 📊 **Visualization:** Plotly dashboard polish, interactive filters, chart standardization
- 📝 **Documentation:** worked-example notebooks, scenario cookbook, model explainers

> **Comment on an issue to claim it before starting work.**

---

## 🗺️ Roadmap

| Milestone | Focus | Status |
|-----------|-------|--------|
| **v1.1 — Engineering Hardening** | CLI, packaging, config, tests, CI, logging, Docker | 🔄 In Progress |
| **v1.2 — Analytics Upgrades** | IPO event study, M&A classifier, sovereign decomposition, regime Markov | 📋 Planned |
| **v1.3 — UX, Outputs & Docs** | Dashboard filters, PDF/Excel polish, notebooks, cookbook | 📋 Planned |
| **v2.0 — Advanced Research Platform** | Dynamic term structure, factor models, LLM memos, web UI | 💡 Future |

See [ROADMAP.md](ROADMAP.md) for full details and open issues per milestone.

---

## 📜 License

Distributed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

**Created:** March 2026 &nbsp;·&nbsp; **Status:** 🔄 Active Development &nbsp;·&nbsp; **Python:** 3.13

*Built to institutional research standards. No API keys required. Contributions welcome.*

</div>
