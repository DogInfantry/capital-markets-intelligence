"""
Research Memo Generator
Generates 4 application-ready research memos for the Capital Markets Intelligence Platform.
Outputs: output/memos/*.txt
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC = os.path.join(BASE_DIR, "data", "processed")
MEMO_DIR = os.path.join(BASE_DIR, "output", "memos")


def load_all_data():
    """Load all datasets."""
    data = {}
    data["ipo"] = pd.read_csv(os.path.join(DATA_RAW, "ipo_data_raw.csv"), parse_dates=["ipo_date"])
    data["mna"] = pd.read_csv(os.path.join(DATA_RAW, "mna_data_raw.csv"), parse_dates=["announced_date"])
    data["sovereign"] = pd.read_csv(os.path.join(DATA_RAW, "sovereign_issuance_raw.csv"), parse_dates=["issue_date"])
    data["stress"] = pd.read_csv(os.path.join(DATA_PROC, "stress_test_results.csv"))
    data["cases"] = pd.read_csv(os.path.join(DATA_PROC, "case_studies.csv"))
    return data


def memo_gs_gir(data):
    """GS-GIR: Weekly Capital Markets Snapshot."""
    ipo = data["ipo"]
    mna = data["mna"]
    sovereign = data["sovereign"]

    # IPO stats
    ipo_count = len(ipo)
    avg_first_day = ipo["first_day_return_pct"].mean()
    median_first_day = ipo["first_day_return_pct"].median()
    positive_pct = (ipo["first_day_return_pct"] > 0).mean() * 100
    total_raised = ipo["deal_size_usd"].sum() / 1e9
    top_ipo = ipo.loc[ipo["deal_size_usd"].idxmax()]

    # M&A stats
    mna_count = len(mna)
    total_mna_val = mna["deal_value_usd_bn"].sum()
    completed = (mna["status"] == "Completed").sum()
    blocked = mna["status"].str.contains("Blocked").sum()
    cross_border = mna["cross_border"].sum()

    # Sovereign stats
    sov_total = sovereign["issue_size_usd_bn"].sum()
    sov_countries = sovereign["country"].nunique()

    lines = []
    lines.append("=" * 70)
    lines.append("GOLDMAN SACHS GLOBAL INVESTMENT RESEARCH")
    lines.append("Weekly Capital Markets Snapshot")
    lines.append(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"Global capital markets activity remains elevated. Our tracking database")
    lines.append(f"covers {ipo_count} IPOs raising ${total_raised:.1f}B, {mna_count} M&A transactions")
    lines.append(f"totaling ${total_mna_val:.1f}B, and ${sov_total:.1f}B in sovereign issuance across")
    lines.append(f"{sov_countries} countries. Key themes: (1) tech IPOs driving first-day")
    lines.append(f"outperformance, (2) energy sector M&A consolidation, (3) elevated")
    lines.append(f"regulatory intervention blocking cross-border deals.")
    lines.append("")

    lines.append("I. IPO MARKET REVIEW")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"  Pipeline:           {ipo_count} IPOs tracked across {ipo['country'].nunique()} countries")
    lines.append(f"  Capital Raised:     ${total_raised:.1f}B")
    lines.append(f"  Avg First-Day Pop:  {avg_first_day:.1f}% (median: {median_first_day:.1f}%)")
    lines.append(f"  Positive Returns:   {positive_pct:.0f}% of IPOs priced above offer")
    lines.append(f"  Largest IPO:        {top_ipo['company']} (${top_ipo['deal_size_usd']/1e9:.1f}B)")
    lines.append("")
    lines.append("  Notable IPOs:")

    top5 = ipo.nlargest(5, "deal_size_usd")
    for _, row in top5.iterrows():
        lines.append(f"    - {row['company']} ({row['ticker']}): ${row['deal_size_usd']/1e9:.1f}B,")
        lines.append(f"      first-day return {row['first_day_return_pct']:+.1f}%, led by {row['lead_underwriter']}")
    lines.append("")

    lines.append("  Sector Breakdown:")
    sector_counts = ipo["sector"].value_counts().head(5)
    for sector, count in sector_counts.items():
        avg_ret = ipo[ipo["sector"] == sector]["first_day_return_pct"].mean()
        lines.append(f"    - {sector}: {count} IPOs (avg return: {avg_ret:+.1f}%)")
    lines.append("")

    # Underwriter league table
    lines.append("  Underwriter League Table (by deal count involvement):")
    all_underwriters = []
    for uw in ipo["lead_underwriter"]:
        for u in str(uw).split("/"):
            all_underwriters.append(u.strip())
    uw_counts = pd.Series(all_underwriters).value_counts().head(5)
    for uw, count in uw_counts.items():
        lines.append(f"    {count:2d} deals  {uw}")
    lines.append("")

    lines.append("II. M&A DEAL FLOW")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"  Deals Tracked:      {mna_count}")
    lines.append(f"  Total Deal Value:   ${total_mna_val:.1f}B")
    lines.append(f"  Avg Deal Size:      ${mna['deal_value_usd_bn'].mean():.1f}B")
    lines.append(f"  Completed:          {completed} ({completed/mna_count*100:.0f}%)")
    lines.append(f"  Blocked:            {blocked} (regulatory intervention)")
    lines.append(f"  Cross-Border:       {cross_border}")
    lines.append("")
    lines.append("  Top 5 Deals by Value:")
    top5_mna = mna.nlargest(5, "deal_value_usd_bn")
    for _, row in top5_mna.iterrows():
        lines.append(f"    - {row['acquirer']} / {row['target']}: ${row['deal_value_usd_bn']:.1f}B")
        lines.append(f"      {row['deal_type']} | {row['status']} | {row['sector']}")
    lines.append("")

    lines.append("  Regulatory Watch:")
    blocked_deals = mna[mna["status"].str.contains("Blocked|Pending", na=False)]
    for _, row in blocked_deals.iterrows():
        lines.append(f"    - {row['acquirer']} / {row['target']} ({row['status']})")
        lines.append(f"      {row['strategic_rationale']}")
    lines.append("")

    lines.append("III. SOVEREIGN ISSUANCE OVERVIEW")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"  Total Issuance:     ${sov_total:.1f}B across {sov_countries} countries")
    lines.append(f"  USD-Denominated:    {sovereign['is_usd_denominated'].sum()} issuances")
    lines.append(f"  Avg Yield:          {sovereign['yield_at_issue_pct'].mean():.2f}%")
    lines.append("")
    lines.append("  Largest Issuances:")
    top5_sov = sovereign.nlargest(5, "issue_size_usd_bn")
    for _, row in top5_sov.iterrows():
        lines.append(f"    - {row['country']}: ${row['issue_size_usd_bn']:.1f}B {row['bond_type']}")
        lines.append(f"      {row['maturity_years']}Y at {row['yield_at_issue_pct']:.2f}% ({row['rating_sp']})")
    lines.append("")

    lines.append("IV. MARKET OUTLOOK & RISK FACTORS")
    lines.append("-" * 70)
    lines.append("")
    lines.append("  Constructive Signals:")
    lines.append("    - IPO first-day returns remain positive, signaling healthy demand")
    lines.append("    - M&A completions outpace blockages 4:1")
    lines.append("    - EM sovereign issuance access maintained despite spread widening")
    lines.append("")
    lines.append("  Risk Factors:")
    lines.append("    - Regulatory intervention rising (CFIUS, DOJ antitrust)")
    lines.append("    - EM currency volatility could disrupt issuance calendars")
    lines.append("    - Rate path uncertainty affecting IPO pricing decisions")
    lines.append("    - Geopolitical risk premium in cross-border M&A")
    lines.append("")
    lines.append("=" * 70)
    lines.append("CONFIDENTIAL | For Internal Distribution Only")
    lines.append("Capital Markets Intelligence Platform")
    lines.append("=" * 70)

    return "\n".join(lines)


def memo_de_shaw(data):
    """D.E. Shaw: IPO Performance Dashboard."""
    ipo = data["ipo"]

    # Statistical analysis
    first_day = ipo["first_day_return_pct"]
    total_ret = ipo["total_return_pct"]

    lines = []
    lines.append("=" * 70)
    lines.append("D.E. SHAW GROUP — CAPITAL MARKETS RESEARCH")
    lines.append("IPO Performance Dashboard & Quantitative Analysis")
    lines.append(f"Report Date: {datetime.now().strftime('%B %d, %Y')}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("I. STATISTICAL SUMMARY")
    lines.append("-" * 70)
    lines.append("")
    lines.append("  First-Day Returns:")
    lines.append(f"    Mean:               {first_day.mean():+.2f}%")
    lines.append(f"    Median:             {first_day.median():+.2f}%")
    lines.append(f"    Std Dev:            {first_day.std():.2f}%")
    lines.append(f"    Skewness:           {first_day.skew():.3f}")
    lines.append(f"    Kurtosis:           {first_day.kurtosis():.3f}")
    lines.append(f"    Min:                {first_day.min():+.2f}% ({ipo.loc[first_day.idxmin(), 'ticker']})")
    lines.append(f"    Max:                {first_day.max():+.2f}% ({ipo.loc[first_day.idxmax(), 'ticker']})")
    lines.append(f"    % Positive:         {(first_day > 0).mean()*100:.1f}%")
    lines.append(f"    % > +20%:           {(first_day > 20).mean()*100:.1f}%")
    lines.append("")
    lines.append("  Total Returns (to date):")
    lines.append(f"    Mean:               {total_ret.mean():+.2f}%")
    lines.append(f"    Median:             {total_ret.median():+.2f}%")
    lines.append(f"    Std Dev:            {total_ret.std():.2f}%")
    lines.append(f"    % Positive:         {(total_ret > 0).mean()*100:.1f}%")
    lines.append(f"    Sharpe Proxy:       {total_ret.mean() / total_ret.std():.3f}")
    lines.append("")

    lines.append("II. RETURN DISTRIBUTION ANALYSIS")
    lines.append("-" * 70)
    lines.append("")
    lines.append("  First-Day Return Quintiles:")
    quintiles = first_day.quantile([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    for q, v in quintiles.items():
        lines.append(f"    P{int(q*100):3d}:  {v:+.2f}%")
    lines.append("")

    lines.append("  Performance Buckets:")
    buckets = [
        ("< -10%", (first_day < -10).sum()),
        ("-10% to 0%", ((first_day >= -10) & (first_day < 0)).sum()),
        ("0% to +10%", ((first_day >= 0) & (first_day < 10)).sum()),
        ("+10% to +25%", ((first_day >= 10) & (first_day < 25)).sum()),
        ("+25% to +50%", ((first_day >= 25) & (first_day < 50)).sum()),
        ("> +50%", (first_day >= 50).sum()),
    ]
    for label, count in buckets:
        pct = count / len(ipo) * 100
        bar = "#" * int(pct / 2)
        lines.append(f"    {label:>15s}: {count:2d} ({pct:4.1f}%)  {bar}")
    lines.append("")

    lines.append("III. TOP & BOTTOM PERFORMERS")
    lines.append("-" * 70)
    lines.append("")
    lines.append("  Top 5 First-Day Returns:")
    top5 = ipo.nlargest(5, "first_day_return_pct")
    for i, (_, row) in enumerate(top5.iterrows(), 1):
        lines.append(f"    {i}. {row['ticker']:>8s}  {row['first_day_return_pct']:+6.1f}%  "
                     f"${row['deal_size_usd']/1e9:.1f}B  {row['sector']}")
    lines.append("")
    lines.append("  Bottom 5 First-Day Returns:")
    bot5 = ipo.nsmallest(5, "first_day_return_pct")
    for i, (_, row) in enumerate(bot5.iterrows(), 1):
        lines.append(f"    {i}. {row['ticker']:>8s}  {row['first_day_return_pct']:+6.1f}%  "
                     f"${row['deal_size_usd']/1e9:.1f}B  {row['sector']}")
    lines.append("")

    lines.append("  Top 5 Total Returns:")
    top5_total = ipo.nlargest(5, "total_return_pct")
    for i, (_, row) in enumerate(top5_total.iterrows(), 1):
        lines.append(f"    {i}. {row['ticker']:>8s}  {row['total_return_pct']:+6.1f}%  "
                     f"First-day: {row['first_day_return_pct']:+.1f}%  {row['sector']}")
    lines.append("")

    lines.append("IV. UNDERWRITER LEAGUE TABLE")
    lines.append("-" * 70)
    lines.append("")
    all_underwriters = []
    for _, row in ipo.iterrows():
        for u in str(row["lead_underwriter"]).split("/"):
            all_underwriters.append({"underwriter": u.strip(), "deal_size": row["deal_size_usd"], "first_day_ret": row["first_day_return_pct"]})
    uw_df = pd.DataFrame(all_underwriters)
    uw_summary = uw_df.groupby("underwriter").agg(
        deals=("underwriter", "count"),
        total_volume=("deal_size", "sum"),
        avg_return=("first_day_ret", "mean"),
    ).sort_values("total_volume", ascending=False).head(8)
    lines.append(f"  {'Underwriter':<35s} {'Deals':>5s} {'Volume ($B)':>11s} {'Avg Ret':>8s}")
    lines.append(f"  {'─'*35} {'─'*5} {'─'*11} {'─'*8}")
    for uw, row in uw_summary.iterrows():
        lines.append(f"  {uw:<35s} {int(row['deals']):>5d} {row['total_volume']/1e9:>10.1f}  {row['avg_return']:>+7.1f}%")
    lines.append("")

    lines.append("V. GEOGRAPHIC ANALYSIS")
    lines.append("-" * 70)
    lines.append("")
    geo = ipo.groupby("country").agg(
        count=("company", "count"),
        total_raised=("deal_size_usd", "sum"),
        avg_first_day=("first_day_return_pct", "mean"),
    ).sort_values("total_raised", ascending=False)
    lines.append(f"  {'Country':<20s} {'IPOs':>4s} {'Raised ($B)':>11s} {'Avg Ret':>8s}")
    lines.append(f"  {'─'*20} {'─'*4} {'─'*11} {'─'*8}")
    for country, row in geo.iterrows():
        lines.append(f"  {country:<20s} {int(row['count']):>4d} {row['total_raised']/1e9:>10.1f}  {row['avg_first_day']:>+7.1f}%")
    lines.append("")

    lines.append("VI. SIGNAL OBSERVATIONS")
    lines.append("-" * 70)
    lines.append("")
    # Correlation between deal size and returns
    corr = ipo["deal_size_usd"].corr(ipo["first_day_return_pct"])
    lines.append(f"  Deal Size vs First-Day Return Correlation: {corr:.3f}")
    if corr < -0.2:
        lines.append("    -> Negative correlation suggests larger IPOs are priced more efficiently")
    elif corr > 0.2:
        lines.append("    -> Positive correlation suggests larger IPOs attract stronger demand")
    else:
        lines.append("    -> Weak correlation — deal size is not a strong predictor of first-day pop")
    lines.append("")

    # First-day vs total return persistence
    persistence = ipo["first_day_return_pct"].corr(ipo["total_return_pct"])
    lines.append(f"  First-Day vs Total Return Correlation: {persistence:.3f}")
    if persistence > 0.3:
        lines.append("    -> Moderate persistence — first-day winners tend to maintain gains")
    else:
        lines.append("    -> Low persistence — first-day pop is not predictive of long-term returns")
    lines.append("")

    lines.append("=" * 70)
    lines.append("CONFIDENTIAL | D.E. Shaw Capital Markets Research")
    lines.append("=" * 70)

    return "\n".join(lines)


def memo_jpm_sovereign(data):
    """JPM: Sovereign Risk & Capital Issuance Model."""
    stress = data["stress"]
    sovereign = data["sovereign"]

    lines = []
    lines.append("=" * 70)
    lines.append("J.P. MORGAN — COUNTRY RISK ADVISORY")
    lines.append("Sovereign Risk & Capital Issuance Model")
    lines.append(f"Report Date: {datetime.now().strftime('%B %d, %Y')}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("I. SOVEREIGN BASELINE OVERVIEW")
    lines.append("-" * 70)
    lines.append("")
    baseline = stress[stress["scenario"] == "Base Case"]
    lines.append(f"  {'Country':<18s} {'Rating':>6s} {'10Y Yld':>7s} {'Debt/GDP':>8s} {'GDP Gr':>6s} {'Infl':>5s}")
    lines.append(f"  {'─'*18} {'─'*6} {'─'*7} {'─'*8} {'─'*6} {'─'*5}")
    for _, row in baseline.iterrows():
        lines.append(f"  {row['country']:<18s} {row['rating_sp']:>6s} {row['ten_yr_yield_pct']:>6.2f}% "
                     f"{row['debt_to_gdp_pct']:>7.0f}% {row['gdp_growth_pct']:>+5.1f}% {row['inflation_pct']:>4.1f}%")
    lines.append("")

    lines.append("II. STRESS SCENARIO DEFINITIONS")
    lines.append("-" * 70)
    lines.append("")
    scenarios = stress[stress["scenario"] != "Base Case"]["scenario"].unique()
    scenario_desc = stress[stress["scenario"] != "Base Case"].groupby("scenario")["scenario_description"].first()
    for scenario in scenarios:
        lines.append(f"  {scenario}")
        lines.append(f"    {scenario_desc[scenario]}")
        lines.append("")

    lines.append("III. VULNERABILITY ASSESSMENT")
    lines.append("-" * 70)
    lines.append("")
    avg_risk = (
        stress[stress["scenario"] != "Base Case"]
        .groupby("country")["risk_score"]
        .agg(["mean", "max"])
        .sort_values("mean", ascending=False)
    )
    lines.append(f"  {'Country':<18s} {'Avg Risk':>8s} {'Max Risk':>8s} {'Assessment'}")
    lines.append(f"  {'─'*18} {'─'*8} {'─'*8} {'─'*25}")
    for country, row in avg_risk.iterrows():
        if row["mean"] > 50:
            assessment = "HIGH VULNERABILITY"
        elif row["mean"] > 25:
            assessment = "MODERATE VULNERABILITY"
        elif row["mean"] > 15:
            assessment = "LOW-MODERATE RISK"
        else:
            assessment = "LOW RISK"
        lines.append(f"  {country:<18s} {row['mean']:>7.1f}  {row['max']:>7.1f}  {assessment}")
    lines.append("")

    lines.append("IV. SCENARIO-BY-SCENARIO ANALYSIS")
    lines.append("-" * 70)
    lines.append("")
    for scenario in scenarios:
        subset = stress[stress["scenario"] == scenario]
        top3 = subset.nlargest(3, "risk_score")
        bottom3 = subset.nsmallest(3, "risk_score")
        lines.append(f"  {scenario}")
        lines.append(f"  {'.' * 60}")
        lines.append(f"    Most Affected:")
        for _, row in top3.iterrows():
            lines.append(f"      {row['country']}: risk score {row['risk_score']:.0f}, "
                         f"yield {row['ten_yr_yield_pct']:.2f}% -> {row['stressed_yield_pct']:.2f}%")
        lines.append(f"    Least Affected:")
        for _, row in bottom3.iterrows():
            lines.append(f"      {row['country']}: risk score {row['risk_score']:.0f}")
        lines.append("")

    lines.append("V. SOVEREIGN ISSUANCE ACTIVITY")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"  Total Issuance Tracked:  ${sovereign['issue_size_usd_bn'].sum():.1f}B")
    lines.append(f"  Countries:               {sovereign['country'].nunique()}")
    lines.append(f"  Investment Grade:        {sovereign['investment_grade'].sum()} issuances")
    lines.append(f"  High Yield:              {(~sovereign['investment_grade']).sum()} issuances")
    lines.append("")

    lines.append("  Issuance by Region:")
    region_vol = sovereign.groupby("region")["issue_size_usd_bn"].sum().sort_values(ascending=False)
    for region, vol in region_vol.items():
        lines.append(f"    {region:<20s}: ${vol:.1f}B")
    lines.append("")

    lines.append("  EM Sovereign Spread Monitor (vs UST 10Y):")
    em_issuances = sovereign[sovereign["spread_over_ust_bps"] > 0].sort_values("spread_over_ust_bps", ascending=False)
    for _, row in em_issuances.head(8).iterrows():
        lines.append(f"    {row['country']:<18s} {row['bond_type']:<25s} +{row['spread_over_ust_bps']:.0f}bps  ({row['rating_sp']})")
    lines.append("")

    lines.append("VI. POLICY IMPLICATIONS & RECOMMENDATIONS")
    lines.append("-" * 70)
    lines.append("")
    lines.append("  1. EM Currency Crisis is the highest-risk tail scenario. Countries with")
    lines.append("     large external financing needs (Turkey, South Africa, Brazil) are")
    lines.append("     most exposed. Monitor FX reserves and current account balances.")
    lines.append("")
    lines.append("  2. Fed hawkishness transmits globally through the USD channel.")
    lines.append("     DM sovereigns face manageable yield increases; EM sovereigns face")
    lines.append("     amplified capital outflow risk.")
    lines.append("")
    lines.append("  3. Oil shock creates winner/loser divergence: Saudi Arabia and US")
    lines.append("     benefit; India, Japan, and Turkey face stagflation pressure.")
    lines.append("")
    lines.append("  4. Global recession scenario shows classic flight-to-quality:")
    lines.append("     US, Germany, and Japan yields fall while EM spreads widen.")
    lines.append("")
    lines.append("=" * 70)
    lines.append("CONFIDENTIAL | J.P. Morgan Country Risk Advisory")
    lines.append("=" * 70)

    return "\n".join(lines)


def memo_pwc_db(data):
    """PwC/DB: M&A Strategic Rationale Case Studies."""
    cases = data["cases"]
    mna = data["mna"]

    lines = []
    lines.append("=" * 70)
    lines.append("PwC DEALS STRATEGY / DEUTSCHE BANK ADVISORY")
    lines.append("M&A Strategic Rationale: Case Studies & Thematic Analysis")
    lines.append(f"Report Date: {datetime.now().strftime('%B %d, %Y')}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("I. DEAL UNIVERSE OVERVIEW")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"  Deals Analyzed:     {len(cases)}")
    lines.append(f"  Total Deal Value:   ${cases['deal_value_usd_bn'].sum():.1f}B")
    lines.append(f"  Avg Deal Size:      ${cases['deal_value_usd_bn'].mean():.1f}B")
    lines.append(f"  Cross-Border:       {cases['cross_border'].sum()}")
    lines.append("")

    lines.append("  Size Distribution:")
    tier_counts = cases["size_tier"].value_counts()
    for tier, count in tier_counts.items():
        tier_value = cases[cases["size_tier"] == tier]["deal_value_usd_bn"].sum()
        lines.append(f"    {tier:<30s}: {count:2d} deals (${tier_value:.1f}B)")
    lines.append("")

    lines.append("II. TOP 5 DEALS — DEEP DIVE")
    lines.append("-" * 70)
    top5 = cases.nlargest(5, "research_relevance_score")
    for i, (_, cs) in enumerate(top5.iterrows(), 1):
        lines.append("")
        lines.append(f"  {'='*60}")
        lines.append(f"  DEAL #{i}: {cs['deal_name']}")
        lines.append(f"  {'='*60}")
        lines.append(f"  Deal Value:        ${cs['deal_value_usd_bn']:.1f}B")
        lines.append(f"  Announced:         {cs['announced_date']}")
        lines.append(f"  Deal Type:         {cs['deal_type']}")
        lines.append(f"  Sector:            {cs['sector']}")
        lines.append(f"  Size Tier:         {cs['size_tier']}")
        lines.append(f"  Status:            {cs['status']}")
        lines.append(f"  Cross-Border:      {'Yes' if cs['cross_border'] else 'No'}")
        lines.append(f"  Relevance Score:   {cs['research_relevance_score']}/10")
        lines.append(f"")
        lines.append(f"  Strategic Rationale:")
        lines.append(f"    {cs['strategic_rationale']}")
        lines.append(f"")
        lines.append(f"  Value Creation Drivers:")
        for driver in str(cs["value_drivers"]).split("; "):
            lines.append(f"    * {driver}")
        lines.append(f"")
        lines.append(f"  Risk Assessment:")
        for risk in str(cs["risk_factors"]).split("; "):
            lines.append(f"    ! {risk}")
    lines.append("")

    lines.append("III. THEMATIC ANALYSIS")
    lines.append("-" * 70)
    lines.append("")

    # Deal type analysis
    lines.append("  A. Deal Structure Trends")
    lines.append("")
    deal_types = mna["deal_type"].value_counts()
    for dt, count in deal_types.items():
        avg_val = mna[mna["deal_type"] == dt]["deal_value_usd_bn"].mean()
        lines.append(f"    {dt:<30s}: {count:2d} deals (avg ${avg_val:.1f}B)")
    lines.append("")

    # Sector concentration
    lines.append("  B. Sector Concentration")
    lines.append("")
    sector_vol = mna.groupby("sector")["deal_value_usd_bn"].sum().sort_values(ascending=False)
    total_vol = sector_vol.sum()
    cumulative = 0
    for sector, vol in sector_vol.head(5).items():
        cumulative += vol
        lines.append(f"    {sector:<40s}: ${vol:5.1f}B ({vol/total_vol*100:4.1f}%, cum: {cumulative/total_vol*100:.1f}%)")
    lines.append("")

    # Regulatory landscape
    lines.append("  C. Regulatory Landscape")
    lines.append("")
    lines.append("  The regulatory environment has become a material factor in deal")
    lines.append("  completion. Our database shows:")
    completed = (mna["status"] == "Completed").sum()
    pending = mna["status"].str.contains("Pending", na=False).sum()
    blocked = mna["status"].str.contains("Blocked", na=False).sum()
    lines.append(f"    Completed:          {completed} ({completed/len(mna)*100:.0f}%)")
    lines.append(f"    Pending Regulatory: {pending} ({pending/len(mna)*100:.0f}%)")
    lines.append(f"    Blocked:            {blocked} ({blocked/len(mna)*100:.0f}%)")
    lines.append("")
    lines.append("  Blocked Deals:")
    blocked_deals = mna[mna["status"].str.contains("Blocked", na=False)]
    for _, deal in blocked_deals.iterrows():
        lines.append(f"    - {deal['acquirer']} / {deal['target']} ({deal['status']})")
        lines.append(f"      Value: ${deal['deal_value_usd_bn']:.1f}B | Rationale: {deal['strategic_rationale']}")
    lines.append("")

    # Cross-border analysis
    lines.append("  D. Cross-Border Deal Dynamics")
    lines.append("")
    cb = mna[mna["cross_border"] == True]
    if len(cb) > 0:
        lines.append(f"    Cross-border deals: {len(cb)} ({len(cb)/len(mna)*100:.0f}% of universe)")
        lines.append(f"    Avg deal size: ${cb['deal_value_usd_bn'].mean():.1f}B vs ${mna['deal_value_usd_bn'].mean():.1f}B overall")
        lines.append("")
        for _, deal in cb.iterrows():
            lines.append(f"    - {deal['acquirer']} ({deal['acquirer_country']}) -> "
                         f"{deal['target']} ({deal['target_country']})")
            lines.append(f"      ${deal['deal_value_usd_bn']:.1f}B | {deal['status']}")
    lines.append("")

    # Value driver analysis
    lines.append("  E. Value Creation Framework")
    lines.append("")
    all_drivers = []
    for drivers in cases["value_drivers"]:
        for d in str(drivers).split("; "):
            all_drivers.append(d.strip())
    driver_counts = pd.Series(all_drivers).value_counts()
    lines.append("  Most Common Value Drivers:")
    for driver, count in driver_counts.items():
        pct = count / len(cases) * 100
        lines.append(f"    {driver:<30s}: {count:2d} deals ({pct:.0f}%)")
    lines.append("")

    lines.append("IV. STRATEGIC RECOMMENDATIONS")
    lines.append("-" * 70)
    lines.append("")
    lines.append("  1. Energy sector consolidation continues to drive mega-deal activity.")
    lines.append("     Expect further Permian Basin and shale asset consolidation in 2025.")
    lines.append("")
    lines.append("  2. Technology M&A faces heightened regulatory scrutiny. AI/cybersecurity")
    lines.append("     deals draw particular attention from DOJ and international regulators.")
    lines.append("")
    lines.append("  3. PE-backed take-privates remain a viable exit path, particularly in")
    lines.append("     fintech and healthcare where public market valuations are compressed.")
    lines.append("")
    lines.append("  4. Cross-border deals require extended timeline assumptions. CFIUS review")
    lines.append("     and national security considerations are no longer edge cases.")
    lines.append("")
    lines.append("  5. Healthcare/pharma M&A is driven by pipeline acquisition rather than")
    lines.append("     operational synergies — focus due diligence on clinical risk.")
    lines.append("")
    lines.append("=" * 70)
    lines.append("CONFIDENTIAL | PwC Deals Strategy / Deutsche Bank Advisory")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_memo(text, filename):
    """Save memo to file."""
    filepath = os.path.join(MEMO_DIR, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    line_count = text.count("\n") + 1
    print(f"  [OK] {filename} ({line_count} lines)")


def main():
    print("=" * 60)
    print("Research Memo Generator - Capital Markets Intelligence")
    print("=" * 60)
    print()

    print("[1/2] Loading data...")
    data = load_all_data()
    for name, df in data.items():
        print(f"  [OK] {name}: {len(df)} rows")

    print("[2/2] Generating memos...")
    save_memo(memo_gs_gir(data), "gs_gir_weekly_snapshot.txt")
    save_memo(memo_de_shaw(data), "de_shaw_ipo_dashboard.txt")
    save_memo(memo_jpm_sovereign(data), "jpm_sovereign_risk_model.txt")
    save_memo(memo_pwc_db(data), "pwc_db_mna_case_studies.txt")

    print()
    print("=" * 60)
    memos = [f for f in os.listdir(MEMO_DIR) if f.endswith(".txt")]
    print(f"Generated {len(memos)} research memos in output/memos/:")
    for m in sorted(memos):
        size = os.path.getsize(os.path.join(MEMO_DIR, m))
        print(f"  - {m} ({size:,} bytes)")
    print("=" * 60)


if __name__ == "__main__":
    main()
