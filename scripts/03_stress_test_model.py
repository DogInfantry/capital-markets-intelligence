"""
Sovereign Stress Test Model
Simulates impact of macro shocks on sovereign bond yields and credit ratings.
Outputs: data/processed/stress_test_results.csv
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "stress_test_results.csv")


def build_sovereign_baseline():
    """Build baseline sovereign data for stress testing."""
    print("  Building sovereign baseline data...")

    sovereigns = [
        {"country": "United States", "iso": "US", "rating_sp": "AA+", "rating_moody": "Aaa", "ten_yr_yield_pct": 4.25, "debt_to_gdp_pct": 123.0, "gdp_growth_pct": 2.5, "inflation_pct": 3.1, "fx_usd": 1.00, "region": "North America"},
        {"country": "United Kingdom", "iso": "GB", "rating_sp": "AA", "rating_moody": "Aa3", "ten_yr_yield_pct": 4.05, "debt_to_gdp_pct": 101.0, "gdp_growth_pct": 0.6, "inflation_pct": 4.0, "fx_usd": 1.27, "region": "Europe"},
        {"country": "Germany", "iso": "DE", "rating_sp": "AAA", "rating_moody": "Aaa", "ten_yr_yield_pct": 2.35, "debt_to_gdp_pct": 64.0, "gdp_growth_pct": 0.2, "inflation_pct": 2.9, "fx_usd": 1.09, "region": "Europe"},
        {"country": "Japan", "iso": "JP", "rating_sp": "A+", "rating_moody": "A1", "ten_yr_yield_pct": 0.85, "debt_to_gdp_pct": 255.0, "gdp_growth_pct": 1.9, "inflation_pct": 2.8, "fx_usd": 0.0067, "region": "Asia-Pacific"},
        {"country": "China", "iso": "CN", "rating_sp": "A+", "rating_moody": "A1", "ten_yr_yield_pct": 2.30, "debt_to_gdp_pct": 83.0, "gdp_growth_pct": 5.2, "inflation_pct": 0.2, "fx_usd": 0.14, "region": "Asia-Pacific"},
        {"country": "India", "iso": "IN", "rating_sp": "BBB-", "rating_moody": "Baa3", "ten_yr_yield_pct": 7.10, "debt_to_gdp_pct": 81.0, "gdp_growth_pct": 6.5, "inflation_pct": 5.4, "fx_usd": 0.012, "region": "Asia-Pacific"},
        {"country": "Brazil", "iso": "BR", "rating_sp": "BB", "rating_moody": "Ba2", "ten_yr_yield_pct": 11.80, "debt_to_gdp_pct": 74.0, "gdp_growth_pct": 2.9, "inflation_pct": 4.6, "fx_usd": 0.20, "region": "Latin America"},
        {"country": "Mexico", "iso": "MX", "rating_sp": "BBB", "rating_moody": "Baa2", "ten_yr_yield_pct": 9.45, "debt_to_gdp_pct": 53.0, "gdp_growth_pct": 3.2, "inflation_pct": 4.7, "fx_usd": 0.058, "region": "Latin America"},
        {"country": "South Africa", "iso": "ZA", "rating_sp": "BB-", "rating_moody": "Ba2", "ten_yr_yield_pct": 10.50, "debt_to_gdp_pct": 73.0, "gdp_growth_pct": 0.6, "inflation_pct": 5.1, "fx_usd": 0.055, "region": "Africa"},
        {"country": "Turkey", "iso": "TR", "rating_sp": "B+", "rating_moody": "B3", "ten_yr_yield_pct": 25.00, "debt_to_gdp_pct": 30.0, "gdp_growth_pct": 4.5, "inflation_pct": 58.0, "fx_usd": 0.031, "region": "Europe/MENA"},
        {"country": "Saudi Arabia", "iso": "SA", "rating_sp": "A", "rating_moody": "A1", "ten_yr_yield_pct": 4.80, "debt_to_gdp_pct": 26.0, "gdp_growth_pct": -0.8, "inflation_pct": 1.6, "fx_usd": 0.27, "region": "MENA"},
        {"country": "Australia", "iso": "AU", "rating_sp": "AAA", "rating_moody": "Aaa", "ten_yr_yield_pct": 4.15, "debt_to_gdp_pct": 50.0, "gdp_growth_pct": 1.5, "inflation_pct": 3.6, "fx_usd": 0.66, "region": "Asia-Pacific"},
    ]

    df = pd.DataFrame(sovereigns)
    print(f"  [OK] Built baseline for {len(df)} sovereigns")
    return df


def define_stress_scenarios():
    """Define macro stress scenarios."""
    scenarios = {
        "Base Case": {
            "yield_shock_bps": 0,
            "gdp_shock_pct": 0,
            "inflation_shock_pct": 0,
            "fx_shock_pct": 0,
            "description": "No change from current conditions",
        },
        "Fed Hawkish (Rate Hike +100bp)": {
            "yield_shock_bps": 100,
            "gdp_shock_pct": -0.5,
            "inflation_shock_pct": -0.3,
            "fx_shock_pct": 3.0,  # USD strengthens
            "description": "Fed raises rates 100bp; global risk-off",
        },
        "Global Recession": {
            "yield_shock_bps": -50,  # Flight to quality
            "gdp_shock_pct": -2.0,
            "inflation_shock_pct": -1.0,
            "fx_shock_pct": 5.0,  # USD safe haven
            "description": "Synchronized global slowdown; risk-off",
        },
        "EM Currency Crisis": {
            "yield_shock_bps": 200,  # EM yields spike
            "gdp_shock_pct": -1.5,
            "inflation_shock_pct": 3.0,
            "fx_shock_pct": -15.0,  # EM currencies depreciate
            "description": "Capital flight from EM; contagion risk",
        },
        "Oil Shock ($120/bbl)": {
            "yield_shock_bps": 50,
            "gdp_shock_pct": -0.8,
            "inflation_shock_pct": 2.0,
            "fx_shock_pct": -5.0,
            "description": "Oil price spike; stagflation risk for importers",
        },
    }
    return scenarios


def run_stress_test(baseline_df, scenarios):
    """Apply stress scenarios to sovereign baseline data."""
    print("  Running stress scenarios...")
    results = []

    em_countries = {"BR", "MX", "ZA", "TR", "IN", "CN"}
    oil_importers = {"IN", "JP", "DE", "GB", "CN", "TR"}
    oil_exporters = {"SA", "US"}

    for scenario_name, shocks in scenarios.items():
        for _, row in baseline_df.iterrows():
            stressed = row.to_dict()
            stressed["scenario"] = scenario_name
            stressed["scenario_description"] = shocks["description"]

            # Apply yield shock (EM gets larger shock in EM crisis)
            yield_multiplier = 1.5 if (row["iso"] in em_countries and "EM" in scenario_name) else 1.0
            # DM safe havens get inverted yield shock in risk-off
            if row["iso"] in {"US", "DE", "JP"} and "Recession" in scenario_name:
                yield_multiplier = -1.0  # yields fall (flight to quality)
            stressed["stressed_yield_pct"] = round(
                row["ten_yr_yield_pct"] + (shocks["yield_shock_bps"] / 100 * yield_multiplier), 2
            )

            # Apply GDP shock
            stressed["stressed_gdp_growth_pct"] = round(row["gdp_growth_pct"] + shocks["gdp_shock_pct"], 2)

            # Apply inflation shock (oil importers hit harder on oil shock)
            inflation_mult = 1.5 if (row["iso"] in oil_importers and "Oil" in scenario_name) else 1.0
            # Oil exporters benefit from oil shock
            if row["iso"] in oil_exporters and "Oil" in scenario_name:
                inflation_mult = 0.5
            stressed["stressed_inflation_pct"] = round(
                row["inflation_pct"] + (shocks["inflation_shock_pct"] * inflation_mult), 2
            )

            # Apply FX shock (EM currencies hit harder)
            fx_mult = 2.0 if (row["iso"] in em_countries and "EM" in scenario_name) else 1.0
            if row["iso"] == "US":
                fx_mult = 0  # USD is the reference
            stressed["stressed_fx_change_pct"] = round(shocks["fx_shock_pct"] * fx_mult, 2)

            # Simple composite risk score (higher = more stressed)
            stressed["risk_score"] = round(
                abs(stressed["stressed_yield_pct"] - row["ten_yr_yield_pct"]) * 10
                + abs(stressed["stressed_gdp_growth_pct"] - row["gdp_growth_pct"]) * 5
                + abs(stressed["stressed_inflation_pct"] - row["inflation_pct"]) * 3
                + abs(stressed["stressed_fx_change_pct"]) * 2,
                1,
            )

            results.append(stressed)

    result_df = pd.DataFrame(results)
    print(f"  [OK] Generated {len(result_df)} scenario-country combinations")
    return result_df


def save_data(df, filepath):
    """Save DataFrame to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"  [OK] Saved to {filepath}")


def main():
    print("=" * 60)
    print("Sovereign Stress Test — Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    print("[1/4] Building sovereign baseline...")
    baseline = build_sovereign_baseline()

    print("[2/4] Defining stress scenarios...")
    scenarios = define_stress_scenarios()
    print(f"  [OK] Defined {len(scenarios)} scenarios")

    print("[3/4] Running stress tests...")
    results = run_stress_test(baseline, scenarios)

    print("[4/4] Saving results...")
    save_data(results, OUTPUT_FILE)

    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Sovereigns: {baseline['country'].nunique()}")
    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Total combinations: {len(results)}")
    print()
    print("  Highest risk scores by scenario:")
    for scenario in scenarios:
        subset = results[results["scenario"] == scenario]
        top = subset.nlargest(3, "risk_score")[["country", "risk_score"]]
        top_str = ", ".join([f"{r['country']} ({r['risk_score']})" for _, r in top.iterrows()])
        print(f"    {scenario}: {top_str}")
    print("=" * 60)


if __name__ == "__main__":
    main()
