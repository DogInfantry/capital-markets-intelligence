# Capital Markets Intelligence Platform — Weeks 2-5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the full Capital Markets Intelligence Platform — from raw data through analysis, visualizations, stress testing, and polished application-ready memos targeting GS, D.E. Shaw, JPM, PwC/DB.

**Architecture:** Python scripts generate data and charts (matplotlib/seaborn) saved to `output/`. Analysis scripts in `scripts/` replace notebook-dependent workflows. Four polished research memos in `output/memos/` serve as portfolio deliverables. All outputs committed to GitHub.

**Tech Stack:** Python 3.13 (Anaconda), pandas, numpy, matplotlib, seaborn, scipy

**Python executable:** `/c/Users/Anklesh/anaconda3/python.exe`

---

## File Structure

### New files to create:
- `scripts/05_fetch_sovereign_data.py` — Sovereign bond issuance dataset builder
- `scripts/06_generate_visualizations.py` — All charts from the 3 notebooks as a single script
- `scripts/07_generate_memos.py` — All 4 application-ready memos as text files
- `output/memos/gs_gir_weekly_snapshot.txt` — GS-GIR research brief (generated)
- `output/memos/de_shaw_ipo_dashboard.txt` — D.E. Shaw IPO report (generated)
- `output/memos/jpm_sovereign_risk_model.txt` — JPM sovereign risk memo (generated)
- `output/memos/pwc_db_mna_case_studies.txt` — PwC/DB M&A case studies (generated)
- `LICENSE` — MIT license

### Files to modify:
- `.gitignore` — Allow data files and output to be committed
- `README.md` — Update status from "Week 1" to "Complete"

### Existing data files (already generated, need to be committed):
- `data/raw/ipo_data_raw.csv` — 25 IPOs
- `data/raw/mna_data_raw.csv` — 20 M&A deals
- `data/processed/stress_test_results.csv` — 60 stress test results
- `data/processed/case_studies.csv` — 20 case studies
- `output/case_study_summaries.txt` — Text summaries

---

### Task 1: Commit existing data files to GitHub

**Files:**
- Modify: `.gitignore` — remove data exclusion rules to allow sample data
- Stage: all `data/` and `output/` files

- [ ] **Step 1: Update .gitignore to allow sample data**

Remove the CSV/parquet exclusion lines for `data/` and `output/` so sample datasets are tracked. Keep the `.gitkeep` includes.

- [ ] **Step 2: Stage and commit data files**

```bash
git add .gitignore data/ output/
git commit -m "Add sample datasets: 25 IPOs, 20 M&A deals, 60 stress tests, 20 case studies"
```

- [ ] **Step 3: Push to GitHub**

```bash
git push origin main
```

---

### Task 2: Build sovereign bond issuance fetcher

**Files:**
- Create: `scripts/05_fetch_sovereign_data.py`

- [ ] **Step 1: Write sovereign data script**

Build a script that creates a sovereign bond issuance dataset with:
- 15+ countries with recent bond issuances
- Fields: country, iso, bond_type, maturity_years, coupon_pct, issue_size_usd_bn, issue_date, currency, rating, yield_at_issue_pct
- Mix of developed and emerging market issuers
- Save to `data/raw/sovereign_issuance_raw.csv`

- [ ] **Step 2: Run the script**

```bash
/c/Users/Anklesh/anaconda3/python.exe scripts/05_fetch_sovereign_data.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/05_fetch_sovereign_data.py data/raw/sovereign_issuance_raw.csv
git commit -m "Add sovereign bond issuance data fetcher (15+ countries)"
```

---

### Task 3: Generate all visualizations

**Files:**
- Create: `scripts/06_generate_visualizations.py`
- Output: `output/*.png` (6-8 charts)

- [ ] **Step 1: Write visualization script**

A single script that loads all datasets and generates these charts saved to `output/`:

1. `ipo_first_day_returns.png` — Bar chart of first-day returns by company
2. `ipo_total_returns.png` — Bar chart of total returns to date
3. `ipo_by_sector.png` — Deal size by sector (horizontal bar)
4. `mna_by_sector.png` — M&A deal value by sector (horizontal bar)
5. `mna_deal_status.png` — Deal status breakdown (bar)
6. `risk_heatmap.png` — Sovereign risk scores heatmap (scenario x country)
7. `yield_impact.png` — 2x2 subplot of yield changes under each stress scenario
8. `vulnerability_ranking.png` — Average risk score ranking across scenarios
9. `deal_size_distribution.png` — Case study deal sizes
10. `research_relevance.png` — Research relevance scores by deal

Use `matplotlib.use('Agg')` backend (no display needed). Professional styling with seaborn whitegrid theme.

- [ ] **Step 2: Run the script**

```bash
/c/Users/Anklesh/anaconda3/python.exe scripts/06_generate_visualizations.py
```

Verify: 10 PNG files in `output/`

- [ ] **Step 3: Commit**

```bash
git add scripts/06_generate_visualizations.py output/*.png
git commit -m "Add visualization generator: 10 charts covering IPO, M&A, sovereign risk"
```

---

### Task 4: Generate application-ready memos

**Files:**
- Create: `scripts/07_generate_memos.py`
- Create: `output/memos/` directory
- Output: 4 memo text files

- [ ] **Step 1: Write memo generator script**

A script that loads all datasets and generates 4 polished memos:

**Memo 1: GS-GIR Weekly Capital Markets Snapshot**
- Executive summary of capital markets activity
- IPO market review (pipeline, pricing, first-day performance)
- M&A deal flow (volume, sectors, regulatory landscape)
- Market outlook and risk factors
- Target: Goldman Sachs Global Investment Research style

**Memo 2: D.E. Shaw IPO Performance Dashboard**
- Quantitative IPO analysis (returns distribution, sector breakdown)
- Statistical summary (mean, median, std dev of returns)
- Top/bottom performers
- Underwriter league table
- Target: D.E. Shaw quantitative research style

**Memo 3: JPM Sovereign Risk & Capital Issuance Model**
- Sovereign baseline overview (ratings, yields, debt/GDP)
- Stress test results summary
- Vulnerability rankings
- Scenario analysis narratives
- Policy implications
- Target: JPMorgan Country Risk style

**Memo 4: PwC/DB M&A Strategic Rationale Case Studies**
- Deal overview matrix
- Top 5 deals deep-dive (rationale, risks, value drivers)
- Cross-border and regulatory themes
- Sector trends
- Target: PwC Deals / Deutsche Bank Strategy style

- [ ] **Step 2: Run the script**

```bash
/c/Users/Anklesh/anaconda3/python.exe scripts/07_generate_memos.py
```

Verify: 4 files in `output/memos/`

- [ ] **Step 3: Commit**

```bash
git add scripts/07_generate_memos.py output/memos/
git commit -m "Add 4 application-ready research memos (GS, D.E. Shaw, JPM, PwC/DB)"
```

---

### Task 5: Polish and package

**Files:**
- Create: `LICENSE`
- Modify: `README.md`

- [ ] **Step 1: Add MIT LICENSE file**

- [ ] **Step 2: Update README.md**

Update the status from "In progress (Week 1)" to "Complete". Add a section listing the output deliverables and charts.

- [ ] **Step 3: Final commit and push**

```bash
git add LICENSE README.md
git commit -m "Add MIT license, update README to reflect completed project"
git push origin main
```

---

## Execution Order

Tasks 1 → 2 → 3 → 4 → 5 (sequential — each builds on previous data)
