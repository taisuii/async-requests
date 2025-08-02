"""
测试运行脚本
"""

import asyncio
import subprocess
import sys
import os

def run_command(command):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """主函数"""
    print("🧪 开始运行 requests-async 测试套件")
    print("=" * 50)
    
    # 检查是否安装了依赖
    print("1. 检查测试依赖...")
    success, _, _ = run_command("pip show pytest pytest-asyncio")
    if not success:
        print("❌ 请先安装测试依赖: pip install pytest pytest-asyncio")
        return 1
    
    print("✅ 测试依赖已安装")
    
    # 运行不同类型的测试
    test_commands = [
        ("基本功能测试", "pytest tests/test_basic_requests.py -v"),
        ("请求参数测试", "pytest tests/test_request_parameters.py -v"),
        ("AsyncClient 测试", "pytest tests/test_async_client.py -v"),
        ("错误处理测试", "pytest tests/test_error_handling.py -v"),
        ("响应处理测试", "pytest tests/test_response_handling.py -v"),
        ("并发请求测试", "pytest tests/test_concurrent_requests.py -v"),
        ("集成测试", "pytest tests/test_integration.py -v"),
        ("边界情况测试", "pytest tests/test_edge_cases.py -v"),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test_name, command in test_commands:
        print(f"\n2. 运行 {test_name}...")
        success, stdout, stderr = run_command(command)
        
        if success:
            print(f"✅ {test_name} 通过")
            # 尝试提取通过的测试数量
            if "passed" in stdout:
                try:
                    passed = int(stdout.split("passed")[0].split()[-1])
                    total_passed += passed
                except:
                    total_passed += 1
        else:
            print(f"❌ {test_name} 失败")
            print(f"错误输出: {stderr}")
            if "failed" in stdout:
                try:
                    failed = int(stdout.split("failed")[0].split()[-1])
                    total_failed += failed
                except:
                    total_failed += 1
    
    # 运行性能测试（可选）
    print(f"\n3. 运行性能测试（可能较慢）...")
    success, stdout, stderr = run_command("pytest tests/test_performance.py -v -s")
    if success:
        print("✅ 性能测试完成")
    else:
        print("⚠️  性能测试可能因网络条件失败，这是正常的")
    
    # 运行覆盖率测试
    print(f"\n4. 生成测试覆盖率报告...")
    success, stdout, stderr = run_command("pytest --cov=requests_async --cov-report=term-missing tests/")
    if success:
        print("✅ 覆盖率报告生成完成")
        print(stdout)
    else:
        print("⚠️  覆盖率报告生成失败，请安装 pytest-cov")
    
    # 总结
    print("\n" + "=" * 50)
    print("🎯 测试总结:")
    print(f"✅ 通过的测试: {total_passed}")
    print(f"❌ 失败的测试: {total_failed}")
    
    if total_failed == 0:
        print("🎉 所有测试都通过了！")
        return 0
    else:
        print("💔 有一些测试失败了，请检查上面的错误信息")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
