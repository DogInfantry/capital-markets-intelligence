"""
Advanced Capital Markets Analysis
Builds proprietary analytical models from real data:

1. Yield Curve Decomposition — level/slope/curvature regime analysis
2. Proprietary Sovereign Risk Index — composite from 10+ real macro indicators
3. Cross-Asset Regime Detection — risk-on vs risk-off classification
4. M&A Deal Screening Model — what predicts completion vs. block?
5. IPO Event Study — abnormal return methodology

Outputs:
  data/processed/yield_curve_analysis.csv
  data/processed/sovereign_risk_index.csv
  data/processed/regime_indicators.csv
  data/processed/deal_screening_model.csv
  data/processed/ipo_event_study.csv
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")


def load_data():
    """Load all available datasets."""
    data = {}
    files = {
        "yields": ("yield_curve_history.csv", {"index_col": 0, "parse_dates": True}),
        "market": ("market_rates.csv", {"index_col": 0, "parse_dates": True}),
        "fx": ("fx_rates.csv", {"index_col": 0, "parse_dates": True}),
        "wb": ("worldbank_indicators.csv", {}),
        "panel": ("country_macro_panel.csv", {}),
        "ipo": ("ipo_data_raw.csv", {"parse_dates": ["ipo_date"]}),
        "mna": ("mna_data_raw.csv", {"parse_dates": ["announced_date"]}),
        "stress": ("../processed/stress_test_results.csv", {}),
    }
    for key, (filename, kwargs) in files.items():
        filepath = os.path.join(RAW_DIR, filename)
        if os.path.exists(filepath):
            data[key] = pd.read_csv(filepath, **kwargs)
            print(f"    [OK] {key}: {len(data[key])} rows")
        else:
            print(f"    [WARN] {key}: not found ({filename})")
    return data


# ============================================================
# 1. YIELD CURVE DECOMPOSITION
# ============================================================

def analyze_yield_curve(yields_df):
    """
    Decompose the yield curve into level, slope, and curvature.
    Identify regimes: normal, flat, inverted, steepening, flattening.
    """
    print("\n  [1/5] Yield Curve Decomposition...")

    if yields_df is None or len(yields_df) == 0:
        print("    [WARN] No yield data available")
        return pd.DataFrame()

    df = yields_df.copy()

    # Rename columns if they have ticker names
    col_map = {}
    for col in df.columns:
        if "IRX" in str(col):
            col_map[col] = "3M"
        elif "FVX" in str(col):
            col_map[col] = "5Y"
        elif "TNX" in str(col):
            col_map[col] = "10Y"
        elif "TYX" in str(col):
            col_map[col] = "30Y"
    if col_map:
        df = df.rename(columns=col_map)

    required = ["3M", "5Y", "10Y", "30Y"]
    available = [c for c in required if c in df.columns]
    if len(available) < 3:
        print(f"    [WARN] Need at least 3 tenors, have: {available}")
        return pd.DataFrame()

    result = pd.DataFrame(index=df.index)

    # Level: average across all tenors (proxy for general rate environment)
    result["level"] = df[available].mean(axis=1)

    # Slope: 10Y - 3M (classic measure)
    if "10Y" in df.columns and "3M" in df.columns:
        result["slope_10y_3m"] = df["10Y"] - df["3M"]

    # Curvature: 2 * 5Y - (3M + 10Y) — butterfly spread
    if all(c in df.columns for c in ["3M", "5Y", "10Y"]):
        result["curvature"] = 2 * df["5Y"] - (df["3M"] + df["10Y"])

    # Term premium proxy: 30Y - 10Y
    if "30Y" in df.columns and "10Y" in df.columns:
        result["term_premium_30_10"] = df["30Y"] - df["10Y"]

    # Rolling z-scores (20-day lookback)
    for col in ["level", "slope_10y_3m", "curvature"]:
        if col in result.columns:
            rolling_mean = result[col].rolling(60).mean()
            rolling_std = result[col].rolling(60).std()
            result[f"{col}_zscore"] = (result[col] - rolling_mean) / rolling_std

    # Regime classification
    if "slope_10y_3m" in result.columns:
        conditions = [
            result["slope_10y_3m"] < -0.25,
            result["slope_10y_3m"].between(-0.25, 0.25),
            result["slope_10y_3m"].between(0.25, 1.0),
            result["slope_10y_3m"] > 1.0,
        ]
        labels = ["Inverted", "Flat", "Normal", "Steep"]
        result["curve_regime"] = np.select(conditions, labels, default="Normal")

    # Slope momentum (is curve steepening or flattening?)
    if "slope_10y_3m" in result.columns:
        result["slope_20d_change"] = result["slope_10y_3m"].diff(20)
        result["slope_direction"] = np.where(
            result["slope_20d_change"] > 0.1, "Steepening",
            np.where(result["slope_20d_change"] < -0.1, "Flattening", "Stable")
        )

    # Copy raw yields
    for col in available:
        result[f"yield_{col}"] = df[col]

    result = result.dropna(subset=["level"])
    print(f"    [OK] {len(result)} days analyzed")

    if "curve_regime" in result.columns:
        regime_counts = result["curve_regime"].value_counts()
        for regime, count in regime_counts.items():
            pct = count / len(result) * 100
            print(f"      {regime}: {count} days ({pct:.0f}%)")

    return result


# ============================================================
# 2. PROPRIETARY SOVEREIGN RISK INDEX
# ============================================================

def build_sovereign_risk_index(panel_df):
    """
    Build a composite sovereign risk index from 10+ real macro indicators.
    Uses z-score normalization and weighted aggregation.
    Similar methodology to JPM EMBI / Fitch sovereign risk models.
    """
    print("\n  [2/5] Proprietary Sovereign Risk Index...")

    if panel_df is None or len(panel_df) == 0:
        print("    [WARN] No panel data available")
        return pd.DataFrame()

    df = panel_df.copy()

    # Use latest year with most data
    year_coverage = df.groupby("year").apply(lambda x: x.notna().sum().sum())
    best_year = year_coverage.idxmax()
    latest = df[df["year"] == best_year].copy()
    print(f"    Using year {best_year} ({len(latest)} countries)")

    # Define risk indicators with direction (higher = more risk)
    risk_indicators = {
        # Fiscal indicators
        "Central govt debt (% of GDP)": {"weight": 0.15, "higher_is_riskier": True},
        "Inflation (CPI, annual %)": {"weight": 0.12, "higher_is_riskier": True},
        "Unemployment (% of labor force)": {"weight": 0.08, "higher_is_riskier": True},

        # Growth & stability
        "GDP growth (annual %)": {"weight": 0.12, "higher_is_riskier": False},

        # External vulnerability
        "Current account (% of GDP)": {"weight": 0.10, "higher_is_riskier": False},  # deficit = risk
        "External debt stocks (% of GNI)": {"weight": 0.10, "higher_is_riskier": True},
        "FDI net inflows (% of GDP)": {"weight": 0.05, "higher_is_riskier": False},

        # Reserves & trade
        "Total reserves (includes gold, USD)": {"weight": 0.08, "higher_is_riskier": False},

        # Fiscal balance
        "fiscal_balance_pct_gdp": {"weight": 0.10, "higher_is_riskier": False},  # deficit = risk

        # Trade openness (double-edged but proxy for integration)
        "trade_openness_pct": {"weight": 0.05, "higher_is_riskier": False},

        # Real interest rate (high = tighter, can signal instability)
        "Real interest rate (%)": {"weight": 0.05, "higher_is_riskier": True},
    }

    # Calculate z-scores for each indicator
    scores = pd.DataFrame()
    scores["country_code"] = latest["country_code"]
    scores["country_name"] = latest["country_name"]
    total_weight = 0
    used_indicators = 0

    for indicator, config in risk_indicators.items():
        if indicator not in latest.columns:
            continue
        values = latest[indicator].astype(float)
        if values.notna().sum() < 3:
            continue

        # Z-score normalize
        zscore = (values - values.mean()) / values.std()

        # Flip sign if lower values mean more risk
        if not config["higher_is_riskier"]:
            zscore = -zscore

        scores[f"z_{indicator[:30]}"] = zscore.values
        total_weight += config["weight"]
        used_indicators += 1

    print(f"    Used {used_indicators}/{len(risk_indicators)} indicators")

    # Weighted composite score
    composite = pd.Series(0.0, index=scores.index)
    for indicator, config in risk_indicators.items():
        col = f"z_{indicator[:30]}"
        if col in scores.columns:
            composite += scores[col].fillna(0) * config["weight"]

    scores["composite_risk_score"] = composite

    # Normalize to 0-100 scale
    min_score = scores["composite_risk_score"].min()
    max_score = scores["composite_risk_score"].max()
    if max_score > min_score:
        scores["risk_index_0_100"] = (
            (scores["composite_risk_score"] - min_score) / (max_score - min_score) * 100
        ).round(1)
    else:
        scores["risk_index_0_100"] = 50.0

    # Risk tier classification
    scores["risk_tier"] = pd.cut(
        scores["risk_index_0_100"],
        bins=[0, 25, 50, 75, 100],
        labels=["Low Risk", "Moderate Risk", "Elevated Risk", "High Risk"],
    )

    # Add raw indicators for context
    for col in ["GDP growth (annual %)", "Inflation (CPI, annual %)",
                 "Central govt debt (% of GDP)", "Current account (% of GDP)"]:
        if col in latest.columns:
            scores[col] = latest[col].values

    scores["year"] = best_year
    scores = scores.sort_values("risk_index_0_100", ascending=False)

    print(f"    [OK] Risk index built for {len(scores)} countries")
    print(f"    Risk tier distribution:")
    for tier, count in scores["risk_tier"].value_counts().items():
        print(f"      {tier}: {count}")

    return scores


# ============================================================
# 3. CROSS-ASSET REGIME DETECTION
# ============================================================

def detect_market_regime(market_df, yields_df, fx_df):
    """
    Classify market regime as Risk-On or Risk-Off based on
    cross-asset signals: VIX, yield curve, gold, FX vol.
    """
    print("\n  [3/5] Cross-Asset Regime Detection...")

    if market_df is None or len(market_df) == 0:
        print("    [WARN] No market data available")
        return pd.DataFrame()

    result = pd.DataFrame(index=market_df.index)
    signals = pd.DataFrame(index=market_df.index)

    # Signal 1: VIX level (>20 = risk-off, <15 = risk-on)
    if "VIX" in market_df.columns:
        signals["vix_signal"] = np.where(
            market_df["VIX"] > 25, -2,
            np.where(market_df["VIX"] > 20, -1,
                     np.where(market_df["VIX"] < 15, 1, 0))
        )
        result["VIX"] = market_df["VIX"]

    # Signal 2: S&P 500 trend (above/below 200-day MA)
    if "SP500" in market_df.columns:
        ma200 = market_df["SP500"].rolling(200).mean()
        signals["sp500_trend"] = np.where(market_df["SP500"] > ma200, 1, -1)
        result["SP500"] = market_df["SP500"]
        result["SP500_200ma"] = ma200

    # Signal 3: S&P 500 momentum (20-day return)
    if "SP500" in market_df.columns:
        ret_20d = market_df["SP500"].pct_change(20) * 100
        signals["sp500_momentum"] = np.where(ret_20d > 3, 1, np.where(ret_20d < -3, -1, 0))

    # Signal 4: Gold trend (rising gold = risk-off)
    if "Gold" in market_df.columns:
        gold_20d = market_df["Gold"].pct_change(20) * 100
        signals["gold_signal"] = np.where(gold_20d > 3, -1, np.where(gold_20d < -1, 1, 0))
        result["Gold"] = market_df["Gold"]

    # Signal 5: Yield curve slope
    if yields_df is not None and len(yields_df) > 0:
        # Align indices
        yc = yields_df.copy()
        col_map = {}
        for col in yc.columns:
            if "IRX" in str(col):
                col_map[col] = "3M"
            elif "TNX" in str(col):
                col_map[col] = "10Y"
        yc = yc.rename(columns=col_map)
        if "10Y" in yc.columns and "3M" in yc.columns:
            slope = yc["10Y"] - yc["3M"]
            slope_aligned = slope.reindex(signals.index, method="ffill")
            signals["curve_signal"] = np.where(
                slope_aligned < 0, -2,  # Inverted = strong risk-off
                np.where(slope_aligned > 1.0, 1, 0)
            )

    # Signal 6: FX volatility (EM vol spike = risk-off)
    if fx_df is not None and len(fx_df) > 0:
        em_vol_cols = [c for c in fx_df.columns if "_vol" in c and any(x in c for x in ["BRL", "TRY", "ZAR", "MXN"])]
        if em_vol_cols:
            em_avg_vol = fx_df[em_vol_cols].mean(axis=1)
            em_vol_aligned = em_avg_vol.reindex(signals.index, method="ffill")
            vol_median = em_vol_aligned.median()
            signals["fx_vol_signal"] = np.where(
                em_vol_aligned > vol_median * 1.5, -1,
                np.where(em_vol_aligned < vol_median * 0.7, 1, 0)
            )

    # Composite regime score: average of all signals
    signal_cols = [c for c in signals.columns if c.endswith("_signal")]
    if signal_cols:
        result["regime_score"] = signals[signal_cols].mean(axis=1)
        result["regime"] = np.where(
            result["regime_score"] > 0.3, "Risk-On",
            np.where(result["regime_score"] < -0.3, "Risk-Off", "Neutral")
        )
        result["regime_score_5d_ma"] = result["regime_score"].rolling(5).mean()

        # Add individual signals
        for col in signal_cols:
            result[col] = signals[col]

    result = result.dropna(subset=["regime_score"])
    print(f"    [OK] {len(result)} days classified")
    if "regime" in result.columns:
        for regime, count in result["regime"].value_counts().items():
            pct = count / len(result) * 100
            print(f"      {regime}: {count} days ({pct:.0f}%)")

    return result


# ============================================================
# 4. M&A DEAL SCREENING MODEL
# ============================================================

def build_deal_screening_model(mna_df):
    """
    Build a logistic-regression-style deal screening model.
    Features: deal size, cross-border, sector, deal type.
    Target: completed vs blocked/pending.
    """
    print("\n  [4/5] M&A Deal Screening Model...")

    if mna_df is None or len(mna_df) == 0:
        print("    [WARN] No M&A data available")
        return pd.DataFrame()

    df = mna_df.copy()

    # Target: 1 = completed, 0 = blocked/pending
    df["completed"] = (df["status"] == "Completed").astype(int)

    # Feature engineering
    df["is_cross_border"] = df["cross_border"].astype(int)
    df["is_tech_sector"] = df["sector"].str.contains("Technology", na=False).astype(int)
    df["is_healthcare"] = df["sector"].str.contains("Health|Pharma", na=False).astype(int)
    df["is_energy"] = df["sector"].str.contains("Energy", na=False).astype(int)
    df["is_financial"] = df["sector"].str.contains("Financial", na=False).astype(int)
    df["is_take_private"] = df["deal_type"].str.contains("Take-Private|LBO", na=False).astype(int)
    df["is_cash_deal"] = df["deal_type"].str.contains("Cash", na=False).astype(int)
    df["is_mega_deal"] = (df["deal_value_usd_bn"] >= 30).astype(int)
    df["log_deal_value"] = np.log(df["deal_value_usd_bn"])

    features = [
        "log_deal_value", "is_cross_border", "is_tech_sector", "is_healthcare",
        "is_energy", "is_financial", "is_take_private", "is_cash_deal", "is_mega_deal",
    ]

    # Simple feature importance via point-biserial correlation
    print("    Feature importance (correlation with completion):")
    feature_importance = []
    for feat in features:
        corr, pval = stats.pointbiserialr(df["completed"], df[feat])
        direction = "+" if corr > 0 else "-"
        significance = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else ""
        print(f"      {feat:<25s}: {direction}{abs(corr):.3f}  (p={pval:.3f}) {significance}")
        feature_importance.append({
            "feature": feat,
            "correlation": round(corr, 4),
            "p_value": round(pval, 4),
            "direction": "Positive" if corr > 0 else "Negative",
        })

    # Completion probability estimate (simple logistic approximation)
    # Using weighted feature sum as proxy
    weights = {}
    for fi in feature_importance:
        weights[fi["feature"]] = fi["correlation"]

    df["completion_score"] = sum(df[f] * w for f, w in weights.items())

    # Normalize to 0-100
    min_s = df["completion_score"].min()
    max_s = df["completion_score"].max()
    if max_s > min_s:
        df["completion_probability_pct"] = (
            (df["completion_score"] - min_s) / (max_s - min_s) * 100
        ).round(1)
    else:
        df["completion_probability_pct"] = 50.0

    # Results summary
    output = df[["acquirer", "target", "deal_value_usd_bn", "status", "sector",
                  "deal_type", "cross_border", "completed"] + features +
                 ["completion_score", "completion_probability_pct"]].copy()

    importance_df = pd.DataFrame(feature_importance)
    importance_df.to_csv(os.path.join(PROC_DIR, "deal_feature_importance.csv"), index=False)

    print(f"    [OK] Screened {len(output)} deals")
    return output


# ============================================================
# 5. IPO EVENT STUDY
# ============================================================

def run_ipo_event_study(ipo_df, market_df):
    """
    Event study methodology: calculate abnormal returns for IPOs
    relative to market benchmark.
    """
    print("\n  [5/5] IPO Event Study (Abnormal Returns)...")

    if ipo_df is None or len(ipo_df) == 0:
        print("    [WARN] No IPO data available")
        return pd.DataFrame()

    df = ipo_df.copy()

    # Market return on IPO dates (S&P 500 as benchmark)
    market_returns = None
    if market_df is not None and "SP500" in market_df.columns:
        sp500 = market_df["SP500"]
        market_returns = sp500.pct_change() * 100

    results = []
    for _, row in df.iterrows():
        result = {
            "company": row["company"],
            "ticker": row["ticker"],
            "ipo_date": row["ipo_date"],
            "sector": row["sector"],
            "country": row["country"],
            "offer_price": row["offer_price"],
            "first_day_close": row["first_day_close"],
            "current_price": row["current_price"],
            "deal_size_usd": row["deal_size_usd"],
            "lead_underwriter": row["lead_underwriter"],

            # Raw returns
            "first_day_return_pct": row["first_day_return_pct"],
            "total_return_pct": row["total_return_pct"],
        }

        # Abnormal return (vs market on IPO date)
        if market_returns is not None:
            ipo_date = row["ipo_date"]
            # Find closest market date
            closest_dates = market_returns.index[market_returns.index >= ipo_date]
            if len(closest_dates) > 0:
                mkt_ret = market_returns.loc[closest_dates[0]]
                result["market_return_on_date_pct"] = round(float(mkt_ret), 2)
                result["abnormal_return_pct"] = round(row["first_day_return_pct"] - float(mkt_ret), 2)
            else:
                result["market_return_on_date_pct"] = None
                result["abnormal_return_pct"] = None
        else:
            result["market_return_on_date_pct"] = None
            result["abnormal_return_pct"] = None

        # Money left on the table (underpricing cost)
        result["money_left_on_table_usd"] = round(
            (row["first_day_close"] - row["offer_price"]) * row["shares_offered"], 0
        )

        # Underpricing magnitude classification
        fdr = row["first_day_return_pct"]
        if fdr > 50:
            result["pricing_assessment"] = "Severely Underpriced"
        elif fdr > 20:
            result["pricing_assessment"] = "Significantly Underpriced"
        elif fdr > 5:
            result["pricing_assessment"] = "Moderately Underpriced"
        elif fdr > -5:
            result["pricing_assessment"] = "Fairly Priced"
        elif fdr > -15:
            result["pricing_assessment"] = "Moderately Overpriced"
        else:
            result["pricing_assessment"] = "Significantly Overpriced"

        results.append(result)

    output = pd.DataFrame(results)

    # Summary statistics
    if "abnormal_return_pct" in output.columns:
        ar = output["abnormal_return_pct"].dropna()
        if len(ar) > 0:
            t_stat, p_val = stats.ttest_1samp(ar, 0)
            print(f"    Abnormal return: mean={ar.mean():.2f}%, t={t_stat:.2f}, p={p_val:.4f}")
            output.attrs["ar_mean"] = ar.mean()
            output.attrs["ar_tstat"] = t_stat
            output.attrs["ar_pval"] = p_val

    # Money left on table
    total_mlot = output["money_left_on_table_usd"].sum()
    print(f"    Total money left on table: ${total_mlot/1e9:.2f}B")
    print(f"    Pricing assessment distribution:")
    for assess, count in output["pricing_assessment"].value_counts().items():
        print(f"      {assess}: {count}")

    print(f"    [OK] Event study complete for {len(output)} IPOs")
    return output


def main():
    print("=" * 60)
    print("Advanced Capital Markets Analysis")
    print("Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    os.makedirs(PROC_DIR, exist_ok=True)

    print("  Loading data...")
    data = load_data()

    # 1. Yield Curve
    yc_analysis = analyze_yield_curve(data.get("yields"))
    if len(yc_analysis) > 0:
        yc_analysis.to_csv(os.path.join(PROC_DIR, "yield_curve_analysis.csv"))
        print(f"    Saved yield_curve_analysis.csv")

    # 2. Sovereign Risk Index
    risk_index = build_sovereign_risk_index(data.get("panel"))
    if len(risk_index) > 0:
        risk_index.to_csv(os.path.join(PROC_DIR, "sovereign_risk_index.csv"), index=False)
        print(f"    Saved sovereign_risk_index.csv")

    # 3. Regime Detection
    regime = detect_market_regime(data.get("market"), data.get("yields"), data.get("fx"))
    if len(regime) > 0:
        regime.to_csv(os.path.join(PROC_DIR, "regime_indicators.csv"))
        print(f"    Saved regime_indicators.csv")

    # 4. Deal Screening
    screening = build_deal_screening_model(data.get("mna"))
    if len(screening) > 0:
        screening.to_csv(os.path.join(PROC_DIR, "deal_screening_model.csv"), index=False)
        print(f"    Saved deal_screening_model.csv")

    # 5. IPO Event Study
    event_study = run_ipo_event_study(data.get("ipo"), data.get("market"))
    if len(event_study) > 0:
        event_study.to_csv(os.path.join(PROC_DIR, "ipo_event_study.csv"), index=False)
        print(f"    Saved ipo_event_study.csv")

    print()
    print("=" * 60)
    print("Analysis Complete:")
    outputs = [f for f in os.listdir(PROC_DIR) if f.endswith(".csv")]
    for f in sorted(outputs):
        size = os.path.getsize(os.path.join(PROC_DIR, f))
        print(f"  - {f} ({size:,} bytes)")
    print("=" * 60)


if __name__ == "__main__":
    main()
