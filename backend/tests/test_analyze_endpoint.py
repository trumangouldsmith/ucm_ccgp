"""
Tests for stock analysis endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_endpoint_valid_request():
    """Test analyze endpoint with valid request."""
    request_data = {
        "tickers": ["AAPL", "GOOGL"],
        "date_range": {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        },
        "interval": "1d"
    }
    
    response = client.post("/api/analyze", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "request_id" in data
    assert data["tickers"] == ["AAPL", "GOOGL"]
    assert "metrics" in data
    assert "timestamp" in data
    assert data["cached"] is False
    
    # Check metrics exist for each ticker
    assert "AAPL" in data["metrics"]
    assert "GOOGL" in data["metrics"]


def test_analyze_endpoint_invalid_date_range():
    """Test analyze endpoint with invalid date range."""
    request_data = {
        "tickers": ["AAPL"],
        "date_range": {
            "start_date": "2023-12-31",
            "end_date": "2023-01-01"  # End before start
        }
    }
    
    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_invalid_ticker():
    """Test analyze endpoint with duplicate tickers."""
    request_data = {
        "tickers": ["AAPL", "aapl"],  # Duplicates
        "date_range": {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
    }
    
    response = client.post("/api/analyze", json=request_data)
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_case_normalization():
    """Test that ticker symbols are normalized to uppercase."""
    request_data = {
        "tickers": ["aapl", "googl", "MsFt"],  # Mixed case
        "date_range": {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
    }
    
    response = client.post("/api/analyze", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify tickers are uppercase
    assert data["tickers"] == ["AAPL", "GOOGL", "MSFT"]

