import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from src.autoagentsai.client import MCPClient

async def main():
    # 创建MCP客户端配置
    mcp_client = MCPClient({
        "weather": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp"
        },
        "math": {
            "transport": "stdio", 
            "command": "python",
            "args": ["/path/to/math_server.py"]
        },
        # 示例：连接到smithery.ai的搜索服务
        "search": {
            "transport": "streamable_http",
            "url": "https://server.smithery.ai/exa/mcp?api_key=your_api_key&profileId=your_profile_id"
        }
    })
    
    print("正在获取所有MCP服务器的工具...")
    
    try:
        # 获取所有工具
        tools = await mcp_client.get_tools()
        
        print(f"\n总共找到 {len(tools)} 个工具:")
        for tool in tools:
            print(f"  - {tool['name']} (来自服务器: {tool['server_name']})")
            print(f"    描述: {tool['description']}")
        
        # 示例：调用工具（如果有可用的工具）
        if tools:
            print(f"\n尝试调用第一个工具: {tools[0]['name']}")
            # result = await mcp_client.call_tool(
            #     tool_name=tools[0]['name'],
            #     server_name=tools[0]['server_name'], 
            #     arguments={}
            # )
            # print(f"工具调用结果: {result}")
            
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 