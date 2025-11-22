"""
Analytics endpoints for stock performance analysis.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
import logging

from app.models.requests import StockAnalysisRequest
from app.models.responses import StockAnalysisResponse, StockMetrics
from app.services.yahoo_finance import (
    YahooFinanceService,
    InvalidTickerError,
    DataFetchError
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=StockAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_stocks(request: StockAnalysisRequest):
    """
    Analyze stock performance for multiple tickers over a specified date range.
    
    This endpoint will:
    - Fetch historical stock data from Yahoo Finance
    - Calculate performance metrics (returns, volatility, correlations, moving averages)
    - Cache results in S3 for future requests
    - Return comprehensive analysis
    
    Args:
        request: StockAnalysisRequest containing tickers and date range
        
    Returns:
        StockAnalysisResponse: Comprehensive analysis results
        
    Raises:
        HTTPException: If data fetching or analysis fails
    """
    request_id = str(uuid.uuid4())
    logger.info(f"Processing analysis request {request_id} for tickers: {request.tickers}")
    
    try:
        # Fetch historical data for all tickers
        stock_data = YahooFinanceService.fetch_multiple_tickers(
            tickers=request.tickers,
            start_date=request.date_range.start_date,
            end_date=request.date_range.end_date,
            interval=request.interval
        )
        
        # Build metrics for each ticker (calculations will be added in Task 4)
        metrics = {}
        for ticker, df in stock_data.items():
            # For now, just store basic info - Task 4 will add calculations
            avg_volume = df['Volume'].mean() if 'Volume' in df.columns else None
            
            metrics[ticker] = StockMetrics(
                ticker=ticker,
                total_return=None,      # Task 4: Calculate total return
                volatility=None,         # Task 4: Calculate volatility
                average_volume=float(avg_volume) if avg_volume else None,
                sma_20=None,            # Task 4: Calculate SMA
                sma_50=None,            # Task 4: Calculate SMA
                sma_200=None            # Task 4: Calculate SMA
            )
        
        logger.info(f"Successfully fetched data for {len(metrics)} tickers")
        
        return StockAnalysisResponse(
            request_id=request_id,
            tickers=list(stock_data.keys()),
            metrics=metrics,
            correlation_matrix=None,  # Task 4: Calculate correlation matrix
            cached=False,
            timestamp=datetime.utcnow()
        )
        
    except DataFetchError as e:
        logger.error(f"Data fetch error for request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch stock data: {str(e)}"
        )
    except InvalidTickerError as e:
        logger.warning(f"Invalid ticker in request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ticker symbol: {str(e)}"
        )
    except Exception as e:
        logger.exception(f"Unexpected error in request {request_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/test")
async def test_endpoint():
    """
    Simple test endpoint to verify routing is working.
    
    Returns:
        dict: Test message
    """
    return {
        "message": "Analytics router is working!",
        "endpoints": ["/api/analyze"]
    }

