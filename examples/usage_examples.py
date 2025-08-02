#!/usr/bin/env python3
"""
Simple usage examples for requests-async
"""

import asyncio
import requests_async


async def basic_examples():
    """Basic usage examples"""
    print("🚀 Basic Examples")
    print("=" * 50)
    
    # Simple GET request
    print("\n1. Simple GET request:")
    response = await requests_async.get('https://httpbin.org/get')
    print(f"Status: {response.status_code}")
    print(f"URL: {response.json()['url']}")
    
    # POST with JSON
    print("\n2. POST with JSON:")
    data = {'name': 'requests-async', 'version': '0.2.0'}
    response = await requests_async.post('https://httpbin.org/post', json=data)
    print(f"Status: {response.status_code}")
    print(f"Sent data: {response.json()['json']}")
    
    # Custom headers
    print("\n3. Custom headers:")
    headers = {'User-Agent': 'MyApp/1.0', 'Authorization': 'Bearer token123'}
    response = await requests_async.get('https://httpbin.org/headers', headers=headers)
    print(f"Headers sent: {response.json()['headers']['User-Agent']}")


async def session_examples():
    """Session usage examples"""
    print("\n🔄 Session Examples")
    print("=" * 50)
    
    # Using session for multiple requests
    async with requests_async.AsyncSession(timeout=30.0) as session:
        print("\n1. Multiple requests with session:")
        
        # First request
        response1 = await session.get('https://httpbin.org/get')
        print(f"Request 1 status: {response1.status_code}")
        
        # Second request with the same session
        response2 = await session.post('https://httpbin.org/post', json={'session': 'test'})
        print(f"Request 2 status: {response2.status_code}")


async def advanced_examples():
    """Advanced usage examples"""
    print("\n⚡ Advanced Examples")
    print("=" * 50)
    
    # Concurrent requests
    print("\n1. Concurrent requests:")
    import time
    
    start_time = time.time()
    tasks = [
        requests_async.get(f'https://httpbin.org/delay/1?id={i}')
        for i in range(3)
    ]
    responses = await asyncio.gather(*tasks)
    end_time = time.time()
    
    print(f"Made {len(responses)} requests in {end_time - start_time:.2f} seconds")
    for i, response in enumerate(responses):
        print(f"Response {i+1}: {response.status_code}")
    
    # Error handling
    print("\n2. Error handling:")
    try:
        response = await requests_async.get('https://httpbin.org/status/404')
        print(f"Status: {response.status_code}")
        response.raise_for_status()  # This will raise an exception
    except Exception as e:
        print(f"Caught expected error: {type(e).__name__}")


async def main():
    """Run all examples"""
    await basic_examples()
    await session_examples() 
    await advanced_examples()
    
    print("\n✅ All examples completed successfully!")


if __name__ == '__main__':
    asyncio.run(main())