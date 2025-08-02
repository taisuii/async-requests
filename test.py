
"""
异步HTTP请求库使用示例
"""
import asyncio
from requests_async import (
    requests_async, get, post, get_json, post_json, 
    batch_get, download_file, session, AsyncRequests
)


async def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 方式1: 使用全局实例
    try:
        response = await requests_async.get("https://httpbin.org/get")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 方式2: 使用全局函数
    try:
        response = await get("https://httpbin.org/get", params={"key": "value"})
        print(f"使用全局函数 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"请求失败: {e}")


async def example_different_methods():
    """不同HTTP方法示例"""
    print("\n=== 不同HTTP方法示例 ===")
    
    base_url = "https://httpbin.org"
    
    try:
        # GET请求
        get_response = await get(f"{base_url}/get", params={"test": "get"})
        print(f"GET: {get_response.status_code}")
        
        # POST请求
        post_response = await post(f"{base_url}/post", json={"test": "post"})
        print(f"POST: {post_response.status_code}")
        
        # PUT请求
        put_response = await requests_async.put(f"{base_url}/put", json={"test": "put"})
        print(f"PUT: {put_response.status_code}")
        
        # DELETE请求
        delete_response = await requests_async.delete(f"{base_url}/delete")
        print(f"DELETE: {delete_response.status_code}")
        
    except Exception as e:
        print(f"请求失败: {e}")


async def example_json_convenience():
    """JSON便利方法示例"""
    print("\n=== JSON便利方法示例 ===")
    
    try:
        # 直接获取JSON数据
        data = await get_json("https://httpbin.org/json")
        print(f"JSON数据: {data}")
        
        # POST JSON数据并获取JSON响应
        response_data = await post_json(
            "https://httpbin.org/post", 
            {"name": "测试", "value": 123}
        )
        print(f"POST JSON响应: {response_data.get('json', {})}")
        
    except Exception as e:
        print(f"JSON请求失败: {e}")


async def example_batch_requests():
    """批量请求示例"""
    print("\n=== 批量请求示例 ===")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2", 
        "https://httpbin.org/get?id=1",
        "https://httpbin.org/get?id=2",
    ]
    
    try:
        print("开始批量请求...")
        import time
        start_time = time.time()
        
        responses = await batch_get(urls)
        
        end_time = time.time()
        print(f"批量请求完成，耗时: {end_time - start_time:.2f}秒")
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"URL {i+1} 请求失败: {response}")
            else:
                print(f"URL {i+1} 状态码: {response.status_code}")
                
    except Exception as e:
        print(f"批量请求失败: {e}")


async def example_session_usage():
    """会话使用示例"""
    print("\n=== 会话使用示例 ===")
    
    try:
        # 使用会话上下文管理器
        async with session(timeout=15, max_retries=2) as s:
            # 设置默认头部
            s.set_default_headers({"User-Agent": "AsyncRequests/1.0"})
            
            response1 = await s.get("https://httpbin.org/headers")
            print(f"会话请求1: {response1.status_code}")
            
            response2 = await s.get("https://httpbin.org/user-agent")  
            print(f"会话请求2: {response2.status_code}")
            
            # 安全地解析JSON响应
            try:
                user_agent_data = response2.json()
                if user_agent_data and 'user-agent' in user_agent_data:
                    print(f"User-Agent: {user_agent_data['user-agent']}")
                else:
                    print(f"User-Agent响应: {user_agent_data}")
            except Exception as json_error:
                print(f"JSON解析失败: {json_error}")
                print(f"原始响应: {response2.text}")
            
    except Exception as e:
        print(f"会话请求失败: {e}")
        import traceback
        traceback.print_exc()


async def example_custom_client():
    """自定义客户端示例"""
    print("\n=== 自定义客户端示例 ===")
    
    # 创建自定义配置的客户端
    client = AsyncRequests(
        timeout=20.0,
        max_retries=5,
        default_headers={"Custom-Header": "MyValue"}
    )
    
    try:
        async with client:
            response = await client.get("https://httpbin.org/headers")
            print(f"响应状态码: {response.status_code}")
            
            # 安全地解析JSON响应
            try:
                headers_data = response.json()
                if headers_data and isinstance(headers_data, dict):
                    headers = headers_data.get('headers', {})
                    if isinstance(headers, dict):
                        custom_header = headers.get('Custom-Header', '未找到')
                        print(f"自定义头部已发送: {custom_header}")
                    else:
                        print(f"headers字段不是字典: {headers}")
                else:
                    print(f"响应数据格式异常: {headers_data}")
            except Exception as json_error:
                print(f"JSON解析失败: {json_error}")
                print(f"原始响应: {response.text}")
            
    except Exception as e:
        print(f"自定义客户端请求失败: {e}")
        import traceback
        traceback.print_exc()


async def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    # 测试超时
    try:
        response = await get("https://httpbin.org/delay/15", timeout=5)
        print("不应该执行到这里")
    except Exception as e:
        print(f"预期的超时错误: {type(e).__name__}")
    
    # 测试404错误
    try:
        response = await get("https://httpbin.org/status/404")
        print("不应该执行到这里")
    except Exception as e:
        print(f"预期的404错误: {type(e).__name__}")
    
    # 测试重试机制（服务器错误）
    try:
        response = await get("https://httpbin.org/status/500")
        print("不应该执行到这里")
    except Exception as e:
        print(f"预期的500错误（已重试）: {type(e).__name__}")


async def simple_session_test():
    """简化的会话测试"""
    print("\n=== 简化会话测试 ===")
    
    try:
        async with session() as s:
            response = await s.get("https://httpbin.org/get")
            print(f"简化会话测试成功: {response.status_code}")
    except Exception as e:
        print(f"简化会话测试失败: {e}")
        import traceback
        traceback.print_exc()


async def simple_custom_client_test():
    """简化的自定义客户端测试"""
    print("\n=== 简化自定义客户端测试 ===")
    
    try:
        client = AsyncRequests()
        async with client:
            response = await client.get("https://httpbin.org/get")
            print(f"简化自定义客户端测试成功: {response.status_code}")
    except Exception as e:
        print(f"简化自定义客户端测试失败: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """主函数"""
    print("异步HTTP请求库测试开始\n")
    
    await example_basic_usage()
    await example_different_methods()
    await example_json_convenience()
    await example_batch_requests()
    
    # 先运行简化测试
    await simple_session_test()
    await simple_custom_client_test()
    
    # 再运行原始测试
    await example_session_usage()
    await example_custom_client()
    await example_error_handling()
    
    print("\n测试完成!")


if __name__ == '__main__':
    asyncio.run(main())
