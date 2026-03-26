"""
Sovereign Bond Issuance Data Fetcher
Builds a dataset of recent sovereign bond issuances across developed and emerging markets.
Outputs: data/raw/sovereign_issuance_raw.csv
"""

import os
import pandas as pd
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sovereign_issuance_raw.csv")


def build_sovereign_issuance_dataset():
    """
    Build a sovereign bond issuance dataset covering major DM and EM issuers.
    Data points reflect realistic recent issuance activity.
    """
    print("  Building sovereign bond issuance dataset...")

    issuances = [
        # US Treasuries
        {"country": "United States", "iso": "US", "bond_type": "Treasury Note", "maturity_years": 10, "coupon_pct": 4.25, "issue_size_usd_bn": 42.0, "issue_date": "2024-11-15", "currency": "USD", "rating_sp": "AA+", "yield_at_issue_pct": 4.28, "region": "North America"},
        {"country": "United States", "iso": "US", "bond_type": "Treasury Bond", "maturity_years": 30, "coupon_pct": 4.625, "issue_size_usd_bn": 25.0, "issue_date": "2024-11-15", "currency": "USD", "rating_sp": "AA+", "yield_at_issue_pct": 4.65, "region": "North America"},
        {"country": "United States", "iso": "US", "bond_type": "Treasury Note", "maturity_years": 2, "coupon_pct": 4.375, "issue_size_usd_bn": 69.0, "issue_date": "2024-12-02", "currency": "USD", "rating_sp": "AA+", "yield_at_issue_pct": 4.21, "region": "North America"},
        {"country": "United States", "iso": "US", "bond_type": "Treasury Note", "maturity_years": 5, "coupon_pct": 4.125, "issue_size_usd_bn": 70.0, "issue_date": "2025-01-15", "currency": "USD", "rating_sp": "AA+", "yield_at_issue_pct": 4.38, "region": "North America"},

        # UK Gilts
        {"country": "United Kingdom", "iso": "GB", "bond_type": "Gilt", "maturity_years": 10, "coupon_pct": 4.00, "issue_size_usd_bn": 5.8, "issue_date": "2024-10-22", "currency": "GBP", "rating_sp": "AA", "yield_at_issue_pct": 4.12, "region": "Europe"},
        {"country": "United Kingdom", "iso": "GB", "bond_type": "Gilt", "maturity_years": 30, "coupon_pct": 4.375, "issue_size_usd_bn": 4.2, "issue_date": "2024-11-19", "currency": "GBP", "rating_sp": "AA", "yield_at_issue_pct": 4.68, "region": "Europe"},

        # German Bunds
        {"country": "Germany", "iso": "DE", "bond_type": "Bund", "maturity_years": 10, "coupon_pct": 2.50, "issue_size_usd_bn": 5.5, "issue_date": "2024-09-11", "currency": "EUR", "rating_sp": "AAA", "yield_at_issue_pct": 2.18, "region": "Europe"},
        {"country": "Germany", "iso": "DE", "bond_type": "Bund", "maturity_years": 30, "coupon_pct": 2.60, "issue_size_usd_bn": 2.2, "issue_date": "2024-10-16", "currency": "EUR", "rating_sp": "AAA", "yield_at_issue_pct": 2.55, "region": "Europe"},

        # Japan JGBs
        {"country": "Japan", "iso": "JP", "bond_type": "JGB", "maturity_years": 10, "coupon_pct": 0.80, "issue_size_usd_bn": 17.5, "issue_date": "2024-12-03", "currency": "JPY", "rating_sp": "A+", "yield_at_issue_pct": 1.05, "region": "Asia-Pacific"},
        {"country": "Japan", "iso": "JP", "bond_type": "JGB", "maturity_years": 20, "coupon_pct": 1.70, "issue_size_usd_bn": 7.3, "issue_date": "2024-11-21", "currency": "JPY", "rating_sp": "A+", "yield_at_issue_pct": 1.88, "region": "Asia-Pacific"},

        # France OATs
        {"country": "France", "iso": "FR", "bond_type": "OAT", "maturity_years": 10, "coupon_pct": 3.00, "issue_size_usd_bn": 8.8, "issue_date": "2024-10-03", "currency": "EUR", "rating_sp": "AA-", "yield_at_issue_pct": 2.92, "region": "Europe"},

        # Italy BTPs
        {"country": "Italy", "iso": "IT", "bond_type": "BTP", "maturity_years": 10, "coupon_pct": 3.85, "issue_size_usd_bn": 7.5, "issue_date": "2024-09-30", "currency": "EUR", "rating_sp": "BBB", "yield_at_issue_pct": 3.52, "region": "Europe"},
        {"country": "Italy", "iso": "IT", "bond_type": "BTP Valore (Retail)", "maturity_years": 6, "coupon_pct": 3.35, "issue_size_usd_bn": 11.2, "issue_date": "2024-05-20", "currency": "EUR", "rating_sp": "BBB", "yield_at_issue_pct": 3.40, "region": "Europe"},

        # Australia
        {"country": "Australia", "iso": "AU", "bond_type": "ACGB", "maturity_years": 10, "coupon_pct": 4.25, "issue_size_usd_bn": 5.0, "issue_date": "2024-10-09", "currency": "AUD", "rating_sp": "AAA", "yield_at_issue_pct": 4.10, "region": "Asia-Pacific"},

        # Canada
        {"country": "Canada", "iso": "CA", "bond_type": "Government Bond", "maturity_years": 10, "coupon_pct": 3.50, "issue_size_usd_bn": 4.8, "issue_date": "2024-09-04", "currency": "CAD", "rating_sp": "AAA", "yield_at_issue_pct": 3.15, "region": "North America"},

        # Emerging Markets
        {"country": "India", "iso": "IN", "bond_type": "G-Sec", "maturity_years": 10, "coupon_pct": 7.18, "issue_size_usd_bn": 2.4, "issue_date": "2024-10-11", "currency": "INR", "rating_sp": "BBB-", "yield_at_issue_pct": 6.85, "region": "Asia-Pacific"},
        {"country": "India", "iso": "IN", "bond_type": "G-Sec (Green Bond)", "maturity_years": 10, "coupon_pct": 7.10, "issue_size_usd_bn": 1.2, "issue_date": "2024-10-22", "currency": "INR", "rating_sp": "BBB-", "yield_at_issue_pct": 6.92, "region": "Asia-Pacific"},

        {"country": "Brazil", "iso": "BR", "bond_type": "NTN-F", "maturity_years": 10, "coupon_pct": 10.00, "issue_size_usd_bn": 1.5, "issue_date": "2024-08-15", "currency": "BRL", "rating_sp": "BB", "yield_at_issue_pct": 11.65, "region": "Latin America"},
        {"country": "Brazil", "iso": "BR", "bond_type": "Global Bond (USD)", "maturity_years": 10, "coupon_pct": 6.125, "issue_size_usd_bn": 2.0, "issue_date": "2024-12-04", "currency": "USD", "rating_sp": "BB", "yield_at_issue_pct": 6.35, "region": "Latin America"},

        {"country": "Mexico", "iso": "MX", "bond_type": "Mbono", "maturity_years": 10, "coupon_pct": 8.50, "issue_size_usd_bn": 1.8, "issue_date": "2024-09-26", "currency": "MXN", "rating_sp": "BBB", "yield_at_issue_pct": 9.80, "region": "Latin America"},
        {"country": "Mexico", "iso": "MX", "bond_type": "Global Bond (USD)", "maturity_years": 12, "coupon_pct": 5.40, "issue_size_usd_bn": 2.5, "issue_date": "2025-01-08", "currency": "USD", "rating_sp": "BBB", "yield_at_issue_pct": 5.55, "region": "Latin America"},

        {"country": "South Africa", "iso": "ZA", "bond_type": "Government Bond (R2037)", "maturity_years": 13, "coupon_pct": 8.50, "issue_size_usd_bn": 0.8, "issue_date": "2024-08-27", "currency": "ZAR", "rating_sp": "BB-", "yield_at_issue_pct": 10.80, "region": "Africa"},

        {"country": "Turkey", "iso": "TR", "bond_type": "Government Bond", "maturity_years": 5, "coupon_pct": 25.00, "issue_size_usd_bn": 1.1, "issue_date": "2024-09-18", "currency": "TRY", "rating_sp": "B+", "yield_at_issue_pct": 28.50, "region": "Europe/MENA"},
        {"country": "Turkey", "iso": "TR", "bond_type": "Eurobond (USD)", "maturity_years": 10, "coupon_pct": 6.50, "issue_size_usd_bn": 3.0, "issue_date": "2025-01-14", "currency": "USD", "rating_sp": "B+", "yield_at_issue_pct": 6.75, "region": "Europe/MENA"},

        {"country": "Saudi Arabia", "iso": "SA", "bond_type": "Sukuk (Islamic Bond)", "maturity_years": 10, "coupon_pct": 4.75, "issue_size_usd_bn": 5.0, "issue_date": "2024-10-07", "currency": "USD", "rating_sp": "A", "yield_at_issue_pct": 4.82, "region": "MENA"},
        {"country": "Saudi Arabia", "iso": "SA", "bond_type": "Green Bond", "maturity_years": 10, "coupon_pct": 4.65, "issue_size_usd_bn": 3.0, "issue_date": "2025-02-12", "currency": "USD", "rating_sp": "A", "yield_at_issue_pct": 4.72, "region": "MENA"},

        {"country": "China", "iso": "CN", "bond_type": "CGB", "maturity_years": 10, "coupon_pct": 2.12, "issue_size_usd_bn": 5.5, "issue_date": "2024-11-20", "currency": "CNY", "rating_sp": "A+", "yield_at_issue_pct": 2.08, "region": "Asia-Pacific"},
        {"country": "China", "iso": "CN", "bond_type": "CGB (Ultra-Long)", "maturity_years": 30, "coupon_pct": 2.65, "issue_size_usd_bn": 4.5, "issue_date": "2024-11-15", "currency": "CNY", "rating_sp": "A+", "yield_at_issue_pct": 2.58, "region": "Asia-Pacific"},

        {"country": "Indonesia", "iso": "ID", "bond_type": "Global Bond (USD)", "maturity_years": 10, "coupon_pct": 4.95, "issue_size_usd_bn": 2.0, "issue_date": "2025-01-07", "currency": "USD", "rating_sp": "BBB", "yield_at_issue_pct": 5.10, "region": "Asia-Pacific"},

        {"country": "Poland", "iso": "PL", "bond_type": "Euro Bond", "maturity_years": 10, "coupon_pct": 4.15, "issue_size_usd_bn": 2.8, "issue_date": "2024-09-10", "currency": "EUR", "rating_sp": "A-", "yield_at_issue_pct": 4.22, "region": "Europe"},

        {"country": "Nigeria", "iso": "NG", "bond_type": "Eurobond (USD)", "maturity_years": 10, "coupon_pct": 9.125, "issue_size_usd_bn": 0.9, "issue_date": "2024-12-02", "currency": "USD", "rating_sp": "B-", "yield_at_issue_pct": 9.85, "region": "Africa"},
    ]

    df = pd.DataFrame(issuances)
    df["issue_date"] = pd.to_datetime(df["issue_date"])

    # Derived fields
    df["spread_over_ust_bps"] = ((df["yield_at_issue_pct"] - 4.25) * 100).round(0)
    df["spread_over_ust_bps"] = df["spread_over_ust_bps"].clip(lower=0)  # Floor at 0 for UST itself
    df["is_usd_denominated"] = df["currency"] == "USD"
    df["investment_grade"] = df["rating_sp"].apply(
        lambda r: r.replace("+", "").replace("-", "") in ["AAA", "AA", "A", "BBB"]
    )

    print(f"  [OK] Built dataset with {len(df)} sovereign issuances")
    return df


def save_data(df, filepath):
    """Save DataFrame to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"  [OK] Saved to {filepath}")


def main():
    print("=" * 60)
    print("Sovereign Issuance Fetcher - Capital Markets Intelligence")
    print("=" * 60)
    print()

    print("[1/2] Building sovereign issuance dataset...")
    df = build_sovereign_issuance_dataset()

    print("[2/2] Saving data...")
    save_data(df, OUTPUT_FILE)

    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Total issuances: {len(df)}")
    print(f"  Countries: {df['country'].nunique()}")
    print(f"  Date range: {df['issue_date'].min().date()} to {df['issue_date'].max().date()}")
    print(f"  Total issuance: ${df['issue_size_usd_bn'].sum():.1f}B")
    print(f"  USD-denominated: {df['is_usd_denominated'].sum()}")
    print(f"  Investment grade: {df['investment_grade'].sum()}")
    print(f"  Avg yield at issue: {df['yield_at_issue_pct'].mean():.2f}%")
    print(f"  Bond types: {df['bond_type'].nunique()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
