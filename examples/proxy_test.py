#!/usr/bin/env python3
"""
Proxy testing script for requests-async
"""

import asyncio
import sys
import requests_async
from httpx import ProxyError, ConnectError


async def test_http_proxy():
    """Test HTTP proxy functionality"""
    print("🌐 Testing HTTP Proxy...")
    
    # HTTP proxy configuration
    http_proxy = "http://rtzg67668-region-US-sid-ZhJkqagB-t-5:vni2jars@us.arxlabs.io:3010"
    
    try:
        async with requests_async.AsyncSession(
            proxies={"http://": http_proxy, "https://": http_proxy},
            timeout=30.0
        ) as session:
            response = await session.get('http://mayips.com')
            print(f"  Status: {response.status_code}")
            data = response.json()
            print(f"  Country: {data.get('country', 'Unknown')}")
            print(f"  IP: {data.get('ip', 'Unknown')}")
            print("  ✅ HTTP proxy working!")
            return True
    except Exception as e:
        print(f"  ❌ HTTP proxy failed: {e}")
        return False


async def test_socks5_proxy():
    """Test SOCKS5 proxy functionality"""
    print("\n🔒 Testing SOCKS5 Proxy...")
    
    # SOCKS5 proxy configuration  
    socks5_proxy = "socks5://rtzg67668-region-US-sid-UeG4qQRa-t-5:vni2jars@us.arxlabs.io:3010"
    
    try:
        async with requests_async.AsyncSession(
            proxies={"http://": socks5_proxy, "https://": socks5_proxy},
            timeout=30.0
        ) as session:
            response = await session.get('http://mayips.com')
            print(f"  Status: {response.status_code}")
            data = response.json()
            print(f"  Country: {data.get('country', 'Unknown')}")
            print(f"  IP: {data.get('ip', 'Unknown')}")
            print("  ✅ SOCKS5 proxy working!")
            return True
    except Exception as e:
        print(f"  ❌ SOCKS5 proxy failed: {e}")
        return False


async def test_proxy_with_https():
    """Test proxy with HTTPS requests"""
    print("\n🔐 Testing HTTPS through proxy...")
    
    http_proxy = "http://rtzg67668-region-US-sid-ZhJkqagB-t-5:vni2jars@us.arxlabs.io:3010"
    
    try:
        async with requests_async.AsyncSession(
            proxies={"http://": http_proxy, "https://": http_proxy},
            timeout=30.0
        ) as session:
            response = await session.get('https://httpbin.org/ip')
            print(f"  Status: {response.status_code}")
            data = response.json()
            print(f"  IP: {data.get('origin', 'Unknown')}")
            print("  ✅ HTTPS through proxy working!")
            return True
    except Exception as e:
        print(f"  ❌ HTTPS through proxy failed: {e}")
        return False


async def test_no_proxy():
    """Test without proxy (for comparison)"""
    print("\n🌍 Testing without proxy (direct connection)...")
    
    try:
        response = await requests_async.get('http://mayips.com', timeout=10.0)
        print(f"  Status: {response.status_code}")
        data = response.json()
        print(f"  Country: {data.get('country', 'Unknown')}")
        print(f"  IP: {data.get('ip', 'Unknown')}")
        print("  ✅ Direct connection working!")
        return True
    except Exception as e:
        print(f"  ❌ Direct connection failed: {e}")
        return False


async def test_proxy_authentication():
    """Test proxy authentication with different methods"""
    print("\n🔑 Testing proxy authentication methods...")
    
    # Method 1: URL with credentials
    proxy_url = "http://rtzg67668-region-US-sid-ZhJkqagB-t-5:vni2jars@us.arxlabs.io:3010"
    
    try:
        async with requests_async.AsyncSession(
            proxies={"http://": proxy_url},
            timeout=15.0
        ) as session:
            response = await session.get('http://httpbin.org/ip')
            print(f"  Method 1 (URL auth) Status: {response.status_code}")
            print("  ✅ URL authentication working!")
            return True
    except Exception as e:
        print(f"  ❌ URL authentication failed: {e}")
        return False


async def main():
    """Run all proxy tests"""
    print("🧪 requests-async Proxy Test Suite")
    print("=" * 50)
    
    tests = [
        ("No Proxy (Direct)", test_no_proxy),
        ("HTTP Proxy", test_http_proxy),
        ("SOCKS5 Proxy", test_socks5_proxy),
        ("HTTPS through Proxy", test_proxy_with_https),
        ("Proxy Authentication", test_proxy_authentication),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Proxy Test Results:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All proxy tests passed!")
    else:
        print("💔 Some proxy tests failed.")
    
    return passed == len(results)


if __name__ == '__main__':
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)