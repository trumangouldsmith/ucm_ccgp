"""
Demonstration script for Yahoo Finance data fetcher.

This script shows how to use the YahooFinanceService to fetch stock data.
Run this to verify the Yahoo Finance integration is working.
"""

from datetime import date
from app.services.yahoo_finance import YahooFinanceService
import pandas as pd

# Configure pandas display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def demo_single_ticker():
    """Demonstrate fetching data for a single ticker."""
    print("\n" + "="*70)
    print("DEMO 1: Fetching Single Ticker (AAPL)")
    print("="*70)
    
    try:
        df = YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=date(2025, 11, 17),
            end_date=date(2025, 11, 21),
            interval="1d"
        )
        
        print(f"\nSuccessfully fetched {len(df)} days of data for AAPL")
        print(f"\nData columns: {list(df.columns)}")
        print(f"\nFirst 5 rows:")
        print(df.head())
        print(f"\nLast 5 rows:")
        print(df.tail())
        
        # Show some basic statistics
        print(f"\nBasic Statistics:")
        print(f"  Average Close Price: ${df['Close'].mean():.2f}")
        print(f"  Highest Price: ${df['High'].max():.2f}")
        print(f"  Lowest Price: ${df['Low'].min():.2f}")
        print(f"  Average Volume: {df['Volume'].mean():,.0f}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_multiple_tickers():
    """Demonstrate fetching data for multiple tickers."""
    print("\n" + "="*70)
    print("DEMO 2: Fetching Multiple Tickers (AAPL, GOOGL, MSFT)")
    print("="*70)
    
    tickers = ["AAPL", "GOOGL", "MSFT"]
    
    try:
        results = YahooFinanceService.fetch_multiple_tickers(
            tickers=tickers,
            start_date=date(2025, 11, 17),
            end_date=date(2025, 11, 21),
            interval="1d"
        )
        
        print(f"\nSuccessfully fetched data for {len(results)} tickers")
        
        for ticker, df in results.items():
            print(f"\n{ticker}:")
            print(f"  Data points: {len(df)}")
            print(f"  Date range: {df.index.min().date()} to {df.index.max().date()}")
            print(f"  Avg Close: ${df['Close'].mean():.2f}")
            print(f"  Price range: ${df['Low'].min():.2f} - ${df['High'].max():.2f}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_ticker_validation():
    """Demonstrate ticker validation."""
    print("\n" + "="*70)
    print("DEMO 3: Ticker Validation")
    print("="*70)
    
    test_tickers = ["AAPL", "GOOGL", "INVALIDXYZ123", "MSFT", "FAKESTOCK"]
    
    print("\nValidating tickers...")
    for ticker in test_tickers:
        is_valid = YahooFinanceService.validate_ticker(ticker)
        status = "VALID" if is_valid else "INVALID"
        print(f"  {ticker:20s} -> {status}")


def demo_ticker_info():
    """Demonstrate getting ticker information."""
    print("\n" + "="*70)
    print("DEMO 4: Getting Ticker Information")
    print("="*70)
    
    tickers = ["AAPL", "GOOGL", "TSLA"]
    
    for ticker in tickers:
        try:
            info = YahooFinanceService.get_ticker_info(ticker)
            print(f"\n{ticker}:")
            print(f"  Name: {info['name']}")
            print(f"  Sector: {info['sector']}")
            print(f"  Industry: {info['industry']}")
            print(f"  Exchange: {info['exchange']}")
        except Exception as e:
            print(f"\n{ticker}: Error - {e}")


def demo_different_intervals():
    """Demonstrate different time intervals."""
    print("\n" + "="*70)
    print("DEMO 5: Different Time Intervals")
    print("="*70)
    
    intervals = ["1d", "1wk", "1mo"]
    
    for interval in intervals:
        try:
            df = YahooFinanceService.fetch_historical_data(
                ticker="AAPL",
            start_date=date(2025, 11, 17),
            end_date=date(2025, 11, 21),
                interval=interval
            )
            print(f"\nInterval '{interval}':")
            print(f"  Data points: {len(df)}")
            print(f"  First date: {df.index.min().date()}")
            print(f"  Last date: {df.index.max().date()}")
        except Exception as e:
            print(f"\nInterval '{interval}': Error - {e}")


def demo_error_handling():
    """Demonstrate error handling."""
    print("\n" + "="*70)
    print("DEMO 6: Error Handling")
    print("="*70)
    
    print("\n1. Testing invalid ticker...")
    try:
        YahooFinanceService.fetch_historical_data(
            ticker="INVALIDTICKER123",
            start_date=date(2025, 11, 17),
            end_date=date(2025, 11, 21),
        )
    except Exception as e:
        print(f"   Caught expected error: {type(e).__name__}: {e}")
    
    print("\n2. Testing invalid date range (end before start)...")
    try:
        YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=date(2025, 11, 17),
            end_date=date(2025, 11, 21),
        )
    except Exception as e:
        print(f"   Caught expected error: {type(e).__name__}: {e}")
    
    print("\n3. Testing invalid interval...")
    try:
        YahooFinanceService.fetch_historical_data(
            ticker="AAPL",
            start_date=date(2025, 11, 17),
            end_date=date(2025, 11, 21),
            interval="5m"
        )
    except Exception as e:
        print(f"   Caught expected error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# Yahoo Finance Data Fetcher - Demonstration")
    print("#"*70)
    print("\nThis script demonstrates the Yahoo Finance integration.")
    print("It will fetch real stock data from Yahoo Finance API.")
    print("\nNote: This requires an internet connection.")
    
    # Run all demonstrations
    demo_single_ticker()
    demo_multiple_tickers()
    demo_ticker_validation()
    demo_ticker_info()
    demo_different_intervals()
    demo_error_handling()
    
    print("\n" + "="*70)
    print("Demonstration complete!")
    print("="*70 + "\n")

