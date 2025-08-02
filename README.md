# Async Requests

An asynchronous HTTP request library based on httpx.

## Installation

```bash
pip install async-requests
```

## Usage

```python
from async_requests import AsyncRequests

async def main():
    async with AsyncRequests() as client:
        response = await client.get("https://example.com")
        print(response.text)

# Run the async function
import asyncio
asyncio.run(main())
```

## Features
- Asynchronous HTTP requests
- Automatic retries with backoff
- Support for proxies and cookies

## License
This project is licensed under the MIT License. See the LICENSE file for details.
