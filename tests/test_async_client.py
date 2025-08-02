"""
AsyncClient 测试
"""

import pytest
import asyncio
import requests_async as requests

class TestAsyncClient:
    """AsyncClient 测试类"""
    
    @pytest.mark.asyncio
    async def test_basic_client_usage(self, test_urls):
        """测试基本客户端使用"""
        async with requests.AsyncClient() as client:
            response = await client.get(test_urls['get'])
            assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_client_with_default_headers(self, test_urls):
        """测试带默认请求头的客户端"""
        default_headers = {
            'User-Agent': 'requests-async-client/1.0',
            'X-Client-Version': '0.1.0'
        }
        
        async with requests.AsyncClient(headers=default_headers) as client:
            response = await client.get(test_urls['headers'])
            
            assert response.status_code == 200
            data = response.json()
            
            for key, value in default_headers.items():
                assert data['headers'][key] == value
    
    @pytest.mark.asyncio
    async def test_client_with_timeout(self, test_urls):
        """测试带超时设置的客户端"""
        async with requests.AsyncClient(timeout=5.0) as client:
            response = await client.get(test_urls['delay'])
            assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_client_connection_reuse(self, test_urls):
        """测试连接复用"""
        async with requests.AsyncClient() as client:
            # 发送多个请求到同一域名，应该复用连接
            responses = []
            for _ in range(3):
                response = await client.get(test_urls['get'])
                responses.append(response)
            
            # 所有请求都应该成功
            for response in responses:
                assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_multiple_clients(self, test_urls):
        """测试多个客户端实例"""
        client1 = requests.AsyncClient(headers={'X-Client': 'client1'})
        client2 = requests.AsyncClient(headers={'X-Client': 'client2'})
        
        try:
            async with client1, client2:
                response1 = await client1.get(test_urls['headers'])
                response2 = await client2.get(test_urls['headers'])
                
                data1 = response1.json()
                data2 = response2.json()
                
                assert data1['headers']['X-Client'] == 'client1'
                assert data2['headers']['X-Client'] == 'client2'
        
        finally:
            await client1.close()
            await client2.close()