"""
错误处理测试
"""

import pytest
import asyncio
import requests_async as requests

class TestErrorHandling:
    """错误处理测试类"""
    
    @pytest.mark.asyncio
    async def test_http_404_error(self, test_urls):
        """测试 404 错误"""
        response = await requests.get(test_urls['status_404'])
        
        assert response.status_code == 404
        assert not response.ok
        
        with pytest.raises(requests.HTTPError):
            response.raise_for_status()
    
    @pytest.mark.asyncio
    async def test_http_500_error(self, test_urls):
        """测试 500 错误"""
        response = await requests.get(test_urls['status_500'])
        
        assert response.status_code == 500
        assert not response.ok
        
        with pytest.raises(requests.HTTPError):
            response.raise_for_status()
    
    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """测试连接超时"""
        with pytest.raises(requests.Timeout):
            # 使用很短的超时时间
            await requests.get('https://httpbin.org/delay/5', timeout=0.1)
    
    @pytest.mark.asyncio
    async def test_connection_error(self):
        """测试连接错误"""
        with pytest.raises(requests.ConnectionError):
            # 连接到不存在的域名
            await requests.get('https://this-domain-absolutely-does-not-exist.com')
    
    @pytest.mark.asyncio
    async def test_invalid_url(self):
        """测试无效 URL"""
        with pytest.raises((requests.RequestException, ValueError)):
            await requests.get('invalid-url')
    
    @pytest.mark.asyncio
    async def test_exception_with_response_info(self, test_urls):
        """测试异常包含响应信息"""
        response = await requests.get(test_urls['status_404'])
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            assert e.response is not None
            assert e.response.status_code == 404