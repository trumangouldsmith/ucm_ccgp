"""
Integration tests for the complete API with Yahoo Finance.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAnalyticsIntegration:
    """Integration tests for analytics endpoint with real Yahoo Finance data."""
    
    def test_analyze_single_ticker_success(self):
        """Test analyzing a single ticker successfully fetches data."""
        request_data = {
            "tickers": ["AAPL"],
            "date_range": {
                "start_date": "2025-11-01",
                "end_date": "2025-11-20"
            },
            "interval": "1d"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["tickers"] == ["AAPL"]
        assert "AAPL" in data["metrics"]
        
        metrics = data["metrics"]["AAPL"]
        assert metrics["ticker"] == "AAPL"
        assert metrics["average_volume"] is not None
        assert metrics["total_return"] is not None
        assert metrics["volatility"] is not None
        assert metrics["sma_20"] is not None
        assert metrics["sma_50"] is not None
        assert metrics["sma_200"] is not None
        
        assert data["cached"] is False
    
    def test_analyze_multiple_tickers_success(self):
        """Test analyzing multiple tickers successfully."""
        request_data = {
            "tickers": ["AAPL", "GOOGL", "MSFT"],
            "date_range": {
                "start_date": "2025-11-01",
                "end_date": "2025-11-20"
            },
            "interval": "1d"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["tickers"]) == 3
        assert "AAPL" in data["metrics"]
        assert "GOOGL" in data["metrics"]
        assert "MSFT" in data["metrics"]
        
        # Each ticker should have all metrics calculated
        for ticker in ["AAPL", "GOOGL", "MSFT"]:
            metrics = data["metrics"][ticker]
            assert metrics["average_volume"] is not None
            assert metrics["average_volume"] > 0
            assert metrics["total_return"] is not None
            assert metrics["volatility"] is not None
            assert isinstance(metrics["volatility"], float)
        
        # Should have correlation matrix
        assert data["correlation_matrix"] is not None
        assert "AAPL" in data["correlation_matrix"]
        assert "GOOGL" in data["correlation_matrix"]
        assert "MSFT" in data["correlation_matrix"]
    
    def test_analyze_invalid_ticker_returns_error(self):
        """Test that invalid ticker returns appropriate error."""
        request_data = {
            "tickers": ["INVALIDTICKER123XYZ"],
            "date_range": {
                "start_date": "2025-11-01",
                "end_date": "2025-11-20"
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        # Should return 503 (service unavailable) or 400 (bad request)
        assert response.status_code in [400, 503]
        assert "detail" in response.json()
    
    def test_analyze_weekly_interval(self):
        """Test analyzing with weekly interval."""
        request_data = {
            "tickers": ["AAPL"],
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-11-20"
            },
            "interval": "1wk"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "AAPL" in data["metrics"]
        assert data["metrics"]["AAPL"]["total_return"] is not None
    
    def test_analyze_monthly_interval(self):
        """Test analyzing with monthly interval."""
        request_data = {
            "tickers": ["GOOGL"],
            "date_range": {
                "start_date": "2024-01-01",
                "end_date": "2025-11-20"
            },
            "interval": "1mo"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "GOOGL" in data["metrics"]
        assert data["metrics"]["GOOGL"]["volatility"] is not None
    
    def test_analyze_case_insensitive_tickers(self):
        """Test that ticker symbols are case-insensitive."""
        request_data = {
            "tickers": ["aapl", "GooGL"],
            "date_range": {
                "start_date": "2025-11-01",
                "end_date": "2025-11-20"
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be normalized to uppercase
        assert "AAPL" in data["tickers"]
        assert "GOOGL" in data["tickers"]
        
        # Should have correlation matrix for 2+ tickers
        assert data["correlation_matrix"] is not None
    
    def test_analyze_long_date_range(self):
        """Test analyzing over a longer date range."""
        request_data = {
            "tickers": ["MSFT"],
            "date_range": {
                "start_date": "2024-01-01",
                "end_date": "2025-11-20"
            },
            "interval": "1d"
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "MSFT" in data["metrics"]
        
        metrics = data["metrics"]["MSFT"]
        assert metrics["average_volume"] > 0
        assert metrics["total_return"] is not None
        
        # Long range should have SMA 200 data
        assert metrics["sma_200"] is not None
        assert len(metrics["sma_200"]) > 200
    
    def test_analyze_has_request_id(self):
        """Test that response includes unique request ID."""
        request_data = {
            "tickers": ["AAPL"],
            "date_range": {
                "start_date": "2025-11-01",
                "end_date": "2025-11-20"
            }
        }
        
        response1 = client.post("/api/analyze", json=request_data)
        response2 = client.post("/api/analyze", json=request_data)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Request IDs should be unique
        assert response1.json()["request_id"] != response2.json()["request_id"]
    
    def test_analyze_response_structure(self):
        """Test that response has correct structure."""
        request_data = {
            "tickers": ["AAPL"],
            "date_range": {
                "start_date": "2025-11-01",
                "end_date": "2025-11-20"
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "request_id" in data
        assert "tickers" in data
        assert "metrics" in data
        assert "correlation_matrix" in data
        assert "cached" in data
        assert "timestamp" in data
        
        # Check metrics structure
        metrics = data["metrics"]["AAPL"]
        assert "ticker" in metrics
        assert "total_return" in metrics
        assert "volatility" in metrics
        assert "average_volume" in metrics
        assert "sma_20" in metrics
        assert "sma_50" in metrics
        assert "sma_200" in metrics
        
        # Verify data types
        assert isinstance(metrics["total_return"], (int, float))
        assert isinstance(metrics["volatility"], (int, float))
        assert isinstance(metrics["average_volume"], (int, float))
        assert isinstance(metrics["sma_20"], list)
        assert isinstance(metrics["sma_50"], list)
        assert isinstance(metrics["sma_200"], list)

