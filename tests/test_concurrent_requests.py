"""
并发请求测试
"""

import pytest
import asyncio
import time
import requests_async as requests

class TestConcurrentRequests:
    """并发请求测试类"""
    
    @pytest.mark.asyncio
    async def test_basic_concurrent_requests(self, test_urls):
        """测试基本并发请求"""
        urls = [test_urls['get'], test_urls['json'], test_urls['headers']]
        
        # 并发执行请求
        tasks = [requests.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        # 验证所有请求都成功
        assert len(responses) == len(urls)
        for response in responses:
            assert response.status_code == 200
            assert response.ok
    
    @pytest.mark.asyncio
    async def test_concurrent_performance(self):
        """测试并发性能"""
        # 使用延迟端点测试并发性能
        delay_time = 1
        num_requests = 5
        urls = [f'https://httpbin.org/delay/{delay_time}'] * num_requests
        
        start_time = time.time()
        
        # 并发执行
        tasks = [requests.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 并发执行应该接近单个请求的时间，而不是所有请求时间的总和
        assert total_time < (delay_time * num_requests * 0.8)  # 允许一些网络开销
        
        # 验证所有请求都成功
        for response in responses:
            assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_concurrent_with_different_methods(self, test_urls):
        """测试不同 HTTP 方法的并发请求"""
        tasks = [
            requests.get(test_urls['get']),
            requests.post(test_urls['post'], json={'test': 'data'}),
            requests.put(test_urls['put'], json={'update': 'value'}),
            requests.delete(test_urls['delete'])
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # 验证所有请求都成功
        for response in responses:
            assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_concurrent_error_handling(self):
        """测试并发请求中的错误处理"""
        urls = [
            'https://httpbin.org/get',  # 成功
            'https://httpbin.org/status/404',  # 404 错误
            'https://httpbin.org/status/500',  # 500 错误
            'https://httpbin.org/get'  # 成功
        ]
        
        # 并发执行，不应该因为部分失败而停止
        tasks = [requests.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=False)
        
        # 验证响应状态
        assert responses[0].status_code == 200  # 成功
        assert responses[1].status_code == 404  # 404
        assert responses[2].status_code == 500  # 500
        assert responses[3].status_code == 200  # 成功
    
    @pytest.mark.asyncio
    async def test_concurrent_with_session(self, test_urls):
        """测试使用会话的并发请求"""
        async with requests.AsyncClient() as client:
            tasks = [
                client.get(test_urls['get']),
                client.get(test_urls['json']),
                client.get(test_urls['headers']),
                client.get(test_urls['user_agent'])
            ]
            
            responses = await asyncio.gather(*tasks)
            
            # 验证所有请求都成功
            for response in responses:
                assert response.status_code == 200
