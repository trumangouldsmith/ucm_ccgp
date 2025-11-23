"""
Upload Lambda deployment package to S3 and update function.
Use this when ZIP > 50 MB.
"""

import boto3
import sys
from pathlib import Path

def upload_and_deploy():
    """Upload ZIP to S3 and update Lambda function."""
    
    # Configuration
    BUCKET_NAME = "stock-analyzer-cache-656312098098"  # Reuse cache bucket
    ZIP_FILE = "dist/lambda_deployment.zip"
    S3_KEY = "lambda/lambda_deployment.zip"
    FUNCTION_NAME = "stock-performance-analyzer"
    REGION = "us-east-1"
    
    zip_path = Path(ZIP_FILE)
    
    if not zip_path.exists():
        print(f"ERROR: {ZIP_FILE} not found. Run deploy_lambda.py first.")
        return
    
    # Get file size
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Package size: {size_mb:.2f} MB")
    
    # Upload to S3
    print(f"\nUploading to S3: s3://{BUCKET_NAME}/{S3_KEY}")
    s3 = boto3.client('s3', region_name=REGION)
    
    try:
        s3.upload_file(str(zip_path), BUCKET_NAME, S3_KEY)
        print("Upload complete!")
    except Exception as e:
        print(f"ERROR uploading to S3: {e}")
        return
    
    # Update Lambda function
    print(f"\nUpdating Lambda function: {FUNCTION_NAME}")
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    try:
        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            S3Bucket=BUCKET_NAME,
            S3Key=S3_KEY
        )
        print("Lambda function updated!")
        print(f"Function ARN: {response['FunctionArn']}")
        print(f"Code Size: {response['CodeSize'] / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"ERROR updating Lambda: {e}")
        return
    
    print("\n=== Deployment Complete ===")

if __name__ == "__main__":
    upload_and_deploy()

