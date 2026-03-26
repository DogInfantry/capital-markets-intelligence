"""
Interactive Plotly Dashboard Generator
Creates standalone HTML files with interactive charts — no server needed.
Open directly in any browser.

Outputs:
  output/dashboards/yield_curve_dashboard.html
  output/dashboards/sovereign_risk_dashboard.html
  output/dashboards/market_regime_dashboard.html
  output/dashboards/ipo_analysis_dashboard.html
  output/dashboards/mna_screening_dashboard.html
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
DASH_DIR = os.path.join(BASE_DIR, "output", "dashboards")


def load_data():
    """Load all processed datasets."""
    data = {}
    files = {
        "yc": (PROC_DIR, "yield_curve_analysis.csv", {"index_col": 0, "parse_dates": True}),
        "risk": (PROC_DIR, "sovereign_risk_index.csv", {}),
        "regime": (PROC_DIR, "regime_indicators.csv", {"index_col": 0, "parse_dates": True}),
        "screening": (PROC_DIR, "deal_screening_model.csv", {}),
        "event": (PROC_DIR, "ipo_event_study.csv", {"parse_dates": ["ipo_date"]}),
        "yields_raw": (RAW_DIR, "yield_curve_history.csv", {"index_col": 0, "parse_dates": True}),
        "market": (RAW_DIR, "market_rates.csv", {"index_col": 0, "parse_dates": True}),
        "fx": (RAW_DIR, "fx_rates.csv", {"index_col": 0, "parse_dates": True}),
        "panel": (RAW_DIR, "country_macro_panel.csv", {}),
    }
    for key, (directory, filename, kwargs) in files.items():
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            data[key] = pd.read_csv(filepath, **kwargs)
    return data


def dashboard_yield_curve(data):
    """Interactive yield curve dashboard."""
    print("  [1/5] Yield Curve Dashboard...")

    yc = data.get("yc")
    if yc is None:
        return

    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "Treasury Yields Over Time", "Yield Curve Slope (10Y - 3M)",
            "Curve Regime Classification", "Level / Slope / Curvature Z-Scores",
            "Term Premium (30Y - 10Y)", "Slope Direction (Steepening/Flattening)"
        ),
        vertical_spacing=0.08,
    )

    # Yields over time
    for col, color in [("yield_3M", "#3498db"), ("yield_5Y", "#2ecc71"),
                        ("yield_10Y", "#e67e22"), ("yield_30Y", "#e74c3c")]:
        if col in yc.columns:
            fig.add_trace(go.Scatter(
                x=yc.index, y=yc[col], name=col.replace("yield_", ""),
                line=dict(color=color, width=1.5),
            ), row=1, col=1)

    # Slope
    if "slope_10y_3m" in yc.columns:
        colors = ["red" if v < 0 else "green" for v in yc["slope_10y_3m"]]
        fig.add_trace(go.Bar(
            x=yc.index, y=yc["slope_10y_3m"], name="10Y-3M Spread",
            marker_color=colors, showlegend=False,
        ), row=1, col=2)
        fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)

    # Regime
    if "curve_regime" in yc.columns:
        regime_map = {"Inverted": -1, "Flat": 0, "Normal": 1, "Steep": 2}
        regime_colors = {"Inverted": "red", "Flat": "orange", "Normal": "green", "Steep": "blue"}
        regime_vals = yc["curve_regime"].map(regime_map)
        fig.add_trace(go.Scatter(
            x=yc.index, y=regime_vals, mode="markers",
            marker=dict(
                color=[regime_colors.get(r, "gray") for r in yc["curve_regime"]],
                size=4,
            ),
            name="Regime", showlegend=False,
        ), row=2, col=1)

    # Z-scores
    for col, color in [("level_zscore", "#3498db"), ("slope_10y_3m_zscore", "#e67e22"),
                        ("curvature_zscore", "#9b59b6")]:
        if col in yc.columns:
            fig.add_trace(go.Scatter(
                x=yc.index, y=yc[col], name=col.replace("_zscore", "").title(),
                line=dict(width=1),
            ), row=2, col=2)

    # Term premium
    if "term_premium_30_10" in yc.columns:
        fig.add_trace(go.Scatter(
            x=yc.index, y=yc["term_premium_30_10"], name="30Y-10Y",
            line=dict(color="#9b59b6", width=1.5), showlegend=False,
        ), row=3, col=1)

    # Slope direction
    if "slope_20d_change" in yc.columns:
        fig.add_trace(go.Bar(
            x=yc.index, y=yc["slope_20d_change"], name="20d Slope Change",
            marker_color=["green" if v > 0 else "red" for v in yc["slope_20d_change"]],
            showlegend=False,
        ), row=3, col=2)

    fig.update_layout(
        title_text="<b>Yield Curve Analysis Dashboard</b> | Capital Markets Intelligence",
        height=1000, template="plotly_white",
        font=dict(size=10),
    )
    save_dashboard(fig, "yield_curve_dashboard.html")


def dashboard_sovereign_risk(data):
    """Interactive sovereign risk index dashboard."""
    print("  [2/5] Sovereign Risk Dashboard...")

    risk = data.get("risk")
    panel = data.get("panel")
    if risk is None:
        return

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Sovereign Risk Index (0-100)", "Risk Tier Distribution",
            "GDP Growth vs Inflation", "Debt/GDP vs Current Account"
        ),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "scatter"}, {"type": "scatter"}]],
        vertical_spacing=0.12,
    )

    # Risk index bar chart
    sorted_risk = risk.sort_values("risk_index_0_100", ascending=True)
    colors = []
    for _, row in sorted_risk.iterrows():
        tier = row["risk_tier"]
        if tier == "High Risk":
            colors.append("#e74c3c")
        elif tier == "Elevated Risk":
            colors.append("#e67e22")
        elif tier == "Moderate Risk":
            colors.append("#f39c12")
        else:
            colors.append("#2ecc71")

    fig.add_trace(go.Bar(
        y=sorted_risk["country_name"], x=sorted_risk["risk_index_0_100"],
        orientation="h", marker_color=colors, showlegend=False,
        text=sorted_risk["risk_index_0_100"].round(0),
        textposition="outside",
    ), row=1, col=1)

    # Pie chart of tiers
    tier_counts = risk["risk_tier"].value_counts()
    fig.add_trace(go.Pie(
        labels=tier_counts.index, values=tier_counts.values,
        marker_colors=["#2ecc71", "#f39c12", "#e67e22", "#e74c3c"],
    ), row=1, col=2)

    # GDP Growth vs Inflation scatter
    gdp_col = "GDP growth (annual %)"
    infl_col = "Inflation (CPI, annual %)"
    if gdp_col in risk.columns and infl_col in risk.columns:
        fig.add_trace(go.Scatter(
            x=risk[gdp_col], y=risk[infl_col],
            mode="markers+text", text=risk["country_code"],
            textposition="top center",
            marker=dict(
                size=risk["risk_index_0_100"] / 5 + 5,
                color=risk["risk_index_0_100"],
                colorscale="RdYlGn_r", showscale=True,
                colorbar=dict(title="Risk", x=0.45, len=0.4, y=0.2),
            ),
            showlegend=False,
        ), row=2, col=1)
        fig.update_xaxes(title_text="GDP Growth (%)", row=2, col=1)
        fig.update_yaxes(title_text="Inflation (%)", row=2, col=1)

    # Debt/GDP vs Current Account
    debt_col = "Central govt debt (% of GDP)"
    ca_col = "Current account (% of GDP)"
    if debt_col in risk.columns and ca_col in risk.columns:
        fig.add_trace(go.Scatter(
            x=risk[debt_col], y=risk[ca_col],
            mode="markers+text", text=risk["country_code"],
            textposition="top center",
            marker=dict(
                size=risk["risk_index_0_100"] / 5 + 5,
                color=risk["risk_index_0_100"],
                colorscale="RdYlGn_r", showscale=False,
            ),
            showlegend=False,
        ), row=2, col=2)
        fig.update_xaxes(title_text="Govt Debt (% GDP)", row=2, col=2)
        fig.update_yaxes(title_text="Current Account (% GDP)", row=2, col=2)

    fig.update_layout(
        title_text="<b>Sovereign Risk Index Dashboard</b> | Capital Markets Intelligence",
        height=900, template="plotly_white",
    )
    save_dashboard(fig, "sovereign_risk_dashboard.html")


def dashboard_market_regime(data):
    """Interactive market regime dashboard."""
    print("  [3/5] Market Regime Dashboard...")

    regime = data.get("regime")
    market = data.get("market")
    if regime is None:
        return

    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            "S&P 500 with Regime Overlay",
            "VIX (Fear Index)",
            "Regime Score (positive = Risk-On, negative = Risk-Off)"
        ),
        vertical_spacing=0.08,
        shared_xaxes=True,
    )

    # S&P 500 with regime coloring
    if "SP500" in regime.columns:
        regime_colors = {"Risk-On": "green", "Neutral": "gray", "Risk-Off": "red"}
        for regime_name, color in regime_colors.items():
            mask = regime["regime"] == regime_name
            subset = regime[mask]
            fig.add_trace(go.Scatter(
                x=subset.index, y=subset["SP500"],
                mode="markers", marker=dict(color=color, size=3),
                name=regime_name,
            ), row=1, col=1)
        if "SP500_200ma" in regime.columns:
            fig.add_trace(go.Scatter(
                x=regime.index, y=regime["SP500_200ma"],
                mode="lines", line=dict(color="blue", width=1, dash="dash"),
                name="200-day MA",
            ), row=1, col=1)

    # VIX
    if "VIX" in regime.columns:
        fig.add_trace(go.Scatter(
            x=regime.index, y=regime["VIX"],
            mode="lines", line=dict(color="#e67e22", width=1),
            name="VIX", showlegend=False,
        ), row=2, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=15, line_dash="dash", line_color="green", row=2, col=1)

    # Regime score
    if "regime_score" in regime.columns:
        colors = ["green" if v > 0 else "red" for v in regime["regime_score"]]
        fig.add_trace(go.Bar(
            x=regime.index, y=regime["regime_score"],
            marker_color=colors, name="Regime Score", showlegend=False,
        ), row=3, col=1)
        if "regime_score_5d_ma" in regime.columns:
            fig.add_trace(go.Scatter(
                x=regime.index, y=regime["regime_score_5d_ma"],
                mode="lines", line=dict(color="blue", width=2),
                name="5d MA", showlegend=False,
            ), row=3, col=1)
        fig.add_hline(y=0, line_dash="solid", line_color="black", row=3, col=1)

    fig.update_layout(
        title_text="<b>Cross-Asset Market Regime Dashboard</b> | Capital Markets Intelligence",
        height=900, template="plotly_white",
    )
    save_dashboard(fig, "market_regime_dashboard.html")


def dashboard_ipo_analysis(data):
    """Interactive IPO analysis dashboard."""
    print("  [4/5] IPO Analysis Dashboard...")

    event = data.get("event")
    if event is None:
        return

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "First-Day vs Total Returns", "Money Left on Table ($M)",
            "Abnormal Returns by Sector", "Deal Size vs First-Day Return"
        ),
        vertical_spacing=0.12,
    )

    # Scatter: first-day vs total
    fig.add_trace(go.Scatter(
        x=event["first_day_return_pct"], y=event["total_return_pct"],
        mode="markers+text", text=event["ticker"],
        textposition="top center", textfont=dict(size=8),
        marker=dict(
            size=np.log(event["deal_size_usd"] / 1e6) * 3,
            color=event["first_day_return_pct"],
            colorscale="RdYlGn", showscale=True,
            colorbar=dict(title="1st Day %", x=0.45, len=0.4, y=0.8),
        ),
        showlegend=False,
    ), row=1, col=1)
    fig.add_hline(y=0, line_dash="dash", row=1, col=1)
    fig.add_vline(x=0, line_dash="dash", row=1, col=1)
    fig.update_xaxes(title_text="First-Day Return (%)", row=1, col=1)
    fig.update_yaxes(title_text="Total Return (%)", row=1, col=1)

    # Money left on table
    sorted_mlot = event.sort_values("money_left_on_table_usd", ascending=True)
    colors = ["green" if v > 0 else "red" for v in sorted_mlot["money_left_on_table_usd"]]
    fig.add_trace(go.Bar(
        y=sorted_mlot["ticker"],
        x=sorted_mlot["money_left_on_table_usd"] / 1e6,
        orientation="h", marker_color=colors, showlegend=False,
    ), row=1, col=2)
    fig.update_xaxes(title_text="Money Left on Table ($M)", row=1, col=2)

    # Abnormal returns by pricing assessment
    if "abnormal_return_pct" in event.columns:
        ar_by_assess = event.groupby("pricing_assessment")["abnormal_return_pct"].mean().dropna()
        ar_sorted = ar_by_assess.sort_values()
        fig.add_trace(go.Bar(
            x=ar_sorted.values, y=ar_sorted.index, orientation="h",
            marker_color=["green" if v > 0 else "red" for v in ar_sorted.values],
            showlegend=False,
        ), row=2, col=1)
        fig.update_xaxes(title_text="Avg Abnormal Return (%)", row=2, col=1)

    # Deal size vs return
    fig.add_trace(go.Scatter(
        x=event["deal_size_usd"] / 1e9, y=event["first_day_return_pct"],
        mode="markers+text", text=event["ticker"],
        textposition="top center", textfont=dict(size=8),
        marker=dict(size=8, color="#3498db"),
        showlegend=False,
    ), row=2, col=2)
    fig.update_xaxes(title_text="Deal Size ($B)", row=2, col=2)
    fig.update_yaxes(title_text="First-Day Return (%)", row=2, col=2)

    fig.update_layout(
        title_text="<b>IPO Event Study Dashboard</b> | Capital Markets Intelligence",
        height=900, template="plotly_white",
    )
    save_dashboard(fig, "ipo_analysis_dashboard.html")


def dashboard_mna_screening(data):
    """Interactive M&A deal screening dashboard."""
    print("  [5/5] M&A Screening Dashboard...")

    screening = data.get("screening")
    if screening is None:
        return

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Deal Completion Probability", "Feature Importance",
            "Deal Value vs Completion Score", "Cross-Border vs Domestic"
        ),
        vertical_spacing=0.12,
    )

    # Completion probability
    sorted_s = screening.sort_values("completion_probability_pct", ascending=True)
    deal_names = sorted_s["acquirer"] + " / " + sorted_s["target"]
    colors = ["green" if s == "Completed" else "orange" if "Pending" in str(s) else "red"
              for s in sorted_s["status"]]
    fig.add_trace(go.Bar(
        y=deal_names, x=sorted_s["completion_probability_pct"],
        orientation="h", marker_color=colors, showlegend=False,
    ), row=1, col=1)
    fig.update_xaxes(title_text="Completion Probability (%)", row=1, col=1)

    # Feature importance
    fi_path = os.path.join(PROC_DIR, "deal_feature_importance.csv")
    if os.path.exists(fi_path):
        fi = pd.read_csv(fi_path).sort_values("correlation")
        fig.add_trace(go.Bar(
            y=fi["feature"], x=fi["correlation"], orientation="h",
            marker_color=["green" if c > 0 else "red" for c in fi["correlation"]],
            showlegend=False,
        ), row=1, col=2)
        fig.update_xaxes(title_text="Correlation with Completion", row=1, col=2)

    # Deal value vs score
    fig.add_trace(go.Scatter(
        x=screening["deal_value_usd_bn"], y=screening["completion_probability_pct"],
        mode="markers+text",
        text=screening["acquirer"].str[:15],
        textposition="top center", textfont=dict(size=7),
        marker=dict(
            size=10,
            color=screening["completed"],
            colorscale=[[0, "red"], [1, "green"]],
        ),
        showlegend=False,
    ), row=2, col=1)
    fig.update_xaxes(title_text="Deal Value ($B)", row=2, col=1)
    fig.update_yaxes(title_text="Completion Prob (%)", row=2, col=1)

    # Cross-border breakdown
    cb_stats = screening.groupby("is_cross_border").agg(
        count=("acquirer", "count"),
        avg_completion=("completed", "mean"),
    )
    fig.add_trace(go.Bar(
        x=["Domestic", "Cross-Border"],
        y=[cb_stats.loc[0, "avg_completion"] * 100 if 0 in cb_stats.index else 0,
           cb_stats.loc[1, "avg_completion"] * 100 if 1 in cb_stats.index else 0],
        marker_color=["#2ecc71", "#e67e22"],
        showlegend=False,
    ), row=2, col=2)
    fig.update_yaxes(title_text="Completion Rate (%)", row=2, col=2)

    fig.update_layout(
        title_text="<b>M&A Deal Screening Dashboard</b> | Capital Markets Intelligence",
        height=900, template="plotly_white",
    )
    save_dashboard(fig, "mna_screening_dashboard.html")


def save_dashboard(fig, filename):
    """Save Plotly figure as standalone HTML."""
    os.makedirs(DASH_DIR, exist_ok=True)
    filepath = os.path.join(DASH_DIR, filename)
    fig.write_html(filepath, include_plotlyjs=True)
    size = os.path.getsize(filepath)
    print(f"    [OK] {filename} ({size/1024:.0f} KB)")


def main():
    print("=" * 60)
    print("Plotly Interactive Dashboard Generator")
    print("Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    print("  Loading data...")
    data = load_data()

    dashboard_yield_curve(data)
    dashboard_sovereign_risk(data)
    dashboard_market_regime(data)
    dashboard_ipo_analysis(data)
    dashboard_mna_screening(data)

    print()
    print("=" * 60)
    htmls = [f for f in os.listdir(DASH_DIR) if f.endswith(".html")]
    print(f"Generated {len(htmls)} interactive dashboards:")
    for h in sorted(htmls):
        size = os.path.getsize(os.path.join(DASH_DIR, h))
        print(f"  - {h} ({size/1024:.0f} KB)")
    print("Open any HTML file in a browser — no server needed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
