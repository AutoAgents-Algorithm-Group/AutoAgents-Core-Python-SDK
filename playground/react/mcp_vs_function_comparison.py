"""
MCP工具 vs 本地函数工具 - 格式对比详解

详细展示两种工具类型在定义、标准化、选择、执行各个环节的格式差异
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import json
from datetime import datetime
from src.autoagentsai.tools import ToolManager, ToolWrapper, tool
from src.autoagentsai.client.MCPClient import McpServerConfig

print("=" * 80)
print("🔄 MCP工具 vs 本地函数工具 - 完整格式对比")
print("=" * 80)

# ============= 1. 工具定义格式对比 =============
print("\n📝 1. 工具定义格式对比")
print("=" * 50)

print("🔹 本地函数工具定义：")
print("```python")
print("""# 方式1: @tool装饰器
@tool(name="加法计算器", description="计算两个数字的和")
def add(a: int, b: int) -> int:
    return a + b

# 方式2: ToolWrapper包装
def multiply(x: float, y: float) -> float:
    return x * y
wrapped_tool = ToolWrapper(multiply, "乘法计算器", "执行乘法运算")

# 方式3: 普通函数（自动推断）
def get_current_time() -> str:
    '''获取当前时间'''
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")""")
print("```")

print("\n🔹 MCP工具定义：")
print("```python")
print("""# MCP服务器配置
mcp_config = {
    "exa": {
        "transport": "streamable_http",
        "url": "https://exa-mcp-server.glitch.me/"
    }
}

# MCP工具通过网络获取，无需本地定义
# 从MCP服务器的 list_tools() 接口获取工具schema""")
print("```")

# ============= 2. 标准化后格式对比 =============
print("\n\n🔧 2. 标准化后的工具格式对比")
print("=" * 50)

# 创建本地函数工具示例
@tool(name="加法计算器", description="计算两个数字的和")
def add(a: int, b: int) -> int:
    return a + b

def get_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 模拟标准化
tool_manager = ToolManager(None, [add, get_time])
function_tool = tool_manager.tools[0].copy()
function_tool.pop('function', None)  # 移除函数对象以便显示

# MCP工具格式
mcp_tool = {
    "name": "search",
    "description": "Perform a search query and get results with content, title, and URLs",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return",
                "default": 10
            }
        },
        "required": ["query"]
    },
    "tool_type": "mcp",
    "server_name": "exa_search",
    "server_config": {
        "transport": "streamable_http",
        "url": "https://exa-mcp-server.glitch.me/"
    }
}

print("🔹 本地函数工具标准化格式：")
print(json.dumps(function_tool, ensure_ascii=False, indent=2))

print("\n🔹 MCP工具标准化格式：")
print(json.dumps(mcp_tool, ensure_ascii=False, indent=2))

# ============= 3. 关键字段对比 =============
print("\n\n🏷️ 3. 关键字段对比")
print("=" * 50)

comparison_table = """
┌─────────────────┬──────────────────────┬──────────────────────┐
│      字段       │      本地函数         │       MCP工具        │
├─────────────────┼──────────────────────┼──────────────────────┤
│ tool_type       │ "function"           │ "mcp"                │
│ server_name     │ "local" 或 无        │ "exa_search" 等      │
│ server_config   │ 无                   │ {transport, url...}  │
│ function        │ Python函数对象        │ 无                   │
│ name            │ 函数名或自定义        │ MCP服务器定义         │
│ description     │ 函数docstring       │ MCP服务器定义         │
│ inputSchema     │ 从类型注解推导        │ MCP服务器提供         │
└─────────────────┴──────────────────────┴──────────────────────┘
"""
print(comparison_table)

# ============= 4. AI工具选择格式对比 =============
print("\n\n🎯 4. AI工具选择格式对比")
print("=" * 50)

print("🔹 选择本地函数工具：")
function_selection = {
    "selected_tools": [
        {
            "tool_name": "加法计算器",
            "arguments": {"a": 15, "b": 25},
            "reason": "用户需要计算两个数字的和"
        },
        {
            "tool_name": "get_time",
            "arguments": {},
            "reason": "用户询问当前时间"
        }
    ]
}
print(json.dumps(function_selection, ensure_ascii=False, indent=2))

print("\n🔹 选择MCP工具：")
mcp_selection = {
    "selected_tools": [
        {
            "tool_name": "search",
            "arguments": {
                "query": "AutoAgents Python SDK",
                "num_results": 5
            },
            "reason": "用户需要搜索AutoAgents相关信息"
        }
    ]
}
print(json.dumps(mcp_selection, ensure_ascii=False, indent=2))

# ============= 5. 工具执行流程对比 =============
print("\n\n🔄 5. 工具执行流程对比")
print("=" * 50)

function_workflow = """
🔹 本地函数工具执行流程：
1. ToolManager.execute_tools()
   ├─ 识别 tool_type='function'
   ├─ 调用 _call_custom_function(tool_config, arguments)
   ├─ 获取 function 对象: tool_config['function']
   ├─ 参数匹配: inspect.signature(func).bind(**arguments)
   ├─ 同步/异步检查: asyncio.iscoroutinefunction(func)
   ├─ 直接调用: func(**arguments) 或 await func(**arguments)
   └─ 返回Python对象结果
"""

mcp_workflow = """
🔹 MCP工具执行流程：
1. ToolManager.execute_tools()
   ├─ 识别 tool_type='mcp'
   ├─ 调用 _call_mcp_tool(tool_name, tool_config, arguments)
   ├─ 获取 server_config: tool_config['server_config']
   ├─ 检查传输类型: server_config.transport
   ├─ 建立连接: streamable_http_client(server_config.url)
   ├─ 创建会话: mcp.ClientSession(read_stream, write_stream)
   ├─ 初始化: await session.initialize()
   ├─ 远程调用: await session.call_tool(tool_name, arguments)
   └─ 返回JSON响应结果
"""

print(function_workflow)
print(mcp_workflow)

# ============= 6. 执行结果格式对比 =============
print("\n\n📊 6. 执行结果格式对比")
print("=" * 50)

print("🔹 本地函数工具执行成功结果：")
function_success = {
    "tool": "加法计算器",
    "tool_type": "function",
    "reason": "用户需要计算两个数字的和",
    "arguments": {"a": 15, "b": 25},
    "result": 40,  # 直接的Python值
    "status": "success"
}
print(json.dumps(function_success, ensure_ascii=False, indent=2))

print("\n🔹 MCP工具执行成功结果：")
mcp_success = {
    "tool": "search",
    "tool_type": "mcp",
    "reason": "用户需要搜索AutoAgents相关信息",
    "arguments": {
        "query": "AutoAgents Python SDK",
        "num_results": 5
    },
    "result": {  # 复杂的JSON结构
        "results": [
            {
                "title": "AutoAgents Python SDK Documentation",
                "url": "https://github.com/autoagents/python-sdk",
                "snippet": "Official Python SDK for AutoAgents platform..."
            }
        ]
    },
    "status": "success"
}
print(json.dumps(mcp_success, ensure_ascii=False, indent=2))

# ============= 7. 错误处理对比 =============
print("\n\n❌ 7. 错误处理格式对比")
print("=" * 50)

print("🔹 本地函数工具错误：")
function_error = {
    "tool": "除法计算器",
    "tool_type": "function",
    "error": "调用函数失败: 除数不能为零",  # Python异常信息
    "status": "error"
}
print(json.dumps(function_error, ensure_ascii=False, indent=2))

print("\n🔹 MCP工具错误：")
mcp_error = {
    "tool": "search",
    "tool_type": "mcp", 
    "error": "MCP模块导入失败: 网络连接超时",  # 网络/协议错误
    "status": "error"
}
print(json.dumps(mcp_error, ensure_ascii=False, indent=2))

# ============= 8. 控制台输出对比 =============
print("\n\n📺 8. 控制台输出对比")
print("=" * 50)

function_console = """
🔹 本地函数工具控制台输出：
🎯 AI选择了 1 个工具:
   1. 加法计算器
      理由: 用户需要计算两个数字的和
      参数: {'a': 15, 'b': 25}

✅ 工具执行成功: 加法计算器
   工具类型: function
   调用参数: {'a': 15, 'b': 25}
   执行结果: 40
"""

mcp_console = """
🔹 MCP工具控制台输出：
🎯 AI选择了 1 个工具:
   1. search
      理由: 用户需要搜索AutoAgents相关信息
      参数: {'query': 'AutoAgents Python SDK', 'num_results': 5}

✅ 工具执行成功: search
   工具类型: mcp
   调用参数: {'query': 'AutoAgents Python SDK', 'num_results': 5}
   执行结果: {'results': [{'title': 'AutoAgents...', 'url': '...'}]}
"""

print(function_console)
print(mcp_console)

# ============= 9. 性能和特性对比 =============
print("\n\n⚡ 9. 性能和特性对比")
print("=" * 50)

performance_comparison = """
┌─────────────────┬──────────────────────┬──────────────────────┐
│      特性       │      本地函数         │       MCP工具        │
├─────────────────┼──────────────────────┼──────────────────────┤
│ 执行速度        │ 极快 (直接调用)       │ 较慢 (网络通信)       │
│ 资源消耗        │ 低 (本地内存)        │ 中等 (网络+解析)      │
│ 可用性          │ 高 (无依赖)          │ 中等 (依赖网络)       │
│ 扩展性          │ 低 (需要代码更新)     │ 高 (动态加载)         │
│ 安全性          │ 中等 (本地执行)       │ 高 (远程隔离)         │
│ 调试难度        │ 低 (本地调试)        │ 高 (远程调试)         │
│ 部署复杂度      │ 低 (打包即可)        │ 中等 (需要MCP服务器)   │
│ 功能丰富度      │ 低 (自定义实现)       │ 高 (生态丰富)         │
└─────────────────┴──────────────────────┴──────────────────────┘
"""
print(performance_comparison)

# ============= 10. 使用场景对比 =============
print("\n\n🎯 10. 使用场景对比")
print("=" * 50)

use_cases = {
    "本地函数工具": [
        "✅ 数学计算、数据处理",
        "✅ 本地文件操作",
        "✅ 简单的业务逻辑",
        "✅ 快速原型开发",
        "✅ 离线环境使用",
        "✅ 性能敏感场景"
    ],
    "MCP工具": [
        "✅ 网页搜索、API调用",
        "✅ 外部数据库查询",
        "✅ 第三方服务集成",
        "✅ 复杂的AI服务",
        "✅ 生产环境部署",
        "✅ 多团队协作开发"
    ]
}

for tool_type, scenarios in use_cases.items():
    print(f"\n🔹 {tool_type}适用场景：")
    for scenario in scenarios:
        print(f"  {scenario}")

# ============= 11. 代码示例对比 =============
print("\n\n💻 11. 完整代码示例对比")
print("=" * 50)

print("🔹 本地函数工具使用示例：")
print("```python")
function_example = """
# 1. 定义工具
@tool(name="计算器", description="数学计算")
def calculate(a: int, b: int, op: str) -> float:
    if op == '+': return a + b
    elif op == '*': return a * b
    return 0

# 2. 创建Agent
tools = [calculate]
agent = create_react_agent(chat_client, tools)

# 3. 使用
result = await agent.invoke("计算 15 + 25")
# 执行: calculate(15, 25, '+') -> 40
"""
print(function_example)
print("```")

print("\n🔹 MCP工具使用示例：")
print("```python")
mcp_example = """
# 1. 配置MCP服务器
mcp_client = MCPClient({
    "search": {
        "transport": "streamable_http",
        "url": "https://search-server.com/"
    }
})

# 2. 获取MCP工具
mcp_tools = await mcp_client.get_tools()

# 3. 创建Agent
agent = create_react_agent(chat_client, mcp_tools)

# 4. 使用
result = await agent.invoke("搜索Python教程")
# 执行: HTTP请求到search-server.com -> JSON响应
"""
print(mcp_example)
print("```")

print("\n" + "=" * 80)
print("✨ 总结：选择指南")
print("=" * 80)

selection_guide = """
🎯 选择本地函数工具，当你需要：
• 🚀 极致性能和低延迟
• 🔒 完全离线运行能力  
• 🛠️ 简单的计算和处理逻辑
• 🐛 便于调试和维护
• 📦 简化部署流程

🎯 选择MCP工具，当你需要：
• 🌐 访问外部API和服务
• 🔧 丰富的工具生态系统
• 🛡️ 更高的安全隔离
• 🔄 动态扩展工具能力
• 👥 多团队协作开发

💡 最佳实践：混合使用
在同一个Agent中同时使用两种类型的工具：
• 本地函数处理计算和基础逻辑
• MCP工具处理外部API和复杂服务
• ToolManager自动识别和分发执行
"""

print(selection_guide) 


agent = create_react_agent(
    chat_client=chat_client,
    tools=tools
)

result = await agent.invoke("计算 15 + 25")
print(result)