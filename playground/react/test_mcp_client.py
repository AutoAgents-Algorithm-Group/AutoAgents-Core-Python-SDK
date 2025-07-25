import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from src.autoagentsai.client import MCPClient
import pprint

mcp_servers_config = {
    "exa": {
        "transport": "streamable_http",
        "url": "https://server.smithery.ai/exa/mcp?api_key=5527ddac-6c10-419c-997a-c311a0115831&profileId=unchanged-whitefish-itZWkW"
    },
    "duckduckgo": {
        "transport": "streamable_http",
        "url": "https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp?api_key=5527ddac-6c10-419c-997a-c311a0115831&profileId=unchanged-whitefish-itZWkW"
    }
}

async def main():

    mcp_client = MCPClient(mcp_servers_config)

    try:
        tools = await mcp_client.get_tools()
        print(tools)
        
        # 示例：调用工具（如果有可用的工具）
        if tools:
            result = await mcp_client.call_tool(
                tool_name=tools[0]['name'],
                server_name=tools[0]['server_name'], 
                arguments={
                    "query": "What is the capital of France?"
                }
            )
            pprint.pprint(f"工具调用结果: {result}")
            
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 