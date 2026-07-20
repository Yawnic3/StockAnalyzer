import math
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = {
    "date",
    "close",
    "volume",
}

def calculate_return_1d(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage price change from the previous trading day"""
    return df["close"].pct_change()

def calculate_momentum_20d(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage price change over the previous 20 trading days"""
    return df["close"].pct_change(periods=20)

def calculate_moving_average(df: pd.DataFrame, window: int) -> pd.Series:
    """Calculate a simply moving average of the closing price"""
    return df["close"].rolling(window=window).mean()

def calculate_volatility(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculate the annualized volatility using daily returns"""
    daily_returns = df["close"].pct_change()
    return daily_returns.rolling(window=window).std() * math.sqrt(252)

def calculate_volume_strength(df: pd.DataFrame, window: int = 20,) -> pd.Series:
    """Calculate today's volume to the average volume over the previous window
    A value of:
        1.0 means normal value
        1.5 means 50% above average
        0.5 means 50% below average"""
    
    average_volume = df["volume"].rolling(window=window).mean()
    return df["volume"] / average_volume.replace(0, np.nan)

def calculate_stock_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate a simple stock score from 0 to 100.

    Score components:
        Trend:          30 points
        Momentum:       30 points
        Volume:         20 points
        Low volatility: 20 points
    """
    score = pd.Series(0.0, index=df.index)

    # Trend score: up to 30 points.
    score += np.where(df["close"] > df["ma_20"], 15, 0)
    score += np.where(df["ma_20"] > df["ma_50"], 15, 0)

    # Momentum score: up to 30 points.
    momentum_score = (df["momentum_20d"] * 300).clip(lower=0, upper=30)
    score += momentum_score.fillna(0)

    # Volume score: up to 20 points.
    volume_score = ((df["volume_strength"] - 1) * 20 + 10).clip(
        lower=0,
        upper=20,
    )
    score += volume_score.fillna(0)

    # Lower volatility receives a higher score.
    volatility_score = (20 - df["volatility_20d"] * 50).clip(
        lower=0,
        upper=20,
    )
    score += volatility_score.fillna(0)

    return score.clip(lower=0, upper=100)

def calculate_indicators(stock_data: pd.DataFrame) -> dict:
    """
    Calculate technical indicators for one stock.
    
    Expected columns:
        date, close, volume
    
    Returns a dictionary of calculatedindicators.
    """

    if stock_data.empty:
        raise ValueError("Input stock_data is empty")
    
    missing_columns = REQUIRED_COLUMNS - set(stock_data.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    
    if stock_data.empty:
        raise ValueError("Input stock_data is empty")
    
    result = stock_data.copy()

    result = result.sort_values(by=["symbol", "date"],).reset_index(drop=True)

    grouped = result.groupby("symbol", group_keys=False)

    result["return_1d"] = grouped.apply(
        lambda stock: calculate_return_1d(stock),
        include_groups = False,
    ).reset_index(level=0, drop=True)
