"""
响应处理测试
"""

import pytest
import json
import requests_async as requests

class TestResponseHandling:
    """响应处理测试类"""
    
    @pytest.mark.asyncio
    async def test_response_properties(self, test_urls):
        """测试响应对象属性"""
        response = await requests.get(test_urls['get'])
        
        # 基本属性
        assert hasattr(response, 'status_code')
        assert hasattr(response, 'headers')
        assert hasattr(response, 'text')
        assert hasattr(response, 'content')
        assert hasattr(response, 'url')
        assert hasattr(response, 'ok')
        
        # 属性值验证
        assert isinstance(response.status_code, int)
        assert isinstance(response.headers, dict)
        assert isinstance(response.text, str)
        assert isinstance(response.content, bytes)
        assert isinstance(response.ok, bool)
    
    @pytest.mark.asyncio
    async def test_json_response_parsing(self, test_urls):
        """测试 JSON 响应解析"""
        response = await requests.get(test_urls['json'])
        
        assert response.status_code == 200
        
        # 测试 JSON 解析
        json_data = response.json()
        assert isinstance(json_data, dict)
        
        # httpbin.org/json 返回固定的 JSON 结构
        assert 'slideshow' in json_data
    
    @pytest.mark.asyncio
    async def test_text_response(self, test_urls):
        """测试文本响应"""
        response = await requests.get(test_urls['get'])
        
        assert response.status_code == 200
        assert len(response.text) > 0
        assert isinstance(response.text, str)
        
        # 文本应该包含 JSON 数据
        parsed = json.loads(response.text)
        assert isinstance(parsed, dict)
    
    @pytest.mark.asyncio
    async def test_binary_content(self, test_urls):
        """测试二进制内容"""
        response = await requests.get(test_urls['get'])
        
        assert response.status_code == 200
        assert isinstance(response.content, bytes)
        assert len(response.content) > 0
        
        # 验证二进制内容可以解码为文本
        decoded = response.content.decode('utf-8')
        assert decoded == response.text
    
    @pytest.mark.asyncio
    async def test_response_headers(self, test_urls):
        """测试响应头"""
        custom_headers = {'X-Test-Header': 'test-value'}
        response = await requests.get(test_urls['headers'], headers=custom_headers)
        
        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert 'Server' in response.headers
        
        # 验证我们发送的头部在响应中
        data = response.json()
        assert data['headers']['X-Test-Header'] == 'test-value'

