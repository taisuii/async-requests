"""
集成测试
"""

import pytest
import asyncio
import requests_async as requests

class TestIntegration:
    """集成测试类"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, test_urls):
        """测试完整工作流程"""
        # 1. 获取初始数据
        response = await requests.get(test_urls['get'])
        assert response.status_code == 200
        initial_data = response.json()
        
        # 2. 发送数据进行处理
        processed_data = {
            'original_url': initial_data['url'],
            'processed_at': '2024-01-01T00:00:00Z',
            'status': 'processed'
        }
        
        response = await requests.post(test_urls['post'], json=processed_data)
        assert response.status_code == 200
        
        # 3. 验证处理结果
        result = response.json()
        assert result['json'] == processed_data
    
    @pytest.mark.asyncio
    async def test_authentication_workflow(self):
        """测试认证工作流程"""
        # 测试基本认证
        auth_url = 'https://httpbin.org/basic-auth/testuser/testpass'
        
        # 使用认证
        response = await requests.get(auth_url, auth=('testuser', 'testpass'))
        assert response.status_code == 200
        
        data = response.json()
        assert data['authenticated'] is True
        assert data['user'] == 'testuser'
    
    @pytest.mark.asyncio
    async def test_complex_data_flow(self, test_urls):
        """测试复杂数据流"""
        # 模拟真实应用场景：获取数据 -> 处理 -> 更新 -> 验证
        
        # 1. 获取用户信息
        user_data = {'user_id': 123, 'name': 'Test User'}
        response = await requests.post(test_urls['post'], json=user_data)
        assert response.status_code == 200
        
        # 2. 更新用户信息
        updated_data = {**user_data, 'last_login': '2024-01-01T12:00:00Z'}
        response = await requests.put(test_urls['put'], json=updated_data)
        assert response.status_code == 200
        
        # 3. 验证更新
        result = response.json()
        assert result['json']['last_login'] == updated_data['last_login']
    
    @pytest.mark.asyncio
    async def test_batch_operations(self, test_urls):
        """测试批量操作"""
        # 模拟批量数据处理
        batch_data = [
            {'id': 1, 'name': 'Item 1', 'status': 'active'},
            {'id': 2, 'name': 'Item 2', 'status': 'inactive'},
            {'id': 3, 'name': 'Item 3', 'status': 'pending'}
        ]
        
        # 并发处理每个项目
        tasks = []
        for item in batch_data:
            task = requests.post(test_urls['post'], json=item)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # 验证所有操作都成功
        for i, response in enumerate(responses):
            assert response.status_code == 200
            result = response.json()
            assert result['json'] == batch_data[i]
