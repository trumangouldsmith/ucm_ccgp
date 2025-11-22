"""
Tests for Pydantic models.
"""

import pytest
from datetime import date
from pydantic import ValidationError

from app.models.requests import DateRange, StockAnalysisRequest


def test_date_range_valid():
    """Test valid date range."""
    dr = DateRange(
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31)
    )
    assert dr.start_date == date(2023, 1, 1)
    assert dr.end_date == date(2023, 12, 31)


def test_date_range_invalid():
    """Test that end_date before start_date raises validation error."""
    with pytest.raises(ValidationError) as exc_info:
        DateRange(
            start_date=date(2023, 12, 31),
            end_date=date(2023, 1, 1)
        )
    assert "end_date must be after start_date" in str(exc_info.value)


def test_stock_analysis_request_valid():
    """Test valid stock analysis request."""
    request = StockAnalysisRequest(
        tickers=["AAPL", "googl", "msft"],  # Mixed case to test normalization
        date_range=DateRange(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        ),
        interval="1d"
    )
    
    # Check tickers are normalized to uppercase
    assert request.tickers == ["AAPL", "GOOGL", "MSFT"]
    assert request.interval == "1d"


def test_stock_analysis_request_duplicate_tickers():
    """Test that duplicate tickers raise validation error."""
    with pytest.raises(ValidationError) as exc_info:
        StockAnalysisRequest(
            tickers=["AAPL", "aapl"],  # Duplicates (case-insensitive)
            date_range=DateRange(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31)
            )
        )
    assert "Ticker symbols must be unique" in str(exc_info.value)


def test_stock_analysis_request_invalid_interval():
    """Test invalid interval raises validation error."""
    with pytest.raises(ValidationError) as exc_info:
        StockAnalysisRequest(
            tickers=["AAPL"],
            date_range=DateRange(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31)
            ),
            interval="5m"  # Invalid interval
        )
    assert "interval must be one of" in str(exc_info.value)


def test_stock_analysis_request_too_many_tickers():
    """Test that more than 10 tickers raises validation error."""
    with pytest.raises(ValidationError):
        StockAnalysisRequest(
            tickers=["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", 
                    "META", "NVDA", "NFLX", "AMD", "INTC", "CSCO"],  # 11 tickers
            date_range=DateRange(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31)
            )
        )


def test_stock_analysis_request_empty_tickers():
    """Test that empty ticker list raises validation error."""
    with pytest.raises(ValidationError):
        StockAnalysisRequest(
            tickers=[],
            date_range=DateRange(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12, 31)
            )
        )

