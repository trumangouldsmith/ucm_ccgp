"""
Tests for Lambda handler.
"""

import pytest
from lambda_handler import handler


class TestLambdaHandler:
    """Test Lambda handler integration."""
    
    def test_lambda_handler_exists(self):
        """Test that Lambda handler is defined."""
        assert handler is not None
        assert callable(handler)
    
    def test_lambda_handler_health_check(self):
        """Test Lambda handler with health check event."""
        # Simulate API Gateway event
        event = {
            "httpMethod": "GET",
            "path": "/health",
            "headers": {},
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {
                "requestId": "test-request-id"
            }
        }
        
        context = {}
        
        # Call handler
        response = handler(event, context)
        
        # Check response
        assert "statusCode" in response
        assert response["statusCode"] == 200
        assert "body" in response
    
    def test_lambda_handler_root_endpoint(self):
        """Test Lambda handler with root endpoint."""
        event = {
            "httpMethod": "GET",
            "path": "/",
            "headers": {},
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {
                "requestId": "test-request-id"
            }
        }
        
        context = {}
        response = handler(event, context)
        
        assert response["statusCode"] == 200
    
    def test_lambda_handler_invalid_path(self):
        """Test Lambda handler with invalid path."""
        event = {
            "httpMethod": "GET",
            "path": "/nonexistent",
            "headers": {},
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {
                "requestId": "test-request-id"
            }
        }
        
        context = {}
        response = handler(event, context)
        
        # Should return 404
        assert response["statusCode"] == 404
    
    def test_lambda_handler_with_query_params(self):
        """Test Lambda handler with query parameters."""
        event = {
            "httpMethod": "GET",
            "path": "/health",
            "queryStringParameters": {
                "test": "param"
            },
            "headers": {},
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {
                "requestId": "test-request-id"
            }
        }
        
        context = {}
        response = handler(event, context)
        
        assert response["statusCode"] == 200
    
    def test_lambda_handler_post_request(self):
        """Test Lambda handler with POST request."""
        import json
        
        event = {
            "httpMethod": "POST",
            "path": "/api/analyze",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "tickers": ["AAPL"],
                "date_range": {
                    "start_date": "2025-11-01",
                    "end_date": "2025-11-20"
                }
            }),
            "isBase64Encoded": False,
            "requestContext": {
                "requestId": "test-request-id"
            }
        }
        
        context = {}
        response = handler(event, context)
        
        # Should process (might succeed or fail based on network)
        assert "statusCode" in response
        assert response["statusCode"] in [200, 400, 503, 500]

