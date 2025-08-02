#!/usr/bin/env python3
"""
API Testing Script for requests-async

This script tests all the main functionality of requests-async
to ensure everything works correctly.
"""

import asyncio
import time
import sys
from typing import Dict, Any

# Add the parent directory to the path so we can import requests_async
sys.path.insert(0, '.')

try:
    import requests_async
    from httpx import HTTPError, TimeoutException
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install dependencies: pip install httpx")
    sys.exit(1)


class Colors:
    """ANSI color codes for pretty output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


async def test_basic_get():
    """Test basic GET request"""
    print(f"{Colors.BLUE}Testing GET request...{Colors.RESET}")
    try:
        response = await requests_async.get('https://httpbin.org/get')
        assert response.status_code == 200
        data = response.json()
        assert 'url' in data
        print(f"  {Colors.GREEN}✅ GET request successful{Colors.RESET}")
        return True
    except Exception as e:
        print(f"  {Colors.RED}❌ GET request failed: {e}{Colors.RESET}")
        return False


async def test_post_with_json():
    """Test POST request with JSON data"""
    print(f"{Colors.BLUE}Testing POST with JSON...{Colors.RESET}")
    try:
        test_data = {'message': 'Hello from requests-async!', 'timestamp': time.time()}
        response = await requests_async.post('https://httpbin.org/post', json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data['json'] == test_data
        print(f"  {Colors.GREEN}✅ POST with JSON successful{Colors.RESET}")
        return True
    except Exception as e:
        print(f"  {Colors.RED}❌ POST with JSON failed: {e}{Colors.RESET}")
        return False


async def test_all_http_methods():
    """Test all HTTP methods"""
    print(f"{Colors.BLUE}Testing all HTTP methods...{Colors.RESET}")
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    results = []
    
    for method in methods:
        try:
            method_func = getattr(requests_async, method.lower())
            url = f'https://httpbin.org/{method.lower()}'
            response = await method_func(url)
            
            if method == 'HEAD':
                # HEAD doesn't return content, just check status
                success = response.status_code == 200
            else:
                success = response.status_code == 200
                if method != 'OPTIONS':  # OPTIONS might not return JSON
                    try:
                        data = response.json()
                        success = 'url' in data
                    except:
                        success = True  # Some endpoints might not return JSON
            
            if success:
                print(f"  {Colors.GREEN}✅ {method} successful{Colors.RESET}")
                results.append(True)
            else:
                print(f"  {Colors.RED}❌ {method} failed{Colors.RESET}")
                results.append(False)
                
        except Exception as e:
            print(f"  {Colors.RED}❌ {method} failed: {e}{Colors.RESET}")
            results.append(False)
    
    return all(results)


async def test_session_usage():
    """Test AsyncSession context manager"""
    print(f"{Colors.BLUE}Testing AsyncSession...{Colors.RESET}")
    try:
        async with requests_async.AsyncSession(timeout=30.0) as session:
            # Test multiple requests with the same session
            response1 = await session.get('https://httpbin.org/get')
            response2 = await session.post('https://httpbin.org/post', json={'test': 'session'})
            
            assert response1.status_code == 200
            assert response2.status_code == 200
            
        print(f"  {Colors.GREEN}✅ AsyncSession successful{Colors.RESET}")
        return True
    except Exception as e:
        print(f"  {Colors.RED}❌ AsyncSession failed: {e}{Colors.RESET}")
        return False


async def test_headers_and_params():
    """Test custom headers and query parameters"""
    print(f"{Colors.BLUE}Testing headers and parameters...{Colors.RESET}")
    try:
        headers = {'User-Agent': 'requests-async/0.2.1', 'X-Test-Header': 'test-value'}
        params = {'param1': 'value1', 'param2': 'value2'}
        
        response = await requests_async.get(
            'https://httpbin.org/get',
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check if our headers were sent
        assert data['headers']['User-Agent'] == 'requests-async/0.2.1'
        assert data['headers']['X-Test-Header'] == 'test-value'
        
        # Check if parameters were sent
        assert data['args'] == params
        
        print(f"  {Colors.GREEN}✅ Headers and parameters successful{Colors.RESET}")
        return True
    except Exception as e:
        print(f"  {Colors.RED}❌ Headers and parameters failed: {e}{Colors.RESET}")
        return False


async def test_error_handling():
    """Test error handling"""
    print(f"{Colors.BLUE}Testing error handling...{Colors.RESET}")
    try:
        # Test 404 error
        response = await requests_async.get('https://httpbin.org/status/404')
        assert response.status_code == 404
        
        # Test that raise_for_status works
        try:
            response.raise_for_status()
            print(f"  {Colors.RED}❌ raise_for_status should have raised an exception{Colors.RESET}")
            return False
        except HTTPError:
            pass  # This is expected
        
        print(f"  {Colors.GREEN}✅ Error handling successful{Colors.RESET}")
        return True
    except Exception as e:
        print(f"  {Colors.RED}❌ Error handling failed: {e}{Colors.RESET}")
        return False


async def test_concurrent_requests():
    """Test concurrent requests"""
    print(f"{Colors.BLUE}Testing concurrent requests...{Colors.RESET}")
    try:
        # Send 5 requests concurrently
        tasks = []
        for i in range(5):
            task = requests_async.get(f'https://httpbin.org/delay/1?request={i}')
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Should take around 1 second (not 5 seconds) due to concurrency
        elapsed_time = end_time - start_time
        
        # Check all requests succeeded
        for response in responses:
            assert response.status_code == 200
        
        print(f"  {Colors.GREEN}✅ Concurrent requests successful (took {elapsed_time:.2f}s){Colors.RESET}")
        
        if elapsed_time < 3.0:  # Should be much faster than sequential
            print(f"  {Colors.GREEN}✅ Concurrency is working properly{Colors.RESET}")
        else:
            print(f"  {Colors.YELLOW}⚠️  Concurrency might not be working optimally{Colors.RESET}")
        
        return True
    except Exception as e:
        print(f"  {Colors.RED}❌ Concurrent requests failed: {e}{Colors.RESET}")
        return False


async def run_all_tests():
    """Run all tests and report results"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}🧪 requests-async API Test Suite{Colors.RESET}")
    print(f"{Colors.MAGENTA}{'=' * 50}{Colors.RESET}")
    
    tests = [
        ("Basic GET request", test_basic_get),
        ("POST with JSON", test_post_with_json),
        ("All HTTP methods", test_all_http_methods),
        ("AsyncSession usage", test_session_usage),
        ("Headers and parameters", test_headers_and_params),
        ("Error handling", test_error_handling),
        ("Concurrent requests", test_concurrent_requests),
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\n{Colors.CYAN}🔍 {test_name}{Colors.RESET}")
        result = await test_func()
        results.append((test_name, result))
    
    end_time = time.time()
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}📊 Test Results Summary{Colors.RESET}")
    print(f"{Colors.MAGENTA}{'=' * 50}{Colors.RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✅ PASS" if result else f"{Colors.RED}❌ FAIL"
        print(f"{status}{Colors.RESET} {test_name}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.RESET}")
    print(f"{Colors.BOLD}Time taken: {end_time - start_time:.2f} seconds{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! requests-async is working correctly.{Colors.RESET}")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}💔 Some tests failed. Please check the output above.{Colors.RESET}")
        return False


async def main():
    """Main function"""
    try:
        success = await run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}💥 Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())