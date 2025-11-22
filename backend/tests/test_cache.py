"""
Tests for cache service.
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError

from app.services.cache import CacheService


class TestCacheService:
    """Test suite for cache service."""
    
    def test_generate_cache_key(self):
        """Test cache key generation."""
        key = CacheService.generate_cache_key(
            tickers=["AAPL", "GOOGL"],
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        assert key.startswith("cache/")
        assert key.endswith(".json")
        assert len(key) > 10
    
    def test_generate_cache_key_consistent(self):
        """Test that same inputs generate same key."""
        key1 = CacheService.generate_cache_key(
            tickers=["AAPL", "GOOGL"],
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        key2 = CacheService.generate_cache_key(
            tickers=["AAPL", "GOOGL"],
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        assert key1 == key2
    
    def test_generate_cache_key_ticker_order_independent(self):
        """Test that ticker order doesn't affect cache key."""
        key1 = CacheService.generate_cache_key(
            tickers=["AAPL", "GOOGL"],
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        key2 = CacheService.generate_cache_key(
            tickers=["GOOGL", "AAPL"],  # Different order
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        assert key1 == key2
    
    def test_generate_cache_key_different_params(self):
        """Test that different parameters generate different keys."""
        key1 = CacheService.generate_cache_key(
            tickers=["AAPL"],
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        key2 = CacheService.generate_cache_key(
            tickers=["GOOGL"],  # Different ticker
            start_date="2025-11-01",
            end_date="2025-11-20",
            interval="1d"
        )
        
        assert key1 != key2
    
    @patch('boto3.client')
    def test_get_cache_hit(self, mock_boto):
        """Test successful cache retrieval."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock S3 response
        cache_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'data': {'test': 'data'}
        }
        
        mock_s3.get_object.return_value = {
            'Body': Mock(read=lambda: json.dumps(cache_data).encode('utf-8'))
        }
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        result = cache_service.get("cache/test.json")
        
        assert result == {'test': 'data'}
        mock_s3.get_object.assert_called_once()
    
    @patch('boto3.client')
    def test_get_cache_miss(self, mock_boto):
        """Test cache miss (key not found)."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock S3 NoSuchKey error
        error_response = {'Error': {'Code': 'NoSuchKey'}}
        mock_s3.get_object.side_effect = ClientError(error_response, 'GetObject')
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        result = cache_service.get("cache/missing.json")
        
        assert result is None
    
    @patch('boto3.client')
    def test_get_cache_expired(self, mock_boto):
        """Test expired cache returns None."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock S3 response with old timestamp
        old_timestamp = (datetime.utcnow() - timedelta(hours=25)).isoformat()
        cache_data = {
            'timestamp': old_timestamp,
            'data': {'test': 'data'}
        }
        
        mock_s3.get_object.return_value = {
            'Body': Mock(read=lambda: json.dumps(cache_data).encode('utf-8'))
        }
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket", ttl_hours=24)
        result = cache_service.get("cache/test.json")
        
        assert result is None
        # Should also delete expired cache
        mock_s3.delete_object.assert_called_once()
    
    @patch('boto3.client')
    def test_set_cache(self, mock_boto):
        """Test storing data in cache."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        data = {'test': 'data', 'value': 123}
        result = cache_service.set("cache/test.json", data)
        
        assert result is True
        mock_s3.put_object.assert_called_once()
        
        # Verify the call
        call_args = mock_s3.put_object.call_args
        assert call_args[1]['Bucket'] == 'test-bucket'
        assert call_args[1]['Key'] == 'cache/test.json'
        assert call_args[1]['ContentType'] == 'application/json'
    
    @patch('boto3.client')
    def test_delete_cache(self, mock_boto):
        """Test deleting cache entry."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        result = cache_service.delete("cache/test.json")
        
        assert result is True
        mock_s3.delete_object.assert_called_once_with(
            Bucket='test-bucket',
            Key='cache/test.json'
        )
    
    @patch('boto3.client')
    def test_clear_all_cache(self, mock_boto):
        """Test clearing all cache entries."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock list_objects response
        mock_s3.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'cache/test1.json'},
                {'Key': 'cache/test2.json'},
                {'Key': 'cache/test3.json'}
            ]
        }
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        count = cache_service.clear_all()
        
        assert count == 3
        mock_s3.delete_objects.assert_called_once()
    
    @patch('boto3.client')
    def test_clear_all_cache_empty(self, mock_boto):
        """Test clearing cache when empty."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock empty list_objects response
        mock_s3.list_objects_v2.return_value = {}
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        count = cache_service.clear_all()
        
        assert count == 0
        mock_s3.delete_objects.assert_not_called()
    
    @patch('boto3.client')
    def test_get_cache_stats(self, mock_boto):
        """Test getting cache statistics."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock list_objects response
        mock_s3.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'cache/test1.json', 'Size': 1024},
                {'Key': 'cache/test2.json', 'Size': 2048},
                {'Key': 'cache/test3.json', 'Size': 1024}
            ]
        }
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        stats = cache_service.get_cache_stats()
        
        assert stats['count'] == 3
        assert stats['total_size_bytes'] == 4096
        assert stats['total_size_mb'] > 0
    
    @patch('boto3.client')
    def test_get_cache_stats_empty(self, mock_boto):
        """Test cache stats when empty."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock empty list_objects response
        mock_s3.list_objects_v2.return_value = {}
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        stats = cache_service.get_cache_stats()
        
        assert stats['count'] == 0
        assert stats['total_size_bytes'] == 0
        assert stats['total_size_mb'] == 0.0
    
    @patch('boto3.client')
    def test_set_cache_handles_error(self, mock_boto):
        """Test that set cache handles errors gracefully."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock S3 error
        mock_s3.put_object.side_effect = Exception("S3 error")
        
        # Test
        cache_service = CacheService(bucket_name="test-bucket")
        result = cache_service.set("cache/test.json", {'test': 'data'})
        
        assert result is False
    
    @patch('boto3.client')
    def test_custom_ttl(self, mock_boto):
        """Test cache with custom TTL."""
        # Setup mock
        mock_s3 = Mock()
        mock_boto.return_value = mock_s3
        
        # Mock S3 response with timestamp 2 hours old
        old_timestamp = (datetime.utcnow() - timedelta(hours=2)).isoformat()
        cache_data = {
            'timestamp': old_timestamp,
            'data': {'test': 'data'}
        }
        
        mock_s3.get_object.return_value = {
            'Body': Mock(read=lambda: json.dumps(cache_data).encode('utf-8'))
        }
        
        # Test with 1 hour TTL (should be expired)
        cache_service = CacheService(bucket_name="test-bucket", ttl_hours=1)
        result = cache_service.get("cache/test.json")
        assert result is None
        
        # Test with 3 hour TTL (should not be expired)
        cache_service = CacheService(bucket_name="test-bucket", ttl_hours=3)
        result = cache_service.get("cache/test.json")
        assert result == {'test': 'data'}

