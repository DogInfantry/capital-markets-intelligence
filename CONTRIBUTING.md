# Contributing to Capital Markets Intelligence Platform

Thank you for your interest in contributing! This project is open to contributions from anyone with an interest in quantitative finance, data engineering, or Python development.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Project Structure](#project-structure)
- [Coding Style](#coding-style)
- [How to Propose Changes](#how-to-propose-changes)
- [Good First Issues](#good-first-issues)
- [Need Help?](#need-help)

---

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/capital-markets-intelligence.git
cd capital-markets-intelligence
```

### 2. Set Up Environment

Requires **Python 3.10+** (developed on 3.13).

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Run a Minimal Pipeline (Quick Validation)

You don't need to run all 13 scripts to test your changes. A fast subset:

```bash
python scripts/01_fetch_ipo_data.py
python scripts/05_fetch_sovereign_data.py
python scripts/10_advanced_analysis.py
python scripts/11_generate_plotly_dashboards.py
```

### 4. Verify Outputs

After running, check that:
- `data/processed/` contains updated CSVs
- `output/dashboards/` contains `.html` files you can open in a browser

---

## Development Workflow

1. **Find or open an issue** — check the [Issues](https://github.com/DogInfantry/capital-markets-intelligence/issues) tab. Look for `good first issue` or `help wanted` labels.
2. **Comment on the issue** to say you're working on it (avoids duplicate work).
3. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```
4. **Make your changes**, commit with clear messages (see below).
5. **Open a Pull Request** against `main` using the PR template.
6. **Respond to review** — we aim to review PRs within 48–72 hours.

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add logistic regression to M&A deal screening
fix: handle missing yield curve data for short-dated tenors
docs: add Scenario Cookbook for IPO event study
refactor: extract CSV loading helpers to utils module
test: add golden-data test for sovereign risk index
chore: update requirements.txt with yfinance and plotly
```

---

## Project Structure

```
capital-markets-intelligence/
├── scripts/          # Numbered 01–13 pipeline (data → analysis → outputs)
├── analysis/         # Jupyter notebooks for exploratory work
├── data/
│   ├── raw/          # Live API + curated source data
│   ├── processed/    # Model output CSVs (generated, not tracked)
│   └── cache/        # API response cache (not tracked)
├── output/
│   ├── dashboards/   # Plotly HTML files
│   ├── excel/        # openpyxl workbooks
│   ├── pdf/          # fpdf reports
│   └── memos/        # Text research memos
├── docs/             # Extended documentation
└── tests/            # (Planned) pytest test suite
```

**Key principle:** Scripts are numbered in execution order. Each script reads from `data/` and writes back to `data/processed/` or `output/`. Avoid cross-script imports — each script should be independently runnable.

---

## Coding Style

- **Formatter:** `black` (line length 100)
- **Linter:** `ruff` or `flake8`
- **Docstrings:** Google-style
- **Type hints:** Encouraged for new functions, required for any new shared utilities
- **No hard-coded paths:** Use `pathlib.Path(__file__).parent` for relative paths
- **No silent failures:** Raise meaningful exceptions or print a clear warning when data is unavailable

To auto-format before committing:
```bash
pip install black ruff
black scripts/ analysis/
ruff check scripts/ analysis/
```

---

## How to Propose Changes

### Bug Reports
Open an issue using the **Bug Report** template. Include:
- Steps to reproduce
- Expected vs actual behaviour
- Python version, OS, and dependency versions (`pip freeze`)
- Any relevant log output or tracebacks

### Feature Requests
Open an issue using the **Feature Request** template. Include:
- Why this improves the platform (which use case / vertical does it help?)
- What data sources it needs
- Whether it requires new dependencies

### Analytics / Model PRs
If your PR changes an analytical model (e.g., event study methodology, sovereign risk weights):
- Include a short write-up (in the PR body or a `docs/` file) explaining the methodology and its source
- Show sample output before and after
- Link to any academic papers or practitioner references used

---

## Good First Issues

Looking for somewhere to start? These are well-scoped entry points:

- 🏷️ Filter by [`good first issue`](https://github.com/DogInfantry/capital-markets-intelligence/issues?q=is%3Aopen+label%3A%22good+first+issue%22)
- 🏷️ Filter by [`help wanted`](https://github.com/DogInfantry/capital-markets-intelligence/issues?q=is%3Aopen+label%3A%22help+wanted%22)

Examples of good first contributions:
- Fix a typo or improve an explanation in the README
- Add a missing dependency to `requirements.txt`
- Add type hints to one script
- Write a pytest test for a single model function

---

## Need Help?

Open a [Discussion](https://github.com/DogInfantry/capital-markets-intelligence/discussions) or tag `@DogInfantry` in an issue comment. We're happy to help you get oriented.

---

*Built to institutional research standards — contributions held to the same bar.*
