"""
Mock stock data generator for demo purposes.
Used when Yahoo Finance is unavailable (e.g., AWS IP blocking).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List


def generate_mock_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Generate realistic-looking mock stock data.
    
    Uses random walk with drift to simulate price movements.
    Each ticker gets consistent data based on hash of ticker name.
    """
    # Parse dates
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Determine frequency
    freq_map = {
        "1d": "D",
        "1wk": "W",
        "1mo": "MS",
        "1h": "H",
        "15m": "15T",
        "5m": "5T"
    }
    freq = freq_map.get(interval, "D")
    
    # Generate date range
    dates = pd.date_range(start=start, end=end, freq=freq)
    if len(dates) == 0:
        dates = pd.date_range(start=start, end=end, periods=2)
    
    # Seed based on ticker for consistency
    seed = sum(ord(c) for c in ticker)
    np.random.seed(seed)
    
    # Base price varies by ticker
    base_price = 50 + (seed % 200)
    
    # Generate realistic price movements (random walk with drift)
    n_periods = len(dates)
    returns = np.random.normal(0.0005, 0.02, n_periods)  # Small positive drift
    price_multipliers = np.exp(returns)
    close_prices = base_price * np.cumprod(price_multipliers)
    
    # Generate OHLC from close
    volatility = 0.015
    high_prices = close_prices * (1 + np.abs(np.random.normal(0, volatility, n_periods)))
    low_prices = close_prices * (1 - np.abs(np.random.normal(0, volatility, n_periods)))
    
    # Open is previous close with small gap
    open_prices = np.zeros(n_periods)
    open_prices[0] = base_price
    open_prices[1:] = close_prices[:-1] * (1 + np.random.normal(0, 0.005, n_periods-1))
    
    # Ensure OHLC logic (high is highest, low is lowest)
    for i in range(n_periods):
        high_prices[i] = max(high_prices[i], open_prices[i], close_prices[i])
        low_prices[i] = min(low_prices[i], open_prices[i], close_prices[i])
    
    # Generate volume (higher volume on bigger price moves)
    base_volume = 1000000 + (seed % 5000000)
    volume_multipliers = 1 + np.abs(returns) * 10
    volumes = (base_volume * volume_multipliers).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices,
        'Volume': volumes
    }, index=dates)
    
    df.index.name = 'Date'
    
    return df


def generate_mock_batch(
    tickers: List[str],
    start_date: str,
    end_date: str,
    interval: str = "1d"
) -> Dict[str, pd.DataFrame]:
    """
    Generate mock data for multiple tickers.
    
    Returns dict of {ticker: DataFrame}
    """
    data = {}
    for ticker in tickers:
        df = generate_mock_stock_data(ticker, start_date, end_date, interval)
        if not df.empty:
            data[ticker] = df
    
    return data

