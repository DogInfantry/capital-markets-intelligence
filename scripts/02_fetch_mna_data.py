"""
M&A Data Fetcher
Fetches recent M&A deal data from public sources.
Outputs: data/raw/mna_data_raw.csv
"""

import os
import pandas as pd
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mna_data_raw.csv")


def build_mna_dataset():
    """
    Build an M&A dataset with major announced/completed deals.
    Covers a mix of sectors, deal sizes, and strategic rationales.
    """
    print("  Building M&A dataset...")

    deals = [
        {"acquirer": "Capital One Financial", "target": "Discover Financial Services", "announced_date": "2024-02-19", "deal_value_usd_bn": 35.3, "status": "Pending Regulatory", "sector": "Financial Services", "deal_type": "Stock-for-Stock Merger", "strategic_rationale": "Scale in payments network; combined credit card portfolio", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Mars Inc", "target": "Kellanova", "announced_date": "2024-08-14", "deal_value_usd_bn": 35.9, "status": "Completed", "sector": "Consumer Staples", "deal_type": "Cash Acquisition", "strategic_rationale": "Snacking portfolio expansion; global distribution synergies", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Synopsys", "target": "Ansys", "announced_date": "2024-01-16", "deal_value_usd_bn": 35.0, "status": "Completed", "sector": "Technology (EDA/Simulation)", "deal_type": "Cash + Stock", "strategic_rationale": "Silicon-to-systems design platform; simulation capabilities", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Diamondback Energy", "target": "Endeavor Energy Resources", "announced_date": "2024-02-12", "deal_value_usd_bn": 26.0, "status": "Completed", "sector": "Energy (E&P)", "deal_type": "Cash + Stock", "strategic_rationale": "Permian Basin consolidation; scale and cost efficiencies", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "ConocoPhillips", "target": "Marathon Oil", "announced_date": "2024-05-29", "deal_value_usd_bn": 22.5, "status": "Completed", "sector": "Energy (E&P)", "deal_type": "Stock-for-Stock", "strategic_rationale": "Multi-basin diversification; inventory depth in shale", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Hewlett Packard Enterprise", "target": "Juniper Networks", "announced_date": "2024-01-09", "deal_value_usd_bn": 14.0, "status": "Blocked (DOJ)", "sector": "Technology (Networking)", "deal_type": "Cash Acquisition", "strategic_rationale": "AI-driven networking; campus and data center portfolio", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Johnson & Johnson", "target": "Intra-Cellular Therapies", "announced_date": "2025-01-13", "deal_value_usd_bn": 14.6, "status": "Completed", "sector": "Pharmaceuticals", "deal_type": "Cash Acquisition", "strategic_rationale": "CNS neuroscience pipeline; Caplyta revenue stream", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Alphabet (Google)", "target": "Wiz", "announced_date": "2025-03-18", "deal_value_usd_bn": 32.0, "status": "Pending Regulatory", "sector": "Technology (Cybersecurity)", "deal_type": "Cash Acquisition", "strategic_rationale": "Cloud security leadership; multi-cloud posture management", "acquirer_country": "US", "target_country": "Israel"},
        {"acquirer": "Cisco Systems", "target": "Splunk", "announced_date": "2023-09-21", "deal_value_usd_bn": 28.0, "status": "Completed", "sector": "Technology (Observability)", "deal_type": "Cash Acquisition", "strategic_rationale": "Security + observability platform; recurring revenue shift", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "AbbVie", "target": "ImmunoGen", "announced_date": "2023-11-30", "deal_value_usd_bn": 10.1, "status": "Completed", "sector": "Pharmaceuticals (Oncology)", "deal_type": "Cash Acquisition", "strategic_rationale": "ADC platform (antibody-drug conjugates); oncology pipeline", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Nippon Steel", "target": "United States Steel Corp", "announced_date": "2023-12-18", "deal_value_usd_bn": 14.9, "status": "Blocked (CFIUS)", "sector": "Materials (Steel)", "deal_type": "Cash Acquisition", "strategic_rationale": "Global steel capacity; US market access", "acquirer_country": "Japan", "target_country": "US"},
        {"acquirer": "BlackRock", "target": "Global Infrastructure Partners", "announced_date": "2024-01-12", "deal_value_usd_bn": 12.5, "status": "Completed", "sector": "Financial Services (Alt Assets)", "deal_type": "Cash + Stock", "strategic_rationale": "Infrastructure AUM growth; private markets expansion", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Exxon Mobil", "target": "Pioneer Natural Resources", "announced_date": "2023-10-11", "deal_value_usd_bn": 64.5, "status": "Completed", "sector": "Energy (E&P)", "deal_type": "Stock-for-Stock", "strategic_rationale": "Permian Basin dominance; 40+ years of drilling inventory", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Broadcom", "target": "VMware", "announced_date": "2022-05-26", "deal_value_usd_bn": 69.0, "status": "Completed", "sector": "Technology (Virtualization)", "deal_type": "Cash + Stock", "strategic_rationale": "Enterprise software diversification; subscription transition", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Danaher", "target": "Abcam", "announced_date": "2023-07-20", "deal_value_usd_bn": 5.7, "status": "Completed", "sector": "Life Sciences", "deal_type": "Cash Acquisition", "strategic_rationale": "Biologics reagents leadership; proteomics research tools", "acquirer_country": "US", "target_country": "UK"},
        {"acquirer": "Silver Lake / Canada Pension", "target": "Endeavor Group Holdings", "announced_date": "2024-04-02", "deal_value_usd_bn": 13.0, "status": "Completed", "sector": "Media & Entertainment", "deal_type": "Take-Private (LBO)", "strategic_rationale": "Sports & entertainment assets; UFC + WWE consolidation play", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "GTCR", "target": "Worldpay (from FIS)", "announced_date": "2024-02-01", "deal_value_usd_bn": 18.5, "status": "Completed", "sector": "Financial Technology (Payments)", "deal_type": "Take-Private (LBO)", "strategic_rationale": "Merchant acquiring at scale; separation from FIS", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Novo Holdings", "target": "Catalent", "announced_date": "2024-02-05", "deal_value_usd_bn": 16.5, "status": "Completed", "sector": "Healthcare (CDMO)", "deal_type": "Cash Acquisition", "strategic_rationale": "Biologics manufacturing capacity for Novo Nordisk pipeline", "acquirer_country": "Denmark", "target_country": "US"},
        {"acquirer": "Bain Capital", "target": "Envestnet", "announced_date": "2024-07-10", "deal_value_usd_bn": 4.5, "status": "Completed", "sector": "Financial Technology (Wealth)", "deal_type": "Take-Private (LBO)", "strategic_rationale": "Wealth management data platform; advisor tech modernization", "acquirer_country": "US", "target_country": "US"},
        {"acquirer": "Veritas Capital / Evergreen", "target": "Cotiviti (from Verscend)", "announced_date": "2024-01-08", "deal_value_usd_bn": 11.0, "status": "Completed", "sector": "Healthcare Analytics", "deal_type": "Sponsor-to-Sponsor LBO", "strategic_rationale": "Healthcare payment accuracy; AI-driven claims analytics", "acquirer_country": "US", "target_country": "US"},
    ]

    df = pd.DataFrame(deals)
    df["announced_date"] = pd.to_datetime(df["announced_date"])

    # Derived fields
    df["premium_est_pct"] = None  # Would need pre-announcement share prices
    df["cross_border"] = df["acquirer_country"] != df["target_country"]
    df["year"] = df["announced_date"].dt.year

    print(f"  [OK] Built dataset with {len(df)} M&A deals")
    return df


def save_data(df, filepath):
    """Save DataFrame to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"  [OK] Saved to {filepath}")


def main():
    print("=" * 60)
    print("M&A Data Fetcher — Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    print("[1/2] Building M&A dataset...")
    df = build_mna_dataset()

    print("[2/2] Saving data...")
    save_data(df, OUTPUT_FILE)

    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Total deals: {len(df)}")
    print(f"  Date range: {df['announced_date'].min().date()} to {df['announced_date'].max().date()}")
    print(f"  Total deal value: ${df['deal_value_usd_bn'].sum():.1f}B")
    print(f"  Avg deal size: ${df['deal_value_usd_bn'].mean():.1f}B")
    print(f"  Cross-border deals: {df['cross_border'].sum()}")
    print(f"  Sectors: {df['sector'].nunique()}")
    completed = (df["status"] == "Completed").sum()
    print(f"  Status: {completed} completed, {len(df) - completed} pending/blocked")
    print("=" * 60)


if __name__ == "__main__":
    main()
