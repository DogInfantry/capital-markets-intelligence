"""
M&A Case Study Builder
Generates structured case study analyses for selected M&A deals.
Outputs: data/processed/case_studies.csv, output/case_study_summaries.txt
"""

import os
import pandas as pd
from datetime import datetime

INPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "mna_data_raw.csv")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "case_studies.csv")
OUTPUT_TXT = os.path.join(os.path.dirname(__file__), "..", "output", "case_study_summaries.txt")


def load_mna_data(filepath):
    """Load M&A data from CSV."""
    if not os.path.exists(filepath):
        print(f"  [ERR] File not found: {filepath}")
        print("  -> Run 02_fetch_mna_data.py first")
        return None
    df = pd.read_csv(filepath, parse_dates=["announced_date"])
    print(f"  [OK] Loaded {len(df)} deals from {filepath}")
    return df


def analyze_deal(deal):
    """Generate a structured case study analysis for a single deal."""
    analysis = {}

    # Deal overview
    analysis["deal_name"] = f"{deal['acquirer']} / {deal['target']}"
    analysis["deal_value_usd_bn"] = deal["deal_value_usd_bn"]
    analysis["announced_date"] = deal["announced_date"]
    analysis["sector"] = deal["sector"]
    analysis["deal_type"] = deal["deal_type"]
    analysis["status"] = deal["status"]
    analysis["cross_border"] = deal["cross_border"]

    # Strategic assessment
    analysis["strategic_rationale"] = deal["strategic_rationale"]

    # Deal size classification
    if deal["deal_value_usd_bn"] >= 50:
        analysis["size_tier"] = "Mega-Deal (>$50B)"
    elif deal["deal_value_usd_bn"] >= 20:
        analysis["size_tier"] = "Large-Cap ($20-50B)"
    elif deal["deal_value_usd_bn"] >= 10:
        analysis["size_tier"] = "Mid-Cap ($10-20B)"
    else:
        analysis["size_tier"] = "Core Middle Market (<$10B)"

    # Risk factors
    risks = []
    if deal["cross_border"]:
        risks.append("Cross-border regulatory risk (CFIUS/antitrust)")
    if deal["deal_value_usd_bn"] >= 30:
        risks.append("Size-related execution complexity")
    if "Pending" in str(deal["status"]):
        risks.append("Regulatory approval uncertainty")
    if "Blocked" in str(deal["status"]):
        risks.append("DEAL BLOCKED — regulatory intervention")
    if "LBO" in str(deal["deal_type"]) or "Take-Private" in str(deal["deal_type"]):
        risks.append("Leverage risk (PE sponsor deal)")
    if "Technology" in str(deal["sector"]):
        risks.append("Tech integration risk; talent retention")
    analysis["risk_factors"] = "; ".join(risks) if risks else "Standard execution risk"

    # Value creation thesis
    value_drivers = []
    rationale = str(deal["strategic_rationale"]).lower()
    if "synerg" in rationale or "cost" in rationale or "scale" in rationale:
        value_drivers.append("Cost synergies")
    if "revenue" in rationale or "cross-sell" in rationale or "portfolio" in rationale:
        value_drivers.append("Revenue synergies")
    if "platform" in rationale or "pipeline" in rationale:
        value_drivers.append("Platform/capability expansion")
    if "market" in rationale or "consolidat" in rationale or "dominan" in rationale:
        value_drivers.append("Market consolidation")
    if not value_drivers:
        value_drivers.append("Strategic repositioning")
    analysis["value_drivers"] = "; ".join(value_drivers)

    # GS/JPM relevance score (how relevant for capital markets research)
    relevance = 5  # base
    if deal["deal_value_usd_bn"] >= 20:
        relevance += 2
    if deal["cross_border"]:
        relevance += 1
    if "Blocked" in str(deal["status"]) or "Pending" in str(deal["status"]):
        relevance += 2  # regulatory angle is interesting
    if deal["sector"] in ["Technology (Cybersecurity)", "Technology (AI Chips)", "Financial Services"]:
        relevance += 1
    analysis["research_relevance_score"] = min(relevance, 10)

    return analysis


def generate_text_summary(case_studies_df):
    """Generate human-readable case study summaries."""
    lines = []
    lines.append("=" * 70)
    lines.append("M&A CASE STUDY SUMMARIES")
    lines.append(f"Capital Markets Intelligence Platform — {datetime.now().strftime('%B %Y')}")
    lines.append("=" * 70)
    lines.append("")

    for i, (_, cs) in enumerate(case_studies_df.iterrows(), 1):
        lines.append(f"{'─' * 70}")
        lines.append(f"CASE STUDY #{i}: {cs['deal_name']}")
        lines.append(f"{'─' * 70}")
        lines.append(f"  Deal Value:      ${cs['deal_value_usd_bn']:.1f}B")
        lines.append(f"  Announced:       {cs['announced_date']}")
        lines.append(f"  Sector:          {cs['sector']}")
        lines.append(f"  Deal Type:       {cs['deal_type']}")
        lines.append(f"  Size Tier:       {cs['size_tier']}")
        lines.append(f"  Status:          {cs['status']}")
        lines.append(f"  Cross-Border:    {'Yes' if cs['cross_border'] else 'No'}")
        lines.append(f"")
        lines.append(f"  Strategic Rationale:")
        lines.append(f"    {cs['strategic_rationale']}")
        lines.append(f"")
        lines.append(f"  Value Drivers:   {cs['value_drivers']}")
        lines.append(f"  Risk Factors:    {cs['risk_factors']}")
        lines.append(f"  Research Score:  {cs['research_relevance_score']}/10")
        lines.append(f"")

    lines.append("=" * 70)
    lines.append(f"Total deals analyzed: {len(case_studies_df)}")
    lines.append(f"Avg research relevance: {case_studies_df['research_relevance_score'].mean():.1f}/10")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_outputs(case_studies_df, text_summary):
    """Save case studies to CSV and text summary."""
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_TXT), exist_ok=True)

    case_studies_df.to_csv(OUTPUT_CSV, index=False)
    print(f"  [OK] Saved CSV to {OUTPUT_CSV}")

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(text_summary)
    print(f"  [OK] Saved text summary to {OUTPUT_TXT}")


def main():
    print("=" * 60)
    print("M&A Case Study Builder — Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    print("[1/4] Loading M&A data...")
    mna_df = load_mna_data(INPUT_FILE)
    if mna_df is None:
        return

    print("[2/4] Analyzing deals...")
    case_studies = []
    for _, deal in mna_df.iterrows():
        cs = analyze_deal(deal)
        case_studies.append(cs)
    cs_df = pd.DataFrame(case_studies)
    print(f"  [OK] Analyzed {len(cs_df)} deals")

    print("[3/4] Generating text summaries...")
    text_summary = generate_text_summary(cs_df)

    print("[4/4] Saving outputs...")
    save_outputs(cs_df, text_summary)

    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Deals analyzed: {len(cs_df)}")
    print(f"  Size tiers: {cs_df['size_tier'].value_counts().to_dict()}")
    print(f"  Avg research relevance: {cs_df['research_relevance_score'].mean():.1f}/10")
    print(f"  Top 3 by relevance:")
    top3 = cs_df.nlargest(3, "research_relevance_score")
    for _, row in top3.iterrows():
        print(f"    {row['deal_name']} — {row['research_relevance_score']}/10")
    print("=" * 60)


if __name__ == "__main__":
    main()
