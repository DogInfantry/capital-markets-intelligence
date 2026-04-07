# 📖 Scenario Cookbook

Practical recipes for common extension tasks. Each recipe walks through exactly which files to edit and what to change.

---

## Recipe 1: Add a New IPO to the Event Study

**File:** `data/raw/ipo_data_raw.csv`

Add a row with the following columns:

| Column | Description | Example |
|--------|-------------|----------|
| `company` | Company name | `Stripe Inc` |
| `ticker` | Yahoo Finance ticker | `STRP` |
| `ipo_date` | ISO date | `2025-03-15` |
| `offer_price` | USD offer price | `32.00` |
| `first_day_close` | Closing price on IPO day | `38.50` |
| `shares_offered_m` | Shares offered (millions) | `45.0` |
| `sector` | Sector | `Technology` |
| `country` | Country of listing | `USA` |
| `underwriter` | Lead underwriter | `Goldman Sachs` |
| `exchange` | Exchange | `NASDAQ` |

Then re-run:
```bash
python scripts/01_fetch_ipo_data.py
python scripts/10_advanced_analysis.py
python scripts/11_generate_plotly_dashboards.py
python scripts/12_generate_excel_reports.py
python scripts/13_generate_pdf_reports.py
```

---

## Recipe 2: Add a New Country to Sovereign Risk Coverage

**File:** `scripts/05_fetch_sovereign_data.py`

1. Find the `SOVEREIGN_COUNTRIES` list near the top of the script.
2. Add the ISO2 country code (e.g., `"KE"` for Kenya).
3. Add issuance data to `data/raw/sovereign_issuance_raw.csv` with columns:
   `country`, `country_code`, `issuance_date`, `maturity_years`, `amount_bn_usd`, `coupon_pct`, `currency`, `type`.

Then re-run:
```bash
python scripts/05_fetch_sovereign_data.py
python scripts/09_fetch_worldbank_data.py
python scripts/10_advanced_analysis.py
```

---

## Recipe 3: Change the IPO Event Window

**File:** `scripts/10_advanced_analysis.py`

Search for `EVENT_WINDOWS` (or the dictionary that defines `+5d`, `+30d`, `+90d` windows). Change the values to your desired horizon (e.g., add `+180d`).

Make sure `yfinance` has enough history for the new window. Re-run:
```bash
python scripts/10_advanced_analysis.py
python scripts/11_generate_plotly_dashboards.py
```

---

## Recipe 4: Add a New Macro Stress Scenario

**File:** `scripts/03_stress_test_model.py`

1. Find the `SCENARIOS` dict that defines Base Case, Fed Hawkish Surprise, etc.
2. Add a new entry with your scenario name and shock magnitudes for each macro factor (e.g., `gdp_shock`, `rate_shock`, `fx_shock`).
3. Existing 12 sovereigns will automatically be tested against the new scenario.

Re-run:
```bash
python scripts/03_stress_test_model.py
python scripts/12_generate_excel_reports.py
python scripts/13_generate_pdf_reports.py
```

---

## Recipe 5: Add a New M&A Deal

**File:** `data/raw/mna_data_raw.csv`

Add a row with columns:
`deal_id`, `acquirer`, `target`, `sector`, `deal_value_bn`, `deal_type` (Merger/Acquisition/JV),
`cross_border` (0/1), `premium_pct`, `status` (Completed/Pending/Withdrawn),
`announced_date`, `closed_date`, `geography`, `strategic_rationale`.

Re-run:
```bash
python scripts/02_fetch_mna_data.py
python scripts/04_case_study_builder.py
python scripts/10_advanced_analysis.py
```

---

## Recipe 6: Run Only One Vertical

You don't need to run all 13 scripts every time.

| Vertical | Minimum scripts to re-run |
|----------|---------------------------|
| IPO only | `01` → `10` → `11` → `12` → `13` |
| M&A only | `02` → `04` → `10` → `11` → `12` → `13` |
| Sovereign only | `05` → `09` → `10` → `11` → `12` → `13` |
| Macro / Yield Curve | `08` → `10` → `11` |
