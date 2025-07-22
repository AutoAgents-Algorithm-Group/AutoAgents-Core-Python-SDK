import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import asyncio
from src.autoagentsai.prebuilt import create_react_agent
from src.autoagentsai.client import MCPClient

async def main():
    mcp_client = MCPClient(
        {
            "math": {
                "command": "python",
                # Replace with absolute path to your math_server.py file
                "args": ["/path/to/math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # Ensure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    tools = await mcp_client.get_tools()

    agent = create_react_agent(
        model = "anthropic:claude-3-7-sonnet-latest",
        tools = tools
    )

    result = await agent.ainvoke("What is the weather in Tokyo?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())