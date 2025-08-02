"""
pytest 配置文件和共享的 fixtures
"""

import pytest
import asyncio
import httpx
from unittest.mock import AsyncMock, MagicMock
import requests_async as requests

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环用于整个测试会话"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mock_httpx_client():
    """模拟 httpx 客户端的 fixture"""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    return mock_client

@pytest.fixture
async def sample_response():
    """创建示例响应对象"""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.headers = {'Content-Type': 'application/json'}
    mock_response.text = '{"message": "success", "data": {"id": 1, "name": "test"}}'
    mock_response.content = b'{"message": "success", "data": {"id": 1, "name": "test"}}'
    mock_response.json.return_value = {"message": "success", "data": {"id": 1, "name": "test"}}
    mock_response.url = "https://httpbin.org/get"
    mock_response.ok = True
    return mock_response

@pytest.fixture
def test_urls():
    """测试用的 URL 列表"""
    return {
        'get': 'https://httpbin.org/get',
        'post': 'https://httpbin.org/post', 
        'put': 'https://httpbin.org/put',
        'delete': 'https://httpbin.org/delete',
        'patch': 'https://httpbin.org/patch',
        'head': 'https://httpbin.org/head',
        'options': 'https://httpbin.org/options',
        'status_404': 'https://httpbin.org/status/404',
        'status_500': 'https://httpbin.org/status/500',
        'delay': 'https://httpbin.org/delay/1',
        'json': 'https://httpbin.org/json',
        'headers': 'https://httpbin.org/headers',
        'user_agent': 'https://httpbin.org/user-agent',
        'cookies': 'https://httpbin.org/cookies',
        'basic_auth': 'https://httpbin.org/basic-auth/user/pass'
    }
