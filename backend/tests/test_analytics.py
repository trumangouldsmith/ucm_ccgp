"""
Tests for analytics service.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta

from app.services.analytics import AnalyticsService


class TestAnalyticsService:
    """Test suite for analytics calculations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample stock data for testing."""
        dates = pd.date_range(start='2025-11-01', periods=30, freq='D')
        data = {
            'Close': [100 + i for i in range(30)],  # Steady increase
            'Volume': [1000000 + i*10000 for i in range(30)],
            'Open': [99 + i for i in range(30)],
            'High': [101 + i for i in range(30)],
            'Low': [98 + i for i in range(30)]
        }
        return pd.DataFrame(data, index=dates)
    
    @pytest.fixture
    def volatile_data(self):
        """Create volatile stock data for testing."""
        dates = pd.date_range(start='2025-11-01', periods=30, freq='D')
        # Alternating ups and downs
        closes = [100 + (10 if i % 2 == 0 else -10) for i in range(30)]
        data = {
            'Close': closes,
            'Volume': [1000000] * 30
        }
        return pd.DataFrame(data, index=dates)
    
    def test_calculate_daily_returns(self, sample_data):
        """Test daily returns calculation."""
        returns = AnalyticsService.calculate_daily_returns(sample_data)
        
        assert isinstance(returns, pd.Series)
        assert len(returns) == 29  # One less than input due to pct_change
        
        # Check first return (100 to 101 = 1% increase)
        assert abs(returns.iloc[0] - 1.0) < 0.01
    
    def test_calculate_total_return(self, sample_data):
        """Test total return calculation."""
        total_return = AnalyticsService.calculate_total_return(sample_data)
        
        # Start: 100, End: 129, Return: (129-100)/100 = 29%
        assert abs(total_return - 29.0) < 0.1
    
    def test_calculate_total_return_negative(self):
        """Test total return with declining prices."""
        df = pd.DataFrame({
            'Close': [100, 90, 80]
        })
        
        total_return = AnalyticsService.calculate_total_return(df)
        
        # (80-100)/100 = -20%
        assert abs(total_return - (-20.0)) < 0.1
    
    def test_calculate_volatility(self, sample_data):
        """Test volatility calculation."""
        volatility = AnalyticsService.calculate_volatility(sample_data)
        
        # Steady increase should have low volatility
        assert volatility >= 0
        assert volatility < 1.0  # Less than 1% for steady increases
    
    def test_calculate_volatility_high(self, volatile_data):
        """Test volatility with volatile data."""
        volatility = AnalyticsService.calculate_volatility(volatile_data)
        
        # Alternating prices should have high volatility
        assert volatility > 5.0
    
    def test_calculate_sma_20(self, sample_data):
        """Test 20-day SMA calculation."""
        sma = AnalyticsService.calculate_sma(sample_data, 20)
        
        assert isinstance(sma, list)
        assert len(sma) == len(sample_data)
        
        # First 19 values should be NaN
        assert pd.isna(sma[0])
        assert pd.isna(sma[18])
        
        # 20th value should be average of first 20 closes
        expected_20th = sum(range(100, 120)) / 20
        assert abs(sma[19] - expected_20th) < 0.1
    
    def test_calculate_sma_50(self, sample_data):
        """Test 50-day SMA calculation."""
        sma = AnalyticsService.calculate_sma(sample_data, 50)
        
        assert len(sma) == len(sample_data)
        
        # All values should be NaN (only 30 days of data)
        assert all(pd.isna(val) for val in sma)
    
    def test_calculate_sma_invalid_window(self, sample_data):
        """Test SMA with invalid window."""
        with pytest.raises(ValueError):
            AnalyticsService.calculate_sma(sample_data, 0)
        
        with pytest.raises(ValueError):
            AnalyticsService.calculate_sma(sample_data, -5)
    
    def test_calculate_average_volume(self, sample_data):
        """Test average volume calculation."""
        avg_volume = AnalyticsService.calculate_average_volume(sample_data)
        
        assert avg_volume > 0
        # Should be around 1,145,000 (midpoint of range)
        assert abs(avg_volume - 1145000) < 10000
    
    def test_calculate_correlation_matrix_two_stocks(self):
        """Test correlation matrix with two stocks."""
        dates = pd.date_range(start='2025-11-01', periods=20, freq='D')
        
        stock_data = {
            'AAPL': pd.DataFrame({
                'Close': [100 + i for i in range(20)]
            }, index=dates),
            'GOOGL': pd.DataFrame({
                'Close': [200 + i*2 for i in range(20)]  # Perfect positive correlation
            }, index=dates)
        }
        
        corr_matrix = AnalyticsService.calculate_correlation_matrix(stock_data)
        
        assert 'AAPL' in corr_matrix
        assert 'GOOGL' in corr_matrix
        
        # Diagonal should be 1.0
        assert abs(corr_matrix['AAPL']['AAPL'] - 1.0) < 0.01
        assert abs(corr_matrix['GOOGL']['GOOGL'] - 1.0) < 0.01
        
        # Perfect positive correlation
        assert abs(corr_matrix['AAPL']['GOOGL'] - 1.0) < 0.01
        assert abs(corr_matrix['GOOGL']['AAPL'] - 1.0) < 0.01
    
    def test_calculate_correlation_matrix_negative_correlation(self):
        """Test correlation matrix with negatively correlated stocks."""
        dates = pd.date_range(start='2025-11-01', periods=20, freq='D')
        
        stock_data = {
            'AAPL': pd.DataFrame({
                'Close': [100 + i for i in range(20)]
            }, index=dates),
            'GOOGL': pd.DataFrame({
                'Close': [200 - i for i in range(20)]  # Perfect negative correlation
            }, index=dates)
        }
        
        corr_matrix = AnalyticsService.calculate_correlation_matrix(stock_data)
        
        # Should be close to -1.0
        assert corr_matrix['AAPL']['GOOGL'] < -0.9
    
    def test_calculate_correlation_matrix_single_stock(self):
        """Test correlation matrix with single stock returns empty."""
        dates = pd.date_range(start='2025-11-01', periods=20, freq='D')
        
        stock_data = {
            'AAPL': pd.DataFrame({
                'Close': [100 + i for i in range(20)]
            }, index=dates)
        }
        
        corr_matrix = AnalyticsService.calculate_correlation_matrix(stock_data)
        
        # Should return empty dict for single stock
        assert corr_matrix == {}
    
    def test_calculate_all_metrics(self, sample_data):
        """Test calculating all metrics at once."""
        metrics = AnalyticsService.calculate_all_metrics('AAPL', sample_data)
        
        assert metrics['ticker'] == 'AAPL'
        assert 'total_return' in metrics
        assert 'volatility' in metrics
        assert 'average_volume' in metrics
        assert 'sma_20' in metrics
        assert 'sma_50' in metrics
        assert 'sma_200' in metrics
        
        # Verify types
        assert isinstance(metrics['total_return'], float)
        assert isinstance(metrics['volatility'], float)
        assert isinstance(metrics['average_volume'], float)
        assert isinstance(metrics['sma_20'], list)
        assert isinstance(metrics['sma_50'], list)
        assert isinstance(metrics['sma_200'], list)
    
    def test_calculate_volume_trend_increasing(self):
        """Test volume trend detection - increasing."""
        dates = pd.date_range(start='2025-11-01', periods=40, freq='D')
        # Volume doubles over the period
        volumes = [1000000 + i*50000 for i in range(40)]
        
        df = pd.DataFrame({'Volume': volumes}, index=dates)
        
        trend = AnalyticsService.calculate_volume_trend(df, window=20)
        assert trend == 'increasing'
    
    def test_calculate_volume_trend_decreasing(self):
        """Test volume trend detection - decreasing."""
        dates = pd.date_range(start='2025-11-01', periods=40, freq='D')
        # Volume decreases
        volumes = [2000000 - i*50000 for i in range(40)]
        
        df = pd.DataFrame({'Volume': volumes}, index=dates)
        
        trend = AnalyticsService.calculate_volume_trend(df, window=20)
        assert trend == 'decreasing'
    
    def test_calculate_volume_trend_stable(self):
        """Test volume trend detection - stable."""
        dates = pd.date_range(start='2025-11-01', periods=40, freq='D')
        # Consistent volume
        volumes = [1000000] * 40
        
        df = pd.DataFrame({'Volume': volumes}, index=dates)
        
        trend = AnalyticsService.calculate_volume_trend(df, window=20)
        assert trend == 'stable'
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            AnalyticsService.calculate_daily_returns(df)
    
    def test_missing_columns(self):
        """Test handling of missing required columns."""
        df = pd.DataFrame({'Open': [100, 101, 102]})
        
        with pytest.raises(ValueError):
            AnalyticsService.calculate_daily_returns(df)
    
    def test_calculate_total_return_insufficient_data(self):
        """Test total return with insufficient data."""
        df = pd.DataFrame({'Close': [100]})
        
        total_return = AnalyticsService.calculate_total_return(df)
        assert total_return == 0.0
    
    def test_calculate_total_return_zero_start_price(self):
        """Test total return when start price is zero."""
        df = pd.DataFrame({'Close': [0, 100, 200]})
        
        total_return = AnalyticsService.calculate_total_return(df)
        assert total_return == 0.0

