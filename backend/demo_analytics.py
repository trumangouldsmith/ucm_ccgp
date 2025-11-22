"""
Demonstration of analytics calculations.
"""

from datetime import date
from app.services.yahoo_finance import YahooFinanceService
from app.services.analytics import AnalyticsService
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def demo_single_stock_analytics():
    """Demonstrate analytics for a single stock."""
    print("\n" + "="*70)
    print("Analytics Demo: Single Stock (AAPL)")
    print("="*70)
    
    # Fetch data
    df = YahooFinanceService.fetch_historical_data(
        ticker="AAPL",
        start_date=date(2025, 11, 1),
        end_date=date(2025, 11, 20),
        interval="1d"
    )
    
    # Calculate all metrics
    metrics = AnalyticsService.calculate_all_metrics("AAPL", df)
    
    print(f"\nData period: {df.index.min().date()} to {df.index.max().date()}")
    print(f"Number of trading days: {len(df)}")
    print(f"\nMetrics:")
    print(f"  Total Return: {metrics['total_return']:.2f}%")
    print(f"  Volatility: {metrics['volatility']:.2f}%")
    print(f"  Average Volume: {metrics['average_volume']:,.0f}")
    print(f"\nMoving Averages (last 5 values):")
    print(f"  SMA 20: {[f'{x:.2f}' if not pd.isna(x) else 'N/A' for x in metrics['sma_20'][-5:]]}")
    
    # Volume trend
    trend = AnalyticsService.calculate_volume_trend(df)
    print(f"\nVolume Trend: {trend}")


def demo_multiple_stocks_correlation():
    """Demonstrate correlation analysis between stocks."""
    print("\n" + "="*70)
    print("Analytics Demo: Multiple Stocks Correlation")
    print("="*70)
    
    tickers = ["AAPL", "GOOGL", "MSFT"]
    
    # Fetch data for all tickers
    stock_data = YahooFinanceService.fetch_multiple_tickers(
        tickers=tickers,
        start_date=date(2025, 11, 1),
        end_date=date(2025, 11, 20),
        interval="1d"
    )
    
    # Calculate metrics for each
    print(f"\nIndividual Stock Metrics:")
    for ticker, df in stock_data.items():
        metrics = AnalyticsService.calculate_all_metrics(ticker, df)
        print(f"\n{ticker}:")
        print(f"  Total Return: {metrics['total_return']:+.2f}%")
        print(f"  Volatility: {metrics['volatility']:.2f}%")
        print(f"  Avg Volume: {metrics['average_volume']:,.0f}")
    
    # Calculate correlation matrix
    corr_matrix = AnalyticsService.calculate_correlation_matrix(stock_data)
    
    print(f"\nCorrelation Matrix:")
    print(f"{'':10s}", end='')
    for ticker in tickers:
        print(f"{ticker:>10s}", end='')
    print()
    
    for ticker1 in tickers:
        print(f"{ticker1:10s}", end='')
        for ticker2 in tickers:
            if ticker1 in corr_matrix and ticker2 in corr_matrix[ticker1]:
                print(f"{corr_matrix[ticker1][ticker2]:>10.3f}", end='')
            else:
                print(f"{'N/A':>10s}", end='')
        print()


if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# Analytics Service - Demonstration")
    print("#"*70)
    
    demo_single_stock_analytics()
    demo_multiple_stocks_correlation()
    
    print("\n" + "="*70)
    print("Demonstration complete!")
    print("="*70 + "\n")

