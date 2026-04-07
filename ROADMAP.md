# Roadmap — Capital Markets Intelligence Platform

> **Current status:** v1.0 complete — 6 proprietary models, 5 dashboards, 4 Excel workbooks, 4 PDFs, 4 research memos. Zero API keys required.

This roadmap outlines what we're building next. Contributions on any milestone are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## v1.1 — Engineering Hardening *(in progress)*

Goal: make the platform production-grade and contributor-friendly.

- [ ] Turn pipeline into a Python package with CLI entrypoint (`cmi run data|analysis|outputs|all`)
- [ ] Add YAML/JSON configuration for tickers, countries, event windows, and scenarios
- [ ] Refactor duplicated data-loading logic into shared utility module (`cmi/data_utils.py`)
- [ ] Add structured logging and graceful error handling across the pipeline
- [ ] Add pytest test suite with golden-data tests for core models
- [ ] Add GitHub Actions CI (tests + lint on every PR)
- [ ] Add type hints and mypy checks for core modules
- [ ] Add Dockerfile and optional VS Code devcontainer
- [ ] Add a `cmi run happy-path` command for fast end-to-end validation

---

## v1.2 — Analytics Upgrades *(planned)*

Goal: deepen the quantitative models across all four verticals.

### IPO Event Study
- [ ] Add configurable estimation windows and additional statistical tests (rank tests, parametric vs non-parametric)
- [ ] Add market-adjusted vs market-model comparison
- [ ] Cross-check abnormal returns against an external event-study library
- [ ] Add multi-event aggregation: CARs by sector, country, underwriter (with boxplots)

### M&A Deal Screening
- [ ] Move from simple correlations to logistic regression / tree-based classification model with held-out validation
- [ ] Add sector-level M&A summaries (median premium, completion rate, typical deal size)
- [ ] Add time-to-completion analysis as a function of deal characteristics

### Sovereign Risk & Macro
- [ ] Decompose sovereign risk index contributions by indicator (tornado charts per country)
- [ ] Add rating-style mapping (IG/BB/B buckets) and watch-list flag for downgrade risk
- [ ] Add commodity-linked stress scenarios (oil exporter vs importer differential)

### Cross-Asset Regime Detection
- [ ] Add Markov transition probabilities and regime persistence stats (half-life, expected duration)
- [ ] Add a toy strategy backtest using regime calls (with appropriate disclaimers)

---

## v1.3 — UX, Outputs & Documentation *(planned)*

Goal: make the platform feel like a real institutional research product.

### Dashboards
- [ ] Add a global navigation "home page" HTML linking all dashboards, reports, and workbooks
- [ ] Add interactive filters (country, sector, date range) to Plotly dashboards
- [ ] Standardize chart style, color palette, and fonts across all dashboards

### Excel & PDF Reports
- [ ] Add TOC, numbered sections, and figure captions to PDF reports
- [ ] Add hyperlinks in Excel workbooks (tickers → Yahoo Finance, countries → World Bank)
- [ ] Generate a "Data Inventory" appendix (source, coverage period, last updated) in both Excel and PDF

### Documentation
- [ ] Add a "Scenario Cookbook" in `docs/` (how to add a new IPO, country, or scenario)
- [ ] Add a full worked-example Jupyter notebook for each vertical (IPO, M&A, sovereign, macro)

---

## v2.0 — Advanced Research Platform *(future)*

Longer-horizon ideas — contributions and proposals welcome:

- Dynamic term structure models (Nelson-Siegel-Svensson)
- Multi-factor risk models for cross-asset portfolios
- Integration with open-source trading agents (FinRL, FinRobot) for research simulation
- Optional LLM-powered memo generation (narrative summaries from structured model output)
- Real-time data refresh mode (scheduled pipeline runs)
- Web-based UI for non-technical users to configure and run analyses

---

## Contributing

We are actively looking for help with:

- **Quant finance:** regime-switching models, factor models, advanced event-study statistics
- **Python engineering:** packaging, CI, type safety, testing
- **Visualization:** Plotly dashboard polish, cross-asset chart design
- **Documentation:** notebooks, cookbooks, written explanations of models

See [CONTRIBUTING.md](CONTRIBUTING.md) and browse [open issues](../../issues) — especially those labeled `good first issue` or `help wanted`.
