import math
import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "close",
    "volume",
}

def calculate_return_1d(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage price change from the previous trading day"""
    return df["close"].pct_change()


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
