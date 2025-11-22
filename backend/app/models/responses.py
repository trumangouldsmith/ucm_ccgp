"""
Response models for API endpoints.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
import math


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(
        ...,
        description="Health status of the API",
        example="healthy"
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp",
        example="2023-11-22T12:00:00Z"
    )
    version: str = Field(
        ...,
        description="API version",
        example="1.0.0"
    )


class StockMetrics(BaseModel):
    """Performance metrics for a single stock."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    total_return: Optional[float] = Field(None, description="Total return percentage")
    volatility: Optional[float] = Field(None, description="Volatility (standard deviation)")
    average_volume: Optional[float] = Field(None, description="Average trading volume")
    sma_20: Optional[List[Optional[float]]] = Field(None, description="20-day simple moving average")
    sma_50: Optional[List[Optional[float]]] = Field(None, description="50-day simple moving average")
    sma_200: Optional[List[Optional[float]]] = Field(None, description="200-day simple moving average")
    
    @validator('sma_20', 'sma_50', 'sma_200', pre=True)
    def convert_nan_to_none(cls, v):
        """Convert NaN values to None for JSON serialization."""
        if v is None:
            return None
        return [None if (isinstance(x, float) and math.isnan(x)) else x for x in v]
    
    @validator('total_return', 'volatility', 'average_volume', pre=True)
    def convert_nan_float_to_none(cls, v):
        """Convert NaN float values to None."""
        if isinstance(v, float) and math.isnan(v):
            return None
        return v


class StockAnalysisResponse(BaseModel):
    """Response model for stock analysis endpoint."""
    
    request_id: str = Field(
        ...,
        description="Unique identifier for this analysis request"
    )
    tickers: List[str] = Field(
        ...,
        description="List of analyzed ticker symbols"
    )
    metrics: Dict[str, StockMetrics] = Field(
        ...,
        description="Performance metrics for each ticker"
    )
    correlation_matrix: Optional[Dict[str, Dict[str, float]]] = Field(
        None,
        description="Correlation matrix between tickers"
    )
    historical_data: Optional[Dict[str, List[Dict[str, Any]]]] = Field(
        None,
        description="Historical price and volume data for charts"
    )
    cached: bool = Field(
        ...,
        description="Whether results were retrieved from cache"
    )
    timestamp: datetime = Field(
        ...,
        description="Analysis timestamp"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "request_id": "abc123xyz",
                "tickers": ["AAPL", "GOOGL"],
                "metrics": {
                    "AAPL": {
                        "ticker": "AAPL",
                        "total_return": 45.2,
                        "volatility": 0.25,
                        "average_volume": 85000000
                    }
                },
                "correlation_matrix": {
                    "AAPL": {"AAPL": 1.0, "GOOGL": 0.75},
                    "GOOGL": {"AAPL": 0.75, "GOOGL": 1.0}
                },
                "cached": False,
                "timestamp": "2023-11-22T12:00:00Z"
            }
        }

