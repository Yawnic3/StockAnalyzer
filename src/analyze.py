import numpy as np
import pandas as pd
from download_data import download_stock

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
