"""
Tests for health check endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint returns expected response."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_root_endpoint():
    """Test the root endpoint returns API information."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Stock Performance Comparison API"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"


def test_analytics_test_endpoint():
    """Test the analytics test endpoint."""
    response = client.get("/api/test")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Analytics router is working!"
    assert "/api/analyze" in data["endpoints"]

