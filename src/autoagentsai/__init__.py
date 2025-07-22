from .client.ChatClient import ChatClient
from .types import ChatRequest, ImageInput, ChatHistoryRequest, FileInput
from .utils import extract_json, FileUploader
from .prebuilt import create_react_agent, create_ppt_agent, create_html_agent
from .client.McpClient import MCPClient

__all__ = ["ChatRequest", "ImageInput", "ChatClient", "ChatHistoryRequest", "FileInput", "extract_json", "FileUploader", "create_react_agent", "create_ppt_agent", "create_html_agent", "MCPClient"]


def main() -> None:
    print("Hello from autoagents-python-sdk!")