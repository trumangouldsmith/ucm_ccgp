"""
Simple Lambda deployment package builder.
Works on Windows by using pure-Python packages and Lambda Layer for pandas/numpy.
"""

import shutil
import subprocess
import zipfile
from pathlib import Path

def build():
    print("=== Building Lambda Package (Simple Method) ===\n")
    
    package_dir = Path("lambda_package")
    dist_dir = Path("dist")
    
    # Clean
    if package_dir.exists():
        shutil.rmtree(package_dir)
    dist_dir.mkdir(exist_ok=True)
    package_dir.mkdir()
    
    # Install pure-Python dependencies
    print("Installing dependencies...")
    subprocess.run([
        "pip", "install",
        "fastapi==0.95.0",
        "mangum==0.17.0",
        "pydantic==1.10.12",
        "starlette==0.26.1",
        "-t", str(package_dir),
        "--no-deps"
    ], check=True)
    
    # Install yfinance with its dependencies
    print("\nInstalling yfinance...")
    subprocess.run([
        "pip", "install",
        "yfinance==0.2.32",
        "requests",
        "lxml",
        "multitasking",
        "appdirs",
        "frozendict",
        "peewee",
        "html5lib",
        "beautifulsoup4",
        "-t", str(package_dir),
        "--no-deps"
    ], check=True)
    
    # Copy additional needed packages
    print("\nCopying additional dependencies...")
    extras = [
        "anyio", "sniffio", "idna", "certifi", "urllib3", 
        "charset_normalizer", "python_dateutil", "pytz", 
        "tzdata", "six", "typing_extensions", "webencodings", "soupsieve"
    ]
    
    for pkg in extras:
        try:
            subprocess.run(["pip", "install", pkg, "-t", str(package_dir), "--no-deps"], 
                         check=True, capture_output=True)
        except:
            pass
    
    # Copy app code
    print("\nCopying application code...")
    shutil.copytree("app", package_dir / "app")
    shutil.copy("lambda_handler.py", package_dir / "lambda_handler.py")
    
    # Create ZIP
    print("\nCreating ZIP file...")
    zip_path = dist_dir / "lambda_deployment.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in package_dir.rglob('*'):
            if root.is_file():
                arcname = root.relative_to(package_dir)
                zipf.write(root, arcname)
    
    # Cleanup
    shutil.rmtree(package_dir)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n=== Done! ===")
    print(f"Package: {zip_path}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"\nNext steps:")
    print(f"1. Upload to S3: stock-analyzer-cache-656312098098")
    print(f"2. Update Lambda from S3")
    print(f"3. Add Layer: arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:13")

if __name__ == "__main__":
    build()

