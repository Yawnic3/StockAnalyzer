import math

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "date",
    "symbol",
    "close",
    "volume",
}


def calculate_return_1d(prices: pd.Series) -> pd.Series:
    """Calculate the percentage price change from the previous trading day."""
    return prices.pct_change(fill_method=None)


def calculate_momentum_20d(prices: pd.Series) -> pd.Series:
    """Calculate the percentage price change over 20 trading days."""
    return prices.pct_change(
        periods=20,
        fill_method=None,
    )


def calculate_moving_average(
    prices: pd.Series,
    window: int,
) -> pd.Series:
    """Calculate a simple moving average of closing prices."""
    return prices.rolling(window=window).mean()


def calculate_volatility(
    prices: pd.Series,
    window: int = 20,
) -> pd.Series:
    """Calculate annualized volatility using daily returns."""
    daily_returns = prices.pct_change(fill_method=None)

    return (
        daily_returns
        .rolling(window=window)
        .std()
        * math.sqrt(252)
    )


def calculate_volume_strength(
    volumes: pd.Series,
    window: int = 20,
) -> pd.Series:
    """
    Compare current volume with average volume.

    Values:
        1.0 means normal volume
        1.5 means 50% above average
        0.5 means 50% below average
    """
    average_volume = volumes.rolling(window=window).mean()

    return volumes / average_volume.replace(0, np.nan)


def calculate_stock_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate a stock score from 0 to 100.

    Score components:
        Trend:          30 points
        Momentum:       30 points
        Volume:         20 points
        Low volatility: 20 points
    """
    score = pd.Series(
        0.0,
        index=df.index,
        dtype=float,
    )

    # Trend score: up to 30 points.
    score += np.where(
        df["close"] > df["ma_20"],
        15,
        0,
    )

    score += np.where(
        df["ma_20"] > df["ma_50"],
        15,
        0,
    )

    # Momentum score: up to 30 points.
    momentum_score = (
        df["momentum_20d"] * 300
    ).clip(
        lower=0,
        upper=30,
    )

    score += momentum_score.fillna(0)

    # Volume score: up to 20 points.
    volume_score = (
        (df["volume_strength"] - 1) * 20 + 10
    ).clip(
        lower=0,
        upper=20,
    )

    score += volume_score.fillna(0)

    # Low-volatility score: up to 20 points.
    volatility_score = (
        20 - df["volatility_20d"] * 50
    ).clip(
        lower=0,
        upper=20,
    )

    score += volatility_score.fillna(0)

    return score.clip(
        lower=0,
        upper=100,
    )


def calculate_indicators(
    stock_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate technical indicators for one or more stocks.

    Expected columns:
        date, symbol, close, volume

    Returns:
        A DataFrame containing the original data and calculated indicators.
    """
    if stock_data.empty:
        raise ValueError("Input stock_data is empty.")

    missing_columns = REQUIRED_COLUMNS - set(stock_data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = stock_data.copy()

    result["date"] = pd.to_datetime(
        result["date"],
        errors="raise",
    )

    result = result.sort_values(
        by=["symbol", "date"],
    ).reset_index(drop=True)

    grouped_close = result.groupby(
        "symbol",
        sort=False,
    )["close"]

    grouped_volume = result.groupby(
        "symbol",
        sort=False,
    )["volume"]

    result["return_1d"] = grouped_close.transform(
        calculate_return_1d
    )

    result["momentum_20d"] = grouped_close.transform(
        calculate_momentum_20d
    )

    result["ma_20"] = grouped_close.transform(
        lambda prices: calculate_moving_average(
            prices,
            window=20,
        )
    )

    result["ma_50"] = grouped_close.transform(
        lambda prices: calculate_moving_average(
            prices,
            window=50,
        )
    )

    result["volatility_20d"] = grouped_close.transform(
        lambda prices: calculate_volatility(
            prices,
            window=20,
        )
    )

    result["volume_strength"] = grouped_volume.transform(
        lambda volumes: calculate_volume_strength(
            volumes,
            window=20,
        )
    )

    result["stock_score"] = calculate_stock_score(result)

    return result