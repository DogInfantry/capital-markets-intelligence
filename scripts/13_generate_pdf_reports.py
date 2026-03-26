"""
PDF Report Generator
Creates professional PDF research reports using fpdf2.

Outputs:
  output/pdf/gs_gir_capital_markets_snapshot.pdf
  output/pdf/jpm_sovereign_risk_report.pdf
  output/pdf/de_shaw_ipo_dashboard.pdf
  output/pdf/pwc_db_mna_case_studies.pdf
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
PDF_DIR = os.path.join(BASE_DIR, "output", "pdf")


class ReportPDF(FPDF):
    """Custom PDF class with header/footer."""

    def __init__(self, title="", subtitle=""):
        super().__init__()
        self.report_title = title
        self.report_subtitle = subtitle

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, self.report_title, align="L")
        self.cell(0, 5, "CONFIDENTIAL", align="R", ln=1)
        self.set_draw_color(44, 62, 80)
        self.set_line_width(0.5)
        self.line(10, 12, 200, 12)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Capital Markets Intelligence Platform | {datetime.now().strftime('%B %Y')}",
                  align="L")
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="R")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(44, 62, 80)
        self.cell(0, 8, title, ln=1)
        self.set_draw_color(44, 62, 80)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def subsection(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(52, 73, 94)
        self.cell(0, 6, self._sanitize(title), ln=1)
        self.ln(1)

    @staticmethod
    def _sanitize(text):
        """Remove non-latin1 characters for fpdf 1.x compatibility."""
        return str(text).encode("latin-1", errors="replace").decode("latin-1")

    def body_text(self, text):
        text = self._sanitize(text)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 4.5, text)
        self.ln(2)

    def key_value(self, key, value):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(52, 73, 94)
        self.cell(60, 5, self._sanitize(key))
        self.set_font("Helvetica", "", 9)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, self._sanitize(value), ln=1)

    def add_table(self, headers, data, col_widths=None):
        """Add a formatted table."""
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            self.cell(width, 6, self._sanitize(str(header)[:int(width/2)]), border=1, fill=True, align="C")
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in data:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(240, 245, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for val, width in zip(row, col_widths):
                text = self._sanitize(str(val)[:int(width/1.8)]) if val is not None else ""
                self.cell(width, 5, text, border=1, fill=True, align="C")
            self.ln()
            fill = not fill


def load_data():
    data = {}
    files = {
        "ipo": (RAW_DIR, "ipo_data_raw.csv"),
        "mna": (RAW_DIR, "mna_data_raw.csv"),
        "sovereign": (RAW_DIR, "sovereign_issuance_raw.csv"),
        "risk_index": (PROC_DIR, "sovereign_risk_index.csv"),
        "event_study": (PROC_DIR, "ipo_event_study.csv"),
        "screening": (PROC_DIR, "deal_screening_model.csv"),
        "cases": (PROC_DIR, "case_studies.csv"),
        "stress": (PROC_DIR, "stress_test_results.csv"),
        "yc": (PROC_DIR, "yield_curve_analysis.csv"),
    }
    for key, (directory, filename) in files.items():
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            data[key] = pd.read_csv(filepath)
    return data


def pdf_gs_gir(data):
    """GS-GIR Capital Markets Snapshot PDF."""
    print("  [1/4] GS-GIR Capital Markets Snapshot...")

    pdf = ReportPDF("Goldman Sachs | Global Investment Research", "Weekly Capital Markets Snapshot")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title page content
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(44, 62, 80)
    pdf.ln(20)
    pdf.cell(0, 12, "Weekly Capital Markets Snapshot", align="C", ln=1)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 8, f"Report Date: {datetime.now().strftime('%B %d, %Y')}", align="C", ln=1)
    pdf.cell(0, 8, "Capital Markets Intelligence Platform", align="C", ln=1)
    pdf.ln(10)

    # Executive Summary
    ipo_df = pd.DataFrame(data.get("ipo", []))
    mna_df = pd.DataFrame(data.get("mna", []))
    sov_df = pd.DataFrame(data.get("sovereign", []))

    pdf.section_title("I. Executive Summary")
    total_raised = ipo_df["deal_size_usd"].sum() / 1e9 if "deal_size_usd" in ipo_df.columns else 0
    total_mna = mna_df["deal_value_usd_bn"].sum() if "deal_value_usd_bn" in mna_df.columns else 0
    total_sov = sov_df["issue_size_usd_bn"].sum() if "issue_size_usd_bn" in sov_df.columns else 0

    pdf.body_text(
        f"Global capital markets activity remains elevated across all verticals. "
        f"Our tracking database covers {len(ipo_df)} IPOs raising ${total_raised:.1f}B, "
        f"{len(mna_df)} M&A transactions totaling ${total_mna:.1f}B, and "
        f"${total_sov:.1f}B in sovereign issuance across {sov_df['country'].nunique() if 'country' in sov_df.columns else 0} countries. "
        f"Key themes: (1) technology IPOs driving first-day outperformance, "
        f"(2) energy sector M&A consolidation, (3) elevated regulatory intervention."
    )

    # IPO Section
    pdf.add_page()
    pdf.section_title("II. IPO Market Review")

    if len(ipo_df) > 0:
        pdf.key_value("Total IPOs:", str(len(ipo_df)))
        pdf.key_value("Capital Raised:", f"${total_raised:.1f}B")
        if "first_day_return_pct" in ipo_df.columns:
            pdf.key_value("Avg First-Day Return:", f"{ipo_df['first_day_return_pct'].mean():.1f}%")
            pdf.key_value("Positive Returns:", f"{(ipo_df['first_day_return_pct'] > 0).mean()*100:.0f}%")
        pdf.ln(3)

        pdf.subsection("Top 5 IPOs by Deal Size")
        top5 = ipo_df.nlargest(5, "deal_size_usd") if "deal_size_usd" in ipo_df.columns else ipo_df.head(5)
        headers = ["Company", "Ticker", "Size ($B)", "1st Day %", "Total %"]
        rows = []
        for _, row in top5.iterrows():
            rows.append([
                row.get("company", "")[:20],
                row.get("ticker", ""),
                f"${row.get('deal_size_usd', 0)/1e9:.1f}",
                f"{row.get('first_day_return_pct', 0):+.1f}%",
                f"{row.get('total_return_pct', 0):+.1f}%",
            ])
        pdf.add_table(headers, rows, [55, 25, 35, 35, 35])

    # M&A Section
    pdf.add_page()
    pdf.section_title("III. M&A Deal Flow")

    if len(mna_df) > 0:
        completed = (mna_df["status"] == "Completed").sum() if "status" in mna_df.columns else 0
        pdf.key_value("Total Deals:", str(len(mna_df)))
        pdf.key_value("Total Value:", f"${total_mna:.1f}B")
        pdf.key_value("Completed:", str(completed))
        pdf.key_value("Blocked/Pending:", str(len(mna_df) - completed))
        pdf.ln(3)

        pdf.subsection("Top 5 Deals")
        top5_mna = mna_df.nlargest(5, "deal_value_usd_bn") if "deal_value_usd_bn" in mna_df.columns else mna_df.head(5)
        headers = ["Acquirer", "Target", "Value ($B)", "Status"]
        rows = []
        for _, row in top5_mna.iterrows():
            rows.append([
                str(row.get("acquirer", ""))[:22],
                str(row.get("target", ""))[:22],
                f"${row.get('deal_value_usd_bn', 0):.1f}",
                str(row.get("status", ""))[:18],
            ])
        pdf.add_table(headers, rows, [55, 55, 35, 40])

    # Sovereign Section
    pdf.add_page()
    pdf.section_title("IV. Sovereign Issuance")
    if len(sov_df) > 0:
        pdf.key_value("Total Issuance:", f"${total_sov:.1f}B")
        pdf.key_value("Countries:", str(sov_df["country"].nunique() if "country" in sov_df.columns else 0))
        pdf.key_value("Avg Yield:", f"{sov_df['yield_at_issue_pct'].mean():.2f}%" if "yield_at_issue_pct" in sov_df.columns else "N/A")

    save_pdf(pdf, "gs_gir_capital_markets_snapshot.pdf")


def pdf_jpm_sovereign(data):
    """JPM Sovereign Risk Report PDF."""
    print("  [2/4] JPM Sovereign Risk Report...")

    pdf = ReportPDF("J.P. Morgan | Country Risk Advisory", "Sovereign Risk & Capital Issuance Model")
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(44, 62, 80)
    pdf.ln(20)
    pdf.cell(0, 12, "Sovereign Risk & Capital Issuance", align="C", ln=1)
    pdf.cell(0, 12, "Model Report", align="C", ln=1)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 8, f"Report Date: {datetime.now().strftime('%B %d, %Y')}", align="C", ln=1)
    pdf.ln(10)

    risk = pd.DataFrame(data.get("risk_index", []))
    stress = pd.DataFrame(data.get("stress", []))

    # Risk Index
    pdf.add_page()
    pdf.section_title("I. Proprietary Sovereign Risk Index")
    pdf.body_text(
        "Our proprietary sovereign risk index is constructed from 11 World Bank indicators "
        "covering fiscal health, external vulnerability, growth stability, and reserves adequacy. "
        "Each indicator is z-score normalized and weighted to produce a composite score (0-100 scale)."
    )

    if len(risk) > 0:
        risk_sorted = risk.sort_values("risk_index_0_100", ascending=False)
        headers = ["Country", "Score", "Tier", "GDP Gr%", "Inflation%"]
        rows = []
        for _, row in risk_sorted.iterrows():
            gdp = row.get("GDP growth (annual %)", None)
            infl = row.get("Inflation (CPI, annual %)", None)
            rows.append([
                str(row.get("country_name", ""))[:20],
                f"{row.get('risk_index_0_100', 0):.0f}",
                str(row.get("risk_tier", ""))[:15],
                f"{gdp:.1f}" if pd.notna(gdp) else "N/A",
                f"{infl:.1f}" if pd.notna(infl) else "N/A",
            ])
        pdf.add_table(headers, rows, [50, 25, 40, 35, 35])

    # Stress Tests
    if len(stress) > 0:
        pdf.add_page()
        pdf.section_title("II. Stress Test Results")
        pdf.body_text(
            "Five macro scenarios were tested against 12 sovereign baselines. "
            "The EM Currency Crisis scenario produces the highest tail risk concentration, "
            "while the Global Recession scenario shows classic flight-to-quality dynamics."
        )

        scenarios = stress[stress["scenario"] != "Base Case"]["scenario"].unique()
        for scenario in scenarios[:4]:  # Top 4 scenarios
            pdf.subsection(scenario)
            subset = stress[stress["scenario"] == scenario].nlargest(5, "risk_score")
            for _, row in subset.iterrows():
                pdf.body_text(
                    f"  {row.get('country', 'N/A')}: risk score {row.get('risk_score', 0):.0f}, "
                    f"yield {row.get('ten_yr_yield_pct', 0):.2f}% -> {row.get('stressed_yield_pct', 0):.2f}%"
                )

    save_pdf(pdf, "jpm_sovereign_risk_report.pdf")


def pdf_de_shaw_ipo(data):
    """D.E. Shaw IPO Dashboard PDF."""
    print("  [3/4] D.E. Shaw IPO Dashboard...")

    pdf = ReportPDF("D.E. Shaw Group | Capital Markets Research", "IPO Performance Dashboard")
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(44, 62, 80)
    pdf.ln(20)
    pdf.cell(0, 12, "IPO Performance Dashboard", align="C", ln=1)
    pdf.cell(0, 12, "Quantitative Analysis", align="C", ln=1)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 8, f"Report Date: {datetime.now().strftime('%B %d, %Y')}", align="C", ln=1)

    event = pd.DataFrame(data.get("event_study", []))
    ipo = pd.DataFrame(data.get("ipo", []))

    pdf.add_page()
    pdf.section_title("I. Statistical Summary")

    if "first_day_return_pct" in ipo.columns:
        fdr = ipo["first_day_return_pct"]
        pdf.key_value("Mean First-Day Return:", f"{fdr.mean():+.2f}%")
        pdf.key_value("Median:", f"{fdr.median():+.2f}%")
        pdf.key_value("Std Dev:", f"{fdr.std():.2f}%")
        pdf.key_value("Skewness:", f"{fdr.skew():.3f}")
        pdf.key_value("Kurtosis:", f"{fdr.kurtosis():.3f}")
        pdf.key_value("Min:", f"{fdr.min():+.2f}% ({ipo.loc[fdr.idxmin(), 'ticker']})")
        pdf.key_value("Max:", f"{fdr.max():+.2f}% ({ipo.loc[fdr.idxmax(), 'ticker']})")
        pdf.key_value("% Positive:", f"{(fdr > 0).mean()*100:.1f}%")
        pdf.ln(3)

    # Event study results
    if len(event) > 0 and "money_left_on_table_usd" in event.columns:
        pdf.section_title("II. Event Study Results")
        total_mlot = event["money_left_on_table_usd"].sum()
        pdf.key_value("Total Money Left on Table:", f"${total_mlot/1e9:.2f}B")
        pdf.ln(2)

        pdf.subsection("Pricing Assessment Distribution")
        for assess, count in event["pricing_assessment"].value_counts().items():
            pdf.body_text(f"  {assess}: {count} IPOs")

    # Top/bottom performers
    pdf.add_page()
    pdf.section_title("III. Top & Bottom Performers")
    if len(ipo) > 0:
        pdf.subsection("Top 5 First-Day Returns")
        top5 = ipo.nlargest(5, "first_day_return_pct")
        headers = ["Ticker", "Return %", "Size ($B)", "Sector"]
        rows = [[r["ticker"], f"{r['first_day_return_pct']:+.1f}%",
                 f"${r.get('deal_size_usd',0)/1e9:.1f}", str(r.get("sector",""))[:25]]
                for _, r in top5.iterrows()]
        pdf.add_table(headers, rows, [25, 30, 30, 100])

        pdf.ln(5)
        pdf.subsection("Bottom 5 First-Day Returns")
        bot5 = ipo.nsmallest(5, "first_day_return_pct")
        rows = [[r["ticker"], f"{r['first_day_return_pct']:+.1f}%",
                 f"${r.get('deal_size_usd',0)/1e9:.1f}", str(r.get("sector",""))[:25]]
                for _, r in bot5.iterrows()]
        pdf.add_table(headers, rows, [25, 30, 30, 100])

    save_pdf(pdf, "de_shaw_ipo_dashboard.pdf")


def pdf_pwc_db_mna(data):
    """PwC/DB M&A Case Studies PDF."""
    print("  [4/4] PwC/DB M&A Case Studies...")

    pdf = ReportPDF("PwC Deals Strategy / Deutsche Bank Advisory", "M&A Strategic Rationale")
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(44, 62, 80)
    pdf.ln(20)
    pdf.cell(0, 12, "M&A Strategic Rationale", align="C", ln=1)
    pdf.cell(0, 12, "Case Studies & Thematic Analysis", align="C", ln=1)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 8, f"Report Date: {datetime.now().strftime('%B %d, %Y')}", align="C", ln=1)

    cases = pd.DataFrame(data.get("cases", []))
    mna = pd.DataFrame(data.get("mna", []))

    # Overview
    pdf.add_page()
    pdf.section_title("I. Deal Universe Overview")
    if len(cases) > 0:
        pdf.key_value("Deals Analyzed:", str(len(cases)))
        pdf.key_value("Total Value:", f"${cases['deal_value_usd_bn'].sum():.1f}B")
        pdf.key_value("Cross-Border:", str(cases["cross_border"].sum()) if "cross_border" in cases.columns else "N/A")
        pdf.ln(3)

        # Size tier breakdown
        if "size_tier" in cases.columns:
            pdf.subsection("Size Distribution")
            for tier, count in cases["size_tier"].value_counts().items():
                tier_val = cases[cases["size_tier"] == tier]["deal_value_usd_bn"].sum()
                pdf.body_text(f"  {tier}: {count} deals (${tier_val:.1f}B)")

    # Top deals deep dive
    if len(cases) > 0 and "research_relevance_score" in cases.columns:
        pdf.add_page()
        pdf.section_title("II. Top Deals by Research Relevance")
        top5 = cases.nlargest(5, "research_relevance_score")

        for i, (_, cs) in enumerate(top5.iterrows(), 1):
            if pdf.get_y() > 230:
                pdf.add_page()
            pdf.subsection(f"Deal #{i}: {cs.get('deal_name', 'N/A')}")
            pdf.key_value("Value:", f"${cs.get('deal_value_usd_bn', 0):.1f}B")
            pdf.key_value("Sector:", str(cs.get("sector", "N/A")))
            pdf.key_value("Status:", str(cs.get("status", "N/A")))
            pdf.key_value("Score:", f"{cs.get('research_relevance_score', 0)}/10")
            pdf.body_text(f"Rationale: {cs.get('strategic_rationale', 'N/A')}")
            pdf.body_text(f"Value Drivers: {cs.get('value_drivers', 'N/A')}")
            pdf.body_text(f"Risk Factors: {cs.get('risk_factors', 'N/A')}")
            pdf.ln(2)

    # Regulatory landscape
    if len(mna) > 0:
        pdf.add_page()
        pdf.section_title("III. Regulatory Landscape")
        blocked = mna[mna["status"].str.contains("Blocked|Pending", na=False)] if "status" in mna.columns else pd.DataFrame()
        if len(blocked) > 0:
            for _, deal in blocked.iterrows():
                pdf.subsection(f"{deal.get('acquirer', '')} / {deal.get('target', '')}")
                pdf.key_value("Status:", str(deal.get("status", "")))
                pdf.key_value("Value:", f"${deal.get('deal_value_usd_bn', 0):.1f}B")
                pdf.body_text(str(deal.get("strategic_rationale", "")))

    save_pdf(pdf, "pwc_db_mna_case_studies.pdf")


def save_pdf(pdf, filename):
    os.makedirs(PDF_DIR, exist_ok=True)
    filepath = os.path.join(PDF_DIR, filename)
    pdf.output(filepath)
    size = os.path.getsize(filepath)
    print(f"    [OK] {filename} ({size/1024:.0f} KB)")


def main():
    print("=" * 60)
    print("PDF Report Generator")
    print("Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    print("  Loading data...")
    data = load_data()

    pdf_gs_gir(data)
    pdf_jpm_sovereign(data)
    pdf_de_shaw_ipo(data)
    pdf_pwc_db_mna(data)

    print()
    print("=" * 60)
    pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    print(f"Generated {len(pdfs)} PDF reports:")
    for f in sorted(pdfs):
        size = os.path.getsize(os.path.join(PDF_DIR, f))
        print(f"  - {f} ({size/1024:.0f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
