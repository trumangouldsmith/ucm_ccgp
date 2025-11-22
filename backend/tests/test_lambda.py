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
        # Simulate proper API Gateway v2 event
        event = {
            "version": "2.0",
            "routeKey": "GET /health",
            "rawPath": "/health",
            "rawQueryString": "",
            "headers": {
                "accept": "*/*",
                "content-type": "application/json"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "test-api",
                "domainName": "test.execute-api.us-east-1.amazonaws.com",
                "http": {
                    "method": "GET",
                    "path": "/health",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "127.0.0.1"
                },
                "requestId": "test-request-id",
                "stage": "$default",
                "time": "01/Jan/2025:00:00:00 +0000",
                "timeEpoch": 1640995200000
            },
            "isBase64Encoded": False
        }
        
        context = type('obj', (object,), {
            'request_id': 'test-request-id',
            'function_name': 'test-function',
            'memory_limit_in_mb': '128'
        })()
        
        # Call handler
        response = handler(event, context)
        
        # Check response
        assert "statusCode" in response
        assert response["statusCode"] == 200
        assert "body" in response
    
    def test_lambda_handler_root_endpoint(self):
        """Test Lambda handler with root endpoint."""
        event = {
            "version": "2.0",
            "routeKey": "GET /",
            "rawPath": "/",
            "rawQueryString": "",
            "headers": {
                "accept": "*/*"
            },
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "127.0.0.1"
                },
                "requestId": "test-request-id"
            },
            "isBase64Encoded": False
        }
        
        context = type('obj', (object,), {'request_id': 'test-request-id'})()
        response = handler(event, context)
        
        assert response["statusCode"] == 200
    
    def test_lambda_handler_invalid_path(self):
        """Test Lambda handler with invalid path."""
        event = {
            "version": "2.0",
            "routeKey": "GET /nonexistent",
            "rawPath": "/nonexistent",
            "rawQueryString": "",
            "headers": {
                "accept": "*/*"
            },
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/nonexistent",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "127.0.0.1"
                },
                "requestId": "test-request-id"
            },
            "isBase64Encoded": False
        }
        
        context = type('obj', (object,), {'request_id': 'test-request-id'})()
        response = handler(event, context)
        
        # Should return 404
        assert response["statusCode"] == 404

