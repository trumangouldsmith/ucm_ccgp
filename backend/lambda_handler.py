"""
AWS Lambda handler for FastAPI application.

This module wraps the FastAPI app using Mangum for serverless deployment.
"""

from mangum import Mangum
from app.main import app

# Create Lambda handler
handler = Mangum(app, lifespan="off")

