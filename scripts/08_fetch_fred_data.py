"""
FRED & Market Data Fetcher
Pulls real yield curve data, macro indicators, and market rates from
FRED (Federal Reserve Economic Data) and Yahoo Finance.
Falls back to cached data if APIs are unavailable.

Outputs:
  data/raw/yield_curve_history.csv
  data/raw/macro_indicators.csv
  data/raw/market_rates.csv
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CACHE_DIR = os.path.join(BASE_DIR, "data", "cache")


def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)


def fetch_treasury_yields():
    """Fetch US Treasury yield curve data from Yahoo Finance."""
    print("  [1/3] Fetching Treasury yield curve data...")

    tickers = {
        "^IRX": "3M",   # 13-week T-bill
        "^FVX": "5Y",   # 5-year Treasury
        "^TNX": "10Y",  # 10-year Treasury
        "^TYX": "30Y",  # 30-year Treasury
    }

    if not HAS_YFINANCE:
        print("    [WARN] yfinance not available, using cached data")
        return _load_cache("yield_curve_history.csv")

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 2)  # 2 years of data

        all_data = []
        for ticker, label in tickers.items():
            print(f"    Fetching {label} ({ticker})...")
            data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"),
                               end=end_date.strftime("%Y-%m-%d"), progress=False)
            if len(data) > 0:
                series = data["Close"].copy()
                series.name = label
                all_data.append(series)
                print(f"    [OK] {label}: {len(data)} data points")
            else:
                print(f"    [WARN] No data for {label}")

        if not all_data:
            print("    [WARN] No yield data retrieved, using cache")
            return _load_cache("yield_curve_history.csv")

        df = pd.concat(all_data, axis=1)
        df.index.name = "date"
        df = df.dropna(how="all")

        # Add derived spreads
        if "10Y" in df.columns and "3M" in df.columns:
            df["10Y_3M_spread"] = df["10Y"] - df["3M"]
        if "30Y" in df.columns and "5Y" in df.columns:
            df["30Y_5Y_spread"] = df["30Y"] - df["5Y"]
        if "10Y" in df.columns and "5Y" in df.columns:
            df["10Y_5Y_spread"] = df["10Y"] - df["5Y"]

        # Flag inversions
        if "10Y_3M_spread" in df.columns:
            df["curve_inverted"] = df["10Y_3M_spread"] < 0

        _save_cache(df, "yield_curve_history.csv")
        print(f"    [OK] Yield curve: {len(df)} trading days, {df.columns.tolist()}")
        return df

    except Exception as e:
        print(f"    [ERR] Yahoo Finance error: {e}")
        print("    Falling back to cache...")
        return _load_cache("yield_curve_history.csv")


def fetch_market_indices():
    """Fetch major market indices and volatility from Yahoo Finance."""
    print("  [2/3] Fetching market indices & volatility...")

    tickers = {
        "^GSPC": "SP500",
        "^VIX": "VIX",
        "^DXY": "USD_Index",
        "GC=F": "Gold",
        "CL=F": "WTI_Oil",
    }

    if not HAS_YFINANCE:
        print("    [WARN] yfinance not available, using cached data")
        return _load_cache("market_rates.csv")

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 2)

        all_data = []
        for ticker, label in tickers.items():
            print(f"    Fetching {label} ({ticker})...")
            data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"),
                               end=end_date.strftime("%Y-%m-%d"), progress=False)
            if len(data) > 0:
                series = data["Close"].copy()
                series.name = label
                all_data.append(series)
                print(f"    [OK] {label}: {len(data)} data points")
            else:
                print(f"    [WARN] No data for {label}")

        if not all_data:
            return _load_cache("market_rates.csv")

        df = pd.concat(all_data, axis=1)
        df.index.name = "date"
        df = df.dropna(how="all")

        # Add rolling metrics
        if "SP500" in df.columns:
            df["SP500_20d_vol"] = df["SP500"].pct_change().rolling(20).std() * np.sqrt(252) * 100
            df["SP500_50d_ma"] = df["SP500"].rolling(50).mean()
            df["SP500_200d_ma"] = df["SP500"].rolling(200).mean()
            df["SP500_above_200ma"] = df["SP500"] > df["SP500_200d_ma"]

        _save_cache(df, "market_rates.csv")
        print(f"    [OK] Market data: {len(df)} trading days")
        return df

    except Exception as e:
        print(f"    [ERR] Yahoo Finance error: {e}")
        return _load_cache("market_rates.csv")


def fetch_fx_rates():
    """Fetch FX rates for EM currencies vs USD."""
    print("  [3/3] Fetching FX rates...")

    fx_pairs = {
        "USDINR=X": "USD_INR",
        "USDBRL=X": "USD_BRL",
        "USDMXN=X": "USD_MXN",
        "USDZAR=X": "USD_ZAR",
        "USDTRY=X": "USD_TRY",
        "USDCNY=X": "USD_CNY",
        "GBPUSD=X": "GBP_USD",
        "EURUSD=X": "EUR_USD",
        "USDJPY=X": "USD_JPY",
    }

    if not HAS_YFINANCE:
        return _load_cache("fx_rates.csv")

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        all_data = []
        for ticker, label in fx_pairs.items():
            data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"),
                               end=end_date.strftime("%Y-%m-%d"), progress=False)
            if len(data) > 0:
                series = data["Close"].copy()
                series.name = label
                all_data.append(series)
                print(f"    [OK] {label}: {len(data)} data points")

        if not all_data:
            return _load_cache("fx_rates.csv")

        df = pd.concat(all_data, axis=1)
        df.index.name = "date"

        # Add rolling volatility for each pair
        for col in df.columns:
            df[f"{col}_30d_vol"] = df[col].pct_change().rolling(30).std() * np.sqrt(252) * 100

        _save_cache(df, "fx_rates.csv")
        print(f"    [OK] FX rates: {len(df)} trading days, {len(fx_pairs)} pairs")
        return df

    except Exception as e:
        print(f"    [ERR] FX fetch error: {e}")
        return _load_cache("fx_rates.csv")


def _save_cache(df, filename):
    """Save dataframe to cache."""
    filepath = os.path.join(CACHE_DIR, filename)
    df.to_csv(filepath)


def _load_cache(filename):
    """Load from cache if available."""
    filepath = os.path.join(CACHE_DIR, filename)
    if os.path.exists(filepath):
        print(f"    [OK] Loaded from cache: {filename}")
        return pd.read_csv(filepath, index_col=0, parse_dates=True)
    print(f"    [ERR] No cache found: {filename}")
    return pd.DataFrame()


def save_outputs(yields_df, market_df, fx_df):
    """Save all data to raw directory."""
    if len(yields_df) > 0:
        yields_df.to_csv(os.path.join(RAW_DIR, "yield_curve_history.csv"))
        print(f"  [OK] Saved yield_curve_history.csv ({len(yields_df)} rows)")
    if len(market_df) > 0:
        market_df.to_csv(os.path.join(RAW_DIR, "market_rates.csv"))
        print(f"  [OK] Saved market_rates.csv ({len(market_df)} rows)")
    if len(fx_df) > 0:
        fx_df.to_csv(os.path.join(RAW_DIR, "fx_rates.csv"))
        print(f"  [OK] Saved fx_rates.csv ({len(fx_df)} rows)")


def main():
    print("=" * 60)
    print("FRED & Market Data Fetcher")
    print("Capital Markets Intelligence Platform")
    print("=" * 60)
    print()

    ensure_dirs()

    yields_df = fetch_treasury_yields()
    market_df = fetch_market_indices()
    fx_df = fetch_fx_rates()

    print()
    print("Saving outputs...")
    save_outputs(yields_df, market_df, fx_df)

    print()
    print("=" * 60)
    print("Summary:")
    if len(yields_df) > 0:
        print(f"  Yield Curve: {len(yields_df)} days")
        if "10Y" in yields_df.columns:
            latest = yields_df.iloc[-1]
            print(f"    Latest 10Y: {latest.get('10Y', 'N/A'):.2f}%")
            if "10Y_3M_spread" in yields_df.columns:
                print(f"    10Y-3M Spread: {latest.get('10Y_3M_spread', 'N/A'):.2f}%")
                print(f"    Curve Inverted: {latest.get('curve_inverted', 'N/A')}")
    if len(market_df) > 0:
        print(f"  Market Indices: {len(market_df)} days")
        if "VIX" in market_df.columns:
            print(f"    Latest VIX: {market_df['VIX'].iloc[-1]:.1f}")
    if len(fx_df) > 0:
        print(f"  FX Rates: {len(fx_df)} days, {sum(1 for c in fx_df.columns if '_vol' not in c)} pairs")
    print("=" * 60)


if __name__ == "__main__":
    main()
