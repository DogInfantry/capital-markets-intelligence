# Quick Start Guide

## On Your Local Machine

### Step 1: Clone the Project
```bash
cd ~/projects  # or wherever you keep code
git clone <your-repo-url> capital-markets-intelligence
cd capital-markets-intelligence
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run Week 1 Scripts

```bash
# Fetch IPO data
python scripts/01_fetch_ipo_data.py

# Fetch M&A data
python scripts/02_fetch_mna_data.py

# Check your data
ls -la data/raw/
```

### Step 4: Use Claude Code for Development

When you want Claude to help you build or debug:

```bash
# Start Claude Code in this folder
claude-code

# Then ask Claude:
# "Help me debug the IPO fetch script"
# "Add error handling to the M&A script"
# "Build a stress testing module"
```

### Step 5: Commit Your Work to Git

```bash
# After each successful script run
git add scripts/01_fetch_ipo_data.py
git commit -m "Add IPO data scraper with SEC EDGAR + Renaissance Capital integration"

git add data/raw/ipo_data_raw.csv
git commit -m "Add sample IPO dataset (50 records)"

# Push to GitHub
git push origin main
```

## Week 1 Checklist

- [ ] Clone repo locally
- [ ] Set up Python venv
- [ ] Run `pip install -r requirements.txt`
- [ ] Execute `scripts/01_fetch_ipo_data.py`
- [ ] Verify `data/raw/ipo_data_raw.csv` exists
- [ ] Execute `scripts/02_fetch_mna_data.py`
- [ ] Verify `data/raw/mna_data_raw.csv` exists
- [ ] Run `git add` + `git commit` for each major milestone
- [ ] Push to GitHub

## Week 2: Analysis

Once data is gathered:

```bash
# Start Jupyter
jupyter notebook

# Open: analysis/market_sentiment.ipynb
# Follow the template to:
# 1. Load IPO + M&A data
# 2. Plot trends
# 3. Calculate metrics
# 4. Generate visualizations
```

## Week 3-4: Stress Testing & Memos

```bash
# Run stress test model
python scripts/03_stress_test_model.py

# Generate case studies
python scripts/04_case_study_builder.py

# Export outputs
ls -la output/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas
# OR re-run: pip install -r requirements.txt
```

### "SEC EDGAR API timeout"
The SEC API sometimes has rate limits. The scripts have built-in delays.
If it times out, just run it again in 5 minutes.

### "No data in data/raw/"
Make sure you ran the scripts successfully. Check:
```bash
python scripts/01_fetch_ipo_data.py  # Should print ✓ checkmarks
```

## Getting Help

1. **Claude Code**: Run `claude-code` in the project folder
2. **Debug a script**: `claude-code` + "Debug this error: [error message]"
3. **Add a feature**: `claude-code` + "Add X to the Y script"

---

## Next Steps

1. **Run Week 1 scripts** (this week)
2. **Build Week 2 analysis notebooks** (next week)
3. **Week 3-4**: Stress testing + case studies
4. **Week 5**: Export → Opus for memo writing

Good luck! 🚀
