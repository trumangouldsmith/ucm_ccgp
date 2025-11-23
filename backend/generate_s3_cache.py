"""
Generate pre-cached sample data for S3 cache bucket.
Creates realistic mock stock data with analytics for demo purposes.
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from app.services.mock_data import generate_mock_batch
from app.services.analytics import AnalyticsService


def generate_cache_key(tickers, start_date, end_date, interval):
    """Generate cache key matching CacheService format."""
    sorted_tickers = sorted(tickers)
    key_string = f"{'-'.join(sorted_tickers)}_{start_date}_{end_date}_{interval}"
    hash_object = hashlib.md5(key_string.encode())
    return f"cache/{hash_object.hexdigest()}.json"


def generate_sample_cache_files():
    """Generate multiple cache files for common stock queries."""
    
    output_dir = Path("s3_cache_files")
    output_dir.mkdir(exist_ok=True)
    
    print("Generating S3 cache files for demo...\n")
    
    # Define common queries to pre-cache
    queries = [
        {
            "tickers": ["AAPL", "GOOGL", "MSFT"],
            "start_date": "2024-10-01",
            "end_date": "2024-11-01",
            "interval": "1d",
            "description": "Tech giants - 1 month daily"
        },
        {
            "tickers": ["AAPL", "MSFT"],
            "start_date": "2024-10-01",
            "end_date": "2024-11-01",
            "interval": "1d",
            "description": "AAPL vs MSFT - 1 month"
        },
        {
            "tickers": ["TSLA", "F", "GM"],
            "start_date": "2024-09-01",
            "end_date": "2024-11-01",
            "interval": "1d",
            "description": "Auto sector - 2 months"
        },
        {
            "tickers": ["AAPL", "GOOGL", "MSFT", "AMZN"],
            "start_date": "2024-10-15",
            "end_date": "2024-11-15",
            "interval": "1d",
            "description": "FAANG subset - 1 month"
        },
        {
            "tickers": ["SPY", "QQQ", "DIA"],
            "start_date": "2024-10-01",
            "end_date": "2024-11-01",
            "interval": "1d",
            "description": "Major ETFs - 1 month"
        },
    ]
    
    analytics_service = AnalyticsService()
    
    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Generating: {query['description']}")
        print(f"  Tickers: {', '.join(query['tickers'])}")
        
        # Generate mock stock data
        stock_data = generate_mock_batch(
            tickers=query['tickers'],
            start_date=query['start_date'],
            end_date=query['end_date'],
            interval=query['interval']
        )
        
        # Calculate analytics
        try:
            analytics_result = analytics_service.calculate_analytics(stock_data)
            
            # Format response data
            response_data = {
                "metrics": analytics_result["metrics"],
                "correlation_matrix": analytics_result["correlation_matrix"],
                "historical_data": analytics_result["historical_data"]
            }
            
            # Wrap in cache format
            cache_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": response_data
            }
            
            # Generate cache key
            cache_key = generate_cache_key(
                query['tickers'],
                query['start_date'],
                query['end_date'],
                query['interval']
            )
            
            # Save to file
            filename = cache_key.replace("cache/", "").replace("/", "_")
            file_path = output_dir / filename
            
            with open(file_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            file_size = file_path.stat().st_size / 1024
            print(f"  ✓ Generated: {filename} ({file_size:.1f} KB)")
            print(f"  S3 Key: {cache_key}\n")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}\n")
            continue
    
    print(f"=== Complete ===")
    print(f"Generated {len(list(output_dir.glob('*.json')))} cache files")
    print(f"Output directory: {output_dir.absolute()}")
    print(f"\nUpload to S3:")
    print(f"  Bucket: stock-analyzer-cache-656312098098")
    print(f"  Upload all .json files to 'cache/' prefix")
    print(f"\nManual upload:")
    print(f"  1. Go to S3 Console → stock-analyzer-cache-656312098098")
    print(f"  2. Create folder 'cache' if it doesn't exist")
    print(f"  3. Upload all .json files from {output_dir.absolute()}")
    print(f"  4. Keep the filenames as-is (e.g., abc123.json)")


if __name__ == "__main__":
    generate_sample_cache_files()

