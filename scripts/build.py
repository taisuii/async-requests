#!/usr/bin/env python3
"""
Build and publish script for requests-async
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ {description} failed:")
        print(result.stderr)
        return False
    else:
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(result.stdout)
        return True


def main():
    """Main build and publish process"""
    print("📦 requests-async Build & Publish Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('pyproject.toml'):
        print("❌ Error: pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    if os.path.exists('dist'):
        run_command('rm -rf dist', 'Removing dist directory')
    if os.path.exists('build'):
        run_command('rm -rf build', 'Removing build directory')
    
    # Install build dependencies
    if not run_command('pip install build twine', 'Installing build dependencies'):
        sys.exit(1)
    
    # Run tests first
    print("\n🧪 Running tests...")
    if not run_command('pytest tests/ -v', 'Running test suite'):
        print("⚠️  Tests failed. Continue anyway? (y/N)")
        if input().lower() != 'y':
            sys.exit(1)
    
    # Build the package
    if not run_command('python -m build', 'Building package'):
        sys.exit(1)
    
    # Check the built package
    if not run_command('python -m twine check dist/*', 'Checking package'):
        sys.exit(1)
    
    print("\n📋 Package built successfully!")
    print("Files created:")
    if os.path.exists('dist'):
        for file in os.listdir('dist'):
            print(f"  - dist/{file}")
    
    print("\n🚀 Ready to publish!")
    print("\nTo publish to PyPI:")
    print("  1. Test upload: python -m twine upload --repository testpypi dist/*")
    print("  2. Real upload: python -m twine upload dist/*")
    print("\nTo publish to test PyPI first:")
    print("  pip install --index-url https://test.pypi.org/simple/ requests-async")
    
    print("\n📖 Don't forget to:")
    print("  - Update version in pyproject.toml")
    print("  - Create a git tag: git tag v0.2.0")
    print("  - Push the tag: git push origin v0.2.0")


if __name__ == '__main__':
    main()