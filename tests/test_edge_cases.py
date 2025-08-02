"""
边界情况和边缘案例测试
"""

import pytest
import asyncio
import requests_async as requests

class TestEdgeCases:
    """边界情况测试类"""
    
    @pytest.mark.asyncio
    async def test_empty_response(self):
        """测试空响应"""
        # HEAD 请求通常返回空 body
        response = await requests.head('https://httpbin.org/get')
        
        assert response.status_code == 200
        assert len(response.content) == 0
        assert response.text == ""
    
    @pytest.mark.asyncio
    async def test_large_response(self):
        """测试大响应（如果服务支持）"""
        # 请求一个较大的响应
        try:
            response = await requests.get('https://httpbin.org/bytes/10000')
            assert response.status_code == 200
            assert len(response.content) == 10000
        except Exception:
            # 如果服务不可用，跳过测试
            pytest.skip("Large response test endpoint not available")
    
    @pytest.mark.asyncio
    async def test_unicode_content(self, test_urls):
        """测试 Unicode 内容处理"""
        unicode_data = {
            'chinese': '你好世界',
            'japanese': 'こんにちは',
            'emoji': '🚀✨🎉',
            'arabic': 'مرحبا بالعالم'
        }
        
        response = await requests.post(test_urls['post'], json=unicode_data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['json'] == unicode_data
    
    @pytest.mark.asyncio
    async def test_special_characters_in_url(self):
        """测试 URL 中的特殊字符"""
        # 测试查询参数中的特殊字符
        params = {
            'query': 'hello world & special chars!',
            'symbols': '~`!@#$%^&*()_+-={}[]|\\:";\'<>?,./""'
        }
        
        response = await requests.get('https://httpbin.org/get', params=params)
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_multiple_redirects(self):
        """测试多次重定向"""
        # httpbin 支持多次重定向测试
        response = await requests.get('https://httpbin.org/redirect/3')
        
        assert response.status_code == 200
        data = response.json()
        assert 'url' in data
    
    @pytest.mark.asyncio
    async def test_malformed_json_response(self):
        """测试格式错误的 JSON 响应"""
        # 这个测试需要一个返回无效 JSON 的端点
        # 由于 httpbin 总是返回有效的 JSON，我们模拟这种情况
        try:
            response = await requests.get('https://httpbin.org/html')
            # 尝试将 HTML 解析为 JSON 应该会失败
            with pytest.raises(Exception):  # JSON 解析错误
                response.json()
        except Exception:
            # 如果端点不可用，跳过测试
            pytest.skip("HTML endpoint not available")
    
    @pytest.mark.asyncio
    async def test_extremely_long_url(self):
        """测试极长的 URL"""
        # 创建一个很长的查询字符串
        long_params = {f'param_{i}': f'value_{i}' * 10 for i in range(50)}
        
        try:
            response = await requests.get('https://httpbin.org/get', params=long_params)
            # 如果服务器接受，应该返回 200
            assert response.status_code in [200, 414]  # 414 = URI Too Long
        except requests.RequestException:
            # 可能会因为 URL 太长而失败，这是预期的
            pass
    
    @pytest.mark.asyncio
    async def test_concurrent_client_creation_destruction(self):
        """测试并发创建和销毁客户端"""
        async def create_and_use_client():
            async with requests.AsyncClient() as client:
                response = await client.get('https://httpbin.org/get')
                return response.status_code
        
        # 并发创建多个客户端
        tasks = [create_and_use_client() for _ in range(10)]
        status_codes = await asyncio.gather(*tasks)
        
        # 所有请求都应该成功
        for status_code in status_codes:
            assert status_code == 200
    
    @pytest.mark.asyncio
    async def test_request_cancellation(self):
        """测试请求取消"""
        async def long_request():
            return await requests.get('https://httpbin.org/delay/10')
        
        # 创建任务并立即取消
        task = asyncio.create_task(long_request())
        await asyncio.sleep(0.1)  # 让请求开始
        task.cancel()
        
        with pytest.raises(asyncio.CancelledError):
            await task
