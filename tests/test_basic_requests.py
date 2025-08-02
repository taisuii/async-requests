"""
基本请求功能测试
"""

import pytest
import asyncio
import requests_async as requests

class TestBasicRequests:
    """基本请求测试类"""
    
    @pytest.mark.asyncio
    async def test_get_request(self, test_urls):
        """测试 GET 请求"""
        response = await requests.get(test_urls['get'])
        
        assert response.status_code == 200
        assert response.ok
        assert 'url' in response.json()
        assert response.headers['Content-Type'].startswith('application/json')
    
    @pytest.mark.asyncio
    async def test_post_request(self, test_urls):
        """测试 POST 请求"""
        test_data = {'name': 'test', 'value': 123, 'active': True}
        
        response = await requests.post(test_urls['post'], json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['json'] == test_data
        assert 'Content-Type' in data['headers']
    
    @pytest.mark.asyncio
    async def test_put_request(self, test_urls):
        """测试 PUT 请求"""
        test_data = {'action': 'update', 'id': 42}
        
        response = await requests.put(test_urls['put'], json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['json'] == test_data
    
    @pytest.mark.asyncio
    async def test_delete_request(self, test_urls):
        """测试 DELETE 请求"""
        response = await requests.delete(test_urls['delete'])
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_patch_request(self, test_urls):
        """测试 PATCH 请求"""
        test_data = {'field': 'patched'}
        
        response = await requests.patch(test_urls['patch'], json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['json'] == test_data
    
    @pytest.mark.asyncio
    async def test_head_request(self, test_urls):
        """测试 HEAD 请求"""
        response = await requests.head(test_urls['head'])
        
        assert response.status_code == 200
        assert len(response.content) == 0  # HEAD 请求没有 body
        assert 'Content-Type' in response.headers
    
    @pytest.mark.asyncio
    async def test_options_request(self, test_urls):
        """测试 OPTIONS 请求"""
        response = await requests.options(test_urls['options'])
        
        assert response.status_code == 200
        assert 'Allow' in response.headers
