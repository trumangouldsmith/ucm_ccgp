"""
Configuration settings for the application.
"""

import os
from typing import Optional


class Settings:
    """Application settings."""
    
    # S3 Cache Configuration
    CACHE_BUCKET_NAME: str = os.getenv("CACHE_BUCKET_NAME", "stock-analytics-cache")
    CACHE_TTL_HOURS: int = int(os.getenv("CACHE_TTL_HOURS", "24"))
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # Enable/disable caching
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    # For local development without S3
    USE_LOCAL_CACHE: bool = os.getenv("USE_LOCAL_CACHE", "false").lower() == "true"


settings = Settings()

