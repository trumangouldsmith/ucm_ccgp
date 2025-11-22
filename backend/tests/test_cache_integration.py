"""
Integration tests for caching in API endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCacheIntegration:
    """Test caching integration with API."""
    
    @patch('app.routers.analytics.cache_service')
    def test_analyze_with_cache_miss(self, mock_cache):
        """Test analysis when cache misses."""
        # Mock cache miss
        mock_cache.get.return_value = None
        mock_cache.set.return_value = True
        
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
        
        # Should indicate not cached
        assert data["cached"] is False
        
        # Should have tried to get from cache
        mock_cache.get.assert_called_once()
        # Should have stored in cache
        mock_cache.set.assert_called_once()
    
    @patch('app.routers.analytics.cache_service')
    def test_analyze_with_cache_hit(self, mock_cache):
        """Test analysis when cache hits."""
        # Mock cache hit with pre-calculated data
        cached_data = {
            'tickers': ['AAPL'],
            'metrics': {
                'AAPL': {
                    'ticker': 'AAPL',
                    'total_return': 5.5,
                    'volatility': 1.2,
                    'average_volume': 85000000.0,
                    'sma_20': [150.0, 151.0],
                    'sma_50': None,
                    'sma_200': None
                }
            },
            'correlation_matrix': None
        }
        
        mock_cache.get.return_value = cached_data
        
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
        
        # Should indicate cached
        assert data["cached"] is True
        
        # Should have metrics from cache
        assert data["metrics"]["AAPL"]["total_return"] == 5.5
        assert data["metrics"]["AAPL"]["volatility"] == 1.2
        
        # Should not have tried to set cache (already cached)
        mock_cache.set.assert_not_called()
    
    @patch('app.routers.analytics.cache_service')
    def test_cache_stats_endpoint(self, mock_cache):
        """Test cache stats endpoint."""
        mock_cache.get_cache_stats.return_value = {
            'count': 10,
            'total_size_bytes': 50000,
            'total_size_mb': 0.05
        }
        
        response = client.get("/api/cache/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['cache_enabled'] is True
        assert data['count'] == 10
        assert data['total_size_bytes'] == 50000
    
    @patch('app.routers.analytics.cache_service')
    def test_clear_cache_endpoint(self, mock_cache):
        """Test clear cache endpoint."""
        mock_cache.clear_all.return_value = 15
        
        response = client.delete("/api/cache/clear")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['cache_enabled'] is True
        assert data['items_cleared'] == 15
        assert 'message' in data
    
    @patch('app.routers.analytics.cache_service', None)
    def test_cache_stats_when_disabled(self):
        """Test cache stats when caching is disabled."""
        response = client.get("/api/cache/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['cache_enabled'] is False
        assert 'message' in data
    
    @patch('app.routers.analytics.cache_service', None)
    def test_clear_cache_when_disabled(self):
        """Test clear cache when caching is disabled."""
        response = client.delete("/api/cache/clear")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['cache_enabled'] is False
        assert 'message' in data

