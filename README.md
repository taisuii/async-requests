# requests-async

[![PyPI version](https://badge.fury.io/py/requests-async.svg)](https://badge.fury.io/py/requests-async)
[![Python versions](https://img.shields.io/pypi/pyversions/requests-async.svg)](https://pypi.org/project/requests-async/)
[![License](https://img.shields.io/pypi/l/requests-async.svg)](https://pypi.org/project/requests-async/)

A simple, elegant async HTTP client for Python, built on top of [httpx](https://www.python-httpx.org/). Get the power of async HTTP requests with a familiar requests-like interface - just add `await`!

## Why requests-async?

- 🚀 **Blazing Fast**: Built on httpx for maximum performance
- 🔄 **Drop-in Replacement**: Same API as requests, just add `await`
- 📦 **Simple**: Minimal learning curve if you know requests
- 🛡️ **Reliable**: Built on battle-tested httpx foundation
- 🎯 **Focused**: Does one thing exceptionally well

## Installation

```bash
pip install requests-async
```

## Quick Start

### Basic Usage

```python
import asyncio
import requests_async

async def main():
    # Simple GET request
    response = await requests_async.get('https://httpbin.org/get')
    print(response.json())
    
    # POST with JSON data
    response = await requests_async.post(
        'https://httpbin.org/post',
        json={'key': 'value'}
    )
    print(response.status_code)

asyncio.run(main())
```

### Using Proxies

requests-async supports both HTTP and SOCKS5 proxies:

```python
import asyncio
import requests_async

async def main():
    # HTTP proxy
    http_proxy = "http://user:pass@proxy:port"
    async with requests_async.AsyncSession(proxies=http_proxy) as session:
        response = await session.get('https://httpbin.org/ip')
        print(response.json())
    
    # SOCKS5 proxy
    socks5_proxy = "socks5://user:pass@proxy:port"
    async with requests_async.AsyncSession(proxies=socks5_proxy) as session:
        response = await session.get('https://httpbin.org/ip')
        print(response.json())
    
    # Different proxies for different protocols
    proxies = {
        "http://": "http://proxy:port",
        "https://": "https://proxy:port"
    }
    async with requests_async.AsyncSession(proxies=proxies) as session:
        response = await session.get('https://httpbin.org/ip')
        print(response.json())

asyncio.run(main())
```

## API Reference

### Convenience Functions

All functions return an `httpx.Response` object with the same interface as requests.

```python
# All HTTP methods supported
response = await requests_async.get(url, **kwargs)
response = await requests_async.post(url, **kwargs)
response = await requests_async.put(url, **kwargs)
response = await requests_async.delete(url, **kwargs)
response = await requests_async.patch(url, **kwargs)
response = await requests_async.head(url, **kwargs)
response = await requests_async.options(url, **kwargs)
response = await requests_async.request(method, url, **kwargs)
```

### AsyncSession Class

For better performance with multiple requests:

```python
async with requests_async.AsyncSession(timeout=30.0, headers=headers) as session:
    response = await session.get(url)
```

**AsyncSession Parameters:**
- `timeout`: Request timeout in seconds (default: 30.0)
- `headers`: Default headers for all requests
- `proxies`: Proxy configuration (string or dict)
  - String: `"http://proxy:port"` or `"socks5://proxy:port"`
  - Dict: `{"http://": "http://proxy:port", "https://": "https://proxy:port"}`
- `**kwargs`: Any additional httpx.AsyncClient parameters

### Response Object

The response object is an `httpx.Response` with all the familiar methods:

```python
response.status_code        # HTTP status code
response.headers           # Response headers
response.text             # Response text
response.content          # Response bytes
response.json()           # Parse JSON response
response.raise_for_status()  # Raise exception for 4xx/5xx status codes
```

## Examples

### Different Data Types

```python
# JSON data
await requests_async.post(url, json={'key': 'value'})

# Form data
await requests_async.post(url, data={'key': 'value'})

# Files
with open('file.txt', 'rb') as f:
    await requests_async.post(url, files={'file': f})

# Custom headers
await requests_async.get(url, headers={'Authorization': 'Bearer token'})

# Query parameters
await requests_async.get(url, params={'q': 'search', 'limit': 10})
```

### Error Handling

```python
import requests_async
from httpx import HTTPError, TimeoutException

try:
    response = await requests_async.get('https://httpbin.org/status/404')
    response.raise_for_status()  # Raises exception for 4xx/5xx
except HTTPError as e:
    print(f"HTTP error: {e}")
except TimeoutException:
    print("Request timed out")
```

### Advanced Usage

```python
# Custom timeout and headers
async with requests_async.AsyncSession(
    timeout=60.0,
    headers={'User-Agent': 'MyBot/1.0'}
) as session:
    
    # These headers will be used for all requests
    response = await session.get('https://api.example.com/data')
    
    # Override timeout for specific request
    response = await session.post(
        'https://api.example.com/upload',
        json=large_data,
        timeout=120.0
    )
```

## Comparison with requests

| Feature | requests | requests-async |
|---------|----------|----------------|
| Sync/Async | Synchronous | Asynchronous |
| Performance | Good | Excellent |
| API | `requests.get()` | `await requests_async.get()` |
| Sessions | `requests.Session()` | `async with requests_async.AsyncSession()` |
| Error Handling | requests exceptions | httpx exceptions |

## Migration from requests

Simply replace `requests` with `requests_async` and add `await`:

```python
# Before (requests)
response = requests.get('https://api.example.com')

# After (requests-async)  
response = await requests_async.get('https://api.example.com')
```

For sessions:

```python
# Before (requests)
with requests.Session() as session:
    response = session.get('https://api.example.com')

# After (requests-async)
async with requests_async.AsyncSession() as session:
    response = await session.get('https://api.example.com')
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pip install pytest-cov
pytest --cov=requests_async
```

### API Testing Script

```bash
# Test all endpoints
python examples/api_test.py
```

## Requirements

- Python 3.7+
- httpx >= 0.23.0

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### 0.2.1
- Complete rewrite for simplicity and performance
- Cleaner API design
- Better documentation
- Simplified codebase

### 0.1.0
- Initial release