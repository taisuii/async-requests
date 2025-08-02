"""
异步 HTTP 客户端 - 基于 httpx 实现
"""

import httpx
from typing import Dict, Any, Optional, Union

# 直接使用 httpx 的 Response，它已经兼容 requests 的接口
Response = httpx.Response

class AsyncClient:
    """异步 HTTP 客户端 - httpx.AsyncClient 的封装"""
    
    def __init__(self, 
                 timeout: Optional[float] = None,
                 headers: Optional[Dict[str, str]] = None,
                 cookies: Optional[Dict[str, str]] = None,
                 **kwargs):
        """
        初始化异步客户端
        
        Args:
            timeout: 请求超时时间（秒）
            headers: 默认请求头
            cookies: 默认 cookies
            **kwargs: 其他 httpx.AsyncClient 参数
        """
        self._client_kwargs = {
            'timeout': timeout,
            'headers': headers,
            'cookies': cookies,
            **kwargs
        }
        self._client = None
    
    async def __aenter__(self):
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def _ensure_client(self):
        """确保 httpx 客户端存在"""
        if self._client is None:
            self._client = httpx.AsyncClient(**self._client_kwargs)
    
    async def close(self):
        """关闭客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def request(self, 
                     method: str, 
                     url: str,
                     **kwargs) -> Response:
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法
            url: 请求 URL
            **kwargs: 其他请求参数，与 requests 兼容
            
        Returns:
            Response: HTTP 响应对象
        """
        await self._ensure_client()
        return await self._client.request(method, url, **kwargs)
    
    async def get(self, url: str, **kwargs) -> Response:
        """发送 GET 请求"""
        return await self.request('GET', url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> Response:
        """发送 POST 请求"""
        return await self.request('POST', url, **kwargs)
    
    async def put(self, url: str, **kwargs) -> Response:
        """发送 PUT 请求"""
        return await self.request('PUT', url, **kwargs)
    
    async def delete(self, url: str, **kwargs) -> Response:
        """发送 DELETE 请求"""
        return await self.request('DELETE', url, **kwargs)
    
    async def patch(self, url: str, **kwargs) -> Response:
        """发送 PATCH 请求"""
        return await self.request('PATCH', url, **kwargs)
    
    async def head(self, url: str, **kwargs) -> Response:
        """发送 HEAD 请求"""
        return await self.request('HEAD', url, **kwargs)
    
    async def options(self, url: str, **kwargs) -> Response:
        """发送 OPTIONS 请求"""
        return await self.request('OPTIONS', url, **kwargs)

# 全局默认客户端
_default_client = None

async def _get_default_client():
    """获取默认客户端"""
    global _default_client
    if _default_client is None:
        _default_client = AsyncClient()
    await _default_client._ensure_client()
    return _default_client

# 便捷函数 - 就像 requests，但需要 await
async def request(method: str, url: str, **kwargs) -> Response:
    """
    发送 HTTP 请求的便捷函数
    
    用法：
        response = await requests_async.request('GET', 'https://httpbin.org/get')
    """
    client = await _get_default_client()
    return await client.request(method, url, **kwargs)

async def get(url: str, **kwargs) -> Response:
    """
    发送 GET 请求的便捷函数
    
    用法：
        response = await requests_async.get('https://httpbin.org/get')
    """
    return await request('GET', url, **kwargs)

async def post(url: str, **kwargs) -> Response:
    """
    发送 POST 请求的便捷函数
    
    用法：
        response = await requests_async.post('https://httpbin.org/post', json={'key': 'value'})
    """
    return await request('POST', url, **kwargs)

async def put(url: str, **kwargs) -> Response:
    """
    发送 PUT 请求的便捷函数
    
    用法：
        response = await requests_async.put('https://httpbin.org/put', json={'key': 'value'})
    """
    return await request('PUT', url, **kwargs)

async def delete(url: str, **kwargs) -> Response:
    """
    发送 DELETE 请求的便捷函数
    
    用法：
        response = await requests_async.delete('https://httpbin.org/delete')
    """
    return await request('DELETE', url, **kwargs)

async def patch(url: str, **kwargs) -> Response:
    """
    发送 PATCH 请求的便捷函数
    
    用法：
        response = await requests_async.patch('https://httpbin.org/patch', json={'key': 'value'})
    """
    return await request('PATCH', url, **kwargs)

async def head(url: str, **kwargs) -> Response:
    """
    发送 HEAD 请求的便捷函数
    
    用法：
        response = await requests_async.head('https://httpbin.org/head')
    """
    return await request('HEAD', url, **kwargs)

async def options(url: str, **kwargs) -> Response:
    """
    发送 OPTIONS 请求的便捷函数
    
    用法：
        response = await requests_async.options('https://httpbin.org/options')
    """
    return await request('OPTIONS', url, **kwargs)
