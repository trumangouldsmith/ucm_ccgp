"""
S3 caching service for stock data and analytics results.
"""

import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class CacheService:
    """Service for caching stock data and analytics in S3."""
    
    def __init__(
        self,
        bucket_name: str,
        ttl_hours: int = 24,
        region_name: str = "us-east-1"
    ):
        """
        Initialize cache service.
        
        Args:
            bucket_name: S3 bucket name for cache storage
            ttl_hours: Cache time-to-live in hours (default 24)
            region_name: AWS region
        """
        self.bucket_name = bucket_name
        self.ttl_hours = ttl_hours
        self.s3_client = boto3.client('s3', region_name=region_name)
    
    @staticmethod
    def generate_cache_key(
        tickers: list,
        start_date: str,
        end_date: str,
        interval: str
    ) -> str:
        """
        Generate unique cache key based on request parameters.
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date string
            end_date: End date string
            interval: Data interval
            
        Returns:
            Cache key (hash of parameters)
        """
        # Sort tickers for consistent key generation
        sorted_tickers = sorted(tickers)
        
        # Create string representation
        key_string = f"{'-'.join(sorted_tickers)}_{start_date}_{end_date}_{interval}"
        
        # Generate hash
        hash_object = hashlib.md5(key_string.encode())
        cache_key = hash_object.hexdigest()
        
        return f"cache/{cache_key}.json"
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from cache.
        
        Args:
            cache_key: Cache key to retrieve
            
        Returns:
            Cached data if exists and not expired, None otherwise
        """
        try:
            # Get object from S3
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=cache_key
            )
            
            # Read and parse JSON
            cache_data = json.loads(response['Body'].read().decode('utf-8'))
            
            # Check if expired
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            expiry_time = cached_time + timedelta(hours=self.ttl_hours)
            
            if datetime.utcnow() > expiry_time:
                logger.info(f"Cache expired for key: {cache_key}")
                # Optionally delete expired cache
                self.delete(cache_key)
                return None
            
            logger.info(f"Cache hit for key: {cache_key}")
            return cache_data['data']
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                logger.info(f"Cache miss for key: {cache_key}")
            else:
                logger.error(f"S3 error retrieving cache: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set(self, cache_key: str, data: Dict[str, Any]) -> bool:
        """
        Store data in cache.
        
        Args:
            cache_key: Cache key to store under
            data: Data to cache
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Wrap data with metadata
            cache_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }
            
            # Convert to JSON
            json_data = json.dumps(cache_data)
            
            # Store in S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=cache_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json'
            )
            
            logger.info(f"Cached data for key: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing in cache: {str(e)}")
            return False
    
    def delete(self, cache_key: str) -> bool:
        """
        Delete data from cache.
        
        Args:
            cache_key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=cache_key
            )
            logger.info(f"Deleted cache key: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting from cache: {str(e)}")
            return False
    
    def clear_all(self, prefix: str = "cache/") -> int:
        """
        Clear all cached items with given prefix.
        
        Args:
            prefix: S3 key prefix to delete (default "cache/")
            
        Returns:
            Number of items deleted
        """
        try:
            # List objects with prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                return 0
            
            # Delete all objects
            objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            
            if objects_to_delete:
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={'Objects': objects_to_delete}
                )
            
            count = len(objects_to_delete)
            logger.info(f"Cleared {count} cache entries")
            return count
            
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats (count, total size, etc.)
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix="cache/"
            )
            
            if 'Contents' not in response:
                return {
                    'count': 0,
                    'total_size_bytes': 0,
                    'total_size_mb': 0.0
                }
            
            total_size = sum(obj['Size'] for obj in response['Contents'])
            count = len(response['Contents'])
            
            return {
                'count': count,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {
                'count': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0.0
            }

