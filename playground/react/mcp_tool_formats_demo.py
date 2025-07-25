"""
MCP工具调用格式详解演示

展示MCP (Multi-Client Protocol) 工具的详细格式和调用流程
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import json
from dataclasses import dataclass
from typing import Optional, List
from src.autoagentsai.client.McpClient import McpServerConfig

print("=" * 80)
print("🌐 MCP工具调用格式详解")
print("=" * 80)

# ============= 1. MCP服务器配置格式 =============
print("\n📡 1. MCP服务器配置格式")
print("-" * 50)

print("🔹 McpServerConfig 数据类：")
print("```python")
print("""@dataclass
class McpServerConfig:
    transport: str              # 传输方式: "streamable_http" 或 "stdio"
    command: Optional[str] = None  # stdio命令
    args: Optional[List[str]] = None  # stdio参数
    url: Optional[str] = None   # HTTP服务器URL""")
print("```")

print("\n🔹 具体配置示例：")
# HTTP服务器配置示例
http_config = {
    "transport": "streamable_http",
    "url": "https://exa-mcp-server.glitch.me/"
}

stdio_config = {
    "transport": "stdio", 
    "command": "node",
    "args": ["/path/to/filesystem-server.js"]
}

print("HTTP服务器配置：")
print(json.dumps(http_config, ensure_ascii=False, indent=2))

print("\nSTDIO服务器配置：")
print(json.dumps(stdio_config, ensure_ascii=False, indent=2))

# ============= 2. MCP工具字典格式 =============
print("\n\n🛠️ 2. MCP工具的标准字典格式")
print("-" * 50)

print("从MCP服务器获取的工具会被转换为以下格式：")

# 示例MCP工具格式
mcp_search_tool = {
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
            },
            "start_crawl_date": {
                "type": "string",
                "description": "Start date for crawling (ISO format)"
            }
        },
        "required": ["query"]
    },
    "tool_type": "mcp",
    "server_name": "exa_search", 
    "server_config": McpServerConfig(
        transport="streamable_http", 
        url="https://exa-mcp-server.glitch.me/"
    )
}

# 移除server_config对象以便JSON序列化显示
display_tool = mcp_search_tool.copy()
display_tool["server_config"] = {
    "transport": "streamable_http",
    "url": "https://exa-mcp-server.glitch.me/"
}

print(json.dumps(display_tool, ensure_ascii=False, indent=2))

# ============= 3. MCP工具在MCPClient中的格式 =============
print("\n\n📋 3. MCPClient中的工具管理格式")
print("-" * 50)

print("MCPClient.servers_config 格式：")
servers_config_example = {
    "exa": {
        "transport": "streamable_http",
        "url": "https://exa-mcp-server.glitch.me/"
    },
    "duckduckgo": {
        "transport": "streamable_http",
        "url": "https://duckduckgo-mcp.glitch.me/"
    },
    "smithery": {
        "transport": "streamable_http", 
        "url": "https://smithery-mcp-server.glitch.me/profiles/123"
    }
}

print(json.dumps(servers_config_example, ensure_ascii=False, indent=2))

# ============= 4. MCP工具选择格式 =============
print("\n\n🎯 4. AI选择MCP工具的JSON格式")
print("-" * 50)

print("当AI选择MCP工具时，返回的格式：")
mcp_selection = {
    "selected_tools": [
        {
            "tool_name": "search",
            "arguments": {
                "query": "AutoAgents Python SDK",
                "num_results": 5
            },
            "reason": "用户需要搜索AutoAgents相关信息"
        },
        {
            "tool_name": "get_profile",
            "arguments": {
                "profile_id": "123"
            },
            "reason": "获取用户的profile信息"
        }
    ]
}

print(json.dumps(mcp_selection, ensure_ascii=False, indent=2))

# ============= 5. MCP工具执行流程 =============
print("\n\n🔄 5. MCP工具执行流程")
print("-" * 50)

mcp_workflow = """
1. 工具选择阶段
   ├─ ToolManager.select_tools() 调用ChatClient
   ├─ AI返回包含MCP工具的JSON选择
   └─ 解析得到: {"tool_name": "search", "arguments": {...}}

2. 工具执行阶段 - ToolManager.execute_tools()
   ├─ 识别tool_type为'mcp'
   ├─ 调用 _call_mcp_tool(tool_name, tool_config, arguments)
   └─ 执行MCP调用流程:
       
3. MCP调用详细流程 - _call_mcp_tool()
   ├─ 获取server_config from tool_config
   ├─ 检查transport类型
   ├─ 如果是"streamable_http":
   │   ├─ 导入: from mcp.client.streamable_http import streamable_http_client
   │   ├─ 连接: async with streamable_http_client(server_config.url)
   │   ├─ 会话: async with mcp.ClientSession(read_stream, write_stream)
   │   ├─ 初始化: await session.initialize()
   │   └─ 调用工具: await session.call_tool(tool_name, arguments)
   └─ 如果是"stdio": 抛出NotImplementedError

4. 返回结果格式
   └─ 标准化的工具执行结果字典
"""

print(mcp_workflow)

# ============= 6. MCP工具执行结果格式 =============
print("\n\n📊 6. MCP工具执行结果格式")
print("-" * 50)

print("🔹 MCP工具执行成功的结果：")
mcp_success_result = {
    "tool": "search",
    "tool_type": "mcp", 
    "reason": "用户需要搜索AutoAgents相关信息",
    "arguments": {
        "query": "AutoAgents Python SDK",
        "num_results": 5
    },
    "result": {
        "results": [
            {
                "title": "AutoAgents Python SDK Documentation", 
                "url": "https://github.com/autoagents/python-sdk",
                "snippet": "Official Python SDK for AutoAgents platform..."
            },
            {
                "title": "AutoAgents API Reference",
                "url": "https://docs.autoagents.ai/api",
                "snippet": "Complete API documentation for AutoAgents..."
            }
        ]
    },
    "status": "success"
}

print(json.dumps(mcp_success_result, ensure_ascii=False, indent=2))

print("\n🔹 MCP工具执行失败的结果：")
mcp_error_result = {
    "tool": "search",
    "tool_type": "mcp",
    "error": "MCP服务器连接超时",
    "status": "error"
}

print(json.dumps(mcp_error_result, ensure_ascii=False, indent=2))

# ============= 7. MCP工具的控制台输出 =============
print("\n\n📺 7. MCP工具的控制台输出格式")
print("-" * 50)

mcp_console_output = """
🎯 AI选择了 1 个工具:
   1. search
      理由: 用户需要搜索AutoAgents相关信息
      参数: {'query': 'AutoAgents Python SDK', 'num_results': 5}

✅ 工具执行成功: search
   工具类型: mcp
   调用参数: {'query': 'AutoAgents Python SDK', 'num_results': 5}
   执行结果: {'results': [{'title': 'AutoAgents Python SDK...', 'url': '...'}]}

🤖 基于工具结果生成最终回答...
"""

print("MCP工具执行时的控制台输出：")
print(mcp_console_output)

# ============= 8. 常见的MCP工具类型 =============
print("\n\n🔧 8. 常见的MCP工具类型")
print("-" * 50)

common_mcp_tools = {
    "搜索类": {
        "exa_search": "网页搜索和内容检索",
        "duckduckgo_search": "DuckDuckGo搜索引擎",
        "tavily_search": "AI优化的搜索工具"
    },
    "数据处理": {
        "sqlite": "SQLite数据库操作",
        "postgres": "PostgreSQL数据库连接",
        "filesystem": "文件系统访问"
    },
    "API集成": {
        "github": "GitHub仓库和问题管理",
        "slack": "Slack消息和频道操作", 
        "google_drive": "Google Drive文件操作"
    },
    "开发工具": {
        "brave_search": "Brave搜索API",
        "memory": "持久化记忆存储",
        "time": "时间和日期工具"
    }
}

print("按类别分类的常见MCP工具：")
for category, tools in common_mcp_tools.items():
    print(f"\n📂 {category}:")
    for tool_name, description in tools.items():
        print(f"  • {tool_name}: {description}")

# ============= 9. MCP工具集成示例 =============
print("\n\n🔗 9. 完整的MCP工具集成示例")
print("-" * 50)

integration_example = """
# 1. 配置MCP服务器
mcp_client = MCPClient({
    "exa": {
        "transport": "streamable_http", 
        "url": "https://exa-mcp-server.glitch.me/"
    }
})

# 2. 获取MCP工具
mcp_tools = await mcp_client.get_tools()

# 3. 创建React Agent with MCP工具
react_agent = create_react_agent(
    chat_client=chat_client,
    tools=mcp_tools  # MCP工具列表
)

# 4. 执行查询
result = await react_agent.invoke("搜索最新的AI新闻")
"""

print("完整集成示例：")
print("```python")
print(integration_example)
print("```")

print("\n" + "=" * 80)
print("✨ MCP工具格式总结")
print("=" * 80)

mcp_summary = """
📌 MCP工具核心特点：

1. 🌐 网络化：通过HTTP或STDIO与远程服务器通信
2. 🔄 标准化：遵循MCP协议规范，统一的tool schema
3. 🎯 智能化：AI自动选择和调用合适的MCP工具
4. 🛡️ 安全性：连接认证和错误处理机制
5. 🔧 可扩展：支持多种MCP服务器和工具类型
6. 📊 可观测：详细的执行日志和状态反馈

🎯 MCP vs 本地函数的区别：
┌─────────────────┬──────────────────┬──────────────────┐
│     特性        │   本地函数        │    MCP工具       │
├─────────────────┼──────────────────┼──────────────────┤
│ 执行位置        │ 本地Python进程   │ 远程MCP服务器    │
│ 连接方式        │ 直接调用         │ 网络协议通信     │ 
│ 工具定义        │ Python函数       │ MCP工具schema    │
│ 参数传递        │ Python对象       │ JSON格式         │
│ 结果返回        │ Python对象       │ JSON响应         │
│ 错误处理        │ Python异常       │ 网络+协议错误    │
└─────────────────┴──────────────────┴──────────────────┘

🚀 最佳实践：
• 使用连接池管理MCP会话
• 实现超时和重试机制  
• 缓存常用工具的schema信息
• 监控MCP服务器的健康状态
"""

print(mcp_summary) 