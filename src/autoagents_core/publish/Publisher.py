import requests
import json
from typing import Dict, Any
from ..client import ChatClient

class Publisher:
    def __init__(self, chat_client: ChatClient):
        self.chat_client = chat_client

    def publish_as_mcp(self, name: str, description: str, transport: str, server_url: str = "https://openmcp.agentspro.cn"):
        self.mcp_server_config = {
            "name": name,
            "description": description,
            "transport": transport
        }
        if transport == "streamable_http":
            return self.publish_as_mcp_via_streamable_http(server_url)
        elif transport == "stdio":
            return self.publish_as_stdio()
        else:
            raise ValueError(f"Invalid transport: {transport}")

    def mcp_as_mcp_via_streamable_http(self, name: str, description: str = None, server_url: str = "https://openmcp.agentspro.cn") -> Dict[str, Any]:
        """
        简化的 MCP streamable_http 发布方法
        
        Args:
            name (str): MCP服务名称
            description (str, optional): MCP服务描述，默认使用name
            server_url (str): MCP服务器地址
            
        Returns:
            Dict[str, Any]: 发布结果
        """
        if description is None:
            description = f"MCP service for {name}"
            
        return self.publish_as_mcp_via_streamable_http_internal(name, description, server_url)

    def publish_as_mcp_via_streamable_http_internal(self, name: str, description: str, server_url: str) -> Dict[str, Any]:
        """
        内部实现：发布Agent为MCP streamable_http服务
        """
        try:
            # 构造发布请求数据
            publish_data = {
                "agent_id": self.chat_client.agent_id,
                "name": name,
                "description": description,
                "transport": "streamable_http",
                "config": {
                    "base_url": self.chat_client.base_url,
                    "agent_id": self.chat_client.agent_id
                }
            }
            
            # 发送发布请求
            headers = {
                "Authorization": f"Bearer {self.chat_client.jwt_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{server_url}/api/mcp/publish",
                json=publish_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message": "MCP服务发布成功",
                    "data": result,
                    "mcp_url": result.get("mcp_url"),
                    "service_id": result.get("service_id")
                }
            else:
                return {
                    "success": False,
                    "message": f"发布失败: {response.status_code}",
                    "error": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "网络请求失败",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": "发布过程中出现错误",
                "error": str(e)
            }

    def publish_as_stdio(self):
        """stdio 模式发布（待实现）"""
        return {
            "success": False,
            "message": "stdio模式暂未实现"
        }
