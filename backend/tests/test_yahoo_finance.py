"""
Tests for Yahoo Finance data fetcher.
"""

import pytest
from datetime import date, timedelta
import pandas as pd

from app.services.yahoo_finance import (
    YahooFinanceService,
    InvalidTickerError,
    DataFetchError
)


class TestYahooFinanceService:
    """Test suite for Yahoo Finance service."""
    
    def test_fetch_valid_ticker(self):
        """Test fetching data for a valid ticker."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        df = YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=start,
            end_date=end,
            interval="1d"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) > 0
        
        # Check expected columns exist
        expected_columns = {'Open', 'High', 'Low', 'Close', 'Volume'}
        assert expected_columns.issubset(set(df.columns))
        
        # Check data types
        assert pd.api.types.is_numeric_dtype(df['Close'])
        assert pd.api.types.is_numeric_dtype(df['Volume'])
    
    def test_fetch_invalid_ticker(self):
        """Test that invalid ticker raises appropriate error."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        with pytest.raises(InvalidTickerError) as exc_info:
            YahooFinanceService.fetch_historical_data(
                ticker="INVALIDTICKER123XYZ",
                start_date=start,
                end_date=end
            )
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_fetch_invalid_date_range(self):
        """Test that invalid date range raises ValueError."""
        start = date(2023, 12, 31)
        end = date(2023, 1, 1)  # End before start
        
        with pytest.raises(ValueError) as exc_info:
            YahooFinanceService.fetch_historical_data(
                ticker="AAPL",
                start_date=start,
                end_date=end
            )
        
        assert "start_date must be before end_date" in str(exc_info.value)
    
    def test_fetch_invalid_interval(self):
        """Test that invalid interval raises ValueError."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        with pytest.raises(ValueError) as exc_info:
            YahooFinanceService.fetch_historical_data(
                ticker="AAPL",
                start_date=start,
                end_date=end,
                interval="5m"  # Invalid for our use case
            )
        
        assert "interval must be one of" in str(exc_info.value)
    
    def test_fetch_weekly_interval(self):
        """Test fetching data with weekly interval."""
        start = date(2023, 1, 1)
        end = date(2023, 3, 31)
        
        df = YahooFinanceService.fetch_historical_data(
            ticker="GOOGL",
            start_date=start,
            end_date=end,
            interval="1wk"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        # Weekly data should have fewer rows than daily
        assert len(df) < 90  # Less than days in the range
    
    def test_fetch_monthly_interval(self):
        """Test fetching data with monthly interval."""
        start = date(2022, 1, 1)
        end = date(2023, 12, 31)
        
        df = YahooFinanceService.fetch_historical_data(
            ticker="MSFT",
            start_date=start,
            end_date=end,
            interval="1mo"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        # Should have roughly 24 months of data
        assert len(df) >= 20  # At least 20 months
    
    def test_ticker_case_insensitive(self):
        """Test that ticker symbols are case-insensitive."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        df_lower = YahooFinanceService.fetch_historical_data(
            ticker="aapl",
            start_date=start,
            end_date=end
        )
        
        df_upper = YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=start,
            end_date=end
        )
        
        # Both should return data
        assert not df_lower.empty
        assert not df_upper.empty
        # Should have same number of rows
        assert len(df_lower) == len(df_upper)
    
    def test_validate_ticker_valid(self):
        """Test ticker validation for valid ticker."""
        assert YahooFinanceService.validate_ticker("AAPL") is True
        assert YahooFinanceService.validate_ticker("GOOGL") is True
        assert YahooFinanceService.validate_ticker("msft") is True  # lowercase
    
    def test_validate_ticker_invalid(self):
        """Test ticker validation for invalid ticker."""
        assert YahooFinanceService.validate_ticker("INVALIDXYZ123") is False
        assert YahooFinanceService.validate_ticker("") is False
    
    def test_get_ticker_info_valid(self):
        """Test getting ticker information for valid ticker."""
        info = YahooFinanceService.get_ticker_info("AAPL")
        
        assert isinstance(info, dict)
        assert 'symbol' in info
        assert 'name' in info
        assert info['symbol'] == 'AAPL'
        assert 'Apple' in info['name']
    
    def test_get_ticker_info_invalid(self):
        """Test getting ticker information for invalid ticker."""
        with pytest.raises(InvalidTickerError):
            YahooFinanceService.get_ticker_info("INVALIDXYZ123")
    
    def test_fetch_multiple_tickers_all_valid(self):
        """Test fetching multiple valid tickers."""
        tickers = ["AAPL", "GOOGL", "MSFT"]
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        results = YahooFinanceService.fetch_multiple_tickers(
            tickers=tickers,
            start_date=start,
            end_date=end
        )
        
        assert isinstance(results, dict)
        assert len(results) == 3
        assert "AAPL" in results
        assert "GOOGL" in results
        assert "MSFT" in results
        
        # Each should be a DataFrame
        for ticker, df in results.items():
            assert isinstance(df, pd.DataFrame)
            assert not df.empty
    
    def test_fetch_multiple_tickers_some_invalid(self):
        """Test fetching multiple tickers with some invalid ones."""
        tickers = ["AAPL", "INVALIDXYZ123", "GOOGL"]
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        results = YahooFinanceService.fetch_multiple_tickers(
            tickers=tickers,
            start_date=start,
            end_date=end
        )
        
        # Should get valid tickers only
        assert len(results) == 2
        assert "AAPL" in results
        assert "GOOGL" in results
        assert "INVALIDXYZ123" not in results
    
    def test_fetch_multiple_tickers_all_invalid(self):
        """Test fetching multiple tickers when all are invalid."""
        tickers = ["INVALID1", "INVALID2"]
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        with pytest.raises(DataFetchError) as exc_info:
            YahooFinanceService.fetch_multiple_tickers(
                tickers=tickers,
                start_date=start,
                end_date=end
            )
        
        assert "Failed to fetch data for all tickers" in str(exc_info.value)
    
    def test_fetch_empty_ticker_list(self):
        """Test that empty ticker list raises ValueError."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        with pytest.raises(ValueError) as exc_info:
            YahooFinanceService.fetch_multiple_tickers(
                tickers=[],
                start_date=start,
                end_date=end
            )
        
        assert "At least one ticker must be provided" in str(exc_info.value)
    
    def test_data_has_datetime_index(self):
        """Test that returned DataFrame has DatetimeIndex."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        
        df = YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=start,
            end_date=end
        )
        
        assert isinstance(df.index, pd.DatetimeIndex)
    
    def test_fetch_long_date_range(self):
        """Test fetching data over a long date range."""
        start = date(2020, 1, 1)
        end = date(2023, 12, 31)
        
        df = YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=start,
            end_date=end
        )
        
        assert not df.empty
        # Should have multiple years of data
        assert len(df) > 900  # Roughly 4 years of trading days
    
    def test_fetch_future_date_range(self):
        """Test fetching with future dates returns error or empty."""
        future_start = date.today() + timedelta(days=365)
        future_end = future_start + timedelta(days=30)
        
        # Should raise an error since no future data exists
        with pytest.raises((DataFetchError, InvalidTickerError, ValueError)):
            YahooFinanceService.fetch_historical_data(
                ticker="AAPL",
                start_date=future_start,
                end_date=future_end
            )

