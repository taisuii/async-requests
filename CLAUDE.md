# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
requests-async is a simple, elegant async HTTP client library built on httpx. It provides a requests-compatible API where you just add `await` to make HTTP requests asynchronous.

## Architecture
- **Core module**: `requests_async/client.py` - Contains `AsyncSession` class and convenience functions (140 lines)
- **Package init**: `requests_async/__init__.py` - Public API exports (30 lines)
- **Total codebase**: ~170 lines (down from 1266 lines)

### Key Design Principles
- **Simplicity**: Minimal, focused codebase
- **Compatibility**: Drop-in async replacement for requests
- **Performance**: Built on httpx for speed
- **Ease of use**: Just add `await` to requests calls

## Development Commands

### Testing
- **Run tests**: `pytest`
- **With coverage**: `pytest --cov=requests_async`
- **API test suite**: `python examples/api_test.py`
- **Usage examples**: `python examples/usage_examples.py`

### Building and Publishing
- **Install for development**: `pip install -e .[dev]`
- **Build package**: `python -m build`
- **Upload to PyPI**: `python -m twine upload dist/*`

### Dependencies
- **Runtime**: httpx>=0.23.0
- **Development**: pytest>=7.0.0, pytest-asyncio>=0.21.0, pytest-cov>=4.0.0

## API Design
- `AsyncSession`: Context manager for reusable HTTP client
- Global functions: `get()`, `post()`, etc. for one-off requests
- Response objects: Direct httpx.Response (requests-compatible)
- Error handling: httpx exceptions (HTTPError, TimeoutException, etc.)

## Usage Patterns
- **Simple requests**: `await requests_async.get(url)`
- **Sessions**: `async with requests_async.AsyncSession() as session:`
- **All HTTP methods**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Full requests compatibility**: headers, params, json, data, files, etc.