"""
Main FastAPI application for Stock Performance Comparison Tool.

This module initializes the FastAPI app and sets up core routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, analytics

# Initialize FastAPI app
app = FastAPI(
    title="Stock Performance Comparison API",
    description="Backend API for comparing stock performance across multiple tickers and time ranges",
    version="1.0.0",
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be restricted to CloudFront domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Stock Performance Comparison API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }

