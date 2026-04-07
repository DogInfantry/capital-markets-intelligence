# Contributing to Capital Markets Intelligence Platform

Thank you for your interest in contributing! This platform is built to mirror institutional research standards — contributions that raise analytical depth, code quality, or usability are all welcome.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Running the Pipeline](#running-the-pipeline)
4. [How to Contribute](#how-to-contribute)
5. [Coding Style](#coding-style)
6. [Submitting a PR](#submitting-a-pr)
7. [Issue Labels](#issue-labels)

---

## Getting Started

1. **Fork** the repository and clone your fork locally.
2. Browse [open issues](../../issues) — look for `good first issue` or `help wanted` labels.
3. Comment on an issue to claim it before starting work.

---

## Development Setup

**Requirements:** Python 3.13+

```bash
# Clone your fork
git clone https://github.com/<your-username>/capital-markets-intelligence.git
cd capital-markets-intelligence

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Pipeline

**Quick validation** (minimal run — recommended for contributors):
```bash
python scripts/01_fetch_ipo_data.py
python scripts/05_fetch_sovereign_data.py
python scripts/10_advanced_analysis.py
python scripts/11_generate_plotly_dashboards.py
```

**Full pipeline:**
```bash
# Phase 1 — Data Collection
python scripts/01_fetch_ipo_data.py
python scripts/02_fetch_mna_data.py
python scripts/03_stress_test_model.py
python scripts/04_case_study_builder.py
python scripts/05_fetch_sovereign_data.py

# Phase 2 — Live API Data
python scripts/08_fetch_fred_data.py
python scripts/09_fetch_worldbank_data.py

# Phase 3 — Advanced Analysis
python scripts/10_advanced_analysis.py

# Phase 4 — Outputs
python scripts/06_generate_visualizations.py
python scripts/07_generate_memos.py
python scripts/11_generate_plotly_dashboards.py
python scripts/12_generate_excel_reports.py
python scripts/13_generate_pdf_reports.py
```

Outputs appear in `output/` (dashboards, Excel, PDFs, memos).

---

## How to Contribute

1. Pick an issue or open a new one describing your idea.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes (keep PRs focused — one feature or fix per PR).
4. Run the quick validation pipeline to confirm nothing is broken.
5. Commit with a clear message: `feat: add sector-level M&A summaries`
6. Push and open a Pull Request against `main`.

---

## Coding Style

- **Formatter:** `black` (line length 100)
- **Linter:** `ruff` or `flake8`
- **Docstrings:** NumPy or Google style
- **Paths:** use `pathlib.Path`, not raw string concatenation
- **Logging:** use Python `logging` module, not `print()`
- **Type hints:** encouraged for all new functions

To format before committing:
```bash
pip install black ruff
black scripts/ analysis/
ruff check scripts/ analysis/
```

---

## Submitting a PR

Please fill in the PR template when opening a PR. Key points:

- What changed and why.
- How you tested it (e.g., "ran quick validation, checked Excel output").
- Screenshots or sample output if the change touches dashboards/reports.

---

## Issue Labels

| Label | Meaning |
|-------|---------|
| `good first issue` | Small, well-scoped — great for new contributors |
| `help wanted` | Higher-impact work the maintainer wants community help on |
| `analytics` | Changes to quantitative models or analysis logic |
| `data` | Changes to data fetching, cleaning, or schemas |
| `infra` | Packaging, CI, config, testing, logging |
| `ux` | Dashboards, Excel/PDF polish, visual output |
| `docs` | Documentation, notebooks, cookbooks |
| `IPO` | IPO event study module |
| `M&A` | M&A deal screening module |
| `sovereign` | Sovereign risk index and stress testing |
| `macro` | Cross-asset regime detection and yield curve |

---

*Built to institutional research standards. Contributions held to the same bar.*
