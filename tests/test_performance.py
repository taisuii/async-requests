"""
性能测试
"""

import pytest
import asyncio
import time
import statistics
import requests_async as requests

class TestPerformance:
    """性能测试类"""
    
    @pytest.mark.asyncio
    async def test_single_request_latency(self, test_urls):
        """测试单个请求延迟"""
        latencies = []
        
        for _ in range(10):
            start_time = time.time()
            response = await requests.get(test_urls['get'])
            end_time = time.time()
            
            assert response.status_code == 200
            latencies.append(end_time - start_time)
        
        # 计算统计信息
        avg_latency = statistics.mean(latencies)
        median_latency = statistics.median(latencies)
        
        print(f"\n单请求性能统计:")
        print(f"平均延迟: {avg_latency:.3f}s")
        print(f"中位延迟: {median_latency:.3f}s")
        print(f"最小延迟: {min(latencies):.3f}s")
        print(f"最大延迟: {max(latencies):.3f}s")
        
        # 合理的性能期望（根据网络情况调整）
        assert avg_latency < 10.0  # 平均延迟应该小于10秒
    
    @pytest.mark.asyncio
    async def test_concurrent_throughput(self, test_urls):
        """测试并发吞吐量"""
        num_requests = 50
        
        start_time = time.time()
        
        # 创建大量并发请求
        tasks = [requests.get(test_urls['get']) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 验证所有请求都成功
        successful_requests = sum(1 for r in responses if r.status_code == 200)
        success_rate = successful_requests / num_requests
        
        throughput = num_requests / total_time
        
        print(f"\n并发性能统计:")
        print(f"总请求数: {num_requests}")
        print(f"成功请求数: {successful_requests}")
        print(f"成功率: {success_rate:.2%}")
        print(f"总耗时: {total_time:.3f}s")
        print(f"吞吐量: {throughput:.2f} requests/second")
        
        # 性能期望
        assert success_rate >= 0.95  # 成功率应该至少95%
        assert throughput > 1.0  # 吞吐量应该大于1 req/s
    
    @pytest.mark.asyncio
    async def test_session_vs_individual_requests(self, test_urls):
        """测试会话复用 vs 独立请求的性能"""
        num_requests = 20
        
        # 测试独立请求
        start_time = time.time()
        individual_tasks = [requests.get(test_urls['get']) for _ in range(num_requests)]
        await asyncio.gather(*individual_tasks)
        individual_time = time.time() - start_time
        
        # 测试会话复用
        start_time = time.time()
        async with requests.AsyncClient() as client:
            session_tasks = [client.get(test_urls['get']) for _ in range(num_requests)]
            await asyncio.gather(*session_tasks)
        session_time = time.time() - start_time
        
        print(f"\n会话复用性能对比:")
        print(f"独立请求耗时: {individual_time:.3f}s")
        print(f"会话复用耗时: {session_time:.3f}s")
        print(f"性能提升: {((individual_time - session_time) / individual_time * 100):.1f}%")
        
        # 会话复用通常应该更快（但不是绝对的，取决于网络条件）
        # 这里只是记录性能差异，不做严格断言
        assert session_time > 0  # 基本的合理性检查
        assert individual_time > 0
