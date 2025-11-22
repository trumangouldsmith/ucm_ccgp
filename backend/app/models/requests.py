"""
Request models for API endpoints.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class DateRange(BaseModel):
    """Date range for stock data retrieval."""
    
    start_date: date = Field(
        ...,
        description="Start date for stock data (YYYY-MM-DD)",
        example="2023-01-01"
    )
    end_date: date = Field(
        ...,
        description="End date for stock data (YYYY-MM-DD)",
        example="2023-12-31"
    )
    
    @validator("end_date")
    def end_date_must_be_after_start_date(cls, v, values):
        """Validate that end_date is after start_date."""
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


class TickerInput(BaseModel):
    """Individual ticker symbol input."""
    
    symbol: str = Field(
        ...,
        description="Stock ticker symbol (e.g., AAPL, GOOGL)",
        min_length=1,
        max_length=10,
        example="AAPL"
    )
    
    @validator("symbol")
    def symbol_must_be_uppercase(cls, v):
        """Convert ticker symbols to uppercase."""
        return v.upper().strip()


class StockAnalysisRequest(BaseModel):
    """Request model for stock performance analysis."""
    
    tickers: List[str] = Field(
        ...,
        description="List of stock ticker symbols to analyze",
        min_items=1,
        max_items=10,
        example=["AAPL", "GOOGL", "MSFT"]
    )
    date_range: DateRange = Field(
        ...,
        description="Date range for analysis"
    )
    interval: Optional[str] = Field(
        default="1d",
        description="Data interval (1d, 1wk, 1mo)",
        example="1d"
    )
    
    @validator("tickers")
    def tickers_must_be_uppercase_and_unique(cls, v):
        """Convert ticker symbols to uppercase and ensure uniqueness."""
        normalized = [ticker.upper().strip() for ticker in v]
        if len(normalized) != len(set(normalized)):
            raise ValueError("Ticker symbols must be unique")
        return normalized
    
    @validator("interval")
    def interval_must_be_valid(cls, v):
        """Validate interval is one of the accepted values."""
        valid_intervals = ["1d", "1wk", "1mo"]
        if v not in valid_intervals:
            raise ValueError(f"interval must be one of {valid_intervals}")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "tickers": ["AAPL", "GOOGL", "MSFT"],
                "date_range": {
                    "start_date": "2023-01-01",
                    "end_date": "2023-12-31"
                },
                "interval": "1d"
            }
        }

