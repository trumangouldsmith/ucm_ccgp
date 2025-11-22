"""
Analytics calculations for stock performance metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for calculating stock performance metrics."""
    
    @staticmethod
    def calculate_daily_returns(df: pd.DataFrame) -> pd.Series:
        """
        Calculate daily returns (percentage change).
        
        Args:
            df: DataFrame with 'Close' column
            
        Returns:
            Series of daily returns (as percentages)
        """
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column")
        
        returns = df['Close'].pct_change() * 100
        return returns.dropna()
    
    @staticmethod
    def calculate_total_return(df: pd.DataFrame) -> float:
        """
        Calculate total return over the period.
        
        Args:
            df: DataFrame with 'Close' column
            
        Returns:
            Total return as percentage
        """
        if 'Close' not in df.columns or len(df) < 2:
            return 0.0
        
        start_price = df['Close'].iloc[0]
        end_price = df['Close'].iloc[-1]
        
        if start_price == 0:
            return 0.0
        
        total_return = ((end_price - start_price) / start_price) * 100
        return float(total_return)
    
    @staticmethod
    def calculate_volatility(df: pd.DataFrame) -> float:
        """
        Calculate volatility (standard deviation of daily returns).
        
        Args:
            df: DataFrame with 'Close' column
            
        Returns:
            Volatility as percentage
        """
        daily_returns = AnalyticsService.calculate_daily_returns(df)
        
        if len(daily_returns) < 2:
            return 0.0
        
        volatility = float(daily_returns.std())
        return volatility
    
    @staticmethod
    def calculate_sma(df: pd.DataFrame, window: int) -> List[float]:
        """
        Calculate Simple Moving Average.
        
        Args:
            df: DataFrame with 'Close' column
            window: Window size for moving average
            
        Returns:
            List of SMA values (NaN for periods with insufficient data)
        """
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column")
        
        if window <= 0:
            raise ValueError("Window must be positive")
        
        sma = df['Close'].rolling(window=window).mean()
        return sma.tolist()
    
    @staticmethod
    def calculate_average_volume(df: pd.DataFrame) -> float:
        """
        Calculate average trading volume.
        
        Args:
            df: DataFrame with 'Volume' column
            
        Returns:
            Average volume
        """
        if 'Volume' not in df.columns:
            return 0.0
        
        return float(df['Volume'].mean())
    
    @staticmethod
    def calculate_correlation_matrix(
        stock_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate pairwise correlation matrix between stocks.
        
        Args:
            stock_data: Dictionary mapping ticker symbols to DataFrames
            
        Returns:
            Nested dictionary representing correlation matrix
        """
        if len(stock_data) < 2:
            return {}
        
        # Create a DataFrame with all closing prices
        closes = pd.DataFrame()
        for ticker, df in stock_data.items():
            if 'Close' in df.columns:
                closes[ticker] = df['Close']
        
        if closes.empty:
            return {}
        
        # Calculate correlation matrix
        corr_matrix = closes.corr()
        
        # Convert to nested dictionary
        result = {}
        for ticker1 in corr_matrix.index:
            result[ticker1] = {}
            for ticker2 in corr_matrix.columns:
                value = corr_matrix.loc[ticker1, ticker2]
                # Handle NaN values
                result[ticker1][ticker2] = float(value) if not pd.isna(value) else 0.0
        
        return result
    
    @staticmethod
    def calculate_all_metrics(
        ticker: str,
        df: pd.DataFrame
    ) -> Dict[str, any]:
        """
        Calculate all metrics for a single stock.
        
        Args:
            ticker: Stock ticker symbol
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with all calculated metrics
        """
        try:
            metrics = {
                'ticker': ticker,
                'total_return': AnalyticsService.calculate_total_return(df),
                'volatility': AnalyticsService.calculate_volatility(df),
                'average_volume': AnalyticsService.calculate_average_volume(df),
                'sma_20': AnalyticsService.calculate_sma(df, 20),
                'sma_50': AnalyticsService.calculate_sma(df, 50),
                'sma_200': AnalyticsService.calculate_sma(df, 200),
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics for {ticker}: {str(e)}")
            raise
    
    @staticmethod
    def calculate_volume_trend(df: pd.DataFrame, window: int = 20) -> str:
        """
        Determine volume trend (increasing, decreasing, stable).
        
        Args:
            df: DataFrame with 'Volume' column
            window: Window for trend calculation
            
        Returns:
            Trend description: 'increasing', 'decreasing', or 'stable'
        """
        if 'Volume' not in df.columns or len(df) < window:
            return 'stable'
        
        recent_avg = df['Volume'].tail(window).mean()
        older_avg = df['Volume'].head(window).mean()
        
        if older_avg == 0:
            return 'stable'
        
        change = ((recent_avg - older_avg) / older_avg) * 100
        
        if change > 10:
            return 'increasing'
        elif change < -10:
            return 'decreasing'
        else:
            return 'stable'

