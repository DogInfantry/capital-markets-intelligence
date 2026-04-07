# 🗺️ Roadmap — Capital Markets Intelligence Platform

This document tracks the planned evolution of the platform. It is a living document — items move, priorities shift, and contributions are welcome on any item.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to pick up a roadmap item.

---

## ✅ v1.0 — Complete (March 2026)

- 13-script numbered pipeline (data → analysis → outputs)
- 6 proprietary analytical models (yield curve, sovereign risk, regime detection, M&A screening, IPO event study, stress testing)
- 5 interactive Plotly HTML dashboards
- 4 formatted Excel workbooks
- 4 firm-styled PDF research reports
- 4 research memos (GS, D.E. Shaw, JPM, PwC/DB voice)
- Live data via Yahoo Finance and World Bank (zero API keys required)

---

## 🔧 v1.1 — Engineering Hardening *(In Progress)*

> Focus: make the repo contributor-friendly, reproducible, and testable.

### Packaging & Infrastructure
- [ ] CLI entrypoint (`cmi run`) using `typer` or `argparse` — replaces manual script execution
- [ ] YAML/JSON config system for parameters (tickers, windows, country lists, scenario shocks)
- [ ] Centralized logging and structured error handling across all scripts
- [ ] Dockerfile + devcontainer for reproducible environments
- [ ] Fix `requirements.txt` — add missing `yfinance`, `plotly`, `fpdf2`

### Testing & CI
- [ ] `pytest` test suite with golden-data tests for all 6 models
- [ ] GitHub Actions CI: lint + test on every PR
- [ ] Type hints + mypy for core analytical functions

### Developer Ergonomics
- [ ] Shared utility module (`cmi/utils.py`) for CSV I/O, cache handling, date parsing
- [ ] Single orchestrator script (`scripts/run_all.py`) with dependency ordering
- [ ] Add `Makefile` targets: `make data`, `make analysis`, `make reports`, `make all`

---

## 📊 v1.2 — Analytics Depth *(Planned)*

> Focus: deepen each vertical's analytical capability.

### IPO Event Study
- [ ] Support multiple benchmark models (market-adjusted, market-model, Fama-French)
- [ ] Configurable estimation window and event window lengths
- [ ] Parametric and non-parametric significance tests (t-test, rank test, sign test)
- [ ] Multi-event aggregation: CARs by sector, country, underwriter, market cap tier
- [ ] Expand to 50+ IPOs across more geographies (India, Southeast Asia)

### M&A Deal Screening
- [ ] Replace correlation-only approach with logistic regression + gradient-boosted classifier
- [ ] Cross-validation and held-out test set for completion probability model
- [ ] Sector-level M&A summary stats (median premium, completion rate, time-to-close)
- [ ] Time-to-completion survival analysis (Kaplan-Meier)

### Sovereign Risk & Stress Testing
- [ ] Decomposition charts: which World Bank indicators drive each country's risk score
- [ ] Rating-style watch-list flags (mapping risk bands to IG/HY buckets)
- [ ] Commodity-linked scenarios: differentiate oil exporters vs importers under price shock
- [ ] Add ESG/climate risk dimension to the sovereign composite index

### Cross-Asset Regime Detection
- [ ] Markov transition matrix: regime persistence and half-life estimation
- [ ] Toy backtesting of regime-conditional allocation strategy (illustrative, with disclaimers)
- [ ] Add crypto/digital asset regime signals as an optional module

---

## 🎨 v1.3 — UX & Output Polish *(Planned)*

> Focus: make outputs feel like institutional research products.

### Dashboards
- [ ] Landing page HTML that links to all dashboards, reports, and workbooks
- [ ] Interactive filters (country, sector, date range, rating tier) in Plotly dashboards
- [ ] Unified color palette and font spec across all 5 dashboards
- [ ] Optional: deploy dashboards to GitHub Pages (static HTML, no backend needed)

### Excel & PDF
- [ ] Table of contents and cross-references in all PDF reports
- [ ] Hyperlinks in Excel: tickers → Yahoo Finance, countries → World Bank pages
- [ ] Auto-generated "Data Inventory" appendix (source, coverage, last updated)
- [ ] Scheduled refresh: GitHub Actions workflow to regenerate outputs weekly

### Documentation
- [ ] Scenario Cookbook in `docs/`: recipes for adding a new IPO, country, or scenario
- [ ] Full worked-example notebooks for each vertical (IPO, M&A, Sovereign)
- [ ] Architecture decision records (ADRs) for key model choices

---

## 🚀 v2.0 — Platform Expansion *(Vision)*

> Focus: expand scope into adjacent capital-markets verticals.

- [ ] **Credit markets module** — CDS spreads, IG/HY spread analysis, default probability scoring
- [ ] **Equity factor model** — Fama-French 3/5-factor decomposition, sector rotation signals
- [ ] **LBO screening model** — entry/exit multiple analysis, leverage capacity, returns scenarios
- [ ] **Rates & inflation module** — breakeven inflation, real yield decomposition, TIPS analysis
- [ ] **NLP sentiment layer** — news sentiment scoring for M&A rumours and sovereign events (open models only, no API keys)
- [ ] **Interactive web app** — Streamlit or Dash front-end wrapping the existing models

---

## 🤝 Want to help?

Pick any item marked `[ ]` above, open or find the corresponding issue, and submit a PR.
See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

*Maintainer: [@DogInfantry](https://github.com/DogInfantry)*
