"""
World Bank & IMF Data Fetcher
Pulls real macro indicators by country from World Bank Open Data API.
No API key required.

Outputs:
  data/raw/worldbank_indicators.csv
  data/raw/country_macro_panel.csv
"""

import os
import time
import pandas as pd
import requests
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CACHE_DIR = os.path.join(BASE_DIR, "data", "cache")

# World Bank API base
WB_API = "https://api.worldbank.org/v2"

# Countries relevant to our sovereign analysis
COUNTRIES = {
    "US": "United States", "GB": "United Kingdom", "DE": "Germany",
    "JP": "Japan", "CN": "China", "IN": "India", "BR": "Brazil",
    "MX": "Mexico", "ZA": "South Africa", "TR": "Turkey (Turkiye)",
    "SA": "Saudi Arabia", "AU": "Australia", "FR": "France",
    "IT": "Italy", "CA": "Canada", "ID": "Indonesia",
    "PL": "Poland", "NG": "Nigeria", "KR": "Korea, Rep.",
    "RU": "Russian Federation",
}

# Key World Bank indicators
INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current USD)",
    "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
    "FP.CPI.TOTL.ZG": "Inflation (CPI, annual %)",
    "GC.DOD.TOTL.GD.ZS": "Central govt debt (% of GDP)",
    "BN.CAB.XOKA.GD.ZS": "Current account (% of GDP)",
    "FI.RES.TOTL.CD": "Total reserves (includes gold, USD)",
    "BX.KLT.DINV.WD.GD.ZS": "FDI net inflows (% of GDP)",
    "NE.EXP.GNFS.ZS": "Exports (% of GDP)",
    "NE.IMP.GNFS.ZS": "Imports (% of GDP)",
    "SL.UEM.TOTL.ZS": "Unemployment (% of labor force)",
    "GC.REV.XGRT.GD.ZS": "Revenue excl grants (% of GDP)",
    "GC.XPN.TOTL.GD.ZS": "Expense (% of GDP)",
    "PA.NUS.FCRF": "Official exchange rate (LCU per USD)",
    "FR.INR.RINR": "Real interest rate (%)",
    "DT.DOD.DECT.GN.ZS": "External debt stocks (% of GNI)",
}

RATE_LIMIT_DELAY = 0.3  # Be nice to World Bank API


def fetch_indicator(indicator_code, indicator_name, country_codes, start_year=2018, end_year=2024):
    """Fetch a single indicator for all countries from World Bank API."""
    countries_str = ";".join(country_codes)
    url = f"{WB_API}/country/{countries_str}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 1000,
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if len(data) < 2 or not data[1]:
            return []

        records = []
        for entry in data[1]:
            if entry["value"] is not None:
                records.append({
                    "country_code": entry["country"]["id"],
                    "country_name": entry["country"]["value"],
                    "indicator_code": indicator_code,
                    "indicator_name": indicator_name,
                    "year": int(entry["date"]),
                    "value": float(entry["value"]),
                })
        return records

    except Exception as e:
        print(f"      [WARN] Failed {indicator_code}: {e}")
        return []


def fetch_all_worldbank_data():
    """Fetch all indicators for all countries."""
    print("  Fetching World Bank indicators...")
    country_codes = list(COUNTRIES.keys())
    all_records = []

    for i, (code, name) in enumerate(INDICATORS.items(), 1):
        print(f"    [{i}/{len(INDICATORS)}] {name}...")
        records = fetch_indicator(code, name, country_codes)
        all_records.extend(records)
        if records:
            print(f"      [OK] {len(records)} data points")
        else:
            print(f"      [WARN] No data returned")
        time.sleep(RATE_LIMIT_DELAY)

    if not all_records:
        print("  [WARN] No data from World Bank API, using cache")
        return _load_cache()

    df = pd.DataFrame(all_records)
    print(f"  [OK] Total: {len(df)} data points across {df['country_code'].nunique()} countries")
    return df


def build_country_panel(wb_df):
    """
    Pivot World Bank data into a country-level panel dataset.
    Each row = country-year, columns = indicators.
    """
    print("  Building country macro panel...")

    if len(wb_df) == 0:
        return pd.DataFrame()

    # Pivot: rows = (country, year), columns = indicator
    panel = wb_df.pivot_table(
        index=["country_code", "country_name", "year"],
        columns="indicator_name",
        values="value",
        aggfunc="first",
    ).reset_index()

    # Flatten column names
    panel.columns = [c if isinstance(c, str) else c for c in panel.columns]

    # Sort
    panel = panel.sort_values(["country_code", "year"])

    # Add derived metrics
    if "GDP (current USD)" in panel.columns:
        panel["GDP_trillion_usd"] = panel["GDP (current USD)"] / 1e12

    if "Exports (% of GDP)" in panel.columns and "Imports (% of GDP)" in panel.columns:
        panel["trade_openness_pct"] = panel["Exports (% of GDP)"] + panel["Imports (% of GDP)"]

    if "Revenue excl grants (% of GDP)" in panel.columns and "Expense (% of GDP)" in panel.columns:
        panel["fiscal_balance_pct_gdp"] = (
            panel["Revenue excl grants (% of GDP)"] - panel["Expense (% of GDP)"]
        )

    print(f"  [OK] Panel: {len(panel)} country-year observations, {panel['country_code'].nunique()} countries")
    return panel


def _save_cache(df, filename):
    os.makedirs(CACHE_DIR, exist_ok=True)
    df.to_csv(os.path.join(CACHE_DIR, filename), index=False)


def _load_cache():
    filepath = os.path.join(CACHE_DIR, "worldbank_indicators.csv")
    if os.path.exists(filepath):
        print("  [OK] Loaded from cache")
        return pd.read_csv(filepath)
    return pd.DataFrame()


def main():
    print("=" * 60)
    print("World Bank Macro Data Fetcher")
    print("Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    os.makedirs(RAW_DIR, exist_ok=True)

    # Fetch raw indicator data
    wb_df = fetch_all_worldbank_data()

    if len(wb_df) == 0:
        print("[ERR] No data available. Check internet connection.")
        return

    # Save raw
    wb_df.to_csv(os.path.join(RAW_DIR, "worldbank_indicators.csv"), index=False)
    _save_cache(wb_df, "worldbank_indicators.csv")
    print(f"  [OK] Saved worldbank_indicators.csv")

    # Build panel
    panel = build_country_panel(wb_df)
    if len(panel) > 0:
        panel.to_csv(os.path.join(RAW_DIR, "country_macro_panel.csv"), index=False)
        print(f"  [OK] Saved country_macro_panel.csv")

    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Countries: {wb_df['country_code'].nunique()}")
    print(f"  Indicators: {wb_df['indicator_code'].nunique()}")
    print(f"  Year range: {wb_df['year'].min()}-{wb_df['year'].max()}")
    print(f"  Total data points: {len(wb_df)}")
    if len(panel) > 0:
        latest = panel[panel["year"] == panel["year"].max()]
        print(f"\n  Latest year ({panel['year'].max()}) snapshot:")
        for _, row in latest.head(5).iterrows():
            gdp = row.get("GDP_trillion_usd", None)
            growth = row.get("GDP growth (annual %)", None)
            infl = row.get("Inflation (CPI, annual %)", None)
            gdp_str = f"${gdp:.2f}T" if pd.notna(gdp) else "N/A"
            growth_str = f"{growth:+.1f}%" if pd.notna(growth) else "N/A"
            infl_str = f"{infl:.1f}%" if pd.notna(infl) else "N/A"
            print(f"    {row['country_name']:<25s} GDP: {gdp_str}  Growth: {growth_str}  Inflation: {infl_str}")
    print("=" * 60)


if __name__ == "__main__":
    main()
