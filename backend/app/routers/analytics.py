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
from app.services.analytics import AnalyticsService

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
        
        # Calculate metrics for each ticker
        metrics = {}
        for ticker, df in stock_data.items():
            calculated = AnalyticsService.calculate_all_metrics(ticker, df)
            
            metrics[ticker] = StockMetrics(
                ticker=ticker,
                total_return=calculated['total_return'],
                volatility=calculated['volatility'],
                average_volume=calculated['average_volume'],
                sma_20=calculated['sma_20'],
                sma_50=calculated['sma_50'],
                sma_200=calculated['sma_200']
            )
        
        # Calculate correlation matrix if multiple tickers
        correlation_matrix = None
        if len(stock_data) > 1:
            correlation_matrix = AnalyticsService.calculate_correlation_matrix(stock_data)
        
        logger.info(f"Successfully analyzed {len(metrics)} tickers")
        
        return StockAnalysisResponse(
            request_id=request_id,
            tickers=list(stock_data.keys()),
            metrics=metrics,
            correlation_matrix=correlation_matrix,
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

