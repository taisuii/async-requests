"""
Setup script for requests-async
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="requests-async",
    version="0.1.0", 
    author="Your Name",
    author_email="your.email@example.com",
    description="Async HTTP requests with a requests-like interface, powered by httpx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/requests-async",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "httpx>=0.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
    keywords="http async requests client httpx",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/requests-async/issues",
        "Source": "https://github.com/yourusername/requests-async",
        "Documentation": "https://github.com/yourusername/requests-async#readme",
    },
)
