#!/bin/bash

# Deployment script for AWS Lambda
# Usage: ./deploy.sh

set -e

echo "=== Stock Performance Analyzer - Lambda Deployment ==="

# Configuration
FUNCTION_NAME="stock-performance-analyzer"
REGION="us-east-1"
ZIP_FILE="dist/lambda_deployment.zip"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed"
    exit 1
fi

# Navigate to backend directory
cd "$(dirname "$0")/../backend"

# Create deployment package
echo ""
echo "Creating deployment package..."
python deploy_lambda.py

# Check if ZIP file exists
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: Deployment package not found at $ZIP_FILE"
    exit 1
fi

# Deploy to Lambda
echo ""
echo "Deploying to AWS Lambda..."

# Check if function exists
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" &> /dev/null; then
    echo "Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file "fileb://$ZIP_FILE" \
        --region "$REGION"
else
    echo "Error: Lambda function '$FUNCTION_NAME' does not exist"
    echo "Create it first using AWS Console or:"
    echo "aws lambda create-function --function-name $FUNCTION_NAME ..."
    exit 1
fi

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Function Name: $FUNCTION_NAME"
echo "Region: $REGION"
echo ""
echo "Test the function:"
echo "  aws lambda invoke --function-name $FUNCTION_NAME --region $REGION output.json"

