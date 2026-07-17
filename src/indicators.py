import math
import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "close",
    "volume",
}

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