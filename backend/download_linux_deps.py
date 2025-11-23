"""
Download Linux-compatible wheels for Lambda deployment.
Run this before deploy_lambda.py on Windows machines.
"""

import subprocess
import sys
from pathlib import Path

def download_linux_wheels():
    """Download Linux wheels for problematic binary packages."""
    
    download_dir = Path("lambda_deps_linux")
    download_dir.mkdir(exist_ok=True)
    
    print("Downloading Linux-compatible wheels for Lambda...")
    print(f"Download directory: {download_dir}\n")
    
    # Download only the packages with binary extensions
    binary_packages = [
        "pydantic-core==2.14.1",
        "pandas==2.1.3",
        "numpy==1.26.2",
        "lxml",
    ]
    
    for package in binary_packages:
        print(f"Downloading {package}...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "download",
                package,
                "--platform", "manylinux2014_x86_64",
                "--only-binary=:all:",
                "--python-version", "311",
                "--implementation", "cp",
                "--abi", "cp311",
                "--dest", str(download_dir)
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"  Warning: Could not download {package}")
            print(f"  {e.stderr.decode() if e.stderr else ''}")
    
    print(f"\nDone! Extract .whl files to lambda_package/ before zipping.")
    print(f"Wheels are in: {download_dir}")

if __name__ == "__main__":
    download_linux_wheels()

