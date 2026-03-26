# How to Use Claude Code With This Project

## What You Do Right Now (In Your Terminal)

### Step 1: Download the Project Scaffold

We've created the project skeleton. You need to **get it on your machine**:

```bash
# Option A: If we push to GitHub (best)
git clone https://github.com/YOUR_USERNAME/capital-markets-intelligence.git
cd capital-markets-intelligence

# Option B: If you copy files manually
# (Create folder, then add the files we created)
```

### Step 2: Open Claude Code in This Folder

```bash
cd capital-markets-intelligence
claude-code
```

Claude Code will start and you'll be in the project context.

### Step 3: Ask Claude to Help You with Tasks

Examples:

```
"Run the IPO data fetch script and show me the output"
```

```
"Add error handling to 01_fetch_ipo_data.py if there's a network timeout"
```

```
"Build a new script called 03_fetch_sovereign_data.py that fetches bond issuance data from IMF and World Bank"
```

```
"Debug this error: [paste error message]"
```

```
"Create a Jupyter notebook that analyzes the IPO data we just fetched"
```

---

## Git Workflow: How to Commit Your Work

### After Each Claude Code Session

1. **Check what changed**:
   ```bash
   git status
   ```

2. **Review the changes**:
   ```bash
   git diff scripts/01_fetch_ipo_data.py  # or whatever file changed
   ```

3. **Stage the files**:
   ```bash
   git add scripts/01_fetch_ipo_data.py
   # OR to add everything:
   git add -A
   ```

4. **Commit with a clear message**:
   ```bash
   git commit -m "Add retry logic and better error handling to IPO fetch script"
   ```

5. **Push to GitHub** (if you've linked it):
   ```bash
   git push origin main
   ```

---

## Example Workflow: Week 1

### Monday
```bash
# Start Claude Code session
claude-code

# In Claude:
# "Improve the 01_fetch_ipo_data.py script to handle rate limiting better"
# "Add logging to show progress"
# (Claude makes changes)

# Back in terminal:
git add scripts/01_fetch_ipo_data.py
git commit -m "Improve IPO scraper: add rate limiting and progress logging"
git push origin main
```

### Wednesday
```bash
claude-code

# In Claude:
# "Build 03_fetch_sovereign_data.py script that gets bond issuance data"
# (Claude writes the script)

# Back in terminal:
git add scripts/03_fetch_sovereign_data.py
git commit -m "Add sovereign bond issuance data fetcher (IMF, World Bank sources)"
git push origin main
```

### Friday
```bash
claude-code

# In Claude:
# "Create a Jupyter notebook to analyze all three datasets"
# (Claude creates analysis/market_sentiment.ipynb)

# Back in terminal:
python scripts/01_fetch_ipo_data.py  # Run the scripts
python scripts/02_fetch_mna_data.py
python scripts/03_fetch_sovereign_data.py

# Then commit the data
git add data/raw/
git commit -m "Add raw datasets: IPO, M&A, sovereign data (Week 1 collection)"
git push origin main
```

---

## Claude Code vs. Regular Claude Chat

| Task | Use Claude Code | Use Regular Chat |
|------|---|---|
| Write Python scripts | ✓ Yes | ✗ No |
| Debug code | ✓ Yes | ✓ Maybe (paste error) |
| Test code locally | ✓ Yes | ✗ No |
| Refactor scripts | ✓ Yes | ✗ No |
| Plan project structure | ✓ Better | ✓ OK |
| Write memos/analysis | ✗ No | ✓ Yes (use Opus) |
| Create PowerPoint | ✗ No | ✓ Yes |

---

## Common Claude Code Commands

```bash
# Show current directory
pwd

# List files
ls -la

# Run a Python script
python scripts/01_fetch_ipo_data.py

# Create a new file
touch scripts/04_my_new_script.py

# Check git status
git status

# See recent commits
git log --oneline
```

---

## Setting Up GitHub (Optional But Recommended)

If you want to push to GitHub for a professional portfolio:

1. Create repo on GitHub: `capital-markets-intelligence`
2. Link it locally:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/capital-markets-intelligence.git
   git branch -M main
   git push -u origin main
   ```
3. Now `git push` will automatically push to GitHub

---

## Sample Git Commit Messages (Good Practice)

✓ Good:
```
"Add sovereign debt issuance scraper with error handling"
"Refactor IPO data fetch to use requests.Session for efficiency"
"Create analysis notebook: market sentiment 30-day trends"
```

✗ Bad:
```
"Update script"
"Fix stuff"
"Working version"
```

---

## Your Next Steps

1. **Download the project** (clone from GitHub or copy files)
2. **Create Python virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   ```
3. **Open Claude Code**:
   ```bash
   claude-code
   ```
4. **Ask Claude to run the first script**:
   ```
   "Run scripts/01_fetch_ipo_data.py and show me the results"
   ```
5. **Commit your work**:
   ```bash
   git add -A
   git commit -m "Initial data collection: IPO dataset fetched"
   git push origin main
   ```

---

Good luck! You're building a production-grade financial research project. 🚀
