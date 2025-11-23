"""
Script to prepare Lambda deployment package.

This creates a deployment ZIP file with all dependencies.
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path


def create_deployment_package():
    """Create Lambda deployment package."""
    print("Creating Lambda deployment package...")
    
    # Directories
    package_dir = Path("lambda_package")
    dist_dir = Path("dist")
    
    # Clean up previous builds
    if package_dir.exists():
        shutil.rmtree(package_dir)
    if not dist_dir.exists():
        dist_dir.mkdir()
    
    package_dir.mkdir()
    
    # Install dependencies
    print("\nInstalling dependencies...")
    subprocess.run([
        "pip", "install",
        "-r", "requirements-lambda.txt",
        "-t", str(package_dir)
    ], check=True)
    
    # Copy application code
    print("\nCopying application code...")
    shutil.copytree("app", package_dir / "app")
    shutil.copy("lambda_handler.py", package_dir / "lambda_handler.py")
    
    # Create ZIP file
    print("\nCreating deployment ZIP...")
    zip_path = dist_dir / "lambda_deployment.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    # Get ZIP size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print(f"\nDeployment package created: {zip_path}")
    print(f"Package size: {zip_size_mb:.2f} MB")
    
    if zip_size_mb > 50:
        print("\nWARNING: Package is larger than 50 MB.")
        print("Consider using Lambda Layers for large dependencies.")
    
    # Clean up
    shutil.rmtree(package_dir)
    
    print("\nDone! Upload dist/lambda_deployment.zip to AWS Lambda.")
    return zip_path


if __name__ == "__main__":
    create_deployment_package()

