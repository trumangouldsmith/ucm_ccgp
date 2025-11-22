"""
Yahoo Finance data fetcher service.

This module handles fetching historical stock data from Yahoo Finance API,
with proper error handling for invalid tickers and date ranges.
"""

import yfinance as yf
import pandas as pd
from datetime import date, datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class YahooFinanceError(Exception):
    """Base exception for Yahoo Finance operations."""
    pass


class InvalidTickerError(YahooFinanceError):
    """Raised when a ticker symbol is invalid or not found."""
    pass


class DataFetchError(YahooFinanceError):
    """Raised when data fetching fails."""
    pass


class YahooFinanceService:
    """
    Service for fetching stock data from Yahoo Finance.
    
    This class provides methods to retrieve historical OHLCV 
    (Open, High, Low, Close, Volume) data for stock tickers.
    """
    
    @staticmethod
    def fetch_historical_data(
        ticker: str,
        start_date: date,
        end_date: date,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical stock data for a single ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            start_date: Start date for historical data
            end_date: End date for historical data
            interval: Data interval ('1d', '1wk', '1mo')
            
        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume, Adj Close
            Index is DatetimeIndex
            
        Raises:
            InvalidTickerError: If ticker is invalid or not found
            DataFetchError: If data fetching fails for other reasons
            ValueError: If date range or interval is invalid
        """
        # Validate inputs
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string")
        
        if start_date >= end_date:
            raise ValueError("start_date must be before end_date")
        
        valid_intervals = ["1d", "1wk", "1mo"]
        if interval not in valid_intervals:
            raise ValueError(f"interval must be one of {valid_intervals}")
        
        ticker = ticker.upper().strip()
        
        try:
            # Create ticker object
            stock = yf.Ticker(ticker)
            
            # Fetch historical data
            logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
            
            df = stock.history(
                start=start_date,
                end=end_date,
                interval=interval,
                auto_adjust=False,  # Keep raw prices
                actions=False  # Don't include dividends/splits
            )
            
            # Check if data was returned
            if df is None or df.empty:
                # Try to determine if ticker exists by checking info
                try:
                    info = stock.info
                    # If info is empty or doesn't have basic fields, ticker is invalid
                    if not info or 'symbol' not in info:
                        raise InvalidTickerError(
                            f"Ticker '{ticker}' not found or is invalid"
                        )
                except Exception:
                    raise InvalidTickerError(
                        f"Ticker '{ticker}' not found or is invalid"
                    )
                
                # If ticker exists but no data in range
                raise DataFetchError(
                    f"No data available for {ticker} in date range "
                    f"{start_date} to {end_date}"
                )
            
            # Validate data quality
            if len(df) < 1:
                raise DataFetchError(
                    f"Insufficient data for {ticker} in specified date range"
                )
            
            logger.info(f"Successfully fetched {len(df)} data points for {ticker}")
            
            return df
            
        except InvalidTickerError:
            raise
        except DataFetchError:
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            raise DataFetchError(
                f"Failed to fetch data for {ticker}: {str(e)}"
            )
    
    @staticmethod
    def validate_ticker(ticker: str) -> bool:
        """
        Validate if a ticker symbol exists and can be queried.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            True if ticker is valid, False otherwise
        """
        try:
            ticker = ticker.upper().strip()
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if we got meaningful info back
            # Valid tickers should have at least a symbol or longName
            if info and ('symbol' in info or 'longName' in info):
                return True
            return False
            
        except Exception as e:
            logger.debug(f"Ticker validation failed for {ticker}: {str(e)}")
            return False
    
    @staticmethod
    def get_ticker_info(ticker: str) -> Dict[str, Any]:
        """
        Get metadata information about a ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with ticker information (name, sector, etc.)
            
        Raises:
            InvalidTickerError: If ticker is invalid
        """
        try:
            ticker = ticker.upper().strip()
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info or ('symbol' not in info and 'longName' not in info):
                raise InvalidTickerError(f"Ticker '{ticker}' not found")
            
            # Extract useful information
            return {
                'symbol': info.get('symbol', ticker),
                'name': info.get('longName', info.get('shortName', 'Unknown')),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'Unknown')
            }
            
        except InvalidTickerError:
            raise
        except Exception as e:
            raise InvalidTickerError(
                f"Failed to get info for ticker '{ticker}': {str(e)}"
            )
    
    @staticmethod
    def fetch_multiple_tickers(
        tickers: list[str],
        start_date: date,
        end_date: date,
        interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical data for multiple tickers.
        
        Args:
            tickers: List of stock ticker symbols
            start_date: Start date for historical data
            end_date: End date for historical data
            interval: Data interval ('1d', '1wk', '1mo')
            
        Returns:
            Dictionary mapping ticker symbols to their DataFrames
            Invalid tickers are excluded from results
            
        Raises:
            ValueError: If no valid tickers provided or date range invalid
        """
        if not tickers:
            raise ValueError("At least one ticker must be provided")
        
        results = {}
        errors = {}
        
        for ticker in tickers:
            try:
                df = YahooFinanceService.fetch_historical_data(
                    ticker=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    interval=interval
                )
                results[ticker.upper()] = df
                
            except (InvalidTickerError, DataFetchError) as e:
                errors[ticker.upper()] = str(e)
                logger.warning(f"Failed to fetch {ticker}: {str(e)}")
        
        if not results:
            raise DataFetchError(
                f"Failed to fetch data for all tickers. Errors: {errors}"
            )
        
        if errors:
            logger.info(
                f"Successfully fetched {len(results)} of {len(tickers)} tickers. "
                f"Failed: {list(errors.keys())}"
            )
        
        return results

