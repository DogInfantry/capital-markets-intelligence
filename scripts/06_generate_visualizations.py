"""
Visualization Generator
Generates all charts for the Capital Markets Intelligence Platform.
Outputs: output/*.png (10 charts)
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Paths
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC = os.path.join(BASE_DIR, "data", "processed")

# Style
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.dpi": 150,
})

COLORS = {
    "green": "#2ecc71",
    "red": "#e74c3c",
    "blue": "#3498db",
    "orange": "#e67e22",
    "purple": "#9b59b6",
    "dark_red": "#c0392b",
    "yellow": "#f39c12",
    "teal": "#1abc9c",
}


def load_all_data():
    """Load all datasets."""
    print("  Loading datasets...")
    data = {}
    data["ipo"] = pd.read_csv(os.path.join(DATA_RAW, "ipo_data_raw.csv"), parse_dates=["ipo_date"])
    data["mna"] = pd.read_csv(os.path.join(DATA_RAW, "mna_data_raw.csv"), parse_dates=["announced_date"])
    data["stress"] = pd.read_csv(os.path.join(DATA_PROC, "stress_test_results.csv"))
    data["cases"] = pd.read_csv(os.path.join(DATA_PROC, "case_studies.csv"))
    data["sovereign"] = pd.read_csv(os.path.join(DATA_RAW, "sovereign_issuance_raw.csv"), parse_dates=["issue_date"])
    for name, df in data.items():
        print(f"    [OK] {name}: {len(df)} rows")
    return data


def chart_01_ipo_first_day_returns(ipo_df):
    """Bar chart: IPO first-day returns by company."""
    fig, ax = plt.subplots(figsize=(14, 7))
    sorted_df = ipo_df.sort_values("first_day_return_pct", ascending=True)
    colors = [COLORS["green"] if x > 0 else COLORS["red"] for x in sorted_df["first_day_return_pct"]]
    bars = ax.barh(sorted_df["ticker"], sorted_df["first_day_return_pct"], color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title("IPO First-Day Returns (%)", fontweight="bold")
    ax.set_xlabel("Return (%)")
    ax.axvline(x=0, color="black", linewidth=0.8)
    avg = ipo_df["first_day_return_pct"].mean()
    ax.axvline(x=avg, color=COLORS["blue"], linewidth=1.5, linestyle="--", label=f"Avg: {avg:.1f}%")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "ipo_first_day_returns.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] ipo_first_day_returns.png")


def chart_02_ipo_total_returns(ipo_df):
    """Bar chart: IPO total returns to date."""
    fig, ax = plt.subplots(figsize=(14, 7))
    sorted_df = ipo_df.sort_values("total_return_pct", ascending=True)
    colors = [COLORS["green"] if x > 0 else COLORS["red"] for x in sorted_df["total_return_pct"]]
    ax.barh(sorted_df["ticker"], sorted_df["total_return_pct"], color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title("IPO Total Returns to Date (%)", fontweight="bold")
    ax.set_xlabel("Return (%)")
    ax.axvline(x=0, color="black", linewidth=0.8)
    median = ipo_df["total_return_pct"].median()
    ax.axvline(x=median, color=COLORS["orange"], linewidth=1.5, linestyle="--", label=f"Median: {median:.1f}%")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "ipo_total_returns.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] ipo_total_returns.png")


def chart_03_ipo_by_sector(ipo_df):
    """Horizontal bar: IPO deal size by sector."""
    fig, ax = plt.subplots(figsize=(12, 8))
    sector_data = ipo_df.groupby("sector").agg(
        total_size=("deal_size_usd", "sum"),
        count=("company", "count"),
    ).sort_values("total_size", ascending=True)
    sector_data["total_size_bn"] = sector_data["total_size"] / 1e9
    ax.barh(sector_data.index, sector_data["total_size_bn"], color=COLORS["blue"], edgecolor="white", linewidth=0.5)
    ax.set_title("IPO Deal Size by Sector ($B)", fontweight="bold")
    ax.set_xlabel("Total Deal Size ($B)")
    for i, (idx, row) in enumerate(sector_data.iterrows()):
        ax.text(row["total_size_bn"] + 0.1, i, f'{int(row["count"])} deals', va="center", fontsize=9, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "ipo_by_sector.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] ipo_by_sector.png")


def chart_04_mna_by_sector(mna_df):
    """Horizontal bar: M&A deal value by sector."""
    fig, ax = plt.subplots(figsize=(12, 8))
    sector_deals = mna_df.groupby("sector")["deal_value_usd_bn"].sum().sort_values(ascending=True)
    ax.barh(sector_deals.index, sector_deals.values, color=COLORS["teal"], edgecolor="white", linewidth=0.5)
    ax.set_title("M&A Deal Value by Sector ($B)", fontweight="bold")
    ax.set_xlabel("Deal Value ($B)")
    for i, (sector, val) in enumerate(sector_deals.items()):
        ax.text(val + 0.3, i, f"${val:.1f}B", va="center", fontsize=9, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mna_by_sector.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] mna_by_sector.png")


def chart_05_mna_deal_status(mna_df):
    """Bar chart: M&A deal status breakdown."""
    fig, ax = plt.subplots(figsize=(8, 5))
    status_counts = mna_df["status"].value_counts()
    color_map = {
        "Completed": COLORS["green"],
        "Pending Regulatory": COLORS["yellow"],
        "Blocked (DOJ)": COLORS["red"],
        "Blocked (CFIUS)": COLORS["dark_red"],
    }
    colors = [color_map.get(s, "#95a5a6") for s in status_counts.index]
    bars = ax.bar(status_counts.index, status_counts.values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title("M&A Deal Status", fontweight="bold")
    ax.set_ylabel("Number of Deals")
    for bar, val in zip(bars, status_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(val), ha="center", fontweight="bold")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mna_deal_status.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] mna_deal_status.png")


def chart_06_risk_heatmap(stress_df):
    """Heatmap: sovereign risk scores by scenario and country."""
    fig, ax = plt.subplots(figsize=(14, 8))
    heatmap_data = stress_df.pivot_table(index="country", columns="scenario", values="risk_score")
    sns.heatmap(
        heatmap_data, annot=True, fmt=".0f", cmap="RdYlGn_r", ax=ax,
        linewidths=0.5, cbar_kws={"label": "Risk Score"},
        annot_kws={"fontsize": 10},
    )
    ax.set_title("Sovereign Risk Scores by Scenario", fontweight="bold", fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "risk_heatmap.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] risk_heatmap.png")


def chart_07_yield_impact(stress_df):
    """2x2 subplot: yield changes under each stress scenario."""
    stress_df["yield_change_bps"] = (stress_df["stressed_yield_pct"] - stress_df["ten_yr_yield_pct"]) * 100
    scenarios = [s for s in stress_df["scenario"].unique() if s != "Base Case"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for ax, scenario in zip(axes.flatten(), scenarios):
        subset = stress_df[stress_df["scenario"] == scenario].sort_values("yield_change_bps")
        colors = [COLORS["red"] if x > 0 else COLORS["green"] for x in subset["yield_change_bps"]]
        ax.barh(subset["country"], subset["yield_change_bps"], color=colors, edgecolor="white", linewidth=0.5)
        ax.set_title(scenario, fontsize=10, fontweight="bold")
        ax.set_xlabel("Yield Change (bps)")
        ax.axvline(x=0, color="black", linewidth=0.5)

    plt.suptitle("10Y Yield Impact by Stress Scenario", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "yield_impact.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] yield_impact.png")


def chart_08_vulnerability_ranking(stress_df):
    """Bar chart: average risk score ranking across scenarios."""
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_risk = (
        stress_df[stress_df["scenario"] != "Base Case"]
        .groupby("country")["risk_score"]
        .mean()
        .sort_values(ascending=False)
    )
    gradient = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(avg_risk)))
    ax.bar(avg_risk.index, avg_risk.values, color=gradient, edgecolor="white", linewidth=0.5)
    ax.set_title("Sovereign Vulnerability Ranking (Avg Risk Across Stress Scenarios)", fontweight="bold")
    ax.set_ylabel("Average Risk Score")
    for i, (country, score) in enumerate(avg_risk.items()):
        ax.text(i, score + 0.5, f"{score:.0f}", ha="center", fontsize=9, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "vulnerability_ranking.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] vulnerability_ranking.png")


def chart_09_deal_size_distribution(cases_df):
    """Horizontal bar: case study deal sizes."""
    fig, ax = plt.subplots(figsize=(12, 9))
    sorted_cs = cases_df.sort_values("deal_value_usd_bn", ascending=True)
    tier_colors = {
        "Mega-Deal (>$50B)": COLORS["red"],
        "Large-Cap ($20-50B)": COLORS["orange"],
        "Mid-Cap ($10-20B)": COLORS["blue"],
        "Core Middle Market (<$10B)": COLORS["teal"],
    }
    colors = [tier_colors.get(t, "#95a5a6") for t in sorted_cs["size_tier"]]
    ax.barh(sorted_cs["deal_name"], sorted_cs["deal_value_usd_bn"], color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title("M&A Deal Values ($B) by Size Tier", fontweight="bold")
    ax.set_xlabel("Deal Value ($B)")

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l) for l, c in tier_colors.items()]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "deal_size_distribution.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] deal_size_distribution.png")


def chart_10_research_relevance(cases_df):
    """Horizontal bar: research relevance scores by deal."""
    fig, ax = plt.subplots(figsize=(12, 9))
    ranked = cases_df.sort_values("research_relevance_score", ascending=True)
    colors = [
        COLORS["red"] if s >= 8 else COLORS["orange"] if s >= 6 else COLORS["green"]
        for s in ranked["research_relevance_score"]
    ]
    ax.barh(ranked["deal_name"], ranked["research_relevance_score"], color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title("Research Relevance Score (GS / JPM / DB)", fontweight="bold")
    ax.set_xlabel("Score (1-10)")
    ax.set_xlim(0, 10.5)
    for i, (_, row) in enumerate(ranked.iterrows()):
        ax.text(row["research_relevance_score"] + 0.1, i, f'{row["research_relevance_score"]}', va="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "research_relevance.png"), bbox_inches="tight")
    plt.close()
    print("    [OK] research_relevance.png")


def main():
    print("=" * 60)
    print("Visualization Generator - Capital Markets Intelligence")
    print("=" * 60)
    print()

    print("[1/2] Loading data...")
    data = load_all_data()

    print("[2/2] Generating charts...")
    chart_01_ipo_first_day_returns(data["ipo"])
    chart_02_ipo_total_returns(data["ipo"])
    chart_03_ipo_by_sector(data["ipo"])
    chart_04_mna_by_sector(data["mna"])
    chart_05_mna_deal_status(data["mna"])
    chart_06_risk_heatmap(data["stress"])
    chart_07_yield_impact(data["stress"])
    chart_08_vulnerability_ranking(data["stress"])
    chart_09_deal_size_distribution(data["cases"])
    chart_10_research_relevance(data["cases"])

    # Summary
    pngs = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")]
    print()
    print("=" * 60)
    print(f"Generated {len(pngs)} charts in output/:")
    for p in sorted(pngs):
        print(f"  - {p}")
    print("=" * 60)


if __name__ == "__main__":
    main()
