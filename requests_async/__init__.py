"""
Requests-Async: 基于 httpx 的异步 HTTP 客户端库
让你只需要在 requests 调用前加 await 就能异步使用
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import (
    AsyncClient, 
    get, post, put, delete, patch, head, options, request,
    Response
)
from .exceptions import (
    RequestException, HTTPError, Timeout, ConnectionError,
    HTTPStatusError, ConnectError, ReadTimeout, WriteTimeout
)

__all__ = [
    'AsyncClient',
    'get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'request',
    'Response',
    'RequestException', 'HTTPError', 'Timeout', 'ConnectionError',
    'HTTPStatusError', 'ConnectError', 'ReadTimeout', 'WriteTimeout'
]

# requests_async/exceptions.py
"""
异常类定义 - 兼容 requests 的异常体系
"""

# 重新导出 httpx 的异常，保持与 requests 兼容的命名
from httpx import (
    RequestError as RequestException,
    HTTPStatusError as HTTPError,
    TimeoutException as Timeout,
    ConnectError as ConnectionError,
    HTTPStatusError,
    ConnectError,
    ReadTimeout,
    WriteTimeout,
)

__all__ = [
    'RequestException', 'HTTPError', 'Timeout', 'ConnectionError',
    'HTTPStatusError', 'ConnectError', 'ReadTimeout', 'WriteTimeout'
]