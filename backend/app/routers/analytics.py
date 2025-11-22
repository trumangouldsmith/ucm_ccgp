"""
Analytics endpoints for stock performance analysis.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
import logging
import pandas as pd

from app.models.requests import StockAnalysisRequest
from app.models.responses import StockAnalysisResponse, StockMetrics
from app.services.yahoo_finance import (
    YahooFinanceService,
    InvalidTickerError,
    DataFetchError
)
from app.services.analytics import AnalyticsService
from app.services.cache import CacheService
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize cache service if enabled
cache_service = None
if settings.ENABLE_CACHE and not settings.USE_LOCAL_CACHE:
    try:
        cache_service = CacheService(
            bucket_name=settings.CACHE_BUCKET_NAME,
            ttl_hours=settings.CACHE_TTL_HOURS,
            region_name=settings.AWS_REGION
        )
        logger.info("Cache service initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize cache service: {str(e)}")
        cache_service = None


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
    
    # Generate cache key
    cache_key = None
    cached_data = None
    
    if cache_service:
        cache_key = CacheService.generate_cache_key(
            tickers=request.tickers,
            start_date=str(request.date_range.start_date),
            end_date=str(request.date_range.end_date),
            interval=request.interval
        )
        
        # Try to get from cache
        cached_data = cache_service.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached results for request {request_id}")
            
            # Reconstruct metrics from cached data
            metrics = {
                ticker: StockMetrics(**metric_data)
                for ticker, metric_data in cached_data['metrics'].items()
            }
            
            return StockAnalysisResponse(
                request_id=request_id,
                tickers=cached_data['tickers'],
                metrics=metrics,
                correlation_matrix=cached_data.get('correlation_matrix'),
                historical_data=cached_data.get('historical_data'),
                cached=True,
                timestamp=datetime.utcnow()
            )
    
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
        
        # Prepare historical data for charts
        historical_data = {}
        for ticker, df in stock_data.items():
            historical_data[ticker] = [
                {
                    'date': idx.strftime('%Y-%m-%d'),
                    'close': float(row['Close']) if 'Close' in row and not pd.isna(row['Close']) else None,
                    'volume': int(row['Volume']) if 'Volume' in row and not pd.isna(row['Volume']) else None,
                    'open': float(row['Open']) if 'Open' in row and not pd.isna(row['Open']) else None,
                    'high': float(row['High']) if 'High' in row and not pd.isna(row['High']) else None,
                    'low': float(row['Low']) if 'Low' in row and not pd.isna(row['Low']) else None,
                }
                for idx, row in df.iterrows()
            ]
        
        logger.info(f"Successfully analyzed {len(metrics)} tickers")
        
        # Cache the results
        if cache_service and cache_key:
            cache_data = {
                'tickers': list(stock_data.keys()),
                'metrics': {
                    ticker: metric.dict()
                    for ticker, metric in metrics.items()
                },
                'correlation_matrix': correlation_matrix,
                'historical_data': historical_data
            }
            cache_service.set(cache_key, cache_data)
        
        return StockAnalysisResponse(
            request_id=request_id,
            tickers=list(stock_data.keys()),
            metrics=metrics,
            correlation_matrix=correlation_matrix,
            historical_data=historical_data,
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
        "endpoints": ["/api/analyze", "/api/cache/stats", "/api/cache/clear"]
    }


@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics.
    
    Returns:
        dict: Cache statistics (count, size, etc.)
    """
    if not cache_service:
        return {
            "cache_enabled": False,
            "message": "Cache is not enabled"
        }
    
    try:
        stats = cache_service.get_cache_stats()
        return {
            "cache_enabled": True,
            **stats
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@router.delete("/cache/clear")
async def clear_cache():
    """
    Clear all cached data.
    
    Returns:
        dict: Number of items cleared
    """
    if not cache_service:
        return {
            "cache_enabled": False,
            "message": "Cache is not enabled"
        }
    
    try:
        count = cache_service.clear_all()
        return {
            "cache_enabled": True,
            "items_cleared": count,
            "message": f"Cleared {count} cache entries"
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )

