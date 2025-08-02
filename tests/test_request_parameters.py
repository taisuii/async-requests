"""
请求参数测试
"""

import pytest
import requests_async as requests

class TestRequestParameters:
    """请求参数测试类"""
    
    @pytest.mark.asyncio
    async def test_query_parameters(self, test_urls):
        """测试查询参数"""
        params = {
            'param1': 'value1',
            'param2': 'value2',
            'number': 42,
            'boolean': True
        }
        
        response = await requests.get(test_urls['get'], params=params)
        
        assert response.status_code == 200
        data = response.json()
        
        # httpbin 返回的查询参数都是字符串
        assert data['args']['param1'] == 'value1'
        assert data['args']['param2'] == 'value2'
        assert data['args']['number'] == '42'
        assert data['args']['boolean'] == 'True'
    
    @pytest.mark.asyncio
    async def test_form_data(self, test_urls):
        """测试表单数据"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass',
            'remember': 'on'
        }
        
        response = await requests.post(test_urls['post'], data=form_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['form'] == form_data
    
    @pytest.mark.asyncio
    async def test_json_data(self, test_urls):
        """测试 JSON 数据"""
        json_data = {
            'user': {
                'name': 'John Doe',
                'age': 30,
                'preferences': ['coding', 'reading']
            },
            'metadata': {
                'timestamp': '2024-01-01T00:00:00Z',
                'version': '1.0'
            }
        }
        
        response = await requests.post(test_urls['post'], json=json_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['json'] == json_data
        assert data['headers']['Content-Type'] == 'application/json'
    
    @pytest.mark.asyncio
    async def test_custom_headers(self, test_urls):
        """测试自定义请求头"""
        headers = {
            'User-Agent': 'requests-async-test/1.0',
            'Authorization': 'Bearer fake-token-12345',
            'X-API-Key': 'test-api-key',
            'X-Custom-Header': 'custom-value'
        }
        
        response = await requests.get(test_urls['headers'], headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        for key, value in headers.items():
            assert data['headers'][key] == value
    
    @pytest.mark.asyncio
    async def test_cookies(self, test_urls):
        """测试 Cookies"""
        cookies = {
            'session_id': 'abc123',
            'user_pref': 'dark_mode',
            'lang': 'zh-CN'
        }
        
        # 设置 cookies
        response = await requests.get(
            'https://httpbin.org/cookies/set',
            params=cookies,
            allow_redirects=False  # 不跟随重定向
        )
        
        # 验证 cookies 设置
        response = await requests.get(test_urls['cookies'], cookies=cookies)
        assert response.status_code == 200
        data = response.json()
        
        for key, value in cookies.items():
            assert data['cookies'][key] == value
