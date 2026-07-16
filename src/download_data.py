from pathlib import Path

import pandas as pd
import yfinance as yf


TICKERS = ["AAPL", "MSFT", "NVDA", "AMD", "GOOGL"]
OUTPUT_PATH = Path("data/prices.csv")


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


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    stock_frames = []

    for symbol in TICKERS:
        print(f"Downloading {symbol}...")
        stock_frames.append(download_stock(symbol))

    prices = pd.concat(stock_frames, ignore_index=True)
    prices = prices.sort_values(["symbol", "date"])

    prices.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved {len(prices):,} rows to {OUTPUT_PATH}")
    print(prices.tail())


if __name__ == "__main__":
    main()