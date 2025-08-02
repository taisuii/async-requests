
# requests-async

> 一个基于 [httpx](https://www.python-httpx.org/) 封装，API 风格类似 requests 的现代、易用、支持自动重试的 Python 异步 HTTP 客户端

---

## 特性

- 🌟 极易上手，API 仿 requests 式风格
- 🏷️ 支持全局实例/上下文会话/自定义客户端多种用法
- 🔄 自动重试与失败指数回退
- 🔒 支持自定义 headers、代理、cookie、超时
- 📦 支持批量请求、文件下载
- 🛠️ 高度可扩展，可灵活传递所有 httpx 参数

---

## 安装

```bash
pip install requests-async
```

---

## 快速开始

### 1. 全局实例方式

```python
from requests_async import requests_async
response = await requests_async.get('https://example.com')
print(response.text)
```

### 2. 全局函数方式

```python
from requests_async import get, post
response = await get('https://example.com')
```

### 3. 会话 session（推荐）

```python
from requests_async import session

async with session(timeout=10) as s:
    resp = await s.get('https://httpbin.org/get')
    print(resp.json())
```

### 4. 自定义客户端（高级用法）

```python
from requests_async import AsyncRequests

client = AsyncRequests(timeout=25, max_retries=5, default_headers={"User-Agent": "Awesome-Async"})
async with client:
    r = await client.get('https://example.com/api/data')
    print(r.status_code, r.text)
```

---

## 常用 API

| 方法/函数                              | 说明                       |
| --------------------------------------- | -------------------------- |
| `get(url, **kwargs)`                    | 异步 GET 请求              |
| `post(url, **kwargs)`                   | 异步 POST 请求             |
| `put/patch/delete/head/options(...)`    | 其他常规 HTTP 请求         |
| `get_json(url, **kwargs)`               | GET 请求并 parse JSON      |
| `post_json(url, json_data, **kwargs)`   | POST JSON 并 parse JSON    |
| `download_file(url, file_path, **kw)`   | 下载文件，支持断点续传     |
| `batch_get(urls, **kwargs)`             | 批量 GET 请求（并发）      |

- 支持所有 httpx/requests 关键字参数

---

## 参数补充说明

- `timeout`: 超时秒数，默认 10
- `max_retries`: 自动重试次数，默认 3
- `default_headers`: 请求默认头，可全局配置
- `proxies/cookies/headers` 等均和 requests/httpx 兼容

---

## 异常处理

所有请求失败且达到最大重试会抛出 `AsyncRequestError`。建议配合 try/except 捕获：

```python
from requests_async import AsyncRequestError

try:
    await get("https://unreachable.url/")
except AsyncRequestError as e:
    print("请求失败：", e)
```

---

## 依赖

- [httpx](https://www.python-httpx.org/)
- [loguru](https://github.com/Delgan/loguru)

---

## 贡献和反馈

欢迎 PR、issue，也欢迎参与改进文档和样例代码！

---

## License

MIT

