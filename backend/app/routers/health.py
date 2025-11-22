"""
Health check endpoint.
"""

from datetime import datetime
from fastapi import APIRouter

from app.models.responses import HealthResponse
from app import __version__

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        HealthResponse: Current health status, timestamp, and version
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=__version__
    )

