from pathlib import Path

import pandas as pd
import yfinance as yf

def download_stock(symbol: str) -> pd.DataFrame:
    """Download two years of adjusted daily data for one stock."""

    ticker = yf.Ticker(symbol)

    history = ticker.history(
        period="2y",
        interval="1d",
        auto_adjust=True,
    )

    if history.empty:
        raise RuntimeError(f"No data returned for {symbol}")

    history = history.reset_index()

    history = history.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    history["symbol"] = symbol

    required_columns = [
        "date",
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    return history[required_columns]


