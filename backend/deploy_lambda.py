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
    venv_site_packages = Path("venv/Lib/site-packages")
    
    # Clean up previous builds
    if package_dir.exists():
        shutil.rmtree(package_dir)
    if not dist_dir.exists():
        dist_dir.mkdir()
    
    package_dir.mkdir()
    
    # Download Linux wheels for binary packages
    print("\nDownloading Linux-compatible wheels for binary packages...")
    binary_packages = [
        "pydantic-core==2.14.1",
        "pandas==2.1.3", 
        "numpy==1.26.2",
    ]
    
    temp_download = Path("temp_linux_wheels")
    temp_download.mkdir(exist_ok=True)
    
    for pkg in binary_packages:
        print(f"  Downloading {pkg}...")
        try:
            subprocess.run([
                "pip", "download", pkg,
                "--platform", "manylinux2014_x86_64",
                "--only-binary=:all:",
                "--python-version", "3.11",
                "--dest", str(temp_download),
                "--no-deps"
            ], check=True, capture_output=True)
        except:
            print(f"    Warning: Could not download {pkg}, will try from venv")
    
    # Extract downloaded wheels
    print("\nExtracting Linux wheels...")
    for whl_file in temp_download.glob("*.whl"):
        print(f"  Extracting {whl_file.name}...")
        import zipfile
        with zipfile.ZipFile(whl_file, 'r') as zip_ref:
            zip_ref.extractall(package_dir)
    
    # Copy pure-Python packages from venv
    print("\nCopying pure-Python packages from venv...")
    skip_packages = {'pip', 'setuptools', 'wheel', 'pytest', 'httpx', '_distutils_hack', 
                    'pkg_resources', 'pandas', 'numpy', 'pydantic_core', 'pydantic-core'}
    
    if venv_site_packages.exists():
        for item in venv_site_packages.iterdir():
            if item.name in skip_packages or item.name.startswith('~'):
                continue
            if item.name.startswith('pandas') or item.name.startswith('numpy') or 'pydantic_core' in item.name:
                continue
                
            try:
                if item.is_dir() and not item.name.endswith('.dist-info'):
                    print(f"  {item.name}")
                    shutil.copytree(item, package_dir / item.name, 
                                  ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
                elif item.suffix == '.py':
                    shutil.copy2(item, package_dir / item.name)
            except:
                pass
    
    # Cleanup
    shutil.rmtree(temp_download, ignore_errors=True)
    
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

